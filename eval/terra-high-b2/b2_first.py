import sys, math, json
from pathlib import Path
sys.path.insert(0,str(Path('tools/solidworks').resolve()))
import swkit as k
from swkit import *
from swfea import *
k.pin_export_prefs=lambda sw:None
out=Path('cad/_wip/sw-eval/terra-high-b2').resolve(); run=Path('tools/solidworks/playbook/eval/terra-high-b2').resolve()
with job(wait_s=1800) as j:
 d=new_part(j.sw,out/'wall_bracket.SLDPRT')
 with Sk(d,plane(d,'X',2.5,'PLATE_P'),'PLATE') as s: s.rect((2.5,0,0),(2.5,40,60))
 extrude(d,s.feat,'PLATE',5,mode=MID,expect_dv=12000); save(d)
 with Sk(d,plane(d,'X',35,'ARM_P'),'ARM') as s: s.rect((35,15,40),(35,25,52))
 extrude(d,s.feat,'ARM',60,mode=MID,expect_dv=7200); save(d)
 with Sk(d,plane(d,'X',2.5,'HOLES_P'),'HOLES') as s:
  for z in (12,48): s.circle((2.5,20,z),2.25)
 extrude(d,s.feat,'HOLES',5,cut=True,mode=MID,expect_dv=2*math.pi*2.25**2*5); save(d)
 es=edges_where(d,lambda p: abs(p[0]-5)<.01 and (abs(p[2]-40)<.01 or abs(p[2]-52)<.01) and 14.99<=p[1]<=25.01)
 print('fillet edges',len(es),flush=True)
 if len(es)!=2 or fillet(d,es,(3,),'ROOT_FILLET')!=3: raise Failed('root fillet')
 save(d); print('MODEL',volume(d),bbox(d),bodies(d),feature_errors(d),flush=True)
 save_as(d,out/'bracket.stl'); save_as(d,out/'bracket_study.SLDPRT')
 with Sk(d,plane(d,'Z',51.975,'SPLIT_P'),'LOAD_SPLIT') as s: s.rect((8,15,51.975),(55,25,51.975))
 extrude(d,s.feat,'LOAD_SPLIT',.05,cut=True,mode=MID); save(d)
 print('TWIN',volume(d),bbox(d),flush=True)
 close(j.sw,d); j.simulation(); d=open_doc(j.sw,out/'bracket_study.SLDPRT'); d.ForceRebuild3(False)
 for el in (3.0,2.0,1.5):
  fix=pick(d,kind='cyl',r=2.25); load=pick(d,kind='plane',at=(60,20,52),normal=(0,0,1))
  print('PREDICT',el,'nodes',12*19000/el**3,'disp mm',60*55**3/(3*2.1e9*(10*12**3/12)*1e-12)*1e-3,'peak root/holes','picks',len(fix),len(load),flush=True)
  r=static(j,d,'B2_'+str(el).replace('.','_'),PETG,fixtures=[('fixed',fix)],loads=[('normal',load,60)],el=el,max_nodes=199999,loose_ok=True)
  mask=r.away(dist=3.0); print('RESULT',r.summary(mask=mask),'all',float(r.vm.max()),'layers',[(n,r.layer_stress(n,mask),r.layer_shear(n,mask)) for n in ((1,0,0),(0,1,0),(0,0,1))],flush=True)
  np.savez_compressed(run/('b2_'+str(el)+'.npz'),pos=r.pos,s=r.s,disp=r.disp,reaction=r.reaction)
