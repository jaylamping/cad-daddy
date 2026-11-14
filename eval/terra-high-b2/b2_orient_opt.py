exec(open('tools/solidworks/playbook/eval/terra-high-b2/b2_directions.py',encoding='utf-8-sig').read().split('for i in range(1000):')[0])
from scipy.optimize import minimize
def f(v):
 x,y=v
 if x*x+y*y>=1:return 1e3
 n=np.array([x,y,np.sqrt(1-x*x-y*y)]); tx=S[:,1]*n[0]+S[:,4]*n[1]+S[:,5]*n[2]; ty=S[:,4]*n[0]+S[:,2]*n[1]+S[:,6]*n[2]; tz=S[:,5]*n[0]+S[:,6]*n[1]+S[:,3]*n[2]; sn=tx*n[0]+ty*n[1]+tz*n[2]; return max(float(np.sqrt(np.maximum(0,tx*tx+ty*ty+tz*tz-sn*sn)).max())/13,float(sn.max())/22.5,vm/45)
for init in ([0,0],[.03,.07],[-.03,-.07]):
 r=minimize(f,init,method='Nelder-Mead',options={'xatol':1e-6,'maxiter':250});print('best normal xy',r.x,'factor',1/r.fun,'success',r.success)

