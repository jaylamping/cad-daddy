# Third round for `haiku-plan-c`, set C task C2: instructions T1 to T5

For the builder of `eval/haiku-plan-c-round2/`. Do the steps in order, literally.

Rules for the whole round: as in the second round (its INSTRUCTIONS.md, "Rules for the whole round"), with this
folder, `eval/haiku-plan-c-round3/`, in place of that one. **Never write to the earlier rounds' folders.** Do not
commit and do not push. Budget: 30 minutes on this folder's clock. Before the first SolidWorks job, run
`python ../../solidworks/sw_instance.py --status`: if another thread's instance is busy at the splash or loading,
wait five minutes and look again, at most three times, then go on.

What this round changes, and why: the second round fixed the stem (twist gone, full width) and failed at the neck,
where the stem leaves the hub: tension across the layers under the load along Y, at Z -34.5, factor 1.38 with
`STEM_A2` and 1.57 with `STEM_A3`. This round builds `STEM_A4`: the same stem with a deeper and wider neck between
Z -27 and Z -60 (about 1.45 times the section modulus at Z -32). Nothing else changes: same loft pick, same print
direction (tilted 30 degrees towards +X, hub end down), same study.

Two helper files are already in this folder: `apply_edits3.py` and this file. Do not edit them.

## T1. Set up

1. `python apply_edits3.py`
   Expected last line: `EDITS OK: STEM_A4 added; 6 files copied`. If it stops: report the line and stop the round.
2. `python r2_tools.py setup`, then
   `python -c "from common import *; put('C2', table_name='STEM_A4'); stamp(HERE, 'round 3 start'); stamp(HERE, 'C2 start')"`
3. `python -c "import shutil; from common import *; WIP.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / '_wip' / 'sw-eval' / 'haiku-plan-c-round2' / 'link_boxy.stl', WIP / 'link_boxy.stl')"`

## T2. The part

1. `python c2_detail.py`
   Expected: `fixed_items_ok` true with all 33 items, one body, STL watertight with one shell, stem volume 111640
   plus or minus 4 %, `mass_after_g` between 125 and 132 (limit 261.13).
2. `python r2_tools.py twist ../../_wip/sw-eval/haiku-plan-c-round3/link_organic.stl` (expected `TWIST_CHECK ok`)
3. `python r2_tools.py slice ../../_wip/sw-eval/haiku-plan-c-round3/link_organic.stl` (expected `PINCH_CHECK ok`)
4. `python r2_tools.py orient ../../_wip/sw-eval/haiku-plan-c-round3/link_organic.stl`
   Expected `PRINT_CHECK ok`: height 222 plus or minus 2, support 700 plus or minus 250 mm2.
   Copy the three printed tables into the report whatever they say.
5. Branches. At most two runs of `c2_detail.py`.
   - **Stops at "screw-head scallops are shallow":** the deeper neck now covers more of the two lower screw heads.
     Quote the line. If the number is under 200, open `c2_detail.py`, change `abs_tol=60.0` on that one line to
     `abs_tol=170.0`, run again, and write in the report "screw-head pockets at the two lower screws are N mm3
     (30 expected by the first plan)". If it is 200 or more: stop the round at T5 with that line.
   - **Stops at "stem volume" or "finished volume":** quote the line and stop the round at T5. Do not change numbers.
   - **A fixed item fails:** report the item and its value and stop the round at T5.
   - **`c2_detail.py` stops in or just after the blend:** `python c2_detail.py noblend`.
   - **Any of the three checks says fail but the part built:** go on; the report says which and by how much.
6. Fill the "WRITE THIS LINE BY HAND" line for `checkpoint_02.png`.

## T3. The study

1. `python c2_fea.py fresh`
   The reviewer's estimate, not a promise: lowest factor between 1.9 and 2.4, still "+Y, layer" at the neck.
2. Quote from the script's output and nothing else: the verdict, the lowest factor, the lowest entry and its place.
3. The nine direction lines as in the second round's S4.3 (readings, not verdicts).
4. Whatever the verdict is, change nothing and run nothing again. `pass`: C2 is done if the gate is all true.
   Anything else: C2 is "not done: verdict <the word judge() gave>", with the entry and its three values.

## T4. Finish

1. `python c2_finish.py`
2. `python -c "import shutil; from common import *; [shutil.copyfile(WIP / n, HERE / 'exports' / n) for n in ('link_organic.stl', 'link_organic.step') if (WIP / n).exists()]; print(sorted(p.name for p in (HERE / 'exports').iterdir()))"`
3. `DESIGN.md`: 25 lines or less. Add to the end of its last line: " Round 3: neck deepened (STEM_A4) after the
   second round failed there at 1.57; verdict V, lowest factor F." with V and F from the script.
4. Fill the "WRITE THIS LINE BY HAND" line for `c2_before_after.png`.

## T5. Report

End `REPORT.md` with: (1) the state and the gate table; (2) one table, round 2 (STEM_A3) against round 3: mass,
verdict, lowest factor, lowest entry and place, largest twist, half width at Z -78, support area and height of the
chosen print direction; (3) the patches of the chosen direction with their places; (4) the nine direction lines;
(5) branches taken with the line that sent you there; (6) times per step from `times.log` and the total;
(7) anything in these instructions or the helper files that was wrong or did not work as written.

Then close SolidWorks, release the claim, and stop. Do not commit or push.
