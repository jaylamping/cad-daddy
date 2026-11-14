"""T1 bracket build, from plans/A_T1.md section 3. Imported by t1.py (T1), t2.py (T2), t3.py (T3), t4.py (T4), t5.py (T5)."""
from common import *  # noqa: F401,F403

Q = 1 - math.pi / 4
MOTOR_YZ = [(25 + a * 10.960, 28 + b * 10.960) for b in (-1, 1) for a in (-1, 1)]
BASE_XY = [(25, 10), (25, 40), (65, 10), (65, 40)]


def build_bracket(j, path, root_r=4.0):
    """root_r: 4.0 for T1, None for T4's sharp corner, 0.4 for T4's as-printed corner."""
    d = new_part(j.sw, path)
    with Sk(d, plane(d, 'Y', 25.0, 'L_P'), 'L') as s:                      # 1. the L, drawn at mid width
        s.poly([(0, 25, 0), (80, 25, 0), (80, 25, 6), (6, 25, 6), (6, 25, 46), (0, 25, 46)])
    extrude(d, s.feat, 'L', 50.0, mode=MID, expect_dv=36000.0)
    save(d)
    if root_r:                                                              # 2. inside corner
        e = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01)
        must('root edge', len(e), 1)
        v0 = volume(d)
        if fillet(d, e, (root_r,), 'ROOT_R') is None:
            raise Failed('root fillet did not build')
        expect('root fillet dv', volume(d) - v0, Q * root_r ** 2 * 50, 0.01)
        save(d)
    e = edges_where(d, lambda p: abs(p[0] - 80) < 0.01 and min(abs(p[1]), abs(p[1] - 50)) < 0.01)   # 3. base corners
    must('base corner edges', len(e), 2)
    v0 = volume(d)
    if fillet(d, e, (5.0,), 'BASE_R5') is None:
        raise Failed('base rounds did not build')
    expect('base rounds dv', v0 - volume(d), 2 * Q * 25 * 6, 0.01)
    e = edges_where(d, lambda p: abs(p[2] - 46) < 0.01 and min(abs(p[1]), abs(p[1] - 50)) < 0.01)   # 4. upright top corners
    must('upright corner edges', len(e), 2)
    v0 = volume(d)
    if fillet(d, e, (5.0,), 'TOP_R5') is None:
        raise Failed('upright rounds did not build')
    expect('upright rounds dv', v0 - volume(d), 2 * Q * 25 * 6, 0.01)
    save(d)
    with Sk(d, plane(d, 'Z', 3.0, 'BASE_HOLES_P'), 'BASE_HOLES') as s:      # 5. cut Z -0.5..6.5: overshoots into air
        for x, y in BASE_XY:
            s.circle((x, y, 3.0), 2.75)
    extrude(d, s.feat, 'BASE_HOLES', 7.0, cut=True, mode=MID, expect_dv=4 * math.pi * 2.75 ** 2 * 6)
    with Sk(d, plane(d, 'X', 3.0, 'BORE_P'), 'BORE') as s:                  # 6. cut X -0.5..6.5
        s.circle((3.0, 25, 28), 11.0)
    extrude(d, s.feat, 'BORE', 7.0, cut=True, mode=MID, expect_dv=math.pi * 121 * 6)
    with Sk(d, plane(d, 'X', 3.0, 'MOTOR_HOLES_P'), 'MOTOR_HOLES') as s:    # 7.
        for y, z in MOTOR_YZ:
            s.circle((3.0, y, z), 1.7)
    extrude(d, s.feat, 'MOTOR_HOLES', 7.0, cut=True, mode=MID, expect_dv=4 * math.pi * 1.7 ** 2 * 6)
    single_body(d)
    must('rebuild errors', len(feature_errors(d)), 0)
    save(d)
    return d


def hand_volume(root_r=4.0):
    return (36000 + (Q * root_r ** 2 * 50 if root_r else 0) - 4 * Q * 25 * 6
            - 4 * math.pi * 2.75 ** 2 * 6 - math.pi * 121 * 6 - 4 * math.pi * 1.7 ** 2 * 6)
