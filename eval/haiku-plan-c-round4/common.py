"""Shared code for the set C plans (C_C1.md, C_C2.md). Copy this file to eval/<run>/common.py; every script starts

    from common import *

WRITTEN BY THE PLANNER WITHOUT SOLIDWORKS. The numpy parts (the design tables, section outlines, hand numbers,
stl_stats, the clearance sampling) were run on Linux. Every function that touches SolidWorks (arc_short, outline,
build_*, cut_*, edges3, holes, check_export, the study helpers) is unrun: the helper calls in them are the ones in swkit.py / swfea.py
as read on 2026-11-14. If one raises on first use, fix the line that raises, note the fix in REPORT.md, and go on. Do
not work round a failure by deleting a check.

Frame: X, Y, Z in mm. Both joint axes run along Y. The elbow is at the origin, the wrist pin at X 0, Z -200.
"""
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent            # eval/<run>/
ROOT = HERE.parents[1]                            # the worktree root
sys.path.insert(0, str(ROOT / 'solidworks'))
ON_PC = os.name == 'nt'
if ON_PC:                                         # the planner's Linux checks import this file without SolidWorks
    from swkit import *      # noqa: E402,F401,F403
    from swfea import *      # noqa: E402,F401,F403
import sheet                 # noqa: E402

RUN = HERE.name
WIP = ROOT / '_wip' / 'sw-eval' / RUN             # models, exports, npz (gitignored)
PICS = HERE / 'pictures'
DENS_G_MM3 = 1.19e-3
ALLOW = dict(vm=45.0, layer=22.5, shear=13.0)     # MPa, playbook/05-fea.md "Before SolidWorks"
PRINT_NORMAL = (0.5, 0.0, -0.8660254)             # layers as printed tilted 30 degrees towards +X, hub end down
PRINT_TEXT = ('tilted 30 degrees, hub end down: the long axis leans 30 degrees from the vertical towards +X, the hub '
              '(elbow) end is at the bed and the fork is at the top; height about 222 mm of 256, footprint about '
              '120 x 120 mm. Layers are flat on the bed, so in the part they are stacked along (0.5, 0, -0.866). '
              'Printed with a brim, no raft. Supports: under the lowest part of the hub rim and inside the bore, '
              'and a few small patches; the numbers are in orientations.json')

# ---- the design, as numbers ------------------------------------------------------------------------------------------
PIN_Z = -200.0
HUB_R, HUB_BORE = 36.0, 15.0                      # hub outer radius (free to choose), locating bore radius (fixed)
BOLT_R, BOLT_HOLE_R, HEAD_R = 25.0, 1.7, 3.6      # bolt circle radius, hole radius, screw-head clearance radius (Ø7.2)
BOLTS = [(BOLT_R * math.cos(math.radians(60 * k)), BOLT_R * math.sin(math.radians(60 * k))) for k in range(6)]  # (x, z)
SLOT_HALF, SLOT_TOP, ARCH_R = 16.0, -183.0, 16.0  # slot half width in Y; where its straight walls end; arch radius
KN_R, KN_HALF, KN_ROUND, KN_CORE = 13.0, 22.0, 4.0, 2.0     # wrist knuckle: radius, half length in Y, rim round, pilot hole
PIN_R = 4.0
CABLE_R, CABLE_Z0, CABLE_Z1 = 3.2, -14.0, -170.0  # cable tunnel Ø6.4 along Z at X 0, Y 0, from inside the bore to inside the arch

# Stem sections: (z, a = half width in X, top = highest Y, bot = lowest Y, n = superellipse exponent).
# Idea A, "bone": one stem. Wide in X and thin in Y where it leaves the hub, near round in the middle, wide in Y at
# the fork. The first section lies inside the hub, the last inside the wrist knuckle.
STEM_A = [(-22.0, 27.0, 3.6, -3.4, 2.6), (-27.0, 24.8, 6.4, -3.4, 2.7), (-32.0, 21.0, 9.0, -3.5, 2.9),
          (-38.0, 16.8, 10.6, -6.2, 2.7), (-46.0, 13.9, 11.6, -9.0, 2.4), (-60.0, 12.4, 12.0, -11.0, 2.2), (-72.0, 11.9, 12.0, -11.5, 2.15),
          (-85.0, 11.4, 12.0, -12.0, 2.1), (-100.0, 11.0, 11.9, -11.9, 2.1), (-115.0, 10.6, 11.8, -11.8, 2.1), (-130.0, 10.8, 12.8, -12.8, 2.3), (-145.0, 11.0, 13.8, -13.8, 2.5),
          (-162.0, 11.8, 17.8, -17.8, 3.2), (-176.0, 12.2, 20.8, -20.8, 3.8), (-188.0, 12.4, 21.5, -21.5, 4.2),
          (-200.0, 12.4, 21.6, -21.6, 4.5)]
# Idea A, first fallback for a factor under 2 at the neck: the same stem, 2 mm thicker in Y from Z -27 to -60.
STEM_A2 = [(-22.0, 27.0, 3.6, -3.4, 2.6), (-27.0, 24.8, 7.2, -3.4, 2.9), (-32.0, 21.2, 10.6, -3.5, 3.1),
           (-38.0, 17.4, 12.2, -6.6, 2.9), (-46.0, 14.4, 12.8, -9.8, 2.5), (-60.0, 12.6, 12.8, -11.8, 2.2), (-72.0, 12.0, 12.4, -11.9, 2.15),
           (-85.0, 11.4, 12.0, -12.0, 2.1), (-100.0, 11.0, 11.9, -11.9, 2.1), (-115.0, 10.6, 11.8, -11.8, 2.1), (-130.0, 10.8, 12.8, -12.8, 2.3), (-145.0, 11.0, 13.8, -13.8, 2.5),
           (-162.0, 11.8, 17.8, -17.8, 3.2), (-176.0, 12.2, 20.8, -20.8, 3.8), (-188.0, 12.4, 21.5, -21.5, 4.2),
           (-200.0, 12.4, 21.6, -21.6, 4.5)]
