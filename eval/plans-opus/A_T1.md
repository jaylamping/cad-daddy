# A_T1: L bracket from a specification

## 1. Restatement

Build one solid L bracket (base 80 x 50 x 6, upright 6 x 50 x 40), with an R4 inside-corner fillet, four Ø5.5 base
holes, a Ø22 bore and four Ø3.4 holes in the upright, and R5 rounds on four outside corners. Save `bracket.SLDPRT`,
export STEP and STL, and check them.

Checklist (tick at the end):
- [ ] one body, no rebuild errors, volume 32 974.0 mm³ ±0.1 %, bbox (0, 0, 0, 80, 50, 46) ±0.01
- [ ] R4 fillet on the edge X 6, Z 6 (along Y)
- [ ] four Ø5.5 holes through the base at (25,10) (25,40) (65,10) (65,40), measured
- [ ] Ø22 bore along X at Y 25, Z 28, measured
- [ ] four Ø3.4 holes on Ø31 about the bore at 45/135/225/315°, measured
- [ ] R5 on the two vertical base corners at X 80 and the two upright top edges along X at Z 46
- [ ] `bracket.SLDPRT`, `bracket.step` (mm), `bracket.stl` (watertight, volume within 0.5 %, model frame)
- [ ] the build script saved in `E/t1_bracket.py`, so T4 can reuse it

## 2. Hand numbers

| Item | Working | Value |
| --- | --- | --- |
| Base | 80 x 50 x 6 | 24 000.00 |
| Upright | 6 x 50 x 40 | 12 000.00 |
| R4 inside fillet (adds) | (1 − π/4) x 4² x 50 = 0.214602 x 800 | +171.68 |
| 4 base holes | 4 x π x 2.75² x 6 = 4 x 142.55 | −570.20 |
| Bore | π x 11² x 6 | −2 280.80 |
| 4 upright holes | 4 x π x 1.7² x 6 = 4 x 54.475 | −217.90 |
| 4 R5 rounds (remove) | 4 x 0.214602 x 25 x 6 = 4 x 32.19 | −128.76 |
| **Total** | | **32 974.0 mm³** (accept ±0.1 %) |

Mass 32 974.0 x 1.19e-3 = **39.24 g**. Bbox 0, 0, 0, 80, 50, 46.

Upright hole centres: Y = 25 ± 15.5·cos45° = 25 ± 10.960 → 14.040 and 35.960; Z = 28 ± 10.960 → 17.040 and 38.960.
Spec check (07-done "specification itself"): wall bore to Ø3.4 hole = 15.5 − 1.7 − 11 = 2.8 mm; lowest hole edge
Z 15.34 is above the fillet top (Z 10); top hole edge Z 40.66 is 5.3 below the top; base hole edge distance 7.25 mm
(Y 10 − 2.75). Nothing contradicts. Write those numbers in the report.

## 3. Build (one `with job() as j:`)

```python
d = new_part(j.sw, W / 'bracket.SLDPRT')
# 1 base, sketch at mid thickness
with Sk(d, plane(d, 'Z', 3.0, 'BASE_P'), 'BASE') as s:
    s.rect((0, 0, 3.0), (80, 50, 3.0))
extrude(d, s.feat, 'BASE', 6.0, mode=MID, expect_dv=24000.0); save(d)
# 2 upright Z 6..46, sketch at Z 26
with Sk(d, plane(d, 'Z', 26.0, 'UPRIGHT_P'), 'UPRIGHT') as s:
    s.rect((0, 0, 26.0), (6, 50, 26.0))
extrude(d, s.feat, 'UPRIGHT', 40.0, mode=MID, expect_dv=12000.0); save(d)
```
3. Inside fillet, before any hole (simple solid, one edge):
```python
e = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01)
expect('inside corner edges', len(e), 1, 0)
v0 = volume(d); r = fillet(d, e, (4.0,), 'INSIDE_FILLET')
# r must be 4.0, and volume(d) - v0 = +171.68 within 1 %
expect('fillet adds', volume(d) - v0, 171.68, 0.01); save(d)
```
4. Outside rounds, one feature, 4 edges, R5:
```python
e = edges_where(d, lambda p: (abs(p[0] - 80) < 0.01 and min(abs(p[1]), abs(p[1] - 50)) < 0.01)
                          or (abs(p[2] - 46) < 0.01 and min(abs(p[1]), abs(p[1] - 50)) < 0.01))
expect('round edges', len(e), 4, 0)          # two along Z at X 80, two along X at Z 46
v0 = volume(d); fillet(d, e, (5.0,), 'CORNER_R5')
expect('rounds remove', v0 - volume(d), 128.76, 0.01); save(d)
```
Why this test is safe: at X 80 the edge along Y has its middle at Y 25 (fails), the edges along Z at Y 0 and Y 50 pass.
At Z 46 the edges along X (X 0..6) at Y 0 / Y 50 pass; the edges along Y at Z 46 have middle Y 25 (fail).

