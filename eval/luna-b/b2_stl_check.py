"""Check B2's exported STL against the SolidWorks volume and bounding box."""
import json
from pathlib import Path

import trimesh

RUN = Path(__file__).resolve().parent
CAD = Path(__file__).resolve().parents[5] / 'cad' / '_wip' / 'sw-eval' / 'luna-b'
sw_volume = 19034.5852
sw_box = [0.0, 0.0, 0.0, 65.0, 40.0, 60.0]
mesh = trimesh.load(CAD / 'wall_bracket.stl', force='mesh')
box = mesh.bounds.reshape(-1).tolist()
out = {'watertight': bool(mesh.is_watertight), 'shells': len(mesh.split(only_watertight=False)),
       'stl_volume_mm3': float(mesh.volume), 'solidworks_volume_mm3': sw_volume,
       'volume_error_pct': 100 * abs(float(mesh.volume) - sw_volume) / sw_volume,
       'bounds_mm': box, 'solidworks_bounds_mm': sw_box,
       'max_bbox_delta_mm': max(abs(a - b) for a, b in zip(box, sw_box)), 'triangles': len(mesh.faces)}
if not out['watertight'] or out['shells'] != 1 or out['volume_error_pct'] > 0.5 or out['max_bbox_delta_mm'] > 0.1:
    raise RuntimeError(f'B2 STL check failed: {out}')
(RUN / 'b2_stl_checks.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps(out, indent=2), flush=True)
