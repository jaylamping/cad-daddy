# SolidWorks benchmark terra-high-b

Machine: Windows, SolidWorks 2026; local times 2026-11-13, America/Chicago (UTC-06). Model identity: GPT-6 Codex; exact model ID and reasoning effort were not exposed to this session. No commit or push.

This is an incomplete benchmark. A report of “not shown” means the required evidence is missing, not that the part passed. Scripts and logs in this folder are the record; CAD is in `cad/_wip/sw-eval/terra-high-b/`.

## B1 — hub

Start 17:28: approximately 17:28:10 for the first failed script; successful job 17:28:27–17:28:50, plus export inspection through 17:29. The initial run failed before launch because the script used `parents[4]` instead of `parents[5]` for the worktree root; corrected in the saved script. No SolidWorks modeling attempt failed.

The native part has one body, volume 21,865.536 mm³, bounding box (-30,-30,0) to (30,30,25) mm, and zero feature errors. Hand volume 21,865.510 mm³: flange plus boss minus bore, the eight bolt/dowel holes, 110.7035 mm³ keyway outside the bore, and approximately 101.3293 mm³ radial hole outside the bore. The latter integral assumes no interaction with the keyway, which is on the opposite side; its tiny remaining discrepancy (~0.026 mm³) is negligible at this precision. PETG mass at 1.19 g/cm³ is 26.020 g.

Measured cylindrical faces: one R5 bore, six R2.25 bolt holes with centers at the requested hexagon, two R2.75 dowel holes centered on Y ±15, and one R2 radial hole extending from the bore to the boss outside at Z 20.6–24.6. Box and volume are measured, but not every planar face and keyway dimension was independently measured on the finished solid, so the full dimensional gate remains incomplete.

The STL is watertight, one shell, 21,811.007 mm³ (0.249% below native), bounds within 0.01 mm of native. STEP declares millimetres. Image `hub.png`: flange, boss, bore with keyway, six bolt holes, two dowel holes and radial hole are visible. Questions: the dowel holes' inner edges are at radius 12.25 mm while the boss radius is 13 mm, so 0.75 mm of each hole footprint lies under the boss at Z=5; a straight dowel cannot enter freely from that side. The set screw leaves only 0.4 mm from its top to the boss top (25 − 22.6 − 2), below the playbook's 0.6 mm wall guideline. The set-screw hole is unthreaded because no thread was specified.

## B2 — wall bracket

Start 17:29:48; modeling and three initial solves ended 17:30:21. Native `wall_bracket.SLDPRT` has one body, 19,079.585 mm³, box (0,0,0)–(65,40,60), no feature errors; 3 mm rounds on both requested root edges. `wall_bracket.png` shows the plate, arm, rounds and holes. The upper hole opens into the arm at X=5, so a screw inserted from the arm side lacks a clear straight path; investigate assembly access.

Hand estimate: load center X=60, cantilever arm length from root 55 mm, I=10×12³/12=1440 mm⁴, root bending stress 60×55×6/1440=13.75 MPa, ideal beam displacement 60×55³/(3×1900×1440)=1.216 mm before shear and wall flexibility. The script incorrectly logged 0.423 mm, and automatically read stresses although the first 1.887 mm displacement exceeded three times that mistaken prediction; that breached 07's stop-and-investigate gate. The corrected calculation is recorded here, but does not retroactively validate the run.

