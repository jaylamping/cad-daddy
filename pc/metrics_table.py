"""The benchmark's comparison table, from one metrics.json per run. Stdlib only.

    python pc/metrics_table.py [eval]            # a markdown table, one row per run, oldest first
    python pc/metrics_table.py eval --json

Each run owns eval/<run>/metrics.json, so runs made on different machines never touch the same file and git merges
them. Keys (any may be null when it was not recorded; nothing is filled in from memory):

    run, date, machine, set, model, plan ("none", or who wrote the plan the run built from), base_commit
    tasks: total, reached (started and reported), right (verdict and numbers hold), right_basis (who checked:
           "independent check", "review from files" or "own report, not checked")
    wall_minutes, waiting_minutes (launches, locks, hung dialogs, holds for another thread)
    cost_usd (as the session record gives it), cost_basis
    jobs, jobs_failed (from runs.log through pc/run_metrics.py, for runs made after 2026-11-14)
    notes

Derived here: working minutes, minutes and cost per task that was right, and failed jobs per task.
"""
import json
import sys
from pathlib import Path


def rows(root):
    out = []
    for f in sorted(Path(root).glob('*/metrics.json')):
        m = json.loads(f.read_text(encoding='utf-8'))
        t = m.get('tasks') or {}
        right, wall, wait, cost = t.get('right'), m.get('wall_minutes'), m.get('waiting_minutes') or 0, m.get('cost_usd')
        m['working_minutes'] = round(wall - wait, 1) if wall is not None else None
        m['minutes_per_right_task'] = round((wall - wait) / right, 1) if wall is not None and right else None
        m['cost_per_right_task'] = round(cost / right, 2) if cost is not None and right else None
        m['failed_jobs_per_task'] = (round(m['jobs_failed'] / t['reached'], 2)
                                     if m.get('jobs_failed') is not None and t.get('reached') else None)
        out.append(m)
    return sorted(out, key=lambda m: (m.get('date') or '', m.get('run') or ''))


def show(v):
    return '' if v is None else str(v)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    data = rows(args[0] if args else 'eval')
    if '--json' in sys.argv:
        print(json.dumps(data, indent=1))
        sys.exit(0)
    head = ['run', 'machine', 'set', 'model', 'plan', 'right / reached / total', 'checked by', 'wall min', 'waiting',
            'cost $', 'min per right task', '$ per right task', 'failed jobs per task']
    print('| ' + ' | '.join(head) + ' |')
    print('|' + ' --- |' * len(head))
    for m in data:
        t = m.get('tasks') or {}
        cells = [m.get('run'), m.get('machine'), m.get('set'), m.get('model'), m.get('plan'),
                 f"{show(t.get('right'))} / {show(t.get('reached'))} / {show(t.get('total'))}", t.get('right_basis'),
                 m.get('wall_minutes'), m.get('waiting_minutes'), m.get('cost_usd'), m['minutes_per_right_task'],
                 m['cost_per_right_task'], m['failed_jobs_per_task']]
        print('| ' + ' | '.join(show(c) for c in cells) + ' |')
