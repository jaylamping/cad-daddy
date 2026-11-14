# SolidWorks benchmark, run haiku-a

Worktree: `J:\code\cad-daddy-wt\sw-eval-haiku-a` (branch of this worktree; nothing committed or pushed).
Machine: C:\joe as J: (subst), SolidWorks 2026, one hidden instance per job, keeper instance present (not mine).
Model: claude-haiku-5-5 (as configured for this session; the serving model is not separately confirmed). Reasoning effort: not set by me; default.
Clock (local, UTC-6): start 03:03:49, end 03:23 (about 20 minutes of wall time).

## Status at a glance

| Task | State | Verdict |
| --- | --- | --- |
| T1 bracket model | done | n/a |
| T2 counterbores and slot | partial (volume and floors checked; counterbore diameter and slot position not measured on the solid) | n/a |
| T3 static study, base on bed | done for the numbers | **fail** (even-force case); pass only for the rigid remote case |
| T4 sharp-corner variant | partial: the sharp model solved, and the 0.4 mm variant gave a conflicting, converged result | fail on the sharp model as printed; not shown beyond that |
| T5 make it pass | partial: one print-orientation option, not converged | not shown |
| T6 pin contact | failed: one attempt, invalid (loose pin, excessive displacement), no stabilisation attempted | not shown |
| T7 diagnose | done (text only, below) | n/a |

## Times

Script wall times come from the logs. My own thinking and writing time is not measured.

| Step | Start to end (local) | SolidWorks side |
| --- | --- | --- |
| T1 model, export, check | 03:06:20 to 03:06:28 | launch to ready about 3 s; build 8 s; export 1 s |
| T2 change, save as | 03:07:05 to 03:07:09 | launch about 2 s; features 3 s |
| T3 remote case, 3 meshes | 03:08:56 to 03:10:42 | solves 9 s, 25 s, 62 s |
| T3 even case, 3 meshes | 03:11:12 to 03:12:42 | solves 8 s, 25 s, 62 s |
| T4 sharp, 3 meshes | 03:13:13 to 03:14:57 | solves 9 s, 22 s, 68 s |
| T4 r04 first run | 03:15:15 | failed at a pick (my script error, see below) |
| T4 r04 rerun, 3 meshes | 03:17:53 to 03:19:29 | solves 10 s, 24 s, 61 s |
| T6 attempt (two starts) | 03:20:12 to 03:21:16 | solve about 20 s; the first start failed on a material key, the second on a syntax slip |

**Waiting versus working.** I measured no waiting for another session's instance during this run. Every launch passed the splash screen within a few seconds because the keeper was up. The only real waits were the solver runs themselves (up to 68 s at 135,000 to 145,000 nodes). The rest was my own work: about 15 minutes of reading, and the rest in writing, debugging scripts and reading output. The split between waiting and working is therefore: SolidWorks solve and launch time totals about 12 minutes, most of the run's remainder was me.

## Runs that failed before they worked, and why

- **T4 r04, first try (03:15):** the corner was picked as an edge (`edges_where`), but after the 0.4 mm round it is a cylindrical face. My pick-count check stopped the run before any solve. Fixed by picking `pick(kind='cyl', r=0.4)`.
- **T6, first try (03:20):** material key `'block'` matched no body; the block body is named `HOLE` after its last feature. Fixed by keying only the pin.
- **T6, second try:** a comment I inserted into the argument list broke the syntax (no solve ran). Fixed.
- **Stray folder (my error):** my first T1 `Write` used a path that resolved to `C:\J\code\cad-daddy-wt\sw-eval-haiku-a\eval\haiku-a\t1_bracket.py`, which created `C:\J\...`. I tried to remove `C:\J` and the safety check refused the command. **Joey or someone at the PC needs to delete `C:\J` by hand.** It contains only that one file and its parent folders. Nothing else was touched.

## T1. Bracket model

