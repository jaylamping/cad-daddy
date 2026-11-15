# A_T4: the same study on the bracket without the inside fillet

## 1. Restatement

Build `bracket_sharp.SLDPRT` (T1 without the R4 inside fillet), run the T3 load case, report the stress in the inside
corner and whether the part meets the requirement (factor ≥ 2 on von Mises/45 and layer tension/22.5).

Checklist:
- [ ] `bracket_sharp.SLDPRT`: volume 32 802.3 mm³ ±0.1 %, one body, sharp edge at X 6, Z 6
- [ ] series on the sharp part: corner peak at three sizes (it will climb: that is the finding)
- [ ] `bracket_r04.SLDPRT` (R0.4 in the corner, the as-printed radius, 07-done item 6) and its converged series
- [ ] corner stress reported as the R0.4 value with averages; sharp numbers shown as not a stress
- [ ] three measures, five checks, verdict

## 2. Hand numbers

| Quantity | Working | Value | Accept |
| --- | --- | --- | --- |
| Volume sharp | 32 974.0 − 171.68 | **32 802.3 mm³** | ±0.1 % |
| Volume R0.4 | 32 802.3 + 0.214602 x 0.16 x 50 | **32 804.0 mm³** | ±0.1 % |
| Nominal stress at the corner (upright root, compression on the X 6 side) | 3300/300 | 11.0 MPa | – |
| Sharp corner | re-entrant 90° corner: singular | **no finite value**; expect the peak to climb ~20–40 % per refinement step | – |
| R0.4 corner von Mises | Kt for r/t = 0.4/6 = 0.07 in bending ≈ 2.5–3 → 11 x 2.7 | **~30 MPa** (low confidence) | 18–45 MPa |
| Layer tension | the corner is in compression; the layer peak stays at the lower Ø3.4 holes as in T3 | ~16.5 MPa | 12–21 |
| Reaction, displacement, nodes | as T3 (displacement ~2.7 mm, slightly more) | | |

Expected verdict: **fail** (layer factor ≈ 1.4 at the holes, as T3; von Mises at the R0.4 corner ≈ 1.5).

## 3. Build

1. Run the T1 build script (`E/t1_bracket.py`) with step 3 (INSIDE_FILLET) left out and the file name
   `bracket_sharp.SLDPRT`. Every other expect_dv is the same. Final `expect('volume', volume(d), 32802.34, 0.001)`.
   Check the edge: `edges_where(d, lambda p: abs(p[0]-6) < 0.01 and abs(p[2]-6) < 0.01)` → 1 edge.
   No exports needed (export the STL only if you want a picture).
2. Same script, step 3 with `fillet(d, e, (0.4,), 'INSIDE_FILLET')`, file `bracket_r04.SLDPRT`, fillet adds
   +1.717 mm³ (too small for a 1 % check to mean much: check the final volume 32 804.0 ±0.1 % and
   `pick(d, kind='cyl', r=0.4)` → 1 face).

## 4. Study

Exactly T3's model B on support 1 (`run()` of A_T3 section 4, with `r.loaded_pts = None`), plus a control on the
corner:
- sharp part: `corner = edges_where(d, lambda p: abs(p[0]-6) < 0.01 and abs(p[2]-6) < 0.01)` (pick again inside
  `run`), `ctrl=[(holes, 0.3*el), ([corner[0]] , 0.2*el)]` → corner sizes 0.6 / 0.4 / 0.3 (05-fea: a control on an
  edge works and costs few nodes). Shrink the corner control with the global size, so this is a real series.
- R0.4 part: control on the fillet face `pick(d, kind='cyl', r=0.4)` → 1 face, size `0.1*el` (0.3 / 0.2 / 0.15),
  i.e. 3–5 elements round the radius.
Sizes (3.0, 2.0, 1.5). Expected nodes ≈ 25 000 / 80 000 / 185 000 (edge control adds little; face control on R0.4
adds some). One job per part (three studies each).

Read the corner with a box mask, not `peak()`: `mc = r.in_box([5.0, 1.0, 5.0, 7.5, 49.0, 7.5])`;
`r.peak(mc)`, `r.layer_stress((0,0,1), mc)`, and `r.average(at, 0.5)`, `1.0`, `2.0` at the corner peak place with
node counts. Also the whole-part numbers as in T3 (`converge(..., layers=(0,0,1))` rows, holes box of T3 step 4).

## 5. Decisions

- The sharp corner's number is not a stress (05-fea singularity rule). The reported corner stress
  (`reported_stress_mpa`) is the converged R0.4 value: a printed corner is never sharper than about 0.4 mm
  (07-done item 6). The sharp series is reported beside it to show the climb.
- Verdict uses the same rule as T3; the holes still fail on layers whatever the corner does.
- No second load model or support here: T3 did them on the same faces; say so and point at T3's numbers.

## 6. Branches

- Sharp corner peak does NOT climb (under 5 % per step): check the mask `mc` contains nodes on the edge (count > 0)
  and that the edge control was applied (node count should rise more than the global change alone). If it really
  holds, report it with averages; do not call it converged without saying the control size was shrunk with it.
- R0.4 fillet does not build: try `(0.5, 0.3)`; record which built and use its radius in the report.
- R0.4 corner still climbs at the finest step (> 5 %): add one size (global 1.5, fillet control 0.1) in a new job;
  if it still moves, report the rows and "not shown" for the corner.
- R0.4 corner von Mises far from 18–45 MPa: read σx, σz, P3 at the place; if it is compressive and the averages at
  1 and 2 mm fall back to ~11–15, report it as a local peak with its averages. Not explained → say so.
- Excessive displacements, node limits, reaction off: as A_T3 section 6.
- Anything else: stop T4, record, go on.

## 7. Done and results

07-done study items 1, 4, 5 (direction table: same as T3, point to it), 6 (both series), 7. Report the corner:
sharp rows (climbing), R0.4 rows, averages with node counts.

`results.json` T4: `convergence_rows` (both series, labelled), `converged` (R0.4 series), `reported_stress_mpa`
(R0.4 corner von Mises), `how_judged` (one sentence: "The sharp corner's peak climbed a → b → c MPa with refinement,
a singularity, so the corner was judged with the 0.4 mm radius a printed corner has; that converged at x MPa; the
part fails on tension across layers at the lower motor-screw holes (factor y) as in T3"), `verdict`, `status`, `notes`.
