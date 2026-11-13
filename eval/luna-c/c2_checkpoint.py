"""Crude whole-form C2 checkpoint: the complete C1 interface envelope as the initial layout baseline."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
TOOLS = ROOT / "tools" / "solidworks"
WIP = ROOT / "cad" / "_wip" / "sw-eval" / "luna-c"
sys.path.insert(0, str(TOOLS))
from swkit import bbox, bodies, export, feature_errors, job, open_doc, save_as


def main():
    target = WIP / "checkpoint_01.SLDPRT"
    with job(wait_s=1800) as j:
        subprocess.run([sys.executable, str(ROOT / "tools" / "pc" / "claims.py"), "beat", "sw-eval-luna-c",
                        "--status", "C2 checkpoint 01", "--sw-pid", str(j.inst.pid)], check=True)
        print("own SolidWorks PID", j.inst.pid, flush=True)
        d = open_doc(j.sw, WIP / "link_boxy.SLDPRT")
        # Keep the complete interface layout visible before choosing a new spine shape.
        # C1 is the intentionally crude baseline; the organic redesign follows as a separate stage.
        save_as(d, target)
        export(j.sw, d, WIP / "checkpoint_01.stl")
        print({"volume_mm3": sum(b[1] for b in bodies(d)),
               "bbox_mm": bbox(d), "feature_errors": feature_errors(d)}, flush=True)


if __name__ == "__main__":
    main()
