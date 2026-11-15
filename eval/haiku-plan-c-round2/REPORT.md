### Stage 2, detail: link_organic built, fixed items measured (stage ended 0.9 min after C2 start)

- Table `STEM_A2`, loft mode arcs4, order stem first; stem 103679.2 mm3, hub added
  21817.9, knuckle added 11744.5, slot removed 31451.8; hub seam blend:
  not built (tried R3, R2, R1.2 on 1 edges).
- Cuts: pin holes 523.0 mm3, cable tunnel 4894.6, screw holes 436.2, screw-head
  clearances 16.06, below the mounting plane 0.0 (0 means nothing stood there).
- Volume 99920.0 mm3, mass **118.9 g** against 261.13 g boxy: lighter.
- One body, rebuild clean. STL watertight True, 1 shell, volume 99747.2 mm3, bounds
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
- Shape numbers: {'triangles': 12540, 'area_mm2': 28222.6, 'flat_share': 0.208, 'largest_flat': 0.083, 'sharp_mm': 859.9, 'sharp_per_area': 5.12, 'bbox_mm': [71.97, 44.0, 248.94]}.
- Checkpoint 2: 0.9 min after C2 start, `pictures/checkpoint_02.png`. Still missing against the request: the study (three load cases) and the before-and-after sheet; fixed items failing: none; hub seam blend did not build: a crease is left where the stem leaves the hub; sharp_per_area 5.12, flat_share 0.208.
- What I see in checkpoint_02.png, one line: the bone with a straight, even stem down to the fork; the waist that was pinched near Z -74 is gone in the side views, and six screw holes and two pin holes show.

### Stage 2, detail: link_organic built, fixed items measured (stage ended 2.0 min after C2 start)

- Table `STEM_A2`, loft mode arcs4, order stem first; stem 103679.3 mm3, hub added
  21817.9, knuckle added 11744.5, slot removed 31451.8; hub seam blend:
  not built (tried R3, R2, R1.2 on 1 edges).
- Cuts: pin holes 523.0 mm3, cable tunnel 4894.6, screw holes 436.2, screw-head
  clearances 16.06, below the mounting plane 0.0 (0 means nothing stood there).
- Volume 99920.0 mm3, mass **118.9 g** against 261.13 g boxy: lighter.
- One body, rebuild clean. STL watertight True, 1 shell, volume 99746.0 mm3, bounds
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
- Shape numbers: {'triangles': 12540, 'area_mm2': 28222.5, 'flat_share': 0.208, 'largest_flat': 0.083, 'sharp_mm': 859.9, 'sharp_per_area': 5.12, 'bbox_mm': [71.97, 44.0, 248.94]}.
- Checkpoint 2: 2.0 min after C2 start, `pictures/checkpoint_02.png`. Still missing against the request: the study (three load cases) and the before-and-after sheet; fixed items failing: none; hub seam blend did not build: a crease is left where the stem leaves the hub; sharp_per_area 5.12, flat_share 0.208.
- What I see in checkpoint_02.png, one line: the bone with a straight, even stem down to the fork; the waist that was pinched near Z -74 is gone in the side views, and six screw holes and two pin holes show.

### Stage 3, study (stage ended 11.3 min after C2 start)

Model `_wip/sw-eval/haiku-plan-c-round2/link_organic_fea.SLDPRT`, a copy of the exported part (volume checked). Printed PETG. Held:
the mounting face (the flat ring at Y -4, Ø30 to Ø63). Loads: 60 N; +X and -X as bearing loads on the two pin holes;
+Y as an even pressure on the inner face of the +Y cheek, because a force along the pin is not a bearing load on its
holes (`static()` refuses it): the part between the cheeks pushes on that face. Layers as printed tilted 30 degrees towards +X, hub end down. Peaks are read
at least 3.0 mm from the held face and from the loaded faces. Global element sizes [4.0, 3.0, 2.3] mm, 1.2 mm on the
cable tunnel and 1.0 mm on the pin holes at every size.

