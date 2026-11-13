import sys, math, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(ROOT/'tools/solidworks'))
import numpy as np
from scipy.spatial import cKDTree
import swkit as k
from swkit import *
from swfea import PETG,static
k.pin_export_prefs=lambda sw: None
OUT=ROOT/'cad/_wip/sw-eval/terra-high-a'; RUN=Path(__file__).resolve().parent
with job(wait_s=1800) as j:
 j.simulation(); rows=[]
 for name,el,nn,support,local in [('LOCAL125',3.,45000,False,1.25),('LOCAL100',3.,60000,False,1.0),('LOCAL080',3.,90000,False,.8)]:
  d=open_doc(j.sw,OUT/('bracket_support_twin.SLDPRT' if support else 'bracket_load_twin.SLDPRT')); d.ForceRebuild3(False)
  load=[]
  for a in (45,135,225,315):
   y=25+15.5*math.cos(math.radians(a)); z=28+15.5*math.sin(math.radians(a))
   f=pick(d,kind='plane',normal=(-1,0,0),at=(.1,y+2.5,z)); expect('motor ring',len(f),1,0); load+=f
  if support:
   fixed=[]
   for x in (25,65):
    for y in (10,40):
     f=pick(d,kind='plane',normal=(0,0,1),at=(x+3.3,y,5.9)); expect('washer ring',len(f),1,0); fixed+=f
  else: fixed=pick(d,kind='cyl',r=2.75); expect('fixed holes',len(fixed),4,0)
  print('PREDICT',name,nn,'nodes 2.5mm displacement peak root or motor holes',flush=True)
  holewalls=pick(d,kind='cyl',r=1.7); expect('motor hole walls',len(holewalls),4,0)
  print('LOCAL CONTROL',local,flush=True)
  r=static(j,d,name,PETG,fixtures=[('fixed',fixed)],loads=[('normal',load,150)],el=el,ctrl=[(holewalls,local)],max_nodes=199999)
  print('PREDICTION_CHECK',r.nodes,r.max_disp(),r.reaction,flush=True)
  if r.nodes>2*nn or r.nodes<nn/2 or r.max_disp()>7.5 or r.max_disp()<2.5/3:
   print('STOP prediction mismatch: stress not inspected',flush=True); break
  keep=cKDTree(r.fixed_pts).query(r.pos)[0]>=6
  dirs={}
  for label,n in [('X',(1,0,0)),('Y',(0,1,0)),('Z',(0,0,1))]: dirs[label]={'tension':r.layer_stress(n,keep),'shear':r.layer_shear(n,keep)}
  motor=r.in_box([-.1,10,12,6.1,40,43]); row={'study':name,'el':el,'nodes':r.nodes,'peak':r.peak(keep),'all':float(r.vm.max()),'dirs':dirs,'motor_vm':r.peak(motor),'motor_z':r.layer_stress((0,0,1),motor),'disp':r.max_disp(),'reaction':r.reaction}
  rows.append(row); print('ROW',row,flush=True)
  np.savez_compressed(RUN/(name+'.npz'),pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction)
  (RUN/'local_rows.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
  close(j.sw,d)
