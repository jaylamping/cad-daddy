"""Body masks for the D2 pair (by geometry; nodes at interfaces may belong to two bodies; counts printed)."""
import numpy as np
R_SEAT = 26.0
SCREWS = [(sx * 31.0, z) for sx in (1, -1) for z in (0.0, 7.0)]
PADS = [(17.68, 17.68), (-17.68, 17.68), (-17.68, -17.68), (17.68, -17.68)]
def masks(pos):
    x, y, z = pos[:, 0], pos[:, 1], pos[:, 2]
    r = np.hypot(x, y)
    pad = np.zeros(len(pos), bool)
    for px, py in PADS:
        pad |= (np.hypot(x - px, y - py) <= 0.95) & (z >= -0.86) & (z <= 0.16)
    ring = (r >= 23.99) & (r <= 25.97) & (z >= 0.14) & (z <= 7.16) & ~pad
    pin = np.zeros(len(pos), bool); near_pin = np.zeros(len(pos), bool)
    for sx, sz in SCREWS:
        da = np.hypot(x - sx, z - sz)
        pin |= ((da <= 1.55) & (y >= -0.51) & (y <= 28.51)) | ((da <= 2.95) & (y >= 28.49) & (y <= 31.51)) | ((da <= 2.01) & (y >= -6.21) & (y <= -0.49))
        near_pin |= (da <= 3.9) & (y >= -7.6) & (y <= 31.6)       # within about 1 mm of the pin surface everywhere
    recess = np.zeros(len(pos), bool)       # the pad recesses exist only in the FEA twin: leave their surroundings out of every reading
    for px, py in PADS:
        recess |= (np.hypot(x - px, y - py) <= 3.5) & (z >= -1.6) & (z <= 0.5)
    seatedge = ((np.abs(y) < 1.0) & ((np.abs(r - R_SEAT) < 1.0) | (np.abs(r - 23.0) < 1.0)))      # 1 mm round the seat and opening edges at the split plane (contact edge)
    house = ~(pad | ring | pin)
    return dict(recess=recess, seatedge=seatedge, pad=pad, ring=ring, pin=pin, upper=house & (y >= -1e-6), lower=house & (y <= 1e-6), near_pin=near_pin, house=house)
