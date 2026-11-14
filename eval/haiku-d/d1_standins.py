"""D1: stand-in STLs for the assembly pictures (rail, board) and idea B (flat cradle on the top of the rail).

Boxes only, written as binary STL in mm, model frame. They are for the pictures and the envelope check, not for a study.
"""
import struct
import sys
from pathlib import Path

import numpy as np

WT = Path(__file__).resolve().parents[2]
OUT = WT / '_wip' / 'sw-eval' / 'haiku-d' / 'd1'
OUT.mkdir(parents=True, exist_ok=True)


def box_tris(x0, y0, z0, x1, y1, z1):
    p = np.array([[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],
                  [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]], float)
    quads = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    tris = []
    for a, b, c, d in quads:
        tris += [(p[a], p[b], p[c]), (p[a], p[c], p[d])]
    return np.array(tris)


def write_stl(path, tris):
    with open(path, 'wb') as f:
        f.write(b'stand-in'.ljust(80, b' '))
        f.write(struct.pack('<I', len(tris)))
        for t in tris:
            n = np.cross(t[1] - t[0], t[2] - t[0])
            n = n / (np.linalg.norm(n) or 1.0)
            f.write(struct.pack('<3f', *n))
            for v in t:
                f.write(struct.pack('<3f', *v))
            f.write(struct.pack('<H', 0))


if __name__ == '__main__':
    rail = box_tris(-60, -10, -20, 60, 10, 0)                       # 20 x 20 rail along X, top face Z 0
    board_a = box_tris(-42.5, 17.5, -17, 42.5, 19.1, 43)             # 85 x 60 x 1.6, standing in the XZ plane
    write_stl(OUT / 'standin_rail.stl', rail)
    write_stl(OUT / 'standin_board_a.stl', board_a)
    # idea B: board flat on a cradle on the top of the rail (85 x 60 flat, Y ±30 wide, Z 20 high)
    cradle_b = box_tris(-42.5, -30, 0, 42.5, 30, 3)
    board_b = box_tris(-42.5, -30, 20, 42.5, 30, 21.6)
    write_stl(OUT / 'standin_cradle_b.stl', cradle_b)
    write_stl(OUT / 'standin_board_b.stl', board_b)
    print('written', sorted(p.name for p in OUT.glob('standin_*.stl')))
