"""D2 study driver: python d2_fea.py <Y|X> <contact|bonded> <el,el,...> [tag]
One job (<= 4 studies). Saves each result to _wip/.../d2/npz/<tag>_<case>_<mode>_<el>.npz and prints rows. Never run under timeout."""
import json, math, sys
from pathlib import Path
import numpy as np
ROOT = Path(r'J:\code\cad-daddy-wt\sw-eval-sonnet-adv-d'); sys.path.insert(0, str(ROOT / 'solidworks'))
from swkit import *
from swfea import PETG, STEEL, NO_PENETRATION, BONDED, SOLVER_DIRECT, static
W = ROOT / '_wip' / 'sw-eval' / 'sonnet-adv-d' / 'd2'; RUN = ROOT / 'eval' / 'sonnet-adv-d'
(W / 'npz').mkdir(exist_ok=True)
case, mode, els = sys.argv[1], sys.argv[2], [float(v) for v in sys.argv[3].split(',')]
tag = sys.argv[4] if len(sys.argv) > 4 else 'run'
F = (0.0, 300.0, 0.0) if case == 'Y' else (300.0, 0.0, 0.0)
PAD = dict(name='Soft pad', EX=0.5e6, NUXY=0.45, DENS=1000.0, SIGYLD=1e6, SIGXT=1e6)
SCREWS = [(sx * 31.0, z) for sx in (1, -1) for z in (0.0, 7.0)]
PADS = [(17.68, 17.68), (-17.68, 17.68), (-17.68, -17.68), (17.68, -17.68)]
with job(wait_s=1800) as j:
    stamp(RUN, f'D2 fea job {tag} {case} {mode} {els}: instance up')
    j.simulation()
    import os; d = open_doc(j.sw, W / (os.environ.get('D2_MODEL', 'pair_fe') + '.SLDPRT')); d.ForceRebuild3(False)
    held = pick(d, kind='plane', normal=(0, -1, 0), at=(0, -32, 3.5))
    bore = pick(d, kind='cyl', r=24.0, tol=0.01)
    od = pick(d, kind='cyl', r=25.95, tol=0.01)
    seats = pick(d, kind='cyl', r=26.0, tol=0.01)
    # each half's split face is TWO patches (the opening cuts it at X -23..23): both belong in the contact set (the first runs, tags a and c, had only +X)
    up_split = pick(d, kind='plane', normal=(0, -1, 0), at=(30, 0, 3.5)) + pick(d, kind='plane', normal=(0, -1, 0), at=(-30, 0, 3.5))
    lo_split = pick(d, kind='plane', normal=(0, 1, 0), at=(30, 0, 3.5)) + pick(d, kind='plane', normal=(0, 1, 0), at=(-30, 0, 3.5))
    for nm, fs, n in (('held face', held, 1), ('ring bore', bore, 1), ('ring OD', od, 1), ('seats', seats, 2), ('upper split', up_split, 2), ('lower split', lo_split, 2)):
        expect(nm + ' faces', len(fs), n, 0)
    kind = NO_PENETRATION if mode == 'contact' else BONDED
    vol_pred = 38600 + 1600
    for el in els:
        nodes_pred = 12 * vol_pred / el ** 3 * 1.6
        log(f'PREDICT {case} {mode} {el}: nodes about {nodes_pred:.0f}; ring moves about 0.05 mm (closing the 0.05 radial clearance) then 0.01 mm; screws carry about 75 N each for +Y (tension), the peak in the seat wall near the load, bores and screw holes not the governing place')
        r = static(j, d, f'D2_{case}_{mode}_{el}', PETG, fixtures=[('fixed', held)],
                   loads=[('bearing', bore, F)], el=el,
                   ctrl=[(od + seats, max(el * 0.5, 0.8))], contacts=[(kind, od, seats), (kind, up_split, lo_split)],
                   materials={'ring': STEEL, 'pin': STEEL, 'pad': PAD}, solver=SOLVER_DIRECT, loose_ok=True, max_nodes=200000)
        np.savez_compressed(W / 'npz' / f'{tag}_{case}_{mode}_{el}.npz', pos=r.pos, s=r.s, disp=r.disp, reaction=np.array(r.reaction),
                            nodes=r.nodes, el=el, seconds=r.seconds, excessive=bool(getattr(r, 'excessive', False)))
        log('SUMMARY', r.summary())
        log('STUDY DONE', case, mode, el, r.nodes, 'excessive' if getattr(r, 'excessive', False) else 'ok')
    close(j.sw, d)
    stamp(RUN, f'D2 fea job {tag} {case} {mode} {els}: done')
print('D2 FEA DONE')
