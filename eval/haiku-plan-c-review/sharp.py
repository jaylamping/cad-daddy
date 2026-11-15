import sys, numpy as np, math
sys.path.insert(0,'solidworks'); import sheet
t=sheet.read_stl('eval/haiku-plan-c/exports/link_organic.STL')
n,area=sheet._normals(t)
v,vid=np.unique(np.round(t.reshape(-1,3),4),axis=0,return_inverse=True); f=vid.reshape(-1,3)
e=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1); owner=np.tile(np.arange(len(f)),3)
o=np.lexsort((e[:,1],e[:,0])); e,owner=e[o],owner[o]
pair=np.flatnonzero((e[1:]==e[:-1]).all(axis=1)); cosang=np.einsum('ij,ij->i',n[owner[pair]],n[owner[pair+1]])
sh=pair[cosang<math.cos(math.radians(30))]; ang=np.degrees(np.arccos(np.clip(cosang[cosang<math.cos(math.radians(30))],-1,1)))
a,b=v[e[sh,0]],v[e[sh,1]]; L=np.linalg.norm(a-b,axis=1); m=(a+b)/2
bolts=[(25*math.cos(math.radians(60*k)),25*math.sin(math.radians(60*k))) for k in range(6)]
def cls(p):
    x,y,z=p
    if any(math.hypot(x-bx,z-bz)<4.2 for bx,bz in bolts): return 'screw holes, seats and head scallops'
    if math.hypot(x,z)<15.3 and z>-16: return 'bore rims (incl. cable tunnel mouth)'
    if math.hypot(x,y)<3.6 and z<-150: return 'cable tunnel mouth in the arch'
    if math.hypot(x,z+200)<4.3: return 'pin hole rims'
    if abs(abs(y)-16)<0.3 and z<-160: return 'slot / arch edges at the inner cheek faces'
    if z>-45 and math.hypot(x,z)>15.3: return 'elbow: hub face / stem seam and mount-face rim'
    if z<-180: return 'wrist: knuckle against stem and cheek ends'
    return 'other (stem)'
tot={}
for p,l,g in zip(m,L,ang):
    k=cls(p); d=tot.setdefault(k,[0,0]); d[0]+=l; d[1]=max(d[1],g)
for k,(l,g) in sorted(tot.items(),key=lambda x:-x[1][0]): print(f'{l:7.1f} mm  max turn {g:5.1f} deg  {k}')
print('total',L.sum())
# elbow seam detail: edges at y~4 plane, z<-20
sel=[i for i,p in enumerate(m) if cls(p).startswith('elbow')]
pp=m[sel]; print('elbow sharp edges: y range',pp[:,1].min(),pp[:,1].max(),'z range',pp[:,2].min(),pp[:,2].max())
for lo,hi in ((-4.1,-3.9),(-3.9,3.9),(3.9,4.1),(4.1,20)):
    q=[i for i in sel if lo<=m[i,1]<hi]; print('  y',lo,hi,'len',round(L[q].sum(),1),'angles',np.round(np.percentile(ang[q],[0,50,100]),1) if q else None, 'z',(round(m[q,2].min(),1),round(m[q,2].max(),1)) if q else None)
# planes > 1% area
key=np.round(np.c_[n/0.0087,np.einsum('ij,ij->i',n,t[:,0])[:,None]/0.02]).astype(np.int64)
u,inv=np.unique(key,axis=0,return_inverse=True); pa=np.bincount(inv.ravel(),area); tota=area.sum()
for i in np.argsort(-pa)[:8]:
    if pa[i]>=0.01*tota:
        tt=t[inv.ravel()==i]; print('flat',round(pa[i],1),round(pa[i]/tota,3),'normal',np.round(n[inv.ravel()==i][0],2),'box',tt.reshape(-1,3).min(0).round(1),tt.reshape(-1,3).max(0).round(1))
