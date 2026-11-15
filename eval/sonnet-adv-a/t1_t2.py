import math, os, hashlib
from common import *
from swkit import *

V_BASE = 80 * 50 * 6
V_UP = 6 * 50 * 40
V_FIL = (16 - 4 * math.pi) * 50                 # R4 inside corner: r^2 (1 - pi/4) * length 50 (adds material)
V_BH = 4 * math.pi * 2.75 ** 2 * 6
V_BORE = math.pi * 11 ** 2 * 6
V_SH = 4 * math.pi * 1.7 ** 2 * 6
V_RB = 2 * 25 * (1 - math.pi / 4) * 6           # two base corners R5, height 6
V_RU = 2 * 25 * (1 - math.pi / 4) * 6           # two upright top corners R5, length along X 6
HAND = V_BASE + V_UP + V_FIL - V_BH - V_BORE - V_SH - V_RB - V_RU
log('hand volume T1', HAND, 'mass g', HAND * DENS)
H = 15.5 * math.cos(math.radians(45))


def tree(d):
    out = []
    f = d.FirstFeature
    while f is not None:
        out.append(f.Name + '|' + f.GetTypeName2)
        f = f.GetNextFeature
    return out


with job(wait_s=1800) as j:
    stamp(RUN, 'T1 start')
    sw = j.sw
    d = new_part(sw, WIP / 'bracket.SLDPRT')
    with Sk(d, plane(d, 'Z', 3.0, 'BASE_P'), 'BASE') as s:
        s.rect((0, 0, 3.0), (80, 50, 3.0))
    extrude(d, s.feat, 'BASE', 6.0, mode=MID, expect_dv=V_BASE); save(d)
    with Sk(d, plane(d, 'Z', 26.0, 'UP_P'), 'UPRIGHT') as s:
        s.rect((0, 0, 26.0), (6, 50, 26.0))
    extrude(d, s.feat, 'UPRIGHT', 40.0, mode=MID, expect_dv=V_UP); save(d)
    expect('one body', len(bodies(d)), 1, 0)
    # inside corner fillet: the edge along Y at X 6, Z 6
    v0 = volume(d)
    e = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01)
    expect('inside-corner edges', len(e), 1, 0)
    expect('fillet radius built', fillet(d, e, (4.0,), 'INSIDE_FILLET') or 0, 4.0, 0)
    expect('fillet dv', volume(d) - v0, V_FIL, 0.01); save(d)
    # base holes
    with Sk(d, plane(d, 'Z', 3.0, 'BH_P'), 'BASE_HOLES') as s:
        for x, y in ((25, 10), (25, 40), (65, 10), (65, 40)):
            s.circle((x, y, 3.0), 2.75)
    extrude(d, s.feat, 'BASE_HOLES', 10.0, cut=True, mode=MID, expect_dv=V_BH); save(d)
    # bore + 4 small holes, in two features so each has its own check
    with Sk(d, plane(d, 'X', 3.0, 'BORE_P'), 'BORE') as s:
        s.circle((3.0, 25, 28), 11.0)
    extrude(d, s.feat, 'BORE', 10.0, cut=True, mode=MID, expect_dv=V_BORE); save(d)
    with Sk(d, plane(d, 'X', 3.0, 'SH_P'), 'SMALL_HOLES') as s:
        for sy in (1, -1):
            for sz in (1, -1):
                s.circle((3.0, 25 + sy * H, 28 + sz * H), 1.7)
    extrude(d, s.feat, 'SMALL_HOLES', 10.0, cut=True, mode=MID, expect_dv=V_SH); save(d)
    # rounds
    v0 = volume(d)
    e = edges_where(d, lambda p: abs(p[0] - 80) < 0.01 and (abs(p[1]) < 0.01 or abs(p[1] - 50) < 0.01))
    expect('base corner edges', len(e), 2, 0)
    expect('R5 base built', fillet(d, e, (5.0,), 'BASE_ROUNDS') or 0, 5.0, 0)
    expect('base rounds dv', v0 - volume(d), V_RB, 0.01); save(d)
    v0 = volume(d)
    e = edges_where(d, lambda p: abs(p[2] - 46) < 0.01 and (abs(p[1]) < 0.01 or abs(p[1] - 50) < 0.01) and -0.01 <= p[0] <= 6.01)
    expect('upright top edges', len(e), 2, 0)
    expect('R5 upright built', fillet(d, e, (5.0,), 'UPRIGHT_ROUNDS') or 0, 5.0, 0)
    expect('upright rounds dv', v0 - volume(d), V_RU, 0.01); save(d)

    # ---- measure the finished solid
    vol = volume(d); bb = bbox(d)
    expect('T1 volume', vol, HAND, 0.002)
    for k, want in enumerate((0, 0, 0, 80, 50, 46)):
        expect(f'bbox[{k}]', bb[k], want, 0.01, 0.01)
    expect('bodies', len(bodies(d)), 1, 0)
    expect('rebuild errors', len(feature_errors(d)), 0, 0)
    meas = {}

    def centres(r, n):
        fs = pick(d, kind='cyl', r=r)
        expect(f'faces r={r}', len(fs), n, 0)
        out = []
        for f in fs:
            i = face_info(f); b = i['box']
            out.append(tuple(round((b[k] + b[k + 3]) / 2, 3) for k in range(3)) + (round(i['area'], 2),))
        return sorted(out)

    base_h = centres(2.75, 4); meas['base_holes'] = base_h
    for (cx, cy, cz, _), (wx, wy) in zip(base_h, sorted([(25, 10), (25, 40), (65, 10), (65, 40)])):
        expect('base hole x', cx, wx, 0.01, 0.01); expect('base hole y', cy, wy, 0.01, 0.01); expect('base hole z centre', cz, 3.0, 0.01, 0.01)
    bore = centres(11.0, 1); meas['bore'] = bore
    expect('bore y', bore[0][1], 25, 0.01, 0.01); expect('bore z', bore[0][2], 28, 0.01, 0.01); expect('bore x centre', bore[0][0], 3, 0.01, 0.01)
    sm = centres(1.7, 4); meas['small'] = sm
    want_sm = sorted([(3, 25 + a * H, 28 + b * H) for a in (1, -1) for b in (1, -1)])
    for (cx, cy, cz, _), (wx, wy, wz) in zip(sm, want_sm):
        expect('small y', cy, wy, 0.01, 0.01); expect('small z', cz, wz, 0.01, 0.01)
    f4 = pick(d, kind='cyl', r=4.0); expect('R4 faces', len(f4), 1, 0)
    bi = face_info(f4[0])['box']; meas['r4_box'] = bi
    expect('R4 box x0', bi[0], 6.0, 0.01, 0.01); expect('R4 box x1', bi[3], 10.0, 0.01, 0.01)
    expect('R4 z0', bi[2], 6.0, 0.01, 0.01); expect('R4 z1', bi[5], 10.0, 0.01, 0.01)
    f5 = pick(d, kind='cyl', r=5.0); expect('R5 faces', len(f5), 4, 0)
    meas['r5'] = [[round(v, 2) for v in face_info(f)['box']] for f in f5]
    for nm, nrm, ax, want in (('base top', (0, 0, 1), 2, 6.0), ('upright top', (0, 0, 1), 2, 46.0), ('upright outer', (-1, 0, 0), 0, 0.0),
                              ('upright inner', (1, 0, 0), 0, 6.0), ('end face', (1, 0, 0), 0, 80.0)):
        hits = [face_info(f)['box'] for f in pick(d, kind='plane', normal=nrm)]
        vals = sorted({round(b[ax], 3) for b in hits})
        meas[nm] = vals
        expect(nm + ' present', float(any(abs(v - want) < 0.01 for v in vals)), 1.0, 0)
    log('measured', meas)
    q = {'small_hole_edge_to_bore_edge_mm': 15.5 - 11 - 1.7, 'small_hole_dia_mm': 3.4,
         'bore_top_to_upright_top_mm': 46 - 39, 'bore_bottom_to_base_top_mm': 17 - 6, 'bore_y_edge_to_side_mm': 14,
         'base_hole_edge_to_nearest_side_mm': 10 - 2.75, 'base_hole_to_fillet_toe_mm': 25 - 2.75 - 10,
         'upright_thickness_mm': 6, 'bearing_length_over_bore_dia': 6 / 22}
    log('spec', q)
    save(d)
    log('tree T1', tree(d))
    export(sw, d, WIP / 'bracket.step'); export(sw, d, WIP / 'bracket.stl')
    close(sw, d)
    import trimesh
    mesh = trimesh.load(WIP / 'bracket.stl')
    wt = bool(mesh.is_watertight); parts = len(mesh.split())
    expect('STL watertight', float(wt), 1.0, 0); expect('STL shells', parts, 1, 0)
    expect('STL volume', float(mesh.volume), vol, 0.005)
    for k in range(3):
        expect(f'STL min[{k}]', float(mesh.bounds[0][k]), bb[k], 0.1, 0.1); expect(f'STL max[{k}]', float(mesh.bounds[1][k]), bb[k + 3], 0.1, 0.1)
    stp = (WIP / 'bracket.step').read_text(errors='ignore')
    milli = any('SI_UNIT' in ln and '.MILLI.' in ln for ln in stp.splitlines())
    expect('STEP in mm', float(milli), 1.0, 0)
    sha = hashlib.sha256((WIP / 'bracket.SLDPRT').read_bytes()).hexdigest()
    put('T1', volume_mm3=round(vol, 2), hand_volume_mm3=round(HAND, 2), mass_g=round(vol * DENS, 3),
        bbox_mm=[round(v, 3) for v in bb], bodies=1, stl_watertight=wt, stl_volume_mm3=round(float(mesh.volume), 2),
        status='done', notes=f'sha256 {sha}; measured {meas}; spec questions {q}')
    stamp(RUN, 'T1 end')
    orig_sha = sha; orig_vol = vol

    # ================= T2 =================
    stamp(RUN, 'T2 start')
    d = open_doc(sw, WIP / 'bracket.SLDPRT')
    expect('opened bracket volume', volume(d), orig_vol, 0.0001)
    save_as(d, WIP / 'bracket_b.SLDPRT')          # edit the copy, never the original
    expect('open doc is bracket_b', float('bracket_b' in d.GetPathName), 1.0, 0)
    t_before = tree(d)
    V_CB = 4 * math.pi * (25 - 2.75 ** 2) * 3
    V_SLOT = 14 * 6 * 6 + math.pi * 9 * 6
    HAND2 = HAND - V_CB - V_SLOT
    with Sk(d, plane(d, 'Z', 4.5, 'CB_P'), 'CBORE') as s:
        for x, y in ((25, 10), (25, 40), (65, 10), (65, 40)):
            s.circle((x, y, 4.5), 5.0)
    extrude(d, s.feat, 'CBORE', 3.0, cut=True, mode=MID, expect_dv=V_CB)
    save(d)
    with Sk(d, plane(d, 'Z', 3.0, 'SLOT_P'), 'SLOT_RECT') as s:
        s.rect((38, 22, 3.0), (52, 28, 3.0))
    extrude(d, s.feat, 'SLOT_RECT', 10.0, cut=True, mode=MID, expect_dv=14 * 6 * 6); save(d)
    with Sk(d, plane(d, 'Z', 3.0, 'SLOT_E1P'), 'SLOT_END_L') as s:
        s.circle((38, 25, 3.0), 3.0)
    extrude(d, s.feat, 'SLOT_END_L', 10.0, cut=True, mode=MID, expect_dv=math.pi * 9 * 6 / 2); save(d)
    with Sk(d, plane(d, 'Z', 3.0, 'SLOT_E2P'), 'SLOT_END_R') as s:
        s.circle((52, 25, 3.0), 3.0)
    extrude(d, s.feat, 'SLOT_END_R', 10.0, cut=True, mode=MID, expect_dv=math.pi * 9 * 6 / 2); save(d)
    vol2 = volume(d)
    expect('T2 volume', vol2, HAND2, 0.002)
    expect('bodies', len(bodies(d)), 1, 0); expect('rebuild errors', len(feature_errors(d)), 0, 0)
    bb2 = bbox(d)
    for k, want in enumerate((0, 0, 0, 80, 50, 46)):
        expect(f'bbox2[{k}]', bb2[k], want, 0.01, 0.01)
    t_after = tree(d)
    log('tree before', t_before); log('tree after', t_after)
    expect('old features still there', float(all(x in t_after for x in t_before)), 1.0, 0)
    fl = [face_info(f) for f in pick(d, kind='plane', normal=(0, 0, 1))]
    log('plane faces z values', sorted({round(i['box'][2], 3) for i in fl}))
    cb_floor = [i for i in fl if abs(i['box'][2] - 3.0) < 0.05]
    expect('counterbore floors', len(cb_floor), 4, 0)
    for i in cb_floor:
        b = i['box']
        expect('cb floor outer dia', b[3] - b[0], 10.0, 0.01, 0.01); expect('cb floor z', b[2], 3.0, 0.01, 0.01)
    expect('cbore wall faces r5', len(pick(d, kind='cyl', r=5.0, inside=[15, 0, 2.9, 70, 50, 6.1])), 4, 0)
    slot_cyl = pick(d, kind='cyl', r=3.0)
    expect('slot end faces r3', len(slot_cyl), 2, 0)
    slot_box = sorted([face_info(f)['box'] for f in slot_cyl])
    log('slot end boxes', slot_box)
    expect('slot overall length', max(b[3] for b in slot_box) - min(b[0] for b in slot_box), 20.0, 0.01, 0.01)
    expect('slot width', slot_box[0][4] - slot_box[0][1], 6.0, 0.01, 0.01)
    expect('slot centre x', (max(b[3] for b in slot_box) + min(b[0] for b in slot_box)) / 2, 45.0, 0.01, 0.01)
    expect('slot centre y', (slot_box[0][4] + slot_box[0][1]) / 2, 25.0, 0.01, 0.01)
    save(d)
    close(sw, d)
    d0 = open_doc(sw, WIP / 'bracket.SLDPRT')
    expect('original volume after edits', volume(d0), orig_vol, 0.0001)
    close(sw, d0)
    sha_after = hashlib.sha256((WIP / 'bracket.SLDPRT').read_bytes()).hexdigest()
    log('original sha before/after', orig_sha, sha_after)
    put('T2', volume_mm3=round(vol2, 2), hand_volume_mm3=round(HAND2, 2), counterbore_floor_z_mm=3.0, bodies=1, status='done',
        notes=f'original bracket.SLDPRT sha {orig_sha} -> {sha_after}; tree before {t_before}; after {t_after}')
    stamp(RUN, 'T2 end')
