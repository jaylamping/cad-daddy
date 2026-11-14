"""The real link of benchmark run sonnet-c2, rebuilt up to the stem with its junction left sharp, then each blend tried.

    python eval/loft-blend/link.py base            # link_sharp.SLDPRT and what the seam is made of
    python eval/loft-blend/link.py m1 m2 m4        # the trials, each on a copy

Geometry and numbers are those of eval/sonnet-c2/c2_build.py: a revolved elbow flange about Y (D70, 8 thick, rim
rounded with polyline arcs), a ridge loft on its back, and the stem lofted through eight superellipse sections along -Z,
starting inside the flange rim. The cable passage, slot and pin hole are added after the blend, as in that run.
"""
import json
import math
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import OUT  # noqa: E402
from swkit import (MID, NUL, Failed, Sk, bbox, bodies, call, close, export, extrude, face_info, faces, feature_errors, job,  # noqa: E402
                   loft, log, m, new_part, open_doc, plane, revolve, save, solid_bodies, volume)

HERE = Path(__file__).resolve().parent
SEC = [(-32, 14, 8, 2.0, 0), (-46, 14.5, 12.5, 2.2, 0), (-95, 12.5, 11.5, 2.2, 0), (-150, 13.5, 12.5, 2.4, 0),
       (-172, 14.5, 17, 2.6, 0), (-190, 14.5, 23, 3.5, 0), (-204, 13.5, 23, 3.5, 0), (-212, 10.5, 20, 3.0, 0)]
RIDGE = [(-16, 6.5, 4.5, 2.0, 0, 4.0), (-26, 7.0, 4.5, 2.0, 0, 4.0), (-36, 9.0, 4.5, 2.0, 0, 4.0), (-44, 11.0, 5.0, 2.0, 0, 3.0)]


def sec(cx, z, a, b, n=2.0, k=24, y0=0.0):
    pts = []
    for i in range(k):
        t = 2 * math.pi * i / k
        c, s = math.cos(t), math.sin(t)
        pts.append((cx + a * math.copysign(abs(c) ** (2 / n), c), y0 + b * math.copysign(abs(s) ** (2 / n), s), z))
    return pts


def loft_sections(d, secs, name):
    sks = []
    for i, sc in enumerate(secs):
        z, a, b, n, cx = sc[:5]
        y0 = sc[5] if len(sc) > 5 else 0.0
        with Sk(d, plane(d, 'Z', z, f'{name}_P{i}'), f'{name}_S{i}') as s:
            s.spline(sec(cx, z, a, b, n, y0=y0))
        sks.append(s.feat)
    return loft(d, sks, name)


def base(j):
    d = new_part(j.sw, OUT / 'link_sharp.SLDPRT')
    prof = [(15, -4, 0), (32.5, -4, 0)]
    for k in range(1, 9):
        a = math.radians(-90 + 90 * k / 8)
        prof.append((32.5 + 2.5 * math.cos(a), -1.5 + 2.5 * math.sin(a), 0))
    prof += [(35, 7.6, 0), (34.5, 8.7, 0), (33.5, 8.3, 0), (32.4, 7.1, 0), (31.3, 5.9, 0), (30.3, 5.0, 0), (29.4, 4.35, 0),
             (28.6, 4.0, 0), (15, 4, 0)]
    with Sk(d, plane(d, 'Z', 0.0, 'DISC_P'), 'DISC') as s:
        s.poly(prof)
        s.centerline((0, -10, 0), (0, 10, 0))
    revolve(d, s.feat, 'DISC')
    with Sk(d, plane(d, 'Y', 0.0, 'HOLES_P'), 'HOLES') as s:
        for k in range(6):
            a = math.radians(60 * k)
            s.circle((25 * math.cos(a), 0, 25 * math.sin(a)), 1.7)
    extrude(d, s.feat, 'HOLES', 10.0, cut=True, mode=MID, expect_dv=6 * math.pi * 1.7 ** 2 * 8)
    loft_sections(d, RIDGE, 'RIDGE')
    loft_sections(d, SEC, 'STEM')
    save(d)
    log('base volume', round(volume(d), 1), 'bodies', len(bodies(d)), 'errors', feature_errors(d))
    return d


