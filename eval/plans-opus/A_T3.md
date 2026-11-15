# A_T3: static study of the T1 bracket, with a verdict

## 1. Restatement

`bracket.SLDPRT`, screwed down through its four base holes, a motor pulling the bore with 150 N along +X, printed base
on the bed (layers stacked along Z). Requirement: factor ≥ 2.0 on von Mises against 45 MPa and on tension across
layers against 22.5 MPa. Run the study and every check, and give a verdict.

Checklist:
- [ ] hand numbers written in the log before the first solve (section 2)
- [ ] support 1 (hole walls fixed) with load model B, converged over 3 sizes on vm, layer tension and layer shear
- [ ] support 2 (bottom face fixed) with load model B, one size, compared
- [ ] load model A (remote on the motor-screw holes), one size, compared; report the higher
- [ ] five checks with numbers; plateau near the fixed holes at 1, 2, 3, 5 mm
- [ ] three measures with place and factor; print-direction table (Z, Y, X layers)
- [ ] verdict, thinnest margin, cheapest improvement, what was not checked
- [ ] nodal results saved as `.npz` beside the model

## 2. Hand numbers

Section of upright and base: 50 wide x 6 thick, I = 50·6³/12 = 900 mm⁴, Z = 300 mm³. E = 1900 MPa, EI = 1.71e6 N·mm².

| Quantity | Working | Value | Accept |
| --- | --- | --- | --- |
| Upright root stress (Z 6, X 0 face, tension, across layers) | M = 150 x (28 − 6) = 3300 N·mm; σ = 3300/300 | **11.0 MPa** (`hand_root_stress_mpa`) | – |
| Plain-section check point (X 0, Y 3..8, Z 12) | M = 150 x (28 − 12) = 2400; σz = 2400/300 | **+8.0 MPa** σz | ±15 % |
| Base between upright and holes, bottom face (X 15, Y 25, Z 0), in layer plane | M = 150 x (28 − 3) = 3750; 3750/300 + 150/300 | 13.0 MPa σx | ±25 % (holes fixed nearby) |
| Lower motor-screw holes Ø3.4 (Z 17.04), nominal | M ≈ 150 x 10.96 = 1644 (model A) / 1747 (model B); /300 | 5.5–5.8 MPa | – |
| same, hole edge, x3 for a small hole (05-fea) | | **16.4–17.5 MPa across layers** | 12–21 MPa |
| Shear across layers (upright, mean / peak) | 150/300, x1.5, x3 at holes | 0.5 / 0.75 / ~2–3 MPa | below 6 |
| Reaction | equal and opposite to the load | (−150, 0, 0) N | 1 % |
| Max displacement, support 1 (top of upright) | base rotates: θ = 3750 x 22/1.71e6 = 0.048 rad → 0.048 x 43 = 2.07 mm; upright bending to top 0.69 mm | **~2.7 mm** | 0.9–8 mm (x3) |
| Max displacement, support 2 | upright bending only, plus some base | ~0.8 mm | 0.3–2.4 mm |
| Nodes, el 2.0 + controls | 12 x 32 974 / 8 = 49 461, x1.5 for controls | **74 000** | 37 000–148 000 |

Where the peaks should be: layer tension and von Mises at the **lower Ø3.4 holes, on the X 0 face**, at the hole
sides (Y 14.04 ± 1.7 or 35.96 ± 1.7, Z ≈ 17). Bending closes the L, so the X 0 face is in tension and the R4 fillet is
in compression. Expected: sf_layer ≈ 22.5/16.5 ≈ 1.4 → **fail** on layers; sf_yield ≈ 45/16.5 ≈ 2.7 → pass.
This bracket is the one in 05-fea.md ("rigid load lends stiffness"): 15.4–16.0 MPa across layers was measured with an
even load; a rigid load on the bore read 10.4 and passed it wrongly. So do not use a rigid load on the bore.

## 3. Build

None. Open `bracket.SLDPRT`; check `volume(d)` = 32 974.0 ±0.1 % before anything else.

## 4. Study

**Material:** `PETG`.

**Load model B (primary): even pull on the upright's inner face.** `('normal', inner, -150.0)` with
`inner = pick(d, kind='plane', normal=(1, 0, 0), at=(6, 25, 44))` → 1 face (area ≈ 1 373 mm²). Negative = pulls the
face toward +X. Why: the helpers have no directional force on a face (gap, see 6); a uniform traction on this face has
its resultant at Z ≈ 28 (face Z 10..46 and its holes are symmetric about Z 28), so the moment at the root is the same
as the motor's, and it stiffens nothing.

