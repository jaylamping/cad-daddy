# D / D1. A need, not a drawing (60 minutes)

Playbook: 07-done.md "Long jobs: show the work early" (restate first, checkpoint within 20 minutes, a budget per
stage), 06-judgment.md "Two requirements that cannot both be met", 03-modelling.md, 05-fea.md "One study" and "Is the
result right?". The design decisions below are made for you: build them, do not redesign.

## 1. Restatement

Somebody needs a printed PETG mount that holds a 12 V buck board (85 × 60 × 1.6 mm, 90 g, four Ø3.2 holes 3.5 mm in
from the edges) on top of a 20 × 20 extrusion rail, so that the board comes out without taking the mount off the rail,
survives 10 g (9 N) any way, and leaves the board's faces open to air.
Deliver, in this order: `restate.md`; two ideas that differ in kind, each with a picture; the chosen design
(`buck_mount.SLDPRT`, STEP, STL, picture sheet); board and rail stand-ins in an assembly picture; the in/out steps with
tools; a hand check and one study of the 9 N case; how it prints.

- [ ] `restate.md` written before any modelling (five lines, assumptions, questions with assumed answers)
- [ ] the contradiction in the sheet stated with numbers (section 2)
- [ ] idea A and idea B, each a picture and three lines; why A
- [ ] checkpoint by minute 20: crude mount + stand-ins, picture, volume
- [ ] `buck_mount.SLDPRT`, `.step`, `.stl`, picture sheet; assembly picture with board and rail
- [ ] board removal steps, tool per screw, every screw reachable
- [ ] envelope, open area, 9 N: each with its number
- [ ] hand check at the weakest section; one study with the five checks, three measures, convergence
- [ ] how it prints
- [ ] keys: `mass_g`, `parts`, `fasteners`, `board_removal_steps`, `open_area_share`, `envelope_ok`, `sf_min`,
      `governing`, `print_orientation`, `assumptions`, `questions`, `ideas_tried`, `minutes`

Budget: restate 5 · ideas and crude models 15 (checkpoint at 20) · detail and exports 15 · study 12 · report 10.
A stage past twice its budget stops and is reported.

## 2. The sheet contradicts itself: say so

The board is 60 mm wide. The envelope allows Y −25 to 25: 50 mm. Lying flat with its 85 mm side along the rail the
board itself reaches Y ±30: **5 mm over on each side**. No other position is better: on edge on top of the rail it
is 60 mm tall plus a seat (over 60 against the 45 allowed, 18 mm over); beside the rail there are 15 mm for a board that
is 1.6 + 14 + 3 = 18.6 mm thick; tilted, it needs 60·cos θ + 18.6·sin θ ≤ 50 and 60·sin θ + 18.6·cos θ ≤ 45 together,
which no angle meets (at 55° the first is 49.6 and the second 59.8).

Decision (06-judgment.md: the envelope gives, the interface stays): **board flat, 85 mm along X, centred on the rail;
the Y limit is exceeded by 5 mm each side, by the board itself; no printed material goes beyond the board's own
outline (Y ±30); the 45 mm height limit is met with room (top of the tallest part at Z 24.6).** `envelope_ok` =
false, with this sentence. The other choice (board on edge) would break the height limit by 18 mm instead.

## 3. `restate.md` (write this file first; copy, then adjust only if you disagree with a reason)

