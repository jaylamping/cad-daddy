## C1. The link as it is

- Model `_wip/sw-eval/haiku-plan-c/link_boxy.SLDPRT`, one body, rebuild clean. Picture `pictures/c1_boxy.png`.
- Volume 219436.0 mm3 against 219436.0 mm3 by hand (disc 30787.6 - bore 5654.9 - holes
  435.8 + beam 165600 - the beam's top inside the disc rim 457.7 + block 17600
  + cheeks below the block 12600 - pin holes 603.2). Mass 261.1 g at 1.19 g/cm3.
- Box [-35.0, -22.0, -215.0, 35.0, 22.0, 35.0] against [-35.0, -22.0, -215.0, 35.0, 22.0, 35.0].
- Measured on the solid: six Ø3.4 holes at [[-25.0, 0.0, 0.0], [-12.5, 0.0, -21.651], [-12.5, 0.0, 21.651], [12.5, 0.0, -21.651], [12.5, 0.0, 21.651], [25.0, 0.0, 0.0]], bore at [0.0, 0.0, 0.0], pin holes at [[0.0, -19.0, -200.0], [0.0, 19.0, -200.0]],
  cheeks 6.0 thick at the pin.
- STL: watertight True, 1 shell, volume 219351.8 mm3, 1632 triangles.
- Shape numbers: {'triangles': 1632, 'area_mm2': 38261.4, 'flat_share': 0.91, 'largest_flat': 0.144, 'sharp_mm': 2406.4, 'sharp_per_area': 12.3, 'bbox_mm': [70.0, 44.0, 250.0]}.
- What I would question in the drawing: the beam's top face (Z -32) is 3 mm inside the disc rim, so beam and disc
  share 458 mm3; the cheeks are given from Z -170, where the block already is, so 10 mm of each is the
  block. Both are counted once. The beam (40 x 30 solid) carries 197 g of the 261 g.
- Clock: C1 ended at 0.5 min on times.log.

## C2. Make it more organic

### Stage 1, shape: two ideas, checkpoint 1 (stage ended 1.9 min after C2 start)

Restatement: `restate.md`, written before any modelling.

| Idea | Loft | Mass g | flat_share | largest_flat | sharp_mm | sharp_per_area | Hand factor, load Y | Hand factor, load X | Eligible |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | arcs4, stem first | 120.24 | 0.247 | 0.098 | 615.4 | 3.94 | 3.61 at Z -32.0 | 7.97 | True |
| B | did not build: build_form: nothing built the form in 5 tries; last error: stem volume against t | | | | | | 0.89 | 7.83 | False |

- A, "bone" (`pictures/idea_a.png`): one stem, wide and thin where it leaves the hub, near round in the middle, wide
  in Y at the fork; hub and wrist knuckle are bodies of revolution about the two joint axes.
- B, "open frame" (`pictures/idea_b.png`): a thin blade with a long window, two slim legs from the sides of the hub;
  the cable would cross the window in the open.
- Rule (written before the run): eligible = built as one body, lighter than the boxy link (261.13 g, C1 run),
  hand beam factor on yield at least 2.5 for a load along Y and along X; then the lower sharp_per_area, A on a tie.
- **Chosen: A** (only A is eligible; B: built False, hand factor load Y 0.89 at Z -60.0, load X 7.83 (2.5 needed), mass None g).
- Checkpoint 1: 0.6 min after C2 start, `pictures/checkpoint_01.png`.
  Still missing against the request: crude form only: no screw holes, screw-head clearances, pin holes or cable passage yet, nothing measured against the fixed items, no study; mass 120.24 g against 261.13 g boxy; sharp_per_area 3.94, flat_share 0.247.
- What I see in idea_a.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE
- What I see in idea_b.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE

## C2. Make it more organic

### Stage 1, shape: two ideas, checkpoint 1 (stage ended 3.9 min after C2 start)

Restatement: `restate.md`, written before any modelling.

| Idea | Loft | Mass g | flat_share | largest_flat | sharp_mm | sharp_per_area | Hand factor, load Y | Hand factor, load X | Eligible |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | arcs4, stem first | 120.24 | 0.247 | 0.098 | 615.4 | 3.94 | 3.61 at Z -32.0 | 7.97 | True |
| B | did not build: build_form: nothing built the form in 5 tries; last error: stem volume against t | | | | | | 0.89 | 7.83 | False |

