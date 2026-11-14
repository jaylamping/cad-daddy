import math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'

def box(j,name,lo,hi):
 d=new_part(j.sw,OUT/(name+'.SLDPRT')); z=(lo[2]+hi[2])/2
 with Sk(d,plane(d,'Z',z,name+'_P'),name) as s: s.rect((lo[0],lo[1],z),(hi[0],hi[1],z))
 extrude(d,s.feat,name,hi[2]-lo[2],mode=MID,expect_dv=(hi[0]-lo[0])*(hi[1]-lo[1])*(hi[2]-lo[2])); save(d)
 return d

def exp(j,d,name):
 for ext in ('stl','step'):
  save_as(d,OUT/(name+'.'+ext))

with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True)
 print('export preferences',[(i,j.sw.GetUserPreferenceToggle(i)) for i in (69,71)],[(i,j.sw.GetUserPreferenceIntegerValue(i)) for i in (211,78,75)],flush=True)
 d=box(j,'buck_mount',(-52.5,-30,0),(52.5,30,4))
 with Sk(d,plane(d,'Z',2,'WINDOW_P'),'WINDOW') as s:
  s.rect((-35,-25,2),(35,-5,2)); s.rect((-35,5,2),(35,25,2))
 extrude(d,s.feat,'WINDOW',4,cut=True,mode=MID,expect_dv=2*70*20*4); save(d)
 with Sk(d,plane(d,'Z',6,'POST_P'),'POST') as s:
  for x in (-39,39):
   for y in (-26.5,26.5): s.circle((x,y,6),3)
 extrude(d,s.feat,'POST',4,mode=MID,expect_dv=4*math.pi*9*4); save(d)
 with Sk(d,plane(d,'Z',4,'BOARD_HOLE_P'),'BOARD_HOLES') as s:
  for x in (-39,39):
   for y in (-26.5,26.5): s.circle((x,y,4),1.6)
 extrude(d,s.feat,'BOARD_HOLES',8,cut=True,mode=MID,expect_dv=4*math.pi*1.6**2*8); save(d)
 with Sk(d,plane(d,'Z',2,'RAIL_HOLE_P'),'RAIL_HOLES') as s:
  for x in (-47,47): s.circle((x,0,2),2.75)
 extrude(d,s.feat,'RAIL_HOLES',4,cut=True,mode=MID,expect_dv=2*math.pi*2.75**2*4); save(d)
 print('MODEL',volume(d),bbox(d),bodies(d),'errors',feature_errors(d),flush=True); single_body(d); exp(j,d,'buck_mount'); close(j.sw,d)
 d=box(j,'board_standin',(-42.5,-30,8),(42.5,30,9.6)); exp(j,d,'board_standin');close(j.sw,d)
 d=box(j,'rail_standin',(-60,-10,-20),(60,10,0)); exp(j,d,'rail_standin');close(j.sw,d)
 # Different concept: two independent support rails, represented as two bodies in one part.
 d=box(j,'idea_rails',(-42.5,-30,0),(42.5,-23,8))
 with Sk(d,plane(d,'Z',4,'ALT_P'),'ALT') as s: s.rect((-42.5,23,4),(42.5,30,4))
 extrude(d,s.feat,'ALT',8,mode=MID,expect_dv=85*7*8);save(d); exp(j,d,'idea_rails');close(j.sw,d)
