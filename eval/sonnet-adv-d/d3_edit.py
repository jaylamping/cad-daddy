"""D3 part two: the request changes. Every saved part is OPENED and EDITED (save_as first, then edit dimensions and sketches in place, then
add the chamfer): 1.5 mm thicker, counterbore floors where they were measured from the bottom, 1 mm chamfer on the top outside edge,
P3 ring A on a 70 circle. Saves P1_b..P6_b. Not rebuilt from d3_build.py: the feature tree before and after is logged."""
import hashlib, json, math, sys
from pathlib import Path
import trimesh
ROOT = Path(r'J:\code\cad-daddy-wt\sw-eval-sonnet-adv-d'); sys.path.insert(0, str(ROOT / 'solidworks')); sys.path.insert(0, str(Path(__file__).parent))
from swkit import *
from d3_table import RHO, holes, walls_H, best_turn, hand_volume
W = ROOT / '_wip' / 'sw-eval' / 'sonnet-adv-d' / 'd3'; RUN = ROOT / 'eval' / 'sonnet-adv-d'
plan = json.load(open(RUN / 'd3_plan.json'))['plan']
part1 = json.load(open(RUN / 'd3_part1_results.json'))
DT, CH, MIN_WALL = 1.5, 1.0, 0.6


def tree(d):
    out, f = [], d.FirstFeature
    while f is not None:
        out.append((f.Name, f.GetTypeName2, int(call(f, 'GetID'))))
        f = f.GetNextFeature
    return out


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def measure(d, p, floor_expected):
    t = p['t']; nA, dA, cA = p['A']; nB, dB, cB, cbd_, cbdepth = p['B']; floor = t - cbdepth
    thr, cbs, floors = [], {}, []
    for f in faces(d):
        i = face_info(f)
        if i['kind'] == 'cyl':
            bx = i['box']; r, cx, cy, z0, z1 = i['r'], (bx[0] + bx[3]) / 2, (bx[1] + bx[4]) / 2, bx[2], bx[5]
            if abs(cx) < 0.01 and abs(cy) < 0.01 and (abs(r - p['bore'] / 2) < 0.01 or abs(r - p['od'] / 2) < 0.01):
                continue
            if abs(z0) < 0.01 and abs(z1 - t) < 0.01:
                thr.append(['A', cx, cy, r, r])
            elif abs(z0) < 0.01 and abs(z1 - floor) < 0.01:
                thr.append(['B', cx, cy, r, r])
            elif abs(z0 - floor) < 0.01 and z1 >= t - CH - 0.01:      # a counterbore wall now ends at the chamfer or the top
                cbs[(round(cx, 2), round(cy, 2))] = r
        elif i['kind'] == 'plane' and i['normal'] == [0.0, 0.0, 1.0] and abs(i['box'][2] - floor_expected) < 0.01 and abs(i['box'][5] - floor_expected) < 0.01:
            floors.append(i['box'][2])
    out = [(k, x, y, r0, cbs.get((round(x, 2), round(y, 2)), r1) if k == 'B' else r1) for k, x, y, r0, r1 in thr]
    return out, cbs, floors


def top_rim_edge(d, R, z):
    best = None
    for f in faces(d):
        i = face_info(f)
        if i['kind'] == 'plane' and i['normal'] == [0.0, 0.0, 1.0] and abs(i['box'][2] - z) < 0.01 and (best is None or i['area'] > best[0]):
            best = (i['area'], f)
    if best is None:
        raise Failed('no top face')
    for e in (call(best[1], 'GetEdges') or []):
        cp = e.GetCurveParams3
        mid = e.GetCurve.Evaluate2((cp.UMinValue + cp.UMaxValue) / 2, 0)
        pts = [cp.StartPoint[:3], list(mid)[:3]]
        if all(abs(math.hypot(p_[0], p_[1]) * 1e3 - R) < 0.05 for p_ in pts):
            return e
    raise Failed('rim edge not found')


