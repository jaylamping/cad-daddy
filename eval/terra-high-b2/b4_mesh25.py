import sys
from pathlib import Path
sys.path.insert(0,str(Path('tools/solidworks').resolve()))
import swkit as k
from swkit import *
from swfea import *
k.pin_export_prefs=lambda sw:None
out=Path('cad/_wip/sw-eval/terra-high-b2').resolve(); run=Path('tools/solidworks/playbook/eval/terra-high-b2').resolve()
pad=dict(name='Softer pad',EX=0.01e6,NUXY=0.45,DENS=1000.,SIGYLD=1e6,SIGXT=1e6)
with job(wait_s=1800) as j:
 j.simulation(); d=open_doc(j.sw,out/'slot_block.SLDPRT'); d.ForceRebuild3(False)
 def one(at,n):
  fs=pick(d,kind='plane',at=at,normal=n)
  if len(fs)!=1: raise Failed(f'bad pick {at}: {len(fs)}')
  return fs
 for name,el,F in [('MESH25',2.5,80.)]:
  bottom=one((0,0,0),(0,0,-1)); padfix=one((6,0,25),(1,0,0)); load=one((-4,0,35),(-1,0,0))
  left=one((-4.1,0,14),(1,0,0)); right=one((4.1,0,14),(-1,0,0)); tl=one((-4,0,14),(-1,0,0)); tr=one((4,0,14),(1,0,0))
  print('PREDICT',name,'nodes',10510*(3/el)**3,'displacement mm',0.1 if F<1 else .9,'peak slot upper corner; expected wall forces ~100,180 N',flush=True)
  r=static(j,d,'SLOT_'+name,PETG,fixtures=[('fixed',bottom),('fixed',padfix)],loads=[('normal',load,F)],el=el,contacts=[(NO_PENETRATION,left,tl),(NO_PENETRATION,right,tr)],materials={'pad':pad},solver=SOLVER_DIRECT,max_nodes=199999,loose_ok=True)
  print('DISPLACEMENT',r.max_disp(),flush=True)
  if r.max_disp()>2.7: raise Failed('unexpected displacement: contact failed, do not read stress')
  print('RESULT',r.summary(),'all',float(r.vm.max()),flush=True)
  np.savez_compressed(run/('b4_'+name+'.npz'),pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction)


