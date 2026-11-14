import sys
from pathlib import Path
R=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(R/'tools/solidworks'))
import swkit
from swkit import *
swkit.pin_export_prefs=lambda sw:None
O=R/'cad/_wip/sw-eval/terra-high-c'
with job(wait_s=1800) as j:
 print('OWN PID',j.inst.pid,flush=True)
 d=open_doc(j.sw,O/'link_organic.SLDPRT')
 print('NATIVE VOLUME',volume(d),'BBOX',bbox(d),'BODIES',bodies(d),'FEATURE ERRORS',feature_errors(d),flush=True)
 for radius in [1.7,4,15]:
  fs=pick(d,kind='cyl',r=radius); print('CYL',radius,len(fs),[face_info(f) for f in fs],flush=True)
 for pt in [(20,-4,0),(0,16,-208),(0,-16,-208)]:
  fs=pick(d,kind='plane',at=pt); print('PLANE',pt,len(fs),[face_info(f) for f in fs],flush=True)
 save_as(d,O/'link_organic.step')
 close(j.sw,d)
 x,target=import_step(j.sw,O/'link_organic.step',O/'step_roundtrip')
 print('STEP ROUNDTRIP',target,'volume',volume(x),'bbox',bbox(x),'bodies',bodies(x),'errors',feature_errors(x),flush=True)
