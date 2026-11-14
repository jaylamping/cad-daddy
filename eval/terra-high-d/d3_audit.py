import sys,json,math
from pathlib import Path
import trimesh
from d3_build import OUT,RUN,DATA,positions
from d3_edit import edited
for after in (False,True):
 for row0 in DATA:
  row=edited(row0) if after else row0;name,od,t,bore,A,B,cb,dep=row
  rec=json.loads((RUN/('d3_part2.json' if after else 'd3_part1.json')).read_text(encoding='utf-8'))['plates'][name]
  mesh=trimesh.load(OUT/(name+('_b' if after else '')+'.stl'))
  want=[[-od/2,-od/2,0],[od/2,od/2,t]]
  err=float(abs(mesh.bounds-want).max());volerr=abs(mesh.volume/rec['volume_mm3']-1)
  if err>.1 or volerr>.005 or not mesh.is_watertight or len(mesh.split())!=1:raise RuntimeError(f'bad export {name} b={after} box {err} vol {volerr}')
  flags=[]
  for label,pat,D in [('A',A,A[1]),('B counterbore',B,cb)]:
   edge=od/2-(1 if after else 0)-pat[2]/2
   if edge<D:flags.append(f'{label} centre to outer rim {edge:g} mm < diameter {D:g} mm')
  print(name+('_b' if after else ''),'STL bounds max error',round(err,4),'volume relative',round(volerr,6),'edge-distance questions',flags,flush=True)
