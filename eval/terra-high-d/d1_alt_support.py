import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
from swfea import PETG,static
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True);j.simulation();d=open_doc(j.sw,OUT/'buck_mount.SLDPRT');d.ForceRebuild3(False)
 for radius in (1.6,2.75):
  fs=pick(d,kind='cyl',r=radius); print('DIM hole radius',radius,'count',len(fs),'faces',[face_info(f) for f in fs],flush=True)
 fix=pick(d,kind='plane',at=(0,0,0));load=[]
 for x in (-39,39):
  for y in (-26.5,26.5): load+=pick(d,kind='plane',at=(x+2,y,8))
 print('counts',len(fix),len(load),flush=True);assert len(fix)==1 and len(load)==4
 print('PREDICT 46000 nodes, displacement 0.002 mm (short posts fixed at base), peak around post root',flush=True)
 r=static(j,d,'ALT_BASE',PETG,fixtures=[('fixed',fix)],loads=[('normal',load,-9.)],el=2,max_nodes=199999)
 print('ACTUAL',r.nodes,r.max_disp(),r.reaction,flush=True)
 np.savez(OUT/'d1_alt.npz',pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction,fixed_pts=r.fixed_pts,loaded_pts=r.loaded_pts)
 if not (23000<r.nodes<92000 and .002/3<r.max_disp()<.002*3): print('STOP: prediction failed; no stress interpreted',flush=True)
 else:
  print('SUMMARY',r.summary(),flush=True)
 close(j.sw,d)
