import json
from pathlib import Path
p=Path('tools/solidworks/playbook/eval/terra-high-b2/results.json')
r=json.loads(p.read_text(encoding='utf-8')); b=r['B3']; b.update(mass_after_g=9.256341277,saving_pct=59.231619,sf_yield=45/21.68,sf_layer=22.5/5.28858757,sf_shear=13/5.4742544,governing='von Mises yield near the tapered tip, factor 2.08',notes='Linear-static candidate, not approved for printing. Hole-supported 1.0 mm and wall-supported 1.2 mm results are combined conservatively; 4.72 mm displacement, nonlinear stability and real fasteners remain unchecked. Full original wall-face area was not retained.')
b['steps'].extend([{'change':'shorten wall plate to Z4–56','mass_g':9.256341277,'sf_yield':45/21.68,'sf_layer':22.5/5.28858757,'sf_shear':13/5.4742544,'notes':'final candidate: 1.0 mm hole support and 1.2 mm alternate wall support'}, {'change':'add rounded 6×12 mm plate window','mass_g':7419.124773814782*.00119,'sf_yield':45/21.69,'sf_layer':22.5/5.983,'sf_shear':13/7.6347906,'notes':'rejected: Y-layer shear exceeds the factor-2 limit; 1.5 mm hole support'}])
r['B2']['notes']+=' A separate R2 mm side-root trial gives conservative VM/layer/shear factors 2.25/3.83/2.57 with Y-normal printing; this is a design variant, not the requested original.'
p.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
