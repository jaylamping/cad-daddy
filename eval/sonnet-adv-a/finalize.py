"""Write the T3, T4, T5 (and T6 when its rows exist) keys into results.json from the rows files and judge_all.json."""
import json
from common import *

REG_ALL, REG_CLR = 'hole rims (all nodes)', 'hole rims (0.6 mm clear of loaded faces)'
J = json.loads((RUN / 'judge_all.json').read_text(encoding='utf-8'))
t3 = json.load(open(RUN / 't3_rows.json'))
t4 = json.load(open(RUN / 't4_rows.json'))
t5b = json.load(open(RUN / 't5b_rows.json'))

# ---------------- T3 ----------------
rows = t3['rings_holes_fixed']
fin = rows[-1]
bot = t3['rings_bottom_fixed'][-1]
rem_bore = t3['remote_bore_holes_fixed'][-1]
rem_small = t3['remote_smallholes_holes_fixed'][-1]
lz = fin['measures'][REG_ALL]['layer_Z']                 # the series value; the bottom-fixed second support is reported under its own keys
lz2 = bot['measures'][REG_ALL]['layer_Z']
conv_rows = [dict(el_mm=r['el'], nodes=r['nodes'], vm_mpa=r['measures'][REG_CLR]['vm'],
                  layer_Z_hole_rims_mpa=r['measures'][REG_ALL]['layer_Z'],
                  shear_Z_hole_rims_mpa=r['measures'][REG_ALL]['shear_Z'], shear_Z_root_mpa=r['measures']['root and fillet']['shear_Z']) for r in rows]
put('T3', hand_root_stress_mpa=11.0, el_mm=fin['el'], nodes=fin['nodes'], peak_vm_mpa=fin['measures'][REG_CLR]['vm'],
    peak_at_mm=fin['measures'][REG_CLR]['vm_at'], layer_stress_mpa=lz, sf_yield=round(45.0 / fin['measures'][REG_CLR]['vm'], 2),
    sf_layer=round(22.5 / lz, 2), max_disp_mm=round(fin['disp'], 3), reaction_n=abs(fin['reaction'][0]), converged=True,
    convergence_rows=conv_rows, verdict='fail', status='done', judge=J['T3 layers along Z'],
    second_support_bottom_fixed=dict(el_mm=2.2, nodes=bot['nodes'], layer_stress_mpa=lz2, sf_layer=round(22.5 / lz2, 2), max_disp_mm=round(bot['disp'], 3),
                                      peak_vm_mpa=bot['measures'][REG_ALL]['vm']),
    notes=('Governing: tension across layers (layers along Z) at the lower O3.4 hole rims. Hole walls fixed, even force on rings round '
           f'the four O3.4 holes: layer tension {fin["measures"][REG_ALL]["layer_Z"]} MPa (finest) and with the bottom face fixed instead '
           f'{bot["measures"][REG_ALL]["layer_Z"]} MPa at 2.2 mm (higher; given under second_support_bottom_fixed). A rigid remote load on the bore reads '
           f'{rem_bore["measures"][REG_ALL]["layer_Z"]} MPa there (factor 2.3, the trap); rigid on the small-hole walls reads '
           f'{rem_small["measures"][REG_ALL]["layer_Z"]} MPa at the loaded wall (coupling artefact). judge() verdict: {J["T3 layers along Z"]["verdict"]}, '
           f'lowest factor {J["T3 layers along Z"]["lowest_factor"]} at {J["T3 layers along Z"]["lowest_entry"]}. Interlayer shear at the root fillet 7.02 MPa (factor 1.85) also under 2.0.'))

# ---------------- T4 ----------------
sharp, r04 = t4['sharp'], t4['r04']
put('T4', convergence_rows=[dict(el_mm=r['el'], nodes=r['nodes'], corner_vm_sharp_mpa=r['corner']['vm'], corner_sz_mpa=r['corner']['sz_min_on_corner'],
                                 avg_vm_2mm=r['corner']['avg_vm_2.0']) for r in sharp],
    convergence_rows_r04=[dict(el_mm=r['el'], nodes=r['nodes'], corner_vm_mpa=r['corner']['vm'], avg_vm_1mm=r['corner']['avg_vm_1.0'],
                                avg_vm_2mm=r['corner']['avg_vm_2.0']) for r in r04],
    converged=False, reported_stress_mpa=r04[-1]['corner']['vm'], verdict='fail', status='done',
    judge_with_0p4_radius=J['T4 r04 layers along Z'], judge_sharp_mesh=J['T4 sharp layers along Z'])

put('T4', how_judged=('The sharp corner is a singularity (corner von Mises 22.8, 26.0, 30.0 MPa over three sizes, sigma_z -27 to -37 MPa and still falling, '
                      'steps 14 % and 15 %), so I did not report it: I gave the edge the 0.4 mm radius a printed edge has and solved again '
                      '(38.3, 38.4, 40.4 MPa, last step 5.4 %), read the mean over 2 mm (8.6 MPa, steady: the section value), and judged the corner '
                      'against 45 MPa at the 0.4 mm value: factor 1.11, so the part fails; the hole-rim tension across the layers (14.5 MPa, factor 1.55) fails it too.'),
    status='done',
    notes='Same load case, rings and hole walls as T3. See REPORT.md T4 for the table.')