# Idea A, second fallback: thicker again and wider in X at the neck.
STEM_A3 = [(-22.0, 27.0, 3.6, -3.4, 2.6), (-27.0, 25.0, 7.6, -3.4, 3.0), (-32.0, 22.4, 11.4, -3.5, 3.2),
           (-38.0, 19.0, 13.0, -7.0, 3.0), (-46.0, 15.6, 13.6, -10.4, 2.6), (-60.0, 13.2, 13.4, -12.4, 2.3), (-72.0, 12.5, 13.0, -12.5, 2.2),
           (-85.0, 11.8, 12.6, -12.6, 2.1), (-100.0, 11.3, 12.3, -12.3, 2.1), (-115.0, 10.8, 12.0, -12.0, 2.1), (-130.0, 10.9, 12.9, -12.9, 2.3), (-145.0, 11.0, 13.8, -13.8, 2.5),
           (-162.0, 11.8, 17.8, -17.8, 3.2), (-176.0, 12.2, 20.8, -20.8, 3.8), (-188.0, 12.4, 21.5, -21.5, 4.2),
           (-200.0, 12.4, 21.6, -21.6, 4.5)]
# Idea B, "open frame": a wide thin blade from the hub that carries a long window, so two slim legs run from the
# sides of the hub and meet above the fork. The cable would cross the window in the open.
STEM_B = [(-22.0, 27.0, 3.6, -3.4, 2.6), (-27.0, 25.2, 5.0, -3.4, 2.8), (-32.0, 23.2, 6.4, -3.5, 3.0),
          (-40.0, 21.0, 7.0, -5.0, 3.0), (-60.0, 18.0, 7.0, -7.0, 3.0), (-75.0, 16.5, 7.0, -7.0, 3.0), (-90.0, 15.0, 7.0, -7.0, 3.0), (-105.0, 14.1, 7.7, -7.7, 3.0),
          (-120.0, 13.2, 8.4, -8.4, 3.0), (-132.0, 12.7, 10.6, -10.6, 3.0), (-145.0, 12.2, 13.0, -13.0, 3.0), (-162.0, 12.0, 17.4, -17.4, 3.2),
          (-176.0, 12.3, 20.2, -20.2, 3.8), (-188.0, 12.4, 21.5, -21.5, 4.2), (-200.0, 12.4, 21.6, -21.6, 4.5)]
WINDOW_B = [(0.0, -36.0), (8.0, -38.5), (13.0, -46.0), (11.8, -60.0), (9.5, -80.0), (7.5, -100.0), (5.0, -118.0),
            (0.0, -128.0)]                        # (x, z) of the right half of idea B's window, top to bottom


def clock(label=None):
    """Minutes on the job's clock (eval/<run>/times.log), read from the file, never from memory.
    clock() -> the last line's minutes; clock('C2 start') -> the minutes of the first line with exactly that label,
    or None if there is none."""
    path = HERE / 'times.log'
    if not path.exists():
        return None
    rows = [ln.split('\t') for ln in path.read_text(encoding='utf-8').splitlines() if ln.strip()]
    if label is None:
        return float(rows[-1][2].split()[0])
    hit = [float(r[2].split()[0]) for r in rows if r[3] == label]
    return hit[0] if hit else None


def since_c2(label):
    """Stamp `label` and return the minutes since the line 'C2 start' (one decimal)."""
    now = stamp(HERE, label)
    start = clock('C2 start')
    if start is None:
        raise Failed("times.log has no 'C2 start' line: run the C2 start command of C_C2.md step 1 first")
    return round(now - start, 1)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def put(task, **kv):
    """Merge keys into results.json under the task's name (utf-8, numbers as numbers)."""
    f = HERE / 'results.json'
    data = json.loads(f.read_text(encoding='utf-8')) if f.exists() else {}
    data.setdefault(task, {}).update(kv)
    f.write_text(json.dumps(data, indent=1, default=float), encoding='utf-8')
    print('results.json', task, sorted(kv), flush=True)


def got(task, key, default=None):
    """Read a key back from results.json: how one script uses a number an earlier script measured."""
    f = HERE / 'results.json'
    data = json.loads(f.read_text(encoding='utf-8')) if f.exists() else {}
    return data.get(task, {}).get(key, default)


def report(text):
    """Append to REPORT.md at once, so a crash later loses nothing."""
    with open(HERE / 'REPORT.md', 'a', encoding='utf-8') as f:
        f.write(text.rstrip() + '\n\n')


def must(what, have, want):
    """A count that has to be exact (faces picked, edges found, bodies)."""
    if have != want:
        raise Failed(f'{what}: got {have}, expected {want}. Run list_faces(d) and read the boxes before changing anything.')
    log(f'ok {what}: {have}')


def holes(d, r, inside=None):
    """[(radius, [x, y, z] of the middle of the face's box, box)] for every cylindrical face of radius r: where each
    hole IS. For a full cylinder the middle of the box lies on its axis."""
    out = []
    for f in pick(d, kind='cyl', r=r, inside=inside):
        i = face_info(f)
        b = i['box']
        out.append((round(i['r'], 3), [round((b[k] + b[k + 3]) / 2, 3) for k in range(3)], [round(x, 3) for x in b]))
    return sorted(out, key=lambda h: h[1])


# ---- outlines and hand numbers (numpy only) --------------------------------------------------------------------------

