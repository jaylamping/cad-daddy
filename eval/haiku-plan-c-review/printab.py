"""Own printability measure (sheet.py in this folder has no printability()/mesh_diff()). numpy only."""
import sys, numpy as np
sys.path.insert(0,'solidworks'); import sheet
def printability(t, up, bed=256.0, first=0.3, ang=45.0):
    up=np.array(up,float); ax=int(np.argmax(np.abs(up))); s=up[ax]
    # rotate so that build direction is +Z: new z = s*coord[ax]; keep handedness
    others=[i for i in range(3) if i!=ax]
    R=np.zeros((3,3)); R[2,ax]=s; R[0,others[0]]=1; R[1,others[1]]=1
    if np.linalg.det(R)<0: R[1,others[1]]=-1
    q=t@R.T; q[:,:,2]-=q[:,:,2].min()
    n,a=sheet._normals(q)
    ext=q.reshape(-1,3).max(0)-q.reshape(-1,3).min(0)
    low=q[:,:,2].max(axis=1)<first
    contact=float(a[low&(n[:,2]<-0.5)].sum())
    cpts=q[low&(n[:,2]<-0.5)].reshape(-1,3)
    cbox=(cpts.max(0)-cpts.min(0))[:2].round(1).tolist() if len(cpts) else [0,0]
    over=(n[:,2]<-np.sin(np.radians(ang)))&~low
    oa=float(a[over].sum()); oproj=float((a[over]*-n[over,2]).sum())
    # supports: projected overhang area times its height above the bed (upper bound: ignores part below)
    h=q[over][:,:,2].mean(axis=1); sup=float((a[over]*-n[over,2]*h).sum()); hmean=float((a[over]*h).sum()/max(a[over].sum(),1e-9))
    # cross-section area of the first layers: what holds the part to the bed
    return dict(up=up.tolist(), footprint_mm=ext[:2].round(1).tolist(), height_mm=round(float(ext[2]),1), fits_bed=bool((ext[:2]<=bed).all() and ext[2]<=bed),
                contact_mm2=round(contact,1), contact_box_mm=cbox, overhang_area_mm2=round(oa,1), overhang_projected_mm2=round(oproj,1),
                support_upper_cm3=round(sup/1000,1), overhang_mean_height_mm=round(hmean,1))
if __name__=='__main__':
    for name in ['link_organic.STL','link_boxy.STL']:
        t=sheet.read_stl('eval/haiku-plan-c/exports/'+name); print(name)
        for lab,up in [('layers along Y, +Y side on bed (plan)',(0,-1,0)),('layers along Y, -Y side on bed',(0,1,0)),
                       ('layers along X, +X side down',(-1,0,0)),('layers along X, -X side down',(1,0,0)),
                       ('layers along Z, fork down',(0,0,1)),('layers along Z, hub down',(0,0,-1))]:
            print('  ',lab, printability(t,up))
