# Run plan and C1 checkpoint

Benchmark start (clock): 2026-11-13 22:06:38 UTC. 100-minute limit ends 23:46:38 UTC.
Stage budgets from start: C1 boxy reference 15 min; C2 restatement and crude checkpoint 20 min from C2 start; form alternatives and selection 20 min; final fixed-item/model work 20 min; three load studies 15 min; review and report 10 min. I will stop at the clock limit and list unfinished checks.

Machine check before any launch: 19.46 GB free of 31.14 GB; SolidWorks status showed PIDs 20496 and 123948 answering, PID 108796 busy with a live client. Claims list showed `left-arm-organic` owns 108796 and `shoulder-study-fea` has no PID. I did not touch those instances. Claimed `sw-eval-luna-c`; own SolidWorks PID to be added after launch.

C2 restatement is in `restate.md`, written before C2 modeling. Model id: GPT-6; reasoning effort: not exposed to this session.

## C1 status

Pending build, dimensions, export, and picture checks.

C1 failed run 1 (2026-11-13 22:14 UTC): the model features all built and saved, but result collection called `Face.GetBox` as a method. SolidWorks exposed it as a tuple property on this call, so the script stopped before export. This was my script error; I changed it to `swkit.call()` and will rebuild in a fresh owned instance.


C2 failed run 1 (2026-11-13 22:18 UTC): I tried to select the beam's four long edges for a softening fillet, but `edges_where()` found zero edges because those boundaries were not represented as the straight edges I expected after the union. The attempt did not change the file. Decision: checkpoint 01 will record the complete C1 interface layout as the crude baseline and explicitly call out the still-boxy shape; I will choose the organic spine after seeing this baseline.

C1 sheet: the eight views show a round elbow plate, long straight rectangular beam, and forked wrist; the side and three-quarter views make the slab-like arm and sharp transitions clear.

C2 checkpoint 01 — 2026-11-13 22:20 UTC (3 minutes after C2 start), `pictures/checkpoint_01.png`: complete interfaces and whole link are visible. Missing against the request: tapered flowing spine, smooth joint transitions, open cable channel, and swept-slot/print review. This is the crude interface baseline; I chose to keep it intact while evaluating two substantially different spine layouts.

C2 failed run 2 (2026-11-13 22:28 UTC): the Ø6 centerline cylinder cut built, but the follow-on rectangular opening cut reported no volume change. The channel therefore was not proven open. I stopped this version and will inspect the saved intermediate, then adjust the cut so it has a visible opening; I will not claim the cable requirement until the clear Ø6 path is checked.

C2 idea A intermediate sheet (2026-11-13 22:31 UTC): the front shows the round elbow and a smooth waisted spine with a flared wrist hub; the fork is not built in this intermediate. The loft bounds measured 55.25 mm across Y despite section inputs totaling 44 mm. Decision: rebuild the changing loft with four aligned open curves per section, as 03-modelling recommends; `swkit.loft`'s docstring only says “closed section sketches,” so its supported open-curve use is unclear. The first sheet invocation used the wrong WIP directory name and raised `FileNotFoundError`; the corrected invocation generated and I opened `pictures/idea_a_groove_partial.png`.