- A, "bone" (`pictures/idea_a.png`): one stem, wide and thin where it leaves the hub, near round in the middle, wide
  in Y at the fork; hub and wrist knuckle are bodies of revolution about the two joint axes.
- B, "open frame" (`pictures/idea_b.png`): a thin blade with a long window, two slim legs from the sides of the hub;
  the cable would cross the window in the open.
- Rule (written before the run): eligible = built as one body, lighter than the boxy link (261.13 g, C1 run),
  hand beam factor on yield at least 2.5 for a load along Y and along X; then the lower sharp_per_area, A on a tie.
- **Chosen: A** (only A is eligible; B: built False, hand factor load Y 0.89 at Z -60.0, load X 7.83 (2.5 needed), mass None g).
- Checkpoint 1: 2.7 min after C2 start, `pictures/checkpoint_01.png`.
  Still missing against the request: crude form only: no screw holes, screw-head clearances, pin holes or cable passage yet, nothing measured against the fixed items, no study; mass 120.24 g against 261.13 g boxy; sharp_per_area 3.94, flat_share 0.247.
- What I see in idea_a.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE
- What I see in idea_b.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE

## C2. Make it more organic

### Stage 1, shape: two ideas, checkpoint 1 (stage ended 5.9 min after C2 start)

Restatement: `restate.md`, written before any modelling.

| Idea | Loft | Mass g | flat_share | largest_flat | sharp_mm | sharp_per_area | Hand factor, load Y | Hand factor, load X | Eligible |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | arcs4, stem first | 120.24 | 0.247 | 0.098 | 615.4 | 3.94 | 3.61 at Z -32.0 | 7.97 | True |
| B | did not build: build_form: nothing built the form in 5 tries; last error: stem volume against t | | | | | | 0.89 | 7.83 | False |

- A, "bone" (`pictures/idea_a.png`): one stem, wide and thin where it leaves the hub, near round in the middle, wide
  in Y at the fork; hub and wrist knuckle are bodies of revolution about the two joint axes.
- B, "open frame" (`pictures/idea_b.png`): a thin blade with a long window, two slim legs from the sides of the hub;
  the cable would cross the window in the open.
- Rule (written before the run): eligible = built as one body, lighter than the boxy link (261.13 g, C1 run),
  hand beam factor on yield at least 2.5 for a load along Y and along X; then the lower sharp_per_area, A on a tie.
- **Chosen: A** (only A is eligible; B: built False, hand factor load Y 0.89 at Z -60.0, load X 7.83 (2.5 needed), mass None g).
- Checkpoint 1: 4.7 min after C2 start, `pictures/checkpoint_01.png`.
  Still missing against the request: crude form only: no screw holes, screw-head clearances, pin holes or cable passage yet, nothing measured against the fixed items, no study; mass 120.24 g against 261.13 g boxy; sharp_per_area 3.94, flat_share 0.247.
- What I see in idea_a.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE
- What I see in idea_b.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE

## C2. Make it more organic

### Stage 1, shape: two ideas, checkpoint 1 (stage ended 8.1 min after C2 start)

Restatement: `restate.md`, written before any modelling.

| Idea | Loft | Mass g | flat_share | largest_flat | sharp_mm | sharp_per_area | Hand factor, load Y | Hand factor, load X | Eligible |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | arcs4, stem first | 120.24 | 0.247 | 0.098 | 615.4 | 3.94 | 3.61 at Z -32.0 | 7.97 | True |
| B | did not build: build_form: nothing built the form in 5 tries; last error: expected one body, go | | | | | | 0.89 | 7.83 | False |

- A, "bone" (`pictures/idea_a.png`): one stem, wide and thin where it leaves the hub, near round in the middle, wide
  in Y at the fork; hub and wrist knuckle are bodies of revolution about the two joint axes.
- B, "open frame" (`pictures/idea_b.png`): a thin blade with a long window, two slim legs from the sides of the hub;
  the cable would cross the window in the open.
- Rule (written before the run): eligible = built as one body, lighter than the boxy link (261.13 g, C1 run),
  hand beam factor on yield at least 2.5 for a load along Y and along X; then the lower sharp_per_area, A on a tie.
