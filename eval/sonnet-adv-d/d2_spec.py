"""D2: the specification checked by hand before anything is built (numbers in mm)."""
import math, json
R_SEAT, RING_OD, RING_ID, INNER_OD = 26.0, 52.0, 48.0, 44.0
out = {}
out['opening_vs_inner_ring'] = dict(spec_opening=43.5, inner_ring_od=INNER_OD, overlap_radial=(INNER_OD - 43.5) / 2,
    note='lip of the shoulder would cover r 21.75..22 of the turning inner ring (0.25 mm), and touch it')
out['opening_built'] = dict(opening=46.0, clear_to_inner_ring_radial=(46.0 - INNER_OD) / 2, lip_covering_outer_ring_face=(RING_OD - 46.0) / 2 - 0, outer_ring_face_r=(24.0, 26.0),
    note='lip r 23..; outer ring end face spans r 24..26 so the lip fully backs it; r 23..24 faces the seal gap')
# screw holes at X 28.2 against the seat R26 (seat edge at the split plane)
for name, d in (('clearance hole d3.4', 3.4), ('insert hole d4.0', 4.0), ('counterbore d6', 6.0)):
    out['wall_to_seat_at_x28.2 ' + name] = round(28.2 - d / 2 - R_SEAT, 3)
    out['wall_to_seat_at_x31 ' + name] = round(31.0 - d / 2 - R_SEAT, 3)
out['counterbores_z1_z6'] = dict(centre_spacing=5.0, diameter=6.0, overlap=6.0 - 5.0)
out['counterbores_z0_z7'] = dict(centre_spacing=7.0, rib=7.0 - 6.0, wall_to_Z_faces=(0 - 3 - (-4), 11 - 10))
out['counterbore_in_x_at_31'] = dict(outer_edge=31 + 3, envelope=36, wall=36 - 34)
# fit on a +-0.15 printer: Y diameter of the closed bore = bore - gap; ring OD 52 (-0.013)
for g in (0.0, 0.2, 0.3, 0.4):
    out[f'gap_{g}'] = dict(interference_diametral_min=round(52 - 0.013 - (52.15 - g), 3), max=round(52 - (51.85 - g), 3))
# screw length
out['screw'] = dict(counterbore_floor_y=32 - 3.5, length_needed_for_5mm_engagement=28.5 + 5, note='M3x35 reaches 6.5 below the split face; the 6 mm hole is 0.5 short, built 7 mm deep')
# hand screw loads, 300 N
F = 300.0
out['hand_screw_Y_per_screw'] = F / 4
# cosine pressure on the seat for +X: half of the seat sees p0 cos(phi), |phi|<90; Y component per half (separating force)
sep_cos = F / math.pi          # total separating force per half-ring, cosine pressure over 180 deg (ratio 1/pi)
out['hand_screw_X_cosine'] = dict(separating_force_N=sep_cos, per_screw_N=sep_cos / 4, note='ring seated all round the half; first estimate, redone after the study shows the patch')
json.dump(out, open('d2_spec.json', 'w'), indent=1)
for k, v in out.items(): print(k, v)
