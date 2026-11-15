import json
from common import *
rows = json.load(open(RUN / 't6_rows.json'))
post = json.load(open(RUN / 't6_post2.json'))
def line(tag, key, label):
    r = rows[key][-1]
    p = post.get(tag)
    if p is None:
        return f'| {label} | missing |'
    return (f"| {label} | {r['el_ctrl']} | {r['nodes']:,} | {r['solve_s']} | {r['reaction'][2]} | {r['reaction_pads'][2]} | {r['pad_share_pct']} | {p['pin_centre_mean_uz_mm']} | "
            f"{p['smoothed_1.0mm']['peak_mpa']} / {p['smoothed_2.0mm']['peak_mpa']} / {p['raw_peak_mpa']} | {p['half_width_mm']} | {p['block_vm_raw_max']['mpa']} at {p['block_vm_raw_max']['at']} |")
print('| Model, case | contact-face size | nodes | s | Fz | pads Fz | pad share % | pin mean uz mm | peak pressure 1 mm / 2 mm / raw MPa | half-width mm | block vm raw max at |')
for key in rows:
    if key.endswith('FAILED'):
        print('FAILED', key, rows[key]); continue
for key, tag, label in (('E centred, contact set, ctrl1.2', 'T6_E_centred,_contact_set,_ctrl1.2', 'centred, 1.2'),
                        ('E centred ctrl0.8', 'T6_E_centred_ctrl0.8', 'centred, 0.8'),
                        ('E centred ctrl0.6', 'T6_E_centred_ctrl0.6', 'centred, 0.6'),
                        ('E centred proof 0.001 ctrl0.8', 'T6_E_centred_proof_0.001_ctrl0.8', 'centred, proof 0.001 working direction'),
                        ('C full load ctrl1.2', 'T6_C_full_load_ctrl1.2', 'seated, 1.2'), ('A full load ctrl0.8', 'T6_A_full_load_ctrl0.8', 'seated, 0.8'),
                        ('D full load ctrl0.6', 'T6_D_full_load_ctrl0.6', 'seated, 0.6'), ('B reversed 0.001 load ctrl0.8', 'T6_B_reversed_0.001_load_ctrl0.8', 'seated, reversed 0.001')):
    if key in rows:
        print(line(tag, key, label))
