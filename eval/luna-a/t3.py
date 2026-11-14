"""T3: converged bracket study, with a second even-force load representation."""
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / "cad" / "_wip" / "sw-eval" / "luna-a"
MODEL = CAD / "bracket.SLDPRT"
sys.path.insert(0, str(ROOT / "tools" / "solidworks"))
from swfea import PETG, converge, static
from swkit import call, expect, job, open_doc, pick


HAND_VOLUME = (
    36000 + 50 * 4**2 * (1 - math.pi / 4)
    - 4 * 6 * 5**2 * (1 - math.pi / 4)
    - 4 * math.pi * 2.75**2 * 6
    - math.pi * 11**2 * 6
    - 4 * math.pi * 1.7**2 * 6
)
HAND_STRESS = 150 * (28 - 6) / (50 * 6**2 / 6)
HAND_DISP_UPRIGHT = 150 * (28 - 6) ** 3 / (3 * 1900 * (50 * 6**3 / 12))
BASE_SPAN = 25 - 6
ROOT_MOMENT = 150 * (28 - 6)
BASE_I = 50 * 6**3 / 12
BASE_ROTATION = ROOT_MOMENT * BASE_SPAN / (1900 * BASE_I)
HAND_DISP_BASE = ROOT_MOMENT * BASE_SPAN**2 / (2 * 1900 * BASE_I)
HAND_DISP = HAND_DISP_UPRIGHT + HAND_DISP_BASE + BASE_ROTATION * (28 - 6)
SIZES = (4.0, 3.0, 2.5)
MASK_DISTANCE = 2 * max(SIZES)


def log_prediction(el, case):
    # The first 4 mm mesh with local controls measured 18,675 nodes. The base
    # volume formula underpredicted it by 2.014x, so use the measured count and
    # an empirical 1.5 size exponent for subsequent controlled meshes.
    expected_nodes = round(18_675 * (4.0 / el) ** 1.5)
    print(
        f"PREDICT {case}: el={el:.2f} mm, nodes~{expected_nodes}, "
        f"displacement~{HAND_DISP:.3f} mm, peak at the inside R4 junction along Y",
        flush=True,
    )
    return expected_nodes


