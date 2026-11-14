"""Follow-up R2b, T6: a matched mesh on the same contact model. No build: the saved block_fea.SLDPRT is opened.

run_m is run() from t6.py with one change: the pin's own control is the same size as the hole's (ctrl=[(hole, c), (mid, c)]).
Line mean (step a of R2) is read from each result with the mask given in the follow-up.

Run from the worktree root: python eval/haiku-plan-a/t6m.py
"""
from t6 import *  # noqa: F401,F403


def run_m(j, d, name, c, f_each=250.0):
    d.ForceRebuild3(False)
    bottom = pick(d, kind='plane', normal=(0, 0, -1), at=(0, 0, 0))
    must('block bottom', len(bottom), 1)
    hole = pick(d, kind='cyl', r=5.1)
    must('hole', len(hole), 1)
    mid = pick(d, kind='cyl', r=5.0, inside=[-5.1, -17.1, 4.8, 5.1, 17.1, 15.2])
    must('pin mid face', len(mid), 1)
    ea = pick(d, kind='cyl', r=5.0, inside=[-5.1, 16.9, 4.8, 5.1, 25.1, 15.2])
    must('pin end a', len(ea), 1)
    eb = pick(d, kind='cyl', r=5.0, inside=[-5.1, -25.1, 4.8, 5.1, -16.9, 15.2])
    must('pin end b', len(eb), 1)
    pa = pick(d, kind='plane', normal=(0, 1, 0), at=(0, 26.5, 10))
    must('pad a outer', len(pa), 1)
    pb = pick(d, kind='plane', normal=(0, -1, 0), at=(0, -26.5, 10))
    must('pad b outer', len(pb), 1)
    r = static(j, d, name, PETG,
               fixtures=[('fixed', bottom), ('fixed', pa + pb)],
               loads=[('remote', ea, (0.0, 21.0, 10.0), (0, 0, f_each), (0, 0, 0)),
                      ('remote', eb, (0.0, -21.0, 10.0), (0, 0, f_each), (0, 0, 0))],
               el=3.0, ctrl=[(hole, c), (mid, c)],
               contacts=[(NO_PENETRATION, hole, mid)], materials=MATS, solver=SOLVER_DIRECT,
               post=per_node_reaction, loose_ok=False, max_nodes=200_000)
    save_npz(r, name)
    return r


def line_mean(r):
    """Step a of R2: the mean and maximum of the contact pressure on the line along the top of the hole, in MPa."""
    p = r.pos
    rho = np.hypot(p[:, 0], p[:, 2] - 10.0)
    block = rho > 5.096
    line = block & (rho < 5.13) & (np.abs(p[:, 0]) < 0.25) & (p[:, 2] > 10) & (np.abs(p[:, 1]) < 8)
    v = -r.s[line, 3]
    return dict(line_nodes=int(line.sum()), line_mean=round(float(v.mean()), 3) if v.size else None,
                line_max=round(float(v.max()), 3) if v.size else None)


def checks_m(out):
    ok = dict(
        reaction_fz=-505.0 <= out['reaction'][2] <= -495.0 if out.get('reaction') is not None else None,
        fz_block=(-505.0 <= out['fz_block'] <= -495.0) if 'fz_block' in out else None,
        fz_pads=(abs(out['fz_pads']) < 5.0) if 'fz_pads' in out else None,
        pin_rise=0.10 <= out['pin_rise'] <= 0.14,
    )
    return ok


rows = []
with job() as j:
    j.simulation()
    stamp(HERE, 'R2b T6 matched-mesh job start')
    d = open_doc(j.sw, WIP / 'block_fea.SLDPRT')
    res = []
    for name, c, nodes in (('T6M_12', 1.2, 45000), ('T6M_08', 0.8, 84000), ('T6M_06', 0.6, 138000)):
        predict(name, nodes, 0.13, 'top of the hole (x 0, z 15.1), pressure about 6.8 MPa, higher toward y +-15')
        try:
            r = run_m(j, d, name, c)
        except Failed as ex:
            if name == 'T6M_06':
                log(f'T6M_06 refused ({str(ex)[:160]}); running T6M_065 at 0.65')
                name, c = 'T6M_065', 0.65
                r = run_m(j, d, name, c)
            else:
                raise
        compare(name, r, nodes, 0.13)
        out = read(r)
        out.update(line_mean(r))
        out['checks'] = checks_m(out)
        res.append(out)
        log(json.dumps(out, default=float))
        (HERE / 't6m_rows.json').write_text(json.dumps(res, indent=1, default=float), encoding='utf-8')
    close(j.sw, d)
    stamp(HERE, 'R2b T6 matched-mesh job end')
