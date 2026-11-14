"""D3: six adapter plates from one table, one script. Part one builds P1 to P6 from the table; part two edits the saved
parts (open, change, save as _b) for the change request. Run with `part1` or `part2` as the argument.

Plate: disc on Z, Z 0 to t, centre bore. Ring A: through holes. Ring B: through holes with a counterbore from the top.
Angles from +X, the first hole of each ring at its turn angle (0 unless the table row is changed below, with a reason).

Table rows that could not be built as written (each decided before building; see REPORT.md):
  P1  ring A (Ø3.4 on R25, 0 deg) and ring B (counterbore Ø8 on R30, 0 deg) meet on the same ray: centres 5.0 mm apart,
      needed 5.7 (1.7 + 4.0). Ring B turned 45 deg: nearest pair then 8.7 mm centre to centre... see clash check.
  P2  ring A and ring B are the same 6 holes (6 x Ø4.5 on R31, both at 0 deg). Ring B turned 30 deg.
  P3  (part two) ring A on R35 meets the ring B counterbore (R42, Ø10) at 0 deg with 0.3 mm web. Ring A turned 22.5 deg.
  P4  ring B holes and counterbores (R29, Ø4.5 and Ø8) break out of the OD 60 (outer edge 33.0 > 30): OD raised to 68.
      Counterbore 8 x 4.6 in a 5 mm plate leaves a 0.4 mm floor (wall rule 0.6 mm): depth set to 4.0 (floor 1.0).
  Chamfer: P1, P3, P4 have a 1.0 mm wall at the counterbore spots, so a 1.0 mm chamfer leaves no flat: 0.5 mm there.
"""
import json
import math
import sys
from pathlib import Path

WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT / 'solidworks'))
import numpy as np  # noqa: E402
import trimesh  # noqa: E402
from swkit import (MID, Sk, bbox, bodies, close, expect, export, extrude, feature_errors, job, log,  # noqa: E402
                   new_part, open_doc, pick, plane, redraw_circles, save, save_as, set_dim, single_body, volume,
                   edges_where, chamfer, faces)

OUT = WT / '_wip' / 'sw-eval' / 'haiku-d' / 'd3'
EVAL = WT / 'eval' / 'haiku-d'
OUT.mkdir(parents=True, exist_ok=True)
PI = math.pi
PETG_DENSITY = 1.19e-3   # g per mm3

# name: OD, t, bore, ring A (n, dia, circle), ring B (n, dia, circle, cb dia, cb depth), turn A, turn B, chamfer width (mm)
TABLE = {
    'P1': dict(od=70, t=6, bore=30, A=(6, 3.4, 50), B=(4, 4.5, 60, 8, 3), turnA=0, turnB=45, ch=0.5),
    'P2': dict(od=84, t=6, bore=40, A=(6, 4.5, 62), B=(6, 4.5, 62, 8, 3), turnA=0, turnB=30, ch=1.0),
    'P3': dict(od=96, t=8, bore=52, A=(8, 3.4, 66), B=(4, 5.5, 84, 10, 4), turnA=0, turnB=0, ch=0.5),
    'P4': dict(od=68, t=5, bore=28, A=(4, 3.4, 40), B=(6, 4.5, 58, 8, 4.0), turnA=0, turnB=0, ch=0.5),
    'P5': dict(od=120, t=8, bore=60, A=(12, 4.5, 80), B=(6, 6.6, 104, 11, 5), turnA=0, turnB=0, ch=1.0),
    'P6': dict(od=76, t=6, bore=34, A=(6, 3.4, 46), B=(3, 4.5, 64, 8, 3), turnA=0, turnB=0, ch=1.0),
}
# the table as written, for the report (P1, P2, P4 differ from it)
AS_WRITTEN = {
    'P1': dict(od=70, t=6, bore=30, B=(4, 4.5, 60, 8, 3), turnB=0),
    'P2': dict(od=84, t=6, bore=40, B=(6, 4.5, 62, 8, 3), turnB=0),
    'P4': dict(od=60, t=5, bore=28, B=(6, 4.5, 58, 8, 4.6)),
}
# part two: 1.5 mm thicker, counterbore floors kept (measured from the bottom), 1 mm top outside chamfer, P3 ring A on R35
P3_RING_A_B = dict(n=8, dia=3.4, R=35.0, turn=22.5)


def holes(R, n, dia, turn):
    return [(R * math.cos(math.radians(turn + k * 360.0 / n)), R * math.sin(math.radians(turn + k * 360.0 / n)), dia / 2)
            for k in range(n)]


