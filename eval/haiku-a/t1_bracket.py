"""T1: model the L-shaped motor bracket from its specification, measure it, export STEP and STL.

    python eval/haiku-a/t1_bracket.py      (run from the worktree root, in the foreground; never under timeout)

Writes _wip/sw-eval/haiku-a/bracket.SLDPRT, bracket.step, bracket.stl and eval/haiku-a/t1.json.
"""
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'solidworks'))
from swkit import (MID, Sk, bbox, bodies, edges_where, export, extrude, face_info, feature_errors,  # noqa: E402
                   fillet, job, log, new_part, pick, plane, save, single_body, volume)

OUT = ROOT / '_wip' / 'sw-eval' / 'haiku-a'
OUT.mkdir(parents=True, exist_ok=True)
DENSITY_G_CM3 = 1.19                     # PETG, swfea.PETG

# ---- the specification (mm) ---------------------------------------------------------------------------------------
BASE = (80.0, 50.0, 6.0)                 # X, Y, Z: base plate from the origin
UP_T, UP_TOP = 6.0, 46.0                 # upright thickness along X; top of the upright at Z 46
INNER_R = 4.0                            # inside corner fillet on the edge along Y at X 6, Z 6
BASE_HOLES = [(25.0, 10.0), (25.0, 40.0), (65.0, 10.0), (65.0, 40.0)]
BASE_HOLE_D = 5.5
BORE_D, BORE_Y, BORE_Z = 22.0, 25.0, 28.0
PCD, PCD_HOLE_D = 31.0, 3.4
PCD_ANGLES = (45.0, 135.0, 225.0, 315.0)
CORNER_R = 5.0                           # base vertical corners at X 80; upright top corners (edges along X at Z 46)


# ---- hand values --------------------------------------------------------------------------------------------------
def hand_volume():
    v = BASE[0] * BASE[1] * BASE[2] + UP_T * BASE[1] * (UP_TOP - BASE[2])     # base + upright above it = 36000
    v += (1 - math.pi / 4) * INNER_R ** 2 * BASE[1]                           # inside fillet adds material
    v -= len(BASE_HOLES) * math.pi * (BASE_HOLE_D / 2) ** 2 * BASE[2]         # base holes
    v -= math.pi * (BORE_D / 2) ** 2 * UP_T                                   # bore through the upright
    v -= len(PCD_ANGLES) * math.pi * (PCD_HOLE_D / 2) ** 2 * UP_T             # four holes on the PCD
    v -= 2 * (1 - math.pi / 4) * CORNER_R ** 2 * BASE[2]                      # base vertical rounds
    v -= 2 * (1 - math.pi / 4) * CORNER_R ** 2 * UP_T                         # upright top rounds
    return v


def pcd_points():
    """Hole centres (x, y, z) on the Ø31 circle about the bore axis (along X), at the four angles."""
    out = []
    for a in PCD_ANGLES:
        t = math.radians(a)
        out.append((UP_T / 2, BORE_Y + PCD / 2 * math.cos(t), BORE_Z + PCD / 2 * math.sin(t)))
    return out


