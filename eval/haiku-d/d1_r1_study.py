"""D1 variant study: pull case (9 N, board pulled off) on buck_mount_r1.SLDPRT at element sizes 1.5 and 1.0 mm.

The fixtures and loads are the ones of d1_study.py (M5 hole walls fixed, four boss tops loaded). Output is compared with
the sharp-corner model in d1_study_results.json and d1_conv_el1.json.
"""
import sys, json
from pathlib import Path
import numpy as np
WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT / 'solidworks'))
from swfea import PETG, static  # noqa: E402
from swkit import job, open_doc, pick, expect, log  # noqa: E402
from d1_study import BOSS_TOPS  # noqa: E402

R1 = WT / '_wip' / 'sw-eval' / 'haiku-d' / 'd1' / 'buck_mount_r1.SLDPRT'

if __name__ == '__main__':
    out = []
    with job(wait_s=1800) as j:
        j.simulation()
        d = open_doc(j.sw, R1)
        d.ForceRebuild3(False)
        holes = pick(d, kind='cyl', r=2.75, inside=[-30, 9.9, -13.0, 30, 14.1, -7.0])
        tops = [f for x, y, z in BOSS_TOPS for f in pick(d, kind='plane', normal=(0, 1, 0), at=(x, y, z))]
        expect('two M5 hole walls', len(holes), 2, 0)
        expect('four boss tops', len(tops), 4, 0)
        for el in (1.5, 1.0):
            r = static(j, d, f'D1_R1_PULL_EL{str(el).replace(".", "")}', PETG, fixtures=[('fixed', holes)],
                       loads=[('normal', tops, -9.0)], el=el, max_nodes=200_000)
            expect(f'el {el} reaction resultant equals load', r.reaction[3], 9.0, 0.01)
            mask = (np.abs(r.pos[:, 0]) > 20) & (r.pos[:, 2] > -3) & (r.pos[:, 2] < 33)
            corner = (np.abs(np.abs(r.pos[:, 0]) - 35.5) < 1.5) & (r.pos[:, 2] > -9) & (r.pos[:, 2] < -4)
            out.append(dict(el=el, nodes=r.nodes, max_disp_mm=float(r.max_disp()),
                            peak_excl_corners_mpa=float(r.peak(mask)[0]), peak_excl_corners_at=r.peak(mask)[1],
                            vm_max_all_mpa=float(r.vm.max()), vm_max_at=r.pos[int(np.argmax(r.vm))].round(2).tolist(),
                            vm_max_near_old_corner_mpa=float(r.vm[corner].max())))
            log(out[-1])
    (WT / 'eval' / 'haiku-d' / 'd1_r1_results.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out, indent=2))
