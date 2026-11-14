"""T3: static study of the T1 bracket, base on the bed (layers stacked along Z), screwed down through its four base holes,
with a 150 N pull along +X on the bore.

    python eval/haiku-a/t3_study.py remote     # the 150 N as a rigid remote force at the bore centre (the spec's words)
    python eval/haiku-a/t3_study.py even       # the second way: 150 N pull as an even force on the upright's +X face

One case per job (at most four studies per SolidWorks instance, playbook 05-fea.md). The study runs on a byte copy of
bracket.SLDPRT, so the T1 model on disk is not touched by the studies. Writes eval/haiku-a/t3_<case>.json.
"""
import json
import math
import shutil
import sys
import time
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'solidworks'))
from swfea import PETG, static  # noqa: E402
from swkit import bbox, face_info, job, log, open_doc, pick, volume  # noqa: E402

OUT = ROOT / '_wip' / 'sw-eval' / 'haiku-a'
CASE = sys.argv[1] if len(sys.argv) > 1 else 'remote'
F = 150.0                                 # N, the motor's pull
BORE_C = (3.0, 25.0, 28.0)                # bore centre on the upright's mid-thickness
SIZES = (3.0, 2.0, 1.5)                   # global element size, mm (coarse to fine)
CTRL = 0.8                                # mm on the fillet and the screw holes
ALLOW_YIELD, ALLOW_LAYER, ALLOW_SHEAR = 45.0, 22.5, 13.0    # PETG, swfea / playbook 05-fea.md
REQ_SF = 2.0


def hand_values():
    # bending of the upright about Y: the pull acts at Z 28, the root (the base top) is at Z 6
    arm = BORE_C[2] - 6.0
    M = F * arm                                            # N mm at the root
    I = 50.0 * 6.0 ** 3 / 12.0                              # 50 wide (Y), 6 thick (X): mm4
    sig_root = M * 3.0 / I                                 # MPa, plain section, normal stress along Z
    sig_z12 = F * (BORE_C[2] - 12.0) * 3.0 / I              # the same at Z 12, where the fillet no longer matters
    shear = F / (50.0 * 6.0)                               # MPa, average shear on the root section
    E_MPA = PETG['EX'] / 1e6                               # 1900 N/mm2
    defl = F * arm ** 3 / (3 * E_MPA * I)                  # cantilever tip deflection, mm (base compliance not included)
    return dict(hand_root_stress_mpa=round(sig_root, 3), hand_stress_z12_mpa=round(sig_z12, 3),
                hand_root_shear_mpa=round(shear, 3), hand_upright_tip_defl_mm=round(defl, 4), moment_root_nmm=M)


def mask_for(r, el, case):
    """Peak outside 2 elements of the screw-hole fixtures; outside 2 elements of the bore for the remote load, and
    outside 1 element of the +X face for the even load (the root fillet sits 0 to 4 mm from that face, so a 2 element
    exclusion there would hide the root itself; that choice is written in the report)."""
    keep = np.ones(len(r.pos), bool)
    if r.fixed_pts is not None and len(r.fixed_pts):
        keep &= cKDTree(r.fixed_pts).query(r.pos)[0] >= 2 * el
    if r.loaded_pts is not None and len(r.loaded_pts):
        dist = 2 * el if case == 'remote' else 1 * el
        keep &= cKDTree(r.loaded_pts).query(r.pos)[0] >= dist
    return keep


