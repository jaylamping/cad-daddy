# How well the playbook works, measured

The question: can a smaller model do scripted SolidWorks work as well as the strongest one, given this playbook and the
helpers? Tested on holly-pc on 2026-11-13 with two task sets, each run a fresh session in its own worktree that was
not allowed to read any other run's folder. Every number below is in the run's `results.json` and `REPORT.md` under
[eval/](../eval/).

## Short answer

- **Planning can be bought once.** With a per-task plan from Fable, Haiku ran the hard studies on the right model
  with true numbers in twenty minutes a set. Without one it left them undone. What the plan does not transfer is
  judgment over the result ([Plan, then execute](#plan-then-execute-fable-plans-haiku-builds-2026-11-14)).
- **For routine work, yes.** With the playbook Sonnet models, edits, exports and analyses to the same numbers as Fable,
  within about 2 %, in a similar time.
- **The playbook is worth about a third of the time and nearly all of the failed runs.** Sonnet without it finished the
  same tasks in 91 minutes with about 17 crashed or wrong runs; with it, 55 minutes.
- **Depth can mostly be written down.** After the first set, what separated Fable from Sonnet was how far each went
  once the numbers were right. Those habits became required steps ([07-done.md](07-done.md)). On a fresh set built to
  test them, Sonnet did nearly every one, level with Fable on four tasks of five and faster.
- **What is left is judgment under temptation.** On the fifth task both saw a stress that kept climbing with the mesh.
  Sonnet reported the last value and passed the part; Fable would not, and failed it. The rule was on the page.
- **A playbook can make every model wrong together.** Both playbook runs of the first set, Fable's included, passed a
  bracket that fails. The playbook steered them to a rigid load; the run without the playbook got it right. That is the
  strongest argument for keeping the benchmark and a no-playbook control beside the playbook.

## Set A: seven tasks ([TASKS.md](../eval/TASKS.md))

Model a bracket, change it, run a static study, the same on a sharp-cornered variant, make it pass, a pin-in-hole
contact study, five diagnoses.

| | Sonnet + playbook | Fable + playbook | Sonnet, no playbook |
| --- | --- | --- | --- |
| Run folder | [sonnet-playbook](../eval/sonnet-playbook/) | [fable-playbook](../eval/fable-playbook/) | [sonnet-bare](../eval/sonnet-bare/) |
| Wall time | 55 min | 45 min | 91 min |
| Tasks done | 7 of 7 | 7 of 7 | 7 of 7 |
| Failed or wrong runs on the way | not counted | not counted | about 17 |
| T1 volume, hand 32,974.02 mm³ | 32,974.02 | 32,974.02 | 32,976.08 (2 mm³ off, unexplained) |
| T3 peak von Mises, MPa | 15.52 | 15.78 | 18.57 |
| T3 tension across layers, MPa | 10.19 | 10.20 | 16.13 |
| T3 factor on layers (need 2.0) | 2.21, pass | 2.21, pass | **1.40, fail** |
| T3 displacement, mm | 2.355 | 2.361 | 2.743 |
| T4 sharp corner recognised as singular | yes | yes | yes |
| T6 pin rise, mm | 0.1285 | 0.1276 | 0.127 |
| T6 contact pressure, MPa (Hertz 6.8) | 6.1 to 6.5 | 6.26 | 6.55 |

**The T3 disagreement** ([t3-load-check](../eval/t3-load-check/CHECK.md)). The two playbook runs put the 150 N on the bore
as a rigid remote load. That makes the bore wall a rigid body and stops the 2.8 mm ligaments to the motor-screw holes
flexing. Nine solves settled it: rigid load 10.4 MPa at the hole rims; even force on the bore 16.0; load on the screw
holes, where a motor really puts it, 15.4; by hand 5.5 × 3 = 16.5. The bracket fails at about 1.4. No mask or mesh hid
it. The playbook now says where a load belongs, requires a second load model beside small features, and asks for a
hand value at every small hole in a stressed wall.

**What Fable did that Sonnet did not, in set A.** A second support model (bonded washers) to show the result did not
hang on the fixture; interlayer shear; a table of all three print directions (side printing takes the layer factor
from 2.2 to 4.6); contact pressure integrated back to the load; and it caught a study that had silently solved the
wrong problem. None of it needed knowledge Sonnet lacked. All of it is now a required step.

## Set B: five depth tasks ([TASKS_B.md](../eval/TASKS_B.md))

A hub from a specification with two hidden problems; a wall bracket with the print direction left open; make it
lighter; a tongue in a slot held only by contact; review a colleague's report with eight planted flaws.

| | Sonnet + playbook ([sonnet-b](../eval/sonnet-b/)) | Fable + playbook ([fable-b](../eval/fable-b/)) |
| --- | --- | --- |
| Wall time | 62 min, every limit kept | about 160 min over two sessions (the first died), two task limits overrun |
| B1 volume against hand 21,865.51 | 21,865.54 | 21,865.54 |
| B1 hidden problems found (2 planted) | 2, plus two more questions | 2, plus two more questions |
| B2 hand root stress (13.75 MPa) | 13.75 | 13.75 |
| B2 von Mises, printed on its side | 19.5 MPa, factor 2.31 | 19.6 MPa, factor 2.30 |
| B2 other print directions | both shown to fail (1.12 and 1.79) | both shown to fail (1.12 and 1.75 to 1.95) |
| B2 second support | yes | yes |
| B2 layer measures at the square side edges | noticed they rise with the mesh, reported the finest value | showed they double with every halving, rounded the edges to get a real number: 1.88 to 2.08 |
| **B2 verdict** | **pass** | **fail** |
| B3 mass, from 22.7 g | 7.8 g, 66 % less | 5.7 g, 75 % less |
| B3 what stopped it | von Mises 2.08 | strut buckling by hand (2.02), a check the task did not ask for; caught two lighter candidates failing under the load pad, inside the mask |
| B4 wall forces against hand 180.8 / 100.8 N | 183.3 / 103.3 | 183.6 / 102.5 |
| B4 proof it is contact | reversed tiny load | forward tiny load; its reversed run did not converge and was marked invalid |
| B4 block peak called singular, not a design number | yes | yes |
| B4 largest solve | 149,700 nodes | 244,072 nodes, 13 GB, which pushed another thread's solve off the machine |
| B5 planted flaws found (8) | 8, plus 6 more | 8, plus 7 more |

**What set B shows.** On four of five tasks the two are level, and Sonnet was faster and better behaved: it kept every
time limit and every solve small. The difference is B2. Both saw the same numbers. Sonnet reported the finest value of
a stress that was still climbing and passed the part; Fable refused to read a number off a sharp edge, changed the
geometry until the number meant something, and failed it. The playbook already said that a peak which keeps rising is not a
stress ([05-fea.md](05-fea.md)); Sonnet read it and still passed the part. 07-done.md now makes it a gate: no verdict
of pass on a measure that is still moving. That is the remaining gap: not knowledge, and not effort, but
holding a rule against a convenient answer. B3 shows the same thing from the other side: Fable went looking for the
failure the requirement did not name.

The grading keys for sets B to D are kept outside the repository so that later runs cannot read them.

## Set C: design sense ([TASKS_C.md](../eval/TASKS_C.md))

A boxy forearm link and the request "make this more organic, like it grew that way", with the mounting faces, the
loads and the mass fixed. The engineering is a gate; the form is judged by Joey from picture sheets.

| | Sonnet + playbook ([sonnet-c](../eval/sonnet-c/)) | Fable + playbook ([fable-c](../eval/fable-c/)) |
| --- | --- | --- |
| Wall time, limit 100 min | 92 min | 71 min, 27 of them waiting behind other sessions' solves |
| Mass, from 261 g | 160 g | 137 g |
| Lowest factor (need 2.0) | 3.46, shear between layers, reported as "not shown" because it still moved | 2.58, shear between layers, two meshes within 5 to 7 % |
| Fixed items intact | yes, checked on the export | yes, checked on the export |
| First picture inside 20 minutes | yes, at 6 | yes, at 18, drawn from the section table because SolidWorks would not launch |
| Ideas that differ in kind | a waisted strap, a flat leaf | a bone, a wishbone |
| Section through the shaft | rounded rectangle; the round loft pinched and was dropped after six tries | oval; the same loft pinched, cured by drawing each section as two open curves |
| Sharp edge per root of area (boxy 12.3) | 7.9 | 3.4 |
| Its own verdict on the form | "a smooth flat strap, less boxy more than grown" | "a bone"; names the neck crease under the lower screws as the weak spot |
| Joey's pick ([sheet](../eval/fable-c/pictures/c2_before_after.png)) | | **this one** |

Both hit the same wall, a loft that pinches when its sections change shape. One stopped at a form it knew was short of
the request and said so; the other found why and got through. The cure is now in [03-modelling.md](03-modelling.md),
and the same task run again by Sonnet with it is the measure of whether a lesson written down is a lesson learned.
The pick was not fully blind: the card that asked for it carried a recommendation.

**The same task again, one lesson added** ([sonnet-c2](../eval/sonnet-c2/), [sheet](../eval/sonnet-c2/pictures/c2_before_after.png)).
Sonnet with the playbook as it stood after sets C and D:

| | Sonnet, first try | Sonnet, second try | Fable |
| --- | --- | --- | --- |
| Section through the shaft | rounded rectangle, the oval loft dropped after six tries | oval, eight sections, lofted at the first attempt | oval |
| Sharp edge per root of area (boxy 12.3) | 7.9 | 6.5 | 3.4 |
| Flat share of the surface (boxy 0.91) | not recorded here | 0.21 | not recorded here |
| Mass, from 261 g | 160 g | 148 g | 137 g |
| Wall time | 92 min | 82 min, 20 of them waiting | 71 min |
| Lowest factor (need 2.0) | 3.46, "not shown" | 1.94 at the finest mesh, 1.55 with the other support: **requirement not met**, and reported so | 2.58 |
| Its own verdict | "a smooth flat strap" | names the back of the flange, "added, not grown", and a step at the slot | names the neck crease |

The lesson that was written down transferred: the loft that stopped the first try worked at once, and the form
moved from a strap to a round stem. What did not transfer is what was never written: the stem meets the flange at
a sharp edge because no fillet would build there, the stress peak sits on that edge, and the part ends below the
requirement. Sonnet said so plainly and did not pass it, which is the set B gate working. The next lesson is
therefore known and specific: how to blend a loft into a flange (start the loft from a section on the flange, or
build the junction as its own loft, since a fillet across a loft seam does not build). It is not yet in the playbook.

## Set D: stress ([TASKS_D.md](../eval/TASKS_D.md))

A mount from a need with no drawing; a split bearing housing whose specification has three planted errors, with
contact and screws; six plates from a table with bad rows, then a change of mind to be made by editing.

| | Sonnet + playbook ([sonnet-d](../eval/sonnet-d/)) | Fable + playbook ([fable-d](../eval/fable-d/)) |
| --- | --- | --- |
| Time on the tasks, limit 210 min | 90 min (39, 31, 20) | 61 min (13, 34, 14) |
| D1: the 60 mm board in a 50 mm envelope (a real contradiction in the task) | caught; tilted the board 41 degrees to fit, which rests on the tall parts sitting in the middle of the board | caught; built flat, 5 mm over each side, and reported the envelope as not met |
| D1 mass, parts | 23 g, one piece | 11 g, one piece |
| D1 board out with the mount on the rail | yes, four M3 screws | yes, four M3 screws into inserts |
| D1 ideas that differ | two, the second a sketch only | three, the second a crude model, the third on paper |
| D1 study | one mesh, not converged, said so | three meshes; one measure still moving, reported as "not shown" |
| D2 planted errors found (3) | 3, plus 4 more | 3, plus 3 more |
| D2 what was built for the overlapping counterbores | left overlapping, as a figure of eight | screws moved apart, 1.0 mm between |
| D2 fit for a ±0.15 printer | seat 52.0, split gap 0.6 | seat 52.15, each face set back 0.4, gap 0.2 to 1.1 after clamping |
| D2 screw load along the load, hand 75 N | 75.2 | 74.2 to 74.9 on three meshes |
| D2 screw load across the load | 45 to 51 N against a hand 37.5, "not explained", case marked not shown | 67 N in total; found the ring wedges under one half and redid the hand value: 75.7 |
| D2 contact proof | bonded twin, 24 times stiffer | 1 N across the clearance: 0.077 mm against 0.0005 bonded |
| D2 lowest factor | 8.8, shear between layers | 5.85, shear between layers |
| D2 what the study leaves out | head-edge peak named as not shown safe | screw preload: larger than the service load, factor 2.0 at about 285 N per screw |
| D3 bad rows caught before building (P1, P2, P4) | all | all |
| D3 the plate that cannot be built (P4) | moved the hole circle inward, from 58 to 49 | kept the hole circle, which mates with something, and grew the disc to 70 |
| D3 problems the change itself made (P3 holes 0.3 mm apart, chamfer into counterbores) | both caught | both caught |
| D3 volumes against hand, twelve parts | all equal | all equal |
| D3 edited, not rebuilt | yes | yes, shown by feature IDs before and after |

**What set D shows.** The checks hold up under stress: neither model built a broken part, both caught every planted
error and the two that the change request created, and care did not drift between the first plate and the twelfth.
The gap is again in what happens at an unexplained number and at a choice. Sonnet met a screw load it could not
explain and marked the case "not shown", which is the honest answer the playbook asks for; Fable chased it to the
cause. Sonnet resolved two impossible requirements by changing the thing a neighbouring part depends on (a bolt
circle, a board attitude that leans on an assumption); Fable changed the thing nothing else depends on and said which
requirement it gave up. And Fable named the load nobody asked about, the tightening of the screws.

The two answers to D1 are a real difference of opinion, not a right and a wrong: one keeps the envelope, the other
keeps the design simple. That choice is Joey's.

## Other vendors: GPT 6 Luna and GPT 6.1 Terra (Codex, 2026-11-13 and 14)

The same task sets, the same brief, run through `codex exec` on holly-pc with full access to the worktree. Luna ran
at reasoning effort Extra High, Terra at High. One pass each; Luna's sets C and D were not run (C was stopped after
37 minutes with one idea built and no analysis, [luna-c](../eval/luna-c/)).

Two things changed between the Luna and Terra runs, so their wall times are not like for like: a SolidWorks instance
kept running on the PC from 20:07Z made launches take seconds, and before it a run could queue for minutes behind
another session's solve. Luna's two runs include about 45 minutes of such waiting each; Terra's had almost none.

| | Luna, Extra High | Terra, High | Sonnet + playbook | Fable + playbook |
| --- | --- | --- | --- | --- |
| **Set A** wall time | 132 min (about 85 working) [luna-a](../eval/luna-a/) | 42 min [terra-high-a](../eval/terra-high-a/) | 55 min | 45 min |
| T1, T2 volumes | exact | exact | exact | exact |
| T3, the bracket that fails at about 1.4 | **passed it**, with the second load put on the whole front face; its own table showed layer shear at 1.80 | **failed it at 1.38**, load on the motor holes | passed it (rigid load, before the fix) | passed it (same) |
| T5 make it pass | skipped the redesign | real redesign, +3.3 % mass, lowest factor 2.02 converged | done | done |
| T6 contact | not valid: a "Fixture transfer failed" dialog went unread | valid, both proofs | valid | valid |
| Failed runs on the way | about 9 | about 4 | not counted | not counted |
| **Set B** wall time | 120 min [luna-b](../eval/luna-b/) | **8 min, stopped itself** [terra-high-b](../eval/terra-high-b/) | 62 min | about 160 min over two sessions |
| B1 hidden problems (2) | 1 | 2 | 2 | 2 |
| B2 print direction | "not shown" | incomplete, "not shown"; broke the displacement gate and said so | done | done |
| B3 lighter | 48 % | 41 %, one try | 66 % | 75 % |
| B4 tongue in a slot | no answer, declared not valid | **never started**: 7.6 GB free against the 8 GB floor, gave up in 2 s | done | done |
| B5 planted flaws (8) | 8, in a list of 14 | 8, in a list of 13 (the swapped section named as a wrong bending depth) | 8, plus 6 more | 8, plus 7 more |
| **Set C** | not run | 53 min, 261 to 177 g, strength not shown; stem lofted, disc and fork unchanged [terra-high-c](../eval/terra-high-c/) | 148 g (second try) | 137 g |
| **Set D** wall time | not run | 87 min [terra-high-d](../eval/terra-high-d/) | 90 min | 61 min |
| D1 board that cannot fit the envelope | | caught; kept the design simple and reported the envelope as not met (Fable's choice); strength screened only | caught, kept the envelope | caught |
| D2 planted problems (3) | | 3 | 3 | 3 |
| D2 screw load, hand 75 N | | 74.5 | | 75.7 |
| D2 lowest factor | | **none given** after 65 min and twelve contact solves: last changes 8.3 % and 5.7 % | 8.8 | 5.85 |
| D3 bad rows (3) and knock-on problems (2) | | 3 and 2 | 3 and 2 | 3 and 2 |

**What this shows.**

- **Terra at High does routine work at Fable's speed and got T3 right,** with the corrected load guidance on the
  page. Luna at Extra High had the same page and still passed the bracket, on a load placed where no motor puts it,
  while its own shear number said fail. The rule "report the higher of the two load models and every measure" was
  followed in the table and not in the verdict.
- **Terra stops early, in two different ways.** In set B it ended the whole run at eight minutes with three tasks
  open. In sets C and D it worked for an hour and then reported "not shown" rather than a number. The second is honest
  and is what the page asks for when a measure will not converge; the first is not. The "Do not stop early" section of
  [07-done.md](07-done.md) was written from this run; the table below shows what it changed.
- **Luna is careful and slow.** It kept every rule, declared its own invalid results, and found every planted flaw in
  the review, but took about twice the working time and left more tasks without an answer.
- **Both kept the machine rules,** with one class of exception that was the helpers' fault: `job()` and `export()`
  set machine-wide export options while the brief says to change no shared setting. Terra noticed in every run.

**What the "Do not stop early" section was worth** ([terra-high-b2](../eval/terra-high-b2/)): set B again with
Terra at High, the same brief, and only that section (and a launch that waits for memory) added.

| | terra-high-b, plain playbook | terra-high-b2, with the section |
| --- | --- | --- |
| Wall time, all of it working | 8 min | 49 min |
| Commands run | 47 | 256 |
| B1 hub | partial, 2 hidden problems | done, the same 2, every dimension measured |
| B2 study | one support, 3 meshes to 20,572 nodes | two supports, 4 meshes to 155,273 nodes, a twin with the 0.4 mm printed radius |
| B2 verdict | "not shown" | **fail**, layer shear 1.95 against 2.0, converged under 1 % (Fable 1.88, fail; Sonnet passed it) |
| B3 lighter | 41 %, one candidate, "what governs: not established" | 59 %, five steps, two lighter trials shown to fail, von Mises 2.08 governs |
| B4 tongue in a slot | not started | coarse solve: wall forces 114 and 194 N against 101 and 181 by hand; four finer tries gave excessive displacement; **blocked** after 4.5 of its 40 minutes |
| Tasks left open | B1, B2, B3, B4 | B4 |

The section moved three of four open tasks to a real answer, and on B2 to the same verdict as Fable by the same
move (round the edge, then judge). It did not make the model use a task's time: B4 was closed as "blocked after
three different tries" where the tries were three mesh and stiffness variations of one approach, with 35 minutes
left. The rule now says what counts as a different try and ties "blocked" to the time limit.

**Not comparable, and why.** Luna ran from roark 86b0696 and Terra from c6b79c3 (the helpers differ only in launch
code); Sonnet and Fable ran sets A and B on earlier versions of the playbook, before the load guidance and the
no-pass-on-a-moving-measure gate, so their set A row is not the same test. Neither Codex model could report its own
model id; the id is taken from the `codex exec` header in each run's `codex.log`.

## Plan, then execute: Fable plans, Haiku builds (2026-11-14)

The question: can the strongest model's thinking be bought once, as a written plan, and the building be done by
the smallest and cheapest model? Fable wrote one plan per task for sets A and D ([plans-fable](../eval/plans-fable/))
from the task sheets, the playbook and the helper code only, without SolidWorks and without sight of any earlier
run: 43 minutes for ten plans. Haiku then ran each set twice in fresh sessions, once with the playbook alone and
once with the plans as well. Every result below was checked independently: all 57 saved parts re-measured, every
claimed solve read in its log ([haiku-runs-CHECK.md](../eval/haiku-runs-CHECK.md)).

| | Haiku, playbook only | Haiku, playbook and plans |
| --- | --- | --- |
| **Set A** wall time | 19 min [haiku-a](../eval/haiku-a/) | 22 min [haiku-plan-a](../eval/haiku-plan-a/) |
| T1, T2 model and edit | right shapes, but the edit was saved over the original part, and the report said it was not | correct, original untouched |
| T3 bracket (fails at about 1.4) | ran on the wrong part; "fail" at 1.29 by accident, rigid load gave the known wrong 2.17 | **correct: 1.49 at the motor-hole rims**, two load models, washers as second support |
| T4 sharp corner | gave the singular corner a value (31.3 MPa) and distrusted its own correct R0.4 run | correct: no value for the sharp corner, R0.4 converged at 40 MPa |
| T5 make it pass | not done | ribs built, +8 % mass, factors 3.0 to 3.6, but **recorded as "fail"** because one measure still moved 13 % |
| T6 pin contact | not done (one invalid solve, hand value wrong) | **numbers correct**: 6.5 / 6.0 / 6.8 MPa against Hertz 6.8, rise 0.1295 mm; called itself invalid for not converging |
| **Set D** wall time | 21.5 min [haiku-d](../eval/haiku-d/) | 20.5 min [haiku-plan-d](../eval/haiku-plan-d/) |
| D1 mount | conflict found; bosses have no screw holes | conflict found and reported, holes in, tilt checked |
| D2 split housing | the three spec problems found, **no study at all**, stopped 6 minutes into 90 | full contact study at one mesh: screws 75.7 N against 75 by hand; the finer mesh hit the node cap and it stopped at 13 of 90 minutes; reported factors were not the lowest in its own table (true 5.82, as Fable's 5.85) |
| D3 six plates and the change | correct, every bad row found by its own checks | correct, from the plan |

**What the plans bought.** The hard studies ran first time on the right model with true numbers: T3 at the
motor-hole rims, T6 with pads, D2 with full contact. The baselines have a wrong-part T3, an invalid T6 and no D2
study. Traps were avoided (save under a new name before editing, no value for a singular corner), and the designs
would work as built.

**What they did not buy.** Judgment over the numbers: a part at factor 3 recorded as a fail, a correct contact
result called invalid, the headline factor read from the wrong row. Persistence: one refused mesh ended D2 with
five-sixths of its time left and nothing coarser tried. Time sense: all four runs took about 20 minutes, two
reports claimed over an hour, and both baselines gave lack of time as the reason for work left undone. And where
the plan gave the answer it was not tested, so plain modelling (D3, T7) was no better with a plan than without.

**The plans were not right either,** and this mattered less than expected. Node counts were 1.3 to 2.9 times
under, two hand predictions were off by 40 to 60 %, one screw load by half, one material key matched no body, and
one tolerance stopped a build. No helper call in them was invented. The executor got through most of these on the
plan's own "if you see X" branches.

**Cost.** Fable did sets A and D itself in 45 and 61 minutes. Planning both took 43 minutes and Haiku ran both
in 43. So the pair takes about the same wall time as Fable alone, with half of it on the cheapest model; what it
gives up is the second half of each hard task, where a result has to be doubted, chased or defended.

**The third step: review** ([haiku-plan-REVIEW.md](../eval/haiku-plan-REVIEW.md)). Fable then reviewed both plan
runs from the files alone, without SolidWorks and without the answer keys, in 16 minutes. It reached the same
corrections as the independent check that had the keys, and more:

| Task | Haiku's verdict | After review |
| --- | --- | --- |
| T5 ribbed bracket | fail | margin, not converged: lowest factor 3.02; only von Mises at a sharp rib toe still moves |
| T6 pin contact | not valid | valid: 499.8 of 500.0 N through the hole, the proof run moves the pin exactly the gap, pressure 6.4 to 6.8 MPa against Hertz 6.76 |
| D2 split housing | factors 9.85 / 25.7 / 9.25 | 7.34 / 20.9 / 5.82; shear in the lower half governs; a displacement 5.5 times the prediction was never flagged; screw tightening is in no study |
| T4 corner | 40 MPa "not explained" | explained: the curved-beam value, 39.3 by hand; the lowest factor there is 0.57 in shear, which the run left out |
| T1, T2, T3, T7, D1, D3 | as reported | unchanged |

The review changed the outcome of two tasks of ten, corrected the governing number on two more, and wrote five
follow-up runs as step-by-step instructions for the same executor. It also found causes upstream: a plan that
defined "valid" to include convergence, a plan branch that answered a refused mesh with a finer one, and a
tolerance in `expect()` that read 0.02 mm as 2 %.

**Cost of all three steps.** Plan 43 minutes, execute 43, review 16: about 100 minutes for sets A and D, against
106 for Fable alone, with the strong model working for 59 of them and the rest on the cheapest model. The time
is the same; what changes is that the strong model's part needs no SolidWorks seat and no waiting on solves, so
several jobs can be planned and reviewed while the executor runs them.

**The fourth step: the follow-ups handed back** ([haiku-followup-CHECK.md](../eval/haiku-followup-CHECK.md)). The
review's follow-up runs went back to Haiku as written, with `judge()` and the job clock in place. Set A took 14
minutes and set D 24, both from `times.log` and both right this time. Checked independently again:

| Open task | After the follow-up | Check |
| --- | --- | --- |
| T5 ribbed bracket | rib toes rounded at R2: pass, lowest factor 2.99, all three measures converged | confirmed; part re-measured to the hand volume |
| T6 pin contact | valid, line mean 6.07 / 5.73 / 5.64 MPa, converged | confirmed; it sits 17 % under Hertz because the contact is wider than the textbook strip |
| D1 mount | converged at 2.49 MPa, factor 18.07 | confirmed; the reviewer's higher hand value was the wrong model |
| D2 split housing | model valid, lowest factor 4.17, shear still climbing 20 % then 28 % per step: not closed | not closed. The climbing peak is the ring's sharp steel corner bearing 0.15 mm from the seat rim. One millimetre away everything converges at a factor of about 13 |

Three of four open tasks closed, fifteen studies in 38 minutes, every step tried in order, no stop, no invented
number and no verdict of its own. What explicit next steps did not buy is anything past the instruction: results
that needed looking at were reported and left, and the instruction's own mistakes were carried out faithfully. The
last open task needs a decision (round the ring corner, read away from the edge) that neither the plan, the
review nor the executor made. It is now a line in [07-done.md](07-done.md).

`judge()` was wrong on that task: it called a series with growing steps "margin". A rising measure whose steps
grow is the mark of a sharp edge, and it now reads "not shown".

**Cost of the whole loop for sets A and D:** plan 43 minutes, build 43, review 16, follow-up 38. Fable works for
59 of 140 minutes and needs no SolidWorks seat; nine of ten tasks end closed and checked.

**What this says to do next.** Keep the loop: plan, build, review, follow up. Each pass through it has moved
something from the strong model's head into code or a page (the verdict, the clock, the contact-edge rule), and
those help every model. The open questions are whether one planner can keep several executors busy at once, and
whether the same loop holds on a design task with no right answer, where set C showed the largest gap.

## The loop on a design task, another planner, and an advisor (2026-11-14 and 15)

Three questions left open by the section above, each tried once.

### The loop on the organic link (set C, task C2)

Fable planned the link without SolidWorks in 36 minutes ([plans-fable-c](../eval/plans-fable-c/)): a bone with a
revolved hub and wrist, a stem lofted through 13 sections, expected 116 g. Haiku built it in 51.6 minutes
([haiku-plan-c](../eval/haiku-plan-c/)): the boxy link exact, the organic link at 116.4 g with all 33 fixed items
held, and a `fail` at 1.58 that it reported as a fail. Fable reviewed from the files in 17 minutes
([haiku-plan-c-REVIEW.md](../eval/haiku-plan-c-REVIEW.md)), and four rounds of written instructions went back to
the same executor (18, 22, 15 and 13 minutes of work).

| Round | What the review changed | Mass g | Verdict, lowest factor | What it showed |
| --- | --- | --- | --- | --- |
| build | | 116.4 | fail 1.58, flat print | the stem has a waist nobody asked for |
| [follow-up](../eval/haiku-plan-c-followup/) | section rows added, print on edge | 117.9 | not shown 2.06 | the waist only moved: **the review had the wrong cause** |
| [2](../eval/haiku-plan-c-round2/) | every loft section picked at the same corner; print tilted 30 degrees | 124.5 | fail 1.57 | the loft was twisted a quarter turn; untwisted, the stem peak fell from 21.9 to 6.5 MPa and the weak place moved to the neck |
| [3](../eval/haiku-plan-c-round3/) | deeper neck | 128.2 | fail 1.39 | **worse:** the deeper neck stood higher beside two screw-head pockets and made a notch of the pocket edge |
| [4](../eval/haiku-plan-c-round4/) | neck lowered beside the pockets, more material under the cable tunnel | 128.5 | fail 1.78 | three places within 15 % of each other now limit every upright and tilted print; only the on-edge print passes (2.97) |

It ends not done. What it bought:

- **A fault class no check could see.** A loft that pairs the wrong corners between two sections is twisted and
  narrower in the middle. The volume check passed, the picture looked like a styling choice, and the first review
  explained it as sparse sections. It was found by measuring the turn of the STL's own edges about the stem axis:
  about 90 degrees in one stretch, under 8 everywhere else. `sheet.loft_twist()` and `loft(..., at=)` are the
  result ([03-modelling.md](03-modelling.md)).
- **The print direction as a table, not a strength choice.** Joey's rule (2026-11-14): faces that sit on support
  come off rough and are not sanded, and the printer is 256 mm high. Measured on the part: flat 8,000 mm2 of
  support, on edge 4,770, upright 660 but 249 mm tall, tilted 30 degrees with the hub down 770 at 222 mm. The plan
  had chosen flat and the first review on-edge, both on strength alone ([04-export.md](04-export.md), Printing).
- **Where review by instruction stops.** Rounds 3 and 4 were the reviewer nudging a section table from the
  numbers. One nudge made it worse, and the last left the part 12 % short in three places at once. That is a new
  neck (the two lower screws sit in the load path), which is a planner's job, not a follow-up.
- The executor did every round as written, reported every fail as a fail, and twice caught mistakes in the
  instructions (a wrong body count, a task file missing from a worktree).

Form: a blind sheet of this link beside the two from 2026-11-13 is with Joey; the result goes here.

### Opus as the planner

The same planner brief and the same inputs went to Opus. It wrote the ten plans for sets A and D in 46 minutes
([plans-opus](../eval/plans-opus/); Fable took 43), and Haiku built from them in fresh sessions from the same
commit as the Fable-planned round.

| | Fable plans | Opus plans |
| --- | --- | --- |
| Set A | 22 min, 7 tasks reached | 70 min, 35 of them waiting on another thread's solve; 6 reached, T6 not started |
| T3 bracket (fails at about 1.4) | fail 1.49 | fail 1.26 |
| T5 make it pass | ribs, factor 3.0 (recorded as fail; pass after review) | thicker upright printed on its side, 2.06 with convergence not shown, called a pass |
| T6 pin contact | numbers right | not reached |
| Set D | 20.5 min | 47 min, 19 of them lost to two hidden message boxes |
| D2 split housing | one mesh, screws 75.7 N against 75 by hand | two meshes, screws 68.6 to 77.1 N; lowest factor 3.8; convergence not shown |
| D3 six plates | right | right |

Haiku could follow either. The Opus plans named no helper that does not exist and found every planted error in
the D tasks (five on the housing against the three in the key). Where they fell short was the hand numbers the
executor checks itself against: a load model predicted to read low reads 60 % high, a section stress has the
wrong sign, a crown stress predicted at 21 MPa reads 3, a screw load is 27 % off. Each left a "not explained"
line and cost time, and one mesh over the node limit queued behind another thread for 35 minutes. Opus wrote no
shared `common.py`; Fable's plans came with one. **The two Opus-planned runs are graded from their own reports
only:** no part was re-measured and no review pass was run, so the comparison is of what was reached and at what
cost, not yet of what is right.

### Sonnet with a Fable advisor: tried, dropped on cost

Claude Code's advisor setting gives the building model a stronger model to consult. Sonnet with Fable as advisor
did set A in 59 minutes with two advisor calls and set D in 75 with three
([sonnet-adv-a](../eval/sonnet-adv-a/), [sonnet-adv-d](../eval/sonnet-adv-d/)); every task was reported done, and
the advisor's calls caught real errors (a body mask that read 30 MPa where 5.2 was right, twelve contact studies
that were not valid, a screw that bottomed). Set A cost $20.43 as recorded (Sonnet 13.66, advisor 6.77), against
$1.29 to $3.52 for a Haiku run with a plan. Each advisor call reads the whole conversation again uncached, and it
is billed as Fable. Joey dropped the path on 2026-11-14. The two runs are not checked against their logs.

### Cost and process numbers

One `metrics.json` per run folder, read by `python pc/metrics_table.py eval`. "Right" is counted only by the check
named beside it; for the runs of 2026-11-14 morning it is read from the tables above.

| run | machine | set | model | plan | right / reached / total | checked by | wall min | waiting | cost $ | min per right task | $ per right task | failed jobs per task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| haiku-a | holly-pc | A | claude-haiku-5-5 | none | 2 / 5 / 7 | independent check (eval/haiku-runs-CHECK.md) | 19.5 |  | 1.34 | 9.8 | 0.67 |  |
| haiku-d | holly-pc | D | claude-haiku-5-5 | none | 1 / 3 / 3 | independent check (eval/haiku-runs-CHECK.md) | 21.5 |  | 1.94 | 21.5 | 1.94 |  |
| haiku-oplan-a | holly-pc | A | claude-haiku-5-5 | Opus | 5 / 6 / 7 | own report, not checked | 70.0 | 35.0 | 1.5 | 7.0 | 0.3 |  |
| haiku-plan-a | holly-pc | A | claude-haiku-5-5 | Fable | 5 / 7 / 7 | independent check (eval/haiku-runs-CHECK.md) | 22.1 |  | 1.29 | 4.4 | 0.26 |  |
| haiku-plan-a-followup | holly-pc | A | claude-haiku-5-5 | Fable review | 2 / 2 / 2 | independent check (eval/haiku-followup-CHECK.md) | 15.9 |  | 0.45 | 8.0 | 0.23 |  |
| haiku-plan-c | holly-pc | C | claude-haiku-5-5 | Fable | 1 / 2 / 2 | review from files (eval/haiku-plan-c-REVIEW.md) | 51.6 |  | 1.27 | 51.6 | 1.27 |  |
| haiku-plan-c-followup | holly-pc | C | claude-haiku-5-5 | Fable review | 0 / 1 / 1 | results read from the files | 18.2 |  |  |  |  |  |
| haiku-plan-c-round2 | holly-pc | C | claude-haiku-5-5 | Fable review | 0 / 1 / 1 | results read from the files | 22.2 |  |  |  |  |  |
| haiku-plan-c-round3 | holly-pc | C | claude-haiku-5-5 | Fable review | 0 / 1 / 1 | results read from the files | 30.8 | 15.7 |  |  |  |  |
| haiku-plan-c-round4 | holly-pc | C | claude-haiku-5-5 | Fable review | 0 / 1 / 1 | results read from the files | 12.8 |  | 2.65 |  |  |  |
| haiku-plan-d | holly-pc | D | claude-haiku-5-5 | Fable | 2 / 3 / 3 | independent check (eval/haiku-runs-CHECK.md) | 20.7 |  | 3.52 | 10.3 | 1.76 |  |
| haiku-plan-d-followup | holly-pc | D | claude-haiku-5-5 | Fable review | 0 / 1 / 1 | independent check (eval/haiku-followup-CHECK.md) | 25.4 |  | 0.53 |  |  |  |
| sonnet-adv-a | holly-pc | A | claude-sonnet-5-5 with a Fable advisor (2 calls) | none | 7 / 7 / 7 | own report, not checked | 59.9 |  | 20.43 | 8.6 | 2.92 |  |
| sonnet-adv-d | holly-pc | D | claude-sonnet-5-5 with a Fable advisor (3 calls) | none | 3 / 3 / 3 | own report, not checked | 76.2 |  |  | 25.4 |  |  |
| haiku-oplan-d | holly-pc | D | claude-haiku-5-5 | Opus | 1 / 3 / 3 | own report, not checked | 47.0 | 19.0 | 4.51 | 28.0 | 4.51 |  |

What the numbers say: a plan roughly halves the cost of a task that ends right (Haiku on set A, $0.67 without a
plan, $0.26 with Fable's), the advisor path costs ten times that, and on a design task the money goes on rounds
that end not done. Failed jobs per task are not in the older runs; `runs.log` counts them from 2026-11-14 on.

## What each run changed in the playbook

| Run | Changes |
| --- | --- |
| sonnet-playbook | Nine helper bugs fixed (reactions, per-face loads, materials matching, stale faces, the hidden solver prompt, error 24 after an unsaved close) |
| fable-playbook | Screwed-down supports, partial-face loads, pad placement, study order on multi-body parts, print-direction table, `max_nodes` |
| sonnet-bare | Confirmed what the playbook saves; exposed the rigid-load error |
| t3-load-check | Load placement, second load model, the mask warning, the harmless excessive-displacement prompt |
| sonnet-b | Study names, three sizes in `converge()`, four studies per instance, section forces, twin-model check, exclusion distance at a fixed hole |
| fable-b | The heavy-solve lock, one refinement at a time, the unanswered contact-convergence prompt, which contact proof fits which joint, buckling of lightened parts |
| sonnet-c, fable-c | Lofts whose sections change shape, a point-in-solid check (`sheet.inside`), a crop for close-ups, one launch per job when the clock matters |
| sonnet-d, fable-d | Changing a saved part (`set_dim`, `redraw_circles`), screws and clamped joints, results per body (`summary(mask=)`, `converge(mask=)`, shear in `converge()`), the proof for a body seated both sides, a launch that waits (`job(wait_s=)`), assembly pictures (`sheet.py --together`), `call()` on members that return objects, the node-count rule |
| luna-a, luna-b, terra-high-a to d, terra-high-b2 | Export options set only for the export and put back, a launch that waits for memory, an unknown solver dialog fails the run, the contact proof in 07-done.md matched to the joint, node counts with local controls, "Do not stop early" and what counts as blocked |
| bearing-load, loft-blend | A bearing load measured against the hand value; why a loft would not fillet into a flange, and three cures |
| haiku-a, haiku-d, haiku-plan-a, haiku-plan-d | `judge()` and its four verdicts, valid against converged, a job clock, `save_as` before editing into a new file, what to try after a refused mesh |
| haiku-plan-c and its four rounds, haiku-oplan-a, haiku-oplan-d | A loft twist check on the export and pick points for `loft()`; the print direction chosen from a table of height, support on visible faces and strength; one `metrics.json` per run. Still open from these runs: a hidden SolidWorks message box that is not a solver dialog hangs a study and the helper neither answers nor logs its text; `export()` before `save()` leaves no part on disk; `static()` queues a mesh just over the heavy-solve limit without saying how long the wait may be |

## What still needs the strongest model, or Joey

- **Design decisions:** a load path, a split line, a joint, how something should look. The benchmark does not test
  these, and [06-judgment.md](06-judgment.md) still hands them up.
- **Writing the playbook itself.** Every correction above came from comparing runs and asking why they differed.
- **Long open-ended modelling** (an organic shell, a whole link) is untested. The early check-in and time budgets in
  07-done.md are the guard; they have not been exercised on a multi-hour job.
- **Contact models at the machine's limit** (400,000 nodes, many bodies) were not in any set.
- **Which requirement to give up** when two cannot both be met. Set D shows the smaller model picks the one a
  neighbouring part depends on more often; [06-judgment.md](06-judgment.md) hands the choice up.

## Limits of this measurement

One run per model per set, on small parts, graded by the author of the playbook. The model that served the first
Sonnet run could not be confirmed afterwards; later runs reported their own model id. Set B had the corrected
playbook, so set A and set B are not a before-and-after of the same tasks. The Fable run of set B was done by two
sessions, the second picking up the first one's files. Opus has been run only as a planner, and the runs built
from its plans, like the two advisor runs, are graded from their own reports. The Codex runs are one pass each
and Luna's stop at set B.

## Running it on another model

1. A fresh session with its own worktree, told to read [README.md](README.md) and do one task set under a run name.
2. Forbid it from opening other runs' folders; ask it to report its model id, times, failed runs and playbook problems.
3. Grade `results.json` against the hand values in the task file and the table above.
4. Fix what it tripped on in the playbook or the helpers, not in the session.
5. Keep one run without the playbook as a control: it is the only thing that catches the playbook being wrong.
