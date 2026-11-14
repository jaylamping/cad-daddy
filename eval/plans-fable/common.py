"""Shared code for the plans in this folder. Copy this file to eval/<run>/common.py and import it in every script:

    from common import *

WRITTEN BY THE PLANNER WITHOUT SOLIDWORKS. The numpy parts (stl_stats, measures, mask helpers) were run on Linux
against made-up data; the parts that touch SolidWorks (tree, holes, check_export) were not run at all. If one of them
raises on its first use, fix the line that raises (the helper calls are from swkit.py / swfea.py as read on
2026-11-14) and note the fix in REPORT.md. Do not work round a failure by deleting a check.
"""
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent            # eval/<run>/
ROOT = HERE.parents[1]                            # the worktree root
sys.path.insert(0, str(ROOT / 'solidworks'))
from swkit import *      # noqa: E402,F401,F403
from swfea import *      # noqa: E402,F401,F403
import sheet             # noqa: E402

RUN = HERE.name
WIP = ROOT / '_wip' / 'sw-eval' / RUN             # models, exports, npz (gitignored)
PICS = HERE / 'pictures'
T0 = time.time()

SOFT = dict(name='Soft pad', EX=0.5e6, NUXY=0.45, DENS=1000.0, SIGYLD=1e6, SIGXT=1e6)      # as selftest.contact()
PRESS = dict(name='Pressure pad', EX=50e6, NUXY=0.45, DENS=1000.0, SIGYLD=1e6, SIGXT=1e6)  # 2.6 % of PETG: spreads a load, adds no stiffness
DENS_G_MM3 = 1.19e-3
ALLOW = dict(vm=45.0, layer=22.5, shear=13.0)     # MPa, playbook/05-fea.md "Before SolidWorks"


def minutes():
    return round((time.time() - T0) / 60, 1)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def put(task, **kv):
    """Merge keys into results.json under the task's name (utf-8, numbers as numbers)."""
    f = HERE / 'results.json'
    data = json.loads(f.read_text(encoding='utf-8')) if f.exists() else {}
    data.setdefault(task, {}).update(kv)
    f.write_text(json.dumps(data, indent=1, default=float), encoding='utf-8')
    log('results.json', task, sorted(kv))


def report(text):
    """Append to REPORT.md at once, so a crash later loses nothing."""
    with open(HERE / 'REPORT.md', 'a', encoding='utf-8') as f:
        f.write(text.rstrip() + '\n\n')


# ---- STL checks without trimesh --------------------------------------------------------------------------------------

def stl_stats(path):
    """dict(volume mm3, bounds [x0, y0, z0, x1, y1, z1], watertight, shells, triangles) of an STL."""
    t = sheet.read_stl(path)
    vol = float(np.einsum('ij,ij->i', t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6.0)
    v, vid = np.unique(np.round(t.reshape(-1, 3), 4), axis=0, return_inverse=True)
    f = vid.reshape(-1, 3)
    e = np.sort(np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]]), axis=1)
    _, counts = np.unique(e, axis=0, return_counts=True)
    parent = np.arange(len(v))                    # shells: union-find over the vertices

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for a, b in np.unique(e, axis=0):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    shells = len({find(a) for a in range(len(v))})
    lo, hi = t.reshape(-1, 3).min(axis=0), t.reshape(-1, 3).max(axis=0)
    return dict(volume=abs(vol), bounds=[round(float(x), 3) for x in list(lo) + list(hi)],
                watertight=bool((counts == 2).all()), shells=shells, triangles=len(t))


def check_export(d, stl, step=None):
    """playbook/04-export.md: watertight, one shell per body, volume within 0.5 %, box within 0.1 mm, STEP in mm."""
    st = stl_stats(stl)
    expect('STL watertight', float(st['watertight']), 1.0, 0)
    expect('STL shells', st['shells'], len(bodies(d)), 0)
    expect('STL volume', st['volume'], volume(d), 0.005)
    for a, b in zip(st['bounds'], bbox(d)):
        expect('STL box', a, b, 0.1)
    if step is not None:
        text = Path(step).read_text(errors='ignore')
        if not any('SI_UNIT' in ln and '.MILLI.' in ln for ln in text.splitlines()):
            raise Failed(f'{step}: no SI_UNIT line with .MILLI. (not in millimetres?)')
        log('ok STEP is in mm')
    return st


# ---- model checks ----------------------------------------------------------------------------------------------------

