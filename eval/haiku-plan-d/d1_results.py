"""Writes D1 keys to results.json and the D1 section to REPORT.md (values taken from the run logs)."""
from common import *  # noqa: F401,F403

put('D1',
    status='done',
    mass_g=11.84,                       # 9949.07 mm3 measured (9949.07 hand) x 1.19 g/cm3
    parts=1,
    fasteners=['2 x M5 x 8 socket head cap screw into 2 x M5 T-nut (top slot, X +-50)',
               '4 x M3 x 6 socket head cap screw into 4 x M3 heat-set insert (hole D4.0 x 6, X +-39, Y +-26.5)'],
    board_removal_steps=['free the two wire pairs at the +X end',
                         'undo the four M3 x 6 screws at the board corners from above (2.5 mm hex key)',
                         'lift the board straight up (fit check: lifted board clear of the mount)',
                         'refit: lower onto the four pads, wires to +X, four M3 screws',
                         'mount stays on the rail: the two M5 screws are not touched'],
    open_area_share=0.63,               # hand 0.63; measured on the exported STL 0.6298
    envelope_ok=False,                  # board is 60 wide, envelope Y -25..25 (50): flat board 5 mm over each side
    sf_min=18.07,                       # Z print direction, von Mises at the arm root (yield 45 MPa / 2.49 MPa)
    governing='von Mises at the arm root beside the R3 corner, load along Z (2.49 MPa, converged)',
    print_orientation='spine face on the bed, layers stacked along Z, no supports',
    assumptions=['board flat, long side along X, centred on the rail',
                 'wires leave at +X, no strain relief',
                 '112 mm of rail along X free',
                 'M3 heat-set inserts',
                 'nothing under the board within 3 mm of its edges',
                 '2.0 factor on the 9 N case'],
    questions=['Y envelope 50 mm vs board width 60 mm: assumed envelope gives, board only 5 mm over each side',
               'wire exit end: assumed +X, none',
               'rail length free: assumed yes',
               'inserts or direct screws: assumed inserts',
               'parts under board edges: assumed none',
               'factor on 10 g: assumed 2.0 on 9 N'],
    ideas_tried=['A open frame, board screwed from above (chosen)',
                 'B slide-in cradle with C rails along the long edges (rejected: 25.6 g vs 11.8 g, rails reach Y +-32.5, rattle, needs 85 mm clear rail)'],
    minutes=5,
    notes='envelope_ok false: the board itself reaches Y +-30. open_area_share and envelope_ok are hand values checked '
          'against the exported STL (open area 0.6298). Study: 3 mesh sizes converged (vm 2.47, 2.49, 2.49 MPa); '
          'displacement 0.158 mm vs 0.09 hand (within 3x). Second load way and second support way not run.')

