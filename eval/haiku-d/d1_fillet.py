"""D1 variant: the same frame with R1 fillets on the four re-entrant corners of the opening (a printed part has a radius there).

Saved as a new file, buck_mount_r1.SLDPRT, so the sharp-corner model stays as it was. Hand: each concave R1 corner adds
(1 - pi/4) R^2 x length = 0.2146 x 4 = 0.858 mm3, four corners 3.43 mm3.
"""
import sys
from pathlib import Path
import numpy as np
WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT / 'solidworks'))
from swkit import job, open_doc, edges_where, fillet, volume, save_as, feature_errors, expect, bodies, log  # noqa: E402

D = WT / '_wip' / 'sw-eval' / 'haiku-d' / 'd1'
SRC, DST = D / 'buck_mount.SLDPRT', D / 'buck_mount_r1.SLDPRT'

if __name__ == '__main__':
    with job(wait_s=1800) as j:
        d = open_doc(j.sw, SRC)
        d.ForceRebuild3(False)
        v0 = volume(d)
        def corner(p):
            x, y, z = p
            return abs(abs(x) - 35.5) < 0.01 and (abs(z + 7.0) < 0.01 or abs(z - 35.0) < 0.01) and 9.9 < y < 14.1
        edges = edges_where(d, corner)
        log('corner edges found', len(edges))
        expect('four opening corner edges', len(edges), 4, 0)
        r = fillet(d, edges, (1.0,), 'OPEN_R1')
        expect('R1 built', float(r or 0), 1.0, 0.0001)
        d.ForceRebuild3(False)
        dv = volume(d) - v0
        expect('added volume (hand 3.43 mm3)', dv, 3.43, 0.02)
        expect('rebuild errors', len(feature_errors(d)), 0, 0)
        save_as(d, DST)
        log('saved', DST, bodies(d))
