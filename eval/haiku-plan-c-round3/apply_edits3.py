"""Step T1 of INSTRUCTIONS.md: copy the second round's scripts into this folder and add the stem table STEM_A4.

    python apply_edits3.py

Copies common.py, three scripts, restate.md and r2_tools.py from ../haiku-plan-c-round2/ as that round left them
(which is never written to), then replaces one exact piece of text in common.py. If the piece is not found exactly
once, nothing is written. It refuses to run twice.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / 'haiku-plan-c-round2'
FILES = ['common.py', 'c2_detail.py', 'c2_fea.py', 'c2_finish.py', 'restate.md', 'r2_tools.py']

OLD = "TABLES = dict(STEM_A=STEM_A, STEM_A2=STEM_A2, STEM_A3=STEM_A3, STEM_B=STEM_B)"
NEW = OLD + '''
# Idea A, third fallback (round 3): STEM_A3 with a deeper and wider neck, Z -27 to -60. The second round failed at
# the neck (1.38 with STEM_A2, 1.57 with STEM_A3, tension across layers under a load along Y at Z -34.5); the stem
# below Z -72 is STEM_A3 unchanged. Section modulus for a load along Y against STEM_A3: x1.32 at Z -27, x1.45 at
# Z -32, x1.26 at Z -38, x1.14 at Z -46.
STEM_A4 = [(-22.0, 27.0, 3.6, -3.4, 2.6), (-27.0, 26.0, 9.0, -3.4, 3.0), (-32.0, 24.4, 13.7, -3.5, 3.2),
           (-38.0, 20.5, 14.6, -7.0, 3.0), (-46.0, 16.6, 14.4, -10.4, 2.6), (-60.0, 13.6, 13.8, -12.6, 2.3)] + STEM_A3[6:]
TABLES['STEM_A4'] = STEM_A4
STEM_VOL['STEM_A4'] = 111640.0
FORM_VOL['STEM_A4'] = 113840.0'''

if (HERE / 'common.py').exists():
    raise SystemExit('common.py is already in this folder: apply_edits3.py has run before. Do not run it twice.')
texts = {}
for name in FILES:
    raw = (SRC / name).read_bytes()
    if name == 'common.py':
        text = raw.decode('utf-8').replace('\r\n', '\n')
        have = text.count(OLD)
        if have != 1:
            raise SystemExit(f'common.py: expected 1 of this piece, found {have}; nothing written:\n{OLD}')
        if "LOFT_PICK = 'bottom'" not in text:
            raise SystemExit("common.py of round 2 does not have LOFT_PICK = 'bottom': nothing written. Report this line.")
        raw = text.replace(OLD, NEW).encode('utf-8')
    texts[name] = raw
for name, raw in texts.items():
    (HERE / name).write_bytes(raw)
(HERE / 'pictures').mkdir(exist_ok=True)
(HERE / 'exports').mkdir(exist_ok=True)
print('EDITS OK: STEM_A4 added;', len(FILES), 'files copied')
