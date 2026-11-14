# Benchmark run haiku-d: SolidWorks tasks D1, D2, D3

Worktree: `J:\code\cad-daddy-wt\sw-eval-haiku-d`. Nothing committed or pushed. Results: [results.json](results.json).
Model: `claude-haiku-5-5` as configured for this session. Reasoning effort: not visible to me, so not stated.

## Times (UTC, from `date -u` and the run logs)

| Task | Start | End | Limit | Waiting (SolidWorks launch, mesh, solve) | Working |
| --- | --- | --- | --- | --- | --- |
| Reading (playbook, helpers, tasks) | 09:23:22 | 09:26 | none | 0 | about 3 min |
| D1 | 09:26 | 09:34 | 60 min | about 2 min (6 launches of 3 to 6 s, solves of 7 s and 33 s, meshes 4 to 22 s) | about 6 min |
| D2 | 09:34 | 09:40 | 90 min | about 1 min (5 launches, 3 builds) | about 5 min |
| D3 | 09:40 | 09:44 | 60 min | under 1 min (1 launch for six plates, one for part two) | about 3 min |

The task limits were not reached. D2 stopped early (see below), not for time.

No launch waited for another session. The busy instance belonging to `shoulder-study-fea` (pid 14040, then 2228) never blocked a launch of mine. The keeper (pid 10172) stayed up and was not touched.

## D1: a need, not a drawing (done)

**Restatement.** [restate.md](restate.md) has the five lines, the assumptions, the questions with the answers I assumed, and two ideas.

**Conflict found before modelling.** The board is 60 mm across Y in either flat orientation, and the envelope is Y ±25 (50 mm). So it must stand on edge in the XZ plane. Standing on edge, the 14 mm front-component allowance cannot be met: with the board at Y 17.5 to 19.1 the front clearance is 5.9 mm. I built to 5.9 mm and report the 14 mm as not met.

**Two ideas, different in kind.**
- A (built): an open printed frame bolted to the rail's front T-slot, four bosses at the board holes, board on the bosses. Picture: [d1_idea_a_mount.sheet.png](pictures/d1_idea_a_mount.sheet.png).
- B (rejected, picture only): a horizontal cradle on top of the rail. Its board is 60 mm across Y, outside the envelope by 5 mm each side. Picture: [d1_idea_b_envelope.sheet.png](pictures/d1_idea_b_envelope.sheet.png).

**Model.** [buck_mount.SLDPRT](../../_wip/sw-eval/haiku-d/d1/buck_mount.SLDPRT) (gitignored, in `_wip`), with `buck_mount.step` and `buck_mount.stl` beside it. Built by [d1_mount.py](d1_mount.py).
- Volume 8820.72 mm³ against hand 8820.63 (0.001 %). Box X ±42.5, Y 10 to 17.5, Z -17 to 43, so the top is 43 mm above the rail (limit 45).
- STL: watertight, one body, 8818.95 mm³ (0.02 % from the part).
- Mass 10.5 g in PETG (1.19 g/cm³).
- Stand-in rail and board for the assembly picture: [d1_assembly_a.sheet.png](pictures/d1_assembly_a.sheet.png), made by [d1_standins.py](d1_standins.py).

**Picture reads.** I opened each PNG as the playbook asks:
- Mount: a 85 x 60 frame with a 71 x 42 opening, four corner bosses, two rail holes in the bottom bar.
- Assembly: the frame on the rail's front face with the board in front, the rail as a long box behind.
- Idea B: the board and cradle sit far outside the rail's ±10 width, so the envelope failure is visible.

**Board in and out.**
1. Unplug the two 4 mm² pairs at the 60 mm wire edge (X +42.5).
2. With a 2.5 mm hex from the front, remove the four M3 screws in the board holes. These reach the bosses through the board.
3. Pull the board forward (+Y) off the four bosses.

The mount and its two M5 screws stay on the rail. The M5 heads sit behind the board, so they can be reached only after the board is off, which is not needed for removal.

**Hand check, 9 N case.** Each side bar is 7 wide (X) by 4 thick (Y), I about X = 37.33 mm⁴. Each side bar carries one top boss at 2.25 N, 39.5 mm from the bar root at Z 0.
- Stress at the surface, Z 0: σ = M c / I = 88.9 N·mm × 2 / 37.33 = **4.77 MPa**.
- Top-boss deflection: F L³ / 3 E I = 1.06 mm (arm 46.5 mm from the bottom bar).
- Transverse shear: 1.5 V / A = 0.12 MPa.

