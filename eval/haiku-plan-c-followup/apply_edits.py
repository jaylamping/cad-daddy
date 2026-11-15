"""Step R1 of INSTRUCTIONS.md: copy the first round's scripts into this folder and apply the reviewer's edits.

    python apply_edits.py

Copies common.py, the six scripts and restate.md from ../haiku-plan-c/ (which is never written to), then replaces
exact pieces of text. Every replacement must be found the stated number of times, or nothing is written and the
script stops with the piece that was not found. It refuses to run twice (it does not overwrite).
"""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / 'haiku-plan-c'
FILES = ['common.py', 'c1_boxy.py', 'c2_ideas.py', 'c2_detail.py', 'c2_fea.py', 'c2_finish.py', 'c2_loftpairs.py', 'restate.md']

NEW_PRINT_TEXT = """PRINT_TEXT = ('standing on its -X edge: X is vertical, layers stacked along X, the long axis (249 mm) along one bed '
              'axis of 256 mm, footprint 44 x 249 mm, height 72 mm; the mounting face Y -4 and the inner cheek faces '
              'are vertical walls. Only the hub rim touches the bed, on a line, so it is printed on a raft or a brim. '
              'Supports: under the whole stem and fork (they start 24 mm above the bed), under the lower half of the '
              'hub rim, and inside the top of the bore; none in the slot, which is open sideways')"""

