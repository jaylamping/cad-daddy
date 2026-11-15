# D_D2: split housing round a 6808 bearing (90 minutes)

## 1. Restatement

Two printed halves split on Y 0 clamp a 6808-2RS outer ring (Ø52 x 7; inner ring OD 44.0, outer ring ID 48.0), axis Z.
Envelope X ±36, Y ±32, Z −4..11. Four M3 along Y clamp the halves (inserts in the lower half); the lower half mounts by
its Y −32 face (two M4 insert holes). 300 N on the bearing along +Y and along +X, face Y −32 held: factor ≥ 2 on all
three measures in both halves. Build halves + steel ring stand-in, check the fit, run both cases with contact
(ring–seat, half–half) and screws, prove the contact, give screw load by hand and from the study.

Checklist:
- [ ] spec problems found BEFORE building, each with numbers and what was built instead (section 5)
- [ ] `housing_upper.SLDPRT`, `housing_lower.SLDPRT`, `ring.SLDPRT`; STL of each half; picture sheet of each half and
      of the pair (`--together`)
- [ ] fit table: what touches, what clears and by how much, inner ring included
- [ ] FEA model: 2 halves, ring, 4 screw pins, 2 pads; reaction, pad share, body split guard
- [ ] +Y and +X solved; governing case converged on 3 meshes; bonded twin for the contact proof
- [ ] screw load by hand and from a section of the shank, both cases
- [ ] three measures per half, direction table, verdict; checkpoint picture within 20 minutes

## 2. Hand numbers

**Volumes** (built geometry, section 5): block per half 72 x 31.6 x 15 = 34 128.0; seat cut (circle segment R 26 beyond
0.4 from the centre, 7.2 long) 7 495.63; shoulder opening (R 23 segment, 7.8 of length) 6 337.91.

| Body | Working | mm³ | g |
| --- | --- | --- | --- |
| lower | 34 128 − 7 495.63 − 6 337.91 − 4 inserts π·2²·6 (301.59) − 2 mounts π·2.8²·8 (394.08) | **19 598.8** | 23.32 |
| upper | 34 128 − 7 495.63 − 6 337.91 − 4 holes π·1.7²·31.6 (1 147.61) − 4 counterbores π·(3² − 1.7²)·3.5 (268.73) | **18 878.1** | 22.46 |
| ring | π (26² − 24²) 7 | **2 199.11** | 17.3 (steel) |
| screw pin (each) | plug π·2²·6 + shank π·1.5²·28.9 + head π·2.75²·3 | **350.96** | |
| pad (each) | 4.3/360 · π (24² − 23²) · 1 | **1.764** | |

**Loads:**
- +Y: the ring pushes the upper half; the upper half is held only by the four screws → **75 N per screw**
  (`hand_screw_load_n`, snug, no preload). Shank stress 75/(π·1.5²) = 10.6 MPa (steel).
- +X: cosine pressure over the +X half of the seat; the upper half takes the 0..90° part: Fx 150 N, Fy = p0R/2 = 95.5 N
  (wedging), acting at x̄ = 2R/3 = 17.3. Moments about the −X screws (X −31): +X screws carry 95.5 x 48.3/62 = 74.4 N
  → **≈ 37 N each**, −X screws ≈ 10.5 N each; shear 150 N over four screws ≈ 37.5 N each. Low confidence: 05-fea
  ("Do not trust a hand value for screw loads off the load axis") records this very housing at 75.7 N after the ring
  wedged. Redo the statics with the contact patch the study shows before comparing.
- Upper half crown section at X 0 (seat zone Y 26..32 over 7.2 of Z, shoulders Y 23..32 over 7.8): I = 663.6 mm⁴,
  c = 5.07. +Y moment between M = 4 650 (pinned ends, point load) and 1 350 (clamped, spread load); mid estimate
  M = 2 700 → **σx ≈ 21 MPa** (range 10–36), in the layer plane for Z printing → sf_yield ≈ 2.2 (1.3–4.4). This is
  the number to watch; shoulders at the crown are the likely peak.
