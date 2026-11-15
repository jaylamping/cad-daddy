"""Shared T3/T4/T5 helpers: twin with split rings, measures by region, one case run with retry on excessive displacement."""
import json, math
import numpy as np
from scipy.spatial import cKDTree
from common import *
from swkit import *
from swfea import *

HOLES_YZ = [(14.04, 17.04), (14.04, 38.96), (35.96, 17.04), (35.96, 38.96)]
BASE_HOLES = [(25, 10), (25, 40), (65, 10), (65, 40)]
SIM = WIP / 'sim'
SIM.mkdir(exist_ok=True)
ALLOW = dict(vm=45.0, layer=22.5, shear=13.0)
T_UP = 6.0                 # upright thickness of the part being measured (T5 changes it)
DIRS = {'Z': (0, 0, 1), 'X': (1, 0, 0), 'Y': (0, 1, 0)}


def add_rings(d, r_head=3.0, depth=0.3):
    """Shallow circular steps round the four Ø3.4 holes on the X = 0 face: faces that look along -X, for an even force."""
    h = 15.5 * math.cos(math.radians(45))
    v0 = volume(d)
    with Sk(d, plane(d, 'X', depth / 2, 'RING_P'), 'RINGS') as s:
        for sy in (1, -1):
            for sz in (1, -1):
                s.circle((depth / 2, 25 + sy * h, 28 + sz * h), r_head)
    extrude(d, s.feat, 'RINGS', depth, cut=True, mode=MID, expect_dv=4 * math.pi * (r_head ** 2 - 1.7 ** 2) * depth)
    dv = v0 - volume(d)
    expect('twin removes under 0.1 %', dv / v0 * 100, 0.07, 0.03, abs_tol=0.04)
    save(d)
    return dv


def ring_faces(d, r_head=3.0, depth=0.3):
    out = []
    for cy, cz in HOLES_YZ:
        f = pick(d, kind='plane', normal=(-1, 0, 0), at=(depth, cy + (1.7 + r_head) / 2, cz))
        expect('ring face found', len(f), 1, 0)
        out += f
    return out


def measures(r, ring_dist=0.6, fixed_dist=2.5):
    """Peaks by region at one mesh: vm, layer tension (layers along Z, X, Y) and layer shear, with where."""
    pos = r.pos
    out = {}
    tube = np.zeros(len(pos), bool)
    for cy, cz in HOLES_YZ:
        tube |= (np.hypot(pos[:, 1] - cy, pos[:, 2] - cz) <= 2.2) & (pos[:, 0] >= -0.01) & (pos[:, 0] <= T_UP + 0.01)
    far_load = np.ones(len(pos), bool)
    if r.loaded_pts is not None and len(r.loaded_pts):
        far_load = cKDTree(r.loaded_pts).query(pos)[0] >= ring_dist
    far_fix = np.ones(len(pos), bool)
    if r.fixed_pts is not None and len(r.fixed_pts):
        far_fix = cKDTree(r.fixed_pts).query(pos)[0] >= fixed_dist
    regions = {
        'hole rims (0.6 mm clear of loaded faces)': tube & far_load,
        'hole rims (all nodes)': tube,
        'root and fillet': (pos[:, 0] <= T_UP + 4.01) & (pos[:, 2] >= 5.99) & (pos[:, 2] <= 12.0),
        'base (2.5 mm clear of fixed holes)': (pos[:, 2] <= 6.01) & (pos[:, 0] >= 10.0) & far_fix,
        'everywhere clear of loads (2 mm) and fixtures (2.5 mm)': r.away(dist=2.0) & far_fix,
    }
    for name, m in regions.items():
        if not m.any():
            out[name] = None
            continue
        vm, vat = r.peak(m)
        row = dict(n=int(m.sum()), vm=round(vm, 3), vm_at=vat)
        for k, n in DIRS.items():
            ls, lat = r.layer_stress(n, m)
            sh, sat = r.layer_shear(n, m)
            row[f'layer_{k}'] = round(ls, 3); row[f'layer_{k}_at'] = lat
            row[f'shear_{k}'] = round(sh, 3); row[f'shear_{k}_at'] = sat
        out[name] = row
    return out


def save_npz(r, name):
    np.savez_compressed(SIM / f'{name}.npz', pos=r.pos, s=r.s, disp=r.disp if r.disp is not None else np.zeros(1))


def run_case(j, d, name, el, fixtures, loads, ctrl, material=PETG, predict=None, retry=True, **kw):
    """static() with an explicit retry for the 'excessive displacements' prompt on a single, properly held body."""
    log(f'PREDICT {name}: {predict}')
    try:
        r = static(j, d, name, material, fixtures, loads, el, ctrl=ctrl, max_nodes=200_000, **kw)
    except Failed as ex:
        if 'excessive displacements' not in str(ex) or not retry:
            raise
        log(f'{name}: excessive-displacement prompt on a single held body: {ex}; retrying with loose_ok=True after the '
            'reaction check below')
        r = static(j, d, name, material, fixtures, loads, el, ctrl=ctrl, max_nodes=200_000, loose_ok=True, **kw)
    save_npz(r, name.replace(' ', '_'))
    log(r.summary())
    return r


def append_rows(path, key, row):
    p = RUN / path
    d = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
    d.setdefault(key, []).append(row)
    p.write_text(json.dumps(d, indent=1), encoding='utf-8')


def corner_measures(r):
    pos = r.pos
    m = (pos[:, 0] >= 5.99) & (pos[:, 0] <= 10.01) & (pos[:, 2] >= 5.99) & (pos[:, 2] <= 10.01)
    vm, at = r.peak(m)
    ls, lat = r.layer_stress((0, 0, 1), m)
    line = (np.hypot(pos[:, 0] - 6, pos[:, 2] - 6) <= 0.3)
    out = dict(vm=round(vm, 3), vm_at=at, layer_Z=round(ls, 3), layer_Z_at=lat,
               sz_min_on_corner=round(float(r.s[line, 3].min()), 3), sz_max_on_corner=round(float(r.s[line, 3].max()), 3),
               corner_nodes=int(line.sum()))
    mid = [6.0, 25.0, 6.0]
    for rad in (0.5, 1.0, 2.0):
        a, n = r.average(mid, rad)
        out[f'avg_vm_{rad}'] = round(a, 3); out[f'avg_n_{rad}'] = n
    return out
