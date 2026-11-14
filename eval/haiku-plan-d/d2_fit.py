"""D2 fit check on the exported STLs (plan section 6). Plain python, numpy only; run under pc/capped.py."""
import math
import sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'solidworks'))
import sheet
WIP = HERE.parents[1] / '_wip' / 'sw-eval' / 'haiku-plan-d'
up, lo = sheet.read_stl(WIP / 'housing_upper.stl'), sheet.read_stl(WIP / 'housing_lower.stl')


def log(*a):
    print(*a, flush=True)


def shell_pts(r0, r1, z0, z1, nr=5, na=240, nz=9):
    return np.array([(r * math.cos(a), r * math.sin(a), z) for r in np.linspace(r0, r1, nr)
                     for a in np.linspace(0, 2 * math.pi, na, endpoint=False) for z in np.linspace(z0, z1, nz)])


def hits(pts):
    return int(sheet.inside(up, pts).sum()), int(sheet.inside(lo, pts).sum())


log('ring (r 24..25.97, z 0.02..6.98) inside upper, lower: must be (0, 0):', hits(shell_pts(24.0, 25.97, 0.02, 6.98)))
log('ring grown 0.2 radially must hit both (it proves the test sees the seats):', hits(shell_pts(26.15, 26.2, 1.0, 6.0, nr=2)))
log('inner ring and shaft (r 0..22.2, z -4..11) must be (0, 0):', hits(shell_pts(0.5, 22.2, -4.0, 11.0, nr=12)))
log('ring sides: shoulders at z -0.15, 7.15 -> points at z -0.10 and 7.10, r 24.6..25.9: must be (0, 0):',
    hits(shell_pts(24.6, 25.9, -0.10, 7.10, nr=3, nz=2)))
log('and at z -0.20 and 7.20 they must hit (proves the sides are where the shoulder is):',
    hits(shell_pts(24.6, 25.9, -0.20, 7.20, nr=3, nz=2)))
log('as specified (opening 43.5): shoulder would start at r 21.75, inside the inner ring (r 22.0) by 0.25 (hand, not run)')
