"""Print the cylinders, planes and features of one or more measured parts: python show.py <key substring> ..."""
import json, sys
from pathlib import Path
m = json.loads((Path(__file__).parent / 'measured.json').read_text())
for pat in sys.argv[1:]:
    for k, v in m.items():
        if pat not in k or 'error' in v:
            continue
        print('==', k, 'vol', v['volume'], 'bbox', v['bbox'])
        print('   features:', ' '.join(n for n, t in v['features'] if t not in ('CommentsFolder','FavoriteFolder','HistoryFolder','SelectionSetFolder','SensorFolder','DocsFolder','DetailCabinet','SurfaceBodyFolder','SolidBodyFolder','EnvFolder','InkMarkupFolder','EqnFolder','MaterialFolder','OriginProfileFeature') and not n.endswith(' Plane')))
        for b in v['bodies']:
            print('   body', b)
        rows = []
        for f in v['faces']:
            if f['kind'] == 'cyl':
                ax = max(range(3), key=lambda i: abs(f['axis'][i]))
                o = [round(c, 2) for i, c in enumerate(f['origin']) if i != ax]
                rows.append((f['body'][:14], 'cyl', 'XYZ'[ax], f['r'], o, round(f['box'][ax], 2), round(f['box'][ax + 3], 2), f['area']))
            elif f['kind'] != 'plane':
                rows.append((f['body'][:14], f['kind'], '', 0, [round(x, 2) for x in f['box']], 0, 0, f['area']))
        for r in sorted(rows, key=lambda r: (r[0], r[1], r[2], r[3], r[4])):
            print('  ', *r)
        if '-p' in sys.argv:
            for f in v['faces']:
                if f['kind'] == 'plane':
                    print('   plane', f['body'][:14], f['normal'], [round(x, 2) for x in f['box']], f['area'])
