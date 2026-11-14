import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
from swfea import PETG,static
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True);j.simulation();d=open_doc(j.sw,OUT/'buck_mount.SLDPRT');d.ForceRebuild3(False)
 for el,pred in [(3.,13428),(2.,28966),(1.5,57923)]:
  fix=pick(d,kind='cyl',r=2.75);load=[]
  for x in (-39,39):
   for y in (-26.5,26.5): load+=pick(d,kind='plane',at=(x+2,y,8))
  assert len(fix)==2 and len(load)==4
  print('PREDICT',el,'nodes',pred,'displacement mm',0.0787,'peak near inner end of window',flush=True)
  r=static(j,d,'ROUND_'+str(int(el*10)),PETG,fixtures=[('fixed',fix)],loads=[('normal',load,-9.)],el=el,max_nodes=199999)
  print('ACTUAL',r.nodes,r.max_disp(),r.reaction,flush=True)
  np.savez(OUT/('d1_round_'+str(int(el*10))+'.npz'),pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction,fixed_pts=r.fixed_pts,loaded_pts=r.loaded_pts)
  if not (pred/2<r.nodes<pred*2 and .0787/3<r.max_disp()<.0787*3):
   print('STOP prediction failed',flush=True);break
  mask=r.away(dist=6); print('PEAK',r.peak(mask),'TENSION',r.layer_stress((0,0,1),mask),'SHEAR',r.layer_shear((0,0,1),mask),flush=True)
 close(j.sw,d)

