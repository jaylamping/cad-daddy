import sys,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(R/'tools/solidworks'))
import swkit
from swkit import *
from swfea_bearing import static,PETG
swkit.pin_export_prefs=lambda sw:None
O=R/'cad/_wip/sw-eval/terra-high-c'; RUN=R/'tools/solidworks/playbook/eval/terra-high-c'; results={}
with job(wait_s=1800) as j:
 print('OWN PID',j.inst.pid,flush=True)
 d=open_doc(j.sw,O/'variant_d_study.SLDPRT')
 with Sk(d,plane(d,'Y',0,'CENTER_P'),'BEARING_CENTER') as s:
  uv=s.p((0,0,-200)); point=d.SketchManager.CreatePoint(uv[0],uv[1],0)
 d.ClearSelection2(True); sel=d.SelectionManager.CreateSelectData; sel.Mark=1; assert point.Select4(False,sel)
 fs=pick(d,kind='cyl',r=4); sel=d.SelectionManager.CreateSelectData; sel.Mark=8; assert fs[0].Select4(True,sel)
 f=d.FeatureManager.InsertCoordinateSystem(False,False,False); assert f; f.Name='BEARING_CSYS'; save(d)
 print('TRANSFORM',d.Extension.GetCoordinateSystemTransformByName('BEARING_CSYS').ArrayData,flush=True)
 for name,fx,pred in [('D_THRUST',0,6.3),('D_BX_POS',60,2),('D_BX_NEG',-60,2)]:
  root=pick(d,kind='plane',at=(20,-4,0)); holes=pick(d,kind='cyl',r=4)
  if fx: load=('bearing',holes,d.FeatureByName('BEARING_CSYS'),fx)
  else: load=('normal',pick(d,kind='plane',at=(0,16,-208)),60)
  print('PREDICT',name,'nodes 40000, displacement',pred,'mm; peak at root',flush=True)
  r=static(j,d,name,PETG,fixtures=[('fixed',root)],loads=[load],el=5,max_nodes=79999)
  print('CHECK',name,'nodes',r.nodes,'disp',r.max_disp(),'reaction',r.reaction,flush=True)
  if not (20000<r.nodes<80000 and pred/3<r.max_disp()<pred*3): raise Failed('prediction mismatch; stop before stress judgement')
  ix=int(r.vm.argmax()); print('RAW PEAK LOCATION',r.pos[ix],flush=True)
  if not (-55<r.pos[ix,2]<-20): raise Failed('unexpected peak; stop')
  vals={}
  for axis,n in [('X',(1,0,0)),('Y',(0,1,0)),('Z',(0,0,1))]:
   for label,mask in [('all',np.ones(len(r.pos),dtype=bool)),('away',r.away())]:
    vm,vp=r.peak(mask); tens,tp=r.layer_stress(n,mask); shear,sp=r.layer_shear(n,mask)
    vals[axis+'_'+label]={'vm':vm,'vm_at':vp,'tension':tens,'tension_at':tp,'shear':shear,'shear_at':sp,'sf_yield':45/vm,'sf_layer':22.5/tens if tens>0 else None,'sf_shear':13/shear if shear>0 else None}
  results[name]={'nodes':r.nodes,'elements':r.elements,'disp_mm':r.max_disp(),'reaction':r.reaction,'values':vals}
  np.savez_compressed(RUN/(name+'.npz'),pos=r.pos,stress=r.s,disp=r.disp,reaction=r.reaction,fixed_pts=r.fixed_pts,loaded_pts=r.loaded_pts)
  (RUN/'variant_d_results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
  print('RESULT',name,json.dumps(results[name]),flush=True)
