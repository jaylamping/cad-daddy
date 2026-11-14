"""Writes D3 keys to results.json and the D3 section to REPORT.md from d3_part1.json and d3_part2.json."""
from common import *  # noqa: F401,F403

P1 = json.loads((HERE / 'd3_part1.json').read_text(encoding='utf-8'))
P2 = json.loads((HERE / 'd3_part2.json').read_text(encoding='utf-8'))
plates = {n: dict(volume_mm3=round(p['volume_mm3'], 2), hand_volume_mm3=round(p['hand_volume_mm3'], 2),
                  min_wall_mm=p['min_wall_mm'], min_wall_where=p['min_wall_where'], changed=p['changed'], why=p['why'],
                  bodies=p['bodies'], stl_watertight=bool(p['stl_watertight']))
          for n, p in P1.items()}
plates_b = {n: dict(volume_mm3=round(p['volume_mm3'], 2), hand_volume_mm3=round(p['hand_volume_mm3'], 2),
                    min_wall_mm=p['min_wall_mm'], min_wall_where=p['min_wall_where'], changed=p['changed'], why=p['why'],
                    counterbore_floor_z_mm=round(p['counterbore_floor_z_mm'], 3), old_features_unchanged=p['old_features_unchanged'],
                    new_features=p['new_features'], bodies=p['bodies'], stl_watertight=bool(p['stl_watertight']))
            for n, p in P2.items()}
edited = all(p['old_features_unchanged'] and p['new_features'] == ['TOP_CHAMFER'] for p in P2.values())
put('D3',
    status='done',
    plates=plates, plates_b=plates_b,
    table_problems=[
        'P1: ring B counterbore overlaps a ring A hole by 0.7 mm at 0 deg -> ring B turned 45 deg (wall 3.02)',
        'P2: rings A and B are the same six holes at 0 deg -> ring B turned 30 deg (wall 9.80)',
        'P3: fine as table; counterbore edge 1.0 mm from outside (flagged, built as asked)',
        'P4: ring B on Ø58 breaks out of a Ø60 plate by 3.0 mm -> OD 68, bolt circle kept (wall 1.0)',
        'P4: counterbore 4.6 deep in a 5 mm plate leaves 0.4 mm floor -> depth 3.0, floor 2.0',
        'P1, P3 and P4 outer walls 1.0 mm: flagged, built as asked',
        'part two P3: ring A on Ø70 from 0 deg is 0.3 mm from the ring B counterbore -> ring A turned 22.5 deg (wall 9.82)',
        'part two P1, P3, P4: 1.0 mm chamfer meets the counterbore edge (knife edge) -> 0.4 mm chamfer (wall 0.6)'],
    one_script=True,
    edited_not_rebuilt=edited,
    minutes=6,
    notes=('edited_not_rebuilt: opened each saved part, set DISC to T+1.5, moved the counterbore floor check (unchanged, Z = T-c measured), '
           'added one feature TOP_CHAMFER, tree IDs and names before the edit are unchanged. P3 ring A redrawn by redraw_circles. '
           'min_wall_mm from walls() after measure() showed every hole where the numbers say. The STL volume differs from the model by at most 0.1%. '
           'The coordinate check in measure() was made absolute: expect() is relative for a non-zero wanted value, and a coordinate that should be 0 failed on float noise. '
           'Not verified: walls measured on the mesh, the 0.6 mm walls beside the chamfers (P1, P3, P4) are at the limit, not beyond it.'))

