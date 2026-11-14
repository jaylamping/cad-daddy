import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
from swfea import PETG,STEEL,NO_PENETRATION,BONDED,SOLVER_DIRECT,static,_arr
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
pad=dict(name='Soft restraint pad',EX=.5e6,NUXY=.45,DENS=1000.,SIGYLD=1e6,SIGXT=1e6)
def post(st,res): return _arr(res.GetReactionForcesAndMoments(0,NUL,0,L()),9)
with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True);j.simulation();d=open_doc(j.sw,OUT/'housing_fea.SLDPRT');d.ForceRebuild3(False)
 for name,vec,kind,pred in [('Y',(0,300,0),NO_PENETRATION,.159),('X',(300,0,0),NO_PENETRATION,.159),('BOND',(0,300,0),BONDED,.005)]:
  mount=pick(d,kind='plane',at=(0,-32,3.5));anchors=[]
  for pt in [(22,0,3.5),(-22,0,3.5),(0,22,3.5),(0,-22,3.5)]:anchors+=pick(d,kind='plane',at=pt)
  outer=pick(d,kind='cyl',r=26);seat=pick(d,kind='cyl',r=26.075)
  inner=[f for f in pick(d,kind='cyl',r=24) if face_info(f)['area']>100]
  lower=pick(d,kind='plane',at=(35,-.3,3.5))+pick(d,kind='plane',at=(-35,-.3,3.5))
  upper=pick(d,kind='plane',at=(35,.3,3.5))+pick(d,kind='plane',at=(-35,.3,3.5))
  print('COUNTS',name,len(mount),len(anchors),len(outer),len(seat),len(inner),len(lower),len(upper),flush=True)
  assert (len(mount),len(anchors),len(outer),len(seat),len(inner),len(lower),len(upper))==(1,4,1,2,1,2,2)
  print('PREDICT',name,'nodes 34670 displacement',pred,'mm, peak at upper screw/head or seat',flush=True)
  r=static(j,d,'FULL_'+name,PETG,fixtures=[('fixed',mount),('fixed',anchors)],loads=[('remote',inner,(0,0,3.5),vec,(0,0,0))],el=4,
   contacts=[(kind,outer,seat),(NO_PENETRATION,lower,upper)],materials={'ring':STEEL,'bolt':STEEL,'pad':pad},solver=SOLVER_DIRECT,max_nodes=199999,post=post)
  print('ACTUAL',name,r.nodes,r.max_disp(),r.reaction,flush=True)
  np.savez(OUT/('d2_full_'+name+'.npz'),pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction,reactions=r.extra,fixed_pts=r.fixed_pts,loaded_pts=r.loaded_pts)
  if not (17335<r.nodes<69340 and pred/3<r.max_disp()<pred*3):print('STOP prediction failed; stresses not interpreted',flush=True);break
  print('SOLVED',name,flush=True)
 close(j.sw,d)
