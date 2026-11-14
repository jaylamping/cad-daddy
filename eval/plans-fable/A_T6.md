# A / T6. Contact between two bodies (40 minutes)

Playbook: 05-fea.md "Contact between bodies" (all nine rules), "Which contact proof fits", "When the solve fails";
07-done.md study item 8 and "Do not stop early" ("what counts as a different way"); selftest.py `contact()` is the
worked example. Start a clock: at 40 minutes write up what stands.

## 1. Restatement

A PETG block (X ±20, Y ±15, Z 0..20) with a Ø10.2 hole along Y at X 0, Z 10; a Ø10 steel pin, 50 long, centred, 10 mm
out each side. Block bottom fixed; each pin end pulled up with 250 N; the pin touches the block through contact only.
Find the peak bearing stress on the hole and prove the result is a contact result.

- [ ] hand bearing value before the solve
- [ ] no-penetration contact pin to hole, real 0.1 mm radial clearance, direct sparse solver
- [ ] pin held without the contact (soft pads), pads carry under 1 % of the load
- [ ] nodes split by geometry, each body judged against its own material
- [ ] reaction = 500 N; contact force from the results against 500 N
- [ ] proof that the set is contact (a thousandth of the load in the working direction)
- [ ] keys: `hand_bearing_mpa`, `nodes`, `solver`, `how_pin_was_stabilised`, `peak_contact_vm_mpa`,
      `block_peak_at_mm`, `pin_rise_mm`, `reaction_n`, `valid`, `why`

## 2. Hand calculation

| Quantity | Working | Value |
| --- | --- | --- |
| mean bearing (key `hand_bearing_mpa`) | F / (d · L) = 500 / (10 · 30) | **1.67 MPa** |
| peak, pin a perfect fit (cosine) | 4/π · 1.67 | 2.12 MPa |
| **peak with the real clearance (Hertz, line contact)** | R* = 5 · 5.1 / 0.1 = 255 mm; E* = 1 / (0.856/1900 + 0.922/210000) = 2199 MPa; load 500/30 = 16.67 N/mm; half width b = √(4 · 16.67 · 255 / (π · 2199)) = **1.57 mm**; p0 = 2 · 16.67 / (π · 1.57) | **6.8 MPa**, along the top of the hole (X 0, Z 15.1) |
| toward the hole mouths (Y ±15) | the pin bends a little and is loaded outside the block | 10 to 50 % above 6.8: expect 7 to 10 |
| von Mises in the block under the contact | about 0.3 to 0.6 · p0, highest 0.5 to 1 mm below the surface | **2 to 6 MPa**; factor on 45 MPa over 7 |
| ligaments beside the hole, at Z 10 | 500 / (2 · 14.9 · 30) = 500 / 894 | 0.56 MPa mean σz |
| pin rise | 0.100 (the gap) + indentation and stretch, about 0.01 to 0.03 | **0.11 to 0.13 mm** |
| pads' share | shear stiffness of one pad G·A/L = 0.172 · 7.07 / 1.5 = 0.81 N/mm; two pads · 0.115 mm | 0.19 N = **0.04 %** |
| reaction | block bottom plus pads | Fz = −500 N |

Report 1.67 in `hand_bearing_mpa` (the textbook value) and give 6.8 beside it in `why` and the report: with 0.1 mm
clearance the pin bears on a strip 3.1 mm wide, not on its diameter. Agreement wanted: contact pressure at mid-length
within 25 % of 6.8 (5.1 to 8.5). Confidence in 6.8: high for mid-length; the mouth value is a guess.

Nodes: about **40,000 / 60,000 / 120,000** for hole controls 1.2 / 0.8 / 0.5 (low confidence, factor 2).

## 3. The build

Six bodies in one part (05-fea.md "A load on part of a face": separate touching bodies bond). The pin is three
touching steel pieces so that the contact face, the load faces and the pad faces are different faces:

