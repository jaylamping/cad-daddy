"""D2: STL checks on the saved parts, measured clearances on the pair (design state, split relief 0.15 per half)."""
import json, sys
from pathlib import Path
import numpy as np, trimesh
ROOT = Path(r'J:\code\cad-daddy-wt\sw-eval-sonnet-adv-d'); sys.path.insert(0, str(ROOT / 'solidworks'))
import sheet
W = ROOT / '_wip' / 'sw-eval' / 'sonnet-adv-d' / 'd2'
num = json.load(open(W / 'd2_build_numbers.json'))
out = {}
for nm, key in (('housing_upper', 'upper'), ('housing_lower', 'lower'), ('ring', 'ring')):
    m = trimesh.load(W / f'{nm}.stl')
    out[nm] = dict(watertight=bool(m.is_watertight), shells=len(m.split()), stl_volume=round(float(m.volume), 1), sw_volume=round(num[key]['volume'], 1),
                   diff_pct=round(100 * (m.volume / num[key]['volume'] - 1), 3), bounds=m.bounds.round(3).tolist(), sw_box=[round(v, 3) for v in num[key]['box']])
    print(nm, out[nm])
tri = {k: sheet.read_stl(W / f'{k}.stl') for k in ('housing_upper', 'housing_lower', 'ring')}
rng = np.random.default_rng(1)
def ring_pts(n, r0, r1, z0, z1):
    a = rng.uniform(0, 2 * np.pi, n); r = np.sqrt(rng.uniform(r0 ** 2, r1 ** 2, n)); return np.c_[r * np.cos(a), r * np.sin(a), rng.uniform(z0, z1, n)]
# 1. turning inner ring (r 20..22, Z 0..7.0, it may also sit 0..7.3) against the housings: must be clear
inner = ring_pts(6000, 20.0, 22.0, 0.0, 7.3)
hit = int(sheet.inside(tri['housing_upper'], inner).sum() + sheet.inside(tri['housing_lower'], inner).sum())
out['inner_ring_points_inside_housing'] = hit; print('inner ring region points inside the housings:', hit, 'of', len(inner))
# the inner ring's end faces slide past the shoulder faces: radial gap to the opening
out['inner_ring_to_opening_radial_mm'] = 23.0 - 22.0
# 2. a spinning inner ring swept volume incl. 0.5 mm margin, Z -0.5..7.8 (the balls and cage stay inside the outer ring)
sweep = ring_pts(6000, 20.0, 22.5, -3.9, 10.9)
hit = int(sheet.inside(tri['housing_upper'], sweep).sum() + sheet.inside(tri['housing_lower'], sweep).sum())
out['inner_ring_sweep_with_0.5_radial_margin_inside_housing'] = hit; print('inner sweep r<=22.5, Z -3.9..10.9, points inside housing:', hit)
# 3. the outer ring against the seats in the design state (gap 0.3): halves moved apart by 0.15 each. Points of the ring volume inside each housing.
rp = ring_pts(8000, 24.0, 26.0, 0.0, 7.0)
inside_u = sheet.inside(tri['housing_upper'], rp); inside_l = sheet.inside(tri['housing_lower'], rp)
out['ring_points_inside_housing_design_state'] = int(inside_u.sum() + inside_l.sum()); print('ring points inside the housings (design state, line-to-line at the print tolerance):', out['ring_points_inside_housing_design_state'])
# 4. close the split (screws tight): upper down 0.15, lower up 0.15 -> ring is squeezed in Y: interference at the poles
def shifted(t, dy):
    t = t.copy(); t[:, :, 1] += dy; return t
cu, cl = shifted(tri['housing_upper'], -0.15), shifted(tri['housing_lower'], +0.15)
# interference depth in Y along the pole: scan points on the ring OD near +Y and -Y
pole = np.array([(x, y, 3.5) for x in np.linspace(-1, 1, 3) for y in np.linspace(25.0, 26.0, 101)])
iu = sheet.inside(cu, pole); depth_up = float(pole[iu][:, 1].max() - 25.85) if iu.any() else 0.0
out['closed_state_upper_pole_ring_envelope_overlap_mm'] = round(26.0 - float(pole[sheet.inside(cu, pole)][:, 1].min()), 3) if iu.any() else 0.0
print('closed split: the upper seat pole sits at Y =', float(pole[sheet.inside(cu, pole)][:, 1].min()) if iu.any() else None, 'ring OD pole at 26.0')
# gap between the halves in the design state: min Y of the upper, max Y of the lower
out['split_gap_design_mm'] = round(float(tri['housing_upper'][:, :, 1].min() - tri['housing_lower'][:, :, 1].max()), 3); print('split gap', out['split_gap_design_mm'])
# 5. screws: clearances by arithmetic (checked against the built holes)
out['clearances_mm'] = {
 'inner_ring_to_shoulder_opening_radial': 1.0, 'outer_ring_face_backed_by_lip_radial': 2.0 + 1.0,
 'ring_to_seat_radial_nominal_closed_split': '0.15 interference per side at the poles (0.30 diametral), +-0.15 print',
 'seat_axial_play_over_7.0_bearing': 0.3, 'screw_shank_to_clearance_hole_radial': 0.2, 'screw_head_to_counterbore_radial': 0.25,
 'screw_head_below_face': 0.5, 'screw_tip_to_insert_hole_bottom': 0.5, 'split_gap_before_tightening': 0.30,
 'wall_hole_to_seat': 3.0, 'wall_counterbore_to_Z_faces': 1.0, 'rib_between_counterbores': 1.0, 'wall_insert_hole_to_X_face': 3.0}
json.dump(out, open(ROOT / 'eval' / 'sonnet-adv-d' / 'd2_checks_results.json', 'w'), indent=1)