def main():
    t0 = time.time()
    hv = hand_values()
    log('hand values', hv)
    src = OUT / 'bracket.SLDPRT'
    dst = OUT / f'bracket_t3_{CASE}.SLDPRT'
    shutil.copyfile(src, dst)                         # byte copy: the study leaves T1's file alone
    result = {'case': CASE, 'hand': hv, 'rows': [], 'sizes': list(SIZES)}
    with job() as j:
        cw = j.simulation()
        d = open_doc(j.sw, dst)
        d.ForceRebuild3(False)
        log('volume', round(volume(d), 3), 'box', [round(v, 3) for v in bbox(d)])
        holes = pick(d, kind='cyl', r=2.75)
        bore = pick(d, kind='cyl', r=11.0)
        fil = pick(d, kind='cyl', r=4.0)
        xface = pick(d, kind='plane', at=(6.0, 5.0, 20.0))
        log('picks: holes', len(holes), 'bore', len(bore), 'fillet', len(fil), 'X6 face', len(xface))
        if len(holes) != 4 or len(bore) != 1 or len(fil) != 1 or len(xface) != 1:
            raise SystemExit('FAIL: pick counts are not what the bracket has')
        if CASE == 'remote':
            loads = [('remote', bore, BORE_C, (F, 0.0, 0.0), (0.0, 0.0, 0.0))]
        else:
            loads = [('normal', xface, -F)]              # negative = pulls out of the +X face, towards +X
        fixtures = [('fixed', holes)]
        for el in SIZES:
            n_pred = round(12 * volume(d) / el ** 3)
            log(f'predict: {n_pred} nodes before control refinement at el {el}; upright tip deflection about '
                f'{hv["hand_upright_tip_defl_mm"]} mm; peak von Mises near the root')
            r = static(j, d, f'{CASE[:3]}{int(el * 10)}', PETG, fixtures=fixtures, loads=loads, el=el,
                       ctrl=[(fil, CTRL), (holes, CTRL)])
            keep = mask_for(r, el, CASE)
            vm, at = r.peak(keep)
            row = dict(el=el, nodes=r.nodes, peak_vm=round(vm, 3), peak_at=at,
                       layer_z=round(r.layer_stress((0, 0, 1), keep)[0], 3),
                       shear_z=round(r.layer_shear((0, 0, 1), keep)[0], 3),
                       layer_x=round(r.layer_stress((1, 0, 0), keep)[0], 3),
                       layer_y=round(r.layer_stress((0, 1, 0), keep)[0], 3),
                       shear_x=round(r.layer_shear((1, 0, 0), keep)[0], 3),
                       shear_y=round(r.layer_shear((0, 1, 0), keep)[0], 3),
                       max_disp_mm=round(r.max_disp(), 4), reaction_N=[round(v, 3) for v in r.reaction],
                       applied_N=r.applied, solve_s=round(r.seconds))
            # plain-section check: mean sigma_zz on the two upright faces (X 0 and X 6) at Z 12, 4 mm from the root
            near12 = (np.abs(r.pos[:, 2] - 12.0) < 1.0) & (np.abs(r.pos[:, 1] - 25.0) < 8.0)
            row['sz_face_x6_z12'] = round(float(r.s[near12 & (np.abs(r.pos[:, 0] - 6.0) < 0.1), 3].mean()), 3)
            row['sz_face_x0_z12'] = round(float(r.s[near12 & (np.abs(r.pos[:, 0] - 0.0) < 0.1), 3].mean()), 3)
            # displacement where the load goes in and at the top of the upright (the hand value of 0.31 mm is the
            # upright alone; the base overhang rotates about the screw holes and adds to it)
            on_bore = cKDTree(r.loaded_pts).query(r.pos)[0] < 1e-3
            row['ux_bore_mean_mm'] = round(float(r.disp[on_bore, 1].mean()), 4)
            row['ux_top_max_mm'] = round(float(r.disp[r.pos[:, 2] > 45.0, 1].max()), 4)
            row['uz_base_end_mm'] = round(float(r.disp[(r.pos[:, 0] < 0.1) & (r.pos[:, 1] < 0.1), 3].min()), 4)
            result['rows'].append(row)
            log('row', row)
            if abs(abs(r.reaction[0]) - F) > 0.01 * F and CASE == 'remote':
                log('WARNING reaction X differs from the load:', r.reaction)
            result.setdefault('last_study', r.name)
        result['elapsed_s'] = round(time.time() - t0, 1)
        result['file'] = str(dst)
        j.sw.CloseDoc(d.GetTitle)
    (ROOT / 'eval' / 'haiku-a' / f't3_{CASE}.json').write_text(json.dumps(result, indent=2, default=str), encoding='utf-8')
    print(json.dumps(result, indent=2, default=str))


if __name__ == '__main__':
    main()