| File | Shape | Sketch plane, circle, extrude | Volume mm³ |
| --- | --- | --- | --- |
| `block_fea.SLDPRT` | block | `plane Z 10`, `rect((-20,-15,10),(20,15,10))`, MID 20 | 24000.00 |
| | hole Ø10.2 | base plane `plane(d,'Y',0.0,..)`, `circle((0,0,10), 5.1)`, cut MID 31 | −2451.38 → 21548.62 |
| `pin_mid.SLDPRT` | Ø10, Y −17..17 | base plane Y 0, `circle((0,0,10), 5.0)`, MID 34 | 2670.35 |
| `pin_end_a.SLDPRT` / `_b` | Ø10, Y 17..25 / −25..−17 | plane Y ±21, `circle((0,±21,10), 5.0)`, MID 8 | 628.32 each |
| `pad_a.SLDPRT` / `_b` | Ø3, Y 25..26.5 / −26.5..−25 | plane Y ±25.75, `circle((0,±25.75,10), 1.5)`, MID 1.5 | 10.60 each |

```python
from common import *
from swfea import _arr

PIN_Z = 10.0                                   # 10.09 only in fallback A (section 6)

def cyl_y(j, path, y0, y1, r, feat, z=10.0):
    d = new_part(j.sw, path)
    ym = (y0 + y1) / 2
    with Sk(d, plane(d, 'Y', ym, feat + '_P'), feat) as s:
        s.circle((0, ym, z), r)
    extrude(d, s.feat, feat, y1 - y0, mode=MID, expect_dv=math.pi * r * r * (y1 - y0))
    save(d); close(j.sw, d)

def build(j):
    cyl_y(j, WIP / 'pin_mid.SLDPRT', -17, 17, 5.0, 'PINMID', PIN_Z)
    cyl_y(j, WIP / 'pin_end_a.SLDPRT', 17, 25, 5.0, 'PINEND', PIN_Z)
    cyl_y(j, WIP / 'pin_end_b.SLDPRT', -25, -17, 5.0, 'PINEND', PIN_Z)
    cyl_y(j, WIP / 'pad_a.SLDPRT', 25, 26.5, 1.5, 'SOFTPAD', PIN_Z)
    cyl_y(j, WIP / 'pad_b.SLDPRT', -26.5, -25, 1.5, 'SOFTPAD', PIN_Z)
    d = new_part(j.sw, WIP / 'block_fea.SLDPRT')
    with Sk(d, plane(d, 'Z', 10.0, 'BLOCK_P'), 'BLOCK') as s:
        s.rect((-20, -15, 10.0), (20, 15, 10.0))
    extrude(d, s.feat, 'BLOCK', 20.0, mode=MID, expect_dv=24000.0)
    with Sk(d, plane(d, 'Y', 0.0, 'HOLE_P'), 'HOLE') as s:
        s.circle((0, 0, 10.0), 5.1)
    extrude(d, s.feat, 'HOLE', 31.0, cut=True, mode=MID, expect_dv=math.pi * 5.1 ** 2 * 30)
    save(d)
    for f in ('pin_mid', 'pin_end_a', 'pin_end_b', 'pad_a', 'pad_b'):
        insert_body(d, WIP / f'{f}.SLDPRT')
    bs = bodies(d); log(bs); must('bodies', len(bs), 6)
    expect('total volume', volume(d), 21548.62 + 2670.35 + 2 * 628.32 + 2 * 10.60, 0.001)
    save(d); close(j.sw, d)
```

(`PIN_Z` changes only in fallback A of section 6. The block and its hole are always at Z 10.)

Overlap check, by numbers (insert_body does not report one): pin radius 5.0 against hole radius 5.1, same axis: gap
0.1 all round; pin pieces meet at Y ±17 and the pads at Y ±25, face to face.

## 4. The study

