"""Follow-up R1, T5: round the rib toes (R2.0 at the rib corners on the base and the upright) and solve again.

add_ribs is copied unchanged from t5_ribs.py (importing t5_ribs would run its job). run_c is run() from t3lib.py with
one pick added (the toe faces) and the toe faces added as a control.

Run from the worktree root: python eval/haiku-plan-a/t5_toe.py
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


def add_toes(d, r=2.0):
    e = edges_where(d, lambda p: (abs(p[0] - 34) < 0.01 and abs(p[2] - 6) < 0.01) or (abs(p[0] - 6) < 0.01 and abs(p[2] - 34) < 0.01))
    must('rib toe edges', len(e), 4)                 # along Y, 3.5 long: two on the base at x 34, two on the upright at z 34
    v0 = volume(d)
    got = fillet(d, e, (r, 1.5, 1.0), 'RIB_TOE_R')
    if got is None:
        raise Failed('RIB_TOE_R did not build')
    log('toe radius built', got, 'volume change', volume(d) - v0, '(hand for r 2.0: +1.20 mm3)')
    single_body(d); must('rebuild errors', len(feature_errors(d)), 0); save(d)
    return got


def run_c(j, d, name, el, c, TOE_R):
    """run() from t3lib.py, with the rib toe faces added: pads load, base walls fixed, controls on holes, root and toes."""
    d.ForceRebuild3(False)
    walls = pick(d, kind='cyl', r=2.75)
    must('base hole walls', len(walls), 4)
    bore = pick(d, kind='cyl', r=11.0)
    must('bore', len(bore), 1)
    mh = pick(d, kind='cyl', r=1.7)
    must('motor holes', len(mh), 4)
    pads = pick(d, kind='plane', normal=(-1, 0, 0), inside=[-1.01, -1, -1, -0.99, 51, 47])
    must('pad outer faces', len(pads), 4)
    rf = pick(d, kind='cyl', r=4.0, inside=[5.9, -0.1, 5.9, 6.1 + 4.0, 50.1, 6.1 + 4.0])
    must('root fillet', len(rf), 1)
    toe = pick(d, kind='cyl', r=TOE_R)
    must('toe faces', len(toe), 4)
    mats = {'pad_': PRESS}
    fixtures = [('fixed', walls)]
    loads = [('normal', pads, 150.0)]
    r = static(j, d, name, PETG, fixtures, loads, el=el, ctrl=[(mh + bore, c), (rf, c), (toe, c)], materials=mats,
               loose_ok=True, max_nodes=200_000)
    save_npz(r, name)
    return r


with job() as j:
    j.simulation()
    stamp(HERE, 'R1 T5 toe job start')
    d = build_bracket(j, WIP / 'bracket_c2.SLDPRT')
    add_ribs(d)
    TOE_R = add_toes(d)
    expect('bracket_c2 volume', volume(d), 35693.99 + 1.20, 0.001)
    for got, want in zip(bbox(d), (0, 0, 0, 80, 50, 46)):
        expect('box', got, want, 0.01)
    must('base holes', len(holes(d, 2.75)), 4)
    must('bore', len(holes(d, 11.0)), 1)
    must('motor holes', len(holes(d, 1.7)), 4)
    export(j.sw, d, WIP / 'bracket_c2.stl')
    check_export(d, WIP / 'bracket_c2.stl')
    close(j.sw, d)
    make_twin(j, WIP / 'bracket_c2.SLDPRT', WIP / 'bracket_c2_ld.SLDPRT')
    d = open_doc(j.sw, WIP / 'bracket_c2_ld.SLDPRT')
    rows = {}
    for name, el, c, nodes in (('T5_TOE_30', 3.0, 1.0, 45000), ('T5_TOE_22', 2.2, 0.75, 90000),
                               ('T5_TOE_16', 1.6, 0.55, 195000)):
        predict(name, nodes, 0.9, 'rib toe radius on the base, about 12 to 16 MPa von Mises')
        try:
            r = run_c(j, d, name, el, c, TOE_R)
        except Failed as ex:
            if name == 'T5_TOE_16' and 'over' in str(ex) and '200' in str(ex):
                log('T5_TOE_16 refused over 200,000 nodes; running T5_TOE_18 at (1.8, 0.62)')
                name, el, c = 'T5_TOE_18', 1.8, 0.62
                r = run_c(j, d, name, el, c, TOE_R)
            else:
                raise
        ok = compare(name, r, nodes, 0.9)
        rows[name] = row(r)
        rows[name]['compare_ok'] = ok
        rows[name]['checks_full'] = checks(r)
        log(name, json.dumps(rows[name], default=float))
        (HERE / 't5_toe_rows.json').write_text(json.dumps(rows, indent=1, default=float), encoding='utf-8')
    close(j.sw, d)
    stamp(HERE, 'R1 T5 toe job end')
