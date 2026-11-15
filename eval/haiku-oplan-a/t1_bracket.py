"""T1: L-shaped motor bracket from the specification (eval/TASKS.md T1), built per plans/A_T1.md.

Writes _wip/sw-eval/haiku-oplan-a/bracket.SLDPRT, bracket.step, bracket.stl, and eval/haiku-oplan-a/t1.json.
"""
import json
import math
import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, r"J:\code\cad-daddy-wt\sw-eval-haiku-oplan-a\solidworks")
from swkit import *  # noqa: E402,F401,F403

W = Path(r"J:\code\cad-daddy-wt\sw-eval-haiku-oplan-a\_wip\sw-eval\haiku-oplan-a")
E = Path(r"J:\code\cad-daddy-wt\sw-eval-haiku-oplan-a\eval\haiku-oplan-a")
W.mkdir(parents=True, exist_ok=True)
E.mkdir(parents=True, exist_ok=True)
HAND_V = 32974.0
RES = {'task': 'T1', 'status': 'failed', 'notes': []}


def note(s):
    RES['notes'].append(s)
    log(s)


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
    t_start = time.time()
    d = new_part(j.sw, W / 'bracket.SLDPRT')
    # 1 base, sketch at mid thickness
    with Sk(d, plane(d, 'Z', 3.0, 'BASE_P'), 'BASE') as s:
        s.rect((0, 0, 3.0), (80, 50, 3.0))
    extrude(d, s.feat, 'BASE', 6.0, mode=MID, expect_dv=24000.0)
    save(d)
    # 2 upright Z 6..46
    with Sk(d, plane(d, 'Z', 26.0, 'UPRIGHT_P'), 'UPRIGHT') as s:
        s.rect((0, 0, 26.0), (6, 50, 26.0))
    extrude(d, s.feat, 'UPRIGHT', 40.0, mode=MID, expect_dv=12000.0)
    save(d)
    # 3 inside fillet R4 on the edge along Y at X 6, Z 6
    e = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01)
    expect('inside corner edges', len(e), 1, 0)
    v0 = volume(d)
    r = fillet(d, e, (4.0,), 'INSIDE_FILLET')
    expect('fillet radius', r, 4.0, 0)
    expect('fillet adds', volume(d) - v0, 171.68, 0.01)
    save(d)
    # 4 R5 rounds on the two vertical base corners at X 80 and the two upright top edges along X at Z 46
    e = edges_where(d, lambda p: (abs(p[0] - 80) < 0.01 and min(abs(p[1]), abs(p[1] - 50)) < 0.01)
                    or (abs(p[2] - 46) < 0.01 and min(abs(p[1]), abs(p[1] - 50)) < 0.01))
    expect('round edges', len(e), 4, 0)
    v0 = volume(d)
    rr = fillet(d, e, (5.0,), 'CORNER_R5')
    expect('round radius', rr, 5.0, 0)
    expect('rounds remove', v0 - volume(d), 128.76, 0.01)
    save(d)
    # 5 base holes, cut mid-plane 8 about Z 3
    with Sk(d, plane(d, 'Z', 3.0, 'BASE_HOLES_P'), 'BASE_HOLES') as s:
        for x, y in ((25, 10), (25, 40), (65, 10), (65, 40)):
            s.circle((x, y, 3.0), 2.75)
    extrude(d, s.feat, 'BASE_HOLES', 8.0, cut=True, mode=MID, expect_dv=570.20)
    save(d)
    # 6 bore along X at Y 25, Z 28, D22
    with Sk(d, plane(d, 'X', 3.0, 'BORE_P'), 'BORE') as s:
        s.circle((3.0, 25.0, 28.0), 11.0)
    extrude(d, s.feat, 'BORE', 8.0, cut=True, mode=MID, expect_dv=2280.80)
    save(d)
    # 7 four D3.4 holes on a D31 circle about the bore axis, at 45/135/225/315 degrees
    c = 15.5 * math.cos(math.radians(45))
    up = [(3.0, 25 - c, 28 - c), (3.0, 25 + c, 28 - c), (3.0, 25 + c, 28 + c), (3.0, 25 - c, 28 + c)]
    with Sk(d, plane(d, 'X', 3.0, 'UHOLES_P'), 'UPRIGHT_HOLES') as s:
        for p in up:
            s.circle(p, 1.7)
    extrude(d, s.feat, 'UPRIGHT_HOLES', 8.0, cut=True, mode=MID, expect_dv=217.90)
    save(d)
    # 8 checks
    single_body(d)
    errs = feature_errors(d)
    expect('feature errors empty', len(errs), 0, 0)
    expect('volume', volume(d), HAND_V, 0.001)
    bb = bbox(d)
    for got, want in zip(bb, (0, 0, 0, 80, 50, 46)):
        expect('bbox', got, want, 0.01)
    save(d)
    # measure the holes on the finished solid
    m_base = sorted((round(ctr(f)[0], 2), round(ctr(f)[1], 2)) for f in pick(d, kind='cyl', r=2.75))
    m_bore = pick(d, kind='cyl', r=11.0)
    m_up = sorted((round(ctr(f)[1], 2), round(ctr(f)[2], 2)) for f in pick(d, kind='cyl', r=1.7))
    m_fil = pick(d, kind='cyl', r=4.0)
    m_rnd = pick(d, kind='cyl', r=5.0)
    log('counts: base holes', len(m_base), 'bore', len(m_bore), 'upright holes', len(m_up), 'fillet', len(m_fil), 'rounds', len(m_rnd))
    expect('base hole count', len(m_base), 4, 0)
    expect('bore count', len(m_bore), 1, 0)
    expect('upright hole count', len(m_up), 4, 0)
    expect('fillet count', len(m_fil), 1, 0)
    expect('round count', len(m_rnd), 4, 0)
    want_base = sorted([(25, 10), (25, 40), (65, 10), (65, 40)])
    for g, w in zip(m_base, want_base):
        expect('base hole x', g[0], w[0], 0.01)
        expect('base hole y', g[1], w[1], 0.01)
    bc = ctr(m_bore[0])
    expect('bore y', bc[1], 25.0, 0.01)
    expect('bore z', bc[2], 28.0, 0.01)
    want_up = sorted([(round(25 - c, 2), round(28 - c, 2)), (round(25 + c, 2), round(28 - c, 2)),
                      (round(25 + c, 2), round(28 + c, 2)), (round(25 - c, 2), round(28 + c, 2))])
    for g, w in zip(m_up, want_up):
        expect('upright hole y', g[0], w[0], 0.01)
        expect('upright hole z', g[1], w[1], 0.01)
    RES['measured'] = dict(base_holes_xy=m_base, bore_yz=[round(bc[1], 3), round(bc[2], 3)],
                           upright_holes_yz=m_up, fillet_faces=len(m_fil), round_faces=len(m_rnd))
    tree_t1 = tree(d)
    RES['tree_len'] = len(tree_t1)
    RES['volume_mm3'] = round(volume(d), 3)
    RES['hand_volume_mm3'] = HAND_V
    RES['mass_g'] = round(volume(d) * 1.19e-3, 3)
    RES['bbox_mm'] = [round(v, 3) for v in bbox(d)]
    RES['bodies'] = len(solid_bodies(d))
    save(d)
    # exports
    export(j.sw, d, W / 'bracket.step')
    export(j.sw, d, W / 'bracket.stl')
    RES['build_s'] = round(time.time() - t_start)
    return d


