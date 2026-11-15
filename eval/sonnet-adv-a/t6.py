"""T6: PETG block with a Ø10.2 hole, loose Ø10 steel pin, 250 N up on each stub. No-penetration contact, direct sparse solver,
soft end pads clear of the block hold the pin sideways. Studies: A full load el 0.8 (control on the contact faces), B a thousandth
of the load (contact proof), C full load coarser (1.2), D full load finer (0.55)."""
import json, math, sys
from lib3 import *
from swfea import _arr, NO_PENETRATION, SOLVER_DIRECT, STEEL
from swkit import call as swcall

PAD = dict(name='Soft pad', EX=0.5e6, NUXY=0.45, DENS=1000.0, SIGYLD=1e6, SIGXT=1e6)
CASES = sys.argv[1] if len(sys.argv) > 1 else 'ABCD'
ZC = 10.102          # pin axis: 0.002 mm above the hole axis plus the 0.1 mm clearance, so the pin starts touching the crown
T6 = WIP / 't6b'
T6.mkdir(exist_ok=True)


def cyl_part(sw, name, y0, y1, r, zc=ZC):
    d = new_part(sw, T6 / f'{name}.SLDPRT')
    ym = (y0 + y1) / 2
    with Sk(d, plane(d, 'Y', ym, name.upper() + '_P'), name.upper()) as s:
        s.circle((0.0, ym, zc), r)
    extrude(d, s.feat, name.upper(), y1 - y0, mode=MID, expect_dv=math.pi * r * r * (y1 - y0))
    save(d)
    close(sw, d)


# hand numbers -------------------------------------------------------------------------------------------------------
Estar = 1.0 / ((1 - 0.28 ** 2) / 2.1e5 + (1 - 0.38 ** 2) / 1.9e3)
Rstar = 1.0 / (1 / 5.0 - 1 / 5.1)
w = 500.0 / 30.0
b = math.sqrt(4 * w * Rstar / (math.pi * Estar))
p0 = 2 * w / (math.pi * b)
mean = 500.0 / (10.0 * 30.0)
log(f'HAND: mean projected bearing {mean:.2f} MPa (a floor); Hertz in a 0.1 mm larger socket: E* {Estar:.0f} MPa, R* {Rstar:.0f} mm, '
    f'half width {b:.2f} mm, peak {p0:.2f} MPa; pin rises 0.10 mm (the clearance) before it bears')

