# D / D3. Six plates from a table, then a change (60 minutes)

Playbook: 02-com.md "Changing a part that already exists" (`set_dim`, `redraw_circles`, "Thicker is three edits",
"Prove it was an edit", "A change request can break a part that was fine"), 03-modelling.md, 06-judgment.md "Two
requirements that cannot both be met", 07-done.md "A model is done when" and "Long jobs".

## 1. Restatement

Part one: one script builds six adapter plates from the table (disc on Z from 0 to its thickness, centre bore, ring A of
plain holes, ring B of counterbored holes), saves `P1..P6.SLDPRT`, exports an STL of each and writes a table.
Part two, only after part one's table is written: open each saved part and **edit** it (1.5 mm thicker, counterbore
floors stay where they are from the bottom, 1 mm chamfer on the top outside edge, P3's ring A on Ø70), save as
`P1_b..P6_b.SLDPRT`, write the table again. The table has bad rows; catch them before building.

- [ ] the table checked by calculation before anything is built; problems listed with numbers
- [ ] one script, one function, six plates; same checks on P6 as on P1
- [ ] per plate: volume against hand, mass, bodies, STL watertight, thinnest wall, as-table or changed and why
- [ ] part two by editing: tree before and after, same features and IDs plus the chamfer
- [ ] part two: counterbore floor Z measured and unchanged; wall checks run again
- [ ] keys: `plates`, `plates_b`, `table_problems`, `one_script`, `edited_not_rebuilt`, `minutes`

Time: check the table 5; part one 20 (first checkpoint: P1 built and pictured by minute 15); part two 20; report 10.

## 2. Hand calculation: the table checked

Radii in mm. "cb" = counterbore. Wall between a ring A hole and a ring B counterbore = centre distance − rA − r_cb.

| Plate | As the table says | Number | Decision |
| --- | --- | --- | --- |
| P1 | A hole and B counterbore both at 0° (and 180°): centres 30 − 25 = 5.0 apart, radii 1.7 + 4.0 = 5.7 | **overlap 0.7 mm** | turn ring B by 45°: wall 3.02 mm. Dimensions as the table |
| P1 | counterbore edge 30 + 4 = 34 against the outside 35 | wall 1.0 mm | build as asked, flag it |
| P2 | rings A and B are the same: 6 × Ø4.5 on Ø62, both from 0° | **holes coincide** | turn ring B by 30°: twelve holes alternate, wall 9.80 mm |
| P3 | fine. Counterbore edge 42 + 5 = 47 against 48 | wall 1.0 mm | build as asked, flag it. A to B counterbore 2.30 mm |
| P4 | ring B on Ø58 in a Ø60 plate: hole reaches 29 + 2.25 = 31.25, counterbore 29 + 4 = 33, outside is 30 | **3.0 mm beyond the edge** | keep the bolt circle (it is the interface to another part), move the outside diameter: **OD 68** (wall 1.0 mm, as P1 and P3 have). 06-judgment.md: "a bolt circle ... stays; an outside diameter ... moves". The other choice, OD 60 kept, would need ring B on Ø50 or less |
| P4 | counterbore 4.6 deep in a 5 mm plate | **floor 0.4 mm**, under the 0.6 mm minimum | depth **3.0** (as the other Ø8 counterbores), floor 2.0 mm |
| P5 | fine | outer wall 2.5, A to B 4.25 | as the table |
| P6 | fine | outer wall 2.0, A to B 3.30 | as the table |
| part two, P3 | ring A on Ø70 from 0°: B at 42, A at 35: centres 7.0 apart, radii 1.7 + 5.0 = 6.7 | **wall 0.3 mm** | turn ring A by 22.5°: wall 9.82 mm |
| part two, P1, P3, P4 | 1 mm chamfer starts 1.0 mm in from the outside, exactly where the counterbore edge is | **wall 0, a knife edge** | chamfer **0.4 mm** on P1, P3, P4 (leaves 0.6 mm); 1.0 mm on P2, P5, P6 (walls 6.0, 1.5, 1.0) |

