# 8. Who plans, who builds, who reviews

Which model does which part of a SolidWorks job, chosen from the runs in [EVAL.md](EVAL.md). The names are the
models measured there; the rule behind each choice is given so another model can be slotted in once it has been
run on the same sets.

## Choose the lane by one question: is the shape already decided?

| | Shape decided | Shape not decided |
| --- | --- | --- |
| Examples | a part from dimensions, an edit to a saved part, a study with a verdict, a family of parts from a table | an organic link, a cover, anything that will be looked at, anything where the load path is the design |
| Plan | the strongest model, without SolidWorks: steps, the expected change in volume at each step, hand numbers for every check, the branches for the failures it can foresee | the same model that builds |
| Build | the smallest model that follows a plan (measured: Haiku, about 20 minutes a set) | the strongest model, or the next one down (measured: Fable first, Sonnet second) |
| Review | the planner, from the files: rows against logs, verdicts worked again, hand numbers worked again | a second look by the same model at the picture sheet and the weakest section, then a person ranks it blind |
| Fixes | written instructions back to the builder, one round at a time | by the builder itself |
| Stop when | every task is right, or a fix needs a new idea rather than a correction: then it has become the other lane | the gate passes and the form is accepted |

Why the split. On decided shapes the plan carries the judgement and the builder only has to be careful: nine of ten
tasks closed that way, and a plan roughly halves what a right task costs. On undecided shapes the judgement is in
the building. Four review rounds removed every fault a check could name from the small model's organic link (a
twisted loft, the print direction) and it still ended under the strength target and last in a blind ranking of
three.

A plan from a weaker planner still works, but its hand numbers are wrong more often, and the builder checks
itself against them faithfully and cannot repair them. Each wrong hand number costs a "not explained" line and
time.

## Rules for both lanes

1. **The verdict word comes from `swfea.judge()` on the rows.** Never from prose. Both directions have happened:
   "fail" written beside passing factors, and "pass" written beside a caveat that said it was not shown.
2. **Keep the job logs with the run.** Without them a review can check arithmetic and judgement, not what the
   solver returned.
3. **The builder's report is a claim.** The reviewer reads rows and logs, and works the volumes by hand.
4. **Print direction from the table** in [04-export.md](04-export.md): height, support on faces that show,
   strength. Not from strength alone.
5. **A lofted part gets the twist check** ([03-modelling.md](03-modelling.md)) before any review of its strength.
6. **A blind pick carries no recommendation**, and the key stays outside the repository until the pick is in.
7. **One `metrics.json` per run** in its `eval/` folder, with the machine's name.

## Not adopted

- A building model with a stronger model on call as an advisor: the results were good and a right task cost about
  ten times as much as plan and build.

## Not yet measured

- The middle model as the builder under a plan. It may be the right choice for parts that are half decided.
- More than one run of each arrangement. Every comparison above is one run.
