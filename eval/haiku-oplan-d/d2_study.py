"""D2 study: split housing under 300 N on the bearing, +Y and +X, face Y -32 held (plan D_D2 section 4).

    python eval/haiku-oplan-d/d2_study.py a    # job 2: Y 2.5/1.0, X 2.5/1.0, Y bonded twin 2.5/1.0, Y 3.0/1.5
    python eval/haiku-oplan-d/d2_study.py b    # job 3: Y 2.0/0.7 and the governing case at 2.0/0.7 (and 3.0/1.5 if X governs)

Each case: a new model open (d2_fea.SLDPRT), 10 bodies, PETG halves, steel ring and screws, soft pads (EX 0.5 MPa).
Results go to results.json under D2_study_<job>, with the per-body split and the contact proof.
"""
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import W, save_result  # noqa: E402
from swkit import job, log, open_doc, pick, face_info  # noqa: E402
from swfea import PETG, STEEL, BONDED, NO_PENETRATION, SOLVER_DIRECT, static  # noqa: E402
import numpy as np  # noqa: E402

PAD = dict(name='Soft pad', EX=0.5e6, NUXY=0.45, DENS=1000.0, SIGYLD=1e6, SIGXT=1e6)
MATS = {'ring': STEEL, 'screw': STEEL, 'pad_': PAD}          # halves: PETG (default)
SCREWS = [(31.0, -0.2), (31.0, 7.2), (-31.0, -0.2), (-31.0, 7.2)]
F_MAG = 300.0


def picks(d):
    ring_od = pick(d, kind='cyl', r=26.0, inside=[-26.1, -26.1, -0.05, 26.1, 26.1, 7.05])
    seat_up = pick(d, kind='cyl', r=26.0, inside=[-26.1, 0.3, -0.2, 26.1, 26.1, 7.2])
    seat_lo = pick(d, kind='cyl', r=26.0, inside=[-26.1, -26.1, -0.2, 26.1, -0.3, 7.2])
    split_up = pick(d, kind='plane', normal=(0, -1, 0), inside=[-36.1, 0.3, -4.1, 36.1, 0.5, 11.1])
    split_lo = pick(d, kind='plane', normal=(0, 1, 0), inside=[-36.1, -0.5, -4.1, 36.1, -0.3, 11.1])
    ring_id = pick(d, kind='cyl', r=24.0, area=math.pi * 48 * 7)
    pads_in = pick(d, kind='cyl', r=23.0, inside=[-24.1, -2, 2.9, 24.1, 2, 4.1])
    base = pick(d, kind='plane', at=(0, -32, 3.5))
    screws = pick(d, kind='cyl', r=1.5)
    counts = dict(ring_od=len(ring_od), seat_up=len(seat_up), seat_lo=len(seat_lo), split_up=len(split_up),
                  split_lo=len(split_lo), ring_id=len(ring_id), pads_in=len(pads_in), base=len(base), screws=len(screws))
    log('pick counts', counts)
    want = dict(ring_od=1, seat_up=1, seat_lo=1, ring_id=1, pads_in=2, base=1, screws=4)
    au = sum(face_info(f)['area'] for f in split_up)
    al = sum(face_info(f)['area'] for f in split_lo)
    log(f'split faces: upper {len(split_up)} faces area {au:.1f} mm2, lower {len(split_lo)} faces area {al:.1f} mm2 (plan said 2 each)')
    # the two sides differ by the hole openings on the split face (lower Ø4 inserts end on it, upper Ø3.4 holes pass
    # through it), so areas are logged, not required to match
    if len(split_up) == 0 or len(split_lo) == 0:
        raise RuntimeError('split faces missing')
    bad = {k: (counts[k], want[k]) for k in want if counts[k] != want[k]}
    if bad:
        raise RuntimeError(f'pick counts wrong (got, want): {bad}')
    return dict(ring_od=ring_od, seat=seat_up + seat_lo, split_up=split_up, split_lo=split_lo, ring_id=ring_id,
                pads_in=pads_in, base=base, screws=screws)


