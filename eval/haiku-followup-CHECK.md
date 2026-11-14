# Independent check of the follow-up round: haiku-plan-a and haiku-plan-d

2026-11-14. Round two of the two plan runs: the same small-model executor was given the review's corrections as
step-by-step instructions ([FOLLOWUP.md for set A](haiku-plan-a-followup/FOLLOWUP.md),
[for set D](haiku-plan-d-followup/FOLLOWUP.md)) and a brief
([A](haiku-plan-a-followup/followup.brief.txt), [D](haiku-plan-d-followup/followup.brief.txt)). What the runs left is in
[haiku-plan-a-followup/](haiku-plan-a-followup/) and [haiku-plan-d-followup/](haiku-plan-d-followup/). This file checks
it without trusting the runs' reports.

How it was checked, all on the CAD workstation:

- [haiku-followup-check/measure.py](haiku-followup-check/measure.py): copies of the models opened in a SolidWorks
  instance of its own; every body, face and feature written to
  [measured.json](haiku-followup-check/measured.json).
- [haiku-followup-check/recompute.py](haiku-followup-check/recompute.py): no SolidWorks. Row files compared with the
  JSON lines in the job logs, every verdict worked out twice (the rule of `judge()` written again from its docstring,
  and the helper itself), and the saved nodal arrays read again for each claim. Output:
  [recompute.txt](haiku-followup-check/recompute.txt).
- File times against `times.log` and the logs' own clock.

## Short answer

