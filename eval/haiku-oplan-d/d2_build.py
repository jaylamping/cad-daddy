"""D2 build: split housing round a 6808-2RS bearing (plan D_D2 section 3), with the spec fixes of section 5.

    python eval/haiku-oplan-d/d2_build.py     (one job)

Built as the plan says, with the five spec changes (REPORT.md): shoulder opening Ø46.0, screws at X ±31.0 and Z -0.2 / 7.2,
split gap 0.8 (faces at Y ±0.4), seat Ø52.0 at Z -0.1..7.1.
"""
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import W, save_result  # noqa: E402
from swkit import (BLIND, MID, Sk, bbox, bodies, export, extrude, feature_errors, face_info, insert_body, job, log,  # noqa: E402
                   new_part, open_doc, pick, plane, revolve, save, save_as, single_body, volume)

import trimesh  # noqa: E402

SEAT_R = 26.0            # Ø52.0
SHOULDER_R = 23.0        # Ø46.0 (spec Ø43.5 would rub the inner ring Ø44.0)
SCREWS = [(31.0, -0.2), (31.0, 7.2), (-31.0, -0.2), (-31.0, 7.2)]     # (X, Z); axis along Y
SPLIT = 0.4              # faces at Y ±0.4 (gap 0.8)


def expect(what, got, want, tol):
    lim = tol * abs(want) if 0 < tol < 1 and want else tol
    if abs(got - want) > lim:
        raise RuntimeError(f'{what}: got {got:.4f}, want {want:.4f}, allowed {lim:.4f}')
    log(f'ok {what}: {got:.4f} (want {want:.4f})')


def half(j, name, side):
    """side -1: lower (Y -32..-0.4); +1: upper (Y 0.4..32)."""
    y0, y1 = (-32.0, -SPLIT) if side < 0 else (SPLIT, 32.0)
    d = new_part(j.sw, W / f'{name}.SLDPRT')
    with Sk(d, plane(d, 'Z', 3.5, 'BLOCK_P'), 'BLOCK') as s:
        s.rect((-36, y0, 3.5), (36, y1, 3.5))
    extrude(d, s.feat, 'BLOCK', 15.0, mode=MID, expect_dv=72 * 31.6 * 15.0)
    with Sk(d, plane(d, 'Z', 3.5, 'SEAT_P'), 'SEAT') as s:
        s.circle((0, 0, 3.5), SEAT_R)
    extrude(d, s.feat, 'SEAT', 7.2, cut=True, mode=MID, expect_dv=7495.63)
    with Sk(d, plane(d, 'Z', 3.5, 'SH_P'), 'SHOULDER') as s:
        s.circle((0, 0, 3.5), SHOULDER_R)
    extrude(d, s.feat, 'SHOULDER', 20.0, cut=True, mode=MID, expect_dv=6337.91)
    if side < 0:
        # the insert holes for the four M3 screws (heat-set inserts Ø4.0, 6 deep from the split face)
        with Sk(d, plane(d, 'Y', -3.4, 'INS_P'), 'INSERTS') as s:
            for x, z in SCREWS:
                s.circle((x, -3.4, z), 2.0)
        extrude(d, s.feat, 'INSERTS', 6.0, cut=True, mode=MID, expect_dv=4 * math.pi * 2.0 ** 2 * 6.0)
        with Sk(d, plane(d, 'Y', -28.0, 'MNT_P'), 'MOUNTS') as s:
            for x in (-24.0, 24.0):
                s.circle((x, -28.0, 3.5), 2.8)
        extrude(d, s.feat, 'MOUNTS', 8.0, cut=True, mode=MID, expect_dv=2 * math.pi * 2.8 ** 2 * 8)
    else:
        with Sk(d, plane(d, 'Y', 16.2, 'HOLE_P'), 'HOLES') as s:
            for x, z in SCREWS:
                s.circle((x, 16.2, z), 1.7)
        extrude(d, s.feat, 'HOLES', 34.0, cut=True, mode=MID, expect_dv=4 * math.pi * 1.7 ** 2 * 31.6)
        with Sk(d, plane(d, 'Y', 30.25, 'CB_P'), 'CBORES') as s:
            for x, z in SCREWS:
                s.circle((x, 30.25, z), 3.0)
        extrude(d, s.feat, 'CBORES', 3.5, cut=True, mode=MID, expect_dv=4 * math.pi * (9 - 1.7 ** 2) * 3.5)
    single_body(d)
    expect(f'{name} feature errors', len(feature_errors(d)), 0, 0)
    return d


