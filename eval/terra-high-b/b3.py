import sys,math,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
from swfea import PETG,static
OUT=ROOT/'cad/_wip/sw-eval/terra-high-b'
print('B3 start',time.ctime(),flush=True)
with job(wait_s=1800) as j:
 j.simulation(); d=open_doc(j.sw,OUT/'wall_bracket.SLDPRT'); d.ForceRebuild3(False)
 save_as(d,OUT/'wall_bracket_light.SLDPRT')
 with Sk(d,plane(d,'X',2.5,'TRIM_P'),'TRIM') as s:
  s.rect((2.5,-1,-1),(2.5,13,61)); s.rect((2.5,27,-1),(2.5,41,61))
 extrude(d,s.feat,'TRIM',5,mode=MID,cut=True,expect_dv=2*13*60*5); save(d)
 print('light volume',volume(d),'box',bbox(d),'bodies',bodies(d),'errors',feature_errors(d),flush=True)
 save_as(d,OUT/'wall_bracket_light.stl'); save_as(d,OUT/'wall_bracket_light_twin.SLDPRT')
 with Sk(d,plane(d,'Z',51.975,'STEP_P'),'STEP') as s: s.rect((5,15,51.975),(55,25,51.975))
 extrude(d,s.feat,'STEP',0.05,mode=MID,cut=True,min_dv=.01); save(d)
 for size in (4.,3.,2.4):
  fix=pick(d,kind='cyl',r=2.25); load=pick(d,kind='plane',at=(60,20,52))
  print('picks',len(fix),len(load),'predicted nodes',round(12*volume(d)/size**3),'displacement 1.22 mm plus plate flex; peak near root',flush=True)
  if len(fix)!=2 or len(load)!=1: raise RuntimeError('unexpected picks')
  r=static(j,d,'B3_'+str(size).replace('.','_'),PETG,fixtures=[('fixed',fix)],loads=[('normal',load,60.)],el=size,max_nodes=199999)
  print('RESULT',size,'nodes',len(r.pos),'reaction',r.reaction,'disp',r.max_disp(),'summary',r.summary(),'raw',float(r.vm.max()),flush=True)
  for n in ((1,0,0),(0,1,0),(0,0,1)): print('LAYERS',n,r.layer_stress(n),r.layer_shear(n),flush=True)
 print('B3 end',time.ctime(),flush=True)
