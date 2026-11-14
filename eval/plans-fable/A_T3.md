# A / T3. Static study with a verdict

Playbook: 05-fea.md from the top to "Sizing the job" (every bullet of "One study" matters here), 07-done.md "Predict,
then run" and "A study is done when". This bracket is the one 05-fea.md keeps quoting ("the benchmark bracket").

## 1. Restatement

The T1 bracket is screwed down through its four base holes; a motor in the bore pulls 150 N along +X; layers are stacked
along Z. Decide whether it has a factor of 2.0 on von Mises (45 MPa) and on tension across the layers (22.5 MPa), with
the playbook's checks. Expected verdict, from the hand values below: **fail**, on tension across layers at the two
lower motor-screw holes (factor about 1.4).

- [ ] hand values written before the first solve
- [ ] five checks of 05-fea.md with numbers
- [ ] load tried two ways (rigid on the bore; even pressure where the motor screws bear), higher one reported
- [ ] support tried two ways (hole walls fixed; washers fixed)
- [ ] three measures, each with place and factor; print-direction table (X, Y, Z) from the same result
- [ ] convergence series of three sizes on the governing measure
- [ ] keys: `hand_root_stress_mpa`, `el_mm`, `nodes`, `peak_vm_mpa`, `peak_at_mm`, `layer_stress_mpa`, `sf_yield`,
      `sf_layer`, `max_disp_mm`, `reaction_n`, `converged`, `convergence_rows`, `verdict`

## 2. Hand calculation

Load path: 150 N +X at Z 28 on the upright (a 50 × 6 wall standing on the base) → bending of the upright about Y →
through the corner into the base → bending of the base → the four screws. The L closes: the outside (back face X 0,
bottom face Z 0) is in tension, the inside corner and its fillet are in compression.

| Quantity | Working | Value | Accept |
| --- | --- | --- | --- |
| section modulus, upright and base | 50 · 6² / 6 | 300 mm³ | |
| **root stress** (key `hand_root_stress_mpa`) | 150 · (28 − 6) / 300, at Z 6 | **11.0 MPa** (σz, across layers) | |
| same at the fillet's top, Z 10 | 150 · 18 / 300 | 9.0 MPa | |
| back face at Z 12 (check 3) | 150 · 16 / 300, mean σz over the width at X 0 | +8.0 MPa | 6.8 to 9.2 |
| nominal at the lower motor holes, Z 17.04 | 150 · 10.96 / 300 | 5.48 MPa | |
| **rim of the lower motor holes**, back face | 5.48 · 3 (05-fea.md: nominal times 3 for a small hole) | **16.4 MPa** σz; the playbook measured 15.4 to 16.0 | 12 to 20 |
| base bottom face between X 12 and 18 (check 3) | 150 · (28 − 3) / 300 − 150/300 | +12.0 MPa σx (in the layer plane) | 10.2 to 13.8 |
| tip displacement | upright: 150·22³/(3·1900·900) = 0.31 mm, slope 0.0212 · 18 = 0.38; base rotation 3750·19/(1900·900) = 0.042 rad · 43 = 1.79 | **2.5 mm** at Z 46, +X (playbook: 2.7) | 0.9 to 8 |
| reaction | | Fx = −150 N, Fy = Fz = 0, resultant 150 | ±1.5 N |
| factor across layers, layers along Z | 22.5 / 16.4 | **1.37 → fail** (limit stress 11.25 MPa) | |
| factor on yield | 45 / (16 to 22) | 2.0 to 2.8, expected to pass narrowly | |
| shear between layers | 1.5 · 150 / 300 = 0.75 nominal, a few MPa at rims | factor over 2.5 | |

Nodes: 12 · 32974 / el³, times 1.5 for the local controls: **22,000** at el 3.0, **56,000** at el 2.2,
**145,000** at el 1.6. Confidence in these three: low (controls dominate); a factor of 2 either way is normal.

## 3. The models

No change to `bracket.SLDPRT`. Two twin files add small separate bodies so that a load and a support can sit on part
of a face (05-fea.md "A load on part of a face": separate touching bodies bond):

- `bracket_ld.SLDPRT` = bracket + four **pressure pads**: discs Ø7 × 1 mm on the back face (X −1 to 0) over the four
  motor holes, material `PRESS` (50 MPa modulus, 2.6 % of PETG). They stand for the heads of the motor screws.
- `bracket_ld_w.SLDPRT` = the same + four **steel washers**: discs Ø10 × 1 mm on the base top (Z 6 to 7) over the
  four base holes. They stand for the heads of the base screws.

