# Fourth round for `haiku-plan-c`, set C task C2: instructions U1 to U5

For the builder of `eval/haiku-plan-c-round3/`. This round is the third round again with one more stem table. Do
exactly what `eval/haiku-plan-c-round3/INSTRUCTIONS.md` says in T1 to T5, with these substitutions and nothing else:

| Where round 3 says | Use |
| --- | --- |
| `eval/haiku-plan-c-round3/`, `_wip/sw-eval/haiku-plan-c-round3/` | `eval/haiku-plan-c-round4/`, `_wip/sw-eval/haiku-plan-c-round4/` |
| `python apply_edits3.py`, expected `EDITS OK: STEM_A4 added; 6 files copied` | `python apply_edits4.py`, expected `EDITS OK: STEM_A5 added; 6 files copied` |
| `put('C2', table_name='STEM_A4')` | `put('C2', table_name='STEM_A5')` |
| stamp `'round 3 start'` | stamp `'round 4 start'` |
| copy `link_boxy.stl` from `haiku-plan-c-round2` | the same source, `haiku-plan-c-round2` |
| stem volume 111640 plus or minus 4 %, mass between 125 and 132 | stem volume 112000 plus or minus 4 %, mass between 125 and 133 |
| DESIGN.md sentence | " Round 4: neck lowered beside the screw pockets and thickened under the cable tunnel (STEM_A5) after round 3 failed at 1.39; verdict V, lowest factor F." |
| report table "round 2 (STEM_A3) against round 3" | three columns: round 2 (STEM_A3), round 3 (STEM_A4), round 4 (STEM_A5) |
| commit message when saving | "eval: the Haiku organic link fourth round as run" |

Never write to the earlier rounds' folders. No hold applies now, but run `python ../../solidworks/sw_instance.py
--status` before the first SolidWorks job as round 3 says.

Why (measured on round 3's results): the deeper neck moved the failure. Round 3 failed in two places under the load
along Y: shear between layers 9.3 MPa at the edge of a lower screw-head pocket (X -9, Y 4.2, Z -22.4), because the
neck now stood 3 mm higher beside the pocket; and tension across layers 13.2 MPa on the underside of the cable
tunnel at Z -34.5, where only 0.3 to 1.8 mm of material lay under the tunnel. `STEM_A5` lowers the neck beside the
pockets again and puts 3 mm or more under the tunnel. The reviewer's estimate, not a promise: lowest factor between
1.7 and 2.2.

One extra branch in the part step: **the mounting-face area or "one flat face at Y -4" check fails:** the lowered
underside has reached the mounting ring. Quote the line and stop the round at the report step. Do not change numbers.

One extra line in the report: for the load along Y at the finest mesh, the von Mises, across-layers and
between-layers values of the chosen print direction with their places, round 3 against round 4.

When the report is written, save this folder and its solver logs to branch plan-c-loop as before (Joey's approval
for tonight's runs covers it), and give the hash in the final report.
