# Review of the executor's runs: haiku-plan-a (T1 to T7) and haiku-plan-d (D1 to D3)

Reviewer's clock: start Sat Nov 14 20:58:48 UTC 2026 (end time is in the reply; this file was written before the second reading).

Method. No SolidWorks here. Every number below comes from the job logs (`haiku-plan-a/wip-logs/*.log`,
`haiku-plan-d/d2_job2.log`, `d3_part1.log`, `d3_part2.log`) and the row files (`t3_rows.json`, `t4_sharp.json`,
`t4_r04.json`, `t5_rows.json`, `t6_rows.json`, `d2_rows.json`, `d3_part1.json`, `d3_part2.json`), checked against each
other and against hand values worked here. I compared every row file with the JSON line the job logged for the same
study, field by field (T3: 5 studies, T4: 6, T5: 3; T6 and D2 by reading): **no difference anywhere**. So the rows
are what the solver returned. Every disagreement found is between the rows and the executor's prose, summary keys
or statements about time.

What the files do not hold: **no log and no row file for D1** (its numbers exist only as constants typed into
`d1_results.py`), no log of D2's build job or fit check, no log of the first (failed) D3 run, no npz. Where that
stops a decision, it says so below.

Verdict words used: pass; fail; margin, not converged; not shown. Allowables: von Mises 45 MPa, tension across
layers 22.5 MPa, shear between layers 13 MPa (`common.ALLOW`, `swfea.PETG`). Required factor 2.0.

---

## Set A

### T1. Model a bracket from a specification

1. **Done (t1.log, 13:59:22 to 13:59:28).** L extruded 36000.00; root fillet R4 +171.68; base rounds −64.38; upright
   rounds −64.38; base holes −570.20; bore −2280.80; motor holes −217.90; rebuild errors 0. Box 0, 0, 0, 80, 50, 46.
   Four base holes measured at (25, 10), (25, 40), (65, 10), (65, 40), Z 0 to 6; bore at Y 25, Z 28, X 0 to 6; four
   motor holes at Y 14.04 / 35.96, Z 17.04 / 38.96; one R4 face with box [6, 0, 6, 10, 50, 10]; four R5 faces. STEP and
   STL exported; STL watertight, one shell, 32990.38 mm³, box exact.
2. **Valid: yes.** My hand volume: 80·50·6 + 6·50·40 = 36000; + (1 − π/4)·4²·50 = 171.68; − 2·(1 − π/4)·5²·6 = 64.38
   (base), the same for the upright; − 4·π·2.75²·6 = 570.20; − π·11²·6 = 2280.80; − 4·π·1.7²·6 = 217.90.
   Total **32974.02 mm³**; log 32974.0242. Motor hole offsets 15.5·sin 45° = 10.96: 25 ± 10.96 and 28 ± 10.96, as
   logged. Mass 32974.02 · 1.19e-3 = 39.24 g. STL volume +0.05 %.
3. **Verdict: pass.**
4. **Report against logs:** no number differs. Missing from the report: the hand table itself, and the plan's
   2.8 mm ligament note (bore to motor hole: 15.5 − 11 − 1.7 = 2.8 mm, under one hole diameter of 3.4), which
   07-done.md model item 3 asks for.
5. **Stopped short:** nothing that changes the result.
6. **Result:** bracket.SLDPRT is as specified: 32974.02 mm³ (hand 32974.02), 39.24 g, one body, all nine holes and
   both sets of radii measured on the solid, STL watertight. Flag: 2.8 mm between the bore and each motor hole.

### T2. Change an existing part

1. **Done (t2.log, 14:00:16 to 14:00:25).** Opened bracket.SLDPRT (32974.0242), `save_as` bracket_b, then three cuts:
   CBORE 657.38, SLOT_ENDS 339.29, SLOT_MID 334.35. Volume 31642.9999. Four counterbore floors at Z 3.000, floor area
   54.78 each, walls on the four hole centres; slot end faces X 35 to 38 and 52 to 55, Y 22 to 28. Feature tree before
   and after: the 13 T1 features with the same IDs, then 9 new ones. bracket.SLDPRT SHA unchanged (910913e062bd5eb2).
2. **Valid: yes.** Hand: counterbores 4·π·(5² − 2.75²)·3 = 657.38; slot (14·6 + π·3²)·6 = 112.27·6 = 673.65
   (log 339.29 + 334.35 = 673.64). 32974.02 − 657.38 − 673.65 = **31642.99**. Floor annulus π·(25 − 7.5625) = 54.78.
   Slot 20 long (35 to 55), 6 wide (22 to 28), centred (45, 25).
3. **Verdict: pass.**
4. **Report against logs:** none.
5. **Stopped short:** the bracket_b STL was exported but not checked (no watertight line in the log); the task did not
   ask for an export.
6. **Result:** bracket_b.SLDPRT is the saved T1 part edited, not rebuilt: 31643.00 mm³ (hand 31642.99), counterbore
   floors at Z 3.000, slot X 35 to 55, one body.

### T3. Static study with a verdict

1. **Done (t3_job1.log, t3_job2.log).** Twin bracket_ld = bracket (32974.02, same part) + four Ø7 × 1 pressure pads
   (50 MPa) on the back face over the motor holes; bracket_ld_w adds four Ø10 steel washers. Five studies:

   | Study | el / ctrl | Nodes | Fixture | Load | Reaction Fx | Max disp | vm (D 3) | Layer Z | Shear Z |
   | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
   | T3_PADS_30 | 3.0 / 1.0 | 42,611 | 4 hole walls | 150 N on pads | −149.999 | 2.835 | 19.25 | 13.97 | 7.09 |
   | T3_PADS_22 | 2.2 / 0.75 | 85,355 | walls | pads | −149.996 | 2.842 | 21.02 | 14.33 | 7.15 |
   | T3_PADS_16 | 1.6 / 0.55 | 183,846 | walls | pads | −150.001 | 2.844 | 19.12 | 15.12 | 7.25 |
   | T3_REMOTE | 2.2 / 0.75 | 85,355 | walls | rigid on bore | −150.000 | 2.357 | 15.78 | 13.35 (rim 9.72) | 7.26 |
   | T3_WASHERS | 2.2 / 0.75 | 86,443 | washer tops | pads | −150.010 | 2.826 | 21.04 | 14.40 | 7.14 |

   Fixture box X 22.25 to 67.75, Y 7.25 to 42.75, Z 0 to 6 (the four hole walls); load box X −1, Y 10.54 to 39.46,
   Z 13.54 to 42.46 (the four pad faces). Materials logged right on every body.
