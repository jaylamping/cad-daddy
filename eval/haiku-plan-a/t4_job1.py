"""T4, job one: build bracket_sharp and bracket_r04 (with their pad twins), then series A on the sharp corner.

Run from the worktree root: python eval/haiku-plan-a/t4_job1.py
"""
from t3lib import *  # noqa: F401,F403

CORNER = [5.0, -0.1, 5.0, 8.0, 50.1, 8.0]            # box round the inside corner: x 5..8, z 5..8

with job() as j:
    j.simulation()
    for name, rr in (('bracket_sharp', None), ('bracket_r04', 0.4)):
        d = build_bracket(j, WIP / f'{name}.SLDPRT', root_r=rr)
        expect(name + ' volume', volume(d), hand_volume(rr), 0.001)
        for got, want in zip(bbox(d), (0, 0, 0, 80, 50, 46)):
            expect('box', got, want, 0.01)
        if rr is None:
            must('no fillet face', len(pick(d, kind='cyl', r=4.0)), 0)
            export(j.sw, d, WIP / 'bracket_sharp.stl')
            check_export(d, WIP / 'bracket_sharp.stl')
        close(j.sw, d)
        make_twin(j, WIP / f'{name}.SLDPRT', WIP / f'{name}_ld.SLDPRT')      # pads from T3 must exist in WIP

    # Series A, sharp corner: global 2.2, motor holes and bore at 0.75, only the corner control halves each time
    d = open_doc(j.sw, WIP / 'bracket_sharp_ld.SLDPRT')
    A = []
    for cs, nodes in ((1.0, 61000), (0.5, 71000), (0.25, 101000)):
        name = f'T4_SHARP_{int(cs * 100):03d}'
        predict(name, nodes, 2.5, 'the inside corner edge (x 6, z 6): a singularity, expected to climb')
        r = run(j, d, name, 2.2, 0.75, root=None, root_c=cs)
        compare(name, r, nodes, 2.5)
        m = body_mask(r) & r.in_box(CORNER)
        avg = {rad: r.average((6.0, 25.0, 6.0), rad) for rad in (0.5, 1.0, 2.0)}     # (mean von Mises, node count)
        A.append(dict(ctrl=cs, nodes=r.nodes, corner_vm=round(r.peak(m)[0], 2), corner_at=r.peak(m)[1], avg=avg,
                      corner_sz=round(float(r.s[m, 3].min()), 2), row=row(r)))
        log(name, json.dumps(A[-1], default=float))
        (HERE / 't4_sharp.json').write_text(json.dumps(A, indent=1, default=float), encoding='utf-8')
    close(j.sw, d)
