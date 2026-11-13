"""T6: PETG block and a clearanced steel pin, with no-penetration contact and soft axial stabilizer pads."""
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / "cad" / "_wip" / "sw-eval" / "luna-a"
MODEL = CAD / "block_pin.SLDPRT"
sys.path.insert(0, str(ROOT / "tools" / "solidworks"))
from swfea import BONDED, NO_PENETRATION, PETG, STEEL, SOLVER_DIRECT, static
from swkit import MID, L, NUL, Sk, bodies, call, close, expect, extrude, insert_body, job, new_part, open_doc, pick, plane, save, save_as

PAD = dict(name="Soft axial stabilizer", EX=0.5e6, NUXY=0.45, DENS=1000.0, SIGYLD=1e6, SIGXT=1e6)
SIZES = (4.0, 3.0, 2.5)
R_BLOCK, R_PIN, PAD_R = 5.1, 5.0, 1.0
BEARING_HAND = 500.0 / (10.0 * 30.0)
ROOF_T = 20.0 - (10.0 + R_BLOCK)
ROOF_I = 30.0 * ROOF_T**3 / 12.0
HAND_ROOF_DEFLECTION = 500.0 * 40.0**3 / (48.0 * (PETG["EX"] / 1e6) * ROOF_I)
HAND_PIN_RISE = (R_BLOCK - R_PIN) + HAND_ROOF_DEFLECTION


