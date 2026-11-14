"""Bend the test part's stem the weak way (20 N along Y at the top, disc held underneath) and read the junction.

    python eval/loft-blend/fea.py <ctrl mm> <part stem> [<part stem> ...]      # at most three parts per run

Same mesh for every part: 2.5 mm global, <ctrl> on every face above the disc except the loaded top, twice that on the disc top.
Appends to fea.json.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import OUT, TOP  # noqa: E402
from swfea import PETG, static  # noqa: E402
from swkit import close, face_info, faces, job, log, open_doc, pick, volume  # noqa: E402

HERE = Path(__file__).resolve().parent
CTRL = float(sys.argv[1])
f = HERE / 'fea.json'
res = json.loads(f.read_text()) if f.exists() else {}
with job(wait_s=1800) as j:
    j.simulation()
    for name in sys.argv[2:]:
        d = open_doc(j.sw, OUT / f'{name}.SLDPRT')
        d.ForceRebuild3(False)
        bottom = pick(d, kind='plane', normal=(0, 0, -1), at=(0, 0, -6))
        tip = pick(d, kind='plane', normal=(0, 0, 1), at=(0, 0, TOP))
        fine, coarse = [], []
        for x in faces(d):
            i = face_info(x)
            if i['box'][5] < 0.01 or x in tip:
                if i['kind'] == 'plane' and abs(i['box'][5]) < 0.01 and abs(i['box'][2]) < 0.01:
                    coarse.append(x)                                  # the disc's top face
                continue
            if i['kind'] == 'plane' and abs(i['box'][2] - TOP) < 0.01:
                continue
            fine.append(x)
        log(name, 'faces: bottom', len(bottom), 'tip', len(tip), 'fine', len(fine), 'disc top', len(coarse))
        if len(bottom) != 1 or len(tip) != 1 or not fine:
            raise SystemExit('bad picks')
        r = static(j, d, f'{name}_{CTRL}'[-24:], PETG, fixtures=[('fixed', bottom)],
                   loads=[('remote', tip, (0, 0, TOP), (0, 20.0, 0), (0, 0, 0))], el=2.5,
                   ctrl=[(fine, CTRL)] + ([(coarse, min(2.5, 2 * CTRL))] if coarse else []))
        zone = (r.pos[:, 2] > -0.3) & (r.pos[:, 2] < 14)
        k = np.flatnonzero(zone)[np.argmax(r.vm[zone])]
        plain = (np.abs(r.pos[:, 2] - 25) < 1.0)
        row = dict(nodes=r.nodes, volume=round(volume(d), 1), reaction=r.reaction, tip_disp=round(r.max_disp(), 4),
                   junction_vm=round(float(r.vm[k]), 3), at=r.pos[k].round(2).tolist(),
                   junction_avg_1mm=[round(v, 3) for v in r.average(r.pos[k], 1.0)],
                   junction_p1=round(float(r.s[zone, 7].max()), 3),
                   plain_section_vm_z25=round(float(r.vm[plain].max()), 3),
                   profile_y=[[z, round(float(np.abs(r.pos[np.abs(r.pos[:, 2] - z) < 0.35, 1]).max()), 2)]
                              for z in (0.4, 1, 2, 3, 4, 6, 8, 12)])
        res.setdefault(name, {})[str(CTRL)] = row
        log('RESULT', name, CTRL, json.dumps(row))
        f.write_text(json.dumps(res, indent=1))
        close(j.sw, d)
