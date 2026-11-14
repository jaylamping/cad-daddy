"""T2: open the saved T1 native part, then add four counterbores and one rounded slot."""
import json
import math
import sys
from pathlib import Path

import trimesh

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / "cad" / "_wip" / "sw-eval" / "luna-a"
sys.path.insert(0, str(ROOT / "tools" / "solidworks"))
from swkit import MID, Sk, bbox, bodies, call, close, expect, export, extrude, feature_errors, job, open_doc, plane, save, save_as, single_body, volume


def main():
    source = CAD / "bracket.SLDPRT"
    target = CAD / "bracket_b.SLDPRT"
    target.unlink(missing_ok=True)
    hand_t1 = (
        36000 + 50 * 4**2 * (1 - math.pi / 4)
        - 4 * 6 * 5**2 * (1 - math.pi / 4)
        - 4 * math.pi * 2.75**2 * 6
        - math.pi * 11**2 * 6
        - 4 * math.pi * 1.7**2 * 6
    )
    cb_cut = 4 * math.pi * (5**2 - 2.75**2) * 3
    slot_area = (20 - 6) * 6 + math.pi * 3**2
    slot_cut = slot_area * 6
    hand_t2 = hand_t1 - cb_cut - slot_cut

    with job(wait_s=1800) as j:
        d = open_doc(j.sw, source)
        expect("opened T1 bracket native volume", volume(d), hand_t1, 0.001)
        expect("opened T1 one-body count", len(bodies(d)), 1, 0)
        expect("opened T1 feature errors", len(feature_errors(d)), 0, 0)
        save_as(d, target)

        with Sk(d, plane(d, "Z", 4.5, "COUNTERBORES_P"), "COUNTERBORES") as s:
            for x, y in ((25, 10), (25, 40), (65, 10), (65, 40)):
                s.circle((x, y, 4.5), 5.0)
        extrude(d, s.feat, "COUNTERBORES", 3.0, cut=True, mode=MID, expect_dv=cb_cut)
        save(d)

        # A single closed capsule: straight sections are 14 mm, end radii are 3 mm.
        with Sk(d, plane(d, "Z", 3.0, "SLOT_P"), "SLOT") as s:
            s.poly([(38, 22, 3), (52, 22, 3)], closed=False)
            s.arc((52, 25, 3), (52, 22, 3), (52, 28, 3), +1)
            s.poly([(52, 28, 3), (38, 28, 3)], closed=False)
            s.arc((38, 25, 3), (38, 28, 3), (38, 22, 3), +1)
        extrude(d, s.feat, "SLOT", 6.0, cut=True, mode=MID, expect_dv=slot_cut)
        save(d)

        single_body(d)
        expect("T2 volume mm3", volume(d), hand_t2, 0.001)
        expect("T2 feature errors", len(feature_errors(d)), 0, 0)
        expected_box = (0, 0, 0, 80, 50, 46)
        for i, want in enumerate(expected_box):
            expect(f"T2 bbox[{i}] mm", bbox(d)[i], want, 0.01)

        counterbore_faces = []
        for x, y in ((25, 10), (25, 40), (65, 10), (65, 40)):
            fs = [f for f in j_faces(d) if is_cylinder(f, 5.0, box=(x, y))]
            if len(fs) != 1:
                raise RuntimeError(f"expected one Ø10 counterbore wall at {(x, y)}, got {len(fs)}")
            counterbore_faces.extend(fs)
            floors = [f for f in j_faces(d) if on_floor(f, x + 4.0, y, 3.0)]
            if not floors:
                raise RuntimeError(f"counterbore floor at {(x, y)} was not measured")
            zlo = min(call(f, "GetBox")[2] for f in floors) * 1000
            zhi = max(call(f, "GetBox")[5] for f in floors) * 1000
            expect(f"counterbore floor z at {(x, y)} mm", (zlo + zhi) / 2, 3.0, 0.03)
        if len(counterbore_faces) != 4:
            raise RuntimeError(f"expected four counterbore walls, got {len(counterbore_faces)}")

        slot_faces = [f for f in j_faces(d) if is_cylinder(f, 3.0, box=None)]
        # Exclude the original radius-2.75 and radius-1.7 holes by exact radius; this selection is the two slot ends.
        slot_faces = [f for f in slot_faces if slot_box(f)]
        if len(slot_faces) != 2:
            raise RuntimeError(f"expected two rounded slot end faces, got {len(slot_faces)}")
        slot_boxes = sorted([[v * 1000 for v in call(f, "GetBox")] for f in slot_faces], key=lambda b: b[0])
        expect("slot total length mm", slot_boxes[1][3] - slot_boxes[0][0], 20.0, 0.03)
        expect("slot width mm", slot_boxes[0][4] - slot_boxes[0][1], 6.0, 0.03)
        expect("slot through thickness mm", max(b[5] for b in slot_boxes) - min(b[2] for b in slot_boxes), 6.0, 0.03)

        save(d)
        export(j.sw, d, CAD / "bracket_b.stl")
        native_volume = volume(d)
        close(j.sw, d)

    mesh = trimesh.load(CAD / "bracket_b.stl", force="mesh")
    if not mesh.is_watertight or len(mesh.split(only_watertight=False)) != 1:
        raise RuntimeError("T2 STL is not one watertight shell")
    expect("T2 STL volume mm3", float(mesh.volume), hand_t2, 0.005)
    result = {
        "volume_mm3": native_volume,
        "hand_volume_mm3": hand_t2,
        "counterbore_floor_z_mm": 3.0,
        "bodies": 1,
        "stl_watertight": bool(mesh.is_watertight),
        "stl_volume_mm3": float(mesh.volume),
    }
    (RUN / "t2_result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)


def j_faces(d):
    return [f for b in (d.GetBodies2(0, True) or []) for f in (call(b, "GetFaces") or [])]


def is_cylinder(f, radius, box=None):
    s = f.GetSurface
    if not s.IsCylinder or abs(s.CylinderParams[6] * 1000 - radius) > 0.02:
        return False
    b = [min(call(f, "GetBox")[i], call(f, "GetBox")[i + 3]) * 1000 for i in range(3)]
    q = [max(call(f, "GetBox")[i], call(f, "GetBox")[i + 3]) * 1000 for i in range(3)]
    if radius == 3.0:
        return True
    return box is None or (abs((b[0] + q[0]) / 2 - box[0]) < 0.05 and abs((b[1] + q[1]) / 2 - box[1]) < 0.05)


def slot_box(f):
    b = [min(call(f, "GetBox")[i], call(f, "GetBox")[i + 3]) * 1000 for i in range(3)]
    q = [max(call(f, "GetBox")[i], call(f, "GetBox")[i + 3]) * 1000 for i in range(3)]
    return b[0] >= 34.9 and q[0] <= 55.1 and b[1] >= 21.9 and q[1] <= 28.1 and b[2] >= -0.1 and q[2] <= 6.1


def on_floor(f, x, y, z):
    if not f.GetSurface.IsPlane:
        return False
    n = list(f.Normal)
    if abs(n[2]) < 0.99:
        return False
    b = call(f, "GetBox")
    if abs((b[2] + b[5]) * 500 - z) > 0.03:
        return False
    q = f.GetClosestPointOn(x / 1000, y / 1000, z / 1000)
    return q is not None and math.dist([v * 1000 for v in list(q)[:3]], [x, y, z]) < 0.05


if __name__ == "__main__":
    main()