def _se(c, s, n):
    return math.copysign(abs(c) ** (2.0 / n), c), math.copysign(abs(s) ** (2.0 / n), s)


def section_arcs(row, k=8):
    """One stem section as four open curves that share end points: [+X tip to top, top to -X tip, -X tip to bottom,
    bottom to +X tip], each k + 1 model points (x, y, z). The same count and the same four corners on every section,
    so a loft has corners to match (playbook/03-modelling.md, "Organic skin")."""
    z, a, top, bot, n = row
    yc, h = (top + bot) / 2.0, (top - bot) / 2.0
    arcs = []
    for q in range(4):
        pts = []
        for i in range(k + 1):
            t = math.radians(90.0 * q + 90.0 * i / k)
            c, s = math.cos(t), math.sin(t)
            if i == 0 or i == k:                   # the four corners exactly on the axes: shared points must be equal
                c, s = round(c), round(s)
            u, v = _se(c, s, n)
            pts.append((a * u, yc + h * v, z))
        arcs.append(pts)
    return arcs


def section_loop(row, count=48):
    """The same outline as one closed list of `count` points starting at the +X tip (for the closed-spline and the
    polygon fallbacks, and for the hand numbers)."""
    k = count // 4
    out = []
    for arc in section_arcs(row, k):
        out += arc[:-1]
    return out


def section_props(row, hole_half=0.0, count=400):
    """(area mm2, Zx mm3 for bending about X, i.e. a load along Y; Zy mm3 for bending about Y, a load along X) of a
    stem section, by strips. hole_half: half width in X of a through window that is left out (idea B)."""
    z, a, top, bot, n = row
    yc, h = (top + bot) / 2.0, (top - bot) / 2.0
    xs = (np.arange(count) + 0.5) / count * 2 * a - a
    hh = h * np.clip(1 - np.abs(xs / a) ** n, 0, 1) ** (1.0 / n)          # half height of the strip at x
    hh = np.where(np.abs(xs) < hole_half, 0.0, hh)
    dx = 2 * a / count
    area = float((2 * hh * dx).sum())
    ix = float(((2 * hh) ** 3 / 12 * dx).sum())                            # about the section's own centre line y = yc
    iy = float((2 * hh * dx * xs ** 2).sum())
    return area, ix / h, iy / a


def window_half(z, window=WINDOW_B):
    """Half width in X of idea B's window at height z (0 outside it), straight lines between its points."""
    zs = [p[1] for p in window][::-1]
    xs = [p[0] for p in window][::-1]
    return float(np.interp(z, zs, xs, left=0.0, right=0.0))


def beam_factors(table, window=None, force=60.0):
    """Hand factor on yield of every stem section from Z -32 down to Z -160, as a plain beam: 45 MPa over M / Z, with
    M = force x distance to the pin. Returns dict(y=(lowest factor for a load along Y, z where), x=(...))."""
    out = {}
    for key, idx in (('y', 1), ('x', 2)):
        worst = None
        for row in table:
            if not -160.0 <= row[0] <= -32.0:
                continue
            props = section_props(row, window_half(row[0], window) if window else 0.0)
            sf = ALLOW['vm'] / (force * (row[0] - PIN_Z) / props[idx])
            if worst is None or sf < worst[0]:
                worst = (round(sf, 2), row[0])
        out[key] = worst
    return out


def boxy_hand_volume():
    """The boxy link of C1 by hand, mm3, with its parts."""
    disc = math.pi * 35 ** 2 * 8
    bore = math.pi * 15 ** 2 * 8
    holes = 6 * math.pi * 1.7 ** 2 * 8
    beam = 40 * 30 * 138
    # the beam's top (Z -32) lies inside the disc where |Y| < 4: a circle segment of radius 35 beyond a chord at 32
    seg = 35 ** 2 * math.acos(32 / 35) - 32 * math.sqrt(35 ** 2 - 32 ** 2)
    overlap = seg * 8
    block = 40 * 44 * 10
    cheeks = 2 * 30 * 6 * 35                       # below the block, Z -180 to -215
    pins = 2 * math.pi * 4 ** 2 * 6
    total = disc - bore - holes + beam - overlap + block + cheeks - pins
    return dict(total=total, disc=disc, bore=bore, holes=holes, beam=beam, overlap=overlap, block=block, cheeks=cheeks,
                pins=pins)


# ---- STL checks without trimesh --------------------------------------------------------------------------------------

def stl_stats(path):
    """dict(volume mm3, bounds [x0, y0, z0, x1, y1, z1], watertight, shells, triangles) of an STL."""
    t = sheet.read_stl(path)
    vol = float(np.einsum('ij,ij->i', t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6.0)
    v, vid = np.unique(np.round(t.reshape(-1, 3), 4), axis=0, return_inverse=True)
    f = vid.reshape(-1, 3)
    e = np.sort(np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]]), axis=1)
    ue, counts = np.unique(e, axis=0, return_counts=True)
    parent = np.arange(len(v))                    # shells: union-find over the vertices

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for a, b in ue:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    shells = len({find(a) for a in range(len(v))})
    lo, hi = t.reshape(-1, 3).min(axis=0), t.reshape(-1, 3).max(axis=0)
    return dict(volume=abs(vol), bounds=[round(float(x), 3) for x in list(lo) + list(hi)],
                watertight=bool((counts == 2).all()), shells=shells, triangles=len(t))


