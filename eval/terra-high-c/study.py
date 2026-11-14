import sys, json, math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(ROOT/'tools/solidworks'))
import swkit
from swkit import *
from swfea import static, PETG
swkit.pin_export_prefs=lambda sw: None
OUT=ROOT/'cad/_wip/sw-eval/terra-high-c'; RUN=ROOT/'tools/solidworks/playbook/eval/terra-high-c'
results={}
with job(wait_s=1800) as j:
 print('OWN PID',j.inst.pid,flush=True)
 d=open_doc(j.sw,OUT/'link_organic.SLDPRT')
 print('VOLUME',volume(d),'BBOX',bbox(d),'BODIES',bodies(d),'ERRORS',feature_errors(d),flush=True)
 for radius in [1.7,4,15]:
  fs=pick(d,kind='cyl',r=radius); print('CYL',radius,len(fs),[face_info(f) for f in fs],flush=True)
 for pt in [(20,-4,0),(0,16,-208),(0,-16,-208)]:
  fs=pick(d,kind='plane',at=pt); print('PLANE',pt,len(fs),[face_info(f) for f in fs],flush=True)
 save_as(d,OUT/'link_organic.step')
 print('PREDICTION: 5 mm elements about 12672 nodes; ideal uniform oval beam 1.37 mm X or 1.83 mm Y displacement, larger with neck and fork; peak expected at narrow disc-shaft transition.',flush=True)
 for name,force,est in [('PLUS_X',(60,0,0),1.37),('MINUS_X',(-60,0,0),1.37),('PLUS_Y',(0,60,0),1.83)]:
  root=pick(d,kind='plane',at=(20,-4,0)); hole=pick(d,kind='cyl',r=4)
  expect('root faces',len(root),1,0); expect('pin faces',len(hole),2,0)
  print('PREDICT',name,'nodes 12672; displacement mm',est,'peak neck near z=-34',flush=True)
  r=static(j,d,name,PETG,fixtures=[('fixed',root)],loads=[('remote',hole,(0,0,-200),force,(0,0,0))],el=5.0,max_nodes=199999)
  print(r.summary(),flush=True)
  rawmax=float(r.vm.max()); rawpos=r.pos[int(r.vm.argmax())].tolist()
  values={}
  for axis,n in [('X',(1,0,0)),('Y',(0,1,0)),('Z',(0,0,1))]:
   try:
    vm, vp=r.peak(); ln, lp=r.layer_stress(n); sh, sp=r.layer_shear(n)
    values[axis]={'vm':vm,'vm_at':vp,'tension':ln,'tension_at':lp,'shear':sh,'shear_at':sp,'sf_yield':45/vm,'sf_layer':22.5/ln if ln>0 else None,'sf_shear':13/sh if sh>0 else None}
   except Exception as ex: values[axis]={'error':str(ex)}
  results[name]={'nodes':r.nodes,'elements':r.elements,'disp_mm':r.max_disp(),'reaction':r.reaction.tolist() if hasattr(r.reaction,'tolist') else list(r.reaction),'raw_peak':rawmax,'raw_peak_at':rawpos,'layers':values}
  np.savez_compressed(RUN/(name+'.npz'),pos=r.pos,stress=r.s,disp=r.disp,reaction=r.reaction,fixed_pts=r.fixed_pts,loaded_pts=r.loaded_pts)
  (RUN/'fea_results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
