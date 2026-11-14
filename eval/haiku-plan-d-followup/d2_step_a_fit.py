"""Follow-up R3a addendum: rigid fit (translation + turn about Z) of the ring's displacement. No SolidWorks."""
import numpy as np
from pathlib import Path
import types
HERE = Path(__file__).resolve().parent
WIP = HERE.parents[1] / '_wip' / 'sw-eval' / 'haiku-plan-d'
z = np.load(WIP / 'npz' / 'D2_X_30.npz')
p, d = z['pos'], z['disp']
rho = np.hypot(p[:, 0], p[:, 1])
ring = (rho >= 23.99) & (rho <= 26.0005) & (p[:, 2] > -0.001) & (p[:, 2] < 7.001)
x, y = p[ring, 0], p[ring, 1]
u = d[ring, 1:4]
n = ring.sum()
A = np.zeros((2 * n, 3)); b = np.zeros(2 * n)
A[0::2, 0] = 1; A[1::2, 1] = 1
A[0::2, 2] = -y; A[1::2, 2] = x
b[0::2] = u[:, 0]; b[1::2] = u[:, 1]
sol, *_ = np.linalg.lstsq(A, b, rcond=None)
res = b - A @ sol
rx, ry = res[0::2], res[1::2]
rr = np.hypot(rx, ry)
print('rigid fit: translation (mm)', sol[:2], 'turn about Z (rad)', sol[2], 'deg', np.degrees(sol[2]))
print('residual after rigid fit: max', float(rr.max()), 'mean', float(rr.mean()), 'rms', float(np.sqrt((rr**2).mean())))
print('ring |u| max', float(np.hypot(u[:,0],u[:,1]).max()), 'uz range', float(u[:,2].min()), float(u[:,2].max()))
print('ring max |u| total', float(d[ring,4].max()))
