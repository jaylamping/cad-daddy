"""The planner's hand numbers for set C (numpy only; the executor does not need to run this).

A 0.4 mm voxel model of the design tables in common.py: the stem is taken as superellipse sections whose numbers are
interpolated in a straight line between the tables' rows, which is close to, but not the same as, the loft SolidWorks
makes. Volumes from it are good to about 3 %.   python hand_numbers.py
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'solidworks'))
import common as c  # noqa: E402

H = 0.4
xs = np.arange(-38, 38 + H, H)
ys = np.arange(-24, 24 + H, H)


def layer(z, table, window, parts):
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    r = np.hypot(X, z)
    ylo = np.where(r <= 31.5, -4.0, 0.5 - np.sqrt(np.clip(4.5 ** 2 - (r - 31.5) ** 2, 0, None)))
    yhi = np.where(r <= 32.5, 4.0, 0.5 + np.sqrt(np.clip(3.5 ** 2 - (r - 32.5) ** 2, 0, None)))
    hub = (r >= 15) & (r <= 36) & (Y >= ylo) & (Y <= yhi)
    rp = np.hypot(X, z - c.PIN_Z)
    lim = np.where(np.abs(Y) <= 18, 13.0, 9 + np.sqrt(np.clip(16 - (np.abs(Y) - 18) ** 2, 0, None)))
    kn = (rp >= 2) & (rp <= lim) & (np.abs(Y) <= 22)
    zs = [row[0] for row in table][::-1]
    stem = np.zeros_like(hub)
    if zs[0] <= z <= zs[-1]:
        a, top, bot, n = (np.interp(z, zs, [row[k] for row in table][::-1]) for k in (1, 2, 3, 4))
        yc, h = (top + bot) / 2, (top - bot) / 2
        stem = np.abs(X / a) ** n + np.abs((Y - yc) / h) ** n <= 1
    slot = (np.abs(Y) < 16) & ((z < -183) | (Y ** 2 + (z + 183) ** 2 < 256))
    win = (np.abs(X) < c.window_half(z)) if window else np.zeros_like(hub)
    tun = (X ** 2 + Y ** 2 < c.CABLE_R ** 2) & (c.CABLE_Z1 < z < c.CABLE_Z0)
    holes = np.zeros_like(hub)
    heads = np.zeros_like(hub)
    for bx, bz in c.BOLTS:
        dd = np.hypot(X - bx, z - bz)
        holes |= dd < c.BOLT_HOLE_R
        heads |= (dd < c.HEAD_R) & (Y > 4) & (Y < 15)
    pin = rp < 4
    out = {}
    out['stem'] = stem
    out['stem+hub'] = stem | hub
    out['all'] = stem | hub | kn
    out['window'] = out['all'] & ~win
    out['form'] = out['window'] & ~slot
    out['pin'] = out['form'] & ~pin
    out['tunnel'] = out['pin'] & ~tun
    out['holes'] = out['tunnel'] & ~holes
    out['final'] = out['holes'] & ~heads
    out['hub'] = hub
    out['kn'] = kn
    return {k: float(v.sum()) * H * H for k, v in out.items()}


def volumes(table, window):
    tot = {}
    for z in np.arange(-214, 37, H):
        for k, a in layer(z + H / 2, table, window, None).items():
            tot[k] = tot.get(k, 0.0) + a * H
    return tot


b = c.boxy_hand_volume()
print('BOXY', {k: round(v, 1) for k, v in b.items()}, 'mass g', round(b['total'] * c.DENS_G_MM3, 1))
for name, table, window in (('A', c.STEM_A, False), ('A2', c.STEM_A2, False), ('A3', c.STEM_A3, False), ('B', c.STEM_B, True)):
    v = volumes(table, window)
    print(name, {k: round(x) for k, x in v.items()})
    print(name, 'steps: stem', round(v['stem']), 'hub adds', round(v['stem+hub'] - v['stem']), 'knuckle adds',
          round(v['all'] - v['stem+hub']), 'window', round(v['all'] - v['window']), 'slot', round(v['window'] - v['form']),
          'pin', round(v['form'] - v['pin']), 'tunnel', round(v['pin'] - v['tunnel']), 'holes', round(v['tunnel'] - v['holes']),
          'heads', round(v['holes'] - v['final']), 'final', round(v['final']), 'mass g', round(v['final'] * c.DENS_G_MM3, 1),
          'form mass g', round(v['form'] * c.DENS_G_MM3, 1))
    print(name, 'beam factors', c.beam_factors(table, c.WINDOW_B if window else None))
    for row in table:
        area, zx, zy = c.section_props(row, c.window_half(row[0]) if window else 0.0)
        arm = row[0] - c.PIN_Z
        print(f'   z {row[0]:7.1f} area {area:6.0f} Zx {zx:6.0f} Zy {zy:6.0f} sigma +Y {60 * arm / zx:5.1f} sigma X {60 * arm / zy:5.1f} MPa')
