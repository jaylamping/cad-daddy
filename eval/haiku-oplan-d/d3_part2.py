"""D3 part two: the change request, made by EDITING the saved P1..P6 (no rebuild from the script).

    python eval/haiku-oplan-d/d3_part2.py

Change: all plates 1.5 mm thicker (DISC dimension edited), counterbore floors kept (the counterbore is cut from its floor
plane upward, so it follows the new top and its floor does not move), a chamfer round the top outside edge, and P3's
ring A moved to a Ø70 circle (turned 22.5 deg, see REPORT.md: the plan's unturned version would have overlapped the
counterbores by 0.3 mm).
"""
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import E, W, ring, walls, save_result, load_results  # noqa: E402
from d3_part1 import TABLE, hand, expect, MASS_G_PER_MM3  # noqa: E402
from swkit import (bbox, bodies, chamfer, edges_where, export, feature_errors, face_info, job, log, open_doc,  # noqa: E402
                   pick, redraw_circles, save, save_as, set_dim, volume)

import numpy as np  # noqa: E402
import trimesh  # noqa: E402

CHAMFER = {'P1': 0.4, 'P2': 1.0, 'P3': 0.4, 'P4': 0.4, 'P5': 1.0, 'P6': 1.0}   # decision 6: 0.4 where cbore is 1.0 from OD
P3_A_NEW = dict(circ=70, rot=22.5)                                                # decision 5: turned 22.5 deg


def tree(d):
    out, f = [], d.FirstFeature
    while f is not None:
        out.append((f.Name, f.GetTypeName2))
        f = f.GetNextFeature
    return out


def centres(d, r):
    out = []
    for f in pick(d, kind='cyl', r=r):
        bx = face_info(f)['box']
        out.append(((bx[0] + bx[3]) / 2, (bx[1] + bx[4]) / 2, bx[2], bx[5]))
    return out


