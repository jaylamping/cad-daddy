# A_T6: pin in a hole, contact only (40 minutes, hard stop)

## 1. Restatement

PETG block X −20..20, Y −15..15, Z 0..20, Ø10.2 hole along Y at X 0, Z 10. Steel Ø10 pin, Y −25..25, centred (0.1 mm
radial gap all round). Block bottom fixed; 250 N up on each pin end (500 N +Z). Pin to block by contact only. Find the
peak bearing stress on the hole and show the result is valid. At 40 minutes stop and report how far you got.

Checklist:
- [ ] three bodies-plus-pads model built, boxes and volumes checked, no overlaps
- [ ] full-load contact solve: reaction −500 N in Z within 1 %, pads carry < 1 %
- [ ] contact proof: 0.5 N in the working direction gives a pin rise ≈ the 0.1 mm gap (not 1/1000 of the full rise)
- [ ] bearing stress read in the block only (geometry split), with a series on the contact control
- [ ] hand values beside every result

## 2. Hand numbers

| Quantity | Working | Value | Accept |
| --- | --- | --- | --- |
| Volumes | block 40·30·20 − π·5.1²·30 ; pin π·5²·50 | 21 548.6 ; 3 927.0 mm³ | ±0.1 % |
| Mean (projected) bearing | 500 / (10 x 30) | **1.67 MPa** (`hand_bearing_mpa`) | – |
| Peak contact pressure (Hertz, cylinder in a conforming hole) | q = 500/30 = 16.67 N/mm; 1/R = 1/5 − 1/5.1 → R = 255 mm; 1/E* = (1−0.38²)/1900 + (1−0.28²)/210000 → E* = 2 199 MPa; b = √(4qR/πE*) = 1.57 mm; p0 = 2q/(πb) | **p0 ≈ 6.8 MPa**, contact width ±1.57 mm (±18° of the hole) | −P3 at the hole top 5–9 MPa |
| Von Mises in the contact zone | line contact: max ≈ 0.56 p0 at 0.7b below the surface | ≈ 3.8 MPa (plus ligament bending, below) | 2.5–7 |
| Ligament above the hole (Z 15.1..20), bending | clamped beam, span ≈ 10.2, width 30, 4.9 thick: M ≈ FL/8 = 637 N·mm, Z = 30·4.9²/6 = 120 mm³ | ≈ 5.3 MPa σx at Z 20 over the hole | 3–9 |
| Pin rise | gap 0.1 + ligament δ = FL³/(192EI) ≈ 0.005 + contact ≈ 0.005–0.01 | **≈ 0.11–0.12 mm** (`pin_rise_mm`) | 0.10–0.15 |
| Pin bending at the hole mouth | M = 250 x 10 = 2 500 N·mm; 32M/πd³ | 25.5 MPa (steel, not judged) | – |
| Reaction | fixtures push back | Fz = **−500 N** | 1 % |
| Pad share | 2 pads, shear stiffness G·A/L = (0.5/2.9)·4/2 ≈ 0.34 N/mm each; x 0.12 mm | ≈ 0.08 N (0.02 %) | < 5 N (1 %) |
| Nodes | el 2.5 global, contact control c on the hole and pin faces | c 1.2 → 30 000; 0.8 → 50 000; 0.55 → 90 000 | x2 |

Where the peak should be: the top of the hole (Z ≈ 15.1, X ≈ 0) along its length; the hole mouths (Y ±15) may read
higher because the contact ends at a free face there (edge effect): read them separately.

## 3. Build (job 1)

Four parts, all in the model frame:
1. `t6_block.SLDPRT`: plane Z 10, rect (−20, −15, 10)–(20, 15, 10), extrude 20 MID, expect 24 000. Hole: plane Y 0
   (`plane(d, 'Y', 0.0, ...)` returns Top Plane), circle (0, 0, 10) r 5.1, extrude 34 MID cut, expect π·5.1²·30 =
   2 451.4. Save.
