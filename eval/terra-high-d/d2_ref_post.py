import sys,math
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swfea import Result
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
for case in ('Y30','X30','Y22','X22'):
 file=OUT/('d2_ref_'+case+'.npz')
 if not file.exists():continue
 p=np.load(file);pos=p['pos'];x,y,z=pos.T;radius=np.hypot(x,y)
 r=Result(case,4,pos,p['s'],p['fixed_pts'],p['loaded_pts'],p['disp'],p['reaction'],len(pos),0,0,300)
 plastic=((radius>26.125)&(z>-.1)&(z<7.1)) | ((radius>22.55)&((z<-.2)|(z>7.2)))
 screwclear=np.ones(len(pos),bool)
 for cx in (-30.5,30.5):
  for cz in (0,7):
   rad=np.hypot(x-cx,z-cz)
   screwclear &= ~(((y>-.35)&(y<28.55)&(rad<1.75))|((y>=28.45)&(rad<3.05))|((y>-6.35)&(y<-.25)&(rad<2.05)))
 plastic &= screwclear
 for label,m in [('upper',plastic&(y>.35)),('lower',plastic&(y<-.35))]:
  # only exclude the fixed mounting face; the ring is loaded, but the seat must remain in view
  m &= cKDTree(p['fixed_pts']).query(pos)[0]>=2
  print(case,label,'nodes',m.sum(),'peak',r.peak(m),'ztens',r.layer_stress((0,0,1),m),'zshear',r.layer_shear((0,0,1),m),flush=True)
  for n in ((1,0,0),(0,1,0)): print('axis',n,'tension',r.layer_stress(n,m),'shear',r.layer_shear(n,m),flush=True)
 # approx stress integration over shanks (node sample only); reported separately as unvalidated
 for cx in (-30.5,30.5):
  for cz in (0,7):
   m=(np.hypot(x-cx,z-cz)<1.45)&(abs(y-10)<1.5)
   print('bolt-section',cx,cz,'n',m.sum(),'mean_sy',float(np.mean(r.s[m,2])) if m.any() else None,'N',float(np.mean(r.s[m,2])*math.pi*1.5**2) if m.any() else None,flush=True)
 if 'reactions' in p:
  q=p['reactions']; ids=r.s[:,0].astype(int); lookup={int(v):i for i,v in enumerate(ids)}
  active=q[np.any(np.abs(q[:,1:4])>1e-8,axis=1)]
  pads=[];mount=[]
  for row in active:
   idx=lookup.get(int(row[0]));
   if idx is None:continue
   px,py,pz=pos[idx]
   if abs(py+32)<.1:mount.append(row[1:4])
   elif abs(abs(px)-22)<.1 or abs(abs(py)-22)<.1:pads.append(row[1:4])
  print('reaction split mount',np.sum(mount,axis=0),'pads',np.sum(pads,axis=0),flush=True)

