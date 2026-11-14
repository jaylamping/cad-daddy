"""T1: model the bracket, measure every dimension on the solid, export STEP and STL, check the export."""
from bracket import *  # noqa: F401,F403

with job() as j:
    d = build_bracket(j, WIP / 'bracket.SLDPRT')
    expect('volume', volume(d), hand_volume(), 0.001)
    for got, want in zip(bbox(d), (0, 0, 0, 80, 50, 46)):
        expect('box', got, want, 0.01)
    # every dimension measured on the solid (07-done.md, model item 2)
    hb = holes(d, 2.75)
    must('base holes', len(hb), 4)
    for h, (x, y) in zip(hb, BASE_XY):
        expect('base hole x', h[1][0], x, 0.02)
        expect('base hole y', h[1][1], y, 0.02)
        expect('base hole from z', h[2][2], 0.0, 0.02)
        expect('base hole to z', h[2][5], 6.0, 0.02)
    b = holes(d, 11.0)
    must('bore', len(b), 1)
    expect('bore y', b[0][1][1], 25, 0.02)
    expect('bore z', b[0][1][2], 28, 0.02)
    expect('bore from x', b[0][2][0], 0.0, 0.02)
    expect('bore to x', b[0][2][3], 6.0, 0.02)
    hm = holes(d, 1.7)
    must('motor holes', len(hm), 4)
    for h, (y, z) in zip(hm, sorted(MOTOR_YZ)):
        expect('motor hole y', h[1][1], y, 0.02)
        expect('motor hole z', h[1][2], z, 0.02)
    f4 = holes(d, 4.0)
    must('root fillet faces', len(f4), 1)
    log('root fillet box', f4[0][2])
    must('R5 faces', len(holes(d, 5.0)), 4)
    export(j.sw, d, WIP / 'bracket.step')
    export(j.sw, d, WIP / 'bracket.stl')
    st = check_export(d, WIP / 'bracket.stl', WIP / 'bracket.step')
    put('T1', volume_mm3=volume(d), hand_volume_mm3=hand_volume(), mass_g=volume(d) * DENS_G_MM3,
        bbox_mm=bbox(d), bodies=len(bodies(d)), stl_watertight=st['watertight'], stl_volume_mm3=st['volume'],
        status='done', notes='')
    close(j.sw, d)
