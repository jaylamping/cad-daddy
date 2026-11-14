"""judge() on the rows the benchmark runs produced, against what an independent check said.

    python eval/read-results/regression.py <checkout of haiku-followup>/eval      # no SolidWorks; writes regression.json

Round one's rows are on branch haiku-runs, round two's (the follow-up) on haiku-followup, which holds both. With a
checkout of haiku-runs the round-two cases are left out and it says so.

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


def show(name, r, verdict, lowest, entry=None, growing=()):
    out[name] = r
    marked = sorted(q['entry'] for q in r['rows'] if q['step_growing'])
    ok = (r['verdict'] == verdict and abs(r['lowest_factor'] - lowest) < 0.011 and entry in (None, r['lowest_entry'])
          and marked == sorted(growing))
    print(f'{"ok  " if ok else "FAIL"} {name}: {r["verdict"]}, lowest {r["lowest_factor"]} at "{r["lowest_entry"]}",'
          f' growing steps {marked} (expected {verdict}, {lowest}, {sorted(growing)})', flush=True)
    if not ok:
        raise SystemExit(1)


# T5: the ribbed bracket at 3.0 / 2.2 / 1.6 mm, three measures, for each way it could be printed. Von Mises sits on a
# sharp rib toe and rises 3.6 % and then 13.1 %: a growing step, so "not shown" in every direction. That is what
# happened next: with the toes rounded (round two, below) it settled and passed.
t5 = json.loads((SRC / 'haiku-plan-a' / 't5_rows.json').read_text(encoding='utf-8'))
t5 = [t5[k] for k in ('T5_RIB_30', 'T5_RIB_22', 'T5_RIB_16')]
for way, verdict, lowest in (('Y', 'not shown', 3.02), ('X', 'not shown', 2.13), ('Z', 'not shown', 2.15)):
    series = {f'layers along {way}, {m}': [row['table'][way][m] for row in t5] for m in ALLOW}
    show(f'T5 ribs, layers along {way}', judge(series, {k: ALLOW[k.split(', ')[1]] for k in series}), verdict, lowest,
         growing=[f'layers along {way}, vm'])

# T6: contact pressure under the pin and the block's von Mises at hole controls 1.2 / 0.8 / 0.5 mm, against yield.
# The pressures go both ways by up to 0.81 MPa, which is under the floor of 1.125 MPa (5 % of 45 / 2): as a verdict
# on strength it passes at 6.65. Whether the pressure itself is known to 5 % is another question, and the answer was
# no (it moved 13.6 %) until round two read it as a mean along the line of contact.
t6 = json.loads((SRC / 'haiku-plan-a' / 't6_rows.json').read_text(encoding='utf-8'))[:3]
series = {'pressure mid-length': [r['p_mid'][0] for r in t6], 'pressure at the mouth': [r['p_mouth'][0] for r in t6],
          'pressure, whole hole': [r['p_all'][0] for r in t6], 'block von Mises': [round(r['block_vm'][0], 2) for r in t6]}
show('T6 pin in a hole', judge(series, dict.fromkeys(series, 45.0)), 'pass', 6.65, 'pressure mid-length')

# D2: two halves, two load cases, one mesh size, both halves printed with layers along Z. The bonded twin
# (D2_YBOND_30) proves the contact and is not a load case, so it is left out.
d2 = json.loads((SRC / 'haiku-plan-d' / 'd2_rows.json').read_text(encoding='utf-8'))
series = {f'{half} half, +{case}, {m}': [d2[f'D2_{case}_30'][half]['Z'][m]]
          for half in ('upper', 'lower') for case in 'YX' for m in ALLOW}
show('D2 housing', judge(series, {k: ALLOW[k.split(', ')[2]] for k in series}), 'not shown', 5.82, 'lower half, +X, shear')

# Round two, the follow-up runs
toe, d2c = SRC / 'haiku-plan-a-followup' / 't5_toe_rows.json', SRC / 'haiku-plan-d-followup' / 'd2c_rows.json'
if toe.exists() and d2c.exists():
    # T5 with R2 rib toes at 3.0 / 2.2 / 1.6 mm, printed on its side: every measure settles
    t5 = json.loads(toe.read_text(encoding='utf-8'))
    t5 = [t5[k] for k in ('T5_TOE_30', 'T5_TOE_22', 'T5_TOE_16')]
    series = {f'layers along Y, {m}': [row['table']['Y'][m] for row in t5] for m in ALLOW}
    show('T5 rounded toes, layers along Y', judge(series, {k: ALLOW[k.split(', ')[1]] for k in series}), 'pass', 2.99,
         'layers along Y, layer')
    # D2 at seat controls 1.2 / 0.9 / 0.7 mm, both cases. Two shear entries rise with growing steps: the lower half
    # under +X (2.02, 2.43, 3.12) and the upper half under +Y (1.31, 1.40, 1.81). Both are where a corner of the
    # steel ring bears on the rim of a seat; 1 mm away the stress is settled (eval/haiku-followup-CHECK.md). Four
    # other entries move by a large share of a small stress and are settled by the floor.
    d2 = json.loads(d2c.read_text(encoding='utf-8'))
    series = {f'{half} half, +{case}, {m}': [d2[f'D2C_{case}_{cs}'][half]['Z'][m] for cs in ('12', '09', '07')]
              for half in ('upper', 'lower') for case in 'YX' for m in ALLOW}
    show('D2 housing, three sizes', judge(series, {k: ALLOW[k.split(', ')[2]] for k in series}), 'not shown', 4.16,
         'lower half, +X, shear', growing=['lower half, +X, shear', 'upper half, +Y, shear'])
else:
    print(f'left out: the round-two cases ({toe.parent.name}, {d2c.parent.name} are not under {SRC})', flush=True)

(Path(__file__).parent / 'regression.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
print('PASS regression', flush=True)
