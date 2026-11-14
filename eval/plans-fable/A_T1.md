# A / T1. Model a bracket from a specification

Playbook: 03-modelling.md (all), 04-export.md "Exporting", 07-done.md "A model is done when".

## 1. Restatement

Build the L-shaped bracket of TASKS.md T1 as one solid body, in the frame given (base on Z 0 to 6, upright on X 0 to 6).
Save `bracket.SLDPRT`, export `bracket.step` and `bracket.stl`, and check every dimension on the solid.
Write the build as a function, because T4 and T5 call it again.

Requirements (tick at the end):

- [ ] base X 0..80, Y 0..50, Z 0..6; upright X 0..6, Y 0..50, Z 6..46; one body
- [ ] R4 fillet on the inside corner (edge along Y at X 6, Z 6)
- [ ] four Ø5.5 through the base at (25,10), (25,40), (65,10), (65,40)
- [ ] Ø22 bore through the upright, axis X, at Y 25, Z 28
- [ ] four Ø3.4 through the upright on Ø31 about the bore at 45/135/225/315 deg
- [ ] R5 on the two vertical base corners at X 80 and on the two top corners of the upright (edges along X at Z 46)
- [ ] `bracket.SLDPRT`, `bracket.step`, `bracket.stl` in `WIP`
- [ ] keys: `volume_mm3`, `hand_volume_mm3`, `mass_g`, `bbox_mm`, `bodies`, `stl_watertight`, `stl_volume_mm3`

## 2. Hand calculation

q = 1 − π/4 = 0.2146018 (area a fillet of radius 1 adds to, or a round removes from, a square corner).

| Step | Working | mm³ |
| --- | --- | --- |
| L profile | (80·6 + 6·40) · 50 = 720 · 50 | +36000.00 |
| root fillet R4 | q · 4² · 50 | +171.68 |
| base rounds R5 ×2 | 2 · q · 5² · 6 | −64.38 |
| upright rounds R5 ×2 | 2 · q · 5² · 6 | −64.38 |
| base holes | 4 · π · 2.75² · 6 | −570.20 |
| bore | π · 11² · 6 | −2280.80 |
| motor holes | 4 · π · 1.7² · 6 | −217.90 |
| **total** | | **32974.02** |

Mass = 32974.02 · 1.19e-3 = **39.24 g**. Box = [0, 0, 0, 80, 50, 46]. Bodies = 1.
Motor hole offsets: 15.5 · cos 45° = 10.960, so centres (Y, Z) = (14.040, 17.040), (35.960, 17.040), (14.040, 38.960),
(35.960, 38.960).
Acceptance: volume within 0.1 % (±33 mm³), box within 0.01 mm, STL volume within 0.5 % of the part.

## 3. The build

Put this in `eval/<run>/bracket.py` (imported by T3, T4, T5). Confidence that it builds as written: high for the
extrudes and holes, medium for the fillets (edge tests are by position and should find exactly the edges named).

