"""Writes D2 keys to results.json and the D2 section to REPORT.md, from d2_rows.json (the run's numbers)."""
from common import *  # noqa: F401,F403

R = json.loads((HERE / 'd2_rows.json').read_text(encoding='utf-8'))
y, yb, x = R['D2_Y_30'], R['D2_YBOND_30'], R['D2_X_30']
a, b = math.radians(x['angle_upper']), math.radians(x['angle_lower'])
N = 300 / (math.sin(a) + math.cos(a) * math.tan(b))
hand_t, hand_s = N * math.cos(a) / 4, N * math.sin(a) / 4
sf_y = min(y['upper']['Z']['sf_yield'], y['upper']['Z']['sf_layer'], y['upper']['Z']['sf_shear'])
mean_y = sum(s['tension'] for s in y['screws']) / 4
mean_x = sum(s['tension'] for s in x['screws']) / 4
pre_f = 75 * y['upper']['Z']['sf_yield'] / 2
put('D2',
    status='partial',
    spec_problems=[
        'shoulder opening D43.5 vs inner ring D44.0: 0.25 mm radial overlap -> built D49.0',
        'screws X +-28.2: insert hole wall 0.2 mm to the seat (min 0.6) -> built X +-30.0',
        'screws Z 1 and 6: counterbores overlap by 1.0 mm -> built Z 0 and 7',
        'seat D52 with +-0.15 printer tolerance: loose or grips -> seat D52.2, crown touching, split gap 0.8 mm',
        'seat Z 0..7 for a 7 mm ring: zero axial clearance -> seat Z -0.15..7.15',
        'M3x30 bottoms out in 6 mm insert hole (0.5 mm short) -> insert 8 deep, M3x35 (1.9 mm spare)'],
    seat_diameter_mm=52.2, split_gap_mm=0.8,
    fit_reasoning='seat 0.2 larger than the ring at nominal so the crown meets first and the screws pull the half round the ring; gap 0.8 mm exceeds tolerance (0.45 mm) so the screws load the ring, not the split faces',
    clearances_mm=dict(ring_to_seat_crown=0.0, ring_to_seat_split=0.1, halves_at_split=0.8, ring_side_to_shoulder=0.15,
                       inner_ring_to_opening=2.5, outer_ring_bore_to_opening=0.5, shaft_to_opening=4.5,
                       screw_in_clearance_hole=0.2, head_in_counterbore=0.25,
                       hole_wall_to_seat_clearance=2.2, hole_wall_to_seat_insert=1.9,
                       counterbore_to_counterbore=1.0, screw_tip_to_insert_floor=1.9),
    hand_screw_load_n=75.0, screw_load_n=round(mean_y, 1),
    screw_loads_case_y_n=[round(s['tension'], 1) for s in y['screws']],
    screw_loads_case_x_n=[round(s['tension'], 1) for s in x['screws']],
    hand_x_tension_redone_n=round(hand_t, 1), hand_x_shear_redone_n=round(hand_s, 1),
    study_x_tension_mean_n=round(mean_x, 1),
    nodes=160773,
    how_bodies_were_held='lower half: mount face Y -32 fixed; screws bonded under heads and in insert holes; upper half bonded to screws at counterbore floors; ring bonded to four soft pads (inner faces fixed); no-penetration contact ring-to-seat (both) and half-to-half',
    contact_proof=('bonded twin ring UY %.4f vs contact %.4f mm: ratio %.0fx; bonded screw sum %.1f N (under 100); '
                   'contact case lower seat opens by %.3f mm; lower seat pressure %.2f MPa = %.1f%% of upper (case Y)'
                   % (yb['ring_u'][1], y['ring_u'][1], y['ring_u'][1] / yb['ring_u'][1], yb['screw_sum'],
                      y['lower_seat_opens_by'], y['p_lower'], 100 * y['p_lower'] / y['p_upper'])),
    pads_share_n=round(sum(abs(v) for v in y['pads_reaction']), 2),
    sf_yield=round(sf_y, 2),
    sf_layer=round(min(y['upper']['Z']['sf_layer'], x['upper']['Z']['sf_layer']), 2),
    sf_shear=round(min(y['upper']['Z']['sf_shear'], x['upper']['Z']['sf_shear']), 2),
    governing='upper half, case X, von Mises at the counterbore edge beside a screw head (-27.3, 27.5, 6.8), 6.13 MPa at 3.0 mm mesh, not converged',
    print_orientation={'upper': 'bearing axis vertical, face Z -4 on the bed, layers along Z',
                       'lower': 'bearing axis vertical, face Z -4 on the bed, layers along Z'},
    valid=False,
    why='convergence not shown: finer meshes exceed the 200,000-node cap (D2_Y_22 solves to 224,652 nodes, refused before solve); the peak sits at a bonded counterbore rim and has not converged; contact proof done for case Y only',
    preload_factor2_force_n=round(pre_f, 0),
    preload_torque_nmm=round(0.2 * pre_f * 3, 0),
    minutes=75,
    notes='3.0 mm mesh only (160,773 nodes; 2.9x the predicted 55k). Case X: hand value redone with study angles: 45.3 N tension, 7.5 N shear per screw; study mean tension 45.1 N. Preload figures from the plan formula, not run.')

