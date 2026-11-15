"""One CAD job from open to close: its own name and folder, a count of review rounds, and what it cost and broke.

    python pc/cadjob.py open <slug> [--root DIR] [--lane decided|undecided] [--planner NAME] [--builder NAME]
    python pc/cadjob.py round <job folder>          # before each set of review fixes goes back to the builder
    python pc/cadjob.py close <job folder> [--right N --total N] [--cost USD] [--peek]

open makes <root>/<name>/ (root defaults to _wip/jobs under the current folder) and job.json in it. The name is the
slug, the date and four random characters, so two jobs never share a name: use it for the folder, the worktree, the
claim, and as the start of every part file and study name the job makes (playbook/09-pipeline.md says why). It
prints the name and the folder.

round adds one to the job's count of fix rounds and exits 1 instead of counting a fourth: by then the part needs a
new idea, not a correction (playbook/08-workflow.md).

close reads the job's own logs (runs.log from swkit.job(), times.log from swkit.stamp(), stall reports), writes
metrics.json beside them with the keys pc/metrics_table.py reads, and sorts the job's failures into kinds this PC
has seen before and kinds it has not, with the same rule and the same list as pc/sw_watch.py. Exit 1 when a kind is
new: it is fixed in the helpers or the playbook before the job is reported. --peek sorts without adding the new
kinds to the list. Numbers nobody gave (tasks right, cost) stay null; nothing is filled in from memory.
Stdlib only.
"""

from __future__ import annotations

import json
import platform
import re
import secrets
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_metrics
import sw_watch

SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,39}$")
MAX_ROUNDS = 3


def new_name(slug: str, now: float | None = None) -> str:
    if not SLUG.match(slug):
        raise SystemExit(f"slug {slug!r}: lower-case letters, digits and hyphens, at most 40, e.g. elbow-cable-rig")
    return f'{slug}-{time.strftime("%y%m%d", time.localtime(now))}-{secrets.token_hex(2)}'


def commit(folder: Path) -> str | None:
    try:
        out = subprocess.run(["git", "-C", str(folder), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
        return out.stdout.strip() or None
    except OSError:
        return None


def open_job(slug: str, root: Path, lane: str, planner: str | None, builder: str | None) -> Path:
    name = new_name(slug)
    folder = root / name
    folder.mkdir(parents=True)
    job = {"name": name, "opened": time.strftime("%Y-%m-%d %H:%M:%S %z"), "machine": platform.node().lower(), "lane": lane,
           "planner": planner, "builder": builder, "base_commit": commit(Path(__file__).parent), "rounds": 0}
    (folder / "job.json").write_text(json.dumps(job, indent=1), encoding="utf-8")
    return folder


def load(folder: Path) -> dict:
    path = folder / "job.json"
    if not path.exists():
        raise SystemExit(f"{folder} has no job.json: open the job with `cadjob.py open` first")
    return json.loads(path.read_text(encoding="utf-8"))


def next_round(folder: Path) -> int:
    job = load(folder)
    if job["rounds"] >= MAX_ROUNDS:
        raise SystemExit(f'{job["name"]} has had {MAX_ROUNDS} rounds of fixes. A fourth is a new idea, not a correction: '
                         f"stop sending fixes and take the part back to options (playbook/08-workflow.md).")
    job["rounds"] += 1
    (folder / "job.json").write_text(json.dumps(job, indent=1), encoding="utf-8")
    return job["rounds"]


def close_job(folder: Path, right: int | None, total: int | None, cost: float | None, seen: set[str]) -> dict:
    """The job's metrics and its failures sorted by kind. `seen` is the kinds this PC has met before."""
    job = load(folder)
    counted = run_metrics.read(folder)["total"]
    log = folder / "runs.log"
    rows = sw_watch.parse(log.read_text(encoding="utf-8"), str(folder)) if log.exists() else []
    kinds = sw_watch.sort(rows, 0.0, seen)
    stalls = sorted(p.name for p in folder.glob("stall_*.txt"))
    metrics = {"run": job["name"], "date": job["opened"][:10], "machine": job["machine"], "set": None,
               "model": job["builder"], "plan": job["planner"] or "none", "base_commit": job["base_commit"],
               "tasks": {"total": total, "reached": total, "right": right,
                         "right_basis": "review from files" if right is not None else None},
               "wall_minutes": counted["clock_minutes"], "waiting_minutes": None,
               "cost_usd": cost, "cost_basis": "given at close" if cost is not None else None,
               "jobs": counted["jobs"], "jobs_failed": counted["failed"],
               "notes": f'lane {job["lane"]}; {job["rounds"]} rounds of fixes; '
                        f'first-try pass share {counted["first_try_pass_share"]}; {len(stalls)} stall reports'}
    (folder / "metrics.json").write_text(json.dumps(metrics, indent=1), encoding="utf-8")
    return {"metrics": metrics, "new": kinds["new"], "again": kinds["again"], "stalls": stalls,
            "never_passed": counted["never_passed"]}


def option(argv: list[str], name: str, default: str | None = None) -> str | None:
    if name not in argv:
        return default
    i = argv.index(name)
    if i + 1 >= len(argv):
        raise SystemExit(f"{name} needs a value")
    value = argv[i + 1]
    del argv[i:i + 2]
    return value


def main(argv: list[str]) -> int:
    argv = list(argv)
    if len(argv) < 2 or argv[0] not in ("open", "round", "close"):
        raise SystemExit(__doc__)
    verb = argv.pop(0)
    if verb == "open":
        root = Path(option(argv, "--root", "_wip/jobs"))
        lane = option(argv, "--lane", "decided")
        if lane not in ("decided", "undecided"):
            raise SystemExit("--lane is decided or undecided")
        planner, builder = option(argv, "--planner"), option(argv, "--builder")
        if len(argv) != 1:
            raise SystemExit(__doc__)
        folder = open_job(argv[0], root, lane, planner, builder)
        print(f"job {folder.name}\nfolder {folder.resolve()}")
        return 0
    if verb == "round":
        print(f"round {next_round(Path(argv[0]))} of {MAX_ROUNDS}")
        return 0
    right, total, cost = option(argv, "--right"), option(argv, "--total"), option(argv, "--cost")
    peek = "--peek" in argv
    folder = Path([a for a in argv if not a.startswith("--")][0])
    path = sw_watch.state_file()
    state = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    res = close_job(folder, None if right is None else int(right), None if total is None else int(total),
                    None if cost is None else float(cost), set(state.get("seen", [])))
    if res["new"] and not peek:  # the daily look's "until" is left alone: it still reads every other folder from there
        state["seen"] = sorted(set(state.get("seen", [])) | set(res["new"]))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state, indent=1), encoding="utf-8")
    m = res["metrics"]
    print(f'{m["run"]}: {m["jobs"]} jobs, {m["jobs_failed"]} failed, {m["wall_minutes"]} min on the clock, '
          f'{len(res["stalls"])} stall reports, {len(res["new"])} new kinds of failure')
    for label in ("new", "again"):
        for k, g in res[label].items():
            print(f'{label.upper():5} x{g["count"]}  {g["example"][:200]}\n      scripts: {"; ".join(g["scripts"])}')
    if res["never_passed"]:
        print(f'never passed: {", ".join(res["never_passed"])}')
    if res["new"]:
        print("A new kind of failure: fix the helper or the playbook page before reporting the job (09-pipeline.md).")
    return 1 if res["new"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
