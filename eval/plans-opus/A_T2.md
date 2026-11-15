# A_T2: change the saved bracket

## 1. Restatement

Open `bracket.SLDPRT` from T1 (no rebuild from the script), add Ø10 × 3 counterbores from Z 6 on the four base holes
and a 20 × 6 round-ended slot through the base centred at (45, 25) along X, save as `bracket_b.SLDPRT`.

Checklist:
- [ ] opened, not rebuilt: feature tree before = tree after minus the new features (logged)
- [ ] four counterbores Ø10, floor at Z 3.000, measured
- [ ] slot: X 35..55, Y 22..28, through Z 0..6, round ends R3, measured
- [ ] volume 31 643.0 mm³ ±0.1 %, one body, no rebuild errors
- [ ] saved as `bracket_b.SLDPRT`; `bracket.SLDPRT` left unchanged

## 2. Hand numbers

| Item | Working | mm³ |
| --- | --- | --- |
| T1 part | | 32 974.0 |
| 4 counterbores | 4 x π (5² − 2.75²) x 3 = 4 x 164.34 | −657.38 |
| slot, middle rectangle | 14 x 6 x 6 | −504.00 |
| slot, two end half-discs | 2 x (π x 3² / 2) x 6 | −169.65 |
| **Total** | | **31 643.0** (accept ±0.1 %) |

Counterbore floor Z = 6 − 3 = 3.0. Spec check: counterbore edge to base edge 10 − 5 = 5.0 mm (less than one
counterbore diameter, 10: list it as a question, it is still 5 mm of wall); counterbore at X 25 to fillet toe (X 10):
10 mm; slot (Y 22..28) to nearest hole (Y 10 + 5 = 15 counterbore edge): 7 mm; slot X 35..55 to counterbores
(X 30 / X 60 edges): 5 mm. Nothing contradicts.

## 3. Build

```python
d = open_doc(j.sw, W / 'bracket.SLDPRT')
save_as(d, W / 'bracket_b.SLDPRT')          # from here d is bracket_b; bracket.SLDPRT stays as T1 left it
before = tree(d); log(before)
expect('start volume', volume(d), 32974.0, 0.001)
```
1. Counterbores, one-sided cut from a plane at Z 6 going down:
```python
with Sk(d, plane(d, 'Z', 6.0, 'CB_P'), 'CBORE') as s:
    for x, y in ((25, 10), (25, 40), (65, 10), (65, 40)):
        s.circle((x, y, 6.0), 5.0)
extrude(d, s.feat, 'CBORE', 3.0, cut=True, mode=BLIND, want=(2, -1, 6.0), expect_dv=657.38); save(d)
```
2. Slot middle, plane Z 3, cut mid-plane 8: `s.rect((38, 22, 3.0), (52, 28, 3.0))` →
   `extrude(d, s.feat, 'SLOT_MID', 8.0, cut=True, mode=MID, expect_dv=504.0)`; save.
3. Slot ends, plane Z 3 (name `SLOT_ENDS_P`), circles r 3 at (38, 25, 3.0) and (52, 25, 3.0) →
   `extrude(d, s.feat, 'SLOT_ENDS', 8.0, cut=True, mode=MID, expect_dv=169.65)`; save.
4. `single_body(d)`, `feature_errors(d) == []`, `expect('volume', volume(d), 31643.0, 0.001)`, `after = tree(d)`.
   Check: `after[:len(before)] == before` and the added entries are only planes, sketches and the three features
   (`CBORE`, `SLOT_MID`, `SLOT_ENDS`). Log both lists in the report.

Measure:
- floors: `pick(d, kind='plane', normal=(0, 0, 1), inside=[19.9, 4.9, 2.9, 30.1, 15.1, 3.1])` → 1 face, box z 3.0;
  same for the other three holes (shift the box). `counterbore_floor_z_mm` = that z.
- `pick(d, kind='cyl', r=5.0, inside=[15, 0, 2.9, 70, 50, 6.1])` → 4 counterbore walls (the box leaves out the R5
  rounds at X 75..80 and Z 41..46). Each box: centre at the hole, z span 3..6.
- slot: `pick(d, kind='cyl', r=3.0)` → 2 faces, centres (38, 25) and (52, 25); the two flat sides
  `pick(d, kind='plane', at=(45, 22, 3))` and `at=(45, 28, 3)` → 1 each.
- Optional: export `bracket_b.stl` and a picture sheet (cheap; shows the counterbores and slot).

## 4. Study

None.

## 5. Decisions

- The slot is made as a rectangle cut plus two circle cuts, not one sketch with arcs. Why: every volume is exact
  and no arc direction can come out wrong (`Sk.arc` warns its direction may be mirrored). The finished geometry is the
  same slot.
- Counterbore as BLIND from a new plane at Z 6 with `want`, so the floor depth is the feature's own D1 (an edit later
  changes one number).

## 6. Branches

- `open_doc` fails: path wrong, or the file is open from T1 in this instance → `close(j.sw, d)` first / new `job()`.
- Start volume is not 32 974.0: you have the wrong file. Stop T2, record the volume, check T1.
- CBORE raises "no cut changed the volume the right way": the plane at Z 6 coincides with the top face, which is
  allowed; most likely a circle point is off the plane (z must be 6.0). If it still fails, use plane Z 4.5 and
  `mode=MID` depth 3 (Z 3..6), same expect_dv.
- CBORE builds but expect_dv fails with dv ≈ 2 x 657 or the floor is at Z 9: wrong direction was kept; `want` was not
  passed. Undo (`d.EditUndo2(1)`) and repeat with `want=(2, -1, 6.0)`.
- SLOT_ENDS dv = 339.3 (full discs): SLOT_MID did not cut. Check it in `tree()` and `feature_errors()`.
- Tree after does not start with the tree before: something was rebuilt or reordered. Report it and do not claim
  `edited_not_rebuilt`.
- Anything else: stop T2, record, go on to T3 (T3 uses `bracket.SLDPRT`, not this file).

## 7. Done and results

07-done "A model is done": volume, body count, rebuild clean, every new dimension measured, spec checked (section 2).

`results.json` T2: `volume_mm3`, `hand_volume_mm3` 31643.0, `counterbore_floor_z_mm` (measured, expect 3.0),
`bodies` 1, `status`, `notes` (say: opened and edited, tree before/after logged; the 5 mm edge distance question).