The twin is the same part: the bracket body in it must have the T1 volume to 0.01 %.

`t3lib.py` (also used by T4 and T5):

```python
from bracket import *

def make_disc(j, path, axis, centre, r, lo, hi, feat):
    """A solid disc along model axis 'X' or 'Z' from lo to hi; centre = the other two coordinates in x, y, z order."""
    d = new_part(j.sw, path)
    mid = (lo + hi) / 2
    c = (mid, centre[0], centre[1]) if axis == 'X' else (centre[0], centre[1], mid)
    with Sk(d, plane(d, axis, mid, feat + '_P'), feat) as s:
        s.circle(c, r)
    extrude(d, s.feat, feat, hi - lo, mode=MID, expect_dv=math.pi * r * r * (hi - lo))
    save(d); close(j.sw, d)

def make_parts(j):
    for k, (y, z) in enumerate(MOTOR_YZ):
        make_disc(j, WIP / f'pad_{k + 1}.SLDPRT', 'X', (y, z), 3.5, -1.0, 0.0, 'PRESSPAD')     # 38.48 mm3 each
    for k, (x, y) in enumerate(BASE_XY):
        make_disc(j, WIP / f'washer_{k + 1}.SLDPRT', 'Z', (x, y), 5.0, 6.0, 7.0, 'WASHER')    # 78.54 mm3 each

def make_twin(j, src, dst, washers=False):
    d = open_doc(j.sw, src)
    v = volume(d)
    save_as(d, dst)
    for k in range(4):
        insert_body(d, WIP / f'pad_{k + 1}.SLDPRT')
    if washers:
        for k in range(4):
            insert_body(d, WIP / f'washer_{k + 1}.SLDPRT')
    bs = bodies(d); log(bs)
    must('bodies in ' + Path(dst).name, len(bs), 9 if washers else 5)
    expect('bracket body is the same part', max(b[1] for b in bs), v, 0.0001)
    save(d); close(j.sw, d)

def run(j, d, name, el, c, load='pads', fix='walls', root=4.0, root_c=None):
    """One study. load 'pads' (150 N even pressure on the four pads) or 'remote' (rigid, on the bore).
    fix 'walls' (base hole walls) or 'washers' (washer tops). root: the corner fillet radius, or None for the sharp
    corner, whose edge then gets the control root_c."""
    d.ForceRebuild3(False)
    walls = pick(d, kind='cyl', r=2.75); must('base hole walls', len(walls), 4)
    bore = pick(d, kind='cyl', r=11.0); must('bore', len(bore), 1)
    mh = pick(d, kind='cyl', r=1.7); must('motor holes', len(mh), 4)
    pads = pick(d, kind='plane', normal=(-1, 0, 0), inside=[-1.01, -1, -1, -0.99, 51, 47]); must('pad outer faces', len(pads), 4)
    if root:
        rf = pick(d, kind='cyl', r=root, inside=[5.9, -0.1, 5.9, 6.1 + root, 50.1, 6.1 + root]); must('root fillet', len(rf), 1)
    else:
        rf = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01); must('root edge', len(rf), 1)
    mats = {'pad_': PRESS}
    if fix == 'washers':
        tops = pick(d, kind='plane', normal=(0, 0, 1), inside=[19, 4, 6.99, 71, 46, 7.01]); must('washer tops', len(tops), 4)
        fixtures, mats = [('fixed', tops)], {'pad_': PRESS, 'washer_': STEEL}
    else:
        fixtures = [('fixed', walls)]
    loads = ([('normal', pads, 150.0)] if load == 'pads' else
             [('remote', bore, (3.0, 25.0, 28.0), (150.0, 0, 0), (0, 0, 0))])
    r = static(j, d, name, PETG, fixtures, loads, el=el, ctrl=[(mh + bore, c), (rf, root_c or c)], materials=mats,
               loose_ok=True, max_nodes=200_000)
    save_npz(r, name)
    return r

# ---- reading a result ------------------------------------------------------------------------------------------------
def body_mask(r):
    """Bracket nodes only: pads are at x < 0, washers at z > 6 over the base (the bracket has nothing there beyond x 10)."""
    p = r.pos
    return (p[:, 0] > -1e-4) & ~((p[:, 2] > 6.0001) & (p[:, 0] > 15))

def clear_of_fix(r, D, rad=2.75):
    """Nodes at least D mm from the fixed base holes (rad 2.75) or from the washer rims (rad 5.0)."""
    p = r.pos
    dh = np.min([np.hypot(p[:, 0] - x, p[:, 1] - y) for x, y in BASE_XY], axis=0) - rad
    return (p[:, 2] > 6.0001) | (dh >= D)

def rim(r, which=MOTOR_YZ[:2], w=1.5):
    """Nodes within w mm of the walls of the two LOWER motor holes (z 17.04): where the hand value says it fails."""
    p = r.pos
    return body_mask(r) & (np.min([np.hypot(p[:, 1] - y, p[:, 2] - z) for y, z in which], axis=0) <= 1.7 + w)

def checks(r):
    p = r.pos
    back = (p[:, 0] > -1e-4) & (p[:, 0] < 0.05) & (np.abs(p[:, 2] - 12) < 0.5)
    bot = (np.abs(p[:, 2]) < 0.05) & (p[:, 0] > 12) & (p[:, 0] < 18)
    return dict(reaction=r.reaction, applied=r.applied, max_disp=r.max_disp(), excessive=bool(r.excessive),
                top_ux=float(r.disp[p[:, 2] > 45.9, 1].mean()),
                sz_back_z12=float(r.s[back, 3].mean()), sx_bottom_x15=float(r.s[bot, 1].mean()),
                nodes_in_checks=(int(back.sum()), int(bot.sum())))

def row(r, D=3.0, rad=2.75):
    """Everything T3, T4 and T5 report from one result."""
    bm = body_mask(r)
    m = bm & clear_of_fix(r, D, rad)
    z = measures(r, m, (0, 0, 1))
    return dict(study=r.name, el=r.el, nodes=r.nodes, D=D, table=direction_table(r, m),
                rim_layer_z=round(r.layer_stress((0, 0, 1), rim(r))[0], 2), rim_vm=round(r.peak(rim(r))[0], 2),
                vm_all=round(float(r.vm[bm].max()), 2),
                plateau={k: (round(r.peak(bm & clear_of_fix(r, k, rad))[0], 2),
                             round(r.layer_stress((0, 0, 1), bm & clear_of_fix(r, k, rad))[0], 2)) for k in (1, 2, 3, 5)},
                flat=[r.el, r.nodes, z['vm'], z['layer'], z['shear']], checks=checks(r))
```