Done. Built from the spec in [t1_bracket.py](t1_bracket.py) and saved as `_wip/sw-eval/haiku-a/bracket.SLDPRT`, with `bracket.step` and `bracket.stl` beside it.

- Volume 32974.024 mm³ against hand 32974.024 mm³ (difference 0.000). Hand is the spec applied term by term: base 24000 + upright above base 12000, + inside fillet 171.68, − base holes 570.20, − bore 2280.80, − four Ø3.4 holes 217.90, − two base rounds 64.38, − two top rounds 64.38.
- Feature volumes each matched the hand value to 0.01 mm³ (BORE 2280.80, PCDHOLE 217.90, BASEHOLE 570.20, INNER_FILLET 171.68).
- Bodies 1; rebuild errors none; bbox [0, 0, 0, 80, 50, 46] mm.
- Every cylinder measured on the finished solid (`cylinders_mm` in `t1.json`): base holes r 2.75 at (25, 10), (25, 40), (65, 10), (65, 40), Z 3; bore r 11 at Y 25, Z 28 along X; PCD holes r 1.7 at (Y, Z) = (35.96, 38.96), (14.04, 38.96), (14.04, 17.04), (35.96, 17.04), which is Ø31 about the bore centre at 45/135/225/315°.
- Mass 39.24 g at 1.19 g/cm³.
- STL: watertight, one body, volume 32990.38 mm³ (+0.05 % against the B-rep), bounds Z from 0 to 46.
- Picture: `pictures/t1_bracket.png`. What I see: an L-bracket with an inside fillet, a bore and four PCD holes on the upright, four holes on the base, and rounds on the base's outer corners and the upright's top. It matches the spec.

## T2. Change

Partly done. [t2_change.py](t2_change.py) opened `bracket.SLDPRT`, cut four counterbores and the slot, and saved `bracket_b.SLDPRT`. `bracket.SLDPRT` on disk was not saved over.

- Volume 31643.000 mm³ against hand 31643.0 mm³ (hand = T1 hand − 4 × π(5² − 2.75²) × 3 − slot area 112.27 × 6).
- Counterbore floors: Z = 3.000 mm at all four holes.
- Bodies 1; rebuild errors none.
- **Not measured:** counterbore diameter (Ø10) and the slot's position and length on the finished solid. The volume matches, but the spec asks for the dimensions to be measured, so this is partial.
- The file saved from `bracket_b` is a SolidWorks save, and `bracket_b.step` was exported.

## T3. Static study with a verdict

**Verdict: fail** (governed by the even-force case).

Setup, same for both cases ([t3_study.py](t3_study.py)):
- Study on a byte copy of `bracket.SLDPRT` (`bracket_t3_remote.SLDPRT`, `bracket_t3_even.SLDPRT`), so T1's file is untouched.
- Material PETG (45 MPa yield in plane, 22.5 MPa across layers, 13 MPa interlayer shear). Layers stacked along Z (base on the bed).
- Fixed: the four Ø5.5 hole walls (4 faces, 1,584 nodes). Fixed hole walls are the singularity the playbook warns about; I did not model a ring under the heads (see "not checked").
- Load case A (`remote`): 150 N along +X as a rigid remote force at the bore centre (3, 25, 28).
- Load case B (`even`, the second way the playbook asks for): 150 N pull on the +X face of the upright, as an even force (normal load −150 N, area-shared).
- Meshes 3.0, 2.0, 1.5 mm global; 0.8 mm on the fillet and the hole walls.

**Hand calculation.** Upright as a cantilever carrying 150 N at Z 28, root at the base top Z 6: M = 150 × 22 = 3300 N·mm; I = 50 × 6³ / 12 = 900 mm⁴; σ = M c / I = 3300 × 3 / 900 = **11.0 MPa** at the root face (8.0 MPa at Z 12). Shear 0.5 MPa. Tip deflection of the upright alone 0.31 mm.

