"""T4: the T1 bracket without the R4 inside fillet (bracket_sharp.SLDPRT), and with a 0.4 mm corner radius
(bracket_r04.SLDPRT). Same T3 load case (model B, holes fixed). Per plans/A_T4.md.

Job 1: bracket_sharp at (3.0, 2.0, 1.5). Job 2: bracket_r04 at (3.0, 2.0, 1.5).
Writes eval/haiku-oplan-a/t4.json.
"""
import json
import math
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
RES = {'task': 'T4', 'status': 'failed', 'notes': [], 'series': {}}
SIZES = (3.0, 2.0, 1.5)
PRED = {3.0: 25000, 2.0: 80000, 1.5: 185000}


def build(j, fname, radius):
    """T1 steps, with the inside corner rounded to `radius` (None = sharp). Volume checked against the hand value."""
    d = new_part(j.sw, W / fname)
    with Sk(d, plane(d, 'Z', 3.0, 'BASE_P'), 'BASE') as s:
        s.rect((0, 0, 3.0), (80, 50, 3.0))
    extrude(d, s.feat, 'BASE', 6.0, mode=MID, expect_dv=24000.0); save(d)
    with Sk(d, plane(d, 'Z', 26.0, 'UPRIGHT_P'), 'UPRIGHT') as s:
        s.rect((0, 0, 26.0), (6, 50, 26.0))
    extrude(d, s.feat, 'UPRIGHT', 40.0, mode=MID, expect_dv=12000.0); save(d)
    if radius is not None:
        e = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01)
        expect('inside corner edges', len(e), 1, 0)
        v0 = volume(d)
        if fillet(d, e, (radius,), 'INSIDE_FILLET') != radius:
            raise Failed(f'fillet R{radius} did not build')
        log('fillet change', round(volume(d) - v0, 3))
        save(d)
    e = edges_where(d, lambda p: (abs(p[0] - 80) < 0.01 and min(abs(p[1]), abs(p[1] - 50)) < 0.01)
                    or (abs(p[2] - 46) < 0.01 and min(abs(p[1]), abs(p[1] - 50)) < 0.01))
    expect('round edges', len(e), 4, 0)
    fillet(d, e, (5.0,), 'CORNER_R5'); save(d)
    with Sk(d, plane(d, 'Z', 3.0, 'BASE_HOLES_P'), 'BASE_HOLES') as s:
        for x, y in ((25, 10), (25, 40), (65, 10), (65, 40)):
            s.circle((x, y, 3.0), 2.75)
    extrude(d, s.feat, 'BASE_HOLES', 8.0, cut=True, mode=MID, expect_dv=570.20); save(d)
    with Sk(d, plane(d, 'X', 3.0, 'BORE_P'), 'BORE') as s:
        s.circle((3.0, 25.0, 28.0), 11.0)
    extrude(d, s.feat, 'BORE', 8.0, cut=True, mode=MID, expect_dv=2280.80); save(d)
    c = 15.5 * math.cos(math.radians(45))
    with Sk(d, plane(d, 'X', 3.0, 'UHOLES_P'), 'UPRIGHT_HOLES') as s:
        for y, z in ((25 - c, 28 - c), (25 + c, 28 - c), (25 + c, 28 + c), (25 - c, 28 + c)):
            s.circle((3.0, y, z), 1.7)
    extrude(d, s.feat, 'UPRIGHT_HOLES', 8.0, cut=True, mode=MID, expect_dv=217.90); save(d)
    single_body(d)
    expect('feature errors empty', len(feature_errors(d)), 0, 0)
    hand = {None: 32802.34, 0.4: 32804.0}[radius]
    expect('volume', volume(d), hand, 0.001)
    RES.setdefault('volumes', {})[str(radius)] = round(volume(d), 3)
    save(d)
    return d


