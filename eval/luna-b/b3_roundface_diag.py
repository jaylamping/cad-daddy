import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
CAD = ROOT / 'cad' / '_wip' / 'sw-eval' / 'luna-b'
sys.path.insert(0, str(ROOT / 'tools' / 'solidworks'))
from swkit import job, open_doc, close, pick, face_info
with job(wait_s=1800) as j:
    d = open_doc(j.sw, CAD / 'wall_bracket_light_t3p0_h12p0_r0p4.SLDPRT')
    for f in pick(d, kind='plane', normal=(0, 0, 1), at=(60, 20, 52)):
        print(face_info(f), flush=True)
    close(j.sw, d)