| Case | el mm | Nodes | von Mises MPa | Across layers MPa | Between layers MPa | Max disp mm | Reaction N | von Mises peak at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| +X | 4.0 | 83226 | 6.249 | 7.118 | 2.883 | 3.395 | [-60.001, 0.009, -0.003] | [-15.57, -2.59, -32.98] |
| +X | 3.0 | 118596 | 6.602 | 6.92 | 3.107 | 3.397 | [-60.002, 0.002, -0.0] | [14.23, -2.94, -32.97] |
| +X | 2.3 | 177406 | 7.228 | 7.927 | 3.33 | 3.399 | [-59.999, -0.004, -0.002] | [12.98, -2.94, -31.86] |
| -X | 4.0 | 83226 | 6.249 | 4.47 | 2.883 | 3.395 | [60.001, -0.009, 0.003] | [-15.57, -2.59, -32.98] |
| -X | 3.0 | 118596 | 6.602 | 5.281 | 3.107 | 3.397 | [60.002, -0.002, 0.0] | [14.23, -2.94, -32.97] |
| -X | 2.3 | 177406 | 7.228 | 6.26 | 3.33 | 3.399 | [59.999, 0.004, 0.002] | [12.98, -2.94, -31.86] |
| +Y | 4.0 | 83226 | 14.778 | 15.313 | 7.137 | 6.922 | [0.0, -60.015, 0.002] | [0.28, -3.19, -34.48] |
| +Y | 3.0 | 118596 | 15.469 | 16.312 | 7.252 | 6.951 | [-0.001, -59.995, -0.003] | [0.28, -3.19, -34.48] |
| +Y | 2.3 | 177457 | 15.91 | 16.357 | 7.387 | 6.96 | [-0.004, -60.015, 0.001] | [0.28, -3.19, -34.48] |

Verdict from `swfea.judge()`, need 2.0: **fail**, lowest factor **1.38** at "+Y, layer", place [0.28, -3.19, -34.48].

| Entry | Values coarse to fine MPa | Factor | Last step % | State |
| --- | --- | --- | --- | --- |
| +X, vm | [6.249, 6.602, 7.228] | 6.23 | 9.5 | pass |
| +X, layer | [7.118, 6.92, 7.927] | 2.84 | 14.6 | not shown |
| +X, shear | [2.883, 3.107, 3.33] | 3.9 | 7.2 | pass |
| -X, vm | [6.249, 6.602, 7.228] | 6.23 | 9.5 | pass |
| -X, layer | [4.47, 5.281, 6.26] | 3.59 | 18.5 | not shown |
| -X, shear | [2.883, 3.107, 3.33] | 3.9 | 7.2 | pass |
| +Y, vm | [14.778, 15.469, 15.91] | 2.83 | 2.9 | pass |
| +Y, layer | [15.313, 16.312, 16.357] | 1.38 | 0.3 | fail |
| +Y, shear | [7.137, 7.252, 7.387] | 1.76 | 1.9 | fail |

- Keys: sf_yield 2.78, sf_layer 1.35, sf_shear 1.73 (lowest of the three cases at
  2.3 mm, and for +Y the higher of the two ways to load it).
- Not converged: [{'entry': '+X, layer', 'values': [7.118, 6.92, 7.927], 'last_step_pct': 14.6, 'state': 'not shown'}, {'entry': '-X, layer', 'values': [4.47, 5.281, 6.26], 'last_step_pct': 18.5, 'state': 'not shown'}].
- +Y loaded a second way at 3.0 mm (rigid, on both pin holes at the pin axis): rigid over pressure
  {'vm': 1.018, 'layer': 1.018, 'shear': 1.018} (von Mises, across layers, between layers).
- Hand check at the waist (Z -115), mean over 2 mm against M / Z: [('+X', {'hand_mpa': 4.72, 'mean_vm_2mm': 4.43, 'nodes': 24, 'at': (10.6, 0.0, -115.0)}), ('-X', {'hand_mpa': 4.72, 'mean_vm_2mm': 4.41, 'nodes': 24, 'at': (-10.6, 0.0, -115.0)}), ('+Y', {'hand_mpa': 4.24, 'mean_vm_2mm': 3.93, 'nodes': 23, 'at': (0.0, 11.8, -115.0)})].
- Reaction equals load in every study (table). -X against +X, von Mises: 0.00 % apart (the part is
  symmetric about X = 0, so they must agree).
