"""D1 job 1: idea A crude model, board and rail stand-ins, idea B, the chosen mount, its checks and exports.
Plan: plans/D_D1.md section 6. Changes from the plan are marked CHANGED and explained in REPORT.md."""
from common import *  # noqa: F401,F403

Q = 1 - math.pi / 4


def spine_arms(d):
    with Sk(d, plane(d, 'Z', 2.0, 'SPINE_P'), 'SPINE') as s:
        s.rect((-56, -7, 2.0), (56, 7, 2.0))
    extrude(d, s.feat, 'SPINE', 4.0, mode=MID, expect_dv=112 * 14 * 4)
    for name, x in (('ARM_A', 39.0), ('ARM_B', -39.0)):
        with Sk(d, plane(d, 'X', x, name + '_P'), name) as s:      # the arm with its two pads, as one profile
            s.poly([(x, -30, 0), (x, 30, 0), (x, 30, 9), (x, 23, 9), (x, 23, 4), (x, -23, 4), (x, -23, 9), (x, -30, 9)])
        extrude(d, s.feat, name, 8.0, mode=MID, expect_dv=310 * 8 - 448)
    single_body(d)
    save(d)


def build_mount(j, path, crude=False):
    d = new_part(j.sw, path)
    spine_arms(d)
    expect('crude volume', volume(d), 10336.0, 0.001)
    if crude:
        return d
    e = edges_where(d, lambda p: abs(abs(abs(p[0]) - 39) - 4) < 0.01 and abs(abs(p[1]) - 7) < 0.01)
    must('arm-to-spine corner edges', len(e), 8)
    v0 = volume(d)
    if fillet(d, e, (3.0,), 'ROOT_R3') is None:
        raise Failed('ROOT_R3 did not build')
    expect('ROOT_R3 dv', volume(d) - v0, 8 * Q * 9 * 4, 0.02)
    e = edges_where(d, lambda p: abs(abs(p[1]) - 23) < 0.01 and abs(p[2] - 4) < 0.01)
    must('pad step edges', len(e), 4)
    v0 = volume(d)
    if fillet(d, e, (2.5,), 'STEP_R25') is None:
        raise Failed('STEP_R25 did not build')
    expect('STEP_R25 dv', volume(d) - v0, 4 * Q * 6.25 * 8, 0.02)
    with Sk(d, plane(d, 'Z', 2.0, 'M5_P'), 'M5') as s:
        s.circle((50, 0, 2.0), 2.75)
        s.circle((-50, 0, 2.0), 2.75)
    extrude(d, s.feat, 'M5', 5.0, cut=True, mode=MID, expect_dv=2 * math.pi * 2.75 ** 2 * 4)
    with Sk(d, plane(d, 'Z', 6.5, 'INSERT_P'), 'INSERT') as s:
        for x in (39, -39):
            for y in (26.5, -26.5):
                s.circle((x, y, 6.5), 2.0)
    extrude(d, s.feat, 'INSERT', 7.0, cut=True, mode=MID, expect_dv=4 * math.pi * 4 * 6)
    single_body(d)
    must('rebuild errors', len(feature_errors(d)), 0)
    save(d)
    return d


def box_part(j, path, steps):
    """steps: [(feature, axis, lo corner, hi corner, cut)]: boxes extruded mid-plane along axis; returns the open doc."""
    d = new_part(j.sw, path)
    for feat, axis, lo, hi, cut in steps:
        i = 'XYZ'.index(axis)
        mid = (lo[i] + hi[i]) / 2
        a, b = list(lo), list(hi)
        a[i] = b[i] = mid
        with Sk(d, plane(d, axis, mid, feat + '_P'), feat) as s:
            s.rect(tuple(a), tuple(b))
        extrude(d, s.feat, feat, hi[i] - lo[i], cut=cut, mode=MID)
    save(d)
    return d


