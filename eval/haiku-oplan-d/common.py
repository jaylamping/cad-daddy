"""Shared helpers for the haiku-oplan-d run: paths, results.json, ring positions, wall and measurement checks.

Run scripts with:  python eval/haiku-oplan-d/<script>.py   (never under timeout; see RULES.md)
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'solidworks'))
W = ROOT / '_wip' / 'sw-eval' / 'haiku-oplan-d'      # models (gitignored)
E = ROOT / 'eval' / 'haiku-oplan-d'                  # scripts, REPORT.md, results.json, pictures/
RESULTS = E / 'results.json'
W.mkdir(parents=True, exist_ok=True)
(E / 'pictures').mkdir(parents=True, exist_ok=True)


def load_results():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding='utf-8'))
    return {}


def save_result(task, obj):
    """Merge one task's object into results.json (one object per task, as TASKS_D.md asks)."""
    data = load_results()
    data[task] = obj
    RESULTS.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def ring(n, circ, rot, z=0.0):
    """n points on a circle of diameter circ, first at rot degrees from +X (model mm)."""
    r = circ / 2
    return [(r * math.cos(math.radians(rot + 360 * k / n)), r * math.sin(math.radians(rot + 360 * k / n)), z)
            for k in range(n)]


def walls(R, rb, feats):
    """Thinnest wall (mm) between the features and to the outside and the bore.

    feats: list of (x, y, r, kind) with kind 'through' or 'cbore'. Negative means the features overlap. Concentric
    pairs (a through hole inside its own counterbore) are not walls and are skipped.
    Returns (min wall, description, all walls as a list of (value, description)).
    """
    out = []
    for x, y, r, k in feats:
        c = math.hypot(x, y)
        out.append((R - (c + r), f'{k} -> OD'))
        out.append((c - r - rb, f'{k} -> bore'))
    for i in range(len(feats)):
        for j in range(i + 1, len(feats)):
            a, b = feats[i], feats[j]
            d = math.hypot(a[0] - b[0], a[1] - b[1])
            if d < 1e-3:
                continue
            out.append((d - a[2] - b[2], f'{a[3]} -> {b[3]}'))
    best = min(out)
    return best[0], best[1], out


def expect_close(what, got, want, tol_abs):
    """Record a check result without stopping: returns (ok, text)."""
    ok = abs(got - want) <= tol_abs
    return ok, f'{what}: got {got:.4f}, want {want:.4f}, diff {got - want:+.4f}, allowed {tol_abs}'