report("""## D2. Two halves round a bearing

Times: job 1 (build, fit) 14:25 to 14:26; study job 2 started 14:27:42 and ended about 14:36 (+Y 3.5 min, bonded twin 2 min,
+X 3.5 min, the refused 2.2 mm mesh 0.2 min). Waiting: SolidWorks launch 6 s; solves 104 s each; readback about 2.5 min each
(instance reported busy throughout). Working: the rest.

**Spec problems (plan section 2, checked against the build):** six, in results.json `spec_problems`: shoulder opening D43.5 overlaps
the inner ring by 0.25 mm (built D49.0); screws X +-28.2 leave 0.2 mm to the seat at the insert hole (built X +-30.0); screws Z 1
and 6 counterbores overlap 1.0 mm (built Z 0 and 7); seat D52 with +-0.15 printer tolerance (built D52.2, crown touching, gap
0.8 mm); seat Z 0..7 zero clearance (built -0.15..7.15); M3 x 30 bottoms out in the 6 mm insert hole (built 8 deep, M3 x 35,
1.9 mm spare).

**Build.** Upper 17981.68 mm3 measured (hand 17981.68), lower 18601.82 (hand 18601.82), ring 2199.11 (hand 2199.11), screws 352.21
each, pads 6.42 each; box and holes measured; one body per part; STL watertight, one shell. Assembly 11 bodies, volume 40217.15
(hand 40217.13). Pictures: pictures/d2_upper.png, pictures/d2_lower.png, pictures/d2_pair.png (made, not yet looked at by me).

**Fit check (STL, d2_fit.py).** Ring inside the upper and lower halves at r 24..25.9: 0 hits each side. At r 25.97 (0.03 mm inside
the ring's outer face at the crown): 54 hits per half, all at angles 75 to 105 deg, i.e. the crown. The B-rep seat box reads
+-26.095, so the seat is correct; the STL seat facets are inside the true circle by about 0.1 mm at the crown, so the STL test is
inconclusive at the 0.03 mm level. Shoulder sides: 0 hits at z -0.10 and 7.10, 714 hits at -0.20 and 7.20. Inner ring and shaft clear: 0 hits.

**Studies (3.0 mm mesh, 160,773 nodes, contact ring-to-seat and half-to-half; no preload).**

| Study | Max disp mm | Ring UY mm | Screw tension N (4) | Sum N | Peak upper vm MPa (factor) |
| --- | --- | --- | --- | --- | --- |
| D2_Y_30 (+Y 300 N) | 0.094 | 0.092 | 75.2, 75.1, 76.7, 75.8 | 302.7 | 4.57 (9.85) |
| D2_YBOND_30 (bonded twin) | 0.0018 | 0.0018 | 1.9, 2.0, 1.8, 1.9 | 7.6 | 0.09 |
| D2_X_30 (+X 300 N) | 0.555 | 0.136 | 41.3, 40.8, 49.5, 48.6 | 180.2 | 6.13 (7.34) |

- Reaction: Fy -300.0 N (case Y), Fx -300.0 N (case X); exact.
- Node count 160,773 against 55,000 predicted (2.9x). The playbook's stop rule was triggered: I checked the fixture box (mount face
  Y -32 and the pad faces) and the load box (ring sides), and the reaction and displacement (0.094 against 0.1 predicted). The
  model is the right one, so the stresses were kept. The node estimate was wrong, not the model.
- Contact proof (case Y): bonded twin ring UY 0.0018 mm against contact 0.092 mm: 50x stiffer (plan asks 5x). Bonded screw sum 7.6 N
  (asks under 100 N). Contact case: lower seat opens by 0.092 mm (positive). Lower seat pressure 0.098 MPa against upper 4.52 MPa:
  2.2 % (asks under 5 %). Pads' share in case Y: 0.23 N (plan asks under 3 N). Case X reversal proof not run.
- Case Y screws: mean 75.7 N against hand 75 N (within 1 %).
- Case X: the study put the lower seat in contact at 56 deg (p 8.33 MPa) and the upper at 9 deg (p 3.18 MPa), so the ring wedges
  under the lower half. The plan's hand value (23.9 N tension and 37.5 N shear, marked untrusted) is replaced by the redone statics
  with these angles: N_upper = 300 / (sin 9.40 + cos 9.40 tan 56.12) = 183.8 N; tension 45.3 N per screw, shear 7.5 N per screw.
  Study mean tension 45.1 N (within 1 %). Study shear by screw 11.8, 11.8, 3.8, 3.9 N: uneven between the X +30 and X -30 pairs.

**Three measures per half (layers along Z, bearing axis vertical).**
- Case Y upper: von Mises 4.57 MPa (factor 9.85 on 45 MPa), layer tension 0.87 (factor 25.7), shear 1.18 (factor 11.0).
- Case X upper: von Mises 6.13 MPa (factor 7.34), layer tension 0.76 (29.6), shear 1.41 (9.25).
- Case X lower: von Mises 5.13 MPa (8.8), layer tension 1.07 (20.9), shear 2.23 (5.8).
- Case Y lower: von Mises 2.62 MPa (17.2), layer 0.66 (34.3), shear 0.61 (21.4).
- Excluded 1 mm zones round the bonded heads and plugs had higher values (upper 8.7 MPa case Y, 12.4 case X; lower 6.1 and 6.7). These
  are the bonded-rim singularity the playbook names, so they are left out, as the plan's branch says.
- Expected crown stress was 5 to 15 MPa. The peak is not at the crown: it is at a counterbore edge beside a screw head, and it has not
  been shown to converge.
- Steel ring and screws judged as steel: ring 13.7 MPa (case Y), 24.6 (case X); screws 98 and 144 MPa, all under 640 MPa.

**Convergence: not shown.** The 2.2 mm mesh needs 224,652 nodes; D2_Y_22 was refused before solve by the 200,000 cap. The 1.7 mm
meshes would be larger, so the remaining rows (D2_X_22, D2_Y_17, D2_X_17) were not run: they cannot be solved under the rule. Verdict
"not shown"; `valid` false. Coarsening the steel, or cutting the upper half out and loading it with the forces from the full model,
are the playbook's next steps (not tried).

**Preload.** The studies have no preload. Screw force at which the upper half's factor falls to 2.0, by the plan's formula
(75 N times the lowest case-Y factor 9.85, over 2): 369 N per screw. Torque by the plan's formula, 0.2 x 369 x 3 = 222 N mm
(about 0.2 N m). Hand values only, not run.

**Thinnest margin:** case X upper, von Mises 7.3 at the 3.0 mm mesh, not converged. **Cheapest improvement (not done):** a 45 deg chamfer
under the upper lip, or the 52.1 seat (plan section 8). **Not verified:** preload, friction, insert pull-out, the real ring flexibility,
the as-printed seat, convergence of the peak.
""")
log('D2 results and report written at', minutes(), 'min')
