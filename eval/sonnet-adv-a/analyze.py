"""Post-process the rows files into judge() verdicts and results.json keys for T3, T4, T5. Run after the studies."""
import json, sys
from common import *
from swfea import judge
import numpy as np

REG = {'hole rims': 'hole rims (all nodes)', 'hole rims clear': 'hole rims (0.6 mm clear of loaded faces)',
       'root and fillet': 'root and fillet', 'base': 'base (2.5 mm clear of fixed holes)'}
ALLOW = dict(vm=45.0, layer=22.5, shear=13.0)


def series_for(rows, ori, regs=REG):
    series, lim = {}, {}
    for short, reg in regs.items():
        for meas, key in (('vm', 'vm'), ('layer', f'layer_{ori}'), ('shear', f'shear_{ori}')):
            k = f'{short}, {meas}'
            series[k] = [r['measures'][reg][key] for r in rows]
            lim[k] = ALLOW[meas]
    return series, lim


def table(rows, name):
    """Three directions x three measures at the finest mesh, worst region of each."""
    out = {}
    last = rows[-1]
    for ori in 'ZXY':
        for meas, key, L in (('vm', 'vm', 45.0), ('layer tension', f'layer_{ori}', 22.5), ('shear', f'shear_{ori}', 13.0)):
            best = max(((m[key], reg) for reg, m in last['measures'].items() if m and reg in REG.values()), key=lambda t: t[0])
            out[f'layers along {ori}, {meas}'] = dict(mpa=best[0], where=best[1], factor=round(L / best[0], 2))
    return out


if __name__ == '__main__':
    t3 = json.load(open(RUN / 't3_rows.json'))['rings_holes_fixed']
    res = {}
    for ori in 'ZXY':
        s, l = series_for(t3, ori)
        res[f'T3 layers along {ori}'] = judge(s, l, 2.0)
    res['T3 table'] = table(t3, 'T3')
    for key in ('rings_bottom_fixed', 'remote_bore_holes_fixed', 'remote_smallholes_holes_fixed'):
        r = json.load(open(RUN / 't3_rows.json'))[key][-1]
        res['T3 second way: ' + key] = {k: (v['vm'], v['layer_Z'], v['shear_Z'], v['layer_Y'], v['shear_Y']) for k, v in r['measures'].items() if v}
    # T4: the 0.4 mm variant, corner added as an entry
    t4 = json.load(open(RUN / 't4_rows.json'))
    for var in ('sharp', 'r04'):
        rows = t4[var]
        s, l = series_for(rows, 'Z')
        s['inside corner, vm'] = [r['corner']['vm'] for r in rows]; l['inside corner, vm'] = 45.0
        res[f'T4 {var} layers along Z'] = judge(s, l, 2.0)
    # T5
    t5 = json.load(open(RUN / 't5_rows.json'))
    rows5 = t5['rings_holes_fixed']
    for ori in 'ZXY':
        s, l = series_for(rows5, ori)
        res[f'T5 layers along {ori}'] = judge(s, l, 2.0)
    res['T5 table'] = table(rows5, 'T5')
    r5b = t5['rings_bottom_fixed'][-1]
    res['T5 bottom fixed el2.2'] = {k: (v['vm'], v['layer_Z'], v['shear_Z'], v['layer_Y'], v['shear_Y']) for k, v in r5b['measures'].items() if v}
    t5b = json.load(open(RUN / 't5b_rows.json'))
    rows5b = t5b['rings_holes_fixed']
    for ori in 'ZXY':
        s, l = series_for(rows5b, ori)
        res[f'T5b layers along {ori}'] = judge(s, l, 2.0)
    res['T5b table'] = table(rows5b, 'T5b')
    r5bb = t5b['rings_bottom_fixed'][-1]
    res['T5b bottom fixed el2.2'] = {k: (v['vm'], v['layer_Z'], v['shear_Z'], v['layer_Y'], v['shear_Y']) for k, v in r5bb['measures'].items() if v}
    res['T5b bottom fixed table (single size)'] = {f'{o} {m}': max(v[key.format(o)] for k, v in r5bb['measures'].items() if v and k in REG.values()) for o in 'ZXY' for m, key in (('layer', 'layer_{}'), ('shear', 'shear_{}'))}
    (RUN / 'judge_all.json').write_text(json.dumps(res, indent=1), encoding='utf-8')
    for k, v in res['T3 table'].items():
        print('T3', k, v)
    for k, v in res['T5 table'].items():
        print('T5', k, v)
    for k, v in res['T5b table'].items():
        print('T5b', k, v)
    print('T5b bottom', res['T5b bottom fixed table (single size)'])
