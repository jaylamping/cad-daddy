"""T4, job two: series B, the bracket with the 0.4 mm inside-corner radius a printed corner has.

Run from the worktree root: python eval/haiku-plan-a/t4_job2.py
"""
from t3lib import *  # noqa: F401,F403

CORNER = [5.0, -0.1, 5.0, 8.0, 50.1, 8.0]

with job() as j:
    j.simulation()
    d = open_doc(j.sw, WIP / 'bracket_r04_ld.SLDPRT')
    B = []
    for cs, nodes in ((0.3, 71000), (0.2, 86000), (0.13, 126000)):
        name = f'T4_R04_{int(round(cs * 100)):03d}'
        predict(name, nodes, 2.5, 'the 0.4 mm inside-corner radius (x 6, z 6): compressive, about 24 MPa von Mises')
        r = run(j, d, name, 2.2, 0.75, root=0.4, root_c=cs)
        compare(name, r, nodes, 2.5)
        m = body_mask(r) & r.in_box(CORNER)
        avg = {rad: r.average((6.0, 25.0, 6.0), rad) for rad in (0.5, 1.0, 2.0)}
        B.append(dict(ctrl=cs, nodes=r.nodes, corner_vm=round(r.peak(m)[0], 2), corner_at=r.peak(m)[1], avg=avg,
                      corner_sz=round(float(r.s[m, 3].min()), 2), row=row(r)))
        log(name, json.dumps(B[-1], default=float))
        (HERE / 't4_r04.json').write_text(json.dumps(B, indent=1, default=float), encoding='utf-8')
    close(j.sw, d)
