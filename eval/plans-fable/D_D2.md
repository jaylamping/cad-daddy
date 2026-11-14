# D / D2. Two halves round a bearing (90 minutes)

Playbook: 05-fea.md "Contact between bodies", "Which contact proof fits" (first case: a body seated on both sides),
"Screws and clamped joints", "When the node cap and convergence meet", "Forces from a result"; 06-judgment.md "Two
requirements that cannot both be met" and "A number you cannot explain"; 07-done.md "Long jobs" and study item 8.
This is the hardest task. The design decisions are made below; build them. Planner's confidence in the build: medium;
in the contact studies running first time: low. The order below banks the parts that are certain first.

## 1. Restatement

Two printed PETG halves, split on Y 0, clamp the outer ring of a 6808-2RS bearing (40 × 52 × 7; inner ring 44.0 outside,
outer ring 48.0 inside; axis Z) with four M3 screws along Y; the lower half mounts by its face Y −32. 300 N on the
bearing along +Y, and along +X; factor 2.0 on the three measures in both halves.
Deliver: the problems in the specification with numbers; `housing_upper.SLDPRT`, `housing_lower.SLDPRT`, `ring.SLDPRT`,
an STL of each half, three picture sheets; a fit check; two contact load cases shown valid; the screw load by hand and
from the study.

- [ ] `spec_problems` with numbers and what was built instead (section 2), written before modelling
- [ ] both halves and the ring built, volumes against hand, every hole measured
- [ ] fit: what touches, what clears, by how much, inner ring included (`clearances_mm`)
- [ ] +Y and +X studies with contact ring-to-seat and half-to-half, screws as steel pins, every body held
- [ ] contact proved (bonded twin), pads' share, screw load against hand within 15 % or explained
- [ ] three measures per half, per body, print direction per half
- [ ] under 200,000 nodes every solve; checkpoints; minutes
- [ ] keys: see section 9

Budget: spec 8 · build, exports, pictures 22 (checkpoint with picture at minute 20 at the latest) · fit 8 ·
studies 37 · report 15.

## 2. Problems in the specification (hand numbers; this table is `spec_problems`)

| # | What the sheet says | The number | Built instead |
| --- | --- | --- | --- |
| 1 | shoulder opening Ø43.5 each side of the seat | inner ring is Ø44.0 outside and turns: the shoulders overlap its side faces by (44.0 − 43.5)/2 = **0.25 mm** radially, at zero axial clearance: they rub | opening **Ø49.0**: 2.5 mm clear of the inner ring, 0.5 mm clear of the outer ring's bore (Ø48), and still 1.5 mm of shoulder over the outer ring's side (Ø49 to Ø52) |
| 2 | screws at X ±28.2 | to a Ø52 seat: clearance hole wall 28.2 − 1.7 − 26 = **0.5 mm**; insert hole wall 28.2 − 2.0 − 26 = **0.2 mm** at the split face (minimum 0.6; an insert needs about 1.5) | screws at **X ±30.0**: 2.2 mm and 1.9 mm to the seat, 4.0 mm to the outside (X 36) |
| 3 | screws at Z 1 and Z 6, Ø6 counterbores | centres 5 mm apart: the two Ø6 counterbores **overlap by 1.0 mm**, and two Ø5.5 M3 heads by 0.5 mm: the screws cannot both go in | **Z 0 and Z 7** (still centred on the bearing, Z 3.5): 1.0 mm between counterbores and 1.0 mm to the faces Z −4 and Z 11; 3.0 mm between insert holes |
| 4 | seat Ø52 for a Ø52 ring, halves meeting on Y 0, printer ±0.15 | printed 0.15 large the ring is loose by 0.15 with the halves already touching; printed small the halves grip at the split edges and stand apart. Clamping is not assured either way | seat **Ø52.2**, each half's seat arc centred 0.1 mm beyond the axis so its crown just touches the ring; split faces cut back to Y ±0.4: **gap 0.8 mm** when clamped (0.35 to 1.25 over the tolerance), never closed |
| 5 | seat Z 0 to 7 for a ring 7 wide | zero axial clearance: printed 0.15 short, the shoulders pinch the ring before the seat does | seat **Z −0.15 to 7.15** (0.15 clear each side at nominal) |
| 6 | Ø4.0 insert hole 6 deep; counterbore floor at Y 28.5 | the screw needs 28.5 + engagement: M3 × 30 engages 1.5 mm, M3 × 35 reaches 6.5 mm below the split face and **bottoms out by 0.5 mm** in a 6 mm hole | insert hole **8 deep**, screw **M3 × 35** (engages 6.1 mm, 1.9 mm spare at the bottom) |

Not problems (checked): mount holes Ø5.6 × 8 at X ±24, Z 3.5 end at Y −24, 14 mm below the seat (which is at Y −10
there); upper wall over the seat at X 0 is 32 − 26 = 6.0 mm; envelope met exactly.
What was given up and why (06-judgment.md): screw positions, opening diameter and seat size are inside the pair, and
nothing outside depends on them; the envelope, the bearing, the split plane, the screw size and the mounting holes
are kept as given.

## 3. Hand calculations