## 4. The studies

Material PETG everywhere except the pads (`PRESS`) and washers (`STEEL`); `static()` logs each body's material: read it.

| Study | Model | Fixture | Load | el / control | Why |
| --- | --- | --- | --- | --- | --- |
| S1 `T3_REMOTE` | bracket_ld | four base hole walls, fixed | `'remote'` on the bore at (3, 25, 28), (150, 0, 0) | 2.2 / 0.75 | the task's words taken literally. Rigid: 05-fea.md says it hides the motor-hole rims (10.4 MPa there) |
| S2a,b,c `T3_PADS_30/22/16` | bracket_ld | hole walls | `'normal'`, 150 N on the four pad outer faces (pushes +X) | 3.0 / 1.0, 2.2 / 0.75, 1.6 / 0.55 | where a screwed-on motor really bears: its screw heads on the back face. The governing model and the convergence series |
| S3 `T3_WASHERS` | bracket_ld_w | four washer tops, fixed | as S2 | 2.2 / 0.75 | the second support (07-done.md study item 2) |

Controls: the four motor holes, the bore and the root fillet get the control size; it shrinks with the global size, so
the series is a real one (05-fea.md "Sizing the job").

`t3_job1.py` (four studies, the limit for one instance):

```python
from t3lib import *
with job() as j:
    j.simulation()                                    # before any document is opened (05-fea.md, "Order")
    make_parts(j)
    make_twin(j, WIP / 'bracket.SLDPRT', WIP / 'bracket_ld.SLDPRT')
    make_twin(j, WIP / 'bracket.SLDPRT', WIP / 'bracket_ld_w.SLDPRT', washers=True)
    d = open_doc(j.sw, WIP / 'bracket_ld.SLDPRT')
    rows = {}
    for name, el, c, load, nodes in (('T3_PADS_30', 3.0, 1.0, 'pads', 22000), ('T3_PADS_22', 2.2, 0.75, 'pads', 56000),
                                     ('T3_REMOTE', 2.2, 0.75, 'remote', 56000), ('T3_PADS_16', 1.6, 0.55, 'pads', 145000)):
        predict(name, nodes, 2.5, 'back face at the lower motor holes (y 14.04 / 35.96, z 17.04), layer tension about 16 MPa')
        r = run(j, d, name, el, c, load=load)
        ok = compare(name, r, nodes, 2.5)
        rows[name] = row(r); rows[name]['compare_ok'] = ok
        log(name, json.dumps(rows[name], default=float))
        (HERE / 't3_rows.json').write_text(json.dumps(rows, indent=1, default=float), encoding='utf-8')
    close(j.sw, d)
```

