import numpy as np
for name in ('b2_FINE.npz','b3_taper_FINE.npz'):
 p=np.load('tools/solidworks/playbook/eval/terra-high-b2/'+name); a=p['pos']; s=p['s']; dist=np.full(len(a),1e9)
 for z in (12,48):
  d=np.sqrt((a[:,0]-np.clip(a[:,0],0,5))**2+(np.sqrt((a[:,1]-20)**2+(a[:,2]-z)**2)-2.25)**2); dist=np.minimum(dist,d)
 for q in (1,2,3,5):
  keep=(dist>=q)&(a[:,0]<52); i=np.flatnonzero(keep)[np.argmax(s[keep,10])]; print(name,'distance',q,'vm',s[i,10],'at',a[i])
