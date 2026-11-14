# Benchmark run haiku-plan-a: report

Run start 13:57:34 local (2026-11-14, clock from the machine). Model claude-haiku-5-5. Reasoning effort: not set by this session (default). Worktree J:/code/cad-daddy-wt/sw-eval-haiku-plan-a. Claim `sw-eval-haiku-plan-a`.

Brief rule followed: nothing committed or pushed. Plans/README.md says "commit eval/<run>/ at the end"; the brief overrides it, so nothing is committed.

## Timing and waiting

Run ended 14:21 local (about 1 h 24 min). Working = my reading, writing and checking. Waiting = SolidWorks solves, mesh and launch.

| Step | Clock | Notes |
| --- | --- | --- |
| Reading (playbook, helpers, plans) | 13:57 to 13:59 | about 2 min of reads, then plans |
| Gate selftest model + beam | 13:58:40 to 13:59:05 | PASS. One instance |
| T1 | 13:59:22 to 13:59:28 | one job, 6 s of SolidWorks |
| T2 | 14:00:18 to 14:00:25 | one job |
| T3 part one (4 studies) | 14:00:44 to 14:03:20 | solves 6 to 35 s each; instance launch 4 s |
| T3 part two (washers) | 14:04:03 | one job |
| T4 job 1 (builds, series A) | 14:04 to 14:05:33 | |
| T4 job 2 (series B) | 14:06 to 14:08:00 | |
| T5 (ribs, 3 studies) | 14:08:36 to 14:10:46 | |
| T6 (4 studies incl. proof) | 14:11:17 to 14:18:20 | 40-minute cap not reached |

Waiting for SolidWorks: launches took 3 to 4 s each (no splash waits). Solves took 6 to 110 s. Total SolidWorks wall time across all jobs was about 16 min out of 84; the rest was working (reading, writing, checking, and waiting on my own reasoning between steps). No time was spent waiting on another session's instance.

## T7. Diagnose (no SolidWorks)

**a. `--status` shows pid 20948 busy and pid 2536 HALF-CLOSED.**
- Pid 20948 (busy, 7890 s old, 9.1 GB committed): another session is meshing, solving or reading back. It is working, not hung. Do not treat it as hung, do not kill it. A launch goes ahead beside it, and only waits if it is the oldest instance; wait it out or use `job(wait_s=1800)`.
- Pid 2536 (HALF-CLOSED, 2710 s old, not answering, no windows): a dead instance that stalls every launch on the machine. It is not mine. Do not launch. Stop, report the PID to Joey and give him `taskkill /PID 2536 /T /F` for him to run. Running `sw_kill.py --dead` is an option the rules allow any session, but the playbook step for a HALF-CLOSED instance that is not mine is to hand it to Joey, so I would not do it on my own.

**b. Contact study, 796,000 nodes, direct sparse, error 24 after 143 s; log stops at GLOBAL-STIFFNESS-MATRIX-DECOMPOSITION-Start; free memory 26 GB to 12 GB in 11 s.**
- Cause: out of memory in the factorisation. Error 24 here is not a singular model, which is the other cause of error 24 (05-fea.md "When the solve fails"). The memory fall points to out of memory.
- Next: do not retry at 796k. Stop the attempt (never stop a solve that is running, but this one has already failed). Coarsen the global element size and keep the local controls on the contact and loaded faces, so the count drops under 450,000 nodes (the `static()` limit). Check the node count before solving. Check free memory with `job(wait_s=1800)`, and take the heavy-solve lock for anything over 200,000 nodes.
- Must not: change the solver to another one and rerun the same mesh, or push the node count up. Must not report a number from the failed run.

**c. STL fit check: whole part offset by (41.5, 0, 12.0) mm; native part in the right place; export made on a machine set up last week.**
- Cause: the export settings of that machine, most likely the STL "keep the model frame" toggle (71) or the units, so SolidWorks shifted the STL into positive space. The offset is a translation, not a scale, so the export is wrong and the native part is right.
- Next: do not touch the native part. Re-export with `export()` from the helper, which pins toggles 69 and 71 and the mm units, then compare `mesh.bounds` with `bbox(d)` within 0.1 mm (04-export.md). Record the export with `record_export.py`.
- Must not: move the native part to match the STL, or edit the STL by hand to fit.

