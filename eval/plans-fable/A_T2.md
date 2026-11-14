# A / T2. Change an existing part

Playbook: 02-com.md "Changing a part that already exists", 03-modelling.md "Recipes" and "What goes wrong".

## 1. Restatement

Open the saved `bracket.SLDPRT` (do not call `build_bracket`), add four counterbores and one slot, save as
`bracket_b.SLDPRT`. `bracket.SLDPRT` itself must stay unchanged, and the result must be shown to be an edit.

- [ ] Ø10 counterbore, 3 deep from Z 6, on each of the four base holes (floors at Z 3)
- [ ] slot through the base, 20 × 6 overall, round ends, centred X 45, Y 25, long axis along X
- [ ] opened and edited, not rebuilt: feature tree before and after logged; `bracket.SLDPRT` hash unchanged
- [ ] saved as `bracket_b.SLDPRT`
- [ ] keys: `volume_mm3`, `hand_volume_mm3`, `counterbore_floor_z_mm`, `bodies`

## 2. Hand calculation

| Step | Working | mm³ |
| --- | --- | --- |
| start (T1) | | 32974.02 |
| counterbores | 4 · π · (5² − 2.75²) · 3 = 4 · 164.34 | −657.38 |
| slot end circles | 2 · π · 3² · 6 | −339.29 |
| slot middle | 14 · 6 · 6 − π · 3² · 6 (the two half circles already cut) | −334.35 |
| **total** | slot in all: (14·6 + π·3²) · 6 = 673.65 | **31643.00** |

Mass 37.66 g. Box unchanged [0,0,0,80,50,46]. One body. Counterbore floor at Z = 6 − 3 = **3.000**.
Clearances checked: counterbore edge to the root fillet 25 − 5 − 10 = 10 mm; to the R5 base corner 80 − 5 − 70 = 5 mm
(clear); to the Y edges 10 − 5 = 5 mm; slot (X 35..55, Y 22..28) to the nearest counterbore edge
√(10² + 12²) − 5 = 10.6 mm; floor under the counterbores 3 mm. Nothing to question.
Acceptance: volume within 0.1 % (±32 mm³); floor Z within 0.01.

## 3. The build (`t2.py`)

```python
from bracket import *
src, dst = WIP / 'bracket.SLDPRT', WIP / 'bracket_b.SLDPRT'
h0 = sha(src)
with job() as j:
    d = open_doc(j.sw, src)
    expect('opened the T1 part', volume(d), hand_volume(), 0.001)
    before = tree(d); log('tree before', before)
    save_as(d, dst)                                   # from here on d is bracket_b; bracket.SLDPRT is not touched again
    # 1. counterbores: tool Z 3..7 (1 mm of air above the base top), floor exactly at Z 3
    with Sk(d, plane(d, 'Z', 5.0, 'CBORE_P'), 'CBORE') as s:
        for x, y in BASE_XY:
            s.circle((x, y, 5.0), 5.0)
    extrude(d, s.feat, 'CBORE', 4.0, cut=True, mode=MID, expect_dv=4 * math.pi * (25 - 2.75 ** 2) * 3)
    save(d)
    # 2. slot ends: two full Ø6 holes at X 38 and X 52
    with Sk(d, plane(d, 'Z', 3.0, 'SLOT_ENDS_P'), 'SLOT_ENDS') as s:
        s.circle((38, 25, 3.0), 3.0); s.circle((52, 25, 3.0), 3.0)
    extrude(d, s.feat, 'SLOT_ENDS', 7.0, cut=True, mode=MID, expect_dv=2 * math.pi * 9 * 6)
    # 3. slot middle: the rectangle between the two centres
    with Sk(d, plane(d, 'Z', 3.0, 'SLOT_MID_P'), 'SLOT_MID') as s:
        s.rect((38, 22, 3.0), (52, 28, 3.0))
    extrude(d, s.feat, 'SLOT_MID', 7.0, cut=True, mode=MID, expect_dv=14 * 6 * 6 - math.pi * 9 * 6)
    single_body(d); must('rebuild errors', len(feature_errors(d)), 0); save(d)
    hand = hand_volume() - 4 * math.pi * (25 - 2.75 ** 2) * 3 - (14 * 6 + math.pi * 9) * 6
    expect('volume', volume(d), hand, 0.001)
    for got, want in zip(bbox(d), (0, 0, 0, 80, 50, 46)):
        expect('box', got, want, 0.01)
    floors = pick(d, kind='plane', normal=(0, 0, 1), inside=[19, 4, 2.9, 71, 46, 3.1])
    must('counterbore floors', len(floors), 4)
    fz = [face_info(f)['box'][2] for f in floors]
    for z in fz:
        expect('floor z', z, 3.0, 0.01)
    for f in floors:
        expect('floor area', face_info(f)['area'], math.pi * (25 - 2.75 ** 2), 0.02)
    cb = holes(d, 5.0, inside=[19, 4, 2.9, 71, 46, 6.1]); must('counterbore walls', len(cb), 4)
    for h, (x, y) in zip(cb, BASE_XY):
        expect('cbore x', h[1][0], x, 0.02); expect('cbore y', h[1][1], y, 0.02)
    ends = holes(d, 3.0, inside=[34, 21, -0.1, 56, 29, 6.1]); must('slot end faces', len(ends), 2)
    log('slot end boxes', [e[2] for e in ends])       # expect x 35..38 and 52..55, y 22..28
    after = tree(d); log('tree after', after)
    if after[:len(before)] != before or [n for n, _, _ in after[len(before):] if not n.endswith('_P') and not n.endswith('_SK')] != ['CBORE', 'SLOT_ENDS', 'SLOT_MID']:
        log('NOTE: tree is not "old features unchanged + the new ones": read both lists and report what differs')
    put('T2', volume_mm3=volume(d), hand_volume_mm3=hand, counterbore_floor_z_mm=float(np.mean(fz)),
        bodies=len(bodies(d)), status='done', notes='edited in place; tree before/after in the log')
    export(j.sw, d, WIP / 'bracket_b.stl')
    close(j.sw, d)
if sha(src) != h0:
    raise SystemExit('bracket.SLDPRT changed on disk: T2 must not alter it. Rebuild it with t1.py and say so.')
```