**Load model A (second way, 07-done item 3):** `('remote', screws, (3.0, 25.0, 28.0), (150.0, 0, 0), (0, 0, 0))` with
`screws = pick(d, kind='cyl', r=1.7)` → 4 faces: the motor screws are where a motor really pulls. It is rigid, so it
may read low at those holes; report the higher of A and B.

**Clear the load mask** (README) after each `static()`: `r.loaded_pts = None`. Why: with model B the load face is the
whole inner face and `away()` would hide the whole 6 mm upright; with model A it would hide the screw holes, which is
where the peak is (05-fea.md "The default mask can hide exactly that").

**Support 1:** `('fixed', pick(d, kind='cyl', r=2.75))` → 4 faces. Singular at the hole mouths: judge outside 6 mm
(the converge distance) and report the plateau (step 4).
**Support 2 (07-done item 2):** `('fixed', pick(d, kind='plane', at=(40, 25, 0)))` → 1 face, the whole bottom face.
It is too stiff for the base (stops it lifting at X 0) and is a bound; the upright holes are far from both supports
and their numbers must agree between the two.

**Mesh:** `el` global, controls on the four Ø3.4 holes and the R4 fillet face, scaled with el:
```python
def run(el, fix='holes', load='B', loose=False):
    d.ForceRebuild3(False)                               # then pick again: faces go stale
    holes = pick(d, kind='cyl', r=1.7); fil = pick(d, kind='cyl', r=4.0)
    assert len(holes) == 4 and len(fil) == 1
    fx = pick(d, kind='cyl', r=2.75) if fix == 'holes' else pick(d, kind='plane', at=(40, 25, 0))
    if load == 'B':
        ld = [('normal', pick(d, kind='plane', normal=(1, 0, 0), at=(6, 25, 44)), -150.0)]
    else:
        ld = [('remote', holes, (3.0, 25.0, 28.0), (150.0, 0, 0), (0, 0, 0))]
    r = static(j, d, f'T3_{fix}_{load}_{el}'.replace('.', 'p'), PETG, fixtures=[('fixed', fx)], loads=ld,
               el=el, ctrl=[(holes, 0.3 * el), (fil, 0.4 * el)], loose_ok=loose)
    r.loaded_pts = None
    np.savez(W / f'T3_{fix}_{load}_{el}.npz', pos=r.pos, s=r.s, disp=r.disp, reaction=r.reaction)
    log(r.summary())
    return r
```
Expected nodes: el 3.0 ≈ 22 000, el 2.0 ≈ 74 000, el 1.5 ≈ 176 000.

**Job 1 (four studies):**
1. `rows, ok = converge(lambda el: run(el), (3.0, 2.0, 1.5), layers=(0, 0, 1))`. Keep the last Result: wrap `run` so
   it stores `last = r`.
2. Five checks on the el 1.5 result (05-fea.md table): reaction; `max_disp()` vs 2.7; plain-section σz: nodes
   `r.near([(0, y, 12) for y in (3, 4, 5, 6, 7, 8)], 0.6)`, mean of `r.s[mask, 3]` vs +8.0; base check
   `r.near([(15, 25, 0)], 1.0)` mean `r.s[:, 1]` vs 13.0; peak away and `r.vm.max()`; convergence rows.
3. Plateau near the fixed holes: `r.peak(r.away(dist=x))` for x in (1, 2, 3, 5); write all four with places.
4. Small holes read directly: `m = r.in_box([-0.1, 10, 13, 6.1, 40, 21])`; `r.peak(m)`, `r.layer_stress((0,0,1), m)`,
   `r.layer_shear((0,0,1), m)`; and `r.average(at, 0.5 / 1.0 / 2.0)` at the layer peak place with node counts.
5. `run(2.0, fix='bottom')`: compare the box-4 numbers with the el 2.0 row of the series (accept within 5 %).

**Job 2:** `run(2.0, load='A')` and `run(1.5, load='A')`: compare box-4 numbers with model B at the same sizes.

