# SolidWorks playbook benchmark — luna-b

## Run record

- Machine: Windows, SolidWorks 2026; worktree `J:\code\roark-wt\sw-eval-luna-b`.
- Benchmark start: 2026-11-13 20:06:38 UTC (clock tool); tasks start in order below.
- Model ID: GPT-6-based Codex; exact runtime model ID and reasoning-effort setting are not exposed to this session. This is recorded as unavailable rather than guessed.
- SolidWorks ownership: `sw-eval-luna-b` claim; every CAD job uses `swkit.job(wait_s=1800)` and its own PID.
- Existing workspace state: `git status --short` already showed deletions elsewhere under the playbook evaluation tree before run files were created. These were not read, restored, or otherwise changed.

## Decisions and playbook/helper issues

- B1 keyway interpretation: 3 mm width is along Y, centered on +X, with the flat floor at X=6.4 mm; it opens into the Ø10 bore.
- B1 set-screw interpretation: a Ø4 mm radial hole along +Y, axis at X=0, Z=22.6 mm, from the bore wall through the boss outer wall.
- B1 specification collision: the Ø5.5 dowel holes at radius 15 mm overlap the Ø26 boss footprint (radius 13 mm) by 0.75 mm. I preserve the stated flange-only depth and call out the partially obstructed top openings.
- No other playbook/helper issue confirmed yet; task-specific results and any failed attempts are recorded below as work proceeds.

## B1 — Hub

