# Review of `eval/haiku-plan-c` (set C), from files only

Reviewer had no SolidWorks. Everything below was measured with numpy on the three STLs in `exports/`, on
`fea_rows.json`, `results.json`, `times.log` and the pictures. Scratch scripts: `review_work/` (`geom.py`, `fixed.py`,
`fea.py` with `judge_copy.py`, `printab.py`, `profile.py`, `sharp.py`, two crop sheets). Clock (`date -u`):
start 02:58, end 03:16 UTC, 18 minutes.

`solidworks/sheet.py` in this folder has `read_stl`, `shape_stats` and `inside` only. It has no `printability` and no
`mesh_diff`, so the print check is my own (`review_work/printab.py`, the same code is in
`eval/haiku-plan-c-followup/r_tools.py`). `judge()` is the function from `solidworks/swfea.py`, taken by source
extraction because `swfea` does not import without the Windows modules.

## Result in short

- **C1: done.** Confirmed.
- **C2: not done.** The builder's own statement is right: with layers along Y the verdict is fail, 1.58.
- All fixed items pass on the STL. Mass, watertightness and shell count are as claimed.
- "Layers along X 2.38" is right, and it is a `pass` from `judge()` with all nine entries settled. Printing that way
  fits the bed and is possible on supports, but the part then touches the bed on a line (9.5 mm2). It is a real
  option with a real cost, and it is the smallest change that meets the requirement.
- **A defect neither the builder nor DESIGN.md names:** the stem is pinched at Z -74 to 8.6 x 8.8 mm half-size where
  the section table says about 11.9 x 12.3, and it bulges at Z -94. This is a loft artefact (the planner's volume
  model does not have it). It is the lump seen in every view, it is where von Mises governs, and it is very likely
  why idea B's window split the stem.
- Process: only one idea has a picture, so "two ideas, each with a picture" is not met. The rest of the process
  items are met in form; details below.

## 1. Geometry, measured on the STLs

| Quantity | Builder | Reviewer (STL) | Agrees |
| --- | --- | --- | --- |
| Boxy volume, mass | 219436.0 mm3 solid, 219351.8 STL, 261.13 g | 219351.8 mm3, 261.03 g | yes (0.04 % faceting) |
| Boxy box | -35..35, -22..22, -215..35 | the same | yes |
| Organic volume, mass | 97787.2 mm3 solid, 97581.6 STL, 116.37 g | 97581.6 mm3, 116.12 g | yes (0.21 % faceting) |
| Organic watertight, shells | true, 1 | true (every edge shared by two triangles, opposite directions), 1 | yes |
| Organic box | -35.985..35.985, -22..22, -213..35.942 | the same | yes |
| Mass against boxy | 116.4 below 261.1 | 44 % of the boxy link | yes |
| Idea A crude | 120.24 g | 100822.8 mm3, 119.98 g, watertight, 1 shell | yes |
| Enclosed cavity | none | none (one shell) | yes |

Density 1190 kg/m3 from `swfea.PETG`.

### Fixed items of C2 on `link_organic.STL` (`sheet.inside()` sampling, planes and vertices)