- Counterbore floor under a head: 75 N on π/4·(5.5² − 3.4²) = 14.7 mm² → 5.1 MPa (rim is a singular bonded edge:
  read outside 1–2 mm).
- Insert hole wall, lower half: 75/(π·4·6) = 1.0 MPa shear.
- Reaction: (0, −300, 0) and (−300, 0, 0) within 1 %. Pad share: 2 pads x 0.9 N/mm x ring travel ≈ 0.3 mm ≈ 0.5 N
  (0.2 %).
- Displacement, ring, +Y: ≈ 0.3 mm (0.1–0.9). Bonded twin: many times stiffer (benchmark 24x).
- Nodes: about 41 000 mm³ of solid; el 2.5 → 12·41 000/15.6 ≈ 31 000, controls (seats 1.0, screws 0.8, pads 0.5)
  → **90 000** expected at the middle mesh; coarse ≈ 60 000, fine ≈ 150 000. Every solve under 200 000.

## 3. Build (job 1)

Frame: bearing axis Z through the origin. Screw axes along Y at (X, Z) = (±31.0, −0.2) and (±31.0, 7.2).
1. `housing_lower.SLDPRT`: `BLOCK` plane Z 3.5, rect (−36, −32, 3.5)–(36, −0.4, 3.5), extrude 15 MID, expect 34 128.0.
   `SEAT` plane Z 3.5 (`SEAT_P`), circle (0, 0, 3.5) r 26, cut 7.2 MID (Z −0.1..7.1), expect 7 495.63.
   `SHOULDER` plane Z 3.5 (`SH_P`), circle r 23, cut 20 MID, expect 6 337.91.
   `INSERTS` plane Y −3.4, circles r 2.0 at (±31, −3.4, −0.2) and (±31, −3.4, 7.2), cut 6 MID (Y −6.4..−0.4), expect 301.59.
   `MOUNTS` plane Y −28, circles r 2.8 at (±24, −28, 3.5), cut 8 MID (Y −32..−24), expect 394.08.
   single body, errors empty, volume 19 598.8 ±0.1 %, bbox (−36, −32, −4, 36, −0.4, 11). Save, STL, sheet.
2. `housing_upper.SLDPRT`: `BLOCK` rect (−36, 0.4, 3.5)–(36, 32, 3.5), 15 MID, 34 128.0; `SEAT`, `SHOULDER` as above
   (same expects); `HOLES` plane Y 16.2, circles r 1.7 at the four screw points (y 16.2), cut 34 MID, expect 1 147.61;
   `CBORES` plane Y 30.25, circles r 3.0, cut 3.5 MID (Y 28.5..32), expect 268.73. Volume 18 878.1, bbox
   (−36, 0.4, −4, 36, 32, 11). Save, STL, sheet.
3. `ring.SLDPRT`: plane Y 0 (Top Plane), `s.rect((24, 0, 0), (26, 0, 7))`, `s.centerline((0, 0, -5), (0, 0, 12))`,
   `revolve(d, s.feat, 'RING', expect_dv=2199.11)`. Box (−26, −26, 0, 26, 26, 7).
4. Four `screw_<n>.SLDPRT` (n 1..4 for (31, −0.2), (31, 7.2), (−31, −0.2), (−31, 7.2)): plane Z z0, profile
   `s.poly([(x0, -6.4, z0), (x0+2, -6.4, z0), (x0+2, -0.4, z0), (x0+1.5, -0.4, z0), (x0+1.5, 28.5, z0),
   (x0+2.75, 28.5, z0), (x0+2.75, 31.5, z0), (x0, 31.5, z0)])`, `s.centerline((x0, -10, z0), (x0, 35, z0))`,
   `revolve(..., 'PIN', expect_dv=350.96)`. Plug fills the insert hole (bonded), shank Ø3 in the Ø3.4 hole (free), head
   Ø5.5 on the counterbore floor (bonded).
