"""C1: the boxy forearm link. Build, measure, export, picture, results.   python c1_boxy.py

Every number written to results.json comes from this run; the hand values go in the hand_* keys only."""
import math

from common import *

stamp(HERE, 'C1 start')
hv = boxy_hand_volume()                         # disc, bore, holes, beam, overlap, block, cheeks, pins, total
log('hand volume', {k: round(v, 1) for k, v in hv.items()})
MODEL, STL = WIP / 'link_boxy.SLDPRT', WIP / 'link_boxy.stl'

with job(wait_s=1800) as j:
    d = new_part(j.sw, MODEL)
    # 1. elbow disc Ø70, Y -4 to 4
    with Sk(d, plane(d, 'Y', 0.0, 'DISC_P'), 'DISC') as s:
        s.circle((0.0, 0.0, 0.0), 35.0)
    extrude(d, s.feat, 'DISC', 8.0, mode=MID, expect_dv=hv['disc'])
    save(d)
    # 2. beam X -20..20, Y -15..15, Z -32..-170 (its top end lies inside the disc rim: 457.7 mm3 counted once)
    with Sk(d, plane(d, 'Z', -101.0, 'BEAM_P'), 'BEAM') as s:
        s.rect((-20.0, -15.0, -101.0), (20.0, 15.0, -101.0))
    extrude(d, s.feat, 'BEAM', 138.0, mode=MID, expect_dv=hv['beam'] - hv['overlap'])
    save(d)
    # 3. block X -20..20, Y -22..22, Z -170..-180
    with Sk(d, plane(d, 'Z', -175.0, 'BLOCK_P'), 'BLOCK') as s:
        s.rect((-20.0, -22.0, -175.0), (20.0, 22.0, -175.0))
    extrude(d, s.feat, 'BLOCK', 10.0, mode=MID, expect_dv=hv['block'])
    save(d)
    # 4. cheeks X -15..15, Y 16..22 and -22..-16, below the block: Z -180..-215 (Z -170..-180 is the block itself)
    with Sk(d, plane(d, 'Z', -197.5, 'CHEEK_P'), 'CHEEKS') as s:
        s.rect((-15.0, 16.0, -197.5), (15.0, 22.0, -197.5))
        s.rect((-15.0, -22.0, -197.5), (15.0, -16.0, -197.5))
    extrude(d, s.feat, 'CHEEKS', 35.0, mode=MID, expect_dv=hv['cheeks'])
    must('bodies after the cheeks', len(bodies(d)), 1)
    save(d)
    # 5. bore Ø30, six Ø3.4 on Ø50 (first on +X, 60 degrees apart), pin hole Ø8 at X 0, Z -200. Each cut overshoots.
    with Sk(d, plane(d, 'Y', 0.0, 'BORE_P'), 'BORE') as s:
        s.circle((0.0, 0.0, 0.0), 15.0)
    extrude(d, s.feat, 'BORE', 9.0, cut=True, mode=MID, expect_dv=hv['bore'])
    with Sk(d, plane(d, 'Y', 0.0, 'HOLES_P'), 'HOLES') as s:
        for bx, bz in BOLTS:
            s.circle((bx, 0.0, bz), 1.7)
    extrude(d, s.feat, 'HOLES', 9.0, cut=True, mode=MID, expect_dv=hv['holes'])
    with Sk(d, plane(d, 'Y', 0.0, 'PIN_P'), 'PIN') as s:
        s.circle((0.0, 0.0, -200.0), 4.0)
    extrude(d, s.feat, 'PIN', 46.0, cut=True, mode=MID, expect_dv=hv['pins'])
    save(d)

    # 6. the finished solid against the hand values
    single_body(d)
    must('rebuild errors', len(feature_errors(d)), 0)
    vol = volume(d)
    expect('volume against the hand value', vol, hv['total'], 0.001)
    box = bbox(d)
    want_box = [-35.0, -22.0, -215.0, 35.0, 22.0, 35.0]
    for k in range(6):
        expect(f'box[{k}]', box[k], want_box[k], 0, abs_tol=0.01)
    # 7. every specified dimension measured on the solid
    hs = holes(d, 1.7)
    must('Ø3.4 holes', len(hs), 6)
    for h in hs:
        near = min(math.hypot(h[1][0] - bx, h[1][2] - bz) for bx, bz in BOLTS)
        expect(f'hole at {h[1]} against the bolt circle', near, 0.0, 0, abs_tol=0.02)
        expect('hole runs Y -4 to 4', h[2][4] - h[2][1], 8.0, 0, abs_tol=0.02)
    bore = holes(d, 15.0)
    must('Ø30 bore faces', len(bore), 1)
    expect('bore centre X', bore[0][1][0], 0.0, 0, abs_tol=0.02)
    expect('bore centre Z', bore[0][1][2], 0.0, 0, abs_tol=0.02)
    pins = holes(d, 4.0)
    must('Ø8 pin hole faces (one in each cheek)', len(pins), 2)
    for h in pins:
        expect('pin hole X', h[1][0], 0.0, 0, abs_tol=0.02)
        expect('pin hole Z', h[1][2], -200.0, 0, abs_tol=0.02)
        expect('cheek thickness at the pin hole', h[2][4] - h[2][1], 6.0, 0, abs_tol=0.02)
    must('Ø70 rim faces', len(pick(d, kind='cyl', r=35.0)), 1)
    save(d)
    export(j.sw, d, STL)
    st = check_export(d, STL, want_box)
    close(j.sw, d)

