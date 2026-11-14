from pathlib import Path
p=Path('tools/solidworks/playbook/eval/terra-high-b2/REPORT.md')
s=p.read_text(encoding='utf-8')
s=s.replace('20:17:29 | 3.2 mm tip candidate; 3 mm trial fails yield. The candidate is not approved for printing.', '20:17:29; follow-up 20:36:46–20:42:17 | Shortened plate and 3.2 mm tip candidate; 3 mm tip and window trials fail. The candidate is not approved for printing.')
a=s.index('## B3 — lighter bracket'); b=s.index('## B4 — tongue in a slot')
section='''## B3 — lighter bracket

`wall_bracket_light.SLDPRT` (SHA-256 `18e7a2c42c18d0dd612696186cdf7dd8880cbd634d50efa342b19ccd88be5f8f`) is the final candidate: one body, volume 7,778.438 mm³, **9.256 g** versus **22.705 g**, a **59.23%** mass saving at the same density. Its box is [0,13,4;65,27,56]; screw holes and the X=0 wall plane remain, as does the 10×10 top load face from X55–65 at Z52. I interpreted “wall face at X 0” as retaining its plane and the fixed holes, not retaining the original full 40×60 contact area; that interpretation needs agreement before use. Hole positions and R2.25 are independently measured in `measure_final.log`; each hole has 5.75 mm from its edge to the nearer plate end and 4.75 mm to a side. The STL is watertight, one shell, volume 7,779.725 mm³ and matching bounds. The 3.2 mm tip retains more than two nominal 0.6 mm walls; print support and anisotropy need process-specific checking. `bracket_light_final.png` shows the geometry.

The steps below list the available factors for the selected Y layer-normal trial, as **VM / layer tension / layer shear**. Values in parentheses are preliminary where not converged or not checked with both supports; they are not approval claims. Masses in g.

| Change | Mass | Factors | Evidence |
|---|---:|---|---|
| Narrow wall plate to 20 mm | 15.565 | (2.54 / 4.28 / 4.09) | 1.5 mm; Y shear not converged. |
| Narrow plate to 14 mm, sharp side root | 13.423 | (2.44 / 5.14 / 5.45) | 1.5 mm; fine mesh changed Y shear markedly. |
| Add R0.4 side roots | 13.424 | (2.37 / 3.68 / 2.00) | 1.2 mm hole support; 2 mm wall support shear factor 1.47. |
| Increase side-root radius to 1 mm | 13.431 | (2.39 / 5.33 / 2.99) | 1.2 mm hole support; 2 mm wall support shear factor 2.41. |
| Taper underside to 6 mm tip | 11.039 | (2.31 / 5.24 / 2.88) | 1.0 mm hole support; wall support also checked. |
| Taper to 4 mm tip | 10.242 | (2.41 / 4.99 / 2.92) | 1.5 mm preliminary hole support. |
| Taper to 3 mm tip | 9.843 | **1.92 / 5.08 / 2.86** | Yield fails at ~23.46 MPa near X49, 1.5 mm mesh. |
| Taper to 3.2 mm tip | 9.923 | **2.08 / 4.10 / 2.49** | Conservative of 1.2 mm hole and 2 mm wall support values. |
| Shorten plate to Z4–56 | 9.256 | **2.08 / 4.25 / 2.37** | Final candidate, values conservatively combined from finest hole and alternate wall support. |
| Add a 6×12 mm rounded-corner window in that plate | 8.829 | (2.07 / 3.76 / **1.70**) | Rejected: Y-layer shear rises from 7.25 to 7.63 MPa on 2→1.5 mm meshes, above 6.5 MPa allowed at factor 2. The window is saved separately. |

The final hole-supported 3/2/1.5/1.2/1.0 mm meshes have 9,857/17,773/35,487/62,650/99,566 nodes. At the last two, VM 21.675→21.68 MPa, Y tension 4.199→4.225 MPa and Y shear 4.328→4.505 MPa changed less than 5%; reaction at 1.0 mm is [-0.001,0.001,60.001] N and maximum displacement is 4.717 mm. The 1.2 mm wall-fixed alternative gave VM 21.675, Y tension 5.289 and Y shear 5.474 MPa; the table uses the higher values for each measure. The governing factor is **yield 2.08**, at approximately (48,17,47.5) mm. A 20% load increase would reduce it to about 1.73. An explicit read of the normally masked load neighbourhood at X>52 on the 1.2 mm mesh found VM 20.85 MPa, Y tension 5.12 MPa and Y shear 1.38 MPa, below the governing values from the alternate support. The 3 mm tip and 6 mm-wide plate-window trials stop further thinning along those families; they do not prove a globally optimal shape.

At X=35 mm the tapered section is 6.945 mm deep: hand surface bending stress is 18.66 MPa and the measured mean X stress at the upper surface is 18.95 MPa on 59 nodes (1.6% high). On the 1.0 mm hole-supported result, layer normals X/Y/Z respectively have peak tension 21.56/4.225/6.743 MPa and shear 6.367/4.505/6.360 MPa; the Y direction is preferable for this case. There is no separate compression strut in this solid cantilever for a direct Euler column calculation; overall lateral and local instability were not established.

The computed 4.72 mm tip displacement is about 8.6% of the 55 mm arm, so geometric nonlinearity and stability require a stronger check; a linear solve and these idealized restraints do not establish a safe printable part. No nonlinear, buckling, bolt preload, fatigue or actual print test was performed. A more conservative 6 mm-tip option remains as `wall_bracket_light_taper6.SLDPRT`. The 3 mm-tip script predicted the peak at the root even though a hand check near X49 already suggested the thin arm could govern; it printed stresses and continued when the peak moved there. The 3.2 mm rerun explicitly predicted the tip peak, and the missed stop is recorded rather than hidden. The R0.4 edge-selection attempt initially found zero edges because its Z bounds omitted the 37–55 mm end points; corrected bounds found two (`b3_round_failed.log`, `b3_edges.log`). Its initial node prediction also omitted curvature-driven refinement; the script continued to print stresses rather than stopping on the >2× node surprise. Those preliminary values were rechecked with the face boxes and later meshes, but the missed stop is a process failure.

'''
s=s[:a]+section+s[b:]; p.write_text(s,encoding='utf-8')
