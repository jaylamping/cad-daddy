"""Idea B: two smooth load-bearing rails with an exposed cable passage between them."""
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
TOOLS = ROOT / "tools" / "solidworks"
WIP = ROOT / "cad" / "_wip" / "sw-eval" / "luna-c"
sys.path.insert(0, str(TOOLS))
from swkit import BLIND, MID, Sk, bbox, bodies, export, extrude, feature_errors, job, new_part, plane, save, single_body, volume


def main():
    model = WIP / "idea_b.SLDPRT"
    with job(wait_s=1800) as j:
        subprocess.run([sys.executable, str(ROOT / "tools" / "pc" / "claims.py"), "beat", "sw-eval-luna-c",
                        "--status", "C2 idea B twin rails", "--sw-pid", str(j.inst.pid)], check=True)
        print("own SolidWorks PID", j.inst.pid, flush=True)
        d = new_part(j.sw, model)

        with Sk(d, plane(d, "Y", 0.0, "ELBOW_MID"), "ELBOW_DISC") as s:
            s.circle((0, 0, 0), 35.0)
        extrude(d, s.feat, "ELBOW_DISC", 8.0, mode=MID, expect_dv=math.pi * 35**2 * 8)
        save(d)
        with Sk(d, plane(d, "Y", 0.0, "BORE_MID"), "BORE") as s:
            s.circle((0, 0, 0), 15.0)
        extrude(d, s.feat, "LOCATING_BORE", 8.0, cut=True, mode=MID, expect_dv=math.pi * 15**2 * 8)
        save(d)
        with Sk(d, plane(d, "Y", 0.0, "BOLT_MID"), "BOLTS") as s:
            for k in range(6):
                a = math.radians(60 * k)
                s.circle((25 * math.cos(a), 0, 25 * math.sin(a)), 1.7)
        extrude(d, s.feat, "BOLT_HOLES", 8.0, cut=True, mode=MID, expect_dv=6 * math.pi * 1.7**2 * 8)
        save(d)

        # Two round rails stand 23 mm apart, leaving a 7 mm open lane for the cable.
        for label, x in (("RAIL_POS", 11.5), ("RAIL_NEG", -11.5)):
            with Sk(d, plane(d, "Z", -101.0, label + "_MID"), label) as s:
                s.circle((x, 0.0, -101.0), 8.0)
            extrude(d, s.feat, label, 139.0, mode=MID)
            save(d)

        with Sk(d, plane(d, "Z", -175.0, "HUB_MID"), "WRIST_HUB") as s:
            s.poly([(20.0 * math.cos(math.radians(a)), 22.0 * math.sin(math.radians(a)), -175.0)
                    for a in range(0, 360, 5)])
        extrude(d, s.feat, "WRIST_HUB", 12.0, mode=MID)
        save(d)

        # The channel exits from the elbow bore, runs between the rails and opens through the hub into the fork.
        with Sk(d, plane(d, "Z", -90.5, "CABLE_OPEN_MID"), "CABLE_OPEN") as s:
            s.rect((-3.0, 4.0, -90.5), (3.0, 22.0, -90.5))
        extrude(d, s.feat, "CABLE_OPENING", 181.0, cut=True, mode=MID)
        save(d)
        with Sk(d, plane(d, "Z", -90.5, "CABLE_ROUND_MID"), "CABLE_ROUND") as s:
            s.circle((0.0, 4.0, -90.5), 3.0)
        extrude(d, s.feat, "CABLE_ROUND_GROOVE", 181.0, cut=True, mode=MID)
        save(d)

        for label, y0, sign in (("CHEEK_POS", 16.0, 1), ("CHEEK_NEG", -16.0, -1)):
            with Sk(d, plane(d, "Y", y0, label + "_P"), label) as s:
                s.poly([(18.0 * math.cos(math.radians(a)), y0,
                         -195.0 + 20.0 * math.sin(math.radians(a))) for a in range(0, 360, 5)])
            extrude(d, s.feat, label, 6.0, mode=BLIND, want=(1, sign, y0))
            save(d)
        with Sk(d, plane(d, "Y", 0.0, "PIN_MID"), "PIN_HOLE") as s:
            s.circle((0.0, 0.0, -200.0), 4.0)
        extrude(d, s.feat, "WRIST_PIN_HOLE", 50.0, cut=True, mode=MID)
        save(d)
        single_body(d)
        errs = feature_errors(d)
        if errs:
            raise RuntimeError(f"feature errors: {errs}")
        data = {"idea": "B: paired round rails with exposed central cable lane", "volume_mm3": volume(d),
                "mass_g": volume(d) * 0.00119, "bodies": len(bodies(d)), "bbox_mm": bbox(d),
                "feature_errors": errs}
        export(j.sw, d, WIP / "idea_b.stl")
        print(json.dumps(data, indent=2), flush=True)


if __name__ == "__main__":
    main()