def tree(d):
    """[(feature name, type, id)] in tree order: log it before and after an edit to prove the part was edited."""
    out, f = [], d.FirstFeature
    while f is not None:
        try:
            fid = int(call(f, 'GetID'))
        except Exception as ex:      # noqa: BLE001 - logged; names and types still prove the edit
            log('GetID not read:', str(ex)[:60])
            fid = None
        out.append((f.Name, f.GetTypeName2, fid))
        f = f.GetNextFeature
    return out


def holes(d, r, inside=None):
    """[(radius, [centre x, y, z of the face's box], box)] for every cylindrical face of radius r: where each hole IS."""
    out = []
    for f in pick(d, kind='cyl', r=r, inside=inside):
        i = face_info(f)
        b = i['box']
        out.append((round(i['r'], 3), [round((b[k] + b[k + 3]) / 2, 3) for k in range(3)], [round(x, 3) for x in b]))
    return sorted(out, key=lambda h: h[1])


def must(what, got, want):
    """A count that has to be exact (faces picked, edges found, bodies). Prints the faces when it is not."""
    if got != want:
        raise Failed(f'{what}: got {got}, expected {want}. Run list_faces(d) and read the boxes before changing anything.')
    log(f'ok {what}: {got}')


# ---- study results ---------------------------------------------------------------------------------------------------

def measures(r, mask, normal):
    """The three failure measures over the nodes in mask, for layers stacked along normal, each with place and factor."""
    if not mask.any():
        raise Failed(f'{r.name}: empty mask')
    vm, at = r.peak(mask)
    lt, lat = r.layer_stress(normal, mask)
    ls, sat = r.layer_shear(normal, mask)
    return dict(vm=round(vm, 2), vm_at=at, sf_yield=round(ALLOW['vm'] / vm, 2),
                layer=round(lt, 2), layer_at=lat, sf_layer=round(ALLOW['layer'] / lt, 2) if lt > 0.01 else 999.0,
                shear=round(ls, 2), shear_at=sat, sf_shear=round(ALLOW['shear'] / ls, 2) if ls > 0.01 else 999.0)


def direction_table(r, mask):
    """{'X' | 'Y' | 'Z': measures()} : the print-direction table of playbook/07-done.md, study item 5."""
    return {k: measures(r, mask, n) for k, n in (('X', (1, 0, 0)), ('Y', (0, 1, 0)), ('Z', (0, 0, 1)))}


def sf_min(m):
    return min(m['sf_yield'], m['sf_layer'], m['sf_shear'])


def settled(rows, keys=('vm', 'layer', 'shear'), tol=0.05):
    """True when the last two rows (dicts from measures()) agree within tol on every key. Needs three rows."""
    if len(rows) < 3:
        return False
    a, b = rows[-1], rows[-2]
    return all(abs(a[k] - b[k]) <= tol * max(abs(b[k]), 1e-9) for k in keys)


def save_npz(r, name):
    (WIP / 'npz').mkdir(parents=True, exist_ok=True)
    np.savez(WIP / 'npz' / f'{name}.npz', pos=r.pos, s=r.s, disp=r.disp if r.disp is not None else np.zeros((0, 5)),
             reaction=np.array(r.reaction if r.reaction is not None else [np.nan] * 4), nodes=r.nodes, el=r.el)


def near_axis(pos, axis, a, b):
    """Distance of every node from a line parallel to model axis 'X', 'Y' or 'Z' through the other two coordinates a, b
    (in the order x, y, z with the axis left out)."""
    i, k = [n for n in range(3) if n != 'XYZ'.index(axis)]
    return np.hypot(pos[:, i] - a, pos[:, k] - b)


def predict(name, nodes, disp, where):
    log(f'PREDICT {name}: nodes {nodes}, max displacement {disp} mm, peak expected at {where}')


def compare(name, r, nodes, disp):
    """playbook/07-done.md "Predict, then run": stop when the solve is not the one that was predicted."""
    got = r.max_disp()
    log(f'COMPARE {name}: nodes {r.nodes} (predicted {nodes}), max displacement {got} (predicted {disp})')
    if not (nodes / 2 <= r.nodes <= nodes * 2):
        log(f'NOTE {name}: node count is more than 2x off the prediction. Read the fixture and load boxes static() logged.')
        return False
    if got is None or not (disp / 3 <= got <= disp * 3):
        log(f'STOP {name}: displacement is more than 3x off the prediction. Do not read the stresses yet.')
        return False
    return True
