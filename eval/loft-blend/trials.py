"""Build the test part sharp, then try each way of blending the stem into the disc. Writes trials.json.

    python eval/loft-blend/trials.py            # every method
    python eval/loft-blend/trials.py m3 m4      # some

Parts land in _wip/loft-blend/ as tp_<method>.SLDPRT (the best radius of each), for fea.py to solve.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DISC_R, OUT, SEC, disc, sec, sections, stem, stem_at  # noqa: E402
from swkit import (NUL, Failed, Sk, call, close, edges_where, feature_errors, fillet, job, loft, log, m, new_part,  # noqa: E402
                   pick, plane, save, single_body, solid_bodies, volume, bodies, faces, face_info)

HERE = Path(__file__).resolve().parent
RES = {}


def base(j, name):
    d = new_part(j.sw, OUT / f'tp_{name}.SLDPRT')
    disc(d)
    stem(d)
    save(d)
    return d


def top_face(d):
    f = [x for x in pick(d, kind='plane', normal=(0, 0, 1)) if abs(face_info(x)['box'][2]) < 1e-6 and face_info(x)['area'] > 1000]
    if len(f) != 1:
        raise Failed(f'disc top face: {len(f)} found')
    return f[0]


def seam_edges(d):
    """Edges of the disc's top face that are not its rim: the seam where the stem lands."""
    out = []
    for e in call(top_face(d), 'GetEdges') or []:
        cp = e.GetCurveParams3
        mid = e.GetCurve.Evaluate2((cp.UMinValue + cp.UMaxValue) / 2, 0)
        if math.hypot(mid[0], mid[1]) * 1e3 < DISC_R - 1:
            out.append(e)
    return out


def stem_faces(d):
    """Side faces of the stem: not planar, and reaching above the disc."""
    return [f for f in faces(d) if face_info(f)['kind'] != 'plane' and face_info(f)['box'][5] > 1.0
            and face_info(f)['box'][3] < DISC_R - 1]


def undo_last(d, name):
    f = d.FeatureByPositionReverse(0)
    d.ClearSelection2(True)
    f.Select2(False, 0)
    d.Extension.DeleteSelection2(0)
    d.ForceRebuild3(False)


def try_radii(d, label, make, radii):
    """make(r) -> feature or None. Each radius is tried on the same part and removed again; returns what built."""
    rows = []
    for r in radii:
        v0 = volume(d)
        try:
            f = make(r)
        except Exception as ex:      # noqa: BLE001
            log(label, r, 'raised', str(ex)[:120])
            f = None
        if f is None:
            rows.append(dict(r=r, built=False))
            log(f'{label}: R{r} did not build')
            continue
        d.ForceRebuild3(False)
        errs = feature_errors(d)
        dv = volume(d) - v0
        nb = len(solid_bodies(d))
        rows.append(dict(r=r, built=not errs and dv > 0 and nb == 1, dv=round(dv, 2), errors=errs, bodies=nb))
        log(f'{label}: R{r} built, volume {dv:+.2f} mm3, errors {errs}, bodies {nb}')
        undo_last(d, label)
        if abs(volume(d) - v0) > 0.01:
            raise Failed(f'{label}: the trial feature was not removed cleanly')
    return rows


def keep(d, label, make, rows):
    """Rebuild the largest radius that built up to 4 mm (the FEA compares like with like), save, close."""
    ok = [x['r'] for x in rows if x['built']]
    pickr = max([r for r in ok if r <= 4.0], default=(min(ok) if ok else None))
    if pickr is not None:
        f = make(pickr)
        f.Name = label
        d.ForceRebuild3(False)
        single_body(d)
        save(d)
        log(f'{label}: kept R{pickr}, volume {volume(d):.1f}, errors {feature_errors(d)}')
    return pickr


RADII = (0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0)


def m0(j):
    """The house way: edges_where + fillet()."""
    d = base(j, 'm0')
    e = edges_where(d, lambda p: abs(p[2]) < 0.01 and math.hypot(p[0], p[1]) < DISC_R - 1)
    log('m0 edges_where found', len(e))
    r = fillet(d, e, (4.0, 3.0, 2.0, 1.0), 'M0') if e else None
    RES['m0_edges_where_fillet'] = dict(edges=len(e), radius=r, errors=feature_errors(d))
    close(j.sw, d)


def m1(j):
    """Edge fillet, edges taken from the disc top face's own edge list, tangent propagation on."""
    d = base(j, 'm1')
    log('m1 seam edges', len(seam_edges(d)), 'stem faces', len(stem_faces(d)))

    def make(r):
        d.ClearSelection2(True)
        for e in seam_edges(d):
            e.Select4(True, NUL)
        return d.FeatureManager.FeatureFillet3(3, r * m, 0, 0, 0, 0, 0, NUL, NUL, NUL, NUL, NUL, NUL, NUL)
    rows = try_radii(d, 'M1', make, RADII)
    RES['m1_edge_fillet_from_face'] = dict(edges=len(seam_edges(d)), rows=rows, kept=keep(d, 'M1', make, rows))
    close(j.sw, d)


