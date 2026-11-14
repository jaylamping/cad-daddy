"""Assemble eval/haiku-d/results.json from the run outputs (d1_*.json, d3_table1/2.json) and the decisions in the report."""
import json
from pathlib import Path

E = Path(__file__).resolve().parent
t1 = json.loads((E / 'd3_table1.json').read_text(encoding='utf-8'))
t2 = json.loads((E / 'd3_table2.json').read_text(encoding='utf-8'))
s1 = json.loads((E / 'd1_study_results.json').read_text(encoding='utf-8'))
r1 = json.loads((E / 'd1_r1_results.json').read_text(encoding='utf-8'))
cv = json.loads((E / 'd1_conv_el1.json').read_text(encoding='utf-8'))

WHY = {
    'P1': (True, 'Ring B turned 45 deg: as written its counterbore (R30, Ø8) and ring A Ø3.4 hole at 0 deg overlap by 0.7 mm'),
    'P2': (True, 'Ring B turned 30 deg: as written rings A and B are the same 6 holes'),
    'P3': (False, 'Built as written'),
    'P4': (True, 'OD 60 -> 68: as written ring B holes and counterbores break out of the OD by 3.0 mm; counterbore depth 4.6 -> 4.0 (0.4 mm floor)'),
    'P5': (False, 'Built as written'),
    'P6': (False, 'Built as written'),
}
THK_B = {'P1': 7.5, 'P2': 7.5, 'P3': 9.5, 'P4': 6.5, 'P5': 9.5, 'P6': 7.5}

plates, plates_b = {}, {}
for k in ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']:
    v = t1[k]
    plates[k] = dict(volume_mm3=v['volume_sw_mm3'], hand_volume_mm3=v['volume_hand_mm3'], mass_g=v['mass_g'],
                     bodies=v['bodies'], stl_watertight=v['stl_watertight'], stl_volume_mm3=v['stl_volume_mm3'],
                     min_wall_mm=v['hand_checks']['min_wall_mm'], min_wall_at=v['hand_checks']['min_wall_at'],
                     counterbore_floor_z_mm=v['hand_checks']['counterbore_floor_from_bottom_mm'],
                     changed=WHY[k][0], why=WHY[k][1])
    v = t2[k]
    plates_b[k] = dict(volume_mm3=v['volume_sw_mm3'], hand_volume_mm3=v['volume_hand_mm3'], mass_g=v['mass_g'],
                       thickness_mm=THK_B[k], bodies=v['bodies'], stl_watertight=v['stl_watertight'],
                       stl_volume_mm3=v['stl_volume_mm3'], min_wall_mm=v['hand_checks']['min_wall_mm'],
                       min_wall_at=v['hand_checks']['min_wall_at'], counterbore_floor_z_mm=v['counterbore_floor_z_mm'],
                       chamfer_mm=v['chamfer_mm'],
                       changed=True, why='Thicker 1.5 mm; counterbore depth +1.5 keeps the floor; top outside chamfer'
                       + ('; ring A on R35 turned 22.5 deg' if k == 'P3' else ''))

