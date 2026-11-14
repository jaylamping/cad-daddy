"""D3 part two: the change request, made by EDITING the saved P1..P6 parts (not rebuilding). Plan: plans/D_D3.md section 4.
Changes from the plan are marked CHANGED. Run as a script after plates.py has written d3_part1.json."""
from plates import *  # noqa: F401,F403

CHAMFER = {'P1': 0.4, 'P2': 1.0, 'P3': 0.4, 'P4': 0.4, 'P5': 1.0, 'P6': 1.0}
WHY_B = {'P1': 'chamfer 0.4 not 1.0: the counterbore edge is 1.0 mm from the outside, a 1 mm chamfer would meet it',
         'P3': 'ring A on 70 turned 22.5 deg (0.3 mm to the ring B counterbore otherwise); chamfer 0.4 not 1.0, as P1',
         'P4': 'chamfer 0.4 not 1.0, as P1'}


def edge_z(e):
    cp = e.GetCurveParams3
    return list(e.GetCurve.Evaluate2((cp.UMinValue + cp.UMaxValue) / 2, 0))[2] * 1e3


def change(j, name, part1):
    p = spec(name)
    T, R, w = p['t'], p['od'] / 2, CHAMFER[name]
    d = open_doc(j.sw, WIP / f'{name}.SLDPRT')
    expect('opened part one', volume(d), part1['volume_mm3'], 0.0001)
    before = tree(d)
    save_as(d, WIP / f'{name}_b.SLDPRT')
    set_dim(d, 'DISC', T, T + 1.5)                          # 1. thicker: the one driving dimension
    d.ForceRebuild3(False)
    must('rebuild errors', len(feature_errors(d)), 0)
    p = dict(p, t=T + 1.5, cb=(p['cb'][0], p['cb'][1] + 1.5))
    if name == 'P3':                                        # 2. P3: ring A to the 70 circle, turned 22.5 deg
        p = dict(p, a=(8, 3.4, 70), turn_a=22.5)
        redraw_circles(d, 'RING_A_SK', ring_pts(8, 70, 22.5, 0.0), 1.7)
        d.ForceRebuild3(False)
        must('rebuild errors', len(feature_errors(d)), 0)
    wl = walls(p, w)
    log(name, 'walls', wl)
    if min(wl.values()) < 0.6:
        raise Failed(f'{name}_b: a wall under 0.6 mm in the numbers: {wl}')
    expect('thicker, floors kept', volume(d), hand(p), 0.001)
    rim = pick(d, kind='cyl', r=R)
    must('outside face', len(rim), 1)                       # 3. chamfer on the top outside edge
    top = [e for e in (call(rim[0], 'GetEdges') or []) if abs(edge_z(e) - (T + 1.5)) < 0.01]
    must('top outside edge', len(top), 1)
    v0 = volume(d)
    chamfer(d, top, w, 'TOP_CHAMFER')
    expect('chamfer dv', v0 - volume(d), math.pi * w * w * (R - w / 3), 0.02)
    single_body(d)
    must('rebuild errors', len(feature_errors(d)), 0)
    save(d)
    expect(name + '_b volume', volume(d), hand(p, w), 0.001)
    fz = measure(d, p, w)
    expect('floor where it was', fz, part1['counterbore_floor_z_mm'], 0.01)
    after = tree(d)
    old = [tuple(x) for x in part1['tree']]
    same = [tuple(x) for x in after[:len(before)]] == [tuple(x) for x in before] == old
    export(j.sw, d, WIP / f'{name}_b.stl')
    st = check_export(d, WIP / f'{name}_b.stl')
    out = dict(volume_mm3=volume(d), hand_volume_mm3=hand(p, w), mass_g=volume(d) * DENS_G_MM3, bodies=len(bodies(d)),
               stl_watertight=st['watertight'], min_wall_mm=min(wl.values()), min_wall_where=min(wl, key=wl.get),
               changed=name in WHY_B, why=WHY_B.get(name, 'as asked'), counterbore_floor_z_mm=fz,
               old_features_unchanged=same, new_features=[x[0] for x in after[len(before):]])
    close(j.sw, d)
    return out


if __name__ == '__main__':
    part1 = json.loads((HERE / 'd3_part1.json').read_text(encoding='utf-8'))
    with job() as j:
        b = {}
        for n in ASKED:
            b[n] = change(j, n, part1[n])
            (HERE / 'd3_part2.json').write_text(json.dumps(b, indent=1, default=float), encoding='utf-8')
            log(n, '_b done at minute', minutes())