def main():
    t0 = time.time()
    res = {}
    with job() as j:
        d = half(j, 'housing_lower', -1)
        save(d)
        export(j.sw, d, W / 'housing_lower.stl')
        V_lo = volume(d)
        expect('lower volume mm3', V_lo, 19598.8, 0.001 * 19598.8)
        expect('lower bbox ymin', bbox(d)[1], -32.0, 0.01)
        res['lower_volume_mm3'] = round(V_lo, 2)
        d = half(j, 'housing_upper', +1)
        save(d)
        export(j.sw, d, W / 'housing_upper.stl')
        V_up = volume(d)
        expect('upper volume mm3', V_up, 18878.1, 0.001 * 18878.1)
        res['upper_volume_mm3'] = round(V_up, 2)
        # the steel ring that stands in for the outer race: Ø52 x 7 OD ring, ID 48, revolved about Z
        d = new_part(j.sw, W / 'ring.SLDPRT')
        with Sk(d, plane(d, 'Y', 0.0, 'RING_P'), 'RING') as s:
            s.rect((24, 0, 0), (26, 0, 7))
            s.centerline((0, 0, -5), (0, 0, 12))
        revolve(d, s.feat, 'RING', expect_dv=2199.11)
        save(d)
        export(j.sw, d, W / 'ring.stl')
        expect('ring volume', volume(d), 2199.11, 0.001 * 2199.11)
        # four screw pins: plug in the insert, shank in the clearance hole, head on the counterbore floor
        for n, (x0, z0) in enumerate(SCREWS, 1):
            d = new_part(j.sw, W / f'screw_{n}.SLDPRT')
            with Sk(d, plane(d, 'Z', z0, f'SCREW{n}_P'), f'SCREW{n}') as s:
                s.poly([(x0, -6.4, z0), (x0 + 2, -6.4, z0), (x0 + 2, -0.4, z0), (x0 + 1.5, -0.4, z0),
                        (x0 + 1.5, 28.5, z0), (x0 + 2.75, 28.5, z0), (x0 + 2.75, 31.5, z0), (x0, 31.5, z0)])
                s.centerline((x0, -10, z0), (x0, 35, z0))
            revolve(d, s.feat, 'PIN', expect_dv=350.96)
            save(d)
            expect(f'screw {n} volume (plan 350.96, 0.5% tolerance)', volume(d), 350.96, 0.005 * 350.96)
        # two soft pads, between the ring's inside and the housings' seat, 4.3 degrees each
        for name, x0, x1 in (('pad_px', 23.0, 24.0), ('pad_nx', -24.0, -23.0)):
            d = new_part(j.sw, W / f'{name}.SLDPRT')
            with Sk(d, plane(d, 'Y', 0.0, f'{name.upper()}_P'), name.upper()) as s:
                s.rect((x0, 0, 3.0), (x1, 0, 4.0))
                s.centerline((0, 0, 0), (0, 0, 10))
            revolve(d, s.feat, 'PAD', angle=4.3, mid=True, min_dv=0.5, expect_dv=1.764)
            save(d)
        # the assembly for the study: lower half, then the other bodies brought in
        d = open_doc(j.sw, W / 'housing_lower.SLDPRT')
        save_as(d, W / 'd2_fea.SLDPRT')
        insert_body(d, W / 'housing_upper.SLDPRT')
        insert_body(d, W / 'ring.SLDPRT')
        for n in range(1, 5):
            insert_body(d, W / f'screw_{n}.SLDPRT')
        insert_body(d, W / 'pad_px.SLDPRT')
        insert_body(d, W / 'pad_nx.SLDPRT')
        d.ForceRebuild3(False)
        save(d)
        nb = len(bodies(d))
        expect('bodies in d2_fea (2 halves + ring + 4 screws + 2 pads; the plan says 10, which is a miscount)', nb, 9, 0)
        vt = volume(d)
        expect('total volume of the 9 bodies (mm3)', vt, 42083.4, 0.001 * 42083.4)
        res['bodies'] = nb
        res['total_volume_mm3'] = round(vt, 2)
        log('bodies:', [(b[0], b[1]) for b in bodies(d)])
    res['minutes_build'] = round((time.time() - t0) / 60, 2)
    save_result('D2_build', res)
    log('D2 build done', res)


if __name__ == '__main__':
    main()
