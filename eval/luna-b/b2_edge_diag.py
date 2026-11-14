"""Report final-solid edge geometry around the saved R3 wall-bracket root."""
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
CAD = ROOT / 'cad' / '_wip' / 'sw-eval' / 'luna-b'
sys.path.insert(0, str(ROOT / 'tools' / 'solidworks'))
from swkit import job, open_doc, close, solid_bodies, call  # noqa: E402

with job(wait_s=1800) as j:
    d = open_doc(j.sw, CAD / 'wall_bracket.SLDPRT')
    d.ForceRebuild3(False)
    for bi, body in enumerate(solid_bodies(d)):
        for k, e in enumerate(call(body, 'GetEdges') or []):
            cp = e.GetCurveParams3
            mid = e.GetCurve.Evaluate2((cp.UMinValue + cp.UMaxValue) / 2, 0)
            pts = [np.array(cp.StartPoint[:3]) * 1000, np.array(list(mid)[:3]) * 1000,
                   np.array(cp.EndPoint[:3]) * 1000]
            lo = np.min(pts, axis=0); hi = np.max(pts, axis=0)
            if hi[0] >= 4.5 and lo[0] <= 9.0 and hi[1] >= 14 and lo[1] <= 26 and hi[2] >= 39 and lo[2] <= 53:
                print(bi, k, 'start', np.round(pts[0], 4).tolist(), 'mid', np.round(pts[1], 4).tolist(),
                      'end', np.round(pts[2], 4).tolist(), flush=True)
    close(j.sw, d)
