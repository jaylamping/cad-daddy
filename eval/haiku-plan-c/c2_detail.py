"""C2, stage 2 (detail): the chosen form built again as link_organic, with every functional feature cut AFTER the
form so that the fixed items hold whatever the form does; then every fixed item measured, exports, checkpoint 2.

    python c2_detail.py            # the table chosen by c2_ideas.py (results.json, C2.table_name)
    python c2_detail.py noblend    # the same without the fillet at the hub (branch "mesh fails at the hub seam")
"""
import math
import sys

from common import *

TRY_BLEND = 'noblend' not in sys.argv
table_name, window = got('C2', 'table_name', 'STEM_A'), bool(got('C2', 'window', False))
stamp(HERE, f'C2 detail start ({table_name})')
MODEL, STL, STEP = WIP / 'link_organic.SLDPRT', WIP / 'link_organic.stl', WIP / 'link_organic.step'
BOX = [-36.0, -22.0, -213.0, 36.0, 22.0, 36.0]      # hub Ø72 about the origin, knuckle Ø26 about Z -200, Y -22 to 22
steps = {}

with job(wait_s=1800) as j:
    d, m = build_form(j, MODEL, table_name, window)
    steps.update(m)

    # 1. soften the seam where the stem's screw-side surface climbs out of the hub's flat face (Y +4). It may not
    #    build: then the seam stays a crease of about 30 degrees, and the report says so.
    blend = None
    if TRY_BLEND:
        v0 = volume(d)
        seam = edges3(d, lambda a, mid, b: abs(mid[1] - 4.0) < 0.02 and abs(a[1] - 4.0) < 0.02 and abs(b[1] - 4.0) < 0.02
                      and mid[2] < -22.2 and 16.0 < math.hypot(mid[0], mid[2]) < 32.3)
        log('seam edges on the hub face Y +4:', len(seam))
        if seam:
            blend = fillet(d, seam, (3.0, 2.0, 1.2), 'RAMP_BLEND')
            dv = volume(d) - v0
            if blend is not None and (feature_errors(d) or len(bodies(d)) != 1 or not 0.0 < dv < 600.0):
                log(f'RAMP_BLEND built but is not sound (volume change {dv:.1f}, errors {feature_errors(d)}): undone')
                d.EditUndo2(1)
                d.ForceRebuild3(False)
                blend = None
                expect('volume back after undoing the blend', volume(d), v0, 0.0005)
        save(d)
    steps['ramp_blend_radius_mm'] = blend
    steps['ramp_blend_edges'] = len(seam) if TRY_BLEND else 0

    # 2. pin holes Ø8 through both cheeks
    v0 = volume(d)
    with Sk(d, plane(d, 'Y', 0.0, 'PIN_P'), 'PIN') as s:
        s.circle((0.0, 0.0, PIN_Z), PIN_R)
    extrude(d, s.feat, 'PIN', 50.0, cut=True, mode=MID)
    steps['pin_mm3'] = round(v0 - volume(d), 1)
    expect('pin holes removed', steps['pin_mm3'], 524.0, 0.06)
    # 3. cable tunnel Ø6.4 along Z at X 0, Y 0, from inside the bore (Z -14) to inside the arch (Z -170)
    v0 = volume(d)
    zc = (CABLE_Z0 + CABLE_Z1) / 2
    with Sk(d, plane(d, 'Z', zc, 'CABLE_P'), 'CABLE') as s:
        s.circle((0.0, 0.0, zc), CABLE_R)
    extrude(d, s.feat, 'CABLE', CABLE_Z0 - CABLE_Z1, cut=True, mode=MID)
    steps['cable_mm3'] = round(v0 - volume(d), 1)
    if not window:
        expect('cable tunnel removed', steps['cable_mm3'], 4900.0, 0.03)
    # 4. six screw holes Ø3.4 on Ø50, cut right through whatever the stem put there
    v0 = volume(d)
    with Sk(d, plane(d, 'Y', 0.0, 'HOLES_P'), 'HOLES') as s:
        for bx, bz in BOLTS:
            s.circle((bx, 0.0, bz), BOLT_HOLE_R)
    extrude(d, s.feat, 'HOLES', 30.0, cut=True, mode=MID)
    steps['holes_mm3'] = round(v0 - volume(d), 1)
    expect('screw holes removed', steps['holes_mm3'], 437.0, 0.03)
    save(d)
    # 5. screw-head clearances Ø7.2 from Y 4 to Y 15: only the two lower ones meet the stem (shallow scallops)
    v0 = volume(d)
    try:
        with Sk(d, plane(d, 'Y', 9.5, 'HEADS_P'), 'HEADS') as s:
            for bx, bz in BOLTS:
                s.circle((bx, 9.5, bz), HEAD_R)
        extrude(d, s.feat, 'HEADS', 11.0, cut=True, mode=MID, min_dv=0.01)
    except Failed as ex:
        log(f'HEADS: nothing to cut in the screw-head clearances ({ex})')
    steps['heads_mm3'] = round(v0 - volume(d), 2)
    expect('screw-head scallops are shallow (mm3)', steps['heads_mm3'], 30.0, 0, abs_tol=60.0)
    # 6. nothing may stand below the mounting plane inside Ø62.4: cut it if it does (expected: nothing there)
    v0 = volume(d)
    try:
        with Sk(d, plane(d, 'Y', -19.5, 'MOUNT_P'), 'MOUNT_CLEAN') as s:
            s.circle((0.0, -19.5, 0.0), 31.2)
        extrude(d, s.feat, 'MOUNT_CLEAN', 31.0, cut=True, mode=MID, min_dv=0.01)
    except Failed as ex:
        log(f'MOUNT_CLEAN: nothing below the mounting plane (good) ({ex})')
    steps['mount_clean_mm3'] = round(v0 - volume(d), 2)
    single_body(d)
    must('rebuild errors', len(feature_errors(d)), 0)
    save(d)
    vol = volume(d)
    if not window:
        expect('finished volume against the planner number', vol, FORM_VOL[table_name] - 5860.0, 0.07)

    # 7. the fixed items measured on the solid's own faces
    meas = {}
    face = pick(d, kind='plane', normal=(0, -1, 0), at=(0.0, -4.0, 20.0))
    must('mounting face (one flat face at Y -4)', len(face), 1)
    fi = face_info(face[0])
    ring_area = math.pi * (31.5 ** 2 - 15.0 ** 2) - 6 * math.pi * BOLT_HOLE_R ** 2
    expect('mounting face area: the whole ring Ø30 to Ø63 less six holes', fi['area'], ring_area, 0.01)
    expect('mounting face Y', fi['box'][1], -4.0, 0, abs_tol=0.01)
    expect('mounting face reaches X +31.5', fi['box'][3], 31.5, 0, abs_tol=0.05)
    meas['mount_face'] = dict(area_mm2=round(fi['area'], 1), hand_area_mm2=round(ring_area, 1), box=[round(v, 3) for v in fi['box']])
    bore = holes(d, HUB_BORE, inside=[-16, -5, -16, 16, 5, 16])
    must('Ø30 bore faces', len(bore), 1)
    expect('bore centre X', bore[0][1][0], 0.0, 0, abs_tol=0.02)
    expect('bore centre Z', bore[0][1][2], 0.0, 0, abs_tol=0.02)
    meas['bore'] = bore[0][1]
    hs = holes(d, BOLT_HOLE_R, inside=[-28, -5, -28, 28, 16, 28])
    must('Ø3.4 screw holes', len(hs), 6)
    for h in hs:
        near = min(math.hypot(h[1][0] - bx, h[1][2] - bz) for bx, bz in BOLTS)
        expect(f'screw hole at {h[1]} against the bolt circle', near, 0.0, 0, abs_tol=0.02)
        expect('screw hole starts at Y -4', h[2][1], -4.0, 0, abs_tol=0.02)
        expect('screw-head seat at Y +4', h[2][4], 4.0, 0, abs_tol=0.02)
    meas['screw_holes'] = [h[1] for h in hs]
    pins = holes(d, PIN_R, inside=[-5, -23, PIN_Z - 5, 5, 23, PIN_Z + 5])
    must('Ø8 pin hole faces (one in each cheek)', len(pins), 2)
    for h in pins:
        expect('pin hole X', h[1][0], 0.0, 0, abs_tol=0.02)
        expect('pin hole Z', h[1][2], PIN_Z, 0, abs_tol=0.02)
        expect('cheek thickness at the pin hole', h[2][4] - h[2][1], 6.0, 0, abs_tol=0.05)
    meas['pin_holes'] = [dict(centre=h[1], y_from=h[2][1], y_to=h[2][4]) for h in pins]
    for sign, nrm in ((1, (0, -1, 0)), (-1, (0, 1, 0))):
        inner = pick(d, kind='plane', normal=nrm, at=(9.0, sign * SLOT_HALF, -196.0))
        must(f'inner cheek face at Y {sign * 16}', len(inner), 1)
        ii = face_info(inner[0])
        expect(f'inner cheek face Y {sign * 16}: flat at that Y', ii['box'][1], sign * SLOT_HALF, 0, abs_tol=0.01)
        b = ii['box']                              # flat over at least Ø16 round the pin: the face's box must cover it
        if not (b[0] <= -8.0 and b[3] >= 8.0 and b[2] <= PIN_Z - 8.0 and b[5] >= PIN_Z + 8.0):
            raise Failed(f'inner cheek face Y {sign * 16} does not cover Ø16 round the pin: box {[round(v, 2) for v in b]}')
        log(f'ok inner cheek face Y {sign * 16} covers Ø16 round the pin: box {[round(v, 2) for v in b]}')
        meas[f'inner_face_y{sign * 16}'] = dict(area_mm2=round(ii['area'], 1), box=[round(v, 3) for v in ii['box']])
    tun = pick(d, kind='cyl', r=CABLE_R, inside=[-4, -4, CABLE_Z1 - 5, 4, 4, CABLE_Z0 + 5])
    must('cable tunnel face', len(tun), 1)
    save(d)

    # 8. exports, and the fixed items that are about clear space, sampled on the STL
    export(j.sw, d, STL)
    export(j.sw, d, STEP)
    st = check_export(d, STL, BOX, STEP)
    close(j.sw, d)

