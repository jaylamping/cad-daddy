import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / 'cad' / '_wip' / 'sw-eval' / 'luna-b'
sys.path.insert(0, str(ROOT / 'tools' / 'solidworks'))
from swkit import job, open_doc, close, list_faces
with job(wait_s=1800) as j:
    d = open_doc(j.sw, CAD / 'tongue_slot.SLDPRT')
    d.ForceRebuild3(False)
    list_faces(d)
    close(j.sw, d)
