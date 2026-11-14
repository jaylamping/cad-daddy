# A / T4. The same study on a variant

Playbook: 05-fea.md "Is the result right?" (the paragraph on singularities under the table) and "Sizing the job" (edge
controls), 07-done.md study item 6. Needs `bracket.py` (T1) and `t3lib.py` (T3).

## 1. Restatement

Build `bracket_sharp.SLDPRT`: the T1 bracket with no fillet in the inside corner. Run the T3 load case on it. Say what
the stress in the inside corner is, how that was judged, and whether the part meets the factor of 2.0.
The trap: the corner is now a sharp inside edge, so its stress climbs for ever as the mesh shrinks. The last number of
a climbing series is not a stress and must not be reported as one.

- [ ] `bracket_sharp.SLDPRT` built from `build_bracket(..., root_r=None)`, volume checked
- [ ] a refinement series at the corner that shows whether it converges (`convergence_rows`, `converged`)
- [ ] the corner judged in a way that does converge (`reported_stress_mpa`, `how_judged`)
- [ ] `verdict` for the whole part, three measures

## 2. Hand calculation

| Quantity | Working | Value |
| --- | --- | --- |
| volume, sharp | 32974.02 − 171.68 | **32802.34 mm³** (39.03 g) |
| volume, R0.4 corner | 32802.34 + (1 − π/4) · 0.4² · 50 | **32804.06 mm³** |
| nominal bending at the corner | 150 · 22 / 300 (T3) | 11.0 MPa, **compressive** (inside of the L) |
| sharp corner, elastic | theory: unbounded | climbs with every refinement; expect steps of 15 to 40 % |
| R0.4 corner | 11.0 · Kt, Kt about 2.2 for r/t = 0.07 | **about 24 MPa von Mises** (accept 18 to 32); factor on yield about 1.9 |
| tension across layers at the corner | none: the corner is in compression | the layer measure stays at the motor holes, about 16 MPa, as in T3 |
| displacement, reaction | as T3 | 2.5 mm; Fx −150 N |