Volume: V = π·T·(R² − r_bore² − nA·rA² − nB·rB²) − nB·π·(r_cb² − rB²)·c. Part two: T + 1.5, c + 1.5, minus the chamfer
π·w²·(R − w/3). Mass = V · 1.19e-3.

| Plate | OD | T | bore | A: n × Ø on Ø, turn | B: n × Ø on Ø, turn | cb Ø × c | V mm³ | mass g | min wall mm (where) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 70 | 6 | 30 | 6 × 3.4 on 50, 0° | 4 × 4.5 on 60, **45°** | 8 × 3 | 17728.67 | 21.10 | 1.0 (cb to outside) |
| P2 | 84 | 6 | 40 | 6 × 4.5 on 62, 0° | 6 × 4.5 on 62, **30°** | 8 × 3 | 23947.18 | 28.50 | 3.0 (cb floor); 7.0 sideways |
| P3 | 96 | 8 | 52 | 8 × 3.4 on 66, 0° | 4 × 5.5 on 84, 0° | 10 × 4 | 38698.26 | 46.05 | 1.0 (cb to outside) |
| P4 | **68** | 5 | 28 | 4 × 3.4 on 40, 0° | 6 × 4.5 on 58, 0° | 8 × **3** | 13802.43 | 16.42 | 1.0 (cb to outside) |
| P5 | 120 | 8 | 60 | 12 × 4.5 on 80, 0° | 6 × 6.6 on 104, 0° | 11 × 5 | 62864.78 | 74.81 | 2.5 (cb to outside) |
| P6 | 76 | 6 | 34 | 6 × 3.4 on 46, 0° | 3 × 4.5 on 64, 0° | 8 × 3 | 20848.86 | 24.81 | 2.0 (cb to outside) |

| Plate | T | cb depth | floor Z | chamfer | after thicker (no chamfer) | chamfer removes | V mm³ | mass g | min wall mm |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1_b | 7.5 | 4.5 | 3.0 | 0.4 | 22057.75 | 17.53 | 22040.22 | 26.23 | 0.6 (chamfer to cb) |
| P2_b | 7.5 | 4.5 | 3.0 | 1.0 | 29779.35 | 130.90 | 29648.45 | 35.28 | 3.0 (floor) |
| P3_b (A on 70, 22.5°) | 9.5 | 5.5 | 4.0 | 0.4 | 45789.84 | 24.06 | 45765.78 | 54.46 | 0.6 (chamfer to cb) |
| P4_b | 6.5 | 4.5 | 2.0 | 0.4 | 17819.46 | 17.02 | 17802.44 | 21.18 | 0.6 (chamfer to cb) |
| P5_b | 9.5 | 6.5 | 3.0 | 1.0 | 74446.65 | 187.45 | 74259.20 | 88.37 | 1.5 (chamfer to cb) |
| P6_b | 7.5 | 4.5 | 3.0 | 1.0 | 25983.76 | 118.33 | 25865.43 | 30.78 | 1.0 (chamfer to cb) |

Acceptance: volume within 0.1 %; hole centres within 0.02 mm; floor Z within 0.01 mm. Let the script compute the
hand values from the formula and print them beside this table: they must match to 0.01 mm³ before anything is built.

## 3. The build: `plates.py` (part one)

How each plate is built decides how easy part two is. Everything hangs from the bottom (Z 0): the disc is extruded up
from Z 0; bore and holes are cut through all; the counterbore is sketched on a plane **at its floor** (Z = T − c above
the bottom) and cut through all **upward**. Then "thicker" is one dimension (`D1@DISC`), the floors cannot move, and
every through cut follows by itself.