- Excluded: the peak anywhere, including the held edge and the loaded faces, at 2.3 mm:
  [('+X', 8.107), ('-X', 8.107), ('+Y', 37.604)] MPa; on the loaded faces themselves
  [('+X', 2.309), ('-X', 2.317), ('+Y', 9.759)] MPa. Peak outside 2, 3 and 5 mm:
  [('+X', {'2.0': 7.228, '3.0': 7.228, '5.0': 5.937}), ('-X', {'2.0': 7.228, '3.0': 7.228, '5.0': 5.937}), ('+Y', {'2.0': 21.587, '3.0': 15.91, '5.0': 15.087})].
- At the governing peak, mean von Mises over 0.5, 1 and 2 mm (value, nodes): {'0.5': [15.91, 1], '1.0': [13.57, 11], '2.0': [12.82, 79]}.
- The same results read for the other print directions (2.3 mm), lowest factor of the three measures and three
  cases: {'X': 2.3, 'Y': 1.6, 'Z (upright)': 1.21, 'tilt 20 to X': 1.28, 'tilt 30 to X': 1.38, 'tilt 45 to X': 1.6, 'tilt 20 to Y': 1.37, 'tilt 30 to Y': 1.52, 'tilt 45 to Y': 1.42}.

| Case | Layers along | von Mises | Across layers | Between layers |
| --- | --- | --- | --- | --- |
| +X | X | 7.228 | 2.244 | 2.106 |
| +X | Y | 7.228 | 1.443 | 1.899 |
| +X | Z (upright) | 7.228 | 8.419 | 2.074 |
| +X | tilt 20 to X | 7.228 | 8.478 | 2.972 |
| +X | tilt 30 to X | 7.228 | 7.927 | 3.33 |
| +X | tilt 45 to X | 7.228 | 6.547 | 3.367 |
| +X | tilt 20 to Y | 7.228 | 7.946 | 3.446 |
| +X | tilt 30 to Y | 7.228 | 7.126 | 3.755 |
| +X | tilt 45 to Y | 7.228 | 5.427 | 3.729 |
| -X | X | 7.228 | 2.419 | 2.106 |
| -X | Y | 7.228 | 1.407 | 1.899 |
| -X | Z (upright) | 7.228 | 8.752 | 2.074 |
| -X | tilt 20 to X | 7.228 | 7.337 | 2.972 |
| -X | tilt 30 to X | 7.228 | 6.26 | 3.33 |
| -X | tilt 45 to X | 7.228 | 4.537 | 3.367 |
| -X | tilt 20 to Y | 7.228 | 8.324 | 3.446 |
| -X | tilt 30 to Y | 7.228 | 7.496 | 3.755 |
| -X | tilt 45 to Y | 7.228 | 5.75 | 3.729 |
| +Y | X | 15.91 | 9.233 | 5.663 |
| +Y | Y | 15.91 | 14.09 | 7.632 |
| +Y | Z (upright) | 15.91 | 18.559 | 7.734 |
| +Y | tilt 20 to X | 15.91 | 17.564 | 7.606 |
| +Y | tilt 30 to X | 15.91 | 16.357 | 7.387 |
| +Y | tilt 45 to X | 15.91 | 14.045 | 7.577 |
| +Y | tilt 20 to Y | 15.91 | 16.427 | 7.282 |
| +Y | tilt 30 to Y | 15.91 | 14.756 | 7.939 |
| +Y | tilt 45 to Y | 15.91 | 13.686 | 9.18 |

- Load path: the pin presses on the two pin holes (or, for +Y, the swinging part on the +Y cheek), the cheeks carry
  it up either side of the arch into the stem, the stem bends, and the neck hands it to the hub over the held ring.

- The three measures for the tilted print at the finest mesh, read outside 2, 3 and 5 mm from the held and loaded faces (the verdict uses 3.0 mm): [('+X', {'2.0': {'vm': 7.228, 'layer': 7.927, 'shear': 3.33}, '3.0': {'vm': 7.228, 'layer': 7.927, 'shear': 3.33}, '5.0': {'vm': 5.937, 'layer': 6.23, 'shear': 2.807}}), ('-X', {'2.0': {'vm': 7.228, 'layer': 6.566, 'shear': 3.33}, '3.0': {'vm': 7.228, 'layer': 6.26, 'shear': 3.33}, '5.0': {'vm': 5.937, 'layer': 4.927, 'shear': 2.807}}), ('+Y', {'2.0': {'vm': 21.587, 'layer': 21.492, 'shear': 7.607}, '3.0': {'vm': 15.91, 'layer': 16.357, 'shear': 7.387}, '5.0': {'vm': 15.087, 'layer': 9.615, 'shear': 7.387}})]