**Geometry built** (mm): each half is the block X −36..36, Z −4..11, upper Y 0.4..32, lower Y −32..−0.4; minus the
opening (circle r 24.5 about the axis, through); minus the seat (circle r 26.1, centre (0, −0.1) for the upper half and
(0, +0.1) for the lower, Z −0.15..7.15); upper: four Ø3.4 holes through along Y at (X ±30, Z 0 and 7), Ø6 counterbores
Y 28.5..32; lower: four Ø4.0 holes Y −8.4..−0.4, two Ø5.6 holes Y −32..−24 at (X ±24, Z 3.5).

| Piece | Working | mm³ |
| --- | --- | --- |
| block, each half | 72 · 31.6 · 15 | 34128.00 |
| opening | segment of r 24.5 beyond a chord 0.4 from the centre: 24.5²·acos(0.4/24.5) − 0.4·√(24.5² − 0.4²) = 923.27 mm², · 15 | −13849.07 |
| seat (what it adds to the opening) | segment of r 26.1 beyond a chord 0.5 from its centre = 1043.94 mm²; (1043.94 − 923.27) · 7.3 | −880.91 |
| upper: clearance holes | 4 · π · 1.7² · 31.6 | −1147.61 |
| upper: counterbores | 4 · π · (3² − 1.7²) · 3.5 | −268.73 |
| **housing_upper** | | **17981.68** (21.40 g) |
| lower: insert holes | 4 · π · 2² · 8 | −402.12 |
| lower: mount holes | 2 · π · 2.8² · 8 | −394.08 |
| **housing_lower** | | **18601.82** (22.14 g) |
| **ring** (steel stand-in, Ø52 / Ø48 × 7, Z 0..7) | π · (26² − 24²) · 7 | **2199.11** |
| screw stand-in, each | head π·2.75²·3 + shank π·1.5²·28.9 + plug π·2²·6.1 | 352.21 |
| pad, each | (4/360) · π · (24² − 22²) · 2 | 6.42 |

Boxes: upper [−36, 0.4, −4, 36, 32, 11]; lower [−36, −32, −4, 36, −0.4, 11]; pair X ±36, Y ±32, Z −4..11.

**Fit, by numbers** (this is `clearances_mm`; the first seven are checked on the STLs in section 6):

| Between | Value mm | Note |
| --- | --- | --- |
| ring outside and each seat, at the crown | 0.00 | touching: this is the clamp |
| ring outside and each seat, at the split | 0.10 | 0.1 · (1 − cos θ) round the arc |
| the two halves at the split | 0.80 | 0.35 to 1.25 over ±0.15 on seat size and both split faces |
| ring side and shoulder, each side | 0.15 | axial |
| inner ring outside (Ø44) and the opening (Ø49) | 2.50 | radial; nothing faces the inner ring's sides |
| outer ring bore (Ø48) and the opening | 0.50 | so the seals are not touched; the shoulder covers 1.5 of the ring's 2.0 mm side |
| shaft Ø40 and the opening | 4.50 | |
| screw Ø3 in Ø3.4 hole; head Ø5.5 in Ø6 | 0.20; 0.25 | radial; head 0.5 below the face Y 32 |
| hole walls to the seat: clearance, insert | 2.20; 1.90 | at the split face |
| counterbore walls: to each other, to the faces | 1.00; 1.00 | thin, not in the load path |
| screw tip to the insert hole floor | 1.90 | M3 × 35 |

**Fit reasoning** (`fit_reasoning`): the seat is 0.2 mm larger than the ring so that at the worst print (Ø52.05) it is
still not smaller than the ring: each half then always meets the ring at its crown first and the screws pull it
round the ring; to follow the ring a half has to change its curvature by 1/26 − 1/26.1, which costs about
1 MPa of bending in a 6 mm wall, so it conforms. The gap between the halves (0.8 mm nominal) is larger than
everything the tolerances can take from it (0.45 mm), so the screws always load the ring and never the split faces.

**Loads.**