**Study** ([d1_study.py](d1_study.py), output [d1_study_results.json](d1_study_results.json)). Fixed: the two M5 hole walls (the screws are the rail contact; the back face at Y 10 is one ring face, so it cannot be fixed on the bottom bar alone). Load: 9 N over the four boss tops, pull (-9) and push (+9). Element size 1.5 mm, 37,590 nodes. Under the five checks:

| # | Check | Result |
| --- | --- | --- |
| 1 | Reaction equals load | 9.00 N against 9.00 N |
| 2 | Displacement sane | 1.94 mm against hand 1.06 mm. Same order, 1.8 times the top-boss hand value. The top bar also bends; I did not separate that out. Not verified |
| 3 | Stress in the plain section | Surface σz at the side-bar root (X 36 to 42, Z ±2): **±4.76 MPa** against 4.77 MPa hand. Pass |
| 4 | Peak away from fixtures and loads | 5.29 MPa at (36.2, 10, -2.7), on the side bar 4 mm above the bottom bar. The peak at the sharp opening corner (8.99 MPa at (35.5, 10, -6.25)) is singular, see 5 |
| 5 | Convergence | Sharp corner: 8.99 MPa at 1.5 mm, **10.25 at 1.0 mm** (+14 %), not converged. Bulk: 5.29 and 5.32 (converged) |

**Fillet and convergence.** A copy with R1 fillets on the four opening corners, [buck_mount_r1.SLDPRT](../../_wip/sw-eval/haiku-d/d1/buck_mount_r1.SLDPRT), added 3.43 mm³ (hand 3.43). At 1.5 and 1.0 mm the corner peak is 10.67 and 10.75 MPa (0.8 % apart, converged by the 5 % rule). Results: [d1_r1_results.json](d1_r1_results.json). The governing value is 10.7 MPa at the fillet root on the rail face, factor 45 / 10.75 = **4.2**. The side-bar root gives 5.3 MPa (factor 8.5). Across layers (Y is the layer normal when the frame is printed flat) the sharp model gave 0.02 MPa against 22.5 allowable, and shear 0.28 against 13. I did not recompute those on the filleted model.

**Open area (both faces, board 85 x 60 = 5100 mm²).**
- Front: 97.0 % open (boss footprints only).
- Back, frame only: 58.5 %.
- Back, with the rail counted (it sits 7.5 mm behind the board and covers 71 x 7 mm of the opening): **48.7 %**, below the 50 % asked. I report this as not met under the stricter reading.

**Print.** Mount lying flat on the bed (Y up, layers in XZ), bosses up, no supports. Note: the bosses are solid. The M3 pilot holes and heat-set inserts are **not modelled**, so the boss screw joint is a gap in the model.

**Not done or not verified in D1:** the weakest-point factor for layers on the filleted model; a second, bigger fillet (cheapest improvement would be R2 to R3 at the bottom-bar corners, not run); the pilot holes; the board's own front components (limited to 5.9 mm, not checked against any real part).

## D2: two halves round a bearing (partial)

**Built**, with no feature errors and volumes matching hand: [housing_upper.SLDPRT and housing_lower.SLDPRT and ring.SLDPRT](../../_wip/sw-eval/haiku-d/d2) (gitignored), with STL and STEP of each half. Built by [d2_housing.py](d2_housing.py).
- Upper half 19,551.37 mm³ (hand 19,551.37: block 34,344 − seat 7,246.85 − opening 6,122.17 − clearance holes 1,154.87 − counterbores 268.73).
- Lower half 20,279.30 mm³ (hand 20,279.30: block − seat − opening − insert holes 301.59 − M4 holes 394.08).
- Ring 2,199.11 mm³ (π(26² − 24²) × 7).

**Pictures.** [d2_housing_upper](pictures/d2_housing_upper.sheet.png), [d2_housing_lower](pictures/d2_housing_lower.sheet.png), [d2_pair](pictures/d2_pair.sheet.png). Each read as I expected: the seat opens through, the shoulder openings are visible, the counterbores are on the Y 32 face, the insert holes are on the split face and the M4 holes on the mount face.

