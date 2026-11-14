import sys
from pathlib import Path
R=Path(__file__).resolve().parents[5]; sys.path.insert(0,str(R/'tools/solidworks'))
import swkit
from swkit import *
swkit.pin_export_prefs=lambda sw:None
O=R/'cad/_wip/sw-eval/terra-high-c'
with job(wait_s=1800) as j:
 print('OWN PID',j.inst.pid,flush=True)
 for name in ['link_boxy','link_organic']:
  d=open_doc(j.sw,O/(name+'.SLDPRT'))
  print('PART',name,'VOL',volume(d),'BBOX',bbox(d),'BODY',bodies(d),'ERRORS',feature_errors(d),flush=True)
  for radius in [1.7,4,15]:
   fs=pick(d,kind='cyl',r=radius); print('CYL',radius,len(fs),[face_info(f) for f in fs],flush=True)
  for pt in [(20,-4,0),(0,16,-208),(0,-16,-208)]:
   fs=pick(d,kind='plane',at=pt); print('PLANE',pt,len(fs),[face_info(f) for f in fs],flush=True)
  if name=='link_organic': save_as(d,O/'link_organic.step')
  close(j.sw,d)
 d=open_doc(j.sw,O/'bearing_probe.SLDPRT')
 with Sk(d,plane(d,'Y',0,'CENTER_P'),'BEARING_CENTER') as s:
  uv=s.p((0,0,-200)); point=d.SketchManager.CreatePoint(uv[0],uv[1],0)
  print('POINT',point is not None,flush=True)
 d.ClearSelection2(True)
 sel=d.SelectionManager.CreateSelectData; sel.Mark=1
 print('point selected',point.Select4(False,sel),flush=True)
 fs=pick(d,kind='cyl',r=4); sel2=d.SelectionManager.CreateSelectData; sel2.Mark=8
 print('cylinder selected',fs[0].Select4(True,sel2),flush=True)
 f=d.FeatureManager.InsertCoordinateSystem(False,False,False)
 print('COORD',f,flush=True)
 if f:
  f.Name='BEARING_CSYS'; save(d)
  tr=d.Extension.GetCoordinateSystemTransformByName('BEARING_CSYS')
  print('TRANSFORM',tr.ArrayData if tr else None,flush=True)
