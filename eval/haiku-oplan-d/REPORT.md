# haiku-oplan-d: report

Run: `haiku-oplan-d`, tasks D1, D2, D3 from `eval/TASKS_D.md`, following the plans in `plans/D_D3.md`, `plans/D_D1.md`, `plans/D_D2.md`.
Model: `claude-haiku-5-5` (configured for the session). Reasoning effort: not set by this run, so the session default; I did not change it.
Machine: holly-pc, SolidWorks 2026 SP0, own instances only (claim `sw-eval-haiku-oplan-d`). Clock is UTC; the SolidWorks logs are local (UTC-6).
Start 06:22:53Z (after reading the playbook and plans). Last SolidWorks instance of mine closed 07:08Z; report written 07:10Z. Total about 47 minutes.
Models: `_wip/sw-eval/haiku-oplan-d/`. Scripts, results.json, pictures: this folder. Logs: `_wip/sw-eval/haiku-oplan-d/*.log`.

Summary, by task state:

| Task | State | What is missing |
| --- | --- | --- |
| D3 | done | nothing. All twelve parts (P1-P6, P1_b-P6_b) built, checked, changed by editing. |
| D1 | partial | envelope not met (stated, Joey to overrule); peak convergence not shown (climbing at the arm/standoff root); spine section check fails against the hand value (reason unknown, see below); open area is a hand value |
| D2 | partial | convergence of the lower-half peak not shown (only two meshes; the 2.0/0.7 mesh is over 200k nodes, 2.25 meshes failed or hung); upper crown plain-section check and the Y/X print-direction tables not run; the +X screw loads do not match the hand value |

## D3: six plates from a table, then a change (done)

**Table check, before building (plan section 5, checked in code, `eval/haiku-oplan-d/common.py` `walls()`):**
1. P1 as tabled: ring B at 0 deg puts a Ø8 counterbore 0.7 mm into a Ø3.4 A hole (wall -0.70). Built: ring B turned 45 deg, wall 3.02 (A-B counterbore).
2. P2 as tabled: ring B (6 x 4.5 on 62) is identical to ring A (6 x 4.5 on 62), so the B holes are the A holes. The wall check does not catch coincident holes (zero distance is skipped), so this one is caught by reading the table. Built: ring B turned 30 deg, 12 holes, wall 9.8 (A-B). The other reading (six counterbored holes only) is not built.
3. P3 part two: ring A on Ø70 at 0 deg puts the A hole 0.30 mm from the B counterbore. Built: ring A turned 22.5 deg, wall 9.82 (A-B), minimum wall 1.0 (counterbore to OD).
4. P4 as tabled: OD 60 with ring B (Ø8 counterbores on 58) breaks out of the disc by 3.0 mm (wall -3.00). Built: OD 68, cbore to OD 1.0. Bolt circle kept.
5. P4: counterbore 4.6 deep in 5 mm leaves a 0.4 mm floor. Built: depth 4.0 (floor 1.0).
6. P1, P3, P4: counterbore 1.0 mm from OD is legal (at least 0.6) but under one hole diameter. Listed as a question, not changed.
7. Part two chamfer: a 1.0 chamfer where the counterbore is 1.0 from OD leaves zero wall (checked: 0.0). Used 0.4 on P1, P3, P4 (0.6 left), 1.0 on P2, P5, P6.

**Part one (one script, one job, `d3_part1.py`):** all six built. Volume against hand, every plate: the same to 0.00 % (17,728.67 / 23,947.18 / 38,698.26 / 13,596.26 / 62,864.78 / 20,848.86 mm3). STL watertight, one shell, STL volume within 0.1 %, bounds within 0.1 mm. Every hole centre measured on the finished solid within 0.02 mm of its table position. Counterbore floor measured at 3.0 / 3.0 / 4.0 / 1.0 / 3.0 / 3.0 mm. Minimum walls (measured): P1 1.00, P2 7.00, P3 1.00, P4 1.00, P5 2.50, P6 2.00, all at least 0.6.

