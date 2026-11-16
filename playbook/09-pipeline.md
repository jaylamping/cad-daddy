# 9. One job, start to finish

[08-workflow.md](08-workflow.md) says who plans, who builds and who reviews. This page is the order it happens in,
so that every job runs the same way and the owner has nothing to remember. The session that receives the request
runs this page; it is the planner unless it hands that role on.

```text
request -> intake -> shape decided? -- no --> options -> the owner picks -> layout freeze (gate 1) --+
                          |                      ^                                                   |
                         yes                     +--- a 4th round: new idea, new job -------+        |
                          v                                                                 |        |
                        plan  <-------------------------------------------------------------|--------+
                          v                                                                 |
                        build (smallest model, CAD machine) --> review from files (gate 2) -+
                                        ^------ fixes, at most 3 rounds ------+
                                                                              v
                                              close: metrics, failures sorted, new kinds fixed
                                                                              v
                                              one report to the owner --> print and bench --> a change is a new request
```

## The steps

| Step | Who | What | Leaves behind |
| --- | --- | --- | --- |
| 1. Intake | planner | Restate the need in a few lines: what it holds, what it must clear, the load, how it prints. List the questions and the answer assumed for each, and go on. Ask the lane question: is the shape decided? | the restated need |
| 2. Open | planner | On the CAD machine, from the cad-daddy checkout: `python pc/cadjob.py open <slug> --lane <lane> --planner <model> --builder <model>`. Then make the worktree and the claim under the name it prints | the job name, the job folder in `jobs/` beside the checkout, the worktree |
| 3. Options (shape not decided) | planner | Two or three ideas that differ in kind, crude models, a picture sheet of each, the numbers that separate them. The owner picks from pictures; then the layout freeze and review gate 1. A pick carries no recommendation | picture sheets, the pick |
| 4. Plan | planner, without SolidWorks | Steps, the expected change in volume at each, hand numbers for every check, the studies and their branches, a shared `common.py` | `PLAN.md`, `common.py` in the job folder |
| 5. Build | smallest model that follows a plan, in a fresh session, one builder at a time on the machine | The brief below, unchanged apart from its three blanks | part, exports, `results.json`, picture sheet, `runs.log`, `times.log` |
| 6. Review | planner, from the files | Rows against logs, verdicts from `swfea.judge()`, hand numbers worked again, the twist check on a loft, the print-direction table. Review gate 2 | `REVIEW.md` |
| 7. Fixes | planner runs `round`, the builder applies the fixes | `python pc/cadjob.py round <folder>` first, then written instructions to a fresh builder, one round at a time. The script refuses a fourth round: close this job and open a new one, which starts at step 3 | the round count in `job.json` |
| 8. Close | planner | `python pc/cadjob.py close <folder> --total N --reached N --right N`. Exit 1 means a kind of failure this machine has not seen and nobody has fixed, or no `runs.log`: fix it, then `close <folder> --fixed <link to the fix>` | `metrics.json` in the job folder and in `eval/jobs/<name>/`, the fix |
| 9. Report | planner | One message to the owner, laid out as below | the report |

A change after print or bench is a new request. A correction enters at step 4, a new idea at step 3
([08-workflow.md](08-workflow.md), stage 10), and review gate 3 comes before anything load-bearing or powered.

## The owner's part

The owner writes the request, picks from pictures when the shape is not decided, and prints. Everything else on
this page happens without them. Ask the owner only for those, for a review gate that needs a person, and for
anything that cannot be undone.

## The job name

`cadjob.py open` makes the name from `j`, four random hex characters and a slug of at most ten characters, for
example `j7f3a-elbow-rig`. Use it for the job folder, the worktree, the claim, and as the start of every part file and
study name the job makes. `swfea.static()` keeps only the first 24 characters of a study name, so what follows the
job name in a study name is at most 7 characters (`j7f3a-elbow-rig-tip-c2`). The date is in `job.json`, not in the
name. `pc/sw_watch.py` takes the job name out of an error before it sorts it, so the same fault in two jobs is one
kind.

**Why:** the job name keeps every file, study and error traceable to one job. It is not what keeps parallel runs
apart: instances meshing at the same moment overwrite each other's mesh scratch files, which Simulation writes
under fixed names (`body1.x_b`, `Vmesh1.mesh`, ...) in the shared `%TEMP%` work folder, whatever the file and study
names. That gave wrong node counts and a global bonding error (joey-vm, 2026-11-15), and with unique names it
still could. `swfea` meshes under a machine-wide lock (`%TEMP%\sw_simulation_mesh.lock`), so only one instance
meshes at a time; 2 and 4 instances with the same names then all built the right model.

## The machine

