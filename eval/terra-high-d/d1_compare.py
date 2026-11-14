import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'tools/solidworks'))
from swfea import Result
OUT=ROOT/'cad/_wip/sw-eval/terra-high-d'
for name,el in [('d1_30',3),('d1_uplift',2),('d1_15',1.5)]:
 p=np.load(OUT/(name+'.npz'));r=Result(name,el,p['pos'],p['s'],p['fixed_pts'],p['loaded_pts'],p['disp'],p['reaction'],len(p['pos']),0,0,9)
 m=r.away(dist=6); print(name, 'nodes',r.nodes,'disp',r.max_disp(),'peak',r.peak(m),'z_tension',r.layer_stress((0,0,1),m),'z_shear',r.layer_shear((0,0,1),m),'all_max',r.vm.max())