def write_result(result):
    path = RUN / "results.json"
    all_results = json.loads(path.read_text(encoding="utf-8"))
    for item in all_results:
        if item["task"] == "T6":
            item.update(result)
            break
    path.write_text(json.dumps(all_results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (RUN / "t6_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_partial(**values):
    path = RUN / "t6_result.json"
    result = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {
        "hand_bearing_mpa": BEARING_HAND, "nodes": None, "solver": "Intel Direct Sparse",
        "how_pin_was_stabilised": "Two 1 mm long, radius-1 mm soft pads bond to the pin end faces; their outer faces are fixed.",
        "peak_contact_vm_mpa": None, "block_peak_at_mm": None, "pin_rise_mm": None,
        "reaction_n": None, "valid": False, "why": "Task in progress.", "status": "partial", "notes": "In progress."
    }
    result.update(values)
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_result(result)


def make_block(sw):
    d = new_part(sw, CAD / "block.SLDPRT")
    with Sk(d, plane(d, "Z", 10.0, "BLOCK_P"), "BLOCK") as s:
        s.rect((-20, -15, 10), (20, 15, 10))
    extrude(d, s.feat, "BLOCK", 20, mode=MID, expect_dv=40 * 30 * 20)
    save(d)
    with Sk(d, plane(d, "Y", 0.0, "BORE_P"), "BORE") as s:
        s.circle((0, 0, 10), R_BLOCK)
    extrude(d, s.feat, "BORE", 30, cut=True, mode=MID, expect_dv=math.pi * R_BLOCK**2 * 30)
    save(d)
    return d


def make_pin(sw):
    d = new_part(sw, CAD / "pin.SLDPRT")
    with Sk(d, plane(d, "Y", 0.0, "PIN_P"), "PIN") as s:
        s.circle((0, 0, 10), R_PIN)
    extrude(d, s.feat, "PIN", 50, mode=MID, expect_dv=math.pi * R_PIN**2 * 50)
    save(d)
    return d


def make_pad(sw, name, center_y):
    d = new_part(sw, CAD / f"{name.lower()}.SLDPRT")
    with Sk(d, plane(d, "Y", center_y, name + "_P"), name) as s:
        s.circle((0, center_y, 10), PAD_R)
    extrude(d, s.feat, name, 1.0, mode=MID, expect_dv=math.pi * PAD_R**2)
    save(d)
    return d


def build(sw):
    for make in (make_block, make_pin):
        d = make(sw)
        close(sw, d)
    for name, y in (("PAD_POS", 25.5), ("PAD_NEG", -25.5)):
        d = make_pad(sw, name, y)
        close(sw, d)
    d = open_doc(sw, CAD / "block.SLDPRT")
    insert_body(d, CAD / "pin.SLDPRT")
    insert_body(d, CAD / "pad_pos.SLDPRT")
    insert_body(d, CAD / "pad_neg.SLDPRT")
    save_as(d, MODEL)
    save(d)
    bs = bodies(d)
    if len(bs) != 4:
        raise RuntimeError(f"expected block, pin and two separate stabilizer bodies, got {bs}")
    print("BODIES", json.dumps(bs), flush=True)
    return d


def as_array(q, cols):
    if isinstance(q, tuple) and len(q) == 2 and not np.isscalar(q[0]):
        q = q[0]
    return np.asarray(q, dtype=float).reshape(-1, cols)


def reaction_split(st, res):
    raw = as_array(call(st.Mesh, "GetNodes"), 4)
    xyz = {int(row[0]): row[1:] * 1000.0 for row in raw}
    forces = as_array(call(res, "GetReactionForcesAndMoments", 0, NUL, 0, L()), 9)
    block = np.zeros(3)
    pads = np.zeros(3)
    for row in forces:
        p = xyz.get(int(row[0]))
        if p is None:
            continue
        if abs(p[2]) < 0.01:
            block += row[1:4]
        elif abs(abs(p[1]) - 26.0) < 0.02:
            pads += row[1:4]
    return {"block_bottom_reaction_xyz_n": block.round(4).tolist(),
            "pad_reaction_xyz_n": pads.round(4).tolist(),
            "contact_force_z_n": float(abs(block[2])),
            "pad_share_z_n": float(abs(pads[2]))}


def result_metrics(r):
    p = r.pos
    radius = np.hypot(p[:, 0], p[:, 2] - 10.0)
    block_nodes = ((p[:, 0] >= -20.01) & (p[:, 0] <= 20.01) &
                   (p[:, 1] >= -15.01) & (p[:, 1] <= 15.01) &
                   (p[:, 2] >= -0.01) & (p[:, 2] <= 20.01) & (radius >= 5.04))
    contact_zone = block_nodes & (radius <= 7.5)
    if not contact_zone.any():
        raise RuntimeError(f"{r.name}: no block nodes in the 2.4 mm band outside the bore; do not report a contact peak")
    ids = r.s[:, 0].astype(int)
    idx = np.flatnonzero(contact_zone)[np.argmax(r.vm[contact_zone])]
    vm = float(r.vm[idx])
    at = p[idx].round(3).tolist()
    pos_by_id = {int(row[0]): pos for row, pos in zip(r.s, p)}
    disp_by_id = {int(row[0]): row for row in r.disp} if r.disp is not None else {}
    pin_nodes = np.array([np.hypot(q[0], q[2] - 10) <= 5.01 and abs(q[1]) <= 25.01
                          for q in pos_by_id.values()])
    positions = list(pos_by_id.values())
    mid = np.array([np.hypot(q[0], q[2] - 10) <= 5.01 and abs(q[1]) <= max(1.25, r.el * 0.5)
                    for q in positions])
    mid_ids = [node_id for node_id, q in pos_by_id.items()
               if np.hypot(q[0], q[2] - 10) <= 5.01 and abs(q[1]) <= max(1.25, r.el * 0.5)]
    uz = [disp_by_id[node_id][3] for node_id in mid_ids if node_id in disp_by_id]
    if not uz:
        raise RuntimeError(f"{r.name}: no pin displacement nodes at midspan")
    return {"peak_contact_vm_mpa": vm, "block_peak_at_mm": at,
            "pin_rise_mm": float(np.mean(uz)), "pin_midspan_nodes": len(uz),
            "max_disp_mm": r.max_disp(), "nodes": r.nodes,
            "reaction_n": r.reaction[3], "reaction_xyz_n": r.reaction[:3],
            **(r.extra or {})}


def picks(d):
    block_hole = pick(d, kind="cyl", r=R_BLOCK)
    pin_cyl = pick(d, kind="cyl", r=R_PIN)
    bottom = pick(d, kind="plane", normal=(0, 0, -1), at=(10, 0, 0))
    pad_pos = pick(d, kind="plane", at=(0, 26, 10), area=math.pi * PAD_R**2)
    pad_neg = pick(d, kind="plane", at=(0, -26, 10), area=math.pi * PAD_R**2)
    end_pos = pick(d, kind="plane", at=(0, 25, 10), area=math.pi * R_PIN**2)
    end_neg = pick(d, kind="plane", at=(0, -25, 10), area=math.pi * R_PIN**2)
    counts = [len(q) for q in (block_hole, pin_cyl, bottom, pad_pos, pad_neg, end_pos, end_neg)]
    if counts != [1] * 7:
        raise RuntimeError(f"contact/setup face picks expected one each, got {counts}")
    return block_hole, pin_cyl, bottom, pad_pos, pad_neg, end_pos, end_neg


def main(phase="contact"):
    CAD.mkdir(parents=True, exist_ok=True)
    RUN_START = time.time()
    start_file = RUN / "t6_start.json"
    if phase == "contact":
        start_file.write_text(json.dumps({"start_epoch": RUN_START, "start_utc": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(RUN_START))}, indent=2) + "\n", encoding="utf-8")
        update_partial(status="partial", notes="T6 running; do not treat partial results as valid.")
    else:
        stamp = json.loads(start_file.read_text(encoding="utf-8"))
        RUN_START = stamp["start_epoch"]
        if time.time() - RUN_START >= 40 * 60:
            update_partial(status="partial", valid=False,
                           why="The 40 minute T6 hard limit expired before the bonded proof could start.",
                           notes="Bonded proof not run: hard task limit reached.")
            print("T6_LIMIT: bonded proof not started; 40 minute limit reached", flush=True)
            return
    with job(wait_s=1800) as j:
        j.simulation()
        d = build(j.sw) if phase == "contact" else open_doc(j.sw, MODEL)
        j.simulation()
        block_hole, pin_cyl, bottom, pad_pos, pad_neg, end_pos, end_neg = picks(d)
        fixture = [("fixed", bottom + pad_pos + pad_neg)]
        materials = {"pin": STEEL, "pad": PAD}
        ctl_surfaces = [block_hole, pin_cyl, pad_pos, pad_neg, end_pos, end_neg]
        contact_full = [(NO_PENETRATION, block_hole, pin_cyl)]
        vol = sum(row[1] for row in bodies(d))
        hand_disp_mm = HAND_PIN_RISE
        print("MODEL_SHA256", hashlib.sha256(MODEL.read_bytes()).hexdigest(), flush=True)
        print("HAND_CHECK", json.dumps({"bearing_mpa": BEARING_HAND, "radial_clearance_mm": R_BLOCK - R_PIN,
                                         "roof_t_mm": ROOF_T, "roof_I_mm4": round(ROOF_I, 3),
                                         "simple_supported_roof_deflection_mm": round(HAND_ROOF_DEFLECTION, 4),
                                         "predicted_nodes": "12*model_volume/el^3, corrected x4 for thin bodies/contact controls",
                                         "expected_pin_rise_mm": hand_disp_mm,
                                         "expected_peak": "block upper bore wall near y=+/-15 mm"}), flush=True)

        def predict(el, label):
            expect_nodes = round(12 * vol / el**3 * 4.0)
            print(f"PREDICT {label}: el={el:.2f} mm nodes~{expect_nodes} max={min(200000, 2*expect_nodes)} "
                  f"pin/max rise~{hand_disp_mm:.3f} mm peak near upper bore wall at y=+/-15 mm", flush=True)
            return expect_nodes

        def run_contact(el, name, loads):
            expected = predict(el, name)
            local = max(0.6, el * 0.4)
            ctrl = [(fs, local) for fs in ctl_surfaces]
            r = static(j, d, name, PETG, fixtures=fixture, loads=loads, el=el, ctrl=ctrl,
                       contacts=contact_full, materials=materials, solver=SOLVER_DIRECT,
                       post=reaction_split, max_nodes=min(200000, expected * 2))
            print("MESH_CHECK", name, json.dumps({"expected": expected, "actual": r.nodes}), flush=True)
            if r.nodes < expected / 2 or r.nodes > expected * 2:
                raise RuntimeError(f"{name}: nodes {r.nodes} differ by more than 2x from prediction {expected}; discard stresses")
            disp_i = int(np.argmax(np.abs(r.disp[:, 4])))
            disp_id = int(r.disp[disp_i, 0])
            disp_pos = {int(row[0]): pos for row, pos in zip(r.s, r.pos)}.get(disp_id, [float("nan")] * 3)
            print("DISPLACEMENT_CHECK", json.dumps({"max_disp_mm": r.max_disp(), "at_mm": np.round(disp_pos, 3).tolist(),
                                                     "hand_pin_rise_estimate_mm": hand_disp_mm}), flush=True)
            if r.max_disp() is None or not hand_disp_mm / 3 <= r.max_disp() <= hand_disp_mm * 3:
                raise RuntimeError(f"{name}: maximum displacement {r.max_disp()} mm is outside 3x of hand estimate {hand_disp_mm}")
            expect(f"{name} reaction Fz N", r.reaction[2], -sum(abs(ld[3][2]) for ld in loads), 0.01)
            metrics = result_metrics(r)
            print("STUDY", json.dumps({"name": name, **metrics}), flush=True)
            return r, metrics

        if phase in ("contact", "retry"):
            full_rows = []
            full_results = []
            for el in SIZES:
                if time.time() - RUN_START >= 40 * 60:
                    break
                r, m = run_contact(el, f"T6_CONTACT_{el:g}", [
                    ("remote", end_pos, (0, 25, 10), (0, 0, 250), (0, 0, 0)),
                    ("remote", end_neg, (0, -25, 10), (0, 0, 250), (0, 0, 0))])
                full_rows.append([el, m["nodes"], m["peak_contact_vm_mpa"], m["block_peak_at_mm"],
                                  m["contact_force_z_n"], m["pad_share_z_n"], m["pin_rise_mm"]])
                full_results.append((r, m))
                np.savez_compressed(RUN / f"t6_nodes_{str(el).replace('.', '_')}.npz", pos=r.pos, stress_mpa=r.s, disp_mm=r.disp)
                update_partial(nodes=m["nodes"], peak_contact_vm_mpa=m["peak_contact_vm_mpa"],
                               block_peak_at_mm=m["block_peak_at_mm"], pin_rise_mm=m["pin_rise_mm"],
                               reaction_n=m["reaction_n"], contact_force_n=m["contact_force_z_n"],
                               pad_share_n=m["pad_share_z_n"], convergence_rows=full_rows,
                               notes=f"Contact mesh {el:g} mm completed; convergence series in progress.")
            if full_results and time.time() - RUN_START < 40 * 60:
                r, proof = run_contact(2.5, "T6_CONTACT_PROOF_0_5N", [
                    ("remote", end_pos, (0, 25, 10), (0, 0, 0.25), (0, 0, 0)),
                    ("remote", end_neg, (0, -25, 10), (0, 0, 0.25), (0, 0, 0))])
                update_partial(proof_reaction_n=proof["reaction_n"], proof_pin_rise_mm=proof["pin_rise_mm"],
                               proof_contact_force_n=proof["contact_force_z_n"], proof_pad_share_n=proof["pad_share_z_n"],
                               convergence_rows=full_rows,
                               notes="Full-load contact mesh series and same-direction 0.5 N clearance proof completed; bonded proof remains.")
                print("CONTACT_PROOF", json.dumps(proof), flush=True)
            close(j.sw, d)
        else:
            expected = predict(2.5, "T6_BONDED_PROOF_0_5N")
            local = max(0.6, 2.5 * 0.4)
            loads = [("remote", end_pos, (0, 25, 10), (0, 0, 0.25), (0, 0, 0)),
                     ("remote", end_neg, (0, -25, 10), (0, 0, 0.25), (0, 0, 0))]
            r = static(j, d, "T6_BONDED_PROOF_0_5N", PETG, fixtures=fixture, loads=loads, el=2.5,
                       ctrl=[(fs, local) for fs in ctl_surfaces],
                       contacts=[(BONDED, block_hole, pin_cyl)], materials=materials,
                       solver=SOLVER_DIRECT, post=reaction_split, max_nodes=min(200000, expected * 2))
            print("MESH_CHECK", json.dumps({"expected": expected, "actual": r.nodes}), flush=True)
            if r.nodes < expected / 2 or r.nodes > expected * 2:
                raise RuntimeError(f"bonded proof mesh nodes {r.nodes} differ by more than 2x from {expected}")
            metrics = result_metrics(r)
            print("BONDED_PROOF", json.dumps(metrics), flush=True)
            update_partial(bonded_proof_reaction_n=metrics["reaction_n"],
                           bonded_proof_pin_rise_mm=metrics["pin_rise_mm"],
                           bonded_proof_nodes=metrics["nodes"], bonded_proof_contact_force_n=metrics["contact_force_z_n"],
                           bonded_proof_pad_share_n=metrics["pad_share_z_n"])
            close(j.sw, d)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "contact")
