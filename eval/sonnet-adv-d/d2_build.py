"""D2 build: housing_upper / housing_lower / ring (the design, with the 0.15 mm split relief on each half), and the FEA twin
(split faces closed, ring 51.9 so it can sit in the seat, four soft pads in recesses, four steel screws) as pair_fe.SLDPRT.
One job. Numbers: restate in d2_spec.py and REPORT.md."""
import math, sys, json
from pathlib import Path
ROOT = Path(r'J:\code\cad-daddy-wt\sw-eval-sonnet-adv-d'); sys.path.insert(0, str(ROOT / 'solidworks'))
from swkit import *
W = ROOT / '_wip' / 'sw-eval' / 'sonnet-adv-d' / 'd2'; RUN = ROOT / 'eval' / 'sonnet-adv-d'
X_HALF, Y_HALF, Z0, Z1 = 36.0, 32.0, -4.0, 11.0
R_OPEN, R_SEAT, SEAT_Z1 = 23.0, 26.0, 7.3          # opening dia 46 built (spec 43.5), seat dia 52, seat width 7.3 (spec 7.0)
SCREW_X, SCREW_Z = 31.0, (0.0, 7.0)                 # spec 28.2 and (1, 6)
INS_D, INS_DEPTH, CLR_D, CB_D, CB_DEPTH = 4.0, 7.0, 3.4, 6.0, 3.5
M4_X, M4_Z, M4_D, M4_DEPTH = 24.0, 3.5, 5.6, 8.0
RELIEF = 0.15                                       # each half's split face stands back 0.15 mm: closed gap 0.30 mm
PADS = [(17.68, 17.68), (-17.68, 17.68), (-17.68, -17.68), (17.68, -17.68)]    # r 25 at 45, 135, 225, 315 degrees
SCREWS = [(sx * SCREW_X, z) for sx in (1, -1) for z in SCREW_Z]

def seg(r, h):          # area of a disc of radius r on the far side of a chord h from the centre
    return r * r * math.acos(h / r) - h * math.sqrt(r * r - h * h)

def prism(d, name, lo, hi, cut=False, expect_dv=None):
    zc = (lo[2] + hi[2]) / 2
    with Sk(d, plane(d, 'Z', zc, name + '_P'), name) as s:
        s.rect((lo[0], lo[1], zc), (hi[0], hi[1], zc))
    return extrude(d, s.feat, name, hi[2] - lo[2], cut=cut, mode=MID, expect_dv=expect_dv)

def zcyl(d, name, pts, dia, z0, z1, cut=False, expect_dv=None, inner=None):
    zc = (z0 + z1) / 2
    with Sk(d, plane(d, 'Z', zc, name + '_P'), name) as s:
        for x, y in pts:
            s.circle((x, y, zc), dia / 2)
            if inner:
                s.circle((x, y, zc), inner / 2)
    return extrude(d, s.feat, name, z1 - z0, cut=cut, mode=MID, expect_dv=expect_dv)

def ycyl(d, name, pts, dia, y0, y1, cut=False, expect_dv=None):
    yc = (y0 + y1) / 2
    with Sk(d, plane(d, 'Y', yc, name + '_P'), name) as s:
        for x, z in pts:
            s.circle((x, yc, z), dia / 2)
    return extrude(d, s.feat, name, y1 - y0, cut=cut, mode=MID, expect_dv=expect_dv)

