"""A bore that is two half faces (as every STEP import is): does the bearing load take both, whatever way they split?

    python solidworks/selftest.py bearing      # builds _wip/sw-selftest/lug.SLDPRT
    python eval/bearing-load/split_bore.py
"""
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'solidworks'))
from swfea import PETG, static  # noqa: E402
from swkit import close, export, face_info, import_step, job, open_doc, pick  # noqa: E402

W = ROOT / '_wip' / 'sw-selftest'
P0 = 4 * 100 / (math.pi * 20 * 10)
with job(wait_s=1800) as j:
    j.simulation()
    d = open_doc(j.sw, W / 'lug.SLDPRT')
    export(j.sw, d, W / 'lug.step')
    close(j.sw, d)
    d, target = import_step(j.sw, W / 'lug.step', W / 'lug_in')
    close(j.sw, d)
    d = open_doc(j.sw, target)
    d.ForceRebuild3(False)
    bore, root = pick(d, kind='cyl', r=10.0), pick(d, kind='plane', normal=(-1, 0, 0))
    print('bore faces', len(bore), [[round(v, 1) for v in face_info(f)['box']] for f in bore], flush=True)
    for name, f in (('SPLIT_X', (100.0, 0, 0)), ('SPLIT_Y', (0, 100.0, 0)), ('SPLIT_ONE', (100.0, 0, 0))):
        fs = bore[:1] if name == 'SPLIT_ONE' else bore
        r = static(j, d, name, PETG, fixtures=[('fixed', root)], loads=[('bearing', fs, f)], el=2.0, ctrl=[(bore, 0.6)])
        on = (np.abs(np.hypot(r.pos[:, 0], r.pos[:, 1]) - 10) < 0.02) & (np.abs(r.pos[:, 2] - 5) < 3.5)
        n = r.pos[on, :2] / 10
        S = r.s[on]
        srr = n[:, 0] ** 2 * S[:, 1] + n[:, 1] ** 2 * S[:, 2] + 2 * n[:, 0] * n[:, 1] * S[:, 4]
        th = np.degrees(np.arccos(np.clip(n @ (np.array(f[:2]) / 100), -1, 1)))
        print(name, 'faces', len(fs), 'reaction', r.reaction, 'peak pressure', round(float(-srr[th < 2].mean()), 4), 'hand', round(P0, 4),
              'at 45', round(float(-srr[np.abs(th - 45) < 2].mean()), 4), 'back half max', round(float(np.abs(srr[th > 95]).max()), 4), flush=True)
    close(j.sw, d)
