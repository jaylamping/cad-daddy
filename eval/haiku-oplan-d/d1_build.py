"""D1 build: buck board mount (idea A, chosen), rail and board stand-ins, idea B (crude), each checked against its hand value.

    python eval/haiku-oplan-d/d1_build.py      (one job; plan D_D1 section 3)
"""
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import E, W, save_result  # noqa: E402
from swkit import (BLIND, MID, Sk, bbox, bodies, export, extrude, feature_errors, face_info, job, log,  # noqa: E402
                   new_part, pick, plane, save, single_body, volume)

import trimesh  # noqa: E402


def expect(what, got, want, tol):
    """Absolute or relative (tol < 1) check; raises so the block stops."""
    lim = tol * abs(want) if 0 < tol < 1 and want else tol
    if abs(got - want) > lim:
        raise RuntimeError(f'{what}: got {got:.4f}, want {want:.4f}, allowed {lim:.4f}')
    log(f'ok {what}: {got:.4f} (want {want:.4f})')


SO = [(39, 26.5), (-39, 26.5), (39, -26.5), (-39, -26.5)]      # standoff and insert centres
RAIL = [(20, 0), (-20, 0)]


def mount(j):
    t0 = time.time()
    d = new_part(j.sw, W / 'buck_mount.SLDPRT')
    z25 = plane(d, 'Z', 2.5, 'MID_P')
    with Sk(d, z25, 'SPINE') as s:
        s.rect((-45, -8, 2.5), (45, 8, 2.5))
    extrude(d, s.feat, 'SPINE', 5.0, mode=MID, expect_dv=7200.0)
    with Sk(d, z25, 'ARMS') as s:
        s.rect((34, -30.5, 2.5), (44, 30.5, 2.5))
        s.rect((-44, -30.5, 2.5), (-34, 30.5, 2.5))
    extrude(d, s.feat, 'ARMS', 5.0, mode=MID, expect_dv=4500.0)
    z10 = plane(d, 'Z', 10.0, 'SO_P')
    with Sk(d, z10, 'STANDOFFS') as s:
        for x, y in SO:
            s.circle((x, y, 10.0), 4.0)
    extrude(d, s.feat, 'STANDOFFS', 10.0, mode=MID, expect_dv=4 * math.pi * 16 * 10)
    z12 = plane(d, 'Z', 12.0, 'INS_P')
    with Sk(d, z12, 'INSERT_HOLES') as s:
        for x, y in SO:
            s.circle((x, y, 12.0), 2.0)
    extrude(d, s.feat, 'INSERT_HOLES', 6.0, cut=True, mode=MID, expect_dv=4 * math.pi * 4 * 6)
    with Sk(d, z25, 'RAIL_HOLES') as s:
        for x, y in RAIL:
            s.circle((x, y, 2.5), 2.75)
    extrude(d, s.feat, 'RAIL_HOLES', 7.0, cut=True, mode=MID, expect_dv=2 * math.pi * 2.75 ** 2 * 5)
    single_body(d)
    expect('A feature errors', len(feature_errors(d)), 0, 0)
    V = volume(d)
    expect('A volume mm3', V, 13171.4, 0.001 * 13171.4)
    b = bbox(d)
    for k, want in enumerate((-45, -30.5, 0, 45, 30.5, 15)):
        expect(f'A bbox[{k}]', b[k], want, 0.01)
    # holes measured on the finished solid
    holes = {}
    for label, r in (('rail M5', 2.75), ('insert M3', 2.0)):
        fs = pick(d, kind='cyl', r=r)
        cs = []
        for f in fs:
            bx = face_info(f)['box']
            cs.append(((bx[0] + bx[3]) / 2, (bx[1] + bx[4]) / 2))
        holes[label] = cs
        log(label, 'faces', len(fs), 'centres', [(round(x, 3), round(y, 3)) for x, y in cs])
    expect('A rail hole faces', len(holes['rail M5']), 2, 0)
    expect('A insert hole faces', len(holes['insert M3']), 4, 0)
    for x, y in RAIL:
        ok = any(math.hypot(x - a, y - bb) < 0.02 for a, bb in holes['rail M5'])
        if not ok:
            raise RuntimeError(f'rail hole at {(x, y)} not found')
    save(d)
    export(j.sw, d, W / 'buck_mount.step')
    export(j.sw, d, W / 'buck_mount.stl')
    step_txt = (W / 'buck_mount.step').read_text(errors='ignore')
    units_ok = any('.MILLI.' in ln and 'SI_UNIT' in ln for ln in step_txt.splitlines())
    mesh = trimesh.load(W / 'buck_mount.stl')
    stl_vol = float(mesh.volume)
    rowA = dict(volume_mm3=round(V, 2), mass_g=round(V * 1.19e-3, 3), bodies=len(bodies(d)),
                stl_watertight=bool(mesh.is_watertight), stl_shells=len(mesh.split(only_watertight=False)),
                stl_volume_mm3=round(stl_vol, 2), stl_volume_ok=abs(stl_vol - V) / V <= 0.005,
                step_units_mm=units_ok, minutes=round((time.time() - t0) / 60, 2))
    log('A:', rowA)
    return rowA


