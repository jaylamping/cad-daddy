import sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
GAP=.6; SEAT=52.15; OPENING=45.; ZLOW=-.15; ZHIGH=7.15

def seg(r):
 a=GAP/2
 return math.pi*r*r/2-(a*math.sqrt(r*r-a*a)+r*r*math.asin(a/r))

def cut(d,axis,coord,name,draw,depth,dv):
 with Sk(d,plane(d,axis,coord,name+'_P'),name) as s: draw(s)
 extrude(d,s.feat,name,depth,cut=True,mode=MID,expect_dv=dv);save(d)

def run(j,upper):
 name='housing_upper' if upper else 'housing_lower'
 d=new_part(j.sw,OUT/(name+'.SLDPRT')); yc=(.3+32)/2*(1 if upper else -1)
 with Sk(d,plane(d,'Z',3.5,'BLOCK_P'),'BLOCK') as s:
  s.rect((-36,.3 if upper else -32,3.5),(36,32 if upper else -.3,3.5))
 extrude(d,s.feat,'BLOCK',15,mode=MID,expect_dv=72*31.7*15);save(d)
 cut(d,'Z',3.5,'OPENING',lambda s:s.circle((0,0,3.5),OPENING/2),15,seg(OPENING/2)*15)
 cut(d,'Z',3.5,'SEAT',lambda s:s.circle((0,0,3.5),SEAT/2),7.3,(seg(SEAT/2)-seg(OPENING/2))*7.3)
 if upper:
  def circles(s):
   for x in (-30.5,30.5):
    for z in (0,7): s.circle((x,yc,z),1.7)
  cut(d,'Y',yc,'SCREW_HOLES',circles,31.7,4*math.pi*1.7**2*31.7)
  def cb(s):
   for x in (-30.5,30.5):
    for z in (0,7): s.circle((x,30.25,z),3)
  cut(d,'Y',30.25,'COUNTERBORES',cb,3.5,4*math.pi*(3**2-1.7**2)*3.5)
 else:
  def inserts(s):
   for x in (-30.5,30.5):
    for z in (0,7): s.circle((x,-3.3,z),2)
  cut(d,'Y',-3.3,'M3_INSERTS',inserts,6,4*math.pi*2**2*6)
  def mounts(s):
   for x in (-24,24):s.circle((x,-28,3.5),2.8)
  cut(d,'Y',-28,'M4_INSERTS',mounts,8,2*math.pi*2.8**2*8)
 print(name,'volume',volume(d),'box',bbox(d),'bodies',bodies(d),'errors',feature_errors(d),flush=True)
 single_body(d);save(d);save_as(d,OUT/(name+'.stl'));close(j.sw,d)

with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True)
 d=new_part(j.sw,OUT/'ring.SLDPRT')
 with Sk(d,plane(d,'Z',3.5,'RING_P'),'RING') as s:
  s.circle((0,0,3.5),26);s.circle((0,0,3.5),24)
 extrude(d,s.feat,'RING',7,mode=MID,expect_dv=math.pi*(26**2-24**2)*7)
 print('ring',volume(d),bbox(d),bodies(d),feature_errors(d),flush=True);save(d);save_as(d,OUT/'ring.stl');close(j.sw,d)
 run(j,True);run(j,False)

