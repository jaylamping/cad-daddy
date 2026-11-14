# haiku-plan-d-followup: what this folder is

- Round two of run `haiku-plan-d` (task set D), 2026-11-14, in the same worktree as round one, by the same
  small-model executor as round one (as started by the coordinator; the files do not record the model).
- Round one is in [../haiku-plan-d/](../haiku-plan-d/) and was frozen in the worktree as `eval/haiku-plan-d-round1/`
  before round two began. Compared file by file: round two changed no round-one file except those listed below.
- Inputs: `followup.brief.txt` (the brief, kept beside the worktree) and `FOLLOWUP.md` (the step-by-step instructions,
  `followup/FOLLOWUP.md` in the worktree), written from [../haiku-plan-REVIEW.md](../haiku-plan-REVIEW.md).
- Helpers: the worktree had `swfea.judge()`, `swkit.stamp()` and the `07-done.md` verdict section as uncommitted
  edits to `solidworks/` and `playbook/` (the `read-results` branch). They are not copied here.
- Copied here: only what round two added to or changed in the run folder `eval/haiku-plan-d/`:
  - new: `FOLLOWUP_REPORT.md`, `times.log`, `d2_step_a.py`, `d2_step_a_fit.py`, `r3b_edit.py`, `d2_conv.py`,
    `d2_conv_report.py`, `d2c_rows.json`, `wip-logs/` (six logs)
  - changed: `d1_study.py` (five lines added after the direction table), `REPORT.md` (a correction appended),
    `results.json` (D1 `sf_min_note`; D2 keys, `judge`, `verdict`, `valid`)
  - overwritten in `_wip` by step R4: the round-one `D1_Z_*.npz` and the solver files of the D1 study (same script,
    same sizes)
- Left out: `.npz` nodal arrays, SolidWorks models and solver scratch in `_wip/sw-eval/haiku-plan-d/`; they stay in
  the worktree on the CAD workstation. Files are byte for byte as the run left them (some start with a UTF-8 byte
  order mark).
- The run reports on itself in `FOLLOWUP_REPORT.md`. The independent check is in
  [../haiku-followup-CHECK.md](../haiku-followup-CHECK.md).
