# terra-high-c run report

Start 2026-11-13 17:35:35 CST (23:35:35 UTC). Deadline 19:15:35 CST. Model: GPT-6 (Codex); reasoning effort: not exposed to this session.

## C1 — boxy link
Start 17:35:35; model saved 17:36:44. Picture reviewed 17:37. C1 model: 219436.038 mm³, 261.129 g at 1.19 g/cm³, one body, bbox (-35,-22,-215) to (35,22,35) mm, no feature errors. The sheet shows a round mounting disc, rectangular beam and squared fork; flat share 0.910, largest flat 0.144, sharp length 2406.4 mm, sharp/sqrt(area) 12.3.

## C2 — organic link
Start 17:37. Restatement and stage budgets are in restate.md.

Checkpoint 01, 17:38:35 (~1.6 min after C2 start), pictures/checkpoint_01.png: full 132004.7 mm³ form; missing verified driver/slot/cable clearances, smooth end transitions, all FEA, print and export checks.

Checkpoint 02, 17:44:13, pictures/checkpoint_02.png: widened disc junction, volume 134698.93 mm³; still needs native interface, cable, slot and driver clearance measurements, real bearing studies, reliable factors, printing and exports verified. The two-rail concept (idea_b.png) was dropped for a more continuous silhouette; idea A remains the basis.

Checkpoint 03, 17:50:30, pictures/checkpoint_03.png: 0.4 mm elbow junction radius, 134687.33 mm³; absent are a converged load study, a validated axial pin load, a print support plan, and final export verification. Sampled ring, driver, cable, slot, and cheek checks show no violations; sampling is not an exact geometric proof.

### Geometry and checks
C1 hand volume: 219436.038 mm³, using disc 8π35², beam 40×30×138, less 457.715 mm³ disc/beam overlap, plus bridge 40×44×10 and two cheek extensions 30×35×6, less the mounting holes and pin holes. Native agrees to rounding; mass 261.129 g at 1.19 g/cm³. Its STL is one watertight component, 219351.757 mm³ (0.038% low), bounds [-35,-22,-215] to [35,22,35] mm. Native cylinder and plane measurements are in measure_probe.log. The bridge contains the cheeks from Z=-170 to -180; extensions begin at -180. I did not independently measure every C1 beam face.

Idea A: oval shaft, 132004.699 mm³. Idea B: two separated load-path rails, 83487.968 mm³; dropped because it reads as exposed struts rather than a restrained continuous form. Idea C widens A's elbow transition: 134698.929 mm³ (160.292 g), one native body, no feature errors. Its STL is watertight, one component, 134319.467 mm³ (0.282% low), bounds approximately [-34.885,-23,-213] to [34.885,23,35]. The filleted candidate is 134687.328 mm³ (160.278 g), 100.851 g below C1. STL sampling counts and code are in mesh_checks.json and mesh_checks.py; sampling is not an exact solid-subtraction proof.

Native measurement of the unfilleted revised part: six radius 1.7 mm holes centred at (25,0), (12.5,21.651), (-12.5,21.651), (-25,0), (-12.5,-21.651), (12.5,-21.651) in X,Z, each Y=-4..4; central radius 15 mm bore Y=-4..4. Two radius 4 mm pin faces have X=-4..4, Z=-204..-196, Y=16..23 and -23..-16; inner faces lie at Y=±16. Nominal outside cheek radius 13 mm leaves 9 mm material; 288 interior annulus samples through radius 8.9 mm were solid. Six Ø7 × 10 mm driver cylinders: 1,728 samples clear; wrist slot: 6,825 clear; cable passage: 3,420 clear; ring inside and outside near Y=-4: 558 samples each without a violation. These samples are for the filleted candidate. Fixed-items status remains unproven until the filleted native model and continuous clearances are independently measured.

