## T1. Bracket from a specification: done

**What I did.** `t1_t2.py`: base plate and upright as two mid-plane extrudes (24,000 and 12,000 mm³, merged to one body), R4 fillet on the one edge along Y at X 6, Z 6, then the base holes, the bore and the four Ø3.4 holes as three cuts, then the R5 rounds in two groups. Every feature carried `expect_dv`; each raised unless the volume change was within 1 % of the hand value. Saved after every step. `bracket.SLDPRT`, `bracket.step`, `bracket.stl` are in `_wip/sw-eval/sonnet-adv-a/` (gitignored); the script is `t1_t2.py`.

**Hand calculation** (in the script): 24,000 + 12,000 + 171.68 (R4: (16 − 4π) × 50) − 570.2 (4 × π 2.75² × 6) − 2,280.6 (π 11² × 6) − 217.9 (4 × π 1.7² × 6) − 64.4 − 64.4 (four R5 rounds, 5.365 mm² × 6 each) = **32,974.02 mm³**, 39.24 g at 1.19 g/cm³.

**Checks, with numbers.**

| Check | Result |
| --- | --- |
| volume | 32,974.02 mm³ against hand 32,974.02 (0.000 %) |
| box | 0, 0, 0 to 80, 50, 46 (each within 0.01 mm) |
| bodies, rebuild errors | 1, 0 |
| base holes (`pick` + `face_info`) | four Ø5.5 faces with box centres (25, 10), (25, 40), (65, 10), (65, 40), z centre 3.0, all to 0.01 mm |
| bore | one Ø22 face, centre Y 25.0, Z 28.0 |
| small holes | four Ø3.4 faces, centres (Y, Z) = (14.04, 17.04), (14.04, 38.96), (35.96, 17.04), (35.96, 38.96): 25 ± 10.96, 28 ± 10.96 |
| R4 | one face, box X 6 to 10, Z 6 to 10, full width 50 |
| R5 | four faces: (X 75 to 80, Y 0 to 5 and 45 to 50, Z 0 to 6) and (X 0 to 6, Y 0 to 5 and 45 to 50, Z 41 to 46) |
| STL | watertight, one shell, volume 32,990.4 mm³ (0.05 % over the solid: facets), bounds within 0.1 mm of the box |
| STEP | `SI_UNIT` line carries `.MILLI.` |

Picture check (`pictures_bracket.png`): an L-bracket, plate low, upright at the X 0 end, a visible inside round, four holes in the plate, a bore with four small holes in the upright, rounded corners on the far end of the plate and on the top of the upright. It matches the specification.

**The specification, questioned (not changed).** (1) The Ø3.4 holes sit 2.8 mm from the bore wall (15.5 − 11 − 1.7), less than one hole diameter; an M3 boss there is a stress raiser, and T3 finds it governs. (2) The bore has 6 mm of bearing length for a Ø22 (length/diameter 0.27); fine for a pilot, thin for a shaft. (3) The upright is 6 mm thick, loaded across its thickness in T3. (4) Fine otherwise: bore top to upright top 7 mm, bore bottom to plate top 11 mm, base hole edge to side 7.25 mm, to the fillet toe 12.25 mm, all walls over 0.6 mm; nothing contradicts anything.

**Not verified.** Nothing about print: no slice, no overhang check on the bore.

## T2. Change an existing part: done

**What I did.** Opened the saved `bracket.SLDPRT` (volume checked to 0.01 % on opening), `save_as` to `bracket_b.SLDPRT` **before** the edit, then cut the four Ø10 × 3 counterbores (one sketch of four circles, mid-plane on Z 4.5, depth 3) and the slot as a 14 × 6 rectangle plus two R3 circles (so no arc direction to get wrong). Hand volume: 32,974.02 − 4 π (25 − 2.75²) × 3 (657.4) − (14 × 6 × 6 + π 9 × 6) (673.6) = **31,643.0 mm³**; measured 31,643.0.

**Checks.** Feature tree before: 35 entries; after: the same 35 (compared by name and type; I did not compare internal IDs) plus twelve new ones (`CB_P`, `CBORE_SK`, `CBORE`, `SLOT_P`, `SLOT_RECT_SK`, `SLOT_RECT`, `SLOT_E1P`, `SLOT_END_L_SK`, `SLOT_END_L`, `SLOT_E2P`, `SLOT_END_R_SK`, `SLOT_END_R`), so it was an edit and not a rebuild. The original file: same SHA-256 before and after (`e6880b16…a35379`) and the same volume when reopened. Counterbore floors: four planar faces at Z = 3.000 with outer diameter 10.000; four Ø10 wall faces. Slot: two R3 faces, overall length 20.000, width 6.000, centre X 45.000, Y 25.000. One body, no rebuild errors, box unchanged. Picture (`pictures_bracket_b.png`): four stepped holes on the plate, one slot between them on X 45, upright untouched.