```python
from common import *
Q = 1 - math.pi / 4
MOTOR_YZ = [(25 + a * 10.960, 28 + b * 10.960) for b in (-1, 1) for a in (-1, 1)]
BASE_XY = [(25, 10), (25, 40), (65, 10), (65, 40)]

def build_bracket(j, path, root_r=4.0):
    """root_r: 4.0 for T1, None for T4's sharp corner, 0.4 for T4's as-printed corner."""
    d = new_part(j.sw, path)
    with Sk(d, plane(d, 'Y', 25.0, 'L_P'), 'L') as s:                      # 1. the L, drawn at mid width
        s.poly([(0, 25, 0), (80, 25, 0), (80, 25, 6), (6, 25, 6), (6, 25, 46), (0, 25, 46)])
    extrude(d, s.feat, 'L', 50.0, mode=MID, expect_dv=36000.0)
    save(d)
    if root_r:                                                              # 2. inside corner
        e = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01)
        must('root edge', len(e), 1)
        v0 = volume(d)
        if fillet(d, e, (root_r,), 'ROOT_R') is None:
            raise Failed('root fillet did not build')
        expect('root fillet dv', volume(d) - v0, Q * root_r ** 2 * 50, 0.01)
        save(d)
    e = edges_where(d, lambda p: abs(p[0] - 80) < 0.01 and min(abs(p[1]), abs(p[1] - 50)) < 0.01)   # 3. base corners
    must('base corner edges', len(e), 2)
    v0 = volume(d)
    if fillet(d, e, (5.0,), 'BASE_R5') is None:
        raise Failed('base rounds did not build')
    expect('base rounds dv', v0 - volume(d), 2 * Q * 25 * 6, 0.01)
    e = edges_where(d, lambda p: abs(p[2] - 46) < 0.01 and min(abs(p[1]), abs(p[1] - 50)) < 0.01)   # 4. upright top corners
    must('upright corner edges', len(e), 2)
    v0 = volume(d)
    if fillet(d, e, (5.0,), 'TOP_R5') is None:
        raise Failed('upright rounds did not build')
    expect('upright rounds dv', v0 - volume(d), 2 * Q * 25 * 6, 0.01)
    save(d)
    with Sk(d, plane(d, 'Z', 3.0, 'BASE_HOLES_P'), 'BASE_HOLES') as s:      # 5. cut Z -0.5..6.5: overshoots into air
        for x, y in BASE_XY:
            s.circle((x, y, 3.0), 2.75)
    extrude(d, s.feat, 'BASE_HOLES', 7.0, cut=True, mode=MID, expect_dv=4 * math.pi * 2.75 ** 2 * 6)
    with Sk(d, plane(d, 'X', 3.0, 'BORE_P'), 'BORE') as s:                  # 6. cut X -0.5..6.5
        s.circle((3.0, 25, 28), 11.0)
    extrude(d, s.feat, 'BORE', 7.0, cut=True, mode=MID, expect_dv=math.pi * 121 * 6)
    with Sk(d, plane(d, 'X', 3.0, 'MOTOR_HOLES_P'), 'MOTOR_HOLES') as s:    # 7.
        for y, z in MOTOR_YZ:
            s.circle((3.0, y, z), 1.7)
    extrude(d, s.feat, 'MOTOR_HOLES', 7.0, cut=True, mode=MID, expect_dv=4 * math.pi * 1.7 ** 2 * 6)
    single_body(d)
    must('rebuild errors', len(feature_errors(d)), 0)
    save(d)
    return d

def hand_volume(root_r=4.0):
    return (36000 + (Q * root_r ** 2 * 50 if root_r else 0) - 4 * Q * 25 * 6
            - 4 * math.pi * 2.75 ** 2 * 6 - math.pi * 121 * 6 - 4 * math.pi * 1.7 ** 2 * 6)
```

Expected volume after each step: 36000.00, 36171.68, 36107.30, 36042.92, 35472.72, 33191.92, 32974.02.

`t1.py`:

```python
from bracket import *
with job() as j:
    d = build_bracket(j, WIP / 'bracket.SLDPRT')
    expect('volume', volume(d), hand_volume(), 0.001)
    for got, want in zip(bbox(d), (0, 0, 0, 80, 50, 46)):
        expect('box', got, want, 0.01)
    # every dimension measured on the solid (07-done.md, model item 2)
    hb = holes(d, 2.75); must('base holes', len(hb), 4)
    for h, (x, y) in zip(hb, BASE_XY):                       # sorted by x then y: same order as BASE_XY
        expect('base hole x', h[1][0], x, 0.02); expect('base hole y', h[1][1], y, 0.02)
        expect('base hole from z', h[2][2], 0.0, 0.02); expect('base hole to z', h[2][5], 6.0, 0.02)
    b = holes(d, 11.0); must('bore', len(b), 1)
    expect('bore y', b[0][1][1], 25, 0.02); expect('bore z', b[0][1][2], 28, 0.02)
    expect('bore from x', b[0][2][0], 0.0, 0.02); expect('bore to x', b[0][2][3], 6.0, 0.02)
    hm = holes(d, 1.7); must('motor holes', len(hm), 4)
    for h, (y, z) in zip(hm, sorted(MOTOR_YZ)):              # all at x 3: sorted by y then z
        expect('motor hole y', h[1][1], y, 0.02); expect('motor hole z', h[1][2], z, 0.02)
    f4 = holes(d, 4.0); must('root fillet faces', len(f4), 1)
    log('root fillet box', f4[0][2])                         # expect [6, 0, 6, 10, 50, 10]
    must('R5 faces', len(holes(d, 5.0)), 4)
    export(j.sw, d, WIP / 'bracket.step'); export(j.sw, d, WIP / 'bracket.stl')
    st = check_export(d, WIP / 'bracket.stl', WIP / 'bracket.step')
    put('T1', volume_mm3=volume(d), hand_volume_mm3=hand_volume(), mass_g=volume(d) * DENS_G_MM3, bbox_mm=bbox(d),
        bodies=len(bodies(d)), stl_watertight=st['watertight'], stl_volume_mm3=st['volume'], status='done', notes='')
    close(j.sw, d)
```

