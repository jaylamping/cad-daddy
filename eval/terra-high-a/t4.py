import sys,math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(ROOT/'tools/solidworks'))
import numpy as np
import swkit as k
from swkit import *
from swfea import PETG,static
k.pin_export_prefs=lambda sw: None
OUT=ROOT/'cad/_wip/sw-eval/terra-high-a'; RUN=Path(__file__).resolve().parent
with job(wait_s=1800) as j:
 j.simulation(); d=open_doc(j.sw,OUT/'bracket.SLDPRT'); save_as(d,OUT/'bracket_sharp.SLDPRT')
 f=d.FeatureByName('ROOT_R4')
 if f is None or not f.Select2(False,0): raise Failed('cannot select root fillet')
 if not call(d, "EditSuppress2"): raise Failed("cannot suppress root fillet")
 d.ForceRebuild3(False); save(d)
 print('SHARP',volume(d),bbox(d),bodies(d),feature_errors(d),flush=True)
 save_as(d,OUT/'bracket_sharp.stl')
 close(j.sw,d); d=open_doc(j.sw,OUT/'bracket_sharp.SLDPRT'); d.ForceRebuild3(False)
 rows=[]
 for el in (3.,2.2,1.7):
  fixed=pick(d,kind='cyl',r=2.75); bore=pick(d,kind='cyl',r=11)
  expect('fixed',len(fixed),4,0); expect('bore',len(bore),1,0)
  nn=12*32802/el**3; predicted=1.118
  print('PREDICT',el,nn,predicted,'peak sharp root',flush=True)
  r=static(j,d,'T4_'+str(el).replace('.','_'),PETG,fixtures=[('fixed',fixed)],loads=[('remote',bore,(3,25,28),(150,0,0),(0,0,0))],el=el,max_nodes=199999)
  print('PREDICTION_CHECK',r.nodes,r.max_disp(),r.reaction,flush=True)
  if r.nodes>2*nn or r.nodes<nn/2 or r.max_disp()>3*predicted or r.max_disp()<predicted/3:
   print('STOP prediction mismatch',flush=True); break
  mask=r.in_box([5.9,0,5.9,6.1,50,6.1]); keep=r.away(dist=6)
  row={'el':el,'nodes':r.nodes,'corner':r.peak(mask),'away':r.peak(keep),'layer':r.layer_stress((0,0,1),keep),'shear':r.layer_shear((0,0,1),keep),'disp':r.max_disp(),'reaction':r.reaction}
  rows.append(row); print('ROW',row,flush=True)
  np.savez_compressed(RUN/('t4_'+str(el)+'.npz'),pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction)
  (RUN/'t4_rows.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