```python
from common import *

ASKED = {  # the table as given: od, t, bore, a = (n, hole dia, circle dia), b = (n, hole dia, circle dia), cb = (dia, depth)
    'P1': dict(od=70, t=6, bore=30, a=(6, 3.4, 50), b=(4, 4.5, 60), cb=(8, 3)),
    'P2': dict(od=84, t=6, bore=40, a=(6, 4.5, 62), b=(6, 4.5, 62), cb=(8, 3)),
    'P3': dict(od=96, t=8, bore=52, a=(8, 3.4, 66), b=(4, 5.5, 84), cb=(10, 4)),
    'P4': dict(od=60, t=5, bore=28, a=(4, 3.4, 40), b=(6, 4.5, 58), cb=(8, 4.6)),
    'P5': dict(od=120, t=8, bore=60, a=(12, 4.5, 80), b=(6, 6.6, 104), cb=(11, 5)),
    'P6': dict(od=76, t=6, bore=34, a=(6, 3.4, 46), b=(3, 4.5, 64), cb=(8, 3)),
}
FIX = {  # what is built instead, and why (section 2)
    'P1': (dict(turn_b=45.0), 'ring B turned 45 deg: at 0 deg its counterbore overlapped a ring A hole by 0.7 mm'),
    'P2': (dict(turn_b=30.0), 'ring B turned 30 deg: rings A and B were the same six holes'),
    'P4': (dict(od=68, cb=(8, 3.0)), 'OD 60 -> 68: ring B on 58 broke out of a 60 plate by 3.0 mm; counterbore 4.6 -> 3.0 deep: floor was 0.4 mm'),
}

def spec(name):
    p = dict(ASKED[name], turn_a=0.0, turn_b=0.0)
    p.update(FIX.get(name, ({}, ''))[0])
    return p

def ring_pts(n, circle, turn, z):
    return [(circle / 2 * math.cos(math.radians(turn + 360.0 * k / n)),
             circle / 2 * math.sin(math.radians(turn + 360.0 * k / n)), z) for k in range(n)]

def hand(p, chamfer=0.0):
    R, T = p['od'] / 2, p['t']
    (na, da, _), (nb, db, _), (dcb, c) = p['a'], p['b'], p['cb']
    v = math.pi * T * (R * R - p['bore'] ** 2 / 4 - na * da * da / 4 - nb * db * db / 4) - nb * math.pi * (dcb * dcb - db * db) / 4 * c
    return v - math.pi * chamfer ** 2 * (R - chamfer / 3)

def walls(p, chamfer=0.0):
    """Every wall in mm, from the numbers: negative means two features overlap. Run it BEFORE building."""
    R, T = p['od'] / 2, p['t']
    (na, da, ca), (nb, db, cbc), (dcb, c) = p['a'], p['b'], p['cb']
    A, B = ring_pts(na, ca, p['turn_a'], 0), ring_pts(nb, cbc, p['turn_b'], 0)
    gap = lambda P, Q: min(math.dist(a, b) for a in P for b in Q if a is not b)      # noqa: E731
    w = {'A hole to B counterbore': gap(A, B) - da / 2 - dcb / 2,
         'A hole to A hole': gap(A, A) - da if na > 1 else 99.0,
         'B counterbore to B counterbore': gap(B, B) - dcb if nb > 1 else 99.0,
         'A hole to bore': ca / 2 - da / 2 - p['bore'] / 2, 'B counterbore to bore': cbc / 2 - dcb / 2 - p['bore'] / 2,
         'A hole to outside': R - ca / 2 - da / 2, 'B counterbore to outside': R - cbc / 2 - dcb / 2,
         'counterbore floor': T - c}
    if chamfer:
        w['chamfer to B counterbore'] = R - chamfer - cbc / 2 - dcb / 2
    return {k: round(v, 2) for k, v in w.items()}

def measure(d, p, chamfer=0.0):
    """Every dimension read from the solid (07-done.md, model item 2). Returns the measured floor Z."""
    R, T = p['od'] / 2, p['t']
    (na, da, ca), (nb, db, cbc), (dcb, c) = p['a'], p['b'], p['cb']
    for got, want in zip(bbox(d), (-R, -R, 0, R, R, T)):
        expect('box', got, want, 0.01)
    must('outside face', len(pick(d, kind='cyl', r=R)), 1)
    must('bore face', len(pick(d, kind='cyl', r=p['bore'] / 2)), 1)
    want = sorted([(da / 2, q) for q in ring_pts(na, ca, p['turn_a'], 0)] + [(db / 2, q) for q in ring_pts(nb, cbc, p['turn_b'], 0)]
                  + [(dcb / 2, q) for q in ring_pts(nb, cbc, p['turn_b'], 0)])
    got = sorted((h[0], (h[1][0], h[1][1], 0)) for r in sorted({da / 2, db / 2, dcb / 2}) for h in holes(d, r)
                 if math.hypot(h[1][0], h[1][1]) > 1.0)                    # leaves out a bore or rim that shares a radius
    must('hole and counterbore faces', len(got), len(want))
    key = lambda g: (round(g[0], 2), round(math.degrees(math.atan2(g[1][1], g[1][0])) % 360.0, 1) % 360.0)   # noqa: E731
    for (r1, q1), (r2, q2) in zip(sorted(got, key=key), sorted(want, key=key)):
        expect('hole radius', r1, r2, 0.02); expect('hole x', q1[0], q2[0], 0.03); expect('hole y', q1[1], q2[1], 0.03)
    fl = pick(d, kind='plane', normal=(0, 0, 1), inside=[-R, -R, T - c - 0.01, R, R, T - c + 0.01])
    must('counterbore floors', len(fl), nb)
    fz = [face_info(f)['box'][2] for f in fl]
    for z in fz:
        expect('floor z', z, T - c, 0.01)
    return float(np.mean(fz))

def build(j, name):
    p = spec(name)
    R, T = p['od'] / 2, p['t']
    (na, da, ca), (nb, db, cbc), (dcb, c) = p['a'], p['b'], p['cb']
    w = walls(p); log(name, 'walls', w)
    if min(w.values()) < 0.6:
        raise Failed(f'{name}: a wall under 0.6 mm in the numbers: {w}. Do not build; fix the row first.')
    d = new_part(j.sw, WIP / f'{name}.SLDPRT')
    base = lambda: plane(d, 'Z', 0.0, '')                 # noqa: E731  the base plane, fetched fresh each time
    with Sk(d, base(), 'DISC') as s:
        s.circle((0, 0, 0), R)
    extrude(d, s.feat, 'DISC', T, mode=BLIND, want=(2, +1, 0.0), expect_dv=math.pi * R * R * T)
    with Sk(d, base(), 'BORE') as s:
        s.circle((0, 0, 0), p['bore'] / 2)
    extrude(d, s.feat, 'BORE', T, cut=True, mode=THRU_ALL, expect_dv=math.pi * p['bore'] ** 2 / 4 * T)
    with Sk(d, base(), 'RING_A') as s:
        for q in ring_pts(na, ca, p['turn_a'], 0.0):
            s.circle(q, da / 2)
    extrude(d, s.feat, 'RING_A', T, cut=True, mode=THRU_ALL, expect_dv=na * math.pi * da * da / 4 * T)
    with Sk(d, base(), 'RING_B') as s:
        for q in ring_pts(nb, cbc, p['turn_b'], 0.0):
            s.circle(q, db / 2)
    extrude(d, s.feat, 'RING_B', T, cut=True, mode=THRU_ALL, expect_dv=nb * math.pi * db * db / 4 * T)
    zf = T - c                                            # the counterbore floor, measured from the bottom
    with Sk(d, plane(d, 'Z', zf, 'CBORE_P'), 'CBORE') as s:
        for q in ring_pts(nb, cbc, p['turn_b'], zf):
            s.circle(q, dcb / 2)
    extrude(d, s.feat, 'CBORE', c, cut=True, mode=THRU_ALL, want=(2, +1, zf),
            expect_dv=nb * math.pi * (dcb * dcb - db * db) / 4 * c)
    single_body(d); must('rebuild errors', len(feature_errors(d)), 0); save(d)
    expect(name + ' volume', volume(d), hand(p), 0.001)
    fz = measure(d, p)
    export(j.sw, d, WIP / f'{name}.stl')
    st = check_export(d, WIP / f'{name}.stl')
    out = dict(volume_mm3=volume(d), hand_volume_mm3=hand(p), mass_g=volume(d) * DENS_G_MM3, bodies=len(bodies(d)),
               stl_watertight=st['watertight'], min_wall_mm=min(w.values()), min_wall_where=min(w, key=w.get),
               changed=name in FIX, why=FIX.get(name, ({}, 'as the table says'))[1], counterbore_floor_z_mm=fz, tree=tree(d))
    close(j.sw, d)
    return out

if __name__ == '__main__':
    for n in ASKED:                                        # the table as given, checked before SolidWorks starts
        log(n, 'AS GIVEN', walls(dict(ASKED[n], turn_a=0.0, turn_b=0.0)), '| AS BUILT', walls(spec(n)), 'hand', round(hand(spec(n)), 2))
    with job() as j:
        plates = {}
        for n in ASKED:
            plates[n] = build(j, n)
            (HERE / 'd3_part1.json').write_text(json.dumps(plates, indent=1, default=float), encoding='utf-8')
            log(n, 'done at minute', minutes())
```

