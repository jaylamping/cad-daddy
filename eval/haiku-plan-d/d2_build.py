"""D2 job 1: the two housing halves, the ring stand-in, four screw stand-ins, four soft pads, and the assembly file
housing_fea.SLDPRT with every body brought in. Plan: plans/D_D2.md sections 4 and 3.
Changes from the plan are marked CHANGED. The job runs only when this file is run as a script."""
from common import *  # noqa: F401,F403

SEAT_R, OFF, G2, OPEN_R = 26.1, 0.1, 0.4, 24.5      # seat radius, its centre offset, half the split gap, opening radius
SCREWS = [(x, z) for x in (-30.0, 30.0) for z in (0.0, 7.0)]


def half(j, name, sgn):                              # sgn +1: upper (Y 0.4..32); -1: lower (Y -32..-0.4)
    d = new_part(j.sw, WIP / f'{name}.SLDPRT')
    y0, y1 = (G2, 32.0) if sgn > 0 else (-32.0, -G2)
    with Sk(d, plane(d, 'Z', 3.5, 'BODY_P'), 'BODY') as s:
        s.rect((-36, y0, 3.5), (36, y1, 3.5))
    extrude(d, s.feat, 'BODY', 15.0, mode=MID, expect_dv=72 * 31.6 * 15)
    with Sk(d, plane(d, 'Z', 3.5, 'OPENING_P'), 'OPENING') as s:
        s.circle((0, 0, 3.5), OPEN_R)
    extrude(d, s.feat, 'OPENING', 16.0, cut=True, mode=MID, expect_dv=13849.07)
    with Sk(d, plane(d, 'Z', 3.5, 'SEAT_P'), 'SEAT') as s:
        s.circle((0, -sgn * OFF, 3.5), SEAT_R)
    extrude(d, s.feat, 'SEAT', 7.3, cut=True, mode=MID, expect_dv=880.91)
    save(d)
    if sgn > 0:
        with Sk(d, plane(d, 'Y', 16.2, 'CLEAR_P'), 'CLEAR') as s:          # cut Y -0.3..32.7
            for x, z in SCREWS:
                s.circle((x, 16.2, z), 1.7)
        extrude(d, s.feat, 'CLEAR', 33.0, cut=True, mode=MID, expect_dv=4 * math.pi * 1.7 ** 2 * 31.6)
        with Sk(d, plane(d, 'Y', 30.75, 'CBORE_P'), 'CBORE') as s:         # cut Y 28.5..33
            for x, z in SCREWS:
                s.circle((x, 30.75, z), 3.0)
        extrude(d, s.feat, 'CBORE', 4.5, cut=True, mode=MID, expect_dv=4 * math.pi * (9 - 1.7 ** 2) * 3.5)
        hand = 17981.68
    else:
        with Sk(d, plane(d, 'Y', -4.15, 'INSERT_P'), 'INSERT') as s:       # cut Y -8.4..0.1
            for x, z in SCREWS:
                s.circle((x, -4.15, z), 2.0)
        extrude(d, s.feat, 'INSERT', 8.5, cut=True, mode=MID, expect_dv=4 * math.pi * 4 * 8)
        with Sk(d, plane(d, 'Y', -28.25, 'MOUNT_P'), 'MOUNT') as s:        # cut Y -32.5..-24
            for x in (-24.0, 24.0):
                s.circle((x, -28.25, 3.5), 2.8)
        extrude(d, s.feat, 'MOUNT', 8.5, cut=True, mode=MID, expect_dv=2 * math.pi * 2.8 ** 2 * 8)
        hand = 18601.82
    single_body(d)
    must('rebuild errors', len(feature_errors(d)), 0)
    save(d)
    expect(name + ' volume', volume(d), hand, 0.001)
    for got, want in zip(bbox(d), (-36, y0, -4, 36, y1, 11)):
        expect('box', got, want, 0.01)
    seat = holes(d, SEAT_R)
    must('seat face', len(seat), 1)
    log('seat box', seat[0][2])
    must('opening faces', len(holes(d, OPEN_R)), 2)
    if sgn > 0:
        for r, n in ((1.7, 4), (3.0, 4)):
            h = holes(d, r)
            must(f'holes r {r}', len(h), n)
            log(r, [(q[1], q[2]) for q in h])
    else:
        h = holes(d, 2.0)
        must('insert holes', len(h), 4)
        log([(q[1], q[2]) for q in h])
        h = holes(d, 2.8)
        must('mount holes', len(h), 2)
        log([(q[1], q[2]) for q in h])
    export(j.sw, d, WIP / f'{name}.stl')
    check_export(d, WIP / f'{name}.stl')
    close(j.sw, d)


