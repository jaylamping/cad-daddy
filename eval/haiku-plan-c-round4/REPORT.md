### Stage 2, detail: link_organic built, fixed items measured (stage ended 1.3 min after C2 start)

- Table `STEM_A5`, loft mode arcs4, order stem first; stem 111696.8 mm3, hub added
  21813.4, knuckle added 11746.5, slot removed 31447.9; hub seam blend:
  not built (tried R3, R2, R1.2 on 2 edges).
- Cuts: pin holes 523.0 mm3, cable tunnel 4894.6, screw holes 436.2, screw-head
  clearances 14.66, below the mounting plane 0.0 (0 means nothing stood there).
- Volume 107940.3 mm3, mass **128.4 g** against 261.13 g boxy: lighter.
- One body, rebuild clean. STL watertight True, 1 shell, volume 107784.1 mm3, bounds
  [-35.985, -22.0, -213.0, 35.985, 22.0, 35.942] against the design box [-36.0, -22.0, -213.0, 36.0, 22.0, 36.0]; STEP in mm.
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
- Shape numbers: {'triangles': 15188, 'area_mm2': 29011.7, 'flat_share': 0.202, 'largest_flat': 0.081, 'sharp_mm': 866.3, 'sharp_per_area': 5.09, 'bbox_mm': [71.97, 44.0, 248.94]}.
- Checkpoint 2: 1.3 min after C2 start, `pictures/checkpoint_02.png`. Still missing against the request: the study (three load cases) and the before-and-after sheet; fixed items failing: none; hub seam blend did not build: a crease is left where the stem leaves the hub; sharp_per_area 5.09, flat_share 0.202.
- What I see in checkpoint_02.png, one line: a bone with a straight stem to the fork, a lower neck with a shallow step under the hub, six screw holes and two pin holes.

### Stage 3, study (stage ended 12.4 min after C2 start)

Model `_wip/sw-eval/haiku-plan-c-round4/link_organic_fea.SLDPRT`, a copy of the exported part (volume checked). Printed PETG. Held:
the mounting face (the flat ring at Y -4, Ø30 to Ø63). Loads: 60 N; +X and -X as bearing loads on the two pin holes;
+Y as an even pressure on the inner face of the +Y cheek, because a force along the pin is not a bearing load on its
holes (`static()` refuses it): the part between the cheeks pushes on that face. Layers as printed tilted 30 degrees towards +X, hub end down. Peaks are read
at least 3.0 mm from the held face and from the loaded faces. Global element sizes [4.0, 3.0, 2.3] mm, 1.2 mm on the
cable tunnel and 1.0 mm on the pin holes at every size.

| Case | el mm | Nodes | von Mises MPa | Across layers MPa | Between layers MPa | Max disp mm | Reaction N | von Mises peak at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| +X | 4.0 | 88869 | 6.29 | 6.592 | 2.858 | 2.78 | [-60.001, -0.003, 0.006] | [-18.48, -1.87, -31.35] |
| +X | 3.0 | 125674 | 6.063 | 6.906 | 2.88 | 2.781 | [-59.998, -0.001, -0.002] | [-18.82, -1.72, -31.12] |
| +X | 2.3 | 188790 | 6.446 | 6.762 | 2.952 | 2.783 | [-59.999, -0.0, -0.0] | [18.26, -1.95, -31.41] |
| -X | 4.0 | 88869 | 6.29 | 6.065 | 2.858 | 2.78 | [60.001, 0.003, -0.006] | [-18.48, -1.87, -31.35] |
| -X | 3.0 | 125674 | 6.063 | 6.124 | 2.88 | 2.781 | [59.998, 0.001, 0.002] | [-18.82, -1.72, -31.12] |
| -X | 2.3 | 188790 | 6.446 | 5.923 | 2.952 | 2.783 | [59.999, 0.0, 0.0] | [18.26, -1.95, -31.41] |
| +Y | 4.0 | 88869 | 14.949 | 12.886 | 7.43 | 5.892 | [-0.003, -60.005, -0.003] | [-9.48, 4.55, -23.61] |
| +Y | 3.0 | 125674 | 15.112 | 12.309 | 7.334 | 5.896 | [0.001, -59.987, 0.0] | [9.48, 4.55, -23.61] |
| +Y | 2.3 | 188790 | 15.077 | 12.514 | 7.297 | 5.92 | [-0.005, -60.003, 0.001] | [-9.49, 4.56, -23.63] |

