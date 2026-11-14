# Haiku runs A and D, with and without plans: independent check

Four benchmark runs by `claude-haiku-5-5` on 2026-11-14, each in its own worktree at base `908f1cc`:

| Run | Set | Inputs | Folder |
| --- | --- | --- | --- |
| haiku-a | A (T1 to T7) | playbook only | [haiku-a/](haiku-a/) |
| haiku-plan-a | A | playbook + plans | [haiku-plan-a/](haiku-plan-a/) |
| haiku-d | D (D1 to D3) | playbook only | [haiku-d/](haiku-d/) |
| haiku-plan-d | D | playbook + plans | [haiku-plan-d/](haiku-plan-d/) |

The plans are in [plans-fable/](plans-fable/) (branch `plan-execute`, `28d1b41`), written without SolidWorks.

The runs report on themselves. This page is what holds up when their files are checked. How it was checked:

- **Models re-measured.** All 57 saved parts were copied and opened in a separate SolidWorks instance; volume, box,
  bodies, feature names and every face (cylinder radius, axis, position, extent) are in
  [haiku-runs-check/measured.json](haiku-runs-check/measured.json), made by
  [measure.py](haiku-runs-check/measure.py). The 24 plates are checked against the task table and an independent hand
  volume by [d3_check.py](haiku-runs-check/d3_check.py), output in [d3_check.txt](haiku-runs-check/d3_check.txt).
