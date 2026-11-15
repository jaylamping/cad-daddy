# How to use these plans

One plan per task: `A_T1.md` ... `A_T7.md` (task sheet `eval/TASKS.md`) and `D_D1.md` ... `D_D3.md` (`eval/TASKS_D.md`).
The plans assume you have read `playbook/README.md`, `solidworks/RULES.md` (Rules, Hung instances), `01-session.md`,
`02-com.md` and `07-done.md`. They point at playbook sections instead of copying them.

## Order

A set: T7 (no SolidWorks, 15 min) can be written any time. T1 -> T2 -> T3 -> T4 -> T5 must run in that order (each
uses the file before it). T6 stands alone. D set: D3 part one, D3 part two, D1, D2 (D2 last: hardest, longest).
If one task blocks, write down where it stands and go on (07-done.md, "Do not stop early").

## Reading a plan

Each plan has: 1 restatement and checklist, 2 hand numbers (with the tolerance you must meet), 3 build steps,
4 study set-up, 5 decisions already made for you, 6 branches ("if you see X ... do Z"), 7 done list and the result keys.

- **Do the steps in the order written.** Each build step gives the exact helper call and the volume change it must
  make (`expect_dv`). Never drop `expect_dv` to make a step pass: a mismatch means the step is wrong.
- **Decisions in section 5 are made.** Do not reopen them. If the plan says the task sheet is wrong, build what the
  plan says and report it the way it says.
- **Branches:** when something happens, find it in section 6 and do exactly that. When nothing there matches: stop
  that task, write down exactly what you saw (the command, the last 40 log lines, the numbers), and go on with the
  next task.
- **Tolerances:** every hand number has an "accept" band. Outside it: do not report the number as a result. Go to
  the branch for it.

## Conventions used in every plan

```python
import sys, math, json
from pathlib import Path
sys.path.insert(0, r"J:\code\roark-wt\<session>\solidworks")
from swkit import *
from swfea import *
W = Path(r"J:\code\roark-wt\<session>\_wip\sw-eval\<run>")      # models
E = Path(r"J:\code\roark-wt\<session>\eval\<run>")              # scripts, REPORT.md, results.json, pictures/
```

- All coordinates are model mm. `Sk` points are 3D model points that must lie on the sketch plane.
- **Feature tree log** (used to prove an edit, T2 and D3): this loop uses only the calls `feature_errors()` uses.
  ```python
  def tree(d):
      out, f = [], d.FirstFeature
      while f is not None:
          out.append((f.Name, f.GetTypeName2)); f = f.GetNextFeature
      return out
  ```
- **Load-face mask off.** `Result.away()` masks nodes near fixtures AND load faces. Where a plan says "clear the load
  mask", do `r.loaded_pts = None` right after `static()` returns, so `away()`, `peak()`, `layer_*()` and `converge()`
  mask only the fixture. Plans say when and why.
- **Picks:** print `len()` of every pick and compare with the count in the plan before using it. Wrong count: run
  `list_faces(d)`, find the face by its box, narrow the pick with `inside=` or `at=`.
- **Predict, then run** (07-done.md): log the expected nodes, displacement and peak place before each `static()`.
  Each plan gives the three numbers.
- **Studies:** `j.simulation()` first, then `open_doc()`, then `d.ForceRebuild3(False)`, then picks, then `static()`
  (05-fea.md "One study"). At most four `static()` calls per `job()`.
- Pictures: `python solidworks/sheet.py <stl> -o E/pictures/<name>.png`, open the PNG and look at it.
- `results.json`: one object per task with the keys the task sheet names plus `status` and `notes`.
- Mass of PETG = volume x 1.19e-3 g/mm3. Steel 7.85e-3 g/mm3.
