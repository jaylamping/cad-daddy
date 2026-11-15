# A_T5: make the bracket pass

## 1. Restatement

If T3 fails, change the design so it meets factor ≥ 2.0 (von Mises/45 and layer tension/22.5), keeping hole positions,
the bore and the footprint X 0..80, Y 0..50, Z 0..46, mass growth ≤ 10 %. Geometry and print orientation are open.
Show it with a study. Save `bracket_c.SLDPRT`.

Checklist:
- [ ] T3 verdict quoted (expected fail on layers, factor ≈ 1.4 at the lower motor-screw holes)
- [ ] change chosen by 07-done order: print direction first
- [ ] `bracket_c.SLDPRT` saved; mass and growth computed
- [ ] study on `bracket_c` converged on all three measures for the chosen layer direction, both load models
- [ ] verdict, thinnest margin, what the orientation costs (supports)

## 2. Hand numbers

**Change 1 (chosen): print on its side, the Y 0 face on the bed, layers stacked along Y.** Geometry unchanged.
- Mass 39.24 g, growth 0 %.
- In the bending field σz (up the upright) and σx (along the base) lie in the layer plane; across Y layers only σy
  acts. At a Ø3.4 hole in a σz field of 5.5–5.8 MPa, σy at the hole's top and bottom points is about −1 x σz on the
  tension face and +1 x σz on the compression face (X 6 side) → **σy ≈ 5.5–6 MPa → layer factor ≈ 3.8–4.1**.
  05-fea.md measured 2.2 → 4.6 on this bracket for the same turn. Accept 3–6 MPa.
- Von Mises unchanged from T3: ≈ 16.5 MPa → factor ≈ 2.7.
- Shear between Y layers (τxy, τyz): small, ~1–3 MPa → factor > 4.

**Change 2 (fallback, only if change 1 does not pass or is ruled out): upright 7.5 thick (X 0..7.5), printed base
on the bed.**
- Volume: 24 000 + 15 000 + 171.68 − 570.20 − π·121·7.5 (2 851.0) − 4·π·1.7²·7.5 (272.4) − rounds (64.38 base +
  2 x 0.214602 x 25 x 7.5 = 80.47 top) = **35 333.2 mm³**, 42.05 g, growth **+7.15 %**.
- Section modulus x (7.5/6)² = 1.5625 → hole layer stress 16.5/1.5625 ≈ **10.6 MPa → factor ≈ 2.1** (thin margin).

## 3. Build

Change 1: `d = open_doc(j.sw, W/'bracket.SLDPRT')`; `save_as(d, W/'bracket_c.SLDPRT')`; check volume 32 974.0.
Add nothing. Write the orientation in the report and in `results.json`.

Change 2 (only if needed): T1 script with: UPRIGHT rect `(0, 0, 26.0)`–`(7.5, 50, 26.0)`, expect 15 000; inside
fillet edge test `abs(p[0]-7.5) < 0.01 and abs(p[2]-6) < 0.01`, +171.68; corner rounds same test (edges along X at
Z 46 now run X 0..7.5), expect −144.85; bore and upright holes on plane X 3.75, depth 9.5 MID, expect 2 851.0 and
272.38; total 35 333.2 ±0.1 %. Save as `bracket_c.SLDPRT` (overwrite change 1 only if change 1 failed).

## 4. Study

A_T3 section 4 `run()` on `bracket_c.SLDPRT`, support 1, model B, `converge(run, (3.0, 2.0, 1.5), layers=(0, 1, 0))`
(change 1) or `layers=(0, 0, 1)` (change 2). Then `run(1.5, load='A')` and read the same three measures for Y layers.
Clear the load mask as in T3. Five checks as T3 (the numbers must match T3's within 1 % for change 1: same part).
Report the full direction table (Z, Y, X) again from this result.

Predict: nodes as T3; displacement 2.7 mm (change 2: about 2.3 mm, the base still rotates); layer peak for Y layers at
the lower Ø3.4 holes or the bore's top/bottom points.

## 5. Decisions

- Print direction is chosen first because 07-done says to try it first and it costs no mass. Why it works: the
  failing stress is σz, which lies in the layer plane once the part lies on its side.
- What it costs: the Ø22 bore and Ø3.4 holes print with horizontal axes; the bore needs support inside or is
  printed as is with a sagging top (a teardrop top would change the bore: not allowed). The Ø5.5 base holes also
  become horizontal (bridged). Say this in the report as the price; it is not a reason to reject the change.
- Change 2 is the fallback because it keeps the base-on-bed print and stays inside the mass limit (+7.15 %), but its
  margin is thin (≈ 2.1). Report it by hand even if not built, as the alternative (06-judgment: say what the other
  choice would cost).

## 6. Branches

- Y-layer stress over 11 MPa (factor < 2): check `layers=(0, 1, 0)`; read where it is. If it sits at the base holes'
  plateau region, use T3's plateau distance. If real, build change 2 and print base-on-bed; judge Z layers.
- Change 2 also below 2.0 on layers: add the T1 shape back but thicken only the upright's lower part is not allowed
  without a new decision; instead print change 2 on its side too (both changes together) and report.
- Von Mises factor below 2 (peak > 22.5 MPa): it should not happen (T3 ≈ 16.5); if it does at a base fixture hole
  inside the plateau, report the plateau; otherwise stop and record.
- Excessive displacements / nodes / reaction: as A_T3 section 6.
- Anything else: stop T5, record, go on.

## 7. Done and results

07-done study items 1–7 for `bracket_c`, and "It passes is not the end": thinnest margin (von Mises ≈ 2.7 or the
Y-layer factor, whichever is lower, and what eats it: a 20 % higher load leaves ≈ 2.3), cheapest improvement (none
needed; change 2 adds margin for Z printing at +7 % mass), not checked (support removal marks in the bore, bed
contact, screw preload).

`results.json` T5: `change` ("print on its side, Y 0 face on the bed, layers stacked along Y; no geometry change"),
`mass_g` 39.24, `mass_growth_pct` 0.0, `sf_yield`, `sf_layer` (Y layers), `print_orientation` ("Y 0 face on bed,
layers normal +Y"), `verdict`, `status`, `notes` (change 2 numbers by hand, supports needed).
