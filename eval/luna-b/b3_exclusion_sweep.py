"""Check whether the B3 fixed-hole exclusion distance is hiding the layer-shear peak."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
SIM = ROOT / 'cad' / '_sim' / 'sw-eval' / 'luna-b'
sys.path.insert(0, str(ROOT / 'tools' / 'solidworks'))
from swfea import Result  # noqa: E402

files = {
    4.0: 'B3_t3p0_h12p0_4.00.npz', 3.5: 'B3_t3p0_h12p0_3.50.npz',
    3.0: 'B3_t3p0_h12p0_3.00.npz', 2.5: 'B3_t3_refine_2.50.npz',
    2.0: 'B3_t3_fine_2.00.npz', 1.5: 'B3_t3_fine_1.50.npz', 1.2: 'B3_t3_fine_1.20.npz',
}
series_by_distance = {}
for dist in (8.0, 10.0, 12.0):
    rows = []
    for el, filename in files.items():
      with np.load(SIM / filename) as data:
        r = Result(f'B3_fine_{el}', el, data['pos'], data['stress'], data['fixed_points'], data['loaded_points'],
                   data['displacement'], [0.0, 0.0, 60.0, 60.0], len(data['pos']), 0, 0, 60.0)
      keep = r.away(dist=dist)
      vm, vm_at = r.peak(keep)
      orientation = {}
      for axis, n in {'X': (1, 0, 0), 'Y': (0, 1, 0), 'Z': (0, 0, 1)}.items():
          ls, ls_at = r.layer_stress(n, keep)
          sh, sh_at = r.layer_shear(n, keep)
          orientation[axis] = {'layer_tension_mpa': ls, 'layer_tension_at_mm': ls_at,
                               'layer_shear_mpa': sh, 'layer_shear_at_mm': sh_at,
                               'sf_yield': 45 / vm, 'sf_layer': 22.5 / ls if ls > 0 else None,
                               'sf_shear': 13 / sh if sh > 0 else None}
      rows.append({'el_mm': el, 'nodes': len(r.pos), 'peak_vm_mpa': vm, 'peak_vm_at_mm': vm_at,
                   'orientations': orientation})
    last, prev = rows[-1], rows[-2]
    convergence = {}
    for axis in ('X', 'Y', 'Z'):
        a = [last['peak_vm_mpa'], last['orientations'][axis]['layer_tension_mpa'], last['orientations'][axis]['layer_shear_mpa']]
        b = [prev['peak_vm_mpa'], prev['orientations'][axis]['layer_tension_mpa'], prev['orientations'][axis]['layer_shear_mpa']]
        convergence[axis] = [abs(x-y) / max(abs(x), 1e-9) <= 0.05 for x, y in zip(a,b)]
    series_by_distance[str(dist)] = {'series': rows, 'last_step_convergence': convergence}
out = {'exclusion_distances_mm': [8.0, 10.0, 12.0], 'series_by_common_distance': series_by_distance}
(RUN / 'b3_exclusion_sweep.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps(out, indent=2), flush=True)
