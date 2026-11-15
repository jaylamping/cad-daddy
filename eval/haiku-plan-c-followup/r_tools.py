"""Reviewer's checks for the follow-up round (numpy only, no SolidWorks). Run from eval/haiku-plan-c-followup/.

    python r_tools.py slice <part.stl>     # stem widths at fixed heights; last line PINCH_CHECK ok | fail
    python r_tools.py print <part.stl>     # bed fit, bed contact and supported area for layers along X and along Y;
                                           # writes printability.json beside this file

Both print numbers only. INSTRUCTIONS.md says what to do with each result.
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'solidworks'))
import sheet  # noqa: E402

# (z, lowest and highest allowed half width in X, lowest and highest allowed top Y) for table STEM_A2 with the three
# added rows; the design values are 12.2 / 12.1 / 11.9 / 11.7 / 11.2 in X and about 12.6 to 11.9 in Y.
LIMITS = [(-66.0, 11.0, 13.2, 11.4, 13.6), (-70.0, 11.0, 13.2, 11.4, 13.6), (-74.0, 11.0, 13.2, 11.4, 13.6),
          (-78.0, 11.0, 13.2, 11.4, 13.6), (-94.0, 10.4, 12.0, 11.2, 12.8)]


def cut(tris, z):
    """Points where the plane Z = z crosses the triangle edges."""
    pts = []
    for a, b in ((0, 1), (1, 2), (2, 0)):
        p, q = tris[:, a], tris[:, b]
        m = (p[:, 2] - z) * (q[:, 2] - z) < 0
        f = (z - p[m, 2]) / (q[m, 2] - p[m, 2])
        pts.append(p[m] + f[:, None] * (q[m] - p[m]))
    return np.concatenate(pts)


def slices(path):
    tris = sheet.read_stl(path)
    ok = True
    print('    z   half width X   top Y   bottom Y   allowed X       allowed top Y   ')
    for z, x0, x1, y0, y1 in LIMITS:
        p = cut(tris, z + 0.01)
        hx, top, bot = float(np.abs(p[:, 0]).max()), float(p[:, 1].max()), float(p[:, 1].min())
        good = x0 <= hx <= x1 and y0 <= top <= y1
        ok &= good
        print(f'{z:6.1f} {hx:10.2f} {top:10.2f} {bot:9.2f}   {x0} to {x1}   {y0} to {y1}   {"ok" if good else "OUTSIDE"}')
    print('PINCH_CHECK', 'ok' if ok else 'fail')
    return ok


def printability(tris, up, bed=256.0, first=0.3, angle=45.0):
    """up: the model direction that points away from the bed, a unit axis such as (1, 0, 0)."""
    up = np.array(up, float)
    ax = int(np.argmax(np.abs(up)))
    others = [i for i in range(3) if i != ax]
    h = tris[:, :, ax] * up[ax]
    h = h - h.min()
    n, area = sheet._normals(tris)
    down = -n[:, ax] * up[ax]                                  # 1 for a face that looks straight at the bed
    foot = [float(np.ptp(tris[:, :, i])) for i in others]
    on_bed = (h.max(axis=1) < first) & (down > 0.5)
    over = (down > np.sin(np.radians(angle))) & ~on_bed       # faces flatter than 45 degrees that look down
    return dict(footprint_mm=[round(v, 1) for v in foot], height_mm=round(float(h.max()), 1),
                fits_bed=bool(max(foot) <= bed and h.max() <= bed), bed_contact_mm2=round(float(area[on_bed].sum()), 1),
                supported_area_mm2=round(float((area[over] * down[over]).sum()), 1),
                supported_mean_height_mm=round(float((area[over] * h[over].mean(axis=1)).sum() / max(area[over].sum(), 1e-9)), 1))


def printing(path):
    tris = sheet.read_stl(path)
    out = {'layers along X, -X edge on the bed': printability(tris, (1, 0, 0)),
           'layers along X, +X edge on the bed': printability(tris, (-1, 0, 0)),
           'layers along Y, +Y side on the bed (first round)': printability(tris, (0, -1, 0))}
    (HERE / 'printability.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
    print(json.dumps(out, indent=1))
    x = out['layers along X, -X edge on the bed']
    print('PRINT_CHECK', 'ok' if x['fits_bed'] else 'fail', '(fits a 256 mm bed, layers along X)')
    return x['fits_bed']


if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] not in ('slice', 'print'):
        raise SystemExit(__doc__)
    good = slices(sys.argv[2]) if sys.argv[1] == 'slice' else printing(sys.argv[2])
    raise SystemExit(0 if good else 1)