ROOT = {   # the stem's first sections replaced by ones that dive into the flange: the last lies wholly inside it
    'm3a': [(-26, 20.0, 3.6, 2.0, 0), (-36, 15.5, 8.0, 2.0, 0)],
    'm3b': [(-26, 21.0, 3.6, 2.0, 0), (-31, 18.0, 5.6, 2.0, 0), (-38, 15.2, 9.0, 2.1, 0)],
}
SKIRT = {  # a separate loft over the sharp junction; its last section sits 0.15 mm inside the stem
    'm4a': [(-26, 20.0, 3.6, 2.0, 0), (-33, 17.0, 9.0, 2.0, 0), (-46, 14.35, 12.35, 2.2, 0)],
}


def build_variant(j, tag):
    """The link with the junction made the given way, up to the stem. Returns the open document."""
    d = new_part(j.sw, OUT / f'link_{tag}.SLDPRT')
    prof = [(15, -4, 0), (32.5, -4, 0)]
    for k in range(1, 9):
        a = math.radians(-90 + 90 * k / 8)
        prof.append((32.5 + 2.5 * math.cos(a), -1.5 + 2.5 * math.sin(a), 0))
    prof += [(35, 7.6, 0), (34.5, 8.7, 0), (33.5, 8.3, 0), (32.4, 7.1, 0), (31.3, 5.9, 0), (30.3, 5.0, 0), (29.4, 4.35, 0),
             (28.6, 4.0, 0), (15, 4, 0)]
    with Sk(d, plane(d, 'Z', 0.0, 'DISC_P'), 'DISC') as s:
        s.poly(prof)
        s.centerline((0, -10, 0), (0, 10, 0))
    revolve(d, s.feat, 'DISC')
    loft_sections(d, RIDGE, 'RIDGE')
    if tag in ROOT:
        loft_sections(d, ROOT[tag] + SEC[1:], 'STEM')
    else:
        loft_sections(d, SEC, 'STEM')
    if tag in SKIRT:
        v0 = volume(d)
        loft_sections(d, SKIRT[tag], 'SKIRT')
        log('skirt added', round(volume(d) - v0, 1))
    save(d)
    return d


def finish(j, d, tag):
    """Holes, cable passage, slot and pin hole, as the benchmark run cut them; export the STL."""
    with Sk(d, plane(d, 'Y', 0.0, 'HOLES_P'), 'HOLES') as s:
        for k in range(6):
            a = math.radians(60 * k)
            s.circle((25 * math.cos(a), 0, 25 * math.sin(a)), 1.7)
    extrude(d, s.feat, 'HOLES', 40.0, cut=True, mode=MID)
    with Sk(d, plane(d, 'Z', -100.0, 'CABLE_P'), 'CABLE') as s:
        s.circle((0, 2.0, -100.0), 3.0)
    extrude(d, s.feat, 'CABLE', 172.0, cut=True, mode=MID)
    with Sk(d, plane(d, 'X', 0.0, 'SLOT_P'), 'SLOT') as s:
        s.poly([(0, -16, -183), (0, 16, -183), (0, 16, -240), (0, -16, -240)])
    extrude(d, s.feat, 'SLOT', 80.0, cut=True, mode=MID)
    with Sk(d, plane(d, 'Y', 0.0, 'PIN_P'), 'PIN') as s:
        s.circle((0, 0, -200), 4.0)
    extrude(d, s.feat, 'PIN', 80.0, cut=True, mode=MID)
    save(d)
    row = dict(volume=round(volume(d), 1), bodies=len(bodies(d)), errors=feature_errors(d), bbox=[round(v, 2) for v in bbox(d)])
    log(tag, 'finished', row)
    export(j.sw, d, OUT / f'link_{tag}.stl')
    return row


def feat_faces(d, name):
    return list(call(d.FeatureByName(name), 'GetFaces') or [])


def same(a, b):
    return bool(d_sw.IsSame(a, b) == 1)