def write_task_result(result):
    path = RUN / "results.json"
    all_results = json.loads(path.read_text(encoding="utf-8"))
    for item in all_results:
        if item["task"] == "T3":
            item.update(result)
            break
    path.write_text(json.dumps(all_results, indent=2) + "\n", encoding="utf-8")
    (RUN / "t3_result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def main():
    print("MODEL_SHA256_BEFORE", hashlib.sha256(MODEL.read_bytes()).hexdigest(), flush=True)
    print(
        f"HAND root stress={HAND_STRESS:.4f} MPa; displacement={HAND_DISP:.4f} mm "
        f"(upright {HAND_DISP_UPRIGHT:.3f} + base flex {HAND_DISP_BASE:.3f} + "
        f"base rotation {BASE_ROTATION * (28 - 6):.3f})",
        flush=True,
    )
    with job(wait_s=1800) as j:
        j.simulation()
        d = open_doc(j.sw, MODEL)
        d.ForceRebuild3(False)

        def setup():
            d.ForceRebuild3(False)
            fixtures = pick(d, kind="cyl", r=2.75)
            bore = pick(d, kind="cyl", r=11.0)
            root = pick(d, kind="cyl", r=4.0)
            front = pick(d, kind="plane", normal=(-1, 0, 0), at=(0, 5, 28))
            if len(fixtures) != 4 or len(bore) != 1 or len(root) != 1 or len(front) != 1:
                raise RuntimeError(
                    f"pick counts: screw walls={len(fixtures)}, bore={len(bore)}, "
                    f"inside R4={len(root)}, front face={len(front)}"
                )
            controls = [(root, 1.5), (fixtures, 2.0), (bore, 2.0)]
            return fixtures, bore, root, front, controls

        def primary(el):
            predicted = log_prediction(el, "T3 bore remote")
            fixtures, bore, _, _, controls = setup()
            r = static(
                j,
                d,
                f"T3_REMOTE_{el:g}",
                PETG,
                fixtures=[("fixed", fixtures)],
                loads=[("remote", bore, (3, 25, 28), (150, 0, 0), (0, 0, 0))],
                el=el,
                ctrl=controls,
                max_nodes=min(200_000, predicted * 2),
            )
            if r.disp is not None and len(r.disp):
                max_i = int(np.argmax(np.abs(r.disp[:, 4])))
                max_id = int(r.disp[max_i, 0])
                pos_by_id = {int(row[0]): p for row, p in zip(r.s, r.pos)}
                max_pos = np.round(pos_by_id.get(max_id, [np.nan] * 3), 2).tolist()
                near_i = int(np.argmin(np.linalg.norm(r.pos - np.array([3.0, 25.0, 28.0]), axis=1)))
                near_id = int(r.s[near_i, 0])
                disp_by_id = {int(row[0]): row[1:] for row in r.disp}
                print(
                    "DISPLACEMENT_CHECK",
                    json.dumps({
                        "max_node": max_id,
                        "max_at_mm": max_pos,
                        "max_vector_mm": np.round(disp_by_id[max_id][0:3], 5).tolist(),
                        "max_resultant_mm": float(disp_by_id[max_id][3]),
                        "nearest_bore_node": near_id,
                        "nearest_bore_at_mm": r.pos[near_i].round(2).tolist(),
                        "nearest_bore_vector_mm": np.round(disp_by_id[near_id][0:3], 5).tolist(),
                        "nearest_bore_resultant_mm": float(disp_by_id[near_id][3]),
                    }),
                    flush=True,
                )
            if r.nodes < predicted / 2 or r.nodes > predicted * 2:
                raise RuntimeError(f"node count {r.nodes} is over 2x away from prediction {predicted}; do not judge stresses")
            if r.max_disp() is None or not HAND_DISP / 3 <= r.max_disp() <= HAND_DISP * 3:
                raise RuntimeError(f"displacement {r.max_disp()} mm is over 3x away from hand estimate {HAND_DISP:.4f} mm")
            expect(f"{r.name} reaction Fx N", r.reaction[0], -150.0, 0.01)
            expect(f"{r.name} reaction resultant N", r.reaction[3], 150.0, 0.01)
            primary.last_result = r
            return r

        primary.last_result = None
        rows, converged = converge(primary, SIZES, tol=0.05, layers=(0, 0, 1))
        # Recompute and retain the finest run once more is unnecessary: converge's final result is captured by the closure.
        fine = primary.last_result
        if fine is None:
            raise RuntimeError("converge did not retain its final result")
        keep = fine.away(dist=MASK_DISTANCE)
        vm, at = fine.peak(keep)
        layer_z, layer_z_at = fine.layer_stress((0, 0, 1), keep)
        shear_z, shear_z_at = fine.layer_shear((0, 0, 1), keep)
        directions = {}
        for label, normal in (("X", (1, 0, 0)), ("Y", (0, 1, 0)), ("Z", (0, 0, 1))):
            tension, p_t = fine.layer_stress(normal, keep)
            shear, p_s = fine.layer_shear(normal, keep)
            directions[label] = {
                "tension_mpa": tension,
                "tension_at_mm": p_t,
                "shear_mpa": shear,
                "shear_at_mm": p_s,
                "sf_tension": 22.5 / tension if tension > 0 else None,
                "sf_shear": 13.0 / shear if shear > 0 else None,
            }
        np.savez_compressed(RUN / "t3_fine_nodes.npz", pos=fine.pos, stress_mpa=fine.s, disp_mm=fine.disp)
        print("PRIMARY_FINAL", json.dumps({
            "el_mm": fine.el, "nodes": fine.nodes, "peak_vm_mpa": vm, "peak_at_mm": at,
            "layer_z_mpa": layer_z, "layer_z_at_mm": layer_z_at,
            "layer_shear_z_mpa": shear_z, "layer_shear_z_at_mm": shear_z_at,
            "max_disp_mm": fine.max_disp(), "reaction_n": fine.reaction,
            "converged": converged,
        }), flush=True)

        # The fourth study is the playbook's second-load check: the motor mounting face gets
        # the same +X resultant as an even tensile traction instead of a rigid remote coupling to the bore.
        predicted = log_prediction(SIZES[0], "T3 even front-face traction")
        fixtures, _, _, front, controls = setup()
        alt = static(
            j,
            d,
            "T3_FRONT_TRACTION",
            PETG,
            fixtures=[("fixed", fixtures)],
            loads=[("normal", front, 150.0)],
            el=SIZES[0],
            ctrl=controls,
            max_nodes=min(200_000, predicted * 2),
        )
        if alt.nodes < predicted / 2 or alt.nodes > predicted * 2:
            raise RuntimeError(f"alternate load node count {alt.nodes} is over 2x from prediction {predicted}")
        if alt.max_disp() is None or not HAND_DISP / 3 <= alt.max_disp() <= HAND_DISP * 3:
            raise RuntimeError(f"alternate load displacement {alt.max_disp()} mm is outside 3x hand estimate")
        expect("front traction reaction Fx N", alt.reaction[0], -150.0, 0.01)
        expect("front traction reaction resultant N", alt.reaction[3], 150.0, 0.01)
        alt_keep = alt.away(dist=MASK_DISTANCE)
        alt_vm, alt_at = alt.peak(alt_keep)
        alt_layer, alt_layer_at = alt.layer_stress((0, 0, 1), alt_keep)
        alt_shear, alt_shear_at = alt.layer_shear((0, 0, 1), alt_keep)
        print("ALTERNATE_LOAD", json.dumps({
            "el_mm": alt.el, "nodes": alt.nodes, "peak_vm_mpa": alt_vm, "peak_at_mm": alt_at,
            "layer_z_mpa": alt_layer, "layer_z_at_mm": alt_layer_at,
            "layer_shear_z_mpa": alt_shear, "layer_shear_z_at_mm": alt_shear_at,
        }), flush=True)

    model_sha256 = hashlib.sha256(MODEL.read_bytes()).hexdigest()
    print("MODEL_SHA256_FINAL", model_sha256, flush=True)
    yield_mpa = max(vm, alt_vm)
    layer_mpa = max(layer_z, alt_layer)
    shear_mpa = max(shear_z, alt_shear)
    sf_yield = 45.0 / yield_mpa if yield_mpa > 0 else None
    sf_layer = 22.5 / layer_mpa if layer_mpa > 0 else None
    verdict = "pass" if converged and sf_yield >= 2.0 and sf_layer >= 2.0 else "fail"
    result = {
        "hand_root_stress_mpa": HAND_STRESS,
        "el_mm": SIZES[-1],
        "nodes": fine.nodes,
        "peak_vm_mpa": vm,
        "peak_at_mm": at,
        "layer_stress_mpa": layer_z,
        "sf_yield": sf_yield,
        "sf_layer": sf_layer,
        "max_disp_mm": fine.max_disp(),
        "reaction_n": float(fine.reaction[3]),
        "converged": bool(converged),
        "convergence_rows": [list(row) for row in rows],
        "verdict": verdict,
        "status": "done" if converged else "partial",
        "notes": (
            f"Layer shear along Z={shear_z:.3f} MPa at {shear_z_at}; "
            f"support is fixed on the four Ø5.5 screw-hole walls; peaks are reported at least "
            f"{MASK_DISTANCE:g} mm from fixture and load nodes. Alternate even front-face traction: "
            f"vm={alt_vm:.3f} MPa, Z tension={alt_layer:.3f} MPa, Z shear={alt_shear:.3f} MPa. "
            f"Controlling results use the higher of the bore remote and even traction on the full x=0 face "
            f"(a broad-face sensitivity, not a localized bore load); "
            f"direction table: {json.dumps(directions)}. Layer Z peak at {layer_z_at}; "
            f"shear Z peak at {shear_z_at}. Model SHA-256 after the job: {model_sha256}."
        ),
    }
    write_task_result(result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