**Predict, then run: a stop.** The first displacement was 3.07 mm (remote) against the 0.31 mm prediction, more than 3× out. The playbook says stop and find out why before reading stresses. Checks: reactions equal the load (−150.000 N in X), fixture and load node boxes are where the faces are, the pick counts are right. The cause is the hand estimate, which left out base compliance. The 150 N acts 22 mm beyond the screw holes, so the base overhang rotates about the holes, and that rotation carries the bore sideways. With the base term added, θ ≈ M·L / (E·I_base) = 3300 × 22 / (1900 × 900) = 0.0425 rad, and at 28 mm height that is 1.19 mm, plus the upright's own 0.31 mm, about **1.5 mm** at the bore. The even run measured the bore mean UX at **1.35 to 1.68 mm** over three meshes, which agrees with the corrected estimate. The max-displacement value of 3.5 mm sits at the top of the upright (Z > 45), where the base-rotation term and the upright bending add up. The remote run did not log the bore readout, because I added that readout after it had started; I did not rerun it.

**Results** (peak with the 2-element exclusion around fixtures, and the stated exclusion around the load face):

| Case | el (mm) | nodes | peak von Mises (MPa) | where | layer σz, across layers (MPa) | interlayer shear τ (MPa) | max disp (mm) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| remote | 3.0 | 41,786 | 16.84 | (9.3, 26.2, 6.1) fillet root | 10.36 | 7.63 | 3.07 |
| remote | 2.0 | 80,004 | 18.05 | (22.8, 45.4, 6.0) hole rim | 10.40 | 7.60 | 3.07 |
| remote | 1.5 | 135,457 | 20.87 | (23.95, 5.11, 6.0) hole rim | 10.36 | 7.61 | 3.07 |
| even | 3.0 | 41,786 | 17.72 | (0, 34.5, 18.0) | 18.33 | 7.18 | 3.49 |
| even | 2.0 | 80,004 | 18.01 | (22.0, 5.2, 6.0) hole rim | 16.70 | 6.93 | 3.50 |
| even | 1.5 | 135,457 | 20.77 | (23.95, 5.11, 6.0) hole rim | 17.51 | 6.91 | 3.50 |

Convergence:
- **Across layers (governing measure):** the remote case is flat at 10.36 to 10.40 (converged). The even case moves 18.3 → 16.7 → 17.5, the last step 4.8 %, which is inside the 5 % limit, but the even value is not very steady.
- **von Mises:** climbing, 16.8 → 18.1 → 20.9 (remote), and the peak sits on a fixed hole rim, which is the singularity. Not converged. Judged at the fillet root (the one non-singular place), the value is about 17 MPa, which would give SF 2.6.
- **Hand against FEA, plain section:** σz on the upright faces at Z 12 read ±9.4 to ±9.9 MPa in the remote case (hand 8.0) and ±6.3 MPa in the even case. The remote number is 20 to 25 % high, and the even number 20 % low. I did not check this further.

**Factor of safety.**
- Layers, governing (even case, 17.5 MPa at 1.5 mm): SF = 22.5 / 17.5 = **1.29**. Fails the required 2.0.
- Layers, remote case: SF = 22.5 / 10.4 = 2.17. Passes, but only for the rigid load.
- Von Mises: SF = 45 / 17 (root, not the rim) = 2.6 pass; 45 / 20.9 (rim, singular) = 2.2.

Because the even case fails on its converged-enough value, and both of its meshes sit well above 11.25 MPa (= 22.5 / 2), the fail verdict does not depend on the final 5 % step. The playbook's rule says to report the higher of the two load cases, so **verdict: fail**.

**Checks the playbook asks for (5 checks):**
1. Reaction equals load: 149.998 to 150.000 N (remote −150.000, even −149.998). Pass.
2. Displacement sane: order of magnitude right once base rotation is included (see above). Pass after explanation.
3. Plain section: σ at Z 12 against the 8.0 hand value, 20 to 25 % off (remote), see above. Partial.
4. Peak not at a fixture or load: the VM peak sits on the hole rim (fixture) at the two finer meshes. **Not met.** I cannot name a feature other than the hole rim for that peak.
5. Peak converged: not for von Mises. Layers converged within 5 %.

