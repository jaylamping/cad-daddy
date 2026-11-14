import sys
from pathlib import Path
R=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(R/'tools/solidworks'))
import swkit
from swkit import *
swkit.pin_export_prefs=lambda sw: None
O=R/'cad/_wip/sw-eval/terra-high-c'
with job(wait_s=1800) as j:
 print('OWN PID',j.inst.pid,flush=True)
 d=open_doc(j.sw,O/'fillet_e.SLDPRT')
 es=edges_where(d,lambda p: -38<p[2]<-28 and abs(p[1])<14 and abs(p[0])<27)
 print('CANDIDATES',len(es),flush=True)
 for i,e in enumerate(es):
  cp=e.GetCurveParams3; mid=e.GetCurve.Evaluate2((cp.UMinValue+cp.UMaxValue)/2,0)
  print('EDGE',i,[[round(a*1000,3) for a in list(v)[:3]] for v in (cp.StartPoint,mid,cp.EndPoint)],flush=True)
 radius=fillet(d,es,(2,1,0.4),'NECK_ROUND') if es else None
 print('FILLET',radius,flush=True)
 if radius:
  print('VOLUME',volume(d),'BODIES',bodies(d),'ERRORS',feature_errors(d),flush=True)
  save(d); save_as(d,O/'fillet_e.stl')