Expected verdict: **fail**, twice over: tension across layers at the lower motor holes (factor about 1.4, unchanged
from T3) and von Mises at the as-printed corner (factor about 1.9). Confidence in the second: medium (Kt is an estimate;
the playbook's 07-done.md quotes 1.88 for this case).

Nodes: global size fixed at 2.2 (about 56,000 as in T3); the corner control adds roughly 5,000 / 15,000 / 45,000 for
the sharp edge at 1.0 / 0.5 / 0.25, and 15,000 / 30,000 / 70,000 for the R0.4 face at 0.3 / 0.2 / 0.13.

## 3. The build

```python
from t3lib import *
with job() as j:
    j.simulation()
    for name, rr in (('bracket_sharp', None), ('bracket_r04', 0.4)):
        d = build_bracket(j, WIP / f'{name}.SLDPRT', root_r=rr)
        expect(name + ' volume', volume(d), hand_volume(rr), 0.001)
        for got, want in zip(bbox(d), (0, 0, 0, 80, 50, 46)):
            expect('box', got, want, 0.01)
        if rr is None:
            must('no fillet face', len(pick(d, kind='cyl', r=4.0)), 0)
            export(j.sw, d, WIP / 'bracket_sharp.stl'); check_export(d, WIP / 'bracket_sharp.stl')
        close(j.sw, d)
        make_twin(j, WIP / f'{name}.SLDPRT', WIP / f'{name}_ld.SLDPRT')      # pads from T3 must exist in WIP
    ...studies, below
```

`build_bracket(root_r=None)` skips step 2 of T1; every other step and expected volume change is the same.
`bracket_r04` is the same bracket with the 0.4 mm radius a printed inside corner really has (07-done.md study item 6:
"0.4 mm if nothing says otherwise").

## 4. The studies

Fixture and load as T3's governing model: base hole walls fixed, 150 N on the four pads (`load='pads'`, `fix='walls'`),
PETG, pads `PRESS`. Two series, three studies each, in two jobs (four studies per instance at most).

**Series A, sharp corner** (in the build job): global 2.2, motor holes and bore at 0.75, and an edge control on the
corner edge that halves each time. Only the corner control changes (05-fea.md "Refine one thing at a time").

```python
    CORNER = [5.0, -0.1, 5.0, 8.0, 50.1, 8.0]                 # box round the inside corner: x 5..8, z 5..8
    d = open_doc(j.sw, WIP / 'bracket_sharp_ld.SLDPRT')
    A = []
    for cs, nodes in ((1.0, 61000), (0.5, 71000), (0.25, 101000)):
        name = f'T4_SHARP_{int(cs * 100):03d}'
        predict(name, nodes, 2.5, 'the inside corner edge (x 6, z 6): a singularity, expected to climb')
        r = run(j, d, name, 2.2, 0.75, root=None, root_c=cs)
        compare(name, r, nodes, 2.5)
        m = body_mask(r) & r.in_box(CORNER)
        avg = {rad: r.average((6.0, 25.0, 6.0), rad) for rad in (0.5, 1.0, 2.0)}       # (mean von Mises, node count)
        A.append(dict(ctrl=cs, nodes=r.nodes, corner_vm=round(r.peak(m)[0], 2), corner_at=r.peak(m)[1], avg=avg,
                      corner_sz=round(float(r.s[m, 3].min()), 2), row=row(r)))
        log(name, json.dumps(A[-1], default=float))
        (HERE / 't4_sharp.json').write_text(json.dumps(A, indent=1, default=float), encoding='utf-8')
    close(j.sw, d)
```

**Series B, R0.4 corner** (second job, same header, `d = open_doc(j.sw, WIP / 'bracket_r04_ld.SLDPRT')`):
`run(j, d, name, 2.2, 0.75, root=0.4, root_c=cs)` for `cs` in (0.3, 0.2, 0.13), predictions 71,000 / 86,000 /
126,000 nodes, names `T4_R04_030`, `_020`, `_013`; record the same dictionary to `t4_r04.json`.

How to judge:

1. Series A: `convergence_rows = [[ctrl, nodes, corner_vm], ...]`. If the last step moves `corner_vm` by more than
   5 %: `converged = false`. That is the expected outcome and is the finding: a sharp corner has no stress.
   Check the sign: `corner_sz` must be negative (compression).
2. Series B: if the last step moves `corner_vm` by 5 % or less, `reported_stress_mpa` = the last `corner_vm` of
   series B, and `how_judged` = "The sharp corner does not converge (values of series A with their control sizes),
   so it was judged with the 0.4 mm radius a printed corner has; that converged to N MPa von Mises, compressive,
   over controls 0.3 / 0.2 / 0.13 mm. Averages at the sharp corner over 0.5 / 1 / 2 mm: ... (node counts ...)."
3. Verdict for the part, from the finest series-B result's `row`: the same rule as T3 step 7, with
   `vm = max(row['table']['Z']['vm'], corner_vm)`. A corner in compression does not count for the layer measure.

## 5. Decisions made for you

- The variant is rebuilt from the script with one argument changed, not edited (03-modelling.md: rebuilding is the
  first choice, and the task says "build").
- **What number to report for the corner:** the converged von Mises of the R0.4 twin, not the finest sharp value and
  not an average. Why: 07-done.md study item 6 says exactly this, and the averages drift with the mesh (05-fea.md).
  The averages are still listed, at one mesh, as supporting evidence.
- `converged` in results.json describes series A (the sharp part the task asked about): expected `false`.
  `notes` says that series B converged, if it did.
- The load is on the pads, as in T3. The corner is 7 mm from the bore and 11 mm from the nearest pad, so the load
  model does not change the corner; the motor-hole verdict comes from the same result.

## 6. Branches

| You see | It means | Do |
| --- | --- | --- |
| root edge count is not 1 on the sharp part | the edge test | print the edges; the edge runs along Y at x 6, z 6 from y 0 to 50 |
| mesh fails with the edge control | control too small for the mesher | use 1.0 / 0.6 / 0.35 instead; if it still fails, put the control on the two faces that meet at the corner instead of the edge: `pick(d, kind='plane', at=(6, 25, 20))` and `pick(d, kind='plane', at=(40, 25, 6))`, sizes 1.5 / 1.0 / 0.7, and say the series is coarser |
| series A converges (last step under 5 %) | the control is not reaching the corner | read `corner_at`: it must be within 0.3 mm of x 6, z 6. If the peak is elsewhere in the box, shrink the box to x 5.5..6.5, z 5.5..6.5; if it truly converges, report it as converged and say it contradicts the hand expectation |
| `corner_sz` is positive | the load is reversed | reaction Fx must be −150: see T3 branches |
| series B does not converge either | 0.4 mm arc needs smaller elements | one more study at 0.09 (new job); if nodes would pass 200,000, lower the global size to 3.0 for that study only and say so. Still climbing: `reported_stress_mpa` = the average over 1.0 mm at the finest mesh with its node count, `how_judged` says "not shown by convergence", verdict stays fail if the motor holes fail |
| R0.4 corner under 22.5 MPa and converged | Kt lower than estimated | then the corner passes on yield; the part still fails if the motor holes do. Report both |
| `pick(d, kind='cyl', r=0.4)` count is not 1 | the fillet face was split or not built | `list_faces(d)`; a fillet of 0.4 that fails to build returns None from `fillet`: `build_bracket` raises; retry with `root_r=0.5` and say so |
| anything from T3's branch table | same cause | same cure |

Anything else: stop T4, write down exactly what was seen, carry on with T5.

## 7. Done checklist

- [ ] volumes of both variants against the hand values; box; one PETG body; twin shown to be the same part
- [ ] series A table with control sizes, node counts, corner von Mises, its place, and the averages with node counts
- [ ] series B table the same; which one the reported number comes from
- [ ] reaction, displacement, plain-section checks from one study of each series (`row['checks']`)
- [ ] three measures and print-direction table for the R0.4 part (`row['table']`)
- [ ] `put('T4', convergence_rows=[...], converged=False or True, reported_stress_mpa=..., how_judged='...',
      verdict=..., status=..., notes=...)`
- [ ] REPORT.md T4: both series, the sentence on why a sharp corner cannot be given a peak, the verdict with the
      governing measure, what was not verified (the real printed radius), minutes
