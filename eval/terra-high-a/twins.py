import sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(ROOT/'tools/solidworks'))
import swkit as k
from swkit import *
k.pin_export_prefs=lambda sw: None
OUT=ROOT/'cad/_wip/sw-eval/terra-high-a'
with job(wait_s=1800) as j:
 d=open_doc(j.sw,OUT/'bracket.SLDPRT'); save_as(d,OUT/'bracket_load_twin.SLDPRT')
 with Sk(d,plane(d,'X',.05,'MOTOR_FACE_P'),'MOTOR_FACE') as s:
  for a in (45,135,225,315): s.circle((.05,25+15.5*math.cos(math.radians(a)),28+15.5*math.sin(math.radians(a))),4)
 extrude(d,s.feat,'MOTOR_FACE',.1,cut=True,mode=MID,expect_dv=4*math.pi*(4**2-1.7**2)*.1); save(d)
 print('LOAD_TWIN',volume(d),bbox(d),bodies(d),feature_errors(d),flush=True)
 save_as(d,OUT/'bracket_load_twin.stl')
 save_as(d,OUT/'bracket_support_twin.SLDPRT')
 with Sk(d,plane(d,'Z',5.95,'WASHER_FACE_P'),'WASHER_FACE') as s:
  for x in (25,65):
   for y in (10,40): s.circle((x,y,5.95),4)
 extrude(d,s.feat,'WASHER_FACE',.1,cut=True,mode=MID,expect_dv=4*math.pi*(4**2-2.75**2)*.1); save(d)
 print('SUPPORT_TWIN',volume(d),bbox(d),bodies(d),feature_errors(d),flush=True)
 save_as(d,OUT/'bracket_support_twin.stl')