- Time: 2026-11-13 20:10:14–20:22:32 UTC (clock); elapsed 12 min 18 sec, including the separate reopen-and-measure pass.
- Failed run before it worked: `b1_hub.py` first stopped on `ModuleNotFoundError: swkit`; the script computed the worktree root one parent too high. Corrected `Path.parents[5]`; no SolidWorks instance launched on the failed attempt. The full model/export run and the separate dimension-check job then succeeded (PIDs 76028 and 134740, both closed by `job()`).
- Hand volume: 21,865.5096 mm³. SolidWorks: 21,865.5355 mm³ (difference 0.0260 mm³, 0.00012%). The analytic radial set-screw cut predicted 101.3293 mm³; SolidWorks removed 101.3034 mm³ (0.026 mm³ difference, within the helper's 1% check).
- Mass at PETG density 1.19 g/cm³: 26.0200 g. One solid body. Finished bbox: [-30, -30, 0, 30, 30, 25] mm.
- Finished-solid checks: flange cylinder R30, Z0–5; boss cylinder R13, Z5–25; bore R5; flange top Z5 and boss top Z25; six R2.25 holes centered at radius22 and every60° from +X; two R2.75 holes at (0,±15); set-screw R2 axis X0/Z22.6 with wall spanning from bore to boss exterior; keyway floor X6.4, width3 and length25. No rebuild errors; one body.
- Exports: STEP `.MILLI.` unit line found. STL watertight, one shell, 21,811.007 mm³ (0.25% below SolidWorks, within0.5%), model-frame bounds 60 × 59.98 × 25 mm (facet chord tolerance). See `b1_result.json` and `b1_dimensional_checks.json`.
- Picture: the eight-view sheet shows the flange, six bolt holes, paired dowel holes, keyed bore and radial set-screw opening. The dowel-hole openings meet the boss underside as expected from their overlapping pitch circle.
- Playbook/helper issues: none confirmed in B1. SolidWorks' set-screw volume differs from the analytic value by 0.026 mm³; this is retained in the run record, not hidden.

## B2 — Wall bracket

Time: 2026-11-13 20:22:32–20:41:56 UTC; elapsed 19 min 24 sec.

- Failed runs before the final result:
  - Initial model/study script PID125860 completed the geometry checks, then stopped before export or solve on a typo, `expect_faces` instead of `expected_faces`. Corrected and reran; its job block closed the instance.
  - First `sheet.py` call used `cad/_wip/sw-eval-luna-b/...` instead of the specified `cad/_wip/sw-eval/luna-b/...`; it produced no PNG. Corrected path, opened the resulting PNG, and repeated the sheet after final model regeneration.
  - The first full-wall-support mesh series ran, but did not converge all three measures in any orientation. That is an inconclusive support sensitivity result, not a solver error.
  - Print-radius experiment: initial selector found zero side arcs; after edge inspection, an overly broad selector found six edges (including two straight plate edges). The corrected selector rounded four curved edges R0.4 successfully, but it changed the subsequent shallow-step volume: 43.0319 mm³ instead of 45.0. Moving the step start to X11 and X15 still produced 42.0757 vs 44.0 and 38.2506 vs 40.0 mm³. I discarded that variant and restored the specified R3-only geometry to preserve the exact 100 mm² load patch. None of these variants was solved.
- Specification conflict: the upper Ø4.5 hole at Y20,Z48 lies within the arm footprint Y15–25,Z40–52 at X5. I cut both holes through the plate thickness X0–5 only; the upper hole exit is covered by the arm. A real screw path/engagement is not established by this model.
- The partial-face load was represented by a 0.1 mm shallow step over X10–55, leaving a dedicated 10 × 10 mm² planar patch at X55–65,Z52. The changed upstream top is 0.1 mm deep. The final patch was measured at 100 mm².
- Model: `cad/_wip/sw-eval/luna-b/wall_bracket.SLDPRT`, SHA-256 `4082E480916EC8A04FE1AD52ED88AD94FA0CF0342D4B6CA524DAAEF1BF630F72`. One body; bounding box [0,0,0,65,40,60] mm. Hand volume 19,034.5852 mm³; SolidWorks measured 19,034.5852 mm³. R3 fillets add 38.63 mm³; the 45 mm³ load step and two Ø4.5 holes remove 45.00 and 159.04 mm³. STL is watertight, one shell, 410 triangles, 19,036.1071 mm³ (0.0080% from SolidWorks), same model-frame bounds. See `b2_stl_checks.json`.
- Hand calculation: resultant 60 N at x=60 mm, root at x=5 mm, so M=3,300 N·mm. For the 10 × 12 mm section, I=1,440 mm⁴ and nominal root stress is 13.75 MPa. The distributed-load tip deflection estimate including shear is 1.430 mm.
- Primary study: fixed cylindrical walls of both screw holes; 60 N downward normal load over the measured X55–65 top patch; automatic solver; global sizes 4.0, 3.5, 3.0 mm with 1.0 mm controls on the two hole walls and the load patch. Predictions were 3,569 / 5,327 / 8,460 nodes, peak near the root fillet, displacement about 1.43 mm. Actual node counts were 11,217 / 13,101 / 15,362, all below 200,000. Fixture-node box X0–5,Y17.75–22.25,Z9.75–50.25; load-node box X55–65,Y15–25,Z52: both where intended.
- Primary checks at the finest mesh, layers stacked along Z:
  - Reaction 60.0 N vs 60 N applied (0% difference).
  - Maximum displacement 1.895 mm vs 1.430 mm hand estimate (1.33×, same order).
  - Plain section mean von Mises 6.332 MPa at x≈35 mm vs 6.37 MPa hand bending stress (0.6% difference).
  - Peak away from fixture/load by the common 8 mm exclusion: 12.935 MPa at [9.35,25,40] mm. A root ROI using a 2 mm exclusion read 15.464 MPa at [8,22.5,52] mm. The raw maximum was 30.982 MPa at [0,19.49,45.81] mm on the fixed upper-hole wall, the expected fixture singularity.
  - Z-direction mesh series (von Mises / across-layer tension / interlayer shear, MPa): 4.0 mm, 12.871 / 5.613 / 5.044; 3.5 mm, 12.800 / 5.917 / 5.014; 3.0 mm, 12.935 / 6.012 / 4.978. Last-step changes are 1.0%, 1.6%, and 0.7%, so all three converge.
- Print direction comparison from the same finest result:

  | Layers stacked along | von Mises (MPa), FoS | Across-layer tension (MPa), FoS | Interlayer shear (MPa), FoS | All measures converged |
  | --- | ---: | ---: | ---: | --- |
  | X | 12.935, 3.48 | 12.237, 1.84 | 4.747, 2.74 | Yes; fails the layer-tension factor |
  | Y | 12.935, 3.48 | 3.462, 6.50 | 2.087, 6.23 | No; shear changed 8.0% in the last step |
  | Z | 12.935, 3.48 | 6.012, 3.74 | 4.978, 2.61 | Yes |

- Selected orientation for a numeric check: layers stacked along Z. Its primary-support case satisfies all three factor-of-safety thresholds. The thinnest primary margin is 2.61 on shear; a 20% load increase scales it to about 2.18. Printing with layers along Z rather than X raises the layer-tension factor from 1.84 to 3.74 without changing mass. Load path: the tip patch bends the arm, the R3 root transfers moment into the wall plate, and the two hole supports carry the reaction.
- Support check: the second idealization fixed the entire X0 wall face at global sizes 4.0/3.5/3.0 mm (predicted 3,569/5,327/8,460; actual 8,802/10,438/13,139 nodes). Its Z series was 17.306/1.247/2.443, 16.652/1.869/2.404, 16.287/1.906/2.830 MPa (von Mises/layer tension/shear); none of X/Y/Z converged all three measures. The shear peak moved to the sharp root-fillet side junction around [8,15,40] mm. The last Z shear step rose 17.8%. This whole-face restraint is more restrictive than the specified screw support and its peak is not a settled stress. The 0.4 mm edge-round experiment did not preserve the separate load-step volume; I did not substitute it into the benchmark.
- Verdict: **not shown** overall. The required factors are met and converge for the specified hole-wall support when printed with layers stacked along Z; however, the second support idealization remains unconverged, and the upper screw hole is obstructed by the arm. A real wall contact/screw engagement check and a corrected upper screw path are still needed before print approval.
- Not checked: screw preload, wall friction/contact, or nonlinear material response. The cheapest demonstrated improvement is the Z print orientation; no mass or geometry change is needed.

## B3 — Lighter bracket

- Time: 2026-11-13 20:41:56–21:22:52 UTC; elapsed 40 min 56 sec of the 45-minute cap.
- Best saved model: `cad/_wip/sw-eval/luna-b/wall_bracket_light.SLDPRT`; its source script is `b3_edge_round.py`, and its sheet is `pictures/b3_wall_bracket_light_final.png`. The face at X55–65,Z52 was measured at exactly 100 mm²; screw-hole centers and the X0 wall face were checked; one body.
- B2 mass is 22.6512 g. First reduction: trim the plate around the holes and reduce it to 3 mm while retaining the 12 mm arm; mass 11.1654 g, a 50.71% reduction. At 8 mm exclusion, Z FoS was 3.523 / 1.997 / 2.651 (yield / across-layer tension / interlayer shear); the layer-tension requirement narrowly failed. Y had high numerical FoS but its shear had not converged.
- Radius attempt: selected and rounded four curved root-side transitions R0.4. The rounds narrowed the arm's top to 9.2 mm, so I widened the arm to 10.8 mm to restore the fixed 10 mm bearing width. The final patch is exactly 100 mm². The measured shallow-step cut was 5.1813 mm³, not the nominal 5.0 mm³; the actual cut delta is recorded in the model script and result checks.
- Final model mass 11.8668 g, saving 47.61%. With layers along Z, the 8 mm-excluded values are VM 12.741 MPa (FoS 3.532), across-layer tension 11.020 MPa (FoS 2.042), and shear 4.908 MPa (FoS 2.649). Reaction 60.003 N; max displacement 2.671 mm versus 1.465 mm hand estimate. X fails layer tension (FoS 1.894). Y gives FoS 3.532 / 7.603 / 6.144 but is not converged. Z stress changes across 4.0 / 3.5 / 3.0 mm are under 0.5% on the last step, yet the node counts were 84,283 / 84,485 / 84,987 versus predictions 1,870 / 2,791 / 4,432. The mesh barely changed because local controls dominated. `swfea.converge` checks stress deltas but does not reject a series with nearly unchanged node counts; per page 07, the node prediction mismatch should have stopped stress interpretation. **Verdict: not shown**, despite numerical factors above 2 in Z.
- Export: watertight, one shell, 1,424 triangles; STL volume differs by 0.0084%. STL bounds end at Z54.750 while `bbox(d)` reports Z54.871, a 0.121 mm mismatch against the 0.1 mm limit. A plate-top extension attempt moved the BREP maximum to Z55.044 and did not provide a better export match; it was not selected. See `b3_stl_checks.json`.
- Failed attempts before this candidate: the x=10 shallow step created a load-adjacent stress peak and did not converge; moved it to x=50. Three edge-round builds stopped before solving: a syntax error; then selectors that found zero edges because their coordinate windows did not match the actual arc samples; then a broad selector found six edges including two long non-target edges. After inspecting edge coordinates, the selector chose the four intended arcs. The first rounded build failed its load-step volume check (4.7813 vs 5.0 mm³); widening the arm restored the face, and the step delta was measured and recorded. No SolidWorks process was stopped during meshing or solving.
- Decision: retain the lightest candidate that preserves the fixed face, with Z as the provisional print orientation. Its nominal limiting factor is across-layer tension at 2.042; a 20% load increase would reduce that to about 1.70. Do not treat it as print-approved until the mesh prediction/refinement and STL bounding discrepancy are resolved. The export check is not a full pass.

## B4 - Tongue in slot

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

## End record

Benchmark end: 2026-11-13 22:05:28 UTC (clock). After releasing sw-eval-luna-b, claims.py list showed no claim for this run. The final sw_instance.py --status showed no PID launched by this run (latest owned PID 134956 had closed); only PIDs 20496, 108796 and 134436 remained, belonging to other sessions and left untouched. B4 remains NOT SHOWN; B5 review is complete.
