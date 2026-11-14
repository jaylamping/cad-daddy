"""Follow-up R3a: which body moves 0.555 mm in D2_X_30. No SolidWorks."""
import sys, types
import numpy as np
from pathlib import Path
HERE = Path(__file__).resolve().parent
WIP = HERE.parents[1] / '_wip' / 'sw-eval' / 'haiku-plan-d'
SCREWS = [(x, z) for x in (-30.0, 30.0) for z in (0.0, 7.0)]
G2 = 0.4
src = (HERE / 'd2_fea.py').read_text(encoding='utf-8')
start = src.index('def split(r):')
end = src.index('def seat_angle(')
ns = {'np': np, 'SCREWS': SCREWS, 'G2': G2, 'Failed': RuntimeError}
exec(src[start:end], ns)
split = ns['split']
z = np.load(WIP / 'npz' / 'D2_X_30.npz')
r = types.SimpleNamespace(pos=z['pos'], disp=z['disp'], s=z['s'])
m = split(r)
p, d = r.pos, r.disp
print('nodes', len(p), 'disp rows', len(d), 'same order check: ids of disp col0 first 3', d[:3, 0], 'pos first', p[:3])
rho = np.hypot(p[:, 0], p[:, 1])
for name in ('ring', 'upper_all', 'lower_all', 'screw', 'pad'):
    mk = m[name]
    idx = np.where(mk)[0]
    k = idx[np.argmax(d[idx, 4])]
    print(f'{name:10s} n={mk.sum():6d} max |u| {d[k,4]:.4f} mm at node pos ({p[k,0]:.2f}, {p[k,1]:.2f}, {p[k,2]:.2f})')
ring = m['ring']
ut = (-p[:, 1] * d[:, 1] + p[:, 0] * d[:, 2]) / np.where(rho > 0, rho, 1)
print('ring tangential mean (mm)', float(ut[ring].mean()), 'rotation rad', float(ut[ring].mean() / 26.0))
print('ring UX/UY/UZ mean', d[ring, 1:4].mean(axis=0))
print('ring tangential min/max', float(ut[ring].min()), float(ut[ring].max()))
