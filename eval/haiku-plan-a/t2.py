"""T2: open the saved T1 bracket, add four counterbores and one slot by editing it in place, save as bracket_b."""
from bracket import *  # noqa: F401,F403

src, dst = WIP / 'bracket.SLDPRT', WIP / 'bracket_b.SLDPRT'
h0 = sha(src)
with job() as j:
    d = open_doc(j.sw, src)
    expect('opened the T1 part', volume(d), hand_volume(), 0.001)
    before = tree(d)
    log('tree before', before)
    save_as(d, dst)                                   # from here on d is bracket_b; bracket.SLDPRT is not touched again
    # 1. counterbores: tool Z 3..7 (1 mm of air above the base top), floor exactly at Z 3
    with Sk(d, plane(d, 'Z', 5.0, 'CBORE_P'), 'CBORE') as s:
        for x, y in BASE_XY:
            s.circle((x, y, 5.0), 5.0)
    extrude(d, s.feat, 'CBORE', 4.0, cut=True, mode=MID, expect_dv=4 * math.pi * (25 - 2.75 ** 2) * 3)
    save(d)
    # 2. slot ends: two full Ø6 holes at X 38 and X 52
    with Sk(d, plane(d, 'Z', 3.0, 'SLOT_ENDS_P'), 'SLOT_ENDS') as s:
        s.circle((38, 25, 3.0), 3.0)
        s.circle((52, 25, 3.0), 3.0)
    extrude(d, s.feat, 'SLOT_ENDS', 7.0, cut=True, mode=MID, expect_dv=2 * math.pi * 9 * 6)
    # 3. slot middle: the rectangle between the two centres
    with Sk(d, plane(d, 'Z', 3.0, 'SLOT_MID_P'), 'SLOT_MID') as s:
        s.rect((38, 22, 3.0), (52, 28, 3.0))
    extrude(d, s.feat, 'SLOT_MID', 7.0, cut=True, mode=MID, expect_dv=14 * 6 * 6 - math.pi * 9 * 6)
    single_body(d)
    must('rebuild errors', len(feature_errors(d)), 0)
    save(d)
    hand = hand_volume() - 4 * math.pi * (25 - 2.75 ** 2) * 3 - (14 * 6 + math.pi * 9) * 6
    expect('volume', volume(d), hand, 0.001)
    for got, want in zip(bbox(d), (0, 0, 0, 80, 50, 46)):
        expect('box', got, want, 0.01)
    floors = pick(d, kind='plane', normal=(0, 0, 1), inside=[19, 4, 2.9, 71, 46, 3.1])
    must('counterbore floors', len(floors), 4)
    fz = [face_info(f)['box'][2] for f in floors]
    for z in fz:
        expect('floor z', z, 3.0, 0.01)
    for f in floors:
        expect('floor area', face_info(f)['area'], math.pi * (25 - 2.75 ** 2), 0.02)
    cb = holes(d, 5.0, inside=[19, 4, 2.9, 71, 46, 6.1])
    must('counterbore walls', len(cb), 4)
    for h, (x, y) in zip(cb, BASE_XY):
        expect('cbore x', h[1][0], x, 0.02)
        expect('cbore y', h[1][1], y, 0.02)
    ends = holes(d, 3.0, inside=[34, 21, -0.1, 56, 29, 6.1])
    must('slot end faces', len(ends), 2)
    log('slot end boxes', [e[2] for e in ends])       # expect x 35..38 and 52..55, y 22..28
    after = tree(d)
    log('tree after', after)
    new = [n for n, _, _ in after[len(before):] if not n.endswith('_P') and not n.endswith('_SK')]
    if after[:len(before)] != before or new != ['CBORE', 'SLOT_ENDS', 'SLOT_MID']:
        log('NOTE: tree is not "old features unchanged + the new ones": read both lists and report what differs')
    put('T2', volume_mm3=volume(d), hand_volume_mm3=hand, counterbore_floor_z_mm=float(np.mean(fz)),
        bodies=len(bodies(d)), status='done', notes='edited in place; tree before/after in the log')
    export(j.sw, d, WIP / 'bracket_b.stl')
    close(j.sw, d)
if sha(src) != h0:
    raise SystemExit('bracket.SLDPRT changed on disk: T2 must not alter it. Rebuild it with t1.py and say so.')
log('bracket.SLDPRT sha unchanged', h0[:16])