items = fixed_items_stl(STL)
bad = [k for k, v in items.items() if not v['ok']]
shape = picture([STL], PICS / 'checkpoint_02.png')['link_organic.stl']
mass = vol * DENS_G_MM3
mass_before = got('C2', 'mass_before_g')
fixed_ok = bool(not bad)
t2 = since_c2('C2 checkpoint_02')
missing = (f"the study (three load cases) and the before-and-after sheet; fixed items failing: {bad if bad else 'none'}; "
           f"hub seam blend {'R' + str(blend) if blend else 'did not build: a crease is left where the stem leaves the hub'}; "
           f"sharp_per_area {shape['sharp_per_area']}, flat_share {shape['flat_share']}")
cps = [c for c in got('C2', 'checkpoints', []) if c['n'] != 2] + [
    dict(n=2, minutes_since_c2_start=t2, picture='pictures/checkpoint_02.png', missing=missing)]
put('C2', table_name=table_name, build=steps, volume_after_mm3=round(vol, 1), mass_after_g=round(mass, 2),
    mass_ok=bool(mass <= mass_before), shape_after=shape, fixed_items_ok=fixed_ok, fixed_items_failing=bad,
    fixed_items_stl=items, fixed_items_solid=meas, checkpoints=sorted(cps, key=lambda c: c['n']),
    stl=dict(volume=round(st['volume'], 1), watertight=st['watertight'], shells=st['shells'], triangles=st['triangles'],
             bounds=st['bounds']), step_in_mm=True, model_sha256=sha(MODEL), print_orientation=PRINT_TEXT)