def standins(j):
    d = new_part(j.sw, W / 'rail.SLDPRT')
    with Sk(d, plane(d, 'Z', -10.0, 'RAIL_P'), 'RAIL') as s:
        s.rect((-60, -10, -10.0), (60, 10, -10.0))
    extrude(d, s.feat, 'RAIL', 20.0, mode=MID, expect_dv=48000.0)
    with Sk(d, plane(d, 'Z', -3.0, 'SLOT_P'), 'SLOT') as s:
        s.rect((-60, -3, -3.0), (60, 3, -3.0))
    extrude(d, s.feat, 'SLOT', 6.0, cut=True, mode=MID, expect_dv=120 * 6 * 6.0)
    save(d)
    export(j.sw, d, W / 'rail.stl')
    d = new_part(j.sw, W / 'board.SLDPRT')
    with Sk(d, plane(d, 'Z', 15.8, 'BOARD_P'), 'BOARD') as s:
        s.rect((-42.5, -30, 15.8), (42.5, 30, 15.8))
    extrude(d, s.feat, 'BOARD', 1.6, mode=MID, expect_dv=85 * 60 * 1.6)
    with Sk(d, plane(d, 'Z', 15.8, 'BHOLE_P'), 'BHOLES') as s:
        for x, y in SO:
            s.circle((x, y, 15.8), 1.6)
    extrude(d, s.feat, 'BHOLES', 3.0, cut=True, mode=MID, expect_dv=4 * math.pi * 1.6 ** 2 * 1.6)
    save(d)
    export(j.sw, d, W / 'board.stl')
    d = new_part(j.sw, W / 'parts.SLDPRT')
    with Sk(d, plane(d, 'Z', 23.6, 'PARTS_P'), 'PARTS') as s:
        s.rect((-35, -22, 23.6), (35, 22, 23.6))
    # the envelope block: a plane in the middle of its height, a mid-plane extrude of its full height
    extrude(d, s.feat, 'PARTS', 14.0, mode=MID, expect_dv=70 * 44 * 14.0)
    save(d)
    export(j.sw, d, W / 'parts.stl')
    log('stand-ins written')


def idea_b(j):
    """Idea B, crude: base plate, two posts, a groove on each post's inner face. Its top is at Z 70 (over the envelope)."""
    d = new_part(j.sw, W / 'idea_b.SLDPRT')
    with Sk(d, plane(d, 'Z', 2.5, 'BASE_P'), 'BASE') as s:
        s.rect((-50, -8, 2.5), (50, 8, 2.5))
    extrude(d, s.feat, 'BASE', 5.0, mode=MID, expect_dv=8000.0)
    z37 = plane(d, 'Z', 37.5, 'POST_P')
    with Sk(d, z37, 'POSTS') as s:
        s.rect((43, -6, 37.5), (49, 6, 37.5))
        s.rect((-49, -6, 37.5), (-43, 6, 37.5))
    extrude(d, s.feat, 'POSTS', 65.0, mode=MID, expect_dv=2 * 6 * 12 * 65.0)
    for name, xp in (('GROOVE_PX', 44.0), ('GROOVE_NX', -44.0)):
        with Sk(d, plane(d, 'X', xp, name + '_P'), name) as s:
            s.rect((xp, -1, 7.0), (xp, 1, 70.0))
        extrude(d, s.feat, name, 2.0, cut=True, mode=MID, expect_dv=2 * 2 * 63.0)
    save(d)
    expect('idea B volume', volume(d), 8000 + 2 * 4680 - 2 * 252, 0.001 * 13000)
    b = bbox(d)
    log('idea B box', [round(v, 2) for v in b])
    export(j.sw, d, W / 'idea_b.stl')
    log('idea B exported; top Z', round(b[5], 2), 'over envelope by', round(b[5] - 45, 2))


def main():
    t0 = time.time()
    rows = {}
    with job() as j:
        rows['A'] = mount(j)
        standins(j)
        idea_b(j)
    log('part A and stand-ins in', round((time.time() - t0) / 60, 2), 'min')


if __name__ == '__main__':
    main()
