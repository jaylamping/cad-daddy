import json
o = json.load(open('d2_results_calc_d.json')); proof = json.load(open('d2_proof_d.json')); chk = json.load(open('d2_checks_results.json'))
res = dict(
    status='done',
    spec_problems=[
        dict(what='shoulder opening Ø43.5 is smaller than the Ø44.0 inner ring, whose end faces turn past it',
             number='0.25 mm radial overlap (the lip would sit on r 21.75..22 of the turning ring)',
             built='opening Ø46.0: 1.0 mm radial clear of the inner ring; the lip still backs the whole outer-ring face (r 24..26)'),
        dict(what='M3 screws at X 28.2 against the R26 seat',
             number='wall between the Ø3.4 clearance hole and the seat 0.5 mm, between the Ø4.0 insert hole and the seat 0.2 mm (both under 0.6)',
             built='X +-31.0: 3.3 mm and 3.0 mm'),
        dict(what='Ø6 counterbores at Z 1 and Z 6 (5 mm apart)', number='they overlap by 1.0 mm and merge into one slot',
             built='screws at Z 0 and 7: rib 1.0 mm between counterbores, 1.0 mm to the Z faces, still symmetric about the seat middle Z 3.5'),
        dict(what='seat width 7.0 for a 7.0 mm bearing, line to line', number='at +-0.15 the seat prints 6.85..7.15: it can pinch the ring axially',
             built='seat 7.3 (0.3 mm axial play; the clamp is radial)'),
        dict(what='Ø52 seat closing to a zero split gap cannot be shown to clamp a Ø52 ring on a +-0.15 printer',
             number='bore 51.85..52.15 against ring 52.0 (-0.013): from 0.163 loose to 0.15 tight',
             built='each half stands back 0.15 mm from the split plane (gap 0.30 before the screws close it): closed bore in Y is 51.55..51.85, interference 0.14..0.45 mm diametral'),
        dict(what='6 mm deep insert hole for an M3x35 screw (28.5 from the counterbore floor)', number='the screw tip reaches 6.5 mm below the split face',
             built='insert holes 7 mm deep (tip 0.5 mm clear); the 5.7 mm insert sits 0.5 mm below the face'),
        dict(what='no locating dowel between the halves', number='+Y pushes the ring into the upper half and off the lower; four M3 are the only link and none is a dowel',
             built='noted, not changed: sliding in X is held by screw shear and friction only (see weakest point)')],
    seat_diameter_mm=52.0, split_gap_mm=0.30,
    fit_reasoning=('The printer holds +-0.15 mm, so a line-to-line Ø52 seat cannot be shown to clamp: the bore prints 51.85..52.15 against a ring of 52.0 (-0.013). '
                   'Each half stands back 0.15 mm from the split plane, so before tightening the halves are 0.30 mm apart; the screws draw them together and the bore across Y '
                   'becomes bore - 0.30 = 51.55..51.85, always under the ring: 0.14 to 0.45 mm of diametral interference, taken up by the PETG halves (E 1.9 GPa against 210 for steel), not by the ring. '
                   'The split closes when the screws are snug, so the clamp is set by the screws, not by the print. Seat width 7.3 for the 7.0 bearing leaves 0.3 mm of axial play, so a -0.15 print cannot pinch it axially; '
                   'the shoulders (opening Ø46) back the outer ring end faces (r 24..26 against a lip from r 23) and clear the turning inner ring (r 22) by 1.0 mm radially, checked with 6,000 sampled points of the inner ring volume '
                   'and a sweep with 0.5 mm margin: 0 inside the housings. Printed on its split face (Y up) the seat is an open trough with no overhang.'),
    clearances_mm={'inner_ring_to_shoulder_opening_radial': 1.0,
                   'outer_ring_end_face_backed_by_lip': 'lip from r 23, face r 24..26 (2 mm of land, 1 mm of lip over the seal gap)',
                   'ring_to_seat_radial_before_closing': '0.0 nominal, -0.13..+0.15 on the print',
                   'ring_to_seat_after_closing_Y': 'interference 0.07 to 0.22 per side',
                   'seat_axial_play_over_7.0_bearing': 0.3, 'split_gap_before_tightening': 0.30, 'screw_shank_to_clearance_hole_radial': 0.2,
                   'screw_head_to_counterbore_radial': 0.25, 'screw_head_below_face': 0.5, 'screw_tip_to_insert_hole_bottom': 0.5,
                   'rib_between_counterbores': 1.0, 'counterbore_to_Z_faces': 1.0, 'insert_hole_to_seat': 3.0, 'clearance_hole_to_seat': 3.3,
                   'insert_hole_to_X_face': 3.0, 'M4_insert_hole_to_seat': '14 mm of Y at X 24',
                   'measured_in_STL': {'inner_ring_points_inside_housing': chk['inner_ring_points_inside_housing'],
                                       'inner_ring_sweep_r22.5_inside_housing': chk['inner_ring_sweep_with_0.5_radial_margin_inside_housing'],
                                       'split_gap_design': chk['split_gap_design_mm']}},
    hand_screw_load_n={'+Y': '75 per screw (300 / 4, ring on the upper seat only)',
                       '+X, first estimate': '23.9 per screw (cosine pressure on the seat: separating force F/pi = 95.5 N over four screws)',
                       '+X, after the study showed the patch': '28.5 per screw on average (114 N): the ring sits 21 degrees off the X axis (displacement 0.067 in Y over 0.177 in X), F tan 21 = 114'},
    screw_load_n={'+Y': {'per_screw': o['screws']['Y_3.0']['per_screw_N'], 'sum': o['screws']['Y_3.0']['sum_N'],
                         'sum_at_meshes_4.0_3.0_2.4': [o['screws'][f'Y_{e}']['sum_N'] for e in ('4.0', '3.0', '2.4')]},
                  '+X': {'per_screw': o['screws']['X_3.0']['per_screw_N'], 'sum': o['screws']['X_3.0']['sum_N'],
                         'sum_at_meshes_4.0_3.0_2.4': [o['screws'][f'X_{e}']['sum_N'] for e in ('4.0', '3.0', '2.4')]},
                  'note': ('tension = plane-fitted stress over the shank section at three heights times its area. +Y is 21-27 % over the hand value because of prying: '
                           'an independent section through the lower half just below the split reads -68 N (compression between the split faces) and 371 - 300 = 71 N. '
                           '+X: sum 132 against 114 by hand after the patch (16 %); the section below the split reads -103 to -112 N')},
    nodes=o['nodes']['Y'],
    how_bodies_were_held=('Lower half: face Y -32 fixed. Upper half: four steel pins (Ø3.0 shank in the Ø3.4 holes, head bonded on the counterbore floor, Ø4.0 end bonded in the insert hole) '
                          'and no-penetration contact on both patches of the split face (each half has two, X < -23 and X > 23). Ring (Ø51.9 x 7, 0.05 mm radial clearance, 0.4 mm chamfers): '
                          'four soft pads (E 0.5 MPa, Ø1.8 x 1.0) bonded between its end face and the floors of four 0.85 mm recesses in the shoulders; they carry 0.17 to 0.19 N of the 300 N (0.06 %, from their own shear and stretch). '
                          'The load is a bearing load on the ring bore.'),
    contact_proof=('Against a bonded twin, same mesh (74,551 nodes): +Y ring movement 0.140 mm against 0.0111 bonded (12.6 times), largest displacement 0.232 against 0.0348 (6.7 times), '
                   'screws +91..95 N each against -14 N (unloaded) bonded; the unloaded lower seat opens 0.126..0.140 mm at every angle from -180 to -30 degrees while the loaded upper arc is closed (0.000 from 0 to 150). '
                   '+X: movement 0.177 against 0.032 (5.5 times), screws 132 N against 36 N, the -X side opens 0.20 mm. Reaction 300.0 N in both. An independent section force through the lower half reads 295 N (-1.7 %) for +Y. '
                   'A section just below the split reads -68 N: the prying force at the split faces.'),
    sf_yield=6.4, sf_layer=5.9, sf_shear=4.6,
    governing=('lower half, +X case: shear between layers 2.87 MPa (printed split face up, factor 4.6); the same half has von Mises 7.07 MPa (6.4) and layer tension 3.79 MPa (5.9). '
               'Counting the nodes at the seat edge where it meets the split face (a contact edge) the peak is 9.4 MPa von Mises, factor 4.8'),
    print_orientation={'housing_upper': 'split face up, outer face Y +32 on the bed (layers stacked along Y): the seat is an open trough, counterbores and screw holes are vertical, no supports. Lowest factor 4.58 against 3.77 and 3.82 for the other two directions',
                       'housing_lower': 'split face up, mounting face Y -32 on the bed (layers along Y): the M4 insert holes open on the bed face and are filled from the mounting face; the insert holes at the split face are vertical'},
    valid=True,
    why=('Reaction 300.0 N in every solve; contact proved against the bonded twin; both patches of each split face are in the set (the first runs had one patch and were wrong: tags a and c, INVALID); '
         'pads carry 0.06 %; section check 295 N; hand screw loads differ by 21-27 % (+Y) and 16 % (+X) and the difference is accounted for by prying and the contact angle (section force below the split). '
         'Verdict margin, not converged: one entry (upper half +X layer tension, 2.26, 1.94, 1.28 MPa) falls 34 % at the last step. Valid for a snug joint in the split-closed state: no preload modelled'),
    minutes=None)
json.dump(res, open('d2_result.json', 'w'), indent=1)
print(res['sf_yield'], res['screw_load_n']['+Y']['per_screw'], res['nodes'])
