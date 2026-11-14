import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swkit import *
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
with job(wait_s=1800) as j:
 print('PID',j.inst.pid,flush=True);d=open_doc(j.sw,OUT/'housing_lower_round.SLDPRT');save_as(d,OUT/'housing_fea_round.SLDPRT')
 for name in ['housing_upper_round','ring']+['bolt_'+str(i) for i in range(4)]+['pad_'+str(i) for i in range(4)]:
  insert_body(d,OUT/(name+'.SLDPRT'));save(d)
 print('ASSEMBLY',bodies(d),'errors',feature_errors(d),flush=True);save(d);close(j.sw,d)
