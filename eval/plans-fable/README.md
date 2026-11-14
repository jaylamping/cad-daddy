# How to use these plans

One plan per task: `A_T1.md` to `A_T7.md` (eval/TASKS.md) and `D_D1.md` to `D_D3.md` (eval/TASKS_D.md). The planner had
no SolidWorks: every number here is a hand value, every code block is unrun. The plans tell you what to do when a
result disagrees with them.

## Before the first task (once)

1. Read playbook/README.md, RULES.md ("Rules", "Hung, half-closed and orphaned instances"), 01-session.md, 02-com.md.
   Then do 01-session.md "Before the first script" steps 1 to 5 (worktree, `--status`, claim).
2. Pick a run name `<run>`. Make `eval/<run>/` and `eval/<run>/pictures/`. Copy `plans/common.py` to
   `eval/<run>/common.py`. Every script starts with `from common import *`. It gives you `WIP` (= `_wip/sw-eval/<run>/`),
   `HERE`, `PICS`, and: `put(task, **keys)` (writes results.json), `report(text)` (appends to REPORT.md),
   `check_export`, `stl_stats`, `tree`, `holes`, `must`, `measures`, `direction_table`, `sf_min`, `settled`,
   `save_npz`, `near_axis`, `predict`, `compare`, and the materials `SOFT` and `PRESS`.
3. Run `python solidworks/selftest.py model beam` once. If it does not print PASS, stop and report: nothing below
   will work.

## For each task

1. Read the task in the task sheet, then the whole plan, then the playbook sections the plan names.
2. Write the script from the plan's code. Keep the names, numbers and order. One script = one `with job() as j:`
   = at most four studies. Run in the foreground or detached, never under `timeout`.
3. After every step compare with the plan's expected number. Inside the stated tolerance: go on. Outside it: find the
   matching line in the plan's "Branches" and do exactly that.
4. When something happens that no branch covers: stop that task, write in REPORT.md exactly what you ran and what
   you saw (last 40 log lines), set its `status` to `"partial"` or `"failed"`, and go to the next task. Come back
   only if time is left.
5. Tick the plan's "Done checklist". Write the keys with `put()`. Write the REPORT.md section. Never write a number
   you did not get from a run, and never copy a number out of a plan into results.json as if it were measured:
   hand values go in the `hand_*` keys only.

## Order and dependencies

| Order | Task | Needs | Launches |
| --- | --- | --- | --- |
| 1 | T7 | nothing (no SolidWorks): do it first, or while a job runs | 0 |
| 2 | T1 | | 1 |
| 3 | T2 | T1's `bracket.SLDPRT` | 1 |
| 4 | T3 | T1 | 2 (four studies, then one) |
| 5 | T4 | T1's build function, T3's functions | 2 |
| 6 | T5 | T3's saved results | 0 or 1 |
| 7 | T6 | | 1 (40-minute limit) |
| 8 | D3 | | 2 (part one, then part two) |
| 9 | D1 | | 2 |
| 10 | D2 | | 3 |

If T1 fails, T2 to T5 are blocked: say so, and do T6, T7 and set D. Time limits (T6 40, D1 60, D2 90, D3 60 minutes)
are real: when one runs out, write up what stands and move on.

## Rules that apply to every plan

- Units: helpers take mm, degrees, N, MPa. Raw COM takes metres and radians (02-com.md rule 1).
- Every `pick()` and `edges_where()` is followed by `must(name, len(x), n)`. A wrong count is never "close enough":
  run `list_faces(d)`, read the boxes, fix the filter.
- Pick faces again inside every study run, after `d.ForceRebuild3(False)`. Never reuse a face list across runs.
- Multi-body study order (05-fea.md "One study", first bullet): `j.simulation()` first thing in the job, then
  `open_doc`, `ForceRebuild3`, picks, `static`.
- `new_part()` closes every open document without saving. `save(d)` and `close(j.sw, d)` before the next `new_part`.
- Before each solve call `predict(...)`, after it `compare(...)`. If `compare` returns False, follow 07-done.md
  "Predict, then run" before reading any stress.
- A verdict of "pass" needs all three measures converged (07-done.md study item 6). A verdict of "fail" needs only
  that the governing measure fails at every mesh size in the series. Anything else is "not shown".
- Tolerances, unless a plan says otherwise: volume 0.1 %, box 0.01 mm, hole centre 0.02 mm, reaction 1 %,
  plain-section stress 15 %, displacement within a factor of 3, node count within a factor of 2.
- Files: models, exports and npz in `WIP`; scripts, `REPORT.md`, `results.json`, `pictures/` in `eval/<run>/`.
  Pictures: `python solidworks/sheet.py <stl> -o eval/<run>/pictures/<name>.png`, then open the PNG and look.
- When finished: close SolidWorks (leaving `with job()` does it), commit `eval/<run>/` only (nothing from `_wip/`),
  release the claim (01-session.md "When you finish").
