"""Step S1 of INSTRUCTIONS.md: copy the follow-up round's scripts into this folder and apply the reviewer's edits.

    python apply_edits2.py

Copies common.py, three scripts and restate.md from ../haiku-plan-c-followup/ (which is never written to), then
replaces exact pieces of text. Every replacement must be found the stated number of times, or nothing is written and
the script stops with the piece that was not found. It refuses to run twice (it does not overwrite).
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / 'haiku-plan-c-followup'
FILES = ['common.py', 'c2_detail.py', 'c2_fea.py', 'c2_finish.py', 'restate.md']

NEW_PRINT_TEXT = """PRINT_TEXT = ('tilted 30 degrees, hub end down: the long axis leans 30 degrees from the vertical towards +X, the hub '
              '(elbow) end is at the bed and the fork is at the top; height about 222 mm of 256, footprint about '
              '120 x 120 mm. Layers are flat on the bed, so in the part they are stacked along (0.5, 0, -0.866). '
              'Printed with a brim, no raft. Supports: under the lowest part of the hub rim and inside the bore, '
              'and a few small patches; the numbers are in orientations.json')"""

LOFT_PICKED = '''LOFT_PICK = 'x'       # which point of every section the loft is picked at: 'x' (+X tip), 'bottom' (lowest Y), 'none'


def loft_picked(d, sketches, name, rows):
    """Loft like swkit.loft(), but every section is selected AT THE SAME CORNER (its +X tip, or its lowest point).
    SolidWorks joins the sections where they were picked. Picked nowhere, it chose its own corner on each section,
    and between two sections where that choice changed the stem was twisted a quarter turn, which pinched it."""
    v0 = volume(d)
    for merge in (True, False):
        d.ClearSelection2(True)
        for sk, row in zip(sketches, rows):
            z, a, top, bot, n = row
            p = (a, (top + bot) / 2.0, z) if LOFT_PICK == 'x' else (0.0, bot, z)
            done = False
            if LOFT_PICK != 'none':
                done = bool(d.Extension.SelectByID2(sk.Name, 'SKETCH', p[0] / 1000.0, p[1] / 1000.0, p[2] / 1000.0,
                                                    True, 1, NUL, 0))
                if not done:
                    log(f'{name}: section {sk.Name} was not selected at {p}; selected without a point')
            if not done:
                sk.Select2(True, 1)
        f = d.FeatureManager.InsertProtrusionBlend2(False, True, False, 1.0, 0, 0, 1.0, 1.0, True, True, False, 0, 0, 0,
                                                    True, merge, merge, 0)
        if f is not None:
            d.ForceRebuild3(False)
            f.Name = name
            log(f'{name}: added {volume(d) - v0:.2f} mm3 (merge {merge}, sections picked at: {LOFT_PICK})')
            return f
    raise Failed(name + ': loft failed (sections must be closed, and their start points roughly in line)')


def build_stem(d, table, mode, name='STEM'):'''

EDITS = {
    'common.py': [
        ("PRINT_NORMAL = (1, 0, 0)                          # layers are stacked along X (the part stands on its -X edge)",
         "PRINT_NORMAL = (0.5, 0.0, -0.8660254)             # layers as printed tilted 30 degrees towards +X, hub end down", 1),
        ("""PRINT_TEXT = ('standing on its -X edge: X is vertical, layers stacked along X, the long axis (249 mm) along one bed '
              'axis of 256 mm, footprint 44 x 249 mm, height 72 mm; the mounting face Y -4 and the inner cheek faces '
              'are vertical walls. Only the hub rim touches the bed, on a line, so it is printed on a raft or a brim. '
              'Supports: under the whole stem and fork (they start 24 mm above the bed), under the lower half of the '
              'hub rim, and inside the top of the bore; none in the slot, which is open sideways')""", NEW_PRINT_TEXT, 1),
        ("def build_stem(d, table, mode, name='STEM'):", LOFT_PICKED, 1),
        ("    loft(d, sks, name)\n    dv = volume(d) - v0", "    loft_picked(d, sks, name, table)\n    dv = volume(d) - v0", 1),
        ("ATTEMPTS = (('closed', 'stem first'), ('arcs4', 'stem first'), ('arcs4', 'hub first'), ('poly', 'stem first'),",
         "ATTEMPTS = (('arcs4', 'stem first'), ('closed', 'stem first'), ('arcs4', 'hub first'), ('poly', 'stem first'),", 1),
        ("    return {k: measures(r, mask, n) for k, n in (('X', (1, 0, 0)), ('Y', (0, 1, 0)), ('Z', (0, 0, 1)))}",
         "    return {k: measures(r, mask, n) for k, n in (\n"
         "        ('X', (1, 0, 0)), ('Y', (0, 1, 0)), ('Z (upright)', (0, 0, 1)),\n"
         "        ('tilt 20 to X', (0.3420201, 0, -0.9396926)), ('tilt 30 to X', (0.5, 0, -0.8660254)),\n"
         "        ('tilt 45 to X', (0.7071068, 0, -0.7071068)), ('tilt 20 to Y', (0, 0.3420201, -0.9396926)),\n"
         "        ('tilt 30 to Y', (0, 0.5, -0.8660254)), ('tilt 45 to Y', (0, 0.7071068, -0.7071068)))}", 1),
    ],
    'c2_fea.py': [
        ("the three measures for layers stacked along X,", "the three measures for the print direction in common.PRINT_NORMAL,", 1),
        ("Layers stacked along X. Peaks are read", "Layers as printed tilted 30 degrees towards +X, hub end down. Peaks are read", 1),
        ("The three measures for layers along X at the finest mesh", "The three measures for the tilted print at the finest mesh", 1),
    ],
    'c2_finish.py': [
        ('verdict "{verdict}" for layers along X; sharp_per_area', 'verdict "{verdict}" for the print tilted 30 degrees; sharp_per_area', 1),
        ("the print direction was changed from layers along Y (first round, fail) to layers along X; all three read",
         "the stem loft was untwisted and the print direction changed to a 30 degree tilt, hub end down; all directions read", 1),
    ],
}

if (HERE / 'common.py').exists():
    raise SystemExit('common.py is already in this folder: apply_edits2.py has run before. Do not run it twice.')
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
(HERE / 'exports').mkdir(exist_ok=True)
print('EDITS OK:', sum(len(v) for v in EDITS.values()), 'pieces replaced in', len(EDITS), 'files;', len(FILES), 'files copied')
