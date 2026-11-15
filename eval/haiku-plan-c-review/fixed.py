import sys, numpy as np, math
sys.path.insert(0,'solidworks'); import sheet
t=sheet.read_stl('eval/haiku-plan-c/exports/link_organic.STL')
ins=lambda p: sheet.inside(t,np.asarray(p,float),chunk=60)
n,area=sheet._normals(t)
R=[]
def rep(name,ok,meas): R.append((name,ok,meas)); print(('PASS' if ok else 'FAIL'),'|',name,'|',meas)
bolts=[(25*math.cos(math.radians(60*k)),25*math.sin(math.radians(60*k))) for k in range(6)]
def ring(r0,r1,nr,na,y):
    rs=np.linspace(r0,r1,nr); a=np.linspace(0,2*np.pi,na,endpoint=False)
    rr,aa=np.meshgrid(rs,a); x=rr*np.cos(aa); z=rr*np.sin(aa)
    return np.c_[x.ravel(),np.full(x.size,y),z.ravel()]
def nothole(p,m=0.15):
    d=np.min([np.hypot(p[:,0]-bx,p[:,2]-bz) for bx,bz in bolts],axis=0); return d>1.7+m
# 1 mount face
on=(np.abs(t[:,:,1]+4).max(axis=1)<1e-3)&(n[:,1]<-0.999)
A=area[on].sum(); rad=np.hypot(t[on][:,:,0],t[on][:,:,2])
hand=math.pi*(31**2-15**2)-6*math.pi*1.7**2
rep('mount face planar area at Y -4 (normal -Y)', A>=hand-1, f'{A:.1f} mm2, radii {rad.min():.3f} to {rad.max():.3f}; needed ring dia 30..62 less holes = {hand:.1f}; dia 30..63 less holes = {math.pi*(31.5**2-225)-6*math.pi*1.7**2:.1f}')
p=ring(15.15,30.95,40,180,-3.95); p=p[nothole(p)]
# cable tunnel mouth cuts the bore wall near x=0,z=-15
s=ins(p); bad=p[~s]
rep('solid just above Y -4 (y=-3.95) over dia 30.3..61.9 except holes', len(bad)==0, f'{len(p)} pts, {len(bad)} empty'+(f'; empty pts span x {bad[:,0].min():.1f}..{bad[:,0].max():.1f} z {bad[:,2].min():.1f}..{bad[:,2].max():.1f}' if len(bad) else ''))
p=ring(0,31,32,120,-4.05); s=ins(p)
rep('clear just below Y -4 (y=-4.05) inside dia 62', s.sum()==0, f'{len(p)} pts, {s.sum()} solid')
pp=np.concatenate([ring(0,31,16,72,y) for y in np.linspace(-30,-4.2,14)]); s=ins(pp)
rep('nothing below Y -4 inside dia 62 down to Y -30', s.sum()==0, f'{len(pp)} pts, {s.sum()} solid')
# how far beyond does stem go below Y-4
pp=np.array([(x,y,z) for x in np.linspace(-30,30,31) for y in (-4.3,-5,-7,-10) for z in np.linspace(-31,-60,30)]); s=ins(pp)
q=pp[s]; rep('INFO material below Y -4 outside dia 62 (motor body room)', True, f'solid found from z {q[:,2].max():.1f} downward, r_min {np.hypot(q[:,0],q[:,2]).min():.1f} mm, lowest y sampled {q[:,1].min()}')
# 2 bore
pp=np.concatenate([ring(0,14.9,16,90,y) for y in np.linspace(-3.9,3.9,9)]); s=ins(pp)
rep('bore dia 30 clear (r<=14.9, y -3.9..3.9)', s.sum()==0, f'{len(pp)} pts, {s.sum()} solid')
pp=np.concatenate([ring(15.1,15.1,1,360,y) for y in np.linspace(-3.9,3.9,9)]); s=ins(pp); bad=pp[~s]
ang=np.degrees(np.arctan2(bad[:,2],bad[:,0])) if len(bad) else np.array([])
rep('bore wall solid at r 15.1 (bore is not oversize)', len(bad)==0 or (np.abs(ang+90).max()<14), f'{len(pp)} pts, {len(bad)} empty'+(f', all within {np.abs(ang+90).max():.1f} deg of -Z (the cable tunnel mouth, half-angle asin(3.2/15.1)=12.2 deg)' if len(bad) else ''))
# bore radius from vertices
v=np.unique(np.round(t.reshape(-1,3),4),axis=0)
r=np.hypot(v[:,0],v[:,2]); m=(np.abs(r-15)<0.3)&(np.abs(v[:,1])<=4.001)
rep('bore radius from STL vertices', abs(np.median(r[m])-15)<0.02, f'{m.sum()} vertices, r {r[m].min():.3f}..{r[m].max():.3f}, y {v[m][:,1].min():.2f}..{v[m][:,1].max():.2f}')
# 3 holes
for k,(bx,bz) in enumerate(bolts):
    d=np.hypot(v[:,0]-bx,v[:,2]-bz); m=(d<2.2)
    hr=d[m]; ys=v[m][:,1]
    a=np.linspace(0,2*np.pi,24,endpoint=False)
    pin=np.array([(bx+rr*np.cos(x),y,bz+rr*np.sin(x)) for rr in (0,0.8,1.6) for x in a for y in np.linspace(-3.95,3.95,9)])
    pout=np.array([(bx+1.85*np.cos(x),y,bz+1.85*np.sin(x)) for x in a for y in np.linspace(-3.9,3.0,7)])
    si=ins(pin).sum(); so=ins(pout)
    rep(f'screw hole {k} at x {bx:.2f} z {bz:.2f}: dia 3.4 through Y -4..+4', si==0 and so.all() and abs(np.median(hr)-1.7)<0.02,
        f'vertex r {hr.min():.3f}..{hr.max():.3f} (n {m.sum()}), y {ys.min():.2f}..{ys.max():.2f}; clear pts solid {si}/{len(pin)}; wall at r 1.85 solid {so.sum()}/{len(pout)}')
    # head clearance: dia 7 x 10 from y 4 to 14
    pc=np.array([(bx+rr*np.cos(x),y,bz+rr*np.sin(x)) for rr in (0,1.2,2.4,3.45) for x in a for y in np.linspace(4.02,14,21)])
    sc=ins(pc)
    # how much further is clear: radius margin
    pm=np.array([(bx+rr*np.cos(x),y,bz+rr*np.sin(x)) for rr in (3.55,3.65,3.8,4.2) for x in a for y in np.linspace(4.02,14,21)])
    sm=ins(pm); 
    rmin=min([rr for rr,sol in zip(np.repeat([3.55,3.65,3.8,4.2],24*21),sm) if sol],default=None)
    # seat: solid just under y=4 around hole r 1.9..3.5
    ps=np.array([(bx+rr*np.cos(x),3.9,bz+rr*np.sin(x)) for rr in (1.9,2.7,3.45) for x in a]); ss=ins(ps)
    rep(f'screw head {k}: dia 7 x 10 clear from Y +4 to +14', sc.sum()==0, f'{len(pc)} pts, {sc.sum()} solid; first solid radius found in y 4..14: {rmin}; seat solid at y 3.9 r 1.9..3.45: {ss.sum()}/{len(ps)}')
