# A / T5. Make it pass

Playbook: 07-done.md "'It passes' is not the end" (the order of changes: print direction, a radius at the peak,
material where the stress is, a different load path), 05-fea.md paragraph "Report the layer direction too".
Needs T3's `t3_rows.json` and `t3lib.py`.

## 1. Restatement

If the T3 bracket fails, change the design so that it has a factor of 2.0, and show it with a study. Hole positions,
the bore and the outer footprint (X 0..80, Y 0..50, Z 0..46) are fixed; mass may grow at most 10 %
(39.24 g → at most 43.16 g, that is +3297 mm³). How it is printed is open. Save `bracket_c.SLDPRT`.

- [ ] the change, in one sentence, cheapest that works
- [ ] `bracket_c.SLDPRT` saved; mass and growth
- [ ] a study on `bracket_c` showing factor ≥ 2.0 on all three measures, in the chosen print direction, converged
- [ ] holes, bore and footprint unchanged (measured)
- [ ] keys: `change`, `mass_g`, `mass_growth_pct`, `sf_yield`, `sf_layer`, `print_orientation`, `verdict`

## 2. Hand reasoning

T3 fails on tension **across** layers stacked along Z: the upright bends, so its bending stress σz (about 16 MPa at the
lower motor-hole rims) pulls the layers apart; the allowable there is 22.5 MPa. The same stress **in** the layer plane is
judged against 45 MPa: 45 / 16 = 2.8.

Print the bracket on its side (face Y 0 on the bed, layers stacked along Y): both the upright's σz and the base's σx
then lie in the layer plane. What crosses the layers is σy, which a bracket bent about the Y axis hardly has.

| Layers along | Tension across layers, hand | Factor | Note |
| --- | --- | --- | --- |
| Z (T3) | σz 16.4 at the motor holes | 1.4 | fails |
| X | σx: base bending 12.5 nominal, more near the base holes | about 1.5 | fails |
| **Y** | σy: Poisson and hole effects only, guess 4 to 9 MPa (the playbook quotes 4.9 for a rigid load) | **2.5 to 5** | expected to pass |

Von Mises does not depend on print direction: 45 / (16 to 22) = 2.0 to 2.8. **This is the thin one.** Shear between
Y layers: guess 3 to 6 MPa, factor 2.2 to 4. Confidence that the side print alone passes all three: medium (about
65 %); the fallback in section 5 covers the rest.

## 3. Step 1: read T3's results for every print direction (no solve)

```python
from t3lib import *
rows = json.loads((HERE / 't3_rows.json').read_text(encoding='utf-8'))
series = [rows[n] for n in ('T3_PADS_30', 'T3_PADS_22', 'T3_PADS_16')]
for k in 'XYZ':
    t = [s['table'][k] for s in series]
    log(k, 'finest', t[-1], 'sf_min', sf_min(t[-1]), 'converged', settled(t))
log('washers model', {k: sf_min(rows['T3_WASHERS']['table'][k]) for k in 'XYZ'})
```

Decide:

- **Y passes** (finest row: `sf_yield`, `sf_layer`, `sf_shear` all ≥ 2.0, and `settled` is True for Y): go to
  step 2a. No geometry change.
- **Y fails on layer tension or shear only**, or **fails on von Mises with the peak on the upright or at the motor
  holes**: go to step 2b (ribs).
- **Y fails on von Mises with the peak on the base within 5 mm of a fixed hole**: that value belongs to the
  fixed-hole-wall idealisation. Read `rows['T3_WASHERS']['table']['Y']` (the second support). If that passes, go to
  2a and say which support model the verdict rests on and what the other gave. If it fails too, go to 2b.
- **Y passes but is not converged:** go to 2a, run the confirming study at el 1.6, and if the last step still
  moves more than 5 %, verdict "not shown" in notes, `verdict` = "fail".

## 4. Step 2a: same geometry, printed on its side (expected path)

```python
with job() as j:
    j.simulation()
    d = open_doc(j.sw, WIP / 'bracket.SLDPRT')
    save_as(d, WIP / 'bracket_c.SLDPRT')
    expect('same solid', volume(d), hand_volume(), 0.001)
    must('base holes', len(holes(d, 2.75)), 4); must('bore', len(holes(d, 11.0)), 1); must('motor holes', len(holes(d, 1.7)), 4)
    for got, want in zip(bbox(d), (0, 0, 0, 80, 50, 46)):
        expect('footprint', got, want, 0.01)
    export(j.sw, d, WIP / 'bracket_c.stl'); check_export(d, WIP / 'bracket_c.stl')
    vol = volume(d); close(j.sw, d)
    make_twin(j, WIP / 'bracket_c.SLDPRT', WIP / 'bracket_c_ld.SLDPRT')
    d = open_doc(j.sw, WIP / 'bracket_c_ld.SLDPRT')
    predict('T5_C_16', 145000, 2.5, 'von Mises at a lower motor-hole rim or on the base by the X 25 holes; sigma-y small everywhere')
    r = run(j, d, 'T5_C_16', 1.6, 0.55)               # the finest size T3 used; use T3's replacement size if 1.6 was refused
    compare('T5_C_16', r, 145000, 2.5)
    c = row(r); log(json.dumps(c, default=float))
    close(j.sw, d)
y = c['table']['Y']
put('T5', change='No change of shape: printed on its side (face Y 0 on the bed, layers stacked along Y), so the bending '
    'stress of upright and base lies in the layer plane instead of across it.',
    mass_g=vol * DENS_G_MM3, mass_growth_pct=0.0, sf_yield=y['sf_yield'], sf_layer=y['sf_layer'],
    print_orientation='on its side: face Y 0 on the bed, layers stacked along Y',
    verdict='pass' if sf_min(y) >= 2.0 else 'fail', status='done', notes=f"sf_shear {y['sf_shear']}; convergence from T3 series, same solid")
```

