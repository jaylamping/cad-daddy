"""Tests for the job script (pytest)."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cadjob
import sw_watch


def test_two_jobs_with_one_slug_get_different_names() -> None:
    """Guards: bug - SolidWorks instances that solved at once under the same file and study names built each
    other's mesh (joey-vm, 2026-11-15). The job name is what keeps them apart, so it may never repeat."""
    names = {cadjob.new_name("hub", now=0.0) for _ in range(50)}
    assert len(names) == 50 and all(n.startswith("hub-") for n in names)


def test_a_fourth_round_of_fixes_is_refused(tmp_path: Path) -> None:
    """Guards: bug - four rounds of fixes on the organic link (2026-11-14) removed every fault a check could name
    and it still ended under strength: after three the part needs a new idea."""
    folder = cadjob.open_job("link", tmp_path, "decided", "fable", "haiku")
    assert [cadjob.next_round(folder) for _ in range(3)] == [1, 2, 3]
    with pytest.raises(SystemExit, match="new idea"):
        cadjob.next_round(folder)


def test_close_counts_from_the_logs_and_tells_a_new_kind_of_failure_from_a_known_one(tmp_path: Path) -> None:
    """Guards: bug - a job's numbers come from what swkit wrote, and a fault this PC has met before must not be
    reported as new, or the one that is new gets buried."""
    folder = cadjob.open_job("rig", tmp_path, "decided", "fable", "haiku")
    (folder / "runs.log").write_text("\n".join([
        "2026-11-15 03:00:00 -0600\t95 s\tbuild.py\tpid 4100\tFailed: solve of 'A' ended with code 24 at 746211 nodes",
        "2026-11-15 03:05:00 -0600\t60 s\tbuild.py\tpid 4101\tok",
        "2026-11-15 03:10:00 -0600\t30 s\tstudy.py\tpid 4102\tFailed: import of C:\\code\\x\\plate.step did not return",
    ]), encoding="utf-8")
    known = sw_watch.kind("Failed: solve of 'B' ended with code 24 at 5 nodes")

    res = cadjob.close_job(folder, right=1, total=2, cost=None, seen={known})

    assert list(res["again"]) == [known] and len(res["new"]) == 1
    assert res["never_passed"] == ["study.py"]
    written = json.loads((folder / "metrics.json").read_text(encoding="utf-8"))
    assert (written["jobs"], written["jobs_failed"], written["cost_usd"]) == (3, 2, None)
    assert written["tasks"] == {"total": 2, "reached": 2, "right": 1, "right_basis": "review from files"}
