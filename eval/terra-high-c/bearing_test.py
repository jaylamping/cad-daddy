import sys,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(R/'tools/solidworks'))
import swkit
from swkit import *
from swfea_bearing import static,PETG
swkit.pin_export_prefs=lambda sw:None
O=R/'cad/_wip/sw-eval/terra-high-c'; RUN=R/'tools/solidworks/playbook/eval/terra-high-c'
with job(wait_s=1800) as j:
 print('OWN PID',j.inst.pid,flush=True)
 d=open_doc(j.sw,O/'bearing_probe.SLDPRT')
 coord=d.FeatureByName('BEARING_CSYS'); print('COORD',coord,flush=True)
 holes=pick(d,kind='cyl',r=4); root=pick(d,kind='plane',at=(20,-4,0)); print('FACES',len(holes),len(root),flush=True)
 print('PREDICT 40000 nodes, 3 mm displacement (section beam ~2 plus joint compliance), peak at disc/shaft root',flush=True)
 r=static(j,d,'BEARING_PLUS_X',PETG,fixtures=[('fixed',root)],loads=[('bearing',holes,coord,60)],el=5,max_nodes=199999)
 print('CHECK',r.nodes,'disp',r.max_disp(),'reaction',r.reaction,flush=True)
 np.savez_compressed(RUN/'bearing_probe.npz',pos=r.pos,stress=r.s,disp=r.disp,reaction=r.reaction,fixed_pts=r.fixed_pts,loaded_pts=r.loaded_pts)
 if r.nodes>80000 or r.nodes<20000 or r.max_disp()>9 or r.max_disp()<1:
  raise Failed('prediction threshold exceeded: stop before stress judgement')
 print('raw maximum stress diagnostic',r.vm.max(),'at',r.pos[int(r.vm.argmax())],flush=True)
 print(r.summary(),flush=True)