**d. Peak 61 MPa on the edge of a fixed face; 38, 47, 61 at 2.0, 1.5, 1.0 mm; requirement SF 2 against 45 MPa.**
- Cause: a climbing peak with mesh size at a fixed edge is a singularity, not a stress (05-fea.md, 07-done.md study item 6). It does not mean the part fails at 61 MPa.
- Next: do not report 61 as the stress, and do not report it as a pass. Find the corner or fixture edge that causes it. Judge the spot by the plateau of the average outside 1 to 2 mm, or move the fixture away from the edge, or add the real radius the printed part will have (0.4 mm if nothing says otherwise) and solve again. Report the verdict as "not shown" until the governing measure converges.
- Must not: take the last value on the finest mesh, or raise the allowable.

**e. Script silent 25 min; `--status` shows my instance busy; another thread says SolidWorks is hung and suggests a restart.**
- Cause: busy means a mesh, rebuild or readback is running. It does not answer while it works. A 400,000-node contact solve takes 7 to 11 minutes, and a big readback can take over an hour.
- Next: do not restart. Check `--status` and read `%TEMP%\sw_hidden_<pid>.log` for a hidden modal dialog (a hidden dialog holds the client and looks like a hang). Only if it is a hidden dialog in my own instance, read it and press its button. Otherwise wait, and tell the other thread it is busy, not hung.
- Must not: restart or kill another session's instance, or start a second instance for the same job.

## Runs that failed before they worked

- T1 first draft had `mass_g` with an extra 1e-3 factor; fixed before the SolidWorks run (not a SolidWorks failure).
- T5 read script first imported a helper module that does not exist (`common_lite`); changed to `common`.
- No SolidWorks job failed, hung, or needed a restart. Every instance closed on exit.

## Task results (short)

- **T1** done. Volume 32974.02 mm³ = hand 32974.02, box exact, nine holes measured on the solid, STL watertight, STL volume 32990.4 (+0.05%). Picture checked.
- **T2** done. Edited the saved bracket in place (`save_as` before the first edit). Four counterbores floor Z 3.000, slot X 35 to 55. Volume 31643.00 = hand. `bracket.SLDPRT` SHA-256 unchanged (910913e0...). Picture checked.
- **T3** done, verdict **fail**. Governing: tension across layers at the lower motor-hole rims on the back face. At el 1.6 (183,846 nodes): rim 15.12 MPa, factor 1.49; factors at all three sizes 1.61, 1.57, 1.49, so fail stands. Von Mises 19.12 MPa, factor 2.35. Shear across layers 7.25 MPa, factor 1.79. Load two ways: remote bore load 13.35 MPa at el 2.2 (lower) vs pads 14.33 (pads govern). Support two ways: washers 14.40 vs walls 14.33 at el 2.2 (agree). Convergence: layer 13.97 / 14.33 / 15.12 (last step +5.5%), von Mises 19.25 / 21.02 / 19.12 (last step -9%), so not converged; the fail does not depend on it. Hand root stress 11.0 MPa; hand rim 16.4 MPa; study 15.1 MPa at el 1.6. Checks: reaction -150.0 N, displacement 2.84 mm, sz at Z 12 8.04 MPa (hand 8.0), sx at the base 12.04 MPa (hand 12.0). Node counts were 1.9x the prediction (42,611 vs 22,000): inside the 2x limit, recorded here. Print direction table in `t3_rows.json`: Y layers pass von Mises and layer (sf 3.24 at finest) but shear sf 1.79.
- **T4** done for the R0.4 variant, series A not converged (expected). Sharp corner: 20.45 / 28.51 / 37.75 MPa at controls 1.0 / 0.5 / 0.25 mm, compressive, climbing: no stress can be given. R0.4 corner: 38.11 / 39.66 / 40.05 MPa, converged (last step 1.0%). Reported 40.05 MPa. Verdict **fail** (motor-hole layer factor 1.49 and corner von Mises sf 1.12 on yield). **Discrepancy:** hand estimate was about 24 MPa (11 nominal x Kt 2.2); study 40 MPa, 67% above. Not explained; the study implies Kt about 3.2 on sigma_z. Not resolved here.
- **T5** done, verdict recorded as **fail** (status: not shown). Pads on the bracket fail shear on Y layers (1.79), so ribs were built (mass 42.48 g, +8.25%). Finest rib study (el 1.6, 190,958 nodes), layers along Y: von Mises factor 3.60 (12.51 MPa at a rib-leg end on the base top), layer 3.02, shear 3.24. Layer and shear converged (under 5%). Von Mises not converged: 10.68 / 11.06 / 12.51 MPa (+13% at the last step), so under the playbook rule a pass is not shown. A radius at the rib end would settle it. Step 2a (same geometry on its side) was not separately re-solved: the solve does not depend on print direction, so the T3 Y reading was used (see below).
- **T6** done, **valid = false**. Mid-length contact pressure 6.77 MPa at the finest hole control (0.5 mm, 122,007 nodes), vs the 6.8 MPa Hertz value. Series not converged: mid 6.52 / 5.96 / 6.77 MPa (last step +13.6%). Reaction -500.0 N, contact force from the block -499.8 N, pads 0.20 N (0.04%). Pin rise 0.130 mm. Proof at 0.25 N per end: rise 0.100 mm, 0.1% of the load gives 77% of the full rise, so the set is contact, not a bond. Check 3 failed: node-mean lig force 1053 to 1820 N against the plan's 400 to 650 N window; not investigated. Fallback A not run: the gap closed at the first load and checks 1 to 4 held.