def seam(d, name='STEM'):
    """(edges, other faces): the edges where the named feature's faces meet any other face, and those other faces."""
    mine = feat_faces(d, name)
    edges, others = [], []
    for f in mine:
        for e in call(f, 'GetEdges') or []:
            pair = list(e.GetTwoAdjacentFaces2)
            other = [x for x in pair if not any(j_sw.IsSame(x, q) == 1 for q in mine)]
            if other:
                edges.append(e)
                if not any(j_sw.IsSame(other[0], q) == 1 for q in others):
                    others.append(other[0])
    return mine, edges, others


def edge_len(e):
    cp = e.GetCurveParams3
    return e.GetCurve.GetLength3(cp.UMinValue, cp.UMaxValue) * 1e3


def describe(d):
    mine, edges, others = seam(d)
    lens = sorted(round(edge_len(e), 2) for e in edges)
    kinds = {}
    for f in others:
        k = face_info(f)['kind']
        kinds[k] = kinds.get(k, 0) + 1
    out = dict(stem_faces=len(mine), seam_edges=len(edges), edge_lengths_mm=lens, other_faces=len(others), other_kinds=kinds)
    log('seam', json.dumps(out))
    return out


def copy_of(j, tag):
    p = OUT / f'link_{tag}.SLDPRT'
    shutil.copyfile(OUT / 'link_sharp.SLDPRT', p)
    d = open_doc(j.sw, p)
    d.ForceRebuild3(False)
    return d


def attempt(d, label, make):
    v0 = volume(d)
    try:
        f = make()
    except Exception as ex:      # noqa: BLE001
        log(label, 'raised', str(ex)[:120])
        f = None
    if f is None:
        log(f'{label}: did not build')
        return dict(built=False)
    d.ForceRebuild3(False)
    row = dict(built=True, dv=round(volume(d) - v0, 2), errors=feature_errors(d), bodies=len(solid_bodies(d)),
               seam_edges_after=None)
    log(label, row)
    return row


def undo(d):
    f = d.FeatureByPositionReverse(0)
    d.ClearSelection2(True)
    f.Select2(False, 0)
    d.Extension.DeleteSelection2(0)
    d.ForceRebuild3(False)


