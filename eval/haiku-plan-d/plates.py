"""D3 part one: six adapter plates from one table, one function (build). Plan: plans/D_D3.md section 3.
Changes from the plan are marked CHANGED. Run as a script: prints the wall table, then builds P1..P6."""
from common import *  # noqa: F401,F403

ASKED = {  # the table as given: od, t, bore, a = (n, hole dia, circle dia), b = (n, hole dia, circle dia), cb = (dia, depth)
    'P1': dict(od=70, t=6, bore=30, a=(6, 3.4, 50), b=(4, 4.5, 60), cb=(8, 3)),
    'P2': dict(od=84, t=6, bore=40, a=(6, 4.5, 62), b=(6, 4.5, 62), cb=(8, 3)),
    'P3': dict(od=96, t=8, bore=52, a=(8, 3.4, 66), b=(4, 5.5, 84), cb=(10, 4)),
    'P4': dict(od=60, t=5, bore=28, a=(4, 3.4, 40), b=(6, 4.5, 58), cb=(8, 4.6)),
    'P5': dict(od=120, t=8, bore=60, a=(12, 4.5, 80), b=(6, 6.6, 104), cb=(11, 5)),
    'P6': dict(od=76, t=6, bore=34, a=(6, 3.4, 46), b=(3, 4.5, 64), cb=(8, 3)),
}
FIX = {  # what is built instead, and why (section 2)
    'P1': (dict(turn_b=45.0), 'ring B turned 45 deg: at 0 deg its counterbore overlapped a ring A hole by 0.7 mm'),
    'P2': (dict(turn_b=30.0), 'ring B turned 30 deg: rings A and B were the same six holes'),
    'P4': (dict(od=68, cb=(8, 3.0)), 'OD 60 -> 68: ring B on 58 broke out of a 60 plate by 3.0 mm; counterbore 4.6 -> 3.0 deep: floor was 0.4 mm'),
}


def spec(name):
    p = dict(ASKED[name], turn_a=0.0, turn_b=0.0)
    p.update(FIX.get(name, ({}, ''))[0])
    return p


def ring_pts(n, circle, turn, z):
    return [(circle / 2 * math.cos(math.radians(turn + 360.0 * k / n)),
             circle / 2 * math.sin(math.radians(turn + 360.0 * k / n)), z) for k in range(n)]


def hand(p, chamfer=0.0):
    R, T = p['od'] / 2, p['t']
    (na, da, _), (nb, db, _), (dcb, c) = p['a'], p['b'], p['cb']
    v = (math.pi * T * (R * R - p['bore'] ** 2 / 4 - na * da * da / 4 - nb * db * db / 4)
         - nb * math.pi * (dcb * dcb - db * db) / 4 * c)
    return v - math.pi * chamfer ** 2 * (R - chamfer / 3)


def walls(p, chamfer=0.0):
    """Every wall in mm, from the numbers: negative means two features overlap. Run it BEFORE building."""
    R, T = p['od'] / 2, p['t']
    (na, da, ca), (nb, db, cbc), (dcb, c) = p['a'], p['b'], p['cb']
    A, B = ring_pts(na, ca, p['turn_a'], 0), ring_pts(nb, cbc, p['turn_b'], 0)
    gap = lambda P, Q: min(math.dist(a, b) for a in P for b in Q if a is not b)      # noqa: E731
    w = {'A hole to B counterbore': gap(A, B) - da / 2 - dcb / 2,
         'A hole to A hole': gap(A, A) - da if na > 1 else 99.0,
         'B counterbore to B counterbore': gap(B, B) - dcb if nb > 1 else 99.0,
         'A hole to bore': ca / 2 - da / 2 - p['bore'] / 2, 'B counterbore to bore': cbc / 2 - dcb / 2 - p['bore'] / 2,
         'A hole to outside': R - ca / 2 - da / 2, 'B counterbore to outside': R - cbc / 2 - dcb / 2,
         'counterbore floor': T - c}
    if chamfer:
        w['chamfer to B counterbore'] = R - chamfer - cbc / 2 - dcb / 2
    return {k: round(v, 2) for k, v in w.items()}