### Stage 2, detail: link_organic built, fixed items measured (stage ended 12.4 min after C2 start)

- Table `STEM_A3`, loft mode arcs4, order stem first; stem 108427.5 mm3, hub added
  21800.4, knuckle added 11743.5, slot removed 31448.9; hub seam blend:
  not built (tried R3, R2, R1.2 on 1 edges).
- Cuts: pin holes 523.0 mm3, cable tunnel 4894.6, screw holes 436.0, screw-head
  clearances 19.49, below the mounting plane -0.0 (0 means nothing stood there).
- Volume 104649.3 mm3, mass **124.5 g** against 261.13 g boxy: lighter.
- One body, rebuild clean. STL watertight True, 1 shell, volume 104474.5 mm3, bounds
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
- Shape numbers: {'triangles': 13020, 'area_mm2': 28643.3, 'flat_share': 0.205, 'largest_flat': 0.082, 'sharp_mm': 863.5, 'sharp_per_area': 5.1, 'bbox_mm': [71.97, 44.0, 248.94]}.
- Checkpoint 2: 12.4 min after C2 start, `pictures/checkpoint_02.png`. Still missing against the request: the study (three load cases) and the before-and-after sheet; fixed items failing: none; hub seam blend did not build: a crease is left where the stem leaves the hub; sharp_per_area 5.1, flat_share 0.205.
- What I see in checkpoint_02.png, one line: the bone with a straight stem to the fork, six screw holes and two pin holes; no waist in the side views.

### Stage 3, study (stage ended 21.7 min after C2 start)

Model `_wip/sw-eval/haiku-plan-c-round2/link_organic_fea.SLDPRT`, a copy of the exported part (volume checked). Printed PETG. Held:
the mounting face (the flat ring at Y -4, Ø30 to Ø63). Loads: 60 N; +X and -X as bearing loads on the two pin holes;
+Y as an even pressure on the inner face of the +Y cheek, because a force along the pin is not a bearing load on its
holes (`static()` refuses it): the part between the cheeks pushes on that face. Layers as printed tilted 30 degrees towards +X, hub end down. Peaks are read
at least 3.0 mm from the held face and from the loaded faces. Global element sizes [4.0, 3.0, 2.3] mm, 1.2 mm on the
cable tunnel and 1.0 mm on the pin holes at every size.

| Case | el mm | Nodes | von Mises MPa | Across layers MPa | Between layers MPa | Max disp mm | Reaction N | von Mises peak at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| +X | 4.0 | 85867 | 5.622 | 5.638 | 2.612 | 2.931 | [-59.999, -0.004, -0.001] | [14.91, -3.04, -32.96] |
| +X | 3.0 | 122239 | 6.07 | 5.856 | 2.732 | 2.932 | [-60.0, -0.004, -0.002] | [-14.95, -2.95, -32.67] |
| +X | 2.3 | 183663 | 6.546 | 6.368 | 2.883 | 2.934 | [-60.001, -0.003, -0.002] | [-13.82, -3.1, -32.55] |
| -X | 4.0 | 85867 | 5.622 | 4.513 | 2.612 | 2.931 | [59.999, 0.004, 0.001] | [14.91, -3.04, -32.96] |
| -X | 3.0 | 122239 | 6.07 | 4.895 | 2.732 | 2.932 | [60.0, 0.004, 0.002] | [-14.95, -2.95, -32.67] |
| -X | 2.3 | 183663 | 6.546 | 5.511 | 2.883 | 2.934 | [60.001, 0.003, 0.002] | [-13.82, -3.1, -32.55] |
| +Y | 4.0 | 85867 | 14.94 | 13.551 | 7.389 | 6.223 | [0.003, -59.997, -0.001] | [-9.4, 4.66, -23.48] |
| +Y | 3.0 | 122239 | 15.01 | 14.654 | 7.326 | 6.228 | [0.004, -60.007, -0.004] | [9.4, 4.66, -23.48] |
| +Y | 2.3 | 183663 | 14.838 | 14.369 | 7.17 | 6.249 | [0.002, -60.006, -0.001] | [9.41, 4.69, -23.5] |