- **Chosen: A** (only A is eligible; B: built False, hand factor load Y 0.89 at Z -60.0, load X 7.83 (2.5 needed), mass None g).
- Checkpoint 1: 6.6 min after C2 start, `pictures/checkpoint_01.png`.
  Still missing against the request: crude form only: no screw holes, screw-head clearances, pin holes or cable passage yet, nothing measured against the fixed items, no study; mass 120.24 g against 261.13 g boxy; sharp_per_area 3.94, flat_share 0.247.
- What I see in idea_a.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE
- What I see in idea_b.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE

## C2. Make it more organic

### Stage 1, shape: two ideas, checkpoint 1 (stage ended 10.4 min after C2 start)

Restatement: `restate.md`, written before any modelling.

| Idea | Loft | Mass g | flat_share | largest_flat | sharp_mm | sharp_per_area | Hand factor, load Y | Hand factor, load X | Eligible |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | arcs4, stem first | 120.24 | 0.247 | 0.098 | 615.4 | 3.94 | 3.61 at Z -32.0 | 7.97 | True |
| B | did not build: build_form: nothing built the form in 5 tries; last error: expected one body, go | | | | | | 0.89 | 7.83 | False |

- A, "bone" (`pictures/idea_a.png`): one stem, wide and thin where it leaves the hub, near round in the middle, wide
  in Y at the fork; hub and wrist knuckle are bodies of revolution about the two joint axes.
- B, "open frame" (`pictures/idea_b.png`): a thin blade with a long window, two slim legs from the sides of the hub;
  the cable would cross the window in the open.
- Rule (written before the run): eligible = built as one body, lighter than the boxy link (261.13 g, C1 run),
  hand beam factor on yield at least 2.5 for a load along Y and along X; then the lower sharp_per_area, A on a tie.
- **Chosen: A** (only A is eligible; B: built False, hand factor load Y 0.89 at Z -60.0, load X 7.83 (2.5 needed), mass None g).
- Checkpoint 1: 8.9 min after C2 start, `pictures/checkpoint_01.png`.
  Still missing against the request: crude form only: no screw holes, screw-head clearances, pin holes or cable passage yet, nothing measured against the fixed items, no study; mass 120.24 g against 261.13 g boxy; sharp_per_area 3.94, flat_share 0.247.
- What I see in idea_a.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE
- What I see in idea_b.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE

### Stage 2, detail: link_organic built, fixed items measured (stage ended 11.5 min after C2 start)

- Table `STEM_A`, loft mode arcs4, order stem first; stem 98908.6 mm3, hub added
  21832.6, knuckle added 11745.6, slot removed 31445.5; hub seam blend:
  R3.0 mm on 2 edges.
- Cuts: pin holes 523.0 mm3, cable tunnel 4894.6, screw holes 436.0, screw-head
  clearances 10.06, below the mounting plane -0.0 (0 means nothing stood there).
- Volume 95179.6 mm3, mass **113.3 g** against 261.13 g boxy: lighter.
- One body, rebuild clean. STL watertight True, 1 shell, volume 94985.2 mm3, bounds
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

