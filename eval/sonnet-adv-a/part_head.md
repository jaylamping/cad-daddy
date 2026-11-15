# REPORT: benchmark run `sonnet-adv-a`

**Model and effort.** Model `claude-sonnet-5-5` (configured, with `claude-opus-5-5` and `claude-opus-5` as fallbacks; I saw no fallback happen). **Reasoning effort: 5**, as the `reasoning_effort` tag in my session context read (the scale is not given to me). I had an `advisor` tool and used it twice: once at the start before any SolidWorks work (it caught the axial-load trap in T3, the `converge()` mask, and the pad and contact plan), and once near the end on this report; the second call found a wrong body mask in T6, a claim I had not tested, an unread region next to the holes, and a number I had checked in the wrong place. All three were changed (T6, T5/T3 bore wall, T3 check 3).

**Clock (local, CST; UTC is +6 h).** Brief received 17:28:48. Reading done and first stamp 17:33:23 (4.6 min; the label I wrote in that first `times.log` line says "~14 min", which is wrong). First SolidWorks launch 17:34:58. Last SolidWorks job closed 18:24:43 (T6 centred series), report finished 18:3x (the exact end is in my final message). The T6 limit of 40 minutes ran from its first stamp 17:46:25 to 18:24:43 = 38.3 min.

**Which `times.log` lines mark each task** (the file is one clock for several jobs, so jobs that overlapped interleave; T3, T4 and T7 have no end stamp of their own):

| Task | Start line | End line |
| --- | --- | --- |
| T1 | `T1 start` 17:35:03 | `T1 end` 17:35:14 |
| T2 | `T2 start` 17:35:14 | `T2 end` 17:35:20 |
| T3 | `T3a job start` 17:37:59 (the 17:37:23 line is the failed first run) | `T3b studies done` 17:41:34 |
| T4 | `T4 start (build bracket_sharp)` 17:41:34 | `T4b job end` 17:46:11 |
| T5 | `T5 start` 17:44:33 (first build) and 17:48:47 (final build) | `T5 job end` 17:46:33 and 17:51:06 |
| T6 | `T6 start` 17:46:25 (run 1), 17:51:44 (run 2), 18:11:07 and 18:12:31 (centred) | `T6 job end` 17:51:27, 18:02:27, `centred-pin series end` 18:24:43 |
| T7 | none: written while the T4 to T6 solves ran, about 17:42 to 17:47 (file time of `t7.md`) | |
| final checks | `final checks start` 18:02:57 | `final checks end` 18:03:01 |

**Times per task, from those lines and the job logs** (SolidWorks job time includes the launch, about 4 to 5 s a job, and is the whole job; "studies" is the sum of `static()` times: mesh, solve, read-back):

| Task | Status | SolidWorks job time | Studies in it | Launch waits | Waits behind another session's instance |
| --- | --- | --- | --- | --- | --- |
| T1 | done | 11 s (same 22 s job as T2) | none | 5 s | 0 |
| T2 | done | 6 s | none | in the T1 job | 0 |
| T3 | done: **fail** | 138 s over three jobs, one of them the failed first run (15 s) | 117 s (7 studies) | 15 s | 0 |
| T4 | done: **fail** | 265 s over two jobs | 228 s (6) | 10 s | 0 |
| T5 | done: **pass** | 273 s over two jobs (first build, then the mouth-rounded final build) | 212 s (8) | 10 s | 0 |
| T6 | done, valid | 29 min over five jobs (307 s run 1 invalid, 649 s run 2 seated, 51 s and 732 s centred) | 1,600 s = 26.7 min (12) | 25 s | 0 |
| T7 | done | none | none | none | none |
| Final checks | | 4 s | none | 4 s | 0 |

**Waiting against working.** (Measured: the SolidWorks and study times above, from the logs. Estimated: the split of my own time, which has no stamps.) Launch waits: twelve launches of 3 to 5 s, about a minute in all; the keeper (PID 10172) was the oldest instance, no launch ever waited behind another session's solve or rebuild, and no other session had an instance in my window: 0 s waiting for another session. Study time, 33 studies: about 2,150 s = 36 min, most of it the contact studies (453 s for the finest T6, 309 s for the finest seated, 165 s and 147 s for two more). My own time, estimated: reading and planning 4.6 min (measured), writing scripts about 14 min, idle waiting for a solve with nothing else to do about 15 min (mostly the T6 centred series, 12 minutes of it while I wrote this report), reading and analysing results about 12 min, writing this report and the post-processing the advisor asked for about 25 min. These add to the 67 minutes of the clock only roughly because SolidWorks jobs ran while I did other work.

**What was run.** 33 studies, every one under 200,000 nodes (largest 195,072); no heavy-solve lock; no instance half-closed; no hidden dialog stopped anything; my instances (PIDs 124676, 121372 for the failed T3 run, 126596, 119988, 127232, 124912, 132624, 131160, 133004, 131240, 141828, 143020) were closed by their jobs; `sw_instance.py --status` at the end shows the keeper 10172 only. I touched no other process. **Claim:** I claimed `sw-eval-sonnet-adv-a` and did not beat it during the run, so `claims.py list` showed it STALE at the end (57 minutes); the playbook says to beat on a long job and I forgot. The claim records no PID (the brief's `job()` launches per script), and `--status` printed "no claim" beside my instances because the claim's path (`j:\code\...`) and the instance's path (`c:\joe\code\...`) differ in spelling: that is a helper gap, noted below.

## Summary

| Task | Result |
| --- | --- |
| T1 | `bracket.SLDPRT/.step/.stl`: 32,974.02 mm³ (hand 32,974.02), 39.24 g, box 80 × 50 × 46, one body, STL watertight |
| T2 | `bracket_b.SLDPRT`: 31,643.0 mm³ (hand 31,643.0), counterbore floors at Z 3.0, original file unchanged |
| T3 | **Fail.** Tension across the layers (layers along Z) at the lower Ø3.4 hole rims 14.5 MPa (hole-wall support) and 15.3 (bottom-face support) against 22.5: factor 1.56 and 1.47. Von Mises 18.8 (factor 2.39). Hand root stress 11.0 MPa |
| T4 | **Fail.** Sharp corner is a singularity (22.8, 26.0, 30.0 MPa); with the printed 0.4 mm radius 38.3, 38.4, 40.4 MPa (a lower bound): factor 1.11; the hole-rim failure of T3 is the same |
| T5 | **Pass.** `bracket_c.SLDPRT`: upright 6 → 7.5 mm on the inner face, R0.4 on the four hole mouths, printed on its side (layers along Y); mass +7.15 % (42.05 g); `judge()` pass, lowest factor 2.60 |
| T6 | Valid. Peak bearing 5.8 MPa smoothed (6.3 raw node; hand Hertz 6.76, mean 1.67); block von Mises 5.2; pin rise 0.129 mm; reaction 500.00 N; pad share 0.028 % |
| T7 | all five answered below |

Files for the first four tasks (`.SLDPRT`, `.step`, `.stl`, sim `.npz`) are in `_wip/sw-eval/sonnet-adv-a/` (gitignored, so not in any commit; nothing was committed or pushed). Scripts, logs, rows, pictures, `results.json` and this report are in `eval/sonnet-adv-a/`.

