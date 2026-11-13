"""Refine B3 t3/h12 for the Y layer orientation, which was near an FoS of 2 but not yet converged."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / 'cad' / '_wip' / 'sw-eval' / 'luna-b'
SIM = ROOT / 'cad' / '_sim' / 'sw-eval' / 'luna-b'
MODEL = CAD / 'wall_bracket_light_t3p0_h12p0.SLDPRT'
SIZES = (3.0, 2.5, 2.0)
AXES = {'X': (1, 0, 0), 'Y': (0, 1, 0), 'Z': (0, 0, 1)}
sys.path.insert(0, str(ROOT / 'tools' / 'solidworks'))
from swkit import expect, job, open_doc, pick, volume  # noqa: E402
from swfea import PETG, converge, static  # noqa: E402


def main():
    with job(wait_s=1800) as j:
        j.simulation()
        d = open_doc(j.sw, MODEL)
        d.ForceRebuild3(False)
        volume_mm3 = volume(d)
        results = []

        def runner(el):
            holes = pick(d, kind='cyl', r=2.25)
            load = pick(d, kind='plane', normal=(0, 0, 1), at=(60, 20, 52), area=100)
            expect(f'hole fixture faces el={el}', len(holes), 2, 0)
            expect(f'load patch faces el={el}', len(load), 1, 0)
            estimate = round(12 * volume_mm3 / el ** 3)
            print(f'PREDICT B3 refine el={el}: {estimate} nodes; test Y layer tension/shear stability, '
                  'peak near the arm root', flush=True)
            r = static(j, d, f'B3_t3_refine_{el:.2f}', PETG,
                       fixtures=[('fixed', holes)], loads=[('normal', load, 60.0)], el=el,
                       ctrl=[(holes, 1.0), (load, 1.0)], max_nodes=199999)
            results.append(r)
            SIM.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(SIM / f'B3_t3_refine_{el:.2f}.npz', pos=r.pos, stress=r.s, displacement=r.disp,
                                fixed_points=r.fixed_pts, loaded_points=r.loaded_pts)
            return r

        helper_rows, helper_converged_y = converge(runner, SIZES, tol=0.05, layers=(0, 1, 0))
        final = results[-1]
        dist = 2 * max(SIZES)
        orientation = {}
        series_by_axis = {}
        for axis, n in AXES.items():
            keep = final.away(dist=dist)
            vm, vm_at = final.peak(keep)
            ls, ls_at = final.layer_stress(n, keep)
            sh, sh_at = final.layer_shear(n, keep)
            series = []
            for r in results:
                m = r.away(dist=dist)
                series.append([r.peak(m)[0], r.layer_stress(n, m)[0], r.layer_shear(n, m)[0]])
            a, b = np.asarray(series[-2]), np.asarray(series[-1])
            conv = bool(np.all(np.abs(b - a) <= 0.05 * np.maximum(np.abs(b), 1e-9)))
            orientation[axis] = {'peak_vm_mpa': vm, 'peak_vm_at_mm': vm_at,
                                 'layer_stress_mpa': ls, 'layer_stress_at_mm': ls_at,
                                 'layer_shear_mpa': sh, 'layer_shear_at_mm': sh_at,
                                 'sf_yield': 45 / vm, 'sf_layer': 22.5 / ls if ls > 0 else None,
                                 'sf_shear': 13 / sh if sh > 0 else None, 'converged_all_three': conv}
            series_by_axis[axis] = series
        eligible = [a for a in AXES if orientation[a]['converged_all_three']]
        best = max(eligible, key=lambda a: min(orientation[a]['sf_yield'], orientation[a]['sf_layer'],
                                               orientation[a]['sf_shear']), default=None)
        output = {'candidate': 't3p0_h12p0', 'sizes_mm': SIZES, 'helper_rows_y': helper_rows,
                  'helper_converged_y': helper_converged_y, 'orientation_table': orientation,
                  'series_by_axis': series_by_axis, 'nodes': final.nodes,
                  'reaction_n': final.reaction[3] if final.reaction else None,
                  'max_disp_mm': final.max_disp(), 'best_converged_orientation': best}
        if best:
            output['best_orientation_factors'] = orientation[best]
        (RUN / 'b3_refine_y.json').write_text(json.dumps(output, indent=2), encoding='utf-8')
        print(json.dumps(output, indent=2), flush=True)


if __name__ == '__main__':
    main()
