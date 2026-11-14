# Follow-up for run `haiku-plan-a` (set A)

Everything below the next line is copied word for word from the reviewer's review of your first run. Only the
parts for this set are here.

---

## The review's corrected result for each task of this set

### T1

6. **Result:** bracket.SLDPRT is as specified: 32974.02 mm³ (hand 32974.02), 39.24 g, one body, all nine holes and
   both sets of radii measured on the solid, STL watertight. Flag: 2.8 mm between the bore and each motor hole.

### T2

6. **Result:** bracket_b.SLDPRT is the saved T1 part edited, not rebuilt: 31643.00 mm³ (hand 31642.99), counterbore
   floors at Z 3.000, slot X 35 to 55, one body.

### T3

6. **Result:** fails. Tension across the layers at the lower motor-screw holes is 15.1 MPa and still rising
   (factor 1.49 against 2.0, hand 16.4 MPa); shear between layers 7.25 MPa (1.79, converged); von Mises 19 to 21 MPa
   (2.1 to 2.4). Reaction 150.0 N, load and support each tried two ways and agreeing.

### T4

6. **Result:** fails, more clearly than reported. A sharp inside corner has no finite stress (20 → 29 → 38 MPa, still
   climbing). With the 0.4 mm radius a printed corner has: 40.1 MPa von Mises in compression, converged (hand 39.3),
   factor 1.12; shear between the layers there 22.6 MPa, factor 0.57; and the motor-hole layer tension of T3 is
   unchanged (1.57 at this mesh, 1.49 on T3's finer one).

### T5

6. **Result:** two 3.5 mm ribs at the Y edges and printing on its side meet the requirement with margin: lowest
   factor 3.02 (layer tension 7.44 MPa, converged), shear 3.24 (converged), von Mises 3.60 at a sharp rib toe that
   still climbs 13 % per step and would need to rise 80 % to matter. Mass 42.48 g, +8.25 %. Not a clean "pass" until
   the toe is rounded and re-solved; it is not a fail.

### T6

6. **Result:** the pin bears on a strip about 3 mm wide along the top of the hole; peak bearing pressure 6.4 to
   6.8 MPa (Hertz 6.8 MPa; the textbook mean is 1.67), block von Mises 5.3 to 5.5 MPa at the hole mouths. The result
   is a valid contact result: reaction 500.0 N, 499.8 N through the hole, pads 0.04 %, and a thousandth of the load
   moves the pin 0.100 mm, the gap. The peak is known to ±6 %, not to the 5 % the playbook asks.

### T7

6. **Result:** five correct diagnoses; add the T7 object to results.json.

## Follow-up runs for the PC (written for the same executor)

Rules for all of them: one script = one `with job() as j:`; `j.simulation()` first; at most four studies per job;
never under `timeout`; copy each job's log into `eval/<run>/wip-logs/`. Write every number from the log, not from
memory. Do not change anything not named here.

### R1. T5: round the rib toes and solve again (one job, about 3 minutes)

1. Make `eval/haiku-plan-a/t5_toe.py`. Start with `from t3lib import *`. Copy the function `add_ribs` from
   `t5_ribs.py` into it unchanged (do not import `t5_ribs`: it runs a job when imported).
2. Add:
   ```python
   def add_toes(d, r=2.0):
       e = edges_where(d, lambda p: (abs(p[0] - 34) < 0.01 and abs(p[2] - 6) < 0.01) or (abs(p[0] - 6) < 0.01 and abs(p[2] - 34) < 0.01))
       must('rib toe edges', len(e), 4)                 # along Y, 3.5 long: two on the base at x 34, two on the upright at z 34
       v0 = volume(d)
       got = fillet(d, e, (r, 1.5, 1.0), 'RIB_TOE_R')
       if got is None:
           raise Failed('RIB_TOE_R did not build')
       log('toe radius built', got, 'volume change', volume(d) - v0, '(hand for r 2.0: +1.20 mm3)')
       single_body(d); must('rebuild errors', len(feature_errors(d)), 0); save(d)
       return got
   ```
3. Copy `run` from `t3lib.py` into the script as `run_c`, and change two things only: after the `rf` pick add
   `toe = pick(d, kind='cyl', r=TOE_R); must('toe faces', len(toe), 4)` (TOE_R = the radius `add_toes` returned), and
   in the `static(...)` call make the controls `ctrl=[(mh + bore, c), (rf, c), (toe, c)]`.
4. Job: `d = build_bracket(j, WIP / 'bracket_c2.SLDPRT'); add_ribs(d); TOE_R = add_toes(d)`; expect volume
   35693.99 + 1.20 (within 0.1 %); box 0, 0, 0, 80, 50, 46; `holes()` counts 4, 1, 4; export and `check_export`;
   close; `make_twin(j, WIP / 'bracket_c2.SLDPRT', WIP / 'bracket_c2_ld.SLDPRT')`; open the twin; three studies
   `T5_TOE_30` (3.0, 1.0), `T5_TOE_22` (2.2, 0.75), `T5_TOE_16` (1.6, 0.55) with `predict(name, n, 0.9, 'rib toe
   radius on the base, about 12 to 16 MPa von Mises')`, n = 45,000 / 90,000 / 195,000; `rows[name] = row(r)`; write
   `t5_toe_rows.json` after each.
5. If `T5_TOE_16` is refused for over 200,000 nodes: run it as `T5_TOE_18` with (1.8, 0.62).
6. Read `rows[...]['table']['Y']` for the three. Report vm, layer, shear, each with its place, its two steps in
   percent and its factor. Rule: all three factors at least 2.0 and every last step 5 % or less → pass. A factor
   under 2.0 at all three sizes → fail. Otherwise write "margin, not converged" with the value after two more steps
   (last value times the last ratio squared) and say where the moving peak is. If it is now on a rib side root
   (Y 3.5 or 46.5, Z 6, X between 10 and 34), say so and stop: that edge is the next one to round, in a new step.
7. Mass: volume · 1.19e-3; growth against 39.24 g must stay under 10 %.

### R2. T6: read what is there, then a matched mesh (no SolidWorks, then one job of about 8 minutes)

a. No SolidWorks. For `T6_PIN_12`, `T6_PIN_08`, `T6_PIN_05` load `WIP/npz/<name>.npz` (`pos`, `s`, `disp`). With
   `p = pos`, `rho = hypot(p[:,0], p[:,2] - 10)`, block nodes `rho > 5.096`, pin nodes `rho < 5.004`:
   - `line = block & (rho < 5.13) & (abs(p[:,0]) < 0.25) & (p[:,2] > 10) & (abs(p[:,1]) < 8)`; print the mean and the
     maximum of `-s[line, 3]` and the node count. Expect a mean of 6.0 to 6.8.
   - `strip = block & (rho < 5.13) & (p[:,2] > 10) & (abs(p[:,1]) < 8)`; print the largest `abs(p[:,0])` among strip
     nodes whose `-s[:,3]` is over 0.3 MPa (the contact half-width; hand 1.57 mm).
   - For the pin nodes print the mean and the largest of `abs(disp[:,1])` (UX) and of `disp[:,3]` (UZ), and the
     position of the node with the largest `disp[:,4]`. This says where the 0.249 / 0.166 / 0.153 mm is. If it is
     on the pin with UX or a tangential part much larger than the mean, write "the pin turns or slides on the soft
     pads; pressure unaffected". If it is on the block, stop and report: do not go on to b.
b. One job. `from t6 import *` (it has a `__main__` guard). Copy `run` as `run_m(j, d, name, c)` and change one line:
   `ctrl=[(hole, c), (mid, c)]`. Do not call `build`; open `WIP / 'block_fea.SLDPRT'`. Studies `T6M_12` (1.2),
   `T6M_08` (0.8), `T6M_06` (0.6); predicted nodes 45,000 / 84,000 / 138,000, displacement 0.13. `read(r)` each,
   plus the line mean of step a. Write `t6m_rows.json`.
   - Checks on each row: reaction Fz −500 ± 5; `fz_block` −500 ± 5; `fz_pads` under 5 N; pin rise 0.10 to 0.14.
     Ignore `lig_force`: it is not a force.
   - Converged = the line mean moves 5 % or less at the last step. Report the line mean, `p_all`, `contact_vm`,
     each with both steps. `valid` = true if the checks hold and the line mean is within 25 % of 6.76 MPa, whether
     or not it converged; say separately whether it converged.
   - If `T6M_06` is refused: use 0.65.

### R5. Paper corrections (no run)

- results.json T5: `verdict` cannot say "margin" (the sheet allows pass or fail), so leave the key until R1 is done
  and put "margin, not converged: lowest factor 3.02, von Mises 3.60 moving +13 % per step, 2.81 after two more"
  first in `notes`; `status` "partial".
- results.json T4 `notes`: lowest factor 0.57 (shear between Z layers at the R0.4 corner, 22.63 MPa, converged);
  layer factor at the motor holes 1.57 in T4's own rows; hand value 39.3 MPa by curved-beam theory (factor 3.57).
- results.json T6: `valid` true only after R2; until then add to `why`: "block reaction −499.80 N is the exact form
  of check 3 and passed; lig_force is a node mean and is not a force".
- results.json: add `T7` with `status` "done". REPORT (set A): 23 minutes, not 84; T3 Y-layer factor at the finest
  mesh 2.67, not 3.24.
