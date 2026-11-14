"""The same 100 N on the bore of the selftest plate three ways: bearing load, rigid remote load, even normal force.

    python solidworks/selftest.py bearing      # builds _wip/sw-selftest/lug.SLDPRT
    python eval/bearing-load/compare.py

60 x 60 x 10 plate, 20 mm bore at the origin, fixed on the face x = -30, force along +X (the pin pulls away from the
fixture, so the load goes round the bore through the two side ligaments).
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'solidworks'))
from swfea import BEARING_PARABOLIC, PETG, static  # noqa: E402
from swkit import close, job, open_doc, pick  # noqa: E402

HERE = Path(__file__).resolve().parent
out = {}
with job(wait_s=1800) as j:
    j.simulation()
    d = open_doc(j.sw, ROOT / '_wip' / 'sw-selftest' / 'lug.SLDPRT')
    d.ForceRebuild3(False)
    bore, root = pick(d, kind='cyl', r=10.0), pick(d, kind='plane', normal=(-1, 0, 0))
    assert len(bore) == 1 and len(root) == 1
    cases = (('bearing', [('bearing', bore, (100.0, 0, 0))]),
             ('bearing_parabolic', [('bearing', bore, (100.0, 0, 0), BEARING_PARABOLIC)]),
             ('remote_rigid', [('remote', bore, (0, 0, 5.0), (100.0, 0, 0), (0, 0, 0))]),
             ('normal_even', [('normal', bore, 100.0)]))
    for name, loads in cases:
        r = static(j, d, name.upper(), PETG, fixtures=[('fixed', root)], loads=loads, el=2.0, ctrl=[(bore, 0.6)])
        on = (np.abs(np.hypot(r.pos[:, 0], r.pos[:, 1]) - 10) < 0.02) & (np.abs(r.pos[:, 2] - 5) < 3.5)
        n = r.pos[:, :2] / 10
        th = np.degrees(np.arctan2(n[:, 1], n[:, 0]))
        S = r.s
        srr = n[:, 0] ** 2 * S[:, 1] + n[:, 1] ** 2 * S[:, 2] + 2 * n[:, 0] * n[:, 1] * S[:, 4]
        hoop = n[:, 1] ** 2 * S[:, 1] + n[:, 0] ** 2 * S[:, 2] - 2 * n[:, 0] * n[:, 1] * S[:, 4]
        side = on & (np.abs(np.abs(th) - 90) < 3)
        k = np.flatnonzero(on)[np.argmax(r.vm[on])]
        ux = r.disp[:, 1]
        row = dict(nodes=r.nodes, reaction=r.reaction, applied=r.applied,
                   peak_pressure=round(float(-srr[on & (np.abs(th) < 2)].mean()), 4),
                   pressure_back_half=round(float(np.abs(srr[on & (np.abs(th) > 95)]).max()), 4),
                   hoop_at_sides=round(float(hoop[side].mean()), 4),
                   wall_vm_max=round(float(r.vm[k]), 4), wall_vm_max_theta=round(float(th[k]), 1),
                   default_peak_away=round(r.peak()[0], 4), vm_all=round(float(r.vm.max()), 4),
                   bore_ux_front=round(float(ux[on & (np.abs(th) < 3)].mean()) * 1e3, 3),
                   bore_ux_back=round(float(ux[on & (np.abs(th) > 177)].mean()) * 1e3, 3),
                   max_disp_um=round(r.max_disp() * 1e3, 3))
        out[name] = row
        print(name, json.dumps(row), flush=True)
    close(j.sw, d)
out['hand'] = dict(peak_pressure_sine=round(4 * 100 / (math.pi * 20 * 10), 4), peak_pressure_parabolic=round(3 * 100 / (2 * 20 * 10), 4),
                   net_section_nominal=round(100 / ((60 - 20) * 10), 4))
(HERE / 'compare.json').write_text(json.dumps(out, indent=1))