Print candidate with layer normal Y, on its side, projected X×Z envelope about 70×248 mm on a 256 mm bed, with no allowance for a brim or positioning error. The Y=-23 cheek can touch the plate; support is needed under shaft, elbow disc and opposite overhangs and inside the fork as needed. The cable passage opens at the elbow bore and wrist slot, so it is not enclosed. This orientation has not been sliced or support-removal verified.

### Strength exploration — requirement not shown
PETG model E=1.9 GPa, yield 45 MPa; layer tensile and shear allowables 22.5 and 13 MPa. Load path: pin and cheek → fork roots → shaft → elbow disc and held ring. A first narrow-neck version gave 40,363 nodes (prediction 12,672) and 5.874 mm displacement (uniform-beam prediction 1.37 mm), so the prediction rules were violated; its stresses are INVALID. My scripted loop unfortunately proceeded to two more cases before I reviewed the discrepancy. A section-integral diagnostic on that version predicted 1.914 mm X bending for Z=-179.5 to -35, excluding root, disc and fork compliance; the remaining discrepancy is not fully explained. I widened the root.

For the unfilleted wider version, ±X cylindrical bearing loads used a pin-axis coordinate system and 60 N on both Ø8 walls. A 5 mm global high-quality tetrahedral mesh had 40,047 nodes / 25,714 elements; +X displacement 1.9331 mm and reaction (-59.996,0.001,-0.023) N; -X displacement 1.9330 mm and reaction (60.003,-0.018,0.017) N. Predicted ~40,000 nodes and 2 mm; raw stress peaked at the predicted root.

The +Y force is along the hole axis, so radial bearing pressure on the hole cannot supply it. I chose 60 N normal pressure on the +Y cheek inner face as a thrust proxy; it is not the requested bearing-on-hole representation and assumes a thrust-bearing mating face. That proxy gave 6.281 mm and reaction (0.002,-59.984,0.009) N, 40,047 nodes. A real pin and its thrust transfer need to be specified and analysed.

Unfilleted coarse diagnostics, all nodes including fixture and load boundaries (SF yield / layer tension / interlayer shear):

| Load | Layers X | Layers Y | Layers Z |
|---|---|---|---|
| +X bearing | 3.352 / 2.825 / 3.141 | 3.352 / 3.637 / 3.269 | 3.352 / 1.410 / 3.127 |
| -X bearing | 3.352 / 2.180 / 3.140 | 3.352 / 2.650 / 3.269 | 3.352 / 1.205 / 3.128 |
| +Y thrust proxy | 1.294 / 0.756 / 1.684 | 1.294 / 0.693 / 0.774 | 1.294 / 0.490 / 0.771 |

The +Y proxy raw peak is 34.79 MPa at (-9.77,4,-32) mm, a sharp junction close to the held ring; it may include a fixture/edge singularity. A 10 mm exclusion reduced it to 10.95 MPa at (-11.37,6.06,-36.04), which must not hide a real narrow load path. The most concerning raw result, layer tension with layers Z, is 0.490; even the proposed Y orientation gives 0.693 on this mesh. These do not establish failure or pass under the true axial load: neither load fidelity nor convergence is shown. The required safety factors are NOT SHOWN. Nodal arrays and all locations are in the run folder.

The baseline's 5 mm load-response model is not converged; the support was not tried a second way and the axial load was a proxy. A 0.4 mm round was tried at the junction after 2 and 1 mm did not build, and produced 199,455 nodes at 6 mm, far beyond the 23,175 prediction. Its force reaction was (-60.012,-0.011,-0.002) N and displacement 2.0484 mm. The helper starts the solve before returning its mesh, so the discrepancy could not be acted on between mesh and solve; the node cap was not exceeded. Per the prediction rule, its stress is invalid and was not judged. Finer versions are not automatically safe within the cap.