EDITS = {
    'common.py': [
        # the print direction: layers along X
        ("PRINT_NORMAL = (0, 1, 0)                          # layers are stacked along Y (the part lies on its +Y side)",
         "PRINT_NORMAL = (1, 0, 0)                          # layers are stacked along X (the part stands on its -X edge)", 1),
        ("""PRINT_TEXT = ('lying on its +Y side: the flat outer face of the +Y cheek (Y +22) on the bed, layers stacked along Y, '
              'the long axis (248 mm) along one bed axis of 256 mm; the mounting face Y -4 is a top surface. '
              'Supports: under the +Y side of the hub and of the stem (they stand 9 to 18 mm off the bed), and in '
              'the slot under the upper (-Y) cheek')""", NEW_PRINT_TEXT, 1),
        # evenly spaced section rows: one more between Z -60 and -85, -85 and -115, -115 and -145 (straight-line values)
        ("(-60.0, 12.4, 12.0, -11.0, 2.2),", "(-60.0, 12.4, 12.0, -11.0, 2.2), (-72.0, 11.9, 12.0, -11.5, 2.15),", 1),
        ("(-60.0, 12.6, 12.8, -11.8, 2.2),", "(-60.0, 12.6, 12.8, -11.8, 2.2), (-72.0, 12.0, 12.4, -11.9, 2.15),", 1),
        ("(-85.0, 11.4, 12.0, -12.0, 2.1), (-115.0, 10.6, 11.8, -11.8, 2.1),",
         "(-85.0, 11.4, 12.0, -12.0, 2.1), (-100.0, 11.0, 11.9, -11.9, 2.1), (-115.0, 10.6, 11.8, -11.8, 2.1), "
         "(-130.0, 10.8, 12.8, -12.8, 2.3),", 2),                                        # STEM_A and STEM_A2
        ("(-60.0, 13.2, 13.4, -12.4, 2.3),", "(-60.0, 13.2, 13.4, -12.4, 2.3), (-72.0, 12.5, 13.0, -12.5, 2.2),", 1),
        ("(-85.0, 11.8, 12.6, -12.6, 2.1), (-115.0, 10.8, 12.0, -12.0, 2.1),",
         "(-85.0, 11.8, 12.6, -12.6, 2.1), (-100.0, 11.3, 12.3, -12.3, 2.1), (-115.0, 10.8, 12.0, -12.0, 2.1), "
         "(-130.0, 10.9, 12.9, -12.9, 2.3),", 1),                                        # STEM_A3
        ("(-60.0, 18.0, 7.0, -7.0, 3.0), (-90.0, 15.0, 7.0, -7.0, 3.0),",
         "(-60.0, 18.0, 7.0, -7.0, 3.0), (-75.0, 16.5, 7.0, -7.0, 3.0), (-90.0, 15.0, 7.0, -7.0, 3.0), "
         "(-105.0, 14.1, 7.7, -7.7, 3.0),", 1),                                          # STEM_B
        ("(-120.0, 13.2, 8.4, -8.4, 3.0),", "(-120.0, 13.2, 8.4, -8.4, 3.0), (-132.0, 12.7, 10.6, -10.6, 3.0),", 1),
        # idea B back to the planner's window and volumes
        ("WINDOW_B = [(0.0, -38.0), (8.0, -38.5)", "WINDOW_B = [(0.0, -36.0), (8.0, -38.5)", 1),
        ("            (0.0, -126.0)]", "            (0.0, -128.0)]", 1),
        ("STEM_B=88379.1)", "STEM_B=97800.0)", 1),
        ("STEM_B=68979.1)", "STEM_B=78400.0)", 1),
    ],
    'c2_detail.py': [
        ("fillet(d, seam, (3.0, 2.0, 1.2), 'RAMP_BLEND')", "fillet(d, seam, (2.0, 1.2), 'RAMP_BLEND')", 1),
    ],
    'c2_fea.py': [
        ("['Y']", "['chosen']", 17),                 # the measures for the print direction in common.PRINT_NORMAL
        ("Y=measures(r, keep),", "chosen=measures(r, keep),", 1),
        ("for dd in (2.0, 3.0, 5.0)})\n",
         "for dd in (2.0, 3.0, 5.0)})\n"
         "    out['chosen_outside_mm'] = {str(dd): measures(r, r.away(dist=dd)) for dd in (2.0, 3.0, 5.0)}\n", 1),
        ("the three measures for layers stacked along Y,", "the three measures for layers stacked along X,", 1),
        ("Layers stacked along Y. Peaks are read", "Layers stacked along X. Peaks are read", 1),
        ("print('VERDICT', v['verdict'],",
         "report('- The three measures for layers along X at the finest mesh, read outside 2, 3 and 5 mm from the held and '\n"
         "       f'loaded faces (the verdict uses {DIST} mm): '\n"
         "       + str([(c, {dd: {m: mm[m] for m in ALLOW} for dd, mm in fine[c]['chosen_outside_mm'].items()}) for c in CASES]))\n"
         "print('VERDICT', v['verdict'],", 1),
    ],
    'c2_finish.py': [
        ("'tried at R3, R2 and R1.2, did not build: a crease of about 30 degrees is left'",
         "'tried at R3 in the first round and from R2 down in this one, no sound blend: a crease of about 30 degrees is left'", 1),
        ('verdict "{verdict}"; sharp_per_area', 'verdict "{verdict}" for layers along X; sharp_per_area', 1),
        ("the print direction is already the best of the three read",
         "the print direction was changed from layers along Y (first round, fail) to layers along X; all three read", 1),
    ],
}

if (HERE / 'common.py').exists():
    raise SystemExit('common.py is already in this folder: apply_edits.py has run before. Do not run it twice.')
texts = {}
for name in FILES:
    raw = (SRC / name).read_bytes()
    if name in EDITS:
        text = raw.decode('utf-8').replace('\r\n', '\n')      # a Windows checkout gives CRLF; the pieces are LF
        for old, new, count in EDITS[name]:
            have = text.count(old)
            if have != count:
                raise SystemExit(f'{name}: expected {count} of this piece, found {have}; nothing written:\n{old}')
            text = text.replace(old, new)
        raw = text.encode('utf-8')
    texts[name] = raw
for name, raw in texts.items():
    (HERE / name).write_bytes(raw)
(HERE / 'pictures').mkdir(exist_ok=True)
print('EDITS OK:', sum(len(v) for v in EDITS.values()), 'pieces replaced in', len(EDITS), 'files;', len(FILES), 'files copied')
