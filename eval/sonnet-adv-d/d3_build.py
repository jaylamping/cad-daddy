"""D3 part one: ONE script builds P1..P6 from the table (after the table is checked), saves the parts, exports STL, and writes
the table. Run: python d3_build.py"""
import hashlib, json, math, sys
from pathlib import Path
import numpy as np, trimesh
ROOT = Path(r'J:\code\cad-daddy-wt\sw-eval-sonnet-adv-d'); sys.path.insert(0, str(ROOT / 'solidworks')); sys.path.insert(0, str(Path(__file__).parent))
from swkit import *
from d3_table import TABLE, RHO, holes, walls, walls_H, best_turn, hand_volume
W = ROOT / '_wip' / 'sw-eval' / 'sonnet-adv-d' / 'd3'; RUN = ROOT / 'eval' / 'sonnet-adv-d'
W.mkdir(parents=True, exist_ok=True)
MIN_WALL, MIN_FLOOR = 0.6, 1.0

# ---- step 1: the table is checked before anything is built ----
plan, problems = {}, []
for name, p in TABLE.items():
    q = {k: (list(v) if isinstance(v, tuple) else v) for k, v in p.items()}
    why = []
    w0 = walls(p)
    offA = offB = 0.0
    if w0['hole_hole_top'] < 1.5 or w0['hole_hole_through'] < 1.5:      # features overlap or nearly: turn ring B to the pitch that spaces them best
        offB, v = best_turn(p, 'B')
        w1 = walls(p, 0.0, offB)
        why.append(f'ring B turned {offB:g} deg: holes of the two rings overlap at the table angles (thinnest hole-to-hole wall '
                   f'{w0["hole_hole_top"]} mm on the top face, {w0["hole_hole_through"]} through), {w1["hole_hole_top"]} mm after')
        problems.append(f'{name}: rings A and B collide at 0 deg ({w0["hole_hole_top"]} mm top, {w0["hole_hole_through"]} through); '
                        f'built with ring B turned {offB:g} deg')
    R = p['od'] / 2; rB = p['B'][2] / 2; rcb = p['B'][3] / 2
    if R - (rB + rcb) < MIN_WALL:      # a counterbore that breaks out or leaves under the 0.6 mm minimum wall: the outside diameter moves, the bolt circle stays
        new_od = 2 * math.ceil(rB + rcb + 1.5)
        why.append(f'outside diameter {p["od"]} -> {new_od}: ring B circle {p["B"][2]} with counterbore {p["B"][3]} reaches radius {rB + rcb} of a plate radius {R}')
        problems.append(f'{name}: ring B on a {p["B"][2]} circle with a {p["B"][3]} counterbore reaches radius {rB + rcb}, outside the '
                        f'{p["od"]} plate (wall {round(R - rB - rcb, 2)}); built with outside {new_od}')
        q['od'] = new_od
    if p['t'] - p['B'][4] < MIN_FLOOR:
        nd = p['t'] - MIN_FLOOR
        why.append(f'counterbore depth {p["B"][4]} -> {nd:g}: the floor would be {round(p["t"] - p["B"][4], 2)} mm (under {MIN_FLOOR})')
        problems.append(f'{name}: counterbore depth {p["B"][4]} in a {p["t"]} plate leaves a {round(p["t"] - p["B"][4], 2)} mm floor; built with depth {nd:g} (floor {MIN_FLOOR})')
        q['B'][4] = nd
    q['B'] = tuple(q['B']); q['A'] = tuple(q['A'])
    wq = walls(q, offA, offB)
    if MIN_WALL <= wq['hole_outside'] < 1.5:
        problems.append(f'{name}: questioned, built as the table: the counterbores leave only {wq["hole_outside"]} mm to the rim (over the 0.6 mm minimum; a later chamfer or a rim drill will eat it)')
    plan[name] = dict(p=q, offA=offA, offB=offB, why='; '.join(why), changed=bool(why), walls_table=w0, walls_built=walls(q, offA, offB))
    print(name, 'changed' if why else 'as table', plan[name]['why'], plan[name]['walls_built'], flush=True)
json.dump(dict(plan=plan, problems=problems), open(RUN / 'd3_plan.json', 'w'), indent=1, default=str)
assert all(v['walls_built']['min'] >= MIN_WALL for v in plan.values()), 'a plate is still under the minimum wall'


def build(j, name, pl):
    p, offA, offB = pl['p'], pl['offA'], pl['offB']
    t, od, bore = p['t'], p['od'], p['bore']
    nA, dA, cA = p['A']; nB, dB, cB, cbd_, cbdepth = p['B']
    floor = t - cbdepth
    d = new_part(j.sw, W / f'{name}.SLDPRT')
    with Sk(d, plane(d, 'Z', 0.0, 'BASE_P'), 'BODY') as s:
        s.circle((0, 0, 0.0), od / 2)
    extrude(d, s.feat, 'BODY', t, mode=BLIND, want=(2, +1, 0.0), expect_dv=math.pi / 4 * od ** 2 * t)
    cut_p = plane(d, 'Z', 1.0, 'CUT_P')

    def cut(sketch_name, pts, dia, exp):
        with Sk(d, cut_p, sketch_name) as s:
            for x, y in pts:
                s.circle((x, y, 1.0), dia / 2)
        extrude(d, s.feat, sketch_name.replace('_SK', ''), 40.0, cut=True, mode=MID, expect_dv=exp)
    H = holes(p, offA, offB)
    cut('BORE_SK', [(0, 0)], bore, math.pi / 4 * bore ** 2 * t)
    cut('RING_A_SK', [(h[1], h[2]) for h in H if h[0] == 'A'], dA, nA * math.pi / 4 * dA ** 2 * t)
    cut('RING_B_SK', [(h[1], h[2]) for h in H if h[0] == 'B'], dB, nB * math.pi / 4 * dB ** 2 * t)
    # counterbores: sketch on a plane at the FLOOR, cut upward through the top: the floor never moves when the plate gets thicker
    cb_p = plane(d, 'Z', floor, 'CB_P')
    with Sk(d, cb_p, 'RING_B_CB_SK') as s:
        for h in H:
            if h[0] == 'B':
                s.circle((h[1], h[2], floor), cbd_ / 2)
    extrude(d, s.feat, 'RING_B_CB', cbdepth + 1.0, cut=True, mode=BLIND, want=(2, +1, floor),
            expect_dv=nB * math.pi / 4 * (cbd_ ** 2 - dB ** 2) * cbdepth)
    save(d)
    return d


