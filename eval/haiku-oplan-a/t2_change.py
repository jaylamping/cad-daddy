"""T2: open the saved bracket.SLDPRT (T1, not rebuilt), add four D10 x 3 counterbores and a 20 x 6 round-ended slot,
save as bracket_b.SLDPRT. Per plans/A_T2.md. Writes eval/haiku-oplan-a/t2.json.
"""
import json
import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, r"J:\code\cad-daddy-wt\sw-eval-haiku-oplan-a\solidworks")
from swkit import *  # noqa: E402,F401,F403

W = Path(r"J:\code\cad-daddy-wt\sw-eval-haiku-oplan-a\_wip\sw-eval\haiku-oplan-a")
E = Path(r"J:\code\cad-daddy-wt\sw-eval-haiku-oplan-a\eval\haiku-oplan-a")
HAND_V = 31643.0
RES = {'task': 'T2', 'status': 'failed', 'notes': []}
HOLES = ((25, 10), (25, 40), (65, 10), (65, 40))


def ctr(f):
    i = face_info(f)
    b = i['box']
    return ((b[0] + b[3]) / 2, (b[1] + b[4]) / 2, (b[2] + b[5]) / 2)


def tree(d):
    out, f = [], d.FirstFeature
    while f is not None:
        out.append((f.Name, f.GetTypeName2))
        f = f.GetNextFeature
    return out


def build(j):
    t0 = time.time()
    d = open_doc(j.sw, W / 'bracket.SLDPRT')
    expect('start volume', volume(d), 32974.0, 0.001)
    save_as(d, W / 'bracket_b.SLDPRT')          # from here d is bracket_b; bracket.SLDPRT stays as T1 left it
    before = tree(d)
    RES['tree_before'] = before
    # 1 counterbores, one-sided cut from a plane at Z 6 going down
    with Sk(d, plane(d, 'Z', 6.0, 'CB_P'), 'CBORE') as s:
        for x, y in HOLES:
            s.circle((x, y, 6.0), 5.0)
    extrude(d, s.feat, 'CBORE', 3.0, cut=True, mode=BLIND, want=(2, -1, 6.0), expect_dv=657.38)
    save(d)
    # 2 slot middle, Z 3 plane, cut mid-plane 8
    with Sk(d, plane(d, 'Z', 3.0, 'SLOT_MID_P'), 'SLOT_MID') as s:
        s.rect((38, 22, 3.0), (52, 28, 3.0))
    extrude(d, s.feat, 'SLOT_MID', 8.0, cut=True, mode=MID, expect_dv=504.0)
    save(d)
    # 3 slot ends
    with Sk(d, plane(d, 'Z', 3.0, 'SLOT_ENDS_P'), 'SLOT_ENDS') as s:
        s.circle((38, 25, 3.0), 3.0)
        s.circle((52, 25, 3.0), 3.0)
    extrude(d, s.feat, 'SLOT_ENDS', 8.0, cut=True, mode=MID, expect_dv=169.65)
    save(d)
    single_body(d)
    expect('feature errors empty', len(feature_errors(d)), 0, 0)
    expect('volume', volume(d), HAND_V, 0.001)
    after = tree(d)
    RES['tree_after'] = after
    same_prefix = after[:len(before)] == before
    added = after[len(before):]
    RES['tree_prefix_unchanged'] = same_prefix
    RES['tree_added'] = added
    log('tree prefix unchanged:', same_prefix, 'added:', added)
    expect('tree prefix unchanged', int(same_prefix), 1, 0)
    save(d)
    # measure
    floors = []
    for x, y in HOLES:
        fl = pick(d, kind='plane', normal=(0, 0, 1), inside=[x - 5.1, y - 5.1, 2.9, x + 5.1, y + 5.1, 3.1])
        expect('floor count', len(fl), 1, 0)
        floors.append(face_info(fl[0])['box'][2])
    for z in floors:
        expect('counterbore floor z', z, 3.0, 0.01)
    walls = pick(d, kind='cyl', r=5.0, inside=[15, 0, 2.9, 70, 50, 6.1])
    expect('counterbore wall count', len(walls), 4, 0)
    slot_ends = pick(d, kind='cyl', r=3.0)
    expect('slot end count', len(slot_ends), 2, 0)
    # each end is a half-cylinder (the outer half of an R3 about the arc centre), so its box centre is not the arc
    # centre: check the box extents instead. Left end spans X 35..38, right end X 52..55, Y 22..28.
    boxes = sorted(face_info(f)['box'] for f in slot_ends)
    ends = [(round(b[0], 2), round(b[3], 2)) for b in boxes]
    expect('slot left end x0', boxes[0][0], 35.0, 0.01)
    expect('slot left end x1', boxes[0][3], 38.0, 0.01)
    expect('slot right end x0', boxes[1][0], 52.0, 0.01)
    expect('slot right end x1', boxes[1][3], 55.0, 0.01)
    expect('slot end y0', boxes[0][1], 22.0, 0.01)
    expect('slot end y1', boxes[0][4], 28.0, 0.01)
    side_a = pick(d, kind='plane', at=(45, 22, 3))
    side_b = pick(d, kind='plane', at=(45, 28, 3))
    expect('slot side count a', len(side_a), 1, 0)
    expect('slot side count b', len(side_b), 1, 0)
    RES['counterbore_floor_z_mm'] = round(floors[0], 4)
    RES['counterbore_floor_z_all'] = [round(z, 4) for z in floors]
    RES['slot_ends_xy'] = ends
    RES['volume_mm3'] = round(volume(d), 3)
    RES['hand_volume_mm3'] = HAND_V
    RES['bodies'] = len(solid_bodies(d))
    RES['mass_g'] = round(volume(d) * 1.19e-3, 3)
    save(d)
    export(j.sw, d, W / 'bracket_b.stl')
    RES['build_s'] = round(time.time() - t0)
    return d


def main():
    try:
        with job(wait_s=900) as j:
            build(j)
            RES['status'] = 'done'
    except Exception as ex:  # noqa: BLE001
        RES['error'] = f'{type(ex).__name__}: {ex}'
        RES['traceback'] = traceback.format_exc()[-2000:]
        log('FAILED', RES['error'])
    finally:
        RES['finished'] = time.strftime('%H:%M:%S')
        (E / 't2.json').write_text(json.dumps(RES, indent=2, ensure_ascii=False, default=str), encoding='utf-8')
        log('wrote t2.json', RES['status'])


if __name__ == '__main__':
    main()