The loop before `with job()` must print, for the table as given: P1 `A hole to B counterbore` −0.7; P2 the same −6.25;
P4 `B counterbore to outside` −3.0 and `counterbore floor` 0.4; and no value under 0.6 for the plates as built. If it
prints anything else, stop and find the typing error before SolidWorks starts.

Then: write `d3_table_part1.md` from `d3_part1.json` (columns: plate, volume, hand volume, difference %, mass, bodies,
STL watertight, thinnest wall and where, as table or changed and why);
`python solidworks/sheet.py <WIP>/P1.stl ... <WIP>/P6.stl -o eval/<run>/pictures/d3_part1.png` and look at all six
rows (hole counts, ring B turned on P1 and P2, counterbores on top). Commit or note the checkpoint with the time.
**Only now** read the change request again and start part two.

## 4. Part two: `plates_b.py` (edit, do not rebuild)

```python
from plates import *
CHAMFER = {'P1': 0.4, 'P2': 1.0, 'P3': 0.4, 'P4': 0.4, 'P5': 1.0, 'P6': 1.0}
WHY_B = {'P1': 'chamfer 0.4 not 1.0: the counterbore edge is 1.0 mm from the outside, a 1 mm chamfer would meet it',
         'P3': 'ring A on 70 turned 22.5 deg (0.3 mm to the ring B counterbore otherwise); chamfer 0.4 not 1.0, as P1',
         'P4': 'chamfer 0.4 not 1.0, as P1'}

def edge_z(e):
    cp = e.GetCurveParams3
    return list(e.GetCurve.Evaluate2((cp.UMinValue + cp.UMaxValue) / 2, 0))[2] * 1e3

def change(j, name, part1):
    p = spec(name)
    T, R, w = p['t'], p['od'] / 2, CHAMFER[name]
    d = open_doc(j.sw, WIP / f'{name}.SLDPRT')
    expect('opened part one', volume(d), part1['volume_mm3'], 0.0001)
    before = tree(d)
    save_as(d, WIP / f'{name}_b.SLDPRT')
    set_dim(d, 'DISC', T, T + 1.5)                          # 1. thicker: the one driving dimension
    d.ForceRebuild3(False)
    must('rebuild errors', len(feature_errors(d)), 0)
    p = dict(p, t=T + 1.5, cb=(p['cb'][0], p['cb'][1] + 1.5))
    if name == 'P3':                                        # 2. P3: ring A to the 70 circle, turned 22.5 deg
        p = dict(p, a=(8, 3.4, 70), turn_a=22.5)
        redraw_circles(d, 'RING_A_SK', ring_pts(8, 70, 22.5, 0.0), 1.7)
        d.ForceRebuild3(False)
        must('rebuild errors', len(feature_errors(d)), 0)
    wl = walls(p, w); log(name, 'walls', wl)
    if min(wl.values()) < 0.6:
        raise Failed(f'{name}_b: a wall under 0.6 mm in the numbers: {wl}')
    expect('thicker, floors kept', volume(d), hand(p), 0.001)
    rim = pick(d, kind='cyl', r=R); must('outside face', len(rim), 1)           # 3. chamfer on the top outside edge
    top = [e for e in (call(rim[0], 'GetEdges') or []) if abs(edge_z(e) - (T + 1.5)) < 0.01]
    must('top outside edge', len(top), 1)
    v0 = volume(d)
    chamfer(d, top, w, 'TOP_CHAMFER')
    expect('chamfer dv', v0 - volume(d), math.pi * w * w * (R - w / 3), 0.02)
    single_body(d); must('rebuild errors', len(feature_errors(d)), 0); save(d)
    expect(name + '_b volume', volume(d), hand(p, w), 0.001)
    fz = measure(d, p, w)
    expect('floor where it was', fz, part1['counterbore_floor_z_mm'], 0.01)
    after = tree(d)
    old = [tuple(x) for x in part1['tree']]
    same = [tuple(x) for x in after[:len(before)]] == [tuple(x) for x in before] == old
    export(j.sw, d, WIP / f'{name}_b.stl')
    st = check_export(d, WIP / f'{name}_b.stl')
    out = dict(volume_mm3=volume(d), hand_volume_mm3=hand(p, w), mass_g=volume(d) * DENS_G_MM3, bodies=len(bodies(d)),
               stl_watertight=st['watertight'], min_wall_mm=min(wl.values()), min_wall_where=min(wl, key=wl.get),
               changed=name in WHY_B, why=WHY_B.get(name, 'as asked'), counterbore_floor_z_mm=fz,
               old_features_unchanged=same, new_features=[x[0] for x in after[len(before):]])
    close(j.sw, d)
    return out

if __name__ == '__main__':
    part1 = json.loads((HERE / 'd3_part1.json').read_text(encoding='utf-8'))
    with job() as j:
        b = {}
        for n in ASKED:
            b[n] = change(j, n, part1[n])
            (HERE / 'd3_part2.json').write_text(json.dumps(b, indent=1, default=float), encoding='utf-8')
            log(n, '_b done at minute', minutes())
```

