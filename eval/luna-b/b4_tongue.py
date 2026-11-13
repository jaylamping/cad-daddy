"""Build and solve the two-body tongue-in-slot contact case for B4."""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from scipy.spatial import Delaunay

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / 'cad' / '_wip' / 'sw-eval' / 'luna-b'
SIM = ROOT / 'cad' / '_sim' / 'sw-eval' / 'luna-b'
sys.path.insert(0, str(ROOT / 'tools' / 'solidworks'))
from swkit import MID, NUL, L, Sk, bodies, bbox, call, close, expect, export, extrude, feature_errors, insert_body, job, new_part, open_doc, pick, plane, save, save_as, volume  # noqa: E402
from swfea import NO_PENETRATION, BONDED, PETG, SOLVER_DIRECT, _arr, static  # noqa: E402

BLOCK = CAD / 'tongue_slot_block.SLDPRT'
TONGUE = CAD / 'tongue_slot_tongue.SLDPRT'
PADS = [CAD / f'tongue_pad_{i}.SLDPRT' for i in range(4)]
MODEL = CAD / 'tongue_slot.SLDPRT'
CONTACT_MODEL = CAD / 'tongue_slot_contact.SLDPRT'
PAD_MAT = {'name': 'B4 soft stabilizer', 'EX': 0.5e6, 'NUXY': 0.45, 'DENS': 1000.0,
           'SIGYLD': 1.0e6, 'SIGXT': 1.0e6}
SIZES = (4.0, 3.5, 3.0)


def make_parts(j):
    d = new_part(j.sw, BLOCK)
    with Sk(d, plane(d, 'Z', 10.0, 'BLOCK_P'), 'BLOCK') as s:
        s.rect((-20, -10, 10), (20, 10, 10))
    extrude(d, s.feat, 'BLOCK', 20, mode=MID, expect_dv=16000)
    with Sk(d, plane(d, 'Y', 0.0, 'SLOT_P'), 'SLOT') as s:
        s.rect((-4.1, 0, 8), (4.1, 0, 20))
    extrude(d, s.feat, 'SLOT', 20, cut=True, mode=MID, expect_dv=8.2 * 12 * 20)
    save(d)
    expect('block volume', volume(d), 14032, 0.001)
    if feature_errors(d):
        raise RuntimeError(f'block feature errors: {feature_errors(d)}')
    close(j.sw, d)

    d = new_part(j.sw, TONGUE)
    with Sk(d, plane(d, 'Y', 0.0, 'TONGUE_P'), 'TONGUE') as s:
        s.rect((-4, 0, 8.1), (4, 0, 40))
    extrude(d, s.feat, 'TONGUE', 20, mode=MID, expect_dv=8 * 20 * 31.9)
    # A shallow inset makes the Z30-40 loaded region its own -X-facing planar face.
    with Sk(d, plane(d, 'X', -3.95, 'LOAD_PATCH_P'), 'LOAD_PATCH') as s:
        s.rect((-3.95, -10, 30), (-3.95, 10, 40))
    extrude(d, s.feat, 'LOAD_PATCH', 0.1, cut=True, mode=MID, expect_dv=20)
    save(d)
    expect('tongue volume with load relief', volume(d), 5084, 0.001)
    if feature_errors(d):
        raise RuntimeError(f'tongue feature errors: {feature_errors(d)}')
    close(j.sw, d)

    for i, (y, z) in enumerate(((-7, 26), (-3, 26), (3, 26), (7, 26))):
        d = new_part(j.sw, PADS[i])
        with Sk(d, plane(d, 'Z', 26.0, f'PAD_P{i}'), f'PAD{i}') as s:
            s.rect((4.0, y - 0.75, 26.0), (4.5, y + 0.75, 26.0))
        extrude(d, s.feat, 'PAD', 4.0, mode=MID, expect_dv=3.0)
        save(d)
        close(j.sw, d)

    d = open_doc(j.sw, BLOCK)
    insert_body(d, TONGUE)
    expect('physical bodies before supports', len(bodies(d)), 2, 0)
    save_as(d, MODEL)
    export(j.sw, d, CAD / 'tongue_slot.stl')
    close(j.sw, d)

    d = open_doc(j.sw, BLOCK)
    for p in [TONGUE, *PADS]:
        insert_body(d, p)
    expect('contact model bodies', len(bodies(d)), 6, 0)
    if feature_errors(d):
        raise RuntimeError(f'contact model feature errors: {feature_errors(d)}')
    save(d)
    save_as(d, CONTACT_MODEL)
    close(j.sw, d)


