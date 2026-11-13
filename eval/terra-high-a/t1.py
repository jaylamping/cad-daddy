import sys, math, json, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'tools/solidworks'))
import swkit as k
from swkit import *
k.pin_export_prefs=lambda sw: None  # User forbids changing machine-wide preferences.
OUT=ROOT/'cad/_wip/sw-eval/terra-high-a'
RUN=Path(__file__).resolve().parent

def main():
 with job(wait_s=1800) as j:
  d=new_part(j.sw,OUT/'bracket.SLDPRT')
  with Sk(d,plane(d,'Z',3,'BASE_P'),'BASE') as s: s.rect((0,0,3),(80,50,3))
  extrude(d,s.feat,'BASE',6,mode=MID,expect_dv=24000); save(d)
  with Sk(d,plane(d,'X',3,'UP_P'),'UPRIGHT') as s: s.rect((3,0,6),(3,50,46))
  extrude(d,s.feat,'UPRIGHT',6,mode=MID,expect_dv=12000); save(d)
  edges=edges_where(d,lambda p: abs(p[0]-6)<.01 and abs(p[2]-6)<.01)
  expect('inside edge',len(edges),1,0)
  if fillet(d,edges,(4,), 'ROOT_R4') is None: raise Failed('root fillet')
  save(d)
  edges=edges_where(d,lambda p: abs(p[0]-80)<.01 and (abs(p[1])<.01 or abs(p[1]-50)<.01))
  expect('base corner edges',len(edges),2,0)
  if fillet(d,edges,(5,), 'BASE_R5') is None: raise Failed('base rounds')
  save(d)
  edges=edges_where(d,lambda p: abs(p[2]-46)<.01 and (abs(p[1])<.01 or abs(p[1]-50)<.01))
  expect('top corner edges',len(edges),2,0)
  if fillet(d,edges,(5,), 'TOP_R5') is None: raise Failed('top rounds')
  save(d)
  with Sk(d,plane(d,'Z',3,'BASE_HOLES_P'),'BASE_HOLES') as s:
   for x in (25,65):
    for y in (10,40): s.circle((x,y,3),2.75)
  extrude(d,s.feat,'BASE_HOLES',6,cut=True,mode=MID,expect_dv=4*math.pi*2.75**2*6); save(d)
  with Sk(d,plane(d,'X',3,'MOTOR_P'),'MOTOR_HOLES') as s:
   s.circle((3,25,28),11)
   for a in (45,135,225,315):
    s.circle((3,25+15.5*math.cos(math.radians(a)),28+15.5*math.sin(math.radians(a))),1.7)
  extrude(d,s.feat,'MOTOR_HOLES',6,cut=True,mode=MID,expect_dv=math.pi*(11**2+4*1.7**2)*6); save(d)
  for radius in (2.75,11,1.7):
   fs=pick(d,kind='cyl',r=radius); print('HOLES',radius,len(fs),[face_info(f) for f in fs],flush=True)
  print('BODIES',bodies(d),'BOX',bbox(d),'ERRORS',feature_errors(d),flush=True)
  hand=36000+(1-math.pi/4)*16*50-2*(1-math.pi/4)*25*6-2*(1-math.pi/4)*25*6-4*math.pi*2.75**2*6-math.pi*(11**2+4*1.7**2)*6
  print('HAND',hand,'VOLUME',volume(d),flush=True)
  for suffix in ('step','stl'):
   save_as(d,OUT/('bracket.'+suffix))
  print('EXPORTS DONE',flush=True)
  data={'volume_mm3':volume(d),'hand_volume_mm3':hand,'mass_g':volume(d)*.00119,'bbox_mm':bbox(d),'bodies':len(bodies(d)),'stl_watertight':None,'stl_volume_mm3':None,'status':'partial','notes':'Exports use existing machine settings; checks pending.'}
  (RUN/'t1.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
if __name__=='__main__': main()