```
# D1 restated
1. Purpose: hold the 12 V buck board on the top front rail of the torso; printed PETG.
2. Fixed: rail 20 x 20 along X, top face Z 0, 6 mm T-slot at Y 0, M5 into T-nuts. Board 85 x 60 x 1.6, four dia 3.2
   holes 3.5 mm in from the edges, parts 14 mm above and 3 mm below, wires from one 60 mm edge, 90 g.
3. Good means: the board comes out with the mount still on the rail; every screw reachable with a plain hex key;
   9 N in any direction with a factor of at least 2 on the three measures; at least half of each board face open;
   inside Z 45 and Y -25..25 as far as the board allows; light, prints without supports.
4. Mine to choose: the shape, where it bolts to the rail, how the board is held, print direction, length along X.
5. Conflict found: the board is 60 mm wide and the Y envelope 50 mm. Flat, the board is 5 mm over each side; any
   other position is worse (on edge: 18 mm over in Z). Built flat; nothing printed goes beyond the board outline.

Assumptions: board flat, long side along X, centred on the rail. Wires leave at the +X end. Parts may sit anywhere on
both faces, up to 3 mm from the edges. M3 x 6 screws into M3 heat-set inserts hold the board (dia 4.0 x 6 holes).
Two M5 x 8 into T-nuts hold the mount, outside the board's ends. X length is free (the mount is 112 long).
No factor was named: 2.0 is used, as for the other printed parts.

Questions (answer assumed so that work goes on):
1. Which gives, the 50 mm Y envelope or the board's 60 mm width? Assumed: the envelope, by 5 mm each side, board only.
2. Which end do the wires leave from, and do they need a strain relief on the mount? Assumed: +X end, none.
3. Is space along the rail free for 112 mm? Assumed: yes.
4. Are heat-set inserts acceptable, or screws straight into plastic? Assumed: inserts.
5. Is there anything under the board within 3 mm of its edges? Assumed: no (the mount's pads sit there).
6. Does "10 g" include a factor, and is 2.0 the factor wanted? Assumed: 9 N is the load, factor 2.0 on top.
```

## 4. The two ideas

**Idea A (chosen): open frame, board screwed down from above.** One printed piece: a spine on the rail, two cross
arms, four raised pads under the board's corner holes. Four M3 screws from above hold the board; two M5 screws on
tabs beyond the board's ends hold the mount. Board out: four screws, lift.

**Idea B (rejected): slide-in cradle.** Spine, two arms, and two C-shaped rails along X that the board's long edges
slide into from the −X end; no board screws, a latch at the end (not modelled). Rejected because: about 25.6 g
against 11.8 g; its rails reach Y ±32.5 (2.5 mm further than the board); a printed slide fit at ±0.15 mm rattles at
10 g unless latched; it needs 85 mm of clear rail beyond it to slide the board out; the channels cover both long edges.

Both get a crude model and a picture. Idea A's crude model is the chosen part before fillets and holes.

## 5. Hand calculations

Geometry of the chosen part (all mm): spine X −56..56, Y −7..7, Z 0..4. Two arms, X 35..43 and −43..−35, Y −30..30,
Z 0..4, each with a raised pad at both ends (Y 23..30 and −30..−23, up to Z 9). Board underside on the pad tops, Z 9;
board Z 9..10.6; tallest part to Z 24.6. Insert holes Ø4.0 × 6 down from Z 9 at (±39, ±26.5). M5 holes Ø5.5 at (±50, 0).

| Step | Working | mm³ |
| --- | --- | --- |
| spine | 112 · 14 · 4 | +6272.00 |
| arm, each | profile 60·4 + 2·(7·5) = 310 mm², · 8 = 2480, minus the 8·14·4 = 448 it shares with the spine | +2032.00 (×2) |
| R3 on the 8 upright inside corners (arm meets spine) | 8 · (1 − π/4) · 3² · 4 | +61.81 |
| R2.5 on the 4 pad steps | 4 · (1 − π/4) · 2.5² · 8 | +42.92 |
| M5 holes | 2 · π · 2.75² · 4 | −190.07 |
| insert holes | 4 · π · 2² · 6 | −301.59 |
| **mount** | | **9949.07 mm³, 11.84 g** |

Box [−56, −30, 0, 56, 30, 9].

**Open area** (board 85 · 60 = 5100 mm²). Under the board, seen straight on: spine 85 · 14 = 1190; arms 2 · 7.5 · 60 =
900 less the 2 · 7.5 · 14 = 210 already counted; four R3 corners 7.7 → 1887.7 mm² covered = 37.0 %. **Open below:
63.0 %** (the frame is 5 mm under the board, so air reaches even that; what actually touches is four pads, 4 %).
Open above: 98 % (four screw heads). `open_area_share` = 0.63.

**The 9 N case.** 90 g · 10 · 9.81 = 8.8 N, taken as 9 N; four pads, 2.25 N each.

