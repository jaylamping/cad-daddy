"""Re-measure the models round two saved or wrote to again: the T5 bracket with rounded rib toes and its loaded twin
(new), and the three round-one models that round two's studies were run in and saved back to. Opens COPIES
(in _wip/check-followup/) in its own SolidWorks instance and writes volume, mass, box, bodies, features and every
face (kind, radius, axis, box, area) to measured.json. Nothing in the run's worktree is written.

    python eval/haiku-followup-check/measure.py
"""
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'solidworks'))
from swkit import *  # noqa: E402,F403

WT = Path(r'J:\code\cad-daddy-wt')
PARTS = [('haiku-plan-a', n) for n in ('bracket_c2.SLDPRT', 'bracket_c2_ld.SLDPRT', 'bracket_c.SLDPRT', 'block_fea.SLDPRT')]     + [('haiku-plan-d', n) for n in ('buck_mount.SLDPRT', 'housing_fea.SLDPRT')]


def features(d):
    out, f = [], d.FirstFeature
    while f is not None:
        out.append([f.Name, f.GetTypeName2])
        f = f.GetNextFeature
    return out


def face_row(f):
    s = f.GetSurface
    x = [v * 1e3 for v in call(f, 'GetBox')]
    box = [round(min(x[i], x[i + 3]), 4) for i in range(3)] + [round(max(x[i], x[i + 3]), 4) for i in range(3)]
    row = dict(kind='other', box=box, area=round(call(f, 'GetArea') * 1e6, 4))
    if s.IsCylinder:
        p = list(s.CylinderParams)
        row.update(kind='cyl', r=round(p[6] * 1e3, 5), origin=[round(v * 1e3, 4) for v in p[:3]],
                   axis=[round(v, 5) for v in p[3:6]])
    elif s.IsPlane:
        row.update(kind='plane', normal=[round(v, 5) for v in f.Normal])
    return row


out = {}
with job() as j:
    for run, part in PARTS:
        name = f'{run}/{part}'
        q = ROOT / '_wip' / 'check-followup' / run / part
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(WT / f'sw-eval-{run}' / '_wip' / 'sw-eval' / run / part, q)
        d = open_doc(j.sw, q)
        out[name] = dict(volume=round(volume(d), 4), bbox=[round(v, 4) for v in bbox(d)], bodies=bodies(d),
                         rebuild_errors=feature_errors(d), features=features(d),
                         faces=[dict(body=b.Name, **face_row(f)) for b in solid_bodies(d)
                                for f in (call(b, 'GetFaces') or [])])
        log('measured', name, out[name]['volume'], len(out[name]['faces']), 'faces')
        close(j.sw, d)
        (HERE / 'measured.json').write_text(json.dumps(out, indent=1))
