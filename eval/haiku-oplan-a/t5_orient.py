"""T5: make the T3 bracket pass. Change 1 (chosen, plans/A_T5.md): no geometry change, printed on its side with the
Y 0 face on the bed, so the layers run along Y. The study is the T3 load case on bracket_c.SLDPRT (a saved copy of
bracket.SLDPRT), converged on the Y-layer measures, plus the model-A check at 1.5.
Writes eval/haiku-oplan-a/t5.json. Change 2 (thicker upright) is worked by hand in the report, not built.
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
RES = {'task': 'T5', 'status': 'failed', 'notes': []}
LAYERS = (0, 1, 0)


def solve(j, d, el, load='B'):
    d.ForceRebuild3(False)
    holes = pick(d, kind='cyl', r=1.7)
    fx = pick(d, kind='cyl', r=2.75)
    if len(holes) != 4 or len(fx) != 4:
        raise Failed(f'pick counts holes {len(holes)} fixtures {len(fx)}')
    if load == 'B':
        ld = pick(d, kind='plane', normal=(1, 0, 0), at=(6, 25, 44))
        if len(ld) != 1:
            raise Failed(f'load pick {len(ld)}')
        loads = [('normal', ld, -150.0)]
    else:
        loads = [('remote', holes, (3.0, 25.0, 28.0), (150.0, 0, 0), (0, 0, 0))]
    fil = pick(d, kind='cyl', r=4.0)
    name = f'T5_orientY_{load}_{str(el).replace(".", "p")}'
    r = static(j, d, name, PETG, fixtures=[('fixed', fx)], loads=loads, el=el,
               ctrl=[(holes, 0.3 * el), (fil, 0.4 * el)], loose_ok=True)
    r.loaded_pts = None
    np.savez(W / f'{name}.npz', pos=r.pos, s=r.s, disp=r.disp, reaction=np.array(r.reaction, dtype=float))
    return r


def measures(r):
    vm, vat = r.peak()
    yt, yw = r.layer_stress(LAYERS)
    ys, yws = r.layer_shear(LAYERS)
    zt, zw = r.layer_stress((0, 0, 1))
    return dict(el=r.el, nodes=r.nodes, reaction_N=r.reaction, max_disp_mm=r.max_disp(),
                excessive=bool(r.excessive), vm_mpa=round(vm, 3), vm_at=vat, sf_yield=round(45 / vm, 3),
                layer_Y_tension_mpa=round(yt, 3), layer_Y_at=yw, sf_layer_Y=round(22.5 / yt, 3),
                layer_Y_shear_mpa=round(ys, 3), layer_Y_shear_at=yws, sf_shear_Y=round(13 / ys, 3),
                layer_Z_tension_mpa_for_reference=round(zt, 3), layer_Z_at=zw)


def main():
    try:
        with job(wait_s=900) as j:
            j.simulation()
            d = open_doc(j.sw, W / 'bracket.SLDPRT')
            expect('start volume', volume(d), 32974.0, 0.001)
            save_as(d, W / 'bracket_c.SLDPRT')
            expect('bracket_c volume', volume(d), 32974.0, 0.001)
            RES['mass_g'] = round(volume(d) * 1.19e-3, 2)
            RES['mass_growth_pct'] = 0.0
            rows = []
            last = None
            for el in (3.0, 2.0, 1.5):
                last = solve(j, d, el, 'B')
                m = measures(last)
                rows.append(m)
                log('T5 row', json.dumps(m, default=str))
            RES['rows_B_Y_layers'] = rows
            conv = {}
            for key in ('vm_mpa', 'layer_Y_tension_mpa', 'layer_Y_shear_mpa'):
                a, b = rows[-2][key], rows[-1][key]
                conv[key] = round(abs(b - a) / abs(b) * 100, 2)
            RES['last_step_change_pct'] = conv
            RES['converged'] = all(v < 5 for v in conv.values())
            log('last-step change %', conv)
            ra = solve(j, d, 1.5, 'A')
            RES['check_model_A_el1p5_Y'] = measures(ra)
            log('model A Y', json.dumps(RES['check_model_A_el1p5_Y'], default=str))
            # direction table at el 1.5, load model B
            RES['direction_table_B_el1p5'] = {
                'Z_base_on_bed': dict(zip(('tension', 'at'), [round(v, 3) if isinstance(v, float) else v for v in r_tbl(last, (0, 0, 1))])),
                'Y_side_on_bed': dict(zip(('tension', 'at'), [round(v, 3) if isinstance(v, float) else v for v in r_tbl(last, (0, 1, 0))])),
                'X_back_on_bed': dict(zip(('tension', 'at'), [round(v, 3) if isinstance(v, float) else v for v in r_tbl(last, (1, 0, 0))])),
            }
            RES['status'] = 'done'
    except Exception as ex:  # noqa: BLE001
        RES['error'] = f'{type(ex).__name__}: {ex}'
        RES['traceback'] = traceback.format_exc()[-2500:]
        log('FAILED', RES['error'])
    finally:
        RES['finished'] = time.strftime('%H:%M:%S')
        (E / 't5.json').write_text(json.dumps(RES, indent=2, ensure_ascii=False, default=str), encoding='utf-8')
        log('wrote t5.json', RES['status'])


def r_tbl(r, n):
    t, w = r.layer_stress(n)
    return t, w


if __name__ == '__main__':
    main()
