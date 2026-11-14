"""D1 fit checks against the stand-ins (plan section 6). Plain python, numpy only; run under pc/capped.py."""
import itertools
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'solidworks'))
import sheet  # noqa: E402

WIP = HERE.parents[1] / '_wip' / 'sw-eval' / 'haiku-plan-d'
T0 = None


def log(*a):
    print(*a, flush=True)


def grid(lo, hi, n=14):
    return np.array(list(itertools.product(*[np.linspace(a + 0.05, b - 0.05, n) for a, b in zip(lo, hi)])))


mount = sheet.read_stl(WIP / 'buck_mount.stl')
board = np.vstack([grid((-42.5, -30, 9.0), (42.5, 30, 10.6)),
                   grid((-34, -21, 10.6), (34, 21, 24.6)),
                   grid((-34, -21, 6.0), (34, 21, 9.0))])
n_in = int(sheet.inside(mount, board).sum())
log('board points', len(board), 'inside the mount (must be 0):', n_in)

lift = board + np.array([0, 0, 30.0])
n_lift = int(sheet.inside(mount, lift).sum())
log('lifted board points inside the mount (must be 0):', n_lift)

m5_access = grid((45.5, -4.5, 4.1), (54.5, 4.5, 60))
n_m5 = int(sheet.inside(mount, m5_access).sum())
log('M5 driver column inside mount (must be 0):', n_m5, '; column starts at x 45.5, board edge at x 42.5: 3.0 mm clear')

rail = grid((-75, -10, -20), (75, 10, -0.1), 10)
n_rail = int(sheet.inside(mount, rail).sum())
log('rail points inside the mount (must be 0):', n_rail)

# the four M3 driver columns above the board corners (hex key at 2.5 mm, 5 mm clear rule in the plan)
m3_access = grid((36.0, 23.5, 10.7), (42.0, 29.5, 30.0), 6)
n_m3 = int(sheet.inside(mount, m3_access).sum())
log('M3 driver columns (x 36..42, y 23.5..29.5, z 10.7 up) inside mount (must be 0):', n_m3)
