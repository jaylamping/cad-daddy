"""D1 checks on the exported files: STL watertight/volume/box, STEP units, driver and board-exit paths with sheet.inside()."""
import json, sys
from pathlib import Path
import numpy as np, trimesh
ROOT = Path(r'J:\code\cad-daddy-wt\sw-eval-sonnet-adv-d')
sys.path.insert(0, str(ROOT / 'solidworks'))
import sheet
W = ROOT / '_wip' / 'sw-eval' / 'sonnet-adv-d' / 'd1b'
n = json.load(open(W / 'mount_numbers.json'))
m = trimesh.load(W / 'buck_mount.stl')
print('watertight', m.is_watertight, 'shells', len(m.split()), 'volume STL', round(m.volume, 1), 'SW', round(n['volume_mm3'], 1),
      'diff %', round(100 * (m.volume / n['volume_mm3'] - 1), 3))
print('bounds', m.bounds.round(3).tolist(), 'SW box', [round(v, 3) for v in n['box']])
print('STEP unit', [l.strip()[:60] for l in open(W / 'buck_mount.step', errors='ignore') if 'SI_UNIT' in l and 'LENGTH' in l.upper()][:1]
      or [l.strip()[:80] for l in open(W / 'buck_mount.step', errors='ignore') if '.MILLI.' in l][:1])
tris = {k: sheet.read_stl(W / f'{k}.stl') for k in ('buck_mount', 'rail', 'board')}
def column(cx, cy, z0, z1, r, nn=14):
    pts = []
    for z in np.linspace(z0, z1, 18):
        for a in np.linspace(0, 2 * np.pi, nn, endpoint=False):
            for rr in (0, r / 2, r):
                pts.append((cx + rr * np.cos(a), cy + rr * np.sin(a), z))
    return np.array(pts)
allsolid = np.concatenate([tris['buck_mount'], tris['rail']])
res = {}
def hit(name, pts, tr):
    ins = sheet.inside(tr, pts)
    res[name] = int(ins.sum()); print(f'{name}: {int(ins.sum())} of {len(pts)} points inside solid')
# M3 board screws: hex key 2.5 (use a 6 mm radius column for the key and a hand), from 45 down to the screw head top (board top 13.1 + head 3 = 16.1)
for (x, y) in [(39, 26.5), (39, -26.5), (-39, 26.5), (-39, -26.5)]:
    hit(f'M3 key column at ({x},{y}) Z 17..45 (mount, rail)', column(x, y, 17, 45, 3.0), allsolid)
# M5 rail screws: head on the base (Z 4 .. 6.75); key (3 mm hex) column from 7 to 45, radius 3 plus 5 mm for a wrist: check radius 6
for x in (52, -52):
    hit(f'M5 key column at ({x},0) Z 7..45 r 6 (mount, rail)', column(x, 0, 7, 45, 6.0), allsolid)
# the board's own volume as a box for the part envelope: points inside X +-42.5, Y +-30, Z 11.5..27.1 never overlap an M5 column (|x| 52 - 6 = 46 > 42.5)
print('M5 column nearest X to the board parts box: ', 52 - 6 - 42.5, 'mm clear')
# board lift-out: board plus parts block moves straight up from the pads
lift = np.array([(x, y, z) for x in np.linspace(-42.5, 42.5, 18) for y in np.linspace(-30, 30, 13) for z in np.linspace(11.6, 60, 14)])
hit('board + parts block lifting straight up, Z 11.6..60 (mount)', lift, tris['buck_mount'])
# under-parts zone (3 mm below the board, Z 8.5..11.5): only the four pads may be there
zone = np.array([(x, y, z) for x in np.linspace(-42.5, 42.5, 30) for y in np.linspace(-30, 30, 22) for z in np.linspace(8.5, 11.4, 5)])
ins = sheet.inside(tris['buck_mount'], zone)
near_pad = np.zeros(len(zone), bool)
for px in (39, -39):
    for py in (26.5, -26.5):
        near_pad |= np.hypot(zone[:, 0] - px, zone[:, 1] - py) < 3.6
print('under-parts zone points inside the mount:', int(ins.sum()), ' of which on the four pads:', int((ins & near_pad).sum()), ' elsewhere:', int((ins & ~near_pad).sum()))
res['under_zone_elsewhere'] = int((ins & ~near_pad).sum())
# wire exit: wires leave the +X edge: region X 42.6..80, Y -30..30, Z 11.5..40 must be clear of the mount (it is: base top is Z 4) except nothing
wire = np.array([(x, y, z) for x in np.linspace(42.6, 80, 16) for y in np.linspace(-30, 30, 13) for z in np.linspace(11.5, 40, 8)])
hit('wire exit region +X of the board, Z 11.5..40 (mount)', wire, tris['buck_mount'])
# M5 screw heads vs wire path: the +X M5 head (X 47.25..56.75) lies under the wire exit region; record it
res['m5_head_under_wire_path'] = True
json.dump(res, open(ROOT / 'eval' / 'sonnet-adv-d' / 'd1b_checks_results.json', 'w'), indent=1)
