import sys,math,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
from swfea import PETG,static
OUT=ROOT/'cad/_wip/sw-eval/terra-high-b'
print('B2 start',time.ctime(),flush=True)
with job(wait_s=1800) as j:
 j.simulation()
 d=new_part(j.sw,OUT/'wall_bracket.SLDPRT')
 with Sk(d,plane(d,'X',2.5,'PLATE_P'),'PLATE') as s: s.rect((2.5,0,0),(2.5,40,60))
 extrude(d,s.feat,'PLATE',5,mode=MID,expect_dv=12000); save(d)
 with Sk(d,plane(d,'X',35,'ARM_P'),'ARM') as s: s.rect((35,15,40),(35,25,52))
 extrude(d,s.feat,'ARM',60,mode=MID,expect_dv=7200); save(d)
 with Sk(d,plane(d,'X',2.5,'HOLES_P'),'HOLES') as s:
  for z in (12,48): s.circle((2.5,20,z),2.25)
 extrude(d,s.feat,'HOLES',5,mode=MID,cut=True,expect_dv=2*math.pi*2.25**2*5); save(d)
 edges=edges_where(d,lambda p: abs(p[0]-5)<0.01 and min(abs(p[2]-40),abs(p[2]-52))<0.01)
 print('fillet edges',len(edges),flush=True)
 if len(edges)!=2: raise RuntimeError('Expected 2 arm root edges')
 if fillet(d,edges,(3.,),'ROOT_ROUNDS') is None: raise RuntimeError('fillet failed')
 save(d)
 print('B2 model volume',volume(d),'box',bbox(d),'bodies',bodies(d),'errors',feature_errors(d),flush=True)
 save_as(d,OUT/'wall_bracket.stl')
 # Analysis twin: a 0.05 mm step splits the top surface to expose the specified 10 mm load patch.
 save_as(d,OUT/'wall_bracket_load_twin.SLDPRT')
 with Sk(d,plane(d,'Z',51.975,'STEP_P'),'STEP') as s: s.rect((5,15,51.975),(55,25,51.975))
 extrude(d,s.feat,'STEP',0.05,mode=MID,cut=True,min_dv=0.01); save(d)
 print('analysis twin volume',volume(d),flush=True)
 d.ForceRebuild3(False)
 for size in (4.0,3.0,2.4):
  fix=pick(d,kind='cyl',r=2.25); load=pick(d,kind='plane',at=(60,20,52))
  print('picks',len(fix),len(load),'prediction nodes',round(12*volume(d)/size**3),'hand displacement 0.423 mm peak root near x5',flush=True)
  if len(fix)!=2 or len(load)!=1: raise RuntimeError('unexpected picks')
  r=static(j,d,'B2_'+str(size).replace('.','_'),PETG,fixtures=[('fixed',fix)],loads=[('normal',load,60.)],el=size,max_nodes=199999)
  print('RESULT',size,'nodes',len(r.pos),'reaction',r.reaction,'disp',r.max_disp(),'summary',r.summary(),'peak',r.peak(),'raw',float(r.vm.max()),flush=True)
  for n in ((1,0,0),(0,1,0),(0,0,1)):
   print('LAYERS',n,r.layer_stress(n),r.layer_shear(n),flush=True)
 print('B2 end',time.ctime(),flush=True)
