"""D2 studies: the housing pair in housing_fea.SLDPRT, +Y and +X loads, contact ring-to-seat and half-to-half.
Plan: plans/D_D2.md section 7. Changes from the plan are marked CHANGED (and in REPORT.md).
Run as a script: job 2 solves the first four studies; run it again for job 3 (it skips finished rows)."""
from common import *  # noqa: F401,F403
from swfea import _arr  # noqa: E402

SCREWS = [(x, z) for x in (-30.0, 30.0) for z in (0.0, 7.0)]     # as d2_build.py (CHANGED: not imported, so build never runs)
G2 = 0.4
MATS = {'screw_': STEEL, 'ring': STEEL, 'pad_': SOFT}           # CHANGED: 'ring-' did not match "<ring>-<RINGBORE>"


def per_node_reaction(st, res):
    return _arr(res.GetReactionForcesAndMoments(0, NUL, 0, L()), 9)


def run(j, d, name, force, el, cs, bonded=False):
    d.ForceRebuild3(False)
    mount = pick(d, kind='plane', normal=(0, -1, 0), at=(0, -32, 3.5))
    must('mount face', len(mount), 1)
    up_seat = pick(d, kind='cyl', r=26.1, inside=[-27, 0.3, -0.2, 27, 26.2, 7.2])
    must('upper seat', len(up_seat), 1)
    lo_seat = pick(d, kind='cyl', r=26.1, inside=[-27, -26.2, -0.2, 27, -0.3, 7.2])
    must('lower seat', len(lo_seat), 1)
    ring_out = pick(d, kind='cyl', r=26.0, inside=[-26.05, -26.05, -0.05, 26.05, 26.05, 7.05])
    must('ring outside', len(ring_out), 1)
    sides = pick(d, kind='plane', normal=(0, 0, 1), at=(25, 0, 7)) + pick(d, kind='plane', normal=(0, 0, -1), at=(25, 0, 0))
    must('ring sides', len(sides), 2)
    pad_in = pick(d, kind='cyl', r=22.0)
    must('pad inner faces', len(pad_in), 4)

    def big(fs):
        return [f for f in fs if face_info(f)['area'] > 20]        # leaves out the plug ends (5.5 mm2)
    up_split = big(pick(d, kind='plane', normal=(0, -1, 0), inside=[-36.1, 0.39, -4.1, 36.1, 0.41, 11.1]))
    must('upper split faces', len(up_split), 2)
    lo_split = big(pick(d, kind='plane', normal=(0, 1, 0), inside=[-36.1, -0.41, -4.1, 36.1, -0.39, 11.1]))
    must('lower split faces', len(lo_split), 2)
    small = []
    for r, n in ((1.5, 4), (2.0, 8), (2.75, 4), (3.0, 4), (1.7, 4)):   # shanks, plugs + insert holes, heads, counterbores, clearance
        f = pick(d, kind='cyl', r=r)
        must(f'faces r {r}', len(f), n)
        small += f
    kind = BONDED if bonded else NO_PENETRATION
    r = static(j, d, name, PETG, fixtures=[('fixed', mount), ('fixed', pad_in)],
               loads=[('remote', sides, (0.0, 0.0, 3.5), force, (0, 0, 0))],
               el=el, ctrl=[(up_seat + lo_seat + ring_out, cs), (small, 0.8)],
               contacts=[(kind, ring_out, up_seat), (kind, ring_out, lo_seat), (NO_PENETRATION, up_split, lo_split)],
               materials=MATS, solver=SOLVER_DIRECT, post=per_node_reaction, max_nodes=200_000)
    save_npz(r, name)
    return r


def split(r):
    """Node masks by geometry (05-fea.md contact rule 5). Interface nodes on a bonded screw count as screw."""
    p = r.pos
    rho = np.hypot(p[:, 0], p[:, 1])
    pad = rho < 23.99
    ring = (rho >= 23.99) & (rho <= 26.0005) & (p[:, 2] > -0.001) & (p[:, 2] < 7.001)
    dxz = np.min([np.hypot(p[:, 0] - x, p[:, 2] - z) for x, z in SCREWS], axis=0)
    y = p[:, 1]
    screw = (y >= -6.501) & (y <= 31.501) & ((dxz <= 1.5005) | ((dxz <= 2.0005) & (y <= -G2 + 0.001)) | ((dxz <= 2.7505) & (y >= 28.499)))
    other = ~(pad | ring | screw)
    upper, lower = other & (y > G2 - 0.01), other & (y < -G2 + 0.01)
    if (other & ~upper & ~lower).any():
        raise Failed('nodes between the halves that belong to no body: the split is not safe')
    return dict(pad=pad, ring=ring, screw=screw, dxz=dxz,
                upper=upper & ~((dxz < 3.75) & (y > 27.5)),                       # 1 mm round each bonded head left out
                lower=lower & ~((dxz < 3.0) & (y > -7.5)) & (y > -30.0),          # 1 mm round each bonded plug, 2 mm off the fixed face
                upper_all=upper, lower_all=lower)