The three edits of "thicker" (02-com.md), ticked: the body (`D1@DISC`: T → T + 1.5); planes at the old top (none: the
counterbore plane is measured from the bottom); depths from the top (none: every cut is through-all). The floor check
proves it.

Then `d3_table_part2.md`, the picture sheet `d3_part2.png` of the six `_b` STLs, and look: thicker, a chamfer on the
top rim, P3's ring A further out and turned.

## 5. Decisions made for you

- The four table fixes and two change-request fixes of section 2, each with its number. Where a ring is turned, the
  task sheet allows it ("unless you have a reason to turn a ring, in which case say so").
- P4: the bolt circle stays and the outside diameter moves (06-judgment.md). One line lets a person overrule it:
  "P4 was built Ø68; say so if Ø60 matters more than the Ø58 bolt circle."
- P1 and P3 are built with their 1.0 mm outer wall as the table says: thin but above 0.6 mm. Flagged, not changed.
- The 1 mm chamfer is the requirement given up on P1, P3, P4 (to 0.4 mm): nothing else depends on a chamfer's size.
- `min_wall_mm` comes from the numbers (`walls()`), after `measure()` has shown that every hole on the solid is where
  the numbers say. It is not measured on the STL. Say so.
- `one_script` = true (one `build` for six). `edited_not_rebuilt` = true only if, for all six, `old_features_unchanged`
  is true and `new_features` is `['TOP_CHAMFER']` (the chamfer has no sketch or plane); say how you know: opened from
  the saved file, same feature names, types and IDs, one new feature, floor Z unchanged.

