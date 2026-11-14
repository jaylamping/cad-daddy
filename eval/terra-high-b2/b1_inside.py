import sys,numpy as np
from pathlib import Path
sys.path.insert(0,str(Path('tools/solidworks').resolve()))
from sheet import read_stl, inside
p=np.array([(0,0,12),(5.8,0,12),(6.6,0,12),(0,6,22.6),(0,12,22.6),(0,0,24.8),(22,0,2.5),(0,15,2.5),(0,15,5.3)],float)
print(list(zip(p.tolist(),inside(read_stl('cad/_wip/sw-eval/terra-high-b2/hub.stl'),p).tolist())))