| Item | Verdict | Measurement |
| --- | --- | --- |
| Mounting face flat on Y -4, dia 30 to dia 62 | pass | planar area on Y -4 with normal -Y 2353.0 mm2, radius 15.000 to 31.500 (the ring to dia 63 less six holes is 2355.9; to dia 62 needs 2257.7). 7014 points at Y -3.95 all solid, 3840 points at Y -4.05 all empty |
| Nothing below Y -4 inside dia 62 | pass | 16128 points down to Y -30, none solid. Outside dia 62 the stem goes below Y -4 from Z -34 on (radius 34 mm and more), as the boxy beam did. Whether the motor body allows that: could not check |
| Bore dia 30 | pass | vertices at r 15.000, Y -4 to 4. 12960 points inside r 14.9 empty. Wall solid at r 15.1 except within 12.0 degrees of -Z, which is the cable tunnel's mouth |
| Six dia 3.4 holes on dia 50, first on +X, 60 degrees apart | pass | at each of the six positions: vertices at r 1.700, Y -4.00 to 4.00, 648 points inside empty, wall solid at r 1.85 (168 of 168) |
| Dia 7 x 10 clear in front of each hole, Y +4 to +14 | pass, tight on two | 2016 points per hole, none solid. The seat at Y 3.9 is solid round every hole. At the two lower holes (X +/-12.5, Z -21.65) material starts at r 3.65: 0.15 mm outside the required r 3.5 |
| Pin axis X 0, Z -200 along Y, dia 8 | pass | both cheeks: vertices at r 4.000, centroid X 0.000 Z -200.000, Y 16.00 to 22.00 and -22.00 to -16.00; 1080 points inside empty |
| Inner cheek faces Y +/-16 flat over dia 16 | pass | plane at Y +/-16 exactly, 615.4 mm2 each, reaching r 20.4 from the pin (needed r 8); solid at 16.05, empty at 15.95 |
| 5 mm of material round the pin hole | pass, no margin at the outer face | wall all round by Y from the inner face outward: 8.9, 8.9, 8.9, 8.9, 8.7, 8.2, 7.5, 5.5 mm; at the outer face Y +/-22 the knuckle's flat is r 9, so exactly 5.0 |
| Slot clear from Z -183 down, swept dia 30 about the pin | pass | cylinder r 14.95, Y +/-15.95: 5616 points empty. Whole slab Y +/-15.95, Z -183 to -214, X +/-20: 17056 points empty. Roof is the arch: first solid at Z -169.1 (Y 8), -172.4 (Y 12), -177.4 (Y 15), open at Y 0 into the tunnel |
| Straight clear dia 6 cable passage | pass | along Z at X 0, Y 0: all points inside r 3.0 empty from Z +15 (in the bore) to Z -213.5 (the open fork end). Tunnel wall at r 3.2 |
| Cable does not hang outside the form | pass on the letter, two things could not be checked | enclosed all round from Z -15 to Z -167; above that it is inside the bore, below that between the cheeks. Could not check: the passage starts in the dia 30 locating bore (if the motor's spigot fills the bore, the mouth is closed) and runs straight through the pin axis, where the swinging part is |

`fixed_items_ok` true is right. One thing to correct in DESIGN.md: the 0.8 mm skin over the tunnel is "for 8 mm"
only on the screw side (Z -15 to -22). On the mounting side it is 0.8 mm (Y -4.00 to -3.25) at Z -16, -22, -26 and
-30, so at least 15 mm long.

### The stem as built against the section table (`review_work/profile.py`)

| Z | half width X built | top Y built | table STEM_A2 (straight line between rows) |
| --- | --- | --- | --- |
| -58 | 12.96 | 13.07 | 12.8 / 12.8 |
| -66 | 10.66 | 10.96 | 12.3 / 12.6 |
| -70 | 9.24 | 9.52 | 12.1 / 12.5 |
| **-74** | **8.60** | **8.83** | **11.9 / 12.4** |
| -78 | 9.16 | 9.52 | 11.7 / 12.2 |
| -86 | 11.65 | 12.27 | 11.4 / 12.0 |
| -94 | 12.54 | 13.31 | 11.1 / 11.9 |
| -114 | 10.71 | 11.88 | 10.6 / 11.8 |

Between the rows at Z -60 and Z -85 the loft shrinks to 72 % of the table in both directions and then overshoots by
12 % at Z -94. `idea_a.STL` (table STEM_A) has the same (8.54 x 8.70 at Z -74). Evidence that it is the loft and not
the design: the planner's voxel model gives the stem 103700 mm3 and the build gave 101543; idea B's stem came out
9.6 % short (88379 against 97800), with its longest gap (30 mm) in the same place; the rows are 5 to 8 mm apart at
the neck and 25 to 30 mm apart in the middle. I cannot prove the cause from files; uneven row spacing is the likely
one, and the follow-up tests it with a number.

Consequences: (a) the von Mises peak of every case sits there (17.4 MPa at Z -73.4, factor 2.58), not at the neck;
(b) the layers-along-Z reading (1.20) is governed there; (c) idea B's window, 10 mm half-wide at that height, met a
stem only about 12 mm half-wide, which is why it "split the stem at Z -56 to -70"; (d) the 6 % stem-volume check
existed to catch a bad loft, and for B the builder took the plan's branch that replaces the expected volume by the
measured one, which silenced it. The builder's report describes the pinch as "pinches to a waist", as if drawn.

## 2. The verdict, recomputed with `swfea.judge()` from `fea_rows.json`

Limits 45 / 22.5 / 13 MPa, need 2.0, three sizes 4.0, 3.0, 2.3 mm (82002, 116027, 173186 nodes), read 3.0 mm or more
from held and loaded faces. Nine entries per direction.

| Layers along | Verdict | Lowest factor | Entry | Place | Settled entries | Growing step |
| --- | --- | --- | --- | --- | --- | --- |
| X | **pass** | **2.38** | +Y, shear (5.14, 5.45, 5.47 MPa) | [2.57, -1.90, -33.57], the neck | 9 of 9 | none |
| Y (chosen) | **fail** | **1.58** | +Y, layer (14.07, 14.04, 14.21 MPa) | [3.17, -0.41, -32.08], the neck, on the cable tunnel's wall | 9 of 9 | none |
| Z | fail | 1.20 | -X, layer (18.10, 18.96, 18.77 MPa) | [8.53, -1.08, -73.35], the pinch | 9 of 9 | none |

- **"fail 1.58" is right.** Second failing entry with layers along Y: +Y, shear 1.73 at [-9.45, 4.61, -23.56].
  `sf_layer` 1.56 and `sf_shear` 1.70 in `results.json` are the same entries times the rigid-load ratio 1.018.
- **"layers along X 2.38" is right, and it is converged** in `judge()`'s sense: next lowest +Y, layer 2.45 (8.06, 9.19,
  9.17), then von Mises 2.58. One entry (-X, layer, 1.77 to 2.25 MPa, last step 25 %) settles only by the floor rule
  (0.45 MPa against 0.56 allowed); its factor is 10.
