# D1 restatement: buck board mount on the top front rail

Started 2026-11-14 09:23 UTC, the first action of the run (task limit 60 min).

## The five lines

1. A printed PETG mount holds the 85 x 60 x 1.6 mm, 90 g, 12 V buck board on the front face of the 20 x 20 rail.
2. The board comes out forwards by removing four M3 screws from its front side; the mount stays on the rail.
3. Design load: 10 g in any direction, which is 9 N on the board. Both faces of the board stay open to air.
4. Nothing reaches more than 45 mm above the rail (Z 45 or lower) or outside Y -25..25.
5. Two M5 screws into the rail's T-slot hold the mount; no part of it moves when the board comes out.

## Where the brief conflicts with itself (found before any model)

- **Horizontal board does not fit the Y envelope.** A board lying flat on the rail is 60 mm across Y, which is over the
  Y -25..25 limit (50 mm). Turned 85 mm along Y it is worse. Only the 1.6 mm edge fits across Y, so the board must stand
  on edge in the XZ plane.
- **Front components cannot have 14 mm.** With the board standing in front of the rail, the board's front face sits at
  Y about 19 once its mount is in place. Y 25 minus that leaves about 6 mm for components on the front side, not 14.
  The brief's 14 mm allowance cannot be met inside the envelope. Built as: front components limited to 5.9 mm.
- **The board's own footprint is over the Y limit anyway (60 mm in Y would be 30 mm either side of centre).** Taking it
  vertical fixes that. The envelope is applied to the mount and its parts; the board is the load.
- **Open area** is ambiguous when the rail sits behind the board (see the numbers below).

## Assumptions (decided, not asked)

- Board stands in the XZ plane at Y 17.5 to 19.1 (back face at Y 17.5), board Z -17 to 43, X -42.5 to 42.5.
- Board holes Ø3.2 at X ±39, Z -13.5 and 39.5 (3.5 mm in from each edge).
- Rail front T-slot centre line at Z -10; rail front face at Y 10.
- Board wires leave from the X +42.5 edge (the 60 mm edge).
- 9 N is applied as 2.25 N at each board hole, pushing the board forward or back, one load case each way.
- The rail is rigid, and its face is what the mount bears on.
- Print orientation: mount lying flat on the bed (XZ plane on the bed, Y up), so layers run in the XZ plane.

## Questions I would ask, with the answer I am assuming

1. Does the Y ±25 envelope include the board and its components? Assumed: no, the mount and its fasteners only. The board's
   front components are limited to 5.9 mm (the envelope applies to them too).
2. Is 14 mm front clearance a hard need? Assumed: no. Limit set by the envelope; if a taller part is needed, the rail would
   have to move or the envelope grow.
3. Does open area count the rail behind the board? Assumed: yes, the rail counts as a blocking surface behind the board. The
   number is given both ways.
4. Is M3 access from the front enough for removal? Assumed: yes, a 2.5 mm hex driver reaches over 5.9 mm components.

## Two ideas that differ in kind

- **Idea A (chosen): standing frame.** An open printed frame bolted to the rail's front T-slot, with four bosses that the
  board screws onto from the front. Board is in the XZ plane.
- **Idea B: horizontal cradle on top of the rail.** A flat tray in the top T-slot holding the board lying flat. Rejected:
  the 60 mm board across Y breaks the Y ±25 envelope by 5 mm each side, and the 85 mm length would stick out past
  the rail's X length in any stand-in. It is shown as a picture so the envelope failure can be seen.

Pictures for both: `eval/haiku-d/pictures/` (A is `d1_idea_a.sheet.png`, B is `d1_idea_b.sheet.png`).
