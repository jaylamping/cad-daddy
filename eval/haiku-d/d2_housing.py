"""D2: two printed halves round a 6808-2RS bearing, built as the nearest thing to the spec that can work (see REPORT).

Changes from the written spec (each with its number; all are in the report):
  S1 screw centres X ±28.2 -> X ±30.0. At 28.2 the Ø3.4 hole edge is 0.5 mm from the seat (r 26) and the Ø4.0 insert hole
     edge is 0.2 mm from it. At 30.0 the walls are 2.2 mm.
  S2 seat Ø52.0 -> Ø51.6. Ring OD is 52.0, so Ø52.0 is zero fit and the printer's ±0.15 mm could give either a loose or
     a too-tight seat. Ø51.6 is 0.4 mm of interference nominal, a press fit that holds the ring.
  S3 shoulder opening Ø43.5 -> Ø44.4. The inner ring is 44.0 across the outside, so Ø43.5 rubs the turning inner ring
     on its end face. Ø44.4 clears it by 0.2 mm and still carries the outer ring's end face (r 24 to 25.8).
  S4 split gap: not given. 0.4 mm built (0.2 mm each half), so the halves can close on the ring.
  S5 screw heights Z 1 and 6 -> Z 0.5 and 7.5. Two Ø6 counterbores 5 mm apart overlap by 1 mm and SolidWorks refuses the
     cut (checked: the same cut at 6 mm spacing or with Ø2 holes builds). 7 mm spacing leaves a 1 mm web.
Split plane Y 0 (the gap is Y -0.2..0.2). Bearing axis Z.
"""
import sys
from pathlib import Path
WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT / 'solidworks'))
from swkit import (BLIND, MID, Sk, bbox, bodies, close, expect, export, extrude, feature_errors, job, log,  # noqa: E402
                   new_part, plane, save, single_body, volume)

OUT = WT / '_wip' / 'sw-eval' / 'haiku-d' / 'd2'
OUT.mkdir(parents=True, exist_ok=True)
SEAT_R, OPEN_R, SCREW_X, GAP = 25.8, 22.2, 30.0, 0.2       # seat Ø51.6, shoulder opening Ø44.4, screws at ±30, half-gap 0.2
SCREW_Z = (0.5, 7.5)      # S5: spec Z 1 and 6 put the two Ø6 counterbores 5 mm apart: they overlap by 1 mm
PI = 3.141592653589793


def half(j, name, upper):
    """One half: block X ±36, Z -4..11, Y 0.2..32 (upper) or -32..-0.2 (lower), minus the seat and the shoulder opening."""
    d = new_part(j.sw, OUT / f'housing_{name}.SLDPRT')
    y0, y1 = (GAP, 32.0) if upper else (-32.0, -GAP)
    ym = (y0 + y1) / 2
    depth = y1 - y0
    with Sk(d, plane(d, 'Y', ym, f'{name}_BLK_P'), f'{name}_BLK') as s:
        s.rect((-36.0, ym, -4.0), (36.0, ym, 11.0))
    extrude(d, s.feat, f'{name}_BLK', depth, mode=MID, expect_dv=72 * 15 * depth)
    with Sk(d, plane(d, 'Z', 3.5, f'{name}_SEAT_P'), f'{name}_SEAT') as s:
        s.circle((0, 0, 3.5), SEAT_R)
    extrude(d, s.feat, f'{name}_SEAT', 7.0, cut=True, mode=MID)
    with Sk(d, plane(d, 'Z', 3.5, f'{name}_OPEN_P'), f'{name}_OPEN') as s:
        s.circle((0, 0, 3.5), OPEN_R)
    extrude(d, s.feat, f'{name}_OPEN', 15.0, cut=True, mode=MID)
    save(d)
    return d, y0, y1


def screw_holes(d, name, upper, y0, y1):
    if upper:
        # Ø3.4 clearance through the upper half, Ø6 counterbore 3.5 deep from Y 32
        with Sk(d, plane(d, 'Y', 16.1, f'{name}_CL_P'), f'{name}_CL') as s:
            for x in (-SCREW_X, SCREW_X):
                for z in SCREW_Z:
                    s.circle((x, 16.1, z), 1.7)
        extrude(d, s.feat, f'{name}_CL', 40.0, cut=True, mode=MID)
        # Ø6 counterbore Y 28.5 to 32: a mid-plane cut of 4.5 at Y 30.75 (reaches to 33, the end face is at 32)
        with Sk(d, plane(d, 'Y', 30.75, f'{name}_CB_P'), f'{name}_CB') as s:
            for x in (-SCREW_X, SCREW_X):
                for z in SCREW_Z:
                    s.circle((x, 30.75, z), 3.0)
        extrude(d, s.feat, f'{name}_CB', 4.5, cut=True, mode=MID, expect_dv=4 * PI * (3.0 ** 2 - 1.7 ** 2) * 3.5)
    else:
        # Ø4.0 heat-set hole 6 deep from the split face, and Ø5.6 M4 insert holes 8 deep from the mount face Y -32
        with Sk(d, plane(d, 'Y', -3.2, f'{name}_INS_P'), f'{name}_INS') as s:
            for x in (-SCREW_X, SCREW_X):
                for z in SCREW_Z:
                    s.circle((x, -3.2, z), 2.0)
        extrude(d, s.feat, f'{name}_INS', 6.0, cut=True, mode=MID, expect_dv=4 * PI * 2.0 ** 2 * 6)
        with Sk(d, plane(d, 'Y', -28.0, f'{name}_MNT_P'), f'{name}_MNT') as s:
            for x in (-24.0, 24.0):
                s.circle((x, -28.0, 3.5), 2.8)
        extrude(d, s.feat, f'{name}_MNT', 8.0, cut=True, mode=MID, expect_dv=2 * PI * 2.8 ** 2 * 8)
    save(d)


def ring(j):
    d = new_part(j.sw, OUT / 'ring.SLDPRT')
    with Sk(d, plane(d, 'Z', 3.5, 'RING_P'), 'RING') as s:
        s.circle((0, 0, 3.5), 26.0)
        s.circle((0, 0, 3.5), 24.0)
    extrude(d, s.feat, 'RING', 7.0, mode=MID, expect_dv=PI * (26 ** 2 - 24 ** 2) * 7)
    save(d)
    return d


if __name__ == '__main__':
    # new_part() closes every open document, so each part is exported and closed before the next one is made
    res = {}
    with job(wait_s=1800) as j:
        du, y0, y1 = half(j, 'upper', True)
        screw_holes(du, 'upper', True, y0, y1)
        res['upper_volume_mm3'] = volume(du)
        log('upper', bodies(du), 'feature errors', feature_errors(du))
        export(j.sw, du, OUT / 'housing_upper.stl')
        export(j.sw, du, OUT / 'housing_upper.step')
        close(j.sw, du)
        dl, y0, y1 = half(j, 'lower', False)
        screw_holes(dl, 'lower', False, y0, y1)
        res['lower_volume_mm3'] = volume(dl)
        log('lower', bodies(dl), 'feature errors', feature_errors(dl))
        export(j.sw, dl, OUT / 'housing_lower.stl')
        export(j.sw, dl, OUT / 'housing_lower.step')
        close(j.sw, dl)
        dr = ring(j)
        res['ring_volume_mm3'] = volume(dr)
        export(j.sw, dr, OUT / 'ring.stl')
        close(j.sw, dr)
    print('VOLUMES', res)