2. `t6_pin.SLDPRT`: plane Y 0, circle (0, 0, 10) r 5.0, extrude 50 MID, expect 3 927.0. Save.
3. `t6_padA.SLDPRT`: plane Y 26, rect (−1, 26, 9)–(1, 26, 11), extrude 2 MID (Y 25..27), expect 8.0.
   `t6_padB.SLDPRT`: plane Y −26, same at y −26, expect 8.0. Pads sit on the pin end faces, clear of the block
   (which ends at |Y| 15).
4. `t6_model.SLDPRT`: open `t6_block.SLDPRT`, `save_as` to `t6_model.SLDPRT`, `insert_body` the pin, padA, padB.
   `bodies(d)` → 4 bodies; boxes: block (−20,−15,0,20,15,20), pin (−5,−25,5,5,25,15), pads (−1,25,9,1,27,11) and
   (−1,−27,9,1,−25,11). Total volume 21 548.6 + 3 927.0 + 16.0 = 25 491.6. No overlap: the pin box lies inside the
   hole's radius (5.0 < 5.1), check by the radii, not the boxes (the boxes overlap by design). Save.

## 4. Study (job 2, at most four solves)

```python
PAD = dict(name='Soft pad', EX=0.5e6, NUXY=0.45, DENS=1000.0, SIGYLD=1e6, SIGXT=1e6)
j.simulation(); d = open_doc(j.sw, W/'t6_model.SLDPRT'); d.ForceRebuild3(False)
def picks():
    hole = pick(d, kind='cyl', r=5.1)                       # 1 (block hole)
    pin  = pick(d, kind='cyl', r=5.0)                       # 1 (pin surface, Y −25..25)
    base = pick(d, kind='plane', at=(0, 0, 0))              # 1 (block bottom)
    endA = pick(d, kind='plane', normal=(0, 1, 0), at=(0, 25, 13))    # pin end face Y 25 (point off the pad)
    endB = pick(d, kind='plane', normal=(0, -1, 0), at=(0, -25, 13))
    padA = pick(d, kind='plane', at=(0, 27, 10)); padB = pick(d, kind='plane', at=(0, -27, 10))
    return hole, pin, base, endA, endB, padA, padB
def run(c, f_each, name, loose=True):
    hole, pin, base, endA, endB, padA, padB = picks()   # every count must be 1: print them
    r = static(j, d, name, PETG,
        fixtures=[('fixed', base), ('fixed', padA + padB)],
        loads=[('remote', endA, (0, 25, 10), (0, 0, f_each), (0, 0, 0)),
               ('remote', endB, (0, -25, 10), (0, 0, f_each), (0, 0, 0))],
        el=2.5, ctrl=[(hole + pin, c), (padA + padB, 0.7)],
        contacts=[(NO_PENETRATION, hole, pin)],
        materials={'t6_pin': STEEL, 't6_pad': PAD}, solver=SOLVER_DIRECT, loose_ok=loose)
    np.savez(W/f'{name}.npz', pos=r.pos, s=r.s, disp=r.disp, reaction=r.reaction); return r
```
Material log must show: block PETG (default), pin Steel, both pads Soft pad. `loose_ok=True` because the pin is held
only by soft pads until the gap closes: the solver may ask about excessive displacements; that is expected here
(05-fea rule 8) and is answered No.

Solves: `T6_FULL_c08` (c 0.8, 250 N each), `T6_TINY_c08` (c 0.8, 0.25 N each), `T6_FULL_c12` (1.2), `T6_FULL_c055` (0.55).

Body split by geometry (05-fea rule 5): `rp = hypot(x, z − 10)`. Pin: `rp ≤ 5.02 & |y| ≤ 25.01`. Block:
`rp ≥ 5.08 & |y| ≤ 15.01` plus everything with `|y| ≤ 15.01` outside the hole. Pads: `|y| > 25.01`. Guard: no node with
`5.02 < rp < 5.08` and `|y| < 15` (that is the gap); stop if any.

Reading, for each full solve:
- check 1: `r.reaction[2]` ≈ −500 (1 %); pad share: pad nodes' von Mises max x 4 mm² (bound) < 5 N.
- bearing zone: block nodes with `rp ≤ 5.4`, `z > 10`, `|y| ≤ 13`: max von Mises (`peak_contact_vm_mpa`, place →
  `block_peak_at_mm`) and min P3 (`s[:, 9]`, compressive) → compare −P3 with p0 6.8.