results = {
    'D1': dict(
        status='done', minutes=11,
        notes=('Idea A (standing frame on the rail front, Y 10 to 14, bosses to Y 17.5) built and studied for 9 N pull and push. '
               'Reaction 9.00 N. Surface sz at the side-bar root 4.76 MPa against hand 4.77. Max displacement 1.94 mm against hand 1.06 mm '
               '(1.8 times; the top bar also bends, not checked further). Sharp opening corners are singular (8.99 MPa at 1.5 mm, 10.25 at 1.0), '
               'so R1 fillets were added in a copy: 10.67 and 10.75 MPa, 0.8 % apart. Open area 48.7 % with the rail behind the board counted '
               '(fails 50 %), 58.5 % without. Front components are limited to 5.9 mm by the Y 25 envelope, so the 14 mm allowance is not met. '
               'M3 pilot holes and inserts in the bosses are not modelled.'),
        mass_g=round(8824.15 * 1.19e-3, 2), parts=1,
        fasteners=[
            {'type': 'M3 screw through board hole into boss', 'count': 4, 'reach': 'from the board front with a 2.5 mm hex'},
            {'type': 'M5 x 20 with T-nut in rail front T-slot, through bottom bar Ø5.5', 'count': 2,
             'reach': 'behind the board, reached only after the board is off'}],
        board_removal_steps=[
            'Unplug the two 4 mm2 pairs at the 60 mm wire edge (X +42.5).',
            'With a 2.5 mm hex from the front, remove the four M3 screws in the board holes.',
            'Pull the board forward (+Y) off the four bosses. The mount and its M5 screws stay on the rail.'],
        open_area_share=0.487, open_area_front=0.970, open_area_back_no_rail=0.585,
        envelope_ok=False,
        sf_min=round(45 / 10.75, 2),
        governing='In-plane bending at the R1 fillet where the side bar meets the bottom bar on the rail face (10.7 MPa, 9 N pull)',
        print_orientation='Mount lying flat on the bed (Y up, layers in XZ), bosses up, no supports; one piece',
        assumptions=[
            'Board stands in the XZ plane (only orientation that fits Y ±25)',
            'Envelope applies to the mount, not the board',
            'Rail rigid, bears on the two M5 screws',
            'Board holes Ø3.2 at X ±39, Z -13.5 and 39.5',
            '9 N as 2.25 N per boss, pull and push cases'],
        questions=[
            'Does the Y ±25 envelope include the board and its components? (assumed: no)',
            'Is the 14 mm front clearance a hard need? (assumed: no, 5.9 mm)',
            'Does a rail 7.5 mm behind the board count against open area? (assumed: yes)',
            'Is M3 access from the front enough? (assumed: yes)'],
        ideas_tried=[
            'A: standing frame on the rail front (built)',
            'B: horizontal cradle on top of the rail (picture only; the 60 mm board across Y breaks the envelope by 5 mm each side)'],
        hand_checks=dict(sigma_root_mpa=4.77, fea_surface_sz_mpa=4.76, disp_hand_mm=1.06, disp_fea_mm=1.94, reaction_n=9.00),
        studies=s1 + r1,
        convergence_sharp=cv,
        nodes=dict(sharp_1p5=37590, sharp_1p0=cv['nodes'], r1_1p5=r1[0]['nodes'], r1_1p0=r1[1]['nodes'])),
    'D2': dict(
        status='partial', minutes=6,
        notes=('Two halves and the ring built and checked: volumes match hand, no feature errors, STL and picture sheets made. '
               'NOT DONE: no contact study for either load case, no screw load from a study, contact not proved. The brief needs ring-to-seat '
               'and half-to-half contact, which is a multi-body model with clearances and screws, not attempted in the time left. '
               'The design also does not clamp the ring radially (S6).'),
        spec_problems=[
            'S1 screws at X ±28.2: wall from Ø3.4 hole to seat 0.5 mm (0.2 mm for the Ø4.0 insert). Built at X ±30: 2.5 and 2.2 mm',
            'S2 seat Ø52.0 equals ring OD 52.0: zero fit, and ±0.15 mm printing gives loose or too tight. Built Ø51.6: 0.4 mm diametral interference',
            'S3 shoulder opening Ø43.5 is smaller than the inner ring OD 44.0: rubs the turning inner ring on its end face. Built Ø44.4: 0.2 mm clear',
            'S4 split gap not given. Built 0.4 mm (0.2 each half)',
            'S5 screws at Z 1 and 6 are 5 mm apart with Ø6 counterbores: 1 mm overlap, and SolidWorks refuses the cut. Built Z 0.5 and 7.5 (1 mm web)',
            'S6 clamp: Y-screws closing a 0.4 mm split on a concentric seat change its radius by about 0.0008 mm (hand: d²/8R, d/2 = 0.2, R = 25.8). '
            'The halves do not squeeze the ring; it is held by interference only. Not fixed: needs an offset (pinched) seat, not tested'],
        seat_diameter_mm=51.6, split_gap_mm=0.4,
        fit_reasoning=('Ring OD 52.0 into seat 51.6 is 0.2 mm radial interference per side. Printing ±0.15 mm on the seat gives an interference '
                       'of 0.25 to 0.55 mm diametral, so the ring is pressed in. The Y screws do not clamp it radially (S6).'),
        clearances_mm=dict(ring_to_seat_diametral=-0.4, inner_ring_to_shoulder_radial=0.2, screw_3p4_to_seat=2.5,
                           insert_4p0_to_seat=2.2, counterbore_to_outside=3.0, split_gap=0.4),
        hand_screw_load_n=75.0,
        hand_screw_load_note='300 N along +Y: four screws in tension, 75 N each. 300 N along +X: 75 N shear each (no friction).',
        screw_load_n=None, nodes=None, how_bodies_were_held='not run', contact_proof='not run',
        sf_yield=None, sf_layer=None, sf_shear=None, governing=None,
        print_orientation=('Each half printed with the bearing axis Z up (layers in XY, so screw and bearing loads act in-layer). '
                           'The seat ledge at Z 7 is a 3.6 mm radial overhang: needs support inside the seat.'),
        valid=False,
        why='No contact study run and no load result. The design does not clamp the ring radially (S6).',
        masses_g=dict(upper=round(19551.37 * 1.19e-3, 2), lower=round(20279.30 * 1.19e-3, 2), ring_steel=round(2199.11 * 7.85e-3, 2)),
        volumes_mm3=dict(upper=19551.37, lower=20279.30, ring=2199.11)),
    'D3': dict(
        status='done', minutes=4,
        notes=('Part one: one script built P1 to P6 from the table. Each feature checked against its hand volume; STL watertight and one body, '
               'STL volume within 0.2 % of the part. Part two: the saved parts were opened and edited (base depth, counterbore depth, chamfer; '
               'P3 ring A sketch redrawn) and saved as _b. Feature trees before and after match except the added chamfer. '
               'Table problems were found before building; every changed row is in plates[].why.'),
        plates=plates, plates_b=plates_b,
        table_problems=[
            'Column "on circle Ø" is a pitch-circle diameter. Read as radius, every hole lands outside the plate. Built with R = Ø/2.',
            'P1: ring A (Ø3.4 on R25, 0 deg) and ring B counterbore (Ø8 on R30, 0 deg) overlap by 0.7 mm. Ring B turned 45 deg (min wall 1.0 mm).',
            'P2: ring A and ring B are identical (6 x Ø4.5 on Ø62, both 0 deg): duplicate holes. Ring B turned 30 deg.',
            'P4: ring B holes and counterbores at R29 break out of OD 60 by 3.0 mm. OD raised to 68 (1.0 mm wall at the counterbore).',
            'P4: counterbore 8 x 4.6 in a 5 mm plate leaves a 0.4 mm floor, below the 0.6 mm wall rule. Depth set to 4.0 (floor 1.0 mm).',
            'P1, P3, P4: a 1.0 mm wall at the counterbore spots, so a 1.0 mm chamfer leaves no flat. Chamfer 0.5 mm there, 1.0 mm elsewhere.',
            'P3 part two: ring A on R35 at 0 deg leaves a 0.3 mm web to the ring B counterbore (Ø10 at R42). Turned 22.5 deg: min web 1.0 mm.'],
        one_script=True,
        edited_not_rebuilt=True,
        edited_not_rebuilt_evidence=('Part two opens each saved P*.SLDPRT and changes the BASE depth and CB depth with set_dim, '
                                     'redraws HA_SK for P3 with redraw_circles. Feature trees before and after match, plus TOP_CH. '
                                     'Nothing is rebuilt from the script.')),
}

(E / 'results.json').write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
print('written results.json', len(json.dumps(results)), 'chars')
