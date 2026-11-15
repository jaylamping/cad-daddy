## T6. Contact between two bodies: **done, result valid** (38 minutes of the 40; three different models of the pin were run)

**The case.** PETG block X ±20, Y ±15, Z 0 to 20, Ø10.2 hole along Y at X 0, Z 10; Ø10 steel pin, 50 long (Y ±25), 10 mm out each side, **centred**; block bottom fixed; 250 N up (+Z) at each stub. Frictionless no-penetration contact, direct sparse solver. Files in `_wip/sw-eval/sonnet-adv-a/t6c/` (centred, the reported model: `tp_all.SLDPRT` = block plus five inserted bodies) and `t6b/` (the pin seated at the crown); scripts `t6_centred.py`, `t6.py`, post-processing `t6_post2.py`, table `gen_t6.py`.

**Hand calculation.** Mean projected bearing 500 / (10 × 30) = **1.67 MPa** (a floor). Pin in a socket 0.1 mm larger on the radius (Hertz, line contact): R* = 1 / (1/5 − 1/5.1) = 255 mm, E* = 1 / ((1 − 0.28²)/210,000 + (1 − 0.38²)/1,900) = 2,198 MPa, w = 500 / 30 = 16.67 N/mm, half-width b = sqrt(4 w R* / (π E*)) = 1.57 mm, **peak p₀ = 2 w / (π b) = 6.76 MPa** (`hand_bearing_mpa`). The pin must rise 0.100 mm before it bears at all.

**How the pin is held.** Two soft pads (Ø3 × 2 mm discs, E 0.5 MPa, ν 0.45) on the two pin end faces, outer faces fixed, clear of the block; about 0.6 N/mm each in shear by hand (the proof below measured 1.02 N/mm for the two together). The pin is built in three bonded pieces (two 10 mm stubs and a 30 mm centre) so the 250 N `remote` loads sit on the stub cylinders and the contact set takes the centre face alone (the contact set takes whole faces). No other restraint: the pin bears on the hole through contact only.

**Predictions, written before the solve:** nodes 45,000 (actual 86,685 on the 0.8 mm run: 1.9 times, because the 0.8 mm controls on two 950 mm² faces are most of the mesh; my formula covers a global size only, and I should have counted the controlled faces), pin rise 0.10 mm plus a few µm, peak 6.8 MPa on the crown near the block faces, half-width 1.57 mm.

**What I ran, and what each was for.**
1. **Run 1 (centred, `t6_v1_*`): invalid, my mistake.** `contacts=` was never passed. The pin moved 490 mm; pads reacted 99.97 % of the load. Not used.
2. **Run 2 (pin seated at the crown, `t6.py`, `t6b/`):** after run 1 I believed a centred pin with only 0.6 N/mm of pads under a 500 N pull would run away in the solver's first, open-contact step, so I placed the pin 0.100 mm high plus 0.002 mm of overlap so the contact is closed from the start. It works and is kept as a cross-check, but **I had not tested the centred model with the contact set when I wrote that.** A reviewer's challenge made me run it:
3. **Run 3 (centred, contact set present, `t6_centred.py`, `t6c/`): the reported one.** It solves cleanly at 41,136 nodes (43 s) with no excessive-displacement prompt, so the contact solver crosses the 0.1 mm gap by itself and my belief was wrong. The run-2 model is therefore a modelling choice I did not need.

**Studies** (contact faces and pads meshed at the size shown; global 3.0 mm; all direct sparse, Intel Direct Sparse in the benchmark log, 12 to 20 contact iterations). Peak pressure is the radial compression (−σ_rr) on the *block's* hole wall (nodes labelled by geometry and by node-id run, see "Checks"), smoothed over 1 mm and 2 mm; "raw" is the single largest node.

| Model, case | Size mm | Nodes | s | Fz N | Pads Fz N | Pad share | Pin mean uz mm | Peak pressure 1 mm / 2 mm / raw MPa | Half-width mm | Block von Mises, raw max, where |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **centred** | 1.2 | 41,136 | 43 | −500.004 | −0.138 | 0.028 % | 0.1292 | 6.36 / 5.42 / 6.65 | 2.05 | 5.64 at (2.0, −15.0, 16.1) |
| **centred** | 0.8 | 86,564 | 147 | −500.004 | −0.138 | 0.028 % | 0.1291 | 5.99 / 5.21 / 6.61 | 1.98 | 5.12 at (−2.3, 15.0, 15.5) |
| **centred** | 0.6 | 149,971 | 453 | −500.001 | −0.138 | 0.028 % | 0.1292 | **5.79 / 5.03 / 6.27** | 2.08 | **5.22 at (1.7, −15.0, 15.9)** |
| centred, proof | 0.8 | 86,564 | 107 | −0.500 (0.001 load) | −0.102 | 20.4 % | 0.1000 | 0.01 | n/a | 0.04 |
| seated | 1.2 | 40,870 | 35 | −500.0 | −0.035 | 0.007 % | 0.0275 (+0.100 gap) | 6.22 / 5.28 / 10.13 | 2.05 | 6.11 |
| seated | 0.8 | 86,685 | 109 | −500.0 | −0.035 | 0.007 % | 0.0278 | 5.79 / 5.13 / 9.83 | 2.06 | 5.67 |
| seated | 0.6 | 150,090 | 309 | −500.0 | −0.035 | 0.007 % | 0.0278 | 5.48 / 4.97 / 10.65 | 2.08 | 5.77 |
| seated, reversed 0.001 | 0.8 | 86,685 | 165 | +0.500 | +0.206 | 41 % | −0.202 | 0.01 | n/a | 0.03 |

