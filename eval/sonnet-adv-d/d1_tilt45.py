"""D1: at tilt 45 and 40 deg (board 60 edge rising towards +Y), where must the stack go, and by how much does it overshoot?"""
import numpy as np
s = np.linspace(-30, 30, 25); t = np.linspace(-3, 15.6, 11)
S, Tt = np.meshgrid(s, t); S, Tt = S.ravel(), Tt.ravel()
for th in (35, 40, 45):
    r = np.radians(th); u = np.array([np.cos(r), np.sin(r)]); n = np.array([-np.sin(r), np.cos(r)])   # n: tall side faces -Y and up
    best = (1e9,)
    for cy in np.arange(-12, 12.1, 0.5):
        for cz in np.arange(0, 40.1, 0.5):
            P = np.c_[cy + S*u[0] + Tt*n[0], cz + S*u[1] + Tt*n[1]]
            y, z = P[:, 0], P[:, 1]
            oy = np.maximum(np.abs(y)-25, 0).max(); oz = max((z-45).max(), 0)
            ins = (np.abs(y) < 10) & (z < 0); orail = np.where(ins, np.minimum(10-np.abs(y), -z), 0).max()
            m = max(oy, oz, orail)
            if m < best[0]: best = (m, cy, cz, oy, oz, orail, y.min(), y.max(), z.min(), z.max())
    print('tilt', th, 'worst %.1f at centre Y %.1f Z %.1f | over Y %.1f Z %.1f rail %.1f | Y %.1f..%.1f Z %.1f..%.1f' % best)
