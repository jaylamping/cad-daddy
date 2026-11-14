"""D1 convergence: the pull case at element size 1.0 mm (the 1.5 mm run is in d1_study_results.json).

Predicted nodes at el 1.0: about 12 x 8821 / 1.0 = 106,000 (local controls not used), under the 200,000 heavy-solve limit.
"""
import sys, json
from pathlib import Path
import numpy as np
WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT / 'solidworks'))
from swfea import PETG, static  # noqa: E402
from swkit import job, open_doc, pick, log  # noqa: E402
from d1_study import MODEL, BOSS_TOPS  # noqa: E402

if __name__ == '__main__':
    out = {}
    with job(wait_s=1800) as j:
        j.simulation()
        d = open_doc(j.sw, MODEL)
        d.ForceRebuild3(False)
        holes = pick(d, kind='cyl', r=2.75, inside=[-30, 9.9, -13.0, 30, 14.1, -7.0])
        tops = [f for x, y, z in BOSS_TOPS for f in pick(d, kind='plane', normal=(0, 1, 0), at=(x, y, z))]
        assert len(holes) == 2 and len(tops) == 4
        r = static(j, d, 'D1_PULL_9N_EL10', PETG, fixtures=[('fixed', holes)],
                   loads=[('normal', tops, -9.0)], el=1.0, max_nodes=200_000)
        print(r.summary(), flush=True)
        mask = (np.abs(r.pos[:, 0]) > 20) & (r.pos[:, 2] > -3) & (r.pos[:, 2] < 33)
        out = dict(nodes=r.nodes, elements=r.elements, reaction_resultant_n=float(r.reaction[3]),
                   max_disp_mm=float(r.max_disp()), vm_max_all_mpa=float(r.vm.max()),
                   peak_vm_mpa_excl_corners=float(r.peak(mask)[0]), peak_where=r.peak(mask)[1],
                   vm_max_where=r.pos[int(np.argmax(r.vm))].round(2).tolist())
    (WT / 'eval' / 'haiku-d' / 'd1_conv_el1.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out, indent=2))
