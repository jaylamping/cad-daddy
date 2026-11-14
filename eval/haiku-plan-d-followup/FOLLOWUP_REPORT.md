# Follow-up report, run haiku-plan-d (set D)

Clock: eval/haiku-plan-d/times.log. Follow-up start 15:38:20. R3 convergence jobs done 15:59:40 (21.3 min). R4 D1 run done 16:01:08.

## R3a: which body moves 0.555 mm (D2_X_30, no SolidWorks)

- The largest displacement is the ring: 0.5548 mm at (12.12, -23.00, 7.00). Upper half 0.20 mm, lower 0.05 mm, screws 0.16 mm, pads 0.42 mm (104 nodes).
- Ring tangential mean 0.384 mm (rotation 0.0148 rad). Rigid fit (translation plus a turn about Z): turn 0.86 degrees, residual mean 0.02 mm, max 0.53 mm at a few nodes.
- Decision: a rigid turn of the ring with a local deviation, harmless. The brief said "near 0.5 mm"; 0.38 is close and the residual is small. Scripts: eval/haiku-plan-d/d2_step_a.py and d2_step_a_fit.py. Logs: eval/haiku-plan-d/wip-logs/d2_step_a.log and d2_step_a_fit.log.

## R3b: results.json corrections (no run)

- sf_yield 7.34, sf_layer 20.94, sf_shear 5.82, the governing line, pads_share_n 0.23, and the "why" note. Applied as written.

## R3c: convergence series (case X job, then case Y job)

- Script: eval/haiku-plan-d/d2_conv.py. run_c copies run; only the control sizes change (steel 1.5, PETG 0.8, and the three control bands as the brief sets). The picks and their counts are unchanged.
- Rows (global el 4.0; control cs 1.2, 0.9, 0.7): nodes 122,208 / 151,706 / 195,921. None refused (all under 200,000), so the el 5.0 and steel 2.0 fallbacks were not needed.
- Screw nodes per screw 456 / 456 / 461 / 461, so the steel 1.2 fallback was not needed.
- First check (D2C_X_12 against D2_X_30): reaction 300 N. Screw tensions 41.3, 39.4, 48.1, 47.7 N against 41.3, 40.8, 49.5, 48.6 N (all within 3.4 %). Angles 9.97 and 56.09 degrees against 9.4 and 56.1 (within 5 degrees). Lower Z shear 2.02 against 2.23 (-9.4 %). Upper Z von Mises 5.65 against 6.13 (-7.8 %). PASS, so the series went on.
- Case Y check (D2C_Y_12): four screw tensions 76.1, 74.3, 75.1, 75.5 N against 75 N (within 15 %). PASS.

Logs: eval/haiku-plan-d/wip-logs/d2_conv_X.log, d2_conv_Y.log, d2_conv_report.log. Rows: eval/haiku-plan-d/d2c_rows.json.

| Entry (layers along Z) | 1.2 / 0.9 / 0.7 | step % |
|---|---|---|
| upper half, +X, vm | 5.65 / 5.90 / 6.10 MPa | +4.4, +3.4 |
| upper half, +X, layer | 0.89 / 0.90 / 0.71 MPa | +1.1, -21.1 |
| upper half, +X, shear | 1.48 / 1.37 / 1.40 MPa | -7.4, +2.2 |
| lower half, +X, vm | 5.17 / 5.83 / 6.49 MPa | +12.8, +11.3 |
| lower half, +X, layer | 1.04 / 1.00 / 1.43 MPa | -3.8, +43.0 |
| lower half, +X, shear | 2.02 / 2.43 / 3.12 MPa | +20.3, +28.4 |
| upper half, +Y, vm | 4.60 / 4.45 / 4.59 MPa | -3.3, +3.1 |
| upper half, +Y, layer | 0.91 / 0.90 / 0.74 MPa | -1.1, -17.8 |
| upper half, +Y, shear | 1.31 / 1.40 / 1.81 MPa | +6.9, +29.3 |
| lower half, +Y, vm | 2.70 / 2.66 / 2.63 MPa | -1.5, -1.1 |
| lower half, +Y, layer | 0.77 / 0.70 / 0.67 MPa | -9.1, -4.3 |
| lower half, +Y, shear | 0.61 / 0.58 / 0.64 MPa | -4.9, +10.3 |