Verdict from `swfea.judge()`, need 2.0: **fail**, lowest factor **1.78** at "+Y, shear", place [-15.21, 4.57, -24.02].

| Entry | Values coarse to fine MPa | Factor | Last step % | State |
| --- | --- | --- | --- | --- |
| +X, vm | [6.29, 6.063, 6.446] | 6.98 | 6.3 | pass |
| +X, layer | [6.592, 6.906, 6.762] | 3.33 | 2.1 | pass |
| +X, shear | [2.858, 2.88, 2.952] | 4.4 | 2.5 | pass |
| -X, vm | [6.29, 6.063, 6.446] | 6.98 | 6.3 | pass |
| -X, layer | [6.065, 6.124, 5.923] | 3.8 | 3.3 | pass |
| -X, shear | [2.858, 2.88, 2.952] | 4.4 | 2.5 | pass |
| +Y, vm | [14.949, 15.112, 15.077] | 2.98 | 0.2 | pass |
| +Y, layer | [12.886, 12.309, 12.514] | 1.8 | 1.7 | fail |
| +Y, shear | [7.43, 7.334, 7.297] | 1.78 | 0.5 | fail |

- Keys: sf_yield 2.93, sf_layer 1.77, sf_shear 1.75 (lowest of the three cases at
  2.3 mm, and for +Y the higher of the two ways to load it).
- Not converged: nothing: every entry settled.
- +Y loaded a second way at 3.0 mm (rigid, on both pin holes at the pin axis): rigid over pressure
  {'vm': 1.018, 'layer': 1.018, 'shear': 1.018} (von Mises, across layers, between layers).
- Hand check at the waist (Z -115), mean over 2 mm against M / Z: [('+X', {'hand_mpa': 4.47, 'mean_vm_2mm': 4.18, 'nodes': 28, 'at': (10.8, 0.0, -115.0)}), ('-X', {'hand_mpa': 4.47, 'mean_vm_2mm': 4.26, 'nodes': 23, 'at': (-10.8, 0.0, -115.0)}), ('+Y', {'hand_mpa': 4.03, 'mean_vm_2mm': 3.76, 'nodes': 21, 'at': (0.0, 12.0, -115.0)})].
- Reaction equals load in every study (table). -X against +X, von Mises: 0.00 % apart (the part is
  symmetric about X = 0, so they must agree).
- Excluded: the peak anywhere, including the held edge and the loaded faces, at 2.3 mm:
  [('+X', 7.031), ('-X', 7.031), ('+Y', 40.177)] MPa; on the loaded faces themselves
  [('+X', 2.278), ('-X', 2.324), ('+Y', 9.754)] MPa. Peak outside 2, 3 and 5 mm:
  [('+X', {'2.0': 6.446, '3.0': 6.446, '5.0': 6.446}), ('-X', {'2.0': 6.446, '3.0': 6.446, '5.0': 6.446}), ('+Y', {'2.0': 15.361, '3.0': 15.077, '5.0': 15.077})].
- At the governing peak, mean von Mises over 0.5, 1 and 2 mm (value, nodes): {'0.5': [15.08, 1], '1.0': [12.19, 4], '2.0': [9.21, 35]}.
- The same results read for the other print directions (2.3 mm), lowest factor of the three measures and three
  cases: {'X': 2.97, 'Y': 1.72, 'Z (upright)': 1.57, 'tilt 20 to X': 1.67, 'tilt 30 to X': 1.78, 'tilt 45 to X': 1.84, 'tilt 20 to Y': 1.71, 'tilt 30 to Y': 1.78, 'tilt 45 to Y': 1.81}.

