import sys,math,json,traceback
from pathlib import Path
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d';RUN=Path(__file__).resolve().parent
# name, OD, thickness, bore, A count/diameter/PCD/phase, B count/diameter/PCD/phase, CB diameter/depth
DATA=[
 ('P1',70,6,30,(6,3.4,50,0),(4,4.5,60,15),8,3),
 ('P2',84,6,40,(6,4.5,62,0),(6,4.5,62,30),8,3),
 ('P3',96,8,52,(8,3.4,66,0),(4,5.5,84,0),10,4),
 ('P4',60,5,28,(4,3.4,40,0),(6,4.5,48,15),8,4),
 ('P5',120,8,60,(12,4.5,80,0),(6,6.6,104,0),11,5),
 ('P6',76,6,34,(6,3.4,46,0),(3,4.5,64,0),8,3)]
WHY={'P1':'B phase 15°: prevent overlapping A holes and counterbores','P2':'B phase 30°: avoid coincident A/B holes','P4':'B PCD 48 and phase 15°; depth 4: contain holes, separate rings, leave 1 mm floor'}
def positions(pattern,z):
 n,d,pcd,phase=pattern
 return [(pcd/2*math.cos(math.radians(phase+360*i/n)),pcd/2*math.sin(math.radians(phase+360*i/n)),z) for i in range(n)]
def hand(row):
 name,od,t,bore,A,B,cb,dep=row
 return math.pi*(od/2)**2*t-math.pi*(bore/2)**2*t-A[0]*math.pi*(A[1]/2)**2*t-B[0]*math.pi*(B[1]/2)**2*t-B[0]*math.pi*((cb/2)**2-(B[1]/2)**2)*dep
def minwall(row,top_chamfer=0):
 name,od,t,bore,A,B,cb,dep=row;R=od/2
 circles=[('bore',0.,0.,bore/2)]
 for tag,pat,rad in [('A',A,A[1]/2),('B counterbore',B,cb/2)]:
  circles += [(tag,x,y,rad) for x,y,z in positions(pat,0)]
 candidates=[(R-top_chamfer-math.hypot(x,y)-r,'outside to '+label) for label,x,y,r in circles]
 for i,(a,x,y,r) in enumerate(circles):
  for b,u,v,s in circles[i+1:]:candidates.append((math.hypot(x-u,y-v)-r-s,a+' to '+b))
 candidates.append((t-dep,'counterbore floor'))
 return min(candidates,key=lambda x:x[0])
def cut(d,name,points,r,depth,mode,want=None):
 z=points[0][2]
 with Sk(d,plane(d,'Z',z,name+'_P'),name) as s:
  for p in points:s.circle(p,r)
 extrude(d,s.feat,name,depth,cut=True,mode=mode,want=want,expect_dv=len(points)*math.pi*r*r*(depth if mode!=THRU_ALL else CURRENT_T))
 save(d)
def measured(d,row):
 name,od,t,bore,A,B,cb,dep=row;floor=t-dep
 expected=[('bore',0.,0.,bore/2,0.,t)]
 expected += [('A',x,y,A[1]/2,0.,t) for x,y,z in positions(A,0)]
 expected += [('B',x,y,B[1]/2,0.,floor) for x,y,z in positions(B,0)]
 expected += [('CB',x,y,cb/2,floor,t) for x,y,z in positions(B,0)]
 for typ,x,y,r,z0,z1 in expected:
  candidates=[]
  for f in pick(d,kind='cyl',r=r,tol=.002):
   q=face_info(f);b=q['box'];cx=(b[0]+b[3])/2;cy=(b[1]+b[4])/2
   if abs(cx-x)<.01 and abs(cy-y)<.01 and abs(b[2]-z0)<.01 and abs(b[5]-z1)<.01:candidates.append(q)
  if len(candidates)!=1:raise RuntimeError(f'{name} missing/ambiguous {typ} center {(x,y)} r={r} z={z0,z1}, found {len(candidates)}')
 print('MEASURED',name,len(expected),'cylinders and box',bbox(d),flush=True)
def build(j,row):
 global CURRENT_T
 name,od,t,bore,A,B,cb,dep=row;CURRENT_T=t
 wall,where=minwall(row)
 if wall<.6:raise RuntimeError(f'{name} wall {wall} at {where} <.6')
 d=new_part(j.sw,OUT/(name+'.SLDPRT'))
 with Sk(d,plane(d,'Z',0,'BASE_P'),'BASE') as s:s.circle((0,0,0),od/2)
 extrude(d,s.feat,'BASE',t,mode=BLIND,want=(2,+1,0),expect_dv=math.pi*(od/2)**2*t);save(d)
 cut(d,'BORE',[(0,0,0)],bore/2,t,THRU_ALL)
 cut(d,'A_HOLES',positions(A,0),A[1]/2,t,THRU_ALL)
 cut(d,'B_HOLES',positions(B,0),B[1]/2,t,THRU_ALL)
 floor=t-dep
 with Sk(d,plane(d,'Z',floor,'COUNTERBORE_P'),'COUNTERBORE') as s:
  for p in positions(B,floor):s.circle(p,cb/2)
 extrude(d,s.feat,'COUNTERBORE',dep,cut=True,mode=BLIND,want=(2,+1,floor),expect_dv=B[0]*math.pi*((cb/2)**2-(B[1]/2)**2)*dep);save(d)
 v=volume(d);expect(name+' hand volume',v,hand(row),.001);single_body(d);err=feature_errors(d)
 if err:raise RuntimeError(f'{name} rebuild {err}')
 b=bbox(d)
 for i,w in enumerate((-od/2,-od/2,0,od/2,od/2,t)):expect(name+' box '+str(i),b[i],w,.02)
 measured(d,row);save(d);save_as(d,OUT/(name+'.stl'))
 m=trimesh.load(OUT/(name+'.stl')); shells=len(m.split());
 if not m.is_watertight or shells!=1 or abs(m.volume/v-1)>.005:raise RuntimeError(f'{name} STL bad: watertight={m.is_watertight}, shells={shells}, volume={m.volume}')
 print('STL',name,'volume',m.volume,'bounds',m.bounds.tolist(),'watertight',m.is_watertight,flush=True)
 record={'volume_mm3':v,'hand_volume_mm3':hand(row),'mass_g':v*.00119,'bodies':1,'stl_watertight':True,'stl_volume_mm3':float(m.volume),'min_wall_mm':wall,'min_wall_feature':where,'changed':name in WHY,'why':WHY.get(name,''),'counterbore_floor_z_mm':floor}
 close(j.sw,d);return record
if __name__=='__main__':
 records={};errors={}
 with job(wait_s=1800) as j:
  print('PID',j.inst.pid,flush=True)
  for row in DATA:
   try:records[row[0]]=build(j,row)
   except Exception as e:
    errors[row[0]]=repr(e);traceback.print_exc();print('FAILED',row[0],flush=True)
   (RUN/'d3_part1.json').write_text(json.dumps({'plates':records,'errors':errors},indent=2),encoding='utf-8')
 print('PART1 COMPLETE',len(records),'errors',errors,flush=True)