def measure(d, p, pl):
    """Hole list [(kind, x, y, r_through, r_top)] read from the cylinder faces of the finished solid."""
    t = p['t']; nA, dA, cA = p['A']; nB, dB, cB, cbd_, cbdepth = p['B']; floor = t - cbdepth
    thr, cbs = [], {}
    for f in faces(d):
        i = face_info(f)
        if i['kind'] != 'cyl':
            continue
        bx = i['box']; r, cx, cy, z0, z1 = i['r'], (bx[0] + bx[3]) / 2, (bx[1] + bx[4]) / 2, bx[2], bx[5]
        if abs(cx) < 0.01 and abs(cy) < 0.01 and (abs(r - p['bore'] / 2) < 0.01 or abs(r - p['od'] / 2) < 0.01):
            continue
        if abs(z0) < 0.01 and abs(z1 - t) < 0.01:
            thr.append(['A', cx, cy, r, r])
        elif abs(z0) < 0.01 and abs(z1 - floor) < 0.01:
            thr.append(['B', cx, cy, r, r])
        elif abs(z0 - floor) < 0.01 and abs(z1 - t) < 0.01:
            cbs[(round(cx, 2), round(cy, 2))] = r
    out = [(k, x, y, r0, cbs.get((round(x, 2), round(y, 2)), r1) if k == 'B' else r1) for k, x, y, r0, r1 in thr]
    return out, cbs


rows = {}
with job(wait_s=1800) as j:
    stamp(RUN, 'D3 part one: instance up')
    for name, pl in plan.items():
        stamp(RUN, f'D3 {name} build start')
        p = pl['p']; t = p['t']
        nA, dA, cA = p['A']; nB, dB, cB, cbd_, cbdepth = p['B']
        d = build(j, name, pl)
        hand = hand_volume(p)
        expect(f'{name} volume mm3 against hand', volume(d), hand, 0.002)
        expect(f'{name} bodies', len(bodies(d)), 1, 0)
        b = bbox(d)
        for k, want in enumerate((-p['od'] / 2, -p['od'] / 2, 0, p['od'] / 2, p['od'] / 2, t)):
            expect(f'{name} box[{k}]', b[k], want, 0.01)
        expect(f'{name} rebuild errors', len(feature_errors(d)), 0, 0)
        Hf, cbs = measure(d, p, pl)
        expect(f'{name} holes found on the solid', len(Hf), nA + nB, 0)
        expect(f'{name} counterbores found', len(cbs), nB, 0)
        exp_pos = sorted((round(h[1], 3), round(h[2], 3)) for h in holes(p, pl['offA'], pl['offB']))
        got_pos = sorted((round(h[1], 3), round(h[2], 3)) for h in Hf)
        err = max(math.dist(a, c) for a, c in zip(exp_pos, got_pos))
        expect(f'{name} hole centres, worst position error mm', err, 0.0, 0.02)
        radii_err = max(abs(h[3] - dA / 2) if h[0] == 'A' else abs(h[3] - dB / 2) for h in Hf)
        expect(f'{name} through-hole radii, worst error mm', radii_err, 0.0, 0.01)
        cb_err = max(abs(r - cbd_ / 2) for r in cbs.values())
        expect(f'{name} counterbore radii, worst error mm', cb_err, 0.0, 0.01)
        wm = walls_H(Hf, p['od'] / 2, p['bore'] / 2, t, cbdepth)
        log(f'{name} measured walls', wm)
        export(j.sw, d, str(W / f'{name}.stl'))
        m = trimesh.load(W / f'{name}.stl')
        stl = dict(watertight=bool(m.is_watertight), shells=len(m.split()), volume=float(m.volume))
        expect(f'{name} STL volume', stl['volume'], volume(d), 0.005)
        v = volume(d)
        rows[name] = dict(volume_mm3=round(v, 2), hand_volume_mm3=round(hand, 2), mass_g=round(v * RHO, 3), bodies=1,
                          stl_watertight=stl['watertight'], stl_shells=stl['shells'], stl_volume_diff_pct=round(100 * (stl['volume'] / v - 1), 3),
                          min_wall_mm=wm['min'], walls_measured=wm, walls_table_as_given=pl['walls_table'], changed=pl['changed'],
                          why=pl['why'] or 'as the table says', ring_b_turn_deg=pl['offB'], od=p['od'], thickness=t, cb_depth=cbdepth,
                          floor_z_mm=t - cbdepth, sha256=hashlib.sha256(open(W / f'{name}.SLDPRT', 'rb').read()).hexdigest())
        close(j.sw, d)
        stamp(RUN, f'D3 {name} build end')
json.dump(rows, open(RUN / 'd3_part1_results.json', 'w'), indent=1)
stamp(RUN, 'D3 part one: end')
print('D3 PART ONE DONE')