The study on `bracket_c` must repeat T3_PADS_16 within 2 % (same solid, same mesh settings): that is the check that
it is the same part. Convergence is T3's series read for direction Y.

Report with it (07-done.md): the thinnest margin (which of the three, its factor, and that a load 20 % higher or a
print in Z would eat it); the cheapest improvement beyond this (none needed; a 0.5 mm chamfer on the motor-hole
mouths would lower the rim stress, sized by hand, not run); printing notes: 80 × 46 mm footprint on the bed, 50 mm
tall, bore axis horizontal (a Ø22 circle prints without support), base holes horizontal, no supports.

## 5. Step 2b: fallback, two ribs (only if step 1 sends you here)

Two triangular ribs inside the L at the two Y edges, clear of every hole and of the motor: thickness 3.5 mm
(Y 0..3.5 and Y 46.5..50), legs 28 mm (along the base top from X 6 to 34, up the upright from Z 6 to 34).

- Volume each: ½ · 28 · 28 · 3.5 − (1 − π/4) · 4² · 3.5 (the fillet already there) = 1372.00 − 12.02 = **1359.98 mm³**.
- Part: 32974.02 + 2719.96 = **35693.98 mm³**, **42.48 g**, growth **8.25 %** (limit 10 %).
- Clearances: rib inner face Y 3.5 to the Ø10 screw-head circle of the base hole at (25, 10): 5 − 3.5 = 1.5 mm;
  motor holes start at Y 12.3; rib top Z 34 is below the R5 rounds (Z 41).
- Why it works: at Z 17 each rib is 17 mm deep in X, so the upright there is a T-section, not a 6 mm plate; the
  bending stress at the motor holes falls several-fold. Hand value: not computed to better than "at least halved".

```python
def add_ribs(d, t=3.5, leg=28.0):
    for name, y0 in (('RIB_A', 0.0), ('RIB_B', 50.0 - t)):
        ym = y0 + t / 2
        with Sk(d, plane(d, 'Y', ym, name + '_P'), name) as s:      # corner drawn 3 mm inside the body so it merges for certain
            s.poly([(3, ym, 3), (9 + leg, ym, 3), (3, ym, 9 + leg)])
        extrude(d, s.feat, name, t, mode=MID, expect_dv=0.5 * leg * leg * t - Q * 16 * t)
    single_body(d); must('rebuild errors', len(feature_errors(d)), 0); save(d)
```

Build `bracket_c` with `d = build_bracket(j, WIP / 'bracket_c.SLDPRT'); add_ribs(d)`, check volume 35693.98 (0.1 %),
box, the nine holes as in T1, export, `make_twin`, then three studies `T5_RIB_30/22/16` with `run(...)` exactly as
T3's pads series (same sizes, predictions 24,000 / 61,000 / 157,000 nodes, displacement 0.8 mm: stiffer). Read
`row(r)['table']['Y']` for each; pass needs all three factors ≥ 2.0 and `settled`. Print direction stays Y (the ribs
then lie in the layer plane; the upper rib starts in mid-air and needs support under it: say so).
`change` = "Two 3.5 mm ribs between upright and base at the Y edges, and printed on its side".

If the ribs do not reach 2.0 either: state is "not possible within 10 % mass", with the numbers of both attempts and
the nearest thing that works; `verdict` = "fail". Do not try a third geometry unless time is left after set D.

## 6. Branches

| You see | It means | Do |
| --- | --- | --- |
| T3's verdict was "pass" | T5's condition is not met | `change` = "none needed", copy T3's factors, still do step 1 and report the best print direction and by how much |
| `t3_rows.json` missing or without the three pads rows | T3 did not finish | run T3's job 1 first; if it cannot run, T5 is blocked: report |
| `T5_C_16` differs from `T3_PADS_16` by more than 2 % | not the same solid or not the same picks | compare the bracket body's volume in the two twins (`bodies(d)`) and the fixture and load boxes `static()` logged |
| ribs: `extrude` raises on `expect_dv` | the triangle is not where planned | print the three points; legs must end at x 34 and z 34 on the body surface |
| ribs: bodies is 2 or 3 | a rib did not merge | it should (the corner is inside the body); `bodies(d)`, stop and report if it persists |
| ribs: the peak moves to the rib tip on the base or upright | the rib end is a stress raiser | report it with its factor; if under 2.0, lengthen the legs to 32 (growth 10.8 %: over the limit) is not allowed: report "not possible" with numbers |
| anything from T3's branch table | same cause | same cure |

Anything else: stop T5, write down exactly what was seen, carry on with T6.

## 7. Done checklist

- [ ] step 1's table for X, Y, Z (three measures, factors, converged or not) in REPORT.md
- [ ] which path was taken and why, in one sentence
- [ ] `bracket_c.SLDPRT`: volume, mass, growth %, footprint box, nine holes measured unchanged
- [ ] the study on `bracket_c`: five checks (`row['checks']`), three measures for layers along Y, convergence
- [ ] thinnest margin, cheapest further improvement, what was not checked (bed adhesion of an 80 × 46 face, hole
      roundness when printed with horizontal axes)
- [ ] `put('T5', ...)` as in step 2a (or the rib values); REPORT.md T5 with minutes
