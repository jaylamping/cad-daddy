"""D2: everything read from the saved results (no SolidWorks needed). Writes d2_results_calc.json."""
import json, sys, math
import numpy as np
sys.path.insert(0, 'J:/code/cad-daddy-wt/sw-eval-sonnet-adv-d/eval/sonnet-adv-d'); sys.path.insert(0, 'J:/code/cad-daddy-wt/sw-eval-sonnet-adv-d/solidworks')
from d2_post import read
from d2_masks import masks
from swfea import judge
N = 'J:/code/cad-daddy-wt/sw-eval-sonnet-adv-d/_wip/sw-eval/sonnet-adv-d/d2/npz/a_%s_%s_%s.npz'
els = ('4.0', '3.0', '2.4')
R = {c: {el: read(N % (c, 'contact', el)) for el in els} for c in ('Y', 'X')}
B = {c: read(N % (c, 'bonded', '3.0')) for c in ('Y', 'X')}
out = dict(nodes={c: [R[c][el]['nodes'] for el in els] for c in R})
allow = dict(vm=45.0, layer=22.5, shear=13.0)
dirs = {'Y': (0, 1, 0), 'Z': (0, 0, 1), 'X': (1, 0, 0)}
table = {}
for d, nrm in dirs.items():
    ser = {}
    for half in ('upper', 'lower'):
        for c in ('Y', 'X'):
            for m, key in (('vm', 'vm'), ('layer', f'layer_{d}'), ('shear', f'shear_{d}')):
                ser[f'{half} half, +{c}, {m}'] = [R[c][el][half][key] for el in els]
    lim = {k: allow[k.split(', ')[2]] for k in ser}
    v = judge(ser, lim, need=2.0)
    table[d] = dict(verdict=v['verdict'], lowest_factor=v['lowest_factor'], lowest_entry=v['lowest_entry'], rows=v['rows'])
    print('print with', d, 'up: verdict', v['verdict'], 'lowest factor', v['lowest_factor'], v['lowest_entry'])
out['judge_by_layer_direction'] = table
# screws
sc = {}
for c in R:
    for el in els:
        r = R[c][el]
        t = [np.mean([s['sections'][k]['tension'] for k in range(3) if s['sections'][k]]) for s in r['screws']]
        sc[f'{c}_{el}'] = dict(per_screw_N=[round(x, 1) for x in t], sum_N=round(sum(t), 1), max_N=round(max(t), 1),
                               shear_fit=[round(np.mean([s['sections'][k]['shear_x'] for k in range(3) if s['sections'][k]]), 1) for s in r['screws']])
out['screws'] = sc
for c in B:
    t = [np.mean([s['sections'][k]['tension'] for k in range(3) if s['sections'][k]]) for s in B[c]['screws']]
    out[f'bonded_{c}'] = dict(per_screw_N=[round(x, 1) for x in t], sum_N=round(sum(t), 1), max_disp=B[c]['max_disp'], ring_mean_disp=B[c]['ring_mean_disp'],
                              upper_vm=B[c]['upper']['vm'], lower_vm=B[c]['lower']['vm'])
for c in R:
    r = R[c]['3.0']
    out[f'contact_{c}_3.0'] = dict(max_disp=r['max_disp'], ring_mean_disp=r['ring_mean_disp'], upper_mean_disp=r['upper_mean_disp'], lower_mean_disp=r['lower_mean_disp'],
                                   reaction=r['reaction'], pad_vm_polluted=r['pad_vm_max'])
json.dump(out, open('d2_results_calc.json', 'w'), indent=1, default=float)
print(json.dumps({k: out[k] for k in ('screws', 'bonded_Y', 'bonded_X', 'contact_Y_3.0', 'contact_X_3.0')}, indent=1, default=float))