def ring(j):
    d = new_part(j.sw, WIP / 'ring.SLDPRT')
    with Sk(d, plane(d, 'Z', 3.5, 'DISC_P'), 'DISC') as s:
        s.circle((0, 0, 3.5), 26.0)
    extrude(d, s.feat, 'DISC', 7.0, mode=MID, expect_dv=math.pi * 676 * 7)
    with Sk(d, plane(d, 'Z', 3.5, 'RINGBORE_P'), 'RINGBORE') as s:
        s.circle((0, 0, 3.5), 24.0)
    extrude(d, s.feat, 'RINGBORE', 8.0, cut=True, mode=MID, expect_dv=math.pi * 576 * 7)
    expect('ring volume', volume(d), 2199.11, 0.001)
    save(d)
    export(j.sw, d, WIP / 'ring.stl')
    close(j.sw, d)


def screw(j, k, x, z):                               # steel stand-in: shank first, then head and plug onto it
    d = new_part(j.sw, WIP / f'screw_{k}.SLDPRT')
    for feat, r, y0, y1 in (('SHANK', 1.5, -1.0, 29.0), ('HEAD', 2.75, 28.5, 31.5), ('PLUG', 2.0, -6.5, -G2)):
        ym = (y0 + y1) / 2
        with Sk(d, plane(d, 'Y', ym, feat + '_P'), feat) as s:
            s.circle((x, ym, z), r)
        extrude(d, s.feat, feat, y1 - y0, mode=MID)
    must('screw is one body', len(bodies(d)), 1)
    expect('screw volume', volume(d), 352.21, 0.005)
    save(d)
    close(j.sw, d)


def pad(j, k, a, b):                                 # 4 degrees of a soft ring r 22..24, Z 2.5..4.5, inside the steel ring
    d = new_part(j.sw, WIP / f'pad_{k}.SLDPRT')
    pname = 'PAD_PL'                                 # CHANGED: the plan passed '' as the plane name
    with Sk(d, plane(d, 'Y' if a[1] == 0 else 'X', 0.0, pname), 'SOFTPAD') as s:
        s.rect(a, b)
        s.centerline((0, 0, 0), (0, 0, 10))
    revolve(d, s.feat, 'SOFTPAD', angle=4.0, mid=True, expect_dv=6.42)
    save(d)
    close(j.sw, d)


if __name__ == '__main__':
    with job() as j:
        half(j, 'housing_upper', +1)
        half(j, 'housing_lower', -1)
        ring(j)
        log('CHECKPOINT parts built at', minutes(), 'min')
        for k, (x, z) in enumerate(SCREWS):
            screw(j, k + 1, x, z)
        for k, (a, b) in enumerate((((22, 0, 2.5), (24, 0, 4.5)), ((-24, 0, 2.5), (-22, 0, 4.5)),
                                    ((0, 22, 2.5), (0, 24, 4.5)), ((0, -24, 2.5), (0, -22, 4.5)))):
            pad(j, k + 1, a, b)
        d = open_doc(j.sw, WIP / 'housing_lower.SLDPRT')
        save_as(d, WIP / 'housing_fea.SLDPRT')
        for f in ['housing_upper', 'ring'] + [f'screw_{k}' for k in (1, 2, 3, 4)] + [f'pad_{k}' for k in (1, 2, 3, 4)]:
            insert_body(d, WIP / f'{f}.SLDPRT')
        bs = bodies(d)
        log(bs)
        must('bodies', len(bs), 11)
        expect('assembly volume', volume(d), 18601.82 + 17981.68 + 2199.11 + 4 * 352.21 + 4 * 6.42, 0.001)
        save(d)
        close(j.sw, d)
        log('D2 job 1 done at', minutes(), 'min')