**Part two (edit, `d3_part2.py`):** each saved part opened and saved as `P*_b`. Edits: DISC depth `set_dim` (6 -> 7.5 mm), P3 ring A redrawn in its own sketch (`redraw_circles`), a top outside chamfer. Checks per plate: volume against hand (all within 0.001 %); tree prefix identical to part one, extra entry only `TOP_CHAMFER`; counterbore floors unchanged (same Z as part one); STL watertight. Minimum walls after the change (including at the chamfer): P1 0.60, P2 6.00, P3 0.60, P4 0.60, P5 1.50, P6 1.00. P3 ring A measured: 8 holes, radius 35.0 mean, first hole at 22.5 deg.

**Mistake and fix:** my first part-one script exported STLs but never saved the features (`save(d)` was missing), so the `.SLDPRT` files on disk were empty and part two failed with "no feature DISC". The STLs and part-one checks were correct because they come from the open model. Fixed by adding `save(d)` before export and rerunning part one (0.8 min) and part two (0.6 min). The part-one table in this report is from the rerun.

Pictures: `pictures/d3_part1_plates.png` (six plates, rows P1-P6). One line: the plates read as the table says, the turned counterbore ring is visible on P1 and P2, and P5 and P3 are the largest. `pictures/d3_part2_plates.png`: the same six thicker, with the chamfer as a narrow darker rim on the top outside edge; P3's ring A is on the wider circle.

Keys: `plates`, `plates_b`, `table_problems`, `one_script` (true), `edited_not_rebuilt` (true), `minutes` (part one 0.8 SolidWorks minutes plus set-up; part two 0.6). Working time about 6 minutes, waiting time none beyond SolidWorks launches (about 4 s each).

## D1: buck board mount (partial)

**Restate:** `eval/haiku-oplan-d/restate.md` (written before modelling; five lines, assumptions and the questions with answers).

**Envelope contradiction (plan section 5, checked by hand):** the board's 60 mm side must lie across Y or up Z. Flat: 60 > 50 (Y +-25). Upright: 60 > 45 (Z). Tilted: 60 cos + 18.6 sin <= 50 and 60 sin + 18.6 cos <= 45 has no solution (at 55 deg, 49.6 and 59.8). Beside the rail the 18.6 mm thickness needs 15 mm of Y and gets 29.1 mm. **Built: flat, 85 along X, 60 across Y, over the rail. Envelope Y +-30.5 (5.5 over each side), `envelope_ok` false.** Joey can overrule in one line; the other choice costs 18 mm of Z.

**Idea A (built, chosen):** flat cradle on four standoffs (Ø8 x 10, M3 inserts Ø4.0 x 6), two M5 screws through the spine into the rail's T-slot. Mass 15.67 g (13,171.44 mm3, measured 13,171.44 against hand 13,171.4 mm3; STL watertight; STEP in mm). Open area 59 % (hand, plan view, not measured).
**Idea B (crude, rejected):** upright card guides, top at Z 70 (25 mm over the envelope). Volume 16,856 mm3 check passed. Picture `pictures/d1_idea_b.png`.

**Pictures:** `pictures/d1_buck_mount.png` (mount alone). One line: the spine runs between two arms with a standoff on each arm end and the rail holes in the spine. `pictures/d1_assembly.png` (mount, rail, board, parts): one line: the board stand-in rests on the four standoffs and the parts block stands above it, the spine sits under the board between the rail screws. `pictures/d1_idea_b.png`: one line: two tall posts on a base, the grooves on their inner faces, top at 70 mm.

**Removal (4 steps, in results.json):** power off; free the two wire pairs at the board terminals; remove the four M3 screws from above with a 2 mm hex key; lift the board off. Tools: 2 mm hex for the board, 3 mm hex for the M5 screws on the rail (not touched on removal).

**Study (`d1_study.py`, PETG, rigid 9 N on the four standoff tops at (0,0,20), M5 hole walls fixed).** The plan's hand values and results:

| Check | Hand | Study (el 2.0) |
| --- | --- | --- |
| Reaction | (0, 0, -9) | (0, 0, -9.0), 0.0 % |
| Displacement | 0.06-0.1 mm | 0.034 mm (inside the 0.03-0.25 window, below the hand value) |
| Spine top section sigma_x at (30, 0, 5) | +0.61 MPa | **-0.316 MPa** (compression, half the hand value and opposite sign) |
| Peak, away from holes and loads | at the M5 spine, about 1.3 MPa | 0.79 MPa at the arm/standoff root (38.7, 22.5, 5.0) |
| Factor, yield / layer / shear | 22.5 / 13 | 57 / 24 / 31 |

