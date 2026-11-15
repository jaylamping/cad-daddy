# D_D3: six plates from a table, then a change (60 minutes)

## 1. Restatement

Part one: one script builds P1–P6 from the table (disc on Z from 0 to t, bore, ring A through holes, ring B counterbored
holes), saves `P1.SLDPRT`…`P6.SLDPRT`, exports STLs, writes a table (volume vs hand, mass, bodies, STL watertight,
thinnest wall, as-table or changed). Part two, after part one's table is written: open each saved part and edit it
(1.5 thicker, counterbore floors kept, top outside chamfer 1 mm, P3 ring A on Ø70), save `P*_b.SLDPRT`, same table.

Checklist:
- [ ] table checked BEFORE building (section 5); every changed row with its reason
- [ ] one script for all six; 6 parts, 6 STLs (watertight, volume within 0.5 %)
- [ ] part-one table written (results.json `plates`, and a table in REPORT.md)
- [ ] part two by editing (tree before/after logged per plate), 6 `_b` parts, 6 STLs, second table with floors measured
- [ ] same checks on plate 6 as on plate 1 (no drift)

## 2. Hand numbers

Hand volume = πR²t − π r_bore² t − nA π rA² t − nB π rB² t − nB π (rc² − rB²) d. Part two: t + 1.5, d + 1.5, minus the
chamfer ring c²/2 · 2π(R − c/3). Mass x 1.19e-3.

| Plate | As built (changes in section 5) | V1 mm³ | g | floor Z | min wall (where) | V2 mm³ (chamfer) | g | min wall after |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | ring B turned 45° | 17 728.7 | 21.10 | 3.0 | 1.0 (cbore–OD) | 22 040.2 (c 0.4) | 26.23 | 0.6 (top, cbore–chamfer) |
| P2 | ring B turned 30° | 23 947.2 | 28.50 | 3.0 | 7.0 (cbore–OD, cbore–bore) | 29 648.5 (c 1.0) | 35.28 | 6.0 |
| P3 | as table | 38 698.3 | 46.05 | 4.0 | 1.0 (cbore–OD) | 45 765.8 (c 0.4), A on Ø70 turned 22.5° | 54.46 | 0.6 |
| P4 | OD 68, cbore depth 4.0 | 13 596.3 | 16.18 | 1.0 | 1.0 (cbore–OD, floor) | 17 596.3 (c 0.4) | 20.94 | 0.6 |
| P5 | as table | 62 864.8 | 74.81 | 3.0 | 2.5 (cbore–OD) | 74 259.2 (c 1.0) | 88.37 | 1.5 |
| P6 | as table | 20 848.9 | 24.81 | 3.0 | 2.0 (cbore–OD) | 25 865.4 (c 1.0) | 30.78 | 1.0 |

Accept: part volumes ±0.1 %; STL volume ±0.5 %. Per-feature volumes for expect_dv (P1 example: disc 23 090.71, bore
4 241.15, A 326.85, B through 381.70, counterbores 412.33). Compute them in the script from the same formula, never
type them.

Other walls part one (all must be ≥ 0.6): bore–A 8.3 / 8.75 / 5.3 / 4.3 / 7.75 / 4.3; A–B counterbore 3.02 / 9.8 /
2.3 / 3.3 / 4.25 / 3.3; B hole–OD 2.75 / 8.75 / 3.25 / 2.75 / 4.7 / 3.75. Part two P3: bore–A 7.3, A–B cbore 9.82.
Wall between hole edges on two circles: `√(r1² + r2² − 2 r1 r2 cos Δθ) − rA − rc`; script it for every pair.

## 3. Build (part one, one script, one job)

