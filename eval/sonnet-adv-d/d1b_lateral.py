"""D1 lateral study (9 N along Y and along X through the four insert holes, bearing loads) -- was: 9 N (10 g of the 90 g board) on the mount. Series DOWN at three mesh sizes (support: base bottom on the rail),
and the same load with the M5 hole walls fixed instead (second support). Four studies, one job."""
import json, math, sys
from pathlib import Path
import numpy as np
ROOT = Path(r'J:\code\cad-daddy-wt\sw-eval-sonnet-adv-d')
sys.path.insert(0, str(ROOT / 'solidworks'))
from swkit import *
from swfea import PETG, static, judge
ALU = dict(name='Aluminium 6063', EX=6.9e10, NUXY=0.33, DENS=2700.0, SIGYLD=170e6, SIGXT=200e6)
W = ROOT / '_wip' / 'sw-eval' / 'sonnet-adv-d' / 'd1b'
RUN = ROOT / 'eval' / 'sonnet-adv-d'
PADS = [(sx * 39.0, sy * 26.5) for sx in (1, -1) for sy in (1, -1)]
ZT = 11.5
out = {}
def both_signs(r, normal, mask):
    """layer tension and shear for the load as applied and reversed (a linear study: the reverse is the negated stress)."""
    n = np.array(normal, float); n /= np.linalg.norm(n); S = r.s
    sn = n[0]**2*S[:,1]+n[1]**2*S[:,2]+n[2]**2*S[:,3]+2*(n[0]*n[1]*S[:,4]+n[0]*n[2]*S[:,5]+n[1]*n[2]*S[:,6])
    return float(sn[mask].max()), float((-sn[mask]).max())
with job(wait_s=1800) as j:
    stamp(RUN, 'D1 fea job: instance up')
    j.simulation()
    d = open_doc(j.sw, W / 'buck_mount_fea2.SLDPRT')
    d.ForceRebuild3(False)
    base = pick(d, kind='plane', normal=(0, 0, -1), at=(0, 0, -6))      # the rail's bottom face: the rail is held, the mount sits on it
    m5 = pick(d, kind='cyl', r=2.75)
    tops = [f for (x, y) in PADS for f in pick(d, kind='plane', normal=(0, 0, 1), at=(x + 2.75, y, ZT))]
    expect('rail bottom faces', len(base), 1, 0); expect('M5 faces', len(m5), 2, 0); expect('pad tops', len(tops), 4, 0)
    vol = volume(d) - 120 * 20 * 6
    def mount_mask(r):
        # nodes of the printed body: above the rail top, or beyond the rail's side faces; the shared plane Z 0 under the rail is left out
        y, z = r.pos[:, 1], r.pos[:, 2]
        return (z > 0.01) | ((np.abs(y) > 10.3) & (z > -0.01))
    def edge_far(r, dist):
        # the rail's top edges (Y +-10, Z 0) are line supports in the model: leave out nodes within dist of them (a contact-edge singularity)
        return np.hypot(np.abs(r.pos[:, 1]) - 10.0, r.pos[:, 2]) >= dist
    rows = []
    def run(el, tag, fix):
        pred_nodes = 12 * vol / el ** 3 * 1.5
        log(f'PREDICT {tag}: nodes about {pred_nodes:.0f}, displacement about 0.01 mm, peak at the bridge root beside the base edge, about 0.6 MPa (hand M c / I)')
        r = static(j, d, tag, PETG, fixtures=[('fixed', fix)], loads=[('normal', tops, 9.0)], el=el, materials={'rail': ALU},
                   ctrl=[(tops, max(el / 2, 0.6))], max_nodes=200000, loose_ok=True)
        log('mount nodes', int(mount_mask(r).sum()), 'of', r.nodes)
        log('SUMMARY', r.summary())
        return r
    holes = [pick(d, kind='cyl', r=2.0, at=(x + 2.0, y, 8.5)) for (x, y) in PADS]
    expect('insert hole faces', sum(len(h) for h in holes), 4, 0)
    out['rows'] = []
    for tag, F in (('LAT_Y', (0.0, 2.25, 0.0)), ('LAT_X', (2.25, 0.0, 0.0))):
        for el in (2.0, 1.5):
            log(f'PREDICT {tag} {el}: nodes about {12 * vol / el ** 3 * 1.5:.0f}, displacement about 0.01 mm, peak on the pad insert-hole wall and the pad root (bending of a 3.5 mm tall post, hand 0.2 MPa), tension across layers small')
            r = static(j, d, f'{tag}_{el}', PETG, fixtures=[('fixed', base)],
                       loads=[('bearing', h, F) for h in holes], el=el, materials={'rail': ALU},
                       ctrl=[(tops, max(el / 2, 0.6))], max_nodes=200000, loose_ok=True)
            keep = mount_mask(r) & edge_far(r, 6.0)
            vm, at = r.peak(keep); tdn, tup = both_signs(r, (0, 0, 1), keep); sh = r.layer_shear((0, 0, 1), keep)
            # the bore wall is where a bearing load puts its stress: read it unmasked, on the mount only
            allm = mount_mask(r)
            vm_all = float(r.vm[allm].max())
            row = dict(case=tag, el=el, nodes=r.nodes, vm=vm, at=at, layer_down=tdn, layer_up=tup, shear=sh[0], vm_mount_unmasked=vm_all,
                       disp=r.max_disp(), reaction=list(r.reaction), applied=r.applied)
            log('ROW', row); out['rows'].append(row)
    json.dump(out, open(RUN / 'd1b_lateral_results.json', 'w'), indent=1, default=float)
    close(j.sw, d)
    stamp(RUN, 'D1 lateral job: done')
print('LATERAL DONE')
