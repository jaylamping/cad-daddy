"""One finer sharp-corner mesh to check the local inside-corner trend."""
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / "cad" / "_wip" / "sw-eval" / "luna-a"
MODEL = CAD / "bracket_sharp.SLDPRT"
EL = 1.5
MASK_DISTANCE = 8.0
HAND_DISP = 1.4663

sys.path.insert(0, str(ROOT / "tools" / "solidworks"))
from swfea import PETG, static
from swkit import expect, job, open_doc, pick


def main():
    result_path = RUN / "results.json"
    all_results = json.loads(result_path.read_text(encoding="utf-8"))
    t4 = next(row for row in all_results if row["task"] == "T4")
    expected = round(39_274 * (2.5 / EL) ** 1.5)
    print(
        f"PREDICT T4 refinement el={EL:.2f} mm, nodes~{expected}, "
        f"displacement~{HAND_DISP:.3f} mm, peak at sharp inside corner",
        flush=True,
    )
    with job(wait_s=1800) as j:
        j.simulation()
        d = open_doc(j.sw, MODEL)
        d.ForceRebuild3(False)
        fixtures = pick(d, kind="cyl", r=2.75)
        bore = pick(d, kind="cyl", r=11)
        edges = []
        from swkit import edges_where
        edges = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01)
        if len(fixtures) != 4 or len(bore) != 1 or len(edges) != 1:
            raise RuntimeError(f"T4 refinement picks: fixture={len(fixtures)}, bore={len(bore)}, root edge={len(edges)}")
        r = static(
            j,
            d,
            "T4_SHARP_1_5",
            PETG,
            fixtures=[("fixed", fixtures)],
            loads=[("remote", bore, (3, 25, 28), (150, 0, 0), (0, 0, 0))],
            el=EL,
            ctrl=[([edges[0]], 1.0), (fixtures, 2.0), (bore, 2.0)],
            max_nodes=min(200_000, expected * 2),
        )
        if r.nodes < expected / 2 or r.nodes > expected * 2:
            raise RuntimeError(f"T4 refinement nodes {r.nodes} outside 0.5x to 2x expected {expected}")
        if r.max_disp() is None or not HAND_DISP / 3 <= r.max_disp() <= HAND_DISP * 3:
            raise RuntimeError(f"T4 refinement displacement {r.max_disp()} mm outside 3x hand estimate")
        expect("T4 refinement reaction Fx N", r.reaction[0], -150.0, 0.01)
        expect("T4 refinement reaction resultant N", r.reaction[3], 150.0, 0.01)
        box = [4.0, 20.0, 5.5, 8.0, 30.0, 15.0]
        corner = r.in_box(box)
        if not corner.any():
            raise RuntimeError("T4 refinement has no nodes in the inside-corner box")
        idxs = np.flatnonzero(corner)
        idx = idxs[int(np.argmax(r.vm[corner]))]
        vm = float(r.vm[idx])
        at = r.pos[idx].round(2).tolist()
        layer, layer_at = r.layer_stress((0, 0, 1), corner)
        shear, shear_at = r.layer_shear((0, 0, 1), corner)
        away = r.away(dist=MASK_DISTANCE)
        away_vm, away_at = r.peak(away)
        away_layer, away_layer_at = r.layer_stress((0, 0, 1), away)
        away_shear, away_shear_at = r.layer_shear((0, 0, 1), away)
        np.savez_compressed(RUN / "t4_finer_nodes.npz", pos=r.pos, stress_mpa=r.s, disp_mm=r.disp)

    rows = list(t4["convergence_rows"])
    rows.append([EL, r.nodes, vm, at, layer, shear])
    local_measures = lambda row: [row[2], row[4], row[5]]
    a, b = local_measures(rows[-1]), local_measures(rows[-2])
    converged = all(abs(x - y) <= 0.05 * abs(y) for x, y in zip(a, b))
    sf_yield = 45.0 / vm
    result = {
        "convergence_rows": rows,
        "converged": bool(converged),
        "reported_stress_mpa": vm,
        "how_judged": (
            f"Local corner von Mises values are {[round(row[2], 2) for row in rows]} MPa at "
            f"{[row[0] for row in rows]} mm; Z-layer tension values are {[round(row[4], 2) for row in rows]} MPa. "
            f"The final step {'meets' if converged else 'does not meet'} 5% convergence for all three measures, "
            f"so the corner is {'reported as converged' if converged else 'not shown; no pass is claimed'}."
        ),
        "verdict": "pass" if converged and sf_yield >= 2 and layer <= 11.25 else "fail",
        "status": "done",
        "notes": (
            f"Finest local peak at {at}; local Z tension={layer:.3f} MPa at {layer_at}, "
            f"Z shear={shear:.3f} MPa at {shear_at}. Away-peak at finest mesh={away_vm:.3f} MPa at {away_at}; "
            f"away Z tension={away_layer:.3f} MPa at {away_layer_at}, away Z shear={away_shear:.3f} MPa at {away_shear_at}. "
            f"Max displacement={r.max_disp():.3f} mm; model SHA-256={hashlib.sha256(MODEL.read_bytes()).hexdigest()}."
        ),
    }
    for row in all_results:
        if row["task"] == "T4":
            row.update(result)
            break
    result_path.write_text(json.dumps(all_results, indent=2) + "\n", encoding="utf-8")
    (RUN / "t4_result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
