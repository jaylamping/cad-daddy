import sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(ROOT/'tools/solidworks'))
import swkit as k
from swkit import *
k.pin_export_prefs=lambda sw: None
OUT=ROOT/'cad/_wip/sw-eval/terra-high-a'
with job(wait_s=1800) as j:
 d=open_doc(j.sw,OUT/'bracket.SLDPRT'); save_as(d,OUT/'bracket_reinforced.SLDPRT')
 with Sk(d,plane(d,'X',7,'DOUBLER_P'),'DOUBLER') as s:
  s.rect((7,10,12),(7,40,44)); s.circle((7,25,28),11)
  for a in (45,135,225,315): s.circle((7,25+15.5*math.cos(math.radians(a)),28+15.5*math.sin(math.radians(a))),1.7)
 add=2*(30*32-math.pi*(11**2+4*1.7**2))
 extrude(d,s.feat,'DOUBLER',2,mode=MID,expect_dv=add); save(d)
 print('REINFORCED',volume(d),bbox(d),bodies(d),feature_errors(d),'hand_added',add,flush=True)
 for r in (11,1.7): print('HOLES',r,[face_info(f) for f in pick(d,kind='cyl',r=r)],flush=True)
 save_as(d,OUT/'bracket_reinforced.stl')
 save_as(d,OUT/'bracket_reinforced_load.SLDPRT')
 with Sk(d,plane(d,'X',.05,'MOTOR_FACE_P2'),'MOTOR_FACE2') as s:
  for a in (45,135,225,315): s.circle((.05,25+15.5*math.cos(math.radians(a)),28+15.5*math.sin(math.radians(a))),4)
 extrude(d,s.feat,'MOTOR_FACE2',.1,cut=True,mode=MID,expect_dv=4*math.pi*(4**2-1.7**2)*.1); save(d)
 print('TWIN',volume(d),bbox(d),bodies(d),feature_errors(d),flush=True)
 save_as(d,OUT/'bracket_reinforced_load.stl')
