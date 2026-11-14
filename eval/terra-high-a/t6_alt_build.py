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
 for name,yc,length,radius in [('t6c_pin',0,50,5),('t6c_pad_left',-26,2,2.5),('t6c_pad_right',26,2,2.5)]:
  d=new_part(j.sw,OUT/(name+'.SLDPRT'))
  with Sk(d,plane(d,'Y',yc,name+'_P'),name.upper()) as s: s.circle((0,yc,10),radius)
  extrude(d,s.feat,name.upper(),length,mode=MID,expect_dv=math.pi*radius**2*length); save(d); close(j.sw,d)
 d=new_part(j.sw,OUT/'t6c_contact.SLDPRT')
 with Sk(d,plane(d,'Z',10,'BLOCK_P'),'BLOCK') as s: s.rect((-20,-15,10),(20,15,10))
 extrude(d,s.feat,'BLOCK',20,mode=MID,expect_dv=24000); save(d)
 with Sk(d,plane(d,'Y',0,'HOLE_P'),'HOLE') as s: s.circle((0,0,10),5.1)
 extrude(d,s.feat,'HOLE',30,cut=True,mode=MID,expect_dv=math.pi*5.1**2*30); save(d)
 for name in ('t6c_pin','t6c_pad_left','t6c_pad_right'):
  insert_body(d,OUT/(name+'.SLDPRT')); save(d)
 print('ASSEMBLY',bodies(d),bbox(d),feature_errors(d),flush=True)
 expect('four bodies',len(bodies(d)),4,0)
 save_as(d,OUT/'t6c_contact.stl')
 close(j.sw,d)
