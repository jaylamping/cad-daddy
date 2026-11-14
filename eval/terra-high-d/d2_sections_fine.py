from pathlib import Path
import math
import numpy as np
from scipy.spatial import Delaunay
ROOT=Path(__file__).resolve().parents[5];OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
for case in ('Y15',):
 p=np.load(OUT/('d2_ref_'+case+'.npz'));q=p['pos'];s=p['s'];x,y,z=q.T
 print(case)
 for yy in (5,10,15,20):
  forces=[];areas=[]
  for cx,cz in ((-30.5,0),(-30.5,7),(30.5,0),(30.5,7)):
   rad=np.hypot(x-cx,z-cz);m=(rad<1.501)&(abs(y-yy)<.4)
   pts=q[m][:,[0,2]];val=s[m,2]
   pts2,inv=np.unique(np.round(pts,4),axis=0,return_inverse=True)
   vv=np.bincount(inv,weights=val)/np.bincount(inv)
   if len(pts2)<3:forces.append(float('nan'));continue
   tr=Delaunay(pts2).simplices;v=pts2[tr];a=v[:,1]-v[:,0];b=v[:,2]-v[:,0];area=np.abs(a[:,0]*b[:,1]-a[:,1]*b[:,0])/2
   forces.append(float(np.sum(area*vv[tr].mean(axis=1))));areas.append(float(np.sum(area)))
  print('y',yy,'forces',forces,'sum',sum(forces),'areas',areas)


