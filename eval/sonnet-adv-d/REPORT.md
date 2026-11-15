# REPORT: benchmark run sonnet-adv-d (set D, stress)

Model: claude-sonnet-5-5. Reasoning effort: not told to me by the harness (default). Start 18:28:55, last SolidWorks job ended 19:39:19; report written after. Clock from `times.log` and `date`. No commit, no push (the brief wins over the task file's "committed pictures"). Pictures are in `pictures/`.

## Status per task
- **D1: done**, envelope not met on purpose: the specification cannot be met (Y -25..25 cannot hold the 60 x 18.6 board section at any tilt); gave up Y by 5.0 mm each side.
- **D2: done**; valid for a snug joint in the split-closed state; first 12 studies INVALID, rerun valid; judge `margin, not converged`, lowest factor 4.58 (sf_yield 6.4, sf_layer 3.1, sf_shear 4.6).
- **D3: done**; one script, six plates, table problems caught before building, part two by editing.

## Times (times.log)
| Task | Stamped | Waiting | Working |
| --- | --- | --- | --- |
| D1 | 11.9 min (18:44:18-18:56:13) plus about 10 min of envelope arithmetic before the first stamp | about 3.5 min for solves (6-140 s each); launches about 5 s (keeper) | the rest: arithmetic, design, scripts, pictures |
| D2 | 40.9 min (18:56:13-19:37:09) | about 23 min for solves (51k-100k node contact solves 26-110 s each; the invalid series a and c cost about 14 min of it) plus about 5 min for the stuck dialog and the rerun queue | about 13 min: spec arithmetic, build, analysis |
| D3 | 2.2 min run time (19:37:09-19:39:19) | none | the scripts (d3_table, d3_build, d3_edit) were written during D2's solves, so their writing sits inside D2's stamp; true D3 cost about 12 min |
I never waited for another session's instance. All three budgets (60/90/60) were far from used. I did not spend the spare time on more, which is a choice: D1's mass could have been halved, D2 could have run a preload case.

## Runs that failed, and why
- D1 v1: bridge arms 1 mm above the bed (to give the study a fixture face) would need supports; rebuilt flush (d1b) with the rail as a bonded aluminium slab in the study. The first slab (full rail) made the 1.5 mm mesh 296,000 nodes: refused by `static()`; slab cut to 120 x 20 x 6. Two pick errors (rail bottom Z).
- D2 build: wrong `expect_dv` for the pin thread (my hand number).
- D2 first solve: 73,206 nodes against my predicted 28,600 (2.6x) and displacement 0.225 against predicted 0.06 (3.7x). Playbook says stop and explain first. Causes I found before reading stresses: 18,000 nodes sit in pins, pads and ring; I forgot the 6 mm wall over the seat bends.
- **D2 invalid runs (tags a and c, 12 studies):** each half's split face is two patches (the opening cuts it at X -23..23); my `pick(at=(30,0,3.5))` took one and I `expect`ed 1, so the -X patches stayed bonded. I explained the symptoms (screws 88/92/16/20 on a mirror-symmetric model, identical over three meshes; sum 216 for a 300 N load) as physics until the advisor named the pick. Rerun as tag d with 2 patches per half: symmetric 91/95/90/95.
- Two jobs on one model file at once (c chain and d chain on pair_fe2): the second opened it read-only; a hidden dialog "A sharing violation occurred while accessing an unnamed file" blocked instance 178676; I pressed OK on that dialog (my own instance); it then died with "remote procedure call failed" in CreateMesh; another job lost its save (error 3). `sw_kill.py --list` afterwards shows only the keeper. Cost about 6 min.
- D3 part two first run: sketch name `RING_A_SK_SK` (Sk appends `_SK`): P1_b, P2_b built, P3 failed; I deleted my own P*_b files and reran all (log `d3_edit_run1_failed.log`).

## D1. A need, not a drawing: the 12 V buck board mount

**Status: done, with one requirement given up (envelope Y) and said so.** Files: `_wip/sw-eval/sonnet-adv-d/d1b/buck_mount.SLDPRT`, `.step`, `.stl` (the version of record; `d1/` holds the first version, see "Runs that failed"); `restate.md` first (five lines, the arithmetic that shows the specification cannot all be met, assumptions, nine questions each with the assumed answer).

**The decision that shaped everything.** Seen along X the board with its parts is a 60 x 18.6 mm rectangle (3 + 1.6 + 14). `d1_tilt_scan.py` searched every tilt and position for the allowed region (Y -25..25, Z up to 45, outside the rail): least overshoot 5.0 mm flat, 2.8 mm at 45 degrees (which then dips 11 mm beside the rail and runs the under-parts into the rail), 2.0 mm on edge (which needs 18.6 mm beside the rail where 15 are allowed). Even the bare board lying flat is 60 mm against 50. Nearest thing that works: the board lies flat, Y limit given up by 5.0 mm each side (Y -30..30), Z has 21 mm to spare. Cost of the other choice: tilting 45 degrees saves 2.2 mm of Y and costs a leg hanging beside the rail and a pinch where the board plane passes the rail corner. `envelope_ok` is **false** and the report says why, not true.

**Two ideas that differ in kind** (pictures `pictures/d1_idea_A_flat_bridge.png`, `pictures/d1_idea_B_tilted_cradle.png`, crude boxes, not SolidWorks):
A (built): flat board on two bridges and four M3 screws into heat-set inserts; screws all reached straight from above. B (sketched only): board tilted 45 degrees in two grooves, slides out along X, held by one latch; no board screws at all but needs grooves printed to +-0.15, a leg beside the rail, and 66 mm of height. A was chosen because every driver path is vertical and the board comes out by four screws. Picture of B: the board is drawn tilted between two end blocks with the groove bars along its long edges; it is a crude box sketch and the grooves and latch are not dimensioned.

**Design.** One printed part, 18.72 g, 15,727 mm3: a 116 x 20 x 4 base on the rail top, two 8 x 60 x 8 bridges under the board ends (Y -30..30), four Ø7 pads 3.5 tall (Ø4.0 x 6 insert holes). Board bottom at Z 11.5, parts to Z 27.1. Everything measured on the finished solid: hole centres within 0.001 mm, volume 15,727.12 against hand 15,727.12, box exact, STL watertight one shell 15,726.9 mm3, STEP in mm. The first build had the bridge arms 1 mm above the bed (to give the study a fixture face); I saw at the print step that they would need supports and rebuilt with the arms flush (`d1b`).

| Item | Value |
| --- | --- |
| parts / fasteners | 1 printed part; 4 x M3x6 SHCS (2.5 mm hex) into 4 M3 inserts; 2 x M5x10 button head (3 mm hex) into 2 M5 T-nuts |
| board out, step by step | (1) power off, unplug the wire pairs at the board; (2) 2.5 mm hex key straight down, undo the 4 M3x6; (3) lift the board straight up; the mount and its 2 M5 stay on the rail. Fit: reverse, snug by feel |
| reach (checked with `sheet.inside` on the STLs, stand-in board and rail in place) | M3 key column r 3 above each head, Z 17..45: 0 of 756 points inside any solid, all four; M5 key column r 6 at X +-52: 0 of 756; board with its 14 mm parts lifting straight up Z 11.6..60: 0 of 3,276 points inside the mount; under-parts zone: only the four pads, 0 points elsewhere; wire exit region +X: 0 of 1,664. The M5 column stands 3.5 mm clear of the board's parts box in X |
| open area | top face 0.99; underside 0.82 counting only the two 7.5 mm bridge strips, **0.55** counting the base strip under the board as a shadow too (worst case, reported as `open_area_share`) |
| envelope | mount and board Y -30..30, Z 0..27.1; specification Y -25..25: **not met, 5.0 mm each side** |

**Hand check of the 9 N case at the weakest section.** 10 g of 90 g = 9 N; 2.25 N per pad. Weakest section: a bridge arm where it leaves the rail edge (Y 10), 8 wide x 8 tall: M = 2.25 x (26.5 - 10) = 37.1 N.mm, S = 8 x 8^2 / 6 = 85.3 mm3, sigma = 0.43 MPa; at Y 11.5 (where the surface nodes can be read) 0.40 MPa. Second weakest: a pad Ø7/Ø4 (I = 105 mm4) under 2.25 N sideways at 3.5 mm: 0.26 MPa. Insert pull-out at 2.25 N is two orders under what a heat-set insert holds in PETG (not tested here).

**The study** (`d1b_fea.py`, `d1b_lateral.py`; model `buck_mount_fea2.SLDPRT` = the mount plus a 120 x 20 x 6 mm aluminium slab standing for the rail, bonded where they touch, the slab's bottom fixed; the load on the four pad tops (where the board bears), not one rigid load). I predicted 11-80 k nodes, 0.01 mm and a peak at the arm root near 0.6 MPa before each solve. Results, first mesh to finest (3.0 / 2.0 / 1.5 mm, 20.7 k / 58 k / 118 k nodes), 9 N down: von Mises away from the rail edge 0.355 / 0.359 / 0.361 MPa (hand 0.40 at that point, 10 % under), layer tension 0.17 / 0.13 / 0.13, shear 0.068 / 0.079 / 0.079; reaction 9.00 N; displacement 0.0123..0.0126 mm (predicted 0.01); `judge()`: pass, lowest factor 124 (von Mises). Same load with the two M5 hole walls fixed instead: 0.359 MPa, 0.0128 mm, identical. Sideways 9 N (Y and X, through the four insert holes as bearing loads, 2.0 and 1.5 mm): 0.39 to 0.45 MPa away from the holes and **0.93 to 1.06 MPa at the insert-hole wall, still rising 14 % between the two meshes** (a bearing-load edge). Reaction 9.00 N in every case. All three measures in all print directions are two orders under the allowables. `sf_min` = 45 / 1.06 = **42** (von Mises at the insert hole, lateral X), with 22.5 / 0.32 = 70 on layer tension and 13 / 0.157 = 83 on shear: the part is far stiffer than the load needs, which is a finding for mass (see below), not a margin to celebrate.

**Print.** Base down on the bed, Z up, 0.2 mm layers, four walls; no supports: the arms sit on the bed, pads and insert holes are vertical. Layers lie across the pad screws; at 2.25 N that is not a governing load. Slicing was not run (no slicer call made), so time and material are an estimate: 15.7 cm3 of PETG, about 40 minutes.

**Cheapest improvement (not built).** Stress is 1 MPa against 45: the bridges could be half as tall (4 mm) and the base 3 mm, cutting mass from 18.7 g to about 12 g; the base strip and wire exit then need re-checking. A 2 mm zip-tie slot in the +X base end would give strain relief (not asked, not designed).

**What I did not check.** The T-nut and slot dimensions (from memory), whether the wires fit over the M5 head at +X (they pass above it, the head is 2.75 mm tall), insert pull-out, the board's real hole positions against a drawing, any print.

**Weakest point (mine):** the envelope is not met; and the study is over-resolved for a part this lightly loaded.

**Corrected after review:** M3 screws were first M3x10; through the 1.6 mm board that is 8.4 mm into a 6 mm hole (bottoms out, never clamps): M3x6. The M5 is x10 not x12 (slot depth from memory).

**Pictures, one line each:** idea A: flat board on two cross bridges over the rail; idea B: tilted board between two end blocks; buck_mount sheet: a flat strip with two cross bridges and four pads, arms flush; assembly sheet: board on four pads over the mount, the rail with its slot below, two M5 holes outside the board ends.


## D2. Two halves round a bearing
Files `_wip/sw-eval/sonnet-adv-d/d2/housing_upper.SLDPRT`, `housing_lower.SLDPRT`, `ring.SLDPRT` (+ `.stl`, `.step`), sheets `pictures/d2_housing_upper_sheet.png`, `d2_housing_lower_sheet.png`, `d2_pair_sheet.png`. Numbers in `results.json`, `d2_spec.json`, `d2_checks_results.json`, `d2_results_calc_d.json`.

**Pictures, one line each:** upper sheet: a block with a half-bore trough, two Ø6 counterbores per end on the Y+32 face with a thin rib between them, shoulder lips as a stepped groove. Lower sheet: the trough seen from the split face with four insert holes, and two M4 holes on the mounting face. Pair sheet: two blocks forming one 72 x 64 slab split along Y 0 with the Ø52 bore, a thin gap line and screw ends on one face (the ring is inside the seat, hidden).

**Specification problems (what, number, built):** shoulder opening Ø43.5 under the Ø44.0 inner ring (0.25 mm overlap) -> Ø46; screws at X 28.2 leave 0.5 / 0.2 mm of wall to the seat -> X 31 (3.3 / 3.0); counterbores at Z 1 and 6 overlap by 1.0 mm -> Z 0 and 7; seat 7.0 line to line -> 7.3; zero split gap cannot clamp at +-0.15 -> 0.15 relief per half (gap 0.30); 6 mm insert hole vs M3x35 reaching 6.5 mm -> 7 mm; no dowel between the halves (noted).

**Fit.** The ring stops the halves from closing once clamped, so the clamp is the closing travel (0.30 mm minus what the ring takes), not print tolerance. STL checks: inner ring region and a 0.5 mm margin sweep: 0 points inside the housings; with the split closed the upper seat pole sits at Y 25.8 against the ring pole 26.0.

**Hand values.** +Y: 300 N / 4 = 75 N each. +X first estimate: cosine pressure gives a separating force F/pi = 95.5 N, 23.9 N per screw.

**The study.** `pair_fe2.SLDPRT`: 11 bodies: two halves, steel ring Ø51.9 with 0.4 chamfers, four steel pins for screw+insert, four soft pads; 51,793 / 74,551 / 100,690 nodes; direct sparse; no-penetration contact on ring-seat and on both patches of the split; bearing load 300 N on the ring bore; lower half held on Y -32.
| | +Y | +X |
| --- | --- | --- |
| screw tension, 3.0 mm (N) | 90.7 94.9 90.4 94.9 (sum 371) | 39.2 40.8 26.0 26.1 (sum 132) |
| sum at 4.0 / 2.4 mm | 371.4 / 370.9 | 132.3 / 132.5 |
| hand | 75 each | 23.9 each |
| bonded twin screws | -14 each | 18.5 19.2 -0.8 -1.2 |
| largest displacement contact / bonded (mm) | 0.232 / 0.0348 | 0.254 / 0.068 |
| unloaded-side gap | lower seat 0.13 mm | -X side 0.20 mm |

Differences from hand. +Y is 21-27 % high: screw tension = ring push + split compression; sections just above and below the split read -69 N, and 371 = 300 + 71. That prying exists only in the split-closed twin: in the clamped joint the faces stay apart by what the ring takes, so the real service load is nearer 75 N plus preload. +X: 132 N of tension against 110 N of split compression leaves about 22 N of ring push, so the first hand value was wrong in kind; the screws mostly carry prying from the upper half sliding 0.2 mm in X on a frictionless split. I first tried F tan 21 degrees (114 N) and dropped it when the section balance disagreed.

**Contact proof.** Bonded twin: ring moves 12.6x less (0.0111 vs 0.140 mm) for +Y, largest displacement 6.7x less; the unloaded lower seat opens 0.13-0.14 mm while the loaded arc is closed; reaction 300.0 N; section force through the lower half 295 N (-1.7 %); pads carry 0.17-0.19 N (0.06 %). The section method reads within 2 % for +Y but 11-19 % off for +X (shear over a thin slab): rough there.

**Factors** (split face up, layers along Y, both halves, both cases, three meshes, `judge()`): verdict `margin, not converged`, lowest factor 4.58 (lower half +X interlayer shear 2.87 MPa). Von Mises 7.07 MPa (6.4); layer tension 3.8 MPa (5.9) in the plain section but **7.2 MPa (3.1) at the counterbore floor corner, which is sf_layer** (6.6/7.2/7.1 over meshes; 2.7 MPa at 0.5 mm in; about 1 MPa from 1 mm). Other print directions: Z up 3.82 `not shown`, X up 3.77 `not shown`; Y up is best and needs no support. The entry that keeps it from `pass` falls 34 % at the last step (upper half +X layer, 2.26, 1.94, 1.28). Counting the seat edge at the split plane (contact edge, left out 1 mm round by default) the peak is 9.4 MPa von Mises (4.8) and rises with the mesh: `not shown` for that edge. Pad-recess surroundings (twin only) were left out of every reading; counterbore walls and ribs read 6.2-7.2 MPa von Mises, insert surrounds 2.9-7.2.

**Not covered.** Snug joint, split-closed twin; no preload (head bearing limit 196 N per screw, keep snug preload under about 100 N on top of 95 N service; no torque, snug by feel); the saved parts have 0.15 mm relief per half, a Ø52 ring without chamfers, real screws and inserts; frictionless faces; insert pull-out and bearing internal clearance untested. Weakest point: the screw loads are twin loads including prying the real clamped joint would not have. Cheapest improvement: two Ø3 dowels at the split, 3 mm from the seat (not built).

## D3. Six plates, then a change
Files `_wip/sw-eval/sonnet-adv-d/d3/P1..P6.SLDPRT/.stl`, `P1_b..P6_b`. Scripts `d3_table.py` (wall checker; runs on the table alone), `d3_build.py` (one script), `d3_edit.py`. Pictures: `d3_part1_six_plates.png` (six rows, one per plate: flat discs with small holes and counterbores), `d3_part2_six_plates.png` (same with a chamfered rim, thicker edge), `d3_P3_before_after.png` (P3: top row before, bottom row after, ring A turned off ring B and the rim chamfered).

**Checker, before building.** Hole to hole (top face with counterbore radius, and through), hole to bore, hole to outside, floor, rings at the table angles. It flagged P1 (-0.7 mm: A at 0 degrees overlaps B), P2 (-6.25: both rings on the same circle with the same count, so they coincide), P4 (-3.0: the 58 circle with Ø8 counterbores lies outside the Ø60 plate; floor 0.4). P3 passed (rim wall 1.0); P1 and P3 rims listed as questioned. Fixes (circle stays; outside and depth move): P1 ring B turned 15 degrees; P2 ring B turned 30 degrees; P4 outside 60 -> 70, counterbore depth 4.6 -> 4.0. P3, P5, P6 as the table.

**Part one** (`d3_part1_table.md`): volume equals hand exactly, one body, STL watertight one shell (volume within 0.11 %), every hole centre within 0.001 mm and radius within 0.01 mm measured on the solid. Masses 21.10, 28.50, 46.05, 17.47, 74.81, 24.81 g.

**Part two** (`d3_part2_table.md`): opened, `save_as` P#_b, then edited: body depth; counterbore cut depth (its sketch sits on the floor plane, so the floor never moves: Z 3, 3, 4, 1, 3, 3 before and after, measured); outside diameter by redrawing the body sketch (P1 70 -> 72, P3 96 -> 98: a 1 mm chamfer would leave 0.0 mm to the counterbores); P3 ring A redrawn on a 70 circle and turned 22.5 degrees (at 0 degrees it leaves a 0.3 mm wall to the ring B counterbores); then a TOP_CHAMFER. Hand volumes (chamfer pi c^2 (R - c/3)) equal the solids exactly. Thinnest walls 1.0, 3.0, 1.0, 1.0, 1.5, 1.0 mm. Edit proof: the feature list (names, types, IDs) is identical before and after but for TOP_CHAMFER, all six; originals unchanged (SHA-256 same as after part one, volume same). Masses 28.11, 35.28, 57.75, 22.51, 88.37, 30.78 g. Not checked: whether a 1.0 mm rim prints; M6 head height against the P5 counterbore depth.

## Where the playbook or a helper was wrong, unclear or missing
- `Sk` appends `_SK` to the sketch name; `set_dim`/`redraw_circles` need the full name. Not documented.
- Nothing warns that a split face can be two patches; `pick(at=)` returns one.
- Two jobs of one session on one model file: read-only copy, sharing dialog, lost save. The playbook only says one file per session.
- `static()` has no preload, friction or initial interference: the twin cannot show the clamp.
- Node prediction formula ignores small bodies (pins, pads, ring): 2.6x off.
- The playbook's old hand value for +X screw load did not hold here either.
- Launches took about 5 s; no waiting on other sessions.

## Advisor
Called the advisor tool 3 times.
1. After reading the playbook, before any work (D1). It told me to do the envelope arithmetic first, run every SolidWorks job in the background (a foreground shell timeout acts like `timeout`), load the faces that bear, and check D2 and D3 specs in code first. I changed: did the 60 x 18.6 arithmetic first (it decided the concept), ran all jobs in the background, wrote the D3 checker before the builder, loaded the pad tops. Right moment.
2. Mid-D2, after the first contact solves. It told me the split faces were two patches and the -X side was glued (evidence: asymmetric screws on a symmetric model, sum 216 against 300). I changed: patched the pick, marked tags a and c INVALID, reran at three sizes, redid the +X argument. It also said not to move P1/P3 outside diameters in part one (trigger 0.6 mm not 1.5) and to check the M5 length: done. Hindsight: I should have called it when the first asymmetric result appeared (19:05), not 15 min and 12 invalid studies later.
3. Before declaring done. It told me M3x10 would bottom in the 6 mm holes (now M3x6), that the +X hand value must use the section balance (dropped F tan 21), that the fit text contradicted my numbers, that sf_layer must include the counterbore corner (7.2 MPa, factor 3.1), that D3 minutes were run time only. All changed.
Also in hindsight: a call when a solve missed my prediction by 3.7x (I explained it by physics and part of it was a different problem).
