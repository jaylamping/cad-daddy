# terra-high-a benchmark report

Run start: 2026-11-13 16:44:42 CST (22:44:42 UTC). End: 2026-11-13 17:25:39 CST (23:25:39 UTC); elapsed 40 min 57 s. All clock times below are CST. This session identifies itself as Codex, GPT-6; the exact deployed model ID and reasoning effort are not exposed to this assistant. The run name suggests terra/high but that is not independent confirmation.

All work is in this worktree. The models are in `cad/_wip/sw-eval/terra-high-a/`; scripts, logs, nodal arrays, pictures and `results.json` are in this report's folder. No install, shared settings change, commit, or push. I used a separately owned hidden SolidWorks instance for every `job(wait_s=1800)`; I disabled `swkit.pin_export_prefs` in my scripts because `job()` otherwise writes machine-wide export preferences, contrary to the explicit instruction. Exports were checked under the existing settings. All meshes that solved were below 200,000 nodes.

## T1 — bracket (16:44:42–16:46, about 1.3 min; later audit 17:04)

Built and saved the specified single-body bracket, with STEP and STL. Hand volume = 36,000 + (1 − π/4)·4²·50 − 4·(1 − π/4)·5²·6 − 4π·2.75²·6 − π·(11²+4·1.7²)·6 = **32,974.0242 mm³**. Measured volume 32,974.0242 mm³; PETG mass at 1.19 g/cm³ **39.2391 g**. Box (0,0,0)–(80,50,46) mm; one body; no feature errors. Measured native cylinder faces show four R2.75 base holes at the specified centers, the R11 bore at Y25/Z28, and four R1.7 holes at Y/Z = 25±10.9602 / 28±10.9602. The R4 root spans X6–10/Z6–10 along Y; four R5 corner faces are in the specified corners. The eight-view `bracket.png` shows the L bracket and all holes.

STL: watertight, one shell, 32,990.3773 mm³ (0.050% above native), bounds (0,0,0)–(80,50,46) mm. STEP header says AP203 and millimetres. These export checks use the files, not an API success alone. No mating hardware file was specified for a separate fit test. The motor hole-to-bore ligament is 15.5−11−1.7 = **2.8 mm**, less than one 3.4 mm hole diameter, contrary to the playbook's edge-distance guideline; this is a specification concern, not a reason to silently move the holes. The nominal walls and ligaments otherwise exceed 0.6 mm by inspection and dimensions; printer access and as-built clearances were not tested.

## T2 — edit (16:46–16:47:10, about 1.2 min; later audit 17:04)

Opened the saved native T1 part, saved it as `bracket_b.SLDPRT`, then added the four counterbores and slot without rebuilding the T1 feature tree from its script. Counterbore removed volume = 4π(5²−2.75²)·3 = 657.3783 mm³; slot = (14·6+π·3²)·6 = 673.6460 mm³. Hand and measured volume **31,642.9999 mm³**; one body, unchanged box, no rebuild errors. Four R5 counterbore faces span Z3–6; each independent floor pick is Z3. Slot's two R3 end faces span X35–38 and X52–55, Y22–28, Z0–6, so the overall slot is 20×6 mm. `bracket_b.png` shows the counterbores and through-slot. The counterbore outer edge is only 5 mm from the Y edge, less than the 10 mm diameter guideline. A real screw head and driver clearance have not been checked.

## T3 — bracket study (16:47:10–16:49:25, about 2.3 min; alternative load in T5; twin checks 17:05-17:14, overlapping T5)

150 N +X at the bore; all four base-hole cylinders fixed. PETG E=1900 MPa, ν=0.38. Approximate root bending stress = 6·150·22/(50·6²) = **11.0 MPa**. At X0/Z12 a simple beam gives 8 MPa; the finest result's surface sample of 51 nodes averages **8.224 MPa von Mises**, about 2.8% higher. The first upright-only displacement estimate was 0.311 mm; it ignored rotation of the base. After adding a simple 19 mm base bending contribution, the estimate was 1.118 mm. The actual tip resultant is 2.344/2.351/2.357 mm; the estimate is within the playbook's factor-three gate but differs by over 20%, so the simplified hand model is not an independently validated deflection prediction. Fixture compliance, holes and three-dimensional load spread are omitted.

