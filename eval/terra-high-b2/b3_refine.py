import sys
from pathlib import Path
sys.path.insert(0,str(Path('tools/solidworks').resolve()))
import swkit as k
from swkit import *
from swfea import *
k.pin_export_prefs=lambda sw:None
out=Path('cad/_wip/sw-eval/terra-high-b2').resolve(); run=Path('tools/solidworks/playbook/eval/terra-high-b2').resolve()
with job(wait_s=1800) as j:
 j.simulation(); d=open_doc(j.sw,out/'bracket_light_study.SLDPRT'); d.ForceRebuild3(False)
 for name,el,support in [('FINE',1.2,'holes'),('WALL',2.0,'wall')]:
  fix=pick(d,kind='cyl',r=2.25) if support=='holes' else pick(d,kind='plane',normal=(-1,0,0),at=(0,14,30))
  load=pick(d,kind='plane',at=(60,20,52),normal=(0,0,1))
  print('PREDICT',name,'nodes',12*11280/el**3,'disp 1.10 mm peak arm root, hole edges',len(fix),len(load),flush=True)
  r=static(j,d,'B3_'+name,PETG,fixtures=[('fixed',fix)],loads=[('normal',load,60)],el=el,max_nodes=199999,loose_ok=True)
  mask=r.away(dist=3); print('RESULT',r.summary(mask=mask),'all',float(r.vm.max()),'layers',[(n,r.layer_stress(n,mask),r.layer_shear(n,mask)) for n in ((1,0,0),(0,1,0),(0,0,1))],flush=True)
  np.savez_compressed(run/('b3_14_'+name+'.npz'),pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction)

