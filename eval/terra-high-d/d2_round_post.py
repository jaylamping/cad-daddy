import sys,math
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swfea import Result
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
for case in ('Y','X'):
 for k in ('20','12'):
  file=OUT/('d2_round_'+case+k+'.npz')
  if not file.exists():continue
  p=np.load(file);pos=p['pos'];x,y,z=pos.T;radius=np.hypot(x,y)
  r=Result(case+str(k),float(k)/10,pos,p['s'],p['fixed_pts'],p['loaded_pts'],p['disp'],p['reaction'],len(pos),0,0,300)
  mask=(((radius>26.125)&(z>-.1)&(z<7.1))|((radius>22.55)&((z<-.2)|(z>7.2)))) & (cKDTree(p['fixed_pts']).query(pos)[0]>=2)
  for label,side in [('upper',y>.35),('lower',y<-.35)]:
   for dist in (0.5,1,1.5,2,3,5):
    m=mask & side
    for cx in (-30.5,30.5):
     for cz in (0,7):
      rad=np.hypot(x-cx,z-cz)
      m &= (np.hypot(rad-3,y-28.5)>dist) & (np.hypot(rad-2,y+6.3)>dist) & (np.hypot(rad-2,y+.3)>dist)
      m &= ~(((y>-.35)&(y<28.55)&(rad<1.75))|((y>=28.45)&(rad<3.05))|((y>-6.35)&(y<-.25)&(rad<2.05)))
    if m.any():print(case,k,label,dist,'nodes',int(m.sum()),'vm',round(r.peak(m)[0],3),'t',round(r.layer_stress((0,0,1),m)[0],3),'tau',round(r.layer_shear((0,0,1),m)[0],3))


