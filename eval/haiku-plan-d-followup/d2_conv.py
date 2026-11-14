"""Follow-up R3c: convergence series for the D2 housing pair. Changes from d2_fea.py: only the control sizes
(steel and PETG bands, each as the brief sets) and the job; the picks and their counts are unchanged.
Run as: python d2_conv.py X   (job 1, case X, three studies)
        python d2_conv.py Y   (job 2, case Y, three studies)
        python d2_conv.py report   (no SolidWorks: the tables and judge() from d2c_rows.json)"""
import sys
from d2_fea import *  # noqa: F401,F403
from d2_fea import split, read, SCREWS, per_node_reaction  # noqa: F401

C_FILE = HERE / 'd2c_rows.json'


def run_c(j, d, name, force, el, cs, steel_size=1.5, petg_size=0.8):
    d.ForceRebuild3(False)
    mount = pick(d, kind='plane', normal=(0, -1, 0), at=(0, -32, 3.5))
    must('mount face', len(mount), 1)
    up_seat = pick(d, kind='cyl', r=26.1, inside=[-27, 0.3, -0.2, 27, 26.2, 7.2])
    must('upper seat', len(up_seat), 1)
    lo_seat = pick(d, kind='cyl', r=26.1, inside=[-27, -26.2, -0.2, 27, -0.3, 7.2])
    must('lower seat', len(lo_seat), 1)
    ring_out = pick(d, kind='cyl', r=26.0, inside=[-26.05, -26.05, -0.05, 26.05, 26.05, 7.05])
    must('ring outside', len(ring_out), 1)
    sides = pick(d, kind='plane', normal=(0, 0, 1), at=(25, 0, 7)) + pick(d, kind='plane', normal=(0, 0, -1), at=(25, 0, 0))
    must('ring sides', len(sides), 2)
    pad_in = pick(d, kind='cyl', r=22.0)
    must('pad inner faces', len(pad_in), 4)

    def big(fs):
        return [f for f in fs if face_info(f)['area'] > 20]        # leaves out the plug ends (5.5 mm2)
    up_split = big(pick(d, kind='plane', normal=(0, -1, 0), inside=[-36.1, 0.39, -4.1, 36.1, 0.41, 11.1]))
    must('upper split faces', len(up_split), 2)
    lo_split = big(pick(d, kind='plane', normal=(0, 1, 0), inside=[-36.1, -0.41, -4.1, 36.1, -0.39, 11.1]))
    must('lower split faces', len(lo_split), 2)
    fac = {}
    for r, n in ((1.5, 4), (2.0, 8), (2.75, 4), (3.0, 4), (1.7, 4)):
        f = pick(d, kind='cyl', r=r)
        must(f'faces r {r}', len(f), n)
        fac[r] = f
    steel = fac[1.5] + fac[2.75]
    petg = fac[2.0] + fac[3.0] + fac[1.7]
    r = static(j, d, name, PETG, fixtures=[('fixed', mount), ('fixed', pad_in)],
               loads=[('remote', sides, (0.0, 0.0, 3.5), force, (0, 0, 0))],
               el=el, ctrl=[(up_seat + lo_seat + ring_out, cs), (steel, steel_size), (petg, petg_size)],
               contacts=[(NO_PENETRATION, ring_out, up_seat), (NO_PENETRATION, ring_out, lo_seat), (NO_PENETRATION, up_split, lo_split)],
               materials=MATS, solver=SOLVER_DIRECT, post=per_node_reaction, max_nodes=200_000)
    save_npz(r, name)
    return r


def one_c(j, d, rows, name, force, el, cs):
    predict(name, {4.0: 130000}.get(el, 165000), 0.55, 'ring body turns 0.555 mm (step a); peak in the upper half near the screw heads')
    try:
        r = run_c(j, d, name, force, el, cs)
    except Exception as ex:                                       # refused (over 200,000 nodes) or a failed solve: logged
        log(f'REFUSED {name} at el {el}: {str(ex)[:300]}')
        rows[name + '_refused_el%s' % el] = str(ex)[:300]
        (HERE / 'd2c_rows.json').write_text(json.dumps(rows, indent=1, default=float), encoding='utf-8')
        return None
    rows[name] = read(r)
    rows[name]['el_used'] = el
    rows[name]['cs'] = cs
    log(name, 'nodes', r.nodes, 'screw nodes', [q['nodes'] for q in rows[name]['screws']])
    (HERE / 'd2c_rows.json').write_text(json.dumps(rows, indent=1, default=float), encoding='utf-8')
    return r


def series_job(which):
    rows = json.loads(C_FILE.read_text(encoding='utf-8')) if C_FILE.exists() else {}
    with job() as j:
        j.simulation()
        d = open_doc(j.sw, WIP / 'housing_fea.SLDPRT')
        if which == 'X':
            for name, el, cs in (('D2C_X_12', 4.0, 1.2), ('D2C_X_09', 4.0, 0.9), ('D2C_X_07', 4.0, 0.7)):
                if name not in rows:
                    one_c(j, d, rows, name, (300.0, 0, 0), el, cs)
        else:
            for name, el, cs in (('D2C_Y_12', 4.0, 1.2), ('D2C_Y_09', 4.0, 0.9), ('D2C_Y_07', 4.0, 0.7)):
                if name not in rows:
                    one_c(j, d, rows, name, (0, 300.0, 0), el, cs)
        close(j.sw, d)
        log('D2 convergence job', which, 'done at', minutes(), 'min')


if __name__ == '__main__':
    which = sys.argv[1]
    if which in ('X', 'Y'):
        series_job(which)
