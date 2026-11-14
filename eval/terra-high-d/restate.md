# D1 restatement — 2026-11-13 18:30 CST

- Hold the buck board on the rail during a 9 N acceleration, allowing board removal with the mount on the rail.
- Rail 20 mm square with M5 slot, board 85 x 60 x 1.6 and four holes at 3.5 mm edge inset; preserve component clearance.
- Target open air over at least half of each board face; accessible fasteners; printed PETG.
- Given Y envelope is only 50 mm: an 85 x 60 mm horizontal board itself exceeds it by 5 mm on each side. A tilted board plus 14 mm components above and 3 mm below also cannot fit inside a 50 x 45 mm cross-section: the 60 x 18.6 mm minimum rectangle has no rotation that fits both dimensions. Keep the interfaces and ventilation; use Y ±30 mm for the board and mounting frame, 5 mm beyond each side.
- Choose one slotted, open H-frame with four board standoffs; alternative is a full-width pair of independent rails. Choose the single frame for handling and access.

Assumptions and questions (answers used):
- Is the envelope absolute for wires too? Assume no wires included; wire bend radii and adjacent torso parts remain to be checked.
- Which edge carries the wires? Assume the +X 60 mm edge; reserve that end for the cables.
- Are hole areas free of components? Assume a 6 mm diameter footprint around each board hole and M3 screw-head access.
- Is metal-to-board contact allowed? Use nylon washers and M3 hardware; check actual board/component clearances before building.
- Rail nut access? Two M5 T-nuts slide in or drop in, with screw heads outside the board's X extent.
- Board plane? Horizontal, lower face Z=8 mm, parts beneath extend to Z=5, 1 mm above frame; top components reach Z=23.6 mm.
- Is the shared settings restriction compatible with the export helper? No: swkit.export calls pin_export_prefs, which changes machine-wide settings. Use save_as with existing settings and inspect exports; do not change them.

Stage budget: 15 minutes geometry/checkpoint, 15 detail and assembly, 20 study, 10 report. Start 18:30 CST; deadline 19:30 CST.