**Not verified.** Counterbore against a real screw head. Computed, not measured on the solid: the slot ends at X 35 and 55 and the counterbores span X 20 to 30 and 60 to 70, so the web between a slot end and a counterbore is 5 mm each side; the slot to the plate edges 22 mm.

## T3. Static study with a verdict: **fail** (tension across the layers, about 1.5)

**The case, written before SolidWorks.** The bore axis is X and the load is +X, so it is **axial**: a bearing load is refused (05-fea: it must be square to the axis) and an even normal force on the bore sums to zero (reaction 0, 05-fea). A rigid `'remote'` load on the bore stiffens exactly the ligaments that matter (05-fea reports this very bracket passing at 2.2 where it fails at 1.4). So the load goes where a screwed-on motor puts it: through the four M3 heads on the X = 0 face. I made a twin `bracket_t3rings.SLDPRT`: the T1 part plus a 0.3 mm deep, Ø6 circular step round each Ø3.4 hole (volume −23.0 mm³ = 0.07 %, box identical), and put an even 150 N on the four step floors (faces that look along −X, force +X). Support: the four Ø5.5 hole walls fixed. PETG as `swfea.PETG`, layers stacked along Z (base on the bed).

**Hand estimate.** Moment about the plate top 150 × 22 = 3,300 N·mm; root of the upright, 6 M / (b h²) = 6 × 3,300 / (50 × 36) = **11.0 MPa** (compression on the fillet side, tension on the X = 0 face). At the lower Ø3.4 holes the section moment is 150 × 11 = 1,650 N·mm, nominal 5.5 MPa, times 3 for a small hole = **16.5 MPa** across the layers: factor 1.36, a fail before any solve. Upright tip 0.31 mm alone. **My first displacement prediction was wrong:** I forgot the plate turns between the screws (a cantilever 25 mm beyond the first screws, 0.048 rad, 40 mm up the upright = 1.9 mm); with that 2.2 mm, solved 2.84 mm. That was a 9-fold miss, past the factor 3 at which 07-done says to stop; I stopped to explain it (the plate rotation gives 2.2 mm, within 30 % of the solve) before I trusted any stress, and went on only then.

**The series** (`t3a.py`, `lib3.py`; hole walls fixed, rings loaded, controls shrunk with the global size: rings el/3, small and fixed hole walls el/2):

| el mm | nodes | peak von Mises, hole rims | layer tension (Z), hole rims | interlayer shear (Z), hole rims | interlayer shear (Z), root fillet | max disp mm |
| --- | --- | --- | --- | --- | --- | --- |
| 3.0 | 24,804 | 17.84 | 14.59 | 5.56 | 6.69 | 2.837 |
| 2.2 | 53,442 | 18.19 | 14.57 | 6.33 | 7.06 | 2.846 |
| 1.6 | 123,582 | 18.79 | 14.47 | 6.51 | 7.02 | 2.851 |

Hole rims = nodes within 2.2 mm of the hole axis, whole thickness. I did **not** use `converge()`: it masks nodes within two coarse elements of every load face, which swallows exactly these rims (the rings are the load faces). Instead `measures()` in `lib3.py` reads regions at every size and `judge()` is fed the series (three measures × four regions). Peak von Mises sits at (6.0, 15.7, 17.4): on the X = 6 face at the lower Y-low hole.

**The five checks.** (1) Reaction Fx −149.993 N for 150 N (0.005 %), Fy, Fz under 0.005 N. (2) Displacement 2.84 mm against hand 2.2 (the explained 30 % miss; the first prediction, 0.3 mm, was off 9 times). (3) Plain section, σz on the X = 0 face at z 12 to 14: my first reading, the middle of the width only (y 18 to 32), was 5.6 MPa against hand 7.5, 25 % low and outside the 15 % band. I then read it across the full width from the saved nodal results (`T3_RINGS_el*.npz`): the mean over all nodes is 6.7 and over ten equal y-bins 7.1 (7.2 and 7.1 on the two coarser meshes), against 7.5, and the stress is not uniform in y: 5.6 in the middle, 6.0 beside the holes, **9.6 at both edges** (shear lag: the load enters at y ≈ 14 and 36 through the rings). Integrating σz over the whole section at z = 13 gives a net force of −8 N (should be 0) and a moment of 2,541 N·mm against the hand 2,250 (13 % high; 2,596 and 2,566 on the coarser meshes). So check 3 passes on the section as a whole, and the middle-strip reading was the wrong place to look. (4) Peak not on a fixture or load face: the vm peak is a hole rim 6 mm from the loaded face (excluded fixture singularity: fixed hole walls, nodes within 2.5 mm are not read). (5) Converged: layer tension 14.59 → 14.57 → 14.47 (0.7 % last step), shear 2.8 %, vm 3.3 %.

