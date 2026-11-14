"""The benchmark's governing case on the real link: 60 N along +Y at the wrist pin, elbow ring held (eval/sonnet-c2).

    python eval/loft-blend/link_fea.py <el mm> <tag> [<tag> ...]      # at most three per run; appends to link_fea.json

Mesh as in that run: one global size, 1.2 mm on the pin bore. The junction is read between Z -52 and -20, outside the
default exclusion round the fixture and the load.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import OUT  # noqa: E402
from swfea import PETG, static  # noqa: E402
from swkit import close, job, log, open_doc, pick, volume  # noqa: E402

HERE = Path(__file__).resolve().parent
EL = float(sys.argv[1])
f = HERE / 'link_fea.json'
res = json.loads(f.read_text()) if f.exists() else {}
with job(wait_s=1800) as j:
    j.simulation()
    for tag in sys.argv[2:]:
        d = open_doc(j.sw, OUT / f'link_{tag}.SLDPRT')
        d.ForceRebuild3(False)
        ring = pick(d, kind='plane', normal=(0, -1, 0), at=(20, -4, 0))
        tip = pick(d, kind='cyl', r=4.0, inside=[-5, -30, -205, 5, 30, -195])
        log(tag, 'ring faces', len(ring), 'pin faces', len(tip))
        if len(ring) != 1 or len(tip) < 1:
            raise SystemExit('bad picks')
        r = static(j, d, f'{tag}_PY_{EL}', PETG, fixtures=[('fixed', ring)],
                   loads=[('remote', tip, (0, 0, -200), (0, 60, 0), (0, 0, 0))], el=EL, ctrl=[(tip, 1.2)], loose_ok=True)
        away = r.away()
        zone = away & (r.pos[:, 2] > -52) & (r.pos[:, 2] < -20)
        rest = away & (r.pos[:, 2] <= -52)
        k = np.flatnonzero(zone)[np.argmax(r.vm[zone])]
        row = dict(nodes=r.nodes, volume=round(volume(d), 1), reaction=r.reaction, disp=round(r.max_disp(), 3),
                   junction_vm=round(float(r.vm[k]), 2), at=r.pos[k].round(2).tolist(),
                   junction_avg_1mm=[round(v, 2) for v in r.average(r.pos[k], 1.0)],
                   junction_avg_2mm=[round(v, 2) for v in r.average(r.pos[k], 2.0)],
                   rest_of_link_vm=round(float(r.vm[rest].max()), 2), overall_away=round(r.peak()[0], 2),
                   factor_junction=round(45 / float(r.vm[k]), 2))
        res.setdefault(tag, {})[str(EL)] = row
        log('RESULT', tag, EL, json.dumps(row))
        f.write_text(json.dumps(res, indent=1))
        close(j.sw, d)
