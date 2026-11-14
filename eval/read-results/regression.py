"""judge() on the rows three benchmark runs produced (branch haiku-runs), against what an independent check said.

    python eval/read-results/regression.py <checkout of haiku-runs>/eval      # no SolidWorks; writes regression.json

Limits are the ones the runs' own factors were worked out with: von Mises 45, tension across layers 22.5, shear
between layers 22.5 / sqrt(3) = 12.99 MPa.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'solidworks'))
from swfea import judge  # noqa: E402

SRC = Path(sys.argv[1])
ALLOW = dict(vm=45.0, layer=22.5, shear=22.5 / 3 ** 0.5)
out = {}


def show(name, r, verdict, lowest, entry=None):
    out[name] = r
    ok = r['verdict'] == verdict and abs(r['lowest_factor'] - lowest) < 0.011 and entry in (None, r['lowest_entry'])
    print(f'{"ok  " if ok else "FAIL"} {name}: {r["verdict"]}, lowest {r["lowest_factor"]} at "{r["lowest_entry"]}"'
          f' (expected {verdict}, {lowest})', flush=True)
    if not ok:
        raise SystemExit(1)


# T5: the ribbed bracket at 3.0 / 2.2 / 1.6 mm, three measures, for each way it could be printed
t5 = json.loads((SRC / 'haiku-plan-a' / 't5_rows.json').read_text(encoding='utf-8'))
t5 = [t5[k] for k in ('T5_RIB_30', 'T5_RIB_22', 'T5_RIB_16')]
for way, verdict, lowest in (('Y', 'margin, not converged', 3.02), ('X', 'not shown', 2.13),
                             ('Z', 'not shown', 2.15)):
    series = {f'layers along {way}, {m}': [row['table'][way][m] for row in t5] for m in ALLOW}
    show(f'T5 ribs, layers along {way}', judge(series, {k: ALLOW[k.split(', ')[1]] for k in series}), verdict, lowest)

# T6: contact pressure under the pin and the block's von Mises at hole controls 1.2 / 0.8 / 0.5 mm, against yield
t6 = json.loads((SRC / 'haiku-plan-a' / 't6_rows.json').read_text(encoding='utf-8'))[:3]
series = {'pressure mid-length': [r['p_mid'][0] for r in t6], 'pressure at the mouth': [r['p_mouth'][0] for r in t6],
          'pressure, whole hole': [r['p_all'][0] for r in t6], 'block von Mises': [round(r['block_vm'][0], 2) for r in t6]}
show('T6 pin in a hole', judge(series, dict.fromkeys(series, 45.0)), 'margin, not converged', 6.65, 'pressure mid-length')

# D2: two halves, two load cases, one mesh size, both halves printed with layers along Z. The bonded twin
# (D2_YBOND_30) proves the contact and is not a load case, so it is left out.
d2 = json.loads((SRC / 'haiku-plan-d' / 'd2_rows.json').read_text(encoding='utf-8'))
series = {f'{half} half, +{case}, {m}': [d2[f'D2_{case}_30'][half]['Z'][m]]
          for half in ('upper', 'lower') for case in 'YX' for m in ALLOW}
show('D2 housing', judge(series, {k: ALLOW[k.split(', ')[2]] for k in series}), 'not shown', 5.82, 'lower half, +X, shear')

(Path(__file__).parent / 'regression.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
print('PASS regression', flush=True)
