"""Step U1 of INSTRUCTIONS.md: copy the third round's scripts into this folder and add the stem table STEM_A5.

    python apply_edits4.py

Copies common.py, three scripts, restate.md and r2_tools.py from ../haiku-plan-c-round3/ as that round left them
(never written to), then adds to one exact line of common.py. Not found exactly once: nothing is written. It refuses
to run twice.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / 'haiku-plan-c-round3'
FILES = ['common.py', 'c2_detail.py', 'c2_fea.py', 'c2_finish.py', 'restate.md', 'r2_tools.py']

OLD = "FORM_VOL['STEM_A4'] = 113840.0"
NEW = OLD + '''
# Round 4: STEM_A4 with two changes at the neck, each aimed at one of the two places round 3 failed.
# 1. Z -27: top back to 7.6 (as STEM_A3). The deeper neck stood 3 mm higher beside the two lower screw-head pockets
#    and the pocket edge became a notch (shear between layers 9.3 MPa at X -9, Y 4.2, Z -22.4).
# 2. A row at Z -34.5 and a lower underside from there (bot -6.5, -8.5, -10.8): the cable tunnel's underside at
#    Y -3.2 ran 0.3 to 1.8 mm above the stem's underside just past the mounting ring (tension across layers 13.2 MPa
#    at Z -34.5, on the tunnel wall); now there are 3 mm or more under it.
STEM_A5 = [(-22.0, 27.0, 3.6, -3.4, 2.6), (-27.0, 26.0, 7.6, -3.4, 3.0), (-32.0, 24.4, 13.7, -3.5, 3.2),
           (-34.5, 22.8, 14.2, -6.5, 3.1), (-38.0, 20.5, 14.6, -8.5, 3.0), (-46.0, 16.6, 14.4, -10.8, 2.6),
           (-60.0, 13.6, 13.8, -12.6, 2.3)] + STEM_A3[6:]
TABLES['STEM_A5'] = STEM_A5
STEM_VOL['STEM_A5'] = 112000.0
FORM_VOL['STEM_A5'] = 114200.0'''

if (HERE / 'common.py').exists():
    raise SystemExit('common.py is already in this folder: apply_edits4.py has run before. Do not run it twice.')
texts = {}
for name in FILES:
    raw = (SRC / name).read_bytes()
    if name == 'common.py':
        text = raw.decode('utf-8').replace('\r\n', '\n')
        have = text.count(OLD)
        if have != 1:
            raise SystemExit(f'common.py: expected 1 of this piece, found {have}; nothing written:\n{OLD}')
        raw = text.replace(OLD, NEW).encode('utf-8')
    texts[name] = raw
for name, raw in texts.items():
    (HERE / name).write_bytes(raw)
(HERE / 'pictures').mkdir(exist_ok=True)
(HERE / 'exports').mkdir(exist_ok=True)
print('EDITS OK: STEM_A5 added;', len(FILES), 'files copied')
