import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swfea import Result
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
for name,el in [('d1_round_30',3),('d1_round_20',2),('d1_round_15',1.5),('d1_alt',2)]:
 p=np.load(OUT/(name+'.npz'));r=Result(name,el,p['pos'],p['s'],p['fixed_pts'],p['loaded_pts'],p['disp'],p['reaction'],len(p['pos']),0,0,9)
 m=r.away(dist=1 if name=='d1_alt' else 6)
 print(name,'nodes',r.nodes,'disp',r.max_disp(),'peak',r.peak(m),'all max',r.vm.max(),'reaction',r.reaction)
 for n in ((1,0,0),(0,1,0),(0,0,1)):print('layers',n,r.layer_stress(n,m),r.layer_shear(n,m))
 # Linear sign reversal: compression at post tops is physically plausible, while upward loading there is not.
 r.s=r.s.copy();r.s[:,1:10]*=-1
 for n in ((1,0,0),(0,1,0),(0,0,1)):print('reversed tension',n,r.layer_stress(n,m))
