### Stage 2, detail: link_organic built, fixed items measured (stage ended 19.7 min after C2 start)

- Table `STEM_A4`, loft mode arcs4, order stem first; stem 111556.4 mm3, hub added
  21781.8, knuckle added 11747.1, slot removed 31448.6; hub seam blend:
  R2.0 mm on 2 edges.
- Cuts: pin holes 523.0 mm3, cable tunnel 4894.6, screw holes 438.8, screw-head
  clearances 31.98, below the mounting plane 0.0 (0 means nothing stood there).
- Volume 107753.3 mm3, mass **128.2 g** against 261.13 g boxy: lighter.
- One body, rebuild clean. STL watertight True, 1 shell, volume 107591.2 mm3, bounds
  [-35.995, -22.0, -213.0, 35.995, 22.0, 36.0] against the design box [-36.0, -22.0, -213.0, 36.0, 22.0, 36.0]; STEP in mm.
- On the solid's faces: mounting face one flat face at Y -4, area 2355.9 mm2 against
  2355.9 by hand (ring Ø30 to Ø63 less six holes), box [-31.5, -4.0, -31.5, 31.5, -4.0, 31.5]; bore at
  [0.0, 0.0, 0.0]; screw holes at [[-25.0, 0.0, 0.0], [-12.5, 0.0, -21.651], [-12.5, 0.0, 21.651], [12.5, 0.0, -21.651], [12.5, 0.0, 21.651], [25.0, 0.0, 0.0]], each Y -4 to +4; pin holes [{'centre': [0.0, -19.0, -200.0], 'y_from': -22.0, 'y_to': -16.0}, {'centre': [0.0, 19.0, -200.0], 'y_from': 16.0, 'y_to': 22.0}]; inner cheek faces
  {'area_mm2': 616.9, 'box': [-13.0, 16.0, -213.0, 13.0, 16.0, -183.0]} and {'area_mm2': 616.9, 'box': [-13.0, -16.0, -213.0, 13.0, -16.0, -183.0]}.
- On the STL, by sampling (`sheet.inside`), **fixed_items_ok = True**:

| Item | Must be | Measured | |
| --- | --- | --- | --- |
| mount face: solid just above Y -4, Ø31.2 to Ø61.2 | solid | 1.0 of 238 points solid | ok |
| mount face: clear just below Y -4, Ø31.2 to Ø61.2 | clear | 0.0 of 216 points solid | ok |
| mount side: nothing below Y -4 inside Ø62 down to Y -30 | clear | 0.0 of 1080 points solid | ok |
| bore Ø30 clear (sampled Ø29.6) | clear | 0.0 of 605 points solid | ok |
| screw hole 1 Ø3.4 clear (sampled Ø3.2) | clear | 0.0 of 125 points solid | ok |
| screw head 1: Ø7 clear, Y 4 to 14 | clear | 0.0 of 780 points solid | ok |
| screw head 1: seat solid under Y 4 at Ø5.2 | solid | 1.0 of 12 points solid | ok |
| screw hole 2 Ø3.4 clear (sampled Ø3.2) | clear | 0.0 of 125 points solid | ok |
| screw head 2: Ø7 clear, Y 4 to 14 | clear | 0.0 of 780 points solid | ok |
| screw head 2: seat solid under Y 4 at Ø5.2 | solid | 1.0 of 12 points solid | ok |
| screw hole 3 Ø3.4 clear (sampled Ø3.2) | clear | 0.0 of 125 points solid | ok |
| screw head 3: Ø7 clear, Y 4 to 14 | clear | 0.0 of 780 points solid | ok |
| screw head 3: seat solid under Y 4 at Ø5.2 | solid | 1.0 of 12 points solid | ok |
| screw hole 4 Ø3.4 clear (sampled Ø3.2) | clear | 0.0 of 125 points solid | ok |
| screw head 4: Ø7 clear, Y 4 to 14 | clear | 0.0 of 780 points solid | ok |
| screw head 4: seat solid under Y 4 at Ø5.2 | solid | 1.0 of 12 points solid | ok |
| screw hole 5 Ø3.4 clear (sampled Ø3.2) | clear | 0.0 of 125 points solid | ok |
| screw head 5: Ø7 clear, Y 4 to 14 | clear | 0.0 of 780 points solid | ok |
| screw head 5: seat solid under Y 4 at Ø5.2 | solid | 1.0 of 12 points solid | ok |
| screw hole 6 Ø3.4 clear (sampled Ø3.2) | clear | 0.0 of 125 points solid | ok |
| screw head 6: Ø7 clear, Y 4 to 14 | clear | 0.0 of 780 points solid | ok |
| screw head 6: seat solid under Y 4 at Ø5.2 | solid | 1.0 of 12 points solid | ok |
| pin holes Ø8 clear through both cheeks (sampled Ø7.8) | clear | 0.0 of 490 points solid | ok |
| +Y cheek: solid just behind the inner face out to Ø15.8 | solid | 1.0 of 72 points solid | ok |
| +Y cheek: clear just inside the inner face out to Ø16 | clear | 0.0 of 96 points solid | ok |
| +Y cheek: 5 mm of material round the pin hole (solid out to Ø17.6, Y 16.4 to 19.5) | solid | 1.0 of 216 points solid | ok |
| -Y cheek: solid just behind the inner face out to Ø15.8 | solid | 1.0 of 72 points solid | ok |
| -Y cheek: clear just inside the inner face out to Ø16 | clear | 0.0 of 96 points solid | ok |
| -Y cheek: 5 mm of material round the pin hole (solid out to Ø17.6, Y 16.4 to 19.5) | solid | 1.0 of 216 points solid | ok |
| slot: Ø30 swept cylinder about the pin clear, |Y| < 15.8 | clear | 0.0 of 1305 points solid | ok |
| slot: clear from Z -183 down, |Y| < 15.8, all X | clear | 0.0 of 972 points solid | ok |
| cable: Ø6 straight passage clear along Z at X 0, Y 0, from the bore to the slot | clear | 0.0 of 4440 points solid | ok |
| cable: enclosed (solid beside the tunnel at X ±3.6, Z -30 to -160) | solid | 1.0 of 28 points solid | ok |