The plan expected the peak at the M5 holes; the study puts it at the arm root where the standoff meets the arm top. The spine check fails: sigma_x is about half the hand value and opposite in sign. I did not resolve the cause. The sign is consistent with an upward load on the arms bending the spine in compression at the top, so the hand sign was likely wrong. The magnitude may be the arms carrying more of the load than the hand model assumes. Not confirmed.

**Convergence (07-done item 6), series 3.0, 2.0, 1.5:** peak 0.67, 0.79, 0.86 MPa (+9 % at the last step). **Not converged (5 % needed); the peak climbs at a sharp inside corner.** Converged verdict: not shown. Factor on the converged-looking value: at least 52 on yield, 25 on layer.

**Corner fillet (07-done item 6, job C):** the standoff roots filleted 0.4 mm (4 edges found), solved at 2.0 and 1.5: peak 2.1 and 2.1 MPa, higher, because the 0.4 mm fillet is smaller than the 0.8 mm local mesh. **Not converged either;** the fillet needs a finer local mesh than this run did. Not pursued further; the margins stay above 12 on every measure.

**Second load, even pull (07-done item 3):** the 9 N as an even normal pull on the same tops, 2.0 mm: peak 1.49 MPa at the arm root (-34, 8, 5). This is the higher of the two loads and governs: factor 30 on yield, 82 on layer, 24 on shear.

**Second support (07-done item 2), spot-face twin under each M5 head, 0.1 mm deep (10.96 mm3 removed, checked):** peak 0.76 MPa at 2.0, 0.87 MPa at 1.5, the same as the holes support within 15 %. Reaction equals load. Both supports agree; the result is the higher.

Print: spine bottom on the bed, layers normal Z (chosen), no supports. Direction table for the other two normals not run for D1 (the layer tension is checked for Z only, 0.68-0.94 MPa against 22.5).

Thinnest margin and what would eat it: the envelope overrun and the M3 inserts, not stress. Cheapest improvement: thinner arms (4 mm) or lightening holes in the spine, sized by hand, not built.

What I did not check: the envelope cannot be met as specified (only one way built), the insert pull-out (hand 2.25 N, not run), and the rail's real T-slot profile (stand-in box with a 6 mm slot).

## D2: split housing (partial)

**Spec problems (plan section 5, all confirmed by numbers in the build):** listed in results.json `D2.spec_problems`. Built: shoulder Ø46.0; screws X +-31.0 at Z -0.2 and 7.2; split gap 0.8; seat Ø52.0 at Z -0.1..7.1. The "10 bodies" in the plan is a miscount: the assembly is 9 bodies (2 halves, ring, 4 screws, 2 pads), and the plan's own volume total (42,083.4 mm3) is the 9-body sum. The build check now asserts 9.

**Build (`d2_build.py`, all checks passed):** lower half 19,598.79 mm3 (hand 19,598.8), upper 18,878.12 (hand 18,878.1), ring 2,199.11 (hand 2,199.11), each screw 350.96 mm3, each pad 1.764 mm3, the 9-body total 42,083.38. Bodies named by the last feature, as the material log shows.

**Fit:** what touches: ring OD on the seat (line to line, intended, with contact); ring axial 0.1 mm each side in the seat; pads on the ring ID. What clears: inner ring to shoulder 1.0 radial, shank in hole 0.2 radial, head in counterbore 0.25 radial, insert hole to seat 3.0, clearance hole to seat 3.3, counterbore to Z face 0.8, split gap 0.8.

**Study (`d2_study.py`, PETG halves, steel ring and screws, pads Soft pad 0.5 MPa, base Y -32 fixed, pads fixed, 300 N remote on the ring ID, contact no-penetration ring/seat and split faces; direct sparse solver):**

| Case | Nodes | Ring travel (mm) | Peak VM upper / lower (MPa) | Factor VM lower | Layer lower / shear lower (MPa) |
| --- | --- | --- | --- | --- | --- |
| +Y, 2.5/1.0 | 131,254 | 0.041 | 2.98 / 10.44 | 4.31 | 1.69 / 3.03 |
| +X, 2.5/1.0 | 131,254 | 0.050 | 2.95 / 8.00 | 5.62 | 1.28 / 2.32 |
| +Y bonded twin, 2.5/1.0 | 131,254 | 0.0018 | 0.11 / 0.60 | | |
| +Y, 3.0/1.5 | 89,315 | 0.041 | 3.03 / 11.90 | 3.78 | 1.34 / 2.83 |

