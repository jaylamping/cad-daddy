import sys, math, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
OUT=ROOT/'cad/_wip/sw-eval/terra-high-c'
with job(wait_s=1800) as j:
    print('OWN PID',j.inst.pid,flush=True)
    d=new_part(j.sw,OUT/'link_boxy.SLDPRT')
    with Sk(d,plane(d,'Y',0,'DISC_P'),'DISC') as s: s.circle((0,0,0),35)
    extrude(d,s.feat,'DISC',8,mode=MID,expect_dv=math.pi*35**2*8); save(d)
    with Sk(d,plane(d,'Y',0,'BEAM_P'),'BEAM') as s: s.rect((-20,0,-170),(20,0,-32))
    extrude(d,s.feat,'BEAM',30,mode=MID); save(d)
    with Sk(d,plane(d,'Z',-175,'BRIDGE_P'),'BRIDGE') as s: s.rect((-20,-22,-175),(20,22,-175))
    extrude(d,s.feat,'BRIDGE',10,mode=MID); save(d)
    for sign in (-1,1):
        y=19*sign
        with Sk(d,plane(d,'Y',y,'CHEEK_P'+str(sign)),'CHEEK'+str(sign)) as s: s.rect((-15,y,-215),(15,y,-180))
        extrude(d,s.feat,'CHEEK'+str(sign),6,mode=MID,expect_dv=30*35*6); save(d)
    with Sk(d,plane(d,'Y',0,'MOUNT_P'),'MOUNT') as s:
        s.circle((0,0,0),15)
        for k in range(6):
            a=math.pi*k/3; s.circle((25*math.cos(a),0,25*math.sin(a)),1.7)
    extrude(d,s.feat,'MOUNT',8,cut=True,mode=MID); save(d)
    with Sk(d,plane(d,'Y',0,'PIN_P'),'PIN') as s: s.circle((0,0,-200),4)
    extrude(d,s.feat,'PIN',44,cut=True,mode=MID,expect_dv=math.pi*16*12); save(d)
    print('VOLUME',volume(d),'BBOX',bbox(d),'BODIES',bodies(d),'ERRORS',feature_errors(d),flush=True)
    single_body(d); save(d)
    save_as(d,OUT/'link_boxy.stl')
    print('EXPORTED',flush=True)