Every number in both follow-up reports that I traced comes from a log or a row file and is right, with three small
exceptions (two job lengths in set D, one paper correction in set A that the report says was made and was not, and
set A's REPORT.md, which was left uncorrected). All fifteen new studies solved, their reactions match the loads, and
the saved arrays give the same numbers as the rows. Three of the four open tasks are closed and I agree with each.
The fourth, D2, is reported as "margin, not converged, lowest factor 4.17"; the numbers are right, the label is not,
and neither is the reading of what is climbing: it is the corner of the steel ring pressing on the rim of the seat,
not a stress of the part. One millimetre in from that rim the lower half reads 3.5 MPa von Mises and 0.6 MPa shear,
converged, lowest factor about 13.

## Open tasks before and after round two

| Task | Open after round one (review) | Executor after round two | My verdict | Agree |
| --- | --- | --- | --- | --- |
| T5 ribbed bracket | margin, not converged: factor 3.02, von Mises 3.60 at a sharp rib toe climbing 13 % per step | R2 toes; **pass**, lowest factor 2.99 (layer tension), all three measures converged; 42.48 g, +8.25 % | **pass, 2.99**, for layers along Y (the direction the part is printed in). Part re-measured: as specified | yes |
| T6 pin in hole | valid, but the peak known to 6 %, not 5 % | matched mesh: line mean 6.07 / 5.73 / 5.64 MPa, converged, **valid** | **valid and converged at 5.6 MPa**, which is 17 % under the Hertz value because the contact is wider than Hertz gives. The matched mesh was not what settled it (below) | yes, with that note |
| D1 buck mount | 18.07 on the executor's word (no log); about 8 by hand at the M5 holes | rerun with log: 2.47 / 2.49 / 2.49 MPa converged, **sf_min 18.07**; the hand 5.8 MPa at the M5 hole not seen (1.61); "do not know which is right" | **closed, 18.07 stands.** The study is right; the hand value does not apply to a hole whose wall is held (below) | yes; the open question is answered here |
| D2 split housing | not shown: one mesh, lowest 5.82; where the 0.555 mm is; wrong keys in results.json | six studies under the node cap; **margin, not converged, 4.17**, lower-half shear climbing 20 % and 28 %; 0.555 mm = ring turning 0.86 degrees, harmless; **not closed** | model **valid**; verdict **not shown** on the numbers as read; the climbing entry is a contact-edge peak; away from it **converged, lowest about 13**. Ring turn: supported. Not closed until the edge is dealt with | on the numbers and on "not closed": yes. On the label and the cause: no |
| Paper corrections (R5, R3b) | T3, T4, T5, T6, T7 keys; report times | "done, closed" | T4, T5, T7, D2 keys, D's REPORT: done. T6 `why` sentence: not added, though reported as done. Set A's REPORT.md: not touched (still 84 minutes and 3.24); the correction went into a `review_corrections` key instead | partly |

T3 and T4 stay "fail" (correctly: no rerun was asked for). D3 was not part of round two.

## Times

| | Set A | Set D |
| --- | --- | --- |
| Clock in `times.log`, first stamp to last | 14.0 min (15:22:14 to 15:36:17) | 23.8 min (15:38:20 to 16:02:10) |
| First and last file written by the run | 15:22:01 (`t5_toe.py`) to 15:36:35 (report) | 15:37:49 (`d2_step_a.py`) to 16:02:10 |
| SolidWorks jobs, from each log's first and last line | R1 2.3 min (15:22:13 to 15:24:34); R2b 9.2 min (15:25:21 to 15:34:33) | case X 9.8 min; case Y 10.2 min; D1 1.2 min (16:00:01 to 16:01:08) |
| Share of the clock spent in SolidWorks | 11.5 of 14.0 min | 21.2 of 23.8 min |
| Instruction's estimate | R1 about 3 min, R2b about 8 | R4 about 4 min |
| Limit in the brief | 60 min | 60 min |

- The reported totals are right and were taken from `times.log`, as the brief asked. Round one reported 84 minutes
  for 23; this time the error is gone.
- The clock starts at the first `stamp()`, not when the session starts. Set A's first stamp is inside its first job,
  so the reading and script writing before it are not counted (the round-one folder was frozen at 15:17:02, so at
  most five minutes). Set D's "follow-up start (R3 a)" stamp was written 30 seconds after step R3a had already run.
- Set D's report says the two D2 jobs "ran 10.9 and 10.7 min per times.log". Those are not lengths: 10.9 is the
  clock reading when job X ended. The jobs took 9.8 and 10.2 minutes by their own logs (10.0 and 10.4 between
  stamps). The same wrong figures were appended to set D's REPORT.md.
- Not every follow-up was stamped at start and end as the brief asked: R2a and R5 in set A have no stamps (the report
  says so), and in set D only the jobs do.

## The new model: T5 with rounded rib toes

`bracket_c2.SLDPRT`, opened as a copy:

| | Measured | Expected |
| --- | --- | --- |
| Volume | 35695.1936 mm³ | 35693.99 + 1.20 = 35695.19 (bracket_c measures 35693.9888; the difference is 1.2048, hand 1.2048 for four R2 fillets in a 135 degree corner, 3.5 long) |
| Mass at 1.19 g/cm³ | 42.477 g, +8.25 % on 39.24 g | under +10 % |
| Box | 0, 0, 0 to 80, 50, 46 | same |
| Holes | 4 of R2.75 along Z, 1 of R11 and 4 of R1.7 along X | 4, 1, 4 |
| Toe faces | 4 cylinders of R2.000, axis along Y, each 3.5 long: two on the base (X 33.41 to 34.83, Z 6 to 6.59) and two on the upright (X 6 to 6.59, Z 33.41 to 34.83), at Y 0 to 3.5 and 46.5 to 50 | 4 |
| Bodies, rebuild errors, last feature | 1, none, `RIB_TOE_R` | |

The loaded twin `bracket_c2_ld.SLDPRT` has the same bracket body plus four pads (5 bodies, 35849.13 mm³).

Round two also saved studies back into three round-one models (`block_fea`, `buck_mount`, `housing_fea`). Measured
again, each has the same volume, bodies, features and faces as in the round-one check.

## Each new study: solved, reaction, rows

| Study | Nodes (log) | Mesh rc | Reaction against load | Row file equals the log line | Saved arrays give the row's numbers |
| --- | --- | --- | --- | --- | --- |
| T5_TOE_30 / 22 / 16 | 45,729 / 90,202 / 194,421 | 0 | 150.004 / 150.002 / 150.001 N against 150 | yes, all keys | yes (vm, layer, shear at the stated places) |
| T6M_12 / 08 / 06 | 42,660 / 92,444 / 164,532 | 0 | Fz -499.999 / -499.999 / -500.0 against 500; block -499.80; pads -0.20 | yes, all keys | yes (line mean and node count) |
| D2C_X_12 / 09 / 07 | 122,208 / 151,706 / 195,921 | 0 | 300.0 N along X | the job log holds only node counts, so there is no line to compare | yes: all 18 numbers for layers along Z, the screw tensions and the largest displacement |
| D2C_Y_12 / 09 / 07 | 122,208 / 151,706 / 195,921 | 0 | 300.0 N along Y | as above | yes: all 18, and the tensions |
| D1_Z_20 / 15 / 11 | 30,598 / 58,907 / 125,748 | 0 | 9.0 N | the rows are log lines; there is no row file | yes |

No study was refused; the largest is 2 % under the 200,000 cap. The D1 rerun reproduces round one's typed numbers
exactly (same node counts, 2.47 / 2.49 / 2.49 MPa, 0.158 mm), so round one's D1 figures were real.

## Verdicts recomputed

| Task | Series (coarse to fine) | My rule | Helper `judge()` on the same series | What the executor did |
| --- | --- | --- | --- | --- |
| T5, layers along Y | vm 12.85, 13.25, 13.54; layer 7.28, 7.47, 7.52; shear 3.59, 3.92, 3.98 | pass, lowest 2.99 (layer); last steps 2.2 %, 0.7 %, 1.5 % | identical to the saved `t5_toe_judge.json`, digit for digit | used `judge()`. The call itself was not kept in any script |
| D2, twelve entries | see `recompute.txt` | margin, not converged, lowest 4.17 (lower half, +X, shear) | identical to `results.json` D2.judge | used `judge()`, from `d2_conv_report.py` |
| D1 | vm 2.47, 2.49, 2.49; layer 0.17, 0.13, 0.13; shear 0.70, 0.70, 0.71 | pass, lowest 18.07 (vm) | pass, 18.07 | did **not** call `judge()`; took "converged" from `converge()` and the factor from the instruction's formula. Same answer |
| T6 | line mean 6.068, 5.734, 5.643 (steps -5.5 %, -1.6 %) | converged by the instruction's rule (last step 5 % or less); valid (within 25 % of 6.76) | not a `judge()` case: no allowable | wrote "valid" and "converged" by the instruction's rule, as told |

So: where `judge()` applied and the instruction pointed at it, the executor used it and copied its output; it wrote
no verdict of its own. One verdict (D1) did not go through it.

## The claims

**T5: "pass, lowest factor 2.99, all three measures converged."** True. Notes:
- It is a pass for layers along Y only, which is how T5 says to print it. The same three studies read for layers
  along X give shear 6.51 MPa, factor 1.997 (a fail by a hair), and along Z factor 2.03 not converged.
- The peak von Mises moved to the upright toe, where the R2 face runs out at the rib's side face (6.27, 46.5, 33.83).
  The executor read the instruction's stop rule literally (it names the base, Z 6) and went on. That was the right
  call: the unrounded edges where the rib sides meet the upright and the base read 6.5 and 7.7 MPa von Mises at the
  finest mesh, still rising 5 to 7 % per step but at half the governing stress.
- The largest von Mises in the model, 19.08 MPa, is on a fixed hole wall and is correctly left out.

**T6: matched mesh line mean 6.07 / 5.73 / 5.64 MPa, "converged" and valid.** True by the rules given. Three things
the report does not say:
- The matched mesh was not needed. The same line mean read from round one's arrays (step R2a) is 6.08 / 5.74 / 5.60:
  the same series. Round one "did not converge" because it followed a single-node peak (6.52, 5.96, 6.77); the
  measure changed the answer, not the mesh. Nine of the fourteen minutes went on the rerun.
- It converges to a value 17 % under the hand value, and the reason is in the arrays: the contact is 1.7 to 1.9 mm
  wide each side (hand 1.57). The pressure summed across the strip carries about 475 of the 500 N, so the result is
  consistent with itself; Hertz with the measured width gives 5.6 to 6.3 MPa. The pressure is flat along the hole
  (5.64 at mid length, 5.79 at Y 8 to 12, 5.30 at the mouths).
- "The pin turns or slides on the soft pads; pressure unaffected" is supported. Fitted as a rigid body the pin rises
  0.1295 mm and spins about its own axis by 0.55, 0.30 and 0.05 degrees over the three meshes (1.29 degrees in round
  one's coarsest), with 0.007 mm left over. A round pin spinning in a frictionless hole changes nothing; the line
  mean is the same at 1.29 and 0.55 degrees.

**D1: converged 2.47 / 2.49 / 2.49 MPa, factor 18.07; the hand 5.8 MPa at the M5 spine is not in the study (1.61).
Which is right.** The study, for the model it is. Reasons, from the arrays:
- The hand value takes the spine as a beam built in at the two holes (end moment 44.1 N mm), puts all of that
  moment through the two ligaments beside the hole (1.94 MPa) and multiplies by 3 for an open hole. In the study the
  hole wall is the support. The moment goes into the wall on the side facing the arm; the ligaments beside the hole
  carry 0.55 to 0.62 MPa and the spine beyond the hole 0.1. A factor of 3 belongs to an open hole with the load
  passing it, not to a hole that is held, and in bending it would be nearer 2 in any case.
- Between the arm and the hole the top face reads 0.5 MPa rising to 0.9 at the hole (the beam model gives 1.18 on
  the full section). Off the wall by 0.2 to 0.6 mm the largest von Mises is 1.50 MPa. On the fixed wall itself
  sigma-x is 2.10, 2.31, 2.68 MPa and climbing, as any fixed edge does.
- The 1.61 MPa the executor quotes for "the spine round the M5 holes" is not at a hole. It is at the corner of the
  instruction's box nearest the arm (44.1, 7.1), the tail of the arm-root stress. The instruction's probe was badly
  aimed; the executor reported what it returned and did not look where it was.
- On the real part a screw head clamps the spine and the peak would sit at the edge of the head on the full section:
  1.2 MPa nominal, 2 to 3 with a concentration. So the truth lies between the study's 18 and a cautious 8, far above
  2 either way. The arm root governs in the study and 18.07 is the right `sf_min` for it.
- The executor's "I do not know which is right" was honest and it reported both. It also wrote that the study did
  not check the hand values for X and Y; its own log has the arm-top sigma-y at 1.217 MPa against the hand 1.2.

**D2: "margin, not converged, lowest factor 4.17, lower-half shear still climbing 20 % and 28 % per step."** The
numbers are right. Two things are wrong with the conclusion.

1. The label (next section): with steps that grow, "margin" is not supported.
2. What is climbing. The peak is not in the body of the lower half and not at the split seam, as the report
   guesses. In all three meshes it is on the seat within 0.4 mm of the surface, at Z 6.98, 0.05 and 7.05, 57 to 61
   degrees round from the lower crown: where the ring bears (the contact angle is 56 degrees), exactly level with
   the ring's end faces at Z 0 and 7. The seat is 7.3 wide and the ring 7.0, so the ring's sharp steel corner
   presses into the seat 0.15 mm from its edge. That is an edge-of-contact peak. Read by place at the three meshes:

   | Lower half, case X | vm MPa | Layer MPa | Shear MPa |
   | --- | --- | --- | --- |
   | as the run read it | 5.17, 5.83, 6.49 | 1.04, 1.00, 1.43 | 2.02, 2.43, 3.12 |
   | seat nodes level with the ring's end faces or beyond | 3.92, 4.89, 5.86 | 0.55, 0.95, 1.43 | 1.73, 2.31, 2.86 |
   | seat surface away from its rims (Z 1 to 6) | 3.08, 3.05, 3.01 | 0.30, 0.32, 0.35 | 0.46, 0.45, 0.17 |
   | 1.0 mm or more inside the material | 3.55, 3.61, 3.48 | 0.96, 0.95, 0.98 | 0.61, 0.65, 0.63 |

   The upper half's moving shear in case Y (1.31, 1.40, 1.81) is the same thing on the upper seat's rim (26.10 mm
   from its axis, Z -0.15 or 7.15). Both halves read 1 mm in from the seat and its ends, with the wider zone round
   the screw heads: ten of twelve entries converged, lowest factor 12.93 (von Mises, case X); the two that still
   move are at factors 20 and 66.

   `judge()`'s docstring says not to give it a peak that climbs at a sharp corner. This is one, and the instruction
   that wrote the series did not foresee it. The executor's "not closed" is the right state; the next step is not a
   finer mesh but a 0.4 mm radius or chamfer on the ring's corners (a bearing ring has one) or on the seat rims, and
   the same three studies again.

The first check of the series against round one, the screw tensions (41.3, 39.4, 48.1, 47.7 N; 76.1, 74.3, 75.1,
75.5 N), the contact angles and the wider-zone numbers are all as reported.

**D2: the 0.555 mm is "a harmless rigid turn of the ring by 0.86 degrees".** Supported, more strongly than the
executor showed, and with one correction.
- The executor's fit left "0.53 mm at a few nodes". Those nodes are not ring. Its body split calls every node with
  radius up to 26.0005 "ring"; the seats touch the ring at the two crowns, so 222 seat nodes within 2.5 mm of a crown
  are counted as ring (390 and 666 on the finer meshes). The mesh numbers each body's nodes in one block, which
  separates them exactly. On the ring body alone: translation (0.135, 0.070) mm, turn 0.888 degrees, residual
  **0.0002 mm**. The 0.5548 mm node moves 0.5547 by the rigid motion. It is a rigid turn and nothing else.
- The turn is not a property of the part. It is 0.89 degrees on the 3.0 mm mesh and 1.29, 1.22, 1.50 degrees on the
  series (largest displacement 0.735, 0.703, 0.831 mm), while the ring's translation stays at 0.134 to 0.135 mm,
  the halves at 0.201 and 0.053 mm and the screw tensions within 0.3 N. A frictionless ring has nothing but the soft
  pads to stop it spinning; in case Y it does not turn at all. Harmless, yes; "0.86 degrees", no.
- The misfiled seat nodes carry at most 0.92 MPa, so no reported stress is affected.
- The instruction's test was "tangential mean near 0.5 mm"; the executor got 0.38, did a rigid fit of its own, wrote
  down the decision and went on. Good judgement, and the right answer.

## The judge() question

Is a series whose steps are growing "margin, not converged"? No. On the governing entry `judge()` should say
"not shown".

`judge()` takes a moving entry as rising twice more by the share it moved at the last step. That is fair in two
cases, and its docstring names both: a peak that is settling (the next steps are smaller) and a sharp corner, where
each refinement adds about the same share. For 2.02, 2.43, 3.12 the steps are 20 % and 28 %: neither case. The
assumption "same-size steps" is contradicted by the series itself. How much the answer depends on it:

| How the next two steps are taken | Value after two more | Factor |
| --- | --- | --- |
| as `judge()` does: 28 % twice | 5.14 MPa | 2.53 |
| the increase keeps growing by the same amount (0.41, 0.69, then 0.97, 1.25) | 5.34 MPa | 2.43 |
| the step keeps growing by the same ratio (20, 28, then 40, 56 %) | 6.79 MPa | 1.92 |

The margin over 2.0 is thinner than the difference between ways of extending the series, and one of them is under
2.0. Three numbers with growing steps do not establish a rate, so nothing can be projected from them.

The rule I would use, and why (the helper is not changed):

- **"margin, not converged" only when the last step is no larger than the step before.** Then the series is level
  (a corner) or shrinking (settling), and two more steps of the last size is a fair or a cautious reading.
- **A rising entry whose last step is larger than the one before is "not shown", whatever its factor,** and the
  log line says "steps growing" and where the peak is. Growing steps mean the mesh has only just begun to see
  something: a peak moving onto an edge, or a contact edge being resolved. The next action is to look at where it is,
  which is what "not shown" asks for; "margin" lets the report move on.
- To keep small stresses from tripping it: count an entry as settled when its last change is small against what is
  allowed, not only against itself, for example under 5 % of limit / need (0.33 MPa for shear, 0.56 for layer
  tension, 1.1 for von Mises). In D2 that settles five of the seven moving entries (among them the layer entries
  that moved 21 % and 43 % at factors 32 and 16) and leaves two, both shear, both with growing steps, at factors
  4.17 and 7.18: the two contact-edge peaks.

Effect on what exists: D2 becomes "not shown", which is also the review's round-one verdict for it. The playbook's
own worked example of margin (07-done.md: 10.68, 11.06, 12.51 MPa, steps 3.6 % and 13.1 %) has growing steps too and
would become "not shown". That was the sharp rib toe of T5; the action ordered for it was the same either way
(round it and solve again), and it then passed.

Two further limits of `judge()` that D2 shows: it cannot tell that an entry is an edge-of-contact peak (it is told
not to be given one, and nothing checks), and the instruction's hand rule that the brief set against it has no
"not shown" outcome at all, so brief and instruction could not disagree here.

## The follow-up instructions, one by one

| Step | State | What happened |
| --- | --- | --- |
| R1 (T5 toes) | **followed as written** | Script built from steps 1 to 4 as given; all `must` and `expect` checks passed; no fallback needed (194,421 nodes). Verdict from `judge()` instead of step 6's hand rule: same answer. Step 6 asked for both steps in percent and each peak's place: the report gives the last step only and the von Mises place only (the rest is in the row file). Stop rule read correctly. Mass done |
| R2a (T6 read) | **followed as written**; script not kept | Numbers reproduce from the arrays (6.08 / 5.74 / 5.60 on 27 / 81 / 192 nodes, half-width 1.88, peak on the pin end). The expected 6.0 to 6.8 was met only on the coarsest mesh; reported, not examined. Decision sentence written as told |
| R2b (T6 matched mesh) | **followed as written** | One line changed, saved model opened, three studies, the four checks on each row, `valid` and "converged" kept apart. No fallback needed |
| R3a (D2, where the 0.555 mm is) | **followed, with a step of its own** | The instruction's threshold did not fit (0.38 against "near 0.5"); it added a rigid fit, decided, recorded it. The fit's leftover was a fault in the body split it was told to reuse |
| R3b (D2 keys) | **followed as written** | By a small script. After R3c it replaced `governing` with the `judge()` line and set `valid` true, both reasonable |
| R3c (D2 series) | **followed, with four departures** | (1) Predicted nodes: 130,000 written for all three rows, not 130 / 165 / 200 thousand. (2) `compare()` was dropped from the copied `one_c`, so no prediction was checked; the case Y job carried case X's 0.55 mm prediction (got 0.094). (3) The "first check, before anything else" was made after all three X studies had run, not after the first; it passed, so nothing was lost. (4) The fallbacks for a refused row were not coded: `one_c` catches any error, logs "REFUSED" and goes on. None was needed. Everything else as written: controls, faces and counts, screw node check, both checks, the wider zone, the table, `judge()` |
| R4 (D1 with log) | **followed as written** | Five lines added, log kept, three items reported, "which governs" said. It overwrote round one's D1 arrays and solver files, as the instruction made unavoidable, without remark |
| R5 (paper) | **partly** | Done: T4 notes, T5 notes and keys, T7, D2 keys, set D's REPORT.md. Not done: T6 `why` sentence (the old "Check 3 failed: lig_force" text is still there; the report says the sentence was added); set A's REPORT.md (the two corrections were put in `results.json` under `review_corrections` and in the follow-up report) |

The problems found in the instructions before the run, and what the executor did at each (brief against
instructions is split into its two halves here):

| Problem | What happened |
| --- | --- |
| `job()` writes no log file | The executor redirected each script's output into `wip-logs/` itself, three different ways (two logs start with a byte order mark, one has an empty `.err` beside it). All five jobs and the three no-SolidWorks steps of set D have logs. Not logged: the D2 rows (the copied `one_c` logs node counts only), the R2a read and the T5 `judge()` call |
| R4 overwrites round one's `_wip` | It did: `D1_Z_*.npz`, the solver files and a re-save of `buck_mount.SLDPRT`. Nothing was lost: the rerun gives round one's numbers exactly and the part measures the same. The executor did not notice or mention it |
| Brief against instructions on verdicts | The executor followed the brief (`judge()`) and still reported what the instruction's rule asked for. They gave the same result both times, so the conflict never bit. D1 got no `judge()` call |
| Brief against instructions on time | Times were taken from `times.log`; stamps were set at jobs, not at every follow-up. Both sets finished in a quarter and four tenths of the limit |
| Two jobs from one script (R3c) | One script taking `X`, `Y` or `report` on the command line, one `job()` per run of it. A sound reading of "one script, one job" |
| The missing selftest case | The worktrees had `judge()` and `stamp()` but a `selftest.py` without the `verdict` case that 02-com.md cites. The executor used both helpers correctly from the docstrings and 07-done.md; no trace of trouble |
| The R1 node cap | 194,421 nodes against 200,000 (2.8 % under), and D2's finest 195,921 (2.0 % under). Neither fallback was needed, by a small margin. T5's fallback was coded (it matches on the words in the error text); D2's was not |

## What explicit next-step instructions bought, and what they did not

Bought:
- **Everything was tried, in order, with no stop.** Round one stopped D2 at 13 of 90 minutes when a mesh was refused.
  Round two ran fifteen studies in five jobs in 38 minutes of clock for both sets.
- **Three of four open tasks closed, correctly.** T5 passes, T6 is valid and settled, D1's numbers are now on record.
  D2 went from one mesh to a six-study series under the cap, which round one could not get to.
- **No number invented or mistyped.** Every stress, factor, node count, tension and angle I traced matches a log
  or the arrays. Round one's D1 numbers, typed without a log, turn out to have been real.
- **No verdict of its own.** With `judge()` named in the brief, it used it and copied the output; D2 was reported
  as not closed and nothing was dressed up as a pass.
- **Honest about what did not fit**: the 6.0 to 6.8 expectation that was missed, the 0.38 that was not 0.5, the hand
  value the study does not show. Each is written down.

Did not buy:
- **Nothing past the instruction.** Where a result needed looking at, it was reported and left: where D2's climbing
  peak is (guessed at "the split seam"; it is on the seat rim under the ring's corner), where D1's 1.61 MPa is (not
  at a hole), why T6 settles 17 % low, why the rigid fit left 0.53 mm.
- **The instruction's own mistakes were carried out faithfully.** The matched mesh that was not needed, the badly
  aimed D1 box, the overwritten round-one files, a series that fed `judge()` a contact-edge peak.
- **Checks that the copy step dropped stayed dropped.** `compare()` vanished from the D2 series and nothing
  flagged it; a prediction of 0.55 mm stood beside a result of 0.094.
- **Paper work was the least reliable part.** Two of the paper corrections were not made as written, one of them
  reported as made; two job lengths were misread from the clock file.

In one line: step-by-step instructions turned the small model into a dependable pair of hands for runs someone else
has thought through, at about 15 to 25 minutes a set; they did not make it see what the instruction's author had
not seen.

## Rule check

- Each job ran in its own SolidWorks through `swkit.job()`: PIDs 122608, 123876 (set A) and 118908, 121796, 115444
  (set D), each with a "closing pid" line. `sw_instance.py --status` afterwards shows only the keeper instance.
- One `with job()` per script run, three studies per job (the limit is four), every mesh under 200,000 nodes, the
  two sets one after the other, so these runs never had more than one solve going.
- No claim left in `pc/claims.py list`. Nothing committed or pushed in either worktree (both still at `908f1cc`).
- The frozen `eval/<run>-round1/` folders are identical to what was collected after round one.
- No `timeout` wrapper in any script. Whether one was used on a command line cannot be seen from the files.
- This check: its own instance twice (PIDs 123248 and 9488), copies only, claim taken and released, both closed.

## Playbook and helper problems raised

1. **`judge()` calls a series with growing steps "margin".** See above; the worked example in 07-done.md is such a
   series.
2. **Nothing masks the edge of a contact.** `Result.away()` leaves out fixture and load faces only. A steel corner
   on a printed seat climbs like a fixed edge and went straight into a verdict. 07-done.md step 6 (round the edge)
   should name contact pairs: give the harder part's corner its real radius, or read 1 mm in.
3. **A body split by radius fails where two bodies touch.** The D2 split (from the plan, under 05-fea.md contact
   rule 5) files 222 to 666 seat nodes as ring. Harmless to the stresses here, but it spoiled the one reading that
   used the ring's nodes. The mesh numbers each body's nodes in one block, so a helper could return which body a
   node belongs to; `Result` has nothing for it.
4. **A round body in frictionless contact spins freely, and the spin is the "largest displacement".** T6's pin
   (1.29 degrees down to 0.05) and D2's ring (0.9 to 1.5 degrees). `predict()` and `compare()` on the largest
   displacement then check nothing: D2 predicted 0.55 and got 0.70 to 0.83 while the part moved 0.2. Compare a named
   body's translation, or restrain the spin.
5. **`job()` keeps no log.** Whether a run can be audited depends on the session remembering to redirect, and Windows
   PowerShell adds a byte order mark when it does.
6. **`stamp()`**: the clock starts at the first call, so reading and setup go uncounted, and its running-total
   column was read as job lengths.
7. **`selftest.py` in the worktrees had no `verdict` case** although the playbook page they were given cites it: the
   helpers were copied in without their test.
8. **A row function copied "with one change" can lose its checks.** `one_c` lost `compare()` and the full row log.
   An instruction that says "copy X and change only Y" needs a line saying what must still be there afterwards.
