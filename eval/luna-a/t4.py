"""T4: build the sharp-corner variant and run the T3 load case."""
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / "cad" / "_wip" / "sw-eval" / "luna-a"
MODEL = CAD / "bracket_sharp.SLDPRT"
sys.path.insert(0, str(ROOT / "tools" / "solidworks"))
from swfea import PETG, converge, static
from swkit import MID, Sk, bodies, close, edges_where, expect, export, extrude, feature_errors, fillet, job, new_part, open_doc, pick, plane, save, single_body, volume


HAND_VOLUME = (
    36000
    - 4 * 6 * 5**2 * (1 - math.pi / 4)
    - 4 * math.pi * 2.75**2 * 6
    - math.pi * 11**2 * 6
    - 4 * math.pi * 1.7**2 * 6
)
HAND_DISP = 150 * 22**3 / (3 * 1900 * (50 * 6**3 / 12))
M = 150 * 22
BI = 50 * 6**3 / 12
L = 25 - 6
HAND_DISP += M * L**2 / (2 * 1900 * BI) + (M * L / (1900 * BI)) * 22
SIZES = (4.0, 3.0, 2.5)
MASK_DISTANCE = 2 * max(SIZES)


def write_result(result):
    path = RUN / "results.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    for item in rows:
        if item["task"] == "T4":
            item.update(result)
            break
    path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    (RUN / "t4_result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def main():
    CAD.mkdir(parents=True, exist_ok=True)
    with job(wait_s=1800) as j:
        d = new_part(j.sw, MODEL)
        with Sk(d, plane(d, "Z", 3, "BASE_P"), "BASE") as s:
            s.rect((0, 0, 3), (80, 50, 3))
        extrude(d, s.feat, "BASE", 6, mode=MID, expect_dv=24000)
        save(d)
        with Sk(d, plane(d, "Z", 26, "UPRIGHT_P"), "UPRIGHT") as s:
            s.rect((0, 0, 26), (6, 50, 26))
        extrude(d, s.feat, "UPRIGHT", 40, mode=MID, expect_dv=12000)
        if len(bodies(d)) != 1:
            raise RuntimeError(f"base/upright did not merge: {bodies(d)}")
        save(d)
        # T4 intentionally has no inside R4 fillet.
        with Sk(d, plane(d, "Z", 3, "BASE_HOLES_P"), "BASE_HOLES") as s:
            for x, y in ((25, 10), (25, 40), (65, 10), (65, 40)):
                s.circle((x, y, 3), 2.75)
        extrude(d, s.feat, "BASE_HOLES", 6, cut=True, mode=MID, expect_dv=4 * math.pi * 2.75**2 * 6)
        save(d)
        with Sk(d, plane(d, "X", 3, "BORE_P"), "BORE") as s:
            s.circle((3, 25, 28), 11)
        extrude(d, s.feat, "BORE", 6, cut=True, mode=MID, expect_dv=math.pi * 11**2 * 6)
        save(d)
        bolt_centres = [
            (25 + 15.5 * math.cos(math.radians(a)), 28 + 15.5 * math.sin(math.radians(a)))
            for a in (45, 135, 225, 315)
        ]
        with Sk(d, plane(d, "X", 3, "MOTOR_HOLES_P"), "MOTOR_HOLES") as s:
            for y, z in bolt_centres:
                s.circle((3, y, z), 1.7)
        extrude(d, s.feat, "MOTOR_HOLES", 6, cut=True, mode=MID, expect_dv=4 * math.pi * 1.7**2 * 6)
        save(d)
        base_corners = edges_where(
            d,
            lambda p: abs(p[0] - 80) < 0.01 and (abs(p[1]) < 0.01 or abs(p[1] - 50) < 0.01),
        )
        if fillet(d, base_corners, (5,), "BASE_OUTER_R5") != 5.0:
            raise RuntimeError("base R5 corner rounds failed")
        save(d)
        top_corners = edges_where(
            d,
            lambda p: (abs(p[1]) < 0.01 or abs(p[1] - 50) < 0.01) and abs(p[2] - 46) < 0.01,
        )
        if fillet(d, top_corners, (5,), "UPRIGHT_TOP_R5") != 5.0:
            raise RuntimeError("upright R5 corner rounds failed")
        single_body(d)
        expect("sharp bracket volume mm3", volume(d), HAND_VOLUME, 0.001)
        expect("sharp bracket feature errors", len(feature_errors(d)), 0, 0)
        expect("sharp bracket base hole count", len(pick(d, kind="cyl", r=2.75)), 4, 0)
        expect("sharp bracket bore count", len(pick(d, kind="cyl", r=11)), 1, 0)
        expect("sharp bracket motor hole count", len(pick(d, kind="cyl", r=1.7)), 4, 0)
        save(d)
        export(j.sw, d, CAD / "bracket_sharp.stl")
        close(j.sw, d)

        j.simulation()
        d = open_doc(j.sw, MODEL)
        d.ForceRebuild3(False)

        def run(el):
            expected = round(24_000 * (4.0 / el) ** 1.5)
            print(
                f"PREDICT T4 el={el:.2f} mm, nodes~{expected}, displacement~{HAND_DISP:.3f} mm, "
                "peak at the sharp inside junction along Y",
                flush=True,
            )
            d.ForceRebuild3(False)
            fixtures = pick(d, kind="cyl", r=2.75)
            bore = pick(d, kind="cyl", r=11)
            root_edges = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01)
            if len(fixtures) != 4 or len(bore) != 1 or len(root_edges) != 1:
                raise RuntimeError(
                    f"T4 pick counts: screw walls={len(fixtures)}, bore={len(bore)}, root edges={len(root_edges)}"
                )
            r = static(
                j,
                d,
                f"T4_SHARP_{el:g}",
                PETG,
                fixtures=[("fixed", fixtures)],
                loads=[("remote", bore, (3, 25, 28), (150, 0, 0), (0, 0, 0))],
                el=el,
                ctrl=[([root_edges[0]], 1.0), (fixtures, 2.0), (bore, 2.0)],
                max_nodes=min(200_000, expected * 2),
            )
            if r.nodes < expected / 2 or r.nodes > expected * 2:
                raise RuntimeError(f"T4 nodes {r.nodes} is outside 0.5x to 2x prediction {expected}")
            if r.max_disp() is None or not HAND_DISP / 3 <= r.max_disp() <= HAND_DISP * 3:
                raise RuntimeError(f"T4 max displacement {r.max_disp()} mm is outside 3x hand estimate {HAND_DISP:.3f}")
            expect(f"{r.name} reaction Fx N", r.reaction[0], -150.0, 0.01)
            expect(f"{r.name} reaction resultant N", r.reaction[3], 150.0, 0.01)
            corner_mask = r.in_box([4.0, 20.0, 5.5, 8.0, 30.0, 15.0])
            if not corner_mask.any():
                raise RuntimeError("no nodes in the inside-corner measurement box")
            ids = np.flatnonzero(corner_mask)
            idx = ids[int(np.argmax(r.vm[corner_mask]))]
            corner_vm = float(r.vm[idx])
            corner_at = r.pos[idx].round(2).tolist()
            corner_layer, _ = r.layer_stress((0, 0, 1), corner_mask)
            corner_shear, _ = r.layer_shear((0, 0, 1), corner_mask)
            run.corner_rows.append([el, r.nodes, corner_vm, corner_at, corner_layer, corner_shear])
            run.last_result = r
            return r

        run.last_result = None
        run.corner_rows = []
        rows, converged = converge(run, SIZES, tol=0.05, layers=(0, 0, 1))
        fine = run.last_result
        if fine is None:
            raise RuntimeError("no final sharp-corner result")
        corner_rows = run.corner_rows
        corner_vm, corner_at = corner_rows[-1][2], corner_rows[-1][3]
        corner_converged = all(
            abs(a - b) <= 0.05 * abs(b)
            for a, b in zip(corner_rows[-1][2:3] + corner_rows[-1][4:6],
                            corner_rows[-2][2:3] + corner_rows[-2][4:6])
        )
        np.savez_compressed(RUN / "t4_fine_nodes.npz", pos=fine.pos, stress_mpa=fine.s, disp_mm=fine.disp)

    sf_yield = 45.0 / corner_vm if corner_vm > 0 else None
    layer, layer_at = fine.layer_stress((0, 0, 1), fine.away(dist=MASK_DISTANCE))
    shear, shear_at = fine.layer_shear((0, 0, 1), fine.away(dist=MASK_DISTANCE))
    how = (
        f"The sharp-corner box reaches {corner_vm:.2f} MPa at {corner_at} on el={SIZES[-1]:g} mm; "
        f"the local series is {corner_rows}. It is judged as a corner singularity if the series climbs; "
        "the finest local value is not a converged material stress."
    )
    result = {
        "convergence_rows": corner_rows,
        "converged": bool(corner_converged),
        "reported_stress_mpa": corner_vm,
        "how_judged": how,
        "verdict": "pass" if corner_converged and sf_yield >= 2.0 and layer <= 11.25 else "fail",
        "status": "done" if rows else "partial",
        "notes": (
            f"Inside-corner box peak at {corner_at}; Z-layer tension={layer:.3f} MPa at {layer_at}, "
            f"Z-layer shear={shear:.3f} MPa at {shear_at}; von Mises factor based on local corner value={sf_yield:.3f}. "
            f"Helper away-peak rows: {rows}; local corner convergence flag={corner_converged}. "
            f"Hand displacement estimate={HAND_DISP:.3f} mm; maximum displacement={fine.max_disp():.3f} mm."
        ),
    }
    write_result(result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
