import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
from swfea import PETG,static
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True);j.simulation();d=open_doc(j.sw,OUT/'buck_mount.SLDPRT');d.ForceRebuild3(False)
 for axis,vec in [('X',(2.25,0,0)),('Y',(0,2.25,0))]:
  fix=pick(d,kind='cyl',r=2.75);loads=[]
  for x in (-39,39):
   for y in (-26.5,26.5):
    face=pick(d,kind='plane',at=(x+2,y,8));assert len(face)==1
    loads.append(('remote',face,(x,y,8),vec,(0,0,0)))
  assert len(fix)==2
  print('PREDICT',axis,'nodes 46451 displacement .02 mm, peak near window/rail holes; four individually rigid post faces',flush=True)
  r=static(j,d,'LATERAL_'+axis,PETG,fixtures=[('fixed',fix)],loads=loads,el=2,max_nodes=199999)
  print('ACTUAL',r.nodes,r.max_disp(),r.reaction,flush=True)
  np.savez(OUT/('d1_lateral_'+axis+'.npz'),pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction,fixed_pts=r.fixed_pts,loaded_pts=r.loaded_pts)
  if not (23225<r.nodes<92902 and .02/3<r.max_disp()<.02*3): print('STOP PREDICTION; no stress read',flush=True);break
  mask=r.away(dist=6);print('peak',r.peak(mask),flush=True)
  for n in ((1,0,0),(0,1,0),(0,0,1)):print('layers',n,r.layer_stress(n,mask),r.layer_shear(n,mask),flush=True)
 close(j.sw,d)
