# SolidWorks scripted benchmark: luna-a

Start: 2026-11-13 17:54:12 UTC (11:54:12 America/Chicago). Worktree: J:\code\roark-wt\sw-eval-luna-a. No commit or push.

Model id: GPT-6 (the runtime-visible family identifier); reasoning effort: not exposed by this runtime.

## Ask restated

1. Build a one-body PETG motor bracket in the stated X/Y/Z frame, with the R4 inside corner, all eight holes and specified R5 corners.
2. Modify the saved T1 part in place to add four counterbores and the rounded through-slot.
3. Check the T1 bracket under the 150 N +X bore load, including the required strength factors and convergence.
4. Compare the sharp-corner variant under the same load.
5. If T3 fails, change the design within the fixed interfaces and 10% mass cap, then verify it.
6. Model the block and free steel pin contact case; stop it at 40 minutes if still unresolved.
7. Diagnose the five supplied situations without launching SolidWorks.

## Stage budgets and decisions

Target total is about an hour; T6 has the task's separate 40 minute maximum. Initial stage budgets: T1 15 min; T2 8 min; T3 15 min; T4 8 min; T5 12 min; T6 40 min maximum; T7 5 min; report/review 10 min. If a stage exceeds twice its budget, record the reason and stop that stage.

- Older 01-session.md says busy launch refusals occur at 300 seconds. The current RULES.md, swkit.job() and the user's instruction specify job(wait_s=1800); use that.
- --status before work: PID 81988 was busy and PID 109340 solving; neither was HALF-CLOSED. Free memory was 10.64 GB, then 10.31 GB immediately before task preparation. Let the owned job wait; never touch those PIDs.
- claims.py list had one stale claim for upper-arm-r1 in another worktree. Left it untouched.
- git status --short showed pre-existing deletions in other evaluation folders and playbook/EVAL.md; do not restore or inspect them. Work only in this run folder and cad/_wip/sw-eval/luna-a/.
- SolidWorks stays hidden and each script uses one swkit.job(wait_s=1800) instance. All solves are capped at 200,000 nodes. No helper or shared settings are changed.

## T1 — specified bracket

Status: done.

Hand calculation, before modelling: base plus upright = 36,000 mm³; R4 concave fillet adds 50 * 4² * (1 - pi/4); each pair of two R5 outer rounds removes 2 * 6 * 5² * (1 - pi/4), and there are two such pairs; subtract four Ø5.5 base holes, one Ø22 bore, and four Ø3.4 upright holes through 6 mm. Correct result: 32,974.0242 mm³.

Checks: one body; bbox [0, 0, 0, 80, 50, 46] mm; volume 32,974.0242 mm³ vs hand 32,974.0242 mm³; no rebuild errors. All four base-hole centers (25,10), (25,40), (65,10), (65,40) and radius 2.75 mm measured; bore center (Y=25,Z=28), radius 11 mm; four bolt-hole centers measured at (14.0398,17.0398), (14.0398,38.9602), (35.9602,17.0398), (35.9602,38.9602) in Y/Z and radius 1.7 mm. STL is watertight, one shell, with volume 32,990.3773 mm³ (0.050% above native), and STEP declares millimetres.

The first hand expression omitted the upright R5 pair and was 64.3805 mm³ high. The feature logs show each pair removes 64.3805 mm³. I corrected the expression and cross-checked the corrected hand value against the native volume before T2; no geometry change or SolidWorks rerun was needed. No SolidWorks feature failed. The T1 sheet shows the complete bracket and all holes.

What could not be verified: printability and assembly fit to a real motor/screw model were not part of the supplied data.

Elapsed: 9m10s from benchmark start through T1 verification, including the required reading and setup; the SolidWorks build/export/readback itself finished in under one minute after the instance became ready.

## T2 — existing part edit

Status: done. Opened bracket.SLDPRT and checked its corrected hand volume, body count and feature tree before saving the edited document as bracket_b.SLDPRT. Script: t2.py.

Hand volume: T1 volume minus four counterbore annuli 4 * pi * (5² - 2.75²) * 3 and one slot ((20 - 6) * 6 + pi * 3²) * 6 = 31,642.9999 mm³.

