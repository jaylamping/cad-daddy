# cad-daddy

Everything a model needs to do scripted CAD work and get it right: helper code that refuses to carry on after a silent
failure, a playbook of what was learned the hard way, and a benchmark with checkable answers that says how well a given
model does with them. It starts with SolidWorks (modelling, export, static studies with contact) driven from python.

It is written for any model, large or small, closed or open: the helpers are plain python, the playbook is plain
markdown, and the benchmark grades results, not style.

## Layout (planned)

| Folder | What it holds |
| --- | --- |
| `solidworks/` | `swkit.py` (modelling), `swfea.py` (static studies), `sw_instance.py` (one instance per job), `selftest.py` |
| `playbook/` | The pages a session reads before it works: session, COM, modelling, export, FEA, judgment, what finished means |
| `eval/` | Benchmark tasks, graded runs per model, and what each run changed in the playbook |
| `skill/` | The same content packaged as a skill |

## Status

Being proven in [jaylamping/roark](https://github.com/jaylamping/roark) (`tools/solidworks/`). It moves here once the
second benchmark set is graded.
