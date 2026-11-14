"""Build and evaluate one lighter B3 candidate. Args: wall thickness mm, arm bottom z mm (default 40)."""
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / 'cad' / '_wip' / 'sw-eval' / 'luna-b'
SIM = ROOT / 'cad' / '_sim' / 'sw-eval' / 'luna-b'
sys.path.insert(0, str(ROOT / 'tools' / 'solidworks'))
from swkit import MID, Sk, bbox, bodies, expect, export, extrude, feature_errors, face_info, job, new_part, pick, plane, save, single_body, volume, edges_where, fillet, close, open_doc, solid_bodies, call  # noqa: E402
from swfea import PETG, converge, static  # noqa: E402

SIZES = (4.0, 3.5, 3.0)
AXES = {'X': (1, 0, 0), 'Y': (0, 1, 0), 'Z': (0, 0, 1)}


def name_token(v):
    return str(v).replace('.', 'p')


def main():
    t = float(sys.argv[1])
    bottom = float(sys.argv[2]) if len(sys.argv) > 2 else 40.0
    top = 52.0
    h = top - bottom
    if not (1.5 <= t <= 5.0 and 8.0 <= h <= 12.0):
        raise ValueError(f'candidate outside intended search bounds: thickness={t}, arm height={h}')
    token = f't{name_token(t)}_h{name_token(h)}_r0p4'
    model_path = CAD / f'wall_bracket_light_{token}.SLDPRT'
    stl_path = CAD / f'wall_bracket_light_{token}.stl'
    out_path = RUN / f'b3_{token}.json'
    expected_volume = (t * 13.5 * 49.5 + (65 - t) * 10.8 * h
                       + 2 * 3 ** 2 * (1 - math.pi / 4) * 10.8
                       - 5.1813 - 2 * math.pi * 2.25 ** 2 * t)
    nominal_root = 60 * (60 - t) * (h / 2) / (10.8 * h ** 3 / 12)
    span = 65 - t
    e_mpa = PETG['EX'] / 1e6
    inertia = 10.8 * h ** 3 / 12
    w = 6.0
    bending = w / (6 * e_mpa * inertia) * ((span * span ** 3 - span ** 4 / 4)
                                                - (span * (span - 10) ** 3 - (span - 10) ** 4 / 4))
    shear = (60 * (span - 10) + w * 10 ** 2 / 2) / ((5 / 6) * e_mpa / (2 * (1 + PETG['NUXY'])) * (10.8 * h))
    hand_tip = bending + shear

    with job(wait_s=1800) as j:
        if model_path.exists():
            model_path.unlink()
        d = new_part(j.sw, model_path)
        with Sk(d, plane(d, 'X', t / 2, 'WALL_P'), 'WALL') as s:
            s.rect((t / 2, 13.25, 5.25), (t / 2, 26.75, 54.75))
        extrude(d, s.feat, 'WALL', t, mode=MID, expect_dv=t * 13.5 * 49.5)
        save(d)

        with Sk(d, plane(d, 'X', (t + 65) / 2, 'ARM_P'), 'ARM') as s:
            s.rect(((t + 65) / 2, 14.6, bottom), ((t + 65) / 2, 25.4, top))
        extrude(d, s.feat, 'ARM', 65 - t, mode=MID, expect_dv=(65 - t) * 10.8 * h)
        save(d)

        root = edges_where(d, lambda p: abs(p[0] - t) < 0.02
                           and min(abs(p[2] - bottom), abs(p[2] - top)) < 0.02
                           and 14.5 <= p[1] <= 25.5)
        expect('root edges', len(root), 2, 0)
        if fillet(d, root, (3.0,), 'ROOT_FILLET') is None:
            raise RuntimeError('R3 root fillet failed')
        save(d)

        side_candidates = edges_where(d, lambda p: (abs(p[1] - 14.6) < 0.03 or abs(p[1] - 25.4) < 0.03)
                                      and t - 0.02 <= p[0] <= t + 5.2
                                      and 34.5 <= p[2] <= 57.5)
        round_edges = []
        for edge in side_candidates:
            cp = edge.GetCurveParams3
            mid = np.asarray(list(edge.GetCurve.Evaluate2((cp.UMinValue + cp.UMaxValue) / 2, 0))[:3]) * 1e3
            start = np.asarray(cp.StartPoint[:3]) * 1e3
            end = np.asarray(cp.EndPoint[:3]) * 1e3
            if np.linalg.norm(mid - (start + end) / 2) > 0.1 and np.linalg.norm(end - start) < 4.5:
                round_edges.append(edge)
        expect('curved root-side transition edges', len(round_edges), 4, 0)
        base_v = volume(d)
        if fillet(d, round_edges, (0.4,), 'ROOT_SIDE_R04') is None:
            raise RuntimeError('R0.4 root-side round failed')
        expected_volume += volume(d) - base_v
        save(d)

        step_x = 50.0
        step_dv = 5.1813
        with Sk(d, plane(d, 'Z', 51.95, 'LOAD_STEP_P'), 'LOAD_STEP') as s:
            s.rect((step_x, 14.0, 51.95), (55.0, 26.0, 51.95))
        extrude(d, s.feat, 'LOAD_STEP', 0.1, cut=True, mode=MID, expect_dv=step_dv)
        save(d)

        with Sk(d, plane(d, 'X', t / 2, 'SCREW_P'), 'SCREWS') as s:
            s.circle((t / 2, 20, 12), 2.25)
            s.circle((t / 2, 20, 48), 2.25)
        extrude(d, s.feat, 'SCREW_HOLES', t, cut=True, mode=MID, expect_dv=2 * math.pi * 2.25 ** 2 * t)
        save(d)
        if feature_errors(d):
            raise RuntimeError(f'feature errors: {feature_errors(d)}')
        single_body(d)
        expect('one body', len(bodies(d)), 1, 0)
        expect('volume mm3', volume(d), expected_volume, 0.1)
        bb = bbox(d)
        for i, want in enumerate((0, 13.25, 5.25, 65, 26.75, 54.75)):
            expect(f'bbox[{i}]', bb[i], want, 0.02)
        holes = pick(d, kind='cyl', r=2.25)
        expect('fixed holes after final rebuild', len(holes), 2, 0)
        centers = sorted(tuple(round((face_info(f)['box'][i] + face_info(f)['box'][i + 3]) / 2, 2)
                               for i in (1, 2)) for f in holes)
        if centers != [(20.0, 12.0), (20.0, 48.0)]:
            raise RuntimeError(f'fixed screw-hole centres changed: {centers}')
        load = pick(d, kind='plane', normal=(0, 0, 1), at=(60, 20, 52), area=100)
        expect('dedicated load patch', len(load), 1, 0)
        expect('load patch area mm2', face_info(load[0])['area'], 100, 0.05)
        wall = pick(d, kind='plane', normal=(-1, 0, 0), at=(0, 20, 30))
        expect('fixed wall face', len(wall), 1, 0)
        save(d)
        export(j.sw, d, stl_path)

        j.simulation()
        close(j.sw, d)
        d = open_doc(j.sw, model_path)
        d.ForceRebuild3(False)
        volume_mm3 = volume(d)
        print(f'PREDICT B3 {token}: nominal root={nominal_root:.3f} MPa; tip deflection={hand_tip:.3f} mm; '
              f'peak near root; expected nodes at {SIZES}: '
              + ', '.join(str(round(12 * volume_mm3 / el ** 3)) for el in SIZES), flush=True)
        results = []

        def runner(el):
            holes = pick(d, kind='cyl', r=2.25)
            load = pick(d, kind='plane', normal=(0, 0, 1), at=(60, 20, 52), area=100)
            expect(f'fixture walls el={el}', len(holes), 2, 0)
            expect(f'load patch el={el}', len(load), 1, 0)
            print(f'PREDICT B3 {token} el={el}: nodes={round(12 * volume_mm3 / el ** 3)}; '
                  f'peak near root, displacement about {hand_tip:.3f} mm', flush=True)
            r = static(j, d, f'{token}_{el:.2f}', PETG, fixtures=[('fixed', holes)], loads=[('normal', load, 60.0)],
                       el=el, ctrl=[(holes, 1.0), (load, 1.0)], max_nodes=199999)
            results.append(r)
            SIM.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(SIM / f'B3_{token}_{el:.2f}.npz', pos=r.pos, stress=r.s,
                                displacement=r.disp, fixed_points=r.fixed_pts, loaded_points=r.loaded_pts)
            return r

        helper_rows, helper_converged_z = converge(runner, SIZES, tol=0.05, layers=(0, 0, 1))
        r = results[-1]
        dist = 2 * max(SIZES)
        orientation = {}
        series_by_axis = {}
        for axis, normal in AXES.items():
            keep = r.away(dist=dist)
            vm, vm_at = r.peak(keep)
            ls, ls_at = r.layer_stress(normal, keep)
            sh, sh_at = r.layer_shear(normal, keep)
            values = []
            for q in results:
                m = q.away(dist=dist)
                values.append([q.peak(m)[0], q.layer_stress(normal, m)[0], q.layer_shear(normal, m)[0]])
            a, b = np.asarray(values[-2]), np.asarray(values[-1])
            conv = bool(np.all(np.abs(b - a) <= 0.05 * np.maximum(np.abs(b), 1e-9)))
            orientation[axis] = {'peak_vm_mpa': vm, 'peak_vm_at_mm': vm_at,
                                 'layer_stress_mpa': ls, 'layer_stress_at_mm': ls_at,
                                 'layer_shear_mpa': sh, 'layer_shear_at_mm': sh_at,
                                 'sf_yield': 45 / vm, 'sf_layer': 22.5 / ls if ls > 0 else None,
                                 'sf_shear': 13 / sh if sh > 0 else None, 'converged_all_three': conv}
            series_by_axis[axis] = values
        eligible = [axis for axis in AXES if orientation[axis]['converged_all_three']]
        best = max(eligible, key=lambda axis: min(orientation[axis]['sf_yield'], orientation[axis]['sf_layer'],
                                                  orientation[axis]['sf_shear']), default=None)
        o = orientation[best] if best else None
        roi = r.in_box([t, 13.0, bottom - 2, min(18.0, t + 15), 27.0, 54.0]) & r.away(dist=2.0)
        roi_vm, roi_at = r.peak(roi)
        result = {
            'token': token, 'thickness_mm': t, 'arm_height_mm': h,
            'volume_mm3': volume_mm3, 'mass_g': volume_mm3 * 0.00119,
            'bbox_mm': bb, 'hand_root_stress_mpa': nominal_root, 'hand_tip_deflection_mm': hand_tip,
            'print_orientation': f'layers stacked along {best}' if best else None,
            'helper_mesh_series_z': helper_rows, 'helper_converged_z': helper_converged_z,
            'orientation_table': orientation, 'series_by_axis': series_by_axis,
            'nodes': r.nodes, 'peak_vm_mpa': o['peak_vm_mpa'] if o else None,
            'peak_vm_at_mm': o['peak_vm_at_mm'] if o else None,
            'root_roi_vm_mpa': roi_vm, 'root_roi_at_mm': roi_at,
            'layer_stress_mpa': o['layer_stress_mpa'] if o else None,
            'layer_shear_mpa': o['layer_shear_mpa'] if o else None,
            'sf_yield': o['sf_yield'] if o else None, 'sf_layer': o['sf_layer'] if o else None,
            'sf_shear': o['sf_shear'] if o else None,
            'max_disp_mm': r.max_disp(), 'reaction_n': r.reaction[3] if r.reaction else None,
            'converged': bool(o),
        }
        result['verdict'] = ('pass' if result['converged'] and abs(result['reaction_n'] - 60) <= 0.6
                             and min(result['sf_yield'], result['sf_layer'], result['sf_shear']) >= 2
                             else 'fail' if o and min(result['sf_yield'], result['sf_layer'], result['sf_shear']) < 2
                             else 'not shown')
        result['status'] = 'complete'
        result['notes'] = 'Fixed screw-hole walls, normal load on exact 100 mm2 patch; see REPORT.md for limitations.'
        (RUN / out_path.name).write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
