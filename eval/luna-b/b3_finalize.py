import json
from pathlib import Path
RUN = Path(__file__).resolve().parent
main = json.loads((RUN / 'results.json').read_text(encoding='utf-8'))
result = json.loads((RUN / 'b3_t3p0_h12p0_r0p4.json').read_text(encoding='utf-8'))
checks = {
    'watertight': True, 'shells': 1, 'stl_volume_mm3': 9972.904180112906,
    'solidworks_volume_mm3': 9972.068470128394, 'volume_error_pct': 0.008380507885760082,
    'bounds_mm': [0.0, 13.25, 5.25, 65.0, 26.75, 54.75],
    'solidworks_bounds_mm': [0.0, 13.25, 5.25, 65.0, 26.75, 54.871],
    'max_bbox_delta_mm': 0.12100000000000222, 'bbox_tolerance_mm': 0.1,
    'triangles': 1424, 'export_check_valid': False,
}
(RUN / 'b3_stl_checks.json').write_text(json.dumps(checks, indent=2), encoding='utf-8')
before = 22.651156388000004
after = result['mass_g']
first = json.loads((RUN / 'b3_t3p0_h12p0.json').read_text(encoding='utf-8'))['orientation_table']['Z']
final = result['orientation_table']['Z']
b3 = {
    'mass_before_g': before, 'mass_after_g': after, 'saving_pct': 100 * (before-after) / before,
    'steps': [
        {'change': 'Thin the wall plate to 3 mm and trim its Y/Z envelope around the two screw holes; retain 12 mm arm height.',
         'mass_g': 11.16536160000179, 'sf_yield': first['sf_yield'], 'sf_layer': first['sf_layer'],
         'sf_shear': first['sf_shear'], 'print_orientation': 'layers stacked along Z',
         'mesh_converged': first['converged_all_three']},
        {'change': 'Round the four curved root-side transitions R0.4 and widen the arm to 10.8 mm so the top bearing face remains exactly 10 x 10 mm.',
         'mass_g': after, 'sf_yield': final['sf_yield'], 'sf_layer': final['sf_layer'],
         'sf_shear': final['sf_shear'], 'print_orientation': 'layers stacked along Z',
         'mesh_converged_by_stress_only': final['converged_all_three']},
    ],
    'governing': 'Not shown. Numerically, Z-direction across-layer tension is thinnest (FoS 2.042), but the mesh node counts exceeded the playbook pre-solve estimates by 19–45x and changed by less than 1% across nominal sizes.',
    'sf_yield': result['sf_yield'], 'sf_layer': result['sf_layer'], 'sf_shear': result['sf_shear'],
    'print_orientation': result['print_orientation'], 'status': 'complete',
    'notes': 'The force reaction is 60.003 N and the requested 100 mm2 load face was measured. Treat the stresses as provisional: local controls dominated node count, and the STL/solid bounding boxes differ by 0.121 mm (0.1 mm allowed). See REPORT.md and b3_stl_checks.json.',
}
main['B3'] = b3
(RUN / 'b3_result.json').write_text(json.dumps(b3, indent=2), encoding='utf-8')
(RUN / 'results.json').write_text(json.dumps(main, indent=2), encoding='utf-8')
report_path = RUN / 'REPORT.md'
report = report_path.read_text(encoding='utf-8')
report = report.replace('## B3 — Lighter bracket\n\nNot yet run.', '''## B3 — Lighter bracket

- Time: 2026-11-13 20:41:56–21:22:52 UTC; elapsed 40 min 56 sec of the 45-minute cap.
- Best saved model: `cad/_wip/sw-eval/luna-b/wall_bracket_light.SLDPRT`; its source script is `b3_edge_round.py`, and its sheet is `pictures/b3_wall_bracket_light_final.png`. The face at X55–65,Z52 was measured at exactly 100 mm²; screw-hole centers and the X0 wall face were checked; one body.
- B2 mass is 22.6512 g. First reduction: trim the plate around the holes and reduce it to 3 mm while retaining the 12 mm arm; mass 11.1654 g, a 50.71% reduction. At 8 mm exclusion, Z FoS was 3.523 / 1.997 / 2.651 (yield / across-layer tension / interlayer shear); the layer-tension requirement narrowly failed. Y had high numerical FoS but its shear had not converged.
- Radius attempt: selected and rounded four curved root-side transitions R0.4. The rounds narrowed the arm's top to 9.2 mm, so I widened the arm to 10.8 mm to restore the fixed 10 mm bearing width. The final patch is exactly 100 mm². The measured shallow-step cut was 5.1813 mm³, not the nominal 5.0 mm³; the actual cut delta is recorded in the model script and result checks.
- Final model mass 11.8668 g, saving 47.61%. With layers along Z, the 8 mm-excluded values are VM 12.741 MPa (FoS 3.532), across-layer tension 11.020 MPa (FoS 2.042), and shear 4.908 MPa (FoS 2.649). Reaction 60.003 N; max displacement 2.671 mm versus 1.465 mm hand estimate. X fails layer tension (FoS 1.894). Y gives FoS 3.532 / 7.603 / 6.144 but is not converged. Z stress changes across 4.0 / 3.5 / 3.0 mm are under 0.5% on the last step, yet the node counts were 84,283 / 84,485 / 84,987 versus predictions 1,870 / 2,791 / 4,432. The mesh barely changed because local controls dominated. `swfea.converge` checks stress deltas but does not reject a series with nearly unchanged node counts; per page 07, the node prediction mismatch should have stopped stress interpretation. **Verdict: not shown**, despite numerical factors above 2 in Z.
- Export: watertight, one shell, 1,424 triangles; STL volume differs by 0.0084%. STL bounds end at Z54.750 while `bbox(d)` reports Z54.871, a 0.121 mm mismatch against the 0.1 mm limit. A plate-top extension attempt moved the BREP maximum to Z55.044 and did not provide a better export match; it was not selected. See `b3_stl_checks.json`.
- Failed attempts before this candidate: the x=10 shallow step created a load-adjacent stress peak and did not converge; moved it to x=50. Three edge-round builds stopped before solving: a syntax error; then selectors that found zero edges because their coordinate windows did not match the actual arc samples; then a broad selector found six edges including two long non-target edges. After inspecting edge coordinates, the selector chose the four intended arcs. The first rounded build failed its load-step volume check (4.7813 vs 5.0 mm³); widening the arm restored the face, and the step delta was measured and recorded. No SolidWorks process was stopped during meshing or solving.
- Decision: retain the lightest candidate that preserves the fixed face, with Z as the provisional print orientation. Its nominal limiting factor is across-layer tension at 2.042; a 20% load increase would reduce that to about 1.70. Do not treat it as print-approved until the mesh prediction/refinement and STL bounding discrepancy are resolved. The export check is not a full pass.''')
report_path.write_text(report, encoding='utf-8')
print(json.dumps({'B3': b3, 'stl_checks': checks}, indent=2))
