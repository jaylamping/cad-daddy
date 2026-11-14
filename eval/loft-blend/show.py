"""Print fea.json and link_fea.json as tables."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
f = HERE / 'fea.json'
if f.exists():
    for k, v in json.loads(f.read_text()).items():
        for c, x in v.items():
            print(f"{k:34s} ctrl {c} nodes {x['nodes']:7d} vol {x['volume']:9.1f} junction {x['junction_vm']:6.2f} at {x['at']} "
                  f"avg1mm {x['junction_avg_1mm']} p1 {x['junction_p1']:6.2f} plain {x['plain_section_vm_z25']:5.2f} "
                  f"disp {x['tip_disp']} Ry {x['reaction'][1]}")
            print('      half-width in Y by height:', x['profile_y'])
f = HERE / 'link_fea.json'
if f.exists():
    for k, v in json.loads(f.read_text()).items():
        for c, x in v.items():
            print(f"link {k:6s} el {c} nodes {x['nodes']:7d} vol {x['volume']:9.1f} junction {x['junction_vm']:6.2f} at {x['at']} "
                  f"avg1 {x['junction_avg_1mm']} avg2 {x['junction_avg_2mm']} rest {x['rest_of_link_vm']} "
                  f"overall {x['overall_away']} disp {x['disp']} Ry {x['reaction'][1]}")
