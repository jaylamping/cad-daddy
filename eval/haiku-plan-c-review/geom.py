import sys, numpy as np
sys.path.insert(0,'solidworks'); import sheet
E='eval/haiku-plan-c/exports/'
def basic(name):
    t=sheet.read_stl(E+name)
    v,vid=np.unique(np.round(t.reshape(-1,3),4),axis=0,return_inverse=True)
    f=vid.reshape(-1,3)
    vol=float(np.einsum('ij,ij->i',t[:,0],np.cross(t[:,1],t[:,2])).sum()/6)
    e=np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]])
    # directed edge check
    key=e[:,0].astype(np.int64)*len(v)+e[:,1]; rkey=e[:,1].astype(np.int64)*len(v)+e[:,0]
    es=np.sort(e,axis=1); u,c=np.unique(es,axis=0,return_counts=True)
    water=bool((c==2).all()) and len(np.unique(key))==len(key) and set(key.tolist())==set(rkey.tolist())
    # shells via union find
    par=np.arange(len(v))
    def find(a):
        while par[a]!=a:
            par[a]=par[par[a]]; a=par[a]
        return a
    for a,b in u:
        ra,rb=find(a),find(b)
        if ra!=rb: par[ra]=rb
    shells=len({find(i) for i in range(len(v))})
    p=t.reshape(-1,3)
    print(name,'tris',len(t),'vol',round(vol,1),'mass g',round(vol*1.19e-3,2),'watertight',water,'shells',shells,
          'bbox',p.min(0).round(3),p.max(0).round(3),'edges not shared by 2:',int((c!=2).sum()))
    print('  shape',sheet.shape_stats(t))
    return t
for n in ['link_boxy.STL','link_organic.STL','idea_a.STL']: basic(n)