### Playbook and helper findings
- swkit.job() calls pin_export_prefs() on entry and unconditionally writes five per-machine export preferences; this conflicts with the user's no-shared-settings instruction. The first C1 job ran before I discovered it. I did not capture the prior values, so I cannot safely restore unknown settings. Subsequent jobs suppressed the call and checked outputs. The playbook describes pinning but the job example does not call out this side effect.
- Simulation loading displayed a hidden continue/disable prompt; the hider log identified it, and I clicked continue on our own PID. It cost about one minute.
- swfea.static lacks a bearing option and goes directly from mesh to solve before the caller can check the predicted count. The run-local swfea_bearing.py adds bearing loads; all solves set max_nodes below 200,000. Its first COM attempt passed an array as the coordinate-system argument and failed with type mismatch; a feature object and face list worked. API reference: https://help.solidworks.com/2021/english/api/swsimulationapi/SOLIDWORKS.Interop.cosworks~SOLIDWORKS.Interop.cosworks.ICWLoadsAndRestraintsManager~AddBearingLoad.html
- The mesh-check script initially sampled idea A instead of the revised model due to an incorrect path replacement; I caught and corrected it and reran it for each candidate.
- 07-done asks a three-size convergence series for a pass, while set C asks for one mesh; I chose the stricter pass standard. It asks for a checkpoint commit, but the user explicitly prohibited commits; saved images and report entries serve as checkpoints.

Checkpoint 04, 17:55:34, pictures/checkpoint_04.png: four-edge R0.4 junction attempt, 134700.217 mm³; not fully checked, fork still visibly plate-like and strength unproven. The +Y thrust proxy with 79,873 nodes reacted 59.982 N and displaced 7.193 mm. Its raw peak was 286.9 MPa at (12.50,-3.94,-32.69), near the fixed junction; it fell to 8.32 MPa under a 12 mm boundary exclusion. Averages within 0.5, 1, 2, 3 and 5 mm were 81.82, 48.53, 30.22, 23.57 and 18.38 MPa, with 58, 242, 852, 1771 and 4129 nodes. This suggests a strong local concentration or fixture effect, not a converged service stress.

Checkpoint 05, 17:57:59, pictures/checkpoint_05.png: the shaft starts inside the flange and grows out of it, avoiding the previous flat-ended overlap; 136182.210 mm³, one body, no rebuild errors. Sampling found no obstruction at the required ring, driver cylinders, slot and cable and material around the pin. Still missing native dimension checks of this candidate, an appropriate axial pin load, a validated mesh series and a reliable strength verdict.

Checkpoint 06, 18:00:45, pictures/checkpoint_06.png: broad shoulder, 148416.594 mm³, one body and no errors; sampled clearances are clear, but the shoulder reads as a projecting ledge and its load response and exact interface checks are still outstanding. Shape exploration stage ended 18:02, about 25 minutes from C2 start; detail and study checks continue.

### Wider shoulder candidate E and refinement
The broader shoulder weighs 176.616 g (native 148416.594 mm³), still below the 261.129 g baseline, but its ledge is visually prominent. At 5 mm, 42,036 nodes, the +X/-X actual bearing cases each displaced 1.445 mm and reacted 59.997/60.008 N. +Y cheek thrust proxy displaced 5.206 mm and reacted 60.019 N. Its raw von Mises peak is 24.269 MPa at (14.59,4,-29.96) and raw Y-layer tensile and shear factors are 1.249 and 1.719. This is better than candidate C's proxy response but does not meet the target on that coarse raw result. The exclusion around the held face hides much of this junction and is not sufficient to establish it is safe.

For the +Y thrust proxy with mounting face held, global 6/4.5/3.5 mm meshes had 34,826 / 48,545 / 70,798 nodes and displacements 5.140 / 5.228 / 5.395 mm. Raw Y-layer tension was 14.185 / 21.276 / 28.307 MPa; raw von Mises 24.130 / 24.633 / 26.504 MPa; Y-layer shear 7.588 / 8.266 / 8.032 MPa. Tension increased 33% at the last refinement, so it is not converged; the sharp held flange/shoulder intersection is the identified location. The load itself is only a thrust-face proxy.

