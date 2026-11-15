# REPORT: benchmark run `sonnet-adv-a`

**Model and effort.** Model `claude-sonnet-5-5` (configured, with `claude-opus-5-5` and `claude-opus-5` as fallbacks; I saw no fallback happen). **Reasoning effort: 5**, as the `reasoning_effort` tag in my session context read (the scale is not given to me). I had an `advisor` tool and used it twice: once at the start before any SolidWorks work (it caught the axial-load trap in T3, the `converge()` mask, and the pad and contact plan), and once near the end on this report; the second call found a wrong body mask in T6, a claim I had not tested, an unread region next to the holes, and a number I had checked in the wrong place. All three were changed (T6, T5/T3 bore wall, T3 check 3).

**Clock (local, CST; UTC is +6 h).** Brief received 17:28:48. Reading done and first stamp 17:33:23 (4.6 min; the label I wrote in that first `times.log` line says "~14 min", which is wrong). First SolidWorks launch 17:34:58. Last SolidWorks job closed 18:24:43 (T6 centred series), report finished and claim released 18:27:46 (59.0 minutes after the brief). The T6 limit of 40 minutes ran from its first stamp 17:46:25 to 18:24:43 = 38.3 min.

**Which `times.log` lines mark each task** (the file is one clock for several jobs, so jobs that overlapped interleave; T3, T4 and T7 have no end stamp of their own):

| Task | Start line | End line |
| --- | --- | --- |
| T1 | `T1 start` 17:35:03 | `T1 end` 17:35:14 |
| T2 | `T2 start` 17:35:14 | `T2 end` 17:35:20 |
| T3 | `T3a job start` 17:37:59 (the 17:37:23 line is the failed first run) | `T3b studies done` 17:41:34 |
| T4 | `T4 start (build bracket_sharp)` 17:41:34 | `T4b job end` 17:46:11 |
| T5 | `T5 start` 17:44:33 (first build) and 17:48:47 (final build) | `T5 job end` 17:46:33 and 17:51:06 |
| T6 | `T6 start` 17:46:25 (run 1), 17:51:44 (run 2), 18:11:07 and 18:12:31 (centred) | `T6 job end` 17:51:27, 18:02:27, `centred-pin series end` 18:24:43 |
| T7 | none: written while the T4 to T6 solves ran, about 17:42 to 17:47 (file time of `t7.md`) | |
| final checks | `final checks start` 18:02:57 | `final checks end` 18:03:01 |

**Times per task, from those lines and the job logs** (SolidWorks job time includes the launch, about 4 to 5 s a job, and is the whole job; "studies" is the sum of `static()` times: mesh, solve, read-back):

| Task | Status | SolidWorks job time | Studies in it | Launch waits | Waits behind another session's instance |
| --- | --- | --- | --- | --- | --- |
| T1 | done | 11 s (same 22 s job as T2) | none | 5 s | 0 |
| T2 | done | 6 s | none | in the T1 job | 0 |
| T3 | done: **fail** | 138 s over three jobs, one of them the failed first run (15 s) | 117 s (7 studies) | 15 s | 0 |
| T4 | done: **fail** | 265 s over two jobs | 228 s (6) | 10 s | 0 |
| T5 | done: **pass** | 273 s over two jobs (first build, then the mouth-rounded final build) | 212 s (8) | 10 s | 0 |
| T6 | done, valid | 29 min over five jobs (307 s run 1 invalid, 649 s run 2 seated, 51 s and 732 s centred) | 1,600 s = 26.7 min (12) | 25 s | 0 |
| T7 | done | none | none | none | none |
| Final checks | | 4 s | none | 4 s | 0 |

**Waiting against working.** (Measured: the SolidWorks and study times above, from the logs. Estimated: the split of my own time, which has no stamps.) Launch waits: twelve launches of 3 to 5 s, about a minute in all; the keeper (PID 10172) was the oldest instance, no launch ever waited behind another session's solve or rebuild, and no other session had an instance in my window: 0 s waiting for another session. Study time, 33 studies: about 2,150 s = 36 min, most of it the contact studies (453 s for the finest T6, 309 s for the finest seated, 165 s and 147 s for two more). My own time, estimated: reading and planning 4.6 min (measured), writing scripts about 14 min, idle waiting for a solve with nothing else to do about 15 min (mostly the T6 centred series, 12 minutes of it while I wrote this report), reading and analysing results about 12 min, writing this report and the post-processing the advisor asked for about 25 min. These add to the 59 minutes of the clock only roughly because SolidWorks jobs ran while I did other work.

