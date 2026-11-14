# Blending a loft into the feature it grows from: trials

2026-11-14, holly-pc, SolidWorks 2026 SP0. The open row in [03-modelling.md](../../playbook/03-modelling.md): `fillet()`
returns nothing where a loft meets another feature, and that sharp junction was the stress peak on two benchmark links
(eval/sonnet-c2, eval/terra-high-c).

## What was found

1. **The loft is not the cause. Polyline rounds in the parent are.** On the real link the stem crosses a revolved
   flange whose rim round and lip were drawn as straight segments. Every segment revolves into its own cone face, the
   stem crosses 14 of them, and the seam is 32 edges, the shortest 0.04 mm. No fillet of any form builds on that.
   The same stem on the same flange with its two rim rounds drawn as true arcs meets 5 faces in 12 edges, the shortest
   1.64 mm, and the ordinary edge fillet builds at 1 and 2 mm.
2. **On a flat face everything builds.** A stem lofted up from a flat disc has a seam of one edge. `edges_where` +
   `fillet()`, a fillet on the face's own edges, and a face fillet all built at every radius tried, 0.5 to 8 mm.
3. **Where a fillet will not build, a second loft over the junction does**, on the test part and on the real link, and
   it lowers the junction peak. It is not a tangent round on the link: it leaves a shallow crease, and the peak there
   still creeps up with the mesh.

## Test part

A 60 mm disc, 6 thick, with a stem lofted through four closed-spline sections from 1 mm inside the disc to 60 mm above
it: 20 x 12 ellipse at the foot, 14 x 18 and squarer (exponent 3) at the top. [common.py](common.py),
[trials.py](trials.py), numbers in [trials.json](trials.json).

| # | Method | Built | Radii that built, mm | Rebuild errors | Volume added at 4 mm, mm³ |
| --- | --- | --- | --- | --- | --- |
| 0 | `edges_where` + `fillet()` (the house way) | yes | 4 (first tried) | none | 184.7 |
| 1 | Edge fillet, edges taken from the disc face's own edge list, propagation on | yes | 0.5, 1, 2, 3, 4, 5, 6, 8 | none | 184.7 |
| 2 | Face fillet, stem side face against disc top face | yes | 0.5, 1, 2, 3, 4, 5, 6, 8 | none | 185.3 |
| 3 | Round designed in: the stem's own loft starts on a flared section in the disc face, five sections along a quarter circle | yes | 1, 2, 4, 6, 8 | none | 198.3 |
| 4a | Separate skirt loft, five sections along a quarter circle, last one 0.15 mm inside the stem | yes | 1, 2, 4, 6, 8 | none | 201.6 |
| 4b | Separate skirt, two sections, end tangency normal to profile | yes | 1, 2, 4, 6, 8 | none | 282.7 |
| 4c | Separate skirt, two sections, no tangency | yes | 1, 2, 4, 6, 8 | none | 461.0 |
| 5 | Variable-radius fillet on the seam | no | none of 1, 2, 4 | (no feature) | |

Method 3 is not a clean round at small radii: at 1 mm it added 55.8 mm³ where a true round adds 10.7, at 2 mm 76.2
against 44.4. The crowded sections at the foot pull the spline of the whole stem: at 4 mm the stem stood 0.08 to
0.17 mm fatter between 4 and 12 mm up, and its stress at mid height changed (2.08 against 1.98 MPa). Method 4a leaves
the stem untouched.

A revolved skirt was not tried: the stem is oval, and a ring about one axis cannot follow it.

### Stress

20 N along Y at the top (bending the stem the weak way), disc held underneath. Hand value at the foot,
M c / I for a 20 x 12 ellipse: 1200 x 6 / 1696 = 4.24 MPa. Mesh 2.5 mm, with the control size below on every face
above the disc and twice that on the disc top. Peak von Mises between the disc face and 14 mm up.
[fea.py](fea.py), [fea.json](fea.json).

| Part | 1.2 mm control | 0.8 mm control | Change | Peak is at height |
| --- | --- | --- | --- | --- |
| Sharp | 5.96 (80,621 nodes) | 6.67 (206,092) | +12 %, not converged: a singular corner | 0.3 to 0.5 mm |
| 1: edge fillet 4 mm | 4.81 | 4.95 | +2.9 % | 3.2 to 3.4 mm, top of the round |
| 2: face fillet 4 mm | 4.85 | | | 2.9 mm |
| 3: flared loft 4 mm | 4.42 | 4.45 | +0.7 % | 3.0 mm (the stem above it is fatter too, so this is not the blend alone) |
| 4a: arc skirt 4 mm | 4.76 | 5.04 | +5.9 %, just outside 5 % | 3.8 mm, where it sinks into the stem |
| 4b: two-section skirt, normal end | 5.34 | | | 3.1 mm |
| 4c: two-section skirt, plain | 5.30 | | | 4.5 mm |
| 3 at 2 mm | 5.31 | | | 1.5 mm |
| 4a at 2 mm | 5.38 | | | 1.8 mm |

The arc skirt reads within 2 % of a real 4 mm fillet at both meshes (4.76 against 4.81, 5.04 against 4.95), and 24 %
under the sharp corner at the finer mesh. The two-section skirts are a cone, not a round, and give half the gain. At
2 mm the gain halves. Reactions were 20.0 N, and the stress at mid height was 1.96 to 1.99 MPa in every part but
method 3.

