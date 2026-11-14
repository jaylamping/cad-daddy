import trimesh, numpy as np, math
from pathlib import Path
R=Path(__file__).resolve().parents[5]
m=trimesh.load(R/'cad/_wip/sw-eval/terra-high-c/link_organic.stl')
def moment(z):
 s=m.section(plane_origin=[0,0,z],plane_normal=[0,0,1]); paths=s.discrete
 out=[]
 for p in paths:
  x,y=p[:,0],p[:,1]; x1,y1=np.roll(x,-1),np.roll(y,-1); cross=x*y1-x1*y
  area=sum(cross)/2; ix=sum((y*y+y*y1+y1*y1)*cross)/12; iy=sum((x*x+x*x1+x1*x1)*cross)/12
  out.append((abs(area),abs(ix),abs(iy)))
 out.sort(reverse=True)
 return np.array(out[0])-sum((np.array(v) for v in out[1:]),np.zeros(3))
for z in [-35,-36,-38,-40,-45,-60,-100,-140,-170,-179]: print(z,moment(z))
zs=np.arange(-179.5,-35,1.0); m2=np.array([moment(z) for z in zs]);
for label,axis in [('X',2),('Y',1)]:
 val=np.trapezoid(60*(zs+200)**2/(1900*m2[:,axis]),zs)
 print(label,'beam compliance mm, z=-179.5..-35',val)
