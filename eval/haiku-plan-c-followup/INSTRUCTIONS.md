# Follow-up for `haiku-plan-c`, set C task C2: instructions R1 to R6

For the builder of `eval/haiku-plan-c/`. Do the steps in order, literally.

Rules for the whole round:

- Work only in `eval/haiku-plan-c-followup/` (this folder). Models and exports go to
  `_wip/sw-eval/haiku-plan-c-followup/`; the scripts do that by themselves because they take the run name from the
  folder. **Never write to `eval/haiku-plan-c/` or `_wip/sw-eval/haiku-plan-c/`.**
- Verdicts come only from `swfea.judge()` as `c2_fea.py` prints them. Times come only from `swkit.stamp()`
  (`times.log` in this folder). Numbers come only from runs. Do not decide anything by looking at a picture.
- Session rules as in the first round (`playbook/01-session.md`: worktree, `--status`, claim; release the claim at
  the end). Run every command from `eval/haiku-plan-c-followup/`, in the foreground, never under `timeout`.
- Do not commit and do not push.
- Budget: 60 minutes on this folder's clock. At 50 minutes start no new branch: go to R5 and R6 with what exists.

What this round changes, and why (measured by the reviewer on your STL):

1. The stem is pinched: at Z -74 it is 8.6 mm half-wide where the table says 11.9, and it bulges at Z -94. The
   section rows are 25 to 30 mm apart there. This round adds one row in each long gap. The same fault is the likely
   reason idea B's window split the stem.
2. With layers along Y the verdict is fail 1.58 and thicker tables did not help. With layers along X your own rows
   give `pass`, 2.38. This round studies and reports the part for layers along X, standing on its -X edge.
3. Idea B has no picture yet.

Two helper files are already in this folder: `apply_edits.py` and `r_tools.py`. Do not edit them.

## R1. Set up

1. `python apply_edits.py`
   Expected last line: `EDITS OK: 23 pieces replaced in 4 files; 8 files copied`.
   If it stops with "expected N of this piece, found M": nothing was written. Report that line and stop the round.
2. `python -c "from common import *; stamp(HERE, 'follow-up start')"`
3. `python -c "import json; from common import *; put('C1', **json.loads((HERE.parent / 'haiku-plan-c' / 'results.json').read_text(encoding='utf-8-sig'))['C1'])"`
   Expected: `results.json` in this folder now has `C1` with `mass_g` 261.13.
4. `python -c "import shutil; from common import *; WIP.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / '_wip' / 'sw-eval' / 'haiku-plan-c' / 'link_boxy.stl', WIP / 'link_boxy.stl')"`
   If that file is missing, copy `eval/haiku-plan-c/exports/link_boxy.STL` to
   `_wip/sw-eval/haiku-plan-c-followup/link_boxy.stl` instead (lower-case name).
5. `python -c "from common import *; stamp(HERE, 'C2 start')"`

## R2. Both ideas, each with a picture

1. `python c2_ideas.py`
   Expected: idea A built, idea B built, `pictures/idea_a.png` and `pictures/idea_b.png` exist, B not eligible
   (hand factor 0.89 for the load along Y).
2. `python r_tools.py slice ../../_wip/sw-eval/haiku-plan-c-followup/idea_a.stl`
   Expected last line: `PINCH_CHECK ok` (half width at Z -74 between 11.0 and 13.2; the first round had 8.5).
3. Branches. At most three runs of `c2_ideas.py` in this round, counting the first.
   - **`PINCH_CHECK fail`:** in `common.py` change
     `ATTEMPTS = (('arcs4', 'stem first'), ('arcs4', 'hub first'), ('closed', 'stem first'),` to
     `ATTEMPTS = (('closed', 'stem first'), ('arcs4', 'stem first'), ('arcs4', 'hub first'),`,
     run `c2_ideas.py` and the slice command again. If it still says fail: leave the change in, go on, and write in
     the report "the stem pinch at Z -74 remains" with the table `r_tools.py` printed.
   - **B did not build, error names the stem volume:** take the measured stem volume V from the log line
     `STEM: mode ..., added V mm3` of the last B try. In `common.py` set `STEM_VOL['STEM_B']` to V and
     `FORM_VOL['STEM_B']` to V minus 19400. Run again.
   - **B did not build, error is "expected one body" or names the window:** in `common.py` replace the two lines of
     `WINDOW_B = [...]` by the one line
     `WINDOW_B = [(0.0, -36.0), (4.8, -38.5), (7.8, -46.0), (7.1, -60.0), (5.7, -80.0), (4.5, -100.0), (3.0, -118.0), (0.0, -128.0)]`
     and set `FORM_VOL['STEM_B']` to 87000.0. Run again.
   - **B still has no picture after the third run:** write "two ideas, each with a picture: not met" in the report
     with the last error, and go on.
4. Whatever `c2_ideas.py` chose, this round goes on with the bone and the thicker neck:
   `python -c "from common import *; put('C2', chosen='A', table_name='STEM_A2', window=False)"`
   Write in the report: "B was built for the comparison; the choice of A was made in the first round by the rule",
   and quote `eligible` and `choice_reason` from `results.json` as the script wrote them.
5. In `REPORT.md`, fill the two lines the script left as "WRITE THIS LINE BY HAND" (one line each: what the picture
   shows). They describe; they decide nothing.

## R3. The part