```python
MATS = {'pin_': STEEL, 'pad_': SOFT}

def per_node_reaction(st, res):                                  # kept as r.extra: id, Fx Fy Fz Fres, Mx My Mz Mres
    return _arr(res.GetReactionForcesAndMoments(0, NUL, 0, L()), 9)

def run(j, d, name, hole_c, f_each=250.0, loose_ok=False):
    d.ForceRebuild3(False)
    bottom = pick(d, kind='plane', normal=(0, 0, -1), at=(0, 0, 0)); must('block bottom', len(bottom), 1)
    hole = pick(d, kind='cyl', r=5.1); must('hole', len(hole), 1)
    mid = pick(d, kind='cyl', r=5.0, inside=[-5.1, -17.1, 4.8, 5.1, 17.1, 15.2]); must('pin mid face', len(mid), 1)
    ea = pick(d, kind='cyl', r=5.0, inside=[-5.1, 16.9, 4.8, 5.1, 25.1, 15.2]); must('pin end a', len(ea), 1)
    eb = pick(d, kind='cyl', r=5.0, inside=[-5.1, -25.1, 4.8, 5.1, -16.9, 15.2]); must('pin end b', len(eb), 1)
    pa = pick(d, kind='plane', normal=(0, 1, 0), at=(0, 26.5, 10)); must('pad a outer', len(pa), 1)
    pb = pick(d, kind='plane', normal=(0, -1, 0), at=(0, -26.5, 10)); must('pad b outer', len(pb), 1)
    r = static(j, d, name, PETG,
               fixtures=[('fixed', bottom), ('fixed', pa + pb)],
               loads=[('remote', ea, (0.0, 21.0, 10.0), (0, 0, f_each), (0, 0, 0)),
                      ('remote', eb, (0.0, -21.0, 10.0), (0, 0, f_each), (0, 0, 0))],
               el=3.0, ctrl=[(hole, hole_c), (mid, 1.0)],
               contacts=[(NO_PENETRATION, hole, mid)], materials=MATS, solver=SOLVER_DIRECT,
               post=per_node_reaction, loose_ok=loose_ok, max_nodes=200_000)
    save_npz(r, name)
    return r

def read(r):
    p = r.pos
    rho = np.hypot(p[:, 0], p[:, 2] - 10.0)                    # distance from the hole axis
    pin = np.hypot(p[:, 0], p[:, 2] - PIN_Z) < 5.004           # pin and pads: inside the pin's own radius
    blk = ~pin & (rho > 5.096)                                 # block: at or outside the hole wall
    if (~pin & ~blk).any():
        raise Failed('nodes inside the gap: the split by radius is not safe (05-fea.md contact rule 5)')
    crown = blk & (rho < 5.13) & (np.abs(p[:, 0]) < 0.8) & (p[:, 2] > 10)      # the strip along the top of the hole
    press = -r.s[:, 3]                                         # contact pressure there = -sigma_z
    def top(m):
        i = np.flatnonzero(m)[np.argmax(press[m])]
        return round(float(press[i]), 2), p[i].round(2).tolist()
    near = blk & (rho < 8.0) & (p[:, 2] > 10)
    lig = blk & (np.abs(p[:, 2] - 10) < 0.75) & (np.abs(p[:, 0]) > 5.1)
    out = dict(study=r.name, nodes=r.nodes, reaction=r.reaction, applied=r.applied, excessive=bool(r.excessive),
               pin_rise=float(r.disp[pin & (np.abs(p[:, 1]) < 17), 3].mean()),
               p_mid=top(crown & (np.abs(p[:, 1]) < 8)), p_mouth=top(crown & (np.abs(p[:, 1]) > 12)), p_all=top(crown),
               contact_vm=r.peak(near), block_vm=r.peak(blk & (p[:, 2] > 2.0)), block_vm_all=round(float(r.vm[blk].max()), 2),
               pin_vm=r.peak(pin & (np.abs(p[:, 1]) < 24.9)),
               lig_force=float(r.s[lig, 3].mean() * 894.0), crown_nodes=int(crown.sum()))
    try:                                                       # exact split of the reaction between block and pads
        q = r.extra
        idpos = dict(zip(r.s[:, 0].astype(int), p))
        keep = np.array([int(i) in idpos for i in q[:, 0]])
        P = np.array([idpos[int(i)] for i in q[keep, 0]])
        out['fz_block'] = float(q[keep][P[:, 2] < 0.01, 3].sum())
        out['fz_pads'] = float(q[keep][np.abs(P[:, 1]) > 26.4, 3].sum())
    except Exception as ex:                                    # logged, and the stiffness estimate is used instead
        log('per-node reaction not read:', str(ex)[:120])
        out['fz_pads_estimate'] = -2 * 0.81 * out['pin_rise']
    return out
```

`t6.py` (one job, four studies):