`t3_job2.py`: the same header, then `d = open_doc(j.sw, WIP / 'bracket_ld_w.SLDPRT')`,
`r = run(j, d, 'T3_WASHERS', 2.2, 0.75, load='pads', fix='washers')`, `row(r, D=3.0, rad=5.0)`, and add it to
`t3_rows.json` (read the file, add the key, write it back). T4's first three studies can go in this same job.

### Reading the results, in this order

1. **After T3_PADS_30 only** (the cheap one): `checks` must show reaction Fx −150 ± 1.5 with Fy, Fz within ± 1.5;
   `max_disp` between 0.9 and 8 mm with `top_ux` positive; `sz_back_z12` between 6.8 and 9.2; `sx_bottom_x15`
   between 10.2 and 13.8. Read the two boxes `static()` logged: fixture nodes inside X 22..68, Y 7..43, Z 0..6; load
   nodes at X −1, Y 10.5..39.5, Z 13.5..42.5. If any of these is wrong, go to Branches before the other solves.
2. Five checks (05-fea.md table) from T3_PADS_22: (1) reaction; (2) displacement against 2.5 mm; (3) the two plain
   sections; (4) the peak: `table['Z']['vm_at']` and `['layer_at']` must be nameable features (a lower motor-hole
   rim on the back face, or the base near the X 25 holes); `vm_all` is what the 3 mm exclusion left out; (5) the series.
3. Plateau (05-fea.md "How far to stand back"): `plateau` gives (vm, layer Z) outside 1, 2, 3 and 5 mm of the fixed
   holes. If the values at 2 and 3 mm agree within 10 %, D = 3 stands. If vm still falls by more than 10 % from 3 to
   5 mm, say so and report both.
4. Convergence: the three `flat` rows of T3_PADS_30, _22, _16 are `convergence_rows`.
   `converged = settled([rows[n]['table']['Z'] for n in the three])`.
5. Load two ways: `rim_layer_z` of T3_REMOTE against T3_PADS_22. Report both; the higher governs.
   Support two ways: `table['Z']` and `rim_layer_z` of T3_WASHERS against T3_PADS_22. The numbers that agree
   between them (the upright and the motor holes should, within 10 %) are the result; the base near the screws will
   differ, and that difference is reported, not judged.
6. Print-direction table: `rows['T3_PADS_16']['table']`, three directions × three measures. T5 uses it.
7. Verdict, from the finest pads row (`T3_PADS_16`), layers along Z:
   `layer_stress_mpa = max(table['Z']['layer'], rim_layer_z)`, `sf_layer = 22.5 / that`,
   `peak_vm_mpa = table['Z']['vm']`, `sf_yield = 45 / that`, plus `sf_shear` for the report.
   - any factor under 2.0 at **all three** sizes → `verdict = "fail"` (it does not need convergence to fail);
   - all factors at least 2.0 and `converged` → `"pass"`;
   - otherwise → do the branch "not converged" below; if it stays open, put `"fail"` if the finest row fails and say
     "not shown" in `notes` and REPORT.md (the key only allows pass or fail).

## 5. Decisions made for you