def masks(pos):
    """Body masks by geometry (05-fea rule 5). Returns dict of boolean arrays over the nodes."""
    x, y, z = pos[:, 0], pos[:, 1], pos[:, 2]
    rz = np.hypot(x, y)
    ring = (rz >= 23.95) & (rz <= 25.95) & (z >= -0.05) & (z <= 7.05)
    pads = (rz >= 22.95) & (rz <= 24.05) & (z >= 2.95) & (z <= 4.05) & (np.abs(y) < 1)
    scr = np.zeros(len(pos), bool)
    for x0, z0 in SCREWS:
        rs = np.hypot(x - x0, z - z0)
        scr |= ((rs <= 1.95) & (y >= -6.45) & (y <= -0.35)) | ((rs <= 1.55) & (y >= -0.4) & (y <= 28.5)) | \
               ((rs <= 2.8) & (y >= 28.45) & (y <= 31.55))
    band = (rz > 25.95) & (rz < 26.05) & (z >= -0.1) & (z <= 7.1)          # the seat line, left out of both halves
    upper = (y > 0) & ~ring & ~pads & ~scr & ~band
    lower = (y < 0) & ~ring & ~pads & ~scr & ~band
    return dict(ring=ring, pads=pads, screws=scr, upper=upper, lower=lower, band=band)


def case(j, d, tag, direction, el, c, bonded=False):
    P = picks(d)
    F = (0.0, F_MAG, 0.0) if direction == 'Y' else (F_MAG, 0.0, 0.0)
    cs = [(BONDED, P['ring_od'], P['seat'])] if bonded else \
         [(NO_PENETRATION, P['ring_od'], P['seat']), (NO_PENETRATION, P['split_up'], P['split_lo'])]
    name = f'D2_{tag}'
    log(f'{name}: predict nodes for el {el} c {c}: about {int(41000 * 12 / el ** 3 * 0.9)} to {int(90000)} (plan 90000 at 2.5/1.0)')
    t0 = time.time()
    r = static(j, d, name, PETG, fixtures=[('fixed', P['base']), ('fixed', P['pads_in'])],
               loads=[('remote', P['ring_id'], (0, 0, 3.5), F, (0, 0, 0))], el=el,
               ctrl=[(P['seat'] + P['ring_od'], c), (P['screws'], 0.8), (P['pads_in'], 0.5)],
               contacts=cs, materials=MATS, solver=SOLVER_DIRECT, max_nodes=200000)
    M = masks(r.pos)
    out = dict(case=tag, direction=direction, el=el, c=c, bonded=bonded, nodes=r.nodes, solve_s=round(time.time() - t0),
               reaction_N=r.reaction)
    # the reaction must equal the load (check 1)
    want = np.array(F)
    out['check1_reaction_vs_load_pct'] = [round(100 * abs(r.reaction[k] + want[k]) / (abs(want).max()), 3) for k in range(3)]
    # the ring travel (check 2): mean UY/UX of the ring nodes, and the screws
    dv = r.disp[:, 1:4]
    out['ring_travel_mm'] = round(float(np.linalg.norm(dv[M['ring']], axis=1).mean()), 4)
    out['ring_UY_mean'] = round(float(dv[M['ring'], 1].mean()), 4)
    out['ring_UX_mean'] = round(float(dv[M['ring'], 0].mean()), 4)
    out['max_disp_mm'] = round(r.max_disp(), 4)
    # per-half summaries (each body against its own material): all three measures with places
    away = r.away()
    for half in ('upper', 'lower'):
        m = M[half] & away
        vm, at = r.peak(m)
        tz, wtz = r.layer_stress((0, 0, 1), m)
        sh, wsh = r.layer_shear((0, 0, 1), m)
        out[half] = dict(peak_vm_MPa=round(vm, 2), at_mm=at, sf_yield=round(45 / vm, 2), layer_tension_MPa=round(tz, 2),
                         at_layer=wtz, sf_layer=round(22.5 / tz, 2), layer_shear_MPa=round(sh, 2), at_shear=wsh,
                         sf_shear=round(13 / sh, 2), nodes=int(M[half].sum()))
    # the screws: tension per screw from the study (mean sigma_y over the shank slab)
    tens = []
    for x0, z0 in SCREWS:
        rs = np.hypot(r.pos[:, 0] - x0, r.pos[:, 2] - z0)
        row = []
        for yc in (10.0, 15.0, 20.0):
            sl = (np.abs(r.pos[:, 1] - yc) < 0.75) & (rs <= 1.5)
            row.append(round(float(r.s[sl, 2].mean()) * math.pi * 1.5 ** 2, 2) if sl.any() else None)
        tens.append(row)
    out['screw_tension_N_at_y10_15_20'] = tens
    # print-direction table: the three measures per half for each layer normal (the same result, read three ways)
    dirs = {}
    for nm, nv in (('Z', (0, 0, 1)), ('Y', (0, 1, 0)), ('X', (1, 0, 0))):
        row = {}
        for half in ('upper', 'lower'):
            m = M[half] & away
            tz, _ = r.layer_stress(nv, m)
            sh, _ = r.layer_shear(nv, m)
            row[half] = dict(tension_MPa=round(tz, 2), sf_tension=round(22.5 / tz, 2), shear_MPa=round(sh, 2),
                             sf_shear=round(13 / sh, 2))
        dirs[nm] = row
    out['direction_table'] = dirs
    out['screw_sum_N_y15'] = round(float(sum(t[1] for t in tens if t[1] is not None)), 2)
    # the steel and soft bodies, for the record
    out['pad_vm_max_MPa'] = round(float(r.vm[M['pads']].max()), 4) if M['pads'].any() else None
    out['masks_nodes'] = {k: int(v.sum()) for k, v in M.items()}
    out['guard_no_upper_lower_in_band'] = bool(not (M['upper'] & M['band']).any() and not (M['lower'] & M['band']).any())
    # plain section (check 3): upper half crown at X 0, Y 31.9, sigma_x (column 1) on the outer surface, z 0..7
    crown_pts = np.array([[0.0, 31.9, z] for z in range(0, 8)])
    cm = r.near(crown_pts, 0.3)
    if cm.any():
        out['crown_sigma_x_mean_MPa'] = round(float(r.s[cm, 1].mean()), 3)
        out['crown_sigma_x_max_MPa'] = round(float(r.s[cm, 1].max()), 3)
        out['crown_nodes'] = int(cm.sum())
    # the lower seat opens: ring UY minus lower housing UY near (0, -26, 3.5), within 1 mm of the seat surface
    near_lo = (np.hypot(r.pos[:, 0], r.pos[:, 1] + 26) < 1.0) & (np.abs(r.pos[:, 2] - 3.5) < 3) & M['lower']
    if near_lo.any():
        out['lower_seat_opening_mm'] = round(float(dv[M['ring'], 1].mean() - dv[near_lo, 1].mean()), 4)
    log(name, 'done', out['upper']['peak_vm_MPa'], out['lower']['peak_vm_MPa'])
    return out, r


