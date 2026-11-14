"""T6: PETG block with a Ø10.2 hole along Y, a Ø10 steel pin through it, 250 N up at each pin end, block bottom fixed.

    python eval/haiku-a/t6_contact.py      (run from the worktree root, in the foreground; never under timeout)

Builds block.SLDPRT and pin.SLDPRT, brings the pin in as its own body, and solves once with no-penetration contact
between the pin and the hole. Writes eval/haiku-a/t6.json. One attempt; the outcome is what the script reports.
"""
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'solidworks'))
import numpy as np  # noqa: E402
from swfea import NO_PENETRATION, PETG, SOLVER_DIRECT, STEEL, static  # noqa: E402
from swkit import (MID, NUL, Sk, bbox, bodies, export, extrude, face_info, feature_errors, insert_body,  # noqa: E402
                   job, log, new_part, open_doc, pick, plane, save, volume)

OUT = ROOT / '_wip' / 'sw-eval' / 'haiku-a'
HOLE_D, PIN_D, PIN_L = 10.2, 10.0, 50.0
BLK = dict(x=40.0, y=30.0, z=20.0)
ZC = 10.0
F_END = 250.0


def build_parts(j):
    d = new_part(j.sw, OUT / 'block.SLDPRT')
    with Sk(d, plane(d, 'Z', BLK['z'] / 2, 'BLK_P'), 'BLOCK') as s:
        s.rect((-BLK['x'] / 2, -BLK['y'] / 2, BLK['z'] / 2), (BLK['x'] / 2, BLK['y'] / 2, BLK['z'] / 2))
    extrude(d, s.feat, 'BLOCK', BLK['z'], mode=MID, expect_dv=BLK['x'] * BLK['y'] * BLK['z'])
    with Sk(d, plane(d, 'Y', 0.0, 'HOLE_P'), 'HOLE') as s:
        s.circle((0.0, 0.0, ZC), HOLE_D / 2)
    extrude(d, s.feat, 'HOLE', BLK['y'] + 10, cut=True, mode=MID, expect_dv=math.pi * (HOLE_D / 2) ** 2 * BLK['y'])
    save(d)
    j.sw.CloseDoc(d.GetTitle)
    p = new_part(j.sw, OUT / 'pin.SLDPRT')
    with Sk(p, plane(p, 'Y', 0.0, 'PIN_P'), 'PIN') as s:
        s.circle((0.0, 0.0, ZC), PIN_D / 2)
    extrude(p, s.feat, 'PIN', PIN_L, mode=MID, expect_dv=math.pi * (PIN_D / 2) ** 2 * PIN_L)
    save(p)
    j.sw.CloseDoc(p.GetTitle)


def main():
    t0 = time.time()
    hand_bearing = 4 * (2 * F_END) / (math.pi * HOLE_D * BLK['y'])     # 4F/(pi d L) with F = 500 N (both ends), L = 30 mm
    res = dict(hand_bearing_mpa=round(hand_bearing, 3), attempts=[])
    with job() as j:
        build_parts(j)
        d = open_doc(j.sw, OUT / 'block.SLDPRT')
        insert_body(d, OUT / 'pin.SLDPRT')
        save(d)
        log('bodies', bodies(d), 'volume', round(volume(d), 3))
        res['bodies'] = [b[0] for b in bodies(d)]
        cw = j.simulation()
        d = open_doc(j.sw, OUT / 'block.SLDPRT')
        d.ForceRebuild3(False)
        blk_bottom = pick(d, kind='plane', normal=(0, 0, -1), at=(0.0, 0.0, 0.0))
        pin_cyl = [f for f in pick(d, kind='cyl', r=PIN_D / 2) if face_info(f)['box'][4] - face_info(f)['box'][1] > 40]
        hole_cyl = [f for f in pick(d, kind='cyl', r=HOLE_D / 2) if face_info(f)['box'][4] - face_info(f)['box'][1] > 25]
        end_pos = pick(d, kind='plane', at=(0.0, PIN_L / 2, ZC))
        end_neg = pick(d, kind='plane', at=(0.0, -PIN_L / 2, ZC))
        log('picks: bottom', len(blk_bottom), 'pin cyl', len(pin_cyl), 'hole cyl', len(hole_cyl),
            'end+', len(end_pos), 'end-', len(end_neg))
        res['picks'] = dict(bottom=len(blk_bottom), pin=len(pin_cyl), hole=len(hole_cyl), end_pos=len(end_pos),
                            end_neg=len(end_neg))
        if not (blk_bottom and pin_cyl and hole_cyl and end_pos and end_neg):
            raise SystemExit('FAIL: a pick returned nothing')
        loads = [('remote', end_pos, (0.0, PIN_L / 2, ZC), (0.0, 0.0, F_END), (0.0, 0.0, 0.0)),
                 ('remote', end_neg, (0.0, -PIN_L / 2, ZC), (0.0, 0.0, F_END), (0.0, 0.0, 0.0))]
        # attempt 1: pin in the hole, no-penetration contact, nothing else holding the pin
        att = dict(name='A1 contact only', ok=False)
        try:
            r = static(j, d, 'T6_A1', PETG, fixtures=[('fixed', blk_bottom)], loads=loads, el=2.0,
                       contacts=[(NO_PENETRATION, hole_cyl, pin_cyl)], materials={'pin': STEEL},
                       solver=SOLVER_DIRECT, loose_ok=True)
            att.update(nodes=r.nodes, reaction=[round(v, 3) for v in r.reaction], max_disp=round(r.max_disp(), 4),
                       excessive=bool(getattr(r, 'excessive', False)))
            att['ok'] = True
        except Exception as ex:      # noqa: BLE001 - the attempt's failure is the result
            att['error'] = str(ex)[:400]
        res['attempts'].append(att)
        log('attempt A1', att)
        res['elapsed_s'] = round(time.time() - t0, 1)
        j.sw.CloseDoc(d.GetTitle)
    (ROOT / 'eval' / 'haiku-a' / 't6.json').write_text(json.dumps(res, indent=2, default=str), encoding='utf-8')
    print(json.dumps(res, indent=2, default=str))


if __name__ == '__main__':
    main()