An alternative study fixed the six Ø3.4 hole walls instead of the mounting face. Under the same thrust proxy, it had 42,036 nodes, reaction 60.012 N and displacement 10.974 mm versus 5.206 mm; its raw peak shifted to a hole edge at (11.85,-4,-23.22). Because this is a different, unexpected peak, I treat its stresses as INVALID under the prediction rule despite the script logging them. Both supports idealise the joint and agree too poorly to prove a strength result; bolt/head contact and actual thrust transfer are needed.

Checkpoint 07, 18:07:44, pictures/checkpoint_07.png: a 1 mm elbow blend on the broad shoulder, 148372.926 mm³; the ledge remains prominent. Sampling found no violations of the ring, cable, slot, cheek annulus or driver cylinders. Its 5 mm mesh had 111,230 nodes; a deliberately conservative 79,999-node trial guard stopped before solving. A subsequent trial uses the measured count for prediction and remains below the user's 200,000-node cap.

The +X bearing refinement of unrounded E used 6 / 4.5 / 3.5 mm elements and 34,826 / 48,545 / 70,798 nodes. Maximum displacements were 1.434 / 1.454 / 1.491 mm. The first refinement stopped because the raw peak moved unexpectedly from the elbow to the fork root; the pin-load and fixture bounds and reactions were checked, and the fork root lies on the load path. A retry explicitly predicted either location. Raw von Mises was 8.435 / 8.718 / 12.549 MPa; it increased 44% on the last step. Y-layer shear grew from 3.207 MPa at 6 mm to 5.262 MPa at 3.5 mm. It is not converged. The coarse results are not a pass.

### Final selection and reviewer check
Selected candidate E without the radius: the rounded candidate's 111,230-node studies gave 39.55 MPa raw von Mises in the ±X cases and 109.98 MPa in the thrust proxy, both at the held junction. This is not a controlled convergence comparison with the unrounded 42,036-node meshes, but the radius did not demonstrate relief and produced high local stresses. The unrounded candidate's ledge and junction are still shortcomings, and its strength is not proven.

The final native file has volume 148416.594 mm³, mass 176.616 g, one body and no feature errors. The STEP round trip produced one body, 148416.715 mm³ (0.000081% higher), same native bounding box; the STEP declares millimetres. STL is one watertight component, 148060.465 mm³ (0.240% below native), with physical bounds [-35,-23,-213] to [35,23,35] mm. Its final shape statistics are area 33868.1 mm², flat share 0.361, largest flat 0.089, sharp length 1676.3 mm and sharp/sqrt(area) 9.11. Native box Y extents ±25.2 mm are spline control bounds; the STL physical extent is ±23 mm.

Final native face measurements are in final_export.log. Six Ø3.4 holes lie on the Ø50 pattern, the bore is Ø30, the pin holes are Ø8 on X=0, Z=-200 at Y=16..23 and -23..-16, and the inner cheek faces are flat at Y=±16. The final sampled checks show no violations in the ring, driver cylinders, cable, slot or cheek annulus. These checks do not prove the full continuous clear volumes, so fixed_items_ok remains false rather than asserting an unmeasured pass. The slot samples cover Z=-183.1 to -213; the exposed space below the part and the Ø30 motion sweep have not been separately certified. The nominal 9 mm radial cheek margin comes from a faceted semicircle: exact minimum wall measurement remains open.

The second load model used a rigid remote load on both pin holes: at 5 mm it displaced 1.4425 mm and reacted 60.000 N, compared with 1.4449 mm and 59.997 N for the bearing load. On nodes in the wrist below Z=-185, including load faces, the bearing model peaked at 1.216 MPa versus 1.092 MPa for the rigid model. These are coarse comparisons and do not validate the missing axial thrust model.

Final unrounded 5 mm all-node diagnostic SF yield / layer tension / interlayer shear, in X/Y/Z layer normals:

| Case | X | Y | Z |
|---|---|---|---|
| +X bearing | 4.621 / 4.243 / 3.237 | 4.621 / 4.818 / 3.343 | 4.621 / 1.617 / 3.098 |
| -X bearing | 4.621 / 6.113 / 3.240 | 4.621 / 5.781 / 3.344 | 4.621 / 2.585 / 3.097 |
| +Y thrust proxy | 1.854 / 1.504 / 1.702 | 1.854 / 1.249 / 1.719 | 1.854 / 0.894 / 1.682 |

The cheapest improvement is orientation: X layer normal raises the worst coarse proxy factor from 1.249 (Y layer tension) to 1.504 (X layer tension), about 20%, at zero material cost. This supersedes the preliminary Y-normal print suggestion above. Lay the part on its side with X as build direction; the projected bed envelope is roughly 46×248 mm, leaving only 8 mm in the long direction of a 256 mm bed, before brim and positioning. Supports under the disc, curved shaft and fork must be designed and removed without damaging bearing faces; slicing has not been done. At 20% higher load, that coarse X-layer factor would fall from 1.504 to 1.253 in linear analysis; the refined proxy's X-layer factor is only 0.918 before that increase. These are diagnostics, not validated safety factors.

Unfinished: the continuous mounting ring and moving envelope have not been proven by exact boolean measurement; every C1 face was not independently measured; neither final load path nor support is a validated representation of a real pin, thrust surface and bolted motor flange; the governing stresses have not converged and no three-case factor of two has been demonstrated; a suitable print layout/support and actual part fit have not been verified. Do not treat this as a print or structural-release approval. No solve exceeded 199,999 nodes; the largest was 199,455.

Native SHA-256 85712A62731206DA039D38A446297E86E6B52937F1291E2CE5D135A06D636C62; STL 135AA9B65157DC379C9CEF95014E91C5AE4D1B42FA8CB08E6DBAA89E24F6CD6F; STEP 7D90C8BEEB6498A395C55A573A3635CC264ADC7694B844FC76F047DC0C95DD4C. No commit or push was made.

Further rounded-junction thrust-proxy refinement used 6.0 / 5.0 / 4.5 mm global sizes and 104,698 / 111,230 / 116,626 nodes. Reactions remained approximately 60 N; displacements were 5.711 / 5.716 / 5.713 mm. Raw peak von Mises was 95.09 / 109.98 / 111.04 MPa, X-layer tension 64.46 / 55.07 / 54.60 MPa, and X-layer shear 20.32 / 19.86 / 20.88 MPa. The final shear increment was 5.15%, above the 5% convergence criterion. Even where two scalar peaks changed less than 5%, this idealized held-face / cheek-thrust problem does not establish the real joint strength. All rounded-candidate stress results, locations, mesh sizes and directions are in e_fillet_results.json and the associated nodal files.

Timing and process: C1 17:35:35–17:37 (about 1.5 min); C2 shape 17:37–18:02 (25 min); detail/export checks 18:02–18:22 (20 min); studies overlapped modelling and continued to 18:27; reporting and review followed. One shared launch lock was occupied from approximately 18:09 to 18:19 by another session's startup; this run did not touch its process. The launch then proceeded and the owned instances exited normally. The original hand estimates treated a uniform oval cantilever as 1.37 mm in X and 1.83 mm in Y; for the selected E, the X result 1.445 mm was 5.5% higher. The 5.206 mm Y thrust-proxy result is 2.85 times the uniform estimate, and the two support idealizations differed by over a factor of two. The hand model neglects the actual tapered root, disc compliance and offset cheek load, but their individual contributions were not isolated; that discrepancy is not fully explained.

End 2026-11-13 18:27:36 CST (2026-11-14 00:27:36 UTC), 52 minutes 1 second elapsed. The claim was released; final --status showed only the keeper PID 20496 and another session's PID 108976, and no instance belonging to this run. The selected C2 work lasted approximately 50.6 minutes. Model identity exposed to this session: GPT-6 / Codex; exact model variant and reasoning effort were not exposed.
