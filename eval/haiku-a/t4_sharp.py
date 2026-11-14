"""T4: the T1 bracket without the 4 mm inside-corner fillet, under the T3 remote load case.

    python eval/haiku-a/t4_sharp.py sharp     # the variant as specified: sharp inside corner
    python eval/haiku-a/t4_sharp.py r04       # the same part with the 0.4 mm radius the printed corner will have

The variant is a byte copy of bracket.SLDPRT with the INNER_FILLET feature deleted in SolidWorks, then saved as
bracket_sharp.SLDPRT (r04: bracket_sharp_r04.SLDPRT, with a 0.4 mm round put back on that edge). Writes
eval/haiku-a/t4_<mode>.json.
"""
import json
import math
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'solidworks'))
MODE = sys.argv[1] if len(sys.argv) > 1 else 'sharp'
sys.argv = [sys.argv[0], 'remote'] + sys.argv[2:]          # t3_study reads its case from argv: T4 uses the remote case
import t3_study as t3  # noqa: E402
from swfea import PETG, static  # noqa: E402
from swkit import bbox, bodies, edges_where, fillet, job, log, open_doc, pick, save, volume  # noqa: E402

OUT = ROOT / '_wip' / 'sw-eval' / 'haiku-a'
FILLET_HAND_MM3 = (1 - math.pi / 4) * 4.0 ** 2 * 50.0       # 171.68 mm3 the 4 mm round adds (T1)
CORNER_X, CORNER_Z = 6.0, 6.0


def build(j, dst):
    shutil.copyfile(OUT / 'bracket.SLDPRT', dst)
    d = open_doc(j.sw, dst)
    v_before = volume(d)
    feat = d.FeatureByName('INNER_FILLET')
    if feat is None:
        raise SystemExit('FAIL: no INNER_FILLET in the T1 model')
    d.ClearSelection2(True)
    feat.Select2(False, 0)
    d.Extension.DeleteSelection2(0)
    d.ForceRebuild3(False)
    v_sharp = volume(d)
    log(f'sharp: volume {v_sharp:.3f}, removed {v_before - v_sharp:.3f} (hand {FILLET_HAND_MM3:.3f})')
    if abs((v_before - v_sharp) - FILLET_HAND_MM3) > 0.01 * FILLET_HAND_MM3:
        raise SystemExit('FAIL: deleting the fillet did not remove its volume')
    if MODE == 'r04':
        edge = edges_where(d, lambda p: abs(p[0] - CORNER_X) < 0.01 and abs(p[2] - CORNER_Z) < 0.01)
        log('inside corner edges', len(edge))
        if len(edge) != 1 or fillet(d, edge, (0.4,), 'R04_CORNER') is None:
            raise SystemExit('FAIL: 0.4 mm round did not build')
        log(f'r04 volume {volume(d):.3f}')
    save(d)
    j.sw.CloseDoc(d.GetTitle)                       # reopened below, after the Simulation add-in is loaded
    return dst


def main():
    t0 = time.time()
    dst = OUT / ('bracket_sharp.SLDPRT' if MODE == 'sharp' else 'bracket_sharp_r04.SLDPRT')
    with job() as j:
        build(j, dst)
        cw = j.simulation()
        d = open_doc(j.sw, dst)
        d.ForceRebuild3(False)
        if len(bodies(d)) != 1:
            raise SystemExit(f'FAIL: {len(bodies(d))} bodies')
        log('bbox', [round(v, 3) for v in bbox(d)])
        holes = pick(d, kind='cyl', r=2.75)
        bore = pick(d, kind='cyl', r=11.0)
        if MODE == 'r04':                           # the 0.4 round is a face: pick it, not the sharp edge
            corner = pick(d, kind='cyl', r=0.4)
        else:
            corner = edges_where(d, lambda p: abs(p[0] - CORNER_X) < 0.01 and abs(p[2] - CORNER_Z) < 0.01)
        log('picks: holes', len(holes), 'bore', len(bore), 'corner edges', len(corner))
        if len(holes) != 4 or len(bore) != 1 or len(corner) != 1:
            raise SystemExit('FAIL: pick counts')
        loads = [('remote', bore, t3.BORE_C, (t3.F, 0.0, 0.0), (0.0, 0.0, 0.0))]
        rows = []
        for el in t3.SIZES:
            r = static(j, d, f'sh{MODE[:2]}{int(el * 10)}', PETG, fixtures=[('fixed', holes)], loads=loads, el=el,
                       ctrl=[(corner, 0.4), (holes, t3.CTRL)])
            keep = t3.mask_for(r, el, 'remote')
            vm, at = r.peak(keep)
            row = dict(el=el, nodes=r.nodes, peak_vm=round(vm, 3), peak_at=at,
                       layer_z=round(r.layer_stress((0, 0, 1), keep)[0], 3),
                       shear_z=round(r.layer_shear((0, 0, 1), keep)[0], 3),
                       reaction_N=[round(v, 3) for v in r.reaction], solve_s=round(r.seconds))
            rows.append(row)
            log('row', row)
        j.sw.CloseDoc(d.GetTitle)
    climb = [abs(rows[k]['peak_vm'] - rows[k - 1]['peak_vm']) / rows[k - 1]['peak_vm'] for k in range(1, len(rows))]
    out = dict(mode=MODE, rows=rows, relative_change_per_step=[round(c, 4) for c in climb],
               elapsed_s=round(time.time() - t0, 1))
    (ROOT / 'eval' / 'haiku-a' / f't4_{MODE}.json').write_text(json.dumps(out, indent=2, default=str), encoding='utf-8')
    print(json.dumps(out, indent=2, default=str))


if __name__ == '__main__':
    main()
