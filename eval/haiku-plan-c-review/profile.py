import sys, numpy as np
sys.path.insert(0,'solidworks'); import sheet
t=sheet.read_stl('eval/haiku-plan-c/exports/link_organic.STL')
def slice_ext(z):
    pts=[]
    for a,b in ((0,1),(1,2),(2,0)):
        p,q=t[:,a],t[:,b]; m=(p[:,2]-z)*(q[:,2]-z)<0
        f=(z-p[m,2])/(q[m,2]-p[m,2]); pts.append(p[m]+f[:,None]*(q[m]-p[m]))
    return np.concatenate(pts)
print(' z     xhalf   ytop   ybot   (design A2 rows: -46: 14.4/12.8/-9.8  -60: 12.6/12.8/-11.8  -85: 11.4/12/-12  -115: 10.6/11.8/-11.8)')
for z in list(range(-34,-180,-4)):
    p=slice_ext(z+0.01); print(f'{z:5d} {np.abs(p[:,0]).max():6.2f} {p[:,1].max():6.2f} {p[:,1].min():6.2f}')
