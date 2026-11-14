"""B1: scripted hub model, with dimensions and volumes checked against the written specification."""
import json
import math
import sys
from pathlib import Path

import numpy as np
import trimesh
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / 'cad' / '_wip' / 'sw-eval' / 'luna-b'
sys.path.insert(0, str(ROOT / 'tools' / 'solidworks'))
from swkit import MID, Sk, bbox, bodies, expect, export, extrude, feature_errors, face_info, job, list_faces, new_part, pick, plane, save, single_body, volume  # noqa: E402


def hand_values():
    # Keyway: only the rectangular area outside the existing 10 mm bore adds removed volume.
    x0 = math.sqrt(25 - 1.5 ** 2)
    bore_overlap = 3 * x0 + quad(lambda x: 2 * math.sqrt(25 - x * x), x0, 5.0, epsabs=1e-12)[0]
    key_extra_area = 3 * 6.4 - bore_overlap
    # The radial screw bore removes the shell between the 5 mm bore and 13 mm boss over its circular section.
    screw_removed = quad(
        lambda x: 2 * math.sqrt(4 - x * x) * (math.sqrt(169 - x * x) - math.sqrt(25 - x * x)),
        -2.0, 2.0, epsabs=1e-11,
    )[0]
    total = (math.pi * 30 ** 2 * 5 + math.pi * 13 ** 2 * 20 - math.pi * 5 ** 2 * 25
             - 6 * math.pi * 2.25 ** 2 * 5 - 2 * math.pi * 2.75 ** 2 * 5
             - key_extra_area * 25 - screw_removed)
    return total, key_extra_area * 25, screw_removed


def center_of_face(f):
    i = face_info(f)
    return [(i['box'][k] + i['box'][k + 3]) / 2 for k in range(3)]