# 4 pin
a=np.linspace(0,2*np.pi,36,endpoint=False)
for sgn in (1,-1):
    ys=np.linspace(16.05,21.95,8)*sgn
    pin=np.array([(rr*np.cos(x),y,-200+rr*np.sin(x)) for rr in (0,2,3.9) for x in a for y in np.r_[ys,sgn*22.3,sgn*15.7]])
    si=ins(pin).sum()
    res=[]
    for rr in (4.1,6,8,8.9,9.0,9.5,10.5,12):
        pw=np.array([(rr*np.cos(x),y,-200+rr*np.sin(x)) for x in a for y in ys]); res.append((rr,int(ins(pw).sum()),len(pw)))
    ok5=all(s==nn for rr,s,nn in res if rr<=8.9)
    d=np.hypot(v[:,0],v[:,2]+200); m=(np.abs(d-4)<0.2)&(np.sign(v[:,1])==sgn)
    rep(f'pin hole dia 8 at X 0 Z -200, cheek Y {sgn*16:+.0f}..{sgn*22:+.0f}', si==0 and abs(np.median(d[m])-4)<0.02, f'clear pts solid {si}/{len(pin)}; vertex r {d[m].min():.3f}..{d[m].max():.3f}, y {v[m][:,1].min():.2f}..{v[m][:,1].max():.2f}; axis centroid x {v[m][:,0].mean():.3f} z {v[m][:,2].mean():.3f}')
    rep(f'>=5 mm material round pin hole, cheek {sgn:+d} (solid r 4.1..8.9 over full cheek thickness)', ok5, 'solid/total at r: '+', '.join(f'{rr}:{s}/{nn}' for rr,s,nn in res))
    # per-y minimal wall
    walls=[]
    for y in ys:
        rmax=4
        for rr in np.arange(4.1,14,0.1):
            pw=np.array([(rr*np.cos(x),y,-200+rr*np.sin(x)) for x in a])
            if ins(pw).all(): rmax=rr
            else: break
        walls.append(round(rmax-4,1))
    rep(f'  wall thickness all round by y, cheek {sgn:+d}', min(walls)>=4.95, f'y {np.round(ys,2).tolist()} -> wall mm {walls}')
    # inner cheek face flat over dia 16
    on=(np.abs(t[:,:,1]-sgn*16).max(axis=1)<1e-3)&(np.abs(n[:,1])>0.999)
    A=area[on].sum(); tt=t[on]; dd=np.hypot(tt[:,:,0],tt[:,:,2]+200)
    pf=np.array([(rr*np.cos(x),sgn*16.05,-200+rr*np.sin(x)) for rr in (4.15,5,6,7,7.95) for x in a]); pcl=pf.copy(); pcl[:,1]=sgn*15.95
    sf=ins(pf); scl=ins(pcl)
    rep(f'inner cheek face Y {sgn*16:+.0f} flat over dia 16', sf.all() and scl.sum()==0, f'planar area on plane {A:.1f} mm2 (annulus dia 8..16 = {math.pi*(64-16):.1f}), normals y {n[on][:,1].mean():+.3f}; solid at |y| 16.05: {sf.sum()}/{len(pf)}; solid at |y| 15.95: {scl.sum()}/{len(pcl)}; plane reaches r {dd.max():.1f}')
