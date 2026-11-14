import sys,json,math
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(R/'tools/solidworks'))
import swkit
from swkit import *
from swfea_bearing import static,PETG
swkit.pin_export_prefs=lambda sw:None
O=R/'cad/_wip/sw-eval/terra-high-c'; RUN=R/'tools/solidworks/playbook/eval/terra-high-c'
resultfile=RUN/'e_fillet_results.json'
results=json.loads(resultfile.read_text(encoding='utf-8')) if resultfile.exists() else {}
chosen=sys.argv[1] if len(sys.argv)>1 else 'BX_POS'
with job(wait_s=1800) as j:
 print('OWN PID',j.inst.pid,flush=True)
 d=open_doc(j.sw,O/'fillet_e.SLDPRT')
 for case,fx,pred in [x for x in [('BX_POS',60,1.45),('BX_NEG',-60,1.45),('THRUST_Y',0,5.2)]]:
  for el in (5.0,):
   tag=case+'_'+str(el).replace('.','_'); coord=d.FeatureByName('BEARING_CSYS')
   root=pick(d,kind='plane',at=(20,-4,0)); holes=pick(d,kind='cyl',r=4)
   if fx: load=('bearing',holes,coord,fx)
   else:
    side=pick(d,kind='plane',at=(0,16,-208)); expect('thrust face',len(side),1,0); load=('normal',side,60)
   expected=111230*(5/el)**3
   print('PREDICT',tag,'nodes',round(expected),'disp',pred,'raw peak near elbow shaft junction',flush=True)
   r=static(j,d,tag,PETG,fixtures=[('fixed',root)],loads=[load],el=el,max_nodes=149999)
   print('CHECK',tag,r.nodes,r.max_disp(),r.reaction,flush=True)
   if not (expected/2<r.nodes<expected*2 and pred/3<r.max_disp()<pred*3): raise Failed('prediction threshold exceeded; stop')
   ix=int(r.vm.argmax()); print('RAW PEAK LOCATION',r.pos[ix],flush=True)
   if not ((-55<r.pos[ix,2]<-20) or (-185<r.pos[ix,2]<-165)): raise Failed('unexpected peak location; stop')
   vals={}
   for axis,n in [('X',(1,0,0)),('Y',(0,1,0)),('Z',(0,0,1))]:
    for mask_name,mask in [('all',np.ones(len(r.pos),dtype=bool)),('away12',r.away(dist=12))]:
     vm,vp=r.peak(mask); tens,tp=r.layer_stress(n,mask); shear,sp=r.layer_shear(n,mask)
     vals[axis+'_'+mask_name]={'vm':vm,'vm_at':vp,'tension':tens,'tension_at':tp,'shear':shear,'shear_at':sp,'sf_yield':45/vm,'sf_layer':22.5/tens if tens>0 else None,'sf_shear':13/shear if shear>0 else None}
   results[tag]={'nodes':r.nodes,'elements':r.elements,'disp_mm':r.max_disp(),'reaction':r.reaction,'values':vals}
   np.savez_compressed(RUN/(tag+'_e_fillet.npz'),pos=r.pos,stress=r.s,disp=r.disp,reaction=r.reaction,fixed_pts=r.fixed_pts,loaded_pts=r.loaded_pts)
   (RUN/'e_fillet_results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
   print('RESULT',tag,json.dumps(results[tag]),flush=True)
