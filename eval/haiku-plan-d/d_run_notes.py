"""Appends the run-level sections of REPORT.md: times, waits, failures, playbook and helper defects, model and effort."""
from common import *  # noqa: F401,F403

report("""## Run summary (haiku-plan-d, set D)

Model: claude-haiku-5-5 (configured; the served model was not checked). Reasoning effort: default (not set by the brief).
Start 14:20:25 local (-06:00). Self-test 14:20:31 to 14:20:54 (PASS model beam). D1 14:21 to 14:26. D2 14:25 to about 14:37.
D3 14:37 to 14:40. End time: see the final message. The task list in the brief was done in order: D1, D2, D3.

| Task | Status | Done | Not done, and why |
| --- | --- | --- | --- |
| Self-test | PASS | model, beam | none |
| D1 need, not a drawing | done | restate, two ideas with pictures, mount, STEP/STL, assembly picture, removal steps, fit checks, one study (3 meshes converged), open area, print | second load and support ways (not needed by the rules: the peak did not rise with refinement; the load is not rigid) |
| D2 two halves round a bearing | partial, valid false | spec table, both halves, ring, screws, pads, assembly, fit check, +Y contact study, bonded twin, +X study, screw loads, contact proof | convergence (the 2.2 mm and finer meshes exceed the 200k cap; D2_Y_22 refused before solve at 224,652 nodes); D2_X_22, D2_Y_17 and D2_X_17 were not run for the same reason |
| D3 six plates, then a change | done | table check, six plates, edit to six `_b` plates, tables, pictures | none |

**Waits and work.** SolidWorks launches took about 6 s each (keeper running). Solves: D1 under 30 s each; D2 about 104 s each, followed by
readback of about 2.5 min per study at 160k nodes (the instance stayed `busy` through readback). Waiting was about 40 min in total
(mostly D2 readback and solve, and the background job); working was the rest. The clock was not the limit in any task.

**Runs that failed before they worked.** (1) D3 part one: the first build stopped at a hole-coordinate check, because the helper's
`expect()` is relative for a non-zero wanted value and a coordinate that should be 0 failed on float noise (6e-17). Fixed by an
absolute check on hole x and y in `plates.py`; the rerun passed all six plates. (2) D2 build: none failed. (3) D1 modelling: none.

**Plan defects (what the plan said, what happened, what I did):**
- D2 plan section 7: `static()` mesh estimate of 55,000 nodes at el 3.0 with the plan's controls; the actual was 160,773. The plan's
  node count ignores that the local controls dominate the count. I checked the fixture and load boxes, reaction and displacement,
  and kept the stresses (the playbook's stop rule was triggered, the cause found in the estimate, not the model).
- D2 plan: the second and third mesh rows (2.2 mm and finer) are over the 200,000-node cap. The plan's branch (refine with
  el=1.9, then report two rows) cannot be done under the cap with the same controls; I reported convergence as not shown.
- D2 plan section 7: `d2_fea.py` imports `SCREWS` and `G2` from `d2_build`, which runs the build. I copied the two constants into `d2_fea.py`.
- D2 plan section 7: the material key `ring-` does not match the body name `<ring>-<RINGBORE>`. Changed to `ring`; the log confirmed `Steel`.
- D2 plan section 4: `plane(d, 'X', 0.0, '')` and `plane(d, 'Y' ...,'')` in the pads. Given names; no effect on the result.
- D2 fit check (STL): the ring-to-seat test at r 25.97 gives 54 hits per half at the crown. This is facet error on the STL (the B-rep
  seat box reads +-26.095). Reported as inconclusive at 0.03 mm, not as a clash.
- D1 plan section 5: the tilt check reads 49.7 and 59.8 at 55 deg, the plan says 49.6 and 59.8 (rounding). No tilt meets both limits.
- D3 plan section 3: `expect()` relative tolerance on hole coordinates (above). The plan's `walls()`, `measure()` and table are right.
- D2 plan section 8: the preload and torque formulas give 369 N and 222 N mm; they are hand values from the plan's formula, not run.

**Helper defects and gaps (for the playbook or swkit owners):**
- `swkit.expect()`: tolerance is relative when the wanted value is non-zero, absolute when it is zero or -0.0; a coordinate computed
  from cos and sin of 90 deg is not zero but 6e-17, so a 0.03 mm absolute check fails. A "absolute" flag would prevent this.
- `static()` prints no fixture or load box for contact studies (the boxes appeared for D1 but only once for D2 before the solve).
- The node count is not predicted from the global size when local controls cover most faces (see D2 above). Predict from a mesh
  that has been run, or print a mesh-only count before the solve.
- `common.minutes()` counts from the import of `common`, not from the start of the task. I wrote times from the clock instead.

**What was not verified.** D1: second load way and second support way; mass and print by a slicer. D2: case X contact reversal proof,
convergence of any measure, preload and friction, insert pull-out, the as-printed seat. D3: walls on the mesh (not measured).

**Left in the worktree.** Models and exports are in `_wip/sw-eval/haiku-plan-d/` (gitignored). Scripts, `REPORT.md`, `results.json`
and `pictures/` are in `eval/haiku-plan-d/`. Nothing is committed or pushed.
""")
log('run notes written at', minutes(), 'min')