**Spec problems found, and what I built instead.**
- **S1** Screws at X ±28.2 leave 0.5 mm (Ø3.4) and 0.2 mm (Ø4.0 insert) from the spec seat (Ø52). Built at X ±30: 2.5 and 2.2 mm walls with the Ø51.6 seat.
- **S2** Seat Ø52.0 equals the ring OD 52.0: a zero fit, and ±0.15 mm printing gives loose or too tight. Built Ø51.6, 0.4 mm diametral interference.
- **S3** Shoulder opening Ø43.5 is smaller than the inner ring OD 44.0, so it rubs the turning inner ring on its end face. Built Ø44.4, 0.2 mm clear, which still carries the outer ring's end face (r 24 to 25.8).
- **S4** Split gap not given. Built 0.4 mm (0.2 each half).
- **S5** Screws at Z 1 and Z 6 are 5 mm apart with Ø6 counterbores, so they overlap by 1 mm. SolidWorks refused the cut (the counterbore cut failed until I checked the sketch circles). Built Z 0.5 and 7.5, a 1 mm web.
- **S6** The clamp does not work as specified. Closing a 0.4 mm split with Y screws on a concentric seat changes the seat radius by about 0.0008 mm (hand: d²/8R with d/2 = 0.2 and R = 25.8). The halves do not squeeze the ring; it is held by the 0.4 mm interference alone. A real clamp needs an offset (pinched) seat or radial screws. I did not build that and did not test it.

**Clearances (built).** Ring to seat: −0.4 mm diametral (interference). Inner ring to shoulder: 0.2 mm radial. Screw Ø3.4 hole to seat: 2.5 mm. Insert Ø4.0 to seat: 2.2 mm. Counterbore to outside: 3.0 mm.

**Screw load, by hand.** 300 N along +Y pulls the halves apart through four screws: **75 N tension each**. 300 N along +X: 75 N shear each, no friction. I did not check either against a study.

**Print.** Each half printed with Z up (layers in XY, so the screw and bearing loads act in-layer). The seat ledge at Z 7 is a 3.6 mm radial overhang and needs support inside the seat.

**Not done (this is why D2 is partial).**
- No contact study for either load case, so no peak stress, no factor on yield, layer or shear, and no screw load from a study.
- No contact proof. The playbook asks for a reverse-load or bonded-twin test; none was run.
- The brief's ring-to-seat and half-to-half contact needs a multi-body model with clearances and screws. I did not attempt it in the time left, and I would not have trusted a first attempt.
- S6 is a design problem I found but did not fix.

## D3: six plates from a table, then a change (done)

**Part one.** One script, [d3_plates.py](d3_plates.py), built P1 to P6 from the table. Each feature checked against its hand volume, and each plate exported as STL.
- Table: [d3_table1.json](d3_table1.json). Every plate watertight, one body, STL within 0.2 % of the part volume.
- Table reading: "on circle Ø" is a pitch-circle diameter. Read as a radius, every hole lands outside the plate. The script uses R = Ø/2.

**Table problems, checked by hand before building** (numbers from [d3_as_written_checks.json](d3_as_written_checks.json)):
- **P1**: ring A (Ø3.4 on R25, 0 deg) and ring B counterbore (Ø8 on R30, 0 deg) overlap by 0.7 mm. Built with ring B turned 45 deg (min wall 1.0 mm).
- **P2**: ring A and ring B are the same six holes. Built with ring B turned 30 deg.
- **P4**: ring B holes and counterbores at R29 break out of OD 60 by 3.0 mm. Built OD 68 (1.0 mm wall at the counterbore). The 8 x 4.6 counterbore in a 5 mm plate leaves a 0.4 mm floor, below the 0.6 mm wall rule, so depth 4.0 (floor 1.0 mm).
- **P1, P3, P4**: a 1.0 mm wall at the counterbore spots, so a 1.0 mm chamfer would leave no flat. The part-two chamfer is 0.5 mm on these three, 1.0 mm elsewhere.

Plate rows (volume, hand value, mass, min wall, changed): see [results.json](results.json), `D3.plates`. P3 is built as written; P1, P2 and P4 are changed as above, with the reason in `why`.

