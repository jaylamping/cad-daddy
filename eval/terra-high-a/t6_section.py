import sys
from pathlib import Path
import numpy as np
from scipy.interpolate import LinearNDInterpolator
p=Path(sys.argv[1]); a=np.load(p); pos=a['pos']; s=a['s']; rad=np.hypot(pos[:,0],pos[:,2]-10)
for y in (-20,-10,0,10,20):
 m=(rad<5.0001)&(np.abs(pos[:,1]-y)<5.1)&(abs(pos[:,1])<24.95)
 q=pos[m]; v=s[m,6]; print('points',y,len(q),flush=True)
 try:
  interp=LinearNDInterpolator(q,v,fill_value=np.nan)
  dx=.1; xx,zz=np.meshgrid(np.arange(-4.95,5,dx),np.arange(5.05,15,dx)); disk=xx**2+(zz-10)**2<4.99**2
  pts=np.column_stack([xx[disk],np.full(disk.sum(),y),zz[disk]])
  f=interp(pts); print('section',y,'nan',int(np.isnan(f).sum()),'force_N',float(np.nansum(f)*dx**2),'sampled_area',int(np.isfinite(f).sum())*dx**2,flush=True)
 except Exception as ex: print('FAILED',type(ex).__name__,str(ex),flush=True)


