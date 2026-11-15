"""D3: the table, the geometry of each plate and the wall checker. Run alone it checks the table as given (nothing is built).
All lengths mm, angles degrees from +X, counterclockwise. PETG 1.19 g/cm3."""
import itertools, json, math, sys
RHO = 1.19e-3
# plate: OD, thickness, bore, A (n, dia, circle dia), B (n, dia, circle dia, counterbore dia, counterbore depth)
TABLE = {
 'P1': dict(od=70, t=6, bore=30, A=(6, 3.4, 50), B=(4, 4.5, 60, 8, 3)),
 'P2': dict(od=84, t=6, bore=40, A=(6, 4.5, 62), B=(6, 4.5, 62, 8, 3)),
 'P3': dict(od=96, t=8, bore=52, A=(8, 3.4, 66), B=(4, 5.5, 84, 10, 4)),
 'P4': dict(od=60, t=5, bore=28, A=(4, 3.4, 40), B=(6, 4.5, 58, 8, 4.6)),
 'P5': dict(od=120, t=8, bore=60, A=(12, 4.5, 80), B=(6, 6.6, 104, 11, 5)),
 'P6': dict(od=76, t=6, bore=34, A=(6, 3.4, 46), B=(3, 4.5, 64, 8, 3)),
}
def holes(p, offA=0.0, offB=0.0):
    """[(kind, x, y, r_through, r_top)] kind 'A' or 'B'; r_top is the counterbore radius for B (what the top face shows)."""
    out = []
    nA, dA, cA = p['A']; nB, dB, cB, cbd_, cbdepth = p['B']
    for k in range(nA):
        a = math.radians(offA + 360.0 * k / nA); out.append(('A', cA / 2 * math.cos(a), cA / 2 * math.sin(a), dA / 2, dA / 2))
    for k in range(nB):
        a = math.radians(offB + 360.0 * k / nB); out.append(('B', cB / 2 * math.cos(a), cB / 2 * math.sin(a), dB / 2, cbd_ / 2))
    return out
def walls(p, offA=0.0, offB=0.0, chamfer=0.0):
    return walls_H(holes(p, offA, offB), p['od'] / 2, p['bore'] / 2, p['t'], p['B'][4], chamfer)
def walls_H(H, R, rb, t, cbd, chamfer=0.0):
    """Thinnest wall of each kind (mm) for hole list H [(kind, x, y, r_through, r_top)], between features as they show on the
    top face (counterbore radius for B) and through the plate (through radius); negative means the features overlap."""
    res = {'hole_hole_top': 1e9, 'hole_hole_through': 1e9, 'hole_bore': 1e9, 'hole_outside': 1e9}
    for i, j in itertools.combinations(range(len(H)), 2):
        d = math.hypot(H[i][1] - H[j][1], H[i][2] - H[j][2])
        res['hole_hole_top'] = min(res['hole_hole_top'], d - H[i][4] - H[j][4]); res['hole_hole_through'] = min(res['hole_hole_through'], d - H[i][3] - H[j][3])
    for h in H:
        rc = math.hypot(h[1], h[2])
        res['hole_bore'] = min(res['hole_bore'], rc - rb - h[4]); res['hole_outside'] = min(res['hole_outside'], R - rc - h[4])
    res['floor'] = t - cbd
    res['hole_outside_after_chamfer'] = res['hole_outside'] - chamfer
    res['min'] = min(res['hole_hole_top'], res['hole_hole_through'], res['hole_bore'], res['hole_outside_after_chamfer'], res['floor'])
    return {k: round(v, 3) for k, v in res.items()}
def best_turn(p, which, other_off=0.0, step=0.5):
    """Offset (deg) of ring `which` ('A' or 'B') that maximises the thinnest hole-to-hole wall on the top face."""
    n = p[which][0]; pitch = 360.0 / n; best = (-1e9, 0.0)
    for k in range(int(pitch / step)):
        off = k * step
        w = walls(p, offA=off if which == 'A' else other_off, offB=off if which == 'B' else other_off)
        v = w['hole_hole_top']
        if v > best[0] + 1e-9: best = (v, off)
    return best[1], best[0]
def hand_volume(p, chamfer=0.0):
    t = p['t']; nA, dA, _ = p['A']; nB, dB, _, cb, cbd = p['B']; R = p['od'] / 2
    V = math.pi / 4 * (p['od'] ** 2 - p['bore'] ** 2) * t
    V -= nA * math.pi / 4 * dA ** 2 * t
    V -= nB * (math.pi / 4 * dB ** 2 * (t - cbd) + math.pi / 4 * cb ** 2 * cbd)
    if chamfer: V -= math.pi * chamfer ** 2 * (R - chamfer / 3.0)
    return V
if __name__ == '__main__':
    for name, p in TABLE.items():
        w0 = walls(p); print(name, 'as given, rings starting at 0 deg:', w0, 'hand V %.1f mm3' % hand_volume(p))
