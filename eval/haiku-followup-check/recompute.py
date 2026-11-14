"""Recompute round two's numbers from what the runs saved: row files against job logs, every verdict by an
independent copy of the judge() rule (and by the helper itself), and the saved nodal arrays (.npz, in the runs'
worktrees) for the claims the follow-up reports make. No SolidWorks. Writes nothing in the runs' worktrees.

    python eval/haiku-followup-check/recompute.py > eval/haiku-followup-check/recompute.txt
"""
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
EVAL = HERE.parent
WT = Path(r'J:\code\cad-daddy-wt')
NA = WT / 'sw-eval-haiku-plan-a' / '_wip' / 'sw-eval' / 'haiku-plan-a' / 'npz'
ND = WT / 'sw-eval-haiku-plan-d' / '_wip' / 'sw-eval' / 'haiku-plan-d' / 'npz'
FA, FD = EVAL / 'haiku-plan-a-followup', EVAL / 'haiku-plan-d-followup'
ALLOW = dict(vm=45.0, layer=22.5, shear=13.0)


def head(t):
    print('\n' + '=' * 6, t)


def my_judge(series, limits, need=2.0, tol=0.05):
    """The rule of swfea.judge() as its docstring states it, written again from the text."""
    order = ['fail', 'not shown', 'margin, not converged', 'pass']
    rows = []
    for k, v in series.items():
        last, lim = v[-1], limits[k]
        step = abs(v[-1] - v[-2]) / v[-2] if len(v) > 1 else None
        conv = len(v) >= 3 and step <= tol
        fell = all(b <= a for a, b in zip(v, v[1:]))
        proj = last if (step is None or fell) else last * (1 + step) ** 2
        f, fp = lim / last, lim / proj
        state = ('fail' if f < need else 'pass' if conv else
                 'margin, not converged' if (len(v) >= 3 and fp >= need) else 'not shown')
        steps = [round(100 * (b - a) / a, 1) for a, b in zip(v, v[1:])]
        # the same entry with the growth of the steps carried on: next steps s*g and s*g*g, g = last step / step before
        g, fg = None, None
        if len(v) >= 3 and not fell and not conv:
            s1, s2 = abs(v[1] - v[0]) / v[0], step
            g = max(1.0, s2 / s1) if s1 > 0 else float('inf')
            fg = lim / (last * (1 + s2 * g) * (1 + s2 * g * g)) if g != float('inf') else 0.0
        rows.append(dict(entry=k, values=v, steps_pct=steps, factor=round(f, 2), after_two=round(fp, 2), state=state,
                         step_growth=None if g is None else round(g, 2),
                         after_two_growing=None if fg is None else round(fg, 2)))
    verdict = min((r['state'] for r in rows), key=order.index)
    low = min(rows, key=lambda r: r['factor'])
    return dict(verdict=verdict, lowest_factor=low['factor'], lowest_entry=low['entry'], rows=rows)


def helper_judge(series, limits):
    sys.path.insert(0, str(WT / 'sw-eval-haiku-plan-a' / 'solidworks'))      # the helper as the runs had it
    import swfea
    swfea.log = lambda *a, **k: None
    return swfea.judge(series, limits, need=2.0)


def show(j):
    print('  verdict:', j['verdict'], '| lowest factor', j['lowest_factor'], 'at', j['lowest_entry'])
    for r in j['rows']:
        more = ''
        if r['step_growth'] and r['step_growth'] > 1:
            more = f" | steps growing x{r['step_growth']}: after two {r['after_two_growing']}"
        print(f"    {r['entry']:34s} {r['values']} steps % {r['steps_pct']} factor {r['factor']} after two {r['after_two']}"
              f" -> {r['state']}{more}")