- One CAD machine is the default and every job goes there. Each job has its own worktree and its own SolidWorks
  instance ([01-session.md](01-session.md)).
- **One solve at a time.** Two solves at once took longer than one after the other, and a second iterative solve
  stopped at a hidden "insufficient memory" dialog (joey-vm, 2026-11-15). Nothing in the helpers enforces it: the
  heavy-solve lock only covers solves over 200,000 nodes. So the planner runs one builder at a time on the machine,
  and a builder runs its studies one after another.
- **Solver: FFEPlus first, direct sparse as the fallback.** FFEPlus was 4 times faster at 148,000 nodes and 9
  times at 500,000 with the same answers. Use direct sparse from the start on a model with bolt connectors and
  no-penetration contact, where FFEPlus ends with error 24 ([05-fea.md](05-fea.md)). `swfea` refuses a direct-sparse mesh over
  `node_limit()` (760,000 nodes on joey-vm, 450,000 on 32 GB) and an FFEPlus mesh over 2,000,000; direct sparse ran out of joey-vm's 80 GB somewhere between 500,000 and 900,000
  (joey-vm benchmark, 2026-11-15).
- If the machine cannot be reached, the job waits and the owner is told once. Work is not moved to another
  machine without the owner saying so.

## The builder's brief

Give the builder this and nothing else. A longer brief does not help: the plan carries the judgement.

```text
You are building one CAD job from a written plan. Job name: <name>. Job folder: <folder>. Worktree: <worktree>.

1. Read playbook/README.md and the pages it lists for your task, then <folder>/PLAN.md and <folder>/common.py.
2. Follow the plan step by step. Start every part file and study name with the job name. Keep every script, log
   and result in the job folder. Call swkit.stamp(<folder>, label) at the start and end of each task. Run your
   studies one after another, never two at once.
3. Check each step against the number the plan gives for it. If your result disagrees with the plan, do not
   adjust either one: record both numbers in results.json and carry on with the tasks it does not block.
4. Every verdict comes from swfea.judge() on the rows. Do not write a verdict in words of your own.
5. Do not change the design. A choice the plan does not cover (a load path, a split line, a print direction, a
   dimension that cannot be met) is recorded as an open question, not decided.
6. Do not open other jobs' folders or eval/. Do not stop a process you did not start.
7. When every task is done, shown not possible, or blocked after three different tries, write results.json and a
   picture sheet of each part, and report: what was built, the rows, what disagreed with the plan, what you
   could not verify. Then stop.
```

## Closing a job, and what a failure turns into

`cadjob.py close` counts the job from its own `runs.log`, adds the stalls whose report is in the job folder and, on
Windows, every SolidWorks crash or hang on the machine since the job opened (with one builder at a time these are
the job's own), and sorts them into kinds with the same rule and the same list of known kinds as
[sw_watch.py](../pc/sw_watch.py). A new kind goes on that list at once, so the daily look does not report it again,
and stays on the job as unfixed: `close` exits 1 on every run until `--fixed <link>` records the fix.

| Close reports | Do |
| --- | --- |
| a kind seen before, and the job has no unfixed kinds | nothing: it is already written down |
| a new kind caused by the helpers or by SolidWorks (a prompt nobody answers, a call that returns nothing, a crash) | fix the helper so that it raises or answers, add the line to the page that covers it with the date, in one small pull request, before the report |
| a new kind caused by the plan or the brief (a wrong hand number, a step the builder could not follow) | fix the page the planner should have followed, the same way |
| a script that never passed | it goes in the report under "not shown" |

A fix is a small pull request of its own, with the tests passing, and it is merged without waiting for the owner.
The job's `eval/jobs/<name>/metrics.json` goes in the same pull request, or in one of its own when nothing needed
fixing, so the cost of every job is in [metrics_table.py](../pc/metrics_table.py). The parts a job makes are not
merged that way: they wait for the owner's merge, which is gate 2 in practice. No commit or description carries a
tool's attribution line ([CLAUDE.md](../CLAUDE.md)).

**Why:** every correction in these pages came from a run that tripped on something
([EVAL.md](EVAL.md), "What each run changed in the playbook"). Sorting failures when the job ends is what stops a
lesson from living only in a chat.

## The report

One message, in this order, and nothing the owner has to open to understand it:

1. What was made, in a sentence, with the picture sheet.
2. The verdict from `judge()` and the lowest factor, beside the hand number.
3. Weight, print direction, print height, support on faces that show.
4. Where the files are: the print file, the part, the pull request.
5. What was not shown, what was assumed, and anything the owner would want to overrule.
6. What the job cost: minutes, rounds of fixes, failed runs, and what was fixed in the playbook because of it.