Verdict from `swfea.judge()`, need 2.0: **fail**, lowest factor **1.57** at "+Y, layer", place [0.28, -3.19, -34.48].

| Entry | Values coarse to fine MPa | Factor | Last step % | State |
| --- | --- | --- | --- | --- |
| +X, vm | [5.622, 6.07, 6.546] | 6.87 | 7.8 | pass |
| +X, layer | [5.638, 5.856, 6.368] | 3.53 | 8.7 | pass |
| +X, shear | [2.612, 2.732, 2.883] | 4.51 | 5.5 | pass |
| -X, vm | [5.622, 6.07, 6.546] | 6.87 | 7.8 | pass |
| -X, layer | [4.513, 4.895, 5.511] | 4.08 | 12.6 | not shown |
| -X, shear | [2.612, 2.732, 2.883] | 4.51 | 5.5 | pass |
| +Y, vm | [14.94, 15.01, 14.838] | 3.03 | 1.1 | pass |
| +Y, layer | [13.551, 14.654, 14.369] | 1.57 | 1.9 | fail |
| +Y, shear | [7.389, 7.326, 7.17] | 1.81 | 2.1 | fail |

- Keys: sf_yield 2.98, sf_layer 1.54, sf_shear 1.78 (lowest of the three cases at
  2.3 mm, and for +Y the higher of the two ways to load it).
- Not converged: [{'entry': '-X, layer', 'values': [4.513, 4.895, 5.511], 'last_step_pct': 12.6, 'state': 'not shown'}].
- +Y loaded a second way at 3.0 mm (rigid, on both pin holes at the pin axis): rigid over pressure
  {'vm': 1.018, 'layer': 1.018, 'shear': 1.018} (von Mises, across layers, between layers).
- Hand check at the waist (Z -115), mean over 2 mm against M / Z: [('+X', {'hand_mpa': 4.47, 'mean_vm_2mm': 4.23, 'nodes': 21, 'at': (10.8, 0.0, -115.0)}), ('-X', {'hand_mpa': 4.47, 'mean_vm_2mm': 4.19, 'nodes': 23, 'at': (-10.8, 0.0, -115.0)}), ('+Y', {'hand_mpa': 4.03, 'mean_vm_2mm': 3.78, 'nodes': 21, 'at': (0.0, 12.0, -115.0)})].
- Reaction equals load in every study (table). -X against +X, von Mises: 0.00 % apart (the part is
  symmetric about X = 0, so they must agree).
- Excluded: the peak anywhere, including the held edge and the loaded faces, at 2.3 mm:
  [('+X', 7.678), ('-X', 7.678), ('+Y', 36.001)] MPa; on the loaded faces themselves
  [('+X', 2.282), ('-X', 2.308), ('+Y', 9.774)] MPa. Peak outside 2, 3 and 5 mm:
  [('+X', {'2.0': 6.546, '3.0': 6.546, '5.0': 5.631}), ('-X', {'2.0': 6.546, '3.0': 6.546, '5.0': 5.631}), ('+Y', {'2.0': 19.128, '3.0': 14.838, '5.0': 14.838})].
- At the governing peak, mean von Mises over 0.5, 1 and 2 mm (value, nodes): {'0.5': [14.84, 1], '1.0': [11.98, 5], '2.0': [9.32, 36]}.
- The same results read for the other print directions (2.3 mm), lowest factor of the three measures and three
  cases: {'X': 2.65, 'Y': 1.67, 'Z (upright)': 1.39, 'tilt 20 to X': 1.46, 'tilt 30 to X': 1.57, 'tilt 45 to X': 1.81, 'tilt 20 to Y': 1.45, 'tilt 30 to Y': 1.6, 'tilt 45 to Y': 1.63}.

