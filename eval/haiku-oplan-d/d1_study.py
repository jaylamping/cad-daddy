"""D1 study: the buck mount under the 9 N case (plan D_D1 section 4).

    python eval/haiku-oplan-d/d1_study.py a    # job A: rigid 9 N load on the four standoffs, screw holes fixed, mesh series 3.0/2.0/1.5
    python eval/haiku-oplan-d/d1_study.py b    # job B: second support (spot face under the head) at 2.0 and 1.5, and the even pull at 2.0

Hand values (plan section 2): reaction (0, 0, -9.0); displacement about 0.06-0.1 mm; spine top at (30, 0, 5) sigma_x about
0.61 MPa; peak near the M5 holes. Every solve is under 200,000 nodes; each job runs at most four studies.
"""
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import E, W, save_result  # noqa: E402
from swkit import (BLIND, MID, Sk, bbox, export, extrude, feature_errors, face_info, job, log, open_doc,  # noqa: E402
                   pick, plane, save, save_as, set_dim, volume, expect)
from swfea import PETG, static, converge  # noqa: E402
import numpy as np  # noqa: E402

ALLOW = dict(yield_mpa=45.0, layer=22.5, shear=13.0)
SO = [(39, 26.5), (-39, 26.5), (39, -26.5), (-39, -26.5)]   # standoff centres (plan D_D1)
F_UP = 9.0          # N, the 9 N (10 g) case, pulling the board away from the spine (plan: +Z)


def picks(d):
    tops = pick(d, kind='plane', normal=(0, 0, 1), inside=[-45, -31, 14.9, 45, 31, 15.1])
    holes = pick(d, kind='cyl', r=2.75)
    inserts = pick(d, kind='cyl', r=2.0)
    log(f'picks: tops {len(tops)}, M5 holes {len(holes)}, inserts {len(inserts)}')
    if len(tops) != 4 or len(holes) != 2:
        raise RuntimeError(f'pick counts wrong: tops {len(tops)} (want 4), M5 holes {len(holes)} (want 2)')
    return tops, holes, inserts


def load_remote(tops):
    return [('remote', tops, (0, 0, 20.0), (0, 0, F_UP), (0, 0, 0))]


def run_remote(j, d, el, name, support='holes'):
    tops, holes, inserts = picks(d)
    if support == 'holes':
        fixtures = [('fixed', holes)]
    else:
        fixtures = [('fixed', support)]
    ctrl = [(tops, 0.4 * el), (holes if support == 'holes' else support, 0.4 * el)]
    return static(j, d, name, PETG, fixtures=fixtures, loads=load_remote(tops), el=el, ctrl=ctrl)


def checks(r, tag):
    out = {}
    rx = r.reaction
    out['reaction_N'] = rx
    ok = abs(rx[2] + F_UP) <= 0.01 * F_UP and abs(rx[0]) < 0.01 and abs(rx[1]) < 0.01
    out['check1_reaction_ok'] = bool(ok)
    dmax = r.max_disp()
    out['max_disp_mm'] = round(dmax, 4)
    out['check2_disp_in_0.03_0.25'] = bool(0.03 <= dmax <= 0.25)
    # plain section: spine top face beside the screws, away from the arms: sigma_x at (30, 0, 5)
    near = r.near(np.array([[30.0, y, 5.0] for y in np.linspace(-6, 6, 13)]), 0.4)
    sx = float(r.s[near, 1].mean()) if near.any() else None
    out['section_sigma_x_at_30_0_5_MPa'] = round(sx, 3) if sx is not None else None
    out['check3_hand_0.61_within_15pct'] = bool(sx is not None and abs(sx - 0.61) <= 0.15 * 0.61)
    vm, at = r.peak()
    out['peak_vm_away_MPa'] = round(vm, 3)
    out['peak_at_mm'] = at
    out['vm_max_all_MPa'] = round(float(r.vm.max()), 3)
    out['plateau_outside_hole_wall'] = {}
    for k in (1.0, 2.0, 3.0, 5.0):
        m = r.away(dist=k)
        out['plateau_outside_hole_wall'][str(k)] = round(float(r.vm[m].max()), 3) if m.any() else None
    out['layer_tension_z_MPa'] = [round(r.layer_stress((0, 0, 1))[0], 3), r.layer_stress((0, 0, 1))[1]]
    out['layer_shear_z_MPa'] = [round(r.layer_shear((0, 0, 1))[0], 3), r.layer_shear((0, 0, 1))[1]]
    out['sf_yield'] = round(ALLOW['yield_mpa'] / vm, 2)
    out['sf_layer'] = round(ALLOW['layer'] / out['layer_tension_z_MPa'][0], 2)
    out['sf_shear'] = round(ALLOW['shear'] / out['layer_shear_z_MPa'][0], 2)
    # the insert boss walls (the default mask hides the Z 15 rim: read them separately, plan section 4)
    boxes = {'front_R': [34, 21, 4.9, 44, 31, 15.1], 'back_R': [34, -31, 4.9, 44, -21, 15.1],
             'front_L': [-44, 21, 4.9, -34, 31, 15.1], 'back_L': [-44, -31, 4.9, -34, -21, 15.1]}
    out['insert_boss_vm_MPa'] = {k: round(float(r.vm[r.in_box(b)].max()), 3) for k, b in boxes.items()}
    out['nodes'] = r.nodes
    out['el_mm'] = r.el
    out['solve_s'] = round(r.seconds)
    log(tag, json.dumps(out, default=str))
    return out


