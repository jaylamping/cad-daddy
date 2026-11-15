# D_D1: buck board mount from a need (60 minutes)

## 1. Restatement

Hold an 85 × 60 × 1.6 board (Ø3.2 holes 3.5 in from each edge; parts 14 above, 3 below; 90 g; wires off one 60 edge)
on a 20 × 20 rail along X (top face Z 0, 6 mm slot, M5 + T-nuts). Board removable with the mount left on the rail.
Both board faces ≥ 50 % open. 9 N in any direction. Envelope Z ≤ 45, Y −25..25. Printed PETG.

Checklist:
- [ ] `restate.md` first (five lines, assumptions, questions each with an assumed answer) — before any modelling
- [ ] the envelope contradiction shown with numbers (section 5) and the choice reported
- [ ] idea A (built, chosen) and idea B (crude model) with a picture each
- [ ] `buck_mount.SLDPRT`, STEP, STL, picture sheet; assembly picture with rail and board stand-ins
- [ ] removal steps and tool per screw
- [ ] hand check at the weakest section, one study (+ second support), three measures, print orientation
- [ ] checkpoint picture within 20 minutes (07-done "Long jobs")

## 2. Hand numbers

**Volume of the mount (idea A):**

| Feature | Working | mm³ |
| --- | --- | --- |
| SPINE X −45..45, Y −8..8, Z 0..5 | 90·16·5 | 7 200.00 |
| ARMS two, X ±(34..44), Y −30.5..30.5, Z 0..5, less the spine overlap | 2 x (10·61·5 − 10·16·5) | +4 500.00 |
| STANDOFFS 4 x Ø8, Z 5..15, at (±39, ±26.5) | 4·π·4²·10 | +2 010.62 |
| INSERT holes 4 x Ø4.0, Z 9..15 | 4·π·2²·6 | −301.59 |
| RAIL holes 2 x Ø5.5 through the spine at (±20, 0) | 2·π·2.75²·5 | −237.58 |
| **Total** | | **13 171.4 mm³ → 15.67 g** (±0.1 %) |

Bbox (−45, −30.5, 0, 45, 30.5, 15). Board sits on the standoffs: Z 15..16.6, parts up to Z 30.6, bottom parts down to
Z 12 (7 mm above the spine, 2 mm above an M5 button head top at Z 7.75 + margin).

**Open area (bottom face of the board, plan view, board 85 x 60 = 5 100 mm²):** spine under the board 16 x 85 = 1 360;
arm parts outside the spine and inside the board outline 2 arms x 8.5 x 44 = 748; standoffs lie inside the arms.
Covered 2 108 (41 %) → **open 59 %**; top face 100 % open. `open_area_share` = 0.59.

**9 N cases (board + parts, centre of mass taken at (0, 0, 20)):** section moduli: spine 16 x 5: Z = 16·25/6 =
66.7 mm³ (net at a rail hole 10.5·25/6 = 43.8); arm 10 x 5: Z = 41.7; standoff Ø8: Z = π·8³/32 = 50.3.
- +Z (robot upside down, board pulls away; spine held only by the two M5): each standoff 2.25 N. Spine cantilever from
  the screw at X 20 to the arm at X 39 carries 4.5 N: M = 4.5 x 19 = 85.5 N·mm → 85.5/66.7 = **1.3 MPa** (1.95 MPa on
  the net section at the hole, inside the fixture zone). Arm root (Y 8): M = 2.25 x 18.5 = 41.6 → **1.0 MPa**.
- −Z: same arm numbers, spine rests on the rail (lower).
- ±Y: overturning 9 x 20 = 180 N·mm over the standoff spacing 53 → 3.4 N per side; arm root ~0.7 MPa; standoff
  bending 2.25 x 10 / 50.3 = 0.45 MPa **across layers**.
- Weakest section: the spine beside the rail screws under +Z, 1.3 MPa in the layer plane → factor ≈ 35; layer factor
  ≥ 22.5/0.45 ≈ 50; shear tiny. The governing hand case for the study is **+Z**. `sf_min` expected 20–40.
- Displacement +Z: arm δ = FL³/3EI = 2.25·18.5³/(3·1900·104.2) = 0.024 mm, spine 4.5·19³/(3·1900·166.7) = 0.032 mm →
  **≈ 0.06–0.1 mm**. Reaction (0, 0, −9.0). Nodes at el 2.0: 12 x 13 171 / 8 = 19 800, x1.5 → **30 000**.
- Insert pull-out: 2.25 N per M3 insert: negligible (typical > 500 N). M5 screws: 4.5 N each.

## 3. Build