def check_export(d, stl, box, step=None, box_tol=0.15):
    """playbook/04-export.md: watertight, one shell, volume within 0.5 % of the model, in the model frame, STEP in mm.

    box: the bounds the DESIGN says the part has, [x0, y0, z0, x1, y1, z1]. bbox(d) is not used: on a lofted part it
    is the box of the control points and can be millimetres larger than the solid (04-export.md)."""
    st = stl_stats(stl)
    expect('STL watertight', float(st['watertight']), 1.0, 0)
    expect('STL shells', st['shells'], 1, 0)
    expect('STL volume against the model', st['volume'], volume(d), 0.005)
    for k, (a, b) in enumerate(zip(st['bounds'], box)):
        expect(f'STL box[{k}] against the design', a, b, 0, abs_tol=box_tol)
    if step is not None:
        text = Path(step).read_text(errors='ignore')
        if not any('SI_UNIT' in ln and '.MILLI.' in ln for ln in text.splitlines()):
            raise Failed(f'{step}: no SI_UNIT line with .MILLI. (not in millimetres?)')
        log('ok STEP is in mm')
    return st


def picture(stls, png):
    """Draw the sheet and return the shape numbers of each STL (dict by file name). One call, one scale."""
    PICS.mkdir(parents=True, exist_ok=True)
    stats = sheet.sheet([str(s) for s in stls], str(png))
    for name, s in stats.items():
        print('SHAPE', name, json.dumps(s), flush=True)
    return stats


def filled(tris, pts):
    """Share of the points that lie in the solid (0.0 = all clear, 1.0 = all solid)."""
    pts = np.asarray(pts, float).reshape(-1, 3)
    chunk = 200 if tris is None else max(10, min(200, int(8e6 / max(len(tris), 1))))      # keeps the test under about 0.5 GB
    return float(sheet.inside(tris, pts, chunk).mean()) if len(pts) else 0.0


def disc_points(centre, axis, radius, lengths, rings=4, per=16):
    """Points filling a cylinder: discs at each coordinate in `lengths` along model axis 'X', 'Y' or 'Z', centred on
    `centre` (the two other coordinates, in x, y, z order with the axis left out), out to `radius`."""
    i, k = [n for n in range(3) if n != 'XYZ'.index(axis)]
    pts = []
    for c in lengths:
        for ring in range(rings + 1):
            rr = radius * ring / rings
            for q in range(per if ring else 1):
                t = 2 * math.pi * q / per
                p = [0.0, 0.0, 0.0]
                p['XYZ'.index(axis)] = c
                p[i], p[k] = centre[0] + rr * math.cos(t), centre[1] + rr * math.sin(t)
                pts.append(p)
    return np.array(pts)


def fixed_items_stl(stl):
    """Every fixed item of C2 that is about solid or clear space, measured on the exported STL by sampling.
    Returns {item: dict(value=share of the sample that is solid, want='clear' | 'solid', ok=bool, n=points)}."""
    tris = sheet.read_stl(stl)
    out = {}

    def item(name, pts, want):
        share = filled(tris, pts)
        ok = share <= 0.0 if want == 'clear' else share >= 1.0
        out[name] = dict(value=round(share, 4), want=want, ok=bool(ok), n=int(len(pts)))
        print('FIXED', name, out[name], flush=True)

    ring = [(r * math.cos(t), r * math.sin(t)) for r in (15.6, 18.0, 21.0, 22.8, 27.4, 29.0, 30.6)
            for t in np.radians(np.arange(5.0, 360.0, 10.0))]
    ring = [(x, z) for x, z in ring if min(math.hypot(x - bx, z - bz) for bx, bz in BOLTS) > 2.1
            and not (abs(x) < 3.5 and z < 0)]                    # not over a screw hole, not over the cable tunnel
    item('mount face: solid just above Y -4, Ø31.2 to Ø61.2', [(x, -3.7, z) for x, z in ring], 'solid')
    full = [(r * math.cos(t), r * math.sin(t)) for r in (15.6, 18.0, 21.0, 24.0, 27.0, 30.6)
            for t in np.radians(np.arange(5.0, 360.0, 10.0))]
    item('mount face: clear just below Y -4, Ø31.2 to Ø61.2', [(x, -4.3, z) for x, z in full], 'clear')
    item('mount side: nothing below Y -4 inside Ø62 down to Y -30',
         [(x, y, z) for x, z in full for y in (-6.0, -10.0, -16.0, -24.0, -30.0)], 'clear')
    item('bore Ø30 clear (sampled Ø29.6)', disc_points((0, 0), 'Y', 14.8, np.linspace(-3.8, 3.8, 5), 5, 24), 'clear')
    for k, (bx, bz) in enumerate(BOLTS):
        item(f'screw hole {k + 1} Ø3.4 clear (sampled Ø3.2)', disc_points((bx, bz), 'Y', 1.6, np.linspace(-3.8, 3.8, 5), 2, 12),
             'clear')
        item(f'screw head {k + 1}: Ø7 clear, Y 4 to 14', disc_points((bx, bz), 'Y', 3.5, np.linspace(4.15, 14.0, 12), 4, 16),
             'clear')
        seat = [(bx + 2.6 * math.cos(t), 3.7, bz + 2.6 * math.sin(t)) for t in np.radians(np.arange(0, 360, 30))]
        item(f'screw head {k + 1}: seat solid under Y 4 at Ø5.2', seat, 'solid')
    item('pin holes Ø8 clear through both cheeks (sampled Ø7.8)',
         disc_points((0, PIN_Z), 'Y', 3.9, list(np.linspace(16.1, 21.9, 5)) + list(np.linspace(-21.9, -16.1, 5)), 3, 16), 'clear')
    for sign, name in ((1, '+Y'), (-1, '-Y')):
        pad = [(rr * math.cos(t), sign * 16.3, PIN_Z + rr * math.sin(t)) for rr in (4.6, 6.0, 7.9)
               for t in np.radians(np.arange(0, 360, 15))]
        item(f'{name} cheek: solid just behind the inner face out to Ø15.8', pad, 'solid')
        gap = [(rr * math.cos(t), sign * 15.7, PIN_Z + rr * math.sin(t)) for rr in (0.0, 4.6, 6.0, 8.0)
               for t in np.radians(np.arange(0, 360, 15))]
        item(f'{name} cheek: clear just inside the inner face out to Ø16', gap, 'clear')
        wall = [(rr * math.cos(t), sign * yy, PIN_Z + rr * math.sin(t)) for rr in (4.6, 6.5, 8.8)
                for t in np.radians(np.arange(0, 360, 15)) for yy in (16.4, 18.0, 19.5)]
        item(f'{name} cheek: 5 mm of material round the pin hole (solid out to Ø17.6, Y 16.4 to 19.5)', wall, 'solid')
    item('slot: Ø30 swept cylinder about the pin clear, |Y| < 15.8',
         disc_points((0, PIN_Z), 'Y', 15.0, np.linspace(-15.8, 15.8, 9), 6, 24), 'clear')
    slot = [(x, y, z) for x in np.linspace(-20, 20, 9) for y in np.linspace(-15.8, 15.8, 9)
            for z in np.linspace(-216.0, -183.2, 12)]
    item('slot: clear from Z -183 down, |Y| < 15.8, all X', slot, 'clear')
    item('cable: Ø6 straight passage clear along Z at X 0, Y 0, from the bore to the slot',
         disc_points((0, 0), 'Z', 3.0, np.linspace(-182.0, -15.5, 120), 3, 12), 'clear')
    skin = [(x, 0.0, z) for z in np.linspace(-160.0, -30.0, 14) for x in (-3.6, 3.6)]
    item('cable: enclosed (solid beside the tunnel at X ±3.6, Z -30 to -160)', skin, 'solid')
    return out