def layout(p, t_add=0.0, cb_add=0.0, ring_a_R=None, ring_a_turn=None):
    nA, dA, RA = p['A']
    nB, dB, RB, cbd, cbz = p['B']
    # the table's "on circle Ø" is a pitch-circle DIAMETER: the hole centres sit at half of it
    RA = ring_a_R if ring_a_R else RA / 2
    turnA = p['turnA'] if ring_a_turn is None else ring_a_turn
    return dict(A=holes(RA, nA, dA, turnA), B=holes(RB / 2, nB, dB, p['turnB']), cbd=cbd, cbz=cbz + cb_add,
                t=p['t'] + t_add, R=p['od'] / 2, r=p['bore'] / 2)


def hand_checks(name, p, lay, ch):
    """Thinnest walls and clashes from the geometry, before any build (mm)."""
    A, B = lay['A'], lay['B']
    cbr = lay['cbd'] / 2
    walls = []
    # hole to hole: centre distance minus radii (ring B counterbores count at their full radius)
    for i, (x1, y1, r1) in enumerate(A):
        for j, (x2, y2, r2) in enumerate(A):
            if j > i:
                walls.append((math.dist((x1, y1), (x2, y2)) - r1 - r2, f'A{i}-A{j}'))
    for i, (xa, ya, ra) in enumerate(A):
        for j, (xb, yb, rb) in enumerate(B):
            walls.append((math.dist((xa, ya), (xb, yb)) - ra - cbr, f'A{i}-cbB{j}'))
    for j, (xb, yb, rb) in enumerate(B):
        for k, (xc, yc, rc) in enumerate(B):
            if k > j:
                walls.append((math.dist((xb, yb), (xc, yc)) - cbr - cbr, f'cbB{j}-cbB{k}'))
    # to the bore and to the outside (counterbore outer edge and A outer edge)
    for i, (x, y, r) in enumerate(A):
        walls.append((math.hypot(x, y) - r - lay['r'], f'A{i}-bore'))
        walls.append((lay['R'] - math.hypot(x, y) - r, f'A{i}-outside'))
    for j, (x, y, r) in enumerate(B):
        walls.append((math.hypot(x, y) - cbr - lay['r'], f'cbB{j}-bore'))
        walls.append((lay['R'] - math.hypot(x, y) - cbr, f'cbB{j}-outside'))
    worst = min(walls)
    floor = lay['t'] - lay['cbz']
    clash = [w for w in walls if w[0] < 0.6]
    return dict(min_wall_mm=round(worst[0], 3), min_wall_at=worst[1], counterbore_floor_from_bottom_mm=round(floor, 3),
                walls_below_0p6=[(round(w, 2), k) for w, k in clash], floor_ok=floor >= 0.6)


def hand_volume(lay, ch_w=0.0):
    t, R, r = lay['t'], lay['R'], lay['r']
    v = PI * (R * R - r * r) * t
    v -= len(lay['A']) * PI * (lay['A'][0][2] ** 2) * t
    v -= len(lay['B']) * PI * (lay['B'][0][2] ** 2) * t
    cbr = lay['cbd'] / 2
    v -= len(lay['B']) * PI * (cbr * cbr - lay['B'][0][2] ** 2) * lay['cbz']
    if ch_w:
        v -= PI * ch_w * ch_w * (R - ch_w / 3)          # 45 degree chamfer round the top outside edge
    return v


def build(j, name, p):
    lay = layout(p)
    chk = hand_checks(name, p, lay, p['ch'])
    log(name, 'hand checks', chk)
    d = new_part(j.sw, OUT / f'{name}.SLDPRT')
    R, r, t = p['od'] / 2, p['bore'] / 2, p['t']
    with Sk(d, plane(d, 'Z', 0.0, f'{name}_BASE_P'), 'BASE_SK') as s:
        s.circle((0, 0, 0), R)
        s.circle((0, 0, 0), r)
    extrude(d, s.feat, 'BASE', t, mode=0, want=(2, 1, 0.0), expect_dv=PI * (R * R - r * r) * t)
    for key, pts in (('HA', lay['A']), ('HB', lay['B'])):
        with Sk(d, plane(d, 'Z', t / 2, f'{name}_{key}_P'), f'{key}') as s:
            for x, y, rr in pts:
                s.circle((x, y, t / 2), rr)
        extrude(d, s.feat, key, 40.0, cut=True, mode=MID,
                expect_dv=len(pts) * PI * pts[0][2] ** 2 * t)
    top = pick(d, kind='plane', normal=(0, 0, 1))
    expect(f'{name} one top face', len(top), 1, 0)
    cbr = lay['cbd'] / 2
    with Sk(d, top[0], 'CB') as s:
        for x, y, rr in lay['B']:
            s.circle((x, y, t), cbr)
    extrude(d, s.feat, 'CB', lay['cbz'], cut=True, mode=0, want=(2, -1, float(t)),
            expect_dv=len(lay['B']) * PI * (cbr ** 2 - lay['B'][0][2] ** 2) * lay['cbz'])
    single_body(d)
    save(d)
    return d, lay, chk