5. Two pads `pad_px.SLDPRT`, `pad_nx.SLDPRT`: plane Y 0, rect (23, 0, 3)–(24, 0, 4) (pad_nx: (−24, 0, 3)–(−23, 0, 4)),
   centerline on Z, `revolve(d, s.feat, 'PAD', angle=4.3, mid=True, min_dv=0.5, expect_dv=1.764)`.
6. `d2_fea.SLDPRT`: open `housing_lower`, `save_as` `d2_fea`, `insert_body` upper, ring, 4 screws, 2 pads → 10 bodies,
   total 19 598.8 + 18 878.1 + 2 199.11 + 4·350.96 + 2·1.764 = 42 083.4 ±0.1 %. Save.
   Overlap check by numbers (boxes overlap by design): ring OD = seat radius (line-to-line, intended); plug Ø4 = insert
   hole (intended); shank 1.5 < hole 1.7; head 2.75 < counterbore 3.0; pads r 23..24 inside the ring ID 24.
7. Fit pictures: `sheet.py housing_upper.stl housing_lower.stl ring.stl --together`, and a crop of one screw.

## 4. Study (jobs 2 and 3, at most four solves each)

```python
PAD = dict(name='Soft pad', EX=0.5e6, NUXY=0.45, DENS=1000.0, SIGYLD=1e6, SIGXT=1e6)
MATS = {'ring-': STEEL, 'screw': STEEL, 'pad_': PAD}        # halves get PETG (default)
def picks():
    ring_od = pick(d, kind='cyl', r=26.0, inside=[-26.1, -26.1, -0.05, 26.1, 26.1, 7.05])         # 1
    seat_up = pick(d, kind='cyl', r=26.0, inside=[-26.1, 0.3, -0.2, 26.1, 26.1, 7.2])             # 1
    seat_lo = pick(d, kind='cyl', r=26.0, inside=[-26.1, -26.1, -0.2, 26.1, -0.3, 7.2])           # 1
    split_up = pick(d, kind='plane', normal=(0, -1, 0), inside=[-36.1, 0.3, -4.1, 36.1, 0.5, 11.1])  # 2
    split_lo = pick(d, kind='plane', normal=(0, 1, 0), inside=[-36.1, -0.5, -4.1, 36.1, -0.3, 11.1]) # 2
    ring_id = pick(d, kind='cyl', r=24.0, area=math.pi*48*7)                                      # 1
    pads_in = pick(d, kind='cyl', r=23.0, inside=[-24.1, -2, 2.9, 24.1, 2, 4.1])                  # 2
    base = pick(d, kind='plane', at=(0, -32, 3.5))                                                # 1
    screws = [f for f in pick(d, kind='cyl', r=1.5)]                                              # 4 shanks
    return ring_od, seat_up, seat_lo, split_up, split_lo, ring_id, pads_in, base, screws
def run(case, el, c, bonded=False):
    ring_od, seat_up, seat_lo, split_up, split_lo, ring_id, pads_in, base, screws = picks()   # print all counts
    F = (0, 300.0, 0) if case == 'Y' else (300.0, 0, 0)
    cs = [(BONDED, ring_od, seat_up + seat_lo)] if bonded else \
         [(NO_PENETRATION, ring_od, seat_up + seat_lo), (NO_PENETRATION, split_up, split_lo)]
    r = static(j, d, f'D2_{case}_{el}_{c}{"_B" if bonded else ""}', PETG,
               fixtures=[('fixed', base), ('fixed', pads_in)],
               loads=[('remote', ring_id, (0, 0, 3.5), F, (0, 0, 0))],
               el=el, ctrl=[(seat_up + seat_lo + ring_od, c), (screws, 0.8), (pads_in, 0.5)],
               contacts=cs, materials=MATS, solver=SOLVER_DIRECT)
    np.savez(...); return r
```
The material log must show 4 screws and the ring Steel, 2 pads Soft pad, the two halves PETG.
Solves: job 2: `run('Y', 2.5, 1.0)`, `run('X', 2.5, 1.0)`, `run('Y', 2.5, 1.0, bonded=True)`, `run('Y', 3.0, 1.5)`.
Job 3: `run('Y', 2.0, 0.7)`, and the governing case (lower factor) at 3.0/1.5 and 2.0/0.7 if it is X.

