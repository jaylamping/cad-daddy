"""Read the bore wall (the 2.8 mm ligament between the bore and the O3.4 holes) from saved nodal results: nodes within 0.5 mm of the O22 wall."""
import json
import numpy as np
from common import *

def measures(s, pos, mask):
    out = {}
    vm = s[:, 10]
    i = np.flatnonzero(mask)[np.argmax(vm[mask])]
    out['vm'] = (round(float(vm[i]), 3), pos[i].round(2).tolist())
    for nm, n in (('Z', (0, 0, 1)), ('X', (1, 0, 0)), ('Y', (0, 1, 0))):
        n = np.array(n, float)
        sn = (n[0] ** 2 * s[:, 1] + n[1] ** 2 * s[:, 2] + n[2] ** 2 * s[:, 3] + 2 * (n[0] * n[1] * s[:, 4] + n[0] * n[2] * s[:, 5] + n[1] * n[2] * s[:, 6]))
        j = np.flatnonzero(mask)[np.argmax(sn[mask])]
        t = np.c_[s[:, 1] * n[0] + s[:, 4] * n[1] + s[:, 5] * n[2], s[:, 4] * n[0] + s[:, 2] * n[1] + s[:, 6] * n[2], s[:, 5] * n[0] + s[:, 6] * n[1] + s[:, 3] * n[2]]
        tau = np.linalg.norm(t - np.outer(t @ n, n), axis=1)
        k = np.flatnonzero(mask)[np.argmax(tau[mask])]
        out[f'layer_{nm}'] = (round(float(sn[j]), 3), pos[j].round(2).tolist())
        out[f'shear_{nm}'] = (round(float(tau[k]), 3), pos[k].round(2).tolist())
    return out

res = {}
for tag, f, tup in (('T3 el1.6 (6 mm upright)', 'T3_RINGS_el1.6', 6.0), ('T3 el2.2 (6 mm upright)', 'T3_RINGS_el2.2', 6.0), ('T3 el3.0 (6 mm upright)', 'T3_RINGS_el3.0', 6.0),
                    ('T5 final el1.6 (7.5 mm upright)', 'T5_C_el1.6', 7.5), ('T5 final el2.2', 'T5_C_el2.2', 7.5), ('T5 final el3.0', 'T5_C_el3.0', 7.5)):
    d = np.load(WIP / 'sim' / f'{f}.npz')
    pos, s = d['pos'], d['s']
    rb = np.hypot(pos[:, 1] - 25.0, pos[:, 2] - 28.0)
    wall = (rb <= 11.5) & (rb >= 10.99) & (pos[:, 0] >= -0.01) & (pos[:, 0] <= tup + 0.01)
    # the part of the wall facing a small hole: within 2.5 mm of a small-hole axis line
    near_h = np.zeros(len(pos), bool)
    for cy, cz in ((14.04, 17.04), (14.04, 38.96), (35.96, 17.04), (35.96, 38.96)):
        near_h |= np.hypot(pos[:, 1] - cy, pos[:, 2] - cz) <= 5.0
    res[tag] = dict(n_wall=int(wall.sum()), all_wall=measures(s, pos, wall), facing_small_holes=measures(s, pos, wall & near_h))
    print(tag, json.dumps(res[tag]))
(RUN / 'bore_wall.json').write_text(json.dumps(res, indent=1), encoding='utf-8')
