# Review of the Opus-planned runs: haiku-oplan-a (T1 to T7) and haiku-oplan-d (D1 to D3)

Method. No SolidWorks here, and no part was opened again. These runs committed their scripts, row files and
reports but **no job logs** (they stayed in the gitignored `_wip` folder on the machine), so unlike
[haiku-plan-REVIEW.md](haiku-plan-REVIEW.md) the rows cannot be compared with what the solver logged. What was
done: every volume worked again by hand, every verdict worked again from the committed rows against the
allowables (von Mises 45, tension across layers 22.5, shear between layers 13 MPa, factor 2.0), the reports
compared with `results.json`, and set D compared with the grading key.

Verdict words: pass; fail; margin, not converged; not shown.

## Set A

| Task | Reviewed verdict | Agrees with the run? |
| --- | --- | --- |
| T1 | pass | yes |
| T2 | pass | yes |
| T3 | fail, right, with two checks left open | yes |
| T4 | fail, right; one solve broke the node rule | yes |
| T5 | **not shown** | **no: the run says pass** |
| T6 | not started | yes |
| T7 | right on all five | yes |

**T1.** 80·50·6 + 6·50·40 + 171.68 − 2·64.38 − 570.20 − 2280.80 − 217.90 = 32974.02 mm³; reported 32974.02.
Motor holes at 25 ± 10.96 and 28 ± 10.96, as reported. STL +0.05 %. The 2.8 mm between the bore and each motor
hole is in the report this time.

**T2.** 32974.02 − 657.38 (counterbores) − 673.65 (slot) = 31642.99; reported 31643.00. The one failed check was
the run's own (the centre of a half-cylinder's box is not the arc's centre) and it said so.

**T3.** Verdict fail on tension across Z layers at the lower motor-screw holes: 17.75, 17.99, 17.88 MPa over
three sizes (last step 0.6 %), factor 22.5 / 17.88 = 1.26. The independent check of this bracket
([t3-load-check](t3-load-check/CHECK.md)) gives 1.4: same verdict, same place. Reaction 150.0 N. Left open by the
run and still open: the plain section reads 9.54 against 8.00 by hand (150·16 / 300), 19 % high on 14 nodes; and
the rigid load on the four screw holes reads 28 to 30 MPa on layers where the plan said it would read low. The
earlier finding on this part is that a rigid load **stiffens** the wall round small holes; a reading 60 % higher
at the holes it is tied to is most likely stress at the tied hole edges, which is the plan's error to have
called it the low reading and the run's to let it "govern" unexamined. It does not change the verdict.
Not said in the verdict: the run's own table shows shear between Y layers at 7.8 MPa, factor 13 / 7.8 = **1.67**,
so printing on its side fails too. It quotes only the tension factor (2.88) for that direction.

**T4.** Sharp corner 23.2, 27.5, 31.7 MPa: climbing, as it should. R0.4 corner 35.05, 36.35, 36.17: last step
0.5 %. Judged on the radius a printed corner has, and the part fails on the holes as in T3. Right. The 1.5 mm
solve on the R0.4 part had 247,510 nodes against the 200,000 rule; the run reported it itself.

**T5. Not shown, not pass.** The chosen design (upright 7.5 mm, printed on its side) rests on **one mesh** (1.75 mm)
read for Y layers: tension 10.92 MPa under the rigid load, factor 2.06; shear 5.80, factor 2.24. On the unchanged
part the same two measures moved +10.9 % (tension) and +7.7 % (shear) at the last step. Two more steps at those
rates: tension 10.92 · 1.109² = 13.4 MPa, factor **1.68**; shear 5.80 · 1.077² = 6.73, factor **1.93**. So the
margin is inside what the mesh has not settled, and by the playbook's rule that is "not shown". The run's
caveat says exactly this and then writes pass. Mass 35333.25 · 1.19e-3 = 42.05 g, +7.15 %: right. Supports for
the side print were not looked at.

**T6.** Not started; 35 of the 70 minutes went to waiting for the heavy-solve lock behind another thread, which a
mesh of 200,454 nodes took by 454 nodes.

**T7.** All five answers match the pages: busy left alone and the half-closed PID handed up; out of memory, not a
loose body; toggle 71; a singularity read at a distance and supported a second way; busy is not hung.

