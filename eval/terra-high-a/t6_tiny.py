import sys,math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(ROOT/'tools/solidworks'))
import numpy as np
import swkit as k
from swkit import *
from swfea import PETG,STEEL,NO_PENETRATION,SOLVER_DIRECT,static
k.pin_export_prefs=lambda sw: None
OUT=ROOT/'cad/_wip/sw-eval/terra-high-a'; RUN=Path(__file__).resolve().parent
pad=dict(name='Soft pad',EX=.5e6,NUXY=.45,DENS=1000.,SIGYLD=1e6,SIGXT=1e6)
with job(wait_s=1800) as j:
 j.simulation(); d=open_doc(j.sw,OUT/'t6c_contact.SLDPRT'); d.ForceRebuild3(False)
 def body(key):
  bs=[b for b in solid_bodies(d) if key.lower() in b.Name.lower()]
  if len(bs)!=1: raise Failed('body lookup '+key)
  return bs[0]
 def fs(key,fn): return [f for f in (call(body(key),'GetFaces') or []) if fn(face_info(f))]
 block=fs('HOLE',lambda i:i['kind']=='cyl' and abs(i['r']-5.1)<.01)
 pin=fs('t6c_pin',lambda i:i['kind']=='cyl' and abs(i['r']-5)<.01)
 bottom=fs('HOLE',lambda i:i['kind']=='plane' and abs(i['box'][2])<.01 and abs(i['box'][5])<.01)
 ends=[]; pads=[]
 for side,name in [(-1,'t6c_pad_left'),(1,'t6c_pad_right')]:
  ends.append(fs('t6c_pin',lambda i:i['kind']=='plane' and abs(i['box'][1]-side*25)<.01 and abs(i['box'][4]-side*25)<.01))
  pads+=fs(name,lambda i:i['kind']=='plane' and abs(i['box'][1]-side*27)<.01 and abs(i['box'][4]-side*27)<.01)
 if [len(block),len(pin),len(bottom),len(pads)]+[len(f) for f in ends]!=[1,1,1,2,1,1]: raise Failed('bad face counts')
 out=[]
 for label,F,pred in [('TINY',.0025,.002)]:
  print('PREDICT',label,48000,pred,'mm; peak upper hole',flush=True)
  loads=[('remote',ends[0],(0,-25,10),(0,0,F),(0,0,0)),('remote',ends[1],(0,25,10),(0,0,F),(0,0,0))]
  r=static(j,d,'T6E_'+label,PETG,fixtures=[('fixed',bottom+pads)],loads=loads,el=3,ctrl=[(block,1.25),(pin,1.25)],contacts=[(NO_PENETRATION,block,pin)],materials={'t6c_pin':STEEL,'t6c_pad_left':pad,'t6c_pad_right':pad},solver=SOLVER_DIRECT,loose_ok=True,max_nodes=199999)
  print('PREDICTION_CHECK',r.nodes,r.max_disp(),r.reaction,flush=True)
  if r.nodes>96000 or r.nodes<24000 or r.max_disp()>3*pred or r.max_disp()<pred/3:
   print('STOP prediction mismatch, stress not inspected',flush=True); break
  radial=np.sqrt(r.pos[:,0]**2+(r.pos[:,2]-10)**2)
  surf=(radial>=5.08)&(radial<5.35)&(np.abs(r.pos[:,1])<14.9)
  steel=(radial<4.99)&(np.abs(r.pos[:,1])>20)&(np.abs(r.pos[:,1])<25.01)
  padmask=(np.abs(r.pos[:,1])>25.05)&(radial<2.51)
  trac=np.sqrt(r.s[:,4]**2+r.s[:,2]**2+r.s[:,6]**2)
  padbound=float(trac[padmask].max())*2*math.pi*2.5**2 if padmask.any() else None
  row={'label':label,'nodes':r.nodes,'disp':r.max_disp(),'pin_rise_mean':float(r.disp[steel,3].mean()),'reaction':r.reaction,'hole_vm':r.peak(surf),'pad_force_bound':padbound,'excessive':r.excessive}
  print('ROW',row,flush=True); out.append(row)
  np.savez_compressed(RUN/('t6e_'+label+'.npz'),pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction)
  (RUN/'t6e_rows.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
