import sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
from swfea import PETG,static
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True); j.simulation(); d=open_doc(j.sw,OUT/'buck_mount.SLDPRT');d.ForceRebuild3(False)
 fixture=pick(d,kind='cyl',r=2.75); load=[]
 for x in (-39,39):
  for y in (-26.5,26.5): load+=pick(d,kind='plane',at=(x+2,y,8))
 print('fixture and loaded counts',len(fixture),len(load),flush=True)
 assert len(fixture)==2 and len(load)==4
 print('PREDICT nodes=21008 displacement=0.019 mm peak at window-end frame section near rail',flush=True)
 r=static(j,d,'UPLIFT_9N',PETG,fixtures=[('fixed',fixture)],loads=[('normal',load,-9.0)],el=2,max_nodes=199999)
 print('ACTUAL nodes',r.nodes,'disp',r.max_disp(),'reaction',r.reaction,flush=True)
 np.savez(OUT/'d1_uplift.npz',pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction,fixed_pts=r.fixed_pts,loaded_pts=r.loaded_pts)
 if not (21008/2 < r.nodes < 21008*2 and .019/3<r.max_disp()<.019*3):
  print('STOP prediction failed; stresses not interpreted',flush=True)
 else:
  print('SUMMARY',r.summary(),flush=True)
  for n in ((1,0,0),(0,1,0),(0,0,1)):
   print('LAYERS',n,r.layer_stress(n),r.layer_shear(n),flush=True)
 close(j.sw,d)