Then `python solidworks/sheet.py <WIP>/bracket.stl -o eval/<run>/pictures/t1_bracket.png` and look: an L, the bore
and four small holes in the upright, four holes in the base, the fillet inside the corner, four rounded corners.

Faces and edges later tasks pick, all by position: base holes `pick(d, kind='cyl', r=2.75)` (4); bore
`pick(d, kind='cyl', r=11.0)` (1); motor holes `pick(d, kind='cyl', r=1.7)` (4); root fillet
`pick(d, kind='cyl', r=4.0)` (1); the inside-corner edge `edges_where(d, lambda p: abs(p[0]-6)<0.01 and abs(p[2]-6)<0.01)`.

## 4. Studies

None.

## 5. Decisions made for you

- The L is one extruded profile, not two blocks: one body is then certain, and the volume is the same.
- Fillets go before the holes, so no fillet has to run past a hole.
- Holes are cut 0.5 mm beyond both faces (03-modelling.md, "make cutting tools overshoot"); `expect_dv` is the
  material actually removed.
- The specification was checked (07-done.md, model item 3) and is buildable. Report these, do not change them:
  ligament between the bore and each motor hole 15.5 − 11 − 1.7 = **2.8 mm** (thin, and it is where T3 fails);
  base hole edge distance 10 − 2.75 = 7.25 mm; motor hole to upright top 46 − 38.96 − 1.7 = 5.34 mm; no wall under
  0.6 mm, no hole outside its material, nothing contradictory.

## 6. Branches

| You see | It means | Do |
| --- | --- | --- |
| `Sk` raises "point ... off the sketch plane" | a typo in a coordinate | fix the point; all L points have y = 25, base-hole points z = 3, upright points x = 3 |
| `extrude` L raises "no extrude changed the volume" | the profile did not close | print the six points; they must be exactly the list above |
| an edge count is not 1 or 2 | the test matched other edges | print each edge's start/end (`e.GetCurveParams3.StartPoint`), tighten the test; do not fillet |
| `fillet` returns None | radius did not build on that pair | do the two edges one at a time (two calls, names `..._A`, `..._B`); if one still fails, stop T1 as partial and report which |
| a fillet's volume change has the wrong sign or size | wrong edges were rounded | `d.EditUndo2(1)`, print the edges, fix the test |
| a hole cut raises, where other cuts worked | 03-modelling.md table, "plain round pocket" | cut that hole with `revolve(cut=True)`: rectangle from the axis out to the radius in a plane through the axis, `s.centerline` on the axis |
| a hole centre from `holes()` is off by 0.02 to 0.2 mm while every volume is exact | the face's box is loose, not the hole | read the axis instead: `f.GetSurface.CylinderParams` gives a point on the axis in its first three numbers (metres) and the radius in the seventh; compare that |
| final volume off by more than 33 mm³ | one feature is wrong | compare the logged volume after each step with the list above; the first one that differs is the culprit |
| `bodies` is not 1 | a crumb or a split | `bodies(d)`; `single_body` deletes crumbs under 0.2 mm³ and raises otherwise: read its message |
| STL box starts at a shifted origin | export option 71 | you did not use `export()`; use it |
| `check_export` raises in `stl_stats` | planner's untested code | fall back to `trimesh` as in 04-export.md; if neither works set `stl_watertight` and `stl_volume_mm3` to null and say so |

Anything else: stop T1, write down exactly what was seen, go to T6, T7 and set D (T2 to T5 need this part).

## 7. Done checklist

- [ ] `feature_errors(d)` empty, one body
- [ ] volume within 0.1 % of 32974.02, box = [0,0,0,80,50,46] within 0.01
- [ ] all nine holes, the fillet and the four rounds measured by position (numbers in the log)
- [ ] STL watertight, one shell, volume within 0.5 %, box within 0.1 mm; STEP has `.MILLI.` on an `SI_UNIT` line
- [ ] picture looked at
- [ ] results.json `T1` keys written by the script; REPORT.md T1: what was built, the hand table above, each check
      with its number, the 2.8 mm ligament note, what was not verified, minutes