Checks: native volume 31,642.9999 mm³ vs hand 31,642.9999 mm³; one body; no feature errors; all four annular counterbore floors measured at Z=3.0 mm; slot measured 20 mm long, 6 mm wide and through the 6 mm base; T1 bbox retained. The exported STL is watertight with volume 31,663.5454 mm³ (0.065% above native). The sheet shows one capsule slot centered in the base and four counterbore rings.

The first T2 run failed at the slot cut: its lower straight segment started at X=35 while the left arc tangent was X=38, so the profile was open. Correcting that endpoint made the exact slot cut and all following checks pass. This was a script sketch error; no helper or playbook defect.

What could not be verified: fit to actual mounting screws and motor hardware was not supplied.

Elapsed: 5m07s from T1 verification through the successful T2 checks, including the failed attempt and correction.

## T3 — T1 static study

Status: done. Every solve stayed below 200,000 nodes. Model: `bracket.SLDPRT`.

Hand estimate: root moment is 150 N * (28 - 6) mm = 3,300 Nmm. For the upright, section modulus is 50 * 6² / 6 = 300 mm³, so nominal root stress is 11 MPa. The initial 0.311 mm cantilever estimate covered only the upright; adding base-plate translation and rotation over the 19 mm span from X=6 to the first screw line at X=25 gives 0.348 + 0.807 mm, total predicted motion about 1.466 mm.

Failed attempts before the accepted study: (1) the first run printed a Unicode approximation glyph to this cp1252 console and exited before a study; replaced it with ASCII. (2) the first setup used the bore center as a point on the planar front face; that point is empty, so no face was picked; moved the pick to a solid patch. (3) the first 4 mm mesh had 18,675 nodes versus a 9,274 prediction (2.014x); its study was discarded. I calibrated the prediction from the measured controlled mesh. (4) that preliminary study reported 2.346 mm maximum displacement versus the upright-only prediction 0.311 mm; stresses were not used. The missing base-plate rotation is now included in the hand estimate. (5) the initial broad-face traction sensitivity had the wrong sign; its reaction check caught it and the load direction was corrected. The main bore-load study was run with the corrected setup.

Checks and verdict: three meshes at global sizes 4, 3 and 2.5 mm had 18,675, 27,174 and 37,705 nodes. Von Mises peaks were 15.16, 15.18 and 15.16 MPa; layer-Z tension was 9.75, 9.92 and 9.94 MPa; layer-Z shear was 7.26, 7.22 and 7.22 MPa. The finest peaks were 15.155 MPa at [8.72, 32.58, 6.21], 9.941 MPa tension at [0, 28.79, 8.72], and 7.216 MPa shear at [7.16, 26.48, 7.19]. Reactions were 150 N; maximum displacement was 2.351 mm. Yield factor is 2.969 and Z-layer tension factor is 2.263, so the requested checks pass. The broad-face traction sensitivity produced lower values (11.466 MPa VM, 0.321 MPa Z tension, 4.847 MPa Z shear); it is not a localized bore load and does not govern. Same isotropic solution, alternate print directions: Y gives tension factor 4.789 and shear factor 13.35; X gives 1.800 and 1.802. The requested base-down Z result passes. The rough 11 MPa beam estimate is below the local 15.16 MPa R4 transition peak; the geometry has no plain section one beam-depth clear of both load and root, so a 15% plain-section comparison is not applicable.

What could not be verified: no physical screw/motor assembly or slicer was supplied. The print-direction alternatives are stress transforms from the isotropic FEA result, not a print process simulation.

Elapsed: about 37m08s from T2 completion through the accepted T3 studies and checks. Most of the overrun was waiting behind another live SolidWorks client; no session was terminated.

## T4 — sharp-corner variant

Status: partial; no pass is claimed. Same bore load and supports as T3, but no inside R4. `bracket_sharp.SLDPRT` is one body with the same envelope and holes; native volume 32,802.3427 mm^3. The 4, 3, 2.5 and 1.5 mm global meshes had 20,715, 29,493, 39,274 and 63,463 nodes. In the tracked corner box, VM was 20.10, 19.79, 19.22 and 19.79 MPa; layer-Z tension was 4.121, 3.616, 3.256 and 3.355 MPa; Z shear was 9.790, 9.012, 9.306 and 8.851 MPa. Reactions were 150 N; maximum displacement at the finest mesh was 2.650 mm. These tracked values appear locally stable over the last interval.

