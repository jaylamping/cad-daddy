"""One CAD job from open to close: its own name and folder, a count of review rounds, and what it cost and broke.

    python pc/cadjob.py open <slug> [--lane decided|undecided] [--planner NAME] [--builder NAME] [--root DIR]
    python pc/cadjob.py round <job folder>          # the planner, before each set of fixes goes back to the builder
    python pc/cadjob.py close <job folder> [--total N] [--reached N] [--right N] [--cost USD] [--peek]
    python pc/cadjob.py close <job folder> --fixed <link to the fix>

open makes <root>/<name>/ and job.json in it. The root is the folder beside this repository's checkout called jobs
(C:\\code\\jobs on joey-vm). The name is j, four random hex characters, a hyphen and the slug, for example
j7f3a-elbow-rig: at most 16 characters, so that it and a short suffix fit in the 24 characters swfea.static() keeps of
a study name. Use it for the folder, the worktree, the claim, and as the start of every part file and study name the
job makes (playbook/09-pipeline.md says why). A name already in the root is drawn again; two roots are not compared.

round adds one to the job's count of fix rounds and exits 1 instead of counting a fourth: by then the part needs a
new idea, not a correction, and the idea is a new job (playbook/08-workflow.md).

close reads the job's runs.log (swkit.job()), its times.log (swkit.stamp()), the STALLED lines whose report is in the
job folder (sw_instance.stall_watch writes them to the claims folder's runs.log) and, on Windows, crashes and hangs of
SolidWorks since the job opened. It writes metrics.json in the job folder and a copy in this repository's
eval/jobs/<name>/, which pc/metrics_table.py reads, and sorts the failures into kinds this PC has seen and kinds it
has not, with the rule and the list of pc/sw_watch.py. A new kind is added to that list and kept in job.json as
unfixed. close exits 1 while the job has unfixed kinds, on every run, until `--fixed <link>` records the fix.
--peek sorts and writes nothing. Numbers nobody gave (tasks, cost) stay null: nothing is filled in from memory.
Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
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

REPO = Path(__file__).resolve().parent.parent
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,9}$")
MAX_ROUNDS = 3
TRIES = 5


def new_name(slug: str) -> str:
    if not SLUG.match(slug):
        raise SystemExit(f"slug {slug!r}: lower-case letters, digits and hyphens, at most 10, e.g. elbow-rig")
    return f"j{secrets.token_hex(2)}-{slug}"


def commit(folder: Path) -> str | None:
    try:
        out = subprocess.run(["git", "-C", str(folder), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
        return out.stdout.strip() or None
    except OSError:
        return None


def open_job(slug: str, root: Path, lane: str, planner: str | None, builder: str | None) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    for _ in range(TRIES):
        folder = root / new_name(slug)
        try:
            folder.mkdir()
            break
        except FileExistsError:
            continue
    else:
        raise SystemExit(f"{TRIES} names drawn for {slug!r} were all taken in {root}")
    job = {"name": folder.name, "opened": time.strftime("%Y-%m-%d %H:%M:%S %z"), "opened_ts": time.time(),
           "machine": platform.node().lower(), "lane": lane, "planner": planner, "builder": builder,
           "base_commit": commit(REPO), "rounds": 0, "unfixed": [], "fixed": []}
    save(folder, job)
    return folder


def load(folder: Path) -> dict:
    path = folder / "job.json"
    if not path.exists():
        raise SystemExit(f"{folder} has no job.json: open the job with `cadjob.py open` first")
    return json.loads(path.read_text(encoding="utf-8"))


def save(folder: Path, job: dict) -> None:
    (folder / "job.json").write_text(json.dumps(job, indent=1), encoding="utf-8")


def next_round(folder: Path) -> int:
    job = load(folder)
    if job["rounds"] >= MAX_ROUNDS:
        raise SystemExit(f'{job["name"]} has had {MAX_ROUNDS} rounds of fixes. A fourth is a new idea, not a correction: '
                         f"close this job and open a new one for the options (playbook/09-pipeline.md, step 7).")
    job["rounds"] += 1
    save(folder, job)
    return job["rounds"]


def stalls(folder: Path, machine_log: Path) -> list[dict]:
    """The STALLED lines in the machine's runs.log whose report sits in this job folder."""
    if not machine_log.exists():
        return []
    here = str(folder.resolve()).lower()
    return [r for r in sw_watch.parse(machine_log.read_text(encoding="utf-8", errors="replace"), str(machine_log.parent))
            if r["outcome"].startswith("STALLED") and here in r["outcome"].lower()]