with job() as j:
    # checkpoint models first: crude idea A, stand-ins, crude idea B
    d = build_mount(j, WIP / 'idea_a.SLDPRT', crude=True)
    export(j.sw, d, WIP / 'idea_a.stl')
    close(j.sw, d)
    log('CHECKPOINT idea A crude volume (checked above, 10336 mm3) at', minutes(), 'min')

    d = box_part(j, WIP / 'board_standin.SLDPRT', [
        ('BOARD', 'Z', (-42.5, -30, 9.0), (42.5, 30, 10.6), False),
        ('TOP_PARTS', 'Z', (-34, -21, 10.4), (34, 21, 24.6), False),      # 14 mm above the board, 0.2 into it
        ('BOTTOM_PARTS', 'Z', (-34, -21, 6.0), (34, 21, 9.2), False)])    # 3 mm below
    with Sk(d, plane(d, 'Z', 9.8, 'BH_P'), 'BOARD_HOLES') as s:
        for x in (39, -39):
            for y in (26.5, -26.5):
                s.circle((x, y, 9.8), 1.6)
    extrude(d, s.feat, 'BOARD_HOLES', 2.6, cut=True, mode=MID, expect_dv=4 * math.pi * 1.6 ** 2 * 1.6)
    must('board bodies', len(bodies(d)), 1)
    export(j.sw, d, WIP / 'board_standin.stl')
    close(j.sw, d)

    d = box_part(j, WIP / 'rail_standin.SLDPRT', [
        ('RAIL', 'X', (-75, -10, -20), (75, 10, 0), False),
        ('SLOT', 'X', (-75.5, -3, -6), (75.5, 3, 0.5), True)])
    export(j.sw, d, WIP / 'rail_standin.stl')
    close(j.sw, d)

    # idea B: concept only (plan branch: drop expect_dv if it fails; 3 minutes at most)
    d = box_part(j, WIP / 'idea_b.SLDPRT', [
        ('SPINE', 'Z', (-56, -7, 0), (56, 7, 4), False),
        ('ARM_A', 'Z', (25, -32.5, 0), (35, 32.5, 4), False),
        ('ARM_B', 'Z', (-35, -32.5, 0), (-25, 32.5, 4), False)])
    for name, sgn in (('RAIL_P', 1), ('RAIL_N', -1)):                   # C-channel along X, profile in plane X 0
        with Sk(d, plane(d, 'X', 0.0, name + '_PL'), name) as s:      # CHANGED: plane given a name (plan had '')
            s.poly([(0, sgn * y, z) for y, z in ((24, 3), (32.5, 3), (32.5, 13.5), (27.5, 13.5), (27.5, 11),
                                                  (30.4, 11), (30.4, 9), (24, 9))])
        extrude(d, s.feat, name, 85.0, mode=MID, expect_dv=67.7 * 85 - 170)
    log('idea B', volume(d), 'mm3 (hand 21521),', round(volume(d) * DENS_G_MM3, 1), 'g, bodies', len(bodies(d)))
    export(j.sw, d, WIP / 'idea_b.stl')
    close(j.sw, d)

    # the chosen part
    d = build_mount(j, WIP / 'buck_mount.SLDPRT')
    expect('mount volume', volume(d), 9949.07, 0.001)
    for got, want in zip(bbox(d), (-56, -30, 0, 56, 30, 9)):
        expect('box', got, want, 0.01)
    m5 = holes(d, 2.75)
    must('M5 holes', len(m5), 2)
    log('M5 at', [h[1] for h in m5])
    ins = holes(d, 2.0)
    must('insert holes', len(ins), 4)
    log('inserts', [(h[1], h[2]) for h in ins])
    for h in ins:
        expect('insert x', abs(h[1][0]), 39.0, 0.02)
        expect('insert y', abs(h[1][1]), 26.5, 0.02)
        expect('insert floor z', h[2][2], 3.0, 0.02)
        expect('insert top z', h[2][5], 9.0, 0.02)
    must('R3 faces', len(holes(d, 3.0)), 8)
    must('R2.5 faces', len(holes(d, 2.5)), 4)
    export(j.sw, d, WIP / 'buck_mount.step')
    export(j.sw, d, WIP / 'buck_mount.stl')
    check_export(d, WIP / 'buck_mount.stl', WIP / 'buck_mount.step')
    close(j.sw, d)
    log('D1 job 1 done at', minutes(), 'min')
