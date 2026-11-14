"""D1: the 9 N case on buck_mount.SLDPRT, two load directions, one study each.

Set-up (written before the solve):
  fixed:  the back face of the bottom bar (Y 10, Z -17..-7): stands in for the rail's front face, clamped by two M5.
          Only the bottom bar touches the rail, so only its back face is fixed. Real screws are not modelled.
  loads:  9 N in total over the four boss tops (Y 17.5), shared by area.
          'pull' = board pulled forward off the bosses (-9, outward), 'push' = board pushed back onto them (+9).
Hand (PETG, E 1.9 GPa, frame in-plane yield 45 MPa, across layers 22.5, interlayer shear 13):
  side bar 7 wide x 4 thick, I about X = 7 x 4^3 / 12 = 37.33 mm4, top boss 2.25 N at Z 39.5, bar root at Z -7.
  stress at Z 0 (39.5 mm from the boss):  M = 2.25 x 39.5 = 88.9 N.mm, sigma = M (h/2) / I = 4.77 MPa
  deflection of top boss (cantilever from Z -7, arm 46.5): d = F L^3 / 3 E I = 1.06 mm
  transverse shear in the bar: 1.5 V / A = 1.5 x 2.25 / 28 = 0.12 MPa
Predicted nodes at el 1.5: about 12 x V / el^3 = 12 x 8821 / 3.375 = 31,000 (about 1.5 times that with the opening corners).
"""
import sys
from pathlib import Path

WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT / 'solidworks'))
import numpy as np  # noqa: E402
from swfea import PETG, static  # noqa: E402
from swkit import expect, job, log, open_doc, pick  # noqa: E402

MODEL = WT / '_wip' / 'sw-eval' / 'haiku-d' / 'd1' / 'buck_mount.SLDPRT'
BOSS_TOP_AREA = 3.14159265 * 3.5 ** 2                      # 38.48 mm2
BOSS_TOPS = [(-39.0, 17.5, -13.5), (39.0, 17.5, -13.5), (-39.0, 17.5, 39.5), (39.0, 17.5, 39.5)]


def run(j, d, name, value):
    # the back face at Y 10 is one ring-shaped face over the whole frame, so it cannot be fixed on the bottom bar alone.
    # Fix the two M5 hole walls instead: the screws are what holds the frame to the rail (playbook 05-fea: fixed hole walls)
    holes = pick(d, kind='cyl', r=2.75, inside=[-30, 9.9, -13.0, 30, 14.1, -7.0])
    tops = [f for x, y, z in BOSS_TOPS for f in pick(d, kind='plane', normal=(0, 1, 0), at=(x, y, z))]
    log(name, 'fixed hole walls', len(holes), 'boss top faces', len(tops))
    expect('two M5 hole walls', len(holes), 2, 0)
    expect('four boss tops', len(tops), 4, 0)
    r = static(j, d, name, PETG, fixtures=[('fixed', holes)],
               loads=[('normal', tops, value)], el=1.5)
    print(r.summary(), flush=True)
    return r


def checks(r, applied_n, name):
    out = {'name': name, 'nodes': r.nodes, 'elements': r.elements, 'applied_n': applied_n}
    # 1. reaction equals load
    out['reaction_resultant_n'] = float(r.reaction[3])
    expect(f'{name} check 1: reaction resultant equals load', r.reaction[3], abs(applied_n), 0.01)
    # 2. displacement
    out['max_disp_mm'] = float(r.max_disp())
    # 3. stress at Z 0 on the side bar, away from the fixture and the corners (ball of radius 2 mm)
    pt = np.array([39.0, 12.0, 0.0])                       # side bar, mid-bar height, inside the bar (Y 10..14)
    near = np.linalg.norm(r.pos - pt, axis=1) < 2.0
    out['sigma_z_Z0_mpa'] = float(r.s[near, 3].mean())    # sz column; compare with the hand 4.77 (tension or compression, sign printed)
    out['sigma_z_Z0_nodes'] = int(near.sum())
    # 4. peak away from the fixture, the loads and the opening corners (re-entrant corners are singular: reported separately)
    mask = (np.abs(r.pos[:, 0]) > 20) & (r.pos[:, 2] > -3) & (r.pos[:, 2] < 33)
    pk, where = r.peak(mask)
    out['peak_vm_mpa_excl_corners'], out['peak_vm_where_excl_corners'] = pk, where
    out['vm_max_all_mpa'] = float(r.vm.max())
    lay, lay_at = r.layer_stress((0, 1, 0), mask)          # layers stacked along Y: the frame is printed flat
    sh, sh_at = r.layer_shear((0, 1, 0), mask)
    out['layer_stress_mpa'], out['layer_stress_where'] = lay, lay_at
    out['layer_shear_mpa'], out['layer_shear_where'] = sh, sh_at
    return out


if __name__ == '__main__':
    import json
    res = []
    with job(wait_s=1800) as j:
        j.simulation()
        d = open_doc(j.sw, MODEL)
        d.ForceRebuild3(False)
        for name, val in (('D1_PULL_9N', -9.0), ('D1_PUSH_9N', 9.0)):
            r = run(j, d, name, val)
            res.append(checks(r, 9.0, name))
            np.savez(WT / 'eval' / 'haiku-d' / f'{name.lower()}_nodal.npz', pos=r.pos, s=r.s, disp=r.disp)
    (WT / 'eval' / 'haiku-d' / 'd1_study_results.json').write_text(json.dumps(res, indent=2), encoding='utf-8')
    print(json.dumps(res, indent=2))
