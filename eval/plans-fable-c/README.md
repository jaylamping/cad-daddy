# How to use these plans (set C: design sense)

Two plans, in this order: [C_C1.md](C_C1.md) (the boxy link), then [C_C2.md](C_C2.md) (make it more organic). The
task sheet is `eval/TASKS_C.md`; read it first, all of it, including how it is graded. The whole set has
**100 minutes**.

The planner had no SolidWorks. Every number in the plans is a hand value or comes from a numpy model of the design
(`hand_numbers.py`), and every script is unrun. The plans say what to do when a result disagrees with them.

## What is in this folder

| File | What it is |
| --- | --- |
| `common.py` | Shared helpers and **the design as numbers** (section tables, hub, knuckle, slot, tunnel). Every script imports it |
| `scripts/c1_boxy.py` | C1, complete |
| `scripts/c2_ideas.py`, `c2_detail.py`, `c2_fea.py`, `c2_finish.py` | C2, one script per stage, complete |
| `scripts/c2_loftpairs.py` | Diagnosis only (a branch of C2 calls for it) |
| `restate_C2.md` | The restatement C2 must have before any modelling |
| `C_C1.md`, `C_C2.md` | The plans: steps, expected numbers with tolerances, branches, done checklist. The scripts are printed in them in full |
| `hand_numbers.py` | The planner's numpy model. You do not need to run it |
| `PLANNER_NOTES.md` | What the planner was unsure of. Read "Most likely to go wrong" before you start |

## Setup, once

1. Read `playbook/README.md`, `solidworks/RULES.md` ("Rules", "Hung, half-closed and orphaned instances"),
   `playbook/01-session.md`, `02-com.md`, `03-modelling.md`, `05-fea.md`, `07-done.md`. Then do 01-session.md
   "Before the first script", steps 1 to 5 (worktree, `--status`, claim).
2. Pick a run name `<run>`. Make `eval/<run>/` and `eval/<run>/pictures/`.
3. Copy into `eval/<run>/`: `common.py` and the six files in `scripts/` (so that they sit beside `common.py`).
   Do **not** copy `restate_C2.md` yet: C2 step 1 does that.
4. `python solidworks/selftest.py model extras` once. If it does not print PASS, stop and report: nothing below
   will work.
5. All commands below are run **from `eval/<run>/`**, in the foreground or detached, never under `timeout`.

`common.py` gives every script: `HERE` (= `eval/<run>/`), `WIP` (= `_wip/sw-eval/<run>/`, models and exports),
`PICS`, `put(task, **keys)` (writes `results.json`), `got(task, key)`, `report(text)` (appends to `REPORT.md`),
`clock()`, `since_c2(label)`, `must`, `holes`, `picture`, `stl_stats`, `check_export`, `fixed_items_stl`,
`build_form` and the feature builders, `measures`, `direction_table`, `predict`, `compare`.

## Order

| # | Do | Launches | Budget (minutes on the clock) |
| --- | --- | --- | --- |
| 1 | C1: `python c1_boxy.py` | 1 | ends by 10 |
| 2 | C2 step 1: stamp "C2 start", copy the restatement | 0 | 3 |
| 3 | C2 stage 1: `python c2_ideas.py` (two ideas, checkpoint 1, the choice) | 1 | checkpoint 1 within **20 min of C2 start** |
| 4 | C2 stage 2: `python c2_detail.py` (the part, fixed items, exports, checkpoint 2) | 1 | ends by 35 after C2 start |
| 5 | C2 stage 3: `python c2_fea.py` (three cases, three sizes, verdict) | 4 | ends by 62 |
| 6 | C2 stage 4: `python c2_finish.py` (before/after sheet, checkpoint 3, keys, DESIGN.md) | 0 | ends by 70 |
| 7 | The hand-written lines, the done checklists, the final table of states | 0 | ends by 80; the rest is for branches |

If C1 fails, C2 still runs: it takes the boxy mass from the hand value and says so.

## Rules for every step

