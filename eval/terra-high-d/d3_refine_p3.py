import json,math
import trimesh
from d3_build import DATA,OUT,RUN,positions,measured,minwall,hand
from d3_edit import edited,ref
from swkit import *
row=DATA[2];new=edited(row);name,od,t,bore,A,B,cb,dep=new;floor=t-dep
with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True);d=open_doc(j.sw,OUT/'P3_b.SLDPRT')
 names=['BASE','BORE','A_HOLES','B_HOLES','COUNTERBORE','B_HOLES_SK','COUNTERBORE_SK','COUNTERBORE_P','TOP_CHAMFER']
 before={n:ref(d,n) for n in names};v0=volume(d)
 redraw_circles(d,'B_HOLES_SK',positions(B,0),B[1]/2);d.ForceRebuild3(False)
 redraw_circles(d,'COUNTERBORE_SK',positions(B,floor),cb/2);d.ForceRebuild3(False);save(d)
 v=volume(d);expect('unchanged P3 volume after relocation',v,v0,.00001);expect('P3 hand volume',v,hand(new)-math.pi*(od/2-1/3),.001)
 print('errors',feature_errors(d),'bodies',bodies(d),'bbox',bbox(d),flush=True);single_body(d);assert not feature_errors(d)
 measured(d,new);after={n:ref(d,n) for n in names};print('REFS same',before==after,flush=True);assert before==after
 save(d);save_as(d,OUT/'P3_b.stl');m=trimesh.load(OUT/'P3_b.stl');assert m.is_watertight and len(m.split())==1 and abs(m.volume/v-1)<.005
 db=json.loads((RUN/'d3_part2.json').read_text(encoding='utf-8'));r=db['plates']['P3'];wall,where=minwall(new,1)
 r.update(volume_mm3=v,hand_volume_mm3=hand(new)-math.pi*(od/2-1/3),mass_g=v*.00119,stl_volume_mm3=float(m.volume),min_wall_mm=wall,min_wall_feature=where,why='A PCD 66→70 and phase 22.5° to avoid interference; B PCD 84→82 so chamfer retains 1 mm outside wall')
 (RUN/'d3_part2.json').write_text(json.dumps(db,indent=2),encoding='utf-8')
 print('STL',m.volume,m.bounds.tolist(),'wall',wall,flush=True);close(j.sw,d)