| Case | Layers along | von Mises | Across layers | Between layers |
| --- | --- | --- | --- | --- |
| +X | X | 6.546 | 1.787 | 1.832 |
| +X | Y | 6.546 | 1.402 | 1.864 |
| +X | Z (upright) | 6.546 | 7.226 | 1.864 |
| +X | tilt 20 to X | 6.546 | 6.986 | 2.623 |
| +X | tilt 30 to X | 6.546 | 6.368 | 2.883 |
| +X | tilt 45 to X | 6.546 | 5.236 | 3.043 |
| +X | tilt 20 to Y | 6.546 | 6.291 | 3.124 |
| +X | tilt 30 to Y | 6.546 | 5.719 | 3.455 |
| +X | tilt 45 to Y | 6.546 | 4.642 | 3.28 |
| -X | X | 6.546 | 1.968 | 1.832 |
| -X | Y | 6.546 | 1.339 | 1.864 |
| -X | Z (upright) | 6.546 | 7.591 | 1.864 |
| -X | tilt 20 to X | 6.546 | 6.433 | 2.623 |
| -X | tilt 30 to X | 6.546 | 5.511 | 2.883 |
| -X | tilt 45 to X | 6.546 | 4.001 | 3.043 |
| -X | tilt 20 to Y | 6.546 | 7.096 | 3.124 |
| -X | tilt 30 to Y | 6.546 | 6.345 | 3.455 |
| -X | tilt 45 to Y | 6.546 | 4.829 | 3.28 |
| +Y | X | 14.838 | 8.127 | 4.913 |
| +Y | Y | 14.838 | 13.482 | 7.608 |
| +Y | Z (upright) | 14.838 | 16.133 | 7.78 |
| +Y | tilt 20 to X | 14.838 | 15.367 | 7.601 |
| +Y | tilt 30 to X | 14.838 | 14.369 | 7.17 |
| +Y | tilt 45 to X | 14.838 | 12.411 | 6.971 |
| +Y | tilt 20 to Y | 14.838 | 15.479 | 6.423 |
| +Y | tilt 30 to Y | 14.838 | 14.041 | 6.963 |
| +Y | tilt 45 to Y | 14.838 | 12.767 | 7.999 |

- Load path: the pin presses on the two pin holes (or, for +Y, the swinging part on the +Y cheek), the cheeks carry
  it up either side of the arch into the stem, the stem bends, and the neck hands it to the hub over the held ring.

- The three measures for the tilted print at the finest mesh, read outside 2, 3 and 5 mm from the held and loaded faces (the verdict uses 3.0 mm): [('+X', {'2.0': {'vm': 6.546, 'layer': 6.716, 'shear': 2.883}, '3.0': {'vm': 6.546, 'layer': 6.368, 'shear': 2.883}, '5.0': {'vm': 5.631, 'layer': 5.659, 'shear': 2.693}}), ('-X', {'2.0': {'vm': 6.546, 'layer': 5.736, 'shear': 2.883}, '3.0': {'vm': 6.546, 'layer': 5.511, 'shear': 2.883}, '5.0': {'vm': 5.631, 'layer': 4.386, 'shear': 2.693}}), ('+Y', {'2.0': {'vm': 19.128, 'layer': 20.561, 'shear': 7.17}, '3.0': {'vm': 14.838, 'layer': 14.369, 'shear': 7.17}, '5.0': {'vm': 14.838, 'layer': 9.573, 'shear': 7.17}})]

### Stage 4, result (C2 took 22.2 min; the whole set 22.2 min on times.log)

| Gate | |
| --- | --- |
| Fixed items intact | True |
| One body, watertight | True |
| Factor at least 2.0 on all three measures, three cases | False (verdict from judge(): fail; 2.98 / 1.54 / 1.78) |
| Mass not above the boxy link | True (124.53 g against 261.13 g) |

Deliverables: `restate.md`, `pictures/idea_a.png`, `pictures/idea_b.png`, `pictures/checkpoint_01.png` to `_03.png`,
`pictures/c2_before_after.png` (both STLs in one call), `link_organic.SLDPRT` / `.step` / `.stl` in
`_wip/sw-eval/haiku-plan-c-round2/`, `DESIGN.md`, `fea_rows.json`, `times.log`.

| Checkpoint | Min after C2 start | Picture | Still missing against the request |
| --- | --- | --- | --- |
| 2 | 12.4 | `pictures/checkpoint_02.png` | the study (three load cases) and the before-and-after sheet; fixed items failing: none; hub seam blend did not build: a crease is left where the stem leaves the hub; sharp_per_area 5.1, flat_share 0.205 |
| 3 | 22.2 | `pictures/checkpoint_03.png` | gate items not met: ['requirement_met']; verdict fail, lowest factor 1.57; against the look asked for: sharp_per_area 5.1 (boxy 12.3), flat_share 0.205 (boxy 0.91); the hub seam is still a crease |

