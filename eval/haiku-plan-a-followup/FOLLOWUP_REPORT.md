# Follow-up report, run haiku-plan-a (set A)

Times are from `eval/haiku-plan-a/times.log` only. Clock starts at the first stamp (R1 start, 15:22:14 local).
Total: 14.0 min (limit 60 min).

| Step | Start | End | Length |
| --- | --- | --- | --- |
| R1, T5 toe rounding job | 0.0 min (15:22:14) | 2.3 min (15:24:34) | 2.3 min |
| R2b, T6 matched-mesh job | 3.1 min (15:25:23) | 12.3 min (15:34:33) | 9.2 min |
| Follow-up end | | 14.0 min (15:36:17) | |

R2a (T6 read of the saved results, no SolidWorks) and R5 (paper corrections) ran between the stamps, with no SolidWorks.

## R1. T5: rounded rib toes, R2.0 (done, closed)

- Script: `eval/haiku-plan-a/t5_toe.py`. Log: `eval/haiku-plan-a/wip-logs/t5_toe.log`. Rows: `eval/haiku-plan-a/t5_toe_rows.json`. Verdict: `eval/haiku-plan-a/t5_toe_judge.json`.
- Toe fillet built at R2.0 on all 4 rib corners, volume change +1.20 mm3 (hand +1.20). Body count 1, rebuild errors 0, volume 35695.19 mm3.
- Studies (Y print direction table, pads load, base walls fixed):

| Study | Element mm | Nodes | Predicted nodes | Max disp mm | vm MPa | layer MPa | shear MPa |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T5_TOE_30 | 3.0 | 45,729 | 45,000 | 0.904 | 12.85 | 7.28 | 3.59 |
| T5_TOE_22 | 2.2 | 90,202 | 90,000 | 0.907 | 13.25 | 7.47 | 3.92 |
| T5_TOE_16 | 1.6 | 194,421 | 195,000 | 0.910 | 13.54 | 7.52 | 3.98 |

- No refusal; T5_TOE_16 ran at 1.6 mm (fallback 1.8 not needed). All predictions within 3x, displacement within 1 %.
- Peak von Mises now at the upright toe, X 6.3, Y 3.5 / 46.5, Z 33.7, not at a base root (Z 6). The stop rule for a rib-side root at Z 6 does not apply.
- `judge()` output (verbatim from `swfea.judge`): verdict **pass**, lowest factor 2.99 at "layer", need 2.0.
  - vm: 12.85, 13.25, 13.54 MPa, factor 3.32, last step 2.2 %, converged.
  - layer: 7.28, 7.47, 7.52 MPa, factor 2.99, last step 0.7 %, converged.
  - shear: 3.59, 3.92, 3.98 MPa, factor 3.27, last step 1.5 %, converged.
- Mass: 35695.19 mm3 x 1.19e-3 = 42.48 g, +8.25 % against 39.24 g (under the 10 % limit).
- Recorded in `results.json` T5: verdict `pass`, status `done`, sf_yield 3.32, sf_layer 2.99, sf_shear 3.26.
- Decision: the earlier "margin, not converged" note in T5 is kept for history and superseded by this run.

## R2a. T6: where the 0.249 / 0.166 / 0.153 mm is (no SolidWorks, done)

- Read from `_wip/sw-eval/haiku-plan-a/npz/T6_PIN_12/08/05.npz`. Script in the scratchpad (not committed).
- Line mean contact pressure (block nodes at the top of the hole, |x| < 0.25, |y| < 8): **6.08 MPa** (27 nodes, max 6.52) at 1.2; **5.74** (81 nodes, max 5.98) at 0.8; **5.60** (192 nodes, max 6.77) at 0.5. Expected 6.0 to 6.8: met at the coarsest.
- Contact half-width (first node with pressure over 0.3 MPa): largest |x| 1.88 mm at 1.2, hand 1.57 mm. Within the expected scatter, but wider than hand.
- Pin nodes: largest total displacement sits on the pin end at the soft pad, (5.0, -25.0, 9.97): UZ 0.249 mm at 1.2, 0.166 at 0.8, 0.153 at 0.5. Mean pin |UX| 0.053 mm vs max 0.113 at 1.2, so the tangential part is well above its mean.
- Block max total displacement stays at 0.032 mm, so the displacement is not on the block.
- Decision (rule applied as written): "the pin turns or slides on the soft pads; pressure unaffected". Proceeded to R2b.

