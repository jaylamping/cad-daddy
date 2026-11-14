"""T5 step 1: read T3's results for every print direction (no solve). Needs t3_rows.json from T3.

Run from the worktree root: python eval/haiku-plan-a/t5_read.py   (reads only; no SolidWorks)
"""
import json
from pathlib import Path

from common import HERE, log, settled, sf_min  # noqa: E402

rows = json.loads((HERE / 't3_rows.json').read_text(encoding='utf-8'))
series = [rows[n] for n in ('T3_PADS_30', 'T3_PADS_22', 'T3_PADS_16')]
for k in 'XYZ':
    t = [s['table'][k] for s in series]
    log(k, 'finest', t[-1], 'sf_min', sf_min(t[-1]), 'converged', settled(t))
log('washers model', {k: sf_min(rows['T3_WASHERS']['table'][k]) for k in 'XYZ'} if 'T3_WASHERS' in rows else 'no washers row')