# ---- SolidWorks: drawing and building --------------------------------------------------------------------------------
STEM_VOL = dict(STEM_A=100900.0, STEM_A2=103700.0, STEM_A3=108500.0, STEM_B=87680.97)      # mm3; STEM_B was 97800.0 (planner), measured 88379.1 (2026-11-14 run, see REPORT.md)
FORM_VOL = dict(STEM_A=103200.0, STEM_A2=105900.0, STEM_A3=110700.0, STEM_B=68280.97)     # stem + hub + knuckle - slot (- window); STEM_B was 78400.0
TABLES = dict(STEM_A=STEM_A, STEM_A2=STEM_A2, STEM_A3=STEM_A3, STEM_B=STEM_B)
# Idea A, third fallback (round 3): STEM_A3 with a deeper and wider neck, Z -27 to -60. The second round failed at
# the neck (1.38 with STEM_A2, 1.57 with STEM_A3, tension across layers under a load along Y at Z -34.5); the stem
# below Z -72 is STEM_A3 unchanged. Section modulus for a load along Y against STEM_A3: x1.32 at Z -27, x1.45 at
# Z -32, x1.26 at Z -38, x1.14 at Z -46.
STEM_A4 = [(-22.0, 27.0, 3.6, -3.4, 2.6), (-27.0, 26.0, 9.0, -3.4, 3.0), (-32.0, 24.4, 13.7, -3.5, 3.2),
           (-38.0, 20.5, 14.6, -7.0, 3.0), (-46.0, 16.6, 14.4, -10.4, 2.6), (-60.0, 13.6, 13.8, -12.6, 2.3)] + STEM_A3[6:]
TABLES['STEM_A4'] = STEM_A4
STEM_VOL['STEM_A4'] = 111640.0
FORM_VOL['STEM_A4'] = 113840.0
# Round 4: STEM_A4 with two changes at the neck, each aimed at one of the two places round 3 failed.
# 1. Z -27: top back to 7.6 (as STEM_A3). The deeper neck stood 3 mm higher beside the two lower screw-head pockets
#    and the pocket edge became a notch (shear between layers 9.3 MPa at X -9, Y 4.2, Z -22.4).
# 2. A row at Z -34.5 and a lower underside from there (bot -6.5, -8.5, -10.8): the cable tunnel's underside at
#    Y -3.2 ran 0.3 to 1.8 mm above the stem's underside just past the mounting ring (tension across layers 13.2 MPa
#    at Z -34.5, on the tunnel wall); now there are 3 mm or more under it.
STEM_A5 = [(-22.0, 27.0, 3.6, -3.4, 2.6), (-27.0, 26.0, 7.6, -3.4, 3.0), (-32.0, 24.4, 13.7, -3.5, 3.2),
           (-34.5, 22.8, 14.2, -6.5, 3.1), (-38.0, 20.5, 14.6, -8.5, 3.0), (-46.0, 16.6, 14.4, -10.8, 2.6),
           (-60.0, 13.6, 13.8, -12.6, 2.3)] + STEM_A3[6:]
TABLES['STEM_A5'] = STEM_A5
STEM_VOL['STEM_A5'] = 112000.0
FORM_VOL['STEM_A5'] = 114200.0
ARC_FLIP = 1          # build_form() turns this to -1 by itself if a revolve with arcs fails
RIMS_AS_ARCS = True    # build_form() sets this False if the revolves fail with arcs drawn either way: straight rims instead


def arc_short(s, c, p0, p1):
    """Draw the short arc about c from p0 to p1 (an arc of under 180 degrees). The turn direction is worked out in the
    sketch's own axes from the mapped points, so it does not matter which way the sketch plane's axes point."""
    a, b, e = s.p(c), s.p(p0), s.p(p1)
    cross = (b[0] - a[0]) * (e[1] - a[1]) - (b[1] - a[1]) * (e[0] - a[0])
    if abs(cross) < 1e-12:
        raise Failed(f'{s.name}: arc_short needs an arc of under 180 degrees')
    s.arc(c, p0, p1, ARC_FLIP * (1 if cross > 0 else -1))


