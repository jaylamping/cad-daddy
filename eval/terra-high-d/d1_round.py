import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True); d=open_doc(j.sw,OUT/'buck_mount.SLDPRT')
 e=edges_where(d,lambda p: abs(abs(p[0])-35)<.02 and min(abs(abs(p[1])-5),abs(abs(p[1])-25))<.02)
 print('corner edges',len(e),flush=True)
 assert len(e)==8
 assert fillet(d,e,(0.4,),'WINDOW_ROUND') is not None
 print('volume',volume(d),'box',bbox(d),'errors',feature_errors(d),'bodies',bodies(d),flush=True)
 save(d);save_as(d,OUT/'buck_mount.stl');save_as(d,OUT/'buck_mount.step');close(j.sw,d)
