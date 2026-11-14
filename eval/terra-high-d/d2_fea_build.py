import sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True)
 for i,(x,z) in enumerate(((-30.5,0),(-30.5,7),(30.5,0),(30.5,7))):
  name='bolt_'+str(i);d=new_part(j.sw,OUT/(name+'.SLDPRT'))
  with Sk(d,plane(d,'Y',-3.3,'THREAD_P'),'THREAD') as s:s.circle((x,-3.3,z),2)
  extrude(d,s.feat,'THREAD',6,mode=MID,expect_dv=math.pi*4*6);save(d)
  with Sk(d,plane(d,'Y',14.1,'SHANK_P'),'SHANK') as s:s.circle((x,14.1,z),1.5)
  extrude(d,s.feat,'SHANK',28.8,mode=MID,expect_dv=math.pi*2.25*28.8);save(d)
  with Sk(d,plane(d,'Y',30,'HEAD_P'),name.upper()) as s:s.circle((x,30,z),2.95)
  extrude(d,s.feat,name.upper(),3,mode=MID,expect_dv=math.pi*2.95**2*3);single_body(d);save(d);close(j.sw,d)
 p=math.sqrt(24**2-1);dv=(p+24**2*math.asin(1/24)-44)*3
 for i,ang in enumerate((0,math.pi/2,math.pi,3*math.pi/2)):
  name='pad_'+str(i);d=new_part(j.sw,OUT/(name+'.SLDPRT'))
  def q(x,y):return (x*math.cos(ang)-y*math.sin(ang),x*math.sin(ang)+y*math.cos(ang),3.5)
  with Sk(d,plane(d,'Z',3.5,'PAD_P'),name.upper()) as s:
   s.poly([q(22,-1),q(p,-1)],closed=False)
   s.arc((0,0,3.5),q(p,-1),q(p,1),+1)
   s.poly([q(p,1),q(22,1),q(22,-1)],closed=False)
  extrude(d,s.feat,name.upper(),3,mode=MID,expect_dv=dv);save(d);print(name,'volume',volume(d),flush=True);close(j.sw,d)
 d=open_doc(j.sw,OUT/'housing_lower.SLDPRT');save_as(d,OUT/'housing_fea.SLDPRT')
 for name in ['housing_upper','ring']+['bolt_'+str(i) for i in range(4)]+['pad_'+str(i) for i in range(4)]:
  insert_body(d,OUT/(name+'.SLDPRT'));save(d)
 print('ASSEMBLY BODIES',bodies(d),'errors',feature_errors(d),flush=True);save(d);close(j.sw,d)
