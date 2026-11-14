import sys
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swfea import Result
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
for case in ('Y','X'):
 for k in ('30','20','18','17','14'):
  f=OUT/('d2_transition_'+case+k+'.npz')
  if not f.exists():continue
  p=np.load(f);pos=p['pos'];x,y,z=pos.T;rad=np.hypot(x,y);r=Result(case+k,5,pos,p['s'],p['fixed_pts'],p['loaded_pts'],p['disp'],p['reaction'],len(pos),0,0,300)
  mask=(((rad>26.125)&(z>-.1)&(z<7.1))|((rad>22.55)&((z<-.2)|(z>7.2))))&(cKDTree(p['fixed_pts']).query(pos)[0]>=2)
  for label,side in [('upper',y>.35),('lower',y<-.35)]:
   m=mask & side
   for cx in (-30.5,30.5):
    for cz in (0,7):
     rr=np.hypot(x-cx,z-cz)
     m &= (np.hypot(rr-3,y-28.5)>2)&(np.hypot(rr-2,y+6.3)>2)&(np.hypot(rr-2,y+.3)>2)
     m &= ~(((y>-.35)&(y<28.55)&(rr<1.75))|((y>=28.45)&(rr<3.05))|((y>-6.35)&(y<-.25)&(rr<2.05)))
   print(case,k,label,'vm',r.peak(m))
   for axis in ((1,0,0),(0,1,0),(0,0,1)):print(axis,'tension',r.layer_stress(axis,m),'shear',r.layer_shear(axis,m))


