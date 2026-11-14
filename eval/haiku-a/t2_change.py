"""T2: open the saved bracket.SLDPRT from T1 (not rebuilt from its script) and save bracket_b.SLDPRT with
a Ø10 counterbore, 3 deep from the top of the base (Z 6), on each of the four base holes, and a slot through the
base: 20 long and 6 wide overall with round ends, centred at X 45, Y 25, length along X.

    python eval/haiku-a/t2_change.py      (run from the worktree root, in the foreground; never under timeout)

Writes _wip/sw-eval/haiku-a/bracket_b.SLDPRT and eval/haiku-a/t2.json. bracket.SLDPRT itself is not saved to.
"""
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'solidworks'))
from swkit import (MID, Sk, bbox, bodies, export, extrude, face_info, feature_errors, job, log, open_doc,  # noqa: E402
                   pick, plane, save, save_as, single_body, volume)

OUT = ROOT / '_wip' / 'sw-eval' / 'haiku-a'

# T1's hand volume, recomputed from the same specification so T2 does not depend on T1's script being importable
spec = importlib.util.spec_from_file_location('t1', Path(__file__).with_name('t1_bracket.py'))
t1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t1)

BASE_TOP, BASE_T = t1.BASE[2], t1.BASE[2]
CB_D, CB_DEPTH = 10.0, 3.0
SLOT_CX, SLOT_CY = 45.0, 25.0
SLOT_LEN, SLOT_W = 20.0, 6.0
HOLE_R = t1.BASE_HOLE_D / 2


def hand_counterbore():
    return len(t1.BASE_HOLES) * math.pi * ((CB_D / 2) ** 2 - HOLE_R ** 2) * CB_DEPTH


def hand_slot():
    r = SLOT_W / 2
    straight = SLOT_LEN - SLOT_W                          # distance between the two round-end centres
    area = SLOT_W * straight + math.pi * r ** 2
    return area * BASE_T


def build(j):
    d = open_doc(j.sw, OUT / 'bracket.SLDPRT')
    v_start = volume(d)
    log('opened bracket.SLDPRT, volume', round(v_start, 3), 'bodies', len(bodies(d)))
    if len(bodies(d)) != 1:
        raise SystemExit(f'FAIL: bracket has {len(bodies(d))} bodies')

    # counterbores: sketch on the top face (Z 6), cut mid-plane depth 6 so the cut runs Z 3 to 9
    with Sk(d, plane(d, 'Z', BASE_TOP, 'CB_P'), 'CBORE') as s:
        for x, y in t1.BASE_HOLES:
            s.circle((x, y, BASE_TOP), CB_D / 2)
    extrude(d, s.feat, 'CBORE', 2 * CB_DEPTH, cut=True, mode=MID,
            expect_dv=hand_counterbore())
    save(d)

    # slot through the base: centre line along X from 38 to 52, round ends radius 3, sketched on the base mid plane
    x0, x1 = SLOT_CX - (SLOT_LEN - SLOT_W) / 2, SLOT_CX + (SLOT_LEN - SLOT_W) / 2
    r = SLOT_W / 2
    z = BASE_T / 2
    with Sk(d, plane(d, 'Z', z, 'SLOT_P'), 'SLOT') as s:
        s.poly([(x0, SLOT_CY + r, z), (x1, SLOT_CY + r, z)], closed=False)
        s.poly([(x0, SLOT_CY - r, z), (x1, SLOT_CY - r, z)], closed=False)
        s.arc((x1, SLOT_CY, z), (x1, SLOT_CY + r, z), (x1, SLOT_CY - r, z), -1)
        s.arc((x0, SLOT_CY, z), (x0, SLOT_CY - r, z), (x0, SLOT_CY + r, z), -1)
    extrude(d, s.feat, 'SLOT', 2 * BASE_T, cut=True, mode=MID, expect_dv=hand_slot())
    save(d)

    # the new file: save as bracket_b; bracket.SLDPRT on disk is left as T1 wrote it
    save_as(d, OUT / 'bracket_b.SLDPRT')
    return d


def measure(d):
    res = {}
    res['volume_mm3'] = volume(d)
    res['hand_volume_mm3'] = t1.hand_volume() - hand_counterbore() - hand_slot()
    res['bodies'] = len(bodies(d))
    res['bbox_mm'] = bbox(d)
    res['feature_errors'] = feature_errors(d)
    # counterbore floor: the planar face that lies at a point inside each counterbore, outside the 2.75 mm hole
    floors = []
    for x, y in t1.BASE_HOLES:
        fs = pick(d, kind='plane', at=(x + 4.0, y, 3.0))
        floors.append([round(face_info(f)['box'][2], 4) for f in fs])
    res['counterbore_floor_z_mm'] = floors
    res['counterbore_floor_z_all'] = sorted({v for fl in floors for v in fl})
    return res


def main():
    t0 = time.time()
    with job() as j:
        d = build(j)
        single_body(d)
        save(d)
        res = measure(d)
        log('measured', round(res['volume_mm3'], 3), 'hand', round(res['hand_volume_mm3'], 3), 'floors',
            res['counterbore_floor_z_all'])
        if res['feature_errors']:
            raise SystemExit(f"FAIL: rebuild errors {res['feature_errors']}")
        export(j.sw, d, OUT / 'bracket_b.step')
        j.sw.CloseDoc(d.GetTitle)
    res['hand_volume_mm3'] = round(res['hand_volume_mm3'], 2)
    res['elapsed_s'] = round(time.time() - t0, 1)
    (ROOT / 'eval' / 'haiku-a' / 't2.json').write_text(json.dumps(res, indent=2, default=str), encoding='utf-8')
    print(json.dumps(res, indent=2, default=str))


if __name__ == '__main__':
    main()