| Case | Layers along | von Mises | Across layers | Between layers |
| --- | --- | --- | --- | --- |
| +X | X | 6.446 | 2.296 | 1.61 |
| +X | Y | 6.446 | 2.136 | 2.35 |
| +X | Z (upright) | 6.446 | 7.395 | 2.339 |
| +X | tilt 20 to X | 6.446 | 7.25 | 2.69 |
| +X | tilt 30 to X | 6.446 | 6.762 | 2.952 |
| +X | tilt 45 to X | 6.446 | 5.68 | 3.035 |
| +X | tilt 20 to Y | 6.446 | 6.533 | 3.194 |
| +X | tilt 30 to Y | 6.446 | 5.895 | 3.36 |
| +X | tilt 45 to Y | 6.446 | 4.54 | 3.052 |
| -X | X | 6.446 | 2.528 | 1.61 |
| -X | Y | 6.446 | 2.232 | 2.35 |
| -X | Z (upright) | 6.446 | 8.201 | 2.339 |
| -X | tilt 20 to X | 6.446 | 6.899 | 2.69 |
| -X | tilt 30 to X | 6.446 | 5.923 | 2.952 |
| -X | tilt 45 to X | 6.446 | 4.372 | 3.035 |
| -X | tilt 20 to Y | 6.446 | 7.481 | 3.194 |
| -X | tilt 30 to Y | 6.446 | 6.68 | 3.36 |
| -X | tilt 45 to Y | 6.446 | 5.183 | 3.052 |
| +Y | X | 15.077 | 6.675 | 4.375 |
| +Y | Y | 15.077 | 12.872 | 7.577 |
| +Y | Z (upright) | 15.077 | 14.331 | 7.921 |
| +Y | tilt 20 to X | 15.077 | 13.507 | 7.754 |
| +Y | tilt 30 to X | 15.077 | 12.514 | 7.297 |
| +Y | tilt 45 to X | 15.077 | 10.615 | 7.058 |
| +Y | tilt 20 to Y | 15.077 | 13.18 | 6.789 |
| +Y | tilt 30 to Y | 15.077 | 12.629 | 6.765 |
| +Y | tilt 45 to Y | 15.077 | 12.449 | 7.126 |

- Load path: the pin presses on the two pin holes (or, for +Y, the swinging part on the +Y cheek), the cheeks carry
  it up either side of the arch into the stem, the stem bends, and the neck hands it to the hub over the held ring.

- The three measures for the tilted print at the finest mesh, read outside 2, 3 and 5 mm from the held and loaded faces (the verdict uses 3.0 mm): [('+X', {'2.0': {'vm': 6.446, 'layer': 6.762, 'shear': 2.952}, '3.0': {'vm': 6.446, 'layer': 6.762, 'shear': 2.952}, '5.0': {'vm': 6.446, 'layer': 6.039, 'shear': 2.943}}), ('-X', {'2.0': {'vm': 6.446, 'layer': 6.362, 'shear': 2.952}, '3.0': {'vm': 6.446, 'layer': 5.923, 'shear': 2.952}, '5.0': {'vm': 6.446, 'layer': 4.894, 'shear': 2.943}}), ('+Y', {'2.0': {'vm': 15.361, 'layer': 16.332, 'shear': 7.297}, '3.0': {'vm': 15.077, 'layer': 12.514, 'shear': 7.297}, '5.0': {'vm': 15.077, 'layer': 9.491, 'shear': 7.297}})]

### Stage 4, result (C2 took 12.8 min; the whole set 12.8 min on times.log)

| Gate | |
| --- | --- |
| Fixed items intact | True |
| One body, watertight | True |
| Factor at least 2.0 on all three measures, three cases | False (verdict from judge(): fail; 2.93 / 1.77 / 1.75) |
| Mass not above the boxy link | True (128.45 g against 261.13 g) |

Deliverables: `restate.md`, `pictures/idea_a.png`, `pictures/idea_b.png`, `pictures/checkpoint_01.png` to `_03.png`,
`pictures/c2_before_after.png` (both STLs in one call), `link_organic.SLDPRT` / `.step` / `.stl` in
`_wip/sw-eval/haiku-plan-c-round4/`, `DESIGN.md`, `fea_rows.json`, `times.log`.

| Checkpoint | Min after C2 start | Picture | Still missing against the request |
| --- | --- | --- | --- |
| 2 | 1.3 | `pictures/checkpoint_02.png` | the study (three load cases) and the before-and-after sheet; fixed items failing: none; hub seam blend did not build: a crease is left where the stem leaves the hub; sharp_per_area 5.09, flat_share 0.202 |
| 3 | 12.8 | `pictures/checkpoint_03.png` | gate items not met: ['requirement_met']; verdict fail, lowest factor 1.78; against the look asked for: sharp_per_area 5.09 (boxy 12.3), flat_share 0.202 (boxy 0.91); the hub seam is still a crease |

