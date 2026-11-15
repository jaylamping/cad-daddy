# A_T7: diagnose (no SolidWorks)

## 1. Restatement

Five situations; for each write what is happening, what you do next, and what you must not do, in `REPORT.md` under
T7. Use the answers below; copy them in your own words but keep every fact and number. 15 minutes.

Checklist: [ ] a [ ] b [ ] c [ ] d [ ] e, each with happening / do next / must not, and the playbook page it rests on.

## 2–6. Answers

**a. One `busy` instance and one `HALF-CLOSED` instance.**
- Happening: PID 20948 (2 h 11 min old, 9.1 GB, 61 threads) is another session's instance meshing, solving or
  reading results; it is healthy and will answer when done. PID 2536 has no windows and does not answer: a dead,
  half-closed instance (3.6 GB committed, 1 thread). A half-closed instance stalls every launch on the machine, so
  `launch()` refuses at once (RULES.md, Hung, half-closed and orphaned instances).
- Next: do not launch. Check `python pc/claims.py list` and `--status` for who owns 2536. Run
  `python solidworks/sw_kill.py --list`, then `python solidworks/sw_kill.py --dead`, which may end only a half-closed or
  abandoned instance after watching it 20 s (RULES.md, Ending instances; any session may run it). If `--dead` does not
  end it, stop and report to Joey with the PID and the line `taskkill /PID 2536 /T /F` (01-session.md table). Then
  launch with `job(wait_s=1800)`. Do the hand calculations meanwhile.
- Must not: touch 20948 (busy is not hung; never `--force` or kill another session's instance); `taskkill` 2536
  yourself; launch anyway; reach for "the running SolidWorks" (`GetActiveObject`).

**b. 796 000 nodes, contact, direct sparse, error 24 after 143 s, log ends at matrix decomposition, free memory
26 → 12 GB in 11 s.**
- Happening: out of memory in the factorisation, reported as error 24 — not a singular model. About 800 000 nodes
  with contact and direct sparse is known to run out of memory on the 32 GB machine (05-fea.md sizing table; 06-judgment
  mistakes table). It is also over the 450 000-node cap `static()` enforces and over the 200 000-node heavy-solve line.
- Next: shrink the mesh to well under 450 000 (under 200 000 if the job's rule says so): coarsen the global size, keep
  the local controls on the contact and governing faces (05-fea "Sizing the job"; halving size gives ~6x nodes); mesh
  once and read the count before solving; take the heavy-solve lock above 200 000 (`static()` does). If the question
  needs more, use symmetry or cut the governing body out (05-fea "When the node cap and convergence meet").
- Must not: treat it as a loose body and add restraints/pads; run it again unchanged; run it beside another heavy
  solve; raise `max_nodes` past 450 000.

**c. Exported STL offset by (41.5, 0, 12.0) mm; native part right; export machine set up last week.**
- Happening: the STL was shifted to positive space: the "do not translate to positive" toggle (71) was off on the new
  machine's per-user settings, so SolidWorks moved the mesh so its minimum corner sits at 0 (the part's negative
  extents were X −41.5, Z −12.0). 06-judgment mistakes table; 04-export.md.
- Next: re-export with `swkit.export()`, which pins binary, mm, Fine, model frame (toggle 71 on) and puts the user's
  settings back; check `mesh.bounds` against `bbox(d)` within 0.1 mm and the volume within 0.5 %; re-run the fit check;
  record the export (`record_export.py`).
- Must not: move the STL back by hand by the offset; change the machine's SolidWorks settings permanently; trust any
  earlier exports from that machine without checking their bounds.

**d. Peak 61 MPa on the edge of a fixed face, 38 → 47 → 61 at 2.0 / 1.5 / 1.0 mm.**
- Happening: a singularity at the fixture edge: it grows ~25–30 % per refinement and will keep growing. It is not a
  stress (05-fea singularity rule; "a screwed-down part").
- Next: judge the part outside a fixed distance from the fixture: read the peak outside 1, 2, 3, 5 mm and take the
  plateau, same distance at each mesh, and report the value excluded. Try the support a second way (ring under the
  screw head, a bonded washer, a longer fixed face) and report both (07-done item 2). If the real part has a radius
  there, model it. Verdict on the plateau value against 22.5 MPa (factor 2 on 45) and on layer measures.
- Must not: report 61 (or 38) as the stress or fail/pass on it; quote a finer mesh until it "settles"; pass the part
  on the coarsest value.

**e. Silent 25 minutes, own instance `busy`, someone suggests a restart.**
- Happening: your instance is working (meshing, solving or reading a large result back over COM); `busy` means not
  answering but driven by a live client. Large contact solves take 7–11 min; reading back millions of nodes took over
  an hour (01-session.md "When a script hangs or dies").
- Next: run `--status` again; check for `star.exe`/`cwanalysisproc.exe` under it; read `%TEMP%\sw_hidden_<pid>.log`
  for a hidden dialog (`#32770 | Simulation` = a solver question; `static()` answers the excessive-displacement one);
  watch whether the solver files beside the model still change and whether memory moves. Answer the other thread:
  not hung, busy, leave it. If it truly must end, end it through its own handle (`j.inst.close()` /
  `end_session(state_file)`).
- Must not: restart or kill it (an instance 28 min into a solve was killed as "hung" and left orphaned solvers);
  kill the python client (leaves it half-closed and stalls every launch); start a second instance meanwhile; wrap the
  job in `timeout`.

## 7. Done and results

REPORT.md T7: the five answers. `results.json` T7: `status` "done", `notes` "written answers in REPORT.md".
If unsure of any line, write the doubt next to it rather than dropping the case.
