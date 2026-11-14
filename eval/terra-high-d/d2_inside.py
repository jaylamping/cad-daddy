import sys,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
import sheet
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
for name,typ in [('housing_upper.stl','upper'),('housing_lower.stl','lower'),('housing_upper_transition.stl','upper'),('housing_lower_transition.stl','lower')]:
 tri=sheet.read_stl(OUT/name); checks=[]
 for x in (-30.5,30.5):
  for z in (0,7):
   defs=([(16,1.7),(30.5,3)] if typ=='upper' else [(-3.3,2)])
   for y,r in defs:
    checks.extend([(f'hole_{x}_{y}_{z}_centre',(x,y,z),False),(f'hole_{x}_{y}_{z}_outside',(x+r+.3,y,z),True)])
 if typ=='lower':
  for x in (-24,24):checks.extend([(f'mount_{x}_centre',(x,-28,3.5),False),(f'mount_{x}_outside',(x+3.1,-28,3.5),True)])
 got=sheet.inside(tri,np.array([x[1] for x in checks],float));bad=[(label,pt,want,bool(g)) for (label,pt,want),g in zip(checks,got) if want!=g]
 print(name,'samples',len(checks),'failed',bad)
