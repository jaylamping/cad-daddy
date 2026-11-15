# C2 restated, before any modelling

1. **What the part is for.** The forearm link of a humanoid arm: it carries the wrist joint (a Ø8 pin at X 0, Z -200,
   along Y) from the elbow motor's output (a face at Y -4 with six M3 screws and a Ø30 locating bore), and takes a
   cable from one end to the other.
2. **What is fixed** (measured on the finished solid): the flat ring on Y -4 from Ø30 to Ø62, the six Ø3.4 holes on
   Ø50 (first on +X, 60° apart), the Ø30 bore, a Ø7 clear cylinder 10 mm long over each hole on the Y +4 side; the pin
   axis, the inner cheek faces at Y ±16 flat over at least Ø16 round the pin, 5 mm of material round the pin hole, the
   slot clear from Z -183 down (a Ø30 cylinder swings about the pin); a straight clear Ø6 passage for the cable that
   does not leave the form.
3. **What "good" means here.** The look first: one form that reads as grown, smooth and restrained, with no box, no
   plate edge and nothing standing proud. Behind it the gate: factor 2.0 or more on von Mises, on tension across
   layers and on shear between layers for 60 N at the pin in +X, -X and +Y with the elbow face held; mass no more
   than the boxy link's (261 g by hand); printable in one piece on a 256 mm bed with no enclosed cavity.
4. **What is mine to choose.** The section and how it changes, the taper, how hub and fork grow out of the middle,
   the outer diameter of the hub, the cheek outline, where the cable runs, the print direction and supports.
5. **How I will know.** Every fixed item measured on the solid and on the STL; three load cases at three mesh sizes
   with the verdict from `swfea.judge()`; before-and-after sheets at one scale; times from `times.log`.

**"Organic" for this part, in my own words:** the link is one bone, not three parts: a single stem whose section
changes continuously with what it has to carry and to clear (wide and thin where it leaves the plane of the elbow
disc, near round at the waist, wide the other way where it splits into the fork), and whose two ends are the joints
themselves, round about their own axes, so that no face of it is there only because a plate or a block was.

**Three things I will not do:**
- I will not round the edges of the boxy link and call it organic: no box section, no fork made of a block and two
  plates, no square-cornered slot.
- I will not add anything that stands proud of the form (ribs, bosses, a cable clip, a lug): what is needed is
  either inside the form or is the form.
- I will not buy the look with the function: no fixed face, hole, clearance or factor is traded away, and nothing is
  reported that was not measured in this run.