However, the edge sizing control remained fixed at 1 mm for all four global meshes. Offline extraction of exact inside-edge nodes gave 17.284 MPa at global size 2.5 mm and 16.220 MPa at 1.5 mm (6.2% change), with only two data points. The exact sharp edge therefore was not demonstrated to converge, and this stage had already passed twice its 8 minute budget. I stopped without another solve. The reported 19.794 MPa is the finest tracked corner-box result, not a converged singular-edge stress. It is below the 45 MPa in-plane yield limit, but the local peak and factor of safety are not established; verdict is fail to demonstrate the requirement, not proof of material failure.

Failed attempts: two `sheet.py` invocations pointed to the wrong relative STL path and exited before producing a PNG; correcting the path produced the image. No FEA run failed. This was a path typo, not a helper issue. The sheet PNG was opened and checked.

Elapsed: about 18m from T3 completion through image review and postprocessing. The stage overran because I added a finer mesh while queued behind a live busy client; the exact-edge check then showed that another solve was necessary, but the twice-budget stop rule took precedence.

## T5 — improved bracket, if needed

Status: done; conditional redesign was not triggered because T3 passes both required factors. No `bracket_c.SLDPRT` was needed. The same T3 solution shows that rotating the print so layers run along Y improves the layer-tension factor from 2.263 (base-down Z) to 4.789 and shear factor from 1.801 to 13.35 without changing the CAD mass. This is an optional process improvement, not a new design or a separate study.

What could not be verified: no physical print-direction validation or anisotropic material study was available; T5's conditional geometry change and new solve were not required.

Elapsed: under 1 minute; result derived from T3 and no SolidWorks job was needed.

## T6 — block/pin contact

Status: partial at the 40 minute limit. Hard start 2026-11-13 19:16:41 UTC (13:16:41 CST); cutoff 19:56:41 UTC. Model: separate PETG block (40 x 30 x 20 mm, ?10.2 through bore along Y), centered ?10 x 50 mm steel pin, and two 1 mm long radius-1 mm soft pads at its ends to prevent free axial drift. The block bottom and pads? outer faces are fixed; the pin is pulled +Z by 250 N at each end. The only block/pin interface is a 0.1 mm radial-clearance no-penetration contact. Hand projected bearing stress is 500/(10 x 30) = 1.667 MPa. First 4 mm attempt stopped at the displacement gate and did not use stress. On retry, the same 24,034-node mesh passed the revised roof estimate: maximum movement 0.8244 mm at the pin cap [-5,25,10], and mean pin midspan rise 0.1241 mm. The block-hole contact-zone VM is 5.290 MPa at [-1.64,-15,16.073]. Total reaction is 500 N; bottom-block reaction is 499.866 N and pad reaction is 0.134 N, so pads carry 0.027% and the inferred contact share balances within 0.03%. The 3 mm mesh then showed `Fixture <Fixed-1> transfer failed` in a Simulation dialog on my owned PID 127048. `swfea.static()` logs and leaves unrecognized dialogs alone; that call did not return by the limit. After the cutoff, I confirmed PID 127048 had no solver child and that its own Simulation dialog contained only the failed-fixture message and an OK button. I acknowledged that failed setup dialog so the call could return; the helper then answered its known excessive-displacement prompt, `static()` raised `Failed`, no stress was read from that 3 mm run, and `job()` closed PID 127048 normally at 20:00:14 UTC. This was cleanup after the study limit, not a stopped solve.

The planned contact proof was a 0.5 N load in the working direction plus a bonded twin. The detailed 05-fea clearance-fit instruction says not to reverse a load when the body starts with clearance; it prescribes the working-direction proof. The generalized line in 07-done says reverse a tiny load for contact. I followed the clearance-specific instruction in the plan because reversing would pull the centered pin away from either wall and test its stabilizer instead of seating contact. Neither proof fit within the task limit.