- A caveat the builder did not give: the two governing places for layers along X are 3.02 and 3.09 mm from the edge
  of the held ring, that is on the edge of the 3.0 mm exclusion. They are the flank of the fixture-edge peak, read
  at the distance the plan fixed beforehand. For +Y, von Mises reads 21.8 MPa outside 2 mm and 17.2 outside 3 and
  5 mm. The rows hold no such sweep for the layer measures; the follow-up adds it.
- The earlier variants, recomputed: STEM_A along Y fail 1.54 (as claimed), along X "not shown" 2.10 (+Y, shear not
  settled). STEM_A3 along Y fail 1.44 on +Y, shear, with +Y, layer growing (from the appended report; no rows file
  kept). The final `fea_rows.json` equals `backup_STEM_A2/fea_rows.json` in every stress.
- Why thickening did not help: across-layer tension at the neck read 14.6, 14.2, 13.9 MPa for A, A2, A3. It is
  peel at the edge of the held face, raised by the tunnel wall, not plain bending. More of the same table will not
  reach 2.0.
- Maximum displacement 8.0 mm at 60 N in +Y. No requirement on it, worth knowing.

### Is printing with layers along X feasible? (`review_work/printab.py`)

| Orientation | Footprint mm | Height mm | Fits 256 bed | Bed contact mm2 | Supported area mm2 (faces under 45 degrees, projected) | Mean height of it mm |
| --- | --- | --- | --- | --- | --- | --- |
| Layers along Y, +Y side down (plan) | 72 x 249 | 44 | yes | 287.6 (one knuckle face) | 7497 | 17 |
| Layers along X, -X edge down | 44 x 249 | 72 | yes | 9.5 (a line on the hub rim) | 4274 | 28 |
| Layers along X, +X edge down | 44 x 249 | 72 | yes | 7.9 | 4273 | 28 |
| Layers along Z, hub down | 72 x 44 | 249 | yes | 10.9 | 574 | 53 |

