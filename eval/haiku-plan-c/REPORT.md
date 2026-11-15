# haiku-plan-c, set C (design sense)

Run `haiku-plan-c`, worktree `J:\code\cad-daddy-wt\sw-eval-haiku-plan-c`, plan from `eval/plans-fable-c`.
Clock from `times.log`: set start 20:02:46, set end 20:54:23 (51.6 min). Model id and reasoning effort are
given in the coordinator message, not in this file (repo rule: no model identifiers in committed artifacts).

Files: `results.json`, `fea_rows.json`, `DESIGN.md`, `restate.md`, `times.log`, `pictures/`, scripts as copied from
`eval/plans-fable-c` with `common.py` edited in two places (see "Changes to the plan's code"). `REPORT_all_runs_appended.md`
is the raw append from every script run, including the reruns and the superseded STEM_A and STEM_A2/STEM_A3 results.
`backup_STEM_A/` and `backup_STEM_A2/` hold the earlier `results.json`, `fea_rows.json`, `REPORT.md` and `DESIGN.md`.

## Task states

| Task | State | Proof |
| --- | --- | --- |
| C1 | done | `results.json` C1: volume 219436.0 mm3 against 219436.0 by hand; one body; all checks in `c1_boxy.py` passed; STL watertight, one shell, volume 219351.8 mm3 (-0.04 %). Mass 261.1 g. |
| C2 | **not done: requirement not met** (gate item "requirement met" false) | Fixed items all ok (33 STL items, every solid measurement). One body, watertight, one shell. Mass 116.4 g, below 261.1 g. Verdict from `judge()`: **fail**, lowest factor 1.58 at "+Y, layer" at the neck (Z -32). Three neck variants tried (STEM_A, STEM_A2, STEM_A3); none reaches 2.0. See "What is open". |

## Times (from `times.log`)

| Stage | Clock | Minutes |
| --- | --- | --- |
| C1 (script, 2 SolidWorks cuts and features, export, picture) | 20:02:46 to 20:03:14 | 0.5 |
| C2 restate, copied from the plan | 20:03:29 to 20:03:30 | 0.1 |
| C2 stage 1, ideas (final run, after two B fallbacks) | 20:09:31 to 20:11:34 | 2.1 |
| C2 stage 2, detail (final A2 run) | 20:44:51 to 20:45:38 | 0.8 |
| C2 stage 3, FEA (final A2 run, 10 studies in 4 instances) | 20:45:39 to 20:54:18 | 8.7 |
| C2 stage 4, finish | 20:54:19 to 20:54:23 | 0.1 |
| C2 total including all reruns and the STEM_A, STEM_A2 and STEM_A3 studies | 20:03:29 to 20:54:23 | 50.9 |

Waiting against working: I did not time the SolidWorks launches separately. The launches took about 7 s each
(for example `pid 198968` at 20:03:43, `pid 198308` at 20:02:54). The 10 FEA studies took about 9 minutes of
wall time for the first run (20:15:05 to 20:24:14); the solves themselves are in `fea_rows.json` as `solve_s`
(24 to 81 s each, growing with mesh). Almost all of the 50 minutes was SolidWorks meshing and solving, and the
remainder was my own reading and editing. No launch waited behind another session's instance during this run.

## C1. The link as it is

- Model `_wip/sw-eval/haiku-plan-c/link_boxy.SLDPRT`, one body, rebuild clean. Picture `pictures/c1_boxy.png`.
- Volume 219436.0 mm3 against 219436.0 by hand. Mass 261.1 g at 1.19 g/cm3.
- Box -35 to 35, -22 to 22, -215 to 35, against the design. Six Ø3.4 on the Ø50 circle, Ø30 bore, two Ø8 pin holes
  at X 0, Z -200, cheeks 6.0 mm thick, all measured on the solid.
- STL watertight, 1 shell, volume 219351.8 mm3, 1632 triangles, box as designed.
- Shape numbers: flat_share 0.91, largest_flat 0.144, sharp_per_area 12.3.
- What I see in `pictures/c1_boxy.png`: a round elbow disc with six screw holes, a square beam, and a flat fork of two
  cheeks with a pin hole, all square-edged and boxy, as drawn.