```python
with job() as j:
    j.simulation()
    build(j)
    d = open_doc(j.sw, WIP / 'block_fea.SLDPRT')
    res = []
    for name, hc, nodes in (('T6_PIN_12', 1.2, 40000), ('T6_PIN_08', 0.8, 60000), ('T6_PIN_05', 0.5, 120000)):
        predict(name, nodes, 0.115, 'top of the hole (x 0, z 15.1), pressure about 6.8 MPa, higher toward y +-15')
        r = run(j, d, name, hc)
        compare(name, r, nodes, 0.115)
        res.append(read(r)); log(json.dumps(res[-1], default=float))
        (HERE / 't6_rows.json').write_text(json.dumps(res, indent=1, default=float), encoding='utf-8')
    q = read(run(j, d, 'T6_PROOF', 1.2, f_each=0.25, loose_ok=True)); log('PROOF', json.dumps(q, default=float))
    close(j.sw, d)
```

Material: PETG block, steel pin (three bodies), `SOFT` pads; read the "body ... is ..." lines `static()` logs.
Solver: direct sparse; the macro log line must read `after 7`, and `block_fea-T6_PIN_12-BenchMark-Solver.txt` beside
the model names the solver: put that name in `solver`.

Checks, in order, on `T6_PIN_12` before waiting for the finer ones:

1. `reaction[2]` = −500 ± 5; Fx, Fy within ± 5.
2. `pin_rise` between 0.10 and 0.14 mm. (Under 0.10: contact engaged before the gap closed, or the pin is bonded.
   Over 0.2: the contact did not stop the pin.)
3. `fz_block` = −500 ± 5 (this is the contact force: everything the block's fixture reacts came through the hole);
   `fz_pads` magnitude under 5 N (1 %). `lig_force` between 400 and 650 N (node mean, reads high near the hole).
4. `p_mid[1]` and `p_mouth[1]`: X within ±0.8 and Z about 15.1, on the top of the hole. `contact_vm[1]` within 3 mm of
   the top of the hole. `block_vm[1]` should be the same place; if it is at the hole sides (X ±5.1, Z 10) or the
   bottom, report it as it is.
5. `pin_vm[0]` is judged against steel (640 MPa), not PETG.

Series: `p_mid[0]`, `p_all[0]` and `contact_vm[0]` over the three hole controls. Converged = the last step moves
each by 5 % or less.

Proof (`T6_PROOF`, 0.25 N per end = a thousandth): 05-fea.md "Which contact proof fits", third case. Expect
`pin_rise` 0.09 to 0.11 mm: the pin crosses the gap and stops at the wall. Full load gave about 0.115, so a
thousandth of the load moves the pin almost as far: not proportional, which a bond could never do (a bond would give
0.000115 mm). Also say: with no contact set at all the pads alone would let the pin rise 500 / 1.62 = 300 mm.

Keys: `nodes` = finest; `peak_contact_vm_mpa` = `contact_vm[0]` at the finest; `block_peak_at_mm` = `block_vm[1]`;
`pin_rise_mm`; `reaction_n` = `reaction[3]`; `how_pin_was_stabilised` = "two soft pads (Ø3 × 1.5 mm, modulus 0.5 MPa)
bonded to the pin's end faces with their outer faces fixed, clear of the block; they carried N newtons of 500";
`valid` = true only if checks 1 to 4 hold, the proof holds, the series converged, and `p_mid` is within 25 % of 6.8;
`why` = those numbers in one sentence, and the peak bearing stress: `p_all` at the finest mesh with its place, with
`p_mid` beside it.

## 5. Decisions made for you

- **"Each end pulled up" is a rigid remote load on the cylinder face of each end piece,** acting at its middle
  (0, ±21, 10). Rigid is right here: the piece is steel, 100 times stiffer than what it loads.
- **The pin is split at Y ±17, 2 mm outside the block,** so the junction between pin pieces is not at the hole
  mouth where the pressure peaks.
- **Pads on the pin's end faces, not near the hole** (05-fea.md contact rule 2: pads on the loose body, clear of the
  other one). Sized so that they carry 0.04 % at full load and still let the pin cross the gap at a thousandth.
- **The gap is modelled as it is** (0.1 mm radial), not line to line (contact rule 3).
- **What "bearing stress" is reported:** the contact pressure on the hole (−σz along its top) as the answer to the
  task, and the block's von Mises there for the key that asks for it.
- **If the pressure at the mouths keeps climbing while mid-length has converged:** report mid-length as converged,
  the mouth as an edge concentration with its trend, `valid` true for mid-length only, and say so in `why`. The
  hole mouth is a sharp edge; a printed one has about 0.4 mm radius.

