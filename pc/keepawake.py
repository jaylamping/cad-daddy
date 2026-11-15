"""Keep the Mac awake while SolidWorks works inside a Parallels VM on it (joey-vm).

    python pc/keepawake.py watch          # run in the VM; beats while SolidWorks or its solver is busy
    python pc/keepawake.py install        # start `watch` at every logon (Startup folder) and start it now
    python pc/keepawake.py status         # is the watcher running, is the beat fresh, what is busy

The Mac gives the VM far less CPU once nobody is at it: on 2026-11-15 the same solve ran with the Mac's CPU at 46 W and
3.6 GHz while Joey was at the Mac, and at 13 W and 2.5 GHz, cores 52-72 % active, once he stepped away, so identical
solves took from 77 s to 172 s. Heat was never the limit (powermetrics thermal pressure Nominal in 299 of 305 samples).

The VM cannot run a command on the Mac, but both see the Mac home folder (\\\\Mac\\Home in Windows). While SolidWorks,
cwanalysisproc or star is busy, `watch` rewrites a beat file there every 15 s, and deletes it once they go quiet.
pc/keepawake_mac.sh, run on the Mac by launchd, keeps `caffeinate` running while any beat file is under two minutes
old and stops it otherwise, so a VM that crashes or shuts down cannot keep the Mac awake for ever.

Windows only for `watch` and `install`; needs psutil.
"""

from __future__ import annotations

import os
import socket
import sys
import time

BEAT_DIR = os.environ.get("KEEPAWAKE_DIR", r"\\Mac\Home\.keepawake")
SW_NAMES = ("sldworks.exe", "cwanalysisproc.exe", "star.exe")
SOLVERS = ("cwanalysisproc.exe", "star.exe")
EVERY_S = 15
BUSY_CORES = 0.10  # SolidWorks using a tenth of a core or more counts as work; an idle instance uses about 0.01
QUIET_LOOKS = 4  # stay awake through this many quiet looks in a row (a minute), e.g. between two solves of one script


def busy(cpu_before: dict[int, float], cpu_now: dict[int, float], names: dict[int, str], dt: float) -> tuple[bool, str]:
    """(busy, why) from the CPU seconds of each SolidWorks-family process at two looks dt seconds apart. A solver
    process counts as busy whatever its CPU: it lives only for a solve. A process that is new since the last look is
    counted from zero, so a fresh one doing work counts at once."""
    solver = sorted({names[p] for p in cpu_now if names[p] in SOLVERS})
    if solver:
        return True, f"solver running ({', '.join(solver)})"
    used = sum(cpu_now[p] - cpu_before.get(p, 0.0) for p in cpu_now)
    cores = used / dt if dt > 0 else 0.0
    if cores >= BUSY_CORES:
        return True, f"SolidWorks using {cores:.2f} cores"
    return False, f"SolidWorks idle ({cores:.2f} cores)" if cpu_now else "no SolidWorks running"


def _sample() -> tuple[dict[int, float], dict[int, str]]:
    import psutil

    cpu, names = {}, {}
    for p in psutil.process_iter(["name"]):
        name = (p.info["name"] or "").lower()
        if name in SW_NAMES:
            try:
                t = p.cpu_times()
                cpu[p.pid], names[p.pid] = t.user + t.system, name
            except psutil.Error:
                pass
    return cpu, names


def beat_path() -> str:
    return os.path.join(BEAT_DIR, f"{socket.gethostname().lower()}.beat")


def _beat(why: str) -> None:
    os.makedirs(BEAT_DIR, exist_ok=True)
    with open(beat_path(), "w") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {why}\n")


def _unbeat() -> None:
    try:
        os.remove(beat_path())
    except FileNotFoundError:
        pass


def watch() -> None:
    before, _ = _sample()
    t_before, quiet, awake = time.monotonic(), QUIET_LOOKS, None
    try:
        while True:
            time.sleep(EVERY_S)
            now, names = _sample()
            t_now = time.monotonic()
            is_busy, why = busy(before, now, names, t_now - t_before)
            before, t_before = now, t_now
            quiet = 0 if is_busy else quiet + 1
            try:
                if quiet < QUIET_LOOKS:
                    _beat(why)
                else:
                    _unbeat()
            except OSError as e:  # the shared folder can be missing for a while (Parallels Tools restarting)
                why = f"beat folder not reachable ({e})"
            state = quiet < QUIET_LOOKS
            if state != awake:
                print(f"{time.strftime('%H:%M:%S')} {'keep Mac awake' if state else 'let Mac sleep'}: {why}", flush=True)
                awake = state
    finally:
        try:
            _unbeat()
        except OSError:
            pass


def _startup_file() -> str:
    return os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup", "keepawake.cmd")


def install() -> None:
    import subprocess

    pyw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    if not os.path.exists(pyw):
        pyw = sys.executable
    log = os.path.join(os.environ.get("TEMP", os.path.dirname(os.path.abspath(__file__))), "keepawake.log")
    me = os.path.abspath(__file__)
    with open(_startup_file(), "w") as f:
        f.write(f'@start "" /b "{pyw}" "{me}" watch >> "{log}" 2>&1\n')
    if not _watcher_pids():
        subprocess.Popen(["cmd", "/c", _startup_file()], creationflags=0x08000000)  # CREATE_NO_WINDOW
    print(f"installed: {_startup_file()}; log {log}")


def _watcher_pids() -> list[int]:
    import psutil

    me = os.path.basename(__file__)
    out = []
    for p in psutil.process_iter(["pid", "cmdline"]):
        cmd = p.info["cmdline"] or []
        if p.info["pid"] != os.getpid() and any(c.endswith(me) for c in cmd) and "watch" in cmd:
            out.append(p.info["pid"])
    return out


def status() -> int:
    print(f"watcher: {'running, PID ' + ', '.join(map(str, _watcher_pids())) if _watcher_pids() else 'NOT running'}")
    try:
        age = time.time() - os.path.getmtime(beat_path())
        print(f"beat: {beat_path()} written {age:.0f} s ago ({'fresh' if age < 120 else 'stale'})")
    except OSError:
        print(f"beat: none at {beat_path()} (Mac allowed to sleep)")
    before, _ = _sample()
    time.sleep(3)
    now, names = _sample()
    print("now:", busy(before, now, names, 3.0)[1])
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "watch":
        watch()
    elif cmd == "install":
        install()
    elif cmd == "status":
        sys.exit(status())
    else:
        print(__doc__)
        sys.exit(2)
