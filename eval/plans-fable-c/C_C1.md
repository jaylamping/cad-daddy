# Plan C1: the link as it is

Task: `eval/TASKS_C.md`, C1. One script, one launch, budget 10 minutes. Read [README.md](README.md) "Rules for every
step" first.

## What is built

One solid body, joint axes along Y:

| Part | Feature in the script | Hand volume mm3 |
| --- | --- | --- |
| Elbow disc Ø70, Y -4 to 4, about the origin | `DISC`: circle r 35 on the plane Y 0, mid-plane 8 | + 30,787.6 |
| Beam X ±20, Y ±15, Z -32 to -170 | `BEAM`: rectangle on the plane Z -101, mid-plane 138 | + 165,600 - 457.7 (its top lies inside the disc rim for \|Y\| < 4: a circle segment of radius 35 beyond a chord at 32, area 57.2 mm2, times 8) |
| Block X ±20, Y ±22, Z -170 to -180 | `BLOCK`: rectangle on the plane Z -175, mid-plane 10 | + 17,600 |
| Cheeks X ±15, Y 16 to 22 and -22 to -16 | `CHEEKS`: two rectangles on the plane Z -197.5, mid-plane 35 (Z -180 to -215; from -170 to -180 the cheeks are the block) | + 12,600 |
| Bore Ø30 | `BORE`: cut, mid-plane 9 (overshoots 0.5 each side) | - 5,654.9 |
| Six Ø3.4 on Ø50, first on +X, 60° apart, in the X-Z plane | `HOLES`: six circles in one sketch, cut | - 435.8 |
| Pin hole Ø8 at X 0, Z -200 through both cheeks | `PIN`: cut, mid-plane 46 | - 603.2 |
| **Total** | | **219,436.0 mm3 = 261.1 g** at 1.19 g/cm3 |

Hole centres (x, z): (25, 0), (12.5, 21.651), (-12.5, 21.651), (-25, 0), (-12.5, -21.651), (12.5, -21.651).
Box: X -35 to 35, Y -22 to 22, Z -215 to 35.

## Steps

1. From `eval/<run>/`: `python c1_boxy.py`. It stamps "C1 start" (this starts the clock for the whole set).
2. Watch the log against this table. The script stops itself (`Failed`) when a line is outside its tolerance.

| Step | Expected | Tolerance |
| --- | --- | --- |
| `DISC` added | 30,787.6 mm3 | 1 % (relative) |
| `BEAM` added | 165,142.3 mm3 | 1 % |
| `BLOCK` added | 17,600 mm3 | 1 % |
| `CHEEKS` added, bodies after | 12,600 mm3, 1 body | 1 %, exact |
| `BORE`, `HOLES`, `PIN` removed | 5,654.9, 435.8, 603.2 mm3 | 1 % each |
| Volume of the finished solid | 219,436.0 mm3 | 0.1 % |
| Box | -35, -22, -215, 35, 22, 35 | 0.01 mm abs each |
| Ø3.4 faces, their centres, their length | 6, on the bolt circle, 8.0 long | exact, 0.02 mm abs, 0.02 mm abs |
| Ø30 faces, Ø8 faces, Ø70 rim faces | 1, 2, 1 | exact |
| Pin holes: centre, cheek thickness | X 0, Z -200; 6.0 | 0.02 mm abs |
| STL: watertight, shells, volume against the model, bounds against the box | true, 1, same, same | exact, exact, 0.5 %, 0.15 mm abs |
| Mass | 261.1 g | 0.1 % |
| Shape numbers (not a tolerance, for orientation) | flat_share about 0.85 to 0.95, largest_flat about 0.1, sharp_per_area about 10 to 15 | report what is printed |

3. Open `pictures/c1_boxy.png`. Add **one line** to the C1 section of `REPORT.md`: "What I see: ...".
4. Tick the done checklist.

## The script: `c1_boxy.py` (in full)