# ---------------- T5 ----------------
fin5 = t5b['rings_holes_fixed'][-1]
JY = J['T5b layers along Y']
vm5 = max(m['vm'] for k, m in fin5['measures'].items() if m and k in (REG_CLR, 'root and fillet', 'base (2.5 mm clear of fixed holes)'))
base5 = fin5['measures']['base (2.5 mm clear of fixed holes)']
put('T5', change=('Upright thickened from 6 to 7.5 mm on the inner (+X) face (outer face, bore, all holes and the footprint unchanged) with R0.4 rounds on the four '
                  'hole mouths on that face, and the part printed on its side, layers stacked along Y.'),
    mass_g=42.045,
    mass_growth_pct=7.15,
    sf_yield=round(45.0 / vm5, 2),
    sf_layer=round(22.5 / max(m['layer_Y'] for k, m in fin5['measures'].items() if m and k in (REG_ALL, 'root and fillet', 'base (2.5 mm clear of fixed holes)')), 2),
    print_orientation='on its side: layers stacked along Y (the L profile in the layer plane, base and upright both standing on the Y = 0 face)',
    verdict='pass', status='done', judge_layers_along_Y=JY, judge_layers_along_Z=J['T5b layers along Z'], judge_layers_along_X=J['T5b layers along X'],
    bore_wall_check='nodes within 0.5 mm of the O22 wall, finest mesh: vm 6.4, layer tension 3.9 (Z) / 3.9 (Y), shear 3.7 (X): all below the hole rims; see bore_wall.json',
    notes=(f'judge() for layers along Y: {JY["verdict"]}, lowest factor {JY["lowest_factor"]} at {JY["lowest_entry"]}; '
           f'layers along Z: {J["T5b layers along Z"]["verdict"]}, lowest {J["T5b layers along Z"]["lowest_factor"]}; layers along X: {J["T5b layers along X"]["verdict"]}, '
           f'lowest {J["T5b layers along X"]["lowest_factor"]}. Shear between layers (Y) 5.00 MPa, factor 2.60. Study sizes 3.0, 2.2, 1.6; nodes 27,152 / 57,571 / 133,238.'))

# ---------------- T6 ----------------
t6 = json.load(open(RUN / 't6_rows.json'))
p2 = json.load(open(RUN / 't6_post2.json'))
E1, E2, E3 = (t6[k][-1] for k in ('E centred, contact set, ctrl1.2', 'E centred ctrl0.8', 'E centred ctrl0.6'))
EP = t6['E centred proof 0.001 ctrl0.8'][-1]
q1, q2, q3 = (p2[k] for k in ('T6_E_centred,_contact_set,_ctrl1.2', 'T6_E_centred_ctrl0.8', 'T6_E_centred_ctrl0.6'))
qp = p2['T6_E_centred_proof_0.001_ctrl0.8']
put('T6', hand_bearing_mpa=6.76, nodes=E3['nodes'], solver='Intel Direct Sparse (SOLVER_DIRECT; the benchmark log says SOLVER TYPE ACTUALLY USED = Intel Direct Sparse Solver)',
    how_pin_was_stabilised=('Two soft end pads (O3 x 2 mm discs, E 0.5 MPa) on the pin end faces with their outer faces fixed, clear of the block; pin centred (not pre-seated), built in three bonded '
                            'pieces (two stubs, one centre) so the stubs carry the 250 N loads as rigid-coupled faces and only the centre face is in the no-penetration set. '
                            'The pads carried 0.138 N of 500 (0.028 %).'),
    peak_contact_vm_mpa=q3['block_vm_raw_max']['mpa'], block_peak_at_mm=q3['block_vm_raw_max']['at'],
    peak_bearing_mpa=q3['smoothed_1.0mm']['peak_mpa'], peak_bearing_mpa_2mm_smoothed=q3['smoothed_2.0mm']['peak_mpa'], peak_bearing_mpa_raw_node=q3['raw_peak_mpa'],
    bearing_peak_at_mm=q3['smoothed_1.0mm']['at'],
    peak_contact_vm_smoothed_1mm_mpa=q3['block_vm_smoothed_1mm']['mpa'],
    pin_rise_mm=round(q3['pin_centre_mean_uz_mm'], 4), reaction_n=abs(E3['reaction'][2]), valid=True,
    why=('Reaction 500.00 N for 500 N applied (block bottom 499.86, pads 0.138 N = 0.028 %). Contact proof, a thousandth of the load in the working direction: the pin rises 0.1000 mm = the clearance, then bears (a bond would give ~1e-7 mm). '
         'Block and pin nodes were separated by geometry and checked by node-id runs (the first radius-band version put pin nodes in the block band on the seated model and showed 30 MPa; corrected, the block von Mises is 5.2 MPa). '
         'Three meshes (41,136 / 86,564 / 149,971 nodes): peak pressure 6.36, 5.99, 5.79 MPa (1 mm smoothed; last step 3.3 %, under 5 %), pin rise 0.1292, 0.1291, 0.1292 mm, half-width 2.05, 1.98, 2.08 mm. '
         'Hertz hand 6.76 MPa against raw 6.27 (7 % lower) and smoothed 5.79 (14 % lower): the patch is wider than Hertz (conformal contact). The same case with the pin seated 0.1 mm high gives 5.48 at 0.6 mm and the same pin rise.'),
    status='done',
    notes=(f'Centred model, contact-face size 1.2/0.8/0.6 mm: nodes {E1["nodes"]}/{E2["nodes"]}/{E3["nodes"]}; smoothed peak bearing (1 mm) {q1["smoothed_1.0mm"]["peak_mpa"]}/{q2["smoothed_1.0mm"]["peak_mpa"]}/{q3["smoothed_1.0mm"]["peak_mpa"]} MPa. '
           'Cross-check: pin seated at the crown (t6.py). Run 1 (no contact set by my mistake) is kept as t6_v1_* and is invalid.'))

# merge T5b into T5 and drop it
res = json.loads((RUN / 'results.json').read_text(encoding='utf-8'))
res.pop('T5b', None)
(RUN / 'results.json').write_text(json.dumps(res, indent=2), encoding='utf-8')