Shape numbers, before: {'triangles': 1632, 'area_mm2': 38261.4, 'flat_share': 0.91, 'largest_flat': 0.144, 'sharp_mm': 2406.4, 'sharp_per_area': 12.3, 'bbox_mm': [70.0, 44.0, 250.0]}. After: {'triangles': 13020, 'area_mm2': 28643.3, 'flat_share': 0.205, 'largest_flat': 0.082, 'sharp_mm': 863.5, 'sharp_per_area': 5.1, 'bbox_mm': [71.97, 44.0, 248.94]}.

- **Thinnest margin:** +Y, layer at [0.28, -3.19, -34.48] (factor 1.57). At this factor the part carries 47.1 N at the wrist before the
  factor is 2.0; a sharper seam as printed, or the load taken on one cheek only, is what would eat it.
- **Cheapest improvement found:** the stem loft was untwisted and the print direction changed to a 30 degree tilt, hub end down; all directions read
  ({'X': 2.65, 'Y': 1.67, 'Z (upright)': 1.39, 'tilt 20 to X': 1.46, 'tilt 30 to X': 1.57, 'tilt 45 to X': 1.81, 'tilt 20 to Y': 1.45, 'tilt 30 to Y': 1.6, 'tilt 45 to Y': 1.63}); the fork end above the arch is solid and lightly stressed, so mass can come
  out there first.
- **Not checked:** buckling (the stem is stocky: about 22 mm across over 140 mm); the pin's own bending and a loose
  pin (a bearing load covers half the hole exactly); screw preload on the 8 mm hub; the 0.8 mm skins over the cable
  tunnel in print; whether the motor's body leaves room for the stem below Y -4 outside Ø62 (the boxy link went to
  Y -15 there too); fatigue.
- What I see in c2_before_after.png, one line: top row the boxy block link, bottom row the organic bone with a smooth, even stem to the fork and no waist in the side views.


## C2 round 2, S6 report

**1. State: C2 not done: requirement not met.** Gate from `c2_finish.py`: fixed_items_ok true, one_body_watertight true,
requirement_met **false**, mass_not_above_boxy true (124.53 g against 261.13 g). Verdict `fail`, lowest factor 1.57 at
"+Y, layer", place [0.28, -3.19, -34.48] (the neck). Both verdicts of this round were `fail`, see the branches.

**2. Table, follow-up round against this round.**

| | Follow-up round | This round (final table STEM_A3) |
| --- | --- | --- |
| Table name | STEM_A2 | STEM_A3 |
| Mass, g | 117.85 | 124.53 |
| Verdict | not shown | fail |
| Lowest factor | 2.06 | 1.57 |
| Lowest entry and place | "+X, vm" at Z -78.7 (neck area, outside the expected place) | "+Y, layer" at [0.28, -3.19, -34.48], the neck |
| Print direction | on its -X edge (layers along X) | tilted 30 degrees towards +X, hub end down (layers at 30 degrees) |
| Largest twist, degrees | about 90 (Z -72 to -85) | 16.7 (Z -72 to -85), under 20: TWIST_CHECK ok |
| Half width at Z -78, mm | 8.65 | 12.17 |
| von Mises, "+X", finest mesh, MPa | 21.85 | 6.55 |

The first run of this round with STEM_A2, the untwisted stem, gave `fail`, lowest factor 1.38 at "+Y, layer", place
[0.28, -3.19, -34.48]. The STEM_A3 run gave `fail`, 1.57, same entry and place. I stopped there, as S4 says.

