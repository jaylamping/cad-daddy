"""D3: check the twelve plates of each D run against the task table, from measured.json.

For each plate: outside diameter, thickness, bore, every hole and counterbore (count, diameter, circle, first angle,
depth), counterbore floor height, chamfer, volume against an independent hand value for what was BUILT, and the
thinnest wall between features and to the outside, from the measured cylinders.
"""
import json, math
from pathlib import Path
m = json.loads((Path(__file__).parent / 'measured.json').read_text())
# plate: OD, T, bore, (nA, dA, pcdA), (nB, dB, pcdB, cbD, cbDepth)
TABLE = {'P1': (70, 6, 30, (6, 3.4, 50), (4, 4.5, 60, 8, 3)), 'P2': (84, 6, 40, (6, 4.5, 62), (6, 4.5, 62, 8, 3)),
         'P3': (96, 8, 52, (8, 3.4, 66), (4, 5.5, 84, 10, 4)), 'P4': (60, 5, 28, (4, 3.4, 40), (6, 4.5, 58, 8, 4.6)),
         'P5': (120, 8, 60, (12, 4.5, 80), (6, 6.6, 104, 11, 5)), 'P6': (76, 6, 34, (6, 3.4, 46), (3, 4.5, 64, 8, 3))}
PI = math.pi


def plate(key, name, part_b):
    v = m[key]
    od, t, bore, A, B = TABLE[name]
    T = v['bbox'][5]
    cyl = [f for f in v['faces'] if f['kind'] == 'cyl']
    cones = [f for f in v['faces'] if f['kind'] == 'cone']
    onaxis = sorted({round(f['r'], 3) for f in cyl if abs(f['origin'][0]) < 1e-3 and abs(f['origin'][1]) < 1e-3})
    holes = [f for f in cyl if math.hypot(f['origin'][0], f['origin'][1]) > 1e-3]
    grp = {}
    for f in holes:
        x, y = f['origin'][0], f['origin'][1]
        grp.setdefault((round(f['r'], 3), round(math.hypot(x, y), 2), round(f['box'][2], 3), round(f['box'][5], 3)), []).append(
            round(math.degrees(math.atan2(y, x)) % 360, 1))
    rows = []
    for (r, R, z0, z1), angs in sorted(grp.items()):
        angs = sorted(angs)
        step = 360 / len(angs)
        even = all(abs((a - angs[0]) - i * step) < 0.2 for i, a in enumerate(angs))
        rows.append(f'{len(angs)} x D{2*r:g} on D{2*R:g} first {angs[0]:g} deg{"" if even else " UNEVEN " + str(angs)} Z {z0:g}..{z1:g}')
    # independent hand volume of what was built
    R_od = max(onaxis); r_bore = min(onaxis)
    vol = PI * (R_od ** 2 - r_bore ** 2) * T
    for (r, R, z0, z1), angs in grp.items():
        vol -= len(angs) * PI * r ** 2 * (z1 - z0)        # each cylinder face is the full hole over its own Z range
    ch = None
    if cones:
        zc = [c['box'][2] for c in cones] + [c['box'][5] for c in cones]
        ch = round(max(zc) - min(zc), 3)
        vol -= PI * ch * ch * (R_od - ch / 3)
    # walls
    circ = [(r, f['origin'][0], f['origin'][1], f['box'][2], f['box'][5]) for f in holes for r in [f['r']]]
    walls = []
    for i, a in enumerate(circ):
        walls.append((R_od - math.hypot(a[1], a[2]) - a[0] - (ch if ch and a[4] > T - ch - 1e-6 else 0), 'hole to outside' + (' (below chamfer)' if ch and a[4] > T - ch - 1e-6 else '')))
        walls.append((math.hypot(a[1], a[2]) - a[0] - r_bore, 'hole to bore'))
        for b in circ[i + 1:]:
            if math.hypot(a[1] - b[1], a[2] - b[2]) < 1e-3:
                continue
            if min(a[4], b[4]) - max(a[3], b[3]) > 1e-6:                     # overlap in Z
                walls.append((math.hypot(a[1] - b[1], a[2] - b[2]) - a[0] - b[0], 'hole to hole'))
    floor = sorted({z0 for (r, R, z0, z1) in grp if z0 > 1e-6})
    w = min(walls)
    as_table = []
    if abs(2 * R_od - od) > 1e-3: as_table.append(f'OD {2*R_od:g} (table {od})')
    if abs(2 * r_bore - bore) > 1e-3: as_table.append(f'bore {2*r_bore:g} (table {bore})')
    want_T = t + (1.5 if part_b else 0)
    if abs(T - want_T) > 1e-3: as_table.append(f'T {T:g} (want {want_T:g})')
    print(f'{key:28s} OD {2*R_od:g} T {T:g} bore {2*r_bore:g} vol {v["volume"]:.2f} hand {vol:.2f} diff {v["volume"]-vol:+.2f} '
          f'floor Z {floor} chamfer {ch} min wall {w[0]:.2f} ({w[1]}) {"; ".join(as_table)}')
    for r in rows:
        print('      ', r)


for run, sub in (('haiku-d', 'd3/'), ('haiku-plan-d', '')):
    for b in ('', '_b'):
        for n in TABLE:
            plate(f'{run}/{sub}{n}{b}.SLDPRT', n, bool(b))
        print()
