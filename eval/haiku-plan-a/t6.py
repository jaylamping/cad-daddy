"""T6: PETG block with a Ø10.2 hole, Ø10 steel pin with a 0.1 mm radial gap, pulled 250 N at each end. Contact study.

Plan: plans/A_T6.md. Run from the worktree root: python eval/haiku-plan-a/t6.py
Starts with build(); the PIN_Z fallback (A) is run by t6_fallback.py if this run fails the checks.
"""
from common import *  # noqa: F401,F403
from swfea import _arr, BONDED, NO_PENETRATION, SOLVER_DIRECT  # noqa: F401

PIN_Z = 10.0                                   # 10.09 only in fallback A


def cyl_y(j, path, y0, y1, r, feat, z=10.0):
    d = new_part(j.sw, path)
    ym = (y0 + y1) / 2
    with Sk(d, plane(d, 'Y', ym, feat + '_P'), feat) as s:
        s.circle((0, ym, z), r)
    extrude(d, s.feat, feat, y1 - y0, mode=MID, expect_dv=math.pi * r * r * (y1 - y0))
    save(d)
    close(j.sw, d)


def build(j, pin_z=PIN_Z):
    cyl_y(j, WIP / 'pin_mid.SLDPRT', -17, 17, 5.0, 'PINMID', pin_z)
    cyl_y(j, WIP / 'pin_end_a.SLDPRT', 17, 25, 5.0, 'PINEND', pin_z)
    cyl_y(j, WIP / 'pin_end_b.SLDPRT', -25, -17, 5.0, 'PINEND', pin_z)
    cyl_y(j, WIP / 'pad_a.SLDPRT', 25, 26.5, 1.5, 'SOFTPAD', pin_z)
    cyl_y(j, WIP / 'pad_b.SLDPRT', -26.5, -25, 1.5, 'SOFTPAD', pin_z)
    d = new_part(j.sw, WIP / 'block_fea.SLDPRT')
    with Sk(d, plane(d, 'Z', 10.0, 'BLOCK_P'), 'BLOCK') as s:
        s.rect((-20, -15, 10.0), (20, 15, 10.0))
    extrude(d, s.feat, 'BLOCK', 20.0, mode=MID, expect_dv=24000.0)
    with Sk(d, plane(d, 'Y', 0.0, 'HOLE_P'), 'HOLE') as s:
        s.circle((0, 0, 10.0), 5.1)
    extrude(d, s.feat, 'HOLE', 31.0, cut=True, mode=MID, expect_dv=math.pi * 5.1 ** 2 * 30)
    save(d)
    for f in ('pin_mid', 'pin_end_a', 'pin_end_b', 'pad_a', 'pad_b'):
        insert_body(d, WIP / f'{f}.SLDPRT')
    bs = bodies(d)
    log(bs)
    must('bodies', len(bs), 6)
    expect('total volume', volume(d), 21548.62 + 2670.35 + 2 * 628.32 + 2 * 10.60, 0.001)
    save(d)
    close(j.sw, d)


MATS = {'pin_': STEEL, 'pad_': SOFT}


def per_node_reaction(st, res):                                  # kept as r.extra: id, Fx Fy Fz Fres, Mx My Mz Mres
    return _arr(res.GetReactionForcesAndMoments(0, NUL, 0, L()), 9)


def run(j, d, name, hole_c, f_each=250.0, loose_ok=False):
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
               el=3.0, ctrl=[(hole, hole_c), (mid, 1.0)],
               contacts=[(NO_PENETRATION, hole, mid)], materials=MATS, solver=SOLVER_DIRECT,
               post=per_node_reaction, loose_ok=loose_ok, max_nodes=200_000)
    save_npz(r, name)
    return r


def read(r):
    p = r.pos
    rho = np.hypot(p[:, 0], p[:, 2] - 10.0)                    # distance from the hole axis
    pin = np.hypot(p[:, 0], p[:, 2] - PIN_Z) < 5.004           # pin and pads: inside the pin's own radius
    blk = ~pin & (rho > 5.096)                                 # block: at or outside the hole wall
    if (~pin & ~blk).any():
        raise Failed('nodes inside the gap: the split by radius is not safe (05-fea.md contact rule 5)')
    crown = blk & (rho < 5.13) & (np.abs(p[:, 0]) < 0.8) & (p[:, 2] > 10)      # the strip along the top of the hole
    press = -r.s[:, 3]                                         # contact pressure there = -sigma_z

    def top(m):
        i = np.flatnonzero(m)[np.argmax(press[m])]
        return round(float(press[i]), 2), p[i].round(2).tolist()
    near = blk & (rho < 8.0) & (p[:, 2] > 10)
    lig = blk & (np.abs(p[:, 2] - 10) < 0.75) & (np.abs(p[:, 0]) > 5.1)
    out = dict(study=r.name, nodes=r.nodes, reaction=r.reaction, applied=r.applied, excessive=bool(r.excessive),
               pin_rise=float(r.disp[pin & (np.abs(p[:, 1]) < 17), 3].mean()),
               p_mid=top(crown & (np.abs(p[:, 1]) < 8)), p_mouth=top(crown & (np.abs(p[:, 1]) > 12)), p_all=top(crown),
               contact_vm=r.peak(near), block_vm=r.peak(blk & (p[:, 2] > 2.0)),
               block_vm_all=round(float(r.vm[blk].max()), 2),
               pin_vm=r.peak(pin & (np.abs(p[:, 1]) < 24.9)),
               lig_force=float(r.s[lig, 3].mean() * 894.0), crown_nodes=int(crown.sum()))
    try:                                                       # exact split of the reaction between block and pads
        q = r.extra
        idpos = dict(zip(r.s[:, 0].astype(int), p))
        keep = np.array([int(i) in idpos for i in q[:, 0]])
        P = np.array([idpos[int(i)] for i in q[keep, 0]])
        out['fz_block'] = float(q[keep][P[:, 2] < 0.01, 3].sum())
        out['fz_pads'] = float(q[keep][np.abs(P[:, 1]) > 26.4, 3].sum())
    except Exception as ex:                                    # logged, and the stiffness estimate is used instead
        log('per-node reaction not read:', str(ex)[:120])
        out['fz_pads_estimate'] = -2 * 0.81 * out['pin_rise']
    return out


if __name__ == '__main__':
    with job() as j:
        j.simulation()
        build(j)
        d = open_doc(j.sw, WIP / 'block_fea.SLDPRT')
        res = []
        for name, hc, nodes in (('T6_PIN_12', 1.2, 40000), ('T6_PIN_08', 0.8, 60000), ('T6_PIN_05', 0.5, 120000)):
            predict(name, nodes, 0.115, 'top of the hole (x 0, z 15.1), pressure about 6.8 MPa, higher toward y +-15')
            r = run(j, d, name, hc)
            compare(name, r, nodes, 0.115)
            res.append(read(r))
            log(json.dumps(res[-1], default=float))
            (HERE / 't6_rows.json').write_text(json.dumps(res, indent=1, default=float), encoding='utf-8')
        q = read(run(j, d, 'T6_PROOF', 1.2, f_each=0.25, loose_ok=True))
        log('PROOF', json.dumps(q, default=float))
        close(j.sw, d)