- mouths: same with `13 < |y| ≤ 15.01`, reported separately with `r.average(at, 0.5/1.0)` and node counts.
- ligament: block nodes `z > 19.9, |x| < 2, |y| < 10`: mean σx (`s[:, 1]`) vs 5.3.
- pin rise: mean `r.disp[pin_mask, 3]`.
- series: bearing-zone vm and −P3 over c = 1.2, 0.8, 0.55; last step under 5 %.

Contact proof (05-fea "body with clearance on both sides", the pin has 0.1 all round): TINY rise should be ≈ 0.100 mm
(the gap, as a rigid body). A bond would give the full-load elastic rise / 1000 ≈ 1e-5 mm. FULL rise ≈ 0.11–0.12. So
`rise_tiny / rise_full ≈ 0.85`, not 0.001: the response is not proportional, which only contact gives.

## 5. Decisions

- Pin held by two soft pads on its end faces with their outer faces fixed (05-fea rule 2: pads on the loose body, clear
  of the other body). Why: the pin must be held when the contact is open, and pads there cannot disturb the hole.
- The pin is modelled centred with the real 0.1 mm gap (rule 3: not line-to-line), as the task states.
- Loads as rigid remote loads on the pin end faces: they act on the steel pin, not on the judged block, so the rigid
  link stiffens nothing that is judged.
- "Peak bearing stress" is reported two ways: −P3 at the hole top (contact pressure, compare with Hertz p0) and von
  Mises in the bearing zone (the key asks for vm). Mouth values reported apart.

## 6. Branches

- Static raises "contact iteration did not converge": the pin has nothing deciding where it goes. Different way 2:
  rebuild the pin seated, centre at Z 10.1 (touching the hole top along a line, gap 0.2 at the bottom), same pads, and
  solve again. Report that the seated model was used and why.
- Error 24 at once: a body is free. Check the material log (pads matched?), the pad fixture count (2 faces), and that
  the pads touch the pin end faces (pad box Y 25..27 against pin end Y 25). If all that is right, go to way 2
  (seated pin). Way 3, if way 2 also fails: answer by hand (Hertz above) plus a bonded twin of the seated model,
  marked `valid` false for contact, and hand up with the logs (06-judgment).
- Reaction off by > 1 %: the remote loads or the pads. Print `r.applied` (should be 500) and the pad share.
- Pin rise on FULL is ≈ 0.0 (< 0.05 mm): the pin is bonded to the block, not in contact. Check the contact pick (1 face
  each) and that it is `NO_PENETRATION`.
- Pin rise ≫ 0.15 mm or metres: the contact never closed; the pads alone hold it. Check the material log and the
  contact set; then way 2 (seated pin).
- Excessive-displacement answer No and the reaction still −500 within 1 %: fine, record it.
- −P3 at the hole top far from 5–9 MPa: check the mask is the block, top half; check c gives ≥ 3 elements across the
  3.1 mm contact width (c ≤ 1.0). If the series has not settled, report the rows and "not shown".
- Bearing peak sits at a mouth and climbs: edge of contact at a free face; report it with averages, and the
  inside value as the bearing stress.
- Over 40 minutes at any point: stop, write exactly how far you got (which solves ran, their checks), mark
  `valid` false with the reason.
- Anything else: stop T6, record, go on.

## 7. Done and results

07-done study items 1, 4 (vm 45, layers: block printed base-down, report `layer_stress((0,0,1))` on block nodes), 6,
7 (load path: pin ends → pin → top of the hole → ligament above the hole → side walls in tension → bottom face), 8
(contact proof, pad share, contact force = reaction).

`results.json` T6: `hand_bearing_mpa` 1.67 (and Hertz p0 6.8 in notes), `nodes`, `solver` ("direct sparse via macro,
read back 7 = Intel direct sparse"), `how_pin_was_stabilised` ("two 2x2x2 mm pads E 0.5 MPa on the pin end faces,
outer faces fixed; share x N"), `peak_contact_vm_mpa`, `block_peak_at_mm`, `pin_rise_mm`, `reaction_n`, `valid`, `why`,
`status`, `notes`.