**Part two** ([d3_plates.py part2](d3_plates.py)). Each saved plate was opened and edited, not rebuilt from the script, and saved as `_b`.
- Base depth +1.5 with `set_dim` on BASE.
- Counterbore depth +1.5 with `set_dim` on CB. The floor stays at its height from the bottom: P1 3.0, P2 3.0, P3 4.0, P4 1.0, P5 3.0, P6 3.0 mm.
- Top outside chamfer (0.5 or 1.0 mm, above).
- P3 only: ring A redrawn on R35 (Ø70 circle) with `redraw_circles`, turned 22.5 deg. At 0 deg the web to the counterbore is 0.3 mm; turned, the min wall is 1.0 mm.
- Table: [d3_table2.json](d3_table2.json). Each `_b` volume matches its hand value (chamfer included). Feature trees before and after match, with `TOP_CH` added.

**Weakest point of D3:** the hand values are the same formula as the script. The independent checks are the per-feature volume changes, which I worked by hand for P1 (base π·1000·6 = 18,849.6; holes 326.9 and 381.7; counterbore 412.3), and the STL.

## Playbook and helper problems

These are the places the playbook or a helper was wrong, unclear or missing something.
1. **Fixtures on part of a planar face.** A fixture on the bottom bar of the frame was not possible: its back face at Y 10 is one ring-shaped face for the whole frame. [05-fea.md](../../playbook/05-fea.md) says to make a load region its own face, but not how to fix one. I fixed the M5 hole walls instead, which is a reasonable idealisation, but the page should say it.
2. **Overlapping sketch regions give a vague error.** A counterbore whose circles overlap (5 mm spacing, Ø6) makes `extrude` raise "no cut changed the volume the right way (open sketch? sketch off the body? wrong side?)". The real cause was the overlap, which the message does not mention. A check for overlapping sketch regions would save time here.
3. **`new_part()` closes every open document**, not just the failed one. In a script that holds two parts, the first part's handle dies, and the next call fails with "The object invoked has disconnected from its clients". The playbook says `new_part()` closes documents but not that it closes all of them. I lost one export to this.
4. **`swkit.log()` prints local time** (this machine is UTC−6), not UTC, with no label. My timestamps here are from `date -u`. The brief asks for UTC.
5. **`Result.average()` returns a tuple** (von Mises mean and node count), and `layer_stress()` and `layer_shear()` return `(value, where)`. I first assumed a scalar. The playbook examples show the calls, but not the return values.
6. **Negative normal loads (pull)** are not in the playbook. `'normal'` with a negative value pulled the bosses outward, and the reaction came out at 9.00 N, so it works. Worth writing down.
7. **`Sk` on a face works** (I used the top face of a plate for the counterbores), which the playbook does not mention. `pick(kind='plane', normal=(0,0,1))` on a holed plate returns one top face, also not written down.
8. **My own errors, not the helpers':** a hole filter box a few tenths too tight; sampling σz at the neutral axis (mid-thickness reads zero, surface reads 4.76 MPa); a probe with a wrong `FeatureCut4` argument list; the "on circle Ø" radius misread; and a `new_part` call that closed documents I still needed. Each is fixed in the scripts.

## Files

- Scripts: [d1_mount.py](d1_mount.py), [d1_standins.py](d1_standins.py), [d1_study.py](d1_study.py), [d1_conv.py](d1_conv.py), [d1_fillet.py](d1_fillet.py), [d1_r1_study.py](d1_r1_study.py), [d2_housing.py](d2_housing.py), [d3_plates.py](d3_plates.py), [make_results.py](make_results.py).
- Results: [results.json](results.json), [d1_study_results.json](d1_study_results.json), [d1_conv_el1.json](d1_conv_el1.json), [d1_r1_results.json](d1_r1_results.json), [d3_table1.json](d3_table1.json), [d3_table2.json](d3_table2.json), [d3_as_written_checks.json](d3_as_written_checks.json).
- Pictures: [pictures/](pictures/) (D1: three sheets; D2: three sheets).
- Models (gitignored): `_wip/sw-eval/haiku-d/d1`, `d2`, `d3`.
- Logs: `_wip/sw-eval/haiku-d/*/*.log`.

Nothing was committed or pushed. SolidWorks instances are closed (each `job` exits its own PID). `--status` shows no instance of mine. The claim is released at the end of this run.