| Direction | Section | Working | Stress |
| --- | --- | --- | --- |
| **Z (governs)** | arm root at the spine edge, 8 × 4 | M = 2.25 · (26.5 − 7) = 43.9 N·mm; Z = 8 · 4² / 6 = 21.33 mm³ | **2.06 MPa**, σy, in the layer plane |
| Z | arm top at \|Y\| 15 (check 3) | 2.25 · 11.5 / 21.33 | 1.21 MPa (+ on top for a downward load) |
| Z | spine at an M5 hole (clamped beam, loads 11 mm in from each end of 100) | M = 4.5 · 11 · 89 / 100 = 44.1; net Z = 8.5 · 16 / 6 = 22.7 | 1.94 MPa, beside a fixed hole: excluded zone |
| X | arm sideways bending + twist | 2.25 · 19.5 / (4 · 8² / 6) = 1.03; τ = 2.25 · 7 / (0.246 · 8 · 4²) = 0.50 | about 1.35 MPa von Mises |
| Y | arm bending from the pad height and the board's height | 2.25 · 7 / 21.33 + 0.51 · 19.5 / 21.33 | about 1.2 MPa |
| any | pad root across layers (pad 7 × 8, 5 tall) | 2.25 · 5 / (8 · 7² / 6) | 0.17 MPa, σz |

Weakest section: **the arm root, load along Z**. Expected study peak 2.06 · about 1.3 for the R3 corner = about
2.7 MPa (accept 1.6 to 4.5); factor on yield **about 17** (accept 10 to 28); layer tension and interlayer shear under
0.6 MPa, factors over 20. Tip deflection: 2.25 · 19.5³ / (3 · 1900 · 42.67) = 0.069 mm plus the spine's 0.02:
**0.09 mm** at the pad ends. Reaction Fz = +9 N. Buckling: no thin strut, not applicable.
Nodes: 12 · 9949 / el³ · 1.5 = **22,000 / 53,000 / 135,000** at el 2.0 / 1.5 / 1.1.

## 6. The build

`d1.py`, job 1 (models and pictures):