# ---- the changed table, checked BEFORE any edit ----
newp, rows, problems = {}, {}, []
for name, pl in plan.items():
    p = {k: (tuple(v) if isinstance(v, list) else v) for k, v in pl['p'].items()}
    q = dict(p); q['t'] = p['t'] + DT; B = list(p['B']); B[4] = B[4] + DT; q['B'] = tuple(B)
    offA, offB, why = pl['offA'], pl['offB'], []
    if name == 'P3':
        A = list(p['A']); A[2] = 70.0; q['A'] = tuple(A)
        offA, v = best_turn(q, 'A', other_off=offB)
        why.append(f'ring A on a 70 circle as asked, and turned {offA:g} deg: at 0 deg ring A (r 35, Ø3.4) puts holes 7 mm from the Ø5.5 holes of ring B (r 42) and their Ø10 counterbores (r 5) leave a 0.3 mm wall; at {offA:g} deg the thinnest hole-to-hole wall is {round(v, 2)} mm')
        problems.append('P3_b: ring A on a 70 circle at 0 deg leaves a 0.3 mm wall to the ring B counterbores; ring A turned %g deg' % offA)
    R, rc = q['od'] / 2, q['B'][2] / 2 + q['B'][3] / 2
    if R - rc - CH < 1.0:
        new_od = 2 * math.ceil(rc + CH + 1.0)
        why.append(f'outside diameter {q["od"]} -> {new_od}: the 1 mm chamfer would leave {round(R - rc - CH, 2)} mm between it and the counterbores (rim wall was {round(R - rc, 2)})')
        problems.append(f'{name}_b: 1 mm chamfer on a {q["od"]} plate whose counterbores reach radius {rc}: the rim would be {round(R - rc - CH, 2)} mm at the top; outside diameter raised to {new_od}')
        q['od'] = new_od
    H = holes(q, offA, offB)
    w = walls_H(H, q['od'] / 2, q['bore'] / 2, q['t'], q['B'][4], CH)
    assert w['min'] >= MIN_WALL, (name, w)
    newp[name] = dict(p=q, offA=offA, offB=offB, why='; '.join(why), changed=bool(why), walls=w)
    print(name, 'edit plan:', newp[name]['why'] or 'thicker + chamfer only', w, flush=True)

