"""D1: buck board mount, idea A (standing frame on the rail's front face). Builds buck_mount.SLDPRT and exports it.

Frame lies in the XZ plane, Y 10 to 14 (4 mm thick), on the rail's front face (rail front face at Y 10, T-slot centre Z -10).
Four bosses (Ø7, 3.5 tall, Y 14 to 17.5) at the board's holes: X ±39, Z -13.5 and 39.5 (board is 85 x 60, Z -17 to 43).
Two Ø5.5 clearance holes through the bottom bar at X ±25, Z -10 for M5 into the rail's T-slot.

Hand volumes (mm3), all written before the build:
  outer 85 x 60 = 5100, opening X ±35.5 (71) x Z -7..35 (42) = 2982 -> frame 2118 x 4 thick = 8472
  two holes: 2 x pi 2.75^2 x 4 = 190.07 removed
  four bosses: 4 x pi 3.5^2 x 3.5 = 538.7 added
  total = 8820.6 mm3, mass at 1.19 g/cm3 = 10.5 g
"""
import math
import sys
from pathlib import Path

WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT / 'solidworks'))
from swkit import (MID, Sk, bbox, bodies, close, export, extrude, feature_errors, job, new_part, plane,  # noqa: E402
                   save, single_body, volume, expect, log)

OUT = WT / '_wip' / 'sw-eval' / 'haiku-d' / 'd1'
EVAL = WT / 'eval' / 'haiku-d'
OUT.mkdir(parents=True, exist_ok=True)

Y0, T = 10.0, 4.0                     # frame face at the rail, frame thickness (Y)
YB, BH = Y0 + T, 3.5                  # boss base (frame front face) and boss height
HAND = {'frame': 8472.0, 'holes': -190.07, 'bosses': 538.7}
HAND_TOTAL = sum(HAND.values())


def build(j):
    d = new_part(j.sw, OUT / 'buck_mount.SLDPRT')
    # frame: outer 85 x 60 with a 71 x 42 opening, Y 10 to 14
    with Sk(d, plane(d, 'Y', Y0 + T / 2, 'FRAME_P'), 'FRAME') as s:
        s.rect((-42.5, Y0 + T / 2, -17.0), (42.5, Y0 + T / 2, 43.0))
        s.rect((-35.5, Y0 + T / 2, -7.0), (35.5, Y0 + T / 2, 35.0))
    extrude(d, s.feat, 'FRAME', T, mode=MID, expect_dv=8472.0)
    save(d)
    # M5 clearance holes through the bottom bar, into the rail's T-slot
    with Sk(d, plane(d, 'Y', Y0 + T / 2, 'MOUNT_P'), 'MOUNT') as s:
        s.circle((-25.0, Y0 + T / 2, -10.0), 2.75)
        s.circle((25.0, Y0 + T / 2, -10.0), 2.75)
    extrude(d, s.feat, 'MOUNT', T + 2, cut=True, mode=MID, expect_dv=190.07)
    save(d)
    # four bosses for the board's M3 screws, on the frame's front face
    with Sk(d, plane(d, 'Y', YB + BH / 2, 'BOSS_P'), 'BOSS') as s:
        for x, z in ((-39.0, -13.5), (39.0, -13.5), (-39.0, 39.5), (39.0, 39.5)):
            s.circle((x, YB + BH / 2, z), 3.5)
    extrude(d, s.feat, 'BOSS', BH, mode=MID, expect_dv=538.7)
    save(d)
    single_body(d)
    save(d)
    return d


def checks(d):
    v = volume(d)
    expect('volume mm3 against hand total', v, HAND_TOTAL, 0.005)
    b = bbox(d)
    expect('box x0', b[0], -42.5, 0.01)
    expect('box x1', b[3], 42.5, 0.01)
    expect('box y0 (rail face)', b[1], Y0, 0.01)
    expect('box y1 (boss tops)', b[4], YB + BH, 0.01)
    expect('box z0', b[2], -17.0, 0.01)
    expect('box z1 (within 45 above rail)', b[5], 43.0, 0.01)
    expect('rebuild errors', len(feature_errors(d)), 0, 0)
    log('bodies', bodies(d))
    return v, b


if __name__ == '__main__':
    with job(wait_s=1800) as j:
        d = build(j)
        v, b = checks(d)
        export(j.sw, d, OUT / 'buck_mount.step')
        export(j.sw, d, OUT / 'buck_mount.stl')
        close(j.sw, d)
    print('VOLUME', v, 'BOX', b)