- What I would question: the beam's top sits 3 mm into the disc rim (counted once, 457.7 mm3); the cheeks are given
  from Z -170, where the block already is, so 10 mm of each is the block.

## C2. Make it more organic

### Restatement
`restate.md` is the planner's restatement, copied before any modelling and stamped at 20:03:30.

### Stage 1, shape: ideas and checkpoint 1
- Idea A "bone" (STEM_A table, loft `arcs4`, stem first): built as one body, 98909 mm3 stem, form 101041 mm3 after
  the slot, mass 120.2 g, hand beam factors 3.61 (load Y) and 7.97 (load X). Shape: flat_share 0.247, sharp_per_area
  3.94. Eligible.
- Idea B "open frame" (STEM_B table with the window): **did not build**. The planner's stem volume (97800 mm3) did not
  match the loft (88379 mm3 in the last loft try), so the plan's branch set `STEM_VOL` and `FORM_VOL` to the measured
  values. Then the window cut split the stem into separate bodies at Z -56 to -70 ("expected one body"). The plan's
  second fallback (window endpoints at Z -38 and -126) did not change that. Result: B has no picture and no mass.
  The task asks for two ideas each with a picture; **that part of the task is not met**. The choice rule chose A on
  the hand factors (B 0.89 against 2.5 required), not on B's form.
- Checkpoint 1: 0.6 min after "C2 start" on the first run (inside the 20 minute limit). `pictures/checkpoint_01.png`
  is idea A, crude.
- What I see in `pictures/idea_a.png`: one stem that flares into a round elbow hub, pinches to a waist, and widens into
  a two-pronged fork with a round knuckle at the wrist; reads as one bone.
- What I see in idea_b.png: no picture, because idea B did not build.
- Chosen: **A, STEM_A** (rule: only A eligible). The table was then changed to STEM_A2 and STEM_A3 later (see stage 3).

### Stage 2, detail: link_organic, fixed items, exports
Final model: table **STEM_A2** (loft `arcs4`, stem first, `arc_flip` 1). Stem 101543 mm3, hub 21814 mm3, knuckle
11748 mm3, slot removed 31448 mm3, pin holes 523, cable tunnel 4895, screw holes 436, screw-head clearances 16.1,
below the mounting plane 0.0. Volume 97787 mm3, mass **116.37 g** against 261.13 g for the boxy link. One body, rebuild
clean, STL watertight, one shell. STEP in mm.

- Hub seam blend: `RAMP_BLEND` at R3 built on 1 edge but was undone (volume change -0.4 mm3, not a sound solid). So the
  stem leaves the hub's screw-side face as a crease of about 30 degrees, not a blend. I did not try R2 or R1.2 because
  the first radius ended the blend try.
- Fixed items on the solid: mounting face one flat face at Y -4, area against the ring by hand; Ø30 bore; six Ø3.4
  screw holes on the bolt circle, each Y -4 to +4; two Ø8 pin holes at X 0, Z -200, cheek 6.0 mm; inner cheek faces
  flat at Y ±16 covering Ø16 round the pin; cable tunnel face. All inside tolerance.
- Fixed items on the STL by sampling: **all 33 items ok** (`fixed_items_ok` true).
- Print orientation as the plan: lying on its +Y side, layers along Y.
- What I see in `pictures/checkpoint_02.png`: the hub and stem read as one form with a crease at the hub's screw side,
  the waist, the widening fork and the arch; the screw-side scallops are visible on the hub.
- Still missing against the request at this stage: the study, and the before-and-after sheet.

### Stage 3, study: three load cases, three meshes
Held: the mounting face. 60 N at the wrist. +X and -X as bearing loads on the two pin holes; +Y as an even pressure on the
inner face of the +Y cheek (a bearing load cannot take a force along the pin). The +Y rigid load was run as the second
way at 3.0 mm. Layers along Y. Peaks read at least 3.0 mm from held and loaded faces.

Final model (STEM_A2), from `fea_rows.json`:

| Case | el mm | Nodes | von Mises MPa | Across layers MPa | Between layers MPa | Max disp mm |
| --- | --- | --- | --- | --- | --- | --- |
| +X | 4.0 / 3.0 / 2.3 | 82002 / 116027 / 173186 | 16.5 / 17.2 / 17.4 | 3.07 / 3.51 / 3.25 | 2.22 / 2.33 / 2.50 | 4.5 / 4.5 / 4.5 |
| -X | 4.0 / 3.0 / 2.3 | 82002 / 116027 / 173186 | 16.5 / 17.2 / 17.4 | 3.18 / 3.42 / 3.19 | 2.22 / 2.33 / 2.50 | 4.5 / 4.5 / 4.5 |
| +Y (pressure) | 4.0 / 3.0 / 2.3 | 82002 / 116027 / 173186 | 16.3 / 17.2 / 17.2 | **14.07 / 14.04 / 14.21** | 7.64 / 7.42 / 7.53 | 8.0 / 8.0 / 8.0 |
| +Y rigid (second way) | 3.0 | 116027 | 17.7 | 14.3 | 7.6 | 6.8 |

- Reaction equals the load in every study (within 0.01 N). -X against +X on von Mises: 0.0 % apart.
- Verdict from `judge()` at need 2.0: **fail**. Lowest factor **1.58**, "+Y, layer", peak at about [3.2, -0.4, -32.1], the
  neck. Next: "+Y, shear" 1.73. The von Mises entries pass at 2.61 (+Y), 2.58 (+X and -X).
- Factors from `results.json`: yield 2.55, across layers 1.56, between layers 1.70 (lowest of the three cases; for +Y the
  higher of pressure and rigid). Rigid over pressure: 1.02 on each measure, so the load model does not change the answer.
- Lowest factor read for the other print directions, same results: layers along X 2.38, along Y (chosen) 1.58, along Z
  1.20. **Layers along X would pass the 2.0 gate on this study**, and layers along Y would not. I did not change the print
  direction, because the plan fixed Y and the direction is a design choice for Joey to make; I am reporting the number.
- The plan expected across-layer and between-layer factors "above 4". They are not: the +Y bending puts about 14 MPa of
  tension across layers at the neck. That is the place the plan's expectation was wrong.
- Mesh convergence: +Y across-layer reads 14.07, 14.04, 14.21 MPa (last step +1.2 %). `judge()` settled it as a fail at
  1.58; the verdict would have been "margin, not converged" only if the factor were above 2.0.
- The study ran at the expected node counts within 2x, but the counts were higher than the plan's predictions
  (82 k, 116 k, 173 k against 60 k, 80 k, 125 k) and the +Y displacement was 8.0 mm against the plan's 4.5 mm hand value
  (1.8 times, within the 3x limit). The plan's displacement hand value is 2.5 mm for X against 4.5 mm measured.

### Stage 4, result
| Gate | |
| --- | --- |
| Fixed items intact | true (33 of 33 on the STL, solid measurements in `results.json`) |
| One body, watertight | true |
| Factor at least 2.0 on all three measures, three cases | **false**: 1.58 across layers at +Y (the neck) |
| Mass not above the boxy link | true (116.4 g against 261.1 g) |

Shape numbers: before sharp_per_area 12.3, flat_share 0.91; after sharp_per_area 5.14, flat_share 0.21.

- What I see in `pictures/c2_before_after.png` (both STLs, one scale): the boxy link as square plates and a block;
  the organic link as a single continuous stem with a waist, a round hub and a round knuckle.
- Thinnest margin: the neck across layers for +Y. At factor 2.0 the wrist would carry 60 × 1.58 / 2.0 = 47 N in +Y.
- Cheapest improvement found: print direction. Layers along X (2.38) read from the same results, at no mass.
- Not checked: buckling of the stem, a loose pin (a bearing load covers half the hole), screw preload on the 8 mm hub,
  the 0.8 mm skins over the cable tunnel in print, fatigue, and whether the motor body leaves room for the stem below
  Y -4 outside Ø62.

