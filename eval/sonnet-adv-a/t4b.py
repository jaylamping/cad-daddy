"""Job C: sharp el 1.6, then the same bracket with a 0.4 mm inside radius (the printed edge) at three sizes."""
import json
from lib3 import *
from bracket_build import build

with job(wait_s=1800) as j:
    stamp(RUN, 'T4b job start')
    sw = j.sw
    d = open_doc(sw, WIP / 'bracket_sharp_rings.SLDPRT')
    d.ForceRebuild3(False)

    def solve(d, name, el, key, corner_ctrl_face):
        d.ForceRebuild3(False)
        hf = pick(d, kind='cyl', r=2.75); rings = ring_faces(d); smallw = pick(d, kind='cyl', r=1.7)
        if corner_ctrl_face == 'edge':
            ce = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01)
            expect('corner edge', len(ce), 1, 0)
            cc = [(ce, el / 4)]
        else:
            f = pick(d, kind='cyl', r=0.4); expect('R0.4 face', len(f), 1, 0)
            cc = [(f, el / 8)]
        r = run_case(j, d, name, el, [('fixed', hf)], [('normal', rings, 150.0)],
                     [(rings, max(0.3, el / 3)), (smallw, el / 2), (hf, el / 2)] + cc,
                     predict=dict(nodes=int(1.5 * 12 * 33000 / el ** 3), disp_mm='about 2.8, as T3'))
        expect('reaction Fx = -150', r.reaction[0], -150.0, 0.01)
        row = dict(el=el, nodes=r.nodes, disp=r.max_disp(), reaction=r.reaction, measures=measures(r), corner=corner_measures(r),
                   raw_peak_all=round(float(r.vm.max()), 2))
        append_rows('t4_rows.json', key, row)
        log(name, json.dumps(row['corner']))
        stamp(RUN, f'T4b {name} done')

    solve(d, 'T4 SHARP el1.6', 1.6, 'sharp', 'edge')
    d, hand = build(sw, WIP / 'bracket_r04.SLDPRT', fillet_r=0.4)
    save_as(d, WIP / 'bracket_r04_rings.SLDPRT')
    add_rings(d)
    close(sw, d)
    d = open_doc(sw, WIP / 'bracket_r04_rings.SLDPRT')
    for el in (3.0, 2.2, 1.6):
        solve(d, f'T4 R04 el{el}', el, 'r04', 'face')
    stamp(RUN, 'T4b job end')