def m2(j):
    """Face fillet: the stem's side faces against the disc's top face."""
    d = base(j, 'm2')
    out = {}
    for opt in (1, 3, 0):
        def make(r, opt=opt):
            d.ClearSelection2(True)
            sd = d.SelectionManager.CreateSelectData
            sd.Mark = 2
            for f in stem_faces(d):
                f.Select4(True, sd)
            sd2 = d.SelectionManager.CreateSelectData
            sd2.Mark = 4
            top_face(d).Select4(True, sd2)
            return d.FeatureManager.FeatureFillet3(opt, r * m, 0, 0, 2, 0, 0, NUL, NUL, NUL, NUL, NUL, NUL, NUL)
        rows = try_radii(d, f'M2_opt{opt}', make, RADII)
        out[f'options_{opt}'] = rows
        if any(x['built'] for x in rows):
            out['kept'] = keep(d, 'M2', make, rows)
            out['kept_options'] = opt
            break
    RES['m2_face_fillet'] = out
    close(j.sw, d)


def flare_secs(R, phis=(0, 20, 40, 60, 90)):
    """Sections that sweep a quarter-circle blend of radius R out of the stem: the first lies in the disc face."""
    out = []
    for p in phis:
        z = R * (1 - math.cos(math.radians(p)))
        off = R * (1 - math.sin(math.radians(p)))
        a, b, n = stem_at(z)
        out.append((z, a + off, b + off, n))
    a, b, n = stem_at(2 * R)
    out.append((2 * R, a, b, n))             # one plain section close above, so the blend cannot bulge the stem
    return out + [s for s in SEC[1:] if s[0] > 2 * R + 3]


def m3(j):
    """The round designed in: the stem's own loft ends on a flared section lying in the disc face."""
    rows = []
    for R in (1.0, 2.0, 4.0, 6.0, 8.0):
        d = new_part(j.sw, OUT / f'tp_m3_R{R:g}.SLDPRT')
        disc(d)
        v0 = volume(d)
        try:
            stem(d, flare_secs(R))
            d.ForceRebuild3(False)
            errs, nb = feature_errors(d), len(solid_bodies(d))
            rows.append(dict(r=R, built=not errs and nb == 1, dv=round(volume(d) - v0, 2), errors=errs, bodies=nb))
            save(d)
        except Failed as ex:
            rows.append(dict(r=R, built=False, why=str(ex)[:100]))
        log('M3', rows[-1])
        close(j.sw, d)
    RES['m3_flared_loft'] = dict(rows=rows)


def m4(j):
    """A separate lofted skirt over the sharp junction: flared section in the disc face up to a section just inside
    the stem, arriving square to that section (end tangency normal to profile)."""
    out = {}
    for label, end_type, n_mid in (('m4_skirt_2sec_normal_end', 1, 0), ('m4_skirt_2sec_plain', 0, 0), ('m4_skirt_arc', 0, 3)):
        rows = []
        for R in (1.0, 2.0, 4.0, 6.0, 8.0):
            d = base(j, f'{label}_R{R:g}')
            v0 = volume(d)
            a0, b0, n0 = stem_at(0.0)
            secs = [(0.0, a0 + R, b0 + R, n0)]
            for k in range(1, n_mid + 1):
                p = 90 * k / (n_mid + 1)
                z = R * (1 - math.cos(math.radians(p)))
                a, b, n = stem_at(z)
                off = R * (1 - math.sin(math.radians(p)))
                secs.append((z, a + off, b + off, n))
            a, b, n = stem_at(R)
            secs.append((R, a - 0.15, b - 0.15, n))               # 0.15 mm inside the stem: no coincident faces
            sks = sections(d, secs, 'SKIRT')
            f = None
            for merge in (True, False):
                d.ClearSelection2(True)
                for k in sks:
                    k.Select2(True, 1)
                f = d.FeatureManager.InsertProtrusionBlend2(False, True, False, 1.0, 0, end_type, 1.0, 1.0, True, True, False,
                                                            0, 0, 0, True, merge, merge, 0)
                if f is not None:
                    break
            if f is None:
                rows.append(dict(r=R, built=False))
            else:
                d.ForceRebuild3(False)
                errs, nb = feature_errors(d), len(solid_bodies(d))
                rows.append(dict(r=R, built=not errs and nb == 1, dv=round(volume(d) - v0, 2), errors=errs, bodies=nb))
                save(d)
            log(label, rows[-1])
            close(j.sw, d)
        out[label] = rows
    RES['m4_skirt'] = out


def m5(j):
    """Variable-radius fillet on the seam (only meaningful if the constant one half works)."""
    d = base(j, 'm5')

    def make(r):
        d.ClearSelection2(True)
        for e in seam_edges(d):
            e.Select4(True, NUL)
        return d.FeatureManager.FeatureFillet3(1 | 4, r * m, 0, 0, 1, 0, 0, NUL, NUL, NUL, NUL, NUL, NUL, NUL)
    rows = try_radii(d, 'M5', make, (1.0, 2.0, 4.0))
    RES['m5_variable_fillet'] = dict(rows=rows)
    close(j.sw, d)


ALL = dict(m0=m0, m1=m1, m2=m2, m3=m3, m4=m4, m5=m5)
if __name__ == '__main__':
    todo = sys.argv[1:] or list(ALL)
    f = HERE / 'trials.json'
    RES = json.loads(f.read_text()) if f.exists() else {}
    with job(wait_s=1800) as j:
        for k in todo:
            log('----', k)
            try:
                ALL[k](j)
            except Exception as ex:      # noqa: BLE001 - one method failing must not hide the others
                log(k, 'FAILED', repr(ex)[:300])
                RES[k + '_error'] = repr(ex)[:300]
                j.sw.CloseAllDocuments(True)
            f.write_text(json.dumps(RES, indent=1))
    print(json.dumps(RES, indent=1))