# 5 slot
pp=np.array([(rr*np.cos(x),y,-200+rr*np.sin(x)) for rr in np.linspace(0,14.95,12) for x in a for y in np.linspace(-15.95,15.95,13)])
s=ins(pp); rep('slot: swept dia 30 cylinder about pin axis clear, |y|<=15.95', s.sum()==0, f'{len(pp)} pts, {s.sum()} solid')
pp=np.array([(x,y,z) for x in np.linspace(-20,20,41) for y in np.linspace(-15.95,15.95,13) for z in np.linspace(-183,-214,32)])
s=ins(pp); rep('slot: whole slab |y|<=15.95, Z -183 to -214, X -20..20 clear', s.sum()==0, f'{len(pp)} pts, {s.sum()} solid')
# arch above
zs=np.arange(-183,-160,0.25); top=[z for z in zs if not ins(np.array([[0,0,z]]))[0]]
ztop={}
for y in (0,8,12,15):
    col=np.array([(0.0,y,z) for z in np.arange(-183,-150,0.1)]); s=ins(col); ztop[y]=round(float(col[np.argmax(s),2]),1) if s.any() else None
rep('INFO slot roof (first solid above Z -183 at x 0)', True, f'{ztop} (arch R16: apex -167 at y 0)')
# 6 cable
zz=np.arange(35,-214,-0.5)
core=np.array([(rr*np.cos(x),rr*np.sin(x),z) for z in zz for rr in (0,1.5,3.0) for x in np.linspace(0,2*np.pi,12,endpoint=False)])
s=ins(core).reshape(len(zz),-1).any(axis=1)
rep('cable: straight dia 6 clear along Z at X 0 Y 0, from Z +35 to Z -213.5', not s.any(), f'blocked z: {zz[s].min() if s.any() else None}..{zz[s].max() if s.any() else None}; {len(core)} pts')
for rr in (3.1,3.25):
    c2=np.array([(rr*np.cos(x),rr*np.sin(x),z) for z in zz for x in np.linspace(0,2*np.pi,24,endpoint=False)])
    s2=ins(c2).reshape(len(zz),-1)
    print(f'   r {rr}: solid fraction by z ranges:', [(float(zz[i]),round(float(s2[i].mean()),2)) for i in range(0,len(zz),20)])
# enclosure: ring at r 3.5 solid all round?
for rr in (3.5,3.9):
    ringp=np.array([(rr*np.cos(x),rr*np.sin(x),z) for z in zz for x in np.linspace(0,2*np.pi,24,endpoint=False)])
    s3=ins(ringp).reshape(len(zz),-1); full=s3.all(axis=1); anyy=s3.mean(axis=1)
    idx=np.flatnonzero(full)
    print(f'   enclosure r {rr}: fully enclosed z from {zz[idx].max() if len(idx) else None} to {zz[idx].min() if len(idx) else None}, count {len(idx)} of span; partial:', [(float(zz[i]),round(float(anyy[i]),2)) for i in range(len(zz)) if 0<anyy[i]<1][:40])
# is the unenclosed cable inside the form's envelope? (bore: within hub; slot: between cheeks)
# skin thickness over tunnel in hub
for z in (-16,-18,-20,-22,-26,-30):
    col=np.array([(0,y,z) for y in np.arange(-6,14,0.05)]); s=ins(col); ys=col[s,1]
    print(f'   z {z}: solid y ranges at x 0:', [ (round(a,2),round(b,2)) for a,b in zip(ys[np.r_[True,np.diff(ys)>0.07]], ys[np.r_[np.diff(ys)>0.07,True]])])
