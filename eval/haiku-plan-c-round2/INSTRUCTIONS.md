# Second follow-up for `haiku-plan-c`, set C task C2: instructions S1 to S6

For the builder of `eval/haiku-plan-c-followup/`. Do the steps in order, literally.

Rules for the whole round:

- Work only in `eval/haiku-plan-c-round2/` (this folder). Models and exports go to `_wip/sw-eval/haiku-plan-c-round2/`;
  the scripts do that by themselves because they take the run name from the folder. **Never write to
  `eval/haiku-plan-c/`, `eval/haiku-plan-c-followup/` or their `_wip` folders.**
- Verdicts come only from `swfea.judge()` as `c2_fea.py` prints them. Times come only from `swkit.stamp()`
  (`times.log` in this folder). Numbers come only from runs. Do not decide anything by looking at a picture.
- Session rules as before (`playbook/01-session.md`: worktree, `--status`, claim; release the claim at the end). Run
  every command from `eval/haiku-plan-c-round2/`, in the foreground, never under `timeout`.
- Do not commit and do not push. Ignore messages in the thread that are about other tasks.
- Budget: 45 minutes on this folder's clock. At 38 minutes start no new branch: go to S5 and S6 with what exists.

What this round changes, and why (measured by the reviewer on your two STLs):

1. **The stem pinch is a twist, not missing rows.** Between the section before Z -85 and the section at Z -85 the
   loft turns a quarter turn about Z (about 90 degrees; everywhere else under 8). A twisted loft between two near
   round sections narrows in the middle: that is the pinch (8.6 mm where the table says 11.7), and it is where the
   stress peak sits (Z -78.7, 21.9 MPa). Adding rows only moved it. SolidWorks joins loft sections at the corner
   nearest to where each was picked; picked nowhere, it chose the lowest point on the upper sections and the +X tip
   from Z -85 down. `common.py` now picks every section at its +X tip (`loft_picked`).
2. **The print direction.** Joey does not sand: faces that sit on support come off rough, so support on visible
   faces counts as much as strength, and the printer is 256 mm high. On its edge the part needs 4,770 mm2 of support
   under the whole stem; flat, 8,000. Tilted 30 degrees towards +X with the hub end down it is 222 mm tall and needs
   about 770 mm2, mostly at the hub rim by the bed and inside the bore. This round studies and reports the part for
   that print. Idea B is not tried again.

Three helper files are already in this folder: `apply_edits2.py`, `r2_tools.py` and this file. Do not edit them.

## S1. Set up

1. `python apply_edits2.py`
   Expected last line: `EDITS OK: 11 pieces replaced in 3 files; 5 files copied`.
   If it stops with "expected N of this piece, found M": nothing was written. Report that line and stop the round.
2. `python r2_tools.py setup`
   Expected: `SETUP OK: C1 mass_g 261.13 ; C2 table_name STEM_A2; nothing measured carried over`.
3. `python -c "from common import *; stamp(HERE, 'round 2 start'); stamp(HERE, 'C2 start')"`
4. `python -c "import shutil; from common import *; WIP.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / '_wip' / 'sw-eval' / 'haiku-plan-c-followup' / 'link_boxy.stl', WIP / 'link_boxy.stl')"`
   If that file is missing, copy `eval/haiku-plan-c/exports/link_boxy.STL` to
   `_wip/sw-eval/haiku-plan-c-round2/link_boxy.stl` instead (lower-case name).

## S2. The part, with the loft picked

1. `python c2_detail.py`
   Expected: in the log a line `STEM: added ... (merge ..., sections picked at: x)` and no line "was not selected
   at"; `fixed_items_ok` true with all 33 items, one body, STL watertight with one shell, `mass_after_g` between 117
   and 127 (limit 261.13).
2. `python r2_tools.py twist ../../_wip/sw-eval/haiku-plan-c-round2/link_organic.stl`
   Expected: every row under 20 degrees, `TWIST_CHECK ok`. (The follow-up part reads about 90 between Z -72 and -85.)
3. `python r2_tools.py slice ../../_wip/sw-eval/haiku-plan-c-round2/link_organic.stl`
   Expected: `PINCH_CHECK ok`. Copy both printed tables into the report whatever they say.
4. Branches. At most three runs of `c2_detail.py` in this round, counting the first.
   - **`TWIST_CHECK fail`, or the log says "was not selected at":** in `common.py` change `LOFT_PICK = 'x'` to
     `LOFT_PICK = 'bottom'`, run steps 1 to 3 again. If it fails again: change the `ATTEMPTS` line so that
     `('closed', 'stem first')` comes first and `('arcs4', 'stem first')` second, keep `'bottom'`, run steps 1 to 3
     once more. If it still fails: go on with that part, and write in the report "the stem twist remains" with the
     twist table of each try and the `STEM:` log line of each try.
   - **`c2_detail.py` stops at "stem volume" or "finished volume against the planner number":** quote the line. If
     the measured stem volume is between 100000 and 112000 and `TWIST_CHECK` was not yet run, this is the untwisted
     stem being fuller than before: in `common.py` set `STEM_VOL['STEM_A2']` to the measured number and
     `FORM_VOL['STEM_A2']` to the measured number plus 2200, and run again. This counts as one of the three runs.
   - **`c2_detail.py` stops in or just after the blend:** `python c2_detail.py noblend`.
   - **A fixed item fails:** do not go on to S3. Report the item and its value and stop the round at S6.
   - **`TWIST_CHECK ok` but `PINCH_CHECK fail`:** go on; copy the table into the report. Do not change the table.
