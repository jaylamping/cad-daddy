# D1 restatement (written before any modelling)

1. Purpose: hold the 12 V buck board (85 x 60 x 1.6 mm, 90 g) on the top front rail of the torso, printed in PETG, so the board can be lifted out while the mount stays on the rail.
2. Fixed: rail is 20 x 20 aluminium along X, top face at Z 0, 6 mm T-slot, M5 screws into T-nuts. Board Ø3.2 holes 3.5 mm in from each edge, parts up to 14 mm above and 3 mm below the board, two 4 mm² wire pairs leave from one 60 mm edge. Envelope: nothing more than 45 mm above the rail, 15 mm in front of or behind it (Y -25 to 25). Design load 9 N (10 g) in any direction. Both board faces at least half open to air.
3. Good means: the board comes out with the mount still on the rail; every screw is reachable with a named tool; the 9 N case has factor of safety at least 2 on the three measures; both faces at least 50 % open; light; prints without supports.
4. Mine to choose: the mount shape, orientation on the rail, fastener sizes and count, the board's standoff height, the print orientation.
5. Conflict: the envelope (Y ±25) cannot hold a board whose 60 mm side must cross Y (see the envelope analysis in REPORT.md). Chosen: board flat, 85 mm along X, 60 mm across Y, which puts ±30 mm in Y (5 mm over). Reported as envelope_ok = false; Joey can overrule in one line.

## Assumptions (questions with the answer I am assuming)

- Is the Y envelope hard? Assumed no: ±30.5 mm in Y is accepted for this part. (If yes, the board does not fit flat or upright; see REPORT.md.)
- Is the rail top free over X -45 to 45? Assumed yes.
- Which end do the wires leave from? Assumed the +X end of the 60 mm edge.
- Are heat-set inserts acceptable in the printed part? Assumed yes (M3 inserts into Ø4.0 holes).
- Do parts under the board clear the M5 button-head screw tops? Assumed yes: the spine is 7 mm above the screw tops with the arms clear of them.
- Does "open area" mean plan-view area not covered by the mount? Assumed yes.
- Does the 9 N load act on the board's centre of mass at (0, 0, 20)? Assumed yes, the board plus parts, combined.
- Is the board removable with its wires? Assumed the wires are unplugged at the board's terminals first (removal step 2).
