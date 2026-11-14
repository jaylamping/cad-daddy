"""D1 job 2: one static study of the chosen mount, 9 N along -Z on the four pad tops, three mesh sizes.
Plan: plans/D_D1.md section 7. Written from the plan; changes are noted in REPORT.md."""
from common import *  # noqa: F401,F403

with job() as j:
    j.simulation()
    d = open_doc(j.sw, WIP / 'buck_mount.SLDPRT')
    keep = {}

    def run(el):
        d.ForceRebuild3(False)
        walls = pick(d, kind='cyl', r=2.75)
        must('M5 walls', len(walls), 2)
        tops = pick(d, kind='plane', normal=(0, 0, 1), inside=[-43.1, -30.1, 8.99, 43.1, 30.1, 9.01])
        must('pad tops', len(tops), 4)
        fil = pick(d, kind='cyl', r=3.0) + pick(d, kind='cyl', r=2.5)
        must('fillet faces', len(fil), 12)
        name = f'D1_Z_{int(el * 10)}'
        nodes = {2.0: 22000, 1.5: 53000, 1.1: 135000}[el]
        predict(name, nodes, 0.09, 'arm root beside an R3 corner (|x| 35 or 43, |y| 7..10, z 0 or 4), about 2.7 MPa')
        r = static(j, d, name, PETG, [('fixed', walls)], [('normal', tops, 9.0)], el=el,
                   ctrl=[(fil, round(0.4 * el, 2))], max_nodes=200_000)
        ok_cmp = compare(name, r, nodes, 0.09)
        log('compare ok:', ok_cmp)
        save_npz(r, name)
        keep[el] = r
        return r

    rows, ok = converge(run, (2.0, 1.5, 1.1), layers=(0, 0, 1))
    log('rows (el, nodes, vm, layer tension, layer shear):', rows, 'converged', ok)
    r = keep[min(keep)]
    m = r.away(dist=4.0)
    t = direction_table(r, m)
    log(json.dumps(t, default=float))
    for D in (1.0, 2.0, 3.0, 5.0):
        m = r.away(dist=D)
        log('outside', D, 'mm of fixture and load faces: vm', r.peak(m), 'layer Z', r.layer_stress((0, 0, 1), m), 'shear Z', r.layer_shear((0, 0, 1), m))
    sp = r.in_box([44.0, -7.1, -0.1, 56.1, 7.1, 4.1]) | r.in_box([-56.1, -7.1, -0.1, -44.0, 7.1, 4.1])
    log('spine round the M5 holes: vm max', float(r.vm[sp].max()), 'mean sigma-x on the top face', float(r.s[sp & (r.pos[:, 2] > 3.95), 1].mean()))
    p = r.pos
    arm = (p[:, 2] > 3.95) & (np.abs(np.abs(p[:, 1]) - 15) < 1.0) & (np.abs(np.abs(p[:, 0]) - 39) < 3.5)
    log('reaction', r.reaction, 'max disp', r.max_disp(), 'arm top sigma-y at |y| 15:', float(r.s[arm, 2].mean()),
        'on', int(arm.sum()), 'nodes; excluded maximum', float(r.vm.max()))
    close(j.sw, d)
    log('D1 study done at', minutes(), 'min')