rows = '\n'.join(f"| {k} | {v['want']} | {v['value']} of {v['n']} points solid | {'ok' if v['ok'] else 'FAILS'} |" for k, v in items.items())
report(f"""### Stage 2, detail: link_organic built, fixed items measured (stage ended {t2} min after C2 start)

- Table `{table_name}`, loft mode {steps['loft_mode']}, order {steps['order']}; stem {steps['stem_mm3']} mm3, hub added
  {steps['hub_added_mm3']}, knuckle added {steps['knuckle_added_mm3']}, slot removed {steps['slot_mm3']}; hub seam blend:
  {'R' + str(blend) + ' mm on ' + str(steps['ramp_blend_edges']) + ' edges' if blend else 'not built (tried R3, R2, R1.2 on ' + str(steps['ramp_blend_edges']) + ' edges)'}.
- Cuts: pin holes {steps['pin_mm3']} mm3, cable tunnel {steps['cable_mm3']}, screw holes {steps['holes_mm3']}, screw-head
  clearances {steps['heads_mm3']}, below the mounting plane {steps['mount_clean_mm3']} (0 means nothing stood there).
- Volume {vol:.1f} mm3, mass **{mass:.1f} g** against {mass_before} g boxy: {'lighter' if mass <= mass_before else 'HEAVIER: see Branches'}.
- One body, rebuild clean. STL watertight {st['watertight']}, {st['shells']} shell, volume {st['volume']:.1f} mm3, bounds
  {st['bounds']} against the design box {BOX}; STEP in mm.
- On the solid's faces: mounting face one flat face at Y -4, area {meas['mount_face']['area_mm2']} mm2 against
  {meas['mount_face']['hand_area_mm2']} by hand (ring Ø30 to Ø63 less six holes), box {meas['mount_face']['box']}; bore at
  {meas['bore']}; screw holes at {meas['screw_holes']}, each Y -4 to +4; pin holes {meas['pin_holes']}; inner cheek faces
  {meas['inner_face_y16']} and {meas['inner_face_y-16']}.
- On the STL, by sampling (`sheet.inside`), **fixed_items_ok = {fixed_ok}**:

| Item | Must be | Measured | |
| --- | --- | --- | --- |
{rows}

- Print: {PRINT_TEXT}. No enclosed cavity: the cable tunnel is open at both ends; thinnest wall 0.8 mm (the tunnel
  under the hub's two faces, Z -15 to -22).
- Shape numbers: {shape}.
- Checkpoint 2: {t2} min after C2 start, `pictures/checkpoint_02.png`. Still missing against the request: {missing}.
- What I see in checkpoint_02.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE
""")
print('DETAIL DONE fixed_items_ok', fixed_ok, 'mass', round(mass, 1), 'blend', blend, flush=True)
