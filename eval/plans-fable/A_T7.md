# A / T7. Diagnose

No SolidWorks. Playbook: 01-session.md ("Look before you launch", "When a script hangs or dies"), RULES.md "Hung,
half-closed and orphaned instances", 02-com.md "Numbers the scripts use", 04-export.md "Exporting", 05-fea.md
("Is the result right?", "Sizing the job", "When the solve fails"), 06-judgment.md "Mistakes already made here".

## 1. Restatement

Five cases, a to e. For each, REPORT.md (under a heading `T7`) says three things: **what is happening**, **what you
do next**, **what you must not do**. Nothing is run. Do this task first or while a job runs.

- [ ] five answers, each with the three parts, each quoting the numbers from the case
- [ ] each answer names the playbook page it rests on
- [ ] results.json `T7`: `status`, `notes` (the sheet names no other keys for T7)

## 2. Numbers worked out for you

| Case | Working | Result |
| --- | --- | --- |
| a | pid 2536: 1 thread, 0 windows, does not answer, 3610 MB, 2710 s old | the definition of HALF-CLOSED (RULES.md table). pid 20948: 61 threads, 3 windows, 9120 MB, 7890 s: a job at work |
| b | 796,000 nodes with contact, direct sparse | 05-fea.md "Sizing the job": "about 800,000 with contact, direct sparse: ran out of memory on the 32 GB machine, reported as error 24". Memory fell 14 GB in 11 s during the factorisation. Halving the node count needs the element size about 1.35 times larger (nodes go with 1 / size³; 1.26 gives half) |
| c | offset (41.5, 0, 12.0) | equals minus the part's lowest corner: the part's box starts at X −41.5, Y 0, Z −12.0, and the STL was shifted into positive space |
| d | 38 → 47 → 61 MPa at 2.0, 1.5, 1.0 mm | steps of +24 % and +30 %: growing, not shrinking. Allowable 45 / 2 = 22.5 MPa. 61 would be a factor of 0.74, 38 a factor of 1.18: neither is a result |
| e | 25 minutes silent, `busy` | 01-session.md: a 400,000-node contact solve takes 7 to 11 minutes, reading 2.4 M nodes back took over an hour. 06-judgment.md: an instance 28 minutes into a solve was once killed as "hung" |

## 3. The answers (write them in your own words, keep every fact)

**a.** *Happening:* pid 2536 is half-closed: a dead instance that stalls every launch on the machine. pid 20948 is
another session's job, working (busy is not hung). *Next:* do not launch. Report pid 2536 and the line
`taskkill /PID 2536 /T /F` for Joey (01-session.md table); note any claim that names it (`python pc/claims.py list`).
If the instance is your own from an earlier script, end it through `end_session(state_file)`;
`python solidworks/sw_kill.py --list` shows whether it counts as dead. Meanwhile do the work that needs no
SolidWorks (hand calculations, T7). After it is cleared, run `--status` again, then launch. *Must not:* launch
"to see"; kill or `--force` pid 20948 or any instance that is not yours; treat busy as hung; lower the memory floor.

**b.** *Happening:* out of memory in the factorisation, reported as error 24. Not a singular model: a free body fails
at once, this one ran 143 s, reached "GLOBAL-STIFFNESS-MATRIX-DECOMPOSITION-Start", and free memory fell from 26 to
12 GB in eleven seconds. *Next:* make the model smaller, one change only: coarsen the global element size and keep
the local controls on the contact faces (05-fea.md: 4 mm global with 0.8 mm controls gave 400,000 where 800,000 was
too many); aim under 450,000, better under 200,000; check free memory and that no other heavy solve is running;
`static()` takes the heavy-solve lock by itself; solve again and note memory at the end. Record the failed run as
INVALID with the reason. *Must not:* read error 24 as "a body is loose" and start adding fixtures or pads; run the
same mesh again; switch to the iterative solver (it stalls on contact); change two things at once; report any number
from the failed study; lower the 8 GB floor.

**c.** *Happening:* the STL was exported with "keep the model frame" off (toggle 71), so SolidWorks moved it into
positive space; the offset is the part's negative extent. A per-user setting, and this machine's defaults differ.
The part is fine. *Next:* export again with `swkit.export()`, which sets the options for the export and puts the
machine's own back; then check the file: `mesh.bounds` against `bbox(d)` within 0.1 mm, volume within 0.5 %; run the
fit check again; look for other exports made on that machine the same way. *Must not:* move the native part or the
mating part to suit; shift the STL by hand and carry on; change the SolidWorks setting on the machine for good;
trust any export from that machine that was not checked against the model's box.

**d.** *Happening:* a singularity at the edge of the fixture, not a stress: it grows faster with each refinement and
sits on a fixed face. It is neither a failure at 61 nor a pass at 38. *Next:* judge the part away from the fixed
face at one fixed distance for all three meshes (find the plateau: peak outside 1, 2, 3 and 5 mm), and say how large
the excluded value was; try the support a second way (the ring under the screw head, a bonded washer, a longer
fixed face) and keep the numbers the two agree on; if the edge is a real inside corner of the part, model its
radius and converge that; converge all three measures. Until one of these converges the verdict is "not shown".
*Must not:* report 61 MPa as the peak or fail the part on it; report 38 because it is the lowest; pass on the
finest value; keep refining and hope; quietly widen the mask until the number fits.

**e.** *Happening:* almost certainly it is working: busy means a live client is driving it through a mesh, a
rebuild, a solve or a result read-back, and it answers nobody meanwhile. *Next:* look, do not act: `--status`
again (is a solver process under it? has the state changed?), `%TEMP%\sw_hidden_<pid>.log` (a last line
`#32770 | Simulation` is a hidden solver question; `static()` answers the excessive-displacement one itself), whether
the solver's files beside the model are still changing, and free memory. Tell the other thread: busy, not hung, with
what you saw; its own launches go ahead beside a busy instance. Wait. Only if the log shows a dialog nobody answers,
or the files have stopped changing for many minutes with no solver running, and it is your own instance: end it
through its own handle (`j.inst.close()` or `end_session(state_file)`). *Must not:* restart it; kill the python
process; start a second instance to "check"; let another thread stop it; put the next run under `timeout`.

## 4 to 6. Studies, decisions, branches

No studies. Decision made for you: where the playbook gives a rule, the answer is the rule, not an opinion; quote
the page. Branches: none, nothing is run. If a case seems to you to mean something else than written here, write
both readings and which one the numbers support.

## 7. Done checklist

- [ ] five answers in REPORT.md under `T7`, each with "what is happening / next / must not"
- [ ] the numbers of section 2 appear in the answers
- [ ] `put('T7', status='done', notes='five cases answered in REPORT.md')`
- [ ] nothing was launched or killed for this task
