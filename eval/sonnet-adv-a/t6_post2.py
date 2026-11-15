"""T6 post-processing v2: bodies split by node-id run (the mesh numbers each body's nodes in one unbroken run), checked against geometry.
Recomputes peak bearing, half-width, block von Mises, peak location and pin translation with the labels, and reports how many nodes the
radius band of t6_post.py had put in the wrong body."""
import json
import numpy as np
from scipy.spatial import cKDTree
from common import *

SIM = WIP / 'sim'
out = {}
FILES = [p.stem for p in sorted(SIM.glob('T6_*.npz')) if 'proof_0.001_load_ctrl0.8' not in p.stem or '_E_' in p.stem]
FILES = [f for f in FILES if f != 'T6_D_full_load_ctrl0.55']
for f in FILES:
    tag = f
    ZC = 10.0 if '_E_' in f else 10.102
    d = np.load(SIM / f'{f}.npz')
    pos, s, disp = d['pos'], d['s'], d['disp']
    ids = s[:, 0].astype(int)
    dmap = {int(k): i for i, k in enumerate(disp[:, 0])}
    uz = np.array([disp[dmap[k], 3] for k in ids])
    rp = np.hypot(pos[:, 0], pos[:, 2] - ZC)
    yy = pos[:, 1]
    sure = {'block': (np.abs(yy) <= 15.001) & ((pos[:, 2] < 4.5) | (np.abs(pos[:, 0]) > 6.5) | (pos[:, 2] > 16.5)),
            'pin_c': (np.abs(yy) <= 14.9) & (rp < 4.5),
            'stubs': (np.abs(yy) > 15.1) & (np.abs(yy) <= 24.9) & (rp < 4.5),
            'pads': np.abs(yy) > 25.5}
    bounds = {k: (int(ids[m].min()), int(ids[m].max())) for k, m in sure.items()}
    runs = {}
    for k, (lo, hi) in bounds.items():
        runs[k] = (ids >= lo) & (ids <= hi)
    overlap = int(sum(((runs[a] & runs[b]).sum()) for i, a in enumerate(runs) for b in list(runs)[i + 1:]))
    # check that every sure node lies in its own run and in no other
    chk = {k: int((~runs[k][sure[k]]).sum()) for k in sure}
    chk['sure_nodes_in_another_body_run'] = int(sum((runs[a][sure[k]]).sum() for k in sure for a in runs if a != k))
    is_blk, is_pinc = runs['block'], runs['pin_c']
    if '_E_' in f:      # concentric: the pin surface (r 5.0) and the hole wall (r 5.1) are 0.1 mm apart, so radius alone separates them
        is_blk = (np.hypot(pos[:, 0], pos[:, 2] - 10.0) >= 5.09) | (np.abs(yy) <= 15.001) & ((pos[:, 2] < 4.5) | (np.abs(pos[:, 0]) > 6.5) | (pos[:, 2] > 16.5))
        is_blk &= np.abs(yy) <= 15.001
        is_pinc = (np.hypot(pos[:, 0], pos[:, 2] - 10.0) <= 5.0005) & (np.abs(yy) <= 15.001)
    ok_runs = overlap == 0 and chk['sure_nodes_in_another_body_run'] == 0 and all(chk[k] == 0 for k in sure)
    pin_hi, blk_lo, pad_lo = bounds['pin_c'][1], bounds['block'][0], bounds['pads'][0]
    rad = np.hypot(pos[:, 0], pos[:, 2] - 10.0)
    ang = np.arctan2(pos[:, 2] - 10.0, pos[:, 0])
    ux, uzz = np.cos(ang), np.sin(ang)
    p = -(s[:, 1] * ux ** 2 + s[:, 3] * uzz ** 2 + 2 * s[:, 5] * ux * uzz)
    band = (rad >= 5.09) & (rad <= 5.12) & (np.abs(yy) <= 15.001) & (np.abs(pos[:, 0]) <= 6.0)
    band_pin = band & is_pinc
    band_blk = band & is_blk
    wrong = int(band_pin.sum())
    # peak bearing on the block's hole surface: block nodes, hole radius (5.1 from the hole axis) at the crown within the band
    hole = band_blk
    idx = np.flatnonzero(hole)
    tree = cKDTree(pos[idx])
    res = dict(nodes_in_old_band=int(band.sum()), old_band_nodes_that_are_pin=wrong, runs_ok=bool(ok_runs), checks=chk,
               run_bounds=bounds, run_overlap_nodes=overlap)
    for w in (0.5, 1.0, 2.0):
        nb = tree.query_ball_point(pos[idx], w)
        sm = np.array([p[idx][n].mean() for n in nb])
        k = int(np.argmax(sm))
        res[f'smoothed_{w}mm'] = dict(peak_mpa=round(float(sm[k]), 3), at=pos[idx][k].round(2).tolist(), n=len(nb[k]))
    res['raw_peak_mpa'] = round(float(p[idx].max()), 3)
    res['raw_p99_mpa'] = round(float(np.percentile(p[idx], 99)), 3)
    pk = hole & (p > 0.5)
    res['patch_x_range_over_0.5mpa'] = [round(float(pos[pk, 0].min()), 2), round(float(pos[pk, 0].max()), 2)] if pk.any() else None
    res['half_width_mm'] = round(float((pos[pk, 0].max() - pos[pk, 0].min()) / 2), 2) if pk.any() else None
    vm = s[:, 10]
    near = is_blk & (rad >= 5.09) & (rad <= 7.0) & (np.abs(yy) <= 15.001) & (np.abs(pos[:, 0]) <= 8.0)
    ni = np.flatnonzero(near)
    nbv = cKDTree(pos[ni]).query_ball_point(pos[ni], 1.0)
    smv = np.array([vm[ni][n].mean() for n in nbv])
    kk = int(np.argmax(smv))
    res['block_vm_raw_max'] = dict(mpa=round(float(vm[ni].max()), 3), at=pos[ni][int(np.argmax(vm[ni]))].round(2).tolist())
    res['block_vm_smoothed_1mm'] = dict(mpa=round(float(smv[kk]), 3), at=pos[ni][kk].round(2).tolist())
    pn = np.flatnonzero(is_pinc)
    res['pin_centre_mean_uz_mm'] = round(float(uz[pn].mean()), 5)
    res['pin_centre_uz_min_max'] = [round(float(uz[pn].min()), 4), round(float(uz[pn].max()), 4)]
    res['pin_vm_max'] = round(float(vm[pn].max()), 3)
    # the block's own displacement at the crown (nodes on the hole wall, top): how far the roof of the hole rose
    top = band_blk & (pos[:, 2] > 14.5) & (np.abs(pos[:, 0]) < 1.0)
    res['block_crown_mean_uz_mm'] = round(float(uz[top].mean()), 5) if top.any() else None
    top_pin = is_pinc & (rp > 4.9) & (pos[:, 2] > 14.5) & (np.abs(pos[:, 0]) < 1.0)
    res['pin_crown_mean_uz_mm'] = round(float(uz[top_pin].mean()), 5) if top_pin.any() else None
    # full-width mean of sigma_z on the block bottom? (not needed) ; contact force check from the labelled pressure
    out[tag] = res
    print(tag, json.dumps({k: v for k, v in res.items() if k not in ('checks', 'run_bounds')}))
    print('   ', res['checks'], res['run_bounds'], 'runs_ok', ok_runs)
(RUN / 't6_post2.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
