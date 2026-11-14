import json
from pathlib import Path
p=Path('tools/solidworks/playbook/eval/terra-high-d');d=json.loads((p/'d3_part2.json').read_text(encoding='utf-8'))
lines=['# D3 part two — edited native parts','', '| Plate | CAD mm³ | Hand mm³ | Mass g | Bodies | STL watertight | Minimum wall mm | Floor Z mm | Additional changes |','|---|---:|---:|---:|---:|---|---:|---:|---|']
for n,r in d['plates'].items():lines.append(f"| {n}_b | {r['volume_mm3']:.3f} | {r['hand_volume_mm3']:.3f} | {r['mass_g']:.3f} | {r['bodies']} | {r['stl_watertight']} | {r['min_wall_mm']:.3f} ({r['min_wall_feature']}) | {r['counterbore_floor_z_mm']:.1f} | {r['why']} |")
(p/'D3_part2_table.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
