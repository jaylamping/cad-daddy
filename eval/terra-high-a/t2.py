import sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(ROOT/'tools/solidworks'))
import swkit as k
from swkit import *
k.pin_export_prefs=lambda sw: None
OUT=ROOT/'cad/_wip/sw-eval/terra-high-a'
with job(wait_s=1800) as j:
 d=open_doc(j.sw,OUT/'bracket.SLDPRT'); save_as(d,OUT/'bracket_b.SLDPRT')
 with Sk(d,plane(d,'Z',4.5,'CB_P'),'COUNTERBORES') as s:
  for x in (25,65):
   for y in (10,40): s.circle((x,y,4.5),5)
 extrude(d,s.feat,'COUNTERBORES',3,cut=True,mode=MID,expect_dv=4*math.pi*(25-2.75**2)*3); save(d)
 with Sk(d,plane(d,'Z',3,'SLOT_P'),'SLOT_RECT') as s: s.rect((38,22,3),(52,28,3))
 extrude(d,s.feat,'SLOT_RECT',6,cut=True,mode=MID,expect_dv=14*6*6); save(d)
 for x in (38,52):
  with Sk(d,plane(d,'Z',3,'END_P'+str(x)),'SLOT_END'+str(x)) as s: s.circle((x,25,3),3)
  extrude(d,s.feat,'SLOT_END'+str(x),6,cut=True,mode=MID,expect_dv=math.pi*9*3); save(d)
 print('CB FACES', [face_info(f) for f in pick(d,kind='cyl',r=5)],flush=True)
 print('RESULT',volume(d),bbox(d),bodies(d),feature_errors(d),flush=True)
 save_as(d,OUT/'bracket_b.stl')
