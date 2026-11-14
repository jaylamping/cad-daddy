import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True)
 for name in ('housing_upper','housing_lower','housing_upper_transition','housing_lower_transition','ring'):
  d=open_doc(j.sw,OUT/(name+'.SLDPRT')); print('PART',name,'box',bbox(d),'volume',volume(d),'errors',feature_errors(d),flush=True)
  for radius in (1.7,2.,2.8,3.,22.5,24.,26.,26.075,26.5):
   fs=pick(d,kind='cyl',r=radius,tol=.005)
   if fs:print('radius',radius,'count',len(fs),'faces',[face_info(f) for f in fs],flush=True)
  close(j.sw,d)