def job_a(j):
    d = open_doc(j.sw, W / 'd2_fea.SLDPRT')
    res = {}
    for tag, dr, el, c, bd in (('Y_2.5_1.0', 'Y', 2.5, 1.0, False), ('X_2.5_1.0', 'X', 2.5, 1.0, False),
                               ('Y_bonded_2.5_1.0', 'Y', 2.5, 1.0, True), ('Y_3.0_1.5', 'Y', 3.0, 1.5, False)):
        d = open_doc(j.sw, W / 'd2_fea.SLDPRT')
        d.ForceRebuild3(False)
        out, _ = case(j, d, tag, dr, el, c, bd)
        res[tag] = out
        save_result('D2_study_job2', res)


def job_c(j):
    res = {}
    d = open_doc(j.sw, W / 'd2_fea.SLDPRT')
    d.ForceRebuild3(False)
    out, _ = case(j, d, 'Y_2.5_1.0_rerun', 'Y', 2.5, 1.0, False)
    res['Y_2.5_1.0_rerun'] = out
    save_result('D2_study_job4', res)


def job_b(j):
    res = {}
    d = open_doc(j.sw, W / 'd2_fea.SLDPRT')
    d.ForceRebuild3(False)
    # plan branch (D_D2 section 6): 2.0/0.7 is 220,878 nodes, over the 200,000 limit: use el 2.25, c 0.8 instead
    # 2.25/0.8 failed with a solver dialog, "Fixture <Fixed-1> transfer failed" (not in the plan's branches): try 2.25/1.0
    out, _ = case(j, d, 'Y_2.25_1.0', 'Y', 2.25, 1.0, False)
    res['Y_2.25_1.0'] = out
    save_result('D2_study_job3', res)


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'a'
    t0 = time.time()
    with job() as j:
        if which == 'a':
            job_a(j)
        elif which == 'c':
            job_c(j)
        else:
            job_b(j)
    log('D2 study', which, 'done in', round((time.time() - t0) / 60, 2), 'min')