The study twin has a 0.05 mm shallow step along the arm top to isolate the requested 55–65 mm load patch; it removes 25 mm³ (0.131%, exceeding the playbook's 0.1% twin-volume tolerance). Fixed the two hole walls, pressed 60 N downward on the top patch. Automatic solver. Coarse to fine global sizes 4.0, 3.0, 2.4 mm gave 6,674 / 11,241 / 20,572 nodes; reaction each approximately (0,0,+60) N; displacement 1.887 / 1.896 / 1.901 mm. Fixture and load node boxes were logged and consistent with selections. Away-from-fixture/load peaks were 13.66 / 15.25 / 15.72 MPa, finest at (8,16.25,40); unrestricted finest peak 28.66 MPa, a fixture-region value. The changing default exclusion distance makes the apparent 3.1% final VM change insufficient as a convergence proof. No section-average comparison, fixed-distance plateau, alternative support, or second load method was completed.

At 2.4 mm the default-mask directional values (tension MPa / shear MPa) are X 13.53 / 6.19, Y 3.77 / 3.42, Z 6.49 / 6.14. For nominal Y-layer normal these imply approximate factors 45/15.72=2.86, 22.5/3.77=5.96, 13/3.42=3.80. They are provisional: they use the default mask, not converged fixed-region values, and ignore the fixture singularity and possible small-hole load path. Verdict: **not shown**, not pass. The load enters the arm top, bends its root and exits through the two constrained hole walls; actual screw and wall bearing remain unproved. A side orientation with layers normal to Y looks promising from this provisional result, but must be verified with the required support and mesh checks. No full print/assembly gate was run.

## B3 — lightened bracket

Start 17:31:10; last solve 17:31:39; stopped candidate work before B4 at approximately 17:32:24, well before the 45-minute maximum. One candidate only: trim the original wall plate to Y 13–27, preserving the hole centers and X=0 mounting plane. Native `wall_bracket_light.SLDPRT` is one body, 11,279.585 mm³, 13.423 g versus 22.705 g originally, saving 40.88%. `wall_bracket_light.png` shows the narrowed wall strip and original arm. The phrase “wall face at X 0” could require the entire original face to remain; this interpretation preserved its plane but reduced its footprint, so the candidate needs that requirement settled before acceptance.

The 4.0/3.0/2.4 mm study meshes had 4,240/7,270/12,297 nodes and reaction +60 N Z, displacement 1.979/1.993/1.995 mm. Finest default-mask VM 14.71 MPa (factor 3.06); Y-normal layer tension 2.54 MPa (factor 8.85) and shear 1.95 MPa (factor 6.66). These are preliminary, not acceptance factors: same 0.05 mm load step (25 mm³), fixed hole-wall support, varying exclusion and missing support, convergence, section and print checks as B2. No established governing requirement and no proof of the maximum saving: further candidates and required checks were not done. The edge distance of each hole to the narrowed side is 7−2.25=4.75 mm, only 0.25 mm over one hole diameter. The next most useful work is compare a washer support, then reduce material incrementally while keeping the load patch and screw access, and check buckling and all three converged failure measures.

## B4 — tongue in slot

Start 17:32:24; stopped at 17:32:26. The preflight check showed 8.4 GB available, but `job()` measured 7.6 GB and refused launch. No owned SolidWorks process or model was created for B4; no mesh or solve was started. Following the playbook's under-8-GB stop rule, this task is unfinished. B4 script is an unexecuted proposal; its pads and groove are analysis approximations and require validation. Nothing from the script is a result. With assumed contacts at the top and bottom of the 12 mm slot depth, simple moments give rough reactions +180 N and −260 N (opposite walls); actual distributed contact locations are unknown, so those are not the answer. Wall forces, block stress, displacement, contact-opening proof, pad force, section-force balance and convergence are all unverified. `valid=false`.

## B5 — review of motor plate report

Start 17:32:33. **Do not approve for printing.** The report has the following problems, in priority order:

1. Reaction is 96 N against 120 N: 20% imbalance, not the required 1%. Check each force component, selected faces, actual applied load, fixtures, and solver results; rerun the case before trusting any number.
2. The raw von Mises factor is 45/41=1.10, below 2.0. A fixed-hole edge can be singular, but it cannot simply be ignored: measure a fixed-distance plateau, report the excluded maximum, compare a realistic washer/head-bearing support, and converge the physical stress.
3. The reported stress increases 9% from 37.6 to 41.0 MPa, so even its own two-mesh comparison fails the 5% criterion. Use at least three controlled meshes with a common exclusion distance, and converge the governing von Mises, interlayer tension and shear measures. A sharp physical corner may need its actual printed radius modeled.
4. With layers stacked along Z, across-layer normal tension comes from σz (and the maximum tensile value), not σx. The across-layer tensile allowable is 22.5 MPa, not 45 MPa. Even if 19.5 MPa were the correct across-layer tension, its factor would be 1.15, not 2.3. Read the correct stress component and its position.
5. Interlayer shear and its 13 MPa allowable were omitted entirely. Report its peak, location, factor and convergence, and compare feasible print orientations.
6. The hand estimate uses I for a 40 mm bending depth, while the narrative calls the plate 4 mm thick. If the load bends it across that thickness, I=40×4³/12=213.3 mm⁴ and c=2 mm, giving 33.75 MPa, not 3.4. The actual axes and load path must be specified first; an in-plane load may require a different section. Check displacement as well against the appropriate beam estimate.
7. A 0.9 mm displacement is given without a hand comparison or location, and the inconsistent force balance prevents treating it as evidence. Check location, units, support and a defensible hand value.
8. Both meshes exceed this benchmark's 200,000-node cap. A 520,000-node run also exceeds the playbook's 450,000 limit; a heavy solve beside another heavy solve is contrary to machine-wide coordination. Replan with local refinement and remain below 200,000, and follow machine memory/solve coordination.
9. An STL volume of 1.02 versus 16,700 mm³ is not rounding if both are mm³; the ratio is about 16,373. Units are not specified for the first number, so check units, scaling, export, watertightness, number of shells and coordinates, then compare within 0.5%. Do not print the unverified export.
10. Fixing whole hole walls distorts local stresses and may not represent screw and wall bearing. Model the real load path and compare a second support; report reaction distribution. Check screw and tool access.
11. The load is described only as 120 N on a motor face: its footprint, direction relative to geometry, moment arm and real bearing surfaces are not specified. If a rigid remote load or nearby small holes are involved, compare a distributed load on the actual bearing faces and inspect stresses inside any default load mask.
12. The report omits the model identity/hash, measured geometry, mesh controls, solver, peak coordinates and exclusions, plain-section stress, applied-force components, boundary-condition details and enough information to reproduce the analysis. Supply these and preserve nodal results.
13. It asserts print readiness without demonstrating material, orientation, printability, fit/assembly, fastener access, wall thickness, export integrity or the pre-print gate. Redo those checks after a valid study; no pass follows from the current evidence.

## Playbook and helper observations

- `swkit.export()` calls `pin_export_prefs()` which changes per-machine/shared settings. That conflicts with this run's explicit prohibition on changing shared settings. Decision: use `save_as` with existing settings, then independently check STL/STEP; the actual STL and STEP checks above pass, but settings were not pinned.
- `swfea` default away-mask is mesh-dependent, so the B2/B3 reported masked values cannot by themselves prove convergence; the playbook discusses a fixed exclusion but the short summary can make this easy to miss.
- The 01-session page says commit and push when finished; the explicit instruction for this run forbids both, so neither was done.
- The initial B1 worktree root mistake and the B2 prediction error were script/operator errors, not helper failures. B4's job refusal correctly enforced the memory floor. No helper code or shared settings were changed.

B5 review and results file completed at 17:34:10. Final status check showed no owned SolidWorks PID; the keeper and other sessions remained running.
