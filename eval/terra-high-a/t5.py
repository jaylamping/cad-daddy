import sys,math,json
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
 j.simulation(); d=open_doc(j.sw,OUT/'bracket.SLDPRT'); save_as(d,OUT/'bracket_c.SLDPRT'); save(d)
 rows=[]
 for el in (3.,2.2,1.7):
  fixed=pick(d,kind='cyl',r=2.75); holes=pick(d,kind='cyl',r=1.7)
  expect('fixed',len(fixed),4,0); expect('motor holes',len(holes),4,0)
  loads=[]
  for f in holes:
   b=face_info(f)['box']; y=(b[1]+b[4])/2; z=(b[2]+b[5])/2
   loads.append(('remote',[f],(3,y,z),(37.5,0,0),(0,0,0)))
  nn=12*32974/el**3; predicted=1.118
  print('PREDICT',el,nn,predicted,'peak root or motor holes',flush=True)
  r=static(j,d,'T5_'+str(el).replace('.','_'),PETG,fixtures=[('fixed',fixed)],loads=loads,el=el,max_nodes=199999)
  print('PREDICTION_CHECK',r.nodes,r.max_disp(),r.reaction,flush=True)
  if r.nodes>2*nn or r.nodes<nn/2 or r.max_disp()>3*predicted or r.max_disp()<predicted/3:
   print('STOP prediction mismatch',flush=True); break
  keep=cKDTree(r.fixed_pts).query(r.pos)[0]>=6
  dirs={}
  for label,n in [('X',(1,0,0)),('Y',(0,1,0)),('Z',(0,0,1))]: dirs[label]={'tension':r.layer_stress(n,keep),'shear':r.layer_shear(n,keep)}
  row={'el':el,'nodes':r.nodes,'peak':r.peak(keep),'all':float(r.vm.max()),'dirs':dirs,'disp':r.max_disp(),'reaction':r.reaction}
  rows.append(row); print('ROW',row,flush=True)
  np.savez_compressed(RUN/('t5_'+str(el)+'.npz'),pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction)
  (RUN/'t5_rows.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
