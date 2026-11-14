import sys,math,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
import sheet
from d3_build import OUT,DATA,positions
from d3_edit import edited
for after in (False,True):
 for row0 in DATA:
  row=edited(row0) if after else row0
  name,od,t,bore,A,B,cb,dep=row;floor=t-dep
  checks=[]
  for x,y,z in positions(B,0):
   s=(B[1]/2+cb/2)/2
   checks += [('through', (x,y,t/2),False),('floor_below',(x+s,y,floor-.1),True),('floor_above',(x+s,y,floor+.1),False)]
  for x,y,z in positions(A,0):checks.append(('A hole',(x,y,t/2),False))
  checks.append(('bore',(0,0,t/2),False))
  path=OUT/(name+('_b' if after else '')+'.stl');inside=sheet.inside(sheet.read_stl(path),np.array([c[1] for c in checks],float))
  failures=[(label,pt,want,bool(got)) for (label,pt,want),got in zip(checks,inside) if want!=got]
  print(path.name,'samples',len(checks),'failures',failures,flush=True)