def half(j, upper, relief, fe, tag):
    nm = ('housing_upper' if upper else 'housing_lower') + ('_fe' if fe else '')
    path = W / f'{nm}.SLDPRT'
    d = new_part(j.sw, path)
    y0, y1 = (relief, Y_HALF) if upper else (-Y_HALF, -relief)
    hgt = Z1 - Z0
    prism(d, 'BLOCK', (-X_HALF, y0, Z0), (X_HALF, y1, Z1), expect_dv=2 * X_HALF * (y1 - y0) * hgt)
    zcyl(d, 'OPENING', [(0, 0)], 2 * R_OPEN, Z0 - 0.5, Z1 + 0.5, cut=True, expect_dv=seg(R_OPEN, relief) * hgt)
    zcyl(d, 'SEAT', [(0, 0)], 2 * R_SEAT, 0.0, SEAT_Z1, cut=True, expect_dv=(seg(R_SEAT, relief) - seg(R_OPEN, relief)) * SEAT_Z1)
    pts = [(x, z) for x, z in SCREWS]
    if upper:
        ycyl(d, 'CLEARANCE_HOLES', pts, CLR_D, y0 - 0.5, Y_HALF + 0.5, cut=True, expect_dv=4 * math.pi * (CLR_D / 2) ** 2 * (Y_HALF - y0))
        ycyl(d, 'COUNTERBORES', pts, CB_D, Y_HALF - CB_DEPTH, Y_HALF + 0.5, cut=True,
             expect_dv=4 * math.pi * ((CB_D / 2) ** 2 - (CLR_D / 2) ** 2) * CB_DEPTH)
    else:
        ycyl(d, 'INSERT_HOLES', pts, INS_D, y1 - INS_DEPTH, y1 + 0.5, cut=True, expect_dv=4 * math.pi * (INS_D / 2) ** 2 * INS_DEPTH)
        ycyl(d, 'M4_HOLES', [(M4_X, M4_Z), (-M4_X, M4_Z)], M4_D, -Y_HALF - 0.5, -Y_HALF + M4_DEPTH, cut=True,
             expect_dv=2 * math.pi * (M4_D / 2) ** 2 * M4_DEPTH)
    if fe:     # recess for the soft pads in the lower shoulder (0.85 deep from Z 0), the two nearest this half
        mine = [(px, py) for px, py in PADS if (py > 0) == upper]
        zcyl(d, 'RECESS_' + ('U' if upper else 'L'), mine, 2.4, -0.85, 0.0 + 0.2, cut=True,
             expect_dv=None)
    save(d)
    expect(nm + ' bodies', len(bodies(d)), 1, 0); expect(nm + ' errors', len(feature_errors(d)), 0, 0)
    log(nm, 'volume', round(volume(d), 2), 'box', [round(v, 3) for v in bbox(d)])
    for ext in (('step', 'stl') if not fe else ()):
        export(j.sw, d, str(W / f'{nm}.{ext}'))
    info = dict(volume=volume(d), box=bbox(d))
    close(j.sw, d)
    return info

def ring(j, od, z0, z1, name):
    d = new_part(j.sw, W / f'{name}.SLDPRT')
    zcyl(d, 'RING', [(0, 0)], od, z0, z1, expect_dv=math.pi * ((od / 2) ** 2 - 24.0 ** 2) * (z1 - z0), inner=48.0)
    save(d)
    if name == 'ring':
        export(j.sw, d, str(W / 'ring.stl')); export(j.sw, d, str(W / 'ring.step'))
    info = dict(volume=volume(d), box=bbox(d)); close(j.sw, d); return info

def pad(j, k, px, py):
    d = new_part(j.sw, W / f'pad_{k}.SLDPRT')
    zcyl(d, 'PADBODY', [(px, py)], 1.8, -0.85, 0.15, expect_dv=math.pi * 0.9 ** 2 * 1.0)
    save(d); close(j.sw, d)

def pin(j, k, x, z):
    d = new_part(j.sw, W / f'pin_{k}.SLDPRT')
    ycyl(d, 'PINSHANK', [(x, z)], 3.0, -0.5, 28.5, expect_dv=math.pi * 1.5 ** 2 * 29.0)
    ycyl(d, 'PINHEAD', [(x, z)], 5.8, 28.5, 31.5, expect_dv=math.pi * 2.9 ** 2 * 3.0)
    ycyl(d, 'PINTHREAD', [(x, z)], 4.0, -6.2, -0.5, expect_dv=math.pi * 2.0 ** 2 * 5.7)
    save(d); expect(f'pin_{k} bodies', len(bodies(d)), 1, 0); close(j.sw, d)

res = {}
with job(wait_s=1800) as j:
    stamp(RUN, 'D2 build job: instance up')
    res['upper'] = half(j, True, RELIEF, False, 'design')
    res['lower'] = half(j, False, RELIEF, False, 'design')
    res['ring'] = ring(j, 52.0, 0.0, 7.0, 'ring')
    stamp(RUN, 'D2 design parts built')
    res['upper_fe'] = half(j, True, 0.0, True, 'fe')
    res['lower_fe'] = half(j, False, 0.0, True, 'fe')
    res['ring_fe'] = ring(j, 51.9, 0.15, 7.15, 'ring_fe')
    for k, (px, py) in enumerate(PADS): pad(j, k + 1, px, py)
    for k, (x, z) in enumerate(SCREWS): pin(j, k + 1, x, z)
    d = open_doc(j.sw, W / 'housing_lower_fe.SLDPRT')
    save_as(d, W / 'pair_fe.SLDPRT')
    insert_body(d, W / 'housing_upper_fe.SLDPRT'); insert_body(d, W / 'ring_fe.SLDPRT')
    for k in range(4): insert_body(d, W / f'pad_{k + 1}.SLDPRT')
    for k in range(4): insert_body(d, W / f'pin_{k + 1}.SLDPRT')
    expect('bodies in pair_fe', len(bodies(d)), 11, 0)
    for b in bodies(d): log('body', b)
    expect('rebuild errors', len(feature_errors(d)), 0, 0)
    save(d); close(j.sw, d)
    stamp(RUN, 'D2 build job: done')
json.dump(res, open(W / 'd2_build_numbers.json', 'w'), indent=1)
print('D2 BUILD DONE')