## R2b. T6: matched-mesh run (done, closed)

- Script: `eval/haiku-plan-a/t6m.py` (`run_m` = `run` from t6.py, with `ctrl=[(hole, c), (mid, c)]`). Opened the saved `block_fea.SLDPRT`, did not rebuild. Log: `eval/haiku-plan-a/wip-logs/t6m.log`. Rows: `eval/haiku-plan-a/t6m_rows.json`.
- No refusal; T6M_06 ran at 0.6 (fallback 0.65 not needed).
- Predicted vs got: T6M_12 45,000 vs 42,660 nodes; T6M_08 84,000 vs 92,444; T6M_06 138,000 vs 164,532. Max displacement predicted 0.13 mm, got 0.184 / 0.163 / 0.140 mm. All within 3x, so the stresses were read.
- Checks on each row: reaction Fz -500.0 N; fz_block -499.8 N; fz_pads -0.20 N (under 5 N); pin rise 0.129 / 0.130 / 0.129 mm (within 0.10 to 0.14). All pass. `lig_force` ignored, as instructed.

| Measure | 1.2 | 0.8 | 0.6 | Last step |
| --- | --- | --- | --- | --- |
| Line mean MPa | 6.07 | 5.73 | 5.64 | 1.6 % (converged, 5 % limit) |
| p_all MPa | 6.74 | 6.21 | 5.98 | -3.7 % (converged) |
| contact_vm MPa | 5.54 | 5.16 | 5.23 | +1.4 % (converged) |

- `valid` = **true**: checks hold, and line mean 5.64 is within 25 % of 6.76 MPa (5.07 to 8.45).
- Converged: yes, on the line mean, p_all and contact_vm, each at or under 5 % at the last step.
- Recorded in `results.json` T6: `valid` true, plus a `matched_mesh` block.
- Earlier T6 note says the peak is known to ±6 %, not 5 %. With this matched run, the last steps are all under 5 %, so that caveat is closed.

## R5. Paper corrections (done, closed)

- T5: `notes` opens with the margin-not-converged line, then superseded by R1 (`verdict` `pass`, `status` `done`). Done.
- T4: `notes` opens with lowest factor 0.57 (shear between Z layers at the R0.4 corner, 22.63 MPa, converged); layer factor at the motor holes 1.57; hand 39.3 MPa by curved-beam theory (factor 3.57). Done.
- T6: `why` opens with the block reaction and the lig_force sentence, then the R2 result. Done.
- T7: added with `status` `done` and the five-diagnoses note.
- `review_corrections.report_set_a`: 23 minutes, not 84; T3 Y-layer factor at the finest mesh 2.67, not 3.24.

## Status of each follow-up

| Follow-up | Closed? | Why |
| --- | --- | --- |
| T5 (R1 toe rounding) | **Yes** | judge() pass, lowest factor 2.99, all entries converged, mass +8.25 % |
| T6 (R2a + R2b) | **Yes** | valid true, line mean converged over three sizes, within 25 % of 6.76 MPa |
| T4, T3, T1, T2, T7 corrections (R5) | **Yes** (paper only) | Corrections written; no re-run was asked for, so T3 and T4 verdicts stay "fail" as recorded |

## Not done / open

- T3 and T4 are not re-solved. T4 still fails on the sharp-corner stress and on the layer tension at the lower motor holes (factor 1.49 to 1.57). The follow-up only corrected their notes.
- The T5 rib toe is rounded only at R2.0 on the rib corners. The upright toe is now the peak, but its radius is the same R2.0; no further step was asked for.
- No commit or push was made.
