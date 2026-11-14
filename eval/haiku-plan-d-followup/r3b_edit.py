import json, sys
sys.path.insert(0, r'J:\code\cad-daddy-wt\sw-eval-haiku-plan-d\solidworks')
import swkit
from pathlib import Path
f = Path('results.json')
d = json.loads(f.read_text(encoding='utf-8'))
D2 = d['D2']
D2['sf_yield'] = 7.34
D2['sf_layer'] = 20.94
D2['sf_shear'] = 5.82
D2['governing'] = 'lower half, case X, shear between layers 2.23 MPa at (21.71, -15.15, 6.93), factor 5.82, 3.0 mm mesh, not converged'
D2['minutes'] = None  # set from times.log at the end of R3
D2['pads_share_n'] = 0.23
D2['why'] = D2['why'] + ' ; model checks 1 to 5 pass; only convergence is missing'
f.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding='utf-8')
print('ok', D2['governing'], '|', D2['why'])
