from pathlib import Path
import math
import numpy as np
from scipy.spatial import Delaunay,ConvexHull
ROOT=Path(__file__).resolve().parents[5];OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
for case in ('Y15',):
 p=np.load(OUT/('d2_ref_'+case+'.npz'));q=p['pos'];s=p['s'];x,y,z=q.T
 for yy in (5,10,15,20):
  forces=[];areas=[]
  for cx,cz in ((-30.5,0),(-30.5,7),(30.5,0),(30.5,7)):
   rad=np.hypot(x-cx,z-cz);m=(rad<1.501)&(abs(y-yy)<.4)
   pts=q[m][:,[0,2]];val=s[m,2];pts2,inv=np.unique(np.round(pts,4),axis=0,return_inverse=True)
   vv=np.bincount(inv,weights=val)/np.bincount(inv); hull=ConvexHull(pts2);edge=pts2[hull.vertices]
   ang=np.mod(np.arctan2(edge[:,1]-cz,edge[:,0]-cx),2*np.pi);order=np.argsort(ang); ang=ang[order];ev=vv[hull.vertices][order]
   th=np.arange(256)*2*np.pi/256
   vals=np.interp(th, np.r_[ang[-1]-2*np.pi,ang,ang[0]+2*np.pi],np.r_[ev[-1],ev,ev[0]])
   boundary=np.column_stack((cx+1.5*np.cos(th),cz+1.5*np.sin(th)))
   pts3=np.vstack((pts2,boundary));v3=np.r_[vv,vals];tri=Delaunay(pts3).simplices;v=pts3[tri];a=v[:,1]-v[:,0];b=v[:,2]-v[:,0]
   area=np.abs(a[:,0]*b[:,1]-a[:,1]*b[:,0])/2
   forces.append(float(np.sum(area*v3[tri].mean(axis=1))));areas.append(float(area.sum()))
  print(case,'y',yy,'forces',forces,'sum',sum(forces),'section areas',areas)