First run stopped at the prediction gate: 21,760 nodes and 2.344 mm exceeded three times 0.311 mm. No stress was interpreted in that run. The corrected-estimate retry used meshes 3.0/2.2/1.7 mm, 21,760/43,352/86,547 nodes, automatic solver. Reactions were (−150,0,0) N each. Fixture node boxes X22.25–67.75/Y7.25–42.75/Z0–6 and loaded bore boxes X0–6/Y14–36/Z17–39 were checked.

| element mm | nodes | VM away MPa | Z tension away MPa | Z shear away MPa |
|---:|---:|---:|---:|---:|
| 3.0 | 21,760 | 13.986 | 10.196 | 6.915 |
| 2.2 | 43,352 | 14.648 | 10.185 | 7.077 |
| 1.7 | 86,547 | 14.959 | 10.208 | 7.075 |

The fixed 6 mm fixture-and-load exclusion is common to the series. The last changes are below 5% for these masked values, but the mask hides real motor-hole material. The full-model VM maxima were 22.385/23.484/26.517 MPa, including fixed/load singularities; the motor box's Z tension under the rigid bore load was 11.578/12.330/12.592 MPa (finest location approximately X0/Y24.16/Z17.03). Even the latter is on the rigid loaded bore and is not an independent non-rigid bearing check. The finest masked VM is at (9.22,18.53,6.08) mm, giving yield factor 3.01; masked Z tension gives 2.20, and Z shear against 13 MPa gives 1.84. Do not call that a pass: the unmasked and alternate-load results are material.

At the finest mesh, same masked result by layer direction: X tension 13.149, shear 7.075 MPa; Y tension 4.971, shear 3.289; Z tension 10.208, shear 7.075. Locations are in `t3_rows.json`. In the alternate mounting-hole run below, Z tension is 17.593 MPa (factor 1.28), so the requested Z printing direction has an indicative failure even before the even-load check. The even-load and support checks below establish **fail** for the requested Z orientation. Force path: motor mounting region bends the upright into the root and base; base holes transmit it to the support. Bracket SHA-256: `8384921fc7d38048ab92ac7022d7b57b93576f3b1e113a222e361a50248722f2`.

### T3 even-load and alternate-support check (17:05-17:14)

Made a twin with four 0.1 mm deep annular motor load patches and a second twin with 0.1 mm deep annular washer support patches. Their volume differences from the original are 0.050% and 0.082%, with the same box; both are one-body, error-free models. `twins.png` shows them. The shallow steps approximate split faces and add artificial edges; the annular motor pads apply a total even +150 N. The base is fixed first on the four hole walls, then on the washer rings.

At global sizes 3.0/2.2/1.7/1.4 mm, 23,136/44,194/88,065/150,681 nodes, VM was 18.311/18.457/17.841/18.334 MPa and Z tension 15.920/15.067/15.849/16.117 MPa. The 2.2 mm washer-supported case gave VM 18.397 and Z tension 15.240 MPa, compared with 18.457 and 15.067 for hole walls at the same size. The reaction was -150 N X within 0.01 N; deflection was 2.832-2.849 mm for hole walls and 3.043 mm for washers.

To resolve local variation, with global 3 mm and hole-wall controls 1.0/0.8/0.6 mm, nodes were 25,889/29,633/38,052, VM 18.233/18.974/19.270 MPa, Z tension 16.206/16.081/16.313 MPa and Z shear 6.914/6.807/6.888 MPa. All three change under 5% in the last step. The last local Z tension gives **22.5/16.313 = 1.38**, below the requested 2; the higher load-region VM gives **45/19.270 = 2.34**. Verdict **fail**. The loaded hole region is retained in these maxima; only the 6 mm fixture exclusion is applied. The rigid bore and rigid hole load cases are additional sensitivity checks.

## T4 — sharp corner (16:49:25–16:51:25, about 2 min)

Opened T1, saved a copy and suppressed `ROOT_R4`, preserving the rest of the tree. `bracket_sharp.png` shows the square inside corner. Volume 32,802.3427 mm³, exactly 171.6815 mm³ below T1 as expected for the missing internal fillet; same box, one body, no rebuild errors. SHA-256 `69217c602ab543fedea462d11d34cc8adfd6e88b5adf36b1c24af75c2b3453`. First attempt failed because `EditSuppress2` is a Boolean property in this binding, not a callable; `call(d, 'EditSuppress2')` fixed it. No model or solve result from the failed attempt was used.