Excluded (screw and fixture zones) von Mises, upper / lower: case X 12.0 / 6.5, 12.8 / 6.5, 12.2 / 6.5 MPa; case Y 8.6 / 5.4, 9.3 / 6.1, 8.6 / 6.0 MPa.

Upper half with the wider zone round the heads (dxz < 4.75 and y > 26.5, in place of 3.75 and 27.5): the peak leaves the zone edge. Case X von Mises falls from 5.65 / 5.90 / 6.10 to 3.73 / 3.71 / 3.71 MPa. Case Y falls from 4.60 / 4.45 / 4.59 to 3.20 / 3.18 / 3.54 MPa. Upper layer and shear change little.

### judge() output (verdict and lowest factor are judge's, not mine)

- Verdict: **margin, not converged**. Lowest factor **4.17** at "lower half, +X, shear" (need 2.0).
- Entries not at pass: upper +X layer 31.69 (21.1 % last step); lower +X vm 6.93 (11.3 %); lower +X layer 15.73 (43.0 %); lower +X shear 4.17 (28.4 %, factor after two more steps 2.53); upper +Y layer 30.41 (17.8 %); upper +Y shear 7.18 (29.3 %, after two more 4.3); lower +Y shear 20.31 (10.3 %).
- Full output is in results.json under D2.judge.

**D2 state.** Model checks 1 to 5 pass, so the result is valid. The verdict is `margin, not converged`, with a lowest factor of 4.17 (down from 5.82 on the 3.0 mm mesh alone). The lower-half shear between layers still climbs 20 % and 28 % per step. Two more steps would put it at 2.53. The task is **not closed**: convergence is not shown. The lower-half shear is the next thing to resolve (a finer or local refinement at the split seam, or a change to the governing layer). I did not run that.

## R4: D1 with the log kept and the hidden section read

- Log: eval/haiku-plan-d/wip-logs/d1_study.log. Convergence rows (el 2.0 / 1.5 / 1.1; nodes 30,598 / 58,907 / 125,748): vm 2.47 / 2.49 / 2.49 MPa; layer tension 0.17 / 0.13 / 0.13; layer shear 0.70 / 0.70 / 0.71. Converged. Max displacement 0.158 mm (predicted 0.09 mm; the compare check passed).
- Plateau (outside 1, 2, 3, 5 mm of fixture and load faces): vm 2.49 MPa in every case; layer Z 0.126 (1, 2, 3 mm) and 0.119 (5 mm); shear Z 0.708.
- Spine round the M5 holes: vm max 1.61 MPa in the box; mean sigma-x on the top face 0.45 MPa.
- Hand value for the spine beside an M5 hole: 1.94 MPa nominal, about 5.8 at the hole edge. The study does not show that: its spine peak is 1.61 MPa. I report the study number and flag the gap. I do not know which is right without a finer look at the hole edge.
- Outside 1 mm the peak is 2.49 MPa, under 22.5 MPa, so the part passes there too.
- sf_min: the lower of the arm-root factor (45 / 2.49 = 18.07) and 45 / 1.61 = 27.9 for the spine. **Arm root governs: sf_min 18.07.**
- Hand values for the X and Y directions, 1.35 and 1.2 MPa, are recorded here as hand values only. The study did not check them.

## R5: paper corrections

- REPORT.md has a dated correction: D2 took about 12 minutes; the whole set about 20. The follow-up convergence jobs themselves ran 10.9 and 10.7 min per times.log.

## Task states (set D)

- **D1: closed.** Converged over three sizes (2.47 / 2.49 / 2.49 MPa). Spine and plateau read. sf_min 18.07 (arm root).
- **D2: not closed.** Model valid. Verdict `margin, not converged`, lowest factor 4.17 (judge). Needs convergence of the lower-half shear.
- **D3: no change.** The follow-up brief had no D3 run; results.json holds the first-run result.

## Notes

- The worktree's git status shows many eval/ files as deleted. This is not from this run and I did not touch them.
- Claim sw-eval-haiku-plan-d was taken for this run and released at the end.