- Reaction equals load in every case (0.0 %).
- Pad share: not measured. Pad von Mises is at most 0.55 MPa (0.5 MPa material). Estimate only: stress times a patch of about 2 mm2 gives under 1 N, against the 300 N load.
- Contact proof (05-fea "A body seated on both sides"): (1) bonded twin ring travel 0.0018 mm against 0.041 mm with contact, a factor of 22; (2) bonded screws carry 2.3 N each against 75 N with contact; (3) the lower seat opens: ring UY minus lower housing UY at (0,-26,3.5) is +0.041 mm.
- Screw load, +Y: study 68.6-77.1 N per screw (y = 10, 15, 20 agree within 5 %), sum 295 N against the 300 N load (1.7 % off). Hand 75 N each: within 15 %.
- Screw load, +X: study 46.5-48.4 N per screw tension, sum 185 N. Hand (plan) 37 N each: **27 % lower than the study, not within 15 %, not explained.** The plan itself marked this hand value low confidence. The hand value used the wedged-ring statics from the plan; I did not redo it with the contact patch from the study.
- Governing: +Y, lower half, peak at the mount/insert bottom edge (-29.6, -6.4, -1.6). Shear peak at the split face (29.2, -0.4, 8.0).
- Factors: lowest over both halves and both cases at 2.5/1.0: yield 4.31, layer 13.33, shear 4.29. Requirement (factor 2.0 on all three) met with margin at both meshes.

