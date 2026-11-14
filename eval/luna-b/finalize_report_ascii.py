import json
from pathlib import Path

run = Path(__file__).parent
report_path = run / "REPORT.md"
report = report_path.read_text(encoding="utf-8")
start = report.index("## B4 ")
end = report.index("## End record", start)
sections = """## B4 - Tongue in slot

- Time: 2026-11-13 21:24:51-21:59:24 UTC; 34 min 33 sec of the 40-minute cap. Stopped after the last completed series failed the support-share and wall-force validity checks; no solve was interrupted.
- Geometry: block 14,032 mm^3 and tongue 5,084 mm^3; the block slot is open at the top and through Y, and the tongue has the specified 0.1 mm side and floor clearances. Load relief preserves the 200 mm^2 tongue face at X=-3.9. The review model is two PETG bodies; a separate six-body study model adds four analysis-only pads. The sheet opened successfully; it shows the centered tongue standing in the open slot, with the block and tongue as separate solids.
- Hand statics estimated the left/lower and right/upper slot-wall resultants as 101.18 N and 181.18 N respectively (80 N net in +X, with the stated load height and assumed contact locations). These are checks, not validated results.
- Contact setup: two no-penetration wall pairs, direct sparse solver. The clearance proof used the required +X direction at 0.001 N. With the final vertical flexure pads, the tongue lower-left mean UX was -0.0997 mm, showing the gap opens on the unloaded side; proof pad reaction was 0.00124 N. All solves were under 200,000 nodes.
- Final full-load series at global element sizes 4.0 / 3.5 / 3.0 mm had 12,919 / 14,356 / 17,187 nodes. Reactions were 80.0 N and block peak von Mises values were 1.483 / 1.435 / 1.463 MPa at the slot-floor corner region. Tip UX was 0.482 / 0.534 / 0.520 mm. These are provisional because the stabilizers carry 109.22 N (136.5% of the applied load) on the fine mesh, far above the allowed 0.8 N, so the support affects the load path.
- The attempted cross-section integration sampled Txz on Delaunay-triangulated tongue slices at Z=20.5, 19.5 and 8.5 mm. It returned approximately -28.93, -29.02 and -0.66 N at the fine size; differences of these values do not recover either wall resultant or the expected 80 N net. I therefore leave wall_forces_n undetermined and valid false. A correct section-force extraction/contact-traction check and a stabilizer design whose full-load share is below 1% remain unfinished.
- Failed attempts and corrections: the first build expected 8,000 mm^3 for the block extrusion; SolidWorks correctly produced 16,000 mm^3, so the expectation was corrected. Saving the review model over the block made a seven-body study assembly; switched to save_as for the review model. Initial slot-wall selectors had reversed normals and selected zero faces; face diagnostics corrected them. An early result callback treated Mesh.GetNodes as callable and failed after the solve; switched to the helper's late-bound call pattern. The first 1x1x4 mm X pads did not prevent a vertical mechanism: the solver flagged excessive displacement and a diagnostic run showed about 16.1 mm vertical tongue movement. A later four-pad arrangement passed the tiny-load proof, but its contact-force section method did not balance. The final 0.5x1.5x4 mm vertical flexure pads passed the gap proof, yet attracted 109.2 N under full load. A NumPy 2 change also rejected 2-D np.cross; replaced it with the scalar determinant formula for triangle area.
- Decision: NOT SHOWN. The reaction and node checks pass, but pad load share and wall resultants do not. Do not interpret the provisional peak stress or tip displacement as a validated contact solution.
- Playbook/helper gap: the contact guidance says to keep pads away from judged faces and bound their share from pad stress times area; it does not give a worked section/traction extraction method for wall-resultant recovery in a clearance tongue. swfea.static() reports aggregate fixture reactions, so this run needed custom pad-reaction and section post-processing. The custom Delaunay slice integration did not prove force balance and is not accepted as a result.

## B5 - Review of the motor-plate report

14 distinct problems. The report does not support print approval; redo the analysis and export checks before reconsidering it.

1. The stated von Mises factor is 1.1, below the required 2.0, and was ignored. A hole-edge location is not grounds to waive a failing result; resolve the physical hole/support detail and report an appropriate converged design stress.
2. The hand section calculation uses the wrong bending depth and neutral-axis distance. For a 40 mm wide, 4 mm thick section bending through its thickness, I = 40*4^3/12 = 213.33 mm^4 and c=2 mm, not I=21,333 mm^4 and c=20 mm. With M=120*30=3,600 N*mm, nominal stress is 33.75 MPa, about 10 times the reported 3.4 MPa. The inertia error is 100x, partly masked by the 10x error in c.
3. The reactions do not balance. 96 N against 120 N leaves 24 N (20%) unexplained; this is not close enough. Resolve load direction, selected load faces, restraints and solver equilibrium before using stresses.
4. The reported limit is not a converged peak. 37.6 to 41.0 MPa changes about 9%, above the 5% convergence criterion. The claim of convergence is false.
5. The peak is at a mounting-hole edge and rises with refinement. This is consistent with a fixture/edge singularity. Add the real radius and screw/wall load transfer or define a justified physical stress measure and demonstrate a plateau; do not use the rising peak as a material stress.
6. Both meshes exceed the 200,000-node solve cap (212,000 and 520,000). The 520,000-node run was also run beside the forearm solve, contrary to the one-heavy-solve-at-a-time rule. Replan a predicted mesh series under the cap and run heavy studies sequentially.
7. sigma_x is not established as across-layer tension. With layers along Z, across-layer normal stress is sigma_z; determine stress components in the model frame and compare against the 22.5 MPa across-layer allowable, not an assumed sigma_x against the 45 MPa in-plane yield value.
8. Interlayer shear is missing. Report the relevant Z-containing shear components and compare the governing magnitude with the 13 MPa shear allowable.
9. The fixed hole-wall support is unvalidated. It makes the same hole edge the peak location. Model screw engagement and wall contact or justify the idealization with support-sensitivity checks.
10. The 0.9 mm displacement is not judged. Compare it with a hand estimate and a functional limit, and confirm it comes from the validated support/load model.
11. The STL volume comparison is dimensionally invalid. 1.02 has no stated unit or conversion and cannot be compared with 16,700 mm^3 or dismissed as rounding. Re-export and measure in consistent units.
12. Export integrity is unverified. Written does not establish watertightness, a single shell, correct bounds, or preservation of the model coordinate frame. Check each and compare the STL with the source solid.
13. The report lacks evidence that the analyzed geometry matches the intended plate. Verify model dimensions, hole locations, motor/load face, support faces and selected mesh/load regions against the actual part before accepting any numerical result.
14. The pass, ready to print verdict is unsupported. Replace it with a hold/no-pass until equilibrium, mesh validity, directional PETG criteria, displacement and export checks are redone and documented.

"""
report = report[:start] + sections + report[end:]
end_start = report.index("Benchmark end:", report.index("## End record"))
report = report[:end_start] + (
    "Benchmark end: 2026-11-13 22:05:28 UTC (clock). After releasing sw-eval-luna-b, claims.py list showed no claim for this run. "
    "The final sw_instance.py --status showed no PID launched by this run (latest owned PID 134956 had closed); "
    "only PIDs 20496, 108796 and 134436 remained, belonging to other sessions and left untouched. "
    "B4 remains NOT SHOWN; B5 review is complete.\n"
)
report_path.write_text(report, encoding="utf-8")

results_path = run / "results.json"
data = json.loads(results_path.read_text(encoding="utf-8"))
b4 = data["B4"]
b4["wall_forces_n"] = [None, None]
b4["valid"] = False
b4["status"] = "not shown"
b4["notes"] = "Gap proof and full-load solves completed under the node cap, but pad share is 136.5% of load and the section-force estimate fails balance; wall forces are undetermined. See REPORT.md."
b4["why"].update({
    "full_load_pad_share_n": 109.21896201062424,
    "full_load_pad_share_pct": 136.52370251328028,
    "pad_share_limit_n": 0.8,
    "section_balance_verified": False,
    "wall_forces_determined": False,
    "unfinished": ["redesign stabilization pads to carry under 1% at full load", "recover both wall resultants with a force-balanced section or contact-traction method"]
})
data["B5"] = {
    "problems_found": 14,
    "status": "complete",
    "notes": "Fourteen distinct issues are listed in REPORT.md, ordered by severity; approval should be withheld pending reanalysis and export validation."
}
results_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
(run / "b4_result.json").write_text(json.dumps(b4, indent=2), encoding="utf-8")