5. Base holes, cut mid-plane 8 deep about Z 3 (overshoots both faces by 1 mm into air):
```python
with Sk(d, plane(d, 'Z', 3.0, 'BASE_HOLES_P'), 'BASE_HOLES') as s:
    for x, y in ((25, 10), (25, 40), (65, 10), (65, 40)):
        s.circle((x, y, 3.0), 2.75)
extrude(d, s.feat, 'BASE_HOLES', 8.0, cut=True, mode=MID, expect_dv=570.20); save(d)
```
6. Bore, plane X 3, cut 8 mid-plane: `s.circle((3.0, 25, 28), 11.0)` → `extrude(..., 'BORE', 8.0, cut=True, mode=MID, expect_dv=2280.80)`.
7. Upright holes, plane X 3 (name `UHOLES_P`), four circles r 1.7 at (3.0, 14.040, 17.040), (3.0, 35.960, 17.040),
   (3.0, 35.960, 38.960), (3.0, 14.040, 38.960); `extrude(..., 'UPRIGHT_HOLES', 8.0, cut=True, mode=MID, expect_dv=217.90)`.
   Use exact values `25 ± 15.5*math.cos(math.radians(45))`, not the rounded ones.
8. `single_body(d)`; `feature_errors(d) == []`; `expect('volume', volume(d), 32974.0, 0.001)`; bbox each of 6 within 0.01; save.

Measure every dimension (07-done "A model is done", item 2):
- `pick(d, kind='cyl', r=2.75)` → 4 faces; for each `face_info(f)['box']`: centre x = (box[0]+box[3])/2, y likewise,
  z span 0..6. Expect the four (x, y) pairs above within 0.01.
- `pick(d, kind='cyl', r=11.0)` → 1 face, box centre y 25, z 28, x span 0..6.
- `pick(d, kind='cyl', r=1.7)` → 4 faces, centres as step 7.
- `pick(d, kind='cyl', r=4.0)` → 1 (the fillet). `pick(d, kind='cyl', r=5.0)` → 4.

9. Exports: `export(j.sw, d, W/'bracket.step')`, `export(j.sw, d, W/'bracket.stl')`; then checks of 04-export.md:
   trimesh watertight, `len(mesh.split()) == 1`, `mesh.volume` within 0.5 % of `volume(d)`, `mesh.bounds` within 0.1 mm
   of the bbox, `.MILLI.` on an `SI_UNIT` line of the STEP. Picture sheet of the STL.

## 4. Study

None.

## 5. Decisions

- Fillet and rounds go before the holes: on the bare L every edge test is unambiguous. Why: holes add edges that a
  loose test could catch.
- The order of the two fillet features does not change the volume (they do not touch).

## 6. Branches

- `edges_where` for the inside corner returns 0: print all edges with Z between 5.9 and 6.1 (`edges_where(d, lambda p: abs(p[2]-6) < 0.1)`, their end points). If the base and upright did not merge, `bodies(d)` shows 2: the upright
  extrude did not merge. Undo by rebuilding the part from step 1 with the upright drawn on plane X 3 instead: rect
  (3, 0, 6)–(3, 50, 46), extrude 6 MID, expect 12 000.
- Round edges count is not 4: print each edge's start/end; most likely an edge along X at Z 46 matched twice because
  the fillet changed nothing there. Narrow the test to the listed edges, do not loosen it.
- `fillet` returns None at R5: try the two pairs as separate features (`CORNER_R5_BASE`, `CORNER_R5_TOP`), each
  expect −64.38.
- A hole cut raises on `expect_dv`: print the logged dv. If it is exactly half, the circle sits on a face edge (wrong
  coordinate); if 0, the plane is off the body. Check the plane coordinate and the points.
- `extrude(cut=True)` raises on a plain round pocket where others worked (03-modelling.md): use `revolve(cut=True)`
  of the same cylinder (profile rect in a plane through the hole axis plus `centerline` on the axis), same expect_dv.
- STL volume off by 1e9 or 1e-9: unit setting; STL min x not 0: shifted export. Re-export with `export()` (it pins
  the options); never hand-edit the file.
- Anything else: stop T1, record what you saw, go on to T6/T7 (T2–T5 need this part).

## 7. Done and results

07-done "A model is done when": items 1–4 with numbers. Report the spec check numbers from section 2.

`results.json` T1: `volume_mm3` (from `volume(d)`), `hand_volume_mm3` 32974.0, `mass_g` (volume × 1.19e-3),
`bbox_mm` (6 numbers), `bodies` 1, `stl_watertight`, `stl_volume_mm3`, `status`, `notes`.
REPORT.md T1: steps, the table above beside the measured values, each measured hole centre, export checks, minutes.
