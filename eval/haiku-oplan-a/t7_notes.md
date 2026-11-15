## T7. Diagnose (no SolidWorks)

Written from the playbook (01-session.md, RULES.md "Hung, half-closed and orphaned instances", 05-fea.md, 06-judgment.md) and the plan A_T7.md.

**a. One `busy` instance (PID 20948) and one `HALF-CLOSED` instance (PID 2536).**
- What is happening: 20948 is another session's instance, not answering because it is meshing, solving or reading a result back. Its client is alive, so it is `busy`, not hung. 2536 has no windows and does not answer: it is half-closed, and it stalls every launch on the machine, so `launch()` refuses at once.
- What I do next: do not launch. Check `python pc/claims.py list` and `--status` for ownership of 2536. Run `python solidworks/sw_kill.py --list`, then `--dead`, which may end only a half-closed or abandoned instance after watching it. If it does not go, stop and give Joey the line `taskkill /PID 2536 /T /F`. Then launch with `job(wait_s=1800)` and do the hand calculations meanwhile.
- What I must not do: touch 20948 (busy is not hung; no `--force`, no kill); run `taskkill` on 2536 myself; launch anyway; use `GetActiveObject` to reach the running SolidWorks.
- Rests on: playbook/01-session.md (status table), RULES.md (Hung instances, Ending instances).

**b. Contact study, 796,000 nodes, direct sparse, error 24 after 143 s, log stops at GLOBAL-STIFFNESS-MATRIX-DECOMPOSITION-Start, free memory 26 GB to 12 GB in 11 s.**
- What is happening: out of memory in the factorisation, not a singular model. Error 24 is ambiguous; the memory fall and the log stage say OOM. 796k nodes with contact and direct sparse is the case 05-fea.md records as running out of memory on the 32 GB machine.
- What I do next: coarsen the global size and keep the local controls on the contact and governing faces. Mesh once and read the node count before solving. Target well under 450,000 nodes, and under 200,000 if the heavy-solve rule applies. Take the heavy-solve lock above 200,000 (static() does this). If the question needs more, use symmetry or cut the governing body out and load it with the forces read from the full model.
- What I must not do: treat it as a loose body and add restraints or pads; rerun it unchanged; run it beside another heavy solve; raise `max_nodes` above 450,000.
- Rests on: 05-fea.md "Sizing the job" and "When the node cap and convergence meet"; 06-judgment.md mistakes table.

**c. Exported STL offset by (41.5, 0, 12.0) mm; native part correct; export machine set up last week.**
- What is happening: the STL was shifted to positive space. The "do not translate to positive" export option (toggle 71) was off in this machine's user settings, so SolidWorks moved the mesh so its minimum corner sat at zero. The part's negative extents (X -41.5, Z -12.0) are exactly the offset. Earlier exports from that machine are suspect.
- What I do next: re-export with `swkit.export()`, which pins binary STL, mm, Fine and model frame (toggle 71 on) and restores the user's settings afterwards. Check `mesh.bounds` against `bbox(d)` within 0.1 mm and the volume within 0.5 %. Re-run the fit check. Record the export with `record_export.py`.
- What I must not do: move the STL back by hand by the offset; change the machine's SolidWorks settings permanently; trust any earlier exports from that machine without checking their bounds.
- Rests on: playbook/04-export.md (the export checks table), 06-judgment.md mistakes table ("STL shifted to positive space").

**d. Peak of 61 MPa on the edge of a fixed face; 38, 47, 61 at element sizes 2.0, 1.5, 1.0 mm. Requirement SF 2 against 45 MPa.**
- What is happening: a singularity at the fixture edge. The peak grows about 25 to 30 % per refinement and will keep growing with the mesh. It is not a stress the part carries (05-fea.md singularity rule; "a screwed-down part").
- What I do next: judge the part outside a fixed distance from the fixture. Read the peak outside 1, 2, 3 and 5 mm and take the plateau, with the same distance at each mesh, and report the value excluded. Try the support a second way (ring under the screw head, bonded washer, or a longer fixed face) and report both (07-done item 2). If the real part has a radius there, model it and solve again. Judge the plateau value against 22.5 MPa for layers and 45/2 = 22.5 MPa factor-2 limit, and report the layer measures too.
- What I must not do: report 61 (or 38) as the stress; pass or fail on it; quote a finer mesh until the number "settles"; pass the part on the coarsest value.
- Rests on: 05-fea.md "A screwed-down part" and "How far to stand back from a fixed hole wall"; 07-done.md items 2 and 6.

**e. Script silent for 25 minutes, own instance `busy`, another thread suggests restarting SolidWorks.**
- What is happening: the instance is working. `busy` means not answering but driven by a live client, typically meshing, solving or reading a large result back over COM. Large contact solves take 7 to 11 minutes, and reading back millions of nodes has taken over an hour.
- What I do next: run `--status` again. Look for `star.exe` or `cwanalysisproc.exe` under the instance. Read `%TEMP%\sw_hidden_<pid>.log` for a hidden dialog (a last line `#32770 | Simulation` during a solve is the solver asking a question). Watch whether the solver files beside the model still change and whether memory moves. Tell the other thread that it is busy, not hung, and leave it alone. If it truly must end, end it through its own handle (`j.inst.close()` or `end_session(state_file)`).
- What I must not do: restart or kill it (an instance 28 minutes into a solve was once killed as "hung" and left orphaned solvers); kill the Python client (that leaves it half-closed and stalls every launch); start a second instance meanwhile; wrap the job in `timeout`.
- Rests on: playbook/01-session.md "When a script hangs or dies"; RULES.md "An instance does not answer while it solves".
