import sys
from pathlib import Path
sys.path.insert(0,str(Path('tools/solidworks').resolve()))
import swkit as k
from swkit import *
k.pin_export_prefs=lambda sw:None
out=Path('cad/_wip/sw-eval/terra-high-b2').resolve()
with job(wait_s=1800) as j:
 for file in ('hub.SLDPRT','wall_bracket.SLDPRT','wall_bracket_light.SLDPRT'):
  d=open_doc(j.sw,out/file); print('MODEL',file,'volume',volume(d),'box',bbox(d),'bodies',bodies(d),'errors',feature_errors(d),flush=True)
  if file=='hub.SLDPRT':
   for p in ((6.4,0,12.5),(5.8,1.5,12.5),(5.8,-1.5,12.5),(20,0,5),(10,0,25)):
    fs=pick(d,kind='plane',at=p); print('FACE',p,len(fs),[face_info(f) for f in fs],flush=True)
  else:
   for r in (2.25,3.0):
    fs=pick(d,kind='cyl',r=r); print('CYL',r,len(fs),[face_info(f) for f in fs],flush=True)
  close(j.sw,d)