Shape numbers, before: {'triangles': 1632, 'area_mm2': 38261.4, 'flat_share': 0.91, 'largest_flat': 0.144, 'sharp_mm': 2406.4, 'sharp_per_area': 12.3, 'bbox_mm': [70.0, 44.0, 250.0]}. After: {'triangles': 15188, 'area_mm2': 29011.7, 'flat_share': 0.202, 'largest_flat': 0.081, 'sharp_mm': 866.3, 'sharp_per_area': 5.09, 'bbox_mm': [71.97, 44.0, 248.94]}.

- **Thinnest margin:** +Y, shear at [-15.21, 4.57, -24.02] (factor 1.78). At this factor the part carries 53.4 N at the wrist before the
  factor is 2.0; a sharper seam as printed, or the load taken on one cheek only, is what would eat it.
- **Cheapest improvement found:** the stem loft was untwisted and the print direction changed to a 30 degree tilt, hub end down; all directions read
  ({'X': 2.97, 'Y': 1.72, 'Z (upright)': 1.57, 'tilt 20 to X': 1.67, 'tilt 30 to X': 1.78, 'tilt 45 to X': 1.84, 'tilt 20 to Y': 1.71, 'tilt 30 to Y': 1.78, 'tilt 45 to Y': 1.81}); the fork end above the arch is solid and lightly stressed, so mass can come
  out there first.
- **Not checked:** buckling (the stem is stocky: about 22 mm across over 140 mm); the pin's own bending and a loose
  pin (a bearing load covers half the hole exactly); screw preload on the 8 mm hub; the 0.8 mm skins over the cable
  tunnel in print; whether the motor's body leaves room for the stem below Y -4 outside Ø62 (the boxy link went to
  Y -15 there too); fatigue.
- What I see in c2_before_after.png, one line: top row the boxy block link, bottom row the organic bone with a smooth stem to the fork and a lower neck with a shallow step under the hub.


## C2 round 4, T5 report

**1. State: not done: requirement not met.** Gate from `c2_finish.py`: fixed_items_ok true, one_body_watertight true,
requirement_met **false**, mass_not_above_boxy true (128.45 g against 261.13 g). Verdict `fail`, lowest factor 1.78 at
"+Y, shear", place [-15.21, 4.57, -24.02] (the neck, Z -24). Its values: [7.43, 7.334, 7.297] MPa against the 13.0 limit.
Other +Y entries at the finest mesh: "+Y, layer" 1.80 (values [12.886, 12.309, 12.514] against 22.5), "+Y, vm" 2.98.

**2. Round 2, round 3 and round 4 side by side.**

| | Round 2 (STEM_A3) | Round 3 (STEM_A4) | Round 4 (STEM_A5) |
| --- | --- | --- | --- |
| Mass, g | 124.53 | 128.23 | 128.45 |
| Verdict | fail | fail | fail |
| Lowest factor | 1.57 | 1.39 | 1.78 |
| Lowest entry and place | "+Y, layer" at [0.28, -3.19, -34.48] | "+Y, shear" at [-8.98, 4.17, -22.39] | "+Y, shear" at [-15.21, 4.57, -24.02] |
| Largest twist, degrees | 16.7 (Z -72 to -85) | 0.5 | 1.2 (Z -72 to -85) |
| TWIST_CHECK / PINCH_CHECK | ok / ok | ok / ok | ok / ok |
| Half width at Z -78, mm | 12.17 | 12.13 | 12.14 |
| Support area, chosen direction, mm2 | 692 | 702 | 765 |
| Height, chosen direction, mm | 222.2 | 222.2 | 222.2 |
| Bed contact, chosen direction, mm2 | 8.2 | 11.4 | 8.1 |

**3. The load along Y at the finest mesh (2.3 mm), chosen print direction (tilt 30 to +X, hub end down), round 3 against round 4.**
Places are the point where the script recorded each peak (`fea_rows.json`).

