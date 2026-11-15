"""D1 build: buck_mount.SLDPRT (flat bridge design) plus rail and board stand-ins; STEP, STL, checks. One job."""
import math, sys, json
from pathlib import Path
ROOT = Path(r'J:\code\cad-daddy-wt\sw-eval-sonnet-adv-d')
sys.path.insert(0, str(ROOT / 'solidworks'))
from swkit import *
W = ROOT / '_wip' / 'sw-eval' / 'sonnet-adv-d' / 'd1b'
RUN = ROOT / 'eval' / 'sonnet-adv-d'

# --- numbers and sources (restate.md) ---
BASE_X, BASE_Y, BASE_T = 116.0, 20.0, 4.0          # base on the rail top: 20 wide like the rail
M5_X, M5_D = 52.0, 5.5                             # M5 clearance, two screws, outside the board ends (board ends at 42.5)
BR_X0, BR_X1, BR_Y, BR_Z0, BR_Z1 = 35.0, 43.0, 30.0, 0.0, 8.0     # bridges under the board ends, 8 thick in X
PAD_D, PAD_H, PAD_X, PAD_Y = 7.0, 3.5, 39.0, 26.5  # board holes 3.5 in from the 85 x 60 edges
INS_D, INS_DEPTH = 4.0, 6.0                        # M3 heat-set insert hole
Z_TOP = BR_Z1 + PAD_H                              # board bottom face
BOARD = dict(x=85.0, y=60.0, t=1.6)

def prism(d, name, lo, hi, cut=False, expect_dv=None):
    zc = (lo[2] + hi[2]) / 2
    with Sk(d, plane(d, 'Z', zc, name + '_P'), name) as s:
        s.rect((lo[0], lo[1], zc), (hi[0], hi[1], zc))
    return extrude(d, s.feat, name, hi[2] - lo[2], cut=cut, mode=MID, expect_dv=expect_dv)

def cyls(d, name, pts, dia, z0, z1, cut=False, expect_dv=None):
    zc = (z0 + z1) / 2
    with Sk(d, plane(d, 'Z', zc, name + '_P'), name) as s:
        for x, y in pts:
            s.circle((x, y, zc), dia / 2)
    return extrude(d, s.feat, name, z1 - z0, cut=cut, mode=MID, expect_dv=expect_dv)