def solve(j, d, el, radius):
    d.ForceRebuild3(False)
    holes = pick(d, kind='cyl', r=1.7)
    if len(holes) != 4:
        raise Failed(f'hole pick {len(holes)}')
    fx = pick(d, kind='cyl', r=2.75)
    if len(fx) != 4:
        raise Failed(f'fixture pick {len(fx)}')
    inner = pick(d, kind='plane', normal=(1, 0, 0), at=(6, 25, 44))
    if len(inner) != 1:
        raise Failed(f'load pick {len(inner)}')
    if radius is None:
        corner = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01)
        if len(corner) != 1:
            raise Failed(f'corner edge pick {len(corner)}')
        ctrl = [(holes, 0.3 * el), (corner, 0.2 * el)]
    else:
        rf = pick(d, kind='cyl', r=radius)
        if len(rf) != 1:
            raise Failed(f'fillet face pick {len(rf)}')
        ctrl = [(holes, 0.3 * el), (rf, 0.1 * el)]
    tag = 'sharp' if radius is None else 'r04'
    name = f'T4_{tag}_{str(el).replace(".", "p")}'
    log(f'{name}: predicted nodes ~{PRED[el]}')
    r = static(j, d, name, PETG, fixtures=[('fixed', fx)], loads=[('normal', inner, -150.0)], el=el,
               ctrl=ctrl, loose_ok=True)
    r.loaded_pts = None
    np.savez(W / f'{name}.npz', pos=r.pos, s=r.s, disp=r.disp, reaction=np.array(r.reaction, dtype=float))
    # the inside corner: the box round the R-corner (the box of the task's corner, X 5..7.5, Z 5..7.5)
    mc = r.in_box([5.0, 1.0, 5.0, 7.5, 49.0, 7.5])
    row = dict(el=el, nodes=r.nodes, reaction_N=r.reaction, max_disp_mm=r.max_disp(), excessive=bool(r.excessive),
               corner_nodes=int(mc.sum()))
    if mc.any():
        idx = np.flatnonzero(mc)[np.argmax(r.vm[mc])]
        at = r.pos[idx]
        row['corner_vm_mpa'] = round(float(r.vm[idx]), 3)
        row['corner_at_mm'] = at.round(2).tolist()
        row['corner_layer_tension_Z'] = round(r.layer_stress((0, 0, 1), mc)[0], 3)
        row['corner_avg'] = {str(q): [round(r.average(at, q)[0], 3), r.average(at, q)[1]] for q in (0.5, 1.0, 2.0)}
        row['corner_sigma_xyz_at_peak'] = [round(float(v), 3) for v in r.s[idx, 1:4]]
        row['corner_P3_at_peak'] = round(float(r.s[idx, 9]), 3)
    vm, at_g = r.peak(r.away(dist=6.0))
    row['holes_vm_away6_mpa'] = round(vm, 3)
    row['holes_layer_tension_Z'] = round(r.layer_stress((0, 0, 1), r.away(dist=6.0))[0], 3)
    log(name, json.dumps(row, default=str)[:600])
    return row


def series(j, fname, radius, key):
    d = build(j, fname, radius)
    rows = []
    for el in SIZES:
        row = solve(j, d, el, radius)
        rows.append(row)
        RES['series'][key] = rows
    return rows


def main():
    try:
        with job(wait_s=900) as j:
            j.simulation()
            series(j, 'bracket_sharp.SLDPRT', None, 'sharp')
        with job(wait_s=900) as j:
            j.simulation()
            series(j, 'bracket_r04.SLDPRT', 0.4, 'r04')
        RES['status'] = 'done'
    except Exception as ex:  # noqa: BLE001
        RES['error'] = f'{type(ex).__name__}: {ex}'
        RES['traceback'] = traceback.format_exc()[-2500:]
        log('FAILED', RES['error'])
    finally:
        RES['finished'] = time.strftime('%H:%M:%S')
        (E / 't4.json').write_text(json.dumps(RES, indent=2, ensure_ascii=False, default=str), encoding='utf-8')
        log('wrote t4.json', RES['status'])


if __name__ == '__main__':
    main()