What remains unverified: contact-stress convergence; the 0.5 N working-direction proof and bonded twin; a bearing-force integral directly over the contact patch; and a converged peak bearing stress. The 5.290 MPa value is one coarse-mesh result only. The 3 mm attempt had 26,611 nodes and was invalid after fixture-transfer and excessive-displacement errors.

Elapsed: 40m00s of task time, including about 11m20s waiting behind PID 135592; normal cleanup completed at 20:00:14 UTC, 3m33s after cutoff. First failed run: the 0.15 mm whole-model displacement estimate was 5.5x below the observed 0.825 mm, so its stresses were discarded. Second attempt: the 3 mm mesh had 26,611 nodes, then hit the fixture-transfer dialog. After the cutoff it raised `Failed` on excessive displacement; its stress result was not read.
## T7 — diagnosis

Status: done. No SolidWorks was needed. Elapsed 2m02s (started 19:56:43 UTC; diagnosis recorded by 19:58:45 UTC).

**a.** PID 20948 is a live busy client; `job(wait_s=1800)` should wait for it. PID 2536 is explicitly HALF-CLOSED and blocks launches. Stop before starting a job, record PID 2536, and follow the workstation owner?s recovery process. Do not kill or touch either other session?s process.

**b.** Error 24 after 143 seconds at `GLOBAL-STIFFNESS-MATRIX-DECOMPOSITION-Start`, with memory dropping from 26 to 12 GB, points to factorization running out of memory. 796,000 nodes also exceeds the 200,000-node cap. Coarsen or reduce scope, keep the contact and load path, recheck memory and node prediction, then rerun under the cap. Do not relaunch the same mesh or label this a loose body without evidence.

**c.** The constant (41.5, 0, 12) mm shift is an export-frame/translation preference problem, not native geometry. Re-export the native part through `swkit.export()`/`pin_export_prefs()` so STL translation is disabled and units are millimetres; compare STL bounds with native bounds and verify again in the mating frame. Do not move the native model to compensate or change shared settings.

**d.** The fixed-face edge peak climbs 38 ? 47 ? 61 MPa as the mesh shrinks, so it is a support-edge singularity and has not converged. At 61 MPa the raw yield factor is 45/61 = 0.74, below the required 2 (allowable 22.5 MPa), but that singular peak is not a physical stress. Model the real washer/screw support or move the fixture to the actual bearing region, then assess a fixed-distance-away peak and convergence. Do not call it a pass from a coarse mesh or report 61 MPa as a converged design stress.

**e.** `busy` on our own instance means the script may still be in a solve or waiting on a hidden dialog; 25 minutes alone does not prove a hang. Check `--status` and only our own `%TEMP%\sw_hidden_<pid>.log`, heartbeat the claim, and wait for `job()` to return. Do not restart or kill the process, launch another SolidWorks job behind it, or stop a script during mesh/solve.

## Playbook/helper findings

Findings so far: 07-done requires checking the expected node count before judging stresses, but swfea.static() only has a maximum-node guard and proceeds to solve/read results before the calling script can check its prediction. I set max_nodes to 2x the current predicted count to stop an oversized mesh before the solve; the helper still has no lower-bound pre-solve hook. The first mismatch exceeded the prediction by only 2.014x; the result was discarded. The 07-done maximum-displacement gate also comes after static() has already read arrays, so the helper does not expose a pre-stress result check. Do not treat either discarded run as a reported stress result. T4's local edge mesh control stayed at 1 mm across global refinements, so the exact sharp edge did not receive a genuine refinement series; that gap was exposed by offline node extraction and is why T4 remains partial. T6's contact-proof wording conflicts between 05-fea's specific clearance-fit case and 07-done's generalized reverse-load sentence; I record and follow the former for the centered clearance pin. In T6, `swfea._solver_dialogs` leaves unrecognized Simulation dialogs alone, so T6 waited in `RunAnalysis` past its limit. After confirming the own PID had no solver child and reaching the task cutoff, I acknowledged the explicit fixture-transfer failure to allow normal job cleanup; the helper then reported excessive displacement and `static()` raised without returning a result.

## Final review

End: 2026-11-13 20:03:58 UTC (14:03:58 CST). Final `--status` before release showed no instance from this run; the remaining listed processes belonged to other sessions and were left untouched. The claim was released after the artifact review.
