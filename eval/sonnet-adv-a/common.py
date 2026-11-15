import json, sys
from pathlib import Path
ROOT = Path(r'J:\code\cad-daddy-wt\sw-eval-sonnet-adv-a')
sys.path.insert(0, str(ROOT / 'solidworks'))
RUN = ROOT / 'eval' / 'sonnet-adv-a'
WIP = ROOT / '_wip' / 'sw-eval' / 'sonnet-adv-a'
WIP.mkdir(parents=True, exist_ok=True)
DENS = 1.19e-3          # g per mm3 (PETG 1.19 g/cm3)


def put(task, **kw):
    """Merge keys into results.json under task."""
    p = RUN / 'results.json'
    d = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
    d.setdefault(task, {}).update(kw)
    p.write_text(json.dumps(d, indent=2), encoding='utf-8')