- Print: tilted 30 degrees, hub end down: the long axis leans 30 degrees from the vertical towards +X, the hub (elbow) end is at the bed and the fork is at the top; height about 222 mm of 256, footprint about 120 x 120 mm. Layers are flat on the bed, so in the part they are stacked along (0.5, 0, -0.866). Printed with a brim, no raft. Supports: under the lowest part of the hub rim and inside the bore, and a few small patches; the numbers are in orientations.json. No enclosed cavity: the cable tunnel is open at both ends; thinnest wall 0.8 mm (the tunnel
  under the hub's two faces, Z -15 to -22).
- Shape numbers: {'triangles': 13964, 'area_mm2': 28965.4, 'flat_share': 0.201, 'largest_flat': 0.081, 'sharp_mm': 845.8, 'sharp_per_area': 4.97, 'bbox_mm': [71.99, 44.0, 249.0]}.
- Checkpoint 2: 19.7 min after C2 start, `pictures/checkpoint_02.png`. Still missing against the request: the study (three load cases) and the before-and-after sheet; fixed items failing: none; hub seam blend R2.0; sharp_per_area 4.97, flat_share 0.201.
- What I see in checkpoint_02.png, one line: a bone with a deeper, rounder neck just below the hub, the stem straight to the fork, six screw holes and two pin holes.

### Stage 3, study (stage ended 30.3 min after C2 start)

Model `_wip/sw-eval/haiku-plan-c-round3/link_organic_fea.SLDPRT`, a copy of the exported part (volume checked). Printed PETG. Held:
the mounting face (the flat ring at Y -4, Ø30 to Ø63). Loads: 60 N; +X and -X as bearing loads on the two pin holes;
+Y as an even pressure on the inner face of the +Y cheek, because a force along the pin is not a bearing load on its
holes (`static()` refuses it): the part between the cheeks pushes on that face. Layers as printed tilted 30 degrees towards +X, hub end down. Peaks are read
at least 3.0 mm from the held face and from the loaded faces. Global element sizes [4.0, 3.0, 2.3] mm, 1.2 mm on the
cable tunnel and 1.0 mm on the pin holes at every size.

| Case | el mm | Nodes | von Mises MPa | Across layers MPa | Between layers MPa | Max disp mm | Reaction N | von Mises peak at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| +X | 4.0 | 89009 | 5.163 | 5.298 | 2.558 | 2.789 | [-60.0, -0.005, -0.001] | [15.95, 4.17, -22.69] |
| +X | 3.0 | 125376 | 5.24 | 5.354 | 2.546 | 2.79 | [-59.998, 0.003, 0.005] | [-16.66, -2.61, -32.01] |
| +X | 2.3 | 189752 | 5.721 | 5.7 | 2.578 | 2.791 | [-60.0, 0.002, -0.001] | [-14.22, -3.1, -32.4] |
| -X | 4.0 | 89009 | 5.163 | 3.896 | 2.558 | 2.789 | [60.0, 0.005, 0.001] | [15.95, 4.17, -22.69] |
| -X | 3.0 | 125376 | 5.24 | 4.413 | 2.546 | 2.79 | [59.998, -0.003, -0.005] | [-16.66, -2.61, -32.01] |
| -X | 2.3 | 189752 | 5.721 | 4.589 | 2.578 | 2.791 | [60.0, -0.002, 0.001] | [-14.22, -3.1, -32.4] |
| +Y | 4.0 | 89009 | 18.741 | 12.382 | 9.331 | 5.785 | [-0.003, -59.997, -0.004] | [9.22, 4.32, -23.13] |
| +Y | 3.0 | 125376 | 18.686 | 12.814 | 9.272 | 5.794 | [-0.002, -59.993, -0.01] | [-8.98, 4.17, -22.39] |
| +Y | 2.3 | 189752 | 18.943 | 13.223 | 9.339 | 5.804 | [0.002, -59.999, 0.002] | [9.22, 4.32, -23.13] |

Verdict from `swfea.judge()`, need 2.0: **fail**, lowest factor **1.39** at "+Y, shear", place [-8.98, 4.17, -22.39].

| Entry | Values coarse to fine MPa | Factor | Last step % | State |
| --- | --- | --- | --- | --- |
| +X, vm | [5.163, 5.24, 5.721] | 7.87 | 9.2 | pass |
| +X, layer | [5.298, 5.354, 5.7] | 3.95 | 6.5 | pass |
| +X, shear | [2.558, 2.546, 2.578] | 5.04 | 1.3 | pass |
| -X, vm | [5.163, 5.24, 5.721] | 7.87 | 9.2 | pass |
| -X, layer | [3.896, 4.413, 4.589] | 4.9 | 4.0 | pass |
| -X, shear | [2.558, 2.546, 2.578] | 5.04 | 1.3 | pass |
| +Y, vm | [18.741, 18.686, 18.943] | 2.38 | 1.4 | pass |
| +Y, layer | [12.382, 12.814, 13.223] | 1.7 | 3.2 | fail |
| +Y, shear | [9.331, 9.272, 9.339] | 1.39 | 0.7 | fail |

- Keys: sf_yield 2.33, sf_layer 1.67, sf_shear 1.37 (lowest of the three cases at
  2.3 mm, and for +Y the higher of the two ways to load it).
- Not converged: nothing: every entry settled.
- +Y loaded a second way at 3.0 mm (rigid, on both pin holes at the pin axis): rigid over pressure
  {'vm': 1.018, 'layer': 1.018, 'shear': 1.018} (von Mises, across layers, between layers).
- Hand check at the waist (Z -115), mean over 2 mm against M / Z: [('+X', {'hand_mpa': 4.47, 'mean_vm_2mm': 4.19, 'nodes': 23, 'at': (10.8, 0.0, -115.0)}), ('-X', {'hand_mpa': 4.47, 'mean_vm_2mm': 4.2, 'nodes': 23, 'at': (-10.8, 0.0, -115.0)}), ('+Y', {'hand_mpa': 4.03, 'mean_vm_2mm': 3.75, 'nodes': 24, 'at': (0.0, 12.0, -115.0)})].
- Reaction equals load in every study (table). -X against +X, von Mises: 0.00 % apart (the part is
  symmetric about X = 0, so they must agree).
- Excluded: the peak anywhere, including the held edge and the loaded faces, at 2.3 mm:
  [('+X', 6.665), ('-X', 6.665), ('+Y', 32.414)] MPa; on the loaded faces themselves
  [('+X', 2.399), ('-X', 2.315), ('+Y', 9.737)] MPa. Peak outside 2, 3 and 5 mm:
  [('+X', {'2.0': 5.721, '3.0': 5.721, '5.0': 5.122}), ('-X', {'2.0': 5.721, '3.0': 5.721, '5.0': 5.122}), ('+Y', {'2.0': 18.943, '3.0': 18.943, '5.0': 18.943})].
- At the governing peak, mean von Mises over 0.5, 1 and 2 mm (value, nodes): {'0.5': [16.0, 3], '1.0': [13.61, 12], '2.0': [9.33, 64]}.
- The same results read for the other print directions (2.3 mm), lowest factor of the three measures and three
  cases: {'X': 2.38, 'Y': 1.34, 'Z (upright)': 1.32, 'tilt 20 to X': 1.34, 'tilt 30 to X': 1.39, 'tilt 45 to X': 1.51, 'tilt 20 to Y': 1.63, 'tilt 30 to Y': 1.78, 'tilt 45 to Y': 1.77}.

| Case | Layers along | von Mises | Across layers | Between layers |
| --- | --- | --- | --- | --- |
| +X | X | 5.721 | 1.578 | 1.652 |
| +X | Y | 5.721 | 1.864 | 2.532 |
| +X | Z (upright) | 5.721 | 6.196 | 2.526 |
| +X | tilt 20 to X | 5.721 | 6.159 | 2.566 |
| +X | tilt 30 to X | 5.721 | 5.7 | 2.578 |
| +X | tilt 45 to X | 5.721 | 4.603 | 2.686 |
| +X | tilt 20 to Y | 5.721 | 5.844 | 2.712 |
| +X | tilt 30 to Y | 5.721 | 5.615 | 3.003 |
| +X | tilt 45 to Y | 5.721 | 5.398 | 2.814 |
| -X | X | 5.721 | 1.476 | 1.652 |
| -X | Y | 5.721 | 1.653 | 2.532 |
| -X | Z (upright) | 5.721 | 6.223 | 2.526 |
| -X | tilt 20 to X | 5.721 | 5.328 | 2.566 |
| -X | tilt 30 to X | 5.721 | 4.589 | 2.578 |
| -X | tilt 45 to X | 5.721 | 3.345 | 2.686 |
| -X | tilt 20 to Y | 5.721 | 5.856 | 2.712 |
| -X | tilt 30 to Y | 5.721 | 5.454 | 3.003 |
| -X | tilt 45 to Y | 5.721 | 5.246 | 2.814 |
| +Y | X | 18.943 | 7.613 | 4.616 |
| +Y | Y | 18.943 | 12.547 | 9.696 |
| +Y | Z (upright) | 18.943 | 14.864 | 9.853 |
| +Y | tilt 20 to X | 18.943 | 14.143 | 9.709 |
| +Y | tilt 30 to X | 18.943 | 13.223 | 9.339 |
| +Y | tilt 45 to X | 18.943 | 11.437 | 8.608 |
| +Y | tilt 20 to Y | 18.943 | 13.262 | 7.962 |
| +Y | tilt 30 to Y | 18.943 | 12.663 | 6.42 |
| +Y | tilt 45 to Y | 18.943 | 11.89 | 7.34 |

- Load path: the pin presses on the two pin holes (or, for +Y, the swinging part on the +Y cheek), the cheeks carry
  it up either side of the arch into the stem, the stem bends, and the neck hands it to the hub over the held ring.

- The three measures for the tilted print at the finest mesh, read outside 2, 3 and 5 mm from the held and loaded faces (the verdict uses 3.0 mm): [('+X', {'2.0': {'vm': 5.721, 'layer': 5.826, 'shear': 2.578}, '3.0': {'vm': 5.721, 'layer': 5.7, 'shear': 2.578}, '5.0': {'vm': 5.122, 'layer': 4.637, 'shear': 2.564}}), ('-X', {'2.0': {'vm': 5.721, 'layer': 5.206, 'shear': 2.578}, '3.0': {'vm': 5.721, 'layer': 4.589, 'shear': 2.578}, '5.0': {'vm': 5.122, 'layer': 4.172, 'shear': 2.564}}), ('+Y', {'2.0': {'vm': 18.943, 'layer': 16.996, 'shear': 9.339}, '3.0': {'vm': 18.943, 'layer': 13.223, 'shear': 9.339}, '5.0': {'vm': 18.943, 'layer': 9.641, 'shear': 9.339}})]

### Stage 4, result (C2 took 30.8 min; the whole set 30.8 min on times.log)

| Gate | |
| --- | --- |
| Fixed items intact | True |
| One body, watertight | True |
| Factor at least 2.0 on all three measures, three cases | False (verdict from judge(): fail; 2.33 / 1.67 / 1.37) |
| Mass not above the boxy link | True (128.23 g against 261.13 g) |

Deliverables: `restate.md`, `pictures/idea_a.png`, `pictures/idea_b.png`, `pictures/checkpoint_01.png` to `_03.png`,
`pictures/c2_before_after.png` (both STLs in one call), `link_organic.SLDPRT` / `.step` / `.stl` in
`_wip/sw-eval/haiku-plan-c-round3/`, `DESIGN.md`, `fea_rows.json`, `times.log`.

| Checkpoint | Min after C2 start | Picture | Still missing against the request |
| --- | --- | --- | --- |
| 2 | 19.7 | `pictures/checkpoint_02.png` | the study (three load cases) and the before-and-after sheet; fixed items failing: none; hub seam blend R2.0; sharp_per_area 4.97, flat_share 0.201 |
| 3 | 30.8 | `pictures/checkpoint_03.png` | gate items not met: ['requirement_met']; verdict fail, lowest factor 1.39; against the look asked for: sharp_per_area 4.97 (boxy 12.3), flat_share 0.201 (boxy 0.91); the hub seam is blended R2.0 |

Shape numbers, before: {'triangles': 1632, 'area_mm2': 38261.4, 'flat_share': 0.91, 'largest_flat': 0.144, 'sharp_mm': 2406.4, 'sharp_per_area': 12.3, 'bbox_mm': [70.0, 44.0, 250.0]}. After: {'triangles': 13964, 'area_mm2': 28965.4, 'flat_share': 0.201, 'largest_flat': 0.081, 'sharp_mm': 845.8, 'sharp_per_area': 4.97, 'bbox_mm': [71.99, 44.0, 249.0]}.

- **Thinnest margin:** +Y, shear at [-8.98, 4.17, -22.39] (factor 1.39). At this factor the part carries 41.7 N at the wrist before the
  factor is 2.0; a sharper seam as printed, or the load taken on one cheek only, is what would eat it.
- **Cheapest improvement found:** the stem loft was untwisted and the print direction changed to a 30 degree tilt, hub end down; all directions read
  ({'X': 2.38, 'Y': 1.34, 'Z (upright)': 1.32, 'tilt 20 to X': 1.34, 'tilt 30 to X': 1.39, 'tilt 45 to X': 1.51, 'tilt 20 to Y': 1.63, 'tilt 30 to Y': 1.78, 'tilt 45 to Y': 1.77}); the fork end above the arch is solid and lightly stressed, so mass can come
  out there first.
- **Not checked:** buckling (the stem is stocky: about 22 mm across over 140 mm); the pin's own bending and a loose
  pin (a bearing load covers half the hole exactly); screw preload on the 8 mm hub; the 0.8 mm skins over the cable
  tunnel in print; whether the motor's body leaves room for the stem below Y -4 outside Ø62 (the boxy link went to
  Y -15 there too); fatigue.