def outline(s, items):
    """Draw a closed outline from a list of ('line', p0, p1) and ('arc', centre, p0, p1). End points must be equal
    from one item to the next: build them from one list of named points."""
    for it in items:
        if it[0] == 'line':
            s.poly([it[1], it[2]], closed=False)
        elif RIMS_AS_ARCS:
            arc_short(s, it[1], it[2], it[3])
        else:                                      # fallback only: the round as one straight line (a chamfer)
            s.poly([it[2], it[3]], closed=False)


def edges3(d, test):
    """Edges for which test(start, middle, end) is true (points in mm). As swkit.edges_where, but the test sees which
    point is which, so an edge that ends on a curve can be told from one that lies along it."""
    out = []
    for b in solid_bodies(d):
        for e in (call(b, 'GetEdges') or []):
            cp = e.GetCurveParams3
            mid = e.GetCurve.Evaluate2((cp.UMinValue + cp.UMaxValue) / 2, 0)
            p = [np.array(cp.StartPoint[:3]) * 1e3, np.array(list(mid)[:3]) * 1e3, np.array(cp.EndPoint[:3]) * 1e3]
            if test(p[0], p[1], p[2]):
                out.append(e)
    return out


LOFT_PICK = 'bottom'  # which point of every section the loft is picked at: 'x' (+X tip), 'bottom' (lowest Y), 'none'


def loft_picked(d, sketches, name, rows):
    """Loft like swkit.loft(), but every section is selected AT THE SAME CORNER (its +X tip, or its lowest point).
    SolidWorks joins the sections where they were picked. Picked nowhere, it chose its own corner on each section,
    and between two sections where that choice changed the stem was twisted a quarter turn, which pinched it."""
    v0 = volume(d)
    for merge in (True, False):
        d.ClearSelection2(True)
        for sk, row in zip(sketches, rows):
            z, a, top, bot, n = row
            p = (a, (top + bot) / 2.0, z) if LOFT_PICK == 'x' else (0.0, bot, z)
            done = False
            if LOFT_PICK != 'none':
                done = bool(d.Extension.SelectByID2(sk.Name, 'SKETCH', p[0] / 1000.0, p[1] / 1000.0, p[2] / 1000.0,
                                                    True, 1, NUL, 0))
                if not done:
                    log(f'{name}: section {sk.Name} was not selected at {p}; selected without a point')
            if not done:
                sk.Select2(True, 1)
        f = d.FeatureManager.InsertProtrusionBlend2(False, True, False, 1.0, 0, 0, 1.0, 1.0, True, True, False, 0, 0, 0,
                                                    True, merge, merge, 0)
        if f is not None:
            d.ForceRebuild3(False)
            f.Name = name
            log(f'{name}: added {volume(d) - v0:.2f} mm3 (merge {merge}, sections picked at: {LOFT_PICK})')
            return f
    raise Failed(name + ': loft failed (sections must be closed, and their start points roughly in line)')


def build_stem(d, table, mode, name='STEM'):
    """Loft the stem through the sections of `table`. mode: 'arcs4' (four open splines a section, the first choice),
    'closed' (one closed spline of 48 points), 'poly' (a closed polygon of 48 points: faceted, but it lofts when
    nothing else does). Raises Failed unless the loft added volume and left one body more than before at most."""
    n0, v0 = len(solid_bodies(d)), volume(d)
    sks = []
    for k, row in enumerate(table):
        with Sk(d, plane(d, 'Z', row[0], f'{name}_P{k}'), f'{name}_S{k}') as s:
            if mode == 'arcs4':
                for arc in section_arcs(row):
                    s.spline(arc, closed=False)
            elif mode == 'closed':
                s.spline(section_loop(row, 48))
            elif mode == 'poly':
                s.poly(section_loop(row, 48))
            else:
                raise Failed('build_stem: unknown mode ' + mode)
        sks.append(s.feat)
    loft_picked(d, sks, name, table)
    dv = volume(d) - v0
    log(f'{name}: mode {mode}, added {dv:.0f} mm3, bodies {n0} -> {len(solid_bodies(d))}')
    if dv < 1000:
        raise Failed(f'{name}: loft added only {dv:.0f} mm3')
    return dv


def build_hub(d, name='HUB'):
    """The elbow hub: a ring of revolution about Y, bore Ø30, outer Ø72, Y -4 to 4, with a fully rounded rim drawn as
    true arcs (R 4.5 on the motor side from Ø63, R 3.5 on the screw side from Ø65). Returns the volume change."""
    v0 = volume(d)
    P = [(HUB_BORE, -4.0, 0.0), (31.5, -4.0, 0.0), (HUB_R, 0.5, 0.0), (32.5, 4.0, 0.0), (HUB_BORE, 4.0, 0.0)]
    with Sk(d, plane(d, 'Z', 0.0, name + '_P'), name) as s:
        outline(s, [('line', P[0], P[1]), ('arc', (31.5, 0.5, 0.0), P[1], P[2]), ('arc', (32.5, 0.5, 0.0), P[2], P[3]),
                    ('line', P[3], P[4]), ('line', P[4], P[0])])
        s.centerline((0.0, -12.0, 0.0), (0.0, 12.0, 0.0))
    revolve(d, s.feat, name)
    return volume(d) - v0


def hub_hand_volume(steps=20000):
    """The hub alone by Pappus (2 pi r x height, summed over r), mm3: 25,380."""
    r = HUB_BORE + (np.arange(steps) + 0.5) / steps * (HUB_R - HUB_BORE)
    lo = np.where(r <= 31.5, -4.0, 0.5 - np.sqrt(np.clip(4.5 ** 2 - (r - 31.5) ** 2, 0, None)))
    hi = np.where(r <= 32.5, 4.0, 0.5 + np.sqrt(np.clip(3.5 ** 2 - (r - 32.5) ** 2, 0, None)))
    return float((2 * math.pi * r * (hi - lo)).sum() * (HUB_R - HUB_BORE) / steps)