def build(j):
    d = new_part(j.sw, OUT / 'bracket.SLDPRT')

    # base plate X 0..80, Y 0..50, Z 0..6: sketch on its mid plane (Z 3), extruded 6 both ways
    with Sk(d, plane(d, 'Z', 3.0, 'BASE_P'), 'BASE') as s:
        s.rect((0, 0, 3.0), (BASE[0], BASE[1], 3.0))
    extrude(d, s.feat, 'BASE', BASE[2], mode=MID, expect_dv=BASE[0] * BASE[1] * BASE[2])

    # upright X 0..6, Y 0..50, Z 3..46: starts 3 mm inside the base so the union merges cleanly
    v0 = volume(d)
    with Sk(d, plane(d, 'X', UP_T / 2, 'UP_P'), 'UPRIGHT') as s:
        s.rect((UP_T / 2, 0, 3.0), (UP_T / 2, BASE[1], UP_TOP))
    extrude(d, s.feat, 'UPRIGHT', UP_T, mode=MID)
    dv = volume(d) - v0
    want = UP_T * BASE[1] * (UP_TOP - BASE[2])               # only the part above the base adds volume
    log(f'upright adds {dv:.3f} mm3, hand {want:.3f}')
    if abs(dv - want) > 0.01 * want or len(bodies(d)) != 1:
        raise SystemExit(f'FAIL: upright: added {dv:.3f} vs hand {want:.3f}; bodies {bodies(d)}')
    save(d)

    # inside corner fillet R4 on the edge along Y at X 6, Z 6
    inside = edges_where(d, lambda p: abs(p[0] - UP_T) < 0.01 and abs(p[2] - BASE[2]) < 0.01)
    log('inside corner edges found', len(inside))
    if len(inside) != 1:
        raise SystemExit(f'FAIL: expected one inside corner edge, found {len(inside)}')
    v0 = volume(d)
    if fillet(d, inside, (INNER_R,), 'INNER_FILLET') is None:
        raise SystemExit('FAIL: inside fillet did not build')
    exp_fillet = (1 - math.pi / 4) * INNER_R ** 2 * BASE[1]
    got = volume(d) - v0
    log(f'inside fillet adds {got:.3f} mm3 (hand {exp_fillet:.3f})')
    if abs(got - exp_fillet) > 0.01 * exp_fillet:
        raise SystemExit('FAIL: inside fillet volume off')
    save(d)

    # bore Ø22 through the upright along X, centred Y 25, Z 28 (cut 2 mm past each face, into empty space)
    with Sk(d, plane(d, 'X', UP_T / 2, 'BORE_P'), 'BORE') as s:
        s.circle((UP_T / 2, BORE_Y, BORE_Z), BORE_D / 2)
    extrude(d, s.feat, 'BORE', UP_T + 4.0, cut=True, mode=MID,
            expect_dv=math.pi * (BORE_D / 2) ** 2 * UP_T)
    save(d)

    # four Ø3.4 holes on a Ø31 circle about the bore axis, through the upright along X
    with Sk(d, plane(d, 'X', UP_T / 2, 'PCD_P'), 'PCDHOLE') as s:
        for p in pcd_points():
            s.circle(p, PCD_HOLE_D / 2)
    extrude(d, s.feat, 'PCDHOLE', UP_T + 4.0, cut=True, mode=MID,
            expect_dv=len(PCD_ANGLES) * math.pi * (PCD_HOLE_D / 2) ** 2 * UP_T)
    save(d)

    # four Ø5.5 through holes in the base
    with Sk(d, plane(d, 'Z', BASE[2] / 2, 'BHOLE_P'), 'BASEHOLE') as s:
        for x, y in BASE_HOLES:
            s.circle((x, y, BASE[2] / 2), BASE_HOLE_D / 2)
    extrude(d, s.feat, 'BASEHOLE', BASE[2] + 4.0, cut=True, mode=MID,
            expect_dv=len(BASE_HOLES) * math.pi * (BASE_HOLE_D / 2) ** 2 * BASE[2])
    save(d)

    # R5 on the two vertical corners of the base at X 80 (edges along Z)
    vert = edges_where(d, lambda p: abs(p[0] - BASE[0]) < 0.01 and min(abs(p[1]), abs(p[1] - BASE[1])) < 0.01)
    log('base corner edges found', len(vert))
    if len(vert) != 2:
        raise SystemExit(f'FAIL: expected 2 base corner edges, found {len(vert)}')
    if fillet(d, vert, (CORNER_R,), 'BASE_CORNERS') is None:
        raise SystemExit('FAIL: base corner round did not build')
    save(d)

    # R5 on the two top corners of the upright (edges along X at Z 46)
    top = edges_where(d, lambda p: abs(p[2] - UP_TOP) < 0.01 and min(abs(p[1]), abs(p[1] - BASE[1])) < 0.01)
    log('upright top edges found', len(top))
    if len(top) != 2:
        raise SystemExit(f'FAIL: expected 2 upright top edges, found {len(top)}')
    if fillet(d, top, (CORNER_R,), 'UPRIGHT_TOP') is None:
        raise SystemExit('FAIL: upright top round did not build')
    save(d)
    return d


def measure(d):
    res = {}
    res['volume_mm3'] = volume(d)
    res['hand_volume_mm3'] = hand_volume()
    res['mass_g'] = res['volume_mm3'] / 1000.0 * DENSITY_G_CM3
    res['bbox_mm'] = bbox(d)
    res['bodies'] = len(bodies(d))
    res['feature_errors'] = feature_errors(d)
    # every cylindrical face measured on the finished solid: radius and axis position (box centre)
    cyl = {}
    for f in pick(d, kind='cyl'):
        i = face_info(f)
        if i['r'] is None:
            continue
        c = [(i['box'][k] + i['box'][k + 3]) / 2 for k in range(3)]
        cyl.setdefault(round(i['r'], 2), []).append([round(v, 3) for v in c])
    res['cylinders_mm'] = cyl
    return res


def main():
    t0 = time.time()
    with job() as j:
        d = build(j)
        single_body(d)
        save(d)
        res = measure(d)
        log('measured volume', round(res['volume_mm3'], 3), 'hand', round(res['hand_volume_mm3'], 3),
            'bodies', res['bodies'], 'bbox', [round(v, 3) for v in res['bbox_mm']])
        if res['feature_errors']:
            raise SystemExit(f"FAIL: rebuild errors {res['feature_errors']}")
        export(j.sw, d, OUT / 'bracket.step')
        export(j.sw, d, OUT / 'bracket.stl')
        j.sw.CloseDoc(d.GetTitle)
    try:
        import trimesh
        mesh = trimesh.load(OUT / 'bracket.stl')
        res.update(stl_watertight=bool(mesh.is_watertight), stl_volume_mm3=float(mesh.volume),
                   stl_bodies=len(mesh.split(only_watertight=False)), stl_bounds=mesh.bounds.tolist())
    except ImportError:
        res.update(stl_watertight=None, stl_volume_mm3=None)
    res['hand_volume_mm3'] = round(res['hand_volume_mm3'], 2)
    res['elapsed_s'] = round(time.time() - t0, 1)
    (ROOT / 'eval' / 'haiku-a' / 't1.json').write_text(json.dumps(res, indent=2, default=str), encoding='utf-8')
    print(json.dumps(res, indent=2, default=str))


if __name__ == '__main__':
    main()
