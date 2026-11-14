import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
from swfea import PETG,STEEL,NO_PENETRATION,SOLVER_DIRECT,static
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
pad=dict(name='Soft restraint pad',EX=.5e6,NUXY=.45,DENS=1000.,SIGYLD=1e6,SIGXT=1e6)
with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True);j.simulation();d=open_doc(j.sw,OUT/'housing_fea.SLDPRT');d.ForceRebuild3(False)
 mount=pick(d,kind='plane',at=(0,-32,3.5));anchors=[]
 for pt in [(22,0,3.5),(-22,0,3.5),(0,22,3.5),(0,-22,3.5)]:
  fs=pick(d,kind='plane',at=pt);print('anchor',pt,len(fs),flush=True);anchors+=fs
 ring_outer=pick(d,kind='cyl',r=26);seat=pick(d,kind='cyl',r=26.075)
 ring_inner=[f for f in pick(d,kind='cyl',r=24) if face_info(f)['area']>100]
 split_lower=pick(d,kind='plane',at=(35,-.3,3.5));split_upper=pick(d,kind='plane',at=(35,.3,3.5))
 print('COUNTS',len(mount),len(anchors),len(ring_outer),len(seat),len(ring_inner),len(split_lower),len(split_upper),flush=True)
 assert (len(mount),len(anchors),len(ring_outer),len(seat),len(ring_inner),len(split_lower),len(split_upper))==(1,4,1,2,1,1,1)
 for what,fs in [('outer',ring_outer),('seat',seat),('inner',ring_inner),('lower',split_lower),('upper',split_upper)]:print(what,[face_info(f) for f in fs],flush=True)
 print('PREDICT 60000 nodes, .12 mm displacement (0.075 mm radial clearance plus joint compliance), peak at upper screw/head or seat',flush=True)
 r=static(j,d,'CONTACT_Y',PETG,fixtures=[('fixed',mount),('fixed',anchors)],loads=[('remote',ring_inner,(0,0,3.5),(0,300,0),(0,0,0))],el=4,
  contacts=[(NO_PENETRATION,ring_outer,seat),(NO_PENETRATION,split_lower,split_upper)],materials={'ring':STEEL,'bolt':STEEL,'pad':pad},solver=SOLVER_DIRECT,max_nodes=199999)
 print('ACTUAL',r.nodes,r.max_disp(),r.reaction,flush=True)
 np.savez(OUT/'d2_contact_y.npz',pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction,fixed_pts=r.fixed_pts,loaded_pts=r.loaded_pts)
 if not (30000<r.nodes<120000 and .04<r.max_disp()<.36):print('STOP prediction failed; stresses not interpreted',flush=True)
 else: print('SUMMARY all bodies',r.summary(),flush=True)
 close(j.sw,d)
