# cad-daddy

Everything a model needs to do scripted CAD work and get it right: helper code that refuses to carry on after a silent
failure, a playbook of what was learned the hard way, and a benchmark with checkable answers that says how well a given
model does with them. It starts with SolidWorks (modelling, export, static studies with contact) driven from python.

It is written for any model, large or small, closed or open: the helpers are plain python, the playbook is plain
markdown, and the benchmark grades results, not style.

## Layout

| Folder | What it holds |
| --- | --- |
| [solidworks/](solidworks/) | `swkit.py` (modelling), `swfea.py` (static studies), `sheet.py` (picture sheets and shape numbers), `sw_instance.py` (one instance per job), `selftest.py` (103 checks against hand answers), [RULES.md](solidworks/RULES.md) |
| [playbook/](playbook/README.md) | The pages a session reads before it works: session, COM, modelling, export, FEA, judgment, what finished means; and [EVAL.md](playbook/EVAL.md), what was measured |
| [eval/](eval/) | Four task sets (routine, depth, design sense, stress) and every graded run, with its scripts, report and pictures |
| [pc/](pc/) | `capped.py` (a python job under a hard memory cap), `claims.py` (who is using the shared machine) |

## Start here

1. Read [playbook/README.md](playbook/README.md) and the seven pages it lists.
2. On a Windows machine with SolidWorks and Simulation: `python solidworks/selftest.py`. It must print PASS.
3. To measure a model: [playbook/EVAL.md](playbook/EVAL.md#running-it-on-another-model).

## What is still specific to where it was proven

The content was proven in [jaylamping/roark](https://github.com/jaylamping/roark) on one workstation, and some of
that still shows:

- Paths such as `J:\code\roark-wt\<session>` and the machine name holly-pc in [01-session.md](playbook/01-session.md):
  read them as "your own worktree on the CAD machine".
- [04-export.md](playbook/04-export.md) from "From scratch to the design of record" on describes roark's CAD folders
  and its checking scripts (`tools/cad/...`), which did not move.
- Memory limits (6 GB a job, 8 GB free before a launch, 200,000 nodes before the heavy-solve lock) are sized for a
  32 GB machine shared by several sessions.
- The material numbers are for printed PETG.

The answers to the planted problems in the task sets are kept outside this repository so that a run cannot read them.

## Status

Copied from roark at commit 21fea8d (2026-11-13). The self-test passed there at f03828d; it has not been run from
this layout yet.
