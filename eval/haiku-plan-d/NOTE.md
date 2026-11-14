# haiku-plan-d: what this folder is

- Run: `haiku-plan-d`, task set D, done by model `claude-haiku-5-5` on 2026-11-14.
- Base commit of the run's worktree: `908f1cc` (detached HEAD, nothing committed by the run).
- Inputs: playbook plus per-task plans in a `plans/` folder at the worktree root. `plans/` came from branch `plan-execute` at `28d1b41` (`eval/plans-fable/`: README.md, common.py, D_D1 to D_D3; checked identical). The plans are in [../plans-fable/](../plans-fable/).
- Copied here: the run's `eval/haiku-plan-d/` folder as the run left it (scripts, REPORT.md, results.json, pictures).
- Added: `wip-logs/`, the job logs (`*.log`) the run wrote in `_wip/sw-eval/haiku-plan-d/`, because the report's numbers are in them.
- Left out: `.npz` nodal arrays, the SolidWorks models (`.SLDPRT`, `.STL`, `.step`) and the solver scratch in
  `_wip/sw-eval/haiku-plan-d/` (`*-BenchMark-Solver.txt`, `.gsz`, `.BDF`, `.BD2`, `.BMC`, `.CWR`, `.swb`, `solver_*.log`, `PerformanceLog.txt`).
  Those stay in the run's worktree on the CAD workstation.
- The run reports on itself. The independent check is in [../haiku-runs-CHECK.md](../haiku-runs-CHECK.md).
