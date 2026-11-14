import sys
from pathlib import Path
import numpy as np
from scipy.spatial import Delaunay
ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools' / 'solidworks'))
from swfea import Result
SIM = ROOT / 'cad' / '_sim' / 'sw-eval' / 'luna-b'
d = np.load(SIM / 'B4_full_diag.npz')
r = Result('diag', 4.0, d['pos'], d['stress'], d['fixed_points'], d['loaded_points'], d['displacement'], [-80,0,0,80], len(d['pos']),0,0,80)
p = r.pos
body = ((p[:,0]>=-4.02)&(p[:,0]<=4.02)&(p[:,1]>=-10.02)&(p[:,1]<=10.02)&(p[:,2]>=8.08)&(p[:,2]<=40.02))
for z0 in (8.5, 9, 12, 19, 19.5, 20.5, 22, 25, 29):
    m=body&(np.abs(p[:,2]-z0)<=0.45); xy=np.round(p[m,:2],3); txz=r.s[m,5]
    if len(xy)<12: print(z0,'few',len(xy)); continue
    u,inv=np.unique(xy,axis=0,return_inverse=True); tau=np.zeros(len(u)); n=np.zeros(len(u));np.add.at(tau,inv,txz);np.add.at(n,inv,1);tau/=n
    tri=Delaunay(u,qhull_options='QJ'); area_total=0.; force=0.; nt=0
    for ids in tri.simplices:
        q=u[ids]
        if np.any(q[:,0]<-4.01) or np.any(q[:,0]>4.01) or np.any(q[:,1]<-10.01) or np.any(q[:,1]>10.01): continue
        v1=q[1]-q[0];v2=q[2]-q[0]; a=abs(v1[0]*v2[1]-v1[1]*v2[0])/2
        area_total+=a; force+=a*tau[ids].mean();nt+=1
    print(z0,'nodes',len(xy),'unique',len(u),'area',round(area_total,2),'tri',nt,'fx',round(force,2),'tau',round(float(tau.min()),2),round(float(tau.max()),2))