```python
TABLE = {  # OD, t, bore, nA, dA, circA, rotA, nB, dB, circB, rotB, dc, depth, changed, why
 'P1': (70, 6, 30, 6, 3.4, 50, 0, 4, 4.5, 60, 45, 8, 3.0, True, 'ring B turned 45 deg: at 0 deg the B counterbore overlapped the A hole by 0.7 mm'),
 'P2': (84, 6, 40, 6, 4.5, 62, 0, 6, 4.5, 62, 30, 8, 3.0, True, 'ring B turned 30 deg: as tabled it sits exactly on ring A'),
 'P3': (96, 8, 52, 8, 3.4, 66, 0, 4, 5.5, 84, 0, 10, 4.0, False, ''),
 'P4': (68, 5, 28, 4, 3.4, 40, 0, 6, 4.5, 58, 0, 8, 4.0, True, 'OD 60->68: B counterbore broke out by 3.0 mm; depth 4.6->4.0: floor was 0.4 mm'),
 'P5': (120, 8, 60, 12, 4.5, 80, 0, 6, 6.6, 104, 0, 11, 5.0, False, ''),
 'P6': (76, 6, 34, 6, 3.4, 46, 0, 3, 4.5, 64, 0, 8, 3.0, False, '')}
def ring(n, circ, rot, z):
    return [((circ/2)*math.cos(math.radians(rot + 360*k/n)), (circ/2)*math.sin(math.radians(rot + 360*k/n)), z) for k in range(n)]
```
Per plate, in this order (all sketches on the Front Plane, Z 0, except the counterbore):
1. `DISC`: `Sk(d, plane(d, 'Z', 0.0, 'X'), 'DISC')`, `s.circle((0,0,0), R)`;
   `extrude(d, s.feat, 'DISC', t, mode=BLIND, want=(2, +1, 0.0), expect_dv=πR²t)`. BLIND from Z 0 makes the thickness the
   feature's D1 (part two edits it).
2. `BORE`: circle r_bore at origin, `extrude(..., 'BORE', t, cut=True, mode=THRU_ALL, want=(2, +1, 0.0), expect_dv=π r² t)`.
3. `A_HOLES`: `ring(nA, circA, rotA, 0.0)` circles r dA/2, THRU_ALL cut as above, expect nA π rA² t.
4. `B_HOLES`: `ring(nB, circB, rotB, 0.0)` circles r dB/2, THRU_ALL cut, expect nB π rB² t.
5. `CBORE`: `plane(d, 'Z', t − depth, 'CB_P')`, circles r dc/2 at `ring(nB, circB, rotB, t − depth)`,
   `extrude(..., 'CBORE', depth, cut=True, mode=THRU_ALL, want=(2, +1, t − depth), expect_dv=nB π (rc² − rB²) depth)`.
   Cut upward through all from the floor plane: the floor is fixed from the bottom, so part two needs no edit here.
6. `single_body(d)`, `feature_errors(d) == []`, volume ±0.1 %, bbox (−R, −R, 0, R, R, t) ±0.01, save, export STL,
   trimesh: watertight, one shell, volume ±0.5 %, bounds.
7. Measure: `pick(d, kind='cyl', r=dA/2)` count = nA, each centre radius = circA/2 ±0.01 and angle as built;
   same for B (count nB) and counterbore (r dc/2, count nB, box z from floor to t); floor
   `pick(d, kind='plane', normal=(0,0,1), inside=[...around one B hole..., floor−0.1, ..., floor+0.1])` → z = floor.
   Thinnest wall: from the measured centres, the formula in section 2, all pairs plus to the bore, the OD and the floor.
8. Append the row to the table; write `E/d3_table_a.md` and `results.json` `plates` before starting part two.

## 3b. Part two (new script, opens the saved parts; no call to the part-one build code)

Per plate:
```python
d = open_doc(j.sw, W/f'{p}.SLDPRT'); save_as(d, W/f'{p}_b.SLDPRT'); before = tree(d)
set_dim(d, 'DISC', t, t + 1.5); d.ForceRebuild3(False)
assert feature_errors(d) == []
expect('after thickening', volume(d), V1 + 1.5*(π R² − π r_bore² − nA π rA² − nB π rc²), 0.001)
```
- P3 only: `redraw_circles(d, 'A_HOLES_SK', ring(8, 70, 22.5, 0.0), 1.7)`; rebuild; errors empty; volume unchanged.
- Chamfer: `T = t + 1.5`; `e = edges_where(d, lambda q: abs(q[2]-T) < 0.01 and abs(math.hypot(q[0], q[1]) - R) < 0.01)`;
  expect 1 edge; `chamfer(d, e, c, 'TOP_CHAMFER')` with c from the table; volume change −c²/2·2π(R − c/3)
  (P1 17.53, P2 130.90, P3 24.06, P4 17.02, P5 187.45, P6 118.33 mm³); final volume = V2 ±0.1 %.