**Results (centred, 0.6 mm, 149,971 nodes).**
- `peak bearing stress on the hole`: **5.8 MPa** (1 mm smoothed; 5.0 over 2 mm; 6.3 at a single node). Hand Hertz 6.76: the finest raw value is 7 % lower and the smoothed one 14 % lower, inside the 20 % band. The contact patch is 2.05 mm half-wide (hand 1.57), because the contact is conformal (b/R about 0.4).
- Where: the pressure sits on the crown of the hole (Z 15.1, X within 0.2 mm of 0), and along Y between about ±10 and ±12 mm in all three meshes (the sign changes with the mesh: the crown is flat to within the node noise).
- `peak_contact_vm`: the largest von Mises in the block near the hole is **5.2 MPa** (smoothed over 1 mm 4.6), at the **edge of the hole where it meets a block face** (1.7, −15.0, 15.9), about 6 mm from the crown, not at the crown. Factor on 45 MPa: 8.6.
- `pin_rise_mm`: **0.129** (0.100 clearance, then 0.029 as the block's hole roof and pin move up together: the pin's mean uz 0.1292, the block crown's 0.0288 beyond that gap, the pin crown's 0.1294: they move together). The hand value covers only the stretch of the side ligaments (0.004 mm). The rest is bending of the 4.9 mm roof and the ovalising of the hole under 500 N, which I did not calculate by hand: **the 0.029 is not explained by a hand value, and I put nothing on it.** The spread of the pin's centre uz (0.086 to 0.174 on the 0.8 mm mesh, 0.126 to 0.134 on the 0.6) shows it tilts a little, as the end pads are soft: harmless; 07-done step 10 about spin applies.
- Reaction: **500.00 N** (499.86 at the block bottom, 0.138 N in the pads).

**Checks.**
1. **Reaction against load:** 500.00 for 500; pad share 0.028 %, under 1 %; the pads' force at 0.1 mm of pin travel is 0.1 N, as the stiffness says.
2. **The contact is a contact, not a bond (05-fea "A body with clearance on both sides": apply a thousandth of the load in the working direction, never reverse).** At 0.5 N up the pin rises **0.1000 mm** (spread 0.0998 to 0.1003): exactly the radial clearance, then bears on the crown with 0.398 N of the 0.5 N, the pads holding 0.102 N. A bond would have moved it about 1e-7 mm. The seated model's reversed proof (the pin travelling 0.199 of 0.202 mm down onto the hole bottom) says the same.
3. **Nodes are in the right body.** The first version of my post-processing selected the hole wall by radius from the axis, which on the seated model (pin 0.002 mm into the crown) put pin nodes in the "block" band: 797 of 8,047 on the 0.8 mm mesh, which made the block's von Mises 30 MPa (the pin's own 31 MPa, steel). Corrected by node-id runs (the mesh numbers each body's nodes in one unbroken run; 05-fea contact rule 5): checked against nodes that are certainly in one body (zero overlap between the runs, zero certain nodes in another body's run, on every mesh). On the centred model the two walls are 0.1 mm apart, so radius alone separates them (zero pin nodes in the band) and the two methods agree. The corrected block von Mises is 5.2 MPa, not 30.
4. **Hand against study:** Hertz 6.76 against 6.27 raw, 5.79 smoothed. A Hertz-shaped patch of p₀ = 5.79 MPa, b = 2.08 mm, L = 30 mm carries (π/2) p₀ b L = 568 N for 500 applied (14 % over) with the 1 mm-smoothed peak, and 493 N with the 2 mm-smoothed (5.03 MPa): the force closes within 1 to 14 %, depending on the smoothing, which is the best the nodal pressure can do.
5. **Mesh:** peak pressure 6.36, 5.99, 5.79 MPa over 41,136, 86,564, 149,971 nodes (steps −5.8 %, −3.3 %, the last under 5 %); pin translation 0.1292, 0.1291, 0.1292; reaction identical. The seated model gives 6.22, 5.79, 5.48 and the same pin rise (0.128): at 0.6 mm the seated model reads 5.48 (5 % lower at 1 mm smoothing, 1 % lower over 2 mm).
6. **The two models agree on the answer;** the seated one is not needed.

**Verdict: valid.** The pressure series is settled by the 5 % rule at the finest step (3.3 %). The raw node values are noisy at 0.6 to 1 mm element size, so the number to quote is the smoothed one.

**Not verified.** (1) Friction (none, which leaves the pad-held lateral freedom larger than a real pin's). (2) The rigid coupling of the loaded stubs, which keeps the pin ends from ovalising and makes the pin stiffer in bending than a real pin with a clevis or rod end. (3) The block-face edge (Y = ±15): the raw pressure on one node there reads −6 MPa (tension) and the von Mises peak sits there, so a feature of 0.5 mm or less would not be seen at this mesh. (4) The 0.029 mm of pin rise on top of the clearance (above). (5) A contact patch edge finer than 0.6 mm.