2. **Valid: yes.** Right part (twin volume equal), right faces (boxes), reaction −150.0 N (0.001 %), Fy and Fz under
   0.01 N. Hand values, mine: Z = 50·6²/6 = 300 mm³; back face at Z 12: 150·16/300 = 8.00 MPa, study 8.04 (+0.5 %);
   base bottom at X 15: 150·25/300 − 150/300 = 12.0, study 12.04 (+0.3 %); lower motor-hole rim: 150·10.96/300 = 5.48,
   times 3 = 16.4, study 15.12 (−8 %); tip 2.5 mm by hand, study 2.84 (+14 %). Load two ways: pads 14.33 against rigid
   13.35 at the same mesh, and the rigid load reads the motor-hole rims at 9.72 against 14.33: the pads govern, as the
   playbook says they should. Support two ways: 14.40 against 14.33 (+0.5 %), vm 21.04 against 21.02, shear 7.14
   against 7.15. Plateau at el 1.6: vm 23.22 outside 1 mm, 19.12 outside 2, 3 and 5 mm: D 3 stands. Excluded maximum
   26.82 MPa at the fixed hole mouths.
3. **Correct numbers, layers along Z (as the task prints it):**

   | Measure | 3.0 | 2.2 | 1.6 | Steps | Converged | Factor at 1.6 |
   | --- | --- | --- | --- | --- | --- | --- |
   | tension across layers | 13.97 | 14.33 | 15.12 | +2.6 %, +5.5 % | no (5.5 > 5) | 22.5 / 15.12 = **1.49** |
   | shear between layers | 7.09 | 7.15 | 7.25 | +0.8 %, +1.4 % | yes | 13 / 7.25 = **1.79** |
   | von Mises | 19.25 | 21.02 | 19.12 | +9.2 %, −9.0 % | no (it hops between two hole rims) | 45 / 19.12 = 2.35 (2.14 at el 2.2) |

   Governing: tension across layers at the lower motor-hole rims, back face, (0.24, 34.32, 17.48).
   **Lowest factor over all studies and measures, Z layers: 1.49** (T3_PADS_16). The layer factor is under 2.0 at all
   three sizes (1.61, 1.57, 1.49) and falling; the shear factor is under 2.0 and converged (the task names only von
   Mises and layer tension, the playbook wants all three). **Verdict: fail.** It does not need convergence to fail.
4. **Report or results.json against rows:**
   - REPORT: "Y layers pass von Mises and layer (sf 3.24 at finest)". Rows: Y layer factor at the finest mesh is
     22.5 / 8.41 = **2.67**; 3.24 is the coarsest mesh (6.94 MPa at el 3.0).
   - results.json `sf_yield` 2.35 / `peak_vm_mpa` 19.12 is the finest row, but von Mises is not converged and read
     21.02 (factor 2.14) one mesh earlier. The honest statement is "2.1 to 2.4, not converged".
   - REPORT timing: "Run ended 14:21 local (about 1 h 24 min)" with start 13:57:34. The logs run from 13:58:40 to
     14:18:20, and set D's log starts at 14:20:25: the run took **about 23 minutes, not 84**. "SolidWorks about 16 min
     out of 84" should read 16 of 23.
5. **Stopped short:** nothing that changes the verdict. The report lacks the hand table and the print-direction table
   in words (they are only in t3_rows.json).
6. **Result:** fails. Tension across the layers at the lower motor-screw holes is 15.1 MPa and still rising
   (factor 1.49 against 2.0, hand 16.4 MPa); shear between layers 7.25 MPa (1.79, converged); von Mises 19 to 21 MPa
   (2.1 to 2.4). Reaction 150.0 N, load and support each tried two ways and agreeing.

### T4. The same study on a variant

1. **Done (t4_job1.log, t4_job2.log).** bracket_sharp built from the script without the fillet: 32802.3427 mm³
   (hand 32974.02 − 171.68 = 32802.34), box right, no R4 face, STL watertight. bracket_r04: 32804.0595
   (hand + (1 − π/4)·0.16·50 = 1.717). Pad twins, same part. Global 2.2, motor holes and bore 0.75, only the corner
   control changes:

   | Series | Control | Nodes | Corner vm | σz at corner | Shear Z (whole part) | Layer Z | Reaction | Max disp |
   | --- | --- | --- | --- | --- | --- | --- | --- | --- |
   | sharp | 1.0 | 70,569 | 20.45 | −23.95 | 9.68 | 14.30 | −149.997 | 3.135 |
   | sharp | 0.5 | 80,005 | 28.51 | −33.85 | 15.43 | 14.33 | −149.991 | 3.142 |
   | sharp | 0.25 | 98,575 | 37.75 | −46.79 | 20.18 | 14.35 | −150.003 | 3.145 |
   | R0.4 | 0.3 | 94,865 | 38.11 | −34.93 | 21.71 | 14.33 | −149.997 | 3.123 |
   | R0.4 | 0.2 | 122,464 | 39.66 | −34.94 | 22.59 | 14.34 | −150.004 | 3.124 |
   | R0.4 | 0.13 | 166,370 | 40.05 | −34.78 | 22.63 | 14.30 | −150.012 | 3.125 |
2. **Valid: yes,** and the hand value the executor left "not explained" closes. Reaction −150.0 N in all six; plain
   sections 8.08 to 8.11 (hand 8.0) and 12.03 to 12.04 (hand 12.0). The plan's hand value (11.0 · Kt 2.2 = 24 MPa)
   used a shoulder-fillet factor, which is the wrong model for the inside of a knee. Curved-beam value, mine: inner
   radius 0.4, outer 6.4, depth 6: r_n = 6 / ln(6.4 / 0.4) = 2.164; centroid 3.4; e = 3.4 − 2.164 = 1.236;
   σ_inner = M·(r_n − r_i) / (A·e·r_i) = M·1.764 / (6 · 1.236 · 0.4) = 0.595·M per mm width, against 6·M / 6² =
   0.1667·M for a straight wall: **factor 3.57**. 11.0 · 3.57 = **39.3 MPa**; study 40.05 (+2 %). With the base-side
   moment (12.5 MPa nominal) it is 44.6: the study sits between. The study is right and the plan's 24 MPa was wrong.
3. **Correct numbers.**
   - Sharp corner: 20.45, 28.51 (+39 %), 37.75 (+32 %). Singular, compressive. **It has no stress value.**
   - R0.4 corner von Mises: 38.11, 39.66 (+4.1 %), 40.05 (+1.0 %): converged. Factor 45 / 40.05 = **1.12**.
   - R0.4 corner shear between Z layers: 21.71, 22.59 (+4.1 %), 22.63 (+0.2 %): converged. Factor
     13 / 22.63 = **0.57**, at (6.13, 11.88, 6.11). This is in the rows (`table.Z.sf_shear` 0.57) and the executor
     never mentions it. Caveat: the layers there are pressed together (σz −34.8 MPa), which the single 13 MPa
     allowable does not credit; by the playbook's three measures it is the lowest factor all the same.
   - Tension across layers at the motor holes, in T4's own rows: 14.30 MPa, factor 22.5 / 14.30 = **1.57** at this
     mesh (motor-hole control fixed at 0.75, so it is one mesh size, not a series).
   - **Lowest factor: 0.57** (shear between layers at the as-printed corner); then 1.12 (von Mises there); then 1.57
     (layer tension at the motor holes). **Verdict: fail.**
