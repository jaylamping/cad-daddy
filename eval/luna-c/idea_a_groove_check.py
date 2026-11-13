"""Export the saved pre-opening-groove intermediate after a failed open-channel cut."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
TOOLS = ROOT / "tools" / "solidworks"
WIP = ROOT / "cad" / "_wip" / "sw-eval" / "luna-c"
sys.path.insert(0, str(TOOLS))
from swkit import bbox, export, job, open_doc, volume


with job(wait_s=1800) as j:
    subprocess.run([sys.executable, str(ROOT / "tools" / "pc" / "claims.py"), "beat", "sw-eval-luna-c",
                    "--status", "C2 idea A channel review", "--sw-pid", str(j.inst.pid)], check=True)
    d = open_doc(j.sw, WIP / "idea_a.SLDPRT")
    print({"volume_mm3": volume(d), "bbox_mm": bbox(d)}, flush=True)
    export(j.sw, d, WIP / "idea_a_groove_partial.stl")