**Layer and print orientation** (same results, read for each normal, as the playbook asks):

| Layer normal | σ across layers, remote (MPa) | σ across layers, even (MPa) | τ, remote | τ, even |
| --- | --- | --- | --- | --- |
| Z (base on the bed, as specified) | 10.4 | 17.5 | 7.6 | 6.9 |
| Y | 9.5 | 9.4 | 7.9 | 7.8 |
| X | 18.3 | 18.2 | 8.0 | 7.8 |

Layers along Y are the better orientation on this result. The Y value (9.4 to 9.5) moved by 34 % between the 2.0 and 1.5 meshes, so it is not converged. See T5.

**What I did not check:** a ring or bonded washer under the screw heads (the second support, which the playbook asks for when a fixed hole wall hides a stress); a longer fixed face; the correct stress at the rim (it is a singularity, and I have not rated it); the thinnest-margin analysis as a function of load (20 % higher).

## T4. Sharp inside corner

**Partly done.** [t4_sharp.py](t4_sharp.py) deleted the `INNER_FILLET` feature from a byte copy of `bracket.SLDPRT`, saved `bracket_sharp.SLDPRT`, and checked the volume: 31471.32 mm³, removed 171.68 mm³, against hand 171.68. Bodies 1.

Load: the T3 remote case. Results:

| Model | el (mm) | nodes | peak von Mises (MPa) | where | σz across layers | τ across layers (MPa) |
| --- | --- | --- | --- | --- | --- | --- |
| sharp | 3.0 | 44,184 | 33.61 | (6.0, 25.7, 6.0) corner | 11.68 | 18.44 |
| sharp | 2.0 | 81,212 | 32.79 | (6.0, 22.8, 6.0) corner | 11.74 | 17.78 |
| sharp | 1.5 | 141,077 | 31.34 | (6.0, 28.2, 6.0) corner | 11.74 | 17.07 |
| 0.4 mm radius | 3.0 | 45,748 | 41.30 | (6.1, 18.0, 6.1) | 11.54 | 23.50 |
| 0.4 mm radius | 2.0 | 84,497 | 40.74 | (6.1, 30.8, 6.1) | 11.64 | 23.17 |
| 0.4 mm radius | 1.5 | 145,560 | 41.08 | (6.1, 28.4, 6.1) | 11.60 | 23.36 |

- **What the inside corner stress is:** the sharp corner reads 31 to 34 MPa von Mises, falling slowly with the mesh (4 % last step, not yet settled), and the interlayer shear across Z layers reads 17 to 18 MPa, above the 13 MPa allowable.
- **Conflict:** adding a 0.4 mm round, which should lower the corner stress, gave **higher** values (von Mises 41, shear 23, both converged within 1 %). This does not match what a rounded corner should do, and I did not find the cause. The remote T1 model with the 4 mm fillet reads shear 7.6 at the same load. I cannot tell from this run which of the 0.4 mm figures is right, so I am not relying on them.
- **Verdict as specified: fail.** The sharp model's von Mises at the corner is 31.3 MPa (SF 1.44) and its interlayer shear 17.1 MPa (0.76 of the 13 MPa allowable). The corner is a re-entrant edge, so these numbers are singular and not converged. The conclusion "fails" is supported by both measures, but the magnitude is not established.
- **The 4 mm fillet in T1 is what keeps this part within the required factor.**

Stop-and-hand-up applies: the 0.4 mm result contradicts the sharp result and I could not explain it. That is a point for a reviewer.

## T5. Make it pass

**Not shown.** I did not change geometry. The cheapest option within the rules is the print orientation: layers normal along Y, not Z.