def build_b(j, p):
    OD, t, bore, nA, dA, cA, rotA, nB, dB, cB, rotB, dc, depth, changed, why = TABLE[p]
    R, rb, rA, rB, rc = OD / 2, bore / 2, dA / 2, dB / 2, dc / 2
    H = hand(p)
    T = t + 1.5
    fl = t - depth
    c = CHAMFER[p]
    d = open_doc(j.sw, W / f'{p}.SLDPRT')
    d.ForceRebuild3(False)
    save_as(d, W / f'{p}_b.SLDPRT')                      # the edited copy; the original stays as built
    before = tree(d)
    V1 = volume(d)
    log(f'{p}_b: opened, tree has {len(before)} features, volume {V1:.2f}')
    # 1. thicken: edit the disc's depth dimension
    set_dim(d, 'DISC', t, T)
    d.ForceRebuild3(False)
    expect(f'{p}_b feature errors after thickening', len(feature_errors(d)), 0, 0)
    added_hand = 1.5 * (math.pi * R * R - math.pi * rb * rb - nA * math.pi * rA * rA - nB * math.pi * rc * rc)
    expect(f'{p}_b volume after thickening (mm3)', volume(d), V1 + added_hand, 0.001 * (V1 + added_hand))
    save(d)
    # 2. P3 only: ring A redrawn on a Ø70 circle in its own sketch
    if p == 'P3':
        pts = ring(nA, P3_A_NEW['circ'], P3_A_NEW['rot'], 0.0)
        redraw_circles(d, 'A_HOLES_SK', pts, rA)
        d.ForceRebuild3(False)
        expect('P3_b feature errors after redraw', len(feature_errors(d)), 0, 0)
        expect('P3_b volume unchanged by redraw (mm3)', volume(d), V1 + added_hand, 0.001 * (V1 + added_hand))
        save(d)
    # 3. chamfer the top outside edge
    e = edges_where(d, lambda q: abs(q[2] - T) < 0.01 and abs(math.hypot(q[0], q[1]) - R) < 0.01)
    expect(f'{p}_b top outside edges found', len(e), 1, 0)
    V_pre = volume(d)
    chamfer(d, e, c, 'TOP_CHAMFER')
    d.ForceRebuild3(False)
    dv_hand = -(c * c / 2) * 2 * math.pi * (R - c / 3)
    expect(f'{p}_b chamfer volume change (mm3)', volume(d) - V_pre, dv_hand, 0.02)
    V2 = volume(d)
    after = tree(d)
    same_prefix = after[:len(before)] == before
    extra = after[len(before):]
    expect(f'{p}_b tree: original features unchanged (1 = yes)', float(same_prefix), 1.0, 0)
    if p == 'P3':
        log('P3 tree extra entries:', extra)
    feats = [(x, y, rc, 'cbore') for x, y, _, _ in centres(d, rc)]
    save(d)
    fl_meas = [face_info(f)['box'][2] for f in pick(d, kind='plane', normal=(0, 0, 1),
                                                    inside=[-R, -R, fl - 0.1, R, R, fl + 0.1])]
    floor_z = float(np.mean(fl_meas)) if fl_meas else -1.0
    expect(f'{p}_b counterbore floor Z (kept)', floor_z, fl, 0.02)
    # measure the holes after the change
    A_meas = centres(d, rA)
    B_meas = centres(d, rB) if abs(rB - rA) > 1e-6 else []
    cb_meas = centres(d, rc)
    through = [(q[0], q[1], rA, 'through') for q in A_meas] + [(q[0], q[1], rB, 'through') for q in B_meas]
    cbs = [(q[0], q[1], rc, 'cbore') for q in cb_meas]
    wmin_plain, where_plain, _ = walls(R, rb, through + cbs)
    wmin_chamf, where_chamf, _ = walls(R - c, rb, through + cbs)
    wmin = min(wmin_plain, wmin_chamf)
    where = where_plain if wmin_plain <= wmin_chamf else where_chamf + ' (at the chamfer)'
    # P3: check ring A position (radius 35.0, first hole at 22.5 deg)
    a_ok = None
    if p == 'P3':
        rr = [math.hypot(q[0], q[1]) for q in A_meas]
        ang0 = math.degrees(math.atan2(A_meas[0][1], A_meas[0][0])) if A_meas else None
        a_ok = dict(n=len(A_meas), radius_mean=round(float(np.mean(rr)), 3), first_angle_deg=round(ang0 % 360, 2))
        log('P3 ring A after change:', a_ok)
    # chamfer edge present at the top, radius R - c
    ce = edges_where(d, lambda q: abs(q[2] - T) < 0.01 and abs(math.hypot(q[0], q[1]) - (R - c)) < 0.01)
    expect(f'{p}_b chamfer edge at radius R-c present', len(ce), 1, 0)
    save(d)
    export(j.sw, d, W / f'{p}_b.stl')
    mesh = trimesh.load(W / f'{p}_b.stl')
    wt = bool(mesh.is_watertight)
    shells = len(mesh.split(only_watertight=False))
    stl_vol = float(mesh.volume)
    stl_ok = abs(stl_vol - V2) / V2 <= 0.005
    log(f'{p}_b: volume {V2:.2f} hand {V1 + added_hand + dv_hand:.2f} | STL watertight {wt} shells {shells} '
        f'vol {stl_vol:.1f} ok {stl_ok} | min wall {wmin:.2f} ({where}) | floor {floor_z:.3f}')
    return dict(volume_mm3=round(V2, 2), hand_volume_mm3=round(V1 + added_hand + dv_hand, 2),
                volume_before_chamfer_mm3=round(V_pre, 2), mass_g=round(V2 * MASS_G_PER_MM3, 2), bodies=len(bodies(d)),
                stl_watertight=wt, stl_shells=shells, stl_volume_mm3=round(stl_vol, 2), stl_volume_ok=stl_ok,
                min_wall_mm=round(wmin, 3), min_wall_where=where, chamfer_mm=c,
                counterbore_floor_z_mm=round(floor_z, 3), hand_floor_z_mm=fl,
                changed=changed, why=why,
                tree_prefix_identical=same_prefix, tree_extra=[e[0] for e in extra],
                p3_ring_a=a_ok, thickness_mm=T)


def main():
    t0 = time.time()
    rows, failures = {}, {}
    with job() as j:
        for p in TABLE:
            try:
                rows[p] = build_b(j, p)
            except Exception as ex:      # noqa: BLE001 - recorded; the other plates still change
                failures[p] = str(ex)
                log('PLATE FAILED (part two)', p, str(ex))
    out = dict(rows=rows, failures=failures, minutes_part2=round((time.time() - t0) / 60, 2))
    (E / 'd3_part2_rows.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    log('done part two in', out['minutes_part2'], 'min; failures', failures)


if __name__ == '__main__':
    main()