treelog = {}
with job(wait_s=1800) as j:
    stamp(RUN, 'D3 part two: instance up')
    for name, pl in plan.items():
        stamp(RUN, f'D3 {name} edit start')
        n = newp[name]; q = n['p']; p0 = {k: (tuple(v) if isinstance(v, list) else v) for k, v in pl['p'].items()}
        src, dst = W / f'{name}.SLDPRT', W / f'{name}_b.SLDPRT'
        sha0 = sha(src)
        d = open_doc(j.sw, src)
        v_orig = volume(d)
        before = tree(d)
        save_as(d, dst)                                              # the open document IS the new file now; the original on disk stays as it was
        expect(f'{name}: open document is the copy', 1.0 if d.GetPathName.lower().endswith(f'{name}_b.sldprt'.lower()) else 0.0, 1.0, 0)
        t0, cbd0 = p0['t'], p0['B'][4]
        set_dim(d, 'BODY', t0, q['t'])                               # edit 1: the body
        set_dim(d, 'RING_B_CB', cbd0 + 1.0, cbd0 + 1.0 + DT)         # edit 2: the depth measured from the top; its sketch sits on the floor plane and does not move
        d.ForceRebuild3(False)
        if q['od'] != p0['od']:
            redraw_circles(d, 'BODY_SK', [(0, 0, 0.0)], q['od'] / 2)  # edit 3 (P1, P3): outside diameter
        if name == 'P3':
            Hn = holes(q, n['offA'], n['offB'])
            redraw_circles(d, 'RING_A_SK_SK', [(h[1], h[2], 1.0) for h in Hn if h[0] == 'A'], q['A'][1] / 2)   # edit 4: ring A on 70
        d.ForceRebuild3(False)
        expect(f'{name}: errors after the dimension edits', len(feature_errors(d)), 0, 0)
        v_mid = volume(d)
        hand_mid = hand_volume(q)
        expect(f'{name}: volume before the chamfer against hand', v_mid, hand_mid, 0.002)
        floor = q['t'] - q['B'][4]
        expect(f'{name}: floor Z as before the change', floor, t0 - cbd0, 1e-6)
        e = top_rim_edge(d, q['od'] / 2, q['t'])
        chamfer(d, [e], CH, 'TOP_CHAMFER')                           # edit 5: new feature on the top rim edge
        d.ForceRebuild3(False)
        hand = hand_volume(q, chamfer=CH)
        expect(f'{name}: volume against hand (chamfer pi c^2 (R - c/3) = {math.pi * CH ** 2 * (q["od"] / 2 - CH / 3):.2f})', volume(d), hand, 0.002)
        expect(f'{name}: bodies', len(bodies(d)), 1, 0)
        b = bbox(d)
        for k, want in enumerate((-q['od'] / 2, -q['od'] / 2, 0, q['od'] / 2, q['od'] / 2, q['t'])):
            expect(f'{name}: box[{k}]', b[k], want, 0.01)
        expect(f'{name}: errors', len(feature_errors(d)), 0, 0)
        save(d)
        after = tree(d)
        keep = [x for x in after if x[0] != 'TOP_CHAMFER']
        same = (keep == before)
        expect(f'{name}: feature tree identical (names, types, IDs) apart from the new chamfer', 1.0 if same else 0.0, 1.0, 0)
        treelog[name] = dict(before=before, after=after, same_but_chamfer=same)
        # every dimension measured on the changed solid
        Hf, cbs, floors = measure(d, q, floor)
        expect(f'{name}: holes found', len(Hf), q['A'][0] + q['B'][0], 0)
        expect(f'{name}: counterbores found', len(cbs), q['B'][0], 0)
        exp_pos = sorted((round(h[1], 3), round(h[2], 3)) for h in holes(q, n['offA'], n['offB']))
        got_pos = sorted((round(h[1], 3), round(h[2], 3)) for h in Hf)
        expect(f'{name}: hole centres, worst position error mm', max(math.dist(a, c) for a, c in zip(exp_pos, got_pos)), 0.0, 0.02)
        expect(f'{name}: counterbore floor faces found at Z {floor} (measured from the bottom, unchanged)', len(floors), q['B'][0], 0)
        wm = walls_H(Hf, q['od'] / 2, q['bore'] / 2, q['t'], q['B'][4], CH)
        log(f'{name}: measured walls after the change', wm)
        export(j.sw, d, str(W / f'{name}_b.stl'))
        m = trimesh.load(W / f'{name}_b.stl')
        stl = dict(watertight=bool(m.is_watertight), shells=len(m.split()), volume=float(m.volume))
        expect(f'{name}: STL volume', stl['volume'], volume(d), 0.005)
        vb = volume(d)
        close(j.sw, d)
        d = open_doc(j.sw, src)
        expect(f'{name}: the original, reopened, still has its old volume', volume(d), v_orig, 1e-9)
        close(j.sw, d)
        sha1 = sha(src)
        rows[name] = dict(volume_mm3=round(vb, 2), hand_volume_mm3=round(hand, 2), mass_g=round(vb * RHO, 3), bodies=1, stl_watertight=stl['watertight'],
                          stl_shells=stl['shells'], stl_volume_diff_pct=round(100 * (stl['volume'] / vb - 1), 3), min_wall_mm=wm['min'], walls_measured=wm,
                          changed=n['changed'], why=n['why'] or 'as asked: 1.5 mm thicker, floors unchanged, 1 mm chamfer', od=q['od'], thickness=q['t'],
                          counterbore_floor_z_mm=floor, counterbore_floor_z_before_mm=t0 - cbd0, ring_a_turn_deg=n['offA'],
                          original_sha256_before=sha0, original_sha256_after=sha1, original_unchanged=(sha0 == sha1), tree_same_but_chamfer=same)
        stamp(RUN, f'D3 {name} edit end')
json.dump(dict(rows=rows, problems=problems, trees=treelog), open(RUN / 'd3_part2_results.json', 'w'), indent=1)
stamp(RUN, 'D3 part two: end')
print('D3 PART TWO DONE')