def main():
    expected, key_dv, screw_dv = hand_values()
    print(f'HAND B1 volume {expected:.6f} mm3; keyway extra {key_dv:.6f}; set-screw bore {screw_dv:.6f}', flush=True)
    path = CAD / 'hub.SLDPRT'
    with job(wait_s=1800) as j:
        d = new_part(j.sw, path)

        with Sk(d, plane(d, 'Z', 2.5, 'FLANGE_P'), 'FLANGE') as s:
            s.circle((0, 0, 2.5), 30.0)
        extrude(d, s.feat, 'FLANGE', 5.0, mode=MID, expect_dv=math.pi * 30 ** 2 * 5)
        save(d)

        with Sk(d, plane(d, 'Z', 15.0, 'BOSS_P'), 'BOSS') as s:
            s.circle((0, 0, 15.0), 13.0)
        extrude(d, s.feat, 'BOSS', 20.0, mode=MID, expect_dv=math.pi * 13 ** 2 * 20)
        save(d)

        with Sk(d, plane(d, 'Z', 12.5, 'BORE_P'), 'BORE') as s:
            s.circle((0, 0, 12.5), 5.0)
        extrude(d, s.feat, 'BORE', 27.0, cut=True, mode=MID, expect_dv=math.pi * 5 ** 2 * 25)
        save(d)

        with Sk(d, plane(d, 'Z', 12.5, 'KEYWAY_P'), 'KEYWAY') as s:
            s.rect((0, -1.5, 12.5), (6.4, 1.5, 12.5))
        extrude(d, s.feat, 'KEYWAY', 27.0, cut=True, mode=MID, expect_dv=key_dv)
        save(d)

        with Sk(d, plane(d, 'Z', 2.5, 'BOLT_P'), 'BOLT_HOLES') as s:
            for deg in range(0, 360, 60):
                a = math.radians(deg)
                s.circle((22.0 * math.cos(a), 22.0 * math.sin(a), 2.5), 2.25)
        extrude(d, s.feat, 'BOLT_HOLES', 5.0, cut=True, mode=MID,
                expect_dv=6 * math.pi * 2.25 ** 2 * 5)
        save(d)

        with Sk(d, plane(d, 'Z', 2.5, 'DOWEL_P'), 'DOWEL_HOLES') as s:
            s.circle((0, 15.0, 2.5), 2.75)
            s.circle((0, -15.0, 2.5), 2.75)
        extrude(d, s.feat, 'DOWEL_HOLES', 5.0, cut=True, mode=MID,
                expect_dv=2 * math.pi * 2.75 ** 2 * 5)
        save(d)

        with Sk(d, plane(d, 'Y', 7.0, 'SETSCREW_P'), 'SETSCREW') as s:
            s.circle((0, 7.0, 22.6), 2.0)
        extrude(d, s.feat, 'SETSCREW', 14.0, cut=True, mode=MID, expect_dv=screw_dv)
        save(d)

        if len(feature_errors(d)):
            raise RuntimeError(f'feature errors: {feature_errors(d)}')
        single_body(d)
        expect('hub volume mm3', volume(d), expected, 0.001)
        b = bbox(d)
        for k, want in enumerate((-30, -30, 0, 30, 30, 25)):
            expect(f'hub box[{k}] mm', b[k], want, 0.01)

        # Verify hole radii and centers from the final cylindrical faces, not from the feature sketch alone.
        bolt_faces = pick(d, kind='cyl', r=2.25)
        dowel_faces = pick(d, kind='cyl', r=2.75)
        expect('bolt-hole cylindrical faces', len(bolt_faces), 6, 0)
        expect('dowel-hole cylindrical faces', len(dowel_faces), 2, 0)
        bolt_centers = sorted((round(center_of_face(f)[0], 2), round(center_of_face(f)[1], 2)) for f in bolt_faces)
        want_bolts = sorted((round(22 * math.cos(math.radians(a)), 2), round(22 * math.sin(math.radians(a)), 2))
                            for a in range(0, 360, 60))
        if bolt_centers != want_bolts:
            raise RuntimeError(f'bolt centers read from final solid: {bolt_centers}, expected {want_bolts}')
        dowel_centers = sorted((round(center_of_face(f)[0], 2), round(center_of_face(f)[1], 2)) for f in dowel_faces)
        if dowel_centers != [(0.0, -15.0), (0.0, 15.0)]:
            raise RuntimeError(f'dowel centers read from final solid: {dowel_centers}')

        set_faces = pick(d, kind='cyl', r=2.0)
        expect('set-screw cylindrical faces', len(set_faces), 1, 0)
        set_i = face_info(set_faces[0])
        expect('set-screw axis X center', (set_i['box'][0] + set_i['box'][3]) / 2, 0.0, 0.01)
        expect('set-screw axis Z center', (set_i['box'][2] + set_i['box'][5]) / 2, 22.6, 0.01)
        key_floor = pick(d, kind='plane', at=(6.4, 0, 12.5))
        expect('keyway floor face at X=6.4', len(key_floor), 1, 0)
        key_i = face_info(key_floor[0])['box']
        expect('keyway floor width mm', key_i[4] - key_i[1], 3.0, 0.02)
        save(d)
        export(j.sw, d, CAD / 'hub.step')
        export(j.sw, d, CAD / 'hub.stl')
        sw_volume, sw_box, bdy = volume(d), bbox(d), bodies(d)

    mesh = trimesh.load(CAD / 'hub.stl', force='mesh')
    stl_box = np.asarray(mesh.bounds).reshape(-1).tolist()
    stl_volume = float(mesh.volume)
    if not mesh.is_watertight or len(mesh.split(only_watertight=False)) != 1:
        raise RuntimeError(f'STL must be watertight and one shell; watertight={mesh.is_watertight}, shells={len(mesh.split(only_watertight=False))}')
    if abs(stl_volume - sw_volume) / sw_volume > 0.005:
        raise RuntimeError(f'STL volume {stl_volume} differs from SolidWorks {sw_volume}')
    if max(abs(a - b) for a, b in zip(stl_box, sw_box)) > 0.1:
        raise RuntimeError(f'STL box {stl_box} differs from SolidWorks {sw_box}')
    step_text = (CAD / 'hub.step').read_text(encoding='ascii', errors='ignore')
    if not any('.MILLI.' in line and 'SI_UNIT' in line for line in step_text.splitlines()):
        raise RuntimeError('STEP length unit is not SI_UNIT .MILLI. METRE')

    spec_questions = [
        'The two Ø5.5 dowel holes on the Ø30 circle overlap the Ø26 boss footprint by 0.75 mm radially; I kept them through the flange thickness only, as specified, so their top openings meet the boss underside.'
    ]
    result = {
        'volume_mm3': sw_volume,
        'hand_volume_mm3': expected,
        'mass_g': sw_volume * 0.00119,
        'bbox_mm': sw_box,
        'bodies': bdy,
        'stl_watertight': bool(mesh.is_watertight),
        'stl_volume_mm3': stl_volume,
        'stl_bbox_mm': stl_box,
        'spec_questions': spec_questions,
        'status': 'complete',
        'notes': 'All dimensions, feature errors, body count, volume, STEP units and STL checks recorded in REPORT.md.'
    }
    (RUN / 'b1_result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