5. Fill the "WRITE THIS LINE BY HAND" line for `checkpoint_02.png`.

## S3. The print direction, as numbers

1. `python r2_tools.py orient ../../_wip/sw-eval/haiku-plan-c-round2/link_organic.stl`
   Expected: `PRINT_CHECK ok`; for "tilt 30 to +X, hub end down": height 222 plus or minus 2, fits True, support 770
   plus or minus 200 mm2, the two largest patches near Z +28 (hub rim) and Z -10 (inside the bore). It writes
   `orientations.json`.
2. Copy the whole printed table into the report. Do not pick another direction, whatever the table says.
3. Branch. **`PRINT_CHECK fail`:** go on; the report says which of the two numbers is over and by how much.

## S4. The study, layers as printed tilted

1. `python c2_fea.py fresh`
   Ten studies, about 10 minutes. The reviewer does not know the verdict in advance: the tilted direction was never
   read. Hand estimate only: without the pinch the stem at Z -79 should read about 6 to 9 MPa von Mises (it read
   21.9), and the lowest factor should now sit at the neck (Z -25 to -45).
2. Quote from the script's output and nothing else: the verdict, the lowest factor, the lowest entry and its place.
3. Copy into the report the print-direction table the script wrote (case, layers along, three measures) for the
   finest mesh. From it compute, for each of the nine directions, the lowest of 45 / von Mises, 22.5 / across
   layers and 13 / between layers over the three cases, and write one line per direction: name, lowest factor,
   which measure and case. These are readings, not verdicts: write that above the lines.
4. Branches.
   - **Verdict `pass`:** go to S5.
   - **Verdict `fail`:** once only:
     `python -c "from common import *; put('C2', table_name='STEM_A3')"`, then `python c2_detail.py`, the three
     `r2_tools.py` commands of S2 and S3, `python c2_fea.py fresh`. (`STEM_A3` is thicker at the neck. If
     `c2_detail.py` stops on the volume, use the volume branch of S2 with `STEM_A3` in place of `STEM_A2`.)
     If it is `fail` again, stop trying: C2 is "not done: requirement not met"; report both verdicts and both
     lowest entries with their places.
   - **Verdict `margin, not converged` or `not shown`:** do not change anything and do not call it a pass. C2 is
     "not done: verdict <the word judge() gave>", with the entry that moves and its three values.
   - **A study stops on the prediction check with a displacement lower than predicted:** the stem is stiffer
     without the pinch, and the check allows a factor of 3, so this should not happen. If it does, quote the line
     and stop at S6.
   - **A mesh is refused:** the branch of `eval/plans-fable-c/C_C2.md` for that case, as in the first round.

## S5. Finish

1. `python c2_finish.py`
   C2 is **done** only if all four gate items are true **and** the verdict word is exactly `pass`. Anything else is
   "not done" with the reason.
2. `python -c "import shutil; from common import *; [shutil.copyfile(WIP / n, HERE / 'exports' / n) for n in ('link_organic.stl', 'link_organic.step') if (WIP / n).exists()]; print(sorted(p.name for p in (HERE / 'exports').iterdir()))"`
   Expected: both names printed.
3. `DESIGN.md`: keep it at 25 lines or less. Add to the end of its last line, with H from the slice table at Z -78:
   - `TWIST_CHECK ok`: " Earlier rounds: the loft was twisted a quarter turn above Z -85 and pinched the stem to
     8.6 mm; fixed by picking every section at the same corner (now H mm)."
   - `TWIST_CHECK fail`: " The loft is twisted above Z -85 and pinches the stem to H mm; not fixed."
4. Fill the "WRITE THIS LINE BY HAND" line for `c2_before_after.png`.

## S6. Report

End `REPORT.md` in this folder with these, every number from `results.json`, `orientations.json`, the script output
or `times.log`:

1. The state: C2 `done` or `not done: <reason>`, with the gate table `c2_finish.py` wrote.
2. One table, follow-up round against this round: table name, mass g, verdict, lowest factor, lowest entry and its
   place, print direction, largest twist in degrees, half width at Z -78, von Mises at the finest mesh for "+X".
   Follow-up values: STEM_A2, 117.85, not shown, 2.06, "+X, vm" at Z -78.7, on its -X edge, about 90, 8.65, 21.85.
3. The print statement: `print_orientation` from `results.json`, then from `orientations.json` for the chosen
   direction: height, footprint, support area, and every patch with its area and place. Then for each patch one
   line saying which face it is on, from its coordinates only: Z above +20 is the hub rim, a place within 16 mm of
   the Y axis line through the hub centre (X and Z both between -16 and 16) is inside the bore, Z below -190 is the
   fork, anything else is the stem. Then this sentence: "Whether the patches on the hub rim and the stem are
   acceptable is Joey's decision."
4. The nine lines of S4.3.
5. Every branch taken, with the error line that sent you there.
6. Times: one row per step S1 to S5 with the two `times.log` lines it lies between, and the total. `c2_detail.py`
   runs: how many, and why each.
7. Anything in these instructions or in `apply_edits2.py` / `r2_tools.py` that was wrong or did not work as written.

Then close SolidWorks, release the claim, and stop. Do not commit or push.