1. `python c2_detail.py`
   Expected: `fixed_items_ok` true with all 33 items, one body, STL watertight with one shell,
   `mass_after_g` 119 plus or minus 4 (limit 261.13), stem volume 103700 plus or minus 3 %.
   The hub blend is now tried at R 2 and R 1.2; if it is undone the script goes on, and that is fine.
2. `python r_tools.py slice ../../_wip/sw-eval/haiku-plan-c-followup/link_organic.stl`
   Expected: `PINCH_CHECK ok`. Copy the printed table into the report whatever it says.
3. `python r_tools.py print ../../_wip/sw-eval/haiku-plan-c-followup/link_organic.stl`
   Expected: `PRINT_CHECK ok`; for "layers along X, -X edge on the bed": footprint 44 x 249, height 72,
   `bed_contact_mm2` about 10 (under 30), `supported_area_mm2` 4300 plus or minus 500. It writes `printability.json`.
4. Branches.
   - **`c2_detail.py` stops in or just after the blend:** `python c2_detail.py noblend`.
   - **`c2_detail.py` stops at "finished volume against the planner number" or "stem volume":** this is the loft.
     Do the `ATTEMPTS` change of R2 if it is not in yet and run again. If it stops again, take the three added rows
     (Z -72.0, -100.0, -130.0) out of the `STEM_A2` block in `common.py`, run again, and write in the report "built
     from the first round's table; the pinch remains".
   - **A fixed item fails:** do not go on to R4. Report the item and its value and stop the round at R6.
   - **`PINCH_CHECK fail` here but the part built:** go on; the report says the pinch remains, with the table.
   - **`PRINT_CHECK fail`:** go on; the report says the part does not fit the bed standing on its edge.
5. Fill the "WRITE THIS LINE BY HAND" line for `checkpoint_02.png`.

## R4. The study, layers along X

1. `python c2_fea.py fresh`
   Expected: ten studies, about 9 minutes. `VERDICT pass`, lowest factor between 2.1 and 2.7, lowest entry
   "+Y, shear" or "+Y, layer", place at the neck (Z between -30 and -36). Von Mises should be lower than the first
   round's 17.4 MPa if the pinch is gone.
2. Quote from the script's output and nothing else: the verdict, the lowest factor, the lowest entry.
3. Copy into the report the line the script wrote that begins "The three measures for layers along X at the finest
   mesh, read outside 2, 3 and 5 mm". Then compute for the 2.0 mm reading of "+Y": 22.5 divided by its `layer` and
   13 divided by its `shear`. Write both numbers. If either is under 2.0, write this sentence with the numbers:
   "Read 2 mm from the held face instead of 3 mm, the factor is X.XX; the verdict uses 3 mm, as fixed in the plan."
4. Branches.
   - **Verdict `fail`:** once only:
     `python -c "from common import *; put('C2', table_name='STEM_A3')"`, then `python c2_detail.py`, the two
     `r_tools.py` commands of R3, `python c2_fea.py fresh`. If it is `fail` again, stop trying: C2 is "not done:
     requirement not met"; report both verdicts.
   - **Verdict `margin, not converged` or `not shown`:** do not change anything and do not call it a pass. C2 is
     "not done: verdict <the word judge() gave>", with the entry that moves and its three values.
   - **A mesh is refused, or a study stops on the prediction check:** the branches of
     `eval/plans-fable-c/C_C2.md` for those two cases, as in the first round.

## R5. Finish

1. `python c2_finish.py`
   Expected last line: `C2 FINISHED` with `gate` all four true and `verdict` "pass".
   C2 is **done** only if all four gate items are true **and** the verdict word is exactly `pass`. Anything else is
   "not done" with the reason.
2. `python -c "from common import *; print(len((HERE / 'DESIGN.md').read_text(encoding='utf-8-sig').strip().splitlines()))"`
   Expected: 25 or less.
3. Edit `DESIGN.md` only in these cases, and keep it at 25 lines or less:
   - idea B did not build: replace "None g" in the idea B line by "did not build".
   - `PINCH_CHECK` failed in R3: add to the end of the last line: " The loft pinches the stem to H mm half-width
     at Z -74 where the table says 12.0; not fixed." with H from the slice table.
   - `PINCH_CHECK` passed in R3: add to the end of the last line: " First round: the loft pinched the stem to
     8.6 mm half-width at Z -74; fixed by evenly spaced rows."
4. Fill the "WRITE THIS LINE BY HAND" line for `c2_before_after.png`.

## R6. Report

End `REPORT.md` in this folder with these, every number from `results.json`, `printability.json`, the script output
or `times.log`:

1. The table of states: C2 `done` or `not done: <reason>`, with the gate table `c2_finish.py` wrote.
2. One table, first round against this round: table name, mass g, verdict, lowest factor, lowest entry, print
   direction, half width at Z -74, idea B built (yes or no), hub blend radius (or "none").
3. The print statement: `print_orientation` from `results.json`, then the three numbers for "layers along X, -X edge
   on the bed" from `printability.json` (bed contact, supported area, height), then this sentence: "Printing on edge
   is what makes the factor; it rests on a raft and supports. Whether that is acceptable is Joey's decision."
4. Every branch taken in R2 to R4, with the error line that sent you there.
5. Times: one row per step R1 to R5 with the two `times.log` lines it lies between, and the total. `c2_ideas.py`
   runs: how many, and why each.
6. Anything in these instructions or in `apply_edits.py` / `r_tools.py` that was wrong or did not work as written.

Then close SolidWorks, release the claim, and stop. Do not commit or push.