def seat_angle(r, m, sgn):
    """Angle in degrees, from the half's own crown toward +X, of the centre of the contact pressure on its seat."""
    p = r.pos
    nx, ny = p[:, 0], p[:, 1] + sgn * 0.1
    d = np.hypot(nx, ny)
    on = m['upper_all' if sgn > 0 else 'lower_all'] & (d < 26.1 + 0.3) & (p[:, 2] > 0) & (p[:, 2] < 7)
    nx, ny = nx[on] / d[on], ny[on] / d[on]
    S = r.s[on]
    press = np.maximum(-(nx * nx * S[:, 1] + ny * ny * S[:, 2] + 2 * nx * ny * S[:, 4]), 0.0)
    if press.sum() < 1e-6:
        return None, 0.0
    return float(np.degrees(np.arctan2((press * nx).sum(), sgn * (press * ny).sum()))), float(press.max())


def read(r):
    m, p = split(r), r.pos
    out = dict(study=r.name, el=r.el, nodes=r.nodes, reaction=[float(v) for v in r.reaction], excessive=bool(r.excessive),
               ring_u=[float(v) for v in r.disp[m['ring'], 1:4].mean(axis=0)], max_disp=r.max_disp(),
               ring_vm=float(r.vm[m['ring']].max()), screw_vm=float(r.vm[m['screw']].max()))
    for h in ('upper', 'lower'):
        out[h] = direction_table(r, m[h])                              # three measures x three print directions, per half
        out[h + '_excluded_vm'] = float(r.vm[m[h + '_all']].max())
    out['screws'] = []
    for x, z in SCREWS:                                                # tension = mean sigma-y over the shank section x its area
        s = (np.hypot(p[:, 0] - x, p[:, 2] - z) <= 1.5005) & (p[:, 1] > 5) & (p[:, 1] < 23)
        out['screws'].append(dict(x=x, z=z, tension=float(r.s[s, 2].mean() * math.pi * 2.25),
                                  shear_x=float(r.s[s, 4].mean() * math.pi * 2.25), nodes=int(s.sum())))
    out['screw_sum'] = float(sum(q['tension'] for q in out['screws']))
    out['angle_upper'], out['p_upper'] = seat_angle(r, m, +1)
    out['angle_lower'], out['p_lower'] = seat_angle(r, m, -1)
    lc = (m['lower_all'] & (np.abs(p[:, 0]) > 3) & (np.abs(p[:, 0]) < 6) & (p[:, 1] < -25)
          & (np.hypot(p[:, 0], p[:, 1]) < 26.3) & (p[:, 2] > 0) & (p[:, 2] < 7))
    out['lower_seat_opens_by'] = float(out['ring_u'][1] - r.disp[lc, 2].mean())   # ring UY minus the lower seat's UY near its crown
    try:
        q = r.extra
        idpos = dict(zip(r.s[:, 0].astype(int), p))
        keep = np.array([int(i) in idpos for i in q[:, 0]])
        P = np.array([idpos[int(i)] for i in q[keep, 0]])
        inpad = np.hypot(P[:, 0], P[:, 1]) < 23.0
        out['pads_reaction'] = [float(v) for v in q[keep][inpad, 1:4].sum(axis=0)]
    except Exception as ex:                                            # logged; the estimate from the pad stiffness is used instead
        log('per-node reaction not read:', str(ex)[:120])
        out['pads_reaction_estimate_N'] = 6.6 * float(np.hypot(out['ring_u'][0], out['ring_u'][1]))
    return out


def one(j, d, rows, name, force, el, cs, nodes, bonded=False):
    predict(name, nodes, 0.1, 'upper half, outer face over the crown (x 0, y 32) or the seat beside it')
    r = run(j, d, name, force, el, cs, bonded)
    compare(name, r, nodes, 0.1)
    rows[name] = read(r)
    log(name, json.dumps(rows[name], default=float))
    (HERE / 'd2_rows.json').write_text(json.dumps(rows, indent=1, default=float), encoding='utf-8')


if __name__ == '__main__':
    f = HERE / 'd2_rows.json'
    rows = json.loads(f.read_text(encoding='utf-8')) if f.exists() else {}
    with job() as j:
        j.simulation()
        d = open_doc(j.sw, WIP / 'housing_fea.SLDPRT')
        if 'D2_Y_30' not in rows:                                      # job 2: four studies
            one(j, d, rows, 'D2_Y_30', (0, 300.0, 0), 3.0, 1.2, 55000)
            one(j, d, rows, 'D2_YBOND_30', (0, 300.0, 0), 3.0, 1.2, 55000, bonded=True)
            one(j, d, rows, 'D2_X_30', (300.0, 0, 0), 3.0, 1.2, 55000)
            one(j, d, rows, 'D2_Y_22', (0, 300.0, 0), 2.2, 0.9, 110000)
        else:                                                          # job 3 (run the script again): three studies
            one(j, d, rows, 'D2_X_22', (300.0, 0, 0), 2.2, 0.9, 110000)
            one(j, d, rows, 'D2_Y_17', (0, 300.0, 0), 1.7, 0.7, 190000)
            one(j, d, rows, 'D2_X_17', (300.0, 0, 0), 1.7, 0.7, 190000)
        close(j.sw, d)
        log('D2 study job done at', minutes(), 'min')
