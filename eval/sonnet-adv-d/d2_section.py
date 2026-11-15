"""Section force through the lower half: integral of sigma_y over a cut plane Y = y0 (nodes of the slab, Delaunay in X-Z, long triangles dropped)."""
import sys
import numpy as np
from scipy.spatial import Delaunay
sys.path.insert(0, 'eval/sonnet-adv-d')
from d2_masks import masks
def section_force(npz, y0, half=0.8, maxedge=6.0, body='lower'):
    z = np.load(npz); pos, s = z['pos'], z['s']; m = masks(pos)
    sel = m[body] & (np.abs(pos[:, 1] - y0) <= half)
    P = pos[sel][:, [0, 2]]; sy = s[sel, 2]; sxy = s[sel, 4]; syz = s[sel, 6]
    tri = Delaunay(P).simplices
    a, b, c = P[tri[:, 0]], P[tri[:, 1]], P[tri[:, 2]]
    e = np.stack([np.linalg.norm(a - b, axis=1), np.linalg.norm(b - c, axis=1), np.linalg.norm(c - a, axis=1)], 1).max(1)
    area = 0.5 * np.abs((b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (c[:, 0] - a[:, 0]) * (b[:, 1] - a[:, 1]))
    ok = e <= maxedge
    f = lambda v: float((area[ok] * v[tri[ok]].mean(axis=1)).sum())
    return dict(Fy=f(sy), Fx=f(sxy), Fz=f(syz), area=float(area[ok].sum()), nodes=int(sel.sum()))
if __name__ == '__main__':
    for el in sys.argv[2:]:
        for y0 in (-30.0, -22.0, -15.0, -12.0):
            print(el, y0, section_force(f'_wip/sw-eval/sonnet-adv-d/d2/npz/a_{sys.argv[1]}_{el}.npz', y0))