def close_job(folder: Path, seen: set[str], total: int | None = None, reached: int | None = None,
              right: int | None = None, cost: float | None = None, machine_log: Path | None = None,
              crashed: list[dict] | None = None) -> dict:
    """The job's metrics and its failures sorted by kind. `seen` is the kinds this PC has met before."""
    for a, b, what in ((reached, total, "--reached is more than --total"), (right, reached if reached is not None else total,
                                                                             "--right is more than the tasks reached")):
        if a is not None and b is not None and a > b:
            raise SystemExit(what)
    if any(v is not None and v < 0 for v in (total, reached, right, cost)):
        raise SystemExit("counts and cost cannot be negative")
    job = load(folder)
    log = folder / "runs.log"
    counted = run_metrics.read(folder)["total"] if log.exists() else None
    rows = sw_watch.parse(log.read_text(encoding="utf-8", errors="replace"), str(folder)) if log.exists() else []
    stalled = stalls(folder, machine_log) if machine_log else []
    kinds = sw_watch.sort(rows + stalled, 0.0, seen, crashed)
    metrics = {"run": job["name"], "date": job["opened"][:10], "machine": job["machine"], "set": "job",
               "model": job["builder"], "plan": job["planner"] or "none", "base_commit": job["base_commit"],
               "tasks": {"total": total, "reached": reached, "right": right,
                         "right_basis": "review from files" if right is not None else None},
               "wall_minutes": counted["clock_minutes"] if counted else None, "waiting_minutes": None,
               "cost_usd": cost, "cost_basis": "given at close" if cost is not None else None,
               "jobs": counted["jobs"] if counted else None, "jobs_failed": counted["failed"] if counted else None,
               "notes": f'lane {job["lane"]}; {job["rounds"]} rounds of fixes; '
                        f'first-try pass share {counted["first_try_pass_share"] if counted else None}; '
                        f'{len(stalled)} stalls; {"?" if crashed is None else len(crashed)} SolidWorks crashes or '
                        f'hangs on the machine while it was open'}
    return {"job": job, "metrics": metrics, "new": kinds["new"], "again": kinds["again"], "stalls": stalled,
            "no_log": not log.exists(), "never_passed": counted["never_passed"] if counted else []}


def write_close(folder: Path, res: dict, state: Path) -> None:
    job = res["job"]
    job["unfixed"] = sorted(set(job["unfixed"]) | set(res["new"]))
    save(folder, job)
    text = json.dumps(res["metrics"], indent=1)
    (folder / "metrics.json").write_text(text, encoding="utf-8")
    keep = REPO / "eval" / "jobs" / job["name"]
    keep.mkdir(parents=True, exist_ok=True)
    (keep / "metrics.json").write_text(text, encoding="utf-8")
    if res["new"]:  # the daily look's mark is left where it is: it still reads every other folder from there
        sw_watch.save_state(state, seen=res["new"])


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cadjob.py", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="verb", required=True)
    o = sub.add_parser("open")
    o.add_argument("slug")
    o.add_argument("--lane", choices=("decided", "undecided"), default="decided")
    o.add_argument("--planner")
    o.add_argument("--builder")
    o.add_argument("--root", type=Path, default=REPO.parent / "jobs")
    r = sub.add_parser("round")
    r.add_argument("folder", type=Path)
    c = sub.add_parser("close")
    c.add_argument("folder", type=Path)
    for name in ("--total", "--reached", "--right"):
        c.add_argument(name, type=int)
    c.add_argument("--cost", type=float)
    c.add_argument("--peek", action="store_true")
    c.add_argument("--fixed", metavar="LINK", help="the fix for this job's new kinds of failure is in LINK")
    return p


def main(argv: list[str]) -> int:
    a = parser().parse_args(argv)
    if a.verb == "open":
        folder = open_job(a.slug, a.root, a.lane, a.planner, a.builder)
        print(f"job {folder.name}\nfolder {folder.resolve()}")
        return 0
    if a.verb == "round":
        print(f"round {next_round(a.folder)} of {MAX_ROUNDS}")
        return 0
    if a.fixed:
        job = load(a.folder)
        job["fixed"].append({"kinds": job["unfixed"], "fix": a.fixed})
        job["unfixed"] = []
        save(a.folder, job)
        print(f'{job["name"]}: fix recorded, {len(job["fixed"][-1]["kinds"])} kinds')
        return 0
    state = sw_watch.state_file()
    seen = set(json.loads(state.read_text(encoding="utf-8")).get("seen", [])) if state.exists() else set()
    opened = load(a.folder).get("opened_ts", 0.0)
    res = close_job(a.folder, seen, a.total, a.reached, a.right, a.cost, state.with_name("runs.log"),
                    sw_watch.crashes(opened) if os.name == "nt" else None)
    if not a.peek:
        write_close(a.folder, res, state)
    m = res["metrics"]
    print(f'{m["run"]}: {m["jobs"]} jobs, {m["jobs_failed"]} failed, {m["wall_minutes"]} min on the clock, '
          f'{len(res["stalls"])} stalls, {len(res["new"])} new kinds of failure')
    for label in ("new", "again"):
        for k, g in res[label].items():
            print(f'{label.upper():5} x{g["count"]}  {g["example"][:200]}\n      scripts: {"; ".join(g["scripts"])}')
    if res["never_passed"]:
        print(f'never passed: {", ".join(res["never_passed"])}')
    unfixed = set(res["job"]["unfixed"]) | set(res["new"])
    if res["no_log"]:
        print(f"no runs.log in {a.folder}: nothing to count. The builder keeps its scripts in the job folder.")
    if unfixed:
        print(f"{len(unfixed)} kinds of failure new to this PC and not fixed yet: fix the helper or the page, then "
              f"`cadjob.py close {a.folder} --fixed <link>` (09-pipeline.md).")
    return 1 if unfixed or res["no_log"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