**Set A count: 5 right of 6 reached of 7** (T1, T2, T3, T4, T7). The run's own count was the same once its T5
pass is not accepted, which the metrics file already did.

## Set D

**D3. Right.** All twelve volumes worked again here from the table and the changes the run made, with the chamfer
as a ring of π·c²·(R − c/3):

| Plate | Part one, hand | reported | Part two, hand | reported | Chamfer | Thinnest wall after |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | 17728.67 | 17728.67 | 22040.22 | 22040.22 | 0.4 | 0.6 |
| P2 | 23947.18 | 23947.18 | 29648.45 | 29648.45 | 1.0 | 6.0 |
| P3 | 38698.26 | 38698.26 | 45765.78 | 45765.78 | 0.4 | 0.6 |
| P4 (OD 68, counterbore 4.0) | 13596.26 | 13596.26 | 17596.27 | 17596.27 | 0.4 | 0.6 |
| P5 | 62864.78 | 62864.78 | 74259.20 | 74259.20 | 1.0 | 1.5 |
| P6 | 20848.86 | 20848.86 | 25865.43 | 25865.43 | 1.0 | 1.0 |

Against the key: P1's ring turned (found, 45 degrees, wall 3.02); P2's rings coincide (found by reading the
table, since the wall check skips zero distance; turned 30 degrees); P4 breaks out of its disc and leaves a
0.4 mm floor (both found; built on a 68 disc with a 1.0 floor, said plainly); in part two P3's new ring A sits
0.3 mm from the counterbores (found, turned 22.5 degrees) and the 1 mm chamfer meets the counterbores on P1 and
P3 (found, and on the widened P4; 0.4 used). Floors held from the bottom. **Every item in the key, before
anything was built wrong.** Its one slip, exporting before saving so the first part files were empty, it found,
fixed and reported.

**D2. Margin, not converged; contact proved.** The three problems in the key are all found with numbers and
built round: shoulder Ø46.0 (key: 44.5 to 47.5), screws moved out to X ±31.0, screws spread to Z −0.2 and 7.2.
Contact is proved the way the playbook asks: a bonded twin moves the ring 0.0018 mm against 0.041 with contact,
bonded screws carry 2.3 N against 69 to 77. Screw load along Y: sum 295 N against 300, 75 by hand each: inside
15 %. Along X: 46 to 48 N against 37 by hand, 27 % off and not explained (the plan called its own value low
confidence). Lower half von Mises 11.90 at 3.0 / 1.5 and 10.44 at 2.5 / 1.0: the report calls this "climbing";
it **fell** 12 % with the finer mesh. Two sizes do not show convergence either way; factor 45 / 11.90 = 3.8 at
worst, and it would need to nearly double. Not done: the crown check and the print-direction tables for Y and X.
Nineteen minutes went to two hidden message boxes.

**D1. Pass on load with margin; partial as delivered.** The envelope cannot be met by any mount (the board is
60 wide against Y ±25, 60 tall against Z 45), found and assumed, as the earlier run did. The board comes out by
four M3 screws from above with the mount on the rail. Highest stress over all solves 1.49 MPa (even pull),
factor 45 / 1.49 = 30; the peak at the standoff root climbs 9 % a step and would need twenty times that to
matter. The spine check failed in sign as well as size: an upward load on the arms puts the top of the spine in
compression, so the plan's +0.61 MPa has the wrong sign; the run guessed that and did not settle it. Open area
(59 %) is a hand value, not measured on the STL. 15.67 g against 11.84 g for the mount built from the other
plan.

**Set D count: 1 right of 3 reached of 3** (D3), with D1 and D2 both passes on margin whose proofs were not
finished.

## What this changes

1. The counts in the metrics files stand (5 / 6 / 7 and 1 / 3 / 3); their basis is now this review, not the
   runs' own reports. No part was re-measured on SolidWorks, and with no logs committed the rows themselves are
   taken as the runs wrote them.
2. A verdict written as "pass" beside a caveat that says it is not shown (T5) is the same fault the earlier Haiku
   run had in the other direction ("fail" beside passing factors). The verdict word should come from
   `swfea.judge()` on the rows, never from prose.
3. Three of the four "not explained" lines trace to hand numbers in the plans (the load model said to read low,
   the spine sign, the screw load along X). The executor checked itself against them faithfully; it cannot
   repair them.
4. Keep the job logs with the run. Without them a review can check arithmetic and judgement, not the solver.