**Second support (bottom face fixed, 2.2 mm):** layer tension at the rims **15.31** MPa, shear 5.75, vm 16.9; displacement 1.17 mm. Higher than the hole-wall support (14.57 at the same size). Reported value is the higher: 15.31.
**Second load (rigid):** `remote` on the bore at the same mesh: hole rims layer tension **9.80**, vm 10.9 (the trap: factor 2.3, a pass); `remote` on the four Ø3.4 walls: 22.5 at the loaded wall itself (rigid coupling artefact, not used), 1.5 clear of it. Higher of the credible ways: the rings.

**Print directions (finest mesh, worst region of each; same solve):**

| Layers along | von Mises (45) | Tension across layers (22.5) | Interlayer shear (13) |
| --- | --- | --- | --- |
| Z (base on bed) | 18.79, factor 2.39 | 14.47 hole rims, factor **1.56** (15.31 with the other support: 1.47) | 7.02 root fillet, factor **1.85** |
| X (on its back) | 18.79, 2.39 | 17.10 base near the first screws, factor **1.32** | 7.03 root fillet, 1.85 |
| Y (on its side) | 18.79, 2.39 | 8.31 hole rims, 2.71 | 6.495 hole rims, **2.0015** (on the line; the Z-layer shear at the same rims is 6.507, 1.998, which `judge()` prints as "factor 2.0" and calls a fail) |

**Verdict: fail.** `judge()` for Z: `fail`, lowest factor 1.56 (tension across layers at the lower small-hole rims), plus shear at the root fillet 1.85 and at the rims 1.998. Von Mises passes at 2.39. Load path: the 150 N goes from the screw heads into the X = 0 face, across the 6 mm upright as bending about Y, down to the root, then as a moment into the plate, which turns about the first screws; the lower holes sit where the section is weakest and the stress is concentrated. Cheapest fix found (T5): print on its side, then thicken the upright.

