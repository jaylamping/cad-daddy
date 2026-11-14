import math,json,traceback
from pathlib import Path
import numpy as np
import trimesh
from d3_build import ROOT,OUT,RUN,DATA,WHY,positions,hand,minwall,measured
from swkit import *

def edited(row):
 name,od,t,bore,A,B,cb,dep=row
 if name=='P1':B=(B[0],B[1],58,B[3])
 if name=='P3':A=(A[0],A[1],70,22.5);B=(B[0],B[1],82,B[3])
 return (name,od,t+1.5,bore,A,B,cb,dep+1.5)

def ref(d,name):
 f=d.FeatureByName(name)
 if f is None:raise RuntimeError('missing original feature '+name)
 try:
  v=d.Extension.GetPersistReference3(f)
  return bytes((int(x)&255 for x in v)).hex()
 except Exception as e:
  print('PERSISTENT REF unavailable',name,repr(e),flush=True);return None

def edit(j,row):
 name,od,t,bore,A,B,cb,dep=row;new=edited(row);floor=t-dep
 vhand=hand(new)-math.pi*(od/2-1/3)
 wall,where=minwall(new,top_chamfer=1)
 if wall<.6:raise RuntimeError(f'{name} changed min wall {wall} at {where}')
 d=open_doc(j.sw,OUT/(name+'.SLDPRT'))
 names=['BASE','BORE','A_HOLES','B_HOLES','COUNTERBORE','BORE_SK','A_HOLES_SK','B_HOLES_SK','COUNTERBORE_SK','COUNTERBORE_P']
 before={n:ref(d,n) for n in names};print('BEFORE',name,before,flush=True)
 save_as(d,OUT/(name+'_b.SLDPRT'))
 set_dim(d,'BASE',t,t+1.5);set_dim(d,'COUNTERBORE',dep,dep+1.5);d.ForceRebuild3(False);save(d)
 if name in ('P1','P3'):
  newB=new[5]
  redraw_circles(d,'B_HOLES_SK',positions(newB,0),newB[1]/2);d.ForceRebuild3(False)
  redraw_circles(d,'COUNTERBORE_SK',positions(newB,floor),cb/2);d.ForceRebuild3(False);save(d)
 if name=='P3':
  newA=new[4];redraw_circles(d,'A_HOLES_SK',positions(newA,0),newA[1]/2);d.ForceRebuild3(False);save(d)
 v_before=volume(d)
 expect(name+' volume before chamfer',v_before,hand(new),.001)
 edges=edges_where(d,lambda p: abs(math.hypot(p[0],p[1])-od/2)<.02 and abs(p[2]-(t+1.5))<.02)
 print(name,'top rim edges',len(edges),flush=True)
 if len(edges)!=1:raise RuntimeError(f'{name}: expected one outside rim, got {len(edges)}')
 chamfer(d,edges,1.,'TOP_CHAMFER');save(d)
 v=volume(d);expect(name+' chamfer volume',v,vhand,.001);single_body(d)
 errors=feature_errors(d)
 if errors:raise RuntimeError(f'{name}: feature errors {errors}')
 for i,w in enumerate((-od/2,-od/2,0,od/2,od/2,t+1.5)):expect(name+' box '+str(i),bbox(d)[i],w,.02)
 measured(d,new);after={n:ref(d,n) for n in names};print('AFTER',name,after,flush=True)
 stable=all(before[k] is not None and before[k]==after[k] for k in names)
 print('IDENTITY',name,stable,flush=True)
 save(d);save_as(d,OUT/(name+'_b.stl'));m=trimesh.load(OUT/(name+'_b.stl'))
 if not m.is_watertight or len(m.split())!=1 or abs(m.volume/v-1)>.005:raise RuntimeError(f'{name} STL invalid watertight {m.is_watertight}, volume {m.volume}')
 reason=WHY.get(name,'')
 if name=='P1':reason+='; B PCD 60→58 so the 1 mm chamfer does not meet the counterbore'
 if name=='P3':reason='A PCD 66→70 and phase 22.5° to avoid a 0.3 mm ligament; B PCD 84→82 so chamfer clears its counterbore'
 rec={'volume_mm3':v,'hand_volume_mm3':vhand,'mass_g':v*.00119,'bodies':1,'stl_watertight':True,'stl_volume_mm3':float(m.volume),'min_wall_mm':wall,'min_wall_feature':where,'changed':True,'why':reason or 'thickness +1.5, counterbore floor retained, top chamfer','counterbore_floor_z_mm':floor,'feature_refs_stable':stable,'before_refs':before,'after_refs':after}
 print('STL',name+'_b',m.volume,m.bounds.tolist(),flush=True);close(j.sw,d);return rec
if __name__=='__main__':
 if not (RUN/'D3_part1_table.md').exists():raise RuntimeError('part-one table missing; do not start edit')
 print('PART ONE TABLE exists; begin requested change',flush=True)
 out={};fail={}
 with job(wait_s=1800) as j:
  print('PID',j.inst.pid,flush=True)
  for row in DATA:
   try:out[row[0]]=edit(j,row)
   except Exception as e:fail[row[0]]=repr(e);traceback.print_exc();print('FAILED EDIT',row[0],flush=True)
   (RUN/'d3_part2.json').write_text(json.dumps({'plates':out,'errors':fail},indent=2),encoding='utf-8')
 print('PART2 COMPLETE',len(out),'errors',fail,flush=True)