**Mesh and convergence (not shown):**
- +Y and +X at 2.5/1.0: 131,254 nodes (plan expected 90,000).
- +Y at 3.0/1.5: 89,315 nodes. Lower-half peak rose from 10.44 to 11.90 MPa (+14 %): **not converged**.
- +Y at 2.0/0.7: 220,878 nodes, over the 200,000 limit. Plan branch: 2.25/0.8. That run stopped with a solver dialog "Fixture <Fixed-1> transfer failed", which none of the plan's branches cover.
- +Y at 2.25/1.0: hung on a hidden SolidWorks message box ("SOLIDWORKS Design", #32770, 00:49:32 local). The helper answers only solver dialogs, so my client waited for it. I ended my client and its instance (PID 213832) with `sw_kill.py --force` on my own PID.
- +Y at 2.5/1.0, rerun to get the crown and direction table: hung on the same kind of box (00:56:06 local). I ended it (PID 212940) the same way.
- Result: only two meshes give the lower peak (2.5/1.0 and 3.0/1.5). Convergence of that peak: **not shown.**

**Not done:** the upper crown plain-section check (plan: sigma_x at X 0, Y 31.9, against 8/16/28 MPa for M 1,350/2,700/4,650). The hand estimate (about 21 MPa in the layer plane) is not checked: the study's upper-half peak is 2.98 MPa at the counterbore (29.1, 27.9, 5.9), not the crown. **That difference is unexplained.** The Y and X direction tables (only Z is checked) were not run. Load-path split across the screws by section integration was not done.

**Verdict:** requirement met on margin at both meshes (lowest factor 3.8 on yield at the finest). Convergence not shown, so `status` partial. `valid` true for the solves done (under 200,000 nodes, reactions correct, contact proven). Print: both halves flat on the Z -4 face, layers normal Z, the chosen direction. The Y-axis screw holes print horizontal (bridged) per the plan.

**Pictures:** `pictures/d2_upper_half.png` (one line: a U-shaped half with the shoulder opening and counterbored holes on the back), `pictures/d2_lower_half.png` (one line: the same with the Ø46 opening and the mount holes on the Y -32 face), `pictures/d2_pair.png` (one line: two halves meeting at the 0.8 mm gap, the seat clear of the ring, screws in place).

Time: build about 1 minute of SolidWorks; job 2 7 minutes; about 19 minutes lost to two hung instances (hidden message boxes), plus the 2.0/0.7 and 2.25 attempts. D2 working time about 14 minutes; wall time about 32 minutes.

## Helper and playbook problems found

1. **`static()` and the solver dialog watcher.** The watcher answers the excessive-displacement dialog and logs others; a hidden `#32770 SOLIDWORKS Design` message box (not the solver's) came up twice in D2 and hung the study until I ended the instance. The playbook has no branch for a message box that is not a solver dialog, and the helper does not log its text. The hidden log names only the window title. Request: log the text of that box, or give a branch (the playbook's own rule is "in your own instance you may read such a dialog and press its button").
2. **`export()` leaves the document unsaved.** `export()` uses `SaveAs` to the STL, so a part exported before a save is not saved on disk. This caught me (see D3). Request: a note on 02/04, or `export()` saves first.
3. **Playbook 07 "save after each step"** is not stated next to the build helpers; a build script that only exports loses the model on disk.
4. **Body counts in plans.** D2 says 10 bodies; there are 9.
5. **Plan mesh estimates.** D2 predicted 90,000 nodes at 2.5/1.0; the real count is 131,254 (1.5 times). D1 predicted 13,000 / 30,000 / 70,000 and got 13,036 / 33,844 / 71,825 (close).
6. **Plan hand values.** D1 spine-section sign and magnitude (see D1). D2 crown hand value (21 MPa) not reproduced by the study's upper half. D2 +X screw hand value (37 N) 27 % below the study.
7. **`pick()` on split faces.** The lower split face returns 6 faces, the upper 2, for the same design; the difference is the hole openings on the split plane, which the plan does not mention.
8. **Paths.** RULES.md and the plans use `J:\code\roark` and `roark-wt`; this worktree is `cad-daddy-wt`. The playbook's links point to a `roark` repository not in this checkout; not followed (plan says they are intended). `tools/cad/check_cad_layout.py` and `check_sw_refs.py` are not in this repo; not run.
9. **`sw_instance.py --status` after a hang** still lists my hung instance as "no claim" even with the claim present; `sw_kill.py --force <pid>` ended it cleanly.
10. **`feature_errors`, `set_dim`, `redraw_circles`, `edges_where`, `chamfer`, `fillet`, `insert_body`** all behaved as documented in the D3/D1/D2 builds. `set_dim` on a DISC extrude worked directly.

## Times

From the clock (UTC):

| Stage | Start | End | SolidWorks working | Waiting |
| --- | --- | --- | --- | --- |
| D3 part one | 06:24 | 06:26 | 0.8 min | none |
| D3 part one rerun (save fix) | 06:28 | 06:29 | 0.8 min | none |
| D3 part two | 06:29 | 06:30 | 0.6 min | none |
| D1 build | 06:30 | 06:31 | 0.4 min (two reruns) | none |
| D1 study A (3 meshes) | 06:31 | 06:33 | 0.5 min | none |
| D1 study B (twin, pull) | 06:33 | 06:34 | 0.5 min | none |
| D1 study C (fillet) | 06:35 | 06:37 | 1.0 min | none |
| D2 build | 06:37 | 06:38 | 1.0 min | none |
| D2 job 2 (4 cases) | 06:39 | 06:47 | 7 min | solves only |
| D2 job 3 (2.0/0.7, over limit) | 06:47 | 06:48 | 0.2 min | none |
| D2 2.25/0.8 | 06:48 | 06:49 | 0.3 min | fixture dialog |
| D2 2.25/1.0 | 06:49 | 06:56 | hung | about 6 min |
| D2 2.5/1.0 rerun | 06:56 | 07:08 | hung | about 11 min |

No launch waited behind another session's instance: the keeper answered every launch. The shoulder-study instance was busy at times and did not hold any launch of mine.

## Output locations

- `eval/haiku-oplan-d/`: `d3_part1.py`, `d3_part2.py`, `d1_build.py`, `d1_study.py`, `d2_build.py`, `d2_study.py`, `common.py`, `restate.md`, `results.json`, `REPORT.md`, `d3_part1_rows.json`, `d3_part2_rows.json`, `pictures/`.
- `_wip/sw-eval/haiku-oplan-d/`: all models (`P*.SLDPRT`, `P*_b.SLDPRT`, `buck_mount*.SLDPRT`, `housing_*.SLDPRT`, `ring.SLDPRT`, `d2_fea.SLDPRT`, STLs and STEPs), logs, and CWR solver files. Gitignored.