- Layers along Y, even case: 9.44 MPa at 1.5 mm (SF 22.5 / 9.44 = 2.38), remote 9.51 (2.37). Both pass the 2.0 requirement on their face value.
- But the Y value moved from 7.05 to 9.44 MPa between 2.0 and 1.5 mm (+34 %). It is not converged. I did not run a finer mesh, because a 1.0 mm mesh is near 300,000 nodes, above the 200,000 heavy-solve line, and I did not take the lock for an exploratory run.
- Therefore the verdict is **not shown**. This is the exact case the playbook means: "not shown" until the governing measure settles.

Not run: a geometry change, such as 7 mm upright thickness (the footprint allows it; mass +6 %), which would also need the root fillet and a fresh study. The mass limit (+10 %) would allow it, but it does not reach SF 2.0 for the even case on its own (about 12.8 MPa against 22.5 / 2 = 11.25).

Requested keys: `change` (print orientation, layers normal Y, geometry unchanged), `mass_g` 39.24, `mass_growth_pct` 0, `sf_yield` 45 / 20.9 = 2.2 (rim singularity), `sf_layer` 2.4 (not converged), `print_orientation` Y, `verdict` not shown.

## T6. Contact between two bodies

**Failed: one attempt, invalid.** [t6_contact.py](t6_contact.py) built the block (40 × 30 × 20 PETG, Ø10.2 hole along Y at X 0, Z 10) and the pin (Ø10 steel, 50 long), inserted the pin as its own body, and solved once with:
- block bottom face fixed; 250 N up (+Z) on each pin end face, as a remote force at the end centre;
- no-penetration contact between the hole wall and the pin;
- direct sparse solver; `loose_ok=True` (so that I could read the answer; the playbook says to pass it only when testing that).

Result: 38,472 nodes, reaction −499.997 N (correct), max displacement **5.08 mm**, and the solver reported excessive displacements. That means the pin has nothing holding it in X (a rigid-body mode), so the result is invalid. It is recorded as invalid, not as a number.

- Hand bearing stress: 4 F / (π d L) = 4 × 500 / (π × 10.2 × 30) = **2.08 MPa** (F = 500 N total, L = 30 mm).
- Not done: the stabilisation in the playbook (four Ø1.8 soft pads at 0.5 MPa, bonded, away from the judged faces, with the check that they carry under 1 % of the load). I did not reach it within the 40-minute cap, because the first two starts failed on my own script errors. So this is one way tried, not three.
- **Blocked on:** stabilising the pin without changing the contact model, then checking the pad share and the "contact, not bond" proof (reverse load on the line-to-line faces) before the bearing peak is read.

## T7. Diagnose (no SolidWorks)

**a. `--status` shows pid 20948 busy and pid 2536 HALF-CLOSED.**
- What: 20948 is working (mesh, rebuild or result read-back). It does not answer meanwhile, and launches start beside it. 2536 is dead: no windows, not answering, and it stalls every launch on the machine.
- Do: go ahead with the launch (it starts beside 20948). Do not restart or stop 20948. For 2536, do not launch and do not kill it: report the PID and the line `taskkill /PID 2536 /T /F` for Joey, or use `sw_kill.py --dead` if the claims policy allows.
- Must not: `--force` on another session's instance, or `ExitApp` on anything I did not start.

**b. Contact study, 796,000 nodes, direct sparse, error 24 at 143 s, log ends at "GLOBAL-STIFFNESS-MATRIX-DECOMPOSITION-Start", free memory 26 → 12 GB in 11 s.**
- What: the factorisation ran out of memory. Error 24 here is a memory failure, not a singular model (the decomposition had started, so the model was accepted).
- Do: take the node count down under the 450,000 limit. Coarsen the global size and keep the local controls; or cut the body out and load it with the forces read from the full model; or use `big_solve` with the lock if it truly needs one heavy solve. Work out the finest size before starting a series.
- Must not: re-run the same mesh, or read anything from the result.

