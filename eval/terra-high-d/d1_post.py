import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swfea import Result
p=np.load(ROOT/'cad/_wip/sw-eval/terra-high-d/d1_uplift.npz')
hand=2.25*26.5**3/(3*1900*(17.5*4**3/12))
print('Corrected cantilever displacement',hand,'mm; 26.5 mm arm from fixed screw centre, 17.5 mm strip')
r=Result('UPLIFT_9N',2,p['pos'],p['s'],p['fixed_pts'],p['loaded_pts'],p['disp'],p['reaction'],len(p['pos']),16807,0,9)
print('Corrected displacement ratio',r.max_disp()/hand,'summary',r.summary())
for n in ((1,0,0),(0,1,0),(0,0,1)): print(n,'tension',r.layer_stress(n),'shear',r.layer_shear(n))