Same bore load and hole support, 3.0/2.2/1.7 mm: 23,409/43,671/86,565 nodes; reactions −150 N X and displacements 2.622/2.639/2.646 mm. VM picked at the geometric root line was **10.759/9.594/13.599 MPa**; away-mask VM was 14.384/15.127/16.250 MPa and Z shear 5.608/4.981/7.174 MPa. The root line is mesh-dependent, and its final changes fail 5%; no finite converged sharp-corner peak or pass/fail verdict is established. The 4 mm fillet study is the physically rounded comparison, and T3 reports its alternative load and support checks. Do not treat 13.599 MPa as a converged design stress.

## T5 - reinforced candidate (initial trial 16:51-16:53; twin checks 17:05-17:14; reinforcement 17:15-17:22; about 25 min of overlapping work)

The first, unchanged-geometry Y-orientation trial gave finest rigid-hole-load VM 14.976 MPa, Y tension 10.383 MPa and Y shear 4.241 MPa; but a non-rigid load at the motor holes exposed higher shear. With global 3 mm and hole-wall controls 1.0/0.8/0.6 mm it rose 5.974/6.784/6.778 MPa, giving **13/6.784 = 1.92**. The conservative engineering choice was to improve this margin, although the task explicitly sets factor 2 requirements for yield and across-layer tension. A pilot local run stopped at the prediction gate because 25,889 nodes was below half the 60,000 predicted; subsequent runs used measured estimates.

The selected `bracket_c.SLDPRT` is the original bracket with a **2 mm rear pad at X6-8, Y10-40, Z12-44**, and layers stacked along Y. The original diameter 22 bore and four diameter 3.4 holes pass through it, with the same centers; all base holes and the outer X0-80/Y0-50/Z0-46 box remain fixed. One body, empty rebuild errors. Hand added volume = 2*[30*32 - pi*(11^2+4*1.7^2)] = **1,087.101 mm3**; measured volume **34,061.125 mm3**, mass **40.533 g**, growth **3.297%**. `reinforced.png` shows the pad. The pad extends behind the original upright; rear motor, cable, driver and assembly clearance are not established from the specification. The part is a byte-identical copy of the tested standalone native reinforced part, SHA-256 `30d8db6e56f10ea15917b8c5caefe5033f7cdcd6a344cd1391c1d1a45b01b4c8`.

The even-load twin has four shallow 0.1 mm annular motor patches and is 0.048% smaller in volume; the washer-support twin is 0.080% smaller. At fixed global 3 mm and four hole-wall local controls:

| local mm | nodes | VM MPa | Y tension MPa | Y shear MPa |
|---:|---:|---:|---:|---:|
| 1.00 | 27,733 | 14.141 | 5.999 | 4.863 |
| 0.80 | 32,206 | 14.655 | 6.574 | 5.634 |
| 0.60 | 40,514 | 15.144 | 6.932 | 5.543 |
| 0.45 | 56,323 | 15.453 | 6.621 | 6.191 |
| 0.35 | 79,104 | **15.500** | 6.707 | **6.445** |
| 0.25 | 129,153 | 15.417 | 6.715 | 6.391 |

Last-step changes are 0.54%, 0.13% and 0.84%. The last mesh reaction is (-149.993,-0.004,-0.003) N; displacement 2.590 mm. The loaded-hole region is included and only fixture distances are excluded. The 3, 5 and 6 mm fixed-hole distance masks all give 15.417 MPa VM on the last mesh; at 2 mm it is 17.487 and at 1 mm 20.605 MPa. The all-node maximum is 22.416 MPa, at or near the artificial support, and was not treated as material peak. The 2.2 mm washer support gives VM 14.657, Y tension **7.349**, Y shear 5.062 MPa outside its 6 mm fixture mask, with reaction -150 N X and displacement 2.799 mm. Four individually rigid loaded screw holes, global sizes 3.0/2.2/1.7 mm, gave VM 13.970/14.704/14.897 MPa, Y tension 7.032/7.073/6.962, and Y shear 2.614/2.708/2.678; final changes are under 5% for all three. These are sensitivity checks, not actual preloaded screws.

Conservative maxima from these checks yield VM **15.500 MPa** (factor **2.90** against 45), Y tension **7.349 MPa** (factor **3.06** against 22.5), and Y shear **6.445 MPa** (factor **2.02** against 13). The factors on the specified yield and across-layer requirements exceed 2, and all three reported measures converged, so **pass for the stated linear-static case**, with very little shear margin. The worst shear comes from the even-load local series. On the final even-load mesh the layer-direction table is:

| layer normal | tension MPa | interlayer shear MPa |
|---|---:|---:|
| X | 13.080 | 6.807 |
| Y | 6.715 | 6.391 |
| Z | 12.289 | 6.805 |

At Z13, treating the pad and wall as a composite 50 by 6 plus 30 by 2 mm section gives centroid X=3.667 mm and I=1,720 mm4. With M=150*(28-13)=2,250 N mm, hand surface stress is 4.80 MPa; 42 sampled X0 surface nodes give 4.88 MPa VM, 1.7% higher. The crude 1.118 mm cantilever deflection estimate remains below the roughly 2.59 mm result because it neglects three-dimensional compliance of the perforated wall and nonideal base restraint; no independent deflection solution was demonstrated. Load enters the motor-hole pads, bends the upright and root, and exits through the four base supports.

The smallest margin is the **2.02 shear factor**: 20% more load would reduce it to **1.68**, and an actual print may have a lower shear allowable. A 3 mm rather than 2 mm rear pad would add another approximately 1.65% of the original mass, remaining under 10%; a simple inverse-thickness estimate reduces this shear from 6.45 to about 5.73 MPa (factor 2.27), but that option was not modeled and the estimate is not a verdict. Check real rear clearances, layer properties, fastener preload, fatigue, the shallow-patch idealization, print support, and physical testing before use.

## T6 — pin in a block (16:52:55–17:03:30, about 10.6 min)

The nominal projected bearing pressure is 500/(10.2·30) = **1.634 MPa**; that is an average pressure, not a prediction of the peak von Mises stress. Model: Ø10 steel pin through Ø10.2 PETG block hole; 0.1 mm radial gap. Block bottom fixed. Each pin end carries +250 N Z. No-penetration contact uses Intel direct sparse; separate bonded soft pads on the pin ends have radius 2.5 mm, length 2 mm and E=0.5 MPa, with outer faces fixed. `t6c_contact.png` shows the geometry and pads. Under the finest full load, the bound estimated from maximum pad traction times both pad areas is 1.77 N, 0.35% of 500 N. This is an idealized static no-penetration contact model (friction was not independently characterized): manufacturing error, preload, wear, and fatigue were not modeled.

A first model used R1 pads. Its 47,936 nodes exceeded the predicted 16,984 because the cylindrical local controls dominate the mesh, and its maximum displacement 0.959 mm exceeded the initial 0.2 mm estimate. The stress was not accepted. An upper-ligament bending estimate gave about 0.6 mm and a retry passed that broad gate, but inspection found the maximum at a pin end and large rotation while average pin rise was only 0.134 mm. Enlarging the soft pads to R2.5 suppressed this sensitivity; the first wider-pad run stopped at its 0.2 mm lower prediction threshold with 0.196 mm. The subsequent series predicted 0.15 mm, based on the observed pin rise, rather than treating the original maximum as physical. At common global 3 mm and local 1.5/1.25/1.0 mm controls:

| local mm | nodes | hole-surface peak VM MPa | location mm | pin mean rise mm | max displacement mm | pad force bound N |
|---:|---:|---:|---|---:|---:|---:|
| 1.5 | 33,265 | 4.875 | (−3.97,−13.69,13.21) | 0.13725 | 0.1400 | 1.78 |
| 1.25 | 47,614 | 4.842 | (−3.65,−13.37,13.56) | 0.13685 | 0.1961 | 1.78 |
| 1.0 | 73,081 | **4.880** | (4.28,−13.10,12.78) | **0.13708** | 0.1538 | 1.77 |

The final change is 0.79%; the hole-surface result mask is radial 5.08–5.35 mm, |Y|<14.9 mm, separating the block from steel. A separate check including the rim through |Y|≤15.01 found the same peak. All-body VM max 43.86 MPa is at (0,0,5) mm on the steel pin and is not the reported block bearing measure. Full contact pressure itself was not read; **4.880 MPa is hole-surface von Mises, not a claimed peak contact pressure**.

Reaction is (0,0,−500,500) N. Section integration of the pin's τyz over XZ planes, 0.1 mm sampling and 4.99 mm radius, gave −249.066 and +249.102 N at Y−20/+20, compared with 250 N per end (within 0.4%). At Y−10/0/+10 it gave −159.223/−0.063/+159.201 N; the change through the contact region is approximately 498.2 N versus 500 N. At total +0.005 N the wider-pad model rose 0.001575 mm, well below the 0.1 mm clearance, with hole VM 3.4e−9 MPa; the block and pin therefore are not spuriously bonded. At the same 1.25 mm contact mesh, R1 and R2.5 pads gave hole peaks 4.848 and 4.842 MPa respectively (0.12% difference). These checks support the reported VM result for this model; the extreme nodal displacement remains support-sensitive, so it should not be treated as a pin translation. Nodal data and the section-integration script are in this folder.