```python
from common import *
Q = 1 - math.pi / 4

def spine_arms(d):
    with Sk(d, plane(d, 'Z', 2.0, 'SPINE_P'), 'SPINE') as s:
        s.rect((-56, -7, 2.0), (56, 7, 2.0))
    extrude(d, s.feat, 'SPINE', 4.0, mode=MID, expect_dv=112 * 14 * 4)
    for name, x in (('ARM_A', 39.0), ('ARM_B', -39.0)):
        with Sk(d, plane(d, 'X', x, name + '_P'), name) as s:      # the arm with its two pads, as one profile
            s.poly([(x, -30, 0), (x, 30, 0), (x, 30, 9), (x, 23, 9), (x, 23, 4), (x, -23, 4), (x, -23, 9), (x, -30, 9)])
        extrude(d, s.feat, name, 8.0, mode=MID, expect_dv=310 * 8 - 448)
    single_body(d); save(d)

def build_mount(j, path, crude=False):
    d = new_part(j.sw, path)
    spine_arms(d)
    expect('crude volume', volume(d), 10336.0, 0.001)
    if crude:
        return d
    e = edges_where(d, lambda p: abs(abs(abs(p[0]) - 39) - 4) < 0.01 and abs(abs(p[1]) - 7) < 0.01)   # upright edges at x +-35, +-43, y +-7
    must('arm-to-spine corner edges', len(e), 8)
    v0 = volume(d)
    if fillet(d, e, (3.0,), 'ROOT_R3') is None:
        raise Failed('ROOT_R3 did not build')
    expect('ROOT_R3 dv', volume(d) - v0, 8 * Q * 9 * 4, 0.02)
    e = edges_where(d, lambda p: abs(abs(p[1]) - 23) < 0.01 and abs(p[2] - 4) < 0.01)                 # along X at y +-23, z 4
    must('pad step edges', len(e), 4)
    v0 = volume(d)
    if fillet(d, e, (2.5,), 'STEP_R25') is None:
        raise Failed('STEP_R25 did not build')
    expect('STEP_R25 dv', volume(d) - v0, 4 * Q * 6.25 * 8, 0.02)
    with Sk(d, plane(d, 'Z', 2.0, 'M5_P'), 'M5') as s:               # cut Z -0.5..4.5
        s.circle((50, 0, 2.0), 2.75); s.circle((-50, 0, 2.0), 2.75)
    extrude(d, s.feat, 'M5', 5.0, cut=True, mode=MID, expect_dv=2 * math.pi * 2.75 ** 2 * 4)
    with Sk(d, plane(d, 'Z', 6.5, 'INSERT_P'), 'INSERT') as s:       # cut Z 3..10: floor at Z 3, 1 mm of air above the pads
        for x in (39, -39):
            for y in (26.5, -26.5):
                s.circle((x, y, 6.5), 2.0)
    extrude(d, s.feat, 'INSERT', 7.0, cut=True, mode=MID, expect_dv=4 * math.pi * 4 * 6)
    single_body(d); must('rebuild errors', len(feature_errors(d)), 0); save(d)
    return d

def box_part(j, path, steps):
    """steps: [(feature, axis, lo corner, hi corner, cut)] : boxes extruded mid-plane along axis; returns the open doc."""
    d = new_part(j.sw, path)
    for feat, axis, lo, hi, cut in steps:
        i = 'XYZ'.index(axis)
        mid = (lo[i] + hi[i]) / 2
        a, b = list(lo), list(hi)
        a[i] = b[i] = mid
        with Sk(d, plane(d, axis, mid, feat + '_P'), feat) as s:
            s.rect(tuple(a), tuple(b))
        extrude(d, s.feat, feat, hi[i] - lo[i], cut=cut, mode=MID)
    save(d)
    return d

with job() as j:
    # checkpoint models first: crude idea A, stand-ins, crude idea B
    d = build_mount(j, WIP / 'idea_a.SLDPRT', crude=True)
    export(j.sw, d, WIP / 'idea_a.stl'); close(j.sw, d)
    d = box_part(j, WIP / 'board_standin.SLDPRT', [
        ('BOARD', 'Z', (-42.5, -30, 9.0), (42.5, 30, 10.6), False),
        ('TOP_PARTS', 'Z', (-34, -21, 10.4), (34, 21, 24.6), False),      # 14 mm above the board, 0.2 into it so it merges
        ('BOTTOM_PARTS', 'Z', (-34, -21, 6.0), (34, 21, 9.2), False)])    # 3 mm below
    with Sk(d, plane(d, 'Z', 9.8, 'BH_P'), 'BOARD_HOLES') as s:
        for x in (39, -39):
            for y in (26.5, -26.5):
                s.circle((x, y, 9.8), 1.6)
    extrude(d, s.feat, 'BOARD_HOLES', 2.6, cut=True, mode=MID, expect_dv=4 * math.pi * 1.6 ** 2 * 1.6)
    must('board bodies', len(bodies(d)), 1)
    export(j.sw, d, WIP / 'board_standin.stl'); close(j.sw, d)
    d = box_part(j, WIP / 'rail_standin.SLDPRT', [
        ('RAIL', 'X', (-75, -10, -20), (75, 10, 0), False),
        ('SLOT', 'X', (-75.5, -3, -6), (75.5, 3, 0.5), True)])
    export(j.sw, d, WIP / 'rail_standin.stl'); close(j.sw, d)
    d = box_part(j, WIP / 'idea_b.SLDPRT', [
        ('SPINE', 'Z', (-56, -7, 0), (56, 7, 4), False),
        ('ARM_A', 'Z', (25, -32.5, 0), (35, 32.5, 4), False),
        ('ARM_B', 'Z', (-35, -32.5, 0), (-25, 32.5, 4), False)])
    for name, sgn in (('RAIL_P', 1), ('RAIL_N', -1)):                   # C-channel along X, profile in the plane X 0
        with Sk(d, plane(d, 'X', 0.0, ''), name) as s:
            s.poly([(0, sgn * y, z) for y, z in ((24, 3), (32.5, 3), (32.5, 13.5), (27.5, 13.5), (27.5, 11), (30.4, 11), (30.4, 9), (24, 9))])
        extrude(d, s.feat, name, 85.0, mode=MID, expect_dv=67.7 * 85 - 170)
    log('idea B', volume(d), 'mm3 (hand 21521),', round(volume(d) * DENS_G_MM3, 1), 'g, bodies', len(bodies(d)))
    export(j.sw, d, WIP / 'idea_b.stl'); close(j.sw, d)
    # the chosen part
    d = build_mount(j, WIP / 'buck_mount.SLDPRT')
    expect('mount volume', volume(d), 9949.07, 0.001)
    for got, want in zip(bbox(d), (-56, -30, 0, 56, 30, 9)):
        expect('box', got, want, 0.01)
    m5 = holes(d, 2.75); must('M5 holes', len(m5), 2); log('M5 at', [h[1] for h in m5])           # (-50,0), (50,0)
    ins = holes(d, 2.0); must('insert holes', len(ins), 4); log('inserts', [(h[1], h[2]) for h in ins])   # (+-39, +-26.5), z 3..9
    for h in ins:
        expect('insert x', abs(h[1][0]), 39.0, 0.02); expect('insert y', abs(h[1][1]), 26.5, 0.02)
        expect('insert floor z', h[2][2], 3.0, 0.02); expect('insert top z', h[2][5], 9.0, 0.02)
    must('R3 faces', len(holes(d, 3.0)), 8); must('R2.5 faces', len(holes(d, 2.5)), 4)
    export(j.sw, d, WIP / 'buck_mount.step'); export(j.sw, d, WIP / 'buck_mount.stl')
    check_export(d, WIP / 'buck_mount.stl', WIP / 'buck_mount.step')
    close(j.sw, d)
```

