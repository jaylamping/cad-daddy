# Follow-up for run `haiku-plan-d` (set D)

Everything below the next line is copied word for word from the reviewer's review of your first run. Only the
parts for this set are here.

---

## The review's corrected result for each task of this set

### D1

6. **Result:** buck_mount is one 11.8 g printed frame; the board comes out by four M3 screws from above with the
   mount left on the rail; 63 % of the underside open; 9 N gives about 2.5 MPa at the arm roots (factor 18 as
   reported; about 8 by hand at the M5 holes). The Y envelope of ±25 cannot be met by any mount: the board is 60 mm
   wide, so it and the pads under its holes reach Y ±30. That was said and assumed, not used as a reason to stop.
   Study numbers are the executor's and unaudited; check that parts under the board stay 8.5 mm in from its ends.

### D2

6. **Result:** the pair goes together and the contact model is sound: 300 N along Y puts 75.7 N on each screw (hand
   75), proven against a bonded twin 50 times stiffer; along X the ring wedges under the lower half and the screws
   carry 41 to 50 N tension (statics with the study's contact angles: 45.3). On one mesh the lowest factor is 5.8
   (shear between layers in the lower half, load along X), 7.3 on von Mises, 20.9 on layer tension. Not shown:
   convergence (one mesh), where the 0.55 mm in case X is, and tightening, which by hand is the case that limits
   this part (stay under about 0.2 N·m until it is modelled). Six specification problems were found and built round.

### D3

6. **Result:** all twelve plates match hand values to 0.01 mm³; four bad table rows and two bad change-request
   consequences were caught before building; the change was made by editing (same feature IDs, one new feature,
   floors unmoved). Three choices need a yes: P4 Ø68, P4 counterbore 3.0 deep, 0.4 mm chamfer on P1, P3 and P4.

## Follow-up runs for the PC (written for the same executor)

Rules for all of them: one script = one `with job() as j:`; `j.simulation()` first; at most four studies per job;
never under `timeout`; copy each job's log into `eval/<run>/wip-logs/`. Write every number from the log, not from
memory. Do not change anything not named here.

### R3. D2: find the 0.55 mm, correct the keys, then a series that fits the cap

a. No SolidWorks. Load `WIP/npz/D2_X_30.npz`. With the masks of `split(r)` in `d2_fea.py` (build a small object
   with `pos` and call it, or copy the mask lines): for each of ring, upper_all, lower_all, screw, pad print the
   largest `disp[:,4]` and the position of that node. For the ring also print the mean of the tangential
   displacement `(-y·ux + x·uy) / rho` and divide by 26 for the rotation in radians. Write one line: which body
   moves 0.555 mm, and whether it is a rigid turn of the ring (tangential mean near 0.5 mm, harmless) or something
   else (then stop and report before b).
b. No run. In results.json D2 set `sf_yield` 7.34, `sf_layer` 20.94, `sf_shear` 5.82, `governing` "lower half, case
   X, shear between layers 2.23 MPa at (21.71, −15.15, 6.93), factor 5.82, 3.0 mm mesh, not converged", `minutes`
   to the clock difference (about 12), `pads_share_n` 0.23. Keep `valid` as it is until c is done, but add to `why`:
   "model checks 1 to 5 pass; only convergence is missing".
c. One job of three studies, then a second job of three. Make `d2_conv.py`: `from d2_fea import *`; copy `run` as
   `run_c(j, d, name, force, el, cs)` and change only the faces and the controls: keep the five picks and their
   `must` counts, but collect `steel = [faces r 1.5] + [faces r 2.75]` and `petg = [faces r 2.0] + [faces r 3.0] +
   [faces r 1.7]`, and use `ctrl=[(up_seat + lo_seat + ring_out, cs), (steel, 1.5), (petg, 0.8)]`. Copy `one` as
   `one_c` calling `run_c`, writing to `d2c_rows.json`.
   - Job 1, case X (it governs): `D2C_X_12` (el 4.0, cs 1.2), `D2C_X_09` (4.0, 0.9), `D2C_X_07` (4.0, 0.7), force
     (300, 0, 0), predicted nodes 130,000 / 165,000 / 200,000 (my estimate from two mesh counts: low confidence),
     predicted displacement: the value step a found for the ring's body, or 0.55.
   - If a row is refused for over 200,000: rerun that row with el 5.0. If it is refused again: change `steel` to 2.0
     and `petg` to 1.0 and run all three rows again under new names (`D2D_...`), so that the series still changes
     one thing only.
   - First check, before anything else: `D2C_X_12` against `D2_X_30`: reaction; screw tensions 41.3, 40.8, 49.5,
     48.6 (each within 10 %); angles 9.4° and 56.1° (within 5°); lower `Z` shear 2.23 and upper `Z` vm 6.13 (within
     15 %). If not: stop, report both rows; the coarser steel changed the answer.
   - Each screw's `nodes` must be at least 20. If not, set `steel` to 1.2.
   - Job 2, case Y: the same three with force (0, 300, 0); `D2C_Y_12` must give four tensions within 15 % of 75.
   - Report, per half and per case, vm, layer and shear for layers along Z over the three rows, each step in
     percent, and `upper_excluded_vm` / `lower_excluded_vm`. Also print the upper half's three measures once more
     with a wider zone round the heads (`(dxz < 4.75) & (y > 26.5)` in place of `(dxz < 3.75) & (y > 27.5)`), because
     the present peak sits on the zone's edge. Verdict with the same rule as R1 step 6, on the lowest factor over
     everything.

### R4. D1: the same study with its log kept and the hidden section read (one job, about 4 minutes)

1. Run `d1_study.py` again with two additions after the `direction_table` line, and send the output to
   `eval/haiku-plan-d/wip-logs/d1_study.log`:
   ```python
   for D in (1.0, 2.0, 3.0, 5.0):
       m = r.away(dist=D)
       log('outside', D, 'mm of fixture and load faces: vm', r.peak(m), 'layer Z', r.layer_stress((0, 0, 1), m), 'shear Z', r.layer_shear((0, 0, 1), m))
   sp = r.in_box([44.0, -7.1, -0.1, 56.1, 7.1, 4.1]) | r.in_box([-56.1, -7.1, -0.1, -44.0, 7.1, 4.1])
   log('spine round the M5 holes: vm max', float(r.vm[sp].max()), 'mean sigma-x on the top face', float(r.s[sp & (r.pos[:, 2] > 3.95), 1].mean()))
   ```
2. Report the three convergence rows from the log, the four plateau lines, and the spine values. Hand for the spine
   beside an M5 hole: 1.94 MPa nominal, about 5.8 at the hole edge. If the value outside 1 mm is under 22.5 MPa,
   say so: the part passes there too. `sf_min` becomes the lower of the arm-root factor and 45 over the plateau
   value round the holes; say which.
3. Write the plan's hand values for the X and Y directions (1.35 and 1.2 MPa) into the report as hand values.

### R5. Paper corrections (no run)

- REPORT (set D): D2 took about 12 minutes; the whole set about 20.
