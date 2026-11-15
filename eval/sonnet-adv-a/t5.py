"""T5: bracket_c = the T1 bracket with the upright 7.5 mm thick (X 0 to 7.5, outer face and footprint unchanged).
Three sizes with the hole walls fixed and rings load, plus the bottom face fixed at 2.2."""
import json, math, sys
import lib3
from lib3 import *
from bracket_build import build

T_UP = 7.5
MOUTH = 'mouth' in sys.argv
SUF = 'b' if MOUTH else ''
lib3.T_UP = T_UP
V0 = 32974.02416773478
CAP = 1.10 * V0

with job(wait_s=1800) as j:
    stamp(RUN, 'T5 start')
    sw = j.sw
    def mouths(d):
        v0 = volume(d)
        e = edges_where(d, lambda p: abs(p[0] - T_UP) < 0.01 and any(abs(math.hypot(p[1] - cy, p[2] - cz) - 1.7) < 0.02 for cy, cz in HOLES_YZ))
        expect('hole mouth edges on the inner face', len(e), 4, 0)
        expect('R0.4 mouth rounds built', fillet(d, e, (0.4,), 'MOUTH_ROUNDS') or 0, 0.4, 0)
        expect('mouth rounds remove only a sliver', (v0 - volume(d)) / v0 * 100, 0.01, 0.02, abs_tol=0.02)
        save(d)
        expect('bodies', len(bodies(d)), 1, 0); expect('errors', len(feature_errors(d)), 0, 0)

    d, hand = build(sw, WIP / f'bracket_c{SUF}.SLDPRT', fillet_r=4.0, t_up=T_UP, extra=mouths if MOUTH else None)
    vol = volume(d); bb = bbox(d)
    log('bracket_c volume', vol, 'hand', hand, 'growth %', (vol / V0 - 1) * 100, 'box', bb)
    expect('mass cap', float(vol <= CAP), 1.0, 0)
    for k, want in enumerate((0, 0, 0, 80, 50, 46)):
        expect(f'footprint box[{k}]', bb[k], want, 0.01, 0.01)
    # the fixed interfaces, measured on the finished solid
    expect('base holes unchanged', len(pick(d, kind='cyl', r=2.75)), 4, 0)
    bore = pick(d, kind='cyl', r=11.0); expect('bore', len(bore), 1, 0)
    bi = face_info(bore[0])['box']
    expect('bore y centre', (bi[1] + bi[4]) / 2, 25.0, 0.01, 0.01); expect('bore z centre', (bi[2] + bi[5]) / 2, 28.0, 0.01, 0.01)
    expect('small holes unchanged', len(pick(d, kind='cyl', r=1.7)), 4, 0)
    export(sw, d, WIP / f'bracket_c{SUF}.step'); export(sw, d, WIP / f'bracket_c{SUF}.stl')
    save_as(d, WIP / f'bracket_c{SUF}_rings.SLDPRT')
    add_rings(d)
    close(sw, d)
    import trimesh
    mesh = trimesh.load(WIP / f'bracket_c{SUF}.stl')
    expect('STL watertight', float(mesh.is_watertight), 1.0, 0)
    expect('STL volume', float(mesh.volume), vol, 0.005)
    stp = (WIP / f'bracket_c{SUF}.step').read_text(errors='ignore')
    expect('STEP mm', float(any('SI_UNIT' in ln and '.MILLI.' in ln for ln in stp.splitlines())), 1.0, 0)
    put('T5' + SUF, build_volume_mm3=round(vol, 2), build_hand_volume_mm3=round(hand, 2), mass_g=round(vol * DENS, 3),
        mass_growth_pct=round((vol / V0 - 1) * 100, 2))
    d = open_doc(sw, WIP / f'bracket_c{SUF}_rings.SLDPRT')
    d.ForceRebuild3(False)

    def picks():
        d.ForceRebuild3(False)
        hf = pick(d, kind='cyl', r=2.75); expect('fixed hole walls', len(hf), 4, 0)
        rings = ring_faces(d)
        smallw = pick(d, kind='cyl', r=1.7); expect('small hole walls', len(smallw), 4, 0)
        bottom = pick(d, kind='plane', normal=(0, 0, -1)); expect('bottom', len(bottom), 1, 0)
        if MOUTH:
            for cy, cz in HOLES_YZ:
                mf = pick(d, inside=[T_UP - 0.45, cy - 2.2, cz - 2.2, T_UP + 0.01, cy + 2.2, cz + 2.2])
                expect('mouth torus face', len(mf), 1, 0)
                smallw = smallw + mf
        return hf, rings, smallw, bottom

    I = 50 * T_UP ** 3 / 12
    hand_disp = 150 * 22 ** 3 / (3 * PETG['EX'] / 1e6 * I)
    rot = 150 * 22 * 25 / (PETG['EX'] / 1e6 * (50 * 6 ** 3 / 12))
    hand_top = hand_disp + rot * 40
    for el in (3.0, 2.2, 1.6):
        hf, rings, smallw, bottom = picks()
        name = f'T5 C el{el}'
        r = run_case(j, d, name, el, [('fixed', hf)], [('normal', rings, 150.0)],
                     [(rings, max(0.3, el / 3)), (smallw, el / 2), (hf, el / 2)],
                     predict=dict(nodes=int(1.4 * 12 * vol / el ** 3), disp_mm=f'about {hand_top:.1f} (the base still turns between the screws)',
                                  layer_Z_hole_rims_mpa=round(14.5 * (6 / T_UP) ** 2, 1), peak='lower holes'))
        expect('reaction Fx = -150', r.reaction[0], -150.0, 0.01)
        row = dict(el=el, nodes=r.nodes, disp=r.max_disp(), reaction=r.reaction, measures=measures(r), raw_peak_all=round(float(r.vm.max()), 2))
        append_rows(f't5{SUF}_rows.json', 'rings_holes_fixed', row)
        log(name, json.dumps({k: (v['vm'], v['layer_Z'], v['shear_Z'], v['layer_Y'], v['shear_Y']) if v else None for k, v in row['measures'].items()}))
        stamp(RUN, f'T5 {name} done')
    el = 2.2
    hf, rings, smallw, bottom = picks()
    name = 'T5 C BOTTOM el2.2'
    r = run_case(j, d, name, el, [('fixed', bottom)], [('normal', rings, 150.0)], [(rings, el / 3), (smallw, el / 2)],
                 predict=dict(nodes=int(1.4 * 12 * vol / el ** 3)))
    expect('reaction Fx = -150', r.reaction[0], -150.0, 0.01)
    row = dict(el=el, nodes=r.nodes, disp=r.max_disp(), reaction=r.reaction, measures=measures(r, fixed_dist=0.0), raw_peak_all=round(float(r.vm.max()), 2))
    append_rows(f't5{SUF}_rows.json', 'rings_bottom_fixed', row)
    log(name, json.dumps({k: (v['vm'], v['layer_Z'], v['shear_Z'], v['layer_Y'], v['shear_Y']) if v else None for k, v in row['measures'].items()}))
    stamp(RUN, 'T5 job end')