## What is open
1. C2's strength requirement is not met. Three neck variants were tried (`STEM_A` 1.54, `STEM_A2` 1.58, `STEM_A3`
   1.44 on shear). They are one approach (the same stem, thicker in Y), so the plan's rule for "blocked" (three different
   tries) is not met. The honest state is "not met, with the neck as the cause"; the untried kind of change is a print
   direction (layers along X reads 2.38) or a material, both of which are design calls.
2. Idea B did not build, so the "two ideas, each with a picture" requirement is not met.
3. The hub seam crease at the screw side was not blended (R3 built and was undone). Not tried at R2 or R1.2.
4. DESIGN.md was edited by hand for two lines (idea B's mass and the blend text) because the script wrote "None g" and
   "tried at R3, R2 and R1.2" for them; the numbers and the design are otherwise as the script wrote them.

## Failures before it worked, and why
- C2 stage 1, idea B, first run: "nothing built the form in 5 tries": the stem volume check against the planner's 97800
  mm3 (loft gave 88379). Fixed by the plan's branch (measured STEM_B volumes). Then the window cut split the stem (the
  "expected one body" failure); the plan's endpoint fallback did not change it.
- C2 stage 1, idea B: the `STEM_VOL`/`FORM_VOL` edit was rejected once because I had not read `common.py` first, so the
  first rerun used the old values. The next run used them.
- C2 stage 3: STEM_A verdict "fail" (1.54), STEM_A2 "fail" (1.58), STEM_A3 "fail" (1.44; shear, and the +Y layer entry
  flagged as growing, "the mark of a sharp edge or a contact edge").
- The plan's `checkpoint_01` and the detail-stage geometry checks passed on every run; no run needed a branch in the
  detail stage except the blend.

## Where the plan or a helper was wrong, unclear or missing
1. `c2_ideas.py` B path: the stem volume table value (`STEM_VOL['STEM_B']` 97800) did not match the loft in any mode;
   the branch for "every try fails only at stem volume within 12 %" was the right one, and it needed the measured value.
2. The plan expected across-layer and between-layer factors above 4 for +Y. They were 1.56 and 1.70 at the neck.
3. The plan's FEA node predictions were low by about 1.4 times (82 k against 60 k at 4 mm, 116 k against 80 k at 3 mm,
   173 k against 125 k at 2.3 mm). The check in `compare()` passed, so nothing stopped; the prediction should be recalibrated.
5. `c2_finish.py` appends to `REPORT.md` every run, so reruns stack sections. This file is the cleaned version;
   the raw append is in `REPORT_all_runs_appended.md`.
6. `c2_finish.py` writes `DESIGN.md` from the run; the idea B line says "None g" when B did not build, and the blend line
   says "tried at R3, R2 and R1.2" when the blend loop stops after the first radius that builds or is undone. Both edited by hand.
7. `c2_finish.py` reads the "gate" from results; with a failed verdict the status is "not done: see gate", which is right.
8. Nothing in the playbook or helpers was wrong about SolidWorks itself. The launch/solve wait behaviour in RULES.md
   matched what I saw (no waits, solves 24 to 81 s).

## Changes to the plan's code
- `common.py`, `STEM_VOL['STEM_B']` 97800.0 changed to 88379.1 (measured loft volume, branch "planner number is off").
- `common.py`, `FORM_VOL['STEM_B']` 78400.0 changed to 68979.1 (same difference carried through).
- `common.py`, `WINDOW_B` first and last points changed to (0, -38) and (0, -126) (the plan's second fallback for B).
  The change did not make B build; it is kept as the plan's fallback.
- `put('C2', table_name=...)` used to move between STEM_A, STEM_A2 and STEM_A3 (the plan's branch for the neck).
  The final design is STEM_A2.

## Standing items
- Nothing committed or pushed (per the brief). The `_wip` models and exports are gitignored.
- SolidWorks: each script closed its own instance on the way out. The keeper (pid 10172) is the machine's, not mine.
- Claim `sw-eval-haiku-plan-c` is released at the end of this run (see the last line of this file).