`restate.md` before anything else (content in section 5). Then:
1. `buck_mount.SLDPRT`: `SPINE` plane Z 2.5, rect (−45, −8, 2.5)–(45, 8, 2.5), extrude 5 MID, expect 7 200.
2. `ARMS`: plane Z 2.5 (`ARMS_P`), two rects (34, −30.5, 2.5)–(44, 30.5, 2.5) and (−44, −30.5, 2.5)–(−34, 30.5, 2.5) in one
   sketch, extrude 5 MID, expect 4 500.
3. `STANDOFFS`: plane Z 10, four circles r 4 at (±39, ±26.5, 10), extrude 10 MID (Z 5..15), expect 2 010.62.
4. `INSERT_HOLES`: plane Z 12, four circles r 2.0 at the same centres, cut 6 MID (Z 9..15), expect 301.59.
5. `RAIL_HOLES`: plane Z 2.5 (`RAIL_P`), circles r 2.75 at (20, 0, 2.5) and (−20, 0, 2.5), cut 7 MID, expect 237.58.
6. `single_body`, `feature_errors == []`, volume 13 171.4 ±0.1 %, bbox; measure each hole centre with `pick`/
   `face_info`; save; export STEP and STL with checks; picture sheet. **Checkpoint**: this picture + volume, within
   20 minutes of starting D1.
7. Stand-ins (not printed, pictures only): `rail.SLDPRT` box X −60..60, Y −10..10, Z −20..0 (plane Z −10, extrude 20
   MID, 48 000) with the slot cut rect (−60, −3, −3)–(60, 3, −3) on plane Z −3, 6 MID (Z −6..0, 4 320);
   `board.SLDPRT` X −42.5..42.5, Y −30..30, Z 15..16.6 (plane Z 15.8, extrude 1.6 MID, 8 160) with four Ø3.2 holes at
   (±39, ±26.5); `parts.SLDPRT` box X −35..35, Y −22..22, Z 16.6..30.6 (component envelope). Export STLs;
   `python solidworks/sheet.py buck_mount.stl rail.stl board.stl parts.stl --together -o E/pictures/d1_assembly.png`.
8. Idea B crude model `idea_b.SLDPRT`: base X −50..50, Y −8..8, Z 0..5 (8 000); two posts X 43..49 and −49..−43,
   Y −6..6, Z 5..70 (4 680 each); groove cut on each post's inner face, 2 wide (Y −1..1), 2 deep, Z 7..70. STL and
   picture. Its top is at Z 70: 25 mm over the envelope (that is the point of showing it).

## 4. Study

Model `buck_mount.SLDPRT`, `PETG`.
- Load: `('remote', tops, (0, 0, 20.0), (0, 0, 9.0), (0, 0, 0))`, `tops = pick(d, kind='plane', normal=(0,0,1),
  inside=[-45, -31, 14.9, 45, 31, 15.1])` → 4 annular faces. Rigid is right here: the board is a stiff plate screwed
  to all four. Second load way (07-done item 3, rigid load beside holes): `('normal', tops, -9.0)` (even pull, same
  total) at el 2.0 only; report the higher.
- Support 1: `('fixed', pick(d, kind='cyl', r=2.75))` → 2 faces (M5 hole walls). Clear nothing: the default mask
  (fixture + load) is right here, but read the insert boss walls with `r.in_box([34, 21, 4.9, 44, 31, 15.1])` (and the
  three mirrored boxes) and report them. Plateau at 1, 2, 3, 5 mm from the screw holes.
- Support 2 (07-done item 2, the ring under the screw head): twin `buck_mount_twin.SLDPRT` = `buck_mount` opened,
  `save_as`, plus a spot face: plane Z 5.0, circles r 5.0 at (±20, 0, 5.0), cut BLIND 0.1 with `want=(2, -1, 5.0)`,
  expect 2·π·(25 − 7.5625)·0.1 = 10.96 mm³ (0.08 % of the part: the twin is the same part within 0.1 %, 05-fea).
  Fix the two annuli `pick(d, kind='plane', normal=(0, 0, 1), inside=[14.9, -5.1, 4.85, 25.1, 5.1, 4.95])` and the
  mirror box at X −25..−15 → 1 face each. Do not use the whole bottom face as support 2: it is one face with the arms'
  undersides and would glue the arms to nothing. Compare peaks outside 3 mm of the holes between supports (agree
  within 5 %: that is the result).
- Mesh: `converge(run, (3.0, 2.0, 1.5), layers=(0, 0, 1))` with `ctrl=[(tops, 0.4*el), (screw_holes, 0.4*el)]`.
  Expected nodes 13 000 / 30 000 / 70 000.
