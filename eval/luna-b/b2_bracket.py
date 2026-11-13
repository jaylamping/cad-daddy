"""B2: model, inspect, and evaluate the wall bracket with three mesh sizes and a support sensitivity case."""
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
from swkit import MID, Sk, bbox, bodies, expect, export, extrude, feature_errors, face_info, job, new_part, pick, plane, save, single_body, volume, edges_where, fillet  # noqa: E402
from swfea import PETG, converge, static  # noqa: E402


SIZES = (4.0, 3.5, 3.0)
ALLOW = {'vm': 45.0, 'layer': 22.5, 'shear': 13.0}


def expected_faces(d):
    holes = pick(d, kind='cyl', r=2.25)
    load = pick(d, kind='plane', normal=(0, 0, 1), at=(60, 20, 52), area=100)
    backing = pick(d, kind='plane', normal=(-1, 0, 0), at=(0, 20, 30))
    expect('two screw-hole walls', len(holes), 2, 0)
    expect('dedicated last-10-mm load face', len(load), 1, 0)
    expect('load face area mm2', face_info(load[0])['area'], 100, 0.05)
    expect('wall back face', len(backing), 1, 0)
    return holes, load, backing


def make_model(j):
    path = CAD / 'wall_bracket.SLDPRT'
    # Rebuild only this run's own prior output when rerunning the benchmark script.
    if path.exists():
        path.unlink()
    d = new_part(j.sw, path)

    with Sk(d, plane(d, 'X', 2.5, 'WALL_P'), 'WALL') as s:
        s.rect((2.5, 0, 0), (2.5, 40, 60))
    extrude(d, s.feat, 'WALL', 5.0, mode=MID, expect_dv=5 * 40 * 60)
    save(d)

    with Sk(d, plane(d, 'X', 35.0, 'ARM_P'), 'ARM') as s:
        s.rect((35, 15, 40), (35, 25, 52))
    extrude(d, s.feat, 'ARM', 60.0, mode=MID, expect_dv=60 * 10 * 12)
    save(d)

    root = edges_where(d, lambda p: abs(p[0] - 5.0) < 0.02 and min(abs(p[2] - 40.0), abs(p[2] - 52.0)) < 0.02
                       and 14.9 <= p[1] <= 25.1)
    expect('root edges along Y', len(root), 2, 0)
    radius = fillet(d, root, (3.0,), 'ROOT_FILLET')
    if radius is None:
        raise RuntimeError('R3 root fillet did not build')
    expect('root fillet radius', radius, 3.0, 0)
    save(d)

    # A 0.1 mm step gives the specified last-10-mm top load patch its own planar face (05-fea.md).
    v0 = volume(d)
    with Sk(d, plane(d, 'Z', 51.95, 'LOAD_STEP_P'), 'LOAD_STEP') as s:
        s.rect((10.0, 14.0, 51.95), (55.0, 26.0, 51.95))
    extrude(d, s.feat, 'LOAD_STEP', 0.1, cut=True, mode=MID)
    dv = v0 - volume(d)
    expect('load-face step removed volume mm3', dv, 45.0, 0.01)
    save(d)

    with Sk(d, plane(d, 'X', 2.5, 'SCREW_P'), 'SCREWS') as s:
        s.circle((2.5, 20.0, 12.0), 2.25)
        s.circle((2.5, 20.0, 48.0), 2.25)
    # Exactly the 5 mm wall-plate thickness. The upper hole meets the arm at X=5; see REPORT.md.
    extrude(d, s.feat, 'SCREW_HOLES', 5.0, cut=True, mode=MID, expect_dv=2 * math.pi * 2.25 ** 2 * 5)
    save(d)

    if feature_errors(d):
        raise RuntimeError(f'feature errors: {feature_errors(d)}')
    single_body(d)
    expect('one bracket body', len(bodies(d)), 1, 0)
    b = bbox(d)
    for k, want in enumerate((0, 0, 0, 65, 40, 60)):
        expect(f'bracket box[{k}] mm', b[k], want, 0.02)
    hand_volume = (5 * 40 * 60 + 60 * 10 * 12 + 2 * 3 ** 2 * (1 - math.pi / 4) * 10
                   - 45 - 2 * math.pi * 2.25 ** 2 * 5)
    expect('bracket volume mm3', volume(d), hand_volume, 0.1)

    # Measure the hole centres from the finished cylindrical faces.
    holes = pick(d, kind='cyl', r=2.25)
    expect('screw-hole cylindrical faces after fillet and step', len(holes), 2, 0)
    centers = sorted(tuple(round((face_info(f)['box'][i] + face_info(f)['box'][i + 3]) / 2, 2) for i in (1, 2))
                     for f in holes)
    if centers != [(20.0, 12.0), (20.0, 48.0)]:
        raise RuntimeError(f'finished screw-hole centres are {centers}')
    expected_faces(d)
    save(d)
    export(j.sw, d, CAD / 'wall_bracket.stl')
    return d


