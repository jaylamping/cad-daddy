import json
from pathlib import Path
p=Path('tools/solidworks/playbook/eval/terra-high-d');d=json.loads((p/'d3_part1.json').read_text(encoding='utf-8'))
lines=['# D3 part one — written before the change','', '| Plate | CAD mm³ | Hand mm³ | Mass g | Bodies | STL watertight | Minimum wall mm | Modified |','|---|---:|---:|---:|---:|---|---:|---|']
for n,r in d['plates'].items():lines.append(f"| {n} | {r['volume_mm3']:.3f} | {r['hand_volume_mm3']:.3f} | {r['mass_g']:.3f} | {r['bodies']} | {r['stl_watertight']} | {r['min_wall_mm']:.3f} ({r['min_wall_feature']}) | {r['why'] or 'No'} |")
(p/'D3_part1_table.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