Two solves failed with solver error 24 when run as the second and the third study of one instance while two other
instances were solving (the study after them was never reached); all three passed alone in a fresh instance.

## Real link (eval/sonnet-c2)

Rebuilt from that run's numbers by [link.py](link.py): a flange revolved about Y (D70, 8 thick, rim round and lip as
polylines), a ridge loft on its back, and the stem lofted through eight superellipse sections along -Z, starting at
Z -32 just inside the rim. Numbers in [link_trials.json](link_trials.json).

The seam (edges where the stem's faces meet any other face): 32 edges, lengths 0.04, 0.04, 0.16, 0.16, 0.29, 0.30,
0.52 ... 12.42 mm, against 14 faces (1 plane, 1 cylinder, 12 neither: the cones of the polyline rounds, and the ridge).

| # | Method | Built | Detail |
| --- | --- | --- | --- |
| 1 | Edge fillet on all 32 seam edges, propagation on | no | none of 5, 4, 3, 2, 1, 0.5 mm |
| 1 | The same, one edge at a time, 2 mm | 10 of 32 | the 22 that refuse include both 0.04 mm edges, all six of 0.5 mm and both of 12.4 mm |
| 2 | Face fillet, 5 stem faces against the 14 others | no | none of 5, 4, 3, 2, 1 mm, with and without the uniform-radius option |
| 5 | Edges that round alone at 1 mm (19 of 32 without propagation), taken together | no | none of 3, 2, 1 mm |
| 5 | Multi-radius and variable-radius over the whole seam | no | four forms of the call, 1 mm |
| 3 | Rooted loft: the stem's first section replaced by ones that dive into the flange, the last (40 x 7.2 at Z -26) wholly inside it | yes | two variants, no rebuild errors, one body; seam 20 edges, shortest 0.55 mm |
| 4 | Skirt: a second loft of three sections over the sharp junction, from inside the flange to 0.15 mm inside the stem at Z -46 | yes | +1,190 mm³, no rebuild errors, one body |
| | The cause removed: flange rim rounds as true arcs (no lip, no ridge) | | seam 12 edges, shortest 1.64 mm, 5 faces. Edge fillet builds at 2 and 1 mm, not at 3, 4, 5; face fillet at 1 mm only |

Method 5 is recorded as "did not build with these calls": the variable-radius arguments were guessed, not looked up.

### Stress

The run's governing case: 60 N along +Y at the wrist pin, the elbow ring face held, one global mesh size with 1.2 mm on
the pin bore. Peak von Mises between Z -52 and -20, outside the default exclusion. [link_fea.py](link_fea.py),
[link_fea.json](link_fea.json).

| Link | 3.0 mm | 2.5 mm | 2.0 mm | Mean within 2 mm of the peak, 2.0 mm mesh | Factor on 45 MPa, 2.0 mm |
| --- | --- | --- | --- | --- | --- |
| Sharp | 27.51 (93,271 nodes) | 24.18 | 25.31 (197,729) | 11.35 | 1.78 |
| 3: rooted loft (m3a) | 17.48 | 18.22 | 19.27 | 11.94 | 2.33 |
| 3: rooted loft, three root sections (m3b) | 17.57 | | | | |
| 4: skirt (m4a) | 15.14 | 15.50 | 18.12 | 10.73 | 2.48 |

- The sharp peak sits on the stem's blunt end at (5.7, 7.3, -32.0) at every size and does not settle (27.5, 24.2,
  25.3). The benchmark run reported 21.1 and 23.2 at 3.0 and 2.5 mm for the same case.
- Both blends take the peak down at every mesh size: 36 to 45 % at 3 mm, 24 to 28 % at 2 mm. Neither has converged:
  the rooted loft rose 10 % from 3 to 2 mm, the skirt 17 % at the last step. The peak moved to the crease where the
  new surface crosses the flange's lip (X 12 to 14, Y 4.6 to 4.9, Z -32 to -33), which is still an edge, only a
  shallow one.
- The mean over 2 mm does not move (11.4, 11.9, 10.7 MPa): the blend removes a corner, it does not add section.
- Mass: +0.6 g for the rooted loft, +1.4 g for the skirt (PETG).

### With the cause removed

The true-arc flange has no lip and no ridge, so the cable passage breaks out of its +Y face and that sets the level;
the numbers are not comparable with the table above, only with each other.

| Link | 3.0 mm | 2.0 mm | Where |
| --- | --- | --- | --- |
| True-arc flange, sharp | 57.51 | 62.64 | the junction, (7.6, 4.0, -31.8); rising |
| True-arc flange, 2 mm edge fillet | 53.85 | 54.04 | the cable mouth, (2.1, 4.2, -30.8); settled within 0.4 % |

With a real fillet the junction is no longer the peak of the part and the peak that is left converges.

## What became of it

- `swkit.skirt()` and `swkit.offset_loop()`: method 4a as a helper for a stem on a flat face. `selftest.py blend`
  checks its volume against a true round and samples the STL either side of the round's surface.
- The row in 03-modelling.md is replaced by the cause, the three cures in order, their limits and these numbers.
- Not done: a blend that is tangent to a faceted or doubly curved parent. The rooted loft and the hand-drawn skirt
  on the link are sections chosen by eye; there is no helper for that case.