def save_result(r, key):
    SIM.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(SIM / f'{key}.npz', pos=r.pos, stress=r.s, displacement=r.disp,
                        fixed_points=r.fixed_pts, loaded_points=r.loaded_pts)


def evaluate(j, d):
    j.simulation()
    # Re-open after Simulation is loaded, then rebuild before any geometry picks.
    from swkit import close, open_doc  # local to make the required order visible
    close(j.sw, d)
    d = open_doc(j.sw, CAD / 'wall_bracket.SLDPRT')
    d.ForceRebuild3(False)
    volume_mm3 = volume(d)
    results = []
    expected_hand = 60 * 55 * 6 / (10 * 12 ** 3 / 12)
    print(f'PREDICTION hand root stress={expected_hand:.3f} MPa; beam deflection ~1.27 mm; peak near root fillet; '
          f'nodes by plain-part estimate at {SIZES}: '
          + ', '.join(str(round(12 * volume_mm3 / el ** 3)) for el in SIZES), flush=True)

    def runner(el):
        holes, load, _ = expected_faces(d)
        # Add local control at the small loading patch and the two cylindrical screw walls.
        estimate = round(12 * volume_mm3 / el ** 3)
        print(f'PREDICT B2 el={el:.2f} mm nodes={estimate}; peak near root fillet, displacement about 1.27 mm', flush=True)
        r = static(j, d, f'B2_fixed_{el:.2f}', PETG, fixtures=[('fixed', holes)], loads=[('normal', load, 60.0)],
                   el=el, ctrl=[(load, 1.0), (holes, 1.0)], max_nodes=199999)
        save_result(r, f'B2_fixed_{el:.2f}')
        results.append(r)
        return r

    # Y is the hand-predicted best layer normal: bending stress lies in the print plane and the dominant XZ beam shear
    # also lies in the layer plane. All three axes are calculated from each same solve below.
    rows, converged_y = converge(runner, SIZES, tol=0.05, layers=(0, 1, 0))
    r = results[-1]
    stable_dist = 2 * max(SIZES)
    orientations = {}
    for label, n in (('X', (1, 0, 0)), ('Y', (0, 1, 0)), ('Z', (0, 0, 1))):
        keep = r.away(dist=stable_dist)
        vm, at = r.peak(keep)
        layer, layer_at = r.layer_stress(n, keep)
        shear, shear_at = r.layer_shear(n, keep)
        orientations[label] = {'peak_vm_mpa': vm, 'peak_vm_at_mm': at, 'layer_stress_mpa': layer,
                               'layer_stress_at_mm': layer_at, 'layer_shear_mpa': shear,
                               'layer_shear_at_mm': shear_at, 'sf_vm': ALLOW['vm'] / vm,
                               'sf_layer': ALLOW['layer'] / layer if layer > 0 else None,
                               'sf_shear': ALLOW['shear'] / shear if shear > 0 else None}
    root_roi = r.in_box([5.0, 14.0, 38.0, 18.0, 26.0, 54.0]) & r.away(dist=2.0)
    root_peak, root_at = r.peak(root_roi)
    raw_peak = float(r.vm.max())
    raw_at = r.pos[int(np.argmax(r.vm))].round(2).tolist()

    # A second support idealization gives a bound on fixture sensitivity (whole wall face fixed); it is not the physical
    # screw boundary condition. Keep the same coarse mesh and loads.
    holes, load, backing = expected_faces(d)
    alt = static(j, d, 'B2_backface_support', PETG, fixtures=[('fixed', backing)], loads=[('normal', load, 60.0)],
                 el=SIZES[0], ctrl=[(load, 1.0)], max_nodes=199999)
    save_result(alt, 'B2_backface_support')
    alt_vm, alt_at = alt.peak(alt.away(dist=2 * SIZES[0]))

    # Plain section readback at mid-arm, about 25 mm from the load centroid, one full section from the root.
    section = r.in_box([34.5, 18.5, 51.5, 35.5, 21.5, 52.01])
    sec_vm = float(r.vm[section].mean()) if section.any() else None
    per_axis = {}
    for label, n in (('X', (1, 0, 0)), ('Y', (0, 1, 0)), ('Z', (0, 0, 1))):
        series = []
        for item in results:
            keep = item.away(dist=stable_dist)
            series.append([item.peak(keep)[0], item.layer_stress(n, keep)[0], item.layer_shear(n, keep)[0]])
        last = np.array(series[-1], dtype=float)
        prev = np.array(series[-2], dtype=float)
        ok = bool(np.all(np.abs(last - prev) <= 0.05 * np.maximum(np.abs(last), 1e-9)))
        per_axis[label] = {'series_vm_layer_shear': series, 'converged_all_three': ok}
    eligible = [axis for axis in orientations if per_axis[axis]['converged_all_three']]
    best = max(eligible, key=lambda axis: min(orientations[axis]['sf_vm'], orientations[axis]['sf_layer'],
                                               orientations[axis]['sf_shear']), default=None)
    o = orientations[best] if best is not None else None
    converged = bool(best is not None and per_axis[best]['converged_all_three'])
    reaction = r.reaction[3] if r.reaction else None
    max_disp = r.max_disp()
    pass_all = (converged and reaction is not None and abs(reaction - 60) <= 0.6 and max_disp is not None
                and o['sf_vm'] >= 2 and o['sf_layer'] >= 2 and o['sf_shear'] >= 2)
    verdict = 'pass' if pass_all else ('fail' if o is not None and
                                       (o['sf_vm'] < 2 or o['sf_layer'] < 2 or o['sf_shear'] < 2) else 'not shown')
    support_path = RUN / 'b2_support_result.json'
    if pass_all and support_path.exists():
        support_result = json.loads(support_path.read_text(encoding='utf-8'))
        if support_result.get('best_converged_orientation') is None:
            verdict = 'not shown'
    ans = {
        'hand_root_stress_mpa': expected_hand,
        'hand_tip_deflection_mm': (
            6 / (6 * (PETG['EX'] / 1e6) * (10 * 12 ** 3 / 12)) *
            ((60 * 60 ** 3 - 60 ** 4 / 4) - (60 * 50 ** 3 - 50 ** 4 / 4)) +
            (60 * 50 + 6 * 10 ** 2 / 2) /
            ((5 / 6) * (PETG['EX'] / 1e6) / (2 * (1 + PETG['NUXY'])) * (10 * 12))
        ),
        'print_orientation': f'layers stacked along {best}' if best else None,
        'nodes': r.nodes,
        'mesh_series': rows,
        'orientation_table': orientations,
        'convergence_by_orientation': per_axis,
        'peak_vm_mpa': o['peak_vm_mpa'],
        'peak_vm_at_mm': o['peak_vm_at_mm'],
        'root_roi_vm_mpa': root_peak,
        'root_roi_at_mm': root_at,
        'raw_vm_including_exclusions_mpa': raw_peak,
        'raw_vm_at_mm': raw_at,
        'layer_stress_mpa': o['layer_stress_mpa'],
        'layer_shear_mpa': o['layer_shear_mpa'],
        'sf_yield': o['sf_vm'],
        'sf_layer': o['sf_layer'],
        'sf_shear': o['sf_shear'],
        'max_disp_mm': max_disp,
        'reaction_n': reaction,
        'converged': converged,
        'converged_y_from_helper': converged_y,
        'plain_section_mean_vm_mpa': sec_vm,
        'support_sensitivity': {'wall_face_fixed_coarse_vm_mpa': alt_vm, 'at_mm': alt_at, 'nodes': alt.nodes},
        'status': 'complete',
        'verdict': verdict,
        'notes': 'Peak excludes nodes within 8 mm of fixture and load for mesh-series comparability; see REPORT.md for the root ROI and support sensitivity.'
    }
    (RUN / 'b2_result.json').write_text(json.dumps(ans, indent=2), encoding='utf-8')
    print(json.dumps(ans, indent=2), flush=True)
    return ans


def main():
    with job(wait_s=1800) as j:
        d = make_model(j)
        evaluate(j, d)


if __name__ == '__main__':
    main()
