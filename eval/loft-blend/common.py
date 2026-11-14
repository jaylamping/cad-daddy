"""The test part for the loft-to-disc blend trials: a 60 mm disc, 6 thick, with an oval stem lofted up from its top face.

Frame: disc axis Z, disc from z -6 to 0, stem from z -1 (it starts 1 mm inside the disc) to z 60. The stem's sections
change shape on the way up: 20 x 12 ellipse at the root, 14 x 18 rounded rectangle at the top.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'solidworks'))
from swkit import Sk, extrude, loft, plane  # noqa: E402

OUT = ROOT / '_wip' / 'loft-blend'
OUT.mkdir(parents=True, exist_ok=True)

DISC_R, DISC_T, TOP = 30.0, 6.0, 60.0
SEC = [(-1.0, 10.0, 6.0, 2.0), (15.0, 9.5, 6.0, 2.2), (35.0, 8.0, 7.0, 2.6), (TOP, 7.0, 9.0, 3.0)]      # z, a, b, exponent


def sec(z, a, b, n, k=24):
    """k points of the superellipse |x/a|^n + |y/b|^n = 1 at height z, equal angle, same start point every time."""
    pts = []
    for i in range(k):
        t = 2 * math.pi * i / k
        c, s = math.cos(t), math.sin(t)
        pts.append((a * math.copysign(abs(c) ** (2 / n), c), b * math.copysign(abs(s) ** (2 / n), s), z))
    return pts


def stem_at(z):
    """(a, b, n) of the plain stem at height z, straight-line between the defining sections."""
    for (z0, a0, b0, n0), (z1, a1, b1, n1) in zip(SEC, SEC[1:]):
        if z0 <= z <= z1:
            t = (z - z0) / (z1 - z0)
            return a0 + t * (a1 - a0), b0 + t * (b1 - b0), n0 + t * (n1 - n0)
    raise ValueError(z)


def disc(d):
    with Sk(d, plane(d, 'Z', -DISC_T / 2, 'DISC_P'), 'DISC') as s:
        s.circle((0, 0, -DISC_T / 2), DISC_R)
    return extrude(d, s.feat, 'DISC', DISC_T, mode=6, expect_dv=math.pi * DISC_R ** 2 * DISC_T)


def sections(d, secs, name):
    sks = []
    for i, (z, a, b, n) in enumerate(secs):
        with Sk(d, plane(d, 'Z', z, f'{name}_P{i}'), f'{name}_S{i}') as s:
            s.spline(sec(z, a, b, n))
        sks.append(s.feat)
    return sks


def stem(d, secs=None, name='STEM'):
    return loft(d, sections(d, secs or SEC, name), name)
