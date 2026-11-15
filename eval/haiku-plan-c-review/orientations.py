import sys, json, numpy as np
sys.path.insert(0, sys.argv[2])
import sheet
tris = sheet.read_stl(sys.argv[1])
P = tris.reshape(-1,3)
print('box', P.min(0).round(1), P.max(0).round(1))
e1 = tris[:,1]-tris[:,0]; e2 = tris[:,2]-tris[:,0]
cr = np.cross(e1,e2); area = np.linalg.norm(cr,axis=1)/2; n = cr/np.maximum(2*area[:,None],1e-15)
cen = tris.mean(1)
# vertex ids for patch connectivity
key = np.round(P,3); _, vid = np.unique(key, axis=0, return_inverse=True); vid = vid.reshape(-1,3)
def patches(mask):
    idx = np.where(mask)[0]
    parent = {}
    def find(a):
        while parent.setdefault(a,a)!=a:
            parent[a]=parent[parent[a]]; a=parent[a]
        return a
    for i in idx:
        a,b,c = vid[i]; ra=find(a); parent[find(b)]=ra; parent[find(c)]=ra
    groups={}
    for i in idx: groups.setdefault(find(vid[i,0]),[]).append(i)
    out=[]
    for g in groups.values():
        g=np.array(g); A=area[g].sum()
        if A>=5: out.append((round(float(A),0), (np.average(cen[g],axis=0,weights=area[g])).round(0).tolist()))
    return sorted(out, reverse=True)
def scan(name,u):
    u=np.array(u,float); u/=np.linalg.norm(u)
    h = P@u; height = h.max()-h.min()
    # footprint: best rotation about u
    a = np.cross(u,[1,0,0]) if abs(u[0])<0.9 else np.cross(u,[0,1,0]); a/=np.linalg.norm(a); b=np.cross(u,a)
    best=None
    for t in np.radians(np.arange(0,90,1)):
        x = P@(np.cos(t)*a+np.sin(t)*b); y = P@(-np.sin(t)*a+np.cos(t)*b)
        s=(x.max()-x.min(), y.max()-y.min())
        if best is None or max(s)<max(best): best=s
    down = n@u
    th = tris@u
    on_bed = (th.max(1)-h.min()<0.3)
    over = (down < -np.sin(np.radians(45))) & ~on_bed & (area>1e-12)
    ps = patches(over)
    print(f'{name:28s} h {height:6.1f} foot {best[0]:5.0f}x{best[1]:5.0f} fits {height<=250 and max(best)<=250}  support {area[over].sum():6.0f} mm2 in {len(ps)} patches; bed {area[on_bed].sum():5.0f}')
    for A,c in ps[:8]: print(f'      {A:6.0f} mm2 at {c}')
c=np.cos; s=np.sin
scan('upright +Z up',(0,0,1)); scan('upright -Z up',(0,0,-1))
scan('flat +Y up',(0,1,0)); scan('flat -Y up',(0,-1,0)); scan('edge +X up',(1,0,0)); scan('edge -X up',(-1,0,0))
for sign in (1,-1):
  for deg in (20,30,45,60):
    r=np.radians(deg)
    for ax,nm in (((s(r),0,sign*c(r)),'toward +X'),((-s(r),0,sign*c(r)),'toward -X'),((0,s(r),sign*c(r)),'toward +Y'),((0,-s(r),sign*c(r)),'toward -Y')):
        scan(f'{"+" if sign>0 else "-"}Z up tilt {deg} {nm}',ax)