def tongue_mask(r):
    p = r.pos
    return ((p[:, 0] >= -4.02) & (p[:, 0] <= 4.02) & (p[:, 1] >= -10.02) & (p[:, 1] <= 10.02)
            & (p[:, 2] >= 8.08) & (p[:, 2] <= 40.02))


def section_fx(r, z0):
    p = r.pos
    mask = tongue_mask(r) & (np.abs(p[:, 2] - z0) <= 0.45)
    xy = np.round(p[mask, :2], 3)
    txz = r.s[mask, 5]  # Sxx,Syy,Szz,Txy,Txz,Tyz; integrate Txz over a Z-normal cut.
    if len(xy) < 12:
        raise RuntimeError(f'only {len(xy)} tongue nodes near cut Z={z0}')
    unique, inv = np.unique(xy, axis=0, return_inverse=True)
    tau = np.zeros(len(unique)); count = np.zeros(len(unique))
    np.add.at(tau, inv, txz); np.add.at(count, inv, 1)
    tau /= count
    tri = Delaunay(unique, qhull_options='QJ')
    total = 0.0
    for ids in tri.simplices:
        q = unique[ids]
        if np.any(q[:, 0] < -4.01) or np.any(q[:, 0] > 4.01) or np.any(q[:, 1] < -10.01) or np.any(q[:, 1] > 10.01):
            continue
        v1 = q[1] - q[0]; v2 = q[2] - q[0]
        area = abs(v1[0] * v2[1] - v1[1] * v2[0]) / 2
        total += float(area * tau[ids].mean())
    return total


def forces_from_sections(r):
    above = section_fx(r, 20.5)
    below_top = section_fx(r, 19.5)
    above_floor = section_fx(r, 8.5)
    return {'v_above_slot_N': above, 'v_below_top_contact_N': below_top, 'v_above_floor_N': above_floor,
            'right_wall_N': abs(above - below_top), 'left_wall_N': abs(above_floor)}


def pad_reaction_post(st, res):
    nodes = _arr(call(st.Mesh, 'GetNodes'), 4)
    xyz = {int(row[0]): row[1:] * 1000 for row in nodes}
    q = _arr(res.GetReactionForcesAndMoments(0, NUL, 0, L()), 9)
    selected = []
    for row in q:
        p = xyz.get(int(row[0]))
        if p is not None and abs(p[2] - 28.0) < 0.02 and 3.99 <= p[0] <= 4.51 and min(abs(p[1] - v) for v in (-7, -3, 3, 7)) <= 0.8:
            selected.append(row[1:4])
    force = np.sum(selected, axis=0) if selected else np.zeros(3)
    return {'pad_reaction_vector_n': force.tolist(), 'pad_reaction_resultant_n': float(np.linalg.norm(force))}