Feasible, with a cost. On its edge the part has no base of its own: the hub rim touches the bed on a line and the
stem and fork start 24 mm above it, so it needs a raft or brim and support under the whole stem and fork. The
supported area is smaller than in the planned orientation, which itself rests on one 288 mm2 knuckle face with the
hub and stem 9 to 18 mm in the air. Gains on edge: the mounting face and both cheek faces are vertical walls, the
slot needs no support. Losses: the top of the dia 30 locating bore is a bridge, and one flank carries support scars.
It is compatible with "say how it lies on the bed and where supports go": both can be said exactly. The plan told
the builder not to switch ("only one sensible way"); the builder obeyed and reported the number, which was correct
behaviour. The numbers do not support "only one sensible way".

## 3. The form, as a designer would see it

Shape numbers from `sheet.shape_stats` (mine equal the builder's):

| | flat_share | largest_flat | sharp_mm | sharp_per_area |
| --- | --- | --- | --- | --- |
| Boxy | 0.910 | 0.144 | 2406.4 | 12.30 |
| Idea A, crude | 0.247 | 0.098 | 615.4 | 3.94 |
| Organic, final | 0.209 | 0.084 | 862.0 | 5.14 |

The remaining flats are the two hub faces (2353 and 2278 mm2, 16.5 % together) and the two inner cheek faces. Sharp
edges by place: bore rims 208 mm, screw holes and scallops 166, slot and arch edges 162, pin hole rims 100, elbow
seam 86 (31 to 49 degrees), knuckle against stem 30, tunnel mouth 20.

Pictures looked at: `c1_boxy.png`, `idea_a.png`, `checkpoint_01.png` (byte-identical to `idea_a.png`),
`checkpoint_02.png`, `checkpoint_03.png` (byte-identical to `checkpoint_02.png`), `c2_before_after.png`, and my crops
of the elbow and the fork.

- **Where it reads organic.** The front and back outline from the hub into the stem is one tangent sweep, like the
  neck of a spoon. The lower third is the best part: the stem swells in Y and divides round a full R 16 arch, and
  from the side the fork reads as one branching form. The before-and-after is a clear step from plates to one body.
- **The elbow still reads as a plate with a handle.** The hub is a flat 8 mm disc with two flat faces. From the side
  it is a thin blade standing on a bulb. On the screw side the stem meets the flat face in a visible crease line
  right across the hub (31 to 41 degrees over 31 mm), and the two lower screw holes sit on that line with their
  scallops, which look like bites. On the motor side the stem leaves through the rim with a curved crease up to
  49 degrees. This is the "bolted from plates" the request ruled out, in its mildest form.
- **The stem is lumpy, not flowing.** A swelling at Z -50, a pinch at Z -74, a second swelling at Z -94, then the
  true waist: a turned baluster in every view. It is the loft artefact of section 1, not a decision, and it is the
  first thing the eye catches. Restrained it is not.
- **The wrist knuckle is a barrel pushed through the fork.** A crease ring runs round each cheek where the barrel
  meets the stem, and the cheek ends are a cylinder's flat faces. From the top view the fork end is a rectangle with
  two flanges. Acceptable, but assembled-looking.
- **The cuts.** The tunnel mouths are raw holes (in the bore wall and in the arch crown) with 90 degree rims. The pin
  holes and screw holes are plain, which is fine. Nothing sticks out anywhere: that part of the request is met.

**Does DESIGN.md name the same weak spot?** Partly. It names the elbow junction as the least happy part, with the
crease and the scallops, and it names the knuckle ring: both match. It does not name the pinch and bulge in the stem,
which is the larger fault and which it describes as intended ("near round at the waist"). It also does not say that
the hub itself is still a plate. Note that the "least happy" text is the planner's, written before anything was
built and filled in by `c2_finish.py`; the builder edited two lines by hand and said so. It is honest about what it
knew, but it is a forecast, not an observation of this part.

## 4. Process deliverables

| Item | Finding |
| --- | --- |
| `restate.md` before modelling | Met by the clock: "C2 restate.md written" 20:03:30, first C2 modelling 20:03:36. The text is the planner's `restate_C2.md` copied byte for byte (the report says so); "in your own words" is the planner's words |
| `checkpoint_01.png` within 20 minutes | Met: first stamp 0.6 min after "C2 start". The file kept is from the fifth run, 8.9 min (`results.json`). It is a copy of `idea_a.png` |
| Two different ideas, each with a picture | **Not met.** Only `idea_a.png`. Idea B (open frame) is a genuinely different idea but never built. Reported openly |
| Checkpoints compared with the request | Three checkpoints with a "missing" line each. The lines are script-made lists of what is not yet built and of shape numbers; only the last one refers to the look. Checkpoints 2 and 3 are the same picture |
| `DESIGN.md` at most 25 lines | Met: 25 lines |
| `results.json` keys | All C1 and C2 keys present. `ideas_tried` holds B with `built: false`, no picture |
| Before-and-after in one call | Met: one sheet, one scale |
| Checks | Fixed items measured on solid and STL, three cases, three sizes, verdict from `judge()`: met. STEP and SLDPRT are not in the folder (gitignored `_wip`): could not check |

Times in `REPORT.md` against `times.log`:

| Report | times.log | |
| --- | --- | --- |
| Set 20:02:46 to 20:54:23, 51.6 min | the same | right |
| C1 0.5 min; restate 20:03:29 to 20:03:30 | the same | right |
| Stage 1 "final run" 20:09:31 to 20:11:34, 2.1 min | that is the fourth of five runs; the last is 20:11:50 to 20:13:50, 2.0 min | **wrong row quoted**, duration right for the row quoted |
| Stage 2 final 20:44:51 to 20:45:38, 0.8 | the same | right |
| Stage 3 final 20:45:39 to 20:54:18, 8.7; first run 20:15:05 to 20:24:14 | the same | right |
| C2 total 50.9 | 51.6 - 0.7 | right |
| Launch times and pids (20:03:43, 20:02:54) | not in `times.log` | could not check |

No invented times found. `c2_ideas` ran five times because of idea B: (1) first run, stem volume 9.6 % under the
planner's number in all five loft tries; (2) the plan's first branch, "run once more", same; (3) a run after an edit
of `STEM_VOL` that had been rejected, so the old values were still in force, same; (4) with the measured volumes,
now "expected one body" at the window cut; (5) with the plan's second branch (window end points), same. Both of the
plan's branches for B were worked, then B was dropped as the plan allows and the gap was reported. What was not
done, and what the plan did not ask for, was to ask why a loft was 9.6 % short.

Other notes: four full study rounds were run (A, A2, A3, A2 again); the last repeated A2 to restore the final state
and reproduced every stress. The report's statement that three thickenings are one approach and not three is fair.

## 5. What would close the task

The R-list is in `eval/haiku-plan-c-followup/INSTRUCTIONS.md`, with a small numpy tool `r_tools.py` beside it. In
brief: rebuild with evenly spaced section rows (cures the pinch if spacing is the cause; a number decides), build and
picture idea B from the same fix, try the hub blend at R 2 and R 1.2, study once with layers along X and an exclusion
sweep, and state the on-edge print with its measured contact and support. Fallbacks keep the first-round geometry if
the loft does not improve.

Expected end state: gate met by `judge()` pass at about 2.4 with layers along X, two ideas pictured. Whether printing
on edge is acceptable is Joey's call; the report must put the 9.5 mm2 contact next to the 2.38.
