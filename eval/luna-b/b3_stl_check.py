import json
from pathlib import Path
import trimesh
ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / 'cad' / '_wip' / 'sw-eval' / 'luna-b'
sw_volume = 9972.068470128394
sw_box = [0.0, 13.25, 5.25, 65.0, 26.75, 54.871]
mesh = trimesh.load(CAD / 'wall_bracket_light.stl', force='mesh')
box = mesh.bounds.reshape(-1).tolist()
out = {'watertight': bool(mesh.is_watertight), 'shells': len(mesh.split(only_watertight=False)),
       'stl_volume_mm3': float(mesh.volume), 'solidworks_volume_mm3': sw_volume,
       'volume_error_pct': 100 * abs(float(mesh.volume) - sw_volume) / sw_volume,
       'bounds_mm': box, 'solidworks_bounds_mm': sw_box,
       'max_bbox_delta_mm': max(abs(a - b) for a, b in zip(box, sw_box)), 'triangles': len(mesh.faces)}
if not out['watertight'] or out['shells'] != 1 or out['volume_error_pct'] > 0.5 or out['max_bbox_delta_mm'] > 0.1:
    raise RuntimeError(f'B3 STL check failed: {out}')
(RUN / 'b3_stl_checks.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps(out, indent=2), flush=True)
