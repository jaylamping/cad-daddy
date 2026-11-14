"""T3 helpers, from plans/A_T3.md section 3. Used by T3 (t3_job1.py, t3_job2.py), T4 and T5."""
from bracket import *  # noqa: F401,F403


def make_disc(j, path, axis, centre, r, lo, hi, feat):
    """A solid disc along model axis 'X' or 'Z' from lo to hi; centre = the other two coordinates in x, y, z order."""
    d = new_part(j.sw, path)
    mid = (lo + hi) / 2
    c = (mid, centre[0], centre[1]) if axis == 'X' else (centre[0], centre[1], mid)
    with Sk(d, plane(d, axis, mid, feat + '_P'), feat) as s:
        s.circle(c, r)
    extrude(d, s.feat, feat, hi - lo, mode=MID, expect_dv=math.pi * r * r * (hi - lo))
    save(d)
    close(j.sw, d)


def make_parts(j):
    for k, (y, z) in enumerate(MOTOR_YZ):
        make_disc(j, WIP / f'pad_{k + 1}.SLDPRT', 'X', (y, z), 3.5, -1.0, 0.0, 'PRESSPAD')     # 38.48 mm3 each
    for k, (x, y) in enumerate(BASE_XY):
        make_disc(j, WIP / f'washer_{k + 1}.SLDPRT', 'Z', (x, y), 5.0, 6.0, 7.0, 'WASHER')    # 78.54 mm3 each


def make_twin(j, src, dst, washers=False):
    d = open_doc(j.sw, src)
    v = volume(d)
    save_as(d, dst)
    for k in range(4):
        insert_body(d, WIP / f'pad_{k + 1}.SLDPRT')
    if washers:
        for k in range(4):
            insert_body(d, WIP / f'washer_{k + 1}.SLDPRT')
    bs = bodies(d)
    log(bs)
    must('bodies in ' + Path(dst).name, len(bs), 9 if washers else 5)
    expect('bracket body is the same part', max(b[1] for b in bs), v, 0.0001)
    save(d)
    close(j.sw, d)


def run(j, d, name, el, c, load='pads', fix='walls', root=4.0, root_c=None):
    """One study. load 'pads' (150 N even pressure on the four pads) or 'remote' (rigid, on the bore).
    fix 'walls' (base hole walls) or 'washers' (washer tops). root: the corner fillet radius, or None for the sharp
    corner, whose edge then gets the control root_c."""
    d.ForceRebuild3(False)
    walls = pick(d, kind='cyl', r=2.75)
    must('base hole walls', len(walls), 4)
    bore = pick(d, kind='cyl', r=11.0)
    must('bore', len(bore), 1)
    mh = pick(d, kind='cyl', r=1.7)
    must('motor holes', len(mh), 4)
    pads = pick(d, kind='plane', normal=(-1, 0, 0), inside=[-1.01, -1, -1, -0.99, 51, 47])
    must('pad outer faces', len(pads), 4)
    if root:
        rf = pick(d, kind='cyl', r=root, inside=[5.9, -0.1, 5.9, 6.1 + root, 50.1, 6.1 + root])
        must('root fillet', len(rf), 1)
    else:
        rf = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01)
        must('root edge', len(rf), 1)
    mats = {'pad_': PRESS}
    if fix == 'washers':
        tops = pick(d, kind='plane', normal=(0, 0, 1), inside=[19, 4, 6.99, 71, 46, 7.01])
        must('washer tops', len(tops), 4)
        fixtures, mats = [('fixed', tops)], {'pad_': PRESS, 'washer_': STEEL}
    else:
        fixtures = [('fixed', walls)]
    loads = ([('normal', pads, 150.0)] if load == 'pads' else
             [('remote', bore, (3.0, 25.0, 28.0), (150.0, 0, 0), (0, 0, 0))])
    r = static(j, d, name, PETG, fixtures, loads, el=el, ctrl=[(mh + bore, c), (rf, root_c or c)], materials=mats,
               loose_ok=True, max_nodes=200_000)
    save_npz(r, name)
    return r


# ---- reading a result ------------------------------------------------------------------------------------------------

def body_mask(r):
    """Bracket nodes only: pads are at x < 0, washers at z > 6 over the base (the bracket has nothing there beyond x 10)."""
    p = r.pos
    return (p[:, 0] > -1e-4) & ~((p[:, 2] > 6.0001) & (p[:, 0] > 15))


def clear_of_fix(r, D, rad=2.75):
    """Nodes at least D mm from the fixed base holes (rad 2.75) or from the washer rims (rad 5.0)."""
    p = r.pos
    dh = np.min([np.hypot(p[:, 0] - x, p[:, 1] - y) for x, y in BASE_XY], axis=0) - rad
    return (p[:, 2] > 6.0001) | (dh >= D)


def rim(r, which=MOTOR_YZ[:2], w=1.5):
    """Nodes within w mm of the walls of the two LOWER motor holes (z 17.04): where the hand value says it fails."""
    p = r.pos
    return body_mask(r) & (np.min([np.hypot(p[:, 1] - y, p[:, 2] - z) for y, z in which], axis=0) <= 1.7 + w)


def checks(r):
    p = r.pos
    back = (p[:, 0] > -1e-4) & (p[:, 0] < 0.05) & (np.abs(p[:, 2] - 12) < 0.5)
    bot = (np.abs(p[:, 2]) < 0.05) & (p[:, 0] > 12) & (p[:, 0] < 18)
    return dict(reaction=r.reaction, applied=r.applied, max_disp=r.max_disp(), excessive=bool(r.excessive),
                top_ux=float(r.disp[p[:, 2] > 45.9, 1].mean()),
                sz_back_z12=float(r.s[back, 3].mean()), sx_bottom_x15=float(r.s[bot, 1].mean()),
                nodes_in_checks=(int(back.sum()), int(bot.sum())))


def row(r, D=3.0, rad=2.75):
    """Everything T3, T4 and T5 report from one result."""
    bm = body_mask(r)
    m = bm & clear_of_fix(r, D, rad)
    z = measures(r, m, (0, 0, 1))
    return dict(study=r.name, el=r.el, nodes=r.nodes, D=D, table=direction_table(r, m),
                rim_layer_z=round(r.layer_stress((0, 0, 1), rim(r))[0], 2), rim_vm=round(r.peak(rim(r))[0], 2),
                vm_all=round(float(r.vm[bm].max()), 2),
                plateau={k: (round(r.peak(bm & clear_of_fix(r, k, rad))[0], 2),
                             round(r.layer_stress((0, 0, 1), bm & clear_of_fix(r, k, rad))[0], 2)) for k in (1, 2, 3, 5)},
                flat=[r.el, r.nodes, z['vm'], z['layer'], z['shear']], checks=checks(r))