## 6. Branches

| You see | It means | Do |
| --- | --- | --- |
| a `THRU_ALL` cut raises "no cut changed the volume" | neither direction cut | use `mode=BLIND` with depth `T + 1.0` and `want=(2, +1, 0.0)`. Then part two needs one more edit per such feature: `set_dim(d, '<feature>', T + 1.0, T + 2.5)`. Write that in the report |
| `CBORE` volume equals nB·π·(r_cb² − rB²)·(T − c) | it cut downward | `want` was dropped: it must be `(2, +1, zf)` |
| `CBORE` raises where the others worked | 03-modelling.md: the plain round pocket | `revolve(cut=True)` per counterbore: plane through the hole axis is awkward off-axis, so instead sketch the counterbore circles on a plane at the **top** (`plane(d,'Z',T,..)`), `mode=BLIND`, depth c, `want=(2, -1, T)`. Part two then needs two more edits: the plane (`set_dim(d, 'CBORE_P', T, T + 1.5)`) and the depth (`set_dim(d, 'CBORE', c, c + 1.5)`): the "three edits" of 02-com.md |
| `set_dim` raises "no dimension reads ..." | the list it prints shows what the feature has | use the value it shows; if `DISC` shows nothing, the extrude was not blind |
| after `set_dim` the volume grew by more than π·R²·1.5 minus holes | a cut did not follow | `feature_errors(d)`; the feature named there needs its own edit (first row) |
| floor Z moved by 1.5 | the counterbore hangs from the top | see the `CBORE` rows |
| `redraw_circles` raises "no sketch RING_A_SK" | the sketch has another name | `tree(d)` lists it; the helper names sketches `<feature>_SK` |
| P3_b volume after the redraw is not the same as before it | holes fell off the plate or onto each other | `holes(d, 1.7)`: eight, at radius 35, angles 22.5 + 45k |
| top edge count is 0 or 2 | `edge_z` did not find the rim's top edge | print `edge_z(e)` for both edges of the rim face; pick the one at Z = T + 1.5 |
| `chamfer` raises | the chamfer did not build | cut it by revolve instead: `plane(d,'Y',0.0,'')`, `s.poly([(R - w, 0, Tn), (R + 0.5, 0, Tn), (R + 0.5, 0, Tn - w - 0.5)])` with Tn = T + 1.5, `s.centerline((0,0,0),(0,0,Tn))`, `revolve(d, s.feat, 'TOP_CHAMFER', cut=True, expect_dv=math.pi*w*w*(R - w/3))`. `new_features` then has three names; say so |
| `measure` fails on a hole position by under 0.1 mm | loose face boxes | see T1's branch on `CylinderParams`; do not loosen the tolerance silently |
| `measure` count is wrong on P2 | A and B holes share Ø4.5: 12 faces of radius 2.25 are expected | it already counts them together; print `holes(d, 2.25)` |
| a plate fails and the others are fine | one bad row | finish the other plates, come back; never skip the checks on the later plates to save time |
| 60 minutes used | time | report what is built, both tables as far as they go, and `minutes` |

Anything else: stop that plate, write down exactly what was seen, carry on with the next plate, then the next task.

## 7. Done checklist

- [ ] the as-given wall table printed before the build, with the four negative or thin values
- [ ] six parts, each: one body, no rebuild errors, volume within 0.1 % of hand, box, every hole measured, floor Z, STL checked
- [ ] `d3_table_part1.md` written before part two started (file time in the report), picture looked at
- [ ] six `_b` parts with the same checks, floor Z equal to part one, tree before and after
- [ ] `d3_table_part2.md`, picture looked at
- [ ] `put('D3', plates={...}, plates_b={...}, table_problems=[the eight lines of section 2's first table, each "what,
      the number, what was built"], one_script=True, edited_not_rebuilt=..., minutes=minutes_used, status=..., notes=...)`
      with, per plate, `volume_mm3`, `hand_volume_mm3`, `min_wall_mm`, `changed`, `why` (and `counterbore_floor_z_mm` in `plates_b`)
- [ ] REPORT.md D3: the problems and decisions, both tables, the weakest point named by you (the 0.6 mm wall left
      beside the chamfer on P1, P3, P4; the 1.0 mm outer walls), what was not verified (walls not measured on the mesh)
