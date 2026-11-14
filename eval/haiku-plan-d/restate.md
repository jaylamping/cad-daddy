# D1 restated

Written 2026-11-14 before any modelling (14:2x local). Copied from the plan's section 3 with my own check of the
envelope arithmetic (see "Conflict" below).

1. Purpose: hold the 12 V buck board (85 x 60 x 1.6 mm, 90 g) on the top front rail of the torso, printed PETG, so the
   board can be taken out without taking the mount off the rail.
2. Fixed: rail 20 x 20 along X, top face at Z 0, 6 mm T-slot down the middle of each face, M5 screws into T-nuts.
   Board four dia 3.2 holes, 3.5 mm in from each edge; parts may stand 14 mm above and 3 mm below the board; the two
   4 mm^2 wire pairs leave from one 60 mm edge. Load: 10 g in any direction = 9 N (board 90 g). Air to both board faces
   over at least half their area. Nothing above Z 45 or outside Y -25..25 (overall).
3. Good means: the board comes out with the mount still on the rail; every screw reachable with a plain hex key;
   9 N in any direction with a factor of at least 2.0 on the three measures; at least half of each board face open;
   inside Z 45 and Y -25..25 as far as the board allows; light; prints without supports.
4. Mine to choose: the shape, where it bolts to the rail, how the board is held, print direction, length along X.
5. Conflict found: the board is 60 mm wide, the Y envelope is 50 mm. Flat, the board reaches Y +-30, 5 mm over each
   side. On edge it is 60 mm tall plus a seat (over the 45 mm height). Tilted, I checked 60 cos t + 18.6 sin t <= 50
   and 60 sin t + 18.6 cos t <= 45 over 0..90 deg in 0.5 deg steps (script result in the report). Decision: board flat,
   85 mm along X, centred on the rail; the Y limit is exceeded by the board itself by 5 mm each side; no printed
   material goes beyond the board's own outline.

Assumptions: board flat, long side along X, centred on the rail. Wires leave at the +X end. Parts may sit on both
faces, up to 3 mm from the edges. M3 x 6 screws into M3 heat-set inserts (dia 4.0 x 6 holes) hold the board. Two M5 x 8
into T-nuts hold the mount, outside the board's ends. X length is free (the mount is 112 mm long). No factor was named:
2.0 is used, as for the other printed parts.

Questions (answer assumed so that work can go on):
1. Which gives, the 50 mm Y envelope or the board's 60 mm width? Assumed: the envelope, by 5 mm each side, by the board
   only.
2. Which end do the wires leave from, and do they need strain relief? Assumed: the +X end, no strain relief.
3. Is 112 mm of rail along X free? Assumed: yes.
4. Heat-set inserts acceptable, or screws straight into plastic? Assumed: inserts.
5. Anything under the board within 3 mm of its edges? Assumed: no (the mount's pads sit there).
6. Does "10 g" include a factor, and is 2.0 the factor wanted? Assumed: 9 N is the load, 2.0 on top.