1. **Follow the code literally.** Keep names, numbers and order. Do not "improve" a section table or a tolerance.
   The design decisions are made: the form, the sections, the print direction, the load model, the rule that picks
   the idea. Yours are the running, the checking and the honest reporting.
2. **After every step compare with the plan's expected number.** Inside the stated tolerance: go on. Outside it:
   find the line in the plan's "Branches" and do exactly that. Tolerances are written with their kind: "5 %" is
   relative, "0.05 mm abs" is absolute. In code, `expect(what, got, want, tol)` reads a `tol` between 0 and 1 as
   relative; an absolute tolerance is always passed as `abs_tol=` with `tol` 0.
3. **Numbers come from runs.** Every number in `results.json` and `REPORT.md` is written by a script from what it
   measured. Never type a number in, never copy one from a plan (hand values live only in keys named `hand_*` and in
   the plan). If a script did not produce a number, the number does not exist yet.
4. **Verdicts come only from `swfea.judge()`.** Do not read a table and decide pass or fail. `c2_fea.py` calls
   `judge()` and writes its verdict, its lowest factor and its lowest entry; quote those three and nothing else.
5. **Times come only from `swkit.stamp()`** (the file `eval/<run>/times.log`). The scripts stamp themselves. Never
   write a time from memory. The minutes column is a running total since the first stamp; a duration is a
   difference of two lines.
6. **A task ends in one of three states, and only these** (07-done.md, "Do not stop early"): **done** (every item of
   the plan's done checklist has its number), **not possible** (the requirement that cannot be met, shown with
   numbers, and the nearest thing that can), or **blocked** (the same obstacle met three times in three different
   ways, each with its log, and the time used up or the branches worked through). A refused mesh, a failed
   feature, a wrong pick count or a verdict of "not shown" is **not** an end: each has a branch. One task failing
   never ends the other.
7. **Pictures: numbers decide, your eye describes.** After each picture is made, open the PNG, and write **one
   line** in `REPORT.md` where the script left "WRITE THIS LINE BY HAND": what you see (for example "a round hub, a
   stem that narrows to a waist and widens into a two-pronged fork; a crease where the stem meets the hub"). Do not
   change the design because of what you see. Every decision in the plans hangs on a number the script prints
   (shape numbers, mass, sampled clearances, factors).
8. **`new_part()` closes every open document without saving.** The scripts save before it. If you add a step, save
   first.
9. **Picks are counted.** Every `pick()` in the scripts is followed by `must(name, len(x), n)`. If a count is
   wrong, run `list_faces(d)`, read the boxes, and use the branch; never loosen the count to make it pass without
   the check the branch gives.
10. **Study order** (05-fea.md): `j.simulation()` first, then `open_doc`, `ForceRebuild3`, picks, `static`. Faces
    are picked again for every study. At most four studies in one instance: `c2_fea.py` opens one instance per mesh
    size.
11. **Do not commit or push** as part of these plans, and do not reorder the deliverables: the task sheet's own
    order stands (restatement, checkpoint 1 inside 20 minutes, ideas, part, checks, DESIGN.md). Leave committing to
    whoever runs the benchmark.
12. **If a `common.py` function raises on its first use** because of a typing mistake of the planner's (a wrong
    attribute, an index), fix that line, write the fix in `REPORT.md` under "Fixes to the plan's code", and go on.
    Do not delete a check to get past it.
13. **At 85 minutes on the clock** (`python -c "from common import *; print(clock())"`), stop starting new
    branches: run `c2_finish.py` on what exists, fill the states table, and report honestly what is open.

## When you are finished

Close SolidWorks (leaving `with job()` does it), release the claim (01-session.md "When you finish"), and end
`REPORT.md` with this table, one row per task, state from rule 6:

| Task | State | Proof |
| --- | --- | --- |
| C1 | done / not possible / blocked | the keys in results.json, or the log of three tries |
| C2 | done / not possible / blocked | the gate table from c2_finish.py, or the log of three tries |