- What I see in c2_before_after.png, one line: top row the boxy block link, bottom row the organic bone with a smooth stem to the fork and a deeper, rounder neck just below the hub.


## C2 round 3, T5 report

**1. State: not done: requirement not met.** Gate from `c2_finish.py`: fixed_items_ok true, one_body_watertight true,
requirement_met **false**, mass_not_above_boxy true (128.23 g against 261.13 g). Verdict `fail`, lowest factor 1.39 at
"+Y, shear", place [-8.98, 4.17, -22.39] (the neck, Z -22.4). Values of that entry: [9.331, 9.272, 9.339] MPa, limit 13.0.
Other entries: "+Y, layer" 1.70 (values [12.382, 12.814, 13.223], limit 22.5); "+Y, vm" 2.38.

**2. Round 2 (STEM_A3) against round 3 (STEM_A4).**

| | Round 2, STEM_A3 | Round 3, STEM_A4 |
| --- | --- | --- |
| Mass, g | 124.53 | 128.23 |
| Verdict | fail | fail |
| Lowest factor | 1.57 | 1.39 |
| Lowest entry and place | "+Y, layer" at [0.28, -3.19, -34.48] | "+Y, shear" at [-8.98, 4.17, -22.39] |
| Largest twist, degrees | 16.7 (Z -72 to -85), TWIST_CHECK ok | 0.5 (Z -46 to -60 and Z -130 to -145), TWIST_CHECK ok |
| Half width at Z -78, mm | 12.17 | 12.13 |
| Support area, chosen direction, mm2 | 692 | 702 |
| Height, chosen direction, mm | 222.2 | 222.2 |

**3. Patches of the chosen print direction** (tilt 30 to +X, hub end down; `orientations.json`; 702 mm2 total, bed contact 11.4 mm2,
footprint 121 x 120 mm):
- 269 mm2 at [-16, 0, 28]: hub rim (Z above +20).
- 162 mm2 at [9, 0, -10]: inside the bore (X and Z both within 16 of the Y axis line through the hub).
- 42 mm2 at [2, -19, -203]: fork (Z below -190).
- 42 mm2 at [2, 19, -203]: fork.
- 21 mm2 at [13, 0, -23]: stem.
- 21 mm2 at [13, 0, 20]: stem.
- 21 mm2 at [-24, 0, -1]: stem.
- 21 mm2 at [26, 0, -1]: stem.

Whether the patches on the hub rim and the stem are acceptable is Joey's decision.

**4. Nine directions** (readings, not verdicts; lowest of 45 / von Mises, 22.5 / across layers, 13 / between layers over +X, -X, +Y at the finest mesh;
the script's own summary agrees):
- X: 2.38 (+Y, von Mises).
- Y: 1.34 (+Y, between layers).
- Z (upright): 1.32 (+Y, between layers).
- tilt 20 to X: 1.34 (+Y, between layers).
- tilt 30 to X: 1.39 (+Y, between layers).
- tilt 45 to X: 1.51 (+Y, between layers).
- tilt 20 to Y: 1.63 (+Y, between layers).
- tilt 30 to Y: 1.78 (+Y, across layers).
- tilt 45 to Y: 1.77 (+Y, between layers).

**5. Branches taken.** None in T2: `c2_detail.py` ran once, and the screw-head scallop check passed at 31.98 mm3 (expected 30); no
"scallops are shallow" stop, no volume stop, no fixed-item fail. T2 checks all passed: `TWIST_CHECK ok`, `PINCH_CHECK ok`, `PRINT_CHECK ok`.
T3 verdict `fail`: per T3.4, nothing was changed or rerun. The 16 minutes from round-3 start to C2 detail start were a hold for another
thread's SolidWorks build (the coordinator's hold until 22:39:06), not a branch.

