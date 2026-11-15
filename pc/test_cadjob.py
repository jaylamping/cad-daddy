"""Tests for the job script (pytest)."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cadjob
import sw_watch

# what swkit.job() writes when swfea.static() raises: the study name comes first, unquoted
STATIC_FAIL = "FAILED Failed: {}-tip: solve failed (24). 24 is a singular model (a body free to move) or out of memory"


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A job's copy of metrics.json goes to eval/jobs/ in the repository: point it at a scratch folder."""
    monkeypatch.setattr(cadjob, "REPO", tmp_path / "repo")
    monkeypatch.setenv("ROARK_CLAIMS_DIR", str(tmp_path / "claims"))
    return tmp_path


def runs_log(folder, *outcomes):
    (folder / "runs.log").write_text("".join(
        f"2026-11-15 03:0{i}:00 -0600\t60 s\tbuild.py\tpid {4100 + i}\t{o}\n" for i, o in enumerate(outcomes)),
        encoding="utf-8")


def test_a_job_name_and_a_suffix_fit_in_the_part_of_a_study_name_swfea_keeps(repo) -> None:
    """Guards: bug - static() keeps 24 characters of a study name. A long job name lost its random part there, and
    two studies of one job, or two jobs, got the same name: the shared names that built each other's mesh."""
    folder = cadjob.open_job("elbow-rig2", repo / "jobs", "decided", "fable", "haiku")
    assert len(folder.name) <= 16 and len(f"{folder.name}-tip-c2") <= 24
    with pytest.raises(SystemExit, match="at most 10"):
        cadjob.new_name("elbow-cable-rig")
    with pytest.raises(SystemExit):
        cadjob.new_name("../x")


def test_a_name_already_taken_is_drawn_again(repo, monkeypatch) -> None:
    """Guards: bug - two jobs may never share a folder; a clash must draw again, not stop with a traceback."""
    tokens = iter(["aaaa", "aaaa", "bbbb"])
    monkeypatch.setattr(cadjob.secrets, "token_hex", lambda n: next(tokens))
    first = cadjob.open_job("hub", repo / "jobs", "decided", None, None)
    second = cadjob.open_job("hub", repo / "jobs", "decided", None, None)
    assert (first.name, second.name) == ("jaaaa-hub", "jbbbb-hub")


def test_the_same_fault_in_two_jobs_is_one_kind(repo) -> None:
    """Guards: bug - every study name starts with its job's name, so without taking it out the same solve failure
    in each job counted as a new kind and the close gate fired on faults already known."""
    a = sw_watch.kind(STATIC_FAIL.format("j7f3a-rig"))
    assert a == sw_watch.kind(STATIC_FAIL.format("jbe0f-hub-long"))
    folder = cadjob.open_job("hub", repo / "jobs", "decided", "fable", "haiku")
    runs_log(folder, STATIC_FAIL.format(folder.name), "ok")
    res = cadjob.close_job(folder, seen={a})
    assert list(res["again"]) == [a] and not res["new"]


def test_a_fourth_round_is_refused_and_a_new_job_starts_from_none(repo) -> None:
    """Guards: bug - four rounds on the organic link (2026-11-14) removed every fault a check could name and it
    still ended under strength. After three the part goes back to options as a new job, which must not inherit the
    count, or its first round is refused at once."""
    folder = cadjob.open_job("link", repo / "jobs", "decided", "fable", "haiku")
    assert [cadjob.next_round(folder) for _ in range(3)] == [1, 2, 3]
    with pytest.raises(SystemExit, match="open a new one"):
        cadjob.next_round(folder)
    assert cadjob.next_round(cadjob.open_job("link", repo / "jobs", "undecided", "fable", None)) == 1