def job_a(j):
    d = open_doc(j.sw, W / 'buck_mount.SLDPRT')
    d.ForceRebuild3(False)
    expected = {3.0: 13000, 2.0: 30000, 1.5: 70000}
    rows = {}

    def run(el):
        log(f'predict: {expected.get(el)} nodes at el {el}, disp ~0.08 mm, peak at the M5 wall or the spine by the screws')
        r = run_remote(j, d, el, f'D1A_{str(el).replace(".", "p")}')
        rows[el] = checks(r, f'D1A el {el}')
        return r
    rowsc, conv = converge(run, (3.0, 2.0, 1.5), layers=(0, 0, 1))
    rows['converge'] = dict(rows=rowsc, converged=conv)
    save_result('D1_study_a', rows)
    log('converge', rowsc, 'converged', conv)


def make_twin(j):
    """buck_mount_twin: the same part with a 0.1 mm spot face under each M5 head (r 5 about the hole), a second support."""
    d = open_doc(j.sw, W / 'buck_mount.SLDPRT')
    save_as(d, W / 'buck_mount_twin.SLDPRT')
    v0 = volume(d)
    with Sk(d, plane(d, 'Z', 5.0, 'SPOT_P'), 'SPOT') as s:
        for x in (20.0, -20.0):
            s.circle((x, 0, 5.0), 5.0)
    extrude(d, s.feat, 'SPOT', 0.1, cut=True, mode=BLIND, want=(2, -1, 5.0),
            expect_dv=2 * math.pi * (25 - 7.5625) * 0.1)
    save(d)
    log('twin volume change', round(volume(d) - v0, 4), 'expected', round(-2 * math.pi * (25 - 7.5625) * 0.1, 4))
    return d


def annuli(d):
    a = pick(d, kind='plane', normal=(0, 0, 1), inside=[14.9, -5.1, 4.85, 25.1, 5.1, 4.95])
    b = pick(d, kind='plane', normal=(0, 0, 1), inside=[-25.1, -5.1, 4.85, -14.9, 5.1, 4.95])
    log(f'twin annuli: {len(a)} and {len(b)} faces')
    if len(a) != 1 or len(b) != 1:
        raise RuntimeError('twin annuli not found once each')
    return a + b


def job_b(j):
    out = {}
    d = make_twin(j)
    d.ForceRebuild3(False)
    for el in (2.0, 1.5):
        tops, _, _ = picks(d)
        ann = annuli(d)
        ctrl = [(tops, 0.4 * el), (ann, 0.4 * el)]
        r = static(j, d, f'D1B_twin_{str(el).replace(".", "p")}', PETG, fixtures=[('fixed', ann)],
                   loads=load_remote(tops), el=el, ctrl=ctrl)
        out[f'twin_{el}'] = checks(r, f'D1B twin el {el}')
        d = open_doc(j.sw, W / 'buck_mount_twin.SLDPRT')
    d = open_doc(j.sw, W / 'buck_mount.SLDPRT')
    d.ForceRebuild3(False)
    tops, holes, _ = picks(d)
    r = static(j, d, 'D1B_pull_2p0', PETG, fixtures=[('fixed', holes)],
               loads=[('normal', tops, -F_UP)], el=2.0, ctrl=[(tops, 0.8), (holes, 0.8)])
    out['normal_pull_2.0'] = checks(r, 'D1B even pull el 2.0')
    save_result('D1_study_b', out)
    log('job b result saved')


def job_c(j):
    """07-done item 6: the peak climbs at the standoff root (a sharp inside corner). Give those corners the 0.4 mm
    radius a printed part would have (a fillet), solve again at 2.0 and 1.5, and judge that."""
    from swkit import edges_where, fillet
    d = open_doc(j.sw, W / 'buck_mount.SLDPRT')
    save_as(d, W / 'buck_mount_fillet.SLDPRT')
    so = SO
    e = edges_where(d, lambda q: abs(q[2] - 5.0) < 0.01 and any(abs(math.hypot(q[0] - x, q[1] - y) - 4.0) < 0.01 for x, y in so))
    log('standoff root edges found', len(e))
    expect('standoff root edges', len(e), 4, 0)
    r0 = fillet(d, e, (0.4,), 'SO_ROOT')
    if r0 is None:
        raise RuntimeError('fillet did not build')
    d.ForceRebuild3(False)
    save(d)
    out = {}
    for el in (2.0, 1.5):
        tops, _, _ = picks(d)
        r = static(j, d, f'D1C_fillet_{str(el).replace(".", "p")}', PETG, fixtures=[('fixed', pick(d, kind='cyl', r=2.75))],
                   loads=load_remote(tops), el=el, ctrl=[(tops, 0.4 * el), (pick(d, kind='cyl', r=2.75), 0.4 * el)])
        out[f'fillet_{el}'] = checks(r, f'D1C fillet el {el}')
        d = open_doc(j.sw, W / 'buck_mount_fillet.SLDPRT')
    save_result('D1_study_c', out)
    log('job c result saved')


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'a'
    t0 = time.time()
    with job() as j:
        if which == 'a':
            job_a(j)
        elif which == 'b':
            job_b(j)
        elif which == 'c':
            job_c(j)
    log('study', which, 'done in', round((time.time() - t0) / 60, 2), 'min')