Expected volume after each step: 32316.65, 31977.35, 31643.00. Then
`python solidworks/sheet.py <WIP>/bracket_b.stl -o eval/<run>/pictures/t2_bracket_b.png` and look for four
counterbores and one slot in the base.

Notes on the picks: the `inside` box of the floor pick (Z 2.9 to 3.1) lets only faces lying in the plane Z 3 through,
so the base top (Z 6) and bottom (Z 0) cannot match. `holes(d, 5.0, inside=...)` leaves out the four R5 corner rounds
(their boxes reach X 80 or Z 46). `holes(d, 3.0, ...)` finds the two half cylinders left at the slot ends.

## 4. Studies

None.

## 5. Decisions made for you

- The slot is cut as two Ø6 holes (feature `SLOT_ENDS`) plus a 14 × 6 rectangle between their centres (feature
  `SLOT_MID`). Why: `Sk.arc` leaves the arc direction to trial and error (swkit.py, `Sk.arc`), and a
  wrong direction still cuts something. Two circles and a rectangle give the exact slot with nothing to get backwards.
- The counterbore tool starts 1 mm above the base top instead of flush with it, so no face is "almost" coincident.
- `save_as` comes before the first edit, so nothing can be saved into `bracket.SLDPRT` by accident.

## 6. Branches

| You see | It means | Do |
| --- | --- | --- |
| `open_doc` raises | T1's file is missing or open elsewhere | check the path; if T1 failed, T2 is blocked: report it, do not rebuild inside T2 |
| "opened the T1 part" fails | wrong file, or T1 was not finished | stop T2, fix T1 first |
| `CBORE` raises "no cut changed the volume" | 03-modelling.md: a plain round pocket that would not cut | cut each counterbore with `revolve(cut=True)`: plane `plane(d, 'Y', y, name)` through the hole axis, `s.rect((x, y, 3.0), (x + 5.0, y, 7.0))`, `s.centerline((x, y, 0), (x, y, 10))`, `expect_dv=math.pi*(25-2.75**2)*3` each, names `CBORE_1`..`CBORE_4` |
| `CBORE` volume is 4·π·25·3 = 942.5 | the holes are not where the counterbores are | the circles are off the holes: compare with `holes(d, 2.75)` |
| `SLOT_MID` expect fails by exactly 169.65 either way | the end circles are not at X 38 and 52 | print `holes(d, 3.0)`; fix the centres |
| floors count is not 4, or a floor is not at Z 3 | the cut went the wrong depth | the tool is plane Z 5.0, depth 4.0 mid-plane = Z 3..7; check both numbers |
| slot end faces count is 4 | the rectangle did not join the two holes into one slot | print `holes(d, 3.0)`; the rectangle must span X 38..52 exactly |
| the hash of `bracket.SLDPRT` changed | a save went to the source | rebuild T1's file with `t1.py`, rerun T2, report it |
| `tree()` raises on `GetID` | planner's untested call | it already falls back to names and types; if it still raises, log `f.Name` only |

Anything else: stop T2, write down exactly what was seen, carry on with T3 (it needs only `bracket.SLDPRT`).

## 7. Done checklist

- [ ] one body, no rebuild errors, volume within 0.1 % of 31643.00, box unchanged
- [ ] four floors measured at Z 3.000 with area 54.78 mm² each; four counterbore walls on the hole centres; slot ends at X 35..38 and 52..55
- [ ] tree before and after in the log: old features unchanged, new ones `CBORE`, `SLOT_ENDS`, `SLOT_MID`
- [ ] `bracket.SLDPRT` SHA-256 the same before and after
- [ ] picture looked at
- [ ] results.json `T2`; REPORT.md T2: what was changed and how it is known to be an edit, hand table, checks with numbers, minutes