- Print: lying on its +Y side: the flat outer face of the +Y cheek (Y +22) on the bed, layers stacked along Y, the long axis (248 mm) along one bed axis of 256 mm; the mounting face Y -4 is a top surface. Supports: under the +Y side of the hub and of the stem (they stand 9 to 18 mm off the bed), and in the slot under the upper (-Y) cheek. No enclosed cavity: the cable tunnel is open at both ends; thinnest wall 0.8 mm (the tunnel
  under the hub's two faces, Z -15 to -22).
- Shape numbers: {'triangles': 18226, 'area_mm2': 27855.5, 'flat_share': 0.21, 'largest_flat': 0.084, 'sharp_mm': 834.2, 'sharp_per_area': 5.0, 'bbox_mm': [71.97, 44.0, 248.94]}.
- Checkpoint 2: 11.5 min after C2 start, `pictures/checkpoint_02.png`. Still missing against the request: the study (three load cases) and the before-and-after sheet; fixed items failing: none; hub seam blend R3.0; sharp_per_area 5.0, flat_share 0.21.
- What I see in checkpoint_02.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE

### Stage 3, study (stage ended 20.8 min after C2 start)

Model `_wip/sw-eval/haiku-plan-c/link_organic_fea.SLDPRT`, a copy of the exported part (volume checked). Printed PETG. Held:
the mounting face (the flat ring at Y -4, Ø30 to Ø63). Loads: 60 N; +X and -X as bearing loads on the two pin holes;
+Y as an even pressure on the inner face of the +Y cheek, because a force along the pin is not a bearing load on its
holes (`static()` refuses it): the part between the cheeks pushes on that face. Layers stacked along Y. Peaks are read
at least 3.0 mm from the held face and from the loaded faces. Global element sizes [4.0, 3.0, 2.3] mm, 1.2 mm on the
cable tunnel and 1.0 mm on the pin holes at every size.

| Case | el mm | Nodes | von Mises MPa | Across layers MPa | Between layers MPa | Max disp mm | Reaction N | von Mises peak at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| +X | 4.0 | 81132 | 17.804 | 3.456 | 2.308 | 4.755 | [-60.001, -0.002, 0.001] | [-8.53, 0.43, -73.86] |
| +X | 3.0 | 113248 | 17.883 | 3.453 | 2.493 | 4.761 | [-60.002, -0.0, 0.004] | [8.53, -0.04, -73.82] |
| +X | 2.3 | 170305 | 18.224 | 3.4 | 2.667 | 4.764 | [-60.001, 0.0, -0.0] | [-8.54, 0.18, -73.47] |
| -X | 4.0 | 81132 | 17.804 | 3.28 | 2.308 | 4.755 | [60.001, 0.002, -0.001] | [-8.53, 0.43, -73.86] |
| -X | 3.0 | 113322 | 17.857 | 3.246 | 2.506 | 4.761 | [60.002, -0.002, 0.003] | [-8.54, -0.01, -73.36] |
| -X | 2.3 | 170305 | 18.224 | 3.434 | 2.667 | 4.764 | [60.001, -0.0, 0.0] | [-8.54, 0.18, -73.47] |
| +Y | 4.0 | 81132 | 17.235 | 15.059 | 7.594 | 8.949 | [-0.0, -60.01, 0.002] | [0.28, -3.19, -34.48] |
| +Y | 3.0 | 113322 | 17.67 | 14.779 | 7.163 | 8.983 | [0.002, -59.992, -0.004] | [0.28, -3.19, -34.48] |
| +Y | 2.3 | 170305 | 18.404 | 14.59 | 7.059 | 8.983 | [0.004, -59.992, 0.0] | [0.28, -3.19, -34.48] |

Verdict from `swfea.judge()`, need 2.0: **fail**, lowest factor **1.54** at "+Y, layer", place [-3.2, -0.11, -32.08].

| Entry | Values coarse to fine MPa | Factor | Last step % | State |
| --- | --- | --- | --- | --- |
| +X, vm | [17.804, 17.883, 18.224] | 2.47 | 1.9 | pass |
| +X, layer | [3.456, 3.453, 3.4] | 6.62 | 1.5 | pass |
| +X, shear | [2.308, 2.493, 2.667] | 4.87 | 7.0 | pass |
| -X, vm | [17.804, 17.857, 18.224] | 2.47 | 2.1 | pass |
| -X, layer | [3.28, 3.246, 3.434] | 6.55 | 5.8 | pass |
| -X, shear | [2.308, 2.506, 2.667] | 4.87 | 6.4 | pass |
| +Y, vm | [17.235, 17.67, 18.404] | 2.45 | 4.2 | pass |
| +Y, layer | [15.059, 14.779, 14.59] | 1.54 | 1.3 | fail |
| +Y, shear | [7.594, 7.163, 7.059] | 1.84 | 1.5 | fail |

- Keys: sf_yield 2.39, sf_layer 1.51, sf_shear 1.81 (lowest of the three cases at
  2.3 mm, and for +Y the higher of the two ways to load it).
- Not converged: nothing: every entry settled.
- +Y loaded a second way at 3.0 mm (rigid, on both pin holes at the pin axis): rigid over pressure
  {'vm': 1.024, 'layer': 1.018, 'shear': 1.018} (von Mises, across layers, between layers).
- Hand check at the waist (Z -115), mean over 2 mm against M / Z: [('+X', {'hand_mpa': 4.72, 'mean_vm_2mm': 4.52, 'nodes': 21, 'at': (10.6, 0.0, -115.0)}), ('-X', {'hand_mpa': 4.72, 'mean_vm_2mm': 4.55, 'nodes': 20, 'at': (-10.6, 0.0, -115.0)}), ('+Y', {'hand_mpa': 4.24, 'mean_vm_2mm': 3.94, 'nodes': 24, 'at': (0.0, 11.8, -115.0)})].
- Reaction equals load in every study (table). -X against +X, von Mises: 0.00 % apart (the part is
  symmetric about X = 0, so they must agree).
- Excluded: the peak anywhere, including the held edge and the loaded faces, at 2.3 mm:
  [('+X', 18.224), ('-X', 18.224), ('+Y', 40.942)] MPa; on the loaded faces themselves
  [('+X', 2.297), ('-X', 2.305), ('+Y', 9.693)] MPa. Peak outside 2, 3 and 5 mm:
  [('+X', {'2.0': 18.224, '3.0': 18.224, '5.0': 18.224}), ('-X', {'2.0': 18.224, '3.0': 18.224, '5.0': 18.224}), ('+Y', {'2.0': 25.605, '3.0': 18.404, '5.0': 17.687})].
- At the governing peak, mean von Mises over 0.5, 1 and 2 mm (value, nodes): {'0.5': [18.4, 1], '1.0': [16.19, 11], '2.0': [15.48, 82]}.
- The same results read for the other print directions (2.3 mm), lowest factor of the three measures and three
  cases: {'X': 2.1, 'Y': 1.54, 'Z': 1.05}.

| Case | Layers along | von Mises | Across layers | Between layers |
| --- | --- | --- | --- | --- |
| +X | X | 18.224 | 2.208 | 3.78 |
| +X | Y | 18.224 | 3.4 | 2.667 |
| +X | Z | 18.224 | 19.882 | 3.912 |
| -X | X | 18.224 | 2.093 | 3.78 |
| -X | Y | 18.224 | 3.434 | 2.667 |
| -X | Z | 18.224 | 19.82 | 3.912 |
| +Y | X | 18.404 | 10.737 | 5.852 |
| +Y | Y | 18.404 | 14.59 | 7.059 |
| +Y | Z | 18.404 | 21.453 | 7.528 |

- Load path: the pin presses on the two pin holes (or, for +Y, the swinging part on the +Y cheek), the cheeks carry
  it up either side of the arch into the stem, the stem bends, and the neck hands it to the hub over the held ring.

### Stage 4, result (C2 took 21.2 min; the whole set 21.9 min on times.log)

| Gate | |
| --- | --- |
| Fixed items intact | True |
| One body, watertight | True |
| Factor at least 2.0 on all three measures, three cases | False (verdict from judge(): fail; 2.39 / 1.51 / 1.81) |
| Mass not above the boxy link | True (113.26 g against 261.13 g) |

Deliverables: `restate.md`, `pictures/idea_a.png`, `pictures/idea_b.png`, `pictures/checkpoint_01.png` to `_03.png`,
`pictures/c2_before_after.png` (both STLs in one call), `link_organic.SLDPRT` / `.step` / `.stl` in
`_wip/sw-eval/haiku-plan-c/`, `DESIGN.md`, `fea_rows.json`, `times.log`.

| Checkpoint | Min after C2 start | Picture | Still missing against the request |
| --- | --- | --- | --- |
| 1 | 8.9 | `pictures/checkpoint_01.png` | crude form only: no screw holes, screw-head clearances, pin holes or cable passage yet, nothing measured against the fixed items, no study; mass 120.24 g against 261.13 g boxy; sharp_per_area 3.94, flat_share 0.247 |
| 2 | 11.5 | `pictures/checkpoint_02.png` | the study (three load cases) and the before-and-after sheet; fixed items failing: none; hub seam blend R3.0; sharp_per_area 5.0, flat_share 0.21 |
| 3 | 21.2 | `pictures/checkpoint_03.png` | gate items not met: ['requirement_met']; verdict fail, lowest factor 1.54; against the look asked for: sharp_per_area 5.0 (boxy 12.3), flat_share 0.21 (boxy 0.91); the hub seam is blended R3.0 |

Shape numbers, before: {'triangles': 1632, 'area_mm2': 38261.4, 'flat_share': 0.91, 'largest_flat': 0.144, 'sharp_mm': 2406.4, 'sharp_per_area': 12.3, 'bbox_mm': [70.0, 44.0, 250.0]}. After: {'triangles': 18226, 'area_mm2': 27855.5, 'flat_share': 0.21, 'largest_flat': 0.084, 'sharp_mm': 834.2, 'sharp_per_area': 5.0, 'bbox_mm': [71.97, 44.0, 248.94]}.

- **Thinnest margin:** +Y, layer at [-3.2, -0.11, -32.08] (factor 1.54). At this factor the part carries 46.2 N at the wrist before the
  factor is 2.0; a sharper seam as printed, or the load taken on one cheek only, is what would eat it.
- **Cheapest improvement found:** the print direction is already the best of the three read
  ({'X': 2.1, 'Y': 1.54, 'Z': 1.05}); the fork end above the arch is solid and lightly stressed, so mass can come
  out there first.
- **Not checked:** buckling (the stem is stocky: about 22 mm across over 140 mm); the pin's own bending and a loose
  pin (a bearing load covers half the hole exactly); screw preload on the 8 mm hub; the 0.8 mm skins over the cable
  tunnel in print; whether the motor's body leaves room for the stem below Y -4 outside Ø62 (the boxy link went to
  Y -15 there too); fatigue.