**6. Times** (from `times.log`, clock -0600, 2026-11-14):

| Step | Between | Min |
| --- | --- | --- |
| T1 set-up (no SolidWorks) | round 3 start 22:23:50, C2 start 22:23:50 | 0.0 |
| Hold (no SolidWorks) | 22:23:50 to detail start 22:39:30 | 15.7 |
| T2 part, twist, pinch, print | detail start 22:39:30 to study start 22:43:47 | 4.3 |
| T3 study | study start 22:43:47 to study end 22:54:08 | 10.4 |
| T4 finish | study end 22:54:08 to C2 end 22:54:38 | 0.5 |

Total: 30.8 min (C2 start 22:23:50 to C2 end 22:54:38). `c2_detail.py` runs: one. `c2_fea.py` runs: one.

**7. Anything wrong in these instructions or the helpers.**
- T3.1 expected the lowest factor between 1.9 and 2.4 and "+Y, layer" at the neck. Measured 1.39 "+Y, shear", the entry changed
  and the factor is below the range. Report as measured.
- T3.2 place: -22.4 in Z is just above the -25 to -45 band the earlier rounds expected.
- The round-3 header says "for the builder of `eval/haiku-plan-c-round2/`", a copy-over from round 2. Harmless.
- The hold for the other thread's SolidWorks build is not in the instructions; it cost 15.7 minutes of the clock.