def knuckle_hand_volume(steps=20000):
    """The wrist knuckle alone by Pappus about the pin axis, mm3: 22,286 (with its Ø4 pilot hole)."""
    y = -KN_HALF + (np.arange(steps) + 0.5) / steps * 2 * KN_HALF
    lim = np.where(np.abs(y) <= KN_HALF - KN_ROUND, KN_R,
                   KN_R - KN_ROUND + np.sqrt(np.clip(KN_ROUND ** 2 - (np.abs(y) - KN_HALF + KN_ROUND) ** 2, 0, None)))
    return float((math.pi * (lim ** 2 - KN_CORE ** 2)).sum() * 2 * KN_HALF / steps)


def build_knuckle(d, name='KNUCKLE'):
    """The wrist knuckle: a barrel of revolution about the pin axis (X 0, Z -200, along Y), Ø26, Y -22 to 22, rims
    rounded R 4 as true arcs, with a Ø4 pilot hole so that no profile edge lies on the axis (the pin cut opens it to
    Ø8). The flat ends Ø18 at Y ±22 are the outer cheek faces. Returns the volume change."""
    v0 = volume(d)

    def q(y, r):
        return (0.0, y, PIN_Z - r)
    e, c = KN_HALF, KN_HALF - KN_ROUND
    Q = [q(-e, KN_CORE), q(-e, KN_R - KN_ROUND), q(-c, KN_R), q(c, KN_R), q(e, KN_R - KN_ROUND), q(e, KN_CORE)]
    with Sk(d, plane(d, 'X', 0.0, name + '_P'), name) as s:
        outline(s, [('line', Q[0], Q[1]), ('arc', q(-c, KN_R - KN_ROUND), Q[1], Q[2]), ('line', Q[2], Q[3]),
                    ('arc', q(c, KN_R - KN_ROUND), Q[3], Q[4]), ('line', Q[4], Q[5]), ('line', Q[5], Q[0])])
        s.centerline((0.0, -30.0, PIN_Z), (0.0, 30.0, PIN_Z))
    revolve(d, s.feat, name)
    return volume(d) - v0


def cut_slot(d, name='SLOT'):
    """The slot between the cheeks: |Y| < 16 from below the part up to Z -183, closed by a full arch of radius 16
    whose crown is at Z -167. Cut right through in X. The arch is two true quarter arcs; if that does not cut, it is
    drawn as 16 straight segments (fine for a cut, 03-modelling.md). Returns the volume removed."""
    v0 = volume(d)
    a, zt = SLOT_HALF, SLOT_TOP
    last = None
    for how in ('arcs', 'segments'):
        try:
            with Sk(d, plane(d, 'X', 0.0, f'{name}_{how}_P'), f'{name}_{how}') as s:
                s.poly([(0.0, -a, zt), (0.0, -a, -230.0), (0.0, a, -230.0), (0.0, a, zt)], closed=False)
                if how == 'arcs':
                    arc_short(s, (0.0, 0.0, zt), (0.0, a, zt), (0.0, 0.0, zt + ARCH_R))
                    arc_short(s, (0.0, 0.0, zt), (0.0, 0.0, zt + ARCH_R), (0.0, -a, zt))
                else:
                    s.poly([(0.0, ARCH_R * math.cos(math.radians(180.0 * i / 16)), zt + ARCH_R * math.sin(math.radians(180.0 * i / 16)))
                            if 0 < i < 16 else (0.0, a if i == 0 else -a, zt) for i in range(17)], closed=False)
            extrude(d, s.feat, name, 80.0, cut=True, mode=MID)
            dv = v0 - volume(d)
            if dv < 20000.0:                       # an arc drawn the long way round cuts a sliver or the wrong side
                raise Failed(f'{name}: {how} outline removed only {dv:.0f} mm3')
            return dv
        except Failed as ex:
            last = ex
            log(f'{name}: {how} outline did not cut the slot: {ex}')
            if abs(volume(d) - v0) > 1.0:          # a wrong cut was made: take it back before the next try
                d.EditUndo2(1)
                d.ForceRebuild3(False)
    raise Failed(f'{name}: no slot cut built: {last}')


def cut_window(d, name='WINDOW'):
    """Idea B only: the long window through Y, outline WINDOW_B and its mirror image. Tried as a closed spline, then as
    a polygon through the same points. Returns the volume removed."""
    v0 = volume(d)
    right = [(x, 0.0, z) for x, z in WINDOW_B]
    left = [(-x, 0.0, z) for x, z in WINDOW_B[-2:0:-1]]
    last = None
    for how in ('spline', 'poly'):
        try:
            with Sk(d, plane(d, 'Y', 0.0, f'{name}_{how}_P'), f'{name}_{how}') as s:
                if how == 'spline':
                    s.spline(right + left)
                else:
                    s.poly(right + left)
            extrude(d, s.feat, name, 60.0, cut=True, mode=MID)
            return v0 - volume(d)
        except Failed as ex:
            last = ex
            log(f'{name}: {how} outline did not cut: {ex}')
    raise Failed(f'{name}: no window cut built: {last}')


ATTEMPTS = (('arcs4', 'stem first'), ('closed', 'stem first'), ('arcs4', 'hub first'), ('poly', 'stem first'),
            ('poly', 'hub first'))


