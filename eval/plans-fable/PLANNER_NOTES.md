# Planner notes

- Model: `claude-fable-5-2`
- Start: 2026-11-14 08:03:20 UTC. End: 2026-11-14 08:46:07 UTC. Total: 43 minutes.
- Nothing was run in SolidWorks. Hand numbers were computed with Python. The pure-numpy parts of `common.py` and of
  `plates.py` (D3) were run on Linux against the hand values. Every line that touches SolidWorks is untested.

## Confidence per task

"Confidence" = an obedient executor that follows the plan reaches a correct result.

| Task | Confidence | The one place I expect it to go wrong |
| --- | --- | --- |
| T1 | high | Hole cuts and fillet picks: `edges_where` on the inside-corner edge, or a fillet that returns None; the volume checks after each step will catch it, the executor must then not "adjust" numbers |
| T2 | high | The slot built from two circles plus a rectangle: one of the three profiles cutting nothing (`min_dv`), or the before/after feature tree compare (`tree()` uses `GetID`, untested) |
| T3 | medium | The load model. `static()` has no directional face force, so the plan uses soft pads (bonded bodies) plus a remote-load study. If the pads do not bond or the two load models disagree by more than the tolerance, the executor has to pick the branch correctly. Verdict margin is thin near the lower motor hole (hand 16.4 MPa vs 13 MPa layer limit) |
| T4 | medium | Series A (sharp corner) is expected NOT to converge; the executor may read the non-converged number as a result, or run past the four-studies-per-instance limit |
| T5 | medium-low | Depends on T3's rows. Path 2a (print on the side) may not pass all three measures; then the rib fallback (2b) must be built and re-studied, which is a second build plus two or three more studies |
| T6 | low | Contact study with six bodies: the pin may be unconstrained until contact closes (error or excessive displacement), and contact pressure may not converge within the time. Fallbacks A and B are given but each costs a solve |
| T7 | high | None of substance; risk is only paraphrasing away a number |
| D1 | medium | The executor must accept the plan's reading of the contradiction (board 60 wide vs 50 mm envelope) and report `envelope_ok` false rather than quietly shrinking something. Build risk: the R2.5 step fillet and the insert holes |
| D2 | low | Eleven-body contact model written blind: body naming after `insert_body`, the `split`/`seat_angle` post-processing, and the X load case (screw loads 23.9 / 37.5 N are not trusted). Crown stress prediction is a wide range (3 to 37 MPa, expected 5 to 15) |
| D3 | medium-high | Six plates and six changed plates is a lot of repetition: one wrong ring angle or the counterbore cut direction (sketched on the floor plane, cut THRU_ALL upward) will show as a volume miss; the hand volumes are solid, so a miss means the build, not the number |

Least confident, in order: D2, T6, T5 (with T3 feeding it).

## Task-sheet errors I believe are planted or accidental

- **D1**: board 60 mm wide against a 50 mm Y envelope. Cannot both hold. Plan keeps the board flat, 5 mm over each
  side, and says so.
- **D2**: (1) opening Ø43.5 smaller than the bearing inner ring Ø44: built Ø49. (2) screws at X ±28.2 cut into the
  seat: moved to ±30. (3) split planes Z 1 / 6 do not match the 7 mm ring: 0 / 7. These three are clear. Less
  clear, treated as fit and length slips: (4) seat Ø52 with no clearance: Ø52.2; (5) seat width equal to ring
  width: −0.15 to 7.15; (6) insert hole 6 deep for an 8 mm insert: 8 deep, M3×35 screw.
- **D3**: P1 ring B overlaps ring A (turned 45°, 0.7 mm overlap fixed); P2 two rings identical (turned 30°); P4
  bolt circle does not fit OD 60 (OD to 68, "bolt circle stays, OD moves") and counterbore 4.6 deep in a 5 mm
  plate (3.0); P3_b change to Ø70 leaves a 0.3 mm wall (ring A turned 22.5°); chamfer 0.4 collides with the
  counterbores on P1, P3, P4.
- **T4**: asks for "the peak stress at the corner" of a sharp inside corner: a singularity trap. Plan reports
  not-converged for the sharp model and judges the R0.4 model.
- **T3**: the natural reading (rigid remote load on the motor face) stiffens the face and hides the hole-rim
  stress: a load-model trap. Plan runs both.
- **T7 d**: 38 → 47 → 61 MPa is diverging; either end of it as "the answer" is the trap.
- `TASKS_D.md` says "Rules as in set B". No set B is in the folder. Plans use the set A rules and the playbook.

## Playbook and helpers: wrong, missing, contradictory

Missing
- `static()` loads are only `'normal'` and `'remote'`. No force along an axis on a face. This is the largest gap:
  T3, T5, D1, D2 all work round it (soft pads or remote loads). No raw COM for a directional force is documented,
  so none is given.
- `fillet()` and `chamfer()` do not check volume change; `extrude`/`revolve` do. Plans add `expect()` after them.
- No helper for the feature tree; `common.tree()` walks `FirstFeature/GetNextFeature` with `GetID`, untested.
- Files the playbook refers to that are not in the folder: `EVAL.md`, `pc/capped.py`, `pc/claims.py`,
  `solidworks/sw_kill.py`, `eval/fable-d/d2_post.py`, `eval/sonnet-b/b4_tongue.py`. Plans name them only where the
  playbook tells the executor to run them (T7).
- Material lookup: how `materials=` matches body names is not stated exactly; plans name bodies and pass the dict
  by those names, and give a branch for "material not applied".
- The HEAVY threshold (200,000 nodes) is stated for set D work but not for set A.
- `Result.disp` row order relative to `Result.pos` is not stated; plans assume the same order and check lengths.

Contradictory or risky
- `converge()` masks everything within 2 × the coarsest element size of a load face. On small parts this hides
  the feature next to the load (T3's motor holes, D2's seat). Plans pass their own `mask`.
- `edges_where` on closed circular edges: one page says test the midpoint, another that a full circle has no
  usable midpoint. Plans pick circular edges by centre and radius of the adjoining face instead.
- 05-fea.md sizing table: the "over 200,000" row and the "300,000 to 450,000" row overlap and are out of order.
- README "seven lines" lists stop conditions, while the design pages say not to stop for a decision the plan can
  make. Plans read it as: stop for safety and machine state, decide and record for design.
- "Twin within 0.1 %" volume rule cannot hold for a twin that adds pads or washers; plans check the twin's base
  body against the original and the added bodies separately.
- `new_part()` closes all open documents first: a trap when a second part is made inside one job. Plans save
  before every `new_part`.

## Things in the plans the grader should know

- `plans/common.py` is an extra file (shared helpers for results.json, REPORT.md, export checks, the three
  measures). It calls only real `swkit`/`swfea` names.
- Node counts in the plans are estimates (±50 %). Each plan gives a branch for "far more nodes than expected".
- Where a verdict is expected to be "fail" or "not shown" (T3, T4 series A), the plan says so in advance so the
  executor does not tune until it passes.
