"""T6 post-processing from the saved nodal results: smoothed contact pressure on the hole wall, patch width, pressure along y."""
import json, sys
import numpy as np
from scipy.spatial import cKDTree
from common import *

SIM = WIP / 'sim'
out = {}
for f in sorted(SIM.glob('T6_*.npz')):
    d = np.load(f)
    pos, s = d['pos'], d['s']
    rad = np.hypot(pos[:, 0], pos[:, 2] - 10.0)
    ang = np.arctan2(pos[:, 2] - 10.0, pos[:, 0])
    ux, uz = np.cos(ang), np.sin(ang)
    srr = s[:, 1] * ux ** 2 + s[:, 3] * uz ** 2 + 2 * s[:, 5] * ux * uz
    p = -srr
    hole = (rad >= 5.09) & (rad <= 5.12) & (np.abs(pos[:, 1]) <= 15.001) & (np.abs(pos[:, 0]) <= 6.0)
    idx = np.flatnonzero(hole)
    tree = cKDTree(pos[idx])
    res = {}
    for w in (0.5, 1.0, 2.0):
        nb = tree.query_ball_point(pos[idx], w)
        sm = np.array([p[idx][n].mean() for n in nb])
        k = int(np.argmax(sm))
        res[f'smoothed_{w}mm'] = dict(peak_mpa=round(float(sm[k]), 3), at=pos[idx][k].round(2).tolist(), n=len(nb[k]))
    res['raw_peak_mpa'] = round(float(p[idx].max()), 3)
    res['raw_p99_mpa'] = round(float(np.percentile(p[idx], 99)), 3)
    # profile across the crown: mean over y in 0 +- 10, by x slice
    prof = []
    for x0 in np.arange(-3.0, 3.01, 0.5):
        m = hole & (np.abs(pos[:, 0] - x0) < 0.25) & (pos[:, 2] > 10) & (np.abs(pos[:, 1]) < 10)
        prof.append([float(x0), round(float(p[m].mean()), 3) if m.any() else None, int(m.sum())])
    res['x_profile_mean_over_y(+-10)'] = prof
    # profile along y at |x| < 1
    prof = []
    for y0 in np.arange(-15, 15.01, 2.5):
        m = hole & (np.abs(pos[:, 1] - y0) < 1.25) & (np.abs(pos[:, 0]) < 1.0) & (pos[:, 2] > 10)
        prof.append([float(y0), round(float(p[m].mean()), 3) if m.any() else None, int(m.sum())])
    res['y_profile_crown(|x|<1)'] = prof
    # the force carried: integrate nodal p over the patch using a Delaunay-free estimate: mean p x projected area of the patch nodes
    pk = hole & (p > 0.5)
    res['patch_nodes_over_0.5mpa'] = int(pk.sum())
    res['patch_x_range_over_0.5mpa'] = [round(float(pos[pk, 0].min()), 2), round(float(pos[pk, 0].max()), 2)] if pk.any() else None
    vm = s[:, 10]
    blk = (rad >= 5.09) & (rad <= 7.0) & (np.abs(pos[:, 1]) <= 15.001) & (np.abs(pos[:, 0]) <= 8.0)
    nbv = cKDTree(pos[np.flatnonzero(blk)]).query_ball_point(pos[np.flatnonzero(blk)], 1.0)
    smv = np.array([vm[blk][n].mean() for n in nbv])
    kk = int(np.argmax(smv))
    res['vm_block_smoothed_1mm'] = dict(peak_mpa=round(float(smv[kk]), 3), at=pos[blk][kk].round(2).tolist())
    res['vm_block_raw_max'] = round(float(vm[blk].max()), 3)
    out[f.stem] = res
    print(f.stem, json.dumps({k: v for k, v in res.items() if 'profile' not in k}))
(RUN / 't6_post.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
