"""B2 support sensitivity refinement, one second-support mesh series."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / 'cad' / '_wip' / 'sw-eval' / 'luna-b'
SIM = ROOT / 'cad' / '_sim' / 'sw-eval' / 'luna-b'
sys.path.insert(0, str(ROOT / 'tools' / 'solidworks'))
from swkit import job, open_doc, pick, face_info, expect  # noqa: E402
from swfea import PETG, converge, static  # noqa: E402

SIZES = (4.0, 3.5, 3.0)
AXES = {'X': (1, 0, 0), 'Y': (0, 1, 0), 'Z': (0, 0, 1)}


def main():
    with job(wait_s=1800) as j:
        j.simulation()
        d = open_doc(j.sw, CAD / 'wall_bracket.SLDPRT')
        d.ForceRebuild3(False)
        load = pick(d, kind='plane', normal=(0, 0, 1), at=(60, 20, 52), area=100)
        backing = pick(d, kind='plane', normal=(-1, 0, 0), at=(0, 20, 30))
        expect('load patch count', len(load), 1, 0)
        expect('back wall face count', len(backing), 1, 0)
        volume = sum(b.GetMassProperties(1000.0)[3] for b in d.GetBodies2(0, True)) * 1e9
        results = []

        def runner(el):
            # Re-pick after each result/save; COM faces can go stale across a study rebuild.
            load = pick(d, kind='plane', normal=(0, 0, 1), at=(60, 20, 52), area=100)
            backing = pick(d, kind='plane', normal=(-1, 0, 0), at=(0, 20, 30))
            expect(f'load patch at el={el}', len(load), 1, 0)
            expect(f'back wall at el={el}', len(backing), 1, 0)
            estimate = round(12 * volume / el ** 3)
            print(f'PREDICT B2 second support el={el} mm nodes={estimate}; peak near root fillet; displacement about 1.4 mm', flush=True)
            r = static(j, d, f'B2_wall_{el:.2f}', PETG, fixtures=[('fixed', backing)],
                       loads=[('normal', load, 60.0)], el=el, ctrl=[(load, 1.0)], max_nodes=199999)
            results.append(r)
            SIM.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(SIM / f'B2_wall_{el:.2f}.npz', pos=r.pos, stress=r.s, displacement=r.disp,
                                fixed_points=r.fixed_pts, loaded_points=r.loaded_pts)
            return r

        # The Z-normal layer series was converged under the hole-wall support; run the same convergence test for this
        # longer back-face support before comparing the physical quantity.
        helper_rows, converged_z = converge(runner, SIZES, tol=0.05, layers=(0, 0, 1))
        r = results[-1]
        dist = 2 * max(SIZES)
        orientation = {}
        all_series = {}
        for axis, normal in AXES.items():
            keep = r.away(dist=dist)
            vm, vm_at = r.peak(keep)
            ls, ls_at = r.layer_stress(normal, keep)
            sh, sh_at = r.layer_shear(normal, keep)
            series = []
            for q in results:
                m = q.away(dist=dist)
                series.append([q.peak(m)[0], q.layer_stress(normal, m)[0], q.layer_shear(normal, m)[0]])
            prev, last = np.array(series[-2]), np.array(series[-1])
            is_conv = bool(np.all(np.abs(last - prev) <= 0.05 * np.maximum(np.abs(last), 1e-9)))
            orientation[axis] = {'peak_vm_mpa': vm, 'peak_vm_at_mm': vm_at,
                                 'layer_stress_mpa': ls, 'layer_stress_at_mm': ls_at,
                                 'layer_shear_mpa': sh, 'layer_shear_at_mm': sh_at,
                                 'sf_yield': 45 / vm, 'sf_layer': 22.5 / ls if ls > 0 else None,
                                 'sf_shear': 13 / sh if sh > 0 else None,
                                 'converged_all_three': is_conv}
            all_series[axis] = series
        best = max((a for a in orientation if orientation[a]['converged_all_three']),
                   key=lambda a: min(orientation[a]['sf_yield'], orientation[a]['sf_layer'], orientation[a]['sf_shear']),
                   default=None)
        output = {'mesh_series_helper': helper_rows, 'converged_z_from_helper': converged_z,
                  'orientation_series': all_series, 'orientation_table': orientation,
                  'nodes': r.nodes, 'reaction_n': r.reaction[3] if r.reaction else None,
                  'max_disp_mm': r.max_disp(), 'best_converged_orientation': best}
        if best:
            output['best_orientation_factors'] = orientation[best]
        (RUN / 'b2_support_result.json').write_text(json.dumps(output, indent=2), encoding='utf-8')
        print(json.dumps(output, indent=2), flush=True)


if __name__ == '__main__':
    main()
