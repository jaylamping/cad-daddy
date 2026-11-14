"""T3 studies, part one (four studies in one instance): T3_PADS_30, T3_PADS_22, T3_REMOTE, T3_PADS_16.

Run from the worktree root: python eval/haiku-plan-a/t3_job1.py
"""
from t3lib import *  # noqa: F401,F403

with job() as j:
    j.simulation()                                    # before any document is opened (05-fea.md, "Order")
    make_parts(j)
    make_twin(j, WIP / 'bracket.SLDPRT', WIP / 'bracket_ld.SLDPRT')
    make_twin(j, WIP / 'bracket.SLDPRT', WIP / 'bracket_ld_w.SLDPRT', washers=True)
    d = open_doc(j.sw, WIP / 'bracket_ld.SLDPRT')
    rows = {}
    for name, el, c, load, nodes in (('T3_PADS_30', 3.0, 1.0, 'pads', 22000), ('T3_PADS_22', 2.2, 0.75, 'pads', 56000),
                                     ('T3_REMOTE', 2.2, 0.75, 'remote', 56000), ('T3_PADS_16', 1.6, 0.55, 'pads', 145000)):
        predict(name, nodes, 2.5, 'back face at the lower motor holes (y 14.04 / 35.96, z 17.04), layer tension about 16 MPa')
        r = run(j, d, name, el, c, load=load)
        ok = compare(name, r, nodes, 2.5)
        rows[name] = row(r)
        rows[name]['compare_ok'] = ok
        rows[name]['checks_full'] = checks(r)
        log(name, json.dumps(rows[name], default=float))
        (HERE / 't3_rows.json').write_text(json.dumps(rows, indent=1, default=float), encoding='utf-8')
    close(j.sw, d)