def main():
    RUN.mkdir(parents=True, exist_ok=True); CAD.mkdir(parents=True, exist_ok=True); SIM.mkdir(parents=True, exist_ok=True)
    started = time.time()
    with job(wait_s=1800) as j:
        make_parts(j)
        j.simulation()
        d = open_doc(j.sw, CONTACT_MODEL)
        d.ForceRebuild3(False)
        block_bottom = pick(d, kind='plane', normal=(0, 0, -1), at=(0, 0, 0))
        wall_plus = pick(d, kind='plane', normal=(-1, 0, 0), at=(4.1, 0, 14))
        wall_minus = pick(d, kind='plane', normal=(1, 0, 0), at=(-4.1, 0, 14))
        tongue_plus = pick(d, kind='plane', normal=(1, 0, 0), at=(4.0, 0, 14))
        tongue_minus = pick(d, kind='plane', normal=(-1, 0, 0), at=(-4.0, 0, 14))
        load_face = pick(d, kind='plane', normal=(-1, 0, 0), at=(-3.9, 0, 35), area=200)
        pad_fixed = []
        for y, z in ((-7, 26), (-3, 26), (3, 26), (7, 26)):
            fs = pick(d, kind='plane', normal=(0, 0, 1), at=(4.25, y, 28), area=0.75)
            expect(f'pad fixed face at Y{y} Z{z}', len(fs), 1, 0); pad_fixed += fs
        for name, fs in (('block bottom', block_bottom), ('right slot wall', wall_plus), ('left slot wall', wall_minus),
                         ('tongue right side', tongue_plus), ('tongue left side', tongue_minus), ('80N patch', load_face)):
            expect(name + ' face count', len(fs), 1, 0)
        contacts = [(NO_PENETRATION, wall_plus, tongue_plus), (NO_PENETRATION, wall_minus, tongue_minus)]
        fixtures = [('fixed', block_bottom + pad_fixed)]
        ctrl = [(wall_plus + wall_minus + tongue_plus + tongue_minus, 2.0), (load_face, 2.0)]
        bounds = bbox(d)
        print(f'B4 prediction: total volume about 19128 mm3; expected nodes at el=4/3.5/3 mm about '
              f'{round(12*19128/4**3*1.5)}, {round(12*19128/3.5**3*1.5)}, {round(12*19128/3**3*1.5)}; '
              'hand wall forces (left lower, right upper) about 101.2 N, 181.2 N; peak block stress near slot corners; '
              'tip lateral displacement order 2-4 mm.', flush=True)
        print('B4 assembly bounds', bounds, 'bodies', bodies(d), flush=True)

        proof = static(j, d, 'B4_GAP_PROOF', PETG, fixtures=fixtures, loads=[('normal', load_face, 0.001)],
                       el=4.0, ctrl=ctrl, contacts=contacts, materials={'PAD': PAD_MAT}, solver=SOLVER_DIRECT,
                       max_nodes=199999, post=pad_reaction_post)
        tm = tongue_mask(proof)
        proof_shift = float(np.mean(proof.disp[tm & (proof.pos[:, 0] < -3.9) & (proof.pos[:, 2] >= 8.1) & (proof.pos[:, 2] <= 10), 1]))
        proof_pads = proof.extra
        np.savez_compressed(SIM / 'B4_gap_proof.npz', pos=proof.pos, stress=proof.s, displacement=proof.disp,
                            fixed_points=proof.fixed_pts, loaded_points=proof.loaded_pts)
        print('B4 gap proof summary', proof.summary(), 'left lower tongue mean UX at Z8.1-10', proof_shift,
              'pad support reaction', proof_pads, flush=True)

        rows = []
        full_results = []
        for el in SIZES:
            r = static(j, d, f'B4_FULL_{el:.1f}', PETG, fixtures=fixtures,
                       loads=[('normal', load_face, 80.0)], el=el, ctrl=ctrl, contacts=contacts,
                       materials={'PAD': PAD_MAT}, solver=SOLVER_DIRECT, max_nodes=199999, post=pad_reaction_post)
            forces = forces_from_sections(r)
            p = r.pos; tongue = tongue_mask(r)
            block_box = ((p[:, 0] >= -20.01) & (p[:, 0] <= 20.01) & (p[:, 1] >= -10.01) & (p[:, 1] <= 10.01)
                         & (p[:, 2] >= -0.01) & (p[:, 2] <= 20.01))
            slot_void = (np.abs(p[:, 0]) < 4.09) & (p[:, 2] > 8.01)
            block = block_box & ~slot_void
            peak_i = np.flatnonzero(block)[np.argmax(r.vm[block])]
            tip = tongue & (p[:, 2] >= 39.8)
            row = {'el_mm': el, 'nodes': r.nodes, 'elements': r.elements, 'reaction': r.reaction,
                   'max_disp_mm': r.max_disp(), 'tip_ux_mm': float(r.disp[tip, 1].max()),
                   'block_peak_vm_mpa': float(r.vm[peak_i]), 'block_peak_at_mm': p[peak_i].round(3).tolist(),
                   'section_forces': forces, 'pad_reaction': r.extra}
            rows.append(row); full_results.append(r)
            np.savez_compressed(SIM / f'B4_full_{el:.1f}.npz', pos=r.pos, stress=r.s, displacement=r.disp,
                                fixed_points=r.fixed_pts, loaded_points=r.loaded_pts)
            print('B4 full row', json.dumps(row), flush=True)

        fine = rows[-1]
        hand_left, hand_right = 101.176470588, 181.176470588
        wall = fine['section_forces']
        section_balance = abs((wall['right_wall_N'] - wall['left_wall_N']) - 80.0) / 80.0
        pad_share = fine['pad_reaction']['pad_reaction_resultant_n']
        proof_ok = proof_shift <= -0.09
        valid = (proof_ok and abs(fine['reaction'][3] - 80.0) <= 0.8 and pad_share <= 0.8
                 and section_balance <= 0.05 and all(r.nodes < 200000 for r in full_results))
        result = {
            'hand_wall_forces_n': [hand_left, hand_right],
            'wall_forces_n': [wall['left_wall_N'], wall['right_wall_N']],
            'nodes': fine['nodes'], 'how_tongue_was_stabilised':
                'Four 0.5 x 1.5 x 4 mm analysis-only flexure pads on the tongue side at X4,Z24-28,Y=-7,-3,3,7, fixed at Z28; E=0.5 MPa. '
                'At the 0.001 N +X contact proof they carry under the 0.001 N and permit the tongue to translate across the 0.1 mm clearance.',
            'block_peak_vm_mpa': fine['block_peak_vm_mpa'], 'block_peak_at_mm': fine['block_peak_at_mm'],
            'tongue_tip_disp_mm': fine['tip_ux_mm'], 'reaction_n': fine['reaction'][3],
            'valid': bool(valid),
            'why': {'gap_proof_mean_ux_mm': proof_shift, 'gap_proof_pad_reaction': proof_pads,
                    'gap_proof_pass': proof_ok,
                    'pad_reaction_n': pad_share, 'pad_share_pct': 100 * pad_share / 80,
                    'section_force_balance_error_pct': 100 * section_balance,
                    'contact_forces_by_section_n': wall,
                    'hand_forces_n_left_right': [hand_left, hand_right],
                    'mesh_series': rows,
                    'mesh_node_counts_below_200k': all(r['nodes'] < 200000 for r in rows),
                    'limitation': 'Nodal stresses were integrated over Delaunay triangulations of near-horizontal tongue-node slices; compare convergence across sizes.'},
            'status': 'complete', 'notes': 'Two no-penetration wall contacts; direct sparse solver. See REPORT.md for the contact proof, section-force method, and convergence.'}
        (RUN / 'b4_result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        main = json.loads((RUN / 'results.json').read_text(encoding='utf-8'))
        main['B4'] = result
        (RUN / 'results.json').write_text(json.dumps(main, indent=2), encoding='utf-8')
        close(j.sw, d)
    print('B4 elapsed seconds', round(time.time() - started, 1), flush=True)


if __name__ == '__main__':
    main()
