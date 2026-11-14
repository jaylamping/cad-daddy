import sys, math
from pathlib import Path
sys.path.insert(0,str(Path('tools/solidworks').resolve()))
import swkit as k
from swkit import *
from swfea import *
k.pin_export_prefs=lambda sw:None
out=Path('cad/_wip/sw-eval/terra-high-b2').resolve(); run=Path('tools/solidworks/playbook/eval/terra-high-b2').resolve()
pad=dict(name='Soft pad',EX=0.5e6,NUXY=0.45,DENS=1000.,SIGYLD=1e6,SIGXT=1e6)
with job(wait_s=1800) as j:
 for name,lo,hi in [('tongue',(-4,-10,8.1),(4,10,40)),('pad',(4,-2,24),(6,2,27)),('slot_block',(-20,-10,0),(20,10,20))]:
  d=new_part(j.sw,out/(name+'.SLDPRT')); z=(lo[2]+hi[2])/2
  with Sk(d,plane(d,'Z',z,name.upper()+'_P'),name.upper()) as s: s.rect((lo[0],lo[1],z),(hi[0],hi[1],z))
  extrude(d,s.feat,name.upper(),hi[2]-lo[2],mode=MID,expect_dv=math.prod(hi[i]-lo[i] for i in range(3))); save(d)
  if name=='tongue':
   with Sk(d,plane(d,'X',-3.975,'LOAD_P'),'LOAD_SPLIT') as s: s.rect((-3.975,-10,29.9),(-3.975,10,30))
   extrude(d,s.feat,'LOAD_SPLIT',.05,cut=True,mode=MID,min_dv=.001); save(d)
  if name=='slot_block':
   with Sk(d,plane(d,'Y',0,'SLOT_P'),'SLOT') as s: s.rect((-4.1,0,8),(4.1,0,20.1))
   extrude(d,s.feat,'SLOT',20,cut=True,mode=MID,expect_dv=8.2*12*20); save(d)
   insert_body(d,out/'tongue.SLDPRT'); insert_body(d,out/'pad.SLDPRT'); save(d)
   print('BODIES',bodies(d),'errors',feature_errors(d),flush=True)
  if name in ('tongue','slot_block'): save_as(d,out/(name+'.stl'))
  close(j.sw,d)
 j.simulation(); d=open_doc(j.sw,out/'slot_block.SLDPRT'); d.ForceRebuild3(False)
 def one(at,normal):
  fs=pick(d,kind='plane',at=at,normal=normal); print('PICK',at,normal,len(fs),flush=True)
  if len(fs)!=1: raise Failed('unexpected face count')
  return fs
 bottom=one((0,0,0),(0,0,-1)); padfix=one((6,0,25),(1,0,0)); load=one((-4,0,35),(-1,0,0))
 left=one((-4.1,0,14),(1,0,0)); right=one((4.1,0,14),(-1,0,0)); tl=one((-4,0,14),(-1,0,0)); tr=one((4,0,14),(1,0,0))
 print('PREDICT nodes 8500, tip displacement order 1 mm, peak slot wall corners; hand forces lower +100 N upper -180 N',flush=True)
 r=static(j,d,'SLOT_80N',PETG,fixtures=[('fixed',bottom),('fixed',padfix)],loads=[('normal',load,80)],el=3.,contacts=[(NO_PENETRATION,left,tl),(NO_PENETRATION,right,tr)],materials={'pad':pad},solver=SOLVER_DIRECT,max_nodes=199999,loose_ok=True)
 print('RESULT',r.summary(),'all',float(r.vm.max()),flush=True)
 np.savez_compressed(run/'b4_results.npz',pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction)