## 6. Branches

| You see | It means | Do |
| --- | --- | --- |
| `static` raises "excessive displacements" on a full-load run | the solver asked before the contact closed, or the pin is free | rerun that study with `loose_ok=True`. If `pin_rise` is then 0.10 to 0.14 and the reaction −500: the result stands (say the prompt came). If the rise is millimetres: the contact set is not working, next row |
| pin rise of millimetres or more, or error 24 at once | the pin is held by nothing: contact not engaged, or pads not bonded | read the body-material log (pads must be `Soft pad`), `bodies(d)` (pads must touch the pin ends: boxes Y 25..26.5). Then fallback A |
| "Failure to achieve equilibrium" (static raises) | the contact iteration ran out | fallback A |
| **fallback A (a different model of the gap):** | | set `PIN_Z = 10.09` and run `build(j)` again in a new job (the pin and pads are drawn 0.09 mm higher: 0.01 mm clearance at the top, 0.19 at the bottom). The contact closes at once. Everything else the same; `pin_rise` then 0.02 to 0.05. Say in `how_pin_was_stabilised` that the pin was seated |
| **fallback B (if A fails too):** | | hold the pin by symmetry instead of pads is not available in the helpers; instead make the pads stiffer by geometry, not modulus: Ø8 × 1 mm pads (shear 8.7 N/mm each, 2 N of 500 = 0.4 %), and run the proof at 5 N per end instead of 0.25 |
| after A and B both fail | three ways tried | stop. Report each try with its log tail and the hand value 6.8 MPa as the only result; `valid` false; `status` partial |
| pin rise under 0.09 with the gap model | the pin is bonded somewhere | the hole face or pin face is not in the contact set, or pin_mid is longer than drawn; print both picks' boxes |
| `read` raises "nodes inside the gap" | a body is not where it should be | `bodies(d)` and their boxes; do not report |
| `fz_pads` over 5 N | pads too stiff | they are `SOFT`? the material log says. If so report the share and say the result carries that error |
| `p_mid` under 4 at the finest mesh, falling | elements too large for a 3.1 mm strip, or the pin is seated on its sides | check `crown_nodes` (over 50 at control 0.5); look at where `p_all` is |
| `p_mid` over 10, or climbing more than 5 % at the last step | not converged | one more study, hole control 0.35, in a **new job** (the fifth study), if the predicted nodes (about 220,000) fit under 200,000 after raising `el` to 4.0. If not: report the series, `valid` false, "not shown" |
| mesh refused over 200,000 at control 0.5 | cap | `el=4.0` for that study; if still over, hole control 0.6 |
| `materials keys ... match no body` | body names differ from `<file>-<feature>` | read the logged names; pick keys that match the three pin bodies, and the two pads, and not the block |
| solver macro raises | RunMacro2 failed | read its message; 05-fea.md contact rule 1. Do not fall back to Automatic silently: if you must, say so and expect a stall |
| 40 minutes used | time limit | stop, write what stands: which studies ran, their numbers, what failed |

Anything else: stop T6, write down exactly what was seen, carry on with T7 or set D.

## 7. Done checklist

- [ ] hand table; which hand value the study is compared with and why
- [ ] bodies, materials log, solver named from the benchmark log
- [ ] reaction; `fz_block` against 500; pads' share in N and %
- [ ] pin rise; node split guard passed; pin judged as steel
- [ ] contact pressure (mid, mouth, overall) and block von Mises with places, for three meshes; converged or not
- [ ] the proof run's rise beside the full-load rise
- [ ] three measures for the block are not required by the task; give the block's factor on yield (45 / `block_vm`)
      and note that tension across layers was not judged (no print direction given; the stress is compressive under the pin)
- [ ] what was not verified: friction (none modelled), the mouth edge, the pin's own bending stress convergence
- [ ] `put('T6', hand_bearing_mpa=1.67, nodes=..., solver=..., how_pin_was_stabilised=..., peak_contact_vm_mpa=...,
      block_peak_at_mm=..., pin_rise_mm=..., reaction_n=..., valid=..., why=..., status=..., notes=...)`; REPORT.md T6
      with minutes used of the 40