shape = picture([STL], PICS / 'c1_boxy.png')['link_boxy.stl']
mass = vol * DENS_G_MM3
put('C1', status='done', volume_mm3=round(vol, 1), hand_volume_mm3=round(hv['total'], 1), mass_g=round(mass, 2),
    hand_mass_g=round(hv['total'] * DENS_G_MM3, 2), bodies=1, shape=shape, box_mm=[round(v, 3) for v in box],
    stl=dict(volume=round(st['volume'], 1), watertight=st['watertight'], shells=st['shells'], triangles=st['triangles']),
    holes_measured=[h[1] for h in hs], pin_holes_measured=[h[1] for h in pins], model_sha256=sha(MODEL))
t = stamp(HERE, 'C1 end')
report(f"""## C1. The link as it is

- Model `_wip/sw-eval/{RUN}/link_boxy.SLDPRT`, one body, rebuild clean. Picture `pictures/c1_boxy.png`.
- Volume {vol:.1f} mm3 against {hv['total']:.1f} mm3 by hand (disc {hv['disc']:.1f} - bore {hv['bore']:.1f} - holes
  {hv['holes']:.1f} + beam {hv['beam']:.0f} - the beam's top inside the disc rim {hv['overlap']:.1f} + block {hv['block']:.0f}
  + cheeks below the block {hv['cheeks']:.0f} - pin holes {hv['pins']:.1f}). Mass {mass:.1f} g at 1.19 g/cm3.
- Box {[round(v, 2) for v in box]} against {want_box}.
- Measured on the solid: six Ø3.4 holes at {[h[1] for h in hs]}, bore at {bore[0][1]}, pin holes at {[h[1] for h in pins]},
  cheeks 6.0 thick at the pin.
- STL: watertight {st['watertight']}, {st['shells']} shell, volume {st['volume']:.1f} mm3, {st['triangles']} triangles.
- Shape numbers: {shape}.
- What I would question in the drawing: the beam's top face (Z -32) is 3 mm inside the disc rim, so beam and disc
  share {hv['overlap']:.0f} mm3; the cheeks are given from Z -170, where the block already is, so 10 mm of each is the
  block. Both are counted once. The beam (40 x 30 solid) carries {hv['beam'] * DENS_G_MM3:.0f} g of the {mass:.0f} g.
- Clock: C1 ended at {t:.1f} min on times.log.
""")
