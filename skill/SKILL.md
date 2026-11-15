---
name: cad-daddy
description: Use for any request to design, change, model, simulate (FEA) or export a robot part in SolidWorks, from a new part to a fix after a print or bench test.
---

# cad-daddy: one CAD job, start to finish

You are the planner for this job, and the owner should not have to think about the process. The full rules are in the
jaylamping/cad-daddy repo: playbook/09-pipeline.md is the order, 08-workflow.md is who does what. Read both before
step 1. If they disagree with this skill, the repo wins.

## Roles
- Planner and reviewer: you. If the Fable allowance is used up, Opus takes every planner role and work does not wait
  (08-workflow.md, "When the strongest model is not available").
- Builder, when the shape is decided: Haiku, in a fresh Remote Control session on joey-vm (folder C:\code), started
  with the `model` parameter. A shape that is not decided is built by the planner itself.

## Machine
- joey-vm is the CAD machine. Repos: C:\code\cad-daddy and C:\code\roark. Each job works in its own worktree.
- Do not use holly-pc or Joey-PC unless Joey asks.
- If joey-vm cannot be reached, post once to #caddaddy-alerts and tell Joey in the thread. Then wait; do not move the
  job to another machine.

## Steps
1. **Intake.** Restate the need in a few lines: what it holds, what it must clear, the load, how it prints. List each
   question with the answer you assume, and carry on. Answer the lane question: is the shape already decided?
2. **Open.** On joey-vm: `python pc/cadjob.py open <slug> --lane <decided|undecided> --planner <model> --builder <model>`.
   Use the printed job name for the worktree, the claim, and the start of every part file and study name.
3. **Shape not decided:** build two or three crude options with picture sheets and show them to Joey with no
   recommendation. Then the layout freeze and review gate 1. After that the shape is decided.
4. **Plan** without SolidWorks. Write PLAN.md and common.py in the job folder: the steps, the expected change in volume
   at each step, the hand numbers worked twice, the studies, and their branches.
5. **Build.** Start the Haiku session with the builder's brief from 09-pipeline.md, filling in its three blanks and
   changing nothing else. Schedule a check on it; do not poll.
6. **Review** from the files, never from the builder's report: rows against logs, verdicts from swfea.judge(), hand
   numbers worked again, the print-direction table, and the twist check on any loft. This is review gate 2.
7. **Fixes.** Run `cadjob.py round <folder>` before each round. When it refuses a fourth round, the part needs a new
   idea: go back to step 3.
8. **Close.** Run `cadjob.py close <folder> --right N --total N`. If it exits 1, a kind of failure is new: fix the
   helper or playbook page in a small cad-daddy PR before reporting.
9. **Report** to Joey in one message, in the order 09-pipeline.md gives: the picture sheet, the verdict and lowest
   factor beside the hand number, weight and print direction, links to the files and PR, what was not shown, and what
   the job cost.

## Merging (Joey, 2026-11-15)
- Playbook and helper fixes in cad-daddy merge once their tests pass, without waiting for Joey.
- Robot parts in roark always wait for Joey's merge.
- Anything that cannot be undone still needs Joey's go.

## Ask Joey only for
- the pick between options;
- a review gate that needs a person;
- a choice that changes the design goal;
- anything that cannot be undone.

Everything else, decide, say what you assumed, and keep going.
