"""T1: build, measure, and export the specified bracket in our owned SolidWorks instance."""
import json
import math
import sys
from pathlib import Path

import trimesh

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / "cad" / "_wip" / "sw-eval" / "luna-a"
sys.path.insert(0, str(ROOT / "tools" / "solidworks"))
from swkit import MID, Sk, bbox, bodies, call, close, edges_where, expect, export, extrude, feature_errors, fillet, job, new_part, pick, plane, save, single_body, volume


def main():
    CAD.mkdir(parents=True, exist_ok=True)
    dpath = CAD / "bracket.SLDPRT"
    pi = math.pi
    hand = (
        80 * 50 * 6 + 6 * 50 * 40
        + 50 * 4**2 * (1 - pi / 4)
        - 4 * 6 * 5**2 * (1 - pi / 4)
        - 4 * pi * 2.75**2 * 6
        - pi * 11**2 * 6
        - 4 * pi * 1.7**2 * 6
    )
    with job(wait_s=1800) as j:
        d = new_part(j.sw, dpath)

        # Base and upright: dimensions from TASKS.md, model coordinates in mm.
        with Sk(d, plane(d, "Z", 3.0, "BASE_P"), "BASE") as s:
            s.rect((0, 0, 3), (80, 50, 3))
        extrude(d, s.feat, "BASE", 6, mode=MID, expect_dv=80 * 50 * 6)
        save(d)

        with Sk(d, plane(d, "Z", 26.0, "UPRIGHT_P"), "UPRIGHT") as s:
            s.rect((0, 0, 26), (6, 50, 26))
        extrude(d, s.feat, "UPRIGHT", 40, mode=MID, expect_dv=6 * 50 * 40)
        if len(bodies(d)) != 1:
            raise RuntimeError(f"base/upright did not merge into one body: {bodies(d)}")
        save(d)

        inside_edge = edges_where(d, lambda p: abs(p[0] - 6) < 0.01 and abs(p[2] - 6) < 0.01)
        expect("inside junction edge count", len(inside_edge), 1, 0)
        if fillet(d, inside_edge, (4.0,), "INSIDE_R4") != 4.0:
            raise RuntimeError("the R4 inside-corner fillet did not build")
        save(d)

        with Sk(d, plane(d, "Z", 3.0, "BASE_HOLES_P"), "BASE_HOLES") as s:
            for x, y in ((25, 10), (25, 40), (65, 10), (65, 40)):
                s.circle((x, y, 3), 2.75)
        extrude(d, s.feat, "BASE_HOLES", 6, cut=True, mode=MID, expect_dv=4 * pi * 2.75**2 * 6)
        save(d)

        with Sk(d, plane(d, "X", 3.0, "BORE_P"), "BORE") as s:
            s.circle((3, 25, 28), 11)
        extrude(d, s.feat, "BORE", 6, cut=True, mode=MID, expect_dv=pi * 11**2 * 6)
        save(d)

        bolt_centres = [
            (25 + 15.5 * math.cos(math.radians(a)), 28 + 15.5 * math.sin(math.radians(a)))
            for a in (45, 135, 225, 315)
        ]
        with Sk(d, plane(d, "X", 3.0, "MOTOR_HOLES_P"), "MOTOR_HOLES") as s:
            for y, z in bolt_centres:
                s.circle((3, y, z), 1.7)
        extrude(d, s.feat, "MOTOR_HOLES", 6, cut=True, mode=MID, expect_dv=4 * pi * 1.7**2 * 6)
        save(d)

        base_corners = edges_where(
            d,
            lambda p: abs(p[0] - 80) < 0.01 and (abs(p[1]) < 0.01 or abs(p[1] - 50) < 0.01),
        )
        expect("base outer vertical edges", len(base_corners), 2, 0)
        if fillet(d, base_corners, (5.0,), "BASE_OUTER_R5") != 5.0:
            raise RuntimeError("R5 base corner rounds did not build")
        save(d)

        top_corners = edges_where(
            d,
            lambda p: (abs(p[1]) < 0.01 or abs(p[1] - 50) < 0.01) and abs(p[2] - 46) < 0.01,
        )
        expect("upright top corner edges", len(top_corners), 2, 0)
        if fillet(d, top_corners, (5.0,), "UPRIGHT_TOP_R5") != 5.0:
            raise RuntimeError("R5 upright top corner rounds did not build")
        save(d)

        single_body(d)
        expect("bracket volume mm3", volume(d), hand, 0.001)
        expected_box = (0, 0, 0, 80, 50, 46)
        actual_box = bbox(d)
        for i, want in enumerate(expected_box):
            expect(f"bbox[{i}] mm", actual_box[i], want, 0.01)
        expect("rebuild errors", len(feature_errors(d)), 0, 0)

        # Dimension checks on finished cylindrical faces, inferred from their axis-aligned boxes.
        base_r = pick(d, kind="cyl", r=2.75)
        base_xy = sorted(
            [((call(f, "GetBox")[0] + call(f, "GetBox")[3]) * 500,
              (call(f, "GetBox")[1] + call(f, "GetBox")[4]) * 500) for f in base_r]
        )
        # GetBox values are metres and the factor above converts the average to mm.
        expected_xy = [(25, 10), (25, 40), (65, 10), (65, 40)]
        if len(base_xy) != 4:
            raise RuntimeError(f"expected four base-hole cylinders, got {len(base_xy)}")
        for i, (got, want) in enumerate(zip(base_xy, expected_xy)):
            expect(f"base hole {i} center x", got[0], want[0], 0.03)
            expect(f"base hole {i} center y", got[1], want[1], 0.03)

        bore_faces = pick(d, kind="cyl", r=11)
        if len(bore_faces) != 1:
            raise RuntimeError(f"expected one bore face, got {len(bore_faces)}")
        bb = call(bore_faces[0], "GetBox")
        expect("bore center y", (bb[1] + bb[4]) * 500, 25, 0.03)
        expect("bore center z", (bb[2] + bb[5]) * 500, 28, 0.03)
        motor_faces = pick(d, kind="cyl", r=1.7)
        if len(motor_faces) != 4:
            raise RuntimeError(f"expected four motor-hole cylinders, got {len(motor_faces)}")
        motor_yz = sorted([
            ((call(f, "GetBox")[1] + call(f, "GetBox")[4]) * 500,
             (call(f, "GetBox")[2] + call(f, "GetBox")[5]) * 500) for f in motor_faces
        ])
        for got, want in zip(motor_yz, sorted(bolt_centres)):
            expect("motor hole center y", got[0], want[0], 0.03)
            expect("motor hole center z", got[1], want[1], 0.03)
        save(d)
        native_volume = volume(d)
        export(j.sw, d, CAD / "bracket.step")
        export(j.sw, d, CAD / "bracket.stl")
        close(j.sw, d)

    mesh = trimesh.load(CAD / "bracket.stl", force="mesh")
    if not mesh.is_watertight or len(mesh.split(only_watertight=False)) != 1:
        raise RuntimeError(f"STL is not one watertight shell: watertight={mesh.is_watertight}, parts={len(mesh.split())}")
    expect("STL volume mm3", float(mesh.volume), hand, 0.005)
    step = (CAD / "bracket.step").read_text(encoding="utf-8", errors="ignore")
    if ".MILLI." not in step:
        raise RuntimeError("STEP file has no .MILLI. SI length unit")
    result = {
        "volume_mm3": native_volume,
        "hand_volume_mm3": hand,
        "mass_g": hand * 1.19 / 1000,
        "bbox_mm": [round(float(x), 3) for x in mesh.bounds.reshape(-1)],
        "bodies": 1,
        "stl_watertight": bool(mesh.is_watertight),
        "stl_volume_mm3": float(mesh.volume),
    }
    (RUN / "t1_result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
if __name__ == "__main__":
    main()
