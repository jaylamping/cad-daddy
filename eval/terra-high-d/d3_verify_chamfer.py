import math
from d3_build import OUT,DATA
from swkit import *
with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True)
 for row in DATA:
  name,od,t,*_=row;top=t+1.5;R=od/2
  d=open_doc(j.sw,OUT/(name+'_b.SLDPRT'))
  for z,r,label in ((top-1,R,'lower'),(top,R-1,'upper')):
   es=edges_where(d,lambda p:abs(math.hypot(p[0],p[1])-r)<.02 and abs(p[2]-z)<.02)
   print(name,label,'radius',r,'z',z,'count',len(es),flush=True)
   if len(es)!=1:raise RuntimeError(f'{name} {label} chamfer edge expected 1 got {len(es)}')
  if d.FeatureByName('TOP_CHAMFER') is None:raise RuntimeError('chamfer feature missing')
  close(j.sw,d)