**What was run.** 33 studies, every one under 200,000 nodes (largest 195,072); no heavy-solve lock; no instance half-closed; no hidden dialog stopped anything; my instances (PIDs 124676, 121372 for the failed T3 run, 126596, 119988, 127232, 124912, 132624, 131160, 133004, 131240, 141828, 143020) were closed by their jobs; `sw_instance.py --status` at the end shows the keeper 10172 only. I touched no other process. **Claim:** I claimed `sw-eval-sonnet-adv-a` and did not beat it during the run, so `claims.py list` showed it STALE at the end (57 minutes); the playbook says to beat on a long job and I forgot. The claim records no PID (the brief's `job()` launches per script), and `--status` printed "no claim" beside my instances because the claim's path (`j:\code\...`) and the instance's path (`c:\joe\code\...`) differ in spelling: that is a helper gap, noted below.

## Summary

| Task | Result |
| --- | --- |
| T1 | `bracket.SLDPRT/.step/.stl`: 32,974.02 mm³ (hand 32,974.02), 39.24 g, box 80 × 50 × 46, one body, STL watertight |
| T2 | `bracket_b.SLDPRT`: 31,643.0 mm³ (hand 31,643.0), counterbore floors at Z 3.0, original file unchanged |
| T3 | **Fail.** Tension across the layers (layers along Z) at the lower Ø3.4 hole rims 14.5 MPa (hole-wall support) and 15.3 (bottom-face support) against 22.5: factor 1.56 and 1.47. Von Mises 18.8 (factor 2.39). Hand root stress 11.0 MPa |
| T4 | **Fail.** Sharp corner is a singularity (22.8, 26.0, 30.0 MPa); with the printed 0.4 mm radius 38.3, 38.4, 40.4 MPa (a lower bound): factor 1.11; the hole-rim failure of T3 is the same |
| T5 | **Pass.** `bracket_c.SLDPRT`: upright 6 → 7.5 mm on the inner face, R0.4 on the four hole mouths, printed on its side (layers along Y); mass +7.15 % (42.05 g); `judge()` pass, lowest factor 2.60 |
| T6 | Valid. Peak bearing 5.8 MPa smoothed (6.3 raw node; hand Hertz 6.76, mean 1.67); block von Mises 5.2; pin rise 0.129 mm; reaction 500.00 N; pad share 0.028 % |
| T7 | all five answered below |

Files for the first four tasks (`.SLDPRT`, `.step`, `.stl`, sim `.npz`) are in `_wip/sw-eval/sonnet-adv-a/` (gitignored, so not in any commit; nothing was committed or pushed). Scripts, logs, rows, pictures, `results.json` and this report are in `eval/sonnet-adv-a/`.

## T1. Bracket from a specification: done

**What I did.** `t1_t2.py`: base plate and upright as two mid-plane extrudes (24,000 and 12,000 mm³, merged to one body), R4 fillet on the one edge along Y at X 6, Z 6, then the base holes, the bore and the four Ø3.4 holes as three cuts, then the R5 rounds in two groups. Every feature carried `expect_dv`; each raised unless the volume change was within 1 % of the hand value. Saved after every step. `bracket.SLDPRT`, `bracket.step`, `bracket.stl` are in `_wip/sw-eval/sonnet-adv-a/` (gitignored); the script is `t1_t2.py`.

**Hand calculation** (in the script): 24,000 + 12,000 + 171.68 (R4: (16 − 4π) × 50) − 570.2 (4 × π 2.75² × 6) − 2,280.6 (π 11² × 6) − 217.9 (4 × π 1.7² × 6) − 64.4 − 64.4 (four R5 rounds, 5.365 mm² × 6 each) = **32,974.02 mm³**, 39.24 g at 1.19 g/cm³.

**Checks, with numbers.**

| Check | Result |
| --- | --- |
| volume | 32,974.02 mm³ against hand 32,974.02 (0.000 %) |
| box | 0, 0, 0 to 80, 50, 46 (each within 0.01 mm) |
| bodies, rebuild errors | 1, 0 |
| base holes (`pick` + `face_info`) | four Ø5.5 faces with box centres (25, 10), (25, 40), (65, 10), (65, 40), z centre 3.0, all to 0.01 mm |
| bore | one Ø22 face, centre Y 25.0, Z 28.0 |
| small holes | four Ø3.4 faces, centres (Y, Z) = (14.04, 17.04), (14.04, 38.96), (35.96, 17.04), (35.96, 38.96): 25 ± 10.96, 28 ± 10.96 |
| R4 | one face, box X 6 to 10, Z 6 to 10, full width 50 |
| R5 | four faces: (X 75 to 80, Y 0 to 5 and 45 to 50, Z 0 to 6) and (X 0 to 6, Y 0 to 5 and 45 to 50, Z 41 to 46) |
| STL | watertight, one shell, volume 32,990.4 mm³ (0.05 % over the solid: facets), bounds within 0.1 mm of the box |
| STEP | `SI_UNIT` line carries `.MILLI.` |

Picture check (`pictures/bracket.png`): an L-bracket, plate low, upright at the X 0 end, a visible inside round, four holes in the plate, a bore with four small holes in the upright, rounded corners on the far end of the plate and on the top of the upright. It matches the specification.

**The specification, questioned (not changed).** (1) The Ø3.4 holes sit 2.8 mm from the bore wall (15.5 − 11 − 1.7), less than one hole diameter; an M3 boss there is a stress raiser, and T3 finds it governs. (2) The bore has 6 mm of bearing length for a Ø22 (length/diameter 0.27); fine for a pilot, thin for a shaft. (3) The upright is 6 mm thick, loaded across its thickness in T3. (4) Fine otherwise: bore top to upright top 7 mm, bore bottom to plate top 11 mm, base hole edge to side 7.25 mm, to the fillet toe 12.25 mm, all walls over 0.6 mm; nothing contradicts anything.

**Not verified.** Nothing about print: no slice, no overhang check on the bore.

## T2. Change an existing part: done

**What I did.** Opened the saved `bracket.SLDPRT` (volume checked to 0.01 % on opening), `save_as` to `bracket_b.SLDPRT` **before** the edit, then cut the four Ø10 × 3 counterbores (one sketch of four circles, mid-plane on Z 4.5, depth 3) and the slot as a 14 × 6 rectangle plus two R3 circles (so no arc direction to get wrong). Hand volume: 32,974.02 − 4 π (25 − 2.75²) × 3 (657.4) − (14 × 6 × 6 + π 9 × 6) (673.6) = **31,643.0 mm³**; measured 31,643.0.

**Checks.** Feature tree before: 35 entries; after: the same 35 (compared by name and type; I did not compare internal IDs) plus twelve new ones (`CB_P`, `CBORE_SK`, `CBORE`, `SLOT_P`, `SLOT_RECT_SK`, `SLOT_RECT`, `SLOT_E1P`, `SLOT_END_L_SK`, `SLOT_END_L`, `SLOT_E2P`, `SLOT_END_R_SK`, `SLOT_END_R`), so it was an edit and not a rebuild. The original file: same SHA-256 before and after (`e6880b16…a35379`) and the same volume when reopened. Counterbore floors: four planar faces at Z = 3.000 with outer diameter 10.000; four Ø10 wall faces. Slot: two R3 faces, overall length 20.000, width 6.000, centre X 45.000, Y 25.000. One body, no rebuild errors, box unchanged. Picture (`pictures/bracket_b.png`): four stepped holes on the plate, one slot between them on X 45, upright untouched.

**Not verified.** Counterbore against a real screw head. Computed, not measured on the solid: the slot ends at X 35 and 55 and the counterbores span X 20 to 30 and 60 to 70, so the web between a slot end and a counterbore is 5 mm each side; the slot to the plate edges 22 mm.

## T3. Static study with a verdict: **fail** (tension across the layers, about 1.5)

**The case, written before SolidWorks.** The bore axis is X and the load is +X, so it is **axial**: a bearing load is refused (05-fea: it must be square to the axis) and an even normal force on the bore sums to zero (reaction 0, 05-fea). A rigid `'remote'` load on the bore stiffens exactly the ligaments that matter (05-fea reports this very bracket passing at 2.2 where it fails at 1.4). So the load goes where a screwed-on motor puts it: through the four M3 heads on the X = 0 face. I made a twin `bracket_t3rings.SLDPRT`: the T1 part plus a 0.3 mm deep, Ø6 circular step round each Ø3.4 hole (volume −23.0 mm³ = 0.07 %, box identical), and put an even 150 N on the four step floors (faces that look along −X, force +X). Support: the four Ø5.5 hole walls fixed. PETG as `swfea.PETG`, layers stacked along Z (base on the bed).

**Hand estimate.** Moment about the plate top 150 × 22 = 3,300 N·mm; root of the upright, 6 M / (b h²) = 6 × 3,300 / (50 × 36) = **11.0 MPa** (compression on the fillet side, tension on the X = 0 face). At the lower Ø3.4 holes the section moment is 150 × 11 = 1,650 N·mm, nominal 5.5 MPa, times 3 for a small hole = **16.5 MPa** across the layers: factor 1.36, a fail before any solve. Upright tip 0.31 mm alone. **My first displacement prediction was wrong:** I forgot the plate turns between the screws (a cantilever 25 mm beyond the first screws, 0.048 rad, 40 mm up the upright = 1.9 mm); with that 2.2 mm, solved 2.84 mm. That was a 9-fold miss, past the factor 3 at which 07-done says to stop; I stopped to explain it (the plate rotation gives 2.2 mm, within 30 % of the solve) before I trusted any stress, and went on only then.

**The series** (`t3a.py`, `lib3.py`; hole walls fixed, rings loaded, controls shrunk with the global size: rings el/3, small and fixed hole walls el/2):

| el mm | nodes | peak von Mises, hole rims | layer tension (Z), hole rims | interlayer shear (Z), hole rims | interlayer shear (Z), root fillet | max disp mm |
| --- | --- | --- | --- | --- | --- | --- |
| 3.0 | 24,804 | 17.84 | 14.59 | 5.56 | 6.69 | 2.837 |
| 2.2 | 53,442 | 18.19 | 14.57 | 6.33 | 7.06 | 2.846 |
| 1.6 | 123,582 | 18.79 | 14.47 | 6.51 | 7.02 | 2.851 |

Hole rims = nodes within 2.2 mm of the hole axis, whole thickness. I did **not** use `converge()`: it masks nodes within two coarse elements of every load face, which swallows exactly these rims (the rings are the load faces). Instead `measures()` in `lib3.py` reads regions at every size and `judge()` is fed the series (three measures × four regions). Peak von Mises sits at (6.0, 15.7, 17.4): on the X = 6 face at the lower Y-low hole.

**The five checks.** (1) Reaction Fx −149.993 N for 150 N (0.005 %), Fy, Fz under 0.005 N. (2) Displacement 2.84 mm against hand 2.2 (the explained 30 % miss; the first prediction, 0.3 mm, was off 9 times). (3) Plain section, σz on the X = 0 face at z 12 to 14: my first reading, the middle of the width only (y 18 to 32), was 5.6 MPa against hand 7.5, 25 % low and outside the 15 % band. I then read it across the full width from the saved nodal results (`T3_RINGS_el*.npz`): the mean over all nodes is 6.7 and over ten equal y-bins 7.1 (7.2 and 7.1 on the two coarser meshes), against 7.5, and the stress is not uniform in y: 5.6 in the middle, 6.0 beside the holes, **9.6 at both edges** (shear lag: the load enters at y ≈ 14 and 36 through the rings). Integrating σz over the whole section at z = 13 gives a net force of −8 N (should be 0) and a moment of 2,541 N·mm against the hand 2,250 (13 % high; 2,596 and 2,566 on the coarser meshes). So check 3 passes on the section as a whole, and the middle-strip reading was the wrong place to look. (4) Peak not on a fixture or load face: the vm peak is a hole rim 6 mm from the loaded face (excluded fixture singularity: fixed hole walls, nodes within 2.5 mm are not read). (5) Converged: layer tension 14.59 → 14.57 → 14.47 (0.7 % last step), shear 2.8 %, vm 3.3 %.

**Second support (bottom face fixed, 2.2 mm):** layer tension at the rims **15.31** MPa, shear 5.75, vm 16.9; displacement 1.17 mm. Higher than the hole-wall support (14.57 at the same size). Reported value is the higher: 15.31.
**Second load (rigid):** `remote` on the bore at the same mesh: hole rims layer tension **9.80**, vm 10.9 (the trap: factor 2.3, a pass); `remote` on the four Ø3.4 walls: 22.5 at the loaded wall itself (rigid coupling artefact, not used), 1.5 clear of it. Higher of the credible ways: the rings.

**Print directions (finest mesh, worst region of each; same solve):**

| Layers along | von Mises (45) | Tension across layers (22.5) | Interlayer shear (13) |
| --- | --- | --- | --- |
| Z (base on bed) | 18.79, factor 2.39 | 14.47 hole rims, factor **1.56** (15.31 with the other support: 1.47) | 7.02 root fillet, factor **1.85** |
| X (on its back) | 18.79, 2.39 | 17.10 base near the first screws, factor **1.32** | 7.03 root fillet, 1.85 |
| Y (on its side) | 18.79, 2.39 | 8.31 hole rims, 2.71 | 6.495 hole rims, **2.0015** (on the line; the Z-layer shear at the same rims is 6.507, 1.998, which `judge()` prints as "factor 2.0" and calls a fail) |

**Verdict: fail.** `judge()` for Z: `fail`, lowest factor 1.56 (tension across layers at the lower small-hole rims), plus shear at the root fillet 1.85 and at the rims 1.998. Von Mises passes at 2.39. Load path: the 150 N goes from the screw heads into the X = 0 face, across the 6 mm upright as bending about Y, down to the root, then as a moment into the plate, which turns about the first screws; the lower holes sit where the section is weakest and the stress is concentrated. Cheapest fix found (T5): print on its side, then thicken the upright.

**Not verified.** The real motor load path (screw preload, friction, the motor's own pilot in the bore). The ring recess steps are 0.3 mm deep and are part of the model, not of the part as drawn. Peak shear at the fillet is on a 45° surface and is a fair reading of the printed layer lines there but I did not slice it.

## T4. The same study on a variant: **fail**

**What I did.** `bracket_build.py` rebuilds the T1 part with the same features and checks, no fillet: `bracket_sharp.SLDPRT` (volume 32,802.3 mm³ = 32,974.0 − 171.7, as hand; one body; no R4 face). Twin with the same rings, same load case, hole walls fixed, an edge mesh control (el/4) along the sharp corner. Then, because a sharp inside corner cannot converge, the same part with the 0.4 mm radius a printed edge has (`T4 R04`: face control el/8).

| Variant | el mm | nodes | corner von Mises | σz on the corner line | mean vm within 0.5 / 1 / 2 mm of (6, 25, 6) |
| --- | --- | --- | --- | --- | --- |
| sharp | 3.0 | 32,188 | 22.79 | −27.3 | 13.19 / 10.15 / 8.58 |
| sharp | 2.2 | 65,250 | 25.98 | −33.1 | 15.92 / 11.43 / 8.69 |
| sharp | 1.6 | 145,669 | 30.00 | −37.5 | 15.15 / 10.80 / 8.64 |
| R0.4 | 3.0 | 44,019 | 38.31 | −34.6 | 15.20 / 13.43 / 11.32 |
| R0.4 | 2.2 | 85,045 | 38.35 | −34.6 | 16.85 / 13.42 / 10.90 |
| R0.4 | 1.6 | 195,072 | 40.41 | −33.4 | 17.29 / 13.82 / 11.63 |

**Judgement.** The sharp corner is a **singularity** (it is the re-entrant corner, compression under +X, σz −27 → −37 MPa, von Mises 22.8 → 26.0 → 30.0: steps 14 % and 15 %, not settling). It is not a stress of the part, and the number to report is not 30. The mean over 2 mm holds at 8.6 MPa across all three meshes: that is the section value, and it matches the hand value (11.0 nominal at the root, lower 2 mm in). With the printed 0.4 mm radius (the edge the part really has) the corner reads **38.3, 38.4, 40.4 MPa**: the last step is 5.4 % after 0.1 %, so it is **not fully settled**, and Kt ≈ 3.5 (hand: nominal 11.0 × Kt for r/t 0.07 about 3.5 = 38). Factor on von Mises 45 / 40.4 = **1.11**: under 2.0. The hole-rim layer tension (14.5 MPa, factor 1.55) is the same as in T3. **Verdict: fail**, on both. The T3 part with its 4 mm radius reads 15.0 at the same place: the radius is worth a factor 2.7 there, which is why the specification has it. `reported_stress_mpa` is the R0.4 value 40.4 (the number I would stand behind); the sharp-mesh peaks are in `convergence_rows`.

**Not verified.** The R0.4 corner: the control on the 0.4 mm round was el/8 (0.375, 0.275, 0.2 mm elements), so 0.2 to 0.375 mm elements on a round that small make 40.4 a lower bound, not a converged value. The R0.4 corner was left at three sizes, 5 % still moving at the finest, 195,072 nodes (the cap is 200,000); a fourth size would have needed a finer control only on the 31 mm² of the round, which I did not try.

## T5. Make it pass: **done** (bracket_c.SLDPRT)

**First attempt, print direction only (no mass).** From the T3 table, layers along Y gives vm 2.39, tension 2.71, shear 2.00: a pass on paper at no mass, but the shear is on the line (2.0015) and the tension at the rims was climbing 11 % at the last step, so `judge()` says `margin, not converged`. Not good enough by itself.

**Change.** The upright thickened from 6 mm to 7.5 mm **on the inner (+X) face** (the outer face, the bore, every hole, and the footprint X 0 to 80, Y 0 to 50, Z 0 to 46 unchanged; mass +7.15 %, 42.05 g against the 43.16 g cap), and R0.4 on the four hole mouths on the inner face (`MOUTH_ROUNDS`, volume −1.5 mm³). Print on its side: **layers stacked along Y** (the L profile lies in the layer plane, so the bending stress and the hole stress concentration run along the layers). Hand: bending stress ∝ 1/t², so 14.5 × (6 / 7.5)² = 9.3 MPa across Z layers; the study read 9.52.

A first build without the mouth rounds (`t5_first.py`) read the shear at the hole mouths on the X = 7.5 face going 3.74, 3.90, 4.47 MPa (growing step, 13.8 % after 5.2 %) and `judge()` said `not shown`. Per 07-done step 6 I gave that edge its printed radius (0.4 mm) and solved again; the peak moved onto the new round (x = 7.1) and settled to 4.49, 4.81, 5.03 (last step 4.7 %).

**Study** (`t5.py mouth`; same load case as T3, hole walls fixed; sizes 3.0, 2.2, 1.6; nodes 27,152 / 57,571 / 133,238):

| Layers along | von Mises (45) | Tension across layers (22.5) | Interlayer shear (13) | `judge()` |
| --- | --- | --- | --- | --- |
| **Y (chosen)** | 16.52 base, factor **2.72** | 5.98 base, **3.76** (hole rims 5.78) | 5.00 hole rims, **2.60** | **pass**, lowest factor 2.60 |
| Z | 16.52, 2.72 | 9.52 hole rims, **2.36** | 6.43 root fillet, **2.02** | pass, lowest 2.02 (thin) |
| X | 16.52, 2.72 | 17.08 base, **1.32** | 6.43, 2.02 | fail |

Second support (bottom face fixed, 2.2 mm): hole rims tension 9.84 across Z, 4.81 across Y, shear 4.02: no worse than the hole-wall support in Y. Reaction 150 N; displacement 2.23 mm. Mass 42.045 g (hand and STL volumes agree: 35,333.25 against 35,331.71). Footprint box 0, 0, 0 to 80, 50, 46; bore centre Y 25.0, Z 28.0 measured; base and small holes unchanged.

**Bore wall** (the 2.8 mm ligament between the Ø22 bore and the small holes, which none of my regions read; read afterwards from the saved nodal results, nodes within 0.5 mm of the bore wall, `bore_wall.py`): on the T3 part, finest mesh, von Mises 9.5 MPa, tension across Z layers 6.4, across Y 5.9, shear 5.5 (X layers); on `bracket_c`, finest mesh, 6.4, 3.9, 3.9, 3.7, all below the hole-rim values and steady over the three meshes. Nothing there governs, so the T5 pass stands.

**The thinnest margin** is the shear in the root fillet at 2.02 if someone prints it base-down: it is not a pass to rely on. **The cheapest improvement** is the orientation (on its side), at no mass. **Not checked:** the motor's real load; buckling is irrelevant (no slender members); the long-term creep of the pressure under the screw heads; whether the part prints on its side (a 50 mm tall print, bore and base holes horizontal, bridging at the bore top).

(`bracket_c.SLDPRT` is the rounded-mouth build; the first build is kept as `bracket_c_first.SLDPRT` in `_wip`.)
## T6. Contact between two bodies: **done, result valid** (38 minutes of the 40; three different models of the pin were run)

**The case.** PETG block X ±20, Y ±15, Z 0 to 20, Ø10.2 hole along Y at X 0, Z 10; Ø10 steel pin, 50 long (Y ±25), 10 mm out each side, **centred**; block bottom fixed; 250 N up (+Z) at each stub. Frictionless no-penetration contact, direct sparse solver. Files in `_wip/sw-eval/sonnet-adv-a/t6c/` (centred, the reported model: `tp_all.SLDPRT` = block plus five inserted bodies) and `t6b/` (the pin seated at the crown); scripts `t6_centred.py`, `t6.py`, post-processing `t6_post2.py`, table `gen_t6.py`.

**Hand calculation.** Mean projected bearing 500 / (10 × 30) = **1.67 MPa** (a floor). Pin in a socket 0.1 mm larger on the radius (Hertz, line contact): R* = 1 / (1/5 − 1/5.1) = 255 mm, E* = 1 / ((1 − 0.28²)/210,000 + (1 − 0.38²)/1,900) = 2,198 MPa, w = 500 / 30 = 16.67 N/mm, half-width b = sqrt(4 w R* / (π E*)) = 1.57 mm, **peak p₀ = 2 w / (π b) = 6.76 MPa** (`hand_bearing_mpa`). The pin must rise 0.100 mm before it bears at all.

**How the pin is held.** Two soft pads (Ø3 × 2 mm discs, E 0.5 MPa, ν 0.45) on the two pin end faces, outer faces fixed, clear of the block; about 0.6 N/mm each in shear by hand (the proof below measured 1.02 N/mm for the two together). The pin is built in three bonded pieces (two 10 mm stubs and a 30 mm centre) so the 250 N `remote` loads sit on the stub cylinders and the contact set takes the centre face alone (the contact set takes whole faces). No other restraint: the pin bears on the hole through contact only.

**Predictions, written before the solve:** nodes 45,000 (actual 86,685 on the 0.8 mm run: 1.9 times, because the 0.8 mm controls on two 950 mm² faces are most of the mesh; my formula covers a global size only, and I should have counted the controlled faces), pin rise 0.10 mm plus a few µm, peak 6.8 MPa on the crown near the block faces, half-width 1.57 mm.

**What I ran, and what each was for.**
1. **Run 1 (centred, `t6_v1_*`): invalid, my mistake.** `contacts=` was never passed. The pin moved 490 mm; pads reacted 99.97 % of the load. Not used.
2. **Run 2 (pin seated at the crown, `t6.py`, `t6b/`):** after run 1 I believed a centred pin with only 0.6 N/mm of pads under a 500 N pull would run away in the solver's first, open-contact step, so I placed the pin 0.100 mm high plus 0.002 mm of overlap so the contact is closed from the start. It works and is kept as a cross-check, but **I had not tested the centred model with the contact set when I wrote that.** A reviewer's challenge made me run it:
3. **Run 3 (centred, contact set present, `t6_centred.py`, `t6c/`): the reported one.** It solves cleanly at 41,136 nodes (43 s) with no excessive-displacement prompt, so the contact solver crosses the 0.1 mm gap by itself and my belief was wrong. The run-2 model is therefore a modelling choice I did not need.

**Studies** (contact faces and pads meshed at the size shown; global 3.0 mm; all direct sparse, Intel Direct Sparse in the benchmark log, 12 to 20 contact iterations). Peak pressure is the radial compression (−σ_rr) on the *block's* hole wall (nodes labelled by geometry and by node-id run, see "Checks"), smoothed over 1 mm and 2 mm; "raw" is the single largest node.

| Model, case | Size mm | Nodes | s | Fz N | Pads Fz N | Pad share | Pin mean uz mm | Peak pressure 1 mm / 2 mm / raw MPa | Half-width mm | Block von Mises, raw max, where |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **centred** | 1.2 | 41,136 | 43 | −500.004 | −0.138 | 0.028 % | 0.1292 | 6.36 / 5.42 / 6.65 | 2.05 | 5.64 at (2.0, −15.0, 16.1) |
| **centred** | 0.8 | 86,564 | 147 | −500.004 | −0.138 | 0.028 % | 0.1291 | 5.99 / 5.21 / 6.61 | 1.98 | 5.12 at (−2.3, 15.0, 15.5) |
| **centred** | 0.6 | 149,971 | 453 | −500.001 | −0.138 | 0.028 % | 0.1292 | **5.79 / 5.03 / 6.27** | 2.08 | **5.22 at (1.7, −15.0, 15.9)** |
| centred, proof | 0.8 | 86,564 | 107 | −0.500 (0.001 load) | −0.102 | 20.4 % | 0.1000 | 0.01 | n/a | 0.04 |
| seated | 1.2 | 40,870 | 35 | −500.0 | −0.035 | 0.007 % | 0.0275 (+0.100 gap) | 6.22 / 5.28 / 10.13 | 2.05 | 6.11 |
| seated | 0.8 | 86,685 | 109 | −500.0 | −0.035 | 0.007 % | 0.0278 | 5.79 / 5.13 / 9.83 | 2.06 | 5.67 |
| seated | 0.6 | 150,090 | 309 | −500.0 | −0.035 | 0.007 % | 0.0278 | 5.48 / 4.97 / 10.65 | 2.08 | 5.77 |
| seated, reversed 0.001 | 0.8 | 86,685 | 165 | +0.500 | +0.206 | 41 % | −0.202 | 0.01 | n/a | 0.03 |

**Results (centred, 0.6 mm, 149,971 nodes).**
- `peak bearing stress on the hole`: **5.8 MPa** (1 mm smoothed; 5.0 over 2 mm; 6.3 at a single node). Hand Hertz 6.76: the finest raw value is 7 % lower and the smoothed one 14 % lower, inside the 20 % band. The contact patch is 2.05 mm half-wide (hand 1.57), because the contact is conformal (b/R about 0.4).
- Where: the pressure sits on the crown of the hole (Z 15.1, X within 0.2 mm of 0), and along Y between about ±10 and ±12 mm in all three meshes (the sign changes with the mesh: the crown is flat to within the node noise).
- `peak_contact_vm`: the largest von Mises in the block near the hole is **5.2 MPa** (smoothed over 1 mm 4.6), at the **edge of the hole where it meets a block face** (1.7, −15.0, 15.9), about 6 mm from the crown, not at the crown. Factor on 45 MPa: 8.6.
- `pin_rise_mm`: **0.129** (0.100 clearance, then 0.029 as the block's hole roof and pin move up together: the pin's mean uz 0.1292, the block crown's 0.0288 beyond that gap, the pin crown's 0.1294: they move together). The hand value covers only the stretch of the side ligaments (0.004 mm). The rest is bending of the 4.9 mm roof and the ovalising of the hole under 500 N, which I did not calculate by hand: **the 0.029 is not explained by a hand value, and I put nothing on it.** The spread of the pin's centre uz (0.086 to 0.174 on the 0.8 mm mesh, 0.126 to 0.134 on the 0.6) shows it tilts a little, as the end pads are soft: harmless; 07-done step 10 about spin applies.
- Reaction: **500.00 N** (499.86 at the block bottom, 0.138 N in the pads).

**Checks.**
1. **Reaction against load:** 500.00 for 500; pad share 0.028 %, under 1 %; the pads' force at 0.1 mm of pin travel is 0.1 N, as the stiffness says.
2. **The contact is a contact, not a bond (05-fea "A body with clearance on both sides": apply a thousandth of the load in the working direction, never reverse).** At 0.5 N up the pin rises **0.1000 mm** (spread 0.0998 to 0.1003): exactly the radial clearance, then bears on the crown with 0.398 N of the 0.5 N, the pads holding 0.102 N. A bond would have moved it about 1e-7 mm. The seated model's reversed proof (the pin travelling 0.199 of 0.202 mm down onto the hole bottom) says the same.
3. **Nodes are in the right body.** The first version of my post-processing selected the hole wall by radius from the axis, which on the seated model (pin 0.002 mm into the crown) put pin nodes in the "block" band: 797 of 8,047 on the 0.8 mm mesh, which made the block's von Mises 30 MPa (the pin's own 31 MPa, steel). Corrected by node-id runs (the mesh numbers each body's nodes in one unbroken run; 05-fea contact rule 5): checked against nodes that are certainly in one body (zero overlap between the runs, zero certain nodes in another body's run, on every mesh). On the centred model the two walls are 0.1 mm apart, so radius alone separates them (zero pin nodes in the band) and the two methods agree. The corrected block von Mises is 5.2 MPa, not 30.
4. **Hand against study:** Hertz 6.76 against 6.27 raw, 5.79 smoothed. A Hertz-shaped patch of p₀ = 5.79 MPa, b = 2.08 mm, L = 30 mm carries (π/2) p₀ b L = 568 N for 500 applied (14 % over) with the 1 mm-smoothed peak, and 493 N with the 2 mm-smoothed (5.03 MPa): the force closes within 1 to 14 %, depending on the smoothing, which is the best the nodal pressure can do.
5. **Mesh:** peak pressure 6.36, 5.99, 5.79 MPa over 41,136, 86,564, 149,971 nodes (steps −5.8 %, −3.3 %, the last under 5 %); pin translation 0.1292, 0.1291, 0.1292; reaction identical. The seated model gives 6.22, 5.79, 5.48 and the same pin rise (0.128): at 0.6 mm the seated model reads 5.48 (5 % lower at 1 mm smoothing, 1 % lower over 2 mm).
6. **The two models agree on the answer;** the seated one is not needed.

**Verdict: valid.** The pressure series is settled by the 5 % rule at the finest step (3.3 %). The raw node values are noisy at 0.6 to 1 mm element size, so the number to quote is the smoothed one.

**Not verified.** (1) Friction (none, which leaves the pad-held lateral freedom larger than a real pin's). (2) The rigid coupling of the loaded stubs, which keeps the pin ends from ovalising and makes the pin stiffer in bending than a real pin with a clevis or rod end. (3) The block-face edge (Y = ±15): the raw pressure on one node there reads −6 MPa (tension) and the von Mises peak sits there, so a feature of 0.5 mm or less would not be seen at this mesh. (4) The 0.029 mm of pin rise on top of the clearance (above). (5) A contact patch edge finer than 0.6 mm.
## T7. Diagnose (no SolidWorks used)

**a. Status table.** PID 20948 is `busy`: someone is meshing, solving or reading a result back, and it will answer again. It is
not hung. PID 2536 is `HALF-CLOSED`: no windows left, not answering, 3.6 GB still committed. It is a dead instance that stalls every launch.
- *What is happening:* one healthy busy instance (leave it) and one dead one, and `launch()` refuses at once and names 2536.
- *Next:* stop and do not launch (README "Stop and hand it up", 01-session.md, and this run's brief). Write down PID 2536, its age (2710 s, no windows) and the line
  `taskkill /PID 2536 /T /F` for Joey, and carry on with whatever task needs no SolidWorks. The keeper is not an obstacle here; 20948 never was.
  Once 2536 is gone, launch with `job(wait_s=1800)`: a new instance starts beside the busy one and waits at the splash only while the oldest instance cannot answer.
- *Must not:* kill 20948 (rule 3, it is another session's running job; `--force` is for the owner), launch while 2536 exists (the new process sits at the splash screen),
  `taskkill` 2536 myself (it is not mine; the playbook says hand it to Joey), wrap anything in `timeout`, or treat 20948 as hung.
- *Playbook conflict, noted:* RULES.md says any session may run `python solidworks/sw_kill.py --dead`, which ends a half-closed instance after
  watching it 20 s. 01-session.md and the README say stop and give Joey the `taskkill` line. This run follows the brief ("HALF-CLOSED means stop and write down the PID").

**b. Error 24 at 796,000 nodes, direct sparse, memory 26 to 12 GB in eleven seconds.** This is out of memory in the factorisation (the log ends at
"GLOBAL-STIFFNESS-MATRIX-DECOMPOSITION-Start"), not a singular model. 05-fea.md: about 800,000 nodes with contact and direct sparse ran out of memory on the 32 GB machine and was reported as error 24;
the fall in free memory while it factorised is the sign.
- *Next:* do not read it as a loose body. Bring the mesh under the cap: coarsen the global size and keep the local controls, shrink the control to the feature that governs,
  cut at a symmetry plane, or run the governing body alone with the loads the full model gave it. Stay under 200,000 nodes for a benchmark (450,000 is the helper's hard ceiling), and take the heavy-solve lock only for a real job over 200,000.
- *Must not:* add restraints or pads to "cure" a singularity, retry the same mesh, go finer, run it beside another large solve, or report any number from it.

**c. STL offset by (41.5, 0, 12.0) on a machine set up last week; native part right.** The export option "do not translate to positive space"
(toggle 71, `swSTLDontTranslateToPositive`) is off on the new machine, so SolidWorks moved the mesh so its minimum corner is at the origin. The offset is the part's negative extent
(04-export.md, 06-judgment.md "STL shifted to positive space on a new machine").
- *Next:* export through `swkit.export()`, which pins the options (69 binary, 71 keep the model frame, 211 mm, 78 fine, 75 AP203) and puts the machine's values back, then check
  `mesh.bounds` against `bbox(d)` within 0.1 mm and rerun the fit check.
- *Must not:* shift the STL by (41.5, 0, 12) by hand, move the mating part, edit the native part, or change SolidWorks' export settings by hand (they are per-user, written to the registry, and shared with Joey's SolidWorks).

**d. Peak 61 MPa on the edge of a fixed face; 38, 47, 61 at 2.0, 1.5, 1.0 mm.** It is a singularity: the steps are growing (24 %, then 30 %), and the peak sits on the edge of a fixture.
It is not a stress of the part, and neither is it a margin. `judge()` calls a growing step `not shown`, whatever the factor.
- *Next:* do not refine further. Support the part a second way (ring under the screw head, a longer fixed face, a bonded washer) or move the fixture away from the edge, and judge the
  part outside a stand-off distance from the edge (read the plateau at 1, 2, 3 and 5 mm), reporting the distance used and the value inside it. Also read averages at 0.5, 1 and 2 mm with their node counts.
  A value that holds over 2 mm is the section; one that recovers within 1 mm on a handful of nodes is the corner. State the verdict as "not shown" until that is done.
- *Must not:* report 61 as a fail or 38 as a pass, quote the finest value, mask the edge away silently, or declare converged.
  Whichever the plateau gives, the requirement is 22.5 MPa (45 / 2); on the three numbers given nothing can be said about it.

**e. Script silent 25 minutes, `--status` shows `busy`, another thread suggests a restart.** Busy means a live client process is driving the instance (mesh, rebuild or a result read-back);
the instance does not answer meanwhile, and that is normal. 400,000-node contact solves take 7 to 11 minutes, and reading back 2.4 M nodes took over an hour.
- *Next:* reply that it is not hung. Look at what is cheap to read: `sw_instance.py --status` (age, committed memory, the client PID and script), `%TEMP%\sw_hidden_<pid>.log` for a hidden dialog,
  and the solver's benchmark log beside the model for the last stage reached. If a dialog is waiting in my own instance, answer it. Wait.
- *Must not:* restart or kill it, `ExitApp` it, kill the python client (that leaves SolidWorks half-closed and stalls every thread), or wrap it in `timeout`. Another thread has no right to stop it either (rule 3).

## Runs that failed before they worked, and why

1. **First `t1_t2.py` write (shell):** a heredoc containing an apostrophe broke the shell command and nothing ran (cause: how I passed the file, not SolidWorks). From then on I wrote files with the file tool. No SolidWorks time lost.
2. **`t3a.py`, run 1 (`t3a_run1_failed.log`):** the first study solved, then my own check `reaction Fx = 150` raised because the reaction is −150 N (it is what the fixtures push back, 05-fea check 1 says "equal and opposite"). My sign error. It cost one launch and 20 s, and the first study's result was lost (re-run in run 2, same numbers: 24,804 nodes, peak 13.96 away from the fixtures). The printed hand tip deflection was also wrong (0.000 mm: I put E in Pa with the lengths in mm); fixed in the same edit.
3. **`t6.py`, run 1 (`t6_v1_centred.log`, `t6_v1_rows.json`), my bug:** I passed the contact faces as mesh controls and **forgot `contacts=`**, so there was no contact set. The study solved, `static()` raised "excessive displacements", my wrapper retried with `loose_ok=True`, and I got pin displacements of 490 mm, 99.97 % of the 500 N reacted by the soft pads, 0 N by the block. It is exactly the failure the pads-share check exists to catch, and it did. Even the 0.001-load case moved the pin 0.4895 mm, through the 0.1 mm clearance, which is what told me the contact set was missing and not that the pin needed stiffer pads. Four solves, six minutes; the result was never used. I took away the wrapper's retry for T6 (`retry=False`).
4. **`t5.py`, run 1 (`t5_first.log`):** it ran clean, but `judge()` returned `not shown` for the hole-mouth shear (step growing, 13.8 % after 5.2 %). That is not a failure of the run; it led to the R0.4 mouth rounds and the second build (`t5b`), which settled.
5. **T6 post-processing, version 1 (not a failed run: a wrong analysis).** I selected the "block's" hole wall by radius, which on the seated model contained pin nodes, and wrote a block von Mises of 30 MPa with an explanation about node noise. The advisor's review spotted it (the block and pin maxima were the same 31 MPa on every mesh); node-id runs fixed it (T6 check 3).
6. **T6 "centred pin runs away" (an untested belief).** I wrote that into the report before testing it; the test was run after the review and the belief was wrong (issue 10 below).
7. Nothing else failed: no HALF-CLOSED instance, no hidden modal dialog, no launch waited more than about 5 s (the keeper was the oldest instance), no 24 error.

## Where the playbook or a helper was wrong, unclear or missing something

1. **RULES.md and 01-session.md disagree** on what to do with a HALF-CLOSED instance: RULES.md lets any session run `sw_kill.py --dead` (ends it after watching it 20 s); 01-session.md and the README say stop and give Joey the `taskkill` line. T7a asks which; I followed the brief.
2. **Files the playbook names that are not in the worktree:** `tools/cad/record_export.py`, `tools/cad/check_cad_layout.py`, `tools/cad/check_sw_refs.py`, `tools/check_file_sizes.py` (04-export.md), `conventions/*.md` (RULES.md and 01-session.md use GitHub links on `roark`, plus `J:\code\roark` in the example `sys.path`; this tree is `cad-daddy`), `eval/loft-blend`, `eval/t3-load-check/CHECK.md`, `eval/fable-d/*`, `EVAL.md`. I did not need any of them to finish; for exports I did the checks of 04-export by hand and did not record the export (no script).
3. **`converge()` is the wrong tool whenever the governing feature sits beside a load.** 07-done step 6 says to follow the governing measure with `converge(..., layers=normal)`; but `converge()` masks nodes within two of the *coarsest* elements of every load face, which on this bracket (rings round the Ø3.4 holes) removes the very rims that govern. 07-done mentions the mask for `r.peak()` but not for `converge()`. I built the series by region myself (`lib3.measures`) and fed `judge()`. A region-reading helper in swfea would save everyone the same work.
4. **`judge()` rounds in its display and compares unrounded:** shear 6.507 against 13 reads "factor 2.0" and the verdict is `fail` (factor 1.998). The log line "fail: ... factor 2.0" looks wrong at a glance. Print three decimals or round before comparing.
5. **`swkit.expect(what, got, want, tol)` treats `0 < tol < 1` as relative**, so `expect(x, 0.07, 0.03)` meant 3 % of 0.07, not an absolute 0.03. The docstring says so; it still caught me once, and every position check of 0.01 mm needs `abs_tol=0.01`. A named `abs_tol=` default of 0 would be less surprising than the overload on the size of `tol`.
6. **The hand-estimate step has no place for a flexible foundation.** 05-fea "Before SolidWorks" and 07-done "Predict, then run" ask for a displacement from the hand estimate; the natural cantilever formula gave 0.31 mm and the study 2.84 mm because the base plate turns between the screws (a 9-fold miss, past the playbook's own "stop at 3 times" line). A line saying "count the compliance of whatever holds the part" would help.
7. **The task text for T3 is ambiguous and the playbook cannot resolve it:** "pulls on the bore with 150 N along +X" with a bore whose axis is X is axial; `'bearing'` is refused, `'normal'` on the bore sums to zero, `'remote'` is rigid. 05-fea covers each case but not "which load for an axial pull". I chose the screw heads on the X = 0 face (an even force on 0.3 mm steps, the twin must stay within 0.1 %) and report the rigid variants beside it. The load faces are then *invented geometry* (the steps), which is a modelling decision the report should state and I have.
8. **T4/T5 want to judge a corner or a hole mouth that is a sharp edge in the model but a 0.2 to 0.4 mm round in print.** 07-done step 6 gives the rule (round it, 0.4 mm if nothing says otherwise) but nothing says how to put controls on a 0.4 mm torus: `ctrl` on the small face (el/8) worked (a round of 31 mm² at 0.2 mm cost 195,000 nodes at the finest global size; the hole mouths at el/6 on top of that).
9. **`static()` cannot tell a free body from a missing contact set.** With `contacts=` forgotten, the helper solved a pin with only soft pads holding it and only the excessive-displacement prompt, answered No, and the `loose_ok` path hid it: 490 mm and a clean-looking reaction of 500 N. `loose_ok=True` on a multi-body study with a contact set should refuse, or `Result` should carry `excessive` louder than a field (it does set it, and `run_case` ignored it). The pad-share check caught it only because I wrote it.
10. **The playbook's contact guidance warns of an open-contact runaway that did not happen here.** 05-fea contact rule 8 (and rule 2) lead you to expect "Excessive displacements" when a body pulled away with only soft pads under it has 0.1 mm to cross. I believed it, and spent two runs on a pin seated against the crown to avoid it. When I finally tested the plain centred model with the contact set present, it solved cleanly in 43 s: no prompt, the pin crossed the gap by itself, with the same answer. The 490 mm run was only the missing contact set. The page should say that a present contact set handles a gap on its own and that the prompt in a contact study means something is not in the set.
11. **No helper separates nodes by body, and geometry fails exactly where it matters.** 05-fea contact rule 5 says to label nodes by geometry, "with a margin at the interfaces". At a contact, nodes of the two bodies are 0.002 to 0.1 mm apart and a radius band mixes them: my first version put 797 pin nodes in the "block" band (8,047) and reported a 30 MPa block von Mises that was the steel pin's. The reliable method is the node-id run (each body's nodes in one unbroken range), which the playbook mentions in a clause. `static()` could return the per-body id ranges (it already reads the component's bodies), and `Result` could take a body argument.
12. **`swkit.stamp` shares one clock per folder:** two jobs running at once interleave their lines in `times.log` and the "minutes" column is a mix; fine for wall times, not for per-task durations. I reported task durations from the stamps by hand.
13. **`insert_body` names:** a body from `tp_pin_c.SLDPRT` is called `SolidBody 3(<tp_pin_c>-<TP_PIN_C>)` and the block `SolidBody 4(HOLE)` (named after its *last feature*). `materials=` keys must match; it worked, but the block being called HOLE would mislead anyone who keys by feature.
14. **A real number worth keeping:** a thicker upright on the inside face lowers the across-layer tension at the lower Ø3.4 holes by (6 / t)² within 3 % (predicted 9.3 MPa, read 9.5 at t = 7.5), and **the bottom-face support reads higher at the holes (15.3 against 14.6) but far lower in the plate (von Mises 1.8 against 17.3 MPa)**: neither support is the conservative one everywhere, so report both.
15. **`--status` says "no claim" beside an instance whose session holds one,** because the claim's path is `j:\code\...` (the `subst` drive) and the instance's is `c:\joe\code\...`; the match is on text. `claims.py list` also shows no PID for a `job()`-per-script session and marks it STALE after the beat interval; a long run needs `claims.py beat`, which I did not do.
16. SolidWorks left `PerformanceLog.txt` in the model folder and, for hidden launches, put several `#32770` windows in `sw_hidden_<pid>.log`, all of them the solver's progress dialog (title = study name); that is harmless and 01-session.md's note about `#32770 | Simulation` is for the *question* dialog. It is hard to tell the two apart from the log without knowing the title; the log should say which is which.

## What I did not verify, across the set

- No physical test, no slice, no print: every verdict is a linear elastic result against the playbook's PETG allowables (45 MPa in plane, 22.5 across layers, 13 shear).
- The T3 load is a modelling decision (screw heads on 0.3 mm steps), not what the specification says word for word (it says "on the bore"); the specification's reading is axial, and I chose not to use the rigid bore load because it hides the failure. Whoever owns the specification should confirm which it meant.
- T6: friction, the real pin ends, the block-face edge, and the 0.029 mm of pin rise beyond the clearance (no hand value).
- T4's 0.4 mm corner is a lower bound (0.2 to 0.375 mm elements, 5 % from settled).
- The bore wall next to the Ø3.4 holes was read from saved results only for the finest three meshes of T3 and T5 (`bore_wall.json`): every value is below the hole-rim values; it was not in `measures()` at the time of the studies.
- `record_export.py`, the layout and size checks, and the committed-CAD steps of 04-export.md were not run (the scripts are not in the worktree, and the brief said not to commit).

## Files (`eval/sonnet-adv-a/`)

`REPORT.md` (this file), `results.json`, `times.log`, `judge_all.json` (every `judge()` return; the T3, T4 and T5 ones are also in `results.json`), `t3_rows.json`, `t4_rows.json`, `t5_rows.json` (first build), `t5b_rows.json` (final build), `t6_rows.json`, `t6_post2.json` (labelled by body; `t6_post.json` is the superseded first version with the wrong mask, kept for the record), `bore_wall.json`, `t6_v1_rows.json` (invalid first T6), scripts `common.py`, `lib3.py`, `bracket_build.py`, `t1_t2.py`, `t3a.py`, `t3b_t4a.py`, `t4b.py`, `t5.py` (run with and without `mouth`), `t5_first.py`, `t6.py` (seated), `t6_centred.py` (the reported T6), `t6_v1_centred.py`, `t6_post.py`, `t6_post2.py`, `gen_t6.py`, `bore_wall.py`, `t_final.py`, `analyze.py`, `finalize.py`; logs `t*.log` (including the failed `t3a_run1_failed.log`, `t6_v1_centred.log`, `t5_first.log`, and `t6_centred_run1.log`); pictures in `pictures/` (`bracket.png`, `bracket_b.png`, `t4_before_after.png` with the T1 part above and the sharp variant below, `t5_before_after.png` with the T1 part above and `bracket_c` below, `t6_model.png`); one line on what I saw in each is in the task sections above.

## Advisor

I called the `advisor` tool **twice**. I am sure of the count. Neither call was stamped in `times.log`, so the clock times are my estimates from the neighbouring stamps and file times, good to a few minutes.

**Call 1: about 17:31 to 17:33 CST, before T1 (start of the whole run).** State: I had read RULES.md, the playbook pages 01 to 07, TASKS.md, the swkit, swfea and sheet code, and checked `--status` and the claims; I had done nothing in SolidWorks yet. I asked nothing specific (the tool takes no arguments). It told me: stamp now and run every SolidWorks script in the background, never under a shell timeout; read `static()` and the selftest examples first; give every feature an `expect_dv`; and, for T3, that the load is axial along the bore (so `'bearing'` is refused and a rigid `'remote'` load on the bore reads low), so use an even force on split rings and read the hole rims myself rather than through `converge()`; hold the 40-minute limit on T6 and judge with `judge()`; T7a: stop and note PID 2536. What I changed because of it: I stamped immediately; wrote the T3 load as 0.3 mm steps round the Ø3.4 holes (a twin part within 0.1 % volume) instead of a rigid bore load; built my own region-by-region series (`lib3.measures`) for `judge()` instead of `converge()`; added the second support, the second load and the three print directions; kept T6 to pads, direct sparse and a thousandth-load proof; and wrote T7a as a stop. It also gave hand values (about 32,974 mm³ for T1) that I recomputed and matched.

**Call 2: about 18:05 to 18:10 CST, after all studies and a full draft of REPORT.md, before close-out.** State: T1 to T6 results in hand, T6 reported as run with the pin seated at the crown, report written and files saved. It told me the work was not done: (1) my T6 block hole-wall mask very likely contained steel pin nodes (block and pin von Mises were the same 31 MPa on every mesh), so split by node-id run and recompute; (2) I had written that a centred pin with a contact set runs away, but had never run it, so test it or reword; (3) the bore wall beside the Ø3.4 holes was read by no region; (4) check the T3 plain-section stress across the full width; plus smaller items (T3 `results.json` mixed two studies, put the `judge()` returns in `results.json`, T2 wording, T4 element-size caveat, report the reasoning-effort tag, fill in times, fix the claim and picture notes). What I changed: I redid the T6 post-processing by node-id run (the block von Mises went from 30 to 5.2 MPa); ran the centred pin with the contact set (it solved cleanly, so my belief was wrong) and then a three-mesh centred series plus a working-direction proof, and made that the reported T6; read the bore wall from saved results (all below the hole rims, T5 pass stands); read the full-width section stress (7.1 against hand 7.5, so check 3 passes); and made the rest of the listed edits.

**Where I did not call it but should have.**
1. **T6 run 1, 490 mm of pin movement and 99.97 % of the load in the pads.** I found the missing contact set myself after a few minutes, but I then built a theory on it (the "open-contact runaway" and the seated-pin model) without asking. A call there would probably have caught the untested belief that call 2 found 20 minutes later and saved two runs.
2. **The T3 first solve, displacement 2.84 mm against my 0.31 mm prediction (9 times, past the stop-at-3 line).** I explained it myself (the plate turns between the screws), which was right, but I did not check that with anyone before reading stresses.
3. **T5, `judge()` returning `not shown` on a growing hole-mouth shear step, and the choice of R0.4 mouth rounds.** It worked, but the choice between rounding, a finer control and a different support was made alone.
4. **Before I wrote the T6 post-processing masks and before I claimed T3 check 3 "passes on the middle strip reading".** Both errors were in analysis, not in the solves, and both were caught only because call 2 happened at the end. A call after the first T6 result would have found the wrong mask earlier.