**Print-direction table** from the el 1.5 model-B result (and A, same rows): for normals (0,0,1) base on bed,
(0,1,0) on its side (Y 0 face on bed), (1,0,0) on its back (X 0 face on bed): `layer_stress`, `layer_shear`, factors
22.5/σ and 13/τ, plus the von Mises factor (same for all). Expected: Z ≈ 16 MPa (1.4), Y ≈ 5–6 MPa (≈ 4),
X ≈ 13 MPa from base bending (≈ 1.7).

Three measures: von Mises vs 45 (`sf_yield`), tension across Z layers vs 22.5 (`sf_layer`), shear between Z layers
vs 13; each with its place, from the governing (higher) load model.

## 5. Decisions

- Load models: B primary (even, on the face that carries the motor flange), A second (screw holes). A rigid load on
  the bore is not used (05-fea.md shows it hides the failure). Report the higher stress.
- Verdict rule: fail if sf_yield < 2 or sf_layer < 2 in either load model, on converged numbers. If a measure did
  not converge (> 5 % at the last step), the verdict on it is "not shown", not pass.
- Layer shear is not in the requirement but is reported (07-done item 4).
- T3 does not change the design; T5 does.

## 6. Branches

- `static()` raises "excessive displacements" on el 1.5 (expected possibility, 05-fea rule 8: 2.7 mm on a 46 mm
  bracket): check one body and that the el 2.0 reaction was −150 within 1 %; then call `run(1.5, loose=True)` and use
  it (converge cannot pass loose: run the three sizes by hand with `run()` and compare rows yourself, 5 % rule on
  vm, layer and shear).
- Nodes at el 1.5 over 200 000: use 1.75 instead of 1.5 (controls 0.525, 0.7); say so.
- Nodes more than 2x off the expected number at el 2.0, or displacement more than 3x off 2.7 mm: stop, do not read
  stresses; read the fixture box `static()` logs (must be X 22–68, Y 7–43, Z 0–6) and the pick counts.
- Reaction not (−150, 0, 0) within 1 %: the load is not what you meant. For B: sign or wrong face (print
  `face_info` of `inner`; normal must be (1, 0, 0), box X 6). Fix and rerun; never report the stresses of that run.
- Plain-section σz off by more than 15 %: check you read σz (column 3) of X 0 surface nodes; if right and still off,
  write both and say "not explained" for that check (06-judgment: then spend 10 minutes on the cause).
- Layer peak outside 12–21 MPa at the lower holes: if lower, check the load mask was cleared (`r.loaded_pts is None`)
  and that the in_box (step 4) read the holes; if far higher (> 25) and climbing with refinement at one spot, name the
  spot: a hole mouth edge is real geometry (no fillet in the spec), report averages at 0.5/1/2 mm and the climb.
- Peak on the R4 fillet: should be compression-driven von Mises only (~11 x Kt 1.3 ≈ 14). Report it; it is a real
  feature, not excluded.
- Peak lies at a base hole even outside 6 mm and rises with refinement: it is the fixture; read the plateau (step 3),
  support 2 numbers, and judge the part outside the plateau distance; say how large the excluded value was.
- Error 24 at once: empty fixture? (`static` refuses empty lists) — print the pick count; else a fresh `job()`.
- Not converged after (3.0, 2.0, 1.5): one more size in a new job (1.25 global, controls 0.375) only if under 200 000
  nodes; otherwise report "not shown" for that measure with the rows.
- Anything else: stop T3, record, go on (T4 and T6 do not depend on T3's numbers).

## 7. Done and results

07-done "A study is done when" items 1–7 (no contact): five checks, second support, second load, three measures,
direction table, convergence on all three, the load path sentence ("the motor pull bends the upright about Y; the
moment goes through the upright root into the base, which bends between the upright and the X 25 screws, and
leaves through the four screw-hole walls"). Then "It passes is not the end": thinnest margin (layer at the lower
screw holes), cheapest improvement (print on its side: expected layer factor ≈ 4 at no mass, from the table), not
checked (screw preload, bed contact under the base, the motor's real flange contact).

`results.json` T3: `hand_root_stress_mpa` 11.0, `el_mm` (finest), `nodes`, `peak_vm_mpa`, `peak_at_mm`,
`layer_stress_mpa`, `sf_yield`, `sf_layer`, `max_disp_mm`, `reaction_n` (4 numbers), `converged`,
`convergence_rows`, `verdict` ("fail" expected), `status`, `notes` (load models, masks, plateau, support 2).
