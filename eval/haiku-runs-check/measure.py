"""Re-measure the models the four haiku runs saved. Opens COPIES (in _wip/check/) in its own SolidWorks instance and
writes every body, face (kind, radius, axis, box, area) and feature name to measured.json. Nothing in the runs'
worktrees is written.

    python eval/haiku-runs-check/measure.py
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
RUNS = ['haiku-a', 'haiku-plan-a', 'haiku-d', 'haiku-plan-d']
SKIP = ('pad_', 'washer_', 'screw_', 'pin_end', 'pin_mid')      # FEA stand-in bodies, measured inside the assemblies


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
    elif s.IsCone:
        row.update(kind='cone')
    elif s.IsTorus:
        row.update(kind='torus')
    return row


def main():
    out = {}
    with job() as j:
        for run in RUNS:
            src = WT / f'sw-eval-{run}' / '_wip' / 'sw-eval' / run
            dst = ROOT / '_wip' / 'check' / run
            for p in sorted(src.rglob('*.SLDPRT')):
                if p.name.startswith(SKIP) or p.name.startswith('~$'):
                    continue
                rel = p.relative_to(src)
                q = dst / rel
                q.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, q)
                key = f'{run}/{rel.as_posix()}'
                try:
                    d = open_doc(j.sw, q)
                    out[key] = dict(volume=round(volume(d), 4), bbox=[round(v, 4) for v in bbox(d)], bodies=bodies(d),
                                    features=features(d),
                                    faces=[dict(body=b.Name, **face_row(f)) for b in solid_bodies(d)
                                           for f in (call(b, 'GetFaces') or [])])
                    log('measured', key, out[key]['volume'], len(out[key]['faces']), 'faces')
                    close(j.sw, d)
                except Exception as ex:  # noqa: BLE001
                    out[key] = dict(error=repr(ex))
                    log('FAILED', key, repr(ex))
                (HERE / 'measured.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