def same(a, b, tol=1e-9):
    if isinstance(a, dict):
        return isinstance(b, dict) and set(a) == set(b) and all(same(a[k], b[k], tol) for k in a)
    if isinstance(a, (list, tuple)):
        return isinstance(b, (list, tuple)) and len(a) == len(b) and all(same(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, float) or isinstance(b, float):
        return a is not None and b is not None and abs(a - b) <= tol * max(1.0, abs(a))
    return a == b


def load(p):
    z = np.load(p)
    return z['pos'], z['s'], z['disp'], z['reaction'], int(z['nodes'])


def at(pos, arr, where):
    i = np.argmin(np.linalg.norm(pos - np.array(where), axis=1))
    return float(arr[i]), float(np.linalg.norm(pos[i] - np.array(where)))


def tau_z(s):
    return np.hypot(s[:, 5], s[:, 6])


def tau_y(s):
    return np.hypot(s[:, 4], s[:, 6])


def top(pos, arr, mk):
    k = np.flatnonzero(mk)[np.argmax(arr[mk])]
    return round(float(arr[k]), 2), pos[k].round(2).tolist()


# ---------------------------------------------------------------- T5
head('T5 rounded toes: row file against the job log')
log = (FA / 'wip-logs' / 't5_toe.log').read_text(encoding='utf-8-sig')
rows = json.loads((FA / 't5_toe_rows.json').read_text(encoding='utf-8'))
names = ['T5_TOE_30', 'T5_TOE_22', 'T5_TOE_16']
for n in names:
    lg = json.loads(re.search(rf'^\S+ {n} (\{{.*\}})$', log, re.M).group(1))
    mesh = re.search(rf'{n}: mesh rc (\d+), (\d+) nodes', log)
    print(f'  {n}: row == logged row: {same(rows[n], lg)}; mesh rc {mesh.group(1)}, {mesh.group(2)} nodes;'
          f" reaction {rows[n]['checks']['reaction']} against 150 N; max disp {rows[n]['checks']['max_disp']:.4f}")
head('T5: the saved arrays against the rows')
for n in names:
    pos, s, disp, rea, nn = load(NA / f'{n}.npz')
    y = rows[n]['table']['Y']
    print(f'  {n}: nodes {nn} ({len(pos)} rows); reaction {rea.round(3).tolist()}; max disp {disp[:, 4].max():.4f};'
          f" vm at stated place {at(pos, s[:, 10], y['vm_at'])[0]:.2f} (row {y['vm']});"
          f" sigma-y at stated place {at(pos, s[:, 2], y['layer_at'])[0]:.2f} (row {y['layer']});"
          f" shear on Y layers at stated place {at(pos, tau_y(s), y['shear_at'])[0]:.2f} (row {y['shear']})")
    i = np.argmax(s[:, 10])
    print(f'      largest vm anywhere {s[i, 10]:.2f} at {pos[i].round(2).tolist()} (row vm_all {rows[n]["vm_all"]})')
    side = (np.abs(pos[:, 1] - 3.5) < 0.4) | (np.abs(pos[:, 1] - 46.5) < 0.4)
    for lab, mk in (('rib side root on the upright (x 6..6.4, z 12..31)',
                     (pos[:, 0] > 5.99) & (pos[:, 0] < 6.4) & (pos[:, 2] > 12) & (pos[:, 2] < 31)),
                    ('rib side root on the base (z 6..6.4, x 12..31)',
                     (pos[:, 2] > 5.99) & (pos[:, 2] < 6.4) & (pos[:, 0] > 12) & (pos[:, 0] < 31))):
        mk = mk & side
        print(f'      {lab}: vm {top(pos, s[:, 10], mk)}, shear on Y layers {top(pos, tau_y(s), mk)[0]},'
              f' sigma-y {top(pos, s[:, 2], mk)[0]}')
head('T5: verdict, layers along Y (the direction the part is printed in)')
ser = {m: [rows[n]['table']['Y'][m] for n in names] for m in ALLOW}
mine, theirs = my_judge(ser, ALLOW), json.loads((FA / 't5_toe_judge.json').read_text(encoding='utf-8'))
show(mine)
hj = helper_judge(ser, ALLOW)
print('  helper judge() on the same series == the saved t5_toe_judge.json:', same(hj, theirs), '| my rule agrees:',
      mine['verdict'] == theirs['verdict'] and mine['lowest_factor'] == theirs['lowest_factor'])
for d in 'XZ':
    j = my_judge({m: [rows[n]['table'][d][m] for n in names] for m in ALLOW}, ALLOW)
    print(f'  for comparison, layers along {d}: {j["verdict"]}, lowest {j["lowest_factor"]} at {j["lowest_entry"]}')

# ---------------------------------------------------------------- T6
head('T6 matched mesh: row file against the job log')
log = (FA / 'wip-logs' / 't6m.log').read_text(encoding='utf-8-sig')
t6 = {r['study']: r for r in json.loads((FA / 't6m_rows.json').read_text(encoding='utf-8'))}
tn = ['T6M_12', 'T6M_08', 'T6M_06']
for n in tn:
    lg = json.loads(re.search(rf'^\S+ (\{{"study": "{n}".*\}})$', log, re.M).group(1))
    mesh = re.search(rf'{n}: mesh rc (\d+), (\d+) nodes', log)
    r = t6[n]
    print(f'  {n}: row == logged row: {same(r, lg)}; mesh rc {mesh.group(1)}, {mesh.group(2)} nodes;'
          f' reaction Fz {r["reaction"][2]}; fz_block {r["fz_block"]:.2f}; fz_pads {r["fz_pads"]:.3f}; pin rise {r["pin_rise"]:.4f}')
head('T6: recomputed from the saved arrays (matched series, then round one for comparison)')


def t6_read(path):
    pos, s, disp, rea, nn = load(path)
    rho = np.hypot(pos[:, 0], pos[:, 2] - 10)
    block, pin = rho > 5.096, rho < 5.004
    press = -s[:, 3]
    line = block & (rho < 5.13) & (np.abs(pos[:, 0]) < 0.25) & (pos[:, 2] > 10) & (np.abs(pos[:, 1]) < 8)
    strip = block & (rho < 5.13) & (pos[:, 2] > 10) & (np.abs(pos[:, 1]) < 8)
    hw = np.abs(pos[strip & (press > 0.3), 0]).max()
    xs = np.abs(pos[strip, 0])
    prof = []
    for a in np.arange(0, 3.2, 0.2):
        b = (xs >= a) & (xs < a + 0.2)
        prof.append(round(float(press[strip][b].mean()), 2) if b.any() else None)
    crown = block & (rho < 5.13) & (pos[:, 2] > 10) & (np.abs(pos[:, 0]) < 0.25)
    per_y = {}
    for lab, lo, hi in (('|y| < 8', 0, 8), ('8 to 12', 8, 12), ('12 to 15', 12, 15.01)):
        mk = crown & (np.abs(pos[:, 1]) >= lo) & (np.abs(pos[:, 1]) < hi)
        per_y[lab] = round(float(press[mk].mean()), 2)
    pm = pin & (np.abs(pos[:, 1]) < 25.01)                 # the pin as a rigid body: u = t + w x p
    P, U = pos[pm] - np.array([0, 0, 10.0]), disp[pm, 1:4]
    A = np.zeros((3 * len(P), 6))
    for i in range(3):
        A[i::3, i] = 1
    A[0::3, 4], A[0::3, 5] = P[:, 2], -P[:, 1]
    A[1::3, 3], A[1::3, 5] = -P[:, 2], P[:, 0]
    A[2::3, 3], A[2::3, 4] = P[:, 1], -P[:, 0]
    sol = np.linalg.lstsq(A, U.reshape(-1), rcond=None)[0]
    res = np.linalg.norm((U.reshape(-1) - A @ sol).reshape(-1, 3), axis=1)
    k = np.flatnonzero(pm)[np.argmax(disp[pm, 4])]
    return dict(nodes=nn, reaction_fz=round(float(rea[2]), 3), line_nodes=int(line.sum()),
                line_mean=round(float(press[line].mean()), 3), line_max=round(float(press[line].max()), 3),
                half_width_03=round(float(hw), 2), profile=prof, along_y=per_y,
                pin_translation=sol[:3].round(4).tolist(), pin_turn_deg=np.degrees(sol[3:]).round(4).tolist(),
                pin_spin_edge_mm=round(float(abs(sol[4]) * 5.0), 4), pin_fit_residual_max=round(float(res.max()), 4),
                pin_max_u=round(float(disp[k, 4]), 4), pin_max_at=pos[k].round(2).tolist(),
                block_max_u=round(float(disp[block, 4].max()), 4), max_u=round(float(disp[:, 4].max()), 4))


t6n = {}
for n in tn + ['T6_PIN_12', 'T6_PIN_08', 'T6_PIN_05']:
    q = t6n[n] = t6_read(NA / f'{n}.npz')
    print(f'  {n}: nodes {q["nodes"]}, Fz {q["reaction_fz"]}; line mean {q["line_mean"]} on {q["line_nodes"]} nodes'
          f' (max {q["line_max"]}); half-width (pressure over 0.3 MPa) {q["half_width_03"]} mm; line pressure by |y|: {q["along_y"]}')
    print(f'      pressure across the strip, 0.2 mm bins of |x| from 0: {q["profile"]}')
    print(f'      pin as a rigid body: translation {q["pin_translation"]} mm, turn about X, Y, Z {q["pin_turn_deg"]} deg'
          f' (the spin about its own axis moves its surface {q["pin_spin_edge_mm"]} mm), residual max {q["pin_fit_residual_max"]} mm;'
          f' largest pin displacement {q["pin_max_u"]} at {q["pin_max_at"]}; block max {q["block_max_u"]}; model max {q["max_u"]}')
for n in tn:
    print(f'  {n}: recomputed line mean {t6n[n]["line_mean"]} on {t6n[n]["line_nodes"]} nodes; the row has'
          f' {t6[n]["line_mean"]} on {t6[n]["line_nodes"]}')
lm = [t6[n]['line_mean'] for n in tn]
print('  line mean', lm, 'steps %', [round(100 * (b - a) / a, 1) for a, b in zip(lm, lm[1:])], '| against 6.76:',
      [round(100 * (v / 6.76 - 1), 1) for v in lm], '%')
for key in ('p_all', 'contact_vm'):
    v = [t6[n][key][0] for n in tn]
    print(f'  {key}', [round(x, 2) for x in v], 'steps %', [round(100 * (b - a) / a, 1) for a, b in zip(v, v[1:])])
a = t6n['T6M_06']['half_width_03']
print(f'  Hertz line contact, 500 N over 30 mm: peak = 2 F / (pi a L). a 1.57 -> {2 * 500 / (np.pi * 1.57 * 30):.2f} MPa;'
      f' a {a} (read above) -> {2 * 500 / (np.pi * a * 30):.2f} MPa')

# ---------------------------------------------------------------- D1
head('D1: the rerun study, from the job log and the saved arrays')
log = (FD / 'wip-logs' / 'd1_study.log').read_text(encoding='utf-8-sig')
conv = [tuple(float(x) for x in m) for m in re.findall(r'converge \(([\d.]+), (\d+), ([\d.]+), ([\d.]+), ([\d.]+)\)', log)]
print('  logged convergence rows (el, nodes, vm, layer, shear):', conv)
print('  logged mesh lines:', re.findall(r'(D1_Z_\d+): mesh rc (\d+), (\d+) nodes', log))
print('  logged reaction:', re.search(r'reaction (\[.*?\])', log).group(1))
ser = dict(vm=[c[2] for c in conv], layer=[c[3] for c in conv], shear=[c[4] for c in conv])
show(my_judge(ser, ALLOW))
print('  helper judge():', {k: helper_judge(ser, ALLOW)[k] for k in ('verdict', 'lowest_factor', 'lowest_entry')})
M = 4.5 * 11 * 89 / 100
print(f'  hand: spine as a beam built in at the two M5 holes (x +-50), 4.5 N from each arm at x +-39: end moment'
      f' {M:.1f} N mm; full section 14 x 4: {M / (14 * 16 / 6):.2f} MPa; net section beside the hole (8.5 x 4):'
      f' {M / (8.5 * 16 / 6):.2f} MPa; times 3 (open hole in tension): {3 * M / (8.5 * 16 / 6):.1f} MPa')
for n in ('D1_Z_20', 'D1_Z_15', 'D1_Z_11'):
    pos, s, disp, rea, nn = load(ND / f'{n}.npz')
    x, y, z = np.abs(pos[:, 0]), pos[:, 1], pos[:, 2]
    rh = np.hypot(x - 50, y)
    sp = (x >= 44) & (x <= 56.1) & (np.abs(y) <= 7.1) & (z <= 4.1)
    out = [f'{n}: nodes {nn}, reaction {rea.round(2).tolist()}, max disp {disp[:, 4].max():.4f}',
           f'box round the holes: vm max {top(pos, s[:, 10], sp)}']
    for lab, zz in (('top', z > 3.95), ('bottom', z < 0.05)):
        for x0, x1 in ((43.5, 44.5), (44.5, 46.0), (46.0, 47.0)):
            mk = zz & (x > x0) & (x < x1) & (np.abs(y) < 7.1)
            out.append(f'{lab} face, x {x0}..{x1}: mean sigma-x {s[mk, 1].mean():.2f}, largest |sigma-x| {np.abs(s[mk, 1]).max():.2f}'
                       f' on {mk.sum()} nodes')
    for lab, mk in (('on the hole wall (the fixed face)', sp & (rh < 2.76)),
                    ('0.2 to 0.6 mm off the wall', sp & (rh > 2.95) & (rh < 3.35)),
                    ('0.6 to 1.5 mm off the wall', sp & (rh > 3.35) & (rh < 4.25)),
                    ('ligaments beside the hole (|x-50| < 1, |y| 3.4..7)', sp & (np.abs(x - 50) < 1) & (np.abs(y) > 3.4)),
                    ('outboard of the hole (x > 53.5)', sp & (x > 53.5))):
        out.append(f'{lab}: vm max {top(pos, s[:, 10], mk)}, largest |sigma-x| {np.abs(s[mk, 1]).max():.2f}')
    print('  ' + '\n      '.join(out))

# ---------------------------------------------------------------- D2
head('D2 convergence series: rows recomputed from the saved arrays')
SCREWS = [(x, z) for x in (-30.0, 30.0) for z in (0.0, 7.0)]
G2 = 0.4


def d2_masks(pos):
    rho = np.hypot(pos[:, 0], pos[:, 1])
    pad = rho < 23.99
    ring = (rho >= 23.99) & (rho <= 26.0005) & (pos[:, 2] > -0.001) & (pos[:, 2] < 7.001)
    dxz = np.min([np.hypot(pos[:, 0] - x, pos[:, 2] - z) for x, z in SCREWS], axis=0)
    y = pos[:, 1]
    screw = (y >= -6.501) & (y <= 31.501) & ((dxz <= 1.5005) | ((dxz <= 2.0005) & (y <= -G2 + 0.001))
                                            | ((dxz <= 2.7505) & (y >= 28.499)))
    other = ~(pad | ring | screw)
    upper, lower = other & (y > G2 - 0.01), other & (y < -G2 + 0.01)
    return dict(pad=pad, ring=ring, screw=screw, dxz=dxz, upper_all=upper, lower_all=lower,
                upper=upper & ~((dxz < 3.75) & (y > 27.5)), lower=lower & ~((dxz < 3.0) & (y > -7.5)) & (y > -30.0))


def three(pos, s, mk):
    return dict(vm=top(pos, s[:, 10], mk), layer=top(pos, s[:, 3], mk), shear=top(pos, tau_z(s), mk))


def ring_fit(pos, disp, ring):
    x, y, u = pos[ring, 0], pos[ring, 1], disp[ring, 1:3]
    A = np.zeros((2 * ring.sum(), 3))
    A[0::2, 0] = 1
    A[1::2, 1] = 1
    A[0::2, 2], A[1::2, 2] = -y, x
    sol = np.linalg.lstsq(A, u.reshape(-1), rcond=None)[0]
    res = np.linalg.norm((u.reshape(-1) - A @ sol).reshape(-1, 2), axis=1)
    return sol, res


d2 = json.loads((FD / 'd2c_rows.json').read_text(encoding='utf-8'))
dn = {'+X': ['D2C_X_12', 'D2C_X_09', 'D2C_X_07'], '+Y': ['D2C_Y_12', 'D2C_Y_09', 'D2C_Y_07']}
logs = ''.join((FD / 'wip-logs' / f).read_text(encoding='utf-8-sig') for f in ('d2_conv_X.log', 'd2_conv_Y.log'))
ok_all, keep = True, {}
for case, ns in dn.items():
    for n in ns:
        pos, s, disp, rea, nn = load(ND / f'{n}.npz')
        m = d2_masks(pos)
        keep[n] = (pos, s, disp, m)
        row = d2[n]
        bad = []
        for h in ('upper', 'lower'):
            got = three(pos, s, m[h])
            for key in ALLOW:
                if abs(got[key][0] - row[h]['Z'][key]) > 0.011:
                    bad.append((h, key, got[key][0], row[h]['Z'][key]))
        ten = []
        for x, z in SCREWS:
            sk = (np.hypot(pos[:, 0] - x, pos[:, 2] - z) <= 1.5005) & (pos[:, 1] > 5) & (pos[:, 1] < 23)
            ten.append(round(float(s[sk, 2].mean() * np.pi * 2.25), 1))
        mesh = re.search(rf'{n}: mesh rc (\d+), (\d+) nodes', logs)
        ok_all &= not bad
        print(f'  {n}: log mesh rc {mesh.group(1)}, {mesh.group(2)} nodes; arrays {nn} nodes; reaction {rea.round(2).tolist()};'
              f' the six Z-layer numbers match the row file: {not bad} {bad if bad else ""}; screw tensions {ten}'
              f' (row {[round(q["tension"], 1) for q in row["screws"]]}); max disp {disp[:, 4].max():.3f}'
              f' (row {row["max_disp"]:.3f}); angles {row["angle_upper"]:.2f} / {row["angle_lower"]:.2f};'
              f' excessive flag {row["excessive"]}')
print('  all 36 numbers recomputed from the arrays equal the row file:', ok_all)

head('D2: verdict')
ser = {f'{h} half, {case}, {mm}': [d2[n][h]['Z'][mm] for n in ns]
       for case, ns in dn.items() for h in ('upper', 'lower') for mm in ALLOW}
lim = {k: ALLOW[k.split(', ')[2]] for k in ser}
show(my_judge(ser, lim))
saved = json.loads((FD / 'results.json').read_text(encoding='utf-8'))['D2']['judge']
print('  helper judge() on the same series == results.json D2.judge:', same(helper_judge(ser, lim), saved))

head('D2: where the lower half peaks are, case X, and what is there')


def inside(pos, m, d):
    rr = np.hypot(pos[:, 0], pos[:, 1] - 0.1)            # the lower seat: radius 26.1 about (0, +0.1)
    return m['lower'] & (rr > 26.1 + d) & (pos[:, 2] > d) & (pos[:, 2] < 7 - d)


for n in dn['+X']:
    pos, s, disp, m = keep[n]
    lo = m['lower']
    got = three(pos, s, lo)
    print(f'  {n}: vm {got["vm"]}, layer {got["layer"]}, shear {got["shear"]}')
    k = np.flatnonzero(lo)[np.argmax(tau_z(s)[lo])]
    p = pos[k]
    print(f'      shear peak node: {np.hypot(p[0], p[1] - 0.1):.3f} mm from the lower seat axis (seat radius 26.1), z {p[2]:.2f}'
          f' (ring faces at z 0 and 7, seat ends at -0.15 and 7.15), {np.degrees(np.arctan2(p[0], -(p[1] - 0.1))):.1f} deg from the lower crown;'
          f' sigma-z there {s[k, 3]:.2f}, vm {s[k, 10]:.2f}')
    rr = np.hypot(pos[:, 0], pos[:, 1] - 0.1)
    for lab, mk in (('seat surface nodes (r < 26.15)', lo & (rr < 26.15)),
                    ('seat nodes at or beyond the ring faces (r < 26.15, z under 0.05 or over 6.95)', lo & (rr < 26.15) & ((pos[:, 2] < 0.05) | (pos[:, 2] > 6.95))),
                    ('seat surface away from its rims (r < 26.15, z 1..6)', lo & (rr < 26.15) & (pos[:, 2] > 1) & (pos[:, 2] < 6)),
                    ('0.5 mm or more inside the material and off the seat ends', inside(pos, m, 0.5)),
                    ('1.0 mm or more inside', inside(pos, m, 1.0))):
        g = three(pos, s, mk)
        print(f'      {lab}: vm {g["vm"][0]}, layer {g["layer"][0]}, shear {g["shear"][0]} at {g["shear"][1]}')
for d in (0.5, 1.0):
    ser2 = {f'lower half {d} mm inside, {case}, {mm}': [three(keep[n][0], keep[n][1], inside(keep[n][0], keep[n][3], d))[mm][0] for n in ns]
            for case, ns in dn.items() for mm in ALLOW}
    show(my_judge(ser2, {k: ALLOW[k.split(', ')[2]] for k in ser2}))

head("D2: the ring as a rigid body in the XY plane, and the nodes the split of the run files under the wrong body")
# The mesh numbers each body's nodes in one block, so the ring body is the one long run of indices in the ring mask.
# split() calls everything with radius 23.99..26.0005 "ring"; the seats (radius 26.1 about (0, -+0.1)) touch the ring at
# the two crowns, so their nodes within about 2.5 mm of a crown fall under 26.0005 too.
for n in ['D2_X_30'] + dn['+X'] + dn['+Y']:
    if n in keep:
        pos, s, disp, m = keep[n]
    else:
        pos, s, disp, rea, nn = load(ND / f'{n}.npz')
        m = d2_masks(pos)
    i = np.flatnonzero(m['ring'])
    br = np.flatnonzero(np.diff(i) > 1)
    st, en = np.r_[i[0], i[br + 1]], np.r_[i[br], i[-1]]
    k0 = np.argmax(en - st)
    body = np.zeros(len(pos), bool)
    body[st[k0]:en[k0] + 1] = True
    rho = np.hypot(pos[:, 0], pos[:, 1])
    seat_as_ring = m['ring'] & ~body & (rho > 25.9)
    other_as_ring = m['ring'] & ~body & (rho <= 25.9)
    ring_missed = body & ~m['ring']
    print(f'  {n}: ring body is nodes {st[k0]}..{en[k0]} ({body.sum()}); the mask calls {m["ring"].sum()} nodes ring: {seat_as_ring.sum()}'
          f' of them are seat nodes (|x| up to {np.abs(pos[seat_as_ring, 0]).max():.2f}, {int((pos[seat_as_ring, 1] > 0).sum())} at the upper'
          f' crown, {int((pos[seat_as_ring, 1] < 0).sum())} at the lower), {other_as_ring.sum()} are pad or other nodes at the bore;'
          f' ring-body nodes the mask misses: {ring_missed.sum()}')
    for lab, mk in (('upper', seat_as_ring & (pos[:, 1] > 0)), ('lower', seat_as_ring & (pos[:, 1] < 0))):
        if mk.any():
            g = three(pos, s, mk)
            h = three(pos, s, m[lab])
            print(f'      {lab} seat nodes left out of the {lab} half: vm {g["vm"][0]}, layer {g["layer"][0]}, shear {g["shear"][0]}'
                  f' | the {lab} half as the run read it: vm {h["vm"][0]}, layer {h["layer"][0]}, shear {h["shear"][0]}')
    sol, res = ring_fit(pos, disp, body)
    k = np.flatnonzero(body)[np.argmax(disp[body, 4])]
    rig = sol[:2] + sol[2] * np.array([-pos[k, 1], pos[k, 0]])
    print(f'      ring body: largest |u| {disp[k, 4]:.4f} at {pos[k].round(2).tolist()} (model max {disp[:, 4].max():.4f});'
          f' rigid fit: translation {sol[:2].round(4).tolist()} mm, turn {np.degrees(sol[2]):.3f} deg (= {abs(sol[2]) * 26:.3f} mm at r 26);'
          f' rigid motion at that node {np.linalg.norm(rig):.4f}; residual mean {res.mean():.4f}, max {res.max():.4f};'
          f' uz {disp[body, 3].min():.4f}..{disp[body, 3].max():.4f}; ring vm max {s[body, 10].max():.2f} MPa')
    sol2, res2 = ring_fit(pos, disp, m['ring'])
    print(f'      with the mask of the run instead: turn {np.degrees(sol2[2]):.3f} deg, residual mean {res2.mean():.4f}, max {res2.max():.4f}')
    for lab, hm in (('upper', m['upper_all']), ('lower', m['lower_all'])):
        print(f'      {lab} half largest |u| {disp[hm, 4].max():.4f}', end=';')
    print(f' pads largest |u| {disp[m["pad"], 4].max():.4f}')

head('D2: both halves read 1.0 mm in from the seat surface and the seat ends, upper half with the wider zone round the heads')


def inner(pos, m, h, d=1.0):
    rr = np.hypot(pos[:, 0], pos[:, 1] + (0.1 if h == 'upper' else -0.1))
    mk = m[h + '_all'] & (rr > 26.1 + d) & (pos[:, 2] > d) & (pos[:, 2] < 7 - d)
    if h == 'upper':
        return mk & ~((m['dxz'] < 4.75) & (pos[:, 1] > 26.5))
    return mk & ~((m['dxz'] < 3.0) & (pos[:, 1] > -7.5)) & (pos[:, 1] > -30.0)


ser3 = {f'{h} half 1 mm in, {case}, {mm}': [three(keep[n][0], keep[n][1], inner(keep[n][0], keep[n][3], h))[mm][0] for n in ns]
        for case, ns in dn.items() for h in ('upper', 'lower') for mm in ALLOW}
show(my_judge(ser3, {k: ALLOW[k.split(', ')[2]] for k in ser3}))
for n in dn['+X'] + dn['+Y']:
    pos, s, disp, m = keep[n]
    g = three(pos, s, m['upper'])
    p = g['shear'][1]
    print(f'  {n}: upper half as the run read it: shear {g["shear"]}, {np.hypot(p[0], p[1] + 0.1):.2f} mm from the upper seat axis;'
          f' vm {g["vm"]}; layer {g["layer"]}')