with job(wait_s=1800) as j:
    stamp(RUN, 'T6 start')
    sw = j.sw
    cyl_part(sw, 'tp_pin_c', -15, 15, 5.0)
    cyl_part(sw, 'tp_pin_e1', 15, 25, 5.0)
    cyl_part(sw, 'tp_pin_e2', -25, -15, 5.0)
    cyl_part(sw, 'tp_pad_a', 25, 27, 1.5)
    cyl_part(sw, 'tp_pad_b', -27, -25, 1.5)
    d = new_part(sw, T6 / 'tp_all.SLDPRT')
    with Sk(d, plane(d, 'Z', 10.0, 'BLOCK_P'), 'BLOCK') as s:
        s.rect((-20, -15, 10.0), (20, 15, 10.0))
    extrude(d, s.feat, 'BLOCK', 20.0, mode=MID, expect_dv=40 * 30 * 20)
    with Sk(d, plane(d, 'Y', 0.0, 'HOLE_P'), 'HOLE') as s:
        s.circle((0.0, 0.0, 10.0), 5.1)
    extrude(d, s.feat, 'HOLE', 60.0, cut=True, mode=MID, expect_dv=math.pi * 5.1 ** 2 * 30)
    save(d)
    for nm in ('tp_pin_c', 'tp_pin_e1', 'tp_pin_e2', 'tp_pad_a', 'tp_pad_b'):
        insert_body(d, T6 / f'{nm}.SLDPRT')
    save(d)
    bl = bodies(d)
    log('bodies', bl)
    expect('six bodies', len(bl), 6, 0)
    expect('rebuild errors', len(feature_errors(d)), 0, 0)
    vols = {n: v for n, v, _ in bl}
    log('body volumes', vols)
    close(sw, d)
    stamp(RUN, 'T6 model built')

    d = open_doc(sw, T6 / 'tp_all.SLDPRT')
    j.simulation()
    d.ForceRebuild3(False)
    results = {}

    def picks():
        d.ForceRebuild3(False)
        bottom = pick(d, kind='plane', normal=(0, 0, -1), at=(0, 0, 0)); expect('bottom', len(bottom), 1, 0)
        pad_out = (pick(d, kind='plane', at=(0, 27, ZC)) + pick(d, kind='plane', at=(0, -27, ZC)))
        expect('pad outer faces', len(pad_out), 2, 0)
        pin_c = pick(d, kind='cyl', r=5.0, inside=[-5.1, -15.1, 5.0, 5.1, 15.1, 15.2]); expect('pin centre face', len(pin_c), 1, 0)
        hole = pick(d, kind='cyl', r=5.1); expect('hole face', len(hole), 1, 0)
        s1 = pick(d, kind='cyl', r=5.0, inside=[-5.1, 14.9, 5.0, 5.1, 25.1, 15.2]); expect('stub +Y', len(s1), 1, 0)
        s2 = pick(d, kind='cyl', r=5.0, inside=[-5.1, -25.1, 5.0, 5.1, -14.9, 15.2]); expect('stub -Y', len(s2), 1, 0)
        pads = pick(d, kind='cyl', r=1.5); expect('pad walls', len(pads), 2, 0)
        return bottom, pad_out, pin_c, hole, s1, s2, pads

    def split_post(st, res):
        mesh = st.Mesh
        raw = _arr(swcall(mesh, 'GetNodes'), 4)
        xyz = {int(i): row for i, row in zip(raw[:, 0], raw[:, 1:] * 1000)}
        q = _arr(res.GetReactionForcesAndMoments(0, NUL, 0, L()), 9)
        pos = np.array([xyz[int(i)] for i in q[:, 0]])
        return dict(ids=q[:, 0], pos=pos, f=q[:, 1:4])

    def analyse(r, load_scale, el_ctrl):
        pos, s = r.pos, r.s
        ids = s[:, 0].astype(int)
        dmap = {int(k): i for i, k in enumerate(r.disp[:, 0])}
        uz = np.array([r.disp[dmap[k], 3] for k in ids]); uy = np.array([r.disp[dmap[k], 2] for k in ids])
        ux = np.array([r.disp[dmap[k], 1] for k in ids])
        rad = np.hypot(pos[:, 0], pos[:, 2] - 10.0)
        ang = np.arctan2(pos[:, 2] - 10.0, pos[:, 0])
        ux_, uz_ = np.cos(ang), np.sin(ang)
        srr = s[:, 1] * ux_ ** 2 + s[:, 3] * uz_ ** 2 + 2 * s[:, 5] * ux_ * uz_       # sx, sz, txz
        block_hole = (rad >= 5.09) & (rad <= 5.12) & (np.abs(pos[:, 1]) <= 15.001) & (np.abs(pos[:, 0]) <= 6.0)
        pin_c = (np.hypot(pos[:, 0], pos[:, 2] - ZC) <= 5.001) & (np.abs(pos[:, 1]) <= 15.001)
        pressure = -srr
        i = np.flatnonzero(block_hole)[np.argmax(pressure[block_hole])]
        # contact patch: hole-surface nodes with pressure over 5 % of the peak
        patch = block_hole & (pressure > 0.05 * pressure[i])
        # block nodes within 1.5 mm of the hole for the vm
        near = (rad >= 5.09) & (rad <= 6.6) & (np.abs(pos[:, 1]) <= 15.001) & (np.abs(pos[:, 0]) <= 8.0)
        j2 = np.flatnonzero(near)[np.argmax(r.vm[near])]
        ex = r.extra
        fpos, f = ex['pos'], ex['f']
        pad = np.abs(fpos[:, 1]) > 25.5
        blk = ~pad
        out = dict(
            el_ctrl=el_ctrl, load_scale=load_scale, nodes=r.nodes, solve_s=round(r.seconds), reaction=r.reaction,
            reaction_blockbottom=[round(float(v), 4) for v in f[blk].sum(axis=0)],
            reaction_pads=[round(float(v), 5) for v in f[pad].sum(axis=0)],
            pad_share_pct=round(float(np.linalg.norm(f[pad].sum(axis=0)) / (500.0 * abs(load_scale)) * 100), 5),
            pin_uz_mean=round(float(uz[pin_c].mean()), 5), pin_rise_mm=round(0.1 + float(uz[pin_c].mean()), 5), pin_rise_min=round(float(uz[pin_c].min()), 5), pin_rise_max=round(float(uz[pin_c].max()), 5),
            pin_ux_mean=round(float(ux[pin_c].mean()), 6), pin_uy_mean=round(float(uy[pin_c].mean()), 6),
            peak_bearing_mpa=round(float(pressure[i]), 3), peak_bearing_at=pos[i].round(2).tolist(),
            patch_nodes=int(patch.sum()),
            patch_half_width_mm=None,
            peak_vm_near_hole=round(float(r.vm[j2]), 3), peak_vm_near_hole_at=pos[j2].round(2).tolist(),
            peak_vm_block_all=None, vm_pin_max=round(float(r.vm[pin_c].max()), 3),
            hole_pressure_sum_n=None,
        )
        # patch width across the crown (in x at the y of the peak)
        if patch.any():
            xs = pos[patch, 0]
            out['patch_x_range'] = [round(float(xs.min()), 2), round(float(xs.max()), 2)]
            out['patch_half_width_mm'] = round(float((xs.max() - xs.min()) / 2), 2)
        # pressure along y at the crown (x within 0.3 of 0, z>10)
        crown = block_hole & (np.abs(pos[:, 0]) < 0.35) & (pos[:, 2] > 10)
        ys = np.argsort(pos[crown, 1])
        out['crown_pressure_by_y'] = [[round(float(pos[crown][k, 1]), 1), round(float(pressure[crown][k]), 3)] for k in ys][::max(1, len(ys) // 24)]
        return out

    def case(tag, scale, ctrl_size, el=3.0):
        bottom, pad_out, pin_c, hole, s1, s2, pads = picks()
        load_n = 250.0 * scale
        name = f'T6 {tag}'
        ctrl = [(pin_c + hole, ctrl_size), (pads, 0.7)]
        r = run_case(j, d, name, el, [('fixed', bottom), ('fixed', pad_out)],
                     [('remote', s1, (0.0, 20.0, ZC), (0, 0, load_n), (0, 0, 0)),
                      ('remote', s2, (0.0, -20.0, ZC), (0, 0, load_n), (0, 0, 0))],
                     ctrl, contacts=[(NO_PENETRATION, pin_c, hole)], materials={'tp_pin': STEEL, 'tp_pad': PAD}, solver=SOLVER_DIRECT, post=split_post, retry=False,
                     predict=dict(nodes=45000, rise_mm='0.10 (clearance, built in) plus a few micrometres' if scale > 0 else 'pin leaves the crown on the pads, about 0.4 mm', peak_bearing_mpa=round(p0 * 1.0, 1), half_width_mm=round(b, 2),
                                  peak_at='crown, near the block faces y +-15 (pin bends: edge loaded)'))
        expect('reaction Fz = -(2 x load)', r.reaction[2], -2 * load_n, 0.02)
        out = analyse(r, scale, ctrl_size)
        results[tag] = out
        log(name, json.dumps({k: v for k, v in out.items() if k != 'crown_pressure_by_y'}))
        append_rows('t6_rows.json', tag, out)
        stamp(RUN, f'T6 {name} done')
        return out

    if 'A' in CASES:
        case('A full load ctrl0.8', 1.0, 0.8)
    if 'B' in CASES:
        case('B reversed 0.001 load ctrl0.8', -0.001, 0.8)
    if 'C' in CASES:
        case('C full load ctrl1.2', 1.0, 1.2)
    if 'D' in CASES:
        case('D full load ctrl0.6', 1.0, 0.6)
    stamp(RUN, 'T6 job end')
