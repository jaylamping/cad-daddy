import sys,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(R/'tools/solidworks'))
import swkit
from swkit import *
from swfea_bearing import static,PETG
swkit.pin_export_prefs=lambda sw:None
O=R/'cad/_wip/sw-eval/terra-high-c'; RUN=R/'tools/solidworks/playbook/eval/terra-high-c'
results={}
with job(wait_s=1800) as j:
 print('OWN PID',j.inst.pid,flush=True)
 d=open_doc(j.sw,O/'link_organic.SLDPRT')
 for name,fx,pred in [('BX_POS',60,2.0),('BX_NEG',-60,2.0),('THRUST_Y',0,4.0)]:
  coord=d.FeatureByName('BEARING_CSYS'); root=pick(d,kind='plane',at=(20,-4,0)); holes=pick(d,kind='cyl',r=4)
  print('PREDICT',name,'nodes 40000, deflection',pred,'mm, raw peak at disc-shaft root',flush=True)
  if fx: load=('bearing',holes,coord,fx)
  else:
   side=pick(d,kind='plane',at=(0,16,-208)); expect('thrust face',len(side),1,0)
   load=('normal',side,60)
  r=static(j,d,name,PETG,fixtures=[('fixed',root)],loads=[load],el=5,max_nodes=199999)
  print('CHECK',r.nodes,r.max_disp(),r.reaction,flush=True)
  if not (20000<r.nodes<80000 and pred/3<r.max_disp()<pred*3):
   raise Failed('prediction threshold exceeded; stop before stress judgement')
  ix=int(r.vm.argmax()); print('RAW PEAK',r.vm[ix],r.pos[ix],flush=True)
  if r.pos[ix,2] > -25 or r.pos[ix,2] < -50: raise Failed('unexpected peak; stop')
  vals={}
  for axis,n in [('X',(1,0,0)),('Y',(0,1,0)),('Z',(0,0,1))]:
   for mask_name,mask in [('all',np.ones(len(r.pos),dtype=bool)),('away',r.away())]:
    vm,vp=r.peak(mask); tension,tp=r.layer_stress(n,mask); shear,sp=r.layer_shear(n,mask)
    vals[axis+'_'+mask_name]={'vm':vm,'vm_at':vp,'tension':tension,'tension_at':tp,'shear':shear,'shear_at':sp,'sf_yield':45/vm,'sf_layer':22.5/tension if tension>0 else None,'sf_shear':13/shear if shear>0 else None}
  results[name]={'nodes':r.nodes,'elements':r.elements,'disp_mm':r.max_disp(),'reaction':r.reaction,'values':vals}
  np.savez_compressed(RUN/(name+'.npz'),pos=r.pos,stress=r.s,disp=r.disp,reaction=r.reaction,fixed_pts=r.fixed_pts,loaded_pts=r.loaded_pts)
  (RUN/'bearing_results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
  print('RESULT',name,json.dumps(results[name]),flush=True)
