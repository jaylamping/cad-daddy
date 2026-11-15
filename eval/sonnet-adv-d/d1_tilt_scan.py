"""D1: least worst overshoot (mm) of the 60 x 18.6 stack vs tilt, region |Y|<=25, Z<=45, outside the rail box (|Y|<10, Z<0).
Coarse but vectorised. Tilt 0 = lying flat (60 along Y), 90 = on edge (60 along Z). Stack: 3 below, 1.6 board, 14 above."""
import numpy as np
s = np.linspace(-30, 30, 13); t = np.linspace(-3, 15.6, 7)
S, Tt = np.meshgrid(s, t); S, Tt = S.ravel(), Tt.ravel()
for th in range(0, 91, 10):
    r = np.radians(th); u = np.array([np.cos(r), np.sin(r)]); n = np.array([-np.sin(r), np.cos(r)])
    best = (1e9,)
    for sign in (1, -1):       # tall side facing -Y or +Y
        nn = n * sign
        for cy in np.arange(-26, 26.1, 1.0):
            for cz in np.arange(-15, 46, 1.0):
                P = np.c_[cy + S*u[0] + Tt*nn[0], cz + S*u[1] + Tt*nn[1]]
                y, z = P[:, 0], P[:, 1]
                v = np.maximum(z-45, 0) + np.maximum(np.abs(y)-25, 0)
                ins = (np.abs(y) < 10) & (z < 0)
                v = v + np.where(ins, np.minimum(10-np.abs(y), -z), 0)
                m = v.max()
                if m < best[0]: best = (m, sign, cy, cz)
    print('tilt', th, 'least worst overshoot %.1f (tall side sign %d, centre Y %.0f Z %.0f)' % best, flush=True)