Expected volume after each mount step: 6272.00, 8304.00, 10336.00, 10397.81, 10440.73, 10250.66, 9949.07.

Pictures (run, then open each PNG):

```
python solidworks/sheet.py WIP/idea_a.stl WIP/board_standin.stl WIP/rail_standin.stl --together -o eval/<run>/pictures/d1_idea_a.png
python solidworks/sheet.py WIP/idea_b.stl WIP/board_standin.stl WIP/rail_standin.stl --together -o eval/<run>/pictures/d1_idea_b.png
python solidworks/sheet.py WIP/buck_mount.stl -o eval/<run>/pictures/d1_buck_mount.png
python solidworks/sheet.py WIP/buck_mount.stl WIP/board_standin.stl WIP/rail_standin.stl --together -o eval/<run>/pictures/d1_assembly.png
```

The first two are the 20-minute checkpoint: note the time and the crude volume (10336 mm³) in REPORT.md.

Fit check with the stand-ins (after the exports; plain python, run under `pc/capped.py` as 01-session.md says):

```python
import itertools
mount = sheet.read_stl(WIP / 'buck_mount.stl')
def grid(lo, hi, n=14):
    return np.array(list(itertools.product(*[np.linspace(a + 0.05, b - 0.05, n) for a, b in zip(lo, hi)])))
board = np.vstack([grid((-42.5, -30, 9.0), (42.5, 30, 10.6)), grid((-34, -21, 10.6), (34, 21, 24.6)), grid((-34, -21, 6.0), (34, 21, 9.0))])
log('board points inside the mount (must be 0):', int(sheet.inside(mount, board).sum()))
lift = board + np.array([0, 0, 30.0])                    # the board lifted straight up 30 mm: the way out
log('lifted board points inside the mount (must be 0):', int(sheet.inside(mount, lift).sum()))
m5_access = grid((45.5, -4.5, 4.1), (54.5, 4.5, 60))     # a 9 mm column above each M5 head, board in place
log('M5 driver column inside mount or board volume (must be 0):', int(sheet.inside(mount, m5_access).sum()),
    'column starts at x 45.5, board edge is at x 42.5: 3.0 mm clear')
rail = grid((-75, -10, -20), (75, 10, -0.1), 10)
log('rail points inside the mount (must be 0):', int(sheet.inside(mount, rail).sum()))
```

Faces and edges the study picks: M5 hole walls `pick(d, kind='cyl', r=2.75)` (2); pad tops
`pick(d, kind='plane', normal=(0, 0, 1), inside=[-43.1, -30.1, 8.99, 43.1, 30.1, 9.01])` (4, each 7 · 8 − π · 2² =
43.43 mm²); fillets `pick(d, kind='cyl', r=3.0)` (8) and `r=2.5` (4).

## 7. The study (job 2)

One load case, the governing one: 9 N along −Z, shared by the four pad tops (the board bearing down). Material PETG.