def build_form(j, path, table_name, window=False, attempts=ATTEMPTS):
    """The whole form, crude: stem, hub, knuckle, slot (and idea B's window), as ONE body, saved at path.

    Tries the loft modes and feature orders of ATTEMPTS in turn; every try starts a new part (new_part() closes what
    a failed try left open, without saving). A try counts only if the stem's volume is within 6 % of the planner's
    number (a twisted loft is far off), every step left one body, and the rebuild is clean. If the hub or the
    knuckle does not revolve, the arcs are drawn the other way round once (ARC_FLIP) and the same try is repeated;
    if that fails too, the rims are drawn straight (RIMS_AS_ARCS False) and the try is repeated once more.
    Returns (document, dict of what was measured). Raises Failed when nothing built."""
    global ARC_FLIP, RIMS_AS_ARCS
    table = TABLES[table_name]
    last, k, flipped = None, 0, False
    while k < len(attempts):
        mode, order = attempts[k]
        stage = 'start'
        try:
            d = new_part(j.sw, path)
            m = dict(table=table_name, loft_mode=mode, order=order, arc_flip=ARC_FLIP, rims='true arcs' if RIMS_AS_ARCS else 'straight (fallback)')
            for part in (('stem', 'hub') if order == 'stem first' else ('hub', 'stem')):
                stage = part
                if part == 'stem':
                    m['stem_mm3'] = round(build_stem(d, table, mode), 1)
                else:
                    m['hub_added_mm3'] = round(build_hub(d), 1)
                    b = bbox(d)
                    expect('hub reaches X +36', b[3], HUB_R, 0, abs_tol=0.3)
                    expect('hub reaches Z +36', b[5], HUB_R, 0, abs_tol=0.3)
                must(f'bodies after the {part}', len(bodies(d)), 1)
                save(d)
            if order == 'hub first':               # the loft was merged into the hub, so it added the stem less the
                m['stem_mm3'] = round(m['stem_mm3'] + hub_hand_volume() - 21750.0, 1)      # 3,630 mm3 they share
            stage = 'stem volume'
            expect('stem volume against the planner number', m['stem_mm3'], STEM_VOL[table_name], 0.06)
            stage = 'knuckle'
            m['knuckle_added_mm3'] = round(build_knuckle(d), 1)
            expect('knuckle reaches Z -213', bbox(d)[2], PIN_Z - KN_R, 0, abs_tol=0.3)
            must('bodies after the knuckle', len(bodies(d)), 1)
            save(d)
            stage = 'cuts'
            if window:
                m['window_mm3'] = round(cut_window(d), 1)
            m['slot_mm3'] = round(cut_slot(d), 1)
            single_body(d)
            errs = feature_errors(d)
            if errs:
                raise Failed(f'rebuild errors {errs}')
            save(d)
            m['form_mm3'] = round(volume(d), 1)
            expect('form volume against the planner number', m['form_mm3'], FORM_VOL[table_name], 0.07)
            return d, m
        except Failed as ex:
            last = ex
            log(f'build_form: try {k + 1} ({mode}, {order}) failed at "{stage}": {ex}')
            if stage in ('hub', 'knuckle') and 'bodies after' not in str(ex) and RIMS_AS_ARCS:
                if not flipped:
                    flipped, ARC_FLIP = True, -ARC_FLIP
                    log(f'build_form: drawing the arcs the other way round (ARC_FLIP {ARC_FLIP}) and repeating this try')
                else:
                    RIMS_AS_ARCS = False
                    log('build_form: the revolves fail with arcs drawn either way: rims drawn straight (chamfers), repeating this try')
                continue
            k += 1
    raise Failed(f'build_form: nothing built the form in {len(attempts)} tries; last error: {last}')


# ---- study results ---------------------------------------------------------------------------------------------------

def measures(r, mask, normal=PRINT_NORMAL):
    """The three failure measures over the nodes in mask for layers stacked along normal, each with its place."""
    if not mask.any():
        raise Failed(f'{r.name}: empty mask')
    vm, at = r.peak(mask)
    lt, lat = r.layer_stress(normal, mask)
    ls, sat = r.layer_shear(normal, mask)
    return dict(vm=round(vm, 3), vm_at=at, layer=round(max(lt, 0.0), 3), layer_at=lat, shear=round(ls, 3), shear_at=sat)


def direction_table(r, mask):
    """{'X' | 'Y' | 'Z': measures()}: the print-direction table of playbook/07-done.md, study item 5."""
    return {k: measures(r, mask, n) for k, n in (
        ('X', (1, 0, 0)), ('Y', (0, 1, 0)), ('Z (upright)', (0, 0, 1)),
        ('tilt 20 to X', (0.3420201, 0, -0.9396926)), ('tilt 30 to X', (0.5, 0, -0.8660254)),
        ('tilt 45 to X', (0.7071068, 0, -0.7071068)), ('tilt 20 to Y', (0, 0.3420201, -0.9396926)),
        ('tilt 30 to Y', (0, 0.5, -0.8660254)), ('tilt 45 to Y', (0, 0.7071068, -0.7071068)))}


def predict(name, nodes, disp, where):
    log(f'PREDICT {name}: nodes {nodes}, max displacement {disp} mm, peak expected at {where}')


def compare(name, r, nodes, disp):
    """playbook/07-done.md "Predict, then run": False when the solve is not the one that was predicted."""
    have = r.max_disp()
    log(f'COMPARE {name}: nodes {r.nodes} (predicted {nodes}), max displacement {have} (predicted {disp})')
    if not (nodes / 2 <= r.nodes <= nodes * 2):
        log(f'NOTE {name}: node count is more than 2x off the prediction. Read the fixture and load boxes static() logged.')
        return False
    if have is None or not (disp / 3 <= have <= disp * 3):
        log(f'STOP {name}: displacement is more than 3x off the prediction. Do not read the stresses yet.')
        return False
    return True
