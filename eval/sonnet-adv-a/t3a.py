"""T3 job A: bracket_b exports and sheet; the twin with split rings; four studies (rings load, hole walls fixed, three sizes;
remote load on the bore at the middle size)."""
import hashlib, json
from lib3 import *

with job(wait_s=1800) as j:
    stamp(RUN, 'T3a job start (bracket_b export, twin, 4 studies)')
    sw = j.sw
    # --- bracket_b STL for the picture and the check
    d = open_doc(sw, WIP / 'bracket_b.SLDPRT')
    export(sw, d, WIP / 'bracket_b.stl')
    vb = volume(d)
    close(sw, d)
    import trimesh
    mb = trimesh.load(WIP / 'bracket_b.stl')
    expect('bracket_b STL watertight', float(mb.is_watertight), 1.0, 0)
    expect('bracket_b STL volume', float(mb.volume), vb, 0.005)

    # --- the twin: same part with 0.3 mm steps round the four small holes
    d = open_doc(sw, WIP / 'bracket.SLDPRT')
    v_orig = volume(d)
    save_as(d, WIP / 'bracket_t3rings.SLDPRT')
    dv = add_rings(d)
    bb = bbox(d)
    log('twin volume change mm3', dv, 'share %', dv / v_orig * 100, 'box', bb)
    for k, want in enumerate((0, 0, 0, 80, 50, 46)):
        expect(f'twin box[{k}]', bb[k], want, 0.01, 0.01)
    close(sw, d)
    d = open_doc(sw, WIP / 'bracket_t3rings.SLDPRT')
    d.ForceRebuild3(False)
    expect('rebuild errors', len(feature_errors(d)), 0, 0)
    expect('bodies', len(bodies(d)), 1, 0)

    def picks():
        d.ForceRebuild3(False)
        holes_fix = pick(d, kind='cyl', r=2.75)
        expect('fixed hole walls', len(holes_fix), 4, 0)
        rings = ring_faces(d)
        bore = pick(d, kind='cyl', r=11.0)
        expect('bore faces', len(bore), 1, 0)
        smallw = pick(d, kind='cyl', r=1.7)
        expect('small hole walls', len(smallw), 4, 0)
        return holes_fix, rings, bore, smallw

    def ctrls(el, rings, smallw, holes_fix):
        return [(rings, max(0.3, el / 3)), (smallw, el / 2), (holes_fix, el / 2)]

    rows = []
    # hand numbers, written before the solve
    I = 50 * 6 ** 3 / 12
    hand_root = 6 * 150 * 22 / (50 * 36)
    hand_disp = 150 * 22 ** 3 / (3 * PETG['EX'] / 1e6 * I)
    rot = 150 * 22 * 25 / (PETG['EX'] / 1e6 * I)       # base cantilevered 25 mm beyond the first screws, 3300 N.mm
    hand_top = hand_disp + rot * 40
    log(f'HAND root stress {hand_root:.2f} MPa, upright tip {hand_disp:.3f} mm alone; base rotation {rot:.4f} rad -> top of upright about {hand_top:.2f} mm; lower hole rim nominal 5.5 x 3 = 16.5')
    for el in (3.0, 2.2, 1.6):
        name = f'T3 RINGS el{el}'
        holes_fix, rings, bore, smallw = picks()
        fix = [('fixed', holes_fix)]
        n_pred = int(1.4 * 12 * 33000 / el ** 3)
        r = run_case(j, d, name, el, fix, [('normal', rings, 150.0)], ctrls(el, rings, smallw, holes_fix),
                     predict=dict(nodes=n_pred, disp_mm=f'{hand_top:.1f} (base rotation + upright bend)', peak='lower small-hole rims, layer tension about 16 MPa'))
        expect('reaction Fx = -150 (opposes the load)', r.reaction[0], -150.0, 0.01)
        expect('resultant', r.reaction[3], r.applied, 0.01)
        lp = r.loaded_pts
        expect('load faces at x 0.3', float(lp[:, 0].mean()), 0.3, 0.1, 0.1)
        m = measures(r)
        # check 3: plain section on the tension face at z 12-14 (hand: M(13) = 150 x 15 -> 6 M / (b h^2) = 7.5 MPa)
        sel = (r.pos[:, 0] < 0.2) & (r.pos[:, 2] >= 12) & (r.pos[:, 2] <= 14) & (r.pos[:, 1] >= 18) & (r.pos[:, 1] <= 32)
        plain = float(r.s[sel, 3].mean())
        log(f'{name}: plain-section sigma_z on the X=0 face at z 12-14: {plain:.2f} MPa from {int(sel.sum())} nodes (hand 7.5)')
        row = dict(el=el, nodes=r.nodes, solve_s=round(r.seconds), disp=r.max_disp(), reaction=r.reaction, applied=r.applied,
                   plain_sz=round(plain, 2), plain_nodes=int(sel.sum()), measures=m, ring_nodes=int(len(lp)),
                   excessive=bool(r.excessive), raw_peak_all=round(float(r.vm.max()), 2))
        rows.append(row)
        append_rows('t3_rows.json', 'rings_holes_fixed', row)
        log(f'{name}: ' + json.dumps({k: (v['vm'], v['layer_Z'], v['shear_Z']) if v else None for k, v in m.items()}))
        stamp(RUN, f'T3a {name} done')
    # the rigid load on the bore, middle size
    el = 2.2
    name = 'T3 BORE REMOTE el2.2'
    holes_fix, rings, bore, smallw = picks()
    fix = [('fixed', holes_fix)]
    r = run_case(j, d, name, el, fix, [('remote', bore, (3.0, 25.0, 28.0), (150.0, 0, 0), (0, 0, 0))],
                 [(bore, el / 3), (smallw, el / 2), (holes_fix, el / 2)],
                 predict=dict(nodes=int(1.4 * 12 * 33000 / el ** 3), disp_mm='lower than rings (rigid bore)', peak='lower'))
    expect('reaction Fx = -150 (opposes the load)', r.reaction[0], -150.0, 0.01)
    m = measures(r)
    row = dict(el=el, nodes=r.nodes, disp=r.max_disp(), reaction=r.reaction, measures=m, raw_peak_all=round(float(r.vm.max()), 2))
    append_rows('t3_rows.json', 'remote_bore_holes_fixed', row)
    log(f'{name}: ' + json.dumps({k: (v['vm'], v['layer_Z'], v['shear_Z']) if v else None for k, v in m.items()}))
    stamp(RUN, 'T3a job end')
