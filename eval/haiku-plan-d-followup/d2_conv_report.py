"""Follow-up R3c report: tables, step sizes, the wider-zone upper check and judge(). No SolidWorks."""
import json
import numpy as np
from d2_fea import split, measures, ALLOW, judge, WIP, HERE
from swfea import Result

rows = json.loads((HERE / 'd2c_rows.json').read_text(encoding='utf-8'))
NAMES = {'+X': ['D2C_X_12', 'D2C_X_09', 'D2C_X_07'], '+Y': ['D2C_Y_12', 'D2C_Y_09', 'D2C_Y_07']}
HALVES = ('upper', 'lower')
MS = ('vm', 'layer', 'shear')
ok = all(n in rows for c in NAMES for n in NAMES[c])
print('rows present:', ok)
series, limits, lowest_per = {}, {}, {}
for case, names in NAMES.items():
    if not all(n in rows for n in names):
        continue
    for h in HALVES:
        for m in MS:
            key = f'{h} half, {case}, {m}'
            vals = [rows[n][h]['Z'][m] for n in names]
            series[key] = vals
            limits[key] = ALLOW[m]
            print(f'{key:24s}', ' -> '.join(f'{v:.2f}' for v in vals),
                  '  steps %:', [round(100 * (vals[i + 1] - vals[i]) / vals[i], 1) for i in range(len(vals) - 1)])
    for n in names:
        print(n, 'excluded vm upper', round(rows[n]['upper_excluded_vm'], 2), 'lower', round(rows[n]['lower_excluded_vm'], 2),
              'at cs', rows[n]['cs'], 'nodes', rows[n]['nodes'], 'screw tension', [round(q['tension'], 1) for q in rows[n]['screws']])
v = judge(series, {k: limits[k] for k in series}, need=2.0)
print('judge verdict', v['verdict'], 'lowest factor', v['lowest_factor'])
print('judge detail', json.dumps(v, default=float)[:3000])
# wider zone round the upper heads, case X at each of three rows
for n in NAMES['+X'] + NAMES['+Y']:
    f = WIP / 'npz' / f'{n}.npz'
    if not f.exists():
        continue
    z = np.load(f)
    r = Result(n, 0, z['pos'], z['s'], None, None, z['disp'], z['reaction'], int(z['nodes']), None, 0, 0)
    m = split(r)
    wide = m['upper_all'] & ~((m['dxz'] < 4.75) & (r.pos[:, 1] > 26.5))
    narrow = m['upper']
    out = {}
    for lab, mk in (('narrow (3.75, 27.5)', narrow), ('wide (4.75, 26.5)', wide)):
        out[lab] = {k: measures(r, mk, nrm) for k, nrm in (('Z', (0, 0, 1)),)}['Z']
    print(n, 'upper Z narrow', out['narrow (3.75, 27.5)'])
    print(n, 'upper Z wide  ', out['wide (4.75, 26.5)'])
