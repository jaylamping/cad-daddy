"""D2: contact-edge peak at the ring's sharp corner on the seat rim (playbook 07-done step 9): the ring gets its real 0.4 mm chamfer on both
OD corners and the twin is rebuilt as pair_fe2.SLDPRT (ring_fe_c)."""
import math, sys
from pathlib import Path
ROOT = Path(r'J:\code\cad-daddy-wt\sw-eval-sonnet-adv-d'); sys.path.insert(0, str(ROOT / 'solidworks'))
from swkit import *
W = ROOT / '_wip' / 'sw-eval' / 'sonnet-adv-d' / 'd2'; RUN = ROOT / 'eval' / 'sonnet-adv-d'
C = 0.4
with job(wait_s=1800) as j:
    stamp(RUN, 'D2 chamfer twin: instance up')
    d = new_part(j.sw, W / 'ring_fe_c.SLDPRT')
    ro, ri, z0, z1 = 25.95, 24.0, 0.15, 7.15
    prof = [(ri, 0, z0), (ro - C, 0, z0), (ro, 0, z0 + C), (ro, 0, z1 - C), (ro - C, 0, z1), (ri, 0, z1)]
    with Sk(d, plane(d, 'Y', 0.0, 'PROF_P'), 'RING') as s:
        s.poly(prof)
        s.centerline((0, 0, 0), (0, 0, 10.0))
    want = math.pi * (ro ** 2 - ri ** 2) * (z1 - z0) - 2 * math.pi * C ** 2 * (ro - C / 3)
    revolve(d, s.feat, 'RING', expect_dv=want)
    save(d); expect('ring_fe_c bodies', len(bodies(d)), 1, 0)
    log('ring_fe_c box', [round(v, 3) for v in bbox(d)]); close(j.sw, d)
    d = open_doc(j.sw, W / 'housing_lower_fe.SLDPRT')
    save_as(d, W / 'pair_fe2.SLDPRT')
    insert_body(d, W / 'housing_upper_fe.SLDPRT'); insert_body(d, W / 'ring_fe_c.SLDPRT')
    for k in range(4): insert_body(d, W / f'pad_{k + 1}.SLDPRT')
    for k in range(4): insert_body(d, W / f'pin_{k + 1}.SLDPRT')
    expect('bodies in pair_fe2', len(bodies(d)), 11, 0)
    expect('rebuild errors', len(feature_errors(d)), 0, 0)
    for b in bodies(d): log('body', b)
    save(d); close(j.sw, d)
    stamp(RUN, 'D2 chamfer twin: done')
print('CHAMFER TWIN DONE')