**Body split by geometry** (05-fea rule 5), radius about Z `rz = hypot(x, y)`, about each screw axis
`rs = hypot(x − x0, z − z0)`:
ring `23.95 ≤ rz ≤ 25.95 and -0.05 ≤ z ≤ 7.05`; pads `22.95 ≤ rz ≤ 24.05, 2.95 ≤ z ≤ 4.05, |y| < 1`; screws: plug
`rs ≤ 1.95, −6.45 ≤ y ≤ −0.35`, shank `rs ≤ 1.55, −0.4 ≤ y ≤ 28.5`, head `rs ≤ 2.8, 28.45 ≤ y ≤ 31.55`; upper half =
rest with y > 0, lower = rest with y < 0. The seat surface nodes coincide with the ring's (line-to-line), so a band
25.95 < rz < 26.05 within Z −0.1..7.1 is left out of both: say so; the seat is judged from nodes ≥ 0.05 mm inside the
housing. Guard: no node of the upper/lower mask with 1.55 < rs < 1.65 on the shank length (the clearance gap).
Use `r.summary(mask=upper & r.away())`, the same for lower; `layer_stress`/`layer_shear` with the same masks.

**Screw load from the study:** for each screw, shank nodes with `|y − 15| < 0.75` and `rs ≤ 1.5`: mean σy (`s[:, 2]`) x
π·1.5² = tension. Also at y 10 and 20 (must agree within 5 %). Sum over four vs the load the upper half carries.

**Contact proof** (05-fea "A body seated on both sides"): (1) bonded twin ring travel (mean UY of ring nodes) many
times smaller than the contact case; (2) bonded twin screws nearly unloaded; (3) in the contact case the lower seat
opens: ring node UY minus lower-housing node UY near (0, −26, 3.5) > 0. All three, with numbers.

**Five checks** per case: reaction ±1 %; ring travel vs 0.3 mm; plain section: upper half crown, X 0, Y 31.9 (top
outer surface, `r.near` of points (0, 32, z) for z in 0, 1, ... 7, dist 0.3): σx (`s[:, 1]`) is TENSION there for +Y
(the ring pushes the middle of the half outward between the screws; the inner shoulder edges at Y 23 are in
compression). Compare with M·3.93/663.6: 8 / 16 / 28 MPa for M 1 350 / 2 700 / 4 650, and say which end condition the
result matches; peak place named; convergence.

**Direction table** per half for normals (0,0,1), (0,1,0), (1,0,0). Chosen: both halves flat on a Z face (Z −4 down),
layers normal Z: the seat circle prints round, the bending stresses lie in the layers. Cost: the Y-axis screw and mount
holes print horizontal (bridged / supported). Y-layer printing would put the screw-to-seat tension across layers.

## 5. Decisions (spec problems: build these, report each)

1. Shoulder opening Ø43.5 is smaller than the inner ring's Ø44.0: it would rub the turning inner ring (0.25 radial
   overlap). Built **Ø46.0**: 1.0 radial clearance to the inner ring (0.85 worst case), 1.0 land on the outer ring face
   (ID 48).
2. Screws at X ±28.2: Ø3.4 hole is 0.5 mm from the Ø52 seat, the Ø4.0 insert hole 0.2 mm (< 0.6; heat-setting would
   push into the seat). Built **X ±31.0**: 3.3 mm (hole) and 3.0 mm (insert) to the seat and to the outside.
