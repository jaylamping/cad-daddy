"""T3, part two: the washer support study (T3_WASHERS), added to t3_rows.json.

Run from the worktree root: python eval/haiku-plan-a/t3_job2.py
"""
from t3lib import *  # noqa: F401,F403

with job() as j:
    j.simulation()
    d = open_doc(j.sw, WIP / 'bracket_ld_w.SLDPRT')
    predict('T3_WASHERS', 56000, 2.5, 'same upright and motor-hole rims as T3_PADS_22 (second support)')
    r = run(j, d, 'T3_WASHERS', 2.2, 0.75, load='pads', fix='washers')
    ok = compare('T3_WASHERS', r, 56000, 2.5)
    rows = json.loads((HERE / 't3_rows.json').read_text(encoding='utf-8'))
    rows['T3_WASHERS'] = row(r, D=3.0, rad=5.0)
    rows['T3_WASHERS']['compare_ok'] = ok
    rows['T3_WASHERS']['checks_full'] = checks(r)
    (HERE / 't3_rows.json').write_text(json.dumps(rows, indent=1, default=float), encoding='utf-8')
    log('T3_WASHERS', json.dumps(rows['T3_WASHERS'], default=float))
    close(j.sw, d)
