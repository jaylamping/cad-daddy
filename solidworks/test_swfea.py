"""Tests for the parts of swfea that need no SolidWorks (pytest). Windows only: the module imports pywin32."""

import sys
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("win32gui", reason="swfea is Windows only")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import swfea


def test_the_fast_stress_read_is_used_only_when_it_covers_the_mesh():
    """Guards: bug - reading stresses over the bodies is 5 times faster than GetStress (shoulder hub, 2026-11-13) but
    lists a node on two bodies twice, and a read that missed a body would score a part on some of its nodes only."""
    ids = [5, 2, 9, 2]  # node 2 lies on two bodies
    value = {2: 1.0, 5: 2.0, 9: 3.0}
    parts = [(col, np.c_[ids, [value[i] * col for i in ids]]) for col in (1, 2, 3, 4, 5, 6, 10)]
    s = swfea.stress_table(parts, {2, 5, 9})
    assert s[:, 0].tolist() == [2, 5, 9]
    assert s[:, 10].tolist() == [10.0, 20.0, 30.0]
    t = np.array([[s[0, 1], s[0, 4], s[0, 5]], [s[0, 4], s[0, 2], s[0, 6]], [s[0, 5], s[0, 6], s[0, 3]]])
    assert np.allclose(np.linalg.eigvalsh(t)[::-1], s[0, 7:10])
    assert swfea.stress_table(parts, {2, 5, 9, 11}) is None  # the mesh has a node the read did not return
    assert swfea.stress_table(parts[:-1] + [(10, np.c_[[2, 5, 8], [1, 2, 3]])], None) is None  # components disagree
    vm = swfea.stress_table(parts[-1:], {2, 5, 9})  # stress='vm': von Mises only, the rest left unknown
    assert vm[:, 10].tolist() == [10.0, 20.0, 30.0] and np.isnan(vm[:, 1:10]).all() and np.isnan(vm[:, 11]).all()


def test_the_fast_node_displacement_and_reaction_reads_are_used_only_when_they_cover_the_mesh():
    """Guards: bug - the reads over the bodies list a node on two bodies twice, which would count its reaction twice,
    and a read that missed a body would report a reaction and a peak displacement from part of the model."""
    ids = [5, 2, 9, 2]  # node 2 lies on two bodies
    comps = [np.c_[ids, [i * k for i in ids]] for k in (1.0, 2.0, 2.0)]
    d = swfea.disp_table(comps, {2, 5, 9})
    assert d[:, 0].tolist() == [2, 5, 9]
    assert d[0].tolist() == [2, 2.0, 4.0, 4.0, 6.0]  # the resultant is computed
    assert swfea.reaction_total(comps, {2, 5, 9}) == [16.0, 32.0, 32.0, 48.0]  # node 2 counted once
    assert swfea.disp_table(comps, {2, 5, 9, 11}) is None  # the mesh has a node the read did not return
    assert swfea.reaction_total(comps[:2] + [np.c_[[2, 5, 8], [1, 2, 3]]], {2, 5, 9}) is None  # components disagree
    bodies = [np.c_[[5, 2], [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]], np.c_[[9, 2], [[2.0, 0.0, 0.0], [1.0, 0.0, 0.0]]]]
    assert swfea.node_coords(bodies, 3)[:, :2].tolist() == [[2, 1.0], [5, 0.0], [9, 2.0]]
    assert swfea.node_coords(bodies, 4) is None  # the mesh has more nodes than the bodies returned


def test_reactions_read_over_the_fixture_faces_count_each_node_once():
    """Guards: a read over the bodies costs a pass over the whole mesh (~25 s at 500k nodes, joey-vm 2026-11-15), so
    reactions are read over the fixture faces; a node on the edge between two of them is listed by both."""
    ids = [3, 4, 4, 7]  # node 4 is on two fixture faces
    comps = [np.c_[ids, [1.0, 2.0, 2.0, 3.0]], np.c_[ids, [0.0, 0.0, 0.0, 0.0]], np.c_[ids, [-1.0, -1.0, -1.0, -1.0]]]
    assert swfea.face_reaction_total(comps) == [6.0, 0.0, -3.0, round(45 ** 0.5, 3)]
    assert swfea.face_reaction_total(comps[:2] + [np.c_[[3, 4, 8], [1, 2, 3]]]) is None  # components disagree
    assert swfea.face_reaction_total([]) is None


def test_node_limits_follow_the_solver_and_the_machine(monkeypatch):
    """Guards: bug - one 450,000-node limit, set for direct sparse on holly-pc's 32 GB, refused FFEPlus jobs that solve
    at 1.68M nodes and direct-sparse jobs that fit joey-vm's 80 GB; direct sparse ran out of 80 GB at 910,000 (joey-vm,
    2026-11-15). The limit follows the solver and the memory, never below what fits holly-pc, and can be overridden."""
    for name in ("SWFEA_MAX_NODES_DIRECT", "SWFEA_MAX_NODES_FFEPLUS"):
        monkeypatch.delenv(name, raising=False)

    def ram(gb):
        monkeypatch.setattr(swfea.psutil, "virtual_memory", lambda: type("M", (), {"total": gb * 2**30})())

    ram(32)
    assert swfea.node_limit(swfea.SOLVER_DIRECT) == swfea.MAX_NODES == 450_000
    assert swfea.node_limit(None) == 450_000  # Automatic shares the direct limit
    ram(80)
    assert 700_000 <= swfea.node_limit(swfea.SOLVER_DIRECT) < 910_000
    assert swfea.node_limit(swfea.SOLVER_FFEPLUS) == 2_000_000
    monkeypatch.setenv("SWFEA_MAX_NODES_DIRECT", "300000")
    monkeypatch.setenv("SWFEA_MAX_NODES_FFEPLUS", "900000")
    assert swfea.node_limit(swfea.SOLVER_DIRECT) == 300_000
    assert swfea.node_limit(swfea.SOLVER_FFEPLUS) == 900_000