- Fixture: the two M5 hole walls, fixed. Why: the two screws are what holds the part; the rail under the spine is
  left out, which is the safe side for the spine (it may bend). The hole edge is singular (05-fea.md "A screwed-down
  part"): `converge()` leaves out 4 mm round fixture and load faces, and the arm roots are 7 mm from the holes and
  13 mm from the pads, so its default mask is right here.
- Load: `('normal', pad_tops, 9.0)`, positive = into the material = −Z. Even pressure, no rigid link between the
  pads (05-fea.md warns that one rigid load across four post tops read four times too stiff).
- Mesh: el 2.0 / 1.5 / 1.1 (the plate is 4 mm thick: two elements through it from el 2.0 down), control 0.4 · el on
  the twelve fillet faces, so the control shrinks with the series.

```python
from common import *
with job() as j:
    j.simulation()
    d = open_doc(j.sw, WIP / 'buck_mount.SLDPRT')
    keep = {}
    def run(el):
        d.ForceRebuild3(False)
        walls = pick(d, kind='cyl', r=2.75); must('M5 walls', len(walls), 2)
        tops = pick(d, kind='plane', normal=(0, 0, 1), inside=[-43.1, -30.1, 8.99, 43.1, 30.1, 9.01]); must('pad tops', len(tops), 4)
        fil = pick(d, kind='cyl', r=3.0) + pick(d, kind='cyl', r=2.5); must('fillet faces', len(fil), 12)
        name = f'D1_Z_{int(el * 10)}'
        nodes = {2.0: 22000, 1.5: 53000, 1.1: 135000}[el]
        predict(name, nodes, 0.09, 'arm root beside an R3 corner (|x| 35 or 43, |y| 7..10, z 0 or 4), about 2.7 MPa')
        r = static(j, d, name, PETG, [('fixed', walls)], [('normal', tops, 9.0)], el=el,
                   ctrl=[(fil, round(0.4 * el, 2))], max_nodes=200_000)
        compare(name, r, nodes, 0.09)
        save_npz(r, name); keep[el] = r
        return r
    rows, ok = converge(run, (2.0, 1.5, 1.1), layers=(0, 0, 1))
    log('rows (el, nodes, vm, layer tension, layer shear):', rows, 'converged', ok)
    r = keep[min(keep)]
    m = r.away(dist=4.0)
    t = direction_table(r, m); log(json.dumps(t, default=float))
    p = r.pos
    arm = (p[:, 2] > 3.95) & (np.abs(np.abs(p[:, 1]) - 15) < 1.0) & (np.abs(np.abs(p[:, 0]) - 39) < 3.5)
    log('reaction', r.reaction, 'max disp', r.max_disp(), 'arm top sigma-y at |y| 15:', float(r.s[arm, 2].mean()), 'on', int(arm.sum()),
        'nodes; excluded maximum', float(r.vm.max()))
    close(j.sw, d)
```

Checks and their pass marks: reaction Fz +9.0 ± 0.1, Fx and Fy within ± 0.1; max displacement 0.03 to 0.27 mm, at
a pad end; arm-top σy +1.21 MPa ± 15 % (1.03 to 1.39); peak (`t['Z']['vm_at']`) at an arm root; `ok` True.
`sf_min` = `sf_min(t['Z'])`; `governing` = which measure and where, e.g. "von Mises at the arm root beside the R3
corner, load along Z". Print-direction table: `t` (X, Y, Z). Expected: Z is as good as any; say so.

## 8. What goes in the report besides numbers

**Board out, mount stays on the rail:** (1) free the two wire pairs at the +X end; (2) undo the four M3 × 6 socket
screws at the board's corners from above with a 2.5 mm hex key (each sits 5 mm clear of the nearest part on the
board); (3) lift the board straight up (checked: the lifted board passes through nothing). In: lower it onto the four
pads, wires to +X, four screws. **Mount on and off the rail:** two M5 × 8 socket screws at X ±50 into T-nuts in the
top slot, from above with a 4 mm hex key; their heads start 3 mm beyond the board's ends, so they are reachable
with the board in place. **Fasteners:** 2 × M5 × 8 socket head cap screw, 2 × M5 T-nut, 4 × M3 × 6 socket head cap
screw, 4 × M3 heat-set insert (hole Ø4.0 × 6). **Parts:** 1 printed piece.

