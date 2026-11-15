"""T5 change 2 (plans/A_T5.md fallback): upright 7.5 mm thick (X 0..7.5), base on the bed, layers along Z.

Rebuilt with the T1 steps and the plan's numbers (expect_dv each step), saved as bracket_c2.SLDPRT. Study: T3 load case,
model B converged over (3.0, 2.0, 1.5) on Z layers, then model A at 1.5. Writes eval/haiku-oplan-a/t5b.json.
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
RES = {'task': 'T5 change 2', 'status': 'failed', 'notes': []}
T = 7.5                       # upright thickness
C = 15.5 * math.cos(math.radians(45))


def build(j):
    d = new_part(j.sw, W / 'bracket_c2.SLDPRT')
    with Sk(d, plane(d, 'Z', 3.0, 'BASE_P'), 'BASE') as s:
        s.rect((0, 0, 3.0), (80, 50, 3.0))
    extrude(d, s.feat, 'BASE', 6.0, mode=MID, expect_dv=24000.0); save(d)
    with Sk(d, plane(d, 'Z', 26.0, 'UPRIGHT_P'), 'UPRIGHT') as s:
        s.rect((0, 0, 26.0), (T, 50, 26.0))
    extrude(d, s.feat, 'UPRIGHT', 40.0, mode=MID, expect_dv=15000.0); save(d)
    e = edges_where(d, lambda p: abs(p[0] - T) < 0.01 and abs(p[2] - 6) < 0.01)
    expect('inside corner edges', len(e), 1, 0)
    fillet(d, e, (4.0,), 'INSIDE_FILLET'); save(d)
    e = edges_where(d, lambda p: (abs(p[0] - 80) < 0.01 and min(abs(p[1]), abs(p[1] - 50)) < 0.01)
                    or (abs(p[2] - 46) < 0.01 and min(abs(p[1]), abs(p[1] - 50)) < 0.01))
    expect('round edges', len(e), 4, 0)
    v0 = volume(d)
    fillet(d, e, (5.0,), 'CORNER_R5')
    expect('rounds remove', v0 - volume(d), 144.85, 0.01); save(d)
    with Sk(d, plane(d, 'Z', 3.0, 'BASE_HOLES_P'), 'BASE_HOLES') as s:
        for x, y in ((25, 10), (25, 40), (65, 10), (65, 40)):
            s.circle((x, y, 3.0), 2.75)
    extrude(d, s.feat, 'BASE_HOLES', 8.0, cut=True, mode=MID, expect_dv=570.20); save(d)
    with Sk(d, plane(d, 'X', T / 2, 'BORE_P'), 'BORE') as s:
        s.circle((T / 2, 25.0, 28.0), 11.0)
    extrude(d, s.feat, 'BORE', 9.5, cut=True, mode=MID, expect_dv=2851.0); save(d)
    with Sk(d, plane(d, 'X', T / 2, 'UHOLES_P'), 'UPRIGHT_HOLES') as s:
        for y, z in ((25 - C, 28 - C), (25 + C, 28 - C), (25 + C, 28 + C), (25 - C, 28 + C)):
            s.circle((T / 2, y, z), 1.7)
    extrude(d, s.feat, 'UPRIGHT_HOLES', 9.5, cut=True, mode=MID, expect_dv=272.38); save(d)
    single_body(d)
    expect('feature errors empty', len(feature_errors(d)), 0, 0)
    expect('volume', volume(d), 35333.2, 0.001)
    bb = bbox(d)
    RES['bbox_mm'] = [round(v, 3) for v in bb]
    RES['volume_mm3'] = round(volume(d), 3)
    RES['mass_g'] = round(volume(d) * 1.19e-3, 2)
    RES['mass_growth_pct'] = round((volume(d) / 32974.02 - 1) * 100, 2)
    save(d)
    return d


def solve(j, d, el, load):
    d.ForceRebuild3(False)
    holes = pick(d, kind='cyl', r=1.7)
    fx = pick(d, kind='cyl', r=2.75)
    fil = pick(d, kind='cyl', r=4.0)
    if len(holes) != 4 or len(fx) != 4 or len(fil) != 1:
        raise Failed(f'pick counts holes {len(holes)} fixtures {len(fx)} fillet {len(fil)}')
    if load == 'B':
        ld = pick(d, kind='plane', normal=(1, 0, 0), at=(T, 25, 44))
        if len(ld) != 1:
            raise Failed(f'load pick {len(ld)}')
        loads = [('normal', ld, -150.0)]
    else:
        loads = [('remote', holes, (T / 2, 25.0, 28.0), (150.0, 0, 0), (0, 0, 0))]
    name = f'T5c2_{load}_{str(el).replace(".", "p")}'
    log(f'{name}: predicted nodes ~{ {3.0: 22000, 2.0: 74000, 1.75: 120000}[el] }')
    r = static(j, d, name, PETG, fixtures=[('fixed', fx)], loads=loads, el=el,
               ctrl=[(holes, 0.3 * el), (fil, 0.4 * el)], loose_ok=True)
    r.loaded_pts = None
    np.savez(W / f'{name}.npz', pos=r.pos, s=r.s, disp=r.disp, reaction=np.array(r.reaction, dtype=float))
    return r


def measures(r):
    vm, vat = r.peak()
    zt, zw = r.layer_stress((0, 0, 1))
    zs, zsw = r.layer_shear((0, 0, 1))
    return dict(el=r.el, nodes=r.nodes, reaction_N=r.reaction, max_disp_mm=r.max_disp(), excessive=bool(r.excessive),
                vm_mpa=round(vm, 3), vm_at=vat, sf_yield=round(45 / vm, 3),
                layer_Z_tension_mpa=round(zt, 3), layer_Z_at=zw, sf_layer_Z=round(22.5 / zt, 3),
                layer_Z_shear_mpa=round(zs, 3), layer_Z_shear_at=zsw, sf_shear_Z=round(13 / zs, 3))


def main():
    try:
        with job(wait_s=900) as j:
            j.simulation()
            d = build(j)
            rows, last = [], None
            for el in (3.0, 2.0, 1.75):          # 1.5 gave 200,454 nodes, over the 200,000 limit: plan branch, 1.75
                last = solve(j, d, el, 'B')
                m = measures(last)
                rows.append(m)
                log('T5c2 row', json.dumps(m, default=str))
            RES['rows_B_Z_layers'] = rows
            conv = {k: round(abs(rows[-1][k] - rows[-2][k]) / abs(rows[-1][k]) * 100, 2)
                    for k in ('vm_mpa', 'layer_Z_tension_mpa', 'layer_Z_shear_mpa')}
            RES['last_step_change_pct'] = conv
            RES['converged_vm_layerZ'] = conv['vm_mpa'] < 5 and conv['layer_Z_tension_mpa'] < 5
            log('last-step change %', conv)
            ra = solve(j, d, 1.75, 'A')
            RES['check_model_A_el1p5'] = measures(ra)
            log('model A', json.dumps(RES['check_model_A_el1p5'], default=str))
            RES['status'] = 'done'
    except Exception as ex:  # noqa: BLE001
        RES['error'] = f'{type(ex).__name__}: {ex}'
        RES['traceback'] = traceback.format_exc()[-2500:]
        log('FAILED', RES['error'])
    finally:
        RES['finished'] = time.strftime('%H:%M:%S')
        (E / 't5b.json').write_text(json.dumps(RES, indent=2, ensure_ascii=False, default=str), encoding='utf-8')
        log('wrote t5b.json', RES['status'])


if __name__ == '__main__':
    main()