- What I see in c2_before_after.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE

### Stage 2, detail: link_organic built, fixed items measured (stage ended 22.1 min after C2 start)

- Table `STEM_A2`, loft mode arcs4, order stem first; stem 101542.8 mm3, hub added
  21814.0, knuckle added 11747.8, slot removed 31447.6; hub seam blend:
  not built (tried R3, R2, R1.2 on 1 edges).
- Cuts: pin holes 523.0 mm3, cable tunnel 4894.6, screw holes 436.1, screw-head
  clearances 16.12, below the mounting plane 0.0 (0 means nothing stood there).
- Volume 97787.2 mm3, mass **116.4 g** against 261.13 g boxy: lighter.
- One body, rebuild clean. STL watertight True, 1 shell, volume 97581.6 mm3, bounds
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

- Print: lying on its +Y side: the flat outer face of the +Y cheek (Y +22) on the bed, layers stacked along Y, the long axis (248 mm) along one bed axis of 256 mm; the mounting face Y -4 is a top surface. Supports: under the +Y side of the hub and of the stem (they stand 9 to 18 mm off the bed), and in the slot under the upper (-Y) cheek. No enclosed cavity: the cable tunnel is open at both ends; thinnest wall 0.8 mm (the tunnel
  under the hub's two faces, Z -15 to -22).
- Shape numbers: {'triangles': 18542, 'area_mm2': 28096.8, 'flat_share': 0.209, 'largest_flat': 0.084, 'sharp_mm': 862.0, 'sharp_per_area': 5.14, 'bbox_mm': [71.97, 44.0, 248.94]}.
- Checkpoint 2: 22.1 min after C2 start, `pictures/checkpoint_02.png`. Still missing against the request: the study (three load cases) and the before-and-after sheet; fixed items failing: none; hub seam blend did not build: a crease is left where the stem leaves the hub; sharp_per_area 5.14, flat_share 0.209.
- What I see in checkpoint_02.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE

### Stage 3, study (stage ended 30.8 min after C2 start)

Model `_wip/sw-eval/haiku-plan-c/link_organic_fea.SLDPRT`, a copy of the exported part (volume checked). Printed PETG. Held:
the mounting face (the flat ring at Y -4, Ø30 to Ø63). Loads: 60 N; +X and -X as bearing loads on the two pin holes;
+Y as an even pressure on the inner face of the +Y cheek, because a force along the pin is not a bearing load on its
holes (`static()` refuses it): the part between the cheeks pushes on that face. Layers stacked along Y. Peaks are read
at least 3.0 mm from the held face and from the loaded faces. Global element sizes [4.0, 3.0, 2.3] mm, 1.2 mm on the
cable tunnel and 1.0 mm on the pin holes at every size.

| Case | el mm | Nodes | von Mises MPa | Across layers MPa | Between layers MPa | Max disp mm | Reaction N | von Mises peak at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| +X | 4.0 | 82002 | 16.503 | 3.067 | 2.217 | 4.486 | [-59.999, 0.003, -0.0] | [8.58, -0.61, -74.54] |
| +X | 3.0 | 116027 | 17.248 | 3.506 | 2.326 | 4.491 | [-59.996, 0.008, -0.001] | [8.59, -0.14, -73.72] |
| +X | 2.3 | 173186 | 17.431 | 3.251 | 2.497 | 4.495 | [-60.0, 0.003, -0.001] | [8.53, -1.08, -73.35] |
| -X | 4.0 | 82002 | 16.503 | 3.176 | 2.217 | 4.486 | [59.999, -0.003, 0.0] | [8.58, -0.61, -74.54] |
| -X | 3.0 | 116027 | 17.248 | 3.419 | 2.326 | 4.491 | [59.996, -0.008, 0.001] | [8.59, -0.14, -73.72] |
| -X | 2.3 | 173186 | 17.431 | 3.193 | 2.497 | 4.495 | [60.0, -0.003, 0.001] | [8.53, -1.08, -73.35] |
| +Y | 4.0 | 82002 | 16.284 | 14.068 | 7.643 | 7.971 | [-0.008, -60.002, -0.008] | [-0.16, 8.85, -73.32] |
| +Y | 3.0 | 116027 | 17.228 | 14.041 | 7.423 | 7.993 | [0.003, -60.016, -0.001] | [0.25, 8.82, -73.81] |
| +Y | 2.3 | 173186 | 17.229 | 14.209 | 7.531 | 8.012 | [0.0, -59.999, -0.004] | [0.07, -8.66, -73.47] |

Verdict from `swfea.judge()`, need 2.0: **fail**, lowest factor **1.58** at "+Y, layer", place [3.17, -0.41, -32.08].

| Entry | Values coarse to fine MPa | Factor | Last step % | State |
| --- | --- | --- | --- | --- |
| +X, vm | [16.503, 17.248, 17.431] | 2.58 | 1.1 | pass |
| +X, layer | [3.067, 3.506, 3.251] | 6.92 | 7.3 | pass |
| +X, shear | [2.217, 2.326, 2.497] | 5.21 | 7.4 | pass |
| -X, vm | [16.503, 17.248, 17.431] | 2.58 | 1.1 | pass |
| -X, layer | [3.176, 3.419, 3.193] | 7.05 | 6.6 | pass |
| -X, shear | [2.217, 2.326, 2.497] | 5.21 | 7.4 | pass |
| +Y, vm | [16.284, 17.228, 17.229] | 2.61 | 0.0 | pass |
| +Y, layer | [14.068, 14.041, 14.209] | 1.58 | 1.2 | fail |
| +Y, shear | [7.643, 7.423, 7.531] | 1.73 | 1.5 | fail |

- Keys: sf_yield 2.55, sf_layer 1.56, sf_shear 1.70 (lowest of the three cases at
  2.3 mm, and for +Y the higher of the two ways to load it).
- Not converged: nothing: every entry settled.
- +Y loaded a second way at 3.0 mm (rigid, on both pin holes at the pin axis): rigid over pressure
  {'vm': 1.024, 'layer': 1.018, 'shear': 1.018} (von Mises, across layers, between layers).
- Hand check at the waist (Z -115), mean over 2 mm against M / Z: [('+X', {'hand_mpa': 4.72, 'mean_vm_2mm': 4.5, 'nodes': 23, 'at': (10.6, 0.0, -115.0)}), ('-X', {'hand_mpa': 4.72, 'mean_vm_2mm': 4.53, 'nodes': 22, 'at': (-10.6, 0.0, -115.0)}), ('+Y', {'hand_mpa': 4.24, 'mean_vm_2mm': 3.98, 'nodes': 23, 'at': (0.0, 11.8, -115.0)})].
- Reaction equals load in every study (table). -X against +X, von Mises: 0.00 % apart (the part is
  symmetric about X = 0, so they must agree).
- Excluded: the peak anywhere, including the held edge and the loaded faces, at 2.3 mm:
  [('+X', 17.431), ('-X', 17.431), ('+Y', 38.046)] MPa; on the loaded faces themselves
  [('+X', 2.302), ('-X', 2.302), ('+Y', 9.695)] MPa. Peak outside 2, 3 and 5 mm:
  [('+X', {'2.0': 17.431, '3.0': 17.431, '5.0': 17.431}), ('-X', {'2.0': 17.431, '3.0': 17.431, '5.0': 17.431}), ('+Y', {'2.0': 21.799, '3.0': 17.229, '5.0': 17.229})].
- At the governing peak, mean von Mises over 0.5, 1 and 2 mm (value, nodes): {'0.5': [17.23, 1], '1.0': [14.75, 4], '2.0': [13.49, 26]}.
- The same results read for the other print directions (2.3 mm), lowest factor of the three measures and three
  cases: {'X': 2.38, 'Y': 1.58, 'Z': 1.2}.

| Case | Layers along | von Mises | Across layers | Between layers |
| --- | --- | --- | --- | --- |
| +X | X | 17.431 | 2.112 | 3.618 |
| +X | Y | 17.431 | 3.251 | 2.497 |
| +X | Z | 17.431 | 18.721 | 3.704 |
| -X | X | 17.431 | 2.246 | 3.618 |
| -X | Y | 17.431 | 3.193 | 2.497 |
| -X | Z | 17.431 | 18.768 | 3.704 |
| +Y | X | 17.229 | 9.171 | 5.465 |
| +Y | Y | 17.229 | 14.209 | 7.531 |
| +Y | Z | 17.229 | 18.765 | 7.745 |

- Load path: the pin presses on the two pin holes (or, for +Y, the swinging part on the +Y cheek), the cheeks carry
  it up either side of the arch into the stem, the stem bends, and the neck hands it to the hub over the held ring.

### Stage 4, result (C2 took 30.8 min; the whole set 31.5 min on times.log)

| Gate | |
| --- | --- |
| Fixed items intact | True |
| One body, watertight | True |
| Factor at least 2.0 on all three measures, three cases | False (verdict from judge(): fail; 2.55 / 1.56 / 1.7) |
| Mass not above the boxy link | True (116.37 g against 261.13 g) |

Deliverables: `restate.md`, `pictures/idea_a.png`, `pictures/idea_b.png`, `pictures/checkpoint_01.png` to `_03.png`,
`pictures/c2_before_after.png` (both STLs in one call), `link_organic.SLDPRT` / `.step` / `.stl` in
`_wip/sw-eval/haiku-plan-c/`, `DESIGN.md`, `fea_rows.json`, `times.log`.

| Checkpoint | Min after C2 start | Picture | Still missing against the request |
| --- | --- | --- | --- |
| 1 | 8.9 | `pictures/checkpoint_01.png` | crude form only: no screw holes, screw-head clearances, pin holes or cable passage yet, nothing measured against the fixed items, no study; mass 120.24 g against 261.13 g boxy; sharp_per_area 3.94, flat_share 0.247 |
| 2 | 22.1 | `pictures/checkpoint_02.png` | the study (three load cases) and the before-and-after sheet; fixed items failing: none; hub seam blend did not build: a crease is left where the stem leaves the hub; sharp_per_area 5.14, flat_share 0.209 |
| 3 | 30.8 | `pictures/checkpoint_03.png` | gate items not met: ['requirement_met']; verdict fail, lowest factor 1.58; against the look asked for: sharp_per_area 5.14 (boxy 12.3), flat_share 0.209 (boxy 0.91); the hub seam is still a crease |

Shape numbers, before: {'triangles': 1632, 'area_mm2': 38261.4, 'flat_share': 0.91, 'largest_flat': 0.144, 'sharp_mm': 2406.4, 'sharp_per_area': 12.3, 'bbox_mm': [70.0, 44.0, 250.0]}. After: {'triangles': 18542, 'area_mm2': 28096.8, 'flat_share': 0.209, 'largest_flat': 0.084, 'sharp_mm': 862.0, 'sharp_per_area': 5.14, 'bbox_mm': [71.97, 44.0, 248.94]}.

- **Thinnest margin:** +Y, layer at [3.17, -0.41, -32.08] (factor 1.58). At this factor the part carries 47.4 N at the wrist before the
  factor is 2.0; a sharper seam as printed, or the load taken on one cheek only, is what would eat it.
- **Cheapest improvement found:** the print direction is already the best of the three read
  ({'X': 2.38, 'Y': 1.58, 'Z': 1.2}); the fork end above the arch is solid and lightly stressed, so mass can come
  out there first.
- **Not checked:** buckling (the stem is stocky: about 22 mm across over 140 mm); the pin's own bending and a loose
  pin (a bearing load covers half the hole exactly); screw preload on the 8 mm hub; the 0.8 mm skins over the cable
  tunnel in print; whether the motor's body leaves room for the stem below Y -4 outside Ø62 (the boxy link went to
  Y -15 there too); fatigue.
- What I see in c2_before_after.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE

