"""D3 part one: six adapter plates from one table, one script, one SolidWorks job. Writes P1..P6.SLDPRT, STLs and a table.

    python eval/haiku-oplan-d/d3_part1.py
"""
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import E, W, ring, walls, save_result, load_results  # noqa: E402
from swkit import (BLIND, THRU_ALL, Sk, bbox, bodies, export, extrude, feature_errors, job, log,  # noqa: E402
                   new_part, pick, plane, save, single_body, volume, face_info)

import numpy as np  # noqa: E402
import trimesh  # noqa: E402

# OD, t, bore, nA, dA, circA, rotA, nB, dB, circB, rotB, dc, depth, changed, why   (plan D_D3 section 3, decisions 5.1-5.4)
TABLE = {
    'P1': (70, 6, 30, 6, 3.4, 50, 0, 4, 4.5, 60, 45, 8, 3.0, True,
           'ring B turned 45 deg: at 0 deg the B counterbore overlapped the A hole by 0.7 mm'),
    'P2': (84, 6, 40, 6, 4.5, 62, 0, 6, 4.5, 62, 30, 8, 3.0, True,
           'ring B turned 30 deg: as tabled it sits exactly on ring A'),
    'P3': (96, 8, 52, 8, 3.4, 66, 0, 4, 5.5, 84, 0, 10, 4.0, False, ''),
    'P4': (68, 5, 28, 4, 3.4, 40, 0, 6, 4.5, 58, 0, 8, 4.0, True,
           'OD 60->68: B counterbore broke out by 3.0 mm; depth 4.6->4.0: floor was 0.4 mm'),
    'P5': (120, 8, 60, 12, 4.5, 80, 0, 6, 6.6, 104, 0, 11, 5.0, False, ''),
    'P6': (76, 6, 34, 6, 3.4, 46, 0, 3, 4.5, 64, 0, 8, 3.0, False, ''),
}
MASS_G_PER_MM3 = 1.19e-3          # PETG, swfea.PETG DENS 1190 kg/m3


def expect(what, got, want, tol):
    """Absolute check: stop this plate unless |got - want| <= tol (mm, mm3 or a count)."""
    if abs(got - want) > tol:
        raise RuntimeError(f'{what}: got {got:.4f}, want {want:.4f}, allowed {tol}')
    log(f'ok {what}: {got:.4f} (want {want:.4f})')


def hand(p):
    OD, t, bore, nA, dA, cA, rotA, nB, dB, cB, rotB, dc, depth, changed, why = TABLE[p]
    R, rb, rA, rB, rc = OD / 2, bore / 2, dA / 2, dB / 2, dc / 2
    V = (math.pi * R * R * t - math.pi * rb * rb * t - nA * math.pi * rA * rA * t - nB * math.pi * rB * rB * t
         - nB * math.pi * (rc * rc - rB * rB) * depth)
    return dict(V=V, floor=t - depth, parts={
        'disc': math.pi * R * R * t, 'bore': math.pi * rb * rb * t, 'A': nA * math.pi * rA * rA * t,
        'B': nB * math.pi * rB * rB * t, 'cbore': nB * math.pi * (rc * rc - rB * rB) * depth})


def build(j, p, out):
    OD, t, bore, nA, dA, cA, rotA, nB, dB, cB, rotB, dc, depth, changed, why = TABLE[p]
    R, rb, rA, rB, rc = OD / 2, bore / 2, dA / 2, dB / 2, dc / 2
    H = hand(p)
    A_pts, B_pts = ring(nA, cA, rotA, 0.0), ring(nB, cB, rotB, 0.0)
    d = new_part(j.sw, W / f'{p}.SLDPRT')
    with Sk(d, plane(d, 'Z', 0.0, 'X'), 'DISC') as s:
        s.circle((0, 0, 0), R)
    extrude(d, s.feat, 'DISC', t, mode=BLIND, want=(2, +1, 0.0), expect_dv=H['parts']['disc'])
    with Sk(d, plane(d, 'Z', 0.0, 'BORE_P'), 'BORE') as s:
        s.circle((0, 0, 0), rb)
    extrude(d, s.feat, 'BORE', t, cut=True, mode=THRU_ALL, want=(2, +1, 0.0), expect_dv=H['parts']['bore'])
    with Sk(d, plane(d, 'Z', 0.0, 'A_P'), 'A_HOLES') as s:
        for x, y, z in A_pts:
            s.circle((x, y, 0.0), rA)
    extrude(d, s.feat, 'A_HOLES', t, cut=True, mode=THRU_ALL, want=(2, +1, 0.0), expect_dv=H['parts']['A'])
    with Sk(d, plane(d, 'Z', 0.0, 'B_P'), 'B_HOLES') as s:
        for x, y, z in B_pts:
            s.circle((x, y, 0.0), rB)
    extrude(d, s.feat, 'B_HOLES', t, cut=True, mode=THRU_ALL, want=(2, +1, 0.0), expect_dv=H['parts']['B'])
    fl = t - depth
    with Sk(d, plane(d, 'Z', fl, 'CB_P'), 'CBORE') as s:
        for x, y, z in ring(nB, cB, rotB, fl):
            s.circle((x, y, fl), rc)
    extrude(d, s.feat, 'CBORE', depth, cut=True, mode=THRU_ALL, want=(2, +1, fl), expect_dv=H['parts']['cbore'])
    single_body(d)
    errs = feature_errors(d)
    expect(f'{p} feature errors', len(errs), 0, 0)
    V = volume(d)
    expect(f'{p} volume vs hand (mm3)', V, H['V'], 0.001 * H['V'])
    b = bbox(d)
    for k, want in enumerate((-R, -R, 0, R, R, t)):
        expect(f'{p} bbox[{k}]', b[k], want, 0.01)
    # measure the finished solid: centres and radii of every hole, the counterbore and the floor
    def centres(r):
        out = []
        for f in pick(d, kind='cyl', r=r):
            bx = face_info(f)['box']
            out.append(((bx[0] + bx[3]) / 2, (bx[1] + bx[4]) / 2, bx[2], bx[5]))
        return out
    meas_A = centres(rA)
    meas_B = centres(rB) if abs(rB - rA) > 1e-6 else []
    meas_cb = centres(rc)
    faces_expected = nA + (nB if abs(rB - rA) < 1e-6 else 0)
    if len(meas_A) != faces_expected:
        raise RuntimeError(f'{p}: {len(meas_A)} faces of r {rA} found, expected {faces_expected}')
    if len(meas_B) and len(meas_B) != nB:
        raise RuntimeError(f'{p}: {len(meas_B)} faces of r {rB} found, expected {nB}')
    if len(meas_cb) != nB:
        raise RuntimeError(f'{p}: {len(meas_cb)} counterbore faces, expected {nB}')
    dev = 0.0
    for x, y, _ in A_pts + B_pts:
        near = min(math.hypot(x - a[0], y - a[1]) for a in [(q[0], q[1]) for q in meas_A + meas_B])
        dev = max(dev, near)
    if dev > 0.02:
        raise RuntimeError(f'{p}: a hole centre is {dev:.3f} mm off its table position')
    cb_lo = min(q[2] for q in meas_cb)
    cb_hi = max(q[3] for q in meas_cb)
    floors = pick(d, kind='plane', normal=(0, 0, 1), inside=[-R, -R, fl - 0.1, R, R, fl + 0.1])
    floor_z = float(np.mean([face_info(f)['box'][2] for f in floors])) if floors else None
    expect(f'{p} counterbore floor Z', floor_z if floor_z is not None else -1.0, fl, 0.02)
    expect(f'{p} counterbore top', cb_hi, t, 0.02)
    # walls from the measured centres
    thr = [(q[0], q[1], rA, 'through') for q in meas_A] + [(q[0], q[1], rB, 'through') for q in meas_B]
    cbs = [(q[0], q[1], rc, 'cbore') for q in meas_cb]
    wmin, wwhere, _ = walls(R, rb, thr + cbs)
    # the STL
    save(d)                                   # RULES.md rule 5: the part is saved before it is exported
    export(j.sw, d, W / f'{p}.stl')
    mesh = trimesh.load(W / f'{p}.stl')
    wt = bool(mesh.is_watertight)
    shells = len(mesh.split(only_watertight=False))
    stl_vol = float(mesh.volume)
    stl_ok_vol = abs(stl_vol - V) / V <= 0.005
    bnd = mesh.bounds
    bnd_ok = all(abs(float(bnd[0][k]) - float(b[k])) < 0.1 for k in range(3)) and all(
        abs(float(bnd[1][k]) - float(b[k + 3])) < 0.1 for k in range(3))
    log(f'{p}: volume {V:.2f} hand {H["V"]:.2f} | STL watertight {wt} shells {shells} vol {stl_vol:.1f} ok {stl_ok_vol} '
        f'bounds ok {bnd_ok} | min wall {wmin:.2f} ({wwhere}) | floor {floor_z:.3f}')
    return dict(volume_mm3=round(V, 2), hand_volume_mm3=round(H['V'], 2), dv_pct=round(100 * (V - H['V']) / H['V'], 4),
                mass_g=round(V * MASS_G_PER_MM3, 2), bodies=len(bodies(d)), stl_watertight=wt, stl_shells=shells,
                stl_volume_mm3=round(stl_vol, 2), stl_volume_ok=stl_ok_vol, stl_bounds_ok=bnd_ok,
                min_wall_mm=round(wmin, 3), min_wall_where=wwhere, changed=changed, why=why,
                counterbore_floor_z_mm=round(floor_z, 3), hand_floor_z_mm=fl,
                holes_A=[[round(q[0], 3), round(q[1], 3)] for q in meas_A],
                holes_B=[[round(q[0], 3), round(q[1], 3)] for q in meas_B],
                counterbores=[[round(q[0], 3), round(q[1], 3)] for q in meas_cb])


def main():
    t0 = time.time()
    rows, failures = {}, {}
    with job() as j:
        for p in TABLE:
            try:
                rows[p] = build(j, p, None)
            except Exception as ex:      # noqa: BLE001 - a plate that fails is recorded, the rest still build
                failures[p] = str(ex)
                log('PLATE FAILED', p, str(ex))
    res = load_results()
    res['D3_part1'] = dict(rows=rows, failures=failures, minutes_part1=round((time.time() - t0) / 60, 2))
    (E / 'd3_part1_rows.json').write_text(__import__('json').dumps(res['D3_part1'], indent=2), encoding='utf-8')
    log('done part one in', round((time.time() - t0) / 60, 2), 'min; failures', failures)


if __name__ == '__main__':
    main()
