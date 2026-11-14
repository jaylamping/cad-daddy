import numpy as np
p=np.load('tools/solidworks/playbook/eval/terra-high-b2/b2_round_1.5.npz'); a=p['pos']; S=p['s'];
dist=np.full(len(a),1e9)
for z in (12,48):
 d=np.sqrt((a[:,0]-np.clip(a[:,0],0,5))**2+(np.sqrt((a[:,1]-20)**2+(a[:,2]-z)**2)-2.25)**2); dist=np.minimum(dist,d)
load=np.sqrt((a[:,0]-np.clip(a[:,0],55,65))**2+(a[:,1]-np.clip(a[:,1],15,25))**2+(a[:,2]-52)**2)
keep=(dist>=3)&(load>=3); S=S[keep]; vm=float(S[:,10].max()); best=(0,None,None,None)
for i in range(1000):
 z=1-2*(i+.5)/1000; phi=i*2.399963229728653; n=np.array([np.sqrt(1-z*z)*np.cos(phi),np.sqrt(1-z*z)*np.sin(phi),z]);
 tx=S[:,1]*n[0]+S[:,4]*n[1]+S[:,5]*n[2]; ty=S[:,4]*n[0]+S[:,2]*n[1]+S[:,6]*n[2]; tz=S[:,5]*n[0]+S[:,6]*n[1]+S[:,3]*n[2]; sn=tx*n[0]+ty*n[1]+tz*n[2]; tau=np.sqrt(np.maximum(0,tx*tx+ty*ty+tz*tz-sn*sn)); sf=min(45/vm,22.5/max(sn.max(),1e-9),13/max(tau.max(),1e-9));
 if sf>best[0]:best=(sf,n.tolist(),float(sn.max()),float(tau.max()))
print('kept',len(S),'vm',vm,'best approximate min factor, normal, tension, shear',best)
