"""D1 open-area check: share of the board footprint (85 x 60) with no printed material under it (any Z 0.5..8.5)."""
import sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'solidworks'))
import sheet
WIP = HERE.parents[1] / '_wip' / 'sw-eval' / 'haiku-plan-d'
mount = sheet.read_stl(WIP / 'buck_mount.stl')
xs = np.arange(-42.25, 42.5, 0.5)
ys = np.arange(-29.75, 30.0, 0.5)
X, Y = np.meshgrid(xs, ys, indexing='ij')
xy = np.column_stack([X.ravel(), Y.ravel()])
covered = np.zeros(len(xy), bool)
for z in (0.5, 2.0, 4.0, 6.0, 8.5):
    pts = np.column_stack([xy, np.full(len(xy), z)])
    covered |= sheet.inside(mount, pts).astype(bool)
share_cov = covered.mean()
print('grid cells', len(xy), 'covered', int(covered.sum()), 'covered share %.4f' % share_cov, 'open below share %.4f' % (1 - share_cov))
# plan's hand figure: covered 1887.7 mm2 of 5100 mm2
print('hand covered share', round(1887.7 / 5100, 4), 'hand open', round(1 - 1887.7 / 5100, 4))