## Where the plan was wrong or unclear

- **T5 step 2a** asks for a re-solve of bracket_c on its side. The solve does not depend on print direction (playbook 05-fea.md says so), so the re-solve would only duplicate T3_PADS_16. I used the T3 Y reading instead and recorded the decision here.
- **T5 expected** shear on Y layers to pass (guess 2.2 to 4). The study gave 1.79 for the plain bracket, so the rib path was needed.
- **T4 hand value** (about 24 MPa at R0.4) was 67% under the study (40 MPa). Plan's Kt of 2.2 was too low for this geometry.
- **T6 lig-force window** (400 to 650 N) was far below the node-mean reading (1050 to 1820 N). The plan's own note said it reads high near the hole; the window itself is wrong or the measure is useless. Should be redone as a face-force integral.
- **T6 convergence** was never reached at three hole controls; the plan's fallback (a fifth study, control 0.35) was not run because it needs a new job and the 40-minute cap was near.
- **Playbook 01-session** gives the worktree path as `J:/code/roark-wt/<session>`; this run used `J:/code/cad-daddy-wt/...`. Scripts use relative paths so nothing broke.
- **plans/README.md** says to commit `eval/<run>/` at the end; the brief said do not commit. Brief followed; nothing committed.
- **Pictures** were made for T1, T2, T4 (sharp variant) and T5 (ribs). No picture was made for T3 or T6 (the playbook asks for one per sheet run; the T4 picture was rendered but not opened).

## Not done or not verified

- T5 verdict is not a pass: von Mises convergence open. T6 is not valid: series not converged, lig-force check failed.
- Not verified: the T4 0.4 mm discrepancy; the T3 vm convergence; the rib-end radius for T5; the T6 mouth edge and friction (none modelled).
- Not checked by a reviewer: preload of the base screws, the mounting face, fatigue.

## Final state

- All SolidWorks instances closed by their jobs; `sw_instance.py --status` shows only the keeper (pid 10172, not mine).
- Claim released (`pc/claims.py release sw-eval-haiku-plan-a`).
- Nothing committed or pushed. `results.json` holds T1 to T6 (T7 is in REPORT only, as the task sheet asks).

- `plans/common.py` header says it was not run against SolidWorks. Its `must()` takes (what, got, want), the same signature used in plan T1.
- `playbook/01-session.md` names the worktree path `J:/code/roark-wt/<session>` and the claim line as `J:/code/roark-wt`; this run's worktree is `J:/code/cad-daddy-wt/sw-eval-haiku-plan-a`. Paths in the scripts use the worktree root, so no change was needed beyond that.
- `eval/TASKS.md` says the run's results go to `eval/<run>/`; `eval/` in this worktree contains only TASKS.md and this folder, which is consistent with the brief.