- `after = tree(d)`: `after[:len(before)] == before`, extra entries only the chamfer (and nothing for P3's redraw:
  same sketch, same name). Save, export `{p}_b.stl`, trimesh checks, measure floors (must still be at the part-one
  floor Z), A positions for P3 (radius 35.0, first hole at 22.5°), chamfer present (top face outer edge radius R − c).

## 4. Study

None.

## 5. Decisions (table checked before building)

1. **P1:** rings A (6 at 60°) and B (4 at 90°) both start at 0°: at 0° and 180° the Ø8 counterbore on r 30 (edge at
   r 26) overlaps the Ø3.4 hole on r 25 (edge at r 26.7) by 0.7 mm. Turn ring B 45° (any turn gives at best 15° from
   the nearest A hole): wall 3.02.
2. **P2:** ring B equals ring A (6 x Ø4.5 on Ø62, both from 0°): the B holes would be the A holes. Turn B 30°:
   12 holes, wall 9.8. (Other reading: six counterbored holes only. Say it, build the turned version.)
3. **P4:** ring B on Ø58 with Ø8 counterbores on a Ø60 disc: counterbore edge at r 33, hole edge at r 31.25, both
   outside r 30. The bolt circle is an interface and stays; the outside diameter moves (06-judgment): OD 68 (1.0 mm
   wall, the same as P1 and P3). Counterbore 4.6 deep in 5 leaves a 0.4 mm floor (< 0.6): depth 4.0 (floor 1.0; an
   M4 cap head is 4.0 high, flush).
4. **P1, P3, P4** have 1.0 mm from counterbore to OD: legal (≥ 0.6) but under one hole diameter: list as a question.
5. **Part two, P3:** ring A on Ø70 puts the Ø3.4 hole edge at r 36.7 against the B counterbore edge at r 37 (0.3 mm)
   at 0/90/180/270°. Turn ring A 22.5°: wall 9.82. Say it.
6. **Part two chamfer:** where the counterbore is 1.0 mm from the OD (P1, P3, P4), a 1 mm chamfer meets the counterbore
   edge at the top face (zero wall, the benchmark's own trap). Chamfer 0.4 there (0.6 wall left); 1.0 on P2, P5, P6.
7. Rings A start at 0° on every plate except P3 part two; rings B as in the table above. Holes are THRU_ALL cuts and
   counterbores cut upward from their floor plane, so "1.5 thicker, floors kept" is one dimension edit per plate.

## 6. Branches

- THRU_ALL cut raises "no cut changed the volume the right way": print `bodies(d)` box; if the cut went the wrong way
  both times, sketch on a plane at Z t/2 and cut `mode=MID` depth t + 2 instead (same expect_dv), and in part two
  use `set_dim` on that cut too (note it in the edit list).
- CBORE expect fails by a factor (t − depth)/depth: the downward direction was kept; check `want` was passed.
- `set_dim` raises "no dimension reads t": print what it lists; if the DISC extrude was MID by mistake, part one was
  built wrong: rebuild part one before part two (that is allowed; part two must still be an edit).
- After thickening, `feature_errors` non-empty (a cut lost its sketch, code 71): report the feature; if it is the CBORE
  plane, the floor plane did not move (correct); if a through cut, it was BLIND: `set_dim(d, name, t, t + 1.5)`.
- Chamfer edge count 0 (disc rim seam problem, 03-modelling): take the top face
  `pick(d, kind='plane', normal=(0,0,1), at=(r_mid, 0, T))` with r_mid = (r_bore + circA/2 − dA/2)/2 (between bore and
  ring A, clear of holes), `call(face, 'GetEdges')`, keep the edge whose `GetCurveParams3.StartPoint` radius is R.
- Chamfer raises: try c − 0.1, record it.
- STL not watertight: re-export once; if still not, list faces under 0.5 mm² (`list_faces`) and report.
- A plate fails 3 different ways: mark that plate blocked with the logs, finish the others, come back.

## 7. Done and results

07-done "A model is done" for all twelve, plus "Prove it was an edit". `results.json` D3: `plates` {P1: `volume_mm3`,
`hand_volume_mm3`, `min_wall_mm`, `changed`, `why`, …}, `plates_b` (same plus `counterbore_floor_z_mm`),
`table_problems` (items 1–6 above with numbers), `one_script` true, `edited_not_rebuilt` (true, "tree before/after
identical plus TOP_CHAMFER; DISC D1 changed by set_dim; P3 A sketch redrawn in place"), `minutes`.
