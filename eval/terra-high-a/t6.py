import sys,math,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(ROOT/'tools/solidworks'))
import numpy as np
import swkit as k
from swkit import *
from swfea import PETG,STEEL,NO_PENETRATION,SOLVER_DIRECT,static
k.pin_export_prefs=lambda sw: None
OUT=ROOT/'cad/_wip/sw-eval/terra-high-a'; RUN=Path(__file__).resolve().parent
pad=dict(name='Soft pad',EX=0.5e6,NUXY=.45,DENS=1000.,SIGYLD=1e6,SIGXT=1e6)
with job(wait_s=1800) as j:
 j.simulation()
 for name,yc,length,radius in [('t6_pin',0,50,5),('t6_pad_left',-26,2,1),('t6_pad_right',26,2,1)]:
  d=new_part(j.sw,OUT/(name+'.SLDPRT'))
  with Sk(d,plane(d,'Y',yc,name+'_P'),name.upper()) as s: s.circle((0,yc,10),radius)
  extrude(d,s.feat,name.upper(),length,mode=MID,expect_dv=math.pi*radius**2*length); save(d); close(j.sw,d)
 d=new_part(j.sw,OUT/'t6_contact.SLDPRT')
 with Sk(d,plane(d,'Z',10,'BLOCK_P'),'BLOCK') as s: s.rect((-20,-15,10),(20,15,10))
 extrude(d,s.feat,'BLOCK',20,mode=MID,expect_dv=24000); save(d)
 with Sk(d,plane(d,'Y',0,'HOLE_P'),'HOLE') as s: s.circle((0,0,10),5.1)
 extrude(d,s.feat,'HOLE',30,cut=True,mode=MID,expect_dv=math.pi*5.1**2*30); save(d)
 for name in ('t6_pin','t6_pad_left','t6_pad_right'):
  insert_body(d,OUT/(name+'.SLDPRT')); save(d)
 print('ASSEMBLY',bodies(d),bbox(d),feature_errors(d),flush=True)
 expect('four bodies',len(bodies(d)),4,0)
 save_as(d,OUT/'t6_contact.stl')
 close(j.sw,d); d=open_doc(j.sw,OUT/'t6_contact.SLDPRT'); d.ForceRebuild3(False)
 def getbody(key):
  hits=[b for b in solid_bodies(d) if key.lower() in b.Name.lower()]
  if len(hits)!=1: raise Failed('body lookup '+key+': '+str([b.Name for b in solid_bodies(d)]))
  return hits[0]
 def bodyfaces(key,fn): return [f for f in (call(getbody(key),'GetFaces') or []) if fn(face_info(f))]
 block=bodyfaces('HOLE',lambda i:i['kind']=='cyl' and abs(i['r']-5.1)<.01)
 pin=bodyfaces('t6_pin',lambda i:i['kind']=='cyl' and abs(i['r']-5)<.01)
 bottom=bodyfaces('HOLE',lambda i:i['kind']=='plane' and abs(i['box'][2])<.01 and abs(i['box'][5])<.01)
 ends=[]; pads=[]
 for side,name in [(-1,'t6_pad_left'),(1,'t6_pad_right')]:
  end=bodyfaces('t6_pin',lambda i:i['kind']=='plane' and abs(i['box'][1]-side*25)<.01 and abs(i['box'][4]-side*25)<.01)
  outer=bodyfaces(name,lambda i:i['kind']=='plane' and abs(i['box'][1]-side*27)<.01 and abs(i['box'][4]-side*27)<.01)
  expect('pin end',len(end),1,0); expect('pad outer',len(outer),1,0); ends.append(end); pads+=outer
 for n,fs in [('block hole',block),('pin cylinder',pin),('bottom',bottom)]: expect(n,len(fs),1,0)
 el=3.; print('PREDICT',12*(24000-math.pi*5.1**2*30+math.pi*5**2*50)/el**3*1.5,'nodes; displacement 0.2 mm; peak upper hole; nominal bearing',500/(10.2*30),flush=True)
 loads=[('remote',ends[0],(0,-25,10),(0,0,250),(0,0,0)),('remote',ends[1],(0,25,10),(0,0,250),(0,0,0))]
 r=static(j,d,'T6_PRESS',PETG,fixtures=[('fixed',bottom+pads)],loads=loads,el=el,ctrl=[(block,1.25),(pin,1.25)],contacts=[(NO_PENETRATION,block,pin)],materials={'t6_pin':STEEL,'t6_pad_left':pad,'t6_pad_right':pad},solver=SOLVER_DIRECT,loose_ok=True,max_nodes=199999)
 print('PREDICTION_CHECK',r.nodes,r.max_disp(),r.reaction,flush=True)
 if r.nodes>2*17000 or r.nodes<8500 or r.max_disp()>.6 or r.max_disp()<.2/3:
  print('STOP prediction mismatch: no stress read',flush=True)
 else:
  radii=np.sqrt(r.pos[:,0]**2+(r.pos[:,2]-10)**2)
  mask=(radii>=5.08)&(radii<5.35)&(np.abs(r.pos[:,1])<14.9)
  print('BLOCK HOLE PEAK',r.peak(mask),'all',float(r.vm.max()),flush=True)
  np.savez_compressed(RUN/'t6_press.npz',pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction)