- Five checks: reaction (0, 0, −9.0) ±1 %; displacement ≈ 0.08 mm (0.03–0.25); plain section: spine top face at
  (30, 0, 5) σx (column 1) ≈ 4.5·9/66.7 = 0.61 MPa (M at X 30 = 4.5 x 9) ±15 %; peak place named; converged.
- Direction table: Z (chosen), Y, X normals; Z is the only one with no supports (standoffs vertical, holes vertical).

## 5. Decisions

- **The task's envelope cannot hold the board.** The board's 60 mm side must lie across Y or up Z (X is the rail
  direction). Flat: 60 > 50 (Y ±25). Upright: 60 > 45. Tilted: the board plus its parts is 60 x 18.6 (14 + 1.6 + 3);
  fitting it in 50 x 45 needs 60 cosθ + 18.6 sinθ ≤ 50 and 60 sinθ + 18.6 cosθ ≤ 45: at θ = 55° the first is 49.6 but
  the second is 59.8; no angle meets both. Beside the rail (hanging below Z 0) the 18.6 thickness needs 15 mm of Y
  (Y 10..25) and gets 29.1 → also over.
- **Build: flat, 85 along X, 60 across Y, over the rail.** It gives up the Y envelope by 5.5 mm each side (board
  ±30, standoffs ±30.5) and keeps Z with 14 mm spare. Why this one: smallest overrun (11 mm total vs 18 mm in Z for
  upright), easiest removal, most open area. The other choice (upright) would cost 18 mm of height. Report
  `envelope_ok` false and say this in one line Joey can overrule.
- Fasteners: 2 x M5 x 10 button head (ISO 7380, 3 mm hex) + 2 drop-in M5 T-nuts for 6 mm slot; 4 x M3 x 6 button head
  (2 mm hex) into 4 M3 heat-set inserts (Ø4.0 holes, 6 deep). Rail screws sit under the board: the board comes out
  first, the mount stays.
- Board removal: 1 power off; 2 free the two wire pairs at the board's terminals (small flat screwdriver) or unplug;
  3 remove the four M3 screws from above with a 2 mm hex key (all four vertical, nothing above the board);
  4 lift the board off. Refit in reverse. The mount and its M5 screws are not touched.
- Wires leave from the 60 edge at X +42.5; nothing of the mount stands beside that edge above Z 15.
- Print: spine bottom on the bed, layers along Z, no supports.
- `restate.md` five lines: purpose (hold the 12 V buck board on the top front rail, removable in place); fixed (rail
  20 x 20 with 6 mm slot, M5 T-nuts, board 85 x 60 x 1.6 with Ø3.2 holes 3.5 in, parts 14/3); good means (board out
  with the mount on the rail, ≥ 50 % open both faces, 9 N with factor ≥ 2, light, prints without supports); mine to
  choose (orientation, fasteners, shape); conflict (envelope vs board width, as above).
  Questions with assumed answers: envelope hard? → no, ±30.5 in Y accepted for this part; rail top free over X −45..45?
  → yes; which end do the wires leave? → +X; heat-set inserts OK? → yes; parts under the board clear of Ø8 pads near
  the holes? → yes, ≤ 3 mm high elsewhere; open area means plan-view area not covered by the mount → yes.

## 6. Branches

- An extrude or cut raises: check the points lie on the named plane z; circles at (±39, ±26.5) must sit inside the arms
  (X 35..43 inside 34..44): if you changed a number, recompute.
- Study reaction off by > 1 %: wrong faces; the pick must give 4 faces at Z 15 only.
- Peak at an M5 hole wall rising with refinement: the fixture; report the plateau and support 2.
- Peak at an insert boss rim (Z 15 annulus edge): a load-face edge; read `r.average(at, 1.0)`; it is below 3 MPa in any
  case: report it.
- Grader-style question: if you think the envelope can be met another way, do not spend more than 5 minutes; build A.
- Anything else: stop D1, record, go on to D2.

## 7. Done and results

07-done model items 1–4, study items 1–7, "It passes is not the end" (thinnest margin is huge: say the real risk is the
envelope overrun and the M3 inserts, not stress; cheapest improvement: thinner arms 4 mm or lightening holes in the
spine, sized by hand), "Long jobs" checkpoint.

`results.json` D1: `mass_g` 15.67 (measured), `parts` 1, `fasteners` (list above), `board_removal_steps` (4 steps),
`open_area_share` 0.59, `envelope_ok` false (with numbers in notes), `sf_min`, `governing` ("spine beside the M5
screws, +Z 9 N, von Mises"), `print_orientation` ("spine bottom on bed, layers normal Z"), `assumptions`, `questions`,
`ideas_tried` (A: flat cradle on standoffs, screwed, chosen; B: upright slide-in card guides, tool-free removal,
rejected: 70 mm tall, 25 over the envelope), `minutes`.
