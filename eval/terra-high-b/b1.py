import sys, math, json, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
OUT=ROOT/'cad/_wip/sw-eval/terra-high-b'
print('B1 start',time.ctime(),flush=True)
with job(wait_s=1800) as j:
 d=new_part(j.sw, OUT/'hub.SLDPRT')
 with Sk(d,plane(d,'Z',2.5,'FLANGE_P'),'FLANGE') as s: s.circle((0,0,2.5),30)
 extrude(d,s.feat,'FLANGE',5,mode=MID,expect_dv=math.pi*30**2*5); save(d)
 with Sk(d,plane(d,'Z',15,'BOSS_P'),'BOSS') as s: s.circle((0,0,15),13)
 extrude(d,s.feat,'BOSS',20,mode=MID,expect_dv=math.pi*13**2*20); save(d)
 with Sk(d,plane(d,'Z',12.5,'BORE_P'),'BORE') as s: s.circle((0,0,12.5),5)
 extrude(d,s.feat,'BORE',25,mode=MID,cut=True,expect_dv=math.pi*25*25); save(d)
 with Sk(d,plane(d,'Z',2.5,'BOLTS_P'),'BOLTS') as s:
  for i in range(6):
   a=i*math.pi/3; s.circle((22*math.cos(a),22*math.sin(a),2.5),2.25)
  for y in [-15,15]: s.circle((0,y,2.5),2.75)
 extrude(d,s.feat,'BOLTS',5,mode=MID,cut=True,expect_dv=5*math.pi*(6*2.25**2+2*2.75**2)); save(d)
 with Sk(d,plane(d,'Z',12.5,'KEY_P'),'KEY') as s: s.rect((4,-1.5,12.5),(6.4,1.5,12.5))
 extrude(d,s.feat,'KEY',25,mode=MID,cut=True); save(d)
 with Sk(d,plane(d,'Y',7,'SCREW_P'),'SCREW') as s: s.circle((0,7,22.6),2)
 extrude(d,s.feat,'SCREW',14,mode=MID,cut=True); save(d)
 print('B1 volume',volume(d),'box',bbox(d),'bodies',bodies(d),'errors',feature_errors(d),flush=True)
 for r in [5,2.25,2.75,2]:
  fs=pick(d,kind='cyl',r=r); print('RADIUS',r,'COUNT',len(fs),'FACES',[face_info(f) for f in fs],flush=True)
 # Use existing machine export preferences; user prohibits changing shared settings.
 save_as(d,OUT/'hub.step'); save_as(d,OUT/'hub.stl')
 print('B1 end',time.ctime(),flush=True)

