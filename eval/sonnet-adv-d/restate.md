# D1 restated: a mount for the 12 V buck board on the top front rail

## The five lines
1. **What it is for:** hold the 85 x 60 x 1.6 mm, 90 g buck board on the 20 x 20 rail along X (top face Z 0), printed PETG, and let the board be taken out and put back with the mount still screwed to the rail.
2. **Fixed:** the rail (T-slot 6 mm in each face, M5 into T-nuts); the board and its four Ø3.2 holes (78 x 53 mm pattern, 3.5 mm in from each edge); parts 14 mm above and 3 mm below the board; the load 10 g = 9 N in any direction; the two wire pairs leave one 60 mm edge; both board faces at least half open to air; envelope Y -25..25, Z up to 45.
3. **Good means:** the board is out after removing only the four board screws (nothing else touched), every screw is reached by a straight tool path from above, load factor 2 or better on all three printed-PETG measures, a print with no supports, and the lowest mass that does that.
4. **Mine to choose:** the board's orientation, the mount concept, screw sizes and tools, the insert type, print orientation, which limit gives way where the specification cannot be met.
5. **Does not exist / unknown:** where the tall parts stand on the board, which way the wires route, the T-nut type, and whether the +Y and -Y sides of the rail are free.

## The specification does not fit itself (arithmetic, `d1_envelope.py`, `d1_tilt_scan.py`, `d1_tilt45.py`)
Seen along X the board with its parts is a 60 x (3 + 1.6 + 14) = 60 x 18.6 mm rectangle. The region allowed (Y -25..25, Z up to 45, outside the rail below Z 0) cannot hold it at any tilt:

| Tilt of the 60 mm edge (0 = flat) | Least overshoot of the allowed region, mm |
| --- | --- |
| 0 (flat, 60 along Y) | 5.0 (Y -30..30) |
| 30 | 5.8 |
| 40 | 4.0 |
| 45 | 2.8 (but the board then dips 11 mm beside the rail and its 3 mm of under-parts runs into the rail) |
| 90 (on edge, 60 along Z) | 2.0 (needs 18.6 mm of Y beside the rail, 15 are allowed, plus a bracket plate on top of that) |

Even the bare board (no parts) cannot lie flat: 60 mm against 50 mm of Y. Lying flat is the only layout that keeps everything above Z 0 and every screw reachable from above; tilting gains 5.0 -> 2.8 mm at best, at the price of a leg beside the rail and a pinch point where the board plane passes the rail corner.

**Decision (nearest thing that works):** the board lies flat, 85 mm along X, 60 mm across Y. Gave up: the Y limit, by 5.0 mm on each side for the board and its parts (Y -30..30). Z has 21 mm to spare (the stack tops out near 27 mm against 45), and the rail keeps its 20 mm width. The mount body itself stays inside Y -30..30 only at the board pads. Cost of the other choice: tilting 45 degrees saves 2.2 mm of Y and costs a dipped, unsupported leg beside the rail (not drawn).

## Questions I would ask, each with the answer I am assuming so that work goes on
1. Which limit has room: Y (±25), Z (45) or the rail's own sides? **Assumed:** Z has room, Y does not; the sides of the rail beyond Y ±25 are free air for 5 mm.
2. Where are the 14 mm parts on the board? **Assumed:** anywhere, so full height across the whole 60 mm width (nothing about the layout is relied on).
3. Which side is "above"? **Assumed:** the 14 mm side faces +Z, the 3 mm side faces the rail.
4. Which way do the wires run? **Assumed:** out of the +X end edge, over the base, and bend upward away from the mount; 4 mm² wire pairs need about 25 mm of bend room.
5. Which T-nuts are in the rail? **Assumed:** M5 drop-in or roll-in T-nuts for the 6 mm slot, slot lip 1.8 mm thick.
6. Can the robot's rail run be reached by a hex key from above at the mount's X position? **Assumed:** yes, nothing is above the rail within 100 mm.
7. Is a board screw allowed to be M3 with heat-set inserts? **Assumed:** yes, M3 inserts (Ø4.0 holes, 5 mm deep) are on hand; PETG threads strip.
8. Does "10 g in any direction" include the rail moving, so the rail screws must hold the whole 9 N? **Assumed:** 9 N acting at the board's centre of gravity, from the board alone; the mount's own 20 g adds under 1 N.
9. Is a printed strain relief for the wires wanted? **Assumed:** not asked; a zip tie round the base is the user's own.