3. Screws at Z 1 and Z 6 are 5 mm apart: the Ø6 counterbores overlap by 1.0 mm and two M3 heads (Ø5.5) cannot sit side
   by side. Built **Z −0.2 and 7.2**: 1.4 mm between counterbores, 0.8 mm to the Z faces.
4. "Clamp on a ±0.15 printer": with the halves meeting at Y 0 there is no clamp (or up to 0.3 play). Built a **split
   gap of 0.8** (faces at Y ±0.4, seat circles centred on Y 0): seat radius ±0.15 on each half and each face ±0.15
   (0.6 total) still leave 0.2, so the halves always grip the ring before they meet. Seat **Ø52.0**.
5. Seat length 7.0 equals the bearing width with the shoulders line to line: ±0.15 pinches or rattles. Built the seat
   **Z −0.1..7.1** (0.1 axial clearance each side), shoulders Z −4..−0.1 and 7.1..11.
- Screws: steel pins bonded at the head and in the insert, free along the shank (05-fea "Screws"). No preload: the
  result is for a snug joint; give the screw force at which a factor reaches 2.0 by scaling the screw-region stresses
  (linear only roughly with contact: say so).
- Ring held by two soft pads on its inside at ±X, inner faces fixed (rule 2); the ring stand-in is line-to-line in the
  seat because that is the clamped state (the selftest showed pressed faces are seen in contact).
- The remote load is rigid on a steel ring 100 x stiffer than PETG: no second load model; say so (07-done item 3).

## 6. Branches

- Any pick count wrong: `list_faces(d)`, find it by box; seats are partial cylinders (one face each); the split faces
  are two per half (left, right of the opening).
- "Contact iteration did not converge" or error 24: check the material log (pads matched?), pads touching the ring ID,
  pad fixture count 2. Different way: give the ring 0.02 mm radial clearance and shift it 0.02 toward the load (+Y
  case: ring centre at Y 0.02) so it sits on the loaded seat; solve again. Third way: four pads (add ±Y pads).
- Excessive displacements raised: ring or upper half loose. Upper half held only by the screws: check the heads touch
  the counterbore floors (Y 28.5) and the plugs fill the insert holes; then `loose_ok=True` only after a coarse run
  shows reaction = load.
- Screw tensions sum far from the upper-half load (+Y: 300): check the slab mask is inside the shank; check the three
  heights agree; if the halves touch (split contact active), part of the load goes through them: say so.
- Upper crown σx above 22.5 (factor < 2) and converged: it is the design's thin place. Try in order (07-done "When not
  met"): print direction (it is already in the layers: no gain), material at the peak: raise the upper half's crown by
  making the shoulder opening Ø45.0 (more land, 0.5 clearance to the inner ring) and re-solve; report both.
- Nodes over 200 000 at the fine mesh: el 2.25 with c 0.8; say so.
- Peak at a counterbore rim or plug rim climbing: bonded-edge singularity; read outside 1, 2, 3 mm, report the plateau.
- Over 90 minutes: stop, report how far, mark `valid` false with the reason.
- Anything else: stop D2, record, hand up with the log.

## 7. Done and results

07-done study items 1–8 for both halves and both cases (item 8: the three contact proofs, pad share, screw sum vs load).
`results.json` D2: `spec_problems` (items 1–5, each: what, number, built), `seat_diameter_mm` 52.0, `split_gap_mm` 0.8,
`fit_reasoning`, `clearances_mm` {inner ring to shoulder radial 1.0, outer ring land 1.0, ring axial 0.1 each side,
split gap 0.8, shank in hole 0.2 radial, head in counterbore 0.25 radial, insert hole to seat 3.0, hole to seat 3.3,
counterbore to Z face 0.8}, `hand_screw_load_n` (+Y 75, +X 37), `screw_load_n` (study, per case), `nodes`,
`how_bodies_were_held`, `contact_proof`, `sf_yield`, `sf_layer`, `sf_shear` (lowest over halves and cases),
`governing`, `print_orientation` {upper: "Z −4 face on bed", lower: same}, `valid`, `why`, `minutes`.