def check_exports(d):
    import trimesh
    stl = W / 'bracket.stl'
    mesh = trimesh.load(str(stl))
    parts = mesh.split(only_watertight=False)
    RES['stl_watertight'] = bool(mesh.is_watertight)
    RES['stl_bodies'] = len(parts)
    RES['stl_volume_mm3'] = round(float(mesh.volume), 3)
    vol = volume(d) if False else HAND_V
    b = mesh.bounds
    log('stl bounds', b.round(3).tolist(), 'volume', round(float(mesh.volume), 2), 'watertight', mesh.is_watertight, 'parts', len(parts))
    dv = abs(float(mesh.volume) - RES['volume_mm3']) / RES['volume_mm3']
    RES['stl_volume_rel_err'] = round(dv, 5)
    step_txt = (W / 'bracket.step').read_text(encoding='utf-8', errors='ignore')
    milli = any('SI_UNIT' in ln and '.MILLI.' in ln for ln in step_txt.splitlines())
    RES['step_mm'] = milli
    log('step mm', milli)
    ok_bounds = all(abs(a - c) <= 0.1 for a, c in zip(b.flatten()[:3].tolist() + b.flatten()[3:].tolist(), [0, 0, 0, 80, 50, 46]))
    RES['stl_bounds_mm'] = b.round(3).tolist()
    RES['stl_bounds_within_0p1'] = bool(ok_bounds)
    if not (mesh.is_watertight and len(parts) == 1 and dv < 0.005 and milli and ok_bounds):
        raise Failed(f'export checks: watertight {mesh.is_watertight} parts {len(parts)} dv {dv:.4f} mm {milli} bounds {ok_bounds}')


def main():
    try:
        with job(wait_s=900) as j:
            d = build(j)
            check_exports(d)
            RES['status'] = 'done'
    except Exception as ex:  # noqa: BLE001
        RES['error'] = f'{type(ex).__name__}: {ex}'
        RES['traceback'] = traceback.format_exc()[-2000:]
        log('FAILED', RES['error'])
    finally:
        RES['finished'] = time.strftime('%H:%M:%S')
        (E / 't1.json').write_text(json.dumps(RES, indent=2, ensure_ascii=False), encoding='utf-8')
        log('wrote t1.json', RES['status'])


if __name__ == '__main__':
    main()
