import numpy as np
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator
p=np.load('tools/solidworks/playbook/eval/terra-high-b2/b4_SOFT.npz'); a=p['pos'];s=p['s'];d=p['disp']
tong=(a[:,0]>=-4.001)&(a[:,0]<=4.001)&(a[:,1]>=-10.001)&(a[:,1]<=10.001)&(a[:,2]>=8.099)
block=(a[:,2]<=20.001)&((a[:,0]<=-4.099)|(a[:,0]>=4.099)|(a[:,2]<=8.001))
i=np.flatnonzero(block)[np.argmax(s[block,10])]; print('block peak',s[i,10],a[i], 'tip max', np.max(d[tong&(a[:,2]>39.9),4]), flush=True)
print('interpolating',tong.sum(),flush=True)
f=LinearNDInterpolator(a[tong],s[tong,5],fill_value=np.nan); near=NearestNDInterpolator(a[tong],s[tong,5]); xx,yy=np.meshgrid(np.linspace(-4,4,81),np.linspace(-10,10,161));
for z in (9,10,11,12,14,16,18,19,21,22,24,28,29):
 pts=np.c_[xx.ravel(),yy.ravel(),np.full(xx.size,z)]; v=f(pts); bad=np.isnan(v); v[bad]=near(pts[bad]); v=v.reshape(xx.shape); q=np.trapezoid(np.trapezoid(v,xx[0],axis=1),yy[:,0]); print('z',z,'Qxz',q,'extrap frac',bad.mean(),flush=True)

