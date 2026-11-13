import sys, math, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(ROOT/'tools/solidworks'))
import numpy as np
import swkit as k
from swkit import *
from swfea import PETG,static
k.pin_export_prefs=lambda sw: None
OUT=ROOT/'cad/_wip/sw-eval/terra-high-a'; RUN=Path(__file__).resolve().parent
with job(wait_s=1800) as j:
 j.simulation(); d=open_doc(j.sw,OUT/'bracket.SLDPRT'); d.ForceRebuild3(False)
 rows=[]
 for el in (3.0,2.2,1.7):
  fixed=pick(d,kind='cyl',r=2.75); bore=pick(d,kind='cyl',r=11)
  expect('fixture holes',len(fixed),4,0); expect('bore',len(bore),1,0)
  nn=12*32974/el**3; disp=150*22**3/(3*1900*(50*6**3/12))+150*22**2*19/(1900*(50*6**3/12)); print('PREDICT',el,round(nn),disp,'peak root and bolt holes',flush=True)
  r=static(j,d,'T3_'+str(el).replace('.','_'),PETG,fixtures=[('fixed',fixed)],loads=[('remote',bore,(3,25,28),(150,0,0),(0,0,0))],el=el,max_nodes=199999)
  print('PREDICTION_CHECK',r.nodes,r.max_disp(),r.reaction,flush=True)
  if r.nodes>2*nn or r.nodes<nn/2 or r.max_disp()>3*disp or r.max_disp()<disp/3:
   print('STOP prediction mismatch; stress not evaluated',flush=True); break
  mask=r.away(dist=6); vm,at=r.peak(mask); dirs={}
  for label,n in [('X',(1,0,0)),('Y',(0,1,0)),('Z',(0,0,1))]: dirs[label]={'tension':r.layer_stress(n,mask),'shear':r.layer_shear(n,mask)}
  motor=r.in_box([-0.1,10,12,6.1,40,43]); print('MOTOR REGION VM',r.peak(motor),'Z',r.layer_stress((0,0,1),motor),flush=True)
  row={'el':el,'nodes':r.nodes,'peak':vm,'at':at,'all_peak':float(r.vm.max()),'dirs':dirs,'disp':r.max_disp(),'reaction':r.reaction,'motor_vm':r.peak(motor),'motor_layer':r.layer_stress((0,0,1),motor)}
  rows.append(row); print('ROW',row,flush=True)
  np.savez_compressed(RUN/('t3_'+str(el)+'.npz'),pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction)
  (RUN/'t3_rows.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')