report("""## D1. A need, not a drawing

Times (local clock): restate written about 14:21; modelling job 14:21:44 to 14:22:08 (0.4 min of SolidWorks); pictures and fit
checks 14:22 to 14:23; study 14:22:50 to 14:24:06 (three solves, about 1.2 min total); open-area check 14:25.
Waiting: SolidWorks launch about 6 s per job (instance pid 118032 and 115568), no waits for another instance (keeper was
running). Working: nearly all of it.

**Restatement and conflict.** See eval/haiku-plan-d/restate.md. The board is 60 mm wide and the Y envelope is 50 mm.
Checked: no tilt angle meets both height and width (script run, 0.5 deg steps, 0 to 90 deg). Flat board: 5 mm over each side
(the board's own outline reaches Y +-30). Decision: flat board, printed parts inside the board's outline, envelope_ok false.

**Ideas.** A (chosen): open frame, spine on the rail, two arms with four pads, board screwed from above.
B: slide-in cradle with two C rails. Pictures: pictures/d1_idea_a.png, pictures/d1_idea_b.png. B: 21521 mm3, 25.6 g
(hand 21521 mm3), one body, but its rails reach Y +-32.5 and it needs 85 mm of rail clear to slide the board out.

**Chosen mount.** buck_mount.SLDPRT, STEP and STL in _wip/sw-eval/haiku-plan-d (gitignored, not committed).
- Volume 9949.07 mm3 measured (hand 9949.07), mass 11.84 g. Box -56..56, -30..30, 0..9: exact.
- One body; six holes measured: 2 M5 (-50,0) and (50,0), 4 inserts at (+-39, +-26.5) floor z 3 top z 9, 8 R3 and 4 R2.5 fillets.
- Rebuild errors 0. STL watertight, one shell, STL volume 9953.5 vs 9949.07 model (0.04 %), box exact; STEP in mm.
- Fit checks against the stand-ins (eval/haiku-plan-d/d1_fit.py): board points inside mount 0, lifted board 0,
  M5 driver column 0, rail 0, M3 driver columns 0.
- Open area under the board: 0.6298 measured on the STL, hand 0.63.
- Pictures: pictures/d1_buck_mount.png, pictures/d1_assembly.png (board and rail stand-ins), and idea pictures.

**Study (Z load, 9 N on the four pad tops, PETG, two M5 hole walls fixed).** Three meshes, convergence on vm and layer measures:

| el (mm) | nodes | peak vm (MPa) | layer tension Z | layer shear Z |
| --- | --- | --- | --- | --- |
| 2.0 | 30,598 | 2.47 | 0.17 | 0.70 |
| 1.5 | 58,907 | 2.49 | 0.13 | 0.70 |
| 1.1 | 125,748 | 2.49 | 0.13 | 0.71 |

Converged (last step 0.0 % on vm). Nodes vs predicted 22k/53k/135k: within 2x. Displacement 0.158 mm vs predicted 0.09 mm
(within 3x; the hand estimate was for the pad ends, so I accept the study). Reaction Fz +9.0 N, Fx and Fy 0.
Arm-top sigma-y at |y| 15: 1.22 MPa against hand 1.21 MPa (within 1 %).

Five checks: (1) reaction equals load: yes. (2) displacement same order: yes (1.8x hand). (3) plain section stress: yes.
(4) peak away from fixture and load faces: peak at (-43.07, -9.36, 4.0), an arm root beside the R3 corner, 4 mm exclusion.
(5) converged: yes.

Print-direction table (same result, measured): X: vm 2.49, sf_yield 18.07, layer sf 21.8, shear sf 13.33.
Y: sf_yield 18.07, layer sf 9.23 (layer tension across Y layers 2.44 MPa, at the far arm corner), shear sf 13.3.
Z: sf_yield 18.07, layer sf 179, shear sf 18.37. Z (spine on the bed) is best: factor 18.07 on von Mises, the governing one.

Not run: a second load way (the load is an even pressure on the pad tops, which carry the insert holes; not rigid, so not run),
a second support way (the peak did not rise with refinement). Factor 18 is far above the requirement of 2.0, so the thinnest
margin is the one the plan called weakest: the arm root under bending, not the layer measures.

**Board removal.** Free the two wire pairs at +X, undo the four M3 x 6 screws (2.5 mm hex key), lift the board straight up.
Mount stays on the rail. In: lower onto pads, wires to +X, four screws. The M5 screws (4 mm hex) are not touched in this.

**Weakest point (named by me).** The envelope: the board itself is 5 mm over Y +-25 on each side, so the design is only
inside the envelope if the board is narrower or mounted differently. Also: heat-set insert pull-out and screw preload not
studied; wires leaving low may foul the +X M5 screw head (head top about Z 9, under the board edge at x 42.5 — no contact in
the model, but not checked as wiring).

**Printing.** Spine face on the bed, layers along Z, 0.2 mm, four perimeters, no supports (nothing overhangs; the holes are
vertical). Inserts pressed in afterwards.

**Tool per screw.** M5 x 8: 4 mm hex key from above. M3 x 6: 2.5 mm hex key from above.
""")
log('D1 results and report written at', minutes(), 'min')
