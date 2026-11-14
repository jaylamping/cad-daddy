import sys,numpy as np
A=np.load(sys.argv[1]); p=A['pos']; s=A['s']; ds=[]
for x in (25,65):
 for y in (10,40):
  r=np.hypot(p[:,0]-x,p[:,1]-y); dz=np.maximum(np.maximum(-p[:,2],p[:,2]-6),0); ds.append(np.hypot(r-2.75,dz))
d=np.min(np.array(ds),axis=0); sy=s[:,2]; sh=np.hypot(s[:,4],s[:,6]);
for v in (1,2,3,5,6):
 m=d>=v
 def top(values):
  i=np.flatnonzero(m)[np.argmax(values[m])]; return [round(float(values[i]),3),p[i].round(2).tolist()]
 print(v,'vm',top(s[:,10]),'Yt',top(sy),'Yshear',top(sh))