def test_close_counts_from_the_logs_and_leaves_what_nobody_gave_empty(repo) -> None:
    """Guards: bug - a job's numbers come from what swkit wrote; tasks nobody counted must stay null, not be
    copied from another number, or the table divides by the wrong one."""
    folder = cadjob.open_job("rig", repo / "jobs", "decided", "fable", "haiku")
    runs_log(folder, STATIC_FAIL.format(folder.name), "ok")
    res = cadjob.close_job(folder, seen=set(), total=3, right=1)
    assert res["metrics"]["tasks"] == {"total": 3, "reached": None, "right": 1, "right_basis": "review from files"}
    assert (res["metrics"]["jobs"], res["metrics"]["jobs_failed"]) == (2, 1)
    with pytest.raises(SystemExit, match="more than"):
        cadjob.close_job(folder, seen=set(), total=2, reached=3)


def test_a_stall_in_the_job_folder_is_a_failure_of_the_job(repo) -> None:
    """Guards: bug - a job that hangs on a hidden dialog and is killed leaves no line in its own runs.log; the
    stall line the watcher writes to the machine's log is the only trace, and close must see it."""
    folder = cadjob.open_job("rig", repo / "jobs", "decided", "fable", "haiku")
    runs_log(folder, "ok")
    machine = repo / "claims" / "runs.log"
    machine.parent.mkdir()
    report = folder.resolve() / "stall_4100_0300.txt"
    machine.write_text(f"2026-11-15 03:05:00 -0600\t180 s\tbuild.py\tpid 4100\tSTALLED at static; report {report}\tC:\\x\n"
                       f"2026-11-15 03:05:00 -0600\t180 s\tother.py\tpid 4200\tSTALLED at static; report C:\\other\\s.txt\tC:\\x\n",
                       encoding="utf-8")
    res = cadjob.close_job(folder, seen=set(), machine_log=machine)
    assert len(res["stalls"]) == 1 and len(res["new"]) == 1


def test_the_gate_stays_shut_until_the_fix_is_recorded_and_peek_writes_nothing(repo, capsys) -> None:
    """Guards: bug - the first close used to add a new kind to the known list, so a second close passed the gate
    with the fault unfixed. The daily look's mark must not move either."""
    folder = cadjob.open_job("rig", repo / "jobs", "decided", "fable", "haiku")
    runs_log(folder, STATIC_FAIL.format(folder.name))
    state = sw_watch.state_file()
    state.parent.mkdir(parents=True)
    state.write_text(json.dumps({"until": 123.0, "seen": []}), encoding="utf-8")

    assert cadjob.main(["close", str(folder), "--peek"]) == 1
    assert json.loads(state.read_text(encoding="utf-8"))["seen"] == [] and not (folder / "metrics.json").exists()
    assert cadjob.main(["close", str(folder)]) == 1
    assert cadjob.main(["close", str(folder), "--cost", "1.5"]) == 1          # known now, still not fixed
    saved = json.loads(state.read_text(encoding="utf-8"))
    assert saved["until"] == 123.0 and len(saved["seen"]) == 1
    assert (cadjob.REPO / "eval" / "jobs" / folder.name / "metrics.json").exists()
    assert cadjob.main(["close", str(folder), "--fixed", "https://example.invalid/pr/1"]) == 0
    assert cadjob.main(["close", str(folder)]) == 0


def test_a_folder_without_runs_log_is_not_a_clean_job(repo) -> None:
    """Guards: bug - scripts kept outside the job folder leave nothing to count; that read as 0 jobs, 0 failed."""
    folder = cadjob.open_job("rig", repo / "jobs", "decided", "fable", "haiku")
    assert cadjob.main(["close", str(folder)]) == 1
    assert json.loads((folder / "metrics.json").read_text(encoding="utf-8"))["jobs"] is None


def test_a_mistyped_option_is_refused() -> None:
    """Guards: bug - an option the script does not know was passed over, and the metrics came out empty."""
    with pytest.raises(SystemExit):
        cadjob.main(["close", "x", "--rigth", "1"])
    with pytest.raises(SystemExit):
        cadjob.main(["close", "--peek"])
