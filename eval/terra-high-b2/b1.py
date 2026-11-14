import sys, math, json
from pathlib import Path
sys.path.insert(0, str(Path('tools/solidworks').resolve()))
import swkit as k
from swkit import *
k.pin_export_prefs = lambda sw: None  # user prohibits changing shared machine settings
out=Path('cad/_wip/sw-eval/terra-high-b2').resolve()
with job(wait_s=1800) as j:
 d=new_part(j.sw,out/'hub.SLDPRT')
 with Sk(d,plane(d,'Z',2.5,'FLANGE_P'),'FLANGE') as s: s.circle((0,0,2.5),30)
 extrude(d,s.feat,'FLANGE',5,mode=MID,expect_dv=math.pi*30**2*5); save(d)
 with Sk(d,plane(d,'Z',15,'BOSS_P'),'BOSS') as s: s.circle((0,0,15),13)
 extrude(d,s.feat,'BOSS',20,mode=MID,expect_dv=math.pi*13**2*20); save(d)
 with Sk(d,plane(d,'Z',12.5,'BORE_P'),'BORE') as s: s.circle((0,0,12.5),5)
 extrude(d,s.feat,'BORE',25,cut=True,mode=MID,expect_dv=math.pi*25*25); save(d)
 with Sk(d,plane(d,'Z',2.5,'BOLTS_P'),'BOLTS') as s:
  for i in range(6):
   a=i*math.pi/3; s.circle((22*math.cos(a),22*math.sin(a),2.5),2.25)
 extrude(d,s.feat,'BOLTS',5,cut=True,mode=MID,expect_dv=6*math.pi*2.25**2*5); save(d)
 with Sk(d,plane(d,'Z',2.5,'DOWELS_P'),'DOWELS') as s:
  for y in [-15,15]: s.circle((0,y,2.5),2.75)
 extrude(d,s.feat,'DOWELS',5,cut=True,mode=MID,expect_dv=2*math.pi*2.75**2*5); save(d)
 with Sk(d,plane(d,'Z',12.5,'KEY_P'),'KEY') as s: s.rect((4, -1.5,12.5),(6.4,1.5,12.5))
 extrude(d,s.feat,'KEY',25,cut=True,mode=MID); save(d)
 with Sk(d,plane(d,'Y',6.5,'SCREW_P'),'SCREW') as s: s.circle((0,6.5,22.6),2)
 extrude(d,s.feat,'SCREW',13,cut=True,mode=MID); save(d)
 print('VOLUME',volume(d),'BOX',bbox(d),'BODIES',bodies(d),'ERRORS',feature_errors(d),flush=True)
 for radius in [5,2.25,2.75,2]:
  print('FACES',radius,[face_info(f) for f in pick(d,kind='cyl',r=radius)],flush=True)
 save_as(d,out/'hub.step'); save_as(d,out/'hub.stl')