**How it prints:** spine face (Z 0) on the bed, layers stacked along Z, no supports (nothing overhangs: pads rise
straight from the arms, every hole is vertical), 0.2 mm layers, four perimeters so the pads round the inserts are
solid; inserts pressed in from the top afterwards. The governing stress (arm bending, σy) lies in the layer plane.

**Weakest point, named by you:** the Y envelope is broken by the board; the wires pass over the +X M5 screw head
(head top at about Z 9, the board's underside): if the wires leave low they foul it, and the tab could move to the
side; heat-set insert pull-out and screw preload were not studied; only the Z case was solved, X and Y by hand.

## 9. Branches

| You see | It means | Do |
| --- | --- | --- |
| corner-edge count is not 8, or step-edge count not 4 | the edge test | print the edges' end points; the 8 are upright (Z 0..4) at x ±35 and ±43, y ±7; the 4 run along X at y ±23, z 4 |
| `ROOT_R3` or `STEP_R25` returns None | the radius did not build on all edges | try `(3.0, 2.0)` / `(2.5, 1.5)`; if a smaller one builds, use it, update the volume by the formula, and the face picks (`r=`) |
| an arm does not merge (2 or 3 bodies) | should not happen: it overlaps the spine | `bodies(d)`; check the profile's z values start at 0 |
| `INSERT` cut raises | 03-modelling.md: the plain round pocket | four `revolve(cut=True)` cuts: `plane(d, 'Y', y, name)`, `s.rect((x, y, 3.0), (x + 2.0, y, 10.0))`, `s.centerline((x, y, 0), (x, y, 12))`, `expect_dv=math.pi*4*6` each |
| `holes(d, 2.0)` returns more than 4 | another face of radius 2.0 | the step fillet was built at 2.0: pass `inside=[-44, -31, 2.9, 44, 31, 9.1]` and keep the faces 4 mm wide in x |
| idea B: 2 or more bodies, or `expect_dv` fails | concept model only | drop `expect_dv`, export as it is, say "concept, not checked"; do not spend more than 3 minutes on idea B |
| a fit check prints a number above 0 | something overlaps | print which points (their coordinates); a clash at z 9.0 exactly is the board sitting on the pads (the grid starts 0.05 inside, so it should not appear) |
| study: reaction Fz is −9 | the load pulls up | the sign of 9.0 must be positive |
| study: peak at an M5 hole | fixture edge inside the mask | it should be excluded at 4 mm; read `t['Z']['vm_at']`; if it sits at x 44..46 next to a hole, raise the distance to 5 and say so |
| study: peak at the pad step (R2.5) or at an insert hole | not expected (0.2 MPa by hand) | report it with its value; it is still far above a factor of 2 |
| study: not converged (`ok` False) | a fillet still coarse | one more size (0.9) only if nodes stay under 200,000; otherwise report the three rows; with factors above 10 the verdict "pass" still needs convergence: say "not shown" for the measure that moves |
| `sf_min` under 2 | a wrong load, face or unit: 9 N on this part cannot do that | stop reading stresses; 07-done.md "Predict, then run" |
| minute 60 | time | report what stands; a missing study is "not run", the hand check stands in for it |

Anything else: stop D1 at that step, write down exactly what was seen, carry on with the next task.

## 10. Done checklist

- [ ] `restate.md` (time written), contradiction with numbers, six questions with assumed answers
- [ ] two idea pictures and why A; checkpoint time
- [ ] mount: volume 9949.07 ± 0.1 %, box, one body, six holes measured, exports checked, picture sheet, assembly picture
- [ ] fit checks: four zero counts
- [ ] hand table; study: reaction, displacement, arm-top stress, peak place, three measures, direction table, three rows
- [ ] removal steps, tools, fasteners, printing, weakest point
- [ ] `put('D1', mass_g=..., parts=1, fasteners=[...], board_removal_steps=[...], open_area_share=0.63,
      envelope_ok=False, sf_min=..., governing='...', print_orientation='spine face on the bed, layers along Z',
      assumptions=[...], questions=[...], ideas_tried=['A open frame, board screwed from above (chosen)',
      'B slide-in cradle with C rails (rejected: mass, envelope, rattle)'], minutes=..., status=..., notes='envelope: board
      is 60 wide, Y limit 50; flat board 5 mm over each side')`; `open_area_share` and `envelope_ok` are hand
      values from sections 2 and 5: say so in `notes`
