import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools' / 'solidworks'))
from swfea import Result
SIM = ROOT / 'cad' / '_sim' / 'sw-eval' / 'luna-b'
d=np.load(SIM/'B4_full_diag.npz'); r=Result('x',4,d['pos'],d['stress'],d['fixed_points'],d['loaded_points'],d['displacement'],[-80,0,0,80],len(d['pos']),0,0,80)
p=r.pos; U=r.disp
Tong=((p[:,0]>=-4.02)&(p[:,0]<=4.02)&(p[:,1]>=-10.02)&(p[:,1]<=10.02)&(p[:,2]>=8.08)&(p[:,2]<=40.02))
Block=((p[:,0]>=-20.01)&(p[:,0]<=20.01)&(p[:,1]>=-10.01)&(p[:,1]<=10.01)&(p[:,2]>=-0.01)&(p[:,2]<=20.01)) & ~((np.abs(p[:,0])<4.09)&(p[:,2]>8.01))
for nm,m in [('tongue',Tong),('block',Block)]:
 print(nm,'nodes',int(m.sum()),'u resultant max',float(U[m,4].max()),'ux min/max',float(U[m,1].min()),float(U[m,1].max()))
 if nm=='tongue':
  tip=m&(p[:,2]>=39.8); print('tip UX',float(U[tip,1].max()),'tip UZ',float(U[tip,3].min()),float(U[tip,3].max()))
 i=np.flatnonzero(m)[np.argmax(r.vm[m])]; print('vm max',float(r.vm[i]),p[i].tolist())
 print('vm away base z>1',float(r.vm[m&(p[:,2]>1)].max()))