```python
"""C1: the boxy forearm link. Build, measure, export, picture, results.   python c1_boxy.py

Every number written to results.json comes from this run; the hand values go in the hand_* keys only."""
import math

from common import *

stamp(HERE, 'C1 start')
hv = boxy_hand_volume()                         # disc, bore, holes, beam, overlap, block, cheeks, pins, total
log('hand volume', {k: round(v, 1) for k, v in hv.items()})
MODEL, STL = WIP / 'link_boxy.SLDPRT', WIP / 'link_boxy.stl'

with job(wait_s=1800) as j:
    d = new_part(j.sw, MODEL)
    # 1. elbow disc Ø70, Y -4 to 4
    with Sk(d, plane(d, 'Y', 0.0, 'DISC_P'), 'DISC') as s:
        s.circle((0.0, 0.0, 0.0), 35.0)
    extrude(d, s.feat, 'DISC', 8.0, mode=MID, expect_dv=hv['disc'])
    save(d)
    # 2. beam X -20..20, Y -15..15, Z -32..-170 (its top end lies inside the disc rim: 457.7 mm3 counted once)
    with Sk(d, plane(d, 'Z', -101.0, 'BEAM_P'), 'BEAM') as s:
        s.rect((-20.0, -15.0, -101.0), (20.0, 15.0, -101.0))
    extrude(d, s.feat, 'BEAM', 138.0, mode=MID, expect_dv=hv['beam'] - hv['overlap'])
    save(d)
    # 3. block X -20..20, Y -22..22, Z -170..-180
    with Sk(d, plane(d, 'Z', -175.0, 'BLOCK_P'), 'BLOCK') as s:
        s.rect((-20.0, -22.0, -175.0), (20.0, 22.0, -175.0))
    extrude(d, s.feat, 'BLOCK', 10.0, mode=MID, expect_dv=hv['block'])
    save(d)
    # 4. cheeks X -15..15, Y 16..22 and -22..-16, below the block: Z -180..-215 (Z -170..-180 is the block itself)
    with Sk(d, plane(d, 'Z', -197.5, 'CHEEK_P'), 'CHEEKS') as s:
        s.rect((-15.0, 16.0, -197.5), (15.0, 22.0, -197.5))
        s.rect((-15.0, -22.0, -197.5), (15.0, -16.0, -197.5))
    extrude(d, s.feat, 'CHEEKS', 35.0, mode=MID, expect_dv=hv['cheeks'])
    must('bodies after the cheeks', len(bodies(d)), 1)
    save(d)
    # 5. bore Ø30, six Ø3.4 on Ø50 (first on +X, 60 degrees apart), pin hole Ø8 at X 0, Z -200. Each cut overshoots.
    with Sk(d, plane(d, 'Y', 0.0, 'BORE_P'), 'BORE') as s:
        s.circle((0.0, 0.0, 0.0), 15.0)
    extrude(d, s.feat, 'BORE', 9.0, cut=True, mode=MID, expect_dv=hv['bore'])
    with Sk(d, plane(d, 'Y', 0.0, 'HOLES_P'), 'HOLES') as s:
        for bx, bz in BOLTS:
            s.circle((bx, 0.0, bz), 1.7)
    extrude(d, s.feat, 'HOLES', 9.0, cut=True, mode=MID, expect_dv=hv['holes'])
    with Sk(d, plane(d, 'Y', 0.0, 'PIN_P'), 'PIN') as s:
        s.circle((0.0, 0.0, -200.0), 4.0)
    extrude(d, s.feat, 'PIN', 46.0, cut=True, mode=MID, expect_dv=hv['pins'])
    save(d)

    # 6. the finished solid against the hand values
    single_body(d)
    must('rebuild errors', len(feature_errors(d)), 0)
    vol = volume(d)
    expect('volume against the hand value', vol, hv['total'], 0.001)
    box = bbox(d)
    want_box = [-35.0, -22.0, -215.0, 35.0, 22.0, 35.0]
    for k in range(6):
        expect(f'box[{k}]', box[k], want_box[k], 0, abs_tol=0.01)
    # 7. every specified dimension measured on the solid
    hs = holes(d, 1.7)
    must('Ø3.4 holes', len(hs), 6)
    for h in hs:
        near = min(math.hypot(h[1][0] - bx, h[1][2] - bz) for bx, bz in BOLTS)
        expect(f'hole at {h[1]} against the bolt circle', near, 0.0, 0, abs_tol=0.02)
        expect('hole runs Y -4 to 4', h[2][4] - h[2][1], 8.0, 0, abs_tol=0.02)
    bore = holes(d, 15.0)
    must('Ø30 bore faces', len(bore), 1)
    expect('bore centre X', bore[0][1][0], 0.0, 0, abs_tol=0.02)
    expect('bore centre Z', bore[0][1][2], 0.0, 0, abs_tol=0.02)
    pins = holes(d, 4.0)
    must('Ø8 pin hole faces (one in each cheek)', len(pins), 2)
    for h in pins:
        expect('pin hole X', h[1][0], 0.0, 0, abs_tol=0.02)
        expect('pin hole Z', h[1][2], -200.0, 0, abs_tol=0.02)
        expect('cheek thickness at the pin hole', h[2][4] - h[2][1], 6.0, 0, abs_tol=0.02)
    must('Ø70 rim faces', len(pick(d, kind='cyl', r=35.0)), 1)
    save(d)
    export(j.sw, d, STL)
    st = check_export(d, STL, want_box)
    close(j.sw, d)

shape = picture([STL], PICS / 'c1_boxy.png')['link_boxy.stl']
mass = vol * DENS_G_MM3
put('C1', status='done', volume_mm3=round(vol, 1), hand_volume_mm3=round(hv['total'], 1), mass_g=round(mass, 2),
    hand_mass_g=round(hv['total'] * DENS_G_MM3, 2), bodies=1, shape=shape, box_mm=[round(v, 3) for v in box],
    stl=dict(volume=round(st['volume'], 1), watertight=st['watertight'], shells=st['shells'], triangles=st['triangles']),
    holes_measured=[h[1] for h in hs], pin_holes_measured=[h[1] for h in pins], model_sha256=sha(MODEL))
t = stamp(HERE, 'C1 end')
report(f"""## C1. The link as it is

- Model `_wip/sw-eval/{RUN}/link_boxy.SLDPRT`, one body, rebuild clean. Picture `pictures/c1_boxy.png`.
- Volume {vol:.1f} mm3 against {hv['total']:.1f} mm3 by hand (disc {hv['disc']:.1f} - bore {hv['bore']:.1f} - holes
  {hv['holes']:.1f} + beam {hv['beam']:.0f} - the beam's top inside the disc rim {hv['overlap']:.1f} + block {hv['block']:.0f}
  + cheeks below the block {hv['cheeks']:.0f} - pin holes {hv['pins']:.1f}). Mass {mass:.1f} g at 1.19 g/cm3.
- Box {[round(v, 2) for v in box]} against {want_box}.
- Measured on the solid: six Ø3.4 holes at {[h[1] for h in hs]}, bore at {bore[0][1]}, pin holes at {[h[1] for h in pins]},
  cheeks 6.0 thick at the pin.
- STL: watertight {st['watertight']}, {st['shells']} shell, volume {st['volume']:.1f} mm3, {st['triangles']} triangles.
- Shape numbers: {shape}.
- What I would question in the drawing: the beam's top face (Z -32) is 3 mm inside the disc rim, so beam and disc
  share {hv['overlap']:.0f} mm3; the cheeks are given from Z -170, where the block already is, so 10 mm of each is the
  block. Both are counted once. The beam (40 x 30 solid) carries {hv['beam'] * DENS_G_MM3:.0f} g of the {mass:.0f} g.
- Clock: C1 ended at {t:.1f} min on times.log.
""")
```

