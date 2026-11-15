"""Reviewer's checks for the second follow-up round (numpy only, no SolidWorks). Run from eval/haiku-plan-c-round2/.

    python r2_tools.py setup               # results.json for this round: C1 and the choice of idea, nothing measured
    python r2_tools.py twist <part.stl>    # does the stem surface turn about Z between sections? TWIST_CHECK ok | fail
    python r2_tools.py slice <part.stl>    # stem half widths at fixed heights; PINCH_CHECK ok | fail
    python r2_tools.py orient <part.stl>   # print directions compared: height, fit, support area and patches;
                                           # writes orientations.json; PRINT_CHECK ok | fail for the chosen direction

They print numbers only. INSTRUCTIONS.md says what to do with each result.
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'solidworks'))
import sheet  # noqa: E402

CHOSEN = 'tilt 30 to +X, hub end down'
S, C = np.sin, np.cos
DIRS = {                                         # name: the model direction that points away from the bed
    'upright, hub end down': (0, 0, -1), 'upright, fork end down': (0, 0, 1),
    'tilt 20 to +X, hub end down': (S(np.radians(20)), 0, -C(np.radians(20))),
    CHOSEN: (0.5, 0, -0.8660254),
    'tilt 30 to -X, hub end down': (-0.5, 0, -0.8660254),
    'tilt 30 to +Y, hub end down': (0, 0.5, -0.8660254),
    'tilt 30 to -Y, hub end down': (0, -0.5, -0.8660254),
    'tilt 45 to +X, hub end down': (0.7071068, 0, -0.7071068),
    'tilt 30 to +X, fork end down': (0.5, 0, 0.8660254),
    'on its -X edge (follow-up round)': (1, 0, 0), 'flat on its +Y side (first round)': (0, -1, 0),
}
STEM_Z = [-46.0, -60.0, -72.0, -85.0, -100.0, -115.0, -130.0, -145.0]     # section rows of the free stem
# (z, lowest and highest allowed half width in X, lowest and highest allowed top Y), table STEM_A2
LIMITS = [(-66.0, 11.0, 13.2, 11.4, 13.6), (-70.0, 11.0, 13.2, 11.4, 13.6), (-74.0, 11.0, 13.2, 11.4, 13.6),
          (-78.0, 10.8, 13.0, 11.3, 13.4), (-82.0, 10.6, 12.6, 11.2, 13.0), (-94.0, 10.4, 12.0, 11.2, 12.8)]


def setup():
    src = json.loads((HERE.parent / 'haiku-plan-c-followup' / 'results.json').read_text(encoding='utf-8-sig'))
    keep = ('chosen', 'eligible', 'choice_reason', 'ideas_tried', 'mass_before_g', 'mass_before_from')
    c2 = {k: src['C2'][k] for k in keep if k in src['C2']}
    c2.update(table_name='STEM_A2', window=False, checkpoints=[])
    out = HERE / 'results.json'
    if out.exists():
        raise SystemExit('results.json is already here: setup has run before')
    out.write_text(json.dumps(dict(C1=src['C1'], C2=c2), indent=1), encoding='utf-8')
    print('SETUP OK: C1 mass_g', src['C1']['mass_g'], '; C2 table_name STEM_A2; nothing measured carried over')
    return True


def twist(path):
    """Median turn about the Z axis, in degrees, of the STL's own edges inside each stretch between two section rows.
    A sound loft reads under 10; a quarter-turn twist reads 60 to 90."""
    t = sheet.read_stl(path)
    ok = True
    print('  from     to   edges   turn in degrees')
    for z1, z0 in zip(STEM_Z[:-1], STEM_Z[1:]):
        rate = []
        for a, b in ((0, 1), (1, 2), (2, 0)):
            p, q = t[:, a], t[:, b]
            m = ((np.minimum(p[:, 2], q[:, 2]) > z0 + 0.5) & (np.maximum(p[:, 2], q[:, 2]) < z1 - 0.5)
                 & (np.abs(p[:, 2] - q[:, 2]) > 1.0) & (np.hypot(p[:, 0], p[:, 1]) > 6) & (np.hypot(q[:, 0], q[:, 1]) > 6))
            th = np.degrees(np.arctan2(q[m, 1], q[m, 0]) - np.arctan2(p[m, 1], p[m, 0]))
            rate.append(((th + 180) % 360 - 180) / (q[m, 2] - p[m, 2]))
        rate = np.concatenate(rate)
        turn = abs(float(np.median(rate))) * (z1 - z0) if len(rate) else 0.0
        good = turn < 20.0
        ok &= good
        print(f'{z1:6.1f} {z0:6.1f} {len(rate):7d} {turn:8.1f}   {"ok" if good else "TWISTED"}')
    print('TWIST_CHECK', 'ok' if ok else 'fail')
    return ok


def cut(tris, z):
    pts = []
    for a, b in ((0, 1), (1, 2), (2, 0)):
        p, q = tris[:, a], tris[:, b]
        m = (p[:, 2] - z) * (q[:, 2] - z) < 0
        f = (z - p[m, 2]) / (q[m, 2] - p[m, 2])
        pts.append(p[m] + f[:, None] * (q[m] - p[m]))
    return np.concatenate(pts)


def slices(path):
    tris = sheet.read_stl(path)
    ok = True
    print('    z   half width X   top Y   bottom Y   allowed X       allowed top Y   ')
    for z, x0, x1, y0, y1 in LIMITS:
        p = cut(tris, z + 0.01)
        hx, top, bot = float(np.abs(p[:, 0]).max()), float(p[:, 1].max()), float(p[:, 1].min())
        good = x0 <= hx <= x1 and y0 <= top <= y1
        ok &= good
        print(f'{z:6.1f} {hx:10.2f} {top:10.2f} {bot:9.2f}   {x0} to {x1}   {y0} to {y1}   {"ok" if good else "OUTSIDE"}')
    print('PINCH_CHECK', 'ok' if ok else 'fail')
    return ok


def orient(path):
    tris = sheet.read_stl(path)
    P = tris.reshape(-1, 3)
    cr = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    area = np.linalg.norm(cr, axis=1) / 2
    n = cr / np.maximum(2 * area[:, None], 1e-15)
    cen = tris.mean(1)
    _, vid = np.unique(np.round(P, 3), axis=0, return_inverse=True)
    vid = vid.reshape(-1, 3)

    def patches(mask):
        parent = {}

        def find(a):
            while parent.setdefault(a, a) != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a
        idx = np.flatnonzero(mask)
        for i in idx:
            a, b, c = vid[i]
            ra = find(a)
            parent[find(b)] = ra
            parent[find(c)] = ra
        groups = {}
        for i in idx:
            groups.setdefault(find(vid[i, 0]), []).append(i)
        out = []
        for g in groups.values():
            g = np.array(g)
            if area[g].sum() >= 20.0:
                out.append(dict(mm2=round(float(area[g].sum())), at=np.average(cen[g], axis=0, weights=area[g]).round(0).tolist()))
        return sorted(out, key=lambda r: -r['mm2'])

    out = {}
    print(f'{"print direction":36s} height  footprint  fits  support mm2  patches of 20 mm2 or more')
    for name, u in DIRS.items():
        u = np.array(u, float)
        u /= np.linalg.norm(u)
        h = P @ u
        a = np.cross(u, [1, 0, 0]) if abs(u[0]) < 0.9 else np.cross(u, [0, 1, 0])
        a /= np.linalg.norm(a)
        b = np.cross(u, a)
        foot = None
        for tdeg in range(0, 90):                              # the part may be turned on the bed
            tt = np.radians(tdeg)
            x, y = P @ (C(tt) * a + S(tt) * b), P @ (-S(tt) * a + C(tt) * b)
            s = (float(np.ptp(x)), float(np.ptp(y)))
            if foot is None or max(s) < max(foot):
                foot = s
        on_bed = (tris @ u).max(1) - h.min() < 0.3
        over = (n @ u < -np.sin(np.radians(45))) & ~on_bed & (area > 1e-12)
        ps = patches(over)
        row = dict(height_mm=round(float(np.ptp(h)), 1), footprint_mm=[round(v) for v in foot],
                   fits=bool(np.ptp(h) <= 246.0 and max(foot) <= 250.0), support_mm2=round(float(area[over].sum())),
                   patches=ps, bed_contact_mm2=round(float(area[on_bed].sum()), 1))
        out[name] = row
        print(f'{name:36s} {row["height_mm"]:6.1f}  {row["footprint_mm"][0]:4d}x{row["footprint_mm"][1]:<4d} {str(row["fits"]):5s} '
              f'{row["support_mm2"]:8d}     {len(ps)}: ' + ', '.join(f'{p["mm2"]} at {p["at"]}' for p in ps[:5]))
    (HERE / 'orientations.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
    c = out[CHOSEN]
    good = c['fits'] and c['support_mm2'] <= 1200
    print('PRINT_CHECK', 'ok' if good else 'fail', f'({CHOSEN}: height {c["height_mm"]} mm of 246 allowed, support {c["support_mm2"]} mm2 of 1200 allowed)')
    return good


if __name__ == '__main__':
    cmds = dict(twist=twist, slice=slices, orient=orient)
    if len(sys.argv) == 2 and sys.argv[1] == 'setup':
        good = setup()
    elif len(sys.argv) == 3 and sys.argv[1] in cmds:
        good = cmds[sys.argv[1]](sys.argv[2])
    else:
        raise SystemExit(__doc__)
    raise SystemExit(0 if good else 1)