| Quantity | Working | Value | Accept |
| --- | --- | --- | --- |
| screw tension, +Y (`hand_screw_load_n`) | the ring pushes the upper half up with 300 N; four screws hold it | **75 N each** | study within 15 %: 63.8 to 86.3 |
| screw load, +X, first hand value | pressure ∝ sin θ on the +X side of both seats: each half takes 150 N sideways and 150 · 2/π = 95.5 N apart | 23.9 N tension + 37.5 N shear each | **not trusted** (05-fea.md "Do not trust a hand value for screw loads off the load axis"): redo it after the study with the contact angles it shows, section 7 |
| upper half, crown section (X 0): 7.3 wide × 6.0 deep plus 7.7 × 7.5 | A = 101.6 mm², centroid 3.43 below Y 32, I = 416 mm⁴ | Z = 121 mm³ | |
| stress at the crown, +Y | between full wrap (hoop 150/101.6 + 150 · 1/121) and line contact at the crown (150 · 30/121) | **3 to 37 MPa; expected 5 to 15** (the playbook's own run of a housing like this implies about 6) | pass mark 22.5 |
| under a screw head | 75 / (π · (2.75² − 1.7²)) | 5.1 MPa bearing | bonded rim: excluded zone |
| ring displacement, +Y, contact | seat and wall compliance | 0.03 to 0.3 mm | |
| ring displacement, bonded twin | | at least 5 times smaller | |
| reaction | | Fy = −300 (case Y), Fx = −300 (case X) | ±3 N |

Print direction, both halves: bearing axis vertical (face Z −4 on the bed, layers along Z). Then clamp and bearing
loads, which act in the XY plane, lie in the layer plane; tension across layers should be small (expected under 3 MPa).
Nodes: 40,200 mm³ in all; with the controls about **55,000 / 110,000 / 190,000** at el 3.0 / 2.2 / 1.7.

## 4. The build (`d2_build.py`, job 1)

```python
from common import *
SEAT_R, OFF, G2, OPEN_R = 26.1, 0.1, 0.4, 24.5          # seat radius, its centre offset, half the split gap, opening radius
SCREWS = [(x, z) for x in (-30.0, 30.0) for z in (0.0, 7.0)]

def half(j, name, sgn):                                  # sgn +1: upper (Y 0.4..32); -1: lower (Y -32..-0.4)
    d = new_part(j.sw, WIP / f'{name}.SLDPRT')
    y0, y1 = (G2, 32.0) if sgn > 0 else (-32.0, -G2)
    with Sk(d, plane(d, 'Z', 3.5, 'BODY_P'), 'BODY') as s:
        s.rect((-36, y0, 3.5), (36, y1, 3.5))
    extrude(d, s.feat, 'BODY', 15.0, mode=MID, expect_dv=72 * 31.6 * 15)
    with Sk(d, plane(d, 'Z', 3.5, 'OPENING_P'), 'OPENING') as s:
        s.circle((0, 0, 3.5), OPEN_R)
    extrude(d, s.feat, 'OPENING', 16.0, cut=True, mode=MID, expect_dv=13849.07)
    with Sk(d, plane(d, 'Z', 3.5, 'SEAT_P'), 'SEAT') as s:
        s.circle((0, -sgn * OFF, 3.5), SEAT_R)
    extrude(d, s.feat, 'SEAT', 7.3, cut=True, mode=MID, expect_dv=880.91)
    save(d)
    if sgn > 0:
        with Sk(d, plane(d, 'Y', 16.2, 'CLEAR_P'), 'CLEAR') as s:          # cut Y -0.3..32.7
            for x, z in SCREWS:
                s.circle((x, 16.2, z), 1.7)
        extrude(d, s.feat, 'CLEAR', 33.0, cut=True, mode=MID, expect_dv=4 * math.pi * 1.7 ** 2 * 31.6)
        with Sk(d, plane(d, 'Y', 30.75, 'CBORE_P'), 'CBORE') as s:         # cut Y 28.5..33
            for x, z in SCREWS:
                s.circle((x, 30.75, z), 3.0)
        extrude(d, s.feat, 'CBORE', 4.5, cut=True, mode=MID, expect_dv=4 * math.pi * (9 - 1.7 ** 2) * 3.5)
        hand = 17981.68
    else:
        with Sk(d, plane(d, 'Y', -4.15, 'INSERT_P'), 'INSERT') as s:       # cut Y -8.4..0.1
            for x, z in SCREWS:
                s.circle((x, -4.15, z), 2.0)
        extrude(d, s.feat, 'INSERT', 8.5, cut=True, mode=MID, expect_dv=4 * math.pi * 4 * 8)
        with Sk(d, plane(d, 'Y', -28.25, 'MOUNT_P'), 'MOUNT') as s:        # cut Y -32.5..-24
            for x in (-24.0, 24.0):
                s.circle((x, -28.25, 3.5), 2.8)
        extrude(d, s.feat, 'MOUNT', 8.5, cut=True, mode=MID, expect_dv=2 * math.pi * 2.8 ** 2 * 8)
        hand = 18601.82
    single_body(d); must('rebuild errors', len(feature_errors(d)), 0); save(d)
    expect(name + ' volume', volume(d), hand, 0.001)
    for got, want in zip(bbox(d), (-36, y0, -4, 36, y1, 11)):
        expect('box', got, want, 0.01)
    seat = holes(d, SEAT_R); must('seat face', len(seat), 1); log('seat box', seat[0][2])       # z -0.15..7.15
    must('opening faces', len(holes(d, OPEN_R)), 2)                                             # one each side of the seat
    if sgn > 0:
        for r, n in ((1.7, 4), (3.0, 4)):
            h = holes(d, r); must(f'holes r {r}', len(h), n); log(r, [(q[1], q[2]) for q in h])   # x +-30, z 0 / 7
    else:
        h = holes(d, 2.0); must('insert holes', len(h), 4); log([(q[1], q[2]) for q in h])        # y -8.4..-0.4
        h = holes(d, 2.8); must('mount holes', len(h), 2); log([(q[1], q[2]) for q in h])         # x +-24, z 3.5, y -32..-24
    export(j.sw, d, WIP / f'{name}.stl'); check_export(d, WIP / f'{name}.stl')
    close(j.sw, d)

def ring(j):
    d = new_part(j.sw, WIP / 'ring.SLDPRT')
    with Sk(d, plane(d, 'Z', 3.5, 'DISC_P'), 'DISC') as s:
        s.circle((0, 0, 3.5), 26.0)
    extrude(d, s.feat, 'DISC', 7.0, mode=MID, expect_dv=math.pi * 676 * 7)
    with Sk(d, plane(d, 'Z', 3.5, 'RINGBORE_P'), 'RINGBORE') as s:
        s.circle((0, 0, 3.5), 24.0)
    extrude(d, s.feat, 'RINGBORE', 8.0, cut=True, mode=MID, expect_dv=math.pi * 576 * 7)
    expect('ring volume', volume(d), 2199.11, 0.001); save(d)
    export(j.sw, d, WIP / 'ring.stl'); close(j.sw, d)

def screw(j, k, x, z):                                    # steel stand-in: shank first, then head and plug onto it
    d = new_part(j.sw, WIP / f'screw_{k}.SLDPRT')
    for feat, r, y0, y1 in (('SHANK', 1.5, -1.0, 29.0), ('HEAD', 2.75, 28.5, 31.5), ('PLUG', 2.0, -6.5, -G2)):
        ym = (y0 + y1) / 2
        with Sk(d, plane(d, 'Y', ym, feat + '_P'), feat) as s:
            s.circle((x, ym, z), r)
        extrude(d, s.feat, feat, y1 - y0, mode=MID)
    must('screw is one body', len(bodies(d)), 1)
    expect('screw volume', volume(d), 352.21, 0.005); save(d); close(j.sw, d)

def pad(j, k, a, b):                                      # 4 degrees of a soft ring r 22..24, Z 2.5..4.5, inside the steel ring
    d = new_part(j.sw, WIP / f'pad_{k}.SLDPRT')
    with Sk(d, plane(d, 'Y' if a[1] == 0 else 'X', 0.0, ''), 'SOFTPAD') as s:
        s.rect(a, b); s.centerline((0, 0, 0), (0, 0, 10))
    revolve(d, s.feat, 'SOFTPAD', angle=4.0, mid=True, expect_dv=6.42)
    save(d); close(j.sw, d)

with job() as j:
    half(j, 'housing_upper', +1); half(j, 'housing_lower', -1); ring(j)      # checkpoint: pictures now (below)
    for k, (x, z) in enumerate(SCREWS):
        screw(j, k + 1, x, z)
    for k, (a, b) in enumerate((((22, 0, 2.5), (24, 0, 4.5)), ((-24, 0, 2.5), (-22, 0, 4.5)),
                                ((0, 22, 2.5), (0, 24, 4.5)), ((0, -24, 2.5), (0, -22, 4.5)))):
        pad(j, k + 1, a, b)
    d = open_doc(j.sw, WIP / 'housing_lower.SLDPRT')
    save_as(d, WIP / 'housing_fea.SLDPRT')
    for f in ['housing_upper', 'ring'] + [f'screw_{k}' for k in (1, 2, 3, 4)] + [f'pad_{k}' for k in (1, 2, 3, 4)]:
        insert_body(d, WIP / f'{f}.SLDPRT')
    bs = bodies(d); log(bs); must('bodies', len(bs), 11)
    expect('assembly volume', volume(d), 18601.82 + 17981.68 + 2199.11 + 4 * 352.21 + 4 * 6.42, 0.001)
    save(d); close(j.sw, d)
```

Expected volume after each step: upper 34128.00, 20278.93, 19398.02, 18250.41, 17981.68; lower 34128.00, 20278.93,
19398.02, 18995.90, 18601.82.

Pictures, straight after the three parts exist (the checkpoint; note the time):

```
python solidworks/sheet.py WIP/housing_upper.stl -o eval/<run>/pictures/d2_upper.png
python solidworks/sheet.py WIP/housing_lower.stl -o eval/<run>/pictures/d2_lower.png
python solidworks/sheet.py WIP/housing_upper.stl WIP/housing_lower.stl WIP/ring.stl --together -o eval/<run>/pictures/d2_pair.png
```

Look for: a half-round seat with a lip each side in both halves; four holes with counterbores from the top of the
upper half; four holes in the split face and two in the bottom face of the lower half; a visible gap between the halves.

## 5. How the bodies touch in `housing_fea.SLDPRT` (why each is held)

| Body | Held by | How |
| --- | --- | --- |
| lower half (PETG) | fixture | face Y −32 fixed |
| screws ×4 (steel) | global bond | plug Ø4.0 in the Ø4.0 insert hole (touching, Y −6.5..−0.4); free along the shank (0.2 mm clear) |
| upper half (PETG) | global bond to the screws | counterbore floors on the undersides of the screw heads (touching at Y 28.5); head sides are 0.25 mm clear |
| ring (steel) | four soft pads | each pad bonded to the ring's bore (touching at r 24), its inner face (r 22) fixed; `SOFT`, 0.5 MPa |
| ring to the seats | **contact sets** | no penetration, ring outside against each seat; they touch along the crown lines only |
| upper to lower | **contact set** | no penetration between the split faces (0.8 mm apart; it should never close) |

The ring's sides are 0.15 mm from the shoulders and touch nothing: no bond there.

## 6. Fit check on the exported parts (plain python, under `pc/capped.py`)

```python
from common import *
up, lo = sheet.read_stl(WIP / 'housing_upper.stl'), sheet.read_stl(WIP / 'housing_lower.stl')
def shell_pts(r0, r1, z0, z1, nr=5, na=240, nz=9):
    return np.array([(r * math.cos(a), r * math.sin(a), z) for r in np.linspace(r0, r1, nr)
                     for a in np.linspace(0, 2 * math.pi, na, endpoint=False) for z in np.linspace(z0, z1, nz)])
def hits(pts):
    return int(sheet.inside(up, pts).sum()), int(sheet.inside(lo, pts).sum())
log('ring (r 24..25.97, z 0.02..6.98) inside upper, lower: must be (0, 0):', hits(shell_pts(24.0, 25.97, 0.02, 6.98)))
log('ring grown 0.2 radially must hit both (it proves the test sees the seats):', hits(shell_pts(26.15, 26.2, 1.0, 6.0, nr=2)))
log('inner ring and shaft (r 0..22.2, z -4..11) must be (0, 0):', hits(shell_pts(0.5, 22.2, -4.0, 11.0, nr=12)))
log('as specified (opening 43.5): the shoulder would start at r 21.75, inside the inner ring (r 22.0) by 0.25')
log('ring sides: shoulders at z', -0.15, 7.15, '-> points at z -0.10 and 7.10, r 25: must be (0, 0):',
    hits(shell_pts(24.6, 25.9, -0.10, 7.10, nr=3, nz=2)))
log('and at z -0.20 and 7.20 they must hit:', hits(shell_pts(24.6, 25.9, -0.20, 7.20, nr=3, nz=2)))
```

Also from the solid (in the build log): seat radius 26.1 and box, opening radius 24.5, hole centres, split faces at
Y ±0.4. Put the measured values, not the planned ones, into `clearances_mm`.

## 7. The studies (`d2_fea.py`)

```python
from d2_build import SCREWS, G2            # move the build's last "with job()" block under  if __name__ == '__main__':  first
from common import *
from swfea import _arr
MATS = {'screw_': STEEL, 'ring-': STEEL, 'pad_': SOFT}

def per_node_reaction(st, res):
    return _arr(res.GetReactionForcesAndMoments(0, NUL, 0, L()), 9)

def run(j, d, name, force, el, cs, bonded=False):
    d.ForceRebuild3(False)
    mount = pick(d, kind='plane', normal=(0, -1, 0), at=(0, -32, 3.5)); must('mount face', len(mount), 1)
    up_seat = pick(d, kind='cyl', r=26.1, inside=[-27, 0.3, -0.2, 27, 26.2, 7.2]); must('upper seat', len(up_seat), 1)
    lo_seat = pick(d, kind='cyl', r=26.1, inside=[-27, -26.2, -0.2, 27, -0.3, 7.2]); must('lower seat', len(lo_seat), 1)
    ring_out = pick(d, kind='cyl', r=26.0, inside=[-26.05, -26.05, -0.05, 26.05, 26.05, 7.05]); must('ring outside', len(ring_out), 1)
    sides = (pick(d, kind='plane', normal=(0, 0, 1), at=(25, 0, 7)) + pick(d, kind='plane', normal=(0, 0, -1), at=(25, 0, 0)))
    must('ring sides', len(sides), 2)
    pad_in = pick(d, kind='cyl', r=22.0); must('pad inner faces', len(pad_in), 4)
    big = lambda fs: [f for f in fs if face_info(f)['area'] > 20]      # noqa: E731  leaves out the plug ends (5.5 mm2)
    up_split = big(pick(d, kind='plane', normal=(0, -1, 0), inside=[-36.1, 0.39, -4.1, 36.1, 0.41, 11.1])); must('upper split faces', len(up_split), 2)
    lo_split = big(pick(d, kind='plane', normal=(0, 1, 0), inside=[-36.1, -0.41, -4.1, 36.1, -0.39, 11.1])); must('lower split faces', len(lo_split), 2)
    small = []
    for r, n in ((1.5, 4), (2.0, 8), (2.75, 4), (3.0, 4), (1.7, 4)):     # shanks, plugs + insert holes, heads, counterbores, clearance holes
        f = pick(d, kind='cyl', r=r); must(f'faces r {r}', len(f), n); small += f
    kind = BONDED if bonded else NO_PENETRATION
    r = static(j, d, name, PETG, fixtures=[('fixed', mount), ('fixed', pad_in)],
               loads=[('remote', sides, (0.0, 0.0, 3.5), force, (0, 0, 0))],
               el=el, ctrl=[(up_seat + lo_seat + ring_out, cs), (small, 0.8)],
               contacts=[(kind, ring_out, up_seat), (kind, ring_out, lo_seat), (NO_PENETRATION, up_split, lo_split)],
               materials=MATS, solver=SOLVER_DIRECT, post=per_node_reaction, max_nodes=200_000)
    save_npz(r, name)
    return r

def split(r):
    """Node masks by geometry (05-fea.md contact rule 5). Interface nodes on a bonded screw count as screw."""
    p = r.pos
    rho = np.hypot(p[:, 0], p[:, 1])
    pad = rho < 23.99
    ring = (rho >= 23.99) & (rho <= 26.0005) & (p[:, 2] > -0.001) & (p[:, 2] < 7.001)
    dxz = np.min([np.hypot(p[:, 0] - x, p[:, 2] - z) for x, z in SCREWS], axis=0)
    y = p[:, 1]
    screw = (y >= -6.501) & (y <= 31.501) & ((dxz <= 1.5005) | ((dxz <= 2.0005) & (y <= -G2 + 0.001)) | ((dxz <= 2.7505) & (y >= 28.499)))
    other = ~(pad | ring | screw)
    upper, lower = other & (y > G2 - 0.01), other & (y < -G2 + 0.01)
    if (other & ~upper & ~lower).any():
        raise Failed('nodes between the halves that belong to no body: the split is not safe')
    return dict(pad=pad, ring=ring, screw=screw, dxz=dxz,
                upper=upper & ~((dxz < 3.75) & (y > 27.5)),                       # 1 mm round each bonded head left out
                lower=lower & ~((dxz < 3.0) & (y > -7.5)) & (y > -30.0),          # 1 mm round each bonded plug, 2 mm off the fixed face
                upper_all=upper, lower_all=lower)

def seat_angle(r, m, sgn):
    """Angle in degrees, from the half's own crown toward +X, of the centre of the contact pressure on its seat."""
    p = r.pos
    nx, ny = p[:, 0], p[:, 1] + sgn * 0.1
    d = np.hypot(nx, ny)
    on = m['upper_all' if sgn > 0 else 'lower_all'] & (d < 26.1 + 0.3) & (p[:, 2] > 0) & (p[:, 2] < 7)
    nx, ny = nx[on] / d[on], ny[on] / d[on]
    S = r.s[on]
    press = np.maximum(-(nx * nx * S[:, 1] + ny * ny * S[:, 2] + 2 * nx * ny * S[:, 4]), 0.0)
    if press.sum() < 1e-6:
        return None, 0.0
    return float(np.degrees(np.arctan2((press * nx).sum(), sgn * (press * ny).sum()))), float(press.max())

def read(r):
    m, p = split(r), r.pos
    out = dict(study=r.name, el=r.el, nodes=r.nodes, reaction=r.reaction, excessive=bool(r.excessive),
               ring_u=[float(v) for v in r.disp[m['ring'], 1:4].mean(axis=0)], max_disp=r.max_disp(),
               ring_vm=float(r.vm[m['ring']].max()), screw_vm=float(r.vm[m['screw']].max()))
    for h in ('upper', 'lower'):
        out[h] = direction_table(r, m[h])                              # three measures x three print directions, per half
        out[h + '_excluded_vm'] = float(r.vm[m[h + '_all']].max())
    out['screws'] = []
    for x, z in SCREWS:                                                # tension = mean sigma-y over the shank section x its area
        s = (np.hypot(p[:, 0] - x, p[:, 2] - z) <= 1.5005) & (p[:, 1] > 5) & (p[:, 1] < 23)
        out['screws'].append(dict(x=x, z=z, tension=float(r.s[s, 2].mean() * math.pi * 2.25),
                                  shear_x=float(r.s[s, 4].mean() * math.pi * 2.25), nodes=int(s.sum())))
    out['screw_sum'] = float(sum(q['tension'] for q in out['screws']))
    out['angle_upper'], out['p_upper'] = seat_angle(r, m, +1)
    out['angle_lower'], out['p_lower'] = seat_angle(r, m, -1)
    lc = m['lower_all'] & (np.abs(p[:, 0]) > 3) & (np.abs(p[:, 0]) < 6) & (p[:, 1] < -25) & (np.hypot(p[:, 0], p[:, 1]) < 26.3) & (p[:, 2] > 0) & (p[:, 2] < 7)
    out['lower_seat_opens_by'] = float(out['ring_u'][1] - r.disp[lc, 2].mean())      # ring UY minus the lower seat's UY near its crown
    try:
        q = r.extra
        idpos = dict(zip(r.s[:, 0].astype(int), p))
        keep = np.array([int(i) in idpos for i in q[:, 0]])
        P = np.array([idpos[int(i)] for i in q[keep, 0]])
        inpad = np.hypot(P[:, 0], P[:, 1]) < 23.0
        out['pads_reaction'] = [float(v) for v in q[keep][inpad, 1:4].sum(axis=0)]
    except Exception as ex:                                            # logged; the estimate from the pad stiffness is used instead
        log('per-node reaction not read:', str(ex)[:120])
        out['pads_reaction_estimate_N'] = 6.6 * float(np.hypot(out['ring_u'][0], out['ring_u'][1]))
    return out

def one(j, d, rows, name, force, el, cs, nodes, bonded=False):
    predict(name, nodes, 0.1, 'upper half, outer face over the crown (x 0, y 32) or the seat beside it')
    r = run(j, d, name, force, el, cs, bonded)
    compare(name, r, nodes, 0.1)
    rows[name] = read(r); log(name, json.dumps(rows[name], default=float))
    (HERE / 'd2_rows.json').write_text(json.dumps(rows, indent=1, default=float), encoding='utf-8')

if __name__ == '__main__':
    f = HERE / 'd2_rows.json'
    rows = json.loads(f.read_text(encoding='utf-8')) if f.exists() else {}
    with job() as j:
        j.simulation()
        d = open_doc(j.sw, WIP / 'housing_fea.SLDPRT')
        if 'D2_Y_30' not in rows:                                      # job 2: four studies
            one(j, d, rows, 'D2_Y_30', (0, 300.0, 0), 3.0, 1.2, 55000)
            one(j, d, rows, 'D2_YBOND_30', (0, 300.0, 0), 3.0, 1.2, 55000, bonded=True)
            one(j, d, rows, 'D2_X_30', (300.0, 0, 0), 3.0, 1.2, 55000)
            one(j, d, rows, 'D2_Y_22', (0, 300.0, 0), 2.2, 0.9, 110000)
        else:                                                          # job 3 (run the script again): three studies
            one(j, d, rows, 'D2_X_22', (300.0, 0, 0), 2.2, 0.9, 110000)
            one(j, d, rows, 'D2_Y_17', (0, 300.0, 0), 1.7, 0.7, 190000)
            one(j, d, rows, 'D2_X_17', (300.0, 0, 0), 1.7, 0.7, 190000)
        close(j.sw, d)
```

Model choices, and why each is the right one:

- **Load:** `'remote'` at the bearing centre (0, 0, 3.5), rigid, on the ring's two side faces. The real load comes
  through balls and a steel inner ring: stiff. The ring's outside (the contact face) and its bore (the pads) stay free
  of the load.
- **Screws:** steel pins bonded under the head and in the insert hole, free along the shank (05-fea.md "Screws and
  clamped joints"). No preload: the result is for a snug joint (see step 8 below).
- **Mesh:** el 3.0, 1.2 on the two seats and the ring's outside, 0.8 on every screw face, counterbore and screw hole
  (the 1.0 mm counterbore walls need it). Finer rows shrink the seat control with the global size.
- **Solver:** direct sparse. Material: read the body lines in the log: upper and lower PETG, ring and four screws
  steel, four pads soft.

Read the results in this order. After `D2_Y_30` alone, check 1 to 4 before trusting anything:

1. `reaction`: Fy −300 ± 3 (case Y), Fx −300 ± 3 (case X).
2. `ring_u`: case Y: UY +0.03 to +0.3 mm, UX about 0. `max_disp` under 1 mm.
3. `screws`: case Y: four tensions each 63.8 to 86.3 N, `screw_sum` 290 to 303 N (300 less the pads' share), each on
   at least 20 nodes. This is `screw_load_n` (report the four values and their mean).
4. `pads_reaction`: its size under 3 N (1 %).
5. **Contact proof** (`contact_proof`), 05-fea.md "Which contact proof fits", first case: `D2_YBOND_30` against
   `D2_Y_30`: (a) ring UY at least 5 times smaller when bonded (give the ratio); (b) bonded `screw_sum` under
   100 N (the ring is glued to the fixed lower half, so the screws are nearly idle); (c) in the contact case
   `lower_seat_opens_by` is positive (the unloaded seat opens) and `angle_lower` is None or `p_lower` under 5 % of
   `p_upper`.
6. Per half: `rows[...]['upper']['Z']` and `['lower']['Z']`: the three measures for layers along Z, with places;
   the X and Y entries are the print-direction table. `upper_excluded_vm`, `lower_excluded_vm`: what the 1 mm
   zones round the bonded heads and plugs, and the fixed face, left out. `ring_vm` and `screw_vm` are steel
   (640 MPa): never compare them with 45.
7. Case X: `screws` gives tension and shear per screw. Then the hand value **redone** with the angles the study
   found (statics of the ring between two seats, normals at `angle_upper` = a and `angle_lower` = b from the crowns):
   N_upper = 300 / (sin a + cos a · tan b); tension per screw = N_upper · cos a / 4; shear per screw =
   N_upper · sin a / 4. Compare with the study's mean tension: within 15 %, or say what differs (uneven sharing
   between the X +30 and X −30 pairs is expected: report both pairs).
8. Preload: the +Y case is the same load path as tightening (four screws pulling the upper half onto the ring).
   Screw force at which the factor falls to 2.0: F = 75 · (lowest factor of the upper half in case Y) / 2.
   Tightening torque that stays under it: T = 0.2 · F · 3 mm (in N·mm). Report both, and that the studies have no
   preload.
9. Convergence: the three measures of each half over `D2_Y_30`, `_22`, `_17` (`settled([...])`), and the same for X.
   `nodes` = the finest solved.
10. Lowest factors over both cases and both halves, layers along Z: `sf_yield`, `sf_layer`, `sf_shear`; `governing`
    = which half, which case, which measure, where. `valid` = checks 1 to 5 hold, screw load within 15 % (case Y),
    converged; otherwise false, with `why` naming the one that failed.

## 8. Decisions made for you

- The six changes of section 2. One line each lets a person overrule them.
- **Print direction, both halves:** bearing axis vertical, face Z −4 on the bed, layers along Z. Loads lie in the
  layer plane; the seat prints as a true arc; the upper lip overhangs the seat by 1.6 mm (prints without support).
- **Seat fit:** Ø52.2 with the crown touching, gap 0.8 (section 3). The studies model exactly the printed shape.
- **If the upper half fails 2.0 in case Y** (crown stress over 22.5 MPa, converged): do not change the envelope.
  First read where the contact is (`angle_upper`, `p_upper`): a narrow patch at the crown means the half has not
  wrapped the ring. Rebuild both halves with `SEAT_R, OFF = 26.05, 0.05` (seat Ø52.1: it wraps sooner; worst print
  Ø51.95, 0.05 under the ring, which the 0.8 mm gap absorbs), rerun `D2_Y_30` only, and report both. If that fails
  too: state "not possible inside Y ±32 with a 6.0 mm wall", give the wall that would do
  (6.0 · √(2.0 / factor) mm), and name the envelope in Y as the requirement that would have to move.
- **If time runs short:** job 3 (finer meshes) is the first thing to drop: report convergence as "not shown" and
  `valid` false. The bonded twin and the X case are not to be dropped.

## 9. Branches

| You see | It means | Do |
| --- | --- | --- |
| `OPENING` or `SEAT` `expect_dv` fails | the circle centre or radius | print them; the seat centre is (0, −0.1) for the upper half and (0, +0.1) for the lower |
| `CBORE` raises where other cuts worked | 03-modelling.md table: this very counterbore failed once | four `revolve(cut=True)` cuts, one per screw: `plane(d, 'Z', z, name)` (z 0: the base plane), `s.rect((x, 28.5, z), (x + 3.0, 33.0, z))`, `s.centerline((x, 28, z), (x, 34, z))`, `expect_dv=math.pi*(9 - 1.7**2)*3.5` each |
| `must('opening faces', ..., 2)` gets 1 or 3 | how the opening is split by the seat | `list_faces(d)`; accept what is there if the volume is right, and note it |
| screw: more than one body | head or plug did not merge with the shank | they overlap by 0.5 mm, so it should; `bodies(d)`; draw the shank from −2 to 30 |
| pad `revolve` raises | profile or centreline | the rectangle must lie in a plane through Z and not cross the axis; as a fallback make the pad a plain block touching the ring's **side** is not possible here: instead use `angle=8.0` (volume 12.85) |
| `insert_body` raises, or bodies is not 11 | a part came in merged or not at all | `bodies(d)`; rebuild that part; never go on with a wrong count |
| `materials keys ... match no body` | body names are not `<file>-<feature>` | read the logged names; choose keys that match the four screws, the ring, the four pads and nothing else |
| a pick count is wrong | filter | `list_faces(d)`; fix the box; do not solve |
| `static` raises "contact set failed" on the split faces | faces 0.8 mm apart refused | drop that third set, and prove afterwards that the gap stayed open: relative UY of the two halves near X ±30 far below 0.8 mm. Say so |
| "contact set failed" on the bonded twin | a bond across a 0.1 mm gap refused | make the twin differently: skip it, and use proof (c) of step 5 plus this: rerun case Y with force (0, −300, 0); the ring must then load the lower seat and the screws must fall under 10 N. Report which proof was used |
| "excessive displacements" (static raises) | a body is loose: the ring (pads not bonded) or the upper half (screws not bonded) | read `bodies(d)` boxes: screw plugs must touch the insert holes (r 2.0, Y −6.5..−0.4) and heads the counterbore floors (Y 28.5). Fix the geometry, not `loose_ok` |
| "Failure to achieve equilibrium" in case X | the ring finds no seat sideways | first: rerun with the pads at `angle=8.0`. Second (a different model): add a 0.02 mm interference instead of line contact, `OFF = 0.08` in both halves. Third: report case X as not solved, with the hand value 23.9 N / 37.5 N marked untrusted |
| error 24 at once | a free body, or the document issue of 05-fea.md "When the solve fails" | check the three "held by" rows of section 5 in order; new job |
| screw tensions sum to far less than 300 in case Y | the ring is held by something else: bonded to a seat or a shoulder | `lower_seat_opens_by` negative or zero means the lower seat is holding it: the contact set did not replace the bond. Check that both seat faces are in the sets (pick counts) |
| screw tensions uneven (Z 0 against Z 7 by more than 20 %) | the load is off the mid-plane | the remote point must be (0, 0, 3.5) |
| a screw's `nodes` under 20 | shank mesh too coarse to integrate | lower the 0.8 control to 0.6 for all studies |
| peak in a half on a counterbore wall or at a plug rim | bonded-rim singularity or the thin 1.0 mm wall | it should be inside the excluded 1 mm; if it sits just outside and climbs with refinement, widen the zone to 1.5 mm for all rows and say what it hides |
| crown stress 22.5 to 45 MPa | section 8, "If the upper half fails" | follow it |
| mesh refused over 200,000 | cap | `el=1.9, cs=0.8` for that row; if still over, report two rows and "not shown" (05-fea.md "When the node cap and convergence meet") |
| a measure does not settle | not converged | "not shown" for that measure; never pass on the finest value |
| minute 90 | time | stop; report what stands, studies not run are "not run" |

Anything else: stop D2 at that step, write down exactly what was seen (log tail, `d2_rows.json`), carry on with the
report and the next task.

## 10. Done checklist, results.json and REPORT.md

- [ ] section 2's table in REPORT.md and as `spec_problems` (six entries: what, the number, what was built)
- [ ] three parts: volume, box, holes measured, exports checked; three pictures; checkpoint time
- [ ] fit check output (six lines) and `clearances_mm` (the table of section 3 with measured values)
- [ ] per study: reaction, ring displacement, node count against the prediction, solver named
- [ ] contact proof with its three numbers; pads' share in N
- [ ] screw loads: case Y four values against 75; case X tension and shear against the redone hand value
- [ ] per half: three measures with places, print-direction table, excluded values; steel judged as steel
- [ ] convergence rows; preload statement (force for factor 2.0, torque)
- [ ] thinnest margin; cheapest improvement (a 45° chamfer under the upper lip, or the Ø52.1 seat); not verified:
      preload, friction, insert pull-out, the real ring's flexibility, the as-printed seat
- [ ] `put('D2', spec_problems=[...], seat_diameter_mm=52.2, split_gap_mm=0.8, fit_reasoning='...', clearances_mm={...},
      hand_screw_load_n=75.0, screw_load_n=..., nodes=..., how_bodies_were_held='...', contact_proof='...',
      sf_yield=..., sf_layer=..., sf_shear=..., governing='...', print_orientation={'upper': 'bearing axis vertical,
      face Z -4 on the bed, layers along Z', 'lower': 'the same'}, valid=..., why='...', minutes=..., status=..., notes=...)`
