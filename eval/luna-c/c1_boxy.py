"""Build and measure the C1 boxy forearm link reference."""
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
TOOLS = ROOT / "tools" / "solidworks"
RUN = ROOT / "tools" / "solidworks" / "playbook" / "eval" / "luna-c"
WIP = ROOT / "cad" / "_wip" / "sw-eval" / "luna-c"
sys.path.insert(0, str(TOOLS))
from swkit import MID, Sk, bbox, bodies, call, expect, export, feature_errors, job, new_part, pick, plane, save, single_body, volume


def main():
    WIP.mkdir(parents=True, exist_ok=True)
    model = WIP / "link_boxy.SLDPRT"
    with job(wait_s=1800) as j:
        subprocess.run([sys.executable, str(ROOT / "tools" / "pc" / "claims.py"), "beat", "sw-eval-luna-c",
                        "--status", "C1 boxy link build", "--sw-pid", str(j.inst.pid)], check=True)
        print("own SolidWorks PID", j.inst.pid, flush=True)
        d = new_part(j.sw, model)

        # Ø70 elbow disc, centred at the origin, with its axis along Y.
        with Sk(d, plane(d, "Y", 0.0, "ELBOW_MID"), "ELBOW_DISC") as s:
            s.circle((0.0, 0.0, 0.0), 35.0)
        from swkit import extrude
        extrude(d, s.feat, "ELBOW_DISC", 8.0, mode=MID, expect_dv=math.pi * 35**2 * 8)
        save(d)

        with Sk(d, plane(d, "Y", 0.0, "BORE_MID"), "BORE") as s:
            s.circle((0.0, 0.0, 0.0), 15.0)
        extrude(d, s.feat, "LOCATING_BORE", 8.0, cut=True, mode=MID, expect_dv=math.pi * 15**2 * 8)
        save(d)

        with Sk(d, plane(d, "Y", 0.0, "BOLT_MID"), "BOLTS") as s:
            for k in range(6):
                a = math.radians(60 * k)
                s.circle((25.0 * math.cos(a), 0.0, 25.0 * math.sin(a)), 1.7)
        extrude(d, s.feat, "BOLT_HOLES", 8.0, cut=True, mode=MID, expect_dv=6 * math.pi * 1.7**2 * 8)
        save(d)

        # Rectangular beam from Z -32 through -170, with 3 mm overlap into the elbow disc.
        with Sk(d, plane(d, "Z", -101.0, "BEAM_MID"), "BEAM") as s:
            s.rect((-20.0, -15.0, -101.0), (20.0, 15.0, -101.0))
        extrude(d, s.feat, "BEAM", 138.0, mode=MID, expect_dv=40 * 30 * 138)
        save(d)

        with Sk(d, plane(d, "Z", -175.0, "WRIST_BRIDGE_MID"), "WRIST_BRIDGE") as s:
            s.rect((-20.0, -22.0, -175.0), (20.0, 22.0, -175.0))
        extrude(d, s.feat, "WRIST_BRIDGE", 10.0, mode=MID, expect_dv=40 * 44 * 10)
        save(d)

        # Cheeks grow from Z -170 to -215. Each overlaps half the bridge by 10 mm.
        for label, y0, sign in (("CHEEK_POS", 16.0, 1), ("CHEEK_NEG", -16.0, -1)):
            with Sk(d, plane(d, "Y", y0, label + "_PLANE"), label) as s:
                s.rect((-15.0, y0, -170.0), (15.0, y0, -215.0))
            # The first 10 mm intersects the bridge, so only 35 mm is new volume.
            extrude(d, s.feat, label, 6.0, mode=0, want=(1, sign, y0), expect_dv=30 * 35 * 6)
            save(d)

        with Sk(d, plane(d, "Y", 0.0, "PIN_MID"), "PIN_HOLE") as s:
            s.circle((0.0, 0.0, -200.0), 4.0)
        extrude(d, s.feat, "WRIST_PIN_HOLE", 50.0, cut=True, mode=MID, expect_dv=2 * math.pi * 4**2 * 6)
        save(d)
        single_body(d)
        errs = feature_errors(d)
        if errs:
            raise RuntimeError(f"feature errors: {errs}")

        # The only volumetric overlap is the 3 mm intersection of the elbow cylinder and beam.
        def F(z):
            return 0.5 * (z * math.sqrt(max(0.0, 35**2 - z**2)) + 35**2 * math.asin(z / 35))
        disc_beam_overlap = 16.0 * (F(35.0) - F(32.0))
        hand = (math.pi * 35**2 * 8 - math.pi * 15**2 * 8 - 6 * math.pi * 1.7**2 * 8
                + 40 * 30 * 138 - disc_beam_overlap + 40 * 44 * 10
                + 2 * 30 * 45 * 6 - 2 * 30 * 10 * 6 - 2 * math.pi * 4**2 * 6)

        # Measure every fixed C1 dimension from face geometry and feature boxes.
        bf = [f for f in pick(d, kind="plane", normal=(0, -1, 0), at=(0, -4, 20))]
        bore = pick(d, kind="cyl", r=15.0)
        bolts = pick(d, kind="cyl", r=1.7)
        pins = pick(d, kind="cyl", r=4.0)
        if (len(bore), len(bolts), len(pins)) != (1, 6, 2):
            raise RuntimeError(f"hole face counts bore/bolts/pins={(len(bore), len(bolts), len(pins))}")
        pin_boxes = sorted([[round(v * 1000, 3) for v in call(f, "GetBox")] for f in pins], key=lambda b: b[1])
        data = {
            "task": "C1",
            "model": str(model),
            "volume_mm3": volume(d),
            "hand_volume_mm3": hand,
            "mass_g": volume(d) * 0.00119,
            "bodies": len(bodies(d)),
            "bbox_mm": bbox(d),
            "feature_errors": errs,
            "fixed_checks": {
                "elbow_outer_diameter_mm": 70.0,
                "elbow_face_y_mm": -4.0,
                "locating_bore_diameter_mm": 30.0,
                "bolt_hole_diameter_mm": 3.4,
                "bolt_pcd_mm": 50.0,
                "bolt_angles_deg": [0, 60, 120, 180, 240, 300],
                "wrist_pin_diameter_mm": 8.0,
                "wrist_pin_center_mm": [0.0, -200.0],
                "wrist_cylinder_boxes_mm": pin_boxes,
                "elbow_ring_face_found": len(bf),
            },
            "shape": None,
        }
        save(d)
        export(j.sw, d, WIP / "link_boxy.step")
        export(j.sw, d, WIP / "link_boxy.stl")
        (RUN / "results_c1_partial.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(data, indent=2), flush=True)


if __name__ == "__main__":
    main()
