import sys,math,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
from swfea import PETG,static,NO_PENETRATION,SOLVER_DIRECT
OUT=ROOT/'cad/_wip/sw-eval/terra-high-b'
print('B4 start',time.ctime(),flush=True)
def block(j,name,lo,hi):
 d=new_part(j.sw,OUT/(name+'.SLDPRT')); z=(lo[2]+hi[2])/2
 with Sk(d,plane(d,'Z',z,name+'_P'),name) as s: s.rect((lo[0],lo[1],z),(hi[0],hi[1],z))
 extrude(d,s.feat,name,hi[2]-lo[2],mode=MID,expect_dv=(hi[0]-lo[0])*(hi[1]-lo[1])*(hi[2]-lo[2])); save(d); return d
with job(wait_s=1800) as j:
 j.simulation()
 d=block(j,'tongue',(-4,-10,8.1),(4,10,40)); save_as(d,OUT/'tongue.stl'); close(j.sw,d)
 d=block(j,'slot_block',(-20,-10,0),(20,10,20))
 with Sk(d,plane(d,'Y',0,'SLOT_P'),'SLOT') as s: s.rect((-4.1,0,8),(4.1,0,20.2))
 extrude(d,s.feat,'SLOT',20,mode=MID,cut=True,expect_dv=8.2*20*12); save(d); save_as(d,OUT/'slot_block.stl'); close(j.sw,d)
 # Two small soft supports, outside the slot, fixed at their outer faces.
 for name,lo,hi in [('pad_a',(-3,10,24),(-1,11,26)),('pad_b',(1,-11,24),(3,-10,26))]:
  d=block(j,name,lo,hi); close(j.sw,d)
 d=open_doc(j.sw,OUT/'slot_block.SLDPRT'); save_as(d,OUT/'tongue_slot_analysis.SLDPRT')
 insert_body(d,OUT/'tongue.SLDPRT'); insert_body(d,OUT/'pad_a.SLDPRT'); insert_body(d,OUT/'pad_b.SLDPRT'); save(d)
 print('analysis bodies',bodies(d),flush=True)
 # A groove above the slot divides the load face; contact geometry remains unchanged.
 with Sk(d,plane(d,'Y',0,'GROOVE_P'),'GROOVE') as s: s.rect((-4.05,0,29.9),(-3.9,0,30.1))
 extrude(d,s.feat,'GROOVE',20,mode=MID,cut=True,min_dv=.01); save(d)
 fix=pick(d,kind='plane',at=(0,0,0)); pa=pick(d,kind='plane',at=(-2,11,25)); pb=pick(d,kind='plane',at=(2,-11,25))
 load=pick(d,kind='plane',at=(-4,0,35)); left_block=pick(d,kind='plane',at=(-4.1,0,14)); right_block=pick(d,kind='plane',at=(4.1,0,14)); left_tongue=pick(d,kind='plane',at=(-4,0,14)); right_tongue=pick(d,kind='plane',at=(4,0,14))
 print('face counts',*[len(x) for x in (fix,pa,pb,load,left_block,right_block,left_tongue,right_tongue)],flush=True)
 if any(len(x)!=1 for x in (fix,pa,pb,load,left_block,right_block,left_tongue,right_tongue)): raise RuntimeError('unexpected face count')
 pad=dict(name='Soft pad',EX=10000.,NUXY=.4,DENS=1000.,SIGYLD=1e6,SIGXT=1e6)
 print('prediction: rough wall reactions +180 and -260 N (assumed 12 mm contact arm); node estimate 26000; displacement order 0.1 mm plus bending; peak block at slot wall',flush=True)
 r=static(j,d,'B4_CONTACT',PETG,fixtures=[('fixed',fix),('fixed',pa+pb)],loads=[('normal',load,80.)],el=3.,ctrl=[(left_block+right_block+left_tongue+right_tongue,1.5)],contacts=[(NO_PENETRATION,left_block,left_tongue),(NO_PENETRATION,right_block,right_tongue)],materials={'pad_a':pad,'pad_b':pad},solver=SOLVER_DIRECT,loose_ok=True,max_nodes=199999)
 import numpy as np
 np.savez_compressed(OUT/'b4_result.npz',pos=r.pos,stress=r.s,disp=r.disp,vm=r.vm)
 print('RESULT',r.summary(),'reaction',r.reaction,'peak',r.peak(),'maxdisp',r.max_disp(),flush=True)
 print('B4 end',time.ctime(),flush=True)
