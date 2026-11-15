"""Readings from a saved D2 result: screw loads from shank sections, body peaks, layer measures per half, seat opening, pad share."""
import sys, json
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from d2_masks import masks, SCREWS
def _fit(pos, vals, sx, sz):
    """Value at the section centre of a plane fitted over the nodes (area mean of a linear field), so that bending does not bias the mean."""
    A = np.c_[np.ones(len(pos)), pos[:, 0] - sx, pos[:, 2] - sz]
    coef, *_ = np.linalg.lstsq(A, vals, rcond=None)
    return float(coef[0])
def screw_loads(pos, s, ys=(8.0, 14.0, 20.0), half=1.5):
    """Tension (N, + pulls the screw) and shear (N) per screw: the plane-fitted stress at the centre of the shank section times its area."""
    out = []
    for sx, sz in SCREWS:
        rows = []
        for y0 in ys:
            sel = (np.abs(pos[:, 1] - y0) <= 1.0) & (np.hypot(pos[:, 0] - sx, pos[:, 2] - sz) <= half + 0.01)
            if sel.sum() < 12: rows.append(None); continue
            A = np.pi * 1.5 ** 2
            rows.append(dict(y=y0, n=int(sel.sum()), tension=_fit(pos[sel], s[sel, 2], sx, sz) * A, tension_plain_mean=float(s[sel, 2].mean() * A),
                             shear_x=_fit(pos[sel], s[sel, 4], sx, sz) * A, shear_z=_fit(pos[sel], s[sel, 6], sx, sz) * A))
        out.append(dict(screw=(sx, sz), sections=rows))
    return out
def read(path, excl=1.0, away=False):
    z = np.load(path); pos, s, disp = z['pos'], z['s'], z['disp']; m = masks(pos)
    res = dict(nodes=int(z['nodes']), el=float(z['el']), reaction=z['reaction'].tolist())
    # distance of every node from the pin surfaces: the rim of a bonded head and insert is a singular edge
    ok_far = ~m['near_pin'] & ~m['recess']
    for half in ('upper', 'lower'):
        keep = m[half] & ok_far & (~m['seatedge'] if away else True)
        row = dict(vm=float(s[keep, 10].max()), vm_all=float(s[m[half], 10].max()))
        for nm, n in (('Y', (0, 1, 0)), ('Z', (0, 0, 1)), ('X', (1, 0, 0))):
            n = np.array(n, float)
            sn = n[0] ** 2 * s[:, 1] + n[1] ** 2 * s[:, 2] + n[2] ** 2 * s[:, 3] + 2 * (n[0] * n[1] * s[:, 4] + n[0] * n[2] * s[:, 5] + n[1] * n[2] * s[:, 6])
            t = np.c_[s[:, 1] * n[0] + s[:, 4] * n[1] + s[:, 5] * n[2], s[:, 4] * n[0] + s[:, 2] * n[1] + s[:, 6] * n[2], s[:, 5] * n[0] + s[:, 6] * n[1] + s[:, 3] * n[2]]
            tau = np.linalg.norm(t - np.outer(t @ n, n), axis=1)
            row[f'layer_{nm}'] = float(sn[keep].max()); row[f'shear_{nm}'] = float(tau[keep].max())
            i = np.flatnonzero(keep)[np.argmax(sn[keep])]; row[f'layer_{nm}_at'] = pos[i].round(2).tolist()
        i = np.flatnonzero(keep)[np.argmax(s[keep, 10])]; row['vm_at'] = pos[i].round(2).tolist()
        res[half] = row
    res['pad_vm_max'] = float(s[m['pad'], 10].max())
    res['pad_force_bound_N'] = float(s[m['pad'], 10].max() * 4 * np.pi * 0.9 ** 2)
    res['screws'] = screw_loads(pos, s)
    res['ring_mean_disp'] = disp[m['ring'], 1:4].mean(axis=0).tolist()
    res['upper_mean_disp'] = disp[m['upper'], 1:4].mean(axis=0).tolist()
    res['lower_mean_disp'] = disp[m['lower'], 1:4].mean(axis=0).tolist()
    res['max_disp'] = float(np.abs(disp[:, 4]).max())
    return res
if __name__ == '__main__':
    r = read(sys.argv[1]); print(json.dumps(r, indent=1)[:6000])