def measure(d, p, chamfer=0.0):
    """Every dimension read from the solid (07-done.md, model item 2). Returns the measured floor Z."""
    R, T = p['od'] / 2, p['t']
    (na, da, ca), (nb, db, cbc), (dcb, c) = p['a'], p['b'], p['cb']
    for got, want in zip(bbox(d), (-R, -R, 0, R, R, T)):
        expect('box', got, want, 0.01)
    must('outside face', len(pick(d, kind='cyl', r=R)), 1)
    must('bore face', len(pick(d, kind='cyl', r=p['bore'] / 2)), 1)
    want = sorted([(da / 2, q) for q in ring_pts(na, ca, p['turn_a'], 0)]
                  + [(db / 2, q) for q in ring_pts(nb, cbc, p['turn_b'], 0)]
                  + [(dcb / 2, q) for q in ring_pts(nb, cbc, p['turn_b'], 0)])
    got = sorted((h[0], (h[1][0], h[1][1], 0)) for r in sorted({da / 2, db / 2, dcb / 2}) for h in holes(d, r)
                 if math.hypot(h[1][0], h[1][1]) > 1.0)                    # leaves out a bore or rim that shares a radius
    must('hole and counterbore faces', len(got), len(want))
    key = lambda g: (round(g[0], 2), round(math.degrees(math.atan2(g[1][1], g[1][0])) % 360.0, 1) % 360.0)   # noqa: E731
    for (r1, q1), (r2, q2) in zip(sorted(got, key=key), sorted(want, key=key)):
        expect('hole radius', r1, r2, 0.02)
        # CHANGED: expect() is relative when the wanted value is non-zero, and a coordinate that should be 0 comes out
        # as 6e-17 (cos 90 deg), which then needs an impossible relative match. Coordinates use an absolute 0.03 mm.
        for lab, a_, b_ in (('hole x', q1[0], q2[0]), ('hole y', q1[1], q2[1])):
            if abs(a_ - b_) > 0.03:
                raise Failed(f'{lab}: got {a_:.4f}, expected {b_:.4f} (absolute tolerance 0.03)')
            log(f'ok {lab}: {a_:.4f} (expected {b_:.4f})')
    fl = pick(d, kind='plane', normal=(0, 0, 1), inside=[-R, -R, T - c - 0.01, R, R, T - c + 0.01])
    must('counterbore floors', len(fl), nb)
    fz = [face_info(f)['box'][2] for f in fl]
    for z in fz:
        expect('floor z', z, T - c, 0.01)
    return float(np.mean(fz))


def build(j, name):
    p = spec(name)
    R, T = p['od'] / 2, p['t']
    (na, da, ca), (nb, db, cbc), (dcb, c) = p['a'], p['b'], p['cb']
    w = walls(p)
    log(name, 'walls', w)
    if min(w.values()) < 0.6:
        raise Failed(f'{name}: a wall under 0.6 mm in the numbers: {w}. Do not build; fix the row first.')
    d = new_part(j.sw, WIP / f'{name}.SLDPRT')
    base = lambda: plane(d, 'Z', 0.0, '')                 # noqa: E731  the base plane, fetched fresh each time
    with Sk(d, base(), 'DISC') as s:
        s.circle((0, 0, 0), R)
    extrude(d, s.feat, 'DISC', T, mode=BLIND, want=(2, +1, 0.0), expect_dv=math.pi * R * R * T)
    with Sk(d, base(), 'BORE') as s:
        s.circle((0, 0, 0), p['bore'] / 2)
    extrude(d, s.feat, 'BORE', T, cut=True, mode=THRU_ALL, expect_dv=math.pi * p['bore'] ** 2 / 4 * T)
    with Sk(d, base(), 'RING_A') as s:
        for q in ring_pts(na, ca, p['turn_a'], 0.0):
            s.circle(q, da / 2)
    extrude(d, s.feat, 'RING_A', T, cut=True, mode=THRU_ALL, expect_dv=na * math.pi * da * da / 4 * T)
    with Sk(d, base(), 'RING_B') as s:
        for q in ring_pts(nb, cbc, p['turn_b'], 0.0):
            s.circle(q, db / 2)
    extrude(d, s.feat, 'RING_B', T, cut=True, mode=THRU_ALL, expect_dv=nb * math.pi * db * db / 4 * T)
    zf = T - c                                            # the counterbore floor, measured from the bottom
    with Sk(d, plane(d, 'Z', zf, 'CBORE_P'), 'CBORE') as s:
        for q in ring_pts(nb, cbc, p['turn_b'], zf):
            s.circle(q, dcb / 2)
    extrude(d, s.feat, 'CBORE', c, cut=True, mode=THRU_ALL, want=(2, +1, zf),
            expect_dv=nb * math.pi * (dcb * dcb - db * db) / 4 * c)
    single_body(d)
    must('rebuild errors', len(feature_errors(d)), 0)
    save(d)
    expect(name + ' volume', volume(d), hand(p), 0.001)
    fz = measure(d, p)
    export(j.sw, d, WIP / f'{name}.stl')
    st = check_export(d, WIP / f'{name}.stl')
    out = dict(volume_mm3=volume(d), hand_volume_mm3=hand(p), mass_g=volume(d) * DENS_G_MM3, bodies=len(bodies(d)),
               stl_watertight=st['watertight'], min_wall_mm=min(w.values()), min_wall_where=min(w, key=w.get),
               changed=name in FIX, why=FIX.get(name, ({}, 'as the table says'))[1], counterbore_floor_z_mm=fz,
               tree=tree(d))
    close(j.sw, d)
    return out


if __name__ == '__main__':
    for n in ASKED:                                        # the table as given, checked before SolidWorks starts
        log(n, 'AS GIVEN', walls(dict(ASKED[n], turn_a=0.0, turn_b=0.0)), '| AS BUILT', walls(spec(n)),
            'hand', round(hand(spec(n)), 2))
    with job() as j:
        plates = {}
        for n in ASKED:
            plates[n] = build(j, n)
            (HERE / 'd3_part1.json').write_text(json.dumps(plates, indent=1, default=float), encoding='utf-8')
            log(n, 'done at minute', minutes())