j_sw = None
if __name__ == '__main__':
    todo = sys.argv[1:] or ['base']
    f = HERE / 'link_trials.json'
    RES = json.loads(f.read_text()) if f.exists() else {}
    with job(wait_s=1800) as j:
        j_sw = j.sw
        if 'base' in todo:
            d = base(j)
            RES['seam'] = describe(d)
            close(j.sw, d)
        if 'm1' in todo:
            d = copy_of(j, 'm1')
            rows = {}
            for r in (5.0, 4.0, 3.0, 2.0, 1.0, 0.5):
                def make(r=r):
                    d.ClearSelection2(True)
                    for e in seam(d)[1]:
                        e.Select4(True, NUL)
                    return d.FeatureManager.FeatureFillet3(3, r * m, 0, 0, 0, 0, 0, NUL, NUL, NUL, NUL, NUL, NUL, NUL)
                rows[f'all_edges_R{r:g}'] = attempt(d, f'M1 all R{r:g}', make)
                if rows[f'all_edges_R{r:g}']['built']:
                    undo(d)
            # one edge at a time at 2 mm: which refuse
            n = len(seam(d)[1])
            ok = []
            for k in range(n):
                def make(k=k):
                    d.ClearSelection2(True)
                    seam(d)[1][k].Select4(True, NUL)
                    return d.FeatureManager.FeatureFillet3(3, 2.0 * m, 0, 0, 0, 0, 0, NUL, NUL, NUL, NUL, NUL, NUL, NUL)
                L_ = round(edge_len(seam(d)[1][k]), 2)
                row = attempt(d, f'M1 edge {k} ({L_} mm) R2', make)
                ok.append((k, L_, row['built']))
                if row['built']:
                    undo(d)
            rows['one_edge_at_a_time_R2'] = ok
            RES['m1_edge_fillet'] = rows
            close(j.sw, d)
        if 'm2' in todo:
            d = copy_of(j, 'm2')
            rows = {}
            for opt in (1, 3):
                for r in (5.0, 4.0, 3.0, 2.0, 1.0):
                    def make(r=r, opt=opt):
                        mine, edges, others = seam(d)
                        d.ClearSelection2(True)
                        sd = d.SelectionManager.CreateSelectData
                        sd.Mark = 2
                        for x in mine:
                            x.Select4(True, sd)
                        sd2 = d.SelectionManager.CreateSelectData
                        sd2.Mark = 4
                        for x in others:
                            x.Select4(True, sd2)
                        return d.FeatureManager.FeatureFillet3(opt, r * m, 0, 0, 2, 0, 0, NUL, NUL, NUL, NUL, NUL, NUL, NUL)
                    rows[f'opt{opt}_R{r:g}'] = attempt(d, f'M2 opt{opt} R{r:g}', make)
                    if rows[f'opt{opt}_R{r:g}']['built']:
                        undo(d)
            RES['m2_face_fillet'] = rows
            close(j.sw, d)
        if 'm5' in todo:
            import pythoncom
            from win32com.client import VARIANT
            d = copy_of(j, 'm5')
            rows = {}
            n = len(seam(d)[1])
            # which edges round alone at 1 mm, then those together as one feature (kept if it builds)
            alone = []
            for k in range(n):
                def make(k=k):
                    d.ClearSelection2(True)
                    seam(d)[1][k].Select4(True, NUL)
                    return d.FeatureManager.FeatureFillet3(2, 1.0 * m, 0, 0, 0, 0, 0, NUL, NUL, NUL, NUL, NUL, NUL, NUL)
                if attempt(d, f'M5 edge {k} alone R1 no propagation', make)['built']:
                    alone.append(k)
                    undo(d)
            rows['edges_that_round_alone_R1_no_propagation'] = alone
            for r in (3.0, 2.0, 1.0):
                def make(r=r):
                    d.ClearSelection2(True)
                    es = seam(d)[1]
                    for k in alone:
                        es[k].Select4(True, NUL)
                    return d.FeatureManager.FeatureFillet3(2, r * m, 0, 0, 0, 0, 0, NUL, NUL, NUL, NUL, NUL, NUL, NUL)
                rows[f'those_edges_together_R{r:g}'] = attempt(d, f'M5 {len(alone)} edges together R{r:g}', make)
                if rows[f'those_edges_together_R{r:g}']['built']:
                    undo(d)
            # multi-radius and variable-radius forms over the whole seam
            for label, opt, ftyp, count in (('multi_radius', 1, 0, n), ('variable_radius', 1, 1, 2 * n), ('variable_radius_n', 1, 1, n),
                                            ('variable_radius_opt4', 5, 1, 2 * n)):
                def make(opt=opt, ftyp=ftyp, count=count):
                    d.ClearSelection2(True)
                    for e in seam(d)[1]:
                        e.Select4(True, NUL)
                    radii = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [1.0 * m] * count)
                    return d.FeatureManager.FeatureFillet3(opt, 1.0 * m, 0, 0, ftyp, 0, 0, radii, NUL, NUL, NUL, NUL, NUL, NUL)
                rows[label] = attempt(d, f'M5 {label}', make)
                if rows[label]['built']:
                    undo(d)
            RES['m5_partial_multi_variable'] = rows
            close(j.sw, d)
        if 'smooth' in todo:
            # the cause: the same stem on a flange whose rim rounds are true arcs (two torus faces), not polylines
            rows = {}
            for direction in (+1, -1):
                d = new_part(j.sw, OUT / 'link_smooth.SLDPRT')
                try:
                    with Sk(d, plane(d, 'Z', 0.0, 'DISC_P'), 'DISC') as s:
                        s.poly([(32.5, 4, 0), (15, 4, 0), (15, -4, 0), (32.5, -4, 0)], closed=False)
                        s.arc((32.5, -1.5, 0), (32.5, -4, 0), (35, -1.5, 0), direction)
                        s.poly([(35, -1.5, 0), (35, 1.5, 0)], closed=False)
                        s.arc((32.5, 1.5, 0), (35, 1.5, 0), (32.5, 4, 0), direction)
                        s.centerline((0, -10, 0), (0, 10, 0))
                    revolve(d, s.feat, 'DISC', expect_dv=None)
                    hand = math.pi * (32.5 ** 2 - 15 ** 2) * 8 + 2 * math.pi * 3 * 2.5 * 32.5 + 2 * (
                        math.pi * 2.5 ** 2 / 4 * 2 * math.pi * (32.5 + 4 * 2.5 / (3 * math.pi)))
                    if abs(volume(d) - hand) > 0.01 * hand:
                        raise Failed(f'disc volume {volume(d):.0f}, hand {hand:.0f}')
                    break
                except Failed as ex:
                    log('smooth disc with arc direction', direction, 'failed:', str(ex)[:80])
                    j.sw.CloseAllDocuments(True)
                    d = None
            if d is not None:
                loft_sections(d, SEC, 'STEM')
                save(d)
                rows['seam'] = describe(d)
                for r in (5.0, 4.0, 3.0, 2.0, 1.0):
                    def make(r=r):
                        d.ClearSelection2(True)
                        for e in seam(d)[1]:
                            e.Select4(True, NUL)
                        return d.FeatureManager.FeatureFillet3(3, r * m, 0, 0, 0, 0, 0, NUL, NUL, NUL, NUL, NUL, NUL, NUL)
                    rows[f'edge_fillet_R{r:g}'] = attempt(d, f'SMOOTH edge R{r:g}', make)
                    if rows[f'edge_fillet_R{r:g}']['built']:
                        undo(d)

                    def make2(r=r):
                        mine, edges, others = seam(d)
                        d.ClearSelection2(True)
                        sd = d.SelectionManager.CreateSelectData
                        sd.Mark = 2
                        for x in mine:
                            x.Select4(True, sd)
                        sd2 = d.SelectionManager.CreateSelectData
                        sd2.Mark = 4
                        for x in others:
                            x.Select4(True, sd2)
                        return d.FeatureManager.FeatureFillet3(1, r * m, 0, 0, 2, 0, 0, NUL, NUL, NUL, NUL, NUL, NUL, NUL)
                    rows[f'face_fillet_R{r:g}'] = attempt(d, f'SMOOTH face R{r:g}', make2)
                    if rows[f'face_fillet_R{r:g}']['built']:
                        undo(d)
                close(j.sw, d)
            RES['smooth_rim'] = rows
        for tag in [t for t in todo if t in ('smooth_sharp', 'smooth_r2')]:
            # the true-arc flange with the stem, sharp or with the 2 mm edge fillet, finished like the others for FEA
            d = new_part(j.sw, OUT / f'link_{tag}.SLDPRT')
            with Sk(d, plane(d, 'Z', 0.0, 'DISC_P'), 'DISC') as s:
                s.poly([(32.5, 4, 0), (15, 4, 0), (15, -4, 0), (32.5, -4, 0)], closed=False)
                s.arc((32.5, -1.5, 0), (32.5, -4, 0), (35, -1.5, 0), +1)
                s.poly([(35, -1.5, 0), (35, 1.5, 0)], closed=False)
                s.arc((32.5, 1.5, 0), (35, 1.5, 0), (32.5, 4, 0), +1)
                s.centerline((0, -10, 0), (0, 10, 0))
            revolve(d, s.feat, 'DISC')
            loft_sections(d, SEC, 'STEM')
            if tag == 'smooth_r2':
                d.ClearSelection2(True)
                for e in seam(d)[1]:
                    e.Select4(True, NUL)
                ff = d.FeatureManager.FeatureFillet3(3, 2.0 * m, 0, 0, 0, 0, 0, NUL, NUL, NUL, NUL, NUL, NUL, NUL)
                if ff is None:
                    raise Failed('smooth_r2: the fillet did not build')
                ff.Name = 'JUNCTION'
                d.ForceRebuild3(False)
            save(d)
            RES[f'link_{tag}'] = finish(j, d, tag)
            close(j.sw, d)
        for tag in [t for t in todo if t in ('sharp', *ROOT, *SKIRT)]:
            try:
                d = build_variant(j, tag)
                RES[f'link_{tag}'] = dict(seam=describe(d) if tag in ROOT or tag == 'sharp' else None, **finish(j, d, tag))
                close(j.sw, d)
            except Failed as ex:
                log(tag, 'FAILED', str(ex)[:200])
                RES[f'link_{tag}'] = dict(built=False, why=str(ex)[:200])
                j.sw.CloseAllDocuments(True)
        f.write_text(json.dumps(RES, indent=1))
    print(json.dumps(RES, indent=1))