## T7 - diagnoses (written approximately 17:04-17:08; final review 17:23-17:25)

**a.** PID 2536 is HALF-CLOSED and blocks launch; 20948 is another live busy session and is not evidence of a hang. Stop without launching; report PID 2536 and `taskkill /PID 2536 /T /F` for the owner/operator. Never kill or restart PID 20948 or any other session's process. The apparent busy message about launches waiting is old wording; the keeper/current launch behavior can allow launch beside busy, but not beside HALF-CLOSED.

**b.** Error 24 after matrix decomposition with free RAM falling from 26 to 12 GB indicates likely factorization memory exhaustion, not proof of a loose body. Reduce model size, coarsen far away, use targeted local controls, symmetry or submodeling, keep every benchmark solve under 200,000 nodes, and retry after memory is available; inspect restraint/contact connectivity as well. Do not rerun the 796,000-node solve or interpret its failed result as valid.

**c.** An offset equal to a model-frame minimum suggests STL export translated to positive space (preference 71). Inspect the actual STL bounds and compare them with the native box, and check the export options and units. Re-export with frame-preserving settings only when authorized to change the relevant shared setting, or use existing correct settings; verify bounds, units, watertightness and volume. Do not move the native model to compensate or assume that the STEP and STL share the same frame.

**d.** A rising peak on a fixed edge is a likely fixture singularity, not a converged 61 MPa material stress. Name and examine the edge, run a consistent physical-distance exclusion and stress plateau/section check, refine three sizes, and compare a realistic alternate support (e.g. washer ring). Round any real sharp corner, rerun, and judge converged VM/layer stresses against the requested factors. Do not pass on a masked peak that hides a real feature, or declare a material failure solely from the divergent singular nodal maximum.

**e.** `busy` says a live client is driving the instance, not that it is hung; mesh and result readback can take a long time. Check `--status`, solver activity, timestamps of solver files and this instance's hidden-window log; wait if meshing, solving or readback continues. If a hidden dialog is confirmed, address only this owned instance in the way the playbook permits. Never kill a Python client during meshing or solving, restart another session, or infer a hang merely from silence. If our own process is truly stuck outside those operations, use its own handle/authorized cleanup, not another session's PID.

## Playbook/helper findings and remaining work

- `swkit.job.__enter__()` calls `pin_export_prefs()` unconditionally; those are explicitly documented as machine-wide. This conflicts with the user's instruction to change no shared settings, even for modeling-only jobs. We disabled the call locally in each script; the export checks above show the actual settings were suitable on this run. A per-job opt-out would avoid monkey-patching.
- `07-done`'s plain-volume node estimate with the suggested 1.5× refinement factor substantially underpredicted the contact mesh (16,984 predicted, 47,936 measured), because it does not account for entire large cylindrical faces receiving 1.25 mm controls. Predict per controlled region or use a measured pilot. The model's first displacement estimate also missed nearly free pin rotation: maximum displacement is not always pin translation. No stress from the failed prediction gate was passed off as valid.
- The default `away()` mask hides real motor-hole stresses near the rigidly loaded bore. This is already warned about in 05-fea and occurred here; separate region reporting and an even-load twin are necessary.
- The playbook intentionally links to unavailable examples in this benchmark. No other run folder or unavailable linked example was read. The 02-com warning about property versus method was confirmed by the `EditSuppress2` failure.
- T4 still needs a defensible finite sharp-corner judgment and support/load sensitivity; it remains **not shown**. T5 is a narrowly passing linear-static result, not a print or assembly authorization; the rear pad fit and actual fasteners have not been checked.

T6 model SHA-256: `b2eaa9eed3d51cc135eb0943881895551e8e18e86f106996f560c0b617fc99d7`. The image outputs were opened after each sheet run; the visual observations are reflected in the task sections above. T2 original feature IDs were not compared before and after, although the original named features remain in the saved tree.

Final cleanup: every owned SolidWorks job exited; `python tools/solidworks/sw_instance.py --status` showed no instance belonging to this run (only the keeper and another session). The `sw-eval-terra-high-a` claim was released and its absence confirmed in the claim list. No commit or push was made.
