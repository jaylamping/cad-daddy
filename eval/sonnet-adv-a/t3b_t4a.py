"""Job B: T3 second support (bottom face fixed) and second load (rigid, on the small-hole walls), both on the T3 twin at el 2.2;
then build bracket_sharp (T4) and its twin, and solve the first two sizes of the sharp series."""
import json, sys
from lib3 import *
from bracket_build import build

VARIANT = 'sharp'
SIZES = (3.0, 2.2)
if len(sys.argv) > 1:       # job C: python t3b_t4a.py C
    pass


def corner_measures(r, y_hint=None):
    pos = r.pos
    m = (pos[:, 0] >= 5.99) & (pos[:, 0] <= 10.01) & (pos[:, 2] >= 5.99) & (pos[:, 2] <= 10.01)
    vm, at = r.peak(m)
    ls, lat = r.layer_stress((0, 0, 1), m)
    line = (np.hypot(pos[:, 0] - 6, pos[:, 2] - 6) <= 0.3)
    out = dict(vm=round(vm, 3), vm_at=at, layer_Z=round(ls, 3), layer_Z_at=lat,
               sz_min_on_corner=round(float(r.s[line, 3].min()), 3), sz_max_on_corner=round(float(r.s[line, 3].max()), 3),
               corner_nodes=int(line.sum()))
    mid = [6.0, 25.0, 6.0]       # a point on the corner line away from the ends (y 25: the bore and holes are far)
    for rad in (0.5, 1.0, 2.0):
        a, n = r.average(mid, rad)
        out[f'avg_vm_{rad}'] = round(a, 3); out[f'avg_n_{rad}'] = n
    return out


with job(wait_s=1800) as j:
    stamp(RUN, 'T3b+T4a job start')
    sw = j.sw
    d = open_doc(sw, WIP / 'bracket_t3rings.SLDPRT')
    d.ForceRebuild3(False)
    rows = []

    def picks(d):
        d.ForceRebuild3(False)
        holes_fix = pick(d, kind='cyl', r=2.75); expect('fixed hole walls', len(holes_fix), 4, 0)
        rings = ring_faces(d)
        smallw = pick(d, kind='cyl', r=1.7); expect('small hole walls', len(smallw), 4, 0)
        bottom = pick(d, kind='plane', normal=(0, 0, -1)); expect('bottom face', len(bottom), 1, 0)
        return holes_fix, rings, smallw, bottom

    el = 2.2
    hf, rings, smallw, bottom = picks(d)
    name = 'T3 BOTTOM FIXED el2.2'
    r = run_case(j, d, name, el, [('fixed', bottom)], [('normal', rings, 150.0)],
                 [(rings, el / 3), (smallw, el / 2)],
                 predict=dict(nodes=int(1.4 * 12 * 33000 / el ** 3), disp_mm='smaller than 2.8 (base cannot rotate between screws)',
                              peak='upright root / holes'))
    expect('reaction Fx = -150', r.reaction[0], -150.0, 0.01)
    row = dict(el=el, nodes=r.nodes, disp=r.max_disp(), reaction=r.reaction, measures=measures(r, fixed_dist=0.0),
               raw_peak_all=round(float(r.vm.max()), 2))
    append_rows('t3_rows.json', 'rings_bottom_fixed', row)
    log(name, json.dumps({k: (v['vm'], v['layer_Z'], v['shear_Z']) if v else None for k, v in row['measures'].items()}))
    hf, rings, smallw, bottom = picks(d)
    name = 'T3 SMALLHOLES REMOTE el2.2'
    r = run_case(j, d, name, el, [('fixed', hf)], [('remote', smallw, (0.0, 25.0, 28.0), (150.0, 0, 0), (0, 0, 0))],
                 [(smallw, el / 2), (hf, el / 2)],
                 predict=dict(nodes=int(1.4 * 12 * 33000 / el ** 3), disp_mm='about 2.4 to 2.8', peak='hole rims, lower than rings'))
    expect('reaction Fx = -150', r.reaction[0], -150.0, 0.01)
    row = dict(el=el, nodes=r.nodes, disp=r.max_disp(), reaction=r.reaction, measures=measures(r),
               raw_peak_all=round(float(r.vm.max()), 2))
    append_rows('t3_rows.json', 'remote_smallholes_holes_fixed', row)
    log(name, json.dumps({k: (v['vm'], v['layer_Z'], v['shear_Z']) if v else None for k, v in row['measures'].items()}))
    stamp(RUN, 'T3b studies done')

    # ---------------- T4: build the sharp variant ----------------
    stamp(RUN, 'T4 start (build bracket_sharp)')
    d, hand = build(sw, WIP / 'bracket_sharp.SLDPRT', fillet_r=None)
    vol_sharp = volume(d); bb = bbox(d)
    log('bracket_sharp volume', vol_sharp, 'hand', hand, 'box', bb)
    expect('no fillet face r4', len(pick(d, kind='cyl', r=4.0)), 0, 0)
    export(sw, d, WIP / 'bracket_sharp.stl')
    save_as(d, WIP / 'bracket_sharp_rings.SLDPRT')
    add_rings(d)
    close(sw, d)
    put('T4', build_volume_mm3=round(vol_sharp, 2), build_hand_volume_mm3=round(hand, 2))
    d = open_doc(sw, WIP / 'bracket_sharp_rings.SLDPRT')
    d.ForceRebuild3(False)
    for el in SIZES:
        d.ForceRebuild3(False)
        hf = pick(d, kind='cyl', r=2.75); rings = ring_faces(d); smallw = pick(d, kind='cyl', r=1.7)
        corner = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01)
        expect('corner edge', len(corner), 1, 0)
        name = f'T4 SHARP el{el}'
        r = run_case(j, d, name, el, [('fixed', hf)], [('normal', rings, 150.0)],
                     [(rings, max(0.3, el / 3)), (smallw, el / 2), (hf, el / 2), (corner, el / 4)],
                     predict=dict(nodes=int(1.5 * 12 * 33000 / el ** 3), disp_mm='about 2.8, as T3', peak='sharp inside corner climbs; hole rims as T3'))
        expect('reaction Fx = -150', r.reaction[0], -150.0, 0.01)
        row = dict(el=el, nodes=r.nodes, disp=r.max_disp(), reaction=r.reaction, measures=measures(r), corner=corner_measures(r),
                   raw_peak_all=round(float(r.vm.max()), 2))
        append_rows('t4_rows.json', 'sharp', row)
        log(name, json.dumps(row['corner']))
        stamp(RUN, f'T4 {name} done')
    stamp(RUN, 'T3b+T4a job end')