- **Studies.** For every study a run claims, the job log (in each run's `wip-logs/` or its own folder) was read for the
  mesh line, the reaction, and the numbers, and compared with `results.json`. Each claimed solve also has its solver
  benchmark file in the run's `_wip` folder, with a matching time.
- **Times and rules.** From file timestamps and from the four session transcripts on the workstation (every command
  each run issued, with its time).

Verdict words: **correct** (done and right), **wrong** (done, result not right), **partial**, **not done**,
**unsupported** (claimed, files do not back it).

## Times

| Run | First action (UTC) | Last action | Wall time | What the report says | SolidWorks time (from logs) |
| --- | --- | --- | --- | --- | --- |
| haiku-a | 09:03:39 | 09:22:56 | **19 min** | "about 20 minutes": right | about 8 min (report says 12) |
| haiku-d | 09:23:19 | 09:44:51 | **21.5 min** | 09:23 to 09:44, tasks 11 + 6 + 4 min: right | about 3 min |
| haiku-plan-a | 19:57:25 | 20:19:22 | **22 min** | "about 1 h 24 min", "16 min of SolidWorks out of 84": **wrong** (13:57 to 14:21 read as 84 minutes; the real end was 14:19) | about 16 min |
| haiku-plan-d | 20:19:42 | 20:40:15 | **20.5 min** | start and end right; `D2.minutes` **75** and "waiting was about 40 min in total": **wrong** (D2 took 12 min, the whole run 20) | about 12 min |

All four ran about 20 minutes against a brief of "about an hour" and task limits of 40 to 90 minutes. Both baseline
runs gave time as the reason for work left undone (haiku-a: T6 pads "not reached within the 40-minute cap" after one
35-second attempt; haiku-d: no D2 study "in the time left", 6 minutes into a 90-minute task). Neither was short of time.

## Set A

| Task | haiku-a (playbook only) | haiku-plan-a (playbook + plans) |
| --- | --- | --- |
| **T1** bracket | **Correct when built**: log shows 32,974.024 mm³ = hand, box 0/0/0/80/50/46, nine holes at the specified places, STL watertight. **The saved file is no longer T1**: T2 saved over it; `bracket.SLDPRT` now measures 31,643.00 mm³ with counterbores and slot. | **Correct.** Re-measured 32,974.024 mm³ (target 32,974.02), box exact, 4 × Ø5.5 at (25,10) (25,40) (65,10) (65,40), bore Ø22 at Y 25 Z 28, 4 × Ø3.4 on Ø31 at 45° steps, R4 fillet, four R5 rounds. |
| **T2** change | **Geometry correct, done the wrong way.** `bracket_b` 31,643.000 mm³ = hand (32,974.024 − 657.378 − 673.646); 4 × Ø10 counterbores Z 3 to 6, slot ends R3 at X 38 and 52, Y 25. But `t2_change.py` calls `save()` twice on the opened `bracket.SLDPRT` before `save_as`, so T1's file was overwritten. The report says "`bracket.SLDPRT` on disk was not saved over": **false**. | **Correct.** Same geometry, 31,643.000 mm³. `save_as` before the first edit; `bracket.SLDPRT` hash unchanged in the log and re-measured at 32,974.024. |
| **T3** study | **Wrong model, verdict right by accident.** The study opened a copy of the overwritten file: its log prints "volume 31643.0" (the T2 part). Six solves ran, reactions 150.00 N, numbers in `results.json` match the log. The remote case gives layer factor 2.17, the known wrong answer of a rigid remote load. The "fail" comes from a second case with 150 N spread over the whole inner face of the upright (17.5 MPa, factor 1.29), not from the motor screws. Peak von Mises sits on a fixed hole rim; no second support. | **Correct.** On the right part (log: bracket body 32,974.02). 150 N through pads on the four motor-screw rims: tension across layers 13.97 / 14.33 / 15.12 MPa at the lower motor-hole rims, **factor 1.49** at 183,846 nodes (true answer about 1.4). Remote load for comparison 13.35 MPa (1.68), washers as second support 14.40 against 14.33. Reactions 150.00 N; σz at Z 12 8.04 against hand 8.0. Says itself that the last step is +5.5 %, so not converged; the fail does not depend on it. |
| **T4** sharp corner | **Wrong.** Built from the overwritten file (31,471.3 = T2 part − fillet; a T1 part without fillet is 32,802.3). Remote load only. `reported_stress_mpa` **31.34** is a value for the singular corner, which must not be given one. Its 0.4 mm radius run (41.1 MPa, converged within 1 %) is the right kind of answer and agrees with the plan run's 40.05, but the report distrusts it as "conflicting". | **Correct.** `bracket_sharp` 32,802.343, `bracket_r04` 32,804.060 re-measured. Sharp corner 20.45 / 28.51 / 37.75 MPa climbing: no value given. R0.4 corner 38.11 / 39.66 / 40.05, last step 1.0 %: reported 40.05 MPa, verdict fail. Flags that the plan's hand estimate (24 MPa) was 67 % low. Leaves out the lowest factor in its own rows: shear between layers at that corner, 22.6 MPa, 0.57. |
| **T5** make it pass | **Not done.** No `bracket_c.SLDPRT`, no design change, no study. "Print on its side" is read off unconverged results of the wrong part. Status "partial" overstates it. | **Partial, close.** `bracket_c` built: two 3.5 mm ribs, 35,693.99 mm³ re-measured, +8.25 % mass, footprint and all nine holes unchanged. Three studies solved (reactions 150.00 N), finest 190,958 nodes: factors 3.60 / 3.02 / 3.24 for layers along Y. Recorded `verdict: "fail"` because von Mises moved +13 % at a sharp rib end: all three factors pass with margin, so "fail" is the wrong word for "pass not yet shown converged". |
| **T6** pin contact | **Not done.** One solve (38,472 nodes) with the pin unrestrained and `loose_ok=True`: 5.08 mm, excessive displacement, correctly called invalid. No pads, no second attempt. Hand value 2.08 MPa uses the wrong formula (projected area gives 1.67, Hertz 6.8). | **Correct numbers, called invalid by its own rule.** Four solves, reactions 500.00 N. Contact pressure 6.52 / 5.96 / 6.77 MPa (true 6.1 to 6.8, Hertz 6.8); pin rise 0.1295 mm (true 0.128); pads carry 0.20 N of 500; a 0.5 N proof run shows contact, not bond. `valid: false` because the three sizes do not converge (+13.6 %) and one plan check window was wrong. Direct sparse solver confirmed in the log. |
| **T7** diagnose | **Mostly right.** b to e right. (a) contradicts itself: "go ahead with the launch" and, for the half-closed instance, "do not launch". | **Correct**, all five. Written from the playbook: the T7 plan was never opened. |

Largest solve: haiku-a 145,560 nodes, haiku-plan-a 190,958. All under 200,000.

## Set D

| Task | haiku-d (playbook only) | haiku-plan-d (playbook + plans) |
| --- | --- | --- |
| **D1** buck mount | **Partial.** Conflict found (60 mm board, 50 mm envelope). Built a standing frame on the rail's front face: 8,820.72 mm³, **10.50 g**, box X ±42.5, Y 10 to 17.5, Z −17 to 43 (re-measured). The board then has 5.9 mm in front of it, not the 14 mm its parts need: with real parts it is about 8 mm outside Y 25. Open area 48.7 % counted with the rail, under the 50 % asked (reported). **The bosses are solid**: no screw holes, so the board cannot be fastened as modelled (reported as "not modelled"). The two M5 screws sit behind the board. Study solved for push and pull along Y: reaction 9.00 N, section stress 4.76 against hand 4.77 MPa, factor 4.19 on an R1 variant. `envelope_ok: false`, honest. | **Done; envelope not met, said so.** Flat frame on top of the rail: 9,949.07 mm³, **11.84 g**, box X ±56, Y **±30**, Z 0 to 9 (re-measured): the mount itself, not only the board, is 5 mm over each side. Four insert holes Ø4 × 6 at (±39, ±26.5), two M5 holes at X ±50 outside the board, so the board lifts out with the mount in place. Tilt checked (no angle fits both limits). Open area 63 %. Study along Z only, three sizes, 2.47 / 2.49 / 2.49 MPa, reaction 9.00 N, factor 18. Small gap: `idea_b.SLDPRT` was saved before its two rails were added (10,352 mm³ on disk against the 21,521 reported; the STL and picture have them). |
| **D2** housing | **Partial: parts only.** Three known specification problems found with numbers (opening 43.5 under inner ring 44.0; insert hole 0.2 mm from the seat; counterbores overlap 1 mm), plus three more. Hand screw load 75 N. Parts re-measured as reported (19,551.37 / 20,279.30 / 2,199.11 mm³). **No study at all**; stopped 6 minutes into a 90-minute task. The fit would not work off a printer: seat Ø51.6 for a Ø52 ring pinches at the split edges and never seats at the crown; opening Ø44.4 leaves 0.2 mm to the turning inner ring with ±0.15 printing; the upper counterbore at Z 7.5 leaves 0.5 mm to the face Z 11. | **Partial: one mesh size.** Same three problems, with numbers, **taken from the plan's table**. Built as planned and re-measured: seat Ø52.2 with each arc offset 0.1 mm so the crown touches, gap 0.8 mm, opening Ø49, screws X ±30 at Z 0 and 7, insert holes 8 deep. Three solves at 160,773 nodes, reactions 300.00 N. +Y: screws 75.2 / 75.1 / 76.7 / 75.8 N, mean **75.7 against 75 by hand**. Bonded twin 50 times stiffer, so contact is proved for +Y; not for +X. A finer mesh came to 224,652 nodes and was refused before solving, so nothing is converged: `valid: false`, honest. **`sf_yield` 9.85, `sf_layer` 25.73, `sf_shear` 9.25 in `results.json` are not the lowest**: its own rows give 7.34 (upper half, +X), 20.94 and 5.82 (lower half, +X); the lower half's 8.77 and 5.82 match the 8.8 and 5.85 of earlier strong runs. `minutes: 75` is wrong (12). |
| **D3** plates | **Correct.** All twelve parts match an independent hand volume to 0.01 mm³; counts, diameters, circles, angles and depths read from the solids. P1 ring B turned 45°, P2 turned 30°, P4 caught before building (holes break out by 3.0 mm, floor 0.4 mm) and built at OD 68 with a 4.0 mm counterbore. Part two by editing (same features plus one chamfer; originals untouched): floors kept at Z 3 / 3 / 4 / 1 / 3 / 3, P3 ring A on Ø70 turned 22.5° (0.3 mm otherwise), chamfer cut to 0.5 mm on P1, P3, P4. Found from its own checks. Two slips: the 0.5 mm chamfer leaves 0.5 mm of flat beside those counterbores, under its own 0.6 mm rule, and `min_wall_mm` for the `_b` plates still says 1.0. | **Correct.** Same twelve results; P4 at OD 68 with a 3.0 mm counterbore (floor Z 2); chamfer 0.4 mm on P1, P3, P4 (0.6 mm left, reported as the thinnest wall). The table problems and the fixes are the plan's; the run executed the plan's table check before building and added none of its own. First build stopped on a tolerance fault in `expect()`; fixed and rerun. |

Largest solve: haiku-d 112,827 nodes, haiku-plan-d 160,773 (the 224,652-node mesh was never solved).

## Rule check, all four

| Rule | haiku-a | haiku-d | haiku-plan-a | haiku-plan-d |
| --- | --- | --- | --- | --- |
| Own SolidWorks instance through `job()`; no attach, no `ExitApp`, no kill | kept | kept | kept | kept |
| Keeper (pid 10172) and other sessions' instances untouched | kept | kept | kept | kept |
| No `timeout` wrapper, no script stopped during a solve | kept | kept | kept | kept |
| Nothing installed, no shared setting changed, `sw_instance.py` unedited | kept | kept | kept | kept |
| Every solve under 200,000 nodes | kept | kept | kept | kept |
| No commit, no push (all four still at `908f1cc`) | kept | kept | kept | kept |
| Claim taken and released | yes | yes | yes | yes |
| Nothing outside its worktree | **broken once** | kept | kept | kept |

haiku-a wrote its first T1 script to `C:\joe\..\..\J\code\...`, which Windows resolves to `C:\J\...`. It then tried
`rm -r /c/J`; the safety check refused. It reported both. What is there now:
`C:\J\code\cad-daddy-wt\sw-eval-haiku-a\eval\haiku-a\t1_bracket.py`, one file of 8,859 bytes written 09:05:32 UTC
(an early draft; it differs from the real script), inside five otherwise empty folders starting at `C:\J`. Nothing
else is in `C:\J`. Left in place.

Not a rule, but worth knowing: haiku-plan-d checked on its running D2 study about 100 times in 9 minutes (a new
wait-loop or log read every 2 to 3 seconds). It stopped nothing.

## The two plan runs: how the plans were used

Checked by comparing each script with the plan's code, the logs with the plan's predicted numbers, and the session
transcripts with the reports.

**Followed.** In both runs the scripts are the plan's code, copied with small edits; `common.py` is identical to the
plan's. In set A no SolidWorks job failed: every call the plans used exists and worked first time. In set D the design
decisions (D1 shape and envelope choice, D2 seat, gap, opening and screw positions, D3 fixes), the six D2 specification
problems and the eight D3 table problems are the plan's text; the executor ran the plan's checks and did not make its own
(D2: plan read 20:24:56, build script written 20:25:29). Its own additions were a tilt sweep and an open-area
measurement in D1. The T7 plan was never opened: T7 was answered from the playbook, and came out right.

**Plan errors, and what the executor did.**

| Task | The plan said | What happened | What the executor did |
| --- | --- | --- | --- |
| T3, T4, T5 | nodes 22,000 / 56,000 / 145,000 and similar | 42,611 / 85,355 / 183,846: 1.3 to 1.9 times over, the finest rows close to the cap | went on (inside the 2× rule), reported it |
| T3 | shear between layers "over 2.5" | 1.83 / 1.82 / 1.79 | reported |
| T4 | R0.4 corner "about 24 MPa (accept 18 to 32)" | 38.1 / 39.7 / 40.05 | no branch for "above 32"; wrote "not explained", marked the task done |
| T5 | printed on its side, the plain bracket passes shear (2.2 to 4) | 1.79 | took the plan's rib branch; correct |
| T6 | ligament force check window 400 to 650 N | 1,053 / 1,430 / 1,820 N, growing with the mesh | "not investigated", marked done |
| T6 | pressure higher at the hole mouths, 7 to 10 MPa | 6.29 / 6.23 / 5.99, lower than mid-length | not remarked on |
| T6 | the solver benchmark file names the solver | it holds timing lines only; the solver is in the macro log line | cited the file anyway |
| D1 | displacement 0.09 mm; shear between layers under 0.6 MPa | 0.158 mm; 0.71 MPa | accepted (inside 3×); the shear miss not mentioned |
| D2 | material key `ring-` | the body is named `<ring>-<RINGBORE>`: the key would match nothing | changed to `ring` before running |
| D2 | `d2_fea.py` imports constants from `d2_build`, which reruns the build | | copied the constants |
| D2 | nodes 55,000 / 110,000 / 190,000 | 160,773 / 224,652 (refused) | checked boxes, reaction and displacement, kept the stresses |
| D2 | if a mesh is refused over the cap: `el=1.9, cs=0.8` | written for the third row; for the second row 1.9 is finer, so it cannot help | stopped (see below) |
| D2 | +X screw load 23.9 N tension, 37.5 N shear (marked untrusted) | 45.1 N tension; shear 11.8, 11.8, 3.8, 3.9 N | redid the statics with the contact angles from the study: 45.3 N |
| D2 | peak at the crown, 5 to 15 MPa; displacement 0.1 mm in every study | peak 4.6 to 6.1 MPa at a counterbore edge; +X displacement 0.555 mm | reported the peak; the 5.5× displacement was never tested, because the compare step returned at the node-count note |
| D2 | STL fit check "must be (0, 0)" | (54, 54) at the crown | traced to STL facets, reported as inconclusive |
| D3 | `expect('hole x', …, 0.03)` | `expect()` is relative for a non-zero target, and the target was 6e-17: the first build stopped at P1 | made the check absolute, reran, reported. The same fault in the plan's box and floor checks was not noticed |
| README | "commit `eval/<run>/` at the end" | the brief forbids it | followed the brief |

**Departures the reports do not mention.**

- T4: the R0.4 rows give shear between layers of 22.6 MPa at the corner, factor **0.57**, the lowest factor in the run.
  It is in `t4_r04.json` and in neither `REPORT.md` nor `results.json`.
- T3: "remote load 13.35 MPa" is a reading at the loaded bore's edge. At the motor-hole rims, where the plan said to
  compare, the remote case reads 9.72 MPa (factor 2.31) against 14.33 for pads: the known wrong answer of a remote
  load, which the run had and did not show.
- T4: the "1.49" layer factor quoted is T3's; T4's own finest row gives 1.57.
- T5: the step-1 script was started alongside the rib job and its output never read; the decision was made from the
  T3 table. Mass came from the plan's volume, not the measured one (they agree).
- T6: "the 40-minute cap was near" as the reason for skipping the plan's fifth study. The task had used about 10
  minutes, and the same report's table says the cap was not reached.
- D2: `clearances_mm` is the plan's table typed in, not measured. The reported upper peak sits 0.02 mm outside the
  exclusion zone; the plan's branch for that (widen to 1.5 mm) was not taken. Two of three D2 pictures were never
  opened. The final message says five D2 studies solved; three did.
- D2: the report lists as plan or helper faults two things that are not: `plane(…, '')` works, and `static()` did
  print the fixture and load boxes.
- D1: the X and Y load directions are hand values only; the report does not say so.

**Where a surprise left it stuck.**

- D2, mesh refused at 224,652 nodes (20:36:23). Fifteen seconds after reading it: "I'll record the D2 results and
  then run D3". Nothing between 3.0 and 2.2 mm was tried, although the refusal message itself says to coarsen, and
  none of the playbook's four ways on. One row only, 13 of 90 minutes used.
- T6, three sizes not converging: the plan's branch (a fifth study) not taken; result declared invalid.
- T4 (40 against 24 MPa) and T6 (ligament force): recorded and left. The plan README says to stop and mark such a
  task partial; both were marked done.
- T5, von Mises +13 % at a sharp rib end: reported "not shown" and recorded as "fail"; a radius and one more run were
  named and not done, with two-thirds of the hour unused.

## What the plans bought, and what they did not

**Bought**

1. **The hard studies ran, first time, on the right model.** T3 loaded through the motor screws and read at the hole
   rims (1.49; the baseline loaded the whole upright face, on the wrong part). T6 held the pin with soft pads and
   landed on 6.5 to 6.8 MPa and 0.1295 mm (the baseline has one invalid solve). D2 got a full contact model, a bonded
   twin and a screw load within 1 % of hand (the baseline has no study). No SolidWorks job failed in set A.
2. **The traps were stepped over.** `save_as` before the first edit kept `bracket.SLDPRT` intact; the baseline
   overwrote it and ran two tasks on the wrong part. The sharp corner was given no value and the R0.4 series was run
   and believed; the baseline produced the same 41 MPa and dismissed it.
3. **Designs that would work.** D2's seat (Ø52.2, crown touching, 0.8 mm gap, opening Ø49) clamps off a real printer;
   the baseline's Ø51.6 seat pinches at the split. D1 has its insert holes and reachable screws; the baseline's
   bosses are solid. T5 has a built part with ribs; the baseline has none.

**Not bought**

1. **Judgment over the numbers once they exist.** T5 recorded as "fail" with factors of 3.0 to 3.6; T6 with the right
   answer called invalid; D2's three headline factors taken from the wrong half and case; the 0.57 factor in T4 left
   out. The plan produced the rows; reading them was still the executor's job, and that is where the errors are.
2. **Persistence and a sense of time.** Each surprise the plan had no working branch for ended the task: the D2 node
   cap after 13 of 90 minutes, T6 convergence, T5's rib end. Reported durations were as wrong with plans as without
   (84 minutes for 22; 75 for 13).
3. **Checking of its own.** Where the plan gave the answer, the executor did not test it (D2 specification problems,
   clearances typed in, D3 table). D3 came out no better than the baseline, which found every table problem itself.
   T7 was right without the plan being opened. Plan numbers that were off (node counts, the T4 corner, the T6
   windows) were noticed only when a check failed, and then recorded, not resolved.


## Playbook and helper problems the runs raise

1. **Editing a saved part into a new file.** The playbook says "save after every step" and nothing about `save_as`
   first. haiku-a followed it and destroyed its T1 file without noticing; T3 and T4 then ran on the wrong part. A line
   in 03-modelling.md ("when the result goes to a new file, `save_as` before the first edit") and a habit of asserting
   the volume of any part a study opens would both have caught it.
2. **Clock arithmetic.** Three of four reports have wrong durations, and the baseline runs stopped early believing
   they were out of time. `swkit.log()` prints local time with no label and `common.minutes()` counts from import.
   A helper that prints elapsed minutes for the run and for the task would take the arithmetic away from the model.
3. **`expect()` tolerance.** Relative when the wanted value is non-zero: a coordinate that should be 0 and comes out
   6e-17 fails. Needs an absolute option (haiku-plan-d).
4. **`new_part()` closes every open document**, not only a failed one; a script holding two parts loses the first
   (haiku-d).
5. **`materials=` keys match body names**, and a body is named after its last feature; the error does not list the
   names (haiku-a `block`, haiku-plan-d `ring-`).
6. **`converge()` exclusion** of twice the largest element size removes a whole 6 mm wall at 3 mm elements (haiku-a).
7. **Node count before solving.** Local controls dominate contact models: 55,000 predicted, 160,773 meshed. A
   mesh-only count before the first solve would let a series be sized to the cap in advance.
8. **Contact convergence under the cap.** The playbook lists four ways on (coarsen the steel, refine only the governing
   feature, symmetry, cut-out). The run tried none and reported "not shown" with 78 minutes of its task left; the
   page could say that "not shown" is for when those have been tried.
9. **A verdict that is neither pass nor fail.** `verdict` takes "pass" or "fail"; a run with every factor above 3 and
   one measure unconverged wrote "fail". The task sheet or 07-done.md needs a third word.
10. Smaller: no way written down to fix part of a planar face; `extrude` reports overlapping sketch circles as "open
    sketch?"; `Result.average()` and `layer_stress()` return tuples the examples do not show; the playbook's worktree
    path still says `J:\code\roark-wt`; a `C:\joe\..\..\J\` path resolves to `C:\J`.