| Measure | Round 3 (STEM_A4) | Round 4 (STEM_A5) |
| --- | --- | --- |
| von Mises, MPa | 18.943 at [9.22, 4.32, -23.13] | 15.077 at [-9.49, 4.56, -23.63] |
| Across layers, MPa | 13.223 at [0.28, -3.19, -34.48] | 12.514 at [0.28, -3.19, -34.48] |
| Between layers, MPa | 9.339 at [-8.98, 4.17, -22.39] | 7.297 at [-15.21, 4.57, -24.02] |

**4. Patches of the chosen print direction** (tilt 30 to +X, hub end down; `orientations.json`; 765 mm2 total, bed contact 8.1 mm2,
footprint 121 x 120 mm, height 222.2 mm):
- 274 mm2 at [-16, 0, 28]: hub rim (Z above +20).
- 162 mm2 at [9, 0, -10]: inside the bore (X and Z both within 16 of the Y axis line through the hub).
- 75 mm2 at [-18, 9, -29]: stem (Z -29 is not above +20, and X -18 is outside the bore band of 16 mm).
- 42 mm2 at [2, -19, -203]: fork (Z below -190).
- 42 mm2 at [2, 19, -203]: fork.
- 21 mm2 at [13, 0, -23]: stem.
- 21 mm2 at [13, 0, 20]: stem.
- 21 mm2 at [-24, 0, -1]: stem.
- 21 mm2 at [26, 0, -1]: stem.

Whether the patches on the hub rim and the stem are acceptable is Joey's decision.

**5. The nine direction lines** (readings, not verdicts; the lowest of 45 / von Mises, 22.5 / across layers, 13 / between layers, over +X, -X, +Y at the finest mesh):
- X: 2.98 (+Y, von Mises).
- Y: 1.72 (+Y, between layers).
- Z (upright): 1.57 (+Y, across layers).
- tilt 20 to X: 1.67 (+Y, across layers).
- tilt 30 to X: 1.78 (+Y, between layers).
- tilt 45 to X: 1.84 (+Y, between layers).
- tilt 20 to Y: 1.71 (+Y, across layers).
- tilt 30 to Y: 1.78 (+Y, across layers).
- tilt 45 to Y: 1.81 (+Y, across layers).

**6. Branches taken.** None in the build. `c2_detail.py` ran once: the screw-head scallop line printed ok (14.66 mm3 against the expected 30, no stop);
the stem volume was 111697 mm3 (expected 112000, within 4 %); the mounting-face check passed ("one flat face at Y -4" ok, area 2355.9 mm2, Y -4.0000),
so the extra branch did not fire. One line from the build to note: `MOUNT_CLEAN: nothing below the mounting plane (good)` followed by a parenthetical
`MOUNT_CLEAN: no cut changed the volume the right way (open sketch? sketch off the body? wrong side?)`. The check it belongs to was ok, and no fixed item failed,
so I did not stop; I list it so the reviewer can look. The T3 verdict was `fail`, so nothing was changed or rerun.

**7. Times** (from `times.log`, clock -0600, 2026-11-14):

| Step | Between | Min |
| --- | --- | --- |
| T1 set-up | round 4 start 22:58:02, detail start 22:58:15 | 0.2 |
| T2 part, twist, pinch, print | detail start 22:58:15, checkpoint_02 22:59:21 | 1.3 |
| T3 study | study start 22:59:35, study end 23:10:24 | 10.8 |
| T4 finish | study end 23:10:24, C2 end 23:10:52 | 0.5 |

Total: 12.8 min (C2 start 22:58:02 to C2 end 23:10:52). `c2_detail.py` runs: one. `c2_fea.py` runs: one. No SolidWorks hold this round.

**8. Anything wrong in these instructions or the helpers.**
- The T2 "stem volume 112000 plus or minus 4 %" and the mass range 125 to 133 were met (111697 and 128.45).
- The screw-head scallop line reads "ok" at 14.66 against an expected 30 mm3; the T2 branch stops only on the line that is printed as a stop, so this went on.
- MOUNT_CLEAN prints a message that reads as a warning next to a passing check; the instructions do not say what to do about it.
- The T3 expected lowest factor (1.7 to 2.2) was met (1.78); the entry is "+Y, shear" at Z -24, which is above the -25 to -45 band.