**Not verified.** The real motor load path (screw preload, friction, the motor's own pilot in the bore). The ring recess steps are 0.3 mm deep and are part of the model, not of the part as drawn. Peak shear at the fillet is on a 45° surface and is a fair reading of the printed layer lines there but I did not slice it.

## T4. The same study on a variant: **fail**

**What I did.** `bracket_build.py` rebuilds the T1 part with the same features and checks, no fillet: `bracket_sharp.SLDPRT` (volume 32,802.3 mm³ = 32,974.0 − 171.7, as hand; one body; no R4 face). Twin with the same rings, same load case, hole walls fixed, an edge mesh control (el/4) along the sharp corner. Then, because a sharp inside corner cannot converge, the same part with the 0.4 mm radius a printed edge has (`T4 R04`: face control el/8).

| Variant | el mm | nodes | corner von Mises | σz on the corner line | mean vm within 0.5 / 1 / 2 mm of (6, 25, 6) |
| --- | --- | --- | --- | --- | --- |
| sharp | 3.0 | 32,188 | 22.79 | −27.3 | 13.19 / 10.15 / 8.58 |
| sharp | 2.2 | 65,250 | 25.98 | −33.1 | 15.92 / 11.43 / 8.69 |
| sharp | 1.6 | 145,669 | 30.00 | −37.5 | 15.15 / 10.80 / 8.64 |
| R0.4 | 3.0 | 44,019 | 38.31 | −34.6 | 15.20 / 13.43 / 11.32 |
| R0.4 | 2.2 | 85,045 | 38.35 | −34.6 | 16.85 / 13.42 / 10.90 |
| R0.4 | 1.6 | 195,072 | 40.41 | −33.4 | 17.29 / 13.82 / 11.63 |

**Judgement.** The sharp corner is a **singularity** (it is the re-entrant corner, compression under +X, σz −27 → −37 MPa, von Mises 22.8 → 26.0 → 30.0: steps 14 % and 15 %, not settling). It is not a stress of the part, and the number to report is not 30. The mean over 2 mm holds at 8.6 MPa across all three meshes: that is the section value, and it matches the hand value (11.0 nominal at the root, lower 2 mm in). With the printed 0.4 mm radius (the edge the part really has) the corner reads **38.3, 38.4, 40.4 MPa**: the last step is 5.4 % after 0.1 %, so it is **not fully settled**, and Kt ≈ 3.5 (hand: nominal 11.0 × Kt for r/t 0.07 about 3.5 = 38). Factor on von Mises 45 / 40.4 = **1.11**: under 2.0. The hole-rim layer tension (14.5 MPa, factor 1.55) is the same as in T3. **Verdict: fail**, on both. The T3 part with its 4 mm radius reads 15.0 at the same place: the radius is worth a factor 2.7 there, which is why the specification has it. `reported_stress_mpa` is the R0.4 value 40.4 (the number I would stand behind); the sharp-mesh peaks are in `convergence_rows`.

**Not verified.** The R0.4 corner: the control on the 0.4 mm round was el/8 (0.375, 0.275, 0.2 mm elements), so 0.2 to 0.375 mm elements on a round that small make 40.4 a lower bound, not a converged value. The R0.4 corner was left at three sizes, 5 % still moving at the finest, 195,072 nodes (the cap is 200,000); a fourth size would have needed a finer control only on the 31 mm² of the round, which I did not try.

## T5. Make it pass: **done** (bracket_c.SLDPRT)

**First attempt, print direction only (no mass).** From the T3 table, layers along Y gives vm 2.39, tension 2.71, shear 2.00: a pass on paper at no mass, but the shear is on the line (2.0015) and the tension at the rims was climbing 11 % at the last step, so `judge()` says `margin, not converged`. Not good enough by itself.

**Change.** The upright thickened from 6 mm to 7.5 mm **on the inner (+X) face** (the outer face, the bore, every hole, and the footprint X 0 to 80, Y 0 to 50, Z 0 to 46 unchanged; mass +7.15 %, 42.05 g against the 43.16 g cap), and R0.4 on the four hole mouths on the inner face (`MOUTH_ROUNDS`, volume −1.5 mm³). Print on its side: **layers stacked along Y** (the L profile lies in the layer plane, so the bending stress and the hole stress concentration run along the layers). Hand: bending stress ∝ 1/t², so 14.5 × (6 / 7.5)² = 9.3 MPa across Z layers; the study read 9.52.

A first build without the mouth rounds (`t5_first.py`) read the shear at the hole mouths on the X = 7.5 face going 3.74, 3.90, 4.47 MPa (growing step, 13.8 % after 5.2 %) and `judge()` said `not shown`. Per 07-done step 6 I gave that edge its printed radius (0.4 mm) and solved again; the peak moved onto the new round (x = 7.1) and settled to 4.49, 4.81, 5.03 (last step 4.7 %).

**Study** (`t5.py mouth`; same load case as T3, hole walls fixed; sizes 3.0, 2.2, 1.6; nodes 27,152 / 57,571 / 133,238):

| Layers along | von Mises (45) | Tension across layers (22.5) | Interlayer shear (13) | `judge()` |
| --- | --- | --- | --- | --- |
| **Y (chosen)** | 16.52 base, factor **2.72** | 5.98 base, **3.76** (hole rims 5.78) | 5.00 hole rims, **2.60** | **pass**, lowest factor 2.60 |
| Z | 16.52, 2.72 | 9.52 hole rims, **2.36** | 6.43 root fillet, **2.02** | pass, lowest 2.02 (thin) |
| X | 16.52, 2.72 | 17.08 base, **1.32** | 6.43, 2.02 | fail |

Second support (bottom face fixed, 2.2 mm): hole rims tension 9.84 across Z, 4.81 across Y, shear 4.02: no worse than the hole-wall support in Y. Reaction 150 N; displacement 2.23 mm. Mass 42.045 g (hand and STL volumes agree: 35,333.25 against 35,331.71). Footprint box 0, 0, 0 to 80, 50, 46; bore centre Y 25.0, Z 28.0 measured; base and small holes unchanged.

**The thinnest margin** is the shear in the root fillet at 2.02 if someone prints it base-down: it is not a pass to rely on. **The cheapest improvement** is the orientation (on its side), at no mass. **Not checked:** the motor's real load; buckling is irrelevant (no slender members); the long-term creep of the pressure under the screw heads; whether the part prints on its side (a 50 mm tall print, bore and base holes horizontal, bridging at the bore top).

(`bracket_c.SLDPRT` is the rounded-mouth build; the first build is kept as `bracket_c_first.SLDPRT` in `_wip`.)
