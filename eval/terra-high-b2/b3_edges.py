import sys
from pathlib import Path
sys.path.insert(0,str(Path('tools/solidworks').resolve()))
import swkit as k
from swkit import *
k.pin_export_prefs=lambda sw:None
with job(wait_s=1800) as j:
 d=open_doc(j.sw,Path('cad/_wip/sw-eval/terra-high-b2/wall_bracket_light_14_sharp.SLDPRT').resolve())
 for b in solid_bodies(d):
  for e in call(b,'GetEdges'):
   cp=e.GetCurveParams3; a=[round(x*1000,3) for x in cp.StartPoint[:3]]; z=[round(x*1000,3) for x in cp.EndPoint[:3]]
   if max(a[0],z[0])<8.1 and min(a[2],z[2])<53 and max(a[2],z[2])>39: print('EDGE',a,z,flush=True)