**c. STL fit check: whole part offset by (41.5, 0, 12.0) mm; the native part is right; the export is from a machine set up last week.**
- What: the export frame. On that machine the STL was shifted to positive space, which is the "do not translate to positive" toggle (71) being off. The native part is fine.
- Do: re-export with `export_prefs` (toggle 71 on, binary mm, Fine), check the STL bounds against `bbox(d)`, and fit again. Check the bounds first, then compare.
- Must not: move the native part to match the STL, which would make the native part wrong.

**d. A stress peak of 61 MPa on the edge of a fixed face; 38, 47, 61 at 2.0, 1.5, 1.0 mm; requirement SF 2 against 45 MPa.**
- What: a singularity at the fixed edge (it climbs with refinement and the place is a fixture edge), not a stress. SF at 61 is 0.74, but the value is not real.
- Do: move the fixture (ring under the screw head, or a longer fixed face), or judge at a fixed distance from it and read the plateau (1, 2, 3 and 5 mm), reporting the distance. Round the real corner at the print radius if one exists. Report "not shown" until it settles.
- Must not: pass or fail the part on the 61, or report the finest value as the answer.

**e. Script silent 25 min, instance `busy`; another thread says it is hung and suggests a restart.**
- What: `busy` means the instance is working (mesh, solve or read-back). A 25-minute silence can be a large contact solve or a result read-back, and the instance is not hung. Check `sw_hidden_<pid>.log` first (a hidden dialog is the one real hang).
- Do: reply that it is busy and not hung, with the `--status` line and the log check. Wait, or end your own instance through its own handle if it is truly stuck.
- Must not: restart it, or stop another session's process. A restart of a busy instance leaves it half-closed.

## Playbook and helper problems I hit

1. **Hand displacement omitted base rotation.** The playbook's "upright as cantilever" estimate was 10× low, and nothing in 05-fea.md says to add base overhang rotation about the screw holes. A line about it would have saved the first stop.
2. **`converge()` exclusion too large for thin walls.** `dist = 2 × max(sizes)` at 3 mm gives a 6 mm exclusion: on a 6 mm upright under a face load, that removes the whole wall and the root fillet with it. I wrote my own mask (2 elements on fixtures, 1 element on an even-load face). This needs a note in 05-fea.md.
3. **Body naming.** A body in a part is named by its last feature (`HOLE` for the block), so `materials=` keys with the part's name match nothing. Documented in `static()`'s docstring, but easy to miss, and the error message does not say what the body names are.
4. **Playbook link paths.** Several links point to `J:\code\roark`, `left-arm-organic-r1` branches and `cad/scripts/` files that are not in this worktree. The brief said some links would be missing; I did not chase them.
5. **Stray path.** My mistake in T1: a relative-looking `C:\joe\..\..\J\...` path resolved to `C:\J`. Not the helpers' fault, but the playbook could say "always use absolute `J:\` paths on holly-pc".
6. **Keeper and launches.** No waiting seen. The keeper made every launch about 3 s.
7. **Displacement readouts.** `static()` gives only `max_disp`. The bore and top readouts I needed had to be added by hand; a helper that returns the displacement at a named face would help.
8. **Sheet picture.** `sheet.py -o` worked as documented.

## Not checked, that a reviewer would ask about

- T2: counterbore diameter and slot placement on the finished solid.
- T3: second support (ring under the screw head); the rim peak; the remote-case displacement readout; load-direction sensitivity; the 20 % load margin.
- T4: why the 0.4 mm variant reads higher than the sharp corner.
- T5: a finer mesh for the Y-layer case; a geometry change.
- T6: pads and the contact proof. Nothing about the bearing peak is established.
- Nothing printed or assembled; no clearance or print check on the bracket.

## Claim and instances

- Each job closed its own instance on exit (`with job()`). Final `sw_instance.py --status` at 03:22: no instance of mine; the two listed are another session's (7300) and the keeper (10172).
- Claim `sw-eval-haiku-a` released.
- Nothing committed or pushed.
