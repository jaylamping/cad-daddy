import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(ROOT/'tools/solidworks'))
import swkit as k
from swkit import *
k.pin_export_prefs=lambda sw: None
OUT=ROOT/'cad/_wip/sw-eval/terra-high-a'
with job(wait_s=1800) as j:
 for name in ('bracket','bracket_b'):
  d=open_doc(j.sw,OUT/(name+'.SLDPRT')); d.ForceRebuild3(False)
  print('AUDIT',name,'volume',volume(d),'bbox',bbox(d),'bodies',bodies(d),'errors',feature_errors(d),flush=True)
  for radius in (1.7,2.75,3,4,5,11):
   fs=pick(d,kind='cyl',r=radius)
   print('RADIUS',radius,'COUNT',len(fs),'INFO',[face_info(f) for f in fs],flush=True)
  if name=='bracket_b':
   for x in (25,65):
    for y in (10,40):
     fs=pick(d,kind='plane',at=(x+4,y,3)); print('FLOOR',x,y,len(fs),[face_info(f) for f in fs],flush=True)
  close(j.sw,d)
