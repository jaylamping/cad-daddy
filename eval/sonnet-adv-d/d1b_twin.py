"""D1: the FEA twin with a 120 x 20 x 6 mm aluminium rail slab (the full rail meshed at 1.5 mm would pass 200,000 nodes)."""
import sys, hashlib
from pathlib import Path
ROOT = Path(r'J:\code\cad-daddy-wt\sw-eval-sonnet-adv-d'); sys.path.insert(0, str(ROOT / 'solidworks'))
from swkit import *
W = ROOT / '_wip' / 'sw-eval' / 'sonnet-adv-d' / 'd1b'
with job(wait_s=1800) as j:
    dr = new_part(j.sw, W / 'rail_slab.SLDPRT')
    with Sk(dr, plane(dr, 'Z', -3.0, 'RS_P'), 'RAILS') as s:
        s.rect((-60, -10, -3.0), (60, 10, -3.0))
    extrude(dr, s.feat, 'RAILS', 6.0, mode=MID, expect_dv=120 * 20 * 6)
    save(dr); close(j.sw, dr)
    sha0 = hashlib.sha256(open(W / 'buck_mount.SLDPRT', 'rb').read()).hexdigest()
    d = open_doc(j.sw, W / 'buck_mount.SLDPRT')
    save_as(d, W / 'buck_mount_fea2.SLDPRT')
    insert_body(d, W / 'rail_slab.SLDPRT')
    expect('bodies', len(bodies(d)), 2, 0); log(bodies(d)); save(d); close(j.sw, d)
    log('original SHA before', sha0, 'after', hashlib.sha256(open(W / 'buck_mount.SLDPRT', 'rb').read()).hexdigest())
print('TWIN DONE')