with job(wait_s=1800) as j:
    stamp(RUN, 'D1 build job: instance up')
    mount = W / 'buck_mount.SLDPRT'
    d = new_part(j.sw, mount)
    prism(d, 'BASE', (-BASE_X / 2, -BASE_Y / 2, 0), (BASE_X / 2, BASE_Y / 2, BASE_T), expect_dv=BASE_X * BASE_Y * BASE_T)
    save(d)
    ov = 8.0 * BASE_Y * (BASE_T - BR_Z0)            # where the bridge overlaps the base
    br_dv = 8.0 * 2 * BR_Y * (BR_Z1 - BR_Z0) - ov
    prism(d, 'BRIDGE_P', (BR_X0, -BR_Y, BR_Z0), (BR_X1, BR_Y, BR_Z1), expect_dv=br_dv)
    prism(d, 'BRIDGE_N', (-BR_X1, -BR_Y, BR_Z0), (-BR_X0, BR_Y, BR_Z1), expect_dv=br_dv)
    save(d)
    pads = [(sx * PAD_X, sy * PAD_Y) for sx in (1, -1) for sy in (1, -1)]
    cyls(d, 'PADS', pads, PAD_D, BR_Z1, Z_TOP, expect_dv=4 * math.pi * (PAD_D / 2) ** 2 * PAD_H)
    cyls(d, 'INSERT_HOLES', pads, INS_D, Z_TOP - INS_DEPTH, Z_TOP + 0.5, cut=True,
         expect_dv=4 * math.pi * (INS_D / 2) ** 2 * INS_DEPTH)
    cyls(d, 'M5_HOLES', [(M5_X, 0), (-M5_X, 0)], M5_D, -0.1, BASE_T + 0.1, cut=True,
         expect_dv=2 * math.pi * (M5_D / 2) ** 2 * BASE_T)
    save(d)
    # --- checks against the hand values ---
    hand = (BASE_X * BASE_Y * BASE_T + 2 * br_dv + 4 * math.pi * 3.5 ** 2 * PAD_H
            - 4 * math.pi * 2.0 ** 2 * INS_DEPTH - 2 * math.pi * 2.75 ** 2 * BASE_T)
    expect('volume mm3 against hand', volume(d), hand, 0.002)
    expect('bodies', len(bodies(d)), 1, 0)
    b = bbox(d)
    for k, want in enumerate((-58, -30, 0, 58, 30, Z_TOP)):
        expect(f'box[{k}]', b[k], want, 0.01)
    expect('feature errors', len(feature_errors(d)), 0, 0)
    ins = pick(d, kind='cyl', r=2.0)
    m5 = pick(d, kind='cyl', r=2.75)
    expect('insert hole faces', len(ins), 4, 0)
    expect('M5 hole faces', len(m5), 2, 0)
    info = {}
    for nm, fs in (('ins', ins), ('m5', m5)):
        info[nm] = [[round(v, 3) for v in face_info(f)['box']] for f in fs]
    log('hole boxes', info)
    # measured positions: insert-hole centres from their boxes
    for bx in info['ins']:
        cx, cy = (bx[0] + bx[3]) / 2, (bx[1] + bx[4]) / 2
        expect('insert hole centre |x|', abs(cx), PAD_X, 0.01); expect('insert hole centre |y|', abs(cy), PAD_Y, 0.01)
    for bx in info['m5']:
        expect('M5 hole centre |x|', abs((bx[0] + bx[3]) / 2), M5_X, 0.01)
    pt = pick(d, kind='plane', normal=(0, 0, 1), at=(PAD_X + 2.75, PAD_Y, Z_TOP))
    expect('pad top faces found by point', len(pt), 1, 0)
    json.dump(dict(volume_mm3=volume(d), mass_g=volume(d) * 1.19e-3, box=b, bodies=bodies(d)), open(W / 'mount_numbers.json', 'w'))
    for ext in ('step', 'stl'):
        export(j.sw, d, str(W / f'buck_mount.{ext}'))
    sha = __import__('hashlib').sha256(open(mount, 'rb').read()).hexdigest()
    close(j.sw, d)
    # plain rail (no slot) as its own part, then the FEA twin: copy of the mount with the rail inserted as a second body
    dr = new_part(j.sw, W / 'rail_plain.SLDPRT')
    with Sk(dr, plane(dr, 'Z', -10.0, 'RP_P'), 'RAILP') as s:
        s.rect((-80, -10, -10.0), (80, 10, -10.0))
    extrude(dr, s.feat, 'RAILP', 20.0, mode=MID, expect_dv=160 * 20 * 20)
    save(dr); close(j.sw, dr)
    d = open_doc(j.sw, mount)
    save_as(d, W / 'buck_mount_fea.SLDPRT')
    insert_body(d, W / 'rail_plain.SLDPRT')
    expect('bodies in the FEA twin', len(bodies(d)), 2, 0)
    log('FEA twin bodies', bodies(d)); save(d); close(j.sw, d)
    d = open_doc(j.sw, mount)
    expect('original mount volume unchanged after the twin was made', volume(d), hand, 0.002)
    log('mount SHA-256 after build', sha)
    close(j.sw, d)
    stamp(RUN, 'D1 mount built')

    # --- stand-ins: board with its four holes, and the rail with its four T-slots (picture only) ---
    d = new_part(j.sw, W / 'board.SLDPRT')
    zc = Z_TOP + BOARD['t'] / 2
    with Sk(d, plane(d, 'Z', zc, 'BOARD_P'), 'BOARD') as s:
        s.rect((-42.5, -30, zc), (42.5, 30, zc))
    extrude(d, s.feat, 'BOARD', BOARD['t'], mode=MID, expect_dv=85 * 60 * 1.6)
    cyls(d, 'BOARD_HOLES', pads, 3.2, Z_TOP - 0.1, Z_TOP + 1.7, cut=True, expect_dv=4 * math.pi * 1.6 ** 2 * 1.6)
    save(d); export(j.sw, d, str(W / 'board.stl')); close(j.sw, d)
    d = new_part(j.sw, W / 'rail.SLDPRT')
    with Sk(d, plane(d, 'Z', -10.0, 'RAIL_P'), 'RAIL') as s:
        s.rect((-80, -10, -10.0), (80, 10, -10.0))
    extrude(d, s.feat, 'RAIL', 20.0, mode=MID, expect_dv=160 * 20 * 20)
    # the slot on the top face (6 wide, 6 deep) so the picture shows where the T-nuts are
    with Sk(d, plane(d, 'Z', -1.5, 'SLOT_P'), 'SLOT') as s:
        s.rect((-80, -3, -1.5), (80, 3, -1.5))
    extrude(d, s.feat, 'SLOT', 3.0, cut=True, mode=MID, expect_dv=160 * 6 * 3)
    save(d); export(j.sw, d, str(W / 'rail.stl')); close(j.sw, d)
    stamp(RUN, 'D1 build job: done')
print('BUILD DONE')
