"""Idea A: a continuous tapered leaf spine with an open, flush cable channel."""
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
TOOLS = ROOT / "tools" / "solidworks"
WIP = ROOT / "cad" / "_wip" / "sw-eval" / "luna-c"
RUN = ROOT / "tools" / "solidworks" / "playbook" / "eval" / "luna-c"
sys.path.insert(0, str(TOOLS))
from swkit import BLIND, MID, Sk, bbox, bodies, call, edges_where, export, extrude, feature_errors, fillet, job, new_part, pick, plane, save, single_body, volume


def build(j, model):
    d = new_part(j.sw, model)

    # The elbow interface is identical to C1: Ø70 disc, Ø30 bore and six Ø3.4 holes on Ø50 PCD.
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

    # A sampled leaf outline avoids the loft's scale-dependent overshoot. The side view is a broad, rounded taper.
    side = []
    for i in range(81):
        t = i / 80.0
        z = -32.0 - 140.0 * t
        w = 15.0 - 2.0 * math.sin(math.pi * t) + 4.0 * t**4
        side.append((w, 0.0, z))
    outline = side + [(-x, y, z) for x, y, z in reversed(side)]
    with Sk(d, plane(d, "Y", 0.0, "SPINE_MID"), "LEAF_SPINE") as s:
        s.poly(outline)
    extrude(d, s.feat, "LEAF_SPINE", 14.0, mode=MID)
    save(d)

    # Soften the two side-outline edges where the fillet can be picked directly by position.
    spine_edges = edges_where(d, lambda p: min(abs(p[1] - 7.0), abs(p[1] + 7.0)) < 0.03
                              and -171.0 < p[2] < -33.0)
    print("leaf outline edges eligible for softening", len(spine_edges), flush=True)
    if spine_edges:
        rounded = fillet(d, spine_edges, (1.5, 1.0), "LEAF_EDGE_ROUNDS")
        if rounded is not None:
            save(d)

    # An elliptical hub spans Y±22 and overlaps the leaf by 3 mm at the wrist.
    with Sk(d, plane(d, "Z", -175.0, "HUB_MID"), "WRIST_HUB") as s:
        s.poly([(20.0 * math.cos(math.radians(a)), 22.0 * math.sin(math.radians(a)), -175.0)
                for a in range(0, 360, 5)])
    extrude(d, s.feat, "WRIST_HUB", 12.0, mode=MID)
    save(d)

    # The straight Ø6 channel runs down the open centerline and stops before the Ø30 swept wrist cylinder.
    # Its 6 mm wide opening continues through the hub and discharges into the fork slot.
    with Sk(d, plane(d, "Z", -90.5, "CABLE_OPEN_MID"), "CABLE_OPEN") as s:
        s.rect((-3.0, 4.0, -90.5), (3.0, 22.0, -90.5))
    extrude(d, s.feat, "CABLE_OPENING", 181.0, cut=True, mode=MID)
    save(d)
    with Sk(d, plane(d, "Z", -90.5, "CABLE_ROUND_MID"), "CABLE_ROUND") as s:
        s.circle((0.0, 4.0, -90.5), 3.0)
    extrude(d, s.feat, "CABLE_ROUND_GROOVE", 181.0, cut=True, mode=MID)
    save(d)

    # The 72-sided ellipse is a smooth, bounded approximation; the round pin hole is still exact.
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
    return d


def main():
    model = WIP / "idea_a.SLDPRT"
    with job(wait_s=1800) as j:
        subprocess.run([sys.executable, str(ROOT / "tools" / "pc" / "claims.py"), "beat", "sw-eval-luna-c",
                        "--status", "C2 idea A leaf spine", "--sw-pid", str(j.inst.pid)], check=True)
        print("own SolidWorks PID", j.inst.pid, flush=True)
        d = build(j, model)
        data = {"idea": "A: continuous tapered leaf spine", "volume_mm3": volume(d),
                "mass_g": volume(d) * 0.00119, "bodies": len(bodies(d)), "bbox_mm": bbox(d),
                "feature_errors": feature_errors(d)}
        export(j.sw, d, WIP / "idea_a.stl")
        print(json.dumps(data, indent=2), flush=True)


if __name__ == "__main__":
    main()