- **Load path:** the motor is screwed to the upright, so its pull enters at the four motor-screw holes, as pressure
  from the screw heads on the back face, not on the bore wall (05-fea.md: "for a screwed-on part, the screw holes or
  the rings under the heads, not the bore its boss sits in"). The rigid bore load is run once, as the second way.
- **Why soft pads and not a step or a boss:** a cut step would put a sharp corner on the tension face at the very spot
  being judged; a PETG boss would stiffen the rim. A pad 40 times softer than PETG passes pressure and adds nothing.
- **Helper gap:** `static()` has no force along an axis on a face (only `'normal'` and `'remote'`), and the playbook
  documents no raw call for one. So "150 N as an even force on the bore" cannot be applied as such; the pads are the
  fallback. Say this in the report.
- **Exclusion:** fixed hole walls are singular at the hole mouth (05-fea.md: 22.8 to 33.4 MPa on this bracket). Peaks
  are read at least 3 mm from them, and the excluded maximum (`vm_all`) is reported.
- `loose_ok=True` on every run: this bracket bends 2.7 mm and the solver then asks about excessive displacements
  (05-fea.md contact rule 8, last sentences). It is safe here only because step 1 above checks one PETG body,
  bonded pads, the reaction, and a displacement under 8 mm.
- The task names two measures; the playbook wants three. Report all three; the verdict uses all three.

## 6. Branches

| You see | It means | Do |
| --- | --- | --- |
| `static` raises "materials keys ['pad_'] match no body" | the body names are not `<file>-<feature>` | read the body names in the log lines just above; use a piece of the pad bodies' real name as the key (it must not occur in the bracket body's name) |
| `insert_body` raises | the disc did not come in as its own body | `bodies(d)`: if it merged, the disc file holds something else; rebuild that disc, check its volume |
| reaction Fx is +150 | the pads push −X | the pad faces picked are not the outer ones (X −1): print their boxes |
| reaction is 0 or far from 150 | the load went on nothing, or on the wrong faces | read the load box in the log; fix the pick; do not read stresses |
| `max_disp` over 8 mm, or `top_ux` negative | a pad came loose (bond lost) or the wrong problem was solved | 05-fea.md "Order" bullet: close, start a new job with `j.simulation()` first, rebuild, pick again. Second time: build the twin again. Third time: stop T3 |
| `sz_back_z12` or `sx_bottom_x15` outside its band, reaction right | the load is not where it should be, or the mesh is too coarse there | look at `nodes_in_checks` (under 20 nodes: use the next finer row). Still out by more than 20 %: stop, report both numbers, verdict "not shown" in notes |
| node count over twice or under half the prediction, everything else right | the planner's node estimate, not your model | go on; write both numbers in the report |
| mesh refused "over 200000" at el 1.6 | too fine for the cap | rerun that row at el 1.8, control 0.62, name `T3_PADS_18` |
| `rim_layer_z` between 11.25 and 20 at all sizes | as predicted | verdict fail, governing: tension across layers at the lower motor-hole rims |
| `rim_layer_z` under 11.25 with the pads, converged | the hand value (Kt 3) was too high for a plate in bending | check that `table['Z']['layer_at']` is not somewhere else and higher; then the verdict follows the study, and the report says the hand value was 16.4 and the study lower, with both numbers |
| the peak (vm or layer) is on the base within 5 mm of a fixed hole and falls steadily from D 1 to D 5 | fixture singularity, no plateau | judge the base from T3_WASHERS instead (rad 5.0, D 3) and say so; the upright values are unaffected |
| the peak is at the root fillet | not expected (compression side, about 11 to 13 MPa von Mises) | fine if under 22.5; report it |
| a measure moves more than 5 % between the last two rows | not converged | if it already fails at all three sizes: verdict fail. If it passes at the finest: one more row at el 1.8 / control 0.45 is not allowed to exceed 200,000 nodes; if the climb is at a hole mouth edge, that is a real edge: report "not shown" for that measure |
| solve fails with error 24 at once | 05-fea.md "When the solve fails" | check the fixture pick count and the body count; a new job; never change two things |
| error 24 after a minute, memory falling | out of memory | coarsen (el 2.0 instead of 1.6); report |
| the fifth study in one job fails | 05-fea.md: at most four per instance | new job |

Anything else: stop T3, write down exactly what was seen (log tail, `t3_rows.json`), carry on with T6 and set D;
T4 and T5 need T3's functions but not its verdict.

## 7. Done checklist

- [ ] hand table in REPORT.md before the results
- [ ] five checks with numbers; fixture and load boxes quoted
- [ ] S1 against S2 (load two ways) and S3 against S2 (support two ways), with the numbers
- [ ] three measures with place and factor; `vm_all` (excluded) and the plateau table
- [ ] print-direction table (X, Y, Z)
- [ ] three convergence rows; `converged`
- [ ] load path in one sentence (section 2, first paragraph)
- [ ] the thinnest margin and what eats it; the cheapest improvement (print it on its side: T5); what was not checked
      (preload of the base screws, the mounting surface under the base, fatigue)
- [ ] model SHA-256 (`sha(WIP / 'bracket_ld.SLDPRT')`), solver (automatic), npz files in `WIP/npz`
- [ ] `put('T3', hand_root_stress_mpa=11.0, el_mm=..., nodes=..., peak_vm_mpa=..., peak_at_mm=..., layer_stress_mpa=...,
      sf_yield=..., sf_layer=..., max_disp_mm=..., reaction_n=..., converged=..., convergence_rows=[...], verdict=...,
      status=..., notes=...)`; `reaction_n` is `checks['reaction'][3]`
