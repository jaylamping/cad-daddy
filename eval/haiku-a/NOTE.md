# haiku-a: what this folder is

- Run: `haiku-a`, task set A, done by model `claude-haiku-5-5` on 2026-11-14.
- Base commit of the run's worktree: `908f1cc` (detached HEAD, nothing committed by the run).
- Inputs: playbook only (no plans).
- Copied here: the run's `eval/haiku-a/` folder as the run left it (scripts, REPORT.md, results.json, pictures).
- Added: `wip-logs/`, the job logs (`*.log`) the run wrote in `_wip/sw-eval/haiku-a/`, because the report's numbers are in them.
- Left out: `.npz` nodal arrays, the SolidWorks models (`.SLDPRT`, `.STL`, `.step`) and the solver scratch in
  `_wip/sw-eval/haiku-a/` (`*-BenchMark-Solver.txt`, `.gsz`, `.BDF`, `.BD2`, `.BMC`, `.CWR`, `.swb`, `solver_*.log`, `PerformanceLog.txt`).
  Those stay in the run's worktree on the CAD workstation.
- The run reports on itself. The independent check is in [../haiku-runs-CHECK.md](../haiku-runs-CHECK.md).
