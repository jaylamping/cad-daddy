"""D1 study: 9 N (10 g of the 90 g board) on the mount. Series DOWN at three mesh sizes (support: base bottom on the rail),
and the same load with the M5 hole walls fixed instead (second support). Four studies, one job."""
import json, math, sys
from pathlib import Path
import numpy as np
ROOT = Path(r'J:\code\cad-daddy-wt\sw-eval-sonnet-adv-d')
sys.path.insert(0, str(ROOT / 'solidworks'))
from swkit import *
from swfea import PETG, static, judge
W = ROOT / '_wip' / 'sw-eval' / 'sonnet-adv-d' / 'd1'
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
    d = open_doc(j.sw, W / 'buck_mount.SLDPRT')
    d.ForceRebuild3(False)
    base = pick(d, kind='plane', normal=(0, 0, -1), at=(0, 0, 0))
    m5 = pick(d, kind='cyl', r=2.75)
    tops = [f for (x, y) in PADS for f in pick(d, kind='plane', normal=(0, 0, 1), at=(x + 2.75, y, ZT))]
    expect('base bottom faces', len(base), 1, 0); expect('M5 faces', len(m5), 2, 0); expect('pad tops', len(tops), 4, 0)
    vol = volume(d)
    rows = []
    def run(el, tag, fix):
        pred_nodes = 12 * vol / el ** 3 * 1.5
        log(f'PREDICT {tag}: nodes about {pred_nodes:.0f}, displacement about 0.01 mm, peak at the bridge root beside the base edge, about 0.6 MPa (hand M c / I)')
        r = static(j, d, tag, PETG, fixtures=[('fixed', fix)], loads=[('normal', tops, 9.0)], el=el,
                   ctrl=[(tops, max(el / 2, 0.6))], max_nodes=200000, loose_ok=True)
        log('SUMMARY', r.summary())
        return r
    res = {}
    for el in (3.0, 2.0, 1.5):
        r = run(el, f'DOWN_{el}', base)
        res[el] = r
        keep = r.away(dist=6.0)       # one exclusion distance for the series (two of the coarsest elements)
        vm, at = r.peak(keep)
        tdn, tup = both_signs(r, (0, 0, 1), keep)
        sh = r.layer_shear((0, 0, 1), keep)
        rows.append(dict(el=el, nodes=r.nodes, vm=vm, at=at, layer_down=tdn, layer_up=tup, shear=sh[0], shear_at=sh[1],
                         disp=r.max_disp(), reaction=list(r.reaction), applied=r.applied, solve_s=r.seconds,
                         vm_all=float(r.vm.max())))
        log('ROW', rows[-1])
        if el == 2.0:
            # plain-section check: surface nodes of the +Y bridge at Y 14 to 18, X 35..43, top face Z 8 (hand 0.57 MPa at Y=10, falling to 0 at the pad)
            sec = r.in_box([36, 11, 7.9, 42, 14, 8.1])
            out['section_sz_mean'] = float(np.abs(r.s[sec, 2]).mean()) if sec.any() else None
            out['section_syy_mean'] = float(np.abs(r.s[sec, 2]).mean()) if sec.any() else None
            out['section_sy_at_y11_14'] = float(np.abs(r.s[sec, 2]).mean()) if sec.any() else None
            out['section_nodes'] = int(sec.sum())
            np.savez_compressed(W / 'd1_down_el2.npz', pos=r.pos, s=r.s, disp=r.disp)
    # second support: the M5 hole walls fixed instead of the whole base bottom
    r2 = run(2.0, 'DOWN_M5WALLS', m5)
    keep = r2.away(dist=6.0)
    vm2, at2 = r2.peak(keep); t2 = both_signs(r2, (0, 0, 1), keep); sh2 = r2.layer_shear((0, 0, 1), keep)
    out['alt_support'] = dict(nodes=r2.nodes, vm=vm2, at=at2, layer_down=t2[0], layer_up=t2[1], shear=sh2[0], disp=r2.max_disp(),
                              reaction=list(r2.reaction), vm_all=float(r2.vm.max()))
    # a lateral case cannot be read from DOWN; it is done in d1_fea_lateral.py
    out['rows'] = rows
    allow = dict(vm=45.0, layer=22.5, shear=13.0)
    series = {'mount, 9 N, vm': [x['vm'] for x in rows], 'mount, 9 N, layer': [max(x['layer_down'], x['layer_up']) for x in rows],
              'mount, 9 N, shear': [x['shear'] for x in rows]}
    lim = {'mount, 9 N, vm': 45.0, 'mount, 9 N, layer': 22.5, 'mount, 9 N, shear': 13.0}
    out['judge'] = judge(series, lim, need=2.0)
    json.dump(out, open(RUN / 'd1_fea_results.json', 'w'), indent=1, default=float)
    close(j.sw, d)
    stamp(RUN, 'D1 fea job: done')
print('FEA DONE')
