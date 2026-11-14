"""T5, step 2b (ribs): bracket_c = T1 bracket plus two 3.5 mm ribs at the Y edges, printed on its side (layers along Y).

Step 2a (same geometry, on its side) is not re-solved: a solve does not depend on print direction, so the Y reading of the
T3 pad series (T3_PADS_16) already is the 2a study. Step 2b is run because Y fails on layer shear (1.79 < 2.0).

Run from the worktree root: python eval/haiku-plan-a/t5_ribs.py
"""
from t3lib import *  # noqa: F401,F403


def add_ribs(d, t=3.5, leg=28.0):
    for name, y0 in (('RIB_A', 0.0), ('RIB_B', 50.0 - t)):
        ym = y0 + t / 2
        with Sk(d, plane(d, 'Y', ym, name + '_P'), name) as s:      # corner drawn 3 mm inside the body so it merges
            s.poly([(3, ym, 3), (9 + leg, ym, 3), (3, ym, 9 + leg)])
        extrude(d, s.feat, name, t, mode=MID, expect_dv=0.5 * leg * leg * t - Q * 16 * t)
    single_body(d)
    must('rebuild errors', len(feature_errors(d)), 0)
    save(d)


with job() as j:
    j.simulation()
    d = build_bracket(j, WIP / 'bracket_c.SLDPRT')
    add_ribs(d)
    expect('bracket_c volume', volume(d), 35693.98, 0.001)
    for got, want in zip(bbox(d), (0, 0, 0, 80, 50, 46)):
        expect('box', got, want, 0.01)
    must('base holes', len(holes(d, 2.75)), 4)
    must('bore', len(holes(d, 11.0)), 1)
    must('motor holes', len(holes(d, 1.7)), 4)
    export(j.sw, d, WIP / 'bracket_c.stl')
    check_export(d, WIP / 'bracket_c.stl')
    close(j.sw, d)
    make_twin(j, WIP / 'bracket_c.SLDPRT', WIP / 'bracket_c_ld.SLDPRT')
    d = open_doc(j.sw, WIP / 'bracket_c_ld.SLDPRT')
    rows = {}
    for name, el, c, nodes in (('T5_RIB_30', 3.0, 1.0, 24000), ('T5_RIB_22', 2.2, 0.75, 61000),
                               ('T5_RIB_16', 1.6, 0.55, 157000)):
        predict(name, nodes, 0.8, 'lower motor-hole rims or base near the X 25 holes; ribs stiffen the upright')
        r = run(j, d, name, el, c)
        ok = compare(name, r, nodes, 0.8)
        rows[name] = row(r)
        rows[name]['compare_ok'] = ok
        rows[name]['checks_full'] = checks(r)
        log(name, json.dumps(rows[name], default=float))
        (HERE / 't5_rows.json').write_text(json.dumps(rows, indent=1, default=float), encoding='utf-8')
    close(j.sw, d)
