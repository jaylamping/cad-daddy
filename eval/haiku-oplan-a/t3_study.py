"""T3: static study of the T1 bracket (eval/TASKS.md T3), per plans/A_T3.md.

Job A (four studies): converge series (3.0, 2.0, 1.5) on load model B with the hole walls fixed, then the
bottom-face support at 2.0. Job B (two studies): load model A (rigid remote load on the motor-screw holes) at 2.0 and 1.5.
Writes eval/haiku-oplan-a/t3.json; nodal results go to _wip beside the model as .npz.
"""
import json
import sys
import time
import traceback
from pathlib import Path

import numpy as np

sys.path.insert(0, r"J:\code\cad-daddy-wt\sw-eval-haiku-oplan-a\solidworks")
from swkit import *  # noqa: E402,F401,F403
from swfea import *  # noqa: E402,F401,F403

W = Path(r"J:\code\cad-daddy-wt\sw-eval-haiku-oplan-a\_wip\sw-eval\haiku-oplan-a")
E = Path(r"J:\code\cad-daddy-wt\sw-eval-haiku-oplan-a\eval\haiku-oplan-a")
RES = {'task': 'T3', 'status': 'failed', 'notes': [], 'studies': {}}
PRED_NODES = {3.0: 22000, 2.0: 74000, 1.5: 176000}


def solve(j, d, el, fix='holes', load='B'):
    """One study on the open bracket. loaded_pts is cleared so away() masks only the fixture."""
    d.ForceRebuild3(False)                                  # then pick again: faces go stale
    holes = pick(d, kind='cyl', r=1.7)
    fil = pick(d, kind='cyl', r=4.0)
    if len(holes) != 4 or len(fil) != 1:
        raise Failed(f'pick counts holes {len(holes)} fillet {len(fil)}')
    fx = pick(d, kind='cyl', r=2.75) if fix == 'holes' else pick(d, kind='plane', at=(40, 25, 0))
    if not fx:
        raise Failed('empty fixture pick')
    if load == 'B':
        inner = pick(d, kind='plane', normal=(1, 0, 0), at=(6, 25, 44))
        if len(inner) != 1:
            raise Failed(f'load face pick {len(inner)}')
        ld = [('normal', inner, -150.0)]
    else:
        ld = [('remote', holes, (3.0, 25.0, 28.0), (150.0, 0, 0), (0, 0, 0))]
    name = f'T3_{fix}_{load}_{str(el).replace(".", "p")}'
    log(f'{name}: predicted nodes ~{PRED_NODES.get(el, "?")}, max disp ~2.7 mm, peak at lower holes on X 0 face')
    t = time.time()
    r = static(j, d, name, PETG, fixtures=[('fixed', fx)], loads=ld, el=el,
               ctrl=[(holes, 0.3 * el), (fil, 0.4 * el)], loose_ok=True)
    r.loaded_pts = None
    np.savez(W / f'{name}.npz', pos=r.pos, s=r.s, disp=r.disp, reaction=np.array(r.reaction, dtype=float))
    log(f'{name}: solved in {time.time() - t:.0f} s, nodes {r.nodes}, excessive {r.excessive}, reaction {r.reaction}')
    return r


def numbers(r, label):
    """The checks and peaks as numbers, for one study."""
    out = {'label': label, 'nodes': r.nodes, 'el': r.el, 'reaction_N': r.reaction, 'max_disp_mm': r.max_disp(),
           'excessive_displacements_answered_no': bool(r.excessive)}
    vm, at = r.peak()
    out['peak_vm_away_mpa'] = round(vm, 3)
    out['peak_vm_at_mm'] = at
    out['vm_max_all_mpa'] = round(float(r.vm.max()), 3)
    # plain section: upright at the X 0 face, Z 12, Y 3..8, sigma_z = column 3
    m = r.near([(0, y, 12) for y in (3, 4, 5, 6, 7, 8)], 0.6)
    out['plain_sz_mpa'] = round(float(r.s[m, 3].mean()), 3) if m.any() else None
    out['plain_nodes'] = int(m.sum())
    # base between upright and holes, bottom face, sigma_x = column 1
    mb = r.near([(15, 25, 0)], 1.0)
    out['base_sx_mpa'] = round(float(r.s[mb, 1].mean()), 3) if mb.any() else None
    out['base_nodes'] = int(mb.sum())
    # print directions: layers stacked along Z (base on bed), along Y (on its side), along X (on its back)
    dirs = {}
    for label_n, n in (('Z', (0, 0, 1)), ('Y', (0, 1, 0)), ('X', (1, 0, 0))):
        t, tw = r.layer_stress(n)
        s_, sw_ = r.layer_shear(n)
        dirs[label_n] = dict(tension_mpa=round(t, 3), tension_at=tw, shear_mpa=round(s_, 3), shear_at=sw_,
                             sf_layer=round(22.5 / t, 3) if t > 0 else None, sf_shear=round(13.0 / s_, 3))
    out['print_directions'] = dirs
    out['sf_yield'] = round(45.0 / vm, 3)
    # plateau near the fixed hole walls
    out['plateau_vm'] = {str(x): round(r.peak(r.away(dist=x))[0], 3) for x in (1, 2, 3, 5)}
    # small holes read directly: box round the four lower and upper motor-screw holes
    mh = r.in_box([-0.1, 10, 13, 6.1, 40, 21])
    out['holes_box_nodes'] = int(mh.sum())
    if mh.any():
        out['holes_box_vm'] = round(float(r.vm[mh].max()), 3)
        out['holes_box_layer_tension_Z'] = round(r.layer_stress((0, 0, 1), mh)[0], 3)
        out['holes_box_layer_shear_Z'] = round(r.layer_shear((0, 0, 1), mh)[0], 3)
    RES['studies'][label] = out
    log('numbers', label, json.dumps(out, default=str)[:700])
    return out


def job_a(j):
    d = open_doc(j.sw, W / 'bracket.SLDPRT')
    expect('start volume', volume(d), 32974.0, 0.001)
    last = {}

    def run(el):
        r = solve(j, d, el, 'holes', 'B')
        last['r'] = r
        return r
    rows, ok = converge(run, (3.0, 2.0, 1.5), layers=(0, 0, 1))
    RES['convergence_rows'] = rows
    RES['converged'] = bool(ok)
    log('converge rows', rows, 'converged', ok)
    numbers(last['r'], 'B_holes_el1p5')
    r_bot = solve(j, d, 2.0, 'bottom', 'B')
    numbers(r_bot, 'B_bottom_el2')


def job_b(j):
    d = open_doc(j.sw, W / 'bracket.SLDPRT')
    for el in (2.0, 1.5):
        r = solve(j, d, el, 'holes', 'A')
        numbers(r, f'A_holes_el{str(el).replace(".", "p")}')


def main():
    try:
        with job(wait_s=900) as j:
            j.simulation()
            job_a(j)
        with job(wait_s=900) as j:
            j.simulation()
            job_b(j)
        RES['status'] = 'done'
    except Exception as ex:  # noqa: BLE001
        RES['error'] = f'{type(ex).__name__}: {ex}'
        RES['traceback'] = traceback.format_exc()[-2500:]
        log('FAILED', RES['error'])
    finally:
        RES['finished'] = time.strftime('%H:%M:%S')
        (E / 't3.json').write_text(json.dumps(RES, indent=2, ensure_ascii=False, default=str), encoding='utf-8')
        log('wrote t3.json', RES['status'])


if __name__ == '__main__':
    main()
