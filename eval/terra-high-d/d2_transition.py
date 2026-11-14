import math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d';a=.3
def seg(r):return math.pi*r*r/2-(a*math.sqrt(r*r-a*a)+r*r*math.asin(a/r))
with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True)
 for name in ('housing_upper','housing_lower'):
  d=open_doc(j.sw,OUT/(name+'_round.SLDPRT'));save_as(d,OUT/(name+'_transition.SLDPRT'))
  for idx,z in enumerate((.60,6.40)):
   with Sk(d,plane(d,'Z',z,'DEEPER_P'+str(idx)),'DEEPER'+str(idx)) as s:s.circle((0,0,z),26.5)
   extrude(d,s.feat,'DEEPER'+str(idx),.5,cut=True,mode=MID,expect_dv=(seg(26.5)-seg(26.075))*.5);save(d)
  edges=edges_where(d,lambda p: abs(math.hypot(p[0],p[1])-26.5)<.02 and min(abs(p[2]-.85),abs(p[2]-6.15))<.02)
  print(name,'transition edges',len(edges),flush=True);assert len(edges)==2
  v=volume(d);chamfer(d,edges,.3,'SEAT_TRANSITION');print('transition volume delta',volume(d)-v,flush=True)
  print('MEASURE',name,volume(d),bbox(d),feature_errors(d),bodies(d),flush=True);single_body(d);save(d);save_as(d,OUT/(name+'_transition.stl'));close(j.sw,d)
