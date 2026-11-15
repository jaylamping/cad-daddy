"""Tests for when the VM tells the Mac to stay awake (pytest)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import keepawake


def test_the_mac_is_kept_awake_only_while_solidworks_works() -> None:
    """Guards: the Mac cut the VM to a quarter of its CPU power once Joey stepped away, doubling solve times
    (joey-vm, 2026-11-15); an idle SolidWorks or the always-running keeper must not keep the Mac awake for ever."""
    sw = {10: "sldworks.exe"}
    assert keepawake.busy({10: 5.0}, {10: 5.1}, sw, 15)[0] is False  # idle instance: 0.007 cores
    assert keepawake.busy({10: 5.0}, {10: 20.0}, sw, 15)[0] is True  # building or reading back: 1 core
    assert keepawake.busy({}, {11: 0.0}, {11: "star.exe"}, 15)[0] is True  # a solver counts however quiet
    assert keepawake.busy({}, {10: 3.0}, sw, 15)[0] is True  # new since the last look: counted from zero
    assert keepawake.busy({10: 5.0}, {}, {}, 15) == (False, "no SolidWorks running")