report("""## D3. Six plates from a table, then a change

Times: table check 14:37 (before any build); part one 14:37:37 to 14:38:41 (about 1 min of SolidWorks); table and picture 14:38:53;
part two 14:38:59 to 14:39:16 (about 17 s). Waiting: none beyond the launch. The whole task took about 2 minutes of SolidWorks time.

**Table check (before SolidWorks).** Printed by the script for the table as given: P1 A hole to B counterbore -0.7; P2 -6.25;
P4 B counterbore to outside -3.0 and counterbore floor 0.4; P3 2.3 (fine). As built, no value under 0.6 except the chamfer
rows. Hand volumes for every plate agree with the plan's table to 0.01 mm3.

**Problems and decisions (the table fixes are in results.json `table_problems`):**
- P1: B counterbore overlaps an A hole by 0.7 mm -> ring B turned 45 deg (wall 3.02 mm). Dimensions as the table.
- P2: rings A and B are the same six holes -> ring B turned 30 deg (wall 9.80 mm).
- P4: ring B on Ø58 breaks out of the Ø60 plate by 3.0 mm, bolt circle kept -> OD 68 (wall 1.0 mm, like P1 and P3). The other choice
  (keep OD 60) would need ring B on Ø50 or less. "P4 was built Ø68; say so if Ø60 matters more than the Ø58 bolt circle."
- P4: counterbore 4.6 deep in a 5 mm plate leaves a 0.4 mm floor -> depth 3.0, floor 2.0.
- P1, P3, P4 and the 1.0 mm outer walls: built as asked, flagged.
- Part two, P3: ring A on Ø70 from 0 deg is 0.3 mm from the ring B counterbore -> turned 22.5 deg (wall 9.82 mm).
- Part two, P1, P3, P4: 1 mm chamfer meets the counterbore edge (knife edge) -> 0.4 mm chamfer, leaving 0.6 mm. P2, P5, P6 take 1.0 mm.

**Part one (one script, one function, six plates, `d3_table_part1.md`):**

| Plate | Volume mm3 | Hand mm3 | Diff % | Mass g | Bodies | STL watertight | Thinnest wall mm (where) | As table or changed |
|---|---|---|---|---|---|---|---|---|
| P1 | 17728.67 | 17728.67 | 0.000 | 21.10 | 1 | yes | 1.0 (B counterbore to outside) | changed: ring B turned 45 deg |
| P2 | 23947.18 | 23947.18 | 0.000 | 28.50 | 1 | yes | 3.0 (counterbore floor) | changed: ring B turned 30 deg |
| P3 | 38698.26 | 38698.26 | 0.000 | 46.05 | 1 | yes | 1.0 (B counterbore to outside) | as the table |
| P4 | 13802.43 | 13802.43 | 0.000 | 16.42 | 1 | yes | 1.0 (B counterbore to outside) | changed: OD 68, counterbore 3.0 |
| P5 | 62864.78 | 62864.78 | 0.000 | 74.81 | 1 | yes | 2.5 (B counterbore to outside) | as the table |
| P6 | 20848.86 | 20848.86 | 0.000 | 24.81 | 1 | yes | 2.0 (B counterbore to outside) | as the table |

Each plate: box exact; outside face and bore face found; 16, 24, 12 hole and counterbore faces checked (on P1 to P6, counted from the
table); each hole centre and radius read from the solid; counterbore floors at Z = T-c within 0.01; rebuild errors 0; STL volume within
0.1 % of the model; picture pictures/d3_part1.png, looked at: six rings with the expected holes, P1 and P2 turned, P4 larger.

**Part two (by editing, `d3_table_part2.md`).** Each saved part opened, saved as `_b`, DISC set from T to T+1.5 (`set_dim`), P3 ring
A redrawn on Ø70 (`redraw_circles`), and a top outside chamfer added (`chamfer`, one feature, `TOP_CHAMFER`). Tree before and after:
the same features and IDs, one new feature, floor Z unchanged (3.00, 3.00, 4.00, 2.00, 3.00, 3.00).

| Plate | Volume mm3 | Hand mm3 | Mass g | Thinnest wall mm (where) | Floor Z | Old features unchanged | New |
|---|---|---|---|---|---|---|---|
| P1_b | 22040.22 | 22040.22 | 26.23 | 0.6 (chamfer to counterbore) | 3.00 | yes | TOP_CHAMFER |
| P2_b | 29648.45 | 29648.45 | 35.28 | 3.0 (counterbore floor) | 3.00 | yes | TOP_CHAMFER |
| P3_b | 45765.78 | 45765.78 | 54.46 | 0.6 (chamfer to counterbore) | 4.00 | yes | TOP_CHAMFER |
| P4_b | 17802.44 | 17802.44 | 21.18 | 0.6 (chamfer to counterbore) | 2.00 | yes | TOP_CHAMFER |
| P5_b | 74259.20 | 74259.20 | 88.37 | 1.5 (chamfer to counterbore) | 3.00 | yes | TOP_CHAMFER |
| P6_b | 25865.43 | 25865.43 | 30.78 | 1.0 (chamfer to counterbore) | 3.00 | yes | TOP_CHAMFER |

All six `_b` volumes match the plan's hand values. The chamfer dv matches pi w² (R − w/3) within 0.02 mm³ on each plate. The
picture `pictures/d3_part2.png` was looked at: thicker plates, a chamfer on each top rim, P3's ring A further out and turned.

**Weakest points (named by me).** The 0.6 mm wall between each 0.4 mm chamfer and the counterbore on P1, P3 and P4 is at the limit of
the 0.6 mm rule, not beyond it. The 1.0 mm outer walls on P1, P3 and P4 are thin but above the rule. Walls are from the numbers
(`walls()`), checked against the solid by `measure()`, not measured on the mesh.

**Process note.** The first part-one run stopped at the first hole check: `expect()` is relative for a non-zero wanted value, and a
hole coordinate that should be 0 came out as 6e-17. I changed `measure()` to an absolute 0.03 mm check on hole x and y (noted in
plates.py); the same run then passed every plate. This is a fault in the helper's tolerance rule, not in the parts.
""")
log('D3 results and report written at', minutes(), 'min')
