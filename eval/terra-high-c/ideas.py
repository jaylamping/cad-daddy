import sys, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'tools/solidworks'))
import swkit
from swkit import *
swkit.pin_export_prefs=lambda sw: None
OUT=ROOT/'cad/_wip/sw-eval/terra-high-c'
idea=sys.argv[1] if len(sys.argv)>1 else 'a'
with job(wait_s=1800) as j:
    print('OWN PID',j.inst.pid,flush=True)
    d=new_part(j.sw,OUT/('idea_'+idea+'.SLDPRT'))
    with Sk(d,plane(d,'Y',0,'DISC_P'),'DISC') as s: s.circle((0,0,0),35)
    extrude(d,s.feat,'DISC',8,mode=MID,expect_dv=math.pi*35**2*8); save(d)
    # Two different continuous shaft ideas: A elliptical solid, B tapered diamond section.
    if idea in ('a','c','d','e'):
        paths=[(0, ([(-30,15,3),(-34,16,4),(-42,17,11),(-85,17,13),(-140,15,14),(-174,14,16),(-181,14,17)] if idea=='d' else (([( -32,24,12),(-44,22,16),(-85,17,13),(-140,15,14),(-174,14,16),(-181,14,17)] if idea=='e' else [(-32,14,8),(-44,16,12),(-85,17,13),(-140,15,14),(-174,14,16),(-181,14,17)]) if idea in ('c','e') else [(-34,7,3.8),(-44,14,11),(-85,17,13),(-140,15,14),(-174,14,16),(-181,14,17)])))]
    else:
        # Twin rails create a visible through-window and rejoin at the ends.
        paths=[(side*6,[(-34,3,3.8),(-44,5,8),(-85,4,9),(-140,4,10),(-174,9,16),(-181,9,17)]) for side in (-1,1)]
    for rail,(xc,dims) in enumerate(paths):
        sections=[]
        for n,(z,x,y) in enumerate(dims):
            with Sk(d,plane(d,'Z',z,'P%d_%d'%(rail,n)),'S%d_%d'%(rail,n)) as s:
                s.spline([(xc+x*math.cos(t*math.pi/6),y*math.sin(t*math.pi/6),z) for t in range(12)])
            sections.append(s.feat)
        loft(d,sections,'SHAFT'+str(rail)); save(d)
    # Smooth-ended fork cheeks: circle blended by overlap with neck, flat bearing faces.
    for sign in (-1,1):
        y=sign*19.5
        with Sk(d,plane(d,'Y',y,'CHEEK_P'+str(sign)),'CHEEK'+str(sign)) as s:
            pts=[(-13,y,-172),(13,y,-172),(13,y,-200)]
            pts += [(13*math.cos(math.radians(t)),y,-200+13*math.sin(math.radians(t))) for t in range(-15,-181,-15)]
            s.poly(pts)
        extrude(d,s.feat,'CHEEK'+str(sign),7,mode=MID); save(d)
    with Sk(d,plane(d,'Y',0,'MOUNT_P'),'MOUNT') as s:
        s.circle((0,0,0),15)
        for k in range(6):
            a=math.pi*k/3; s.circle((25*math.cos(a),0,25*math.sin(a)),1.7)
    extrude(d,s.feat,'MOUNT',8,cut=True,mode=MID); save(d)
    with Sk(d,plane(d,'Y',0,'PIN_P'),'PIN') as s: s.circle((0,0,-200),4)
    extrude(d,s.feat,'PIN',46,cut=True,mode=MID); save(d)
    with Sk(d,plane(d,'Z',-90,'CABLE_P'),'CABLE') as s: s.circle((0,0,-90),3)
    extrude(d,s.feat,'CABLE',190,cut=True,mode=MID); save(d)
    print('VOLUME',volume(d),'BBOX',bbox(d),'BODIES',bodies(d),'ERRORS',feature_errors(d),flush=True)
    single_body(d); save(d)
    save_as(d,OUT/('idea_'+idea+'.stl'))