**3. The print statement.** `print_orientation` (results.json): tilted 30 degrees, hub end down: the long axis leans
30 degrees from the vertical towards +X, the hub (elbow) end is at the bed and the fork is at the top; height about 222 mm
of 256, footprint about 120 x 120 mm. Layers are flat on the bed, so in the part they are stacked along (0.5, 0, -0.866).
Printed with a brim, no raft. From `orientations.json` for "tilt 30 to +X, hub end down": height 222.2 mm, footprint
121 x 120 mm, fits True, support area 692 mm2, bed contact 8.2 mm2. Patches (area, place, face):
- 273 mm2 at [-16, 0, 28]: hub rim (Z above +20).
- 162 mm2 at [9, 0, -10]: inside the bore (X and Z both within 16 of the Y axis line through the hub).
- 42 mm2 at [2, -19, -203]: fork (Z below -190).
- 42 mm2 at [2, 19, -203]: fork.
- 21 mm2 at [13, 0, -23]: stem.
- 21 mm2 at [13, 0, 20]: stem.
- 21 mm2 at [-24, 0, -1]: stem.
- 21 mm2 at [26, 0, -1]: stem.

Whether the patches on the hub rim and the stem are acceptable is Joey's decision.

**4. Nine directions, from the table the script wrote (finest mesh, three cases).** These are readings, not verdicts. For
each direction: the lowest of 45 / von Mises, 22.5 / across layers, and 13 / between layers, over +X, -X and +Y.
- X: 2.65 (+Y, between layers).
- Y: 1.67 (+Y, across layers).
- Z (upright): 1.39 (+Y, across layers).
- tilt 20 to X: 1.46 (+Y, across layers).
- tilt 30 to X: 1.57 (+Y, across layers).
- tilt 45 to X: 1.81 (+Y, across layers).
- tilt 20 to Y: 1.45 (+Y, across layers).
- tilt 30 to Y: 1.60 (+Y, across layers).
- tilt 45 to Y: 1.63 (+Y, between layers).

**5. Branches taken, with the error line that sent me there.**
- S2.4, first `c2_detail.py` run: `TWIST_CHECK fail`, 75 degrees between Z -72 and -85. Branch: `LOFT_PICK` changed from
  'x' to 'bottom'. Second run: `TWIST_CHECK ok` (largest turn 0.6 degrees), `PINCH_CHECK ok`.
- S4.4, first verdict `fail` (1.38, "+Y, layer"). Branch: `put(C2, table_name='STEM_A3')`, `c2_detail.py` (third run,
  `TWIST_CHECK ok`, `PINCH_CHECK ok`, `PRINT_CHECK ok`), `c2_fea.py fresh` again. Second verdict `fail` (1.57, "+Y, layer").
  Branch: stop trying, C2 "not done: requirement not met".
- A hold was called by the coordinator after the second study: no SolidWorks job was started after it ended (22:19:06).
  The report and the check of the finished result did not need SolidWorks.
- The two `c2_fea.py` runs were started in the background (not under `timeout`, not in the foreground) so the shell
  limit did not stop them. Each was watched to its end.

**6. Times** (from `times.log`, clock -0600, all on 2026-11-14):

| Step | Between | Min |
| --- | --- | --- |
| S1 set-up | round 2 start 21:57:24, to detail start 21:57:30 | 0.1 |
| S2 part, twist, pinch (two `c2_detail.py` runs) | 21:57:30 to checkpoint 21:59:22 | 2.0 |
| S3 print direction | 21:59:22 to study start 21:59:42 | 0.3 |
| S4 study (two runs, one `c2_detail.py` retry) | 21:59:42 to study end 22:19:06 | 19.4 |
| S5 finish | study end 22:19:06 to C2 end 22:19:34 | 0.5 |

Total: 22.2 min, 21:57:24 to 22:19:34 (`C2 end`). `c2_detail.py` runs: three. Run 1, loft at 'x', twist fail;
run 2, loft at 'bottom', twist ok; run 3, table STEM_A3, after the first verdict fail. `c2_fea.py` runs: two.

**7. Anything wrong in the instructions or helpers.**
- S2 expectation "the follow-up part reads about 90 between Z -72 and -85": measured 75 degrees on the first try, so the twist
  check did fail, as the branch predicted.
- S4.1 expectation "lowest factor at the neck (Z -25 to -45)": met (-34.48), and the hand estimate of 6 to 9 MPa at Z -79
  was met (6.55 MPa).
- S3 support expectation 770 ± 200 mm2: measured 692, inside the range.
- The S4.3 "print-direction table" is written by the script into REPORT.md, so I read the figures there, not copied from the console.
- DESIGN.md last line: the twist note says "now 12.2 mm", taken from the final STEM_A3 slice at Z -78 (12.17). It was edited
  after the STEM_A3 retry, from the final part's slice.