## Branches

| What happens | Do exactly this |
| --- | --- |
| `BEAM volume change` fails by about 458 mm3 (it added 165,600) | SolidWorks counted the overlap differently than expected only if the disc is missing: check that `DISC` built (log line above). If the disc is there and the number is still 165,600, the disc is not at the origin: stop, print `bbox(d)`, fix the plane or the circle centre |
| `CHEEKS` raises, or bodies after the cheeks is not 1 | The two rectangles in one sketch did not extrude together. First fallback: two features, `CHEEK_P` and `CHEEK_M`, one rectangle each, same plane Z -197.5, same depth 35, `expect_dv=6300` each. Second fallback: sketch each on the plane Z -180 and extrude `mode=BLIND`, depth 35, `want=(2, -1, -180.0)` |
| A hole cut raises "no cut changed the volume" | Per 03-modelling.md ("a plain round pocket"): build that cut as a revolve instead. For the pin: profile rectangle in the plane X 0 with corners (0, -23, -200) and (0, 23, -196), centreline (0, -30, -200) to (0, 30, -200), `revolve(d, s.feat, 'PIN', cut=True, expect_dv=603.2)`. For the bore: rectangle (0, -4.5, 0) to (15, 4.5, 0) in the plane Z 0, centreline along Y through the origin, `expect_dv=5654.9`. Second fallback for the six holes: six separate sketches and cuts, one circle each, `expect_dv=72.63` each |
| `Ø70 rim faces` is not 1 | Run `list_faces(d)`. If the rim came back as two faces of radius 35, change the expected count to 2 and write that in the report; this is how the kernel split the face, not an error. Any other count: stop and read the boxes |
| Volume off by more than 0.1 % although every step passed | Print `bodies(d)`: a crumb body, or a second body. `single_body(d)` raises on it. Find the feature that did not merge (the one after which the body count rose) |
| Box wrong | A plane or a depth is wrong: compare each box number with the table "What is built" and fix the feature that owns that face |
| STL bounds off by the part's negative extents | The export shifted to positive space: `export()` pins this, so it means `export_prefs` did not take. Export again once; if it repeats, report it (04-export.md) and continue: C2 does not depend on the boxy STL's frame, only its mass and its picture |
| `check_export` raises on volume | Do not edit the check. Export again. Second time: record `status='partial'` with the two volumes and go to C2 |
| Any `common.py` line raises a Python error (not `Failed`) | README rule 12: fix that line, note it, run again |

C1 ends only as **done** (checklist complete), **not possible** (cannot be: every feature here is a prism or a
cylinder) or **blocked** (three different tries at the same step, each logged). If it is blocked, C2 still runs.

## Done checklist

- [ ] `_wip/sw-eval/<run>/link_boxy.SLDPRT` and `link_boxy.stl` exist; `pictures/c1_boxy.png` exists and was opened.
- [ ] `results.json` has, under `C1`: `volume_mm3`, `hand_volume_mm3`, `mass_g`, `bodies`, `shape`, written by the script.
- [ ] Every row of the steps table was inside its tolerance (the script ran to "C1 end" without `Failed`).
- [ ] `REPORT.md` has the C1 section the script wrote, plus your one line on the picture.
- [ ] `times.log` has "C1 start" and "C1 end".
