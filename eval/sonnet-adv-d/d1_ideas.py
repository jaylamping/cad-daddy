"""D1: the two ideas as crude solids (trimesh boxes, not SolidWorks), for the picture sheets only.
Idea A (chosen, built in SolidWorks as buck_mount): flat board on two bridges and four M3 screws into inserts.
Idea B: a 45 degree tilted cradle that the board slides into along X; two grooves and one retaining clip; board leaves along X."""
import numpy as np, trimesh
from pathlib import Path
OUT = Path(r'J:\code\cad-daddy-wt\sw-eval-sonnet-adv-d\_wip\sw-eval\sonnet-adv-d\d1'); OUT.mkdir(parents=True, exist_ok=True)
def box(lo, hi):
    lo, hi = np.array(lo, float), np.array(hi, float)
    m = trimesh.creation.box(extents=hi - lo); m.apply_translation((lo + hi) / 2); return m
rail = box((-80, -10, -20), (80, 10, 0))
# idea A: sketch of the same mount as buck_mount (base, bridges, pads) + board stand-in
A = trimesh.util.concatenate([box((-58, -10, 0), (58, 10, 4)), box((35, -30, 1), (43, 30, 8)), box((-43, -30, 1), (-35, 30, 8))]
        + [box((sx * 39 - 3.5, sy * 26.5 - 3.5, 8), (sx * 39 + 3.5, sy * 26.5 + 3.5, 11.5)) for sx in (1, -1) for sy in (1, -1)])
A.export(OUT / 'ideaA_mount.stl')
trimesh.util.concatenate([box((-42.5, -30, 11.5), (42.5, 30, 13.1))]).export(OUT / 'ideaA_board.stl')
rail.export(OUT / 'rail_sketch.stl')
# idea B: a tilted cradle. Board plane at 45 degrees about X (rises towards +Y); two groove blocks under the long ends.
th = np.radians(45)
R = trimesh.transformations.rotation_matrix(th, (1, 0, 0), (0, 0, 0))
def tilt(m, shift):
    m = m.copy(); m.apply_transform(R); m.apply_translation(shift); return m
# built flat in the board frame (x along rail, y across the board, z normal), then rotated 45 deg and lifted
frame = [box((-58, -10, -14), (58, 10, 0))]      # base on the rail top, replaced below by a plain plate
board = box((-42.5, -30, 0), (42.5, 30, 1.6))
rails_b = [box((-42.5, -31.5, -2), (42.5, -28.5, 3.0)), box((-42.5, 28.5, -2), (42.5, 31.5, 3.0))]   # grooves holding the long edges
stop = box((-45, -31.5, -2), (-42.5, 31.5, 3.0))                                                   # stop at the -X end
clip = box((42.5, -20, -2), (46, 20, 3.0))                                                          # latch at the +X end
shift = np.array([0, 3.0, 22.0])
Bm = trimesh.util.concatenate([tilt(m, shift) for m in rails_b + [stop, clip]] + [box((-58, -10, 0), (58, 10, 4)),
        box((-48, -12, 4), (-42, 12, 28)), box((42, -12, 4), (48, 12, 28))])
Bm.export(OUT / 'ideaB_mount.stl')
tilt(board, shift).export(OUT / 'ideaB_board.stl')
print('ideas written')
