"""D1 pre-check: can the board with its parts (a 60 x 18.6 rectangle seen along X: 3 below, 1.6 board, 14 above) lie in
the allowed region Y -25..25, Z <= 45, minus the rail (|Y|<10, Z<0)? Brute force over tilt and position (mm, deg)."""
import numpy as np, itertools
W, T_BELOW, T_BOARD, T_ABOVE = 60.0, 3.0, 1.6, 14.0
def rect(theta, cy, cz, below=T_BELOW, above=T_ABOVE, board=T_BOARD):
    th = np.radians(theta); u = np.array([np.cos(th), np.sin(th)]); n = np.array([-np.sin(th), np.cos(th)])
    pts = []
    for s in np.linspace(-W/2, W/2, 25):
        for t in np.linspace(-below, board+above, 12):
            pts.append(np.array([cy, cz]) + s*u + t*n)
    return np.array(pts)
def viol(p, zmax=45.0, ymax=25.0, rail=True):
    v = np.maximum(p[:,1]-zmax, 0) + np.maximum(np.abs(p[:,0])-ymax, 0)
    if rail:   # inside rail box |Y|<10, Z<0: distance to leave it
        inside = (np.abs(p[:,0])<10)&(p[:,1]<0)
        d = np.minimum(10-np.abs(p[:,0]), -p[:,1])
        v = v + np.where(inside, d, 0)
    return v.max()
for label, kw in (('region incl. dip beside rail', dict(rail=True)), ('above rail top only (Z>=0)', dict(rail=False))):
    best = (1e9,)
    for th in range(0, 181, 3):
        for cy in np.arange(-25, 25.1, 1.0):
            for cz in np.arange(-15, 46, 1.0):
                p = rect(th, cy, cz)
                v = viol(p, **kw)
                if kw['rail'] is False: v = max(v, (0 - p[:,1].min()) if p[:,1].min()<0 else 0)
                if v < best[0]: best = (v, th, cy, cz)
    print(label, 'least worst overshoot %.1f mm at tilt %d deg, centre Y %.0f Z %.0f' % best)
# bare board only (no parts): fits?
for th in (40,45,50):
    p = rect(th,0,0,below=0,above=0,board=1.6); print('bare board tilt',th,'Y span %.1f Z span %.1f' % (np.ptp(p[:,0]), np.ptp(p[:,1])))