4. **Report or results.json against rows:**
   - "Verdict fail (motor-hole layer factor 1.49 and corner von Mises sf 1.12)". 1.49 is T3's el 1.6 result on the
     filleted part. T4's rows give 14.30 MPa = **1.57**. And the lowest factor in T4's rows is **0.57**, not 1.12.
   - "Averages at the R0.4 corner ..." are right (19.6 / 16.7 / 14.7 on 760 / 2527 / 6605 nodes), but the plan asked
     for the sharp corner's averages (15.3 / 12.5 / 10.4 on 142 / 552 / 1721 nodes at control 0.25).
   - "Discrepancy ... not explained ... Kt about 3.2": explained above (3.57 by curved-beam theory).
5. **Stopped short:** the hand discrepancy of 67 % was reported and left (06-judgment.md question 2: find out which
   is wrong before going on). Ten minutes of hand work closes it; no run is needed. The T4 picture was rendered and
   not opened (the executor says so).
6. **Result:** fails, more clearly than reported. A sharp inside corner has no finite stress (20 → 29 → 38 MPa, still
   climbing). With the 0.4 mm radius a printed corner has: 40.1 MPa von Mises in compression, converged (hand 39.3),
   factor 1.12; shear between the layers there 22.6 MPa, factor 0.57; and the motor-hole layer tension of T3 is
   unchanged (1.57 at this mesh, 1.49 on T3's finer one).

### T5. Make it pass

1. **Done (t5_ribs.log).** Step 1 read T3's rows for layers along Y: shear 6.97 / 6.61 / 7.24 MPa, factors 1.86 /
   1.97 / 1.79: printing on its side alone fails on shear at all three sizes, so the plan's rib path was taken
   (correctly). bracket_c = T1 bracket + two ribs (RIB_A, RIB_B, 1359.98 mm³ each): 35693.9888 mm³, box unchanged,
   hole counts 4 / 1 / 4, STL watertight. Three studies, pads load, hole walls fixed:

   | Study | Nodes | Reaction | Max disp | vm (Y table) | Layer Y | Shear Y | vm excluded (within 3 mm of the holes) |
   | --- | --- | --- | --- | --- | --- | --- | --- |
   | T5_RIB_30 | 43,627 | −150.000 | 0.903 | 10.68 | 7.05 | 4.00 | 16.62 |
   | T5_RIB_22 | 87,418 | −149.996 | 0.907 | 11.06 | 7.15 | 3.93 | 16.41 |
   | T5_RIB_16 | 190,958 | −149.998 | 0.911 | 12.51 | 7.44 | 4.01 | 18.98 |
2. **Valid: partly shown.** Right part: 32974.02 + 2 · (½·28·28·3.5 − (1 − π/4)·16·3.5) = 32974.02 + 2 · 1359.98 =
   35693.98 (log 35693.99). Mass 35693.99 · 1.19e-3 = **42.48 g**, growth 2719.97 / 32974.02 = **8.25 %** (limit
   10 %). Same supports and loads as T3 (boxes equal), reaction 150.0 N. Not shown: a plain-section hand value. The
   plan gave none ("at least halved"), and the executor's `checks()` still reads the unribbed sections. A T-section
   beam value does not predict it (at Z 12: I = 27,057 mm⁴, centroid 7.75 mm from the back, σ = 2400·7.75 / 27057 =
   0.69 MPa against the study's 1.08; base at X 15: 0.78 against 3.80): the ribs sit at the edges and the 43 mm of
   plate between them still bends locally, so beam theory is the wrong hand model, and I cannot close check 3 from
   the files. What does support the result: reaction exact, displacement 0.91 mm against the 0.8 predicted, and the
   same mesh settings reproducing T3. Also: the hole positions on bracket_c were counted, not measured (same build
   function as T1, so low risk); and the ribs take Y 0 to 3.5 and 46.5 to 50 on the motor side out to X 34, Z 34,
   leaving 43 mm between them. Whether the motor fits there is not in the task sheet and was not checked.
3. **Correct numbers, layers along Y (on its side):**

   | Measure | 3.0 | 2.2 | 1.6 | Steps | Converged | Factor at 1.6 |
   | --- | --- | --- | --- | --- | --- | --- |
   | von Mises | 10.68 | 11.06 | 12.51 | +3.6 %, +13.1 % | **no** | 45 / 12.51 = 3.60 |
   | tension across layers | 7.05 | 7.15 | 7.44 | +1.4 %, +4.1 % | yes | 22.5 / 7.44 = **3.02** |
   | shear between layers | 4.00 | 3.93 | 4.01 | −1.8 %, +2.0 % | yes | 13 / 4.01 = 3.24 |

   Lowest factor 3.02 (layer tension at an upper motor-hole rim, front face, (6.0, 35.68, 40.64)). The measure that
   moves is von Mises at the rib toe on the base, (34.0, 49.13, 6.0), a sharp re-entrant edge. Two more steps of the
   same size: 12.51 · 1.131² = **16.0 MPa, factor 2.81**; layer tension 7.44 · 1.041² = 8.06, factor 2.79. Even the
   excluded fixture-edge value holds: 45 / 18.98 = 2.37. Nothing is under 2.0 and nothing would be after two more
   steps. **Verdict: margin, not converged.** (Other directions from the same result: Z shear 4.86 / 5.55 / 6.04,
   factor 2.15 and not converged; X shear 6.11, factor 2.13. Y is the right choice.)
4. **Report or results.json against rows:**
   - results.json `verdict` "fail" with `sf_yield` 3.6 and `sf_layer` 3.02 in the same object, `status` "done", and
     notes that say "all three measures pass 2.0". The rows show no failing measure. The word "fail" came from the
     plan's rule (see the last section), not from the result.
   - REPORT "status: not shown" against results.json `status` "done".
5. **Stopped short.** The executor wrote "a rib-end radius would settle it" and did not do it, with T5 finished at
   14:10:46 and the whole set at minute 23. Next step (follow-up R1): R2 rounds on the four rib-toe edges (adds
   4 · 3.5 · 2² · (tan 22.5° − π/8) = 1.2 mm³, mass unchanged at 42.48 g), control on the new faces, the same three
   sizes 3.0 / 1.0, 2.2 / 0.75, 1.6 / 0.55, read the Y table. Expected: von Mises settles between 12 and 16 MPa
   (factor 2.8 to 3.7).
6. **Result:** two 3.5 mm ribs at the Y edges and printing on its side meet the requirement with margin: lowest
   factor 3.02 (layer tension 7.44 MPa, converged), shear 3.24 (converged), von Mises 3.60 at a sharp rib toe that
   still climbs 13 % per step and would need to rise 80 % to matter. Mass 42.48 g, +8.25 %. Not a clean "pass" until
   the toe is rounded and re-solved; it is not a fail.

### T6. Contact between two bodies

1. **Done (t6.log, 14:11:11 to 14:18:20, 7 minutes of the 40).** Six bodies: block 21548.62 mm³ with the Ø10.2 hole,
   pin in three steel pieces (2670.35 + 2 · 628.32), two soft pads Ø3 × 1.5 (0.5 MPa) on the pin's end faces. Block
   bottom and pad outer faces fixed; 250 N rigid remote load on each end piece; no-penetration set hole to pin with
   the real 0.1 mm radial gap; direct sparse (macro line "after 7"). Materials logged right.

   | Study | Hole ctrl | Nodes | Reaction Fz | Block Fz | Pads Fz | Pin rise | p_mid | p over hole | Block vm | Max disp |
   | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
   | T6_PIN_12 | 1.2 | 52,146 | −500.005 | −499.804 | −0.201 | 0.1297 | 6.52 | 6.71 | 5.54 | 0.249 |
   | T6_PIN_08 | 0.8 | 72,305 | −500.002 | −499.801 | −0.201 | 0.1295 | 5.96 | 6.23 | 5.16 | 0.166 |
   | T6_PIN_05 | 0.5 | 122,007 | −500.001 | −499.799 | −0.201 | 0.1295 | 6.77 | 6.77 | 5.33 | 0.153 |
   | T6_PROOF (0.25 N per end) | 1.2 | 52,146 | −0.500 | −0.352 | −0.148 | 0.1001 | 0.01 | 0.08 | 0.04 | |
2. **Valid: yes.** The executor wrote `valid: false`; that is wrong on the evidence in its own log.
   - Right parts (volumes equal the hand values; total 25496.81), right supports and loads (boxes).
   - Reaction −500.00 N. The block's own reaction, which can only have come through the hole, is −499.80 N; the
     pads carry 0.201 N = 0.04 % (hand: 2 · 0.81 N/mm · 0.1295 mm = 0.21 N).
   - Contact proof, the one that fits a body with clearance: a thousandth of the load lifts the pin 0.1001 mm, the
     gap exactly, against 0.1295 mm at full load: 77 % of the movement for 0.1 % of the load. A bond would give
     0.00013 mm. In the proof run the pads hold 0.148 N (hand 1.62 · 0.100 = 0.16) and the block 0.352: sum 0.500.
   - Hand value: Hertz line contact, R* = 5 · 5.1 / 0.1 = 255 mm, E* = 1 / (0.856 / 1900 + 0.922 / 210000) =
     2198 MPa, 16.67 N/mm, b = √(4 · 16.67 · 255 / (π · 2198)) = 1.57 mm, p0 = 2 · 16.67 / (π · 1.57) =
     **6.76 MPa**. Study 6.52, 5.96, 6.77: −4 %, −12 %, 0 %. All inside the 25 % band, and the peak is where it
     should be, (0.02, 2.88, 15.1), the top of the hole. Textbook mean F / (d·L) = 500 / 300 = 1.67 MPa.
   - The "failed check 3" is not a failure of the model. `lig_force` (1053, 1430, 1820 N against a window of 400 to
     650) is a node mean of σz times 894 mm², and the nodes crowd at the hole wall as the control shrinks, which is
     exactly why it grows with refinement. 05-fea.md warns about this twice ("a mean over nodes drifts as nodes
     crowd"; "nodal stress summed over a face is not a force"). The same check has an exact form, which passed:
     block reaction −499.80 N.
   - One thing unexplained, and not noticed by the executor: maximum displacement 0.249 / 0.166 / 0.153 mm against a
     pin rise of 0.1295. Nothing in the model should move more than the pin. The likeliest cause is the pin turning
     about its own axis or sliding sideways (frictionless, held in those directions only by the soft pads), which
     does not change the pressure; the files cannot confirm it (follow-up R2a).
3. **Correct numbers.** Peak bearing (contact) pressure on the hole: **6.4 ± 0.4 MPa** (mean of the three meshes
   6.42; 6.77 at the finest; Hertz 6.76), along the top of the hole at mid length; no rise toward the mouths
   (6.29, 6.23, 5.99). Block von Mises 5.54 / 5.16 / 5.33 at the mouth edge on the face Y ±15. Convergence: p_mid
   −8.6 %, +13.6 %; p over the hole −7.2 %, +8.7 %; block vm −6.9 %, +3.3 %. **Not converged by the 5 % rule, but it
   does not climb: it scatters ±6 % about 6.4**, which is what the maximum of a nodal contact stress does when the
   hole mesh (1.2 to 0.5) and the pin mesh (fixed 1.0) do not match. Against printed PETG: 45 / 6.77 = 6.6 on the
   pressure, 45 / 5.54 = 8.1 on von Mises; after two more steps of the last size, 6.77 · 1.136² = 8.74 MPa, factor
   5.1. The task sets no factor; taking 2.0: **margin, not converged.** Layer measures in the block were not read
   (no print direction given, no rows).
4. **Report or results.json against rows and logs:**
   - `valid: false` and "Check 3 failed", against block reaction −499.80 N, pads 0.04 %, proof run, and all three
     meshes within 12 % of the hand value.
   - REPORT: "the plan's fallback (a fifth study, control 0.35) was not run because it needs a new job and the
     40-minute cap was near." Its own timing table: T6 ran 14:11:17 to 14:18:20 and "40-minute cap not reached".
     **Seven minutes used, 33 left.**
   - `solver` names a benchmark file but not the solver read from it. The log line is "after 7": Intel direct
     sparse (`swfea.SOLVER_DIRECT` comment). Not a disagreement; an unread check.
5. **Stopped short.** Closed at 7 of 40 minutes with a series that was noisy, not divergent. Next steps, in order
   (follow-up R2): (a) no solve: from the three saved npz files read the mean of −σz over the crown line, not the
   maximum node, and the contact half-width (hand 1.57 mm); (b) one job, three studies with the pin's contact face
   meshed like the hole: 1.2 / 1.2, 0.8 / 0.8, 0.6 / 0.6, el 3.0. My node estimate from the three counts in the log
   (nodes ≈ 37,500 + 21,100 / c² for the hole, and the same law scaled by area for the pin): about 45,000, 84,000,
   138,000. The plan's own fallback (control 0.35) cannot work: the same fit gives 37,500 + 21,100 / 0.1225 =
   210,000 nodes, over the cap.
6. **Result:** the pin bears on a strip about 3 mm wide along the top of the hole; peak bearing pressure 6.4 to
   6.8 MPa (Hertz 6.8 MPa; the textbook mean is 1.67), block von Mises 5.3 to 5.5 MPa at the hole mouths. The result
   is a valid contact result: reaction 500.0 N, 499.8 N through the hole, pads 0.04 %, and a thousandth of the load
   moves the pin 0.100 mm, the gap. The peak is known to ±6 %, not to the 5 % the playbook asks.

### T7. Diagnose

1. **Done:** five answers in REPORT.md, each with what is happening, next, must not. Nothing run.
2. **Checked against the pages:** (a) half-closed 2536 is not launched over, PID and `taskkill /PID 2536 /T /F` go to
   Joey, 20948 is busy and left alone: 01-session.md lines 27, 28, 88. (b) out of memory in the factorisation, coarsen
   the global size and keep the controls, never report the failed run: 05-fea.md "When the solve fails". (c) STL
   moved into positive space by the export toggle, re-export with `export()`, compare boxes: 06-judgment.md table.
   (d) singular fixed edge, neither 61 nor 38, "not shown" until something converges. (e) busy is not hung, read the
   hidden-dialog log, wait. All five are right.
3. **Verdict: pass.**
4. **Against the sheet:** results.json has no `T7` object; TASKS.md asks for one object per task with `status` and
   `notes`, and the plan's checklist has `put('T7', ...)`. The report says "T7 is in REPORT only, as the task sheet
   asks", which the sheet does not say.
5. **Thinner than the plan:** (c) does not say that the offset equals minus the part's lowest corner (box starts at
   X −41.5, Z −12.0); (d) leaves out the second support model and the step sizes (+24 %, +30 %, growing).
6. **Result:** five correct diagnoses; add the T7 object to results.json.

---

## Set D

### D1. A need, not a drawing

1. **What the files show.** Scripts `d1_build.py`, `d1_study.py`, `d1_fit.py`, `d1_open.py`; four pictures (I opened
   `d1_assembly.png`: spine on the rail, two arms, four pads, board and rail stand-ins, M5 tabs beyond the board's
   ends); `restate.md` with the five lines, assumptions and six questions with assumed answers. **There is no log
   and no row file for D1.** Every study number in the report and in results.json was typed into `d1_results.py`
   ("values taken from the run logs"). I cannot check them against what the solver returned.
2. **Valid: consistent with hand values, not verifiable from logs.**
   - Part: 112·14·4 = 6272; arms 2 · (310·8 − 448) = 4064; R3 corners 8·(1 − π/4)·9·4 = 61.81; R2.5 steps
     4·(1 − π/4)·6.25·8 = 42.92; M5 holes −190.07; insert holes −301.59: **9949.07 mm³**, 11.84 g. Reported 9949.07.
   - Open area under the board: (85·14 + 2·7.5·60 − 2·7.5·14 + 7.7) / 5100 = 1887.7 / 5100 = 37.0 % covered,
     **63.0 % open**; reported 0.6298 measured on the STL.
   - Study as reported: 9 N on the four pad tops, two M5 hole walls fixed, reaction Fz +9.0; three meshes 30,598 /
     58,907 / 125,748 nodes; von Mises 2.47 / 2.49 / 2.49, layer Z 0.17 / 0.13 / 0.13, shear Z 0.70 / 0.70 / 0.71.
     Hand: arm root M = 2.25 · 19.5 = 43.9 N·mm, Z = 8·4²/6 = 21.33, σ = 2.06 MPa; 2.49 / 2.06 = 1.21 for the R3
     corner. Arm top at |Y| 15: 2.25 · 11.5 / 21.33 = 1.21 against 1.22 reported.
   - Displacement 0.158 mm against 0.09 by hand: the executor accepted it without a reason. The reason: the hand
     value clamps the arm at the spine's edge, but the arm and the spine are one 4 mm plate there and both pads load
     it evenly, so it bends right across to the centre line: 2.25 · 26.5³ / (3 · 1900 · 42.67) = 0.172 mm. The study
     lies between the two models (0.09 and 0.19 with the spine's 0.014), as it should.
3. **Correct numbers.** As reported, layers along Z: von Mises 45 / 2.49 = 18.07, shear 13 / 0.71 = 18.3, layer
   tension 22.5 / 0.13 = 173 (reported 179, from unrounded values); all three converged (last steps 0 %, 0 %, +1.4 %).
   But 18.07 is the lowest factor **outside the 4 mm exclusion round the fixed M5 holes**, and the section the plan's
   own hand table calls nearly as stressed lies inside it: the spine at an M5 hole, net 8.5 × 4, 1.94 MPa nominal,
   times about 3 for the hole = 5.8 MPa, factor 45 / 5.8 = **7.7 by hand**. The script logs the excluded maximum; the
   report does not give it. So: `sf_min` = 18.07 at the arm root; at the screw holes about 8 by hand and not shown by
   the study. Either way far above 2.0. Only the load along Z was solved; X (about 1.35 MPa von Mises) and Y (about
   1.2 MPa) are the plan's hand values and are not in the report at all.
   **Verdict: pass on the 9 N case** (factor at least about 8 by hand, 18 in the study as reported), with the caveat
   that the study numbers cannot be audited. **Envelope: not met and cannot be** (see 6).
4. **Report or results.json against files:** nothing to compare (no log). Internal: `minutes` 5 agrees with the
   clock times given (14:20:25 to about 14:26). Layer factor 179 against 22.5 / 0.13 = 173 is rounding. The
   assumption "parts may sit on both faces up to 3 mm from the edges" disagrees with the stand-in used for the fit
   check (`BOTTOM_PARTS` X ±34, Y ±21: 8.5 and 9 mm in from the edges). With parts 3 mm from the edge the pads
   (X 35 to 42.5, Y 23 to 30) would be in the way; the fit check as run cannot see that.
5. **Stopped short:** (a) the log was not kept; (b) the excluded maximum and the plateau round the M5 holes are
   missing, so the weakest section may be the one the mask hides; (c) no second support (07-done.md study item 2
   names exactly this case, a fixed hole wall); (d) the hand table for X and Y is not in the report; (e) pictures
   are listed, not said to have been looked at. Follow-up R4 closes (a) to (c) in one four-minute job.
6. **Result:** buck_mount is one 11.8 g printed frame; the board comes out by four M3 screws from above with the
   mount left on the rail; 63 % of the underside open; 9 N gives about 2.5 MPa at the arm roots (factor 18 as
   reported; about 8 by hand at the M5 holes). The Y envelope of ±25 cannot be met by any mount: the board is 60 mm
   wide, so it and the pads under its holes reach Y ±30. That was said and assumed, not used as a reason to stop.
   Study numbers are the executor's and unaudited; check that parts under the board stay 8.5 mm in from its ends.

### D2. Two halves round a bearing

1. **Done (d2_job2.log, 14:27:42 to 14:36:23).** housing_fea: 11 bodies (two PETG halves, steel ring, four steel
   screw stand-ins, four soft pads), materials logged right. Mount face Y −32 and pad inner faces fixed (fixture box
   Y −32 to 22: both are in it); 300 N rigid remote load on the ring's two sides; no-penetration ring to each seat
   and split face to split face; direct sparse. Mesh el 3.0, seats and ring 1.2, screw faces 0.8: **160,773 nodes**
   (predicted 55,000).

   | Study | Reaction | Ring u (X, Y) | Max disp | Screw tensions | Sum | Upper vm / layer Z / shear Z | Lower vm / layer Z / shear Z |
   | --- | --- | --- | --- | --- | --- | --- | --- |
   | D2_Y_30 | Fy −300.0 | 0.000, 0.0917 | 0.094 | 75.2, 75.1, 76.7, 75.8 | 302.7 | 4.57 / 0.87 / 1.18 | 2.62 / 0.66 / 0.61 |
   | D2_YBOND_30 | Fy −300.0 | 0.000, 0.0018 | 0.0018 | 1.9, 2.0, 1.8, 1.9 | 7.6 | 0.09 / 0.02 / 0.02 | 0.84 / 0.74 / 0.28 |
   | D2_X_30 | Fx −299.999 | 0.136, 0.068 | **0.555** | 41.3, 40.8, 49.5, 48.6 | 180.2 | 6.13 / 0.76 / 1.41 | 5.13 / 1.07 / 2.23 |
   | D2_Y_22 | refused before the solve: 224,652 nodes over 200,000 | | | | | | |

   No log of the build job or the fit check is in the folder: the part volumes (17981.68, 18601.82, 2199.11) and the
   fit-check counts are the report's word. I opened `d2_pair.png`: two halves with a visible gap, four counterbores
   on the upper face, two mount holes on the lower; the report says the executor had not looked at it.
2. **Valid: the model yes; converged no. The executor's `valid: false` mixes the two.**
   - Reaction 300.0 N in both cases (0.000 % and 0.0003 %).
   - Contact proof, case Y (a body seated on both sides, so the bonded twin): ring UY 0.0917 against 0.00182 bonded,
     **50 times**; screws 302.7 N against 7.6 N; the lower seat opens by 0.0918 mm; lower seat pressure 0.098 against
     4.52 MPa, 2.2 %; pads 0.23 N (0.08 %).
   - Screw load, case Y: mean 75.7 N against 300 / 4 = 75 (+0.9 %); the four within 2 %.
   - Plain section, mine: crown of the upper half, full wrap: 150 / 101.6 + 150 · 1 / 121 = 2.72 MPa; the study's
     σx on the outer face over the crown is 2.70 MPa at (0.03, 32.0, 3.6) (the X-layer entry of the table): −0.7 %.
     So the half does wrap the ring; the plan's "expected 5 to 15 MPa" assumed it would not.
   - Case X: the ring wedges under the lower seat at 56.1° and bears on the upper at 9.4°. Statics with those
     angles: N_upper = 300 / (sin 9.40° + cos 9.40° · tan 56.12°) = 300 / (0.1633 + 0.9866 · 1.4893) = 183.8 N;
     tension 183.8 · 0.9866 / 4 = 45.3 N per screw (study mean 45.05, −0.6 %); shear 183.8 · 0.1633 / 4 = 7.50
     (study mean 7.81, +4 %). This is a consistency check, not an independent prediction (the angles are the
     study's); the independent first value, 23.9 N, is 47 % low, and the wedge explains why. No separate proof run
     for X; the same sets on the same mesh were proved in Y and the lower seat is visibly carrying, so I accept it.
   - **Open:** case X's maximum displacement is 0.555 mm, 5.5 times the 0.1 predicted and four times the ring's own
     0.136 / 0.068. 07-done.md says stop above 3 times. Nobody stopped, because `compare()` returns at the node-count
     note and never reaches the displacement test (see the last section). A mean of 0.14 with a maximum of 0.55 on
     a ring that only pads hold against turning looks like the ring spinning about Z (about 1.2°), which is harmless,
     but the files cannot show it (follow-up R3a). Until then case X is valid on its forces, not on its
     displacements.
   - Plan weakness that happened to hold: the ring touches both seats line to line at the crowns (0.00 clearance),
     which 05-fea.md contact rule 3 says not to do. The proof shows the contact engaged here.
3. **Correct numbers, layers along Z, one mesh (el 3.0):**

   | Half, case | von Mises (factor) | Layer tension (factor) | Shear (factor) | Excluded maximum (factor) |
   | --- | --- | --- | --- | --- |
   | upper, Y | 4.57 (9.85) | 0.87 (25.7) | 1.18 (11.0) | 8.71 (5.2) |
   | lower, Y | 2.62 (17.2) | 0.66 (34.3) | 0.61 (21.4) | 6.11 (7.4) |
   | upper, X | 6.13 (**7.34**) | 0.76 (29.6) | 1.41 (9.25) | 12.40 (3.6) |
   | lower, X | 5.13 (8.77) | 1.07 (**20.9**) | 2.23 (**5.82**) | 6.69 (6.7) |

   Lowest over both cases and both halves: `sf_yield` **7.34**, `sf_layer` **20.94**, `sf_shear` **5.82**.
   **Lowest factor of all: 5.82**, shear between layers in the lower half, case X, at (21.71, −15.15, 6.93): on
   the seat under the wedged ring, at the seat-to-shoulder corner. The upper half's von Mises peak (−27.28, 27.48,
   6.79) is 0.02 mm outside the exclusion zone (which starts at Y 27.5) under the rim of a bonded screw head: it is
   the edge of a singular zone, not a field value. Steel: ring 24.6 MPa, screws 144 MPa, against 640.
   Convergence: one mesh, so **nothing is converged and no step size exists**. The "margin" test (two more steps of
   the measured size) cannot be applied. For scale only: the governing measure would have to rise 2.9 times to reach
   2.0, and the worst singular edge in this whole set (T4's sharp corner) rose 1.85 times over two halvings.
   **Verdict: not shown** (expected to become margin or pass after follow-up R3).
   Preload is not in any study. The plan's formula gives 75 · 9.85 / 2 = 369 N per screw and 0.2 · 369 · 3 =
   221 N·mm. By the same linear scaling an ordinary M3 torque of 0.5 N·m (833 N per screw) would put the upper half
   at 9.85 · 75 / 833 = 0.89: tightening, not the 300 N, is the case that could break this part, and it rests on an
   unconverged number and a hand formula. That belongs in the one-line result.
4. **Report or results.json against rows and log:**
   - `sf_yield` 9.85, `sf_layer` 25.73, `sf_shear` 9.25. Rows: **7.34, 20.94, 5.82.** The executor took case Y
     upper for two and case X upper for the third; the key asks for the lowest over both cases and halves.
     results.json contradicts itself: `governing` cites 6.13 MPa (factor 7.34) beside `sf_yield` 9.85.
   - `governing` and "Thinnest margin: case X upper, von Mises 7.3". Rows: the thinnest is **5.82**, shear, lower
     half, case X. The report's own measure list has "Case X lower ... shear 2.23 (5.8)" and then ignores it.
   - `minutes` **75**. Log: study job 14:27:42 to 14:36:23; report: D2 "14:25 to about 14:37". **About 12 minutes
     of the 90.**
   - REPORT "solves 104 s each; readback about 2.5 min each". Log: mesh-to-result 142 s, 81 s, 140 s, then 40 s to
     the row each time: about 3.0, 2.0 and 3.0 minutes per study in all. "Waiting was about 40 min in total": the
     whole of set D ran from 14:20:25 to about 14:40, 20 minutes.
   - `pads_share_n` 0.24 against the log's 0.232 (report text 0.23).
   - "D2_Y_22 solves to 224,652 nodes": it meshed to that and was refused; nothing solved.
   - `clearances_mm` are the plan's planned values; the plan asked for measured ones and no build log is here to
     check them.
5. **Stopped short.** At the first refused mesh, with 78 of 90 minutes left, the task was closed as "cannot be
   solved under the rule". The refusal's own text says what to do ("coarsen the global size and keep the local
   controls"), 05-fea.md "When the node cap and convergence meet" lists four ways, and 07-done.md says a helper's
   refusal is not a reason to stop. The executor named two of the ways in its report and tried none. Where the
   nodes are, estimated from the two counts in the log (160,773 at 3.0 / 1.2 / 0.8 and 224,652 at 2.2 / 0.9 / 0.8)
   and the logged 3,560 to 3,600 nodes in 18 mm of each screw shank: about 29,000 nodes are steel screws meshed at
   0.8 mm, which no measure needs. Next step (follow-up R3b): el 4.0, shank and head faces 1.5, the PETG holes and
   counterbores kept at 0.8, seats and ring 1.2 / 0.9 / 0.7; my estimate 130,000 / 165,000 / 200,000 nodes (low
   confidence, so the instruction has a fallback). Case X first: both low factors are there. A symmetry cut at
   Z 3.5 would halve everything but `static()` has no roller or symmetry fixture (see the last section), so it is
   not available to the executor.
6. **Result:** the pair goes together and the contact model is sound: 300 N along Y puts 75.7 N on each screw (hand
   75), proven against a bonded twin 50 times stiffer; along X the ring wedges under the lower half and the screws
   carry 41 to 50 N tension (statics with the study's contact angles: 45.3). On one mesh the lowest factor is 5.8
   (shear between layers in the lower half, load along X), 7.3 on von Mises, 20.9 on layer tension. Not shown:
   convergence (one mesh), where the 0.55 mm in case X is, and tightening, which by hand is the case that limits
   this part (stay under about 0.2 N·m until it is modelled). Six specification problems were found and built round.

### D3. Six plates from a table, then a change

1. **Done (d3_part1.log 14:38:12 to 14:38:41, d3_part2.log 14:39:05 to 14:39:16).** Before SolidWorks the script
   printed the table as given: P1 A hole to B counterbore −0.7; P2 −6.25; P4 B counterbore to outside −3.0 and floor
   0.4; nothing else under 0.6. One `build()` made six plates, each with every feature's volume change checked, box,
   outside and bore faces, every hole and counterbore centre and radius read from the solid (12 to 24 faces per
   plate), floors, STL watertight. Part two opened each saved part (volume equal to part one), `save_as`, DISC
   dimension T → T + 1.5, P3's ring A sketch redrawn on Ø70 at 22.5°, one TOP_CHAMFER, the same measurements again,
   floor Z equal to part one, tree before equal to the first part of the tree after.
2. **Valid: yes.** I recomputed all twelve volumes and every wall from the table, independently of the executor's
   `hand()` and `walls()`:

   | Plate | My hand mm³ | Row mm³ | Thinnest wall, mine | Row | Plate _b: my hand | Row | Thinnest, mine | Floor Z |
   | --- | --- | --- | --- | --- | --- | --- | --- | --- |
   | P1 | 17728.67 | 17728.67 | 1.0 counterbore to outside | 1.0 | 22040.22 | 22040.22 | 0.6 chamfer to counterbore | 3.0 |
   | P2 | 23947.18 | 23947.18 | 3.0 floor | 3.0 | 29648.45 | 29648.45 | 3.0 floor | 3.0 |
   | P3 | 38698.26 | 38698.26 | 1.0 | 1.0 | 45765.78 | 45765.78 | 0.6 | 4.0 |
   | P4 (OD 68, cb 3.0) | 13802.43 | 13802.43 | 1.0 | 1.0 | 17802.44 | 17802.44 | 0.6 | 2.0 |
   | P5 | 62864.78 | 62864.78 | 2.5 | 2.5 | 74259.20 | 74259.20 | 1.5 | 3.0 |
   | P6 | 20848.86 | 20848.86 | 2.0 | 2.0 | 25865.43 | 25865.43 | 1.0 | 3.0 |

   Bad rows, mine: P1 at 0°: 30 − 25 − 1.7 − 4.0 = −0.7; P2: the same six holes twice; P4: 29 + 4 = 33 against 30,
   3.0 mm outside the plate, and a floor of 5 − 4.6 = 0.4; part two P3: 42 − 35 − 1.7 − 5.0 = 0.3, turned 22.5°:
   √(35² + 42² − 2·35·42·cos 22.5°) − 6.7 = 9.82; part two chamfer on P1, P3, P4: counterbore edge 1.0 mm from the
   outside, so a 1 mm chamfer leaves 0.0. All six caught before a part was built. Care does not drift: P6 has the
   same 60 measured lines as P1, and P6_b the same again.
3. **Verdict: pass.**
4. **Report or results.json against rows and logs:** every volume, wall, floor and flag agrees. `minutes` 6 against
   the report's own "D3 14:37 to 14:40" (about 3). The log of the first, failed run (stopped at a hole-coordinate
   check, see the last section) was overwritten by the rerun, so the failure is on the executor's word.
5. **Judgment calls to put to the person, not errors:** P4 was built Ø68 so that the Ø58 bolt circle could stay
   (said in the report). P4's counterbore was cut back from 4.6 to 3.0; the nearest thing that works is 4.4 (floor
   0.6), and a 4 mm M4 head stands 1 mm proud of a 3.0 counterbore in part one (flush again after the 1.5 mm).
   Having chosen P4's outside diameter itself, the executor chose one (68) that then forced the chamfer down to
   0.4 mm in part two; Ø70 would have taken the 1 mm chamfer with a 1.0 mm wall. Walls are from the numbers after
   the holes were measured on the solid, not measured on the mesh (said).
6. **Result:** all twelve plates match hand values to 0.01 mm³; four bad table rows and two bad change-request
   consequences were caught before building; the change was made by editing (same feature IDs, one new feature,
   floors unmoved). Three choices need a yes: P4 Ø68, P4 counterbore 3.0 deep, 0.4 mm chamfer on P1, P3 and P4.

---

## All ten tasks

| Task | Executor's verdict | Review's verdict | Lowest factor (review) | Outcome changed |
| --- | --- | --- | --- | --- |
| T1 | done | pass | n/a (model) | no |
| T2 | done | pass | n/a (model) | no |
| T3 | fail, 1.49 | fail | 1.49 layer tension (shear 1.79, converged) | no |
| T4 | fail, lowest quoted 1.12 | fail | **0.57** shear at the R0.4 corner; 1.12 von Mises; 1.57 layer | verdict no; governing number and hand value yes |
| T5 | fail ("not shown" in notes) | **margin, not converged** | 3.02 (von Mises 3.60 still moving; 2.81 after two more steps) | **yes** |
| T6 | valid false | **valid; margin, not converged** | 6.6 on bearing pressure 6.77 MPa (Hertz 6.76) | **yes** |
| T7 | done | pass | n/a | no (T7 missing from results.json) |
| D1 | done, sf_min 18.07 | pass on the 9 N case; envelope cannot be met | 18.07 as reported, about 8 by hand at the M5 holes; unaudited (no log) | no; sf_min qualified |
| D2 | partial, valid false, factors 9.85 / 25.73 / 9.25 | **not shown**; model valid | **5.82** shear, lower half, case X (7.34 / 20.94 / 5.82) | verdict no; numbers and validity yes |
| D3 | done | pass | n/a (models) | no |

## The three corrections that matter most

1. **T5 is not a fail.** results.json says `verdict: "fail"` for a part whose three factors are 3.60, 3.02 and 3.24,
   two of them converged, and whose only moving number would have to rise 80 % to matter (2.81 after two more steps
   at the measured rate). Anyone reading the key would throw away a design that works. Correct: margin, not
   converged; one rounded edge from pass.
2. **D2's summary numbers are wrong and its stop was early.** Lowest factors are 7.34 / 20.94 / 5.82, not 9.85 /
   25.73 / 9.25, and the governing measure is shear between layers in the lower half under the wedged ring, not von
   Mises in the upper. The task was closed after 12 of 90 minutes (results.json says 75) at the first refused mesh,
   with the helper's message naming the way on. The 0.555 mm in case X broke the stop rule unseen. And the limit on
   this part is tightening torque, which nothing here has shown.
3. **T6 is valid.** `valid: false` rests on a check that cannot work (a node mean times an area, rising with mesh
   density) while the exact form of the same check passed in the same row (499.8 of 500.0 N through the hole), the
   proof run is textbook, and all three meshes are within 12 % of the Hertz value. The answer, 6.4 to 6.8 MPa, was
   there at minute 7 of 40.

Also worth a line: T4's lowest factor is 0.57, not 1.12, and its "unexplained" 40 MPa is the curved-beam value (39.3).

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

- results.json T5: `verdict` cannot say "margin" (the sheet allows pass or fail), so leave the key until R1 is done
  and put "margin, not converged: lowest factor 3.02, von Mises 3.60 moving +13 % per step, 2.81 after two more"
  first in `notes`; `status` "partial".
- results.json T4 `notes`: lowest factor 0.57 (shear between Z layers at the R0.4 corner, 22.63 MPa, converged);
  layer factor at the motor holes 1.57 in T4's own rows; hand value 39.3 MPa by curved-beam theory (factor 3.57).
- results.json T6: `valid` true only after R2; until then add to `why`: "block reaction −499.80 N is the exact form
  of check 3 and passed; lig_force is a node mean and is not a force".
- results.json: add `T7` with `status` "done". REPORT (set A): 23 minutes, not 84; T3 Y-layer factor at the finest
  mesh 2.67, not 3.24. REPORT (set D): D2 took about 12 minutes; the whole set about 20.

## What in the plans, the playbook or the helpers caused an error

1. **`common.compare()` hides the displacement stop.** It returns False at the node-count note and never tests the
   displacement. Every D2 study was over 2 times on nodes, so D2_X_30's 5.5 times on displacement printed only the
   mild "NOTE", and the executor "checked the boxes and kept the stresses". Test both, log both.
2. **D2 plan, node estimate and dead branch.** 55,000 predicted, 160,773 meshed (2.9 times), so the planned three
   sizes never fitted. The branch for "mesh refused over 200,000" says use el 1.9, cs 0.8, which is finer than the
   refused 2.2 / 0.9 and can only be larger. No branch coarsens. The executor followed the table to its end and
   stopped. Controls at 0.8 on steel screws are where the budget went.
3. **T6 plan, three things.** (a) The `lig_force` check with a 400 to 650 N window: a node mean times an area on a
   mesh refined at the hole; it produced a "failed check" on a sound model. (b) The pin's face fixed at 1.0 while
   the hole goes to 0.5, and convergence judged on the maximum node: a recipe for ±7 % scatter. (c) The
   non-convergence branch (control 0.35, "about 220,000 ... if it fits under 200,000 after raising el to 4.0")
   was a dead end by its own number.
4. **`valid` defined to include convergence** (T6 plan section 4, D2 plan step 10). Two sound models were recorded as
   invalid. Valid and converged need separate keys or separate sentences.
5. **The verdict rule for an unconverged pass** (T3 plan step 7, T5 plan section 3: "verdict = 'fail' ... say 'not
   shown' in notes"), forced by TASKS.md's two-word `verdict` key. It turned T5's 3.0 to 3.6 into "fail". The
   playbook (07-done.md study item 6) has only pass and "not shown"; it has no state for "nothing near the limit, one
   singular edge still moving", and no arithmetic for it. The two-more-steps test used in this review would do.
6. **T5 plan.** The ribs end in sharp toes and the branch for "the peak moves to the rib tip" says only "report it
   with its factor"; 07-done.md says give the edge a radius and solve again. No hand value for the ribbed part was
   given ("at least halved"), so check 3 could not be made, and `checks()` went on reading plain-bracket sections.
7. **T4 plan.** Kt 2.2 from a shoulder-fillet chart for the inside of a knee; the curved-beam factor is 3.57. The
   executor could only report "67 % off, not explained". The verdict rule also names von Mises and layer tension
   at the corner and says nothing about shear, so the 0.57 in the row was never read.
8. **D2 plan, summary keys by hand.** `sf_yield`, `sf_layer`, `sf_shear` "lowest over both cases and halves" had no
   code; the executor picked them by eye and picked wrong. Anything that is a minimum over rows should be computed
   by the script (`min(rows[c][h]['Z'][k] ...)`).
9. **D2 plan, line-to-line seats.** The ring is drawn touching both seats (0.00 at the crowns), against 05-fea.md
   contact rule 3, and the fit check then probes 0.03 mm inside the ring, inside the STL's facet error (54 hits per
   half, rightly called inconclusive by the executor).
10. **D1 plan.** A 4 mm mask round fixed M5 hole walls hides the spine section that the plan's own hand table puts
    at 1.94 MPa nominal; no key or checklist line asks for the excluded maximum; no second support. The board
    stand-in keeps parts 8.5 to 9 mm from the edges while the written assumption says 3 mm.
11. **`swkit.expect()` and every plan that uses it for a position.** The tolerance is relative whenever it is
    between 0 and 1 and the wanted value is not zero. So the plans' "hole centre within 0.02 mm" was really 2 %
    (0.78 mm at X 39, 0.5 mm at X 25), "box within 0.01" was 1 %, and a wanted value of 6e-17 could never pass,
    which stopped D3's first run. No harm this time: the logs print both values and they agree to 0.0005 mm. The
    executor's absolute check in `plates.py` is the right repair; the helper needs an explicit absolute form.
12. **`static()` has only 'fixed' and 'hinge'.** 05-fea.md tells a session to "use symmetry" when the node cap and
    convergence meet; no helper can apply a symmetry or roller support. D2 (symmetric about Z 3.5) and T6
    (symmetric about X 0 and Y 0) would both have halved or quartered.
13. **`common.minutes()` counts from the import of `common`** (every "done at minute 0.2" in the logs), and nothing
    else records elapsed time per task. The executor's own figures were then 84 for 23 minutes, 75 for 12, and "40
    minutes of waiting" in a 20-minute set. `put()` could stamp the clock itself.
14. **Logs are not part of the hand-in.** The plans keep logs in `_wip` and never ask for a copy; set A's were
    copied, D1's were not, and D1's results script holds its numbers as typed constants. A results script should
    read the row file, and every task should leave one.
15. **Playbook 07-done.md "Do not stop early"** was read and not acted on in T5, T6 and D2 (7 of 40 minutes, 12 of
    90). The page states the rule; what was missing in each plan was the concrete next model with numbers, and in
    two cases the plan's own branch pointed at a wall.
