import json
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(RUN)); sys.path.insert(0, str(ROOT / 'tools' / 'solidworks'))
from b4_tongue import CONTACT_MODEL, PAD_MAT, pad_reaction_post, forces_from_sections, tongue_mask
from swkit import NUL, Sk, close, expect, job, open_doc, pick, plane
from swfea import PETG, NO_PENETRATION, SOLVER_DIRECT, static
SIM = ROOT / 'cad' / '_sim' / 'sw-eval' / 'luna-b'
with job(wait_s=1800) as j:
    j.simulation()
    d = open_doc(j.sw, CONTACT_MODEL); d.ForceRebuild3(False)
    bottom = pick(d, kind='plane', normal=(0,0,-1), at=(0,0,0))
    wp = pick(d, kind='plane', normal=(-1,0,0), at=(4.1,0,14))
    wm = pick(d, kind='plane', normal=(1,0,0), at=(-4.1,0,14))
    tp = pick(d, kind='plane', normal=(1,0,0), at=(4,0,14))
    tm = pick(d, kind='plane', normal=(-1,0,0), at=(-4,0,14))
    load = pick(d, kind='plane', normal=(-1,0,0), at=(-3.9,0,35), area=200)
    pads=[]
    for y,z in ((-5,24),(5,24),(-5,28),(5,28)):
        pads += pick(d, kind='plane', normal=(1,0,0), at=(8,y,z), area=1)
    r = static(j,d,'B4_FULL_DIAG',PETG,fixtures=[('fixed',bottom+pads)],loads=[('normal',load,80)],
               el=4.0,ctrl=[(wp+wm+tp+tm,2.0),(load,2.0)],
               contacts=[(NO_PENETRATION,wp,tp),(NO_PENETRATION,wm,tm)],materials={'PAD':PAD_MAT},
               solver=SOLVER_DIRECT,loose_ok=True,max_nodes=199999,post=pad_reaction_post)
    p=r.pos; m=tongue_mask(r); tip=m&(p[:,2]>=39.8)
    info={'summary':r.summary(),'tip_ux_mm':float(r.disp[tip,1].max()),'pad_reaction':r.extra,
          'sections':forces_from_sections(r),'excessive':getattr(r,'excessive',False)}
    np.savez_compressed(SIM/'B4_full_diag.npz',pos=r.pos,stress=r.s,displacement=r.disp,fixed_points=r.fixed_pts,loaded_points=r.loaded_pts)
    (RUN/'b4_full_diag.json').write_text(json.dumps(info,indent=2),encoding='utf-8')
    print(json.dumps(info,indent=2),flush=True)
    close(j.sw,d)