def check_part(j, d, name, lay, ch_w, label):
    v_sw = volume(d)
    v_hand = hand_volume(lay, ch_w)
    dv_pct = 100 * (v_sw - v_hand) / v_hand
    b = bodies(d)
    stl = OUT / f'{label}.stl'
    export(j.sw, d, stl)
    m = trimesh.load(stl)
    watertight = bool(m.is_watertight)
    n_bodies = len(m.split(only_watertight=False))
    row = dict(volume_sw_mm3=round(v_sw, 2), volume_hand_mm3=round(v_hand, 2), volume_diff_pct=round(dv_pct, 3),
               mass_g=round(v_sw * PETG_DENSITY, 2), bodies=len(b), stl_watertight=watertight, stl_bodies=n_bodies,
               stl_volume_mm3=round(float(m.volume), 2), box=[round(x, 3) for x in bbox(d)])
    log(label, row)
    return row


def part1():
    rows = {}
    with job(wait_s=1800) as j:
        for name, p in TABLE.items():
            d, lay, chk = build(j, name, p)
            rows[name] = dict(as_built=p, hand_checks=chk, **check_part(j, d, name, lay, 0.0, name))
            close(j.sw, d)
    (EVAL / 'd3_table1.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    return rows


def part2():
    rows = {}
    with job(wait_s=1800) as j:
        for name, p in TABLE.items():
            d = open_doc(j.sw, OUT / f'{name}.SLDPRT')
            d.ForceRebuild3(False)
            before = [f.Name for f in feature_tree(d)]
            t, t2 = p['t'], p['t'] + 1.5
            cbz0 = p['B'][4]
            set_dim(d, 'BASE', t, t2)
            set_dim(d, 'CB', cbz0, cbz0 + 1.5)
            if name == 'P3':
                pts = [(P3_RING_A_B['R'] * math.cos(math.radians(P3_RING_A_B['turn'] + k * 360 / 8)),
                        P3_RING_A_B['R'] * math.sin(math.radians(P3_RING_A_B['turn'] + k * 360 / 8)), t / 2)
                       for k in range(8)]
                redraw_circles(d, 'HA_SK', pts, 1.7)
            d.ForceRebuild3(False)
            R = p['od'] / 2
            ch = edges_where(d, lambda q, R=R, t2=t2: abs(math.hypot(q[0], q[1]) - R) < 0.01 and abs(q[2] - t2) < 0.01)
            expect(f'{name} top outside edges found', len(ch), 1, 0)
            chamfer(d, ch, p['ch'], 'TOP_CH')
            after = [f.Name for f in feature_tree(d)]
            lay = layout(p, t_add=1.5, cb_add=1.5,
                         ring_a_R=(P3_RING_A_B['R'] if name == 'P3' else None),
                         ring_a_turn=(P3_RING_A_B['turn'] if name == 'P3' else None))
            hv = hand_volume(lay, p['ch'])
            chk2 = hand_checks(name, p, lay, p['ch'])
            v = volume(d)
            expect(f'{name}_b volume against hand', v, hv, 0.005)
            floor_z = t2 - (cbz0 + 1.5)
            hx, hy, hr = lay['B'][0]
            ux, uy = math.cos(math.radians(p['turnB'])), math.sin(math.radians(p['turnB']))
            rc = (lay['cbd'] / 2 + hr) / 2                      # a point in the counterbore floor, between hole and counterbore
            floor_faces = pick(d, kind='plane', normal=(0, 0, 1), at=(hx + rc * ux, hy + rc * uy, floor_z))
            log(name, 'counterbore floor face found at', round(floor_z, 3), len(floor_faces))
            save_as(d, OUT / f'{name}_b.SLDPRT')
            rows[name] = dict(feature_tree_before=before, feature_tree_after=after,
                              **check_part(j, d, name, lay, p['ch'], f'{name}_b'),
                              counterbore_floor_z_mm=round(floor_z, 3), floor_face_found=len(floor_faces) > 0,
                              chamfer_mm=p['ch'], errors=feature_errors(d), hand_checks=chk2)
            close(j.sw, d)
    (EVAL / 'd3_table2.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    return rows


def feature_tree(d):
    out = []
    f = d.FirstFeature
    while f is not None:
        out.append(f)
        f = f.GetNextFeature
    return out


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'part1'
    r = part1() if which == 'part1' else part2()
    print(json.dumps(r, indent=2, default=str))
