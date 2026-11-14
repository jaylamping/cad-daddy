# haiku-plan-a-followup: what this folder is

- Round two of run `haiku-plan-a` (task set A), 2026-11-14, in the same worktree as round one, by the same
  small-model executor as round one (as started by the coordinator; the files do not record the model).
- Round one is in [../haiku-plan-a/](../haiku-plan-a/) and was frozen in the worktree as `eval/haiku-plan-a-round1/`
  before round two began. Compared file by file: round two changed no round-one file except those listed below.
- Inputs: `followup.brief.txt` (the brief, kept beside the worktree) and `FOLLOWUP.md` (the step-by-step instructions,
  `followup/FOLLOWUP.md` in the worktree), written from [../haiku-plan-REVIEW.md](../haiku-plan-REVIEW.md).
- Helpers: the worktree had `swfea.judge()`, `swkit.stamp()` and the `07-done.md` verdict section as uncommitted
  edits to `solidworks/` and `playbook/` (the `read-results` branch). They are not copied here.
- Copied here: only what round two added to or changed in the run folder `eval/haiku-plan-a/`:
  - new: `FOLLOWUP_REPORT.md`, `times.log`, `t5_toe.py`, `t5_toe_rows.json`, `t5_toe_judge.json`, `t6m.py`,
    `t6m_rows.json`, `wip-logs/` (`t5_toe.log`, `t6m.log`, and `t6m.err`, which is empty)
  - changed: `results.json` (T4 notes, T5, T6, new T7 and `review_corrections`)
  - not in the folder: the script for step R2a (reading the round-one T6 results) and the call that wrote
    `t5_toe_judge.json`; the run kept neither
- Left out: `.npz` nodal arrays, SolidWorks models and solver scratch in `_wip/sw-eval/haiku-plan-a/`; they stay in
  the worktree on the CAD workstation. Files are byte for byte as the run left them (some start with a UTF-8 byte
  order mark).
- The run reports on itself in `FOLLOWUP_REPORT.md`. The independent check is in
  [../haiku-followup-CHECK.md](../haiku-followup-CHECK.md).
