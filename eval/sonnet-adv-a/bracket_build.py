"""Rebuild the T1 bracket with a chosen inside-corner radius (None = sharp). Same features, same names, same checks as t1_t2.py."""
import math
from lib3 import *

H = 15.5 * math.cos(math.radians(45))


def build(sw, path, fillet_r=4.0, extra=None, t_up=6.0):
    """Returns the open document. extra(d) may add features before the final checks (ribs for T5, say)."""
    v_fil = (fillet_r ** 2 * (1 - math.pi / 4)) * 50 if fillet_r else 0.0
    hand = (80 * 50 * 6 + t_up * 50 * 40 + v_fil - 4 * math.pi * 2.75 ** 2 * 6 - math.pi * 121 * t_up - 4 * math.pi * 1.7 ** 2 * t_up
            - 2 * 25 * (1 - math.pi / 4) * 6 - 2 * 25 * (1 - math.pi / 4) * t_up)
    d = new_part(sw, path)
    with Sk(d, plane(d, 'Z', 3.0, 'BASE_P'), 'BASE') as s:
        s.rect((0, 0, 3.0), (80, 50, 3.0))
    extrude(d, s.feat, 'BASE', 6.0, mode=MID, expect_dv=80 * 50 * 6); save(d)
    with Sk(d, plane(d, 'Z', 26.0, 'UP_P'), 'UPRIGHT') as s:
        s.rect((0, 0, 26.0), (t_up, 50, 26.0))
    extrude(d, s.feat, 'UPRIGHT', 40.0, mode=MID, expect_dv=t_up * 50 * 40); save(d)
    if fillet_r:
        v0 = volume(d)
        e = edges_where(d, lambda p: abs(p[0] - t_up) < 0.01 and abs(p[2] - 6) < 0.01)
        expect('inside-corner edges', len(e), 1, 0)
        expect('fillet radius built', fillet(d, e, (fillet_r,), 'INSIDE_FILLET') or 0, fillet_r, 0)
        expect('fillet dv', volume(d) - v0, v_fil, 0.01); save(d)
    with Sk(d, plane(d, 'Z', 3.0, 'BH_P'), 'BASE_HOLES') as s:
        for x, y in BASE_HOLES:
            s.circle((x, y, 3.0), 2.75)
    extrude(d, s.feat, 'BASE_HOLES', 10.0, cut=True, mode=MID, expect_dv=4 * math.pi * 2.75 ** 2 * 6); save(d)
    with Sk(d, plane(d, 'X', 3.0, 'BORE_P'), 'BORE') as s:
        s.circle((3.0, 25, 28), 11.0)
    extrude(d, s.feat, 'BORE', 10.0, cut=True, mode=MID, expect_dv=math.pi * 121 * t_up); save(d)
    with Sk(d, plane(d, 'X', 3.0, 'SH_P'), 'SMALL_HOLES') as s:
        for sy in (1, -1):
            for sz in (1, -1):
                s.circle((3.0, 25 + sy * H, 28 + sz * H), 1.7)
    extrude(d, s.feat, 'SMALL_HOLES', 10.0, cut=True, mode=MID, expect_dv=4 * math.pi * 1.7 ** 2 * t_up); save(d)
    v0 = volume(d)
    e = edges_where(d, lambda p: abs(p[0] - 80) < 0.01 and (abs(p[1]) < 0.01 or abs(p[1] - 50) < 0.01))
    expect('base corner edges', len(e), 2, 0)
    expect('R5 base built', fillet(d, e, (5.0,), 'BASE_ROUNDS') or 0, 5.0, 0); save(d)
    e = edges_where(d, lambda p: abs(p[2] - 46) < 0.01 and (abs(p[1]) < 0.01 or abs(p[1] - 50) < 0.01) and -0.01 <= p[0] <= t_up + 0.01)
    expect('upright top edges', len(e), 2, 0)
    expect('R5 upright built', fillet(d, e, (5.0,), 'UPRIGHT_ROUNDS') or 0, 5.0, 0); save(d)
    if extra is None:
        expect('volume', volume(d), hand, 0.002)
        expect('bodies', len(bodies(d)), 1, 0); expect('errors', len(feature_errors(d)), 0, 0)
    else:
        extra(d)
    return d, hand
