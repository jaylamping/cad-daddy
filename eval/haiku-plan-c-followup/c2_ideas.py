"""C2, stage 1 (shape): the two ideas as quick models, the first checkpoint, and the choice.   python c2_ideas.py

Idea A "bone": one stem that changes section. Idea B "open frame": a thin blade with a long window, two slim legs.
The choice is made by the rule in choose() from numbers this run measured; the executor does not pick by eye."""
import shutil

from common import *

if not (HERE / 'restate.md').exists():
    raise SystemExit('restate.md is not in eval/<run>/ yet: do C_C2.md step 1 before any modelling')
if clock('C2 start') is None:
    raise SystemExit("times.log has no 'C2 start' line: do C_C2.md step 1")
stamp(HERE, 'C2 ideas start (restate.md present)')
mass_before = got('C1', 'mass_g')
before_from = 'C1 run'
if mass_before is None:                         # C1 did not finish: the hand value stands in, and the report says so
    mass_before, before_from = round(boxy_hand_volume()['total'] * DENS_G_MM3, 2), 'hand value (C1 has no mass_g)'
log('boxy mass g', mass_before, before_from)

ideas = {}
with job(wait_s=1800) as j:
    for key, table_name, window in (('A', 'STEM_A', False), ('B', 'STEM_B', True)):
        model, stl = WIP / f'idea_{key.lower()}.SLDPRT', WIP / f'idea_{key.lower()}.stl'
        hand = beam_factors(TABLES[table_name], WINDOW_B if window else None)
        row = dict(table=table_name, window=window, hand_factor_load_y=hand['y'][0], hand_factor_load_y_at_z=hand['y'][1],
                   hand_factor_load_x=hand['x'][0], hand_factor_load_x_at_z=hand['x'][1], built=False)
        try:
            d, m = build_form(j, model, table_name, window)
            export(j.sw, d, stl)
            st = stl_stats(stl)
            close(j.sw, d)
            png = PICS / f'idea_{key.lower()}.png'
            shape = picture([stl], png)[stl.name]
            row.update(built=True, measured=m, bodies=1, volume_mm3=m['form_mm3'], mass_g=round(m['form_mm3'] * DENS_G_MM3, 2),
                       shape=shape, stl_watertight=st['watertight'], stl_shells=st['shells'], picture=f'pictures/{png.name}')
        except Failed as ex:
            row['error'] = str(ex)
            log(f'idea {key} did not build: {ex}')
        ideas[key] = row
        put('C2', ideas=ideas)
        if key == 'A' and row['built']:           # the first checkpoint: the whole form, crude
            shutil.copyfile(PICS / 'idea_a.png', PICS / 'checkpoint_01.png')
            t1 = since_c2('C2 checkpoint_01')
            missing = ('crude form only: no screw holes, screw-head clearances, pin holes or cable passage yet, nothing '
                       'measured against the fixed items, no study; '
                       f"mass {row['mass_g']} g against {mass_before} g boxy; sharp_per_area {row['shape']['sharp_per_area']}, "
                       f"flat_share {row['shape']['flat_share']}")
            put('C2', checkpoints=[dict(n=1, minutes_since_c2_start=t1, picture='pictures/checkpoint_01.png', missing=missing)],
                checkpoint_01_within_20_min=bool(t1 <= 20.0))
            log(f'checkpoint_01 at {t1} min since C2 start (limit 20)')
    if not ideas['A']['built'] and ideas['B']['built']:      # A did not build: B's picture is the first checkpoint
        shutil.copyfile(PICS / 'idea_b.png', PICS / 'checkpoint_01.png')
        t1 = since_c2('C2 checkpoint_01')
        put('C2', checkpoints=[dict(n=1, minutes_since_c2_start=t1, picture='pictures/checkpoint_01.png',
                                    missing='idea A did not build; this is idea B, crude: no holes, clearances, pin holes '
                                            'or cable passage, nothing measured, no study')],
            checkpoint_01_within_20_min=bool(t1 <= 20.0))


def eligible(r):
    return bool(r['built'] and r['bodies'] == 1 and r['mass_g'] < mass_before
                and r['hand_factor_load_y'] >= 2.5 and r['hand_factor_load_x'] >= 2.5)


def choose():
    """The rule. An idea is eligible when it built as one body, weighs less than the boxy link, and its hand beam
    factor on yield is at least 2.5 for a load along Y and along X. Two eligible: the lower sharp_per_area wins, and
    A wins a tie within 10 %. One eligible: that one. None: A with the thicker table STEM_A2."""
    ok = {k: eligible(r) for k, r in ideas.items()}
    if ok['A'] and ok['B']:
        a, b = ideas['A']['shape']['sharp_per_area'], ideas['B']['shape']['sharp_per_area']
        pick_ = 'A' if a <= 1.10 * b else 'B'
        why = f'both eligible; sharp_per_area A {a}, B {b}'
    elif ok['A'] or ok['B']:
        pick_ = 'A' if ok['A'] else 'B'
        other = 'B' if pick_ == 'A' else 'A'
        o = ideas[other]
        why = (f'only {pick_} is eligible; {other}: built {o["built"]}, hand factor load Y {o["hand_factor_load_y"]} at Z '
               f'{o["hand_factor_load_y_at_z"]}, load X {o["hand_factor_load_x"]} (2.5 needed), mass {o.get("mass_g")} g')
    else:
        pick_, why = 'A2', 'neither idea is eligible as built: A goes on with the thicker table STEM_A2'
    return pick_, ok, why


chosen, ok, why = choose()
table_name = dict(A='STEM_A', B='STEM_B', A2='STEM_A2')[chosen]
put('C2', chosen=chosen, table_name=table_name, window=bool(chosen == 'B'), eligible=ok, choice_reason=why,
    ideas_tried=[dict(idea=k, name='bone: one stem that changes section' if k == 'A' else 'open frame: blade with a window, two legs',
                      built=r['built'], mass_g=r.get('mass_g'), shape=r.get('shape'), hand_factor_load_y=r['hand_factor_load_y'],
                      hand_factor_load_x=r['hand_factor_load_x'], eligible=ok[k], picture=r.get('picture')) for k, r in ideas.items()],
    mass_before_g=mass_before, mass_before_from=before_from)
t = since_c2('C2 ideas end')
lines = []
for k, r in ideas.items():
    if r['built']:
        lines.append(f"| {k} | {r['measured']['loft_mode']}, {r['measured']['order']} | {r['mass_g']} | {r['shape']['flat_share']} | "
                     f"{r['shape']['largest_flat']} | {r['shape']['sharp_mm']} | {r['shape']['sharp_per_area']} | "
                     f"{r['hand_factor_load_y']} at Z {r['hand_factor_load_y_at_z']} | {r['hand_factor_load_x']} | {ok[k]} |")
    else:
        lines.append(f"| {k} | did not build: {r.get('error', '')[:80]} | | | | | | {r['hand_factor_load_y']} | {r['hand_factor_load_x']} | False |")
cp = got('C2', 'checkpoints', [])
report(f"""## C2. Make it more organic

### Stage 1, shape: two ideas, checkpoint 1 (stage ended {t} min after C2 start)

Restatement: `restate.md`, written before any modelling.

| Idea | Loft | Mass g | flat_share | largest_flat | sharp_mm | sharp_per_area | Hand factor, load Y | Hand factor, load X | Eligible |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(lines)}

- A, "bone" (`pictures/idea_a.png`): one stem, wide and thin where it leaves the hub, near round in the middle, wide
  in Y at the fork; hub and wrist knuckle are bodies of revolution about the two joint axes.
- B, "open frame" (`pictures/idea_b.png`): a thin blade with a long window, two slim legs from the sides of the hub;
  the cable would cross the window in the open.
- Rule (written before the run): eligible = built as one body, lighter than the boxy link ({mass_before} g, {before_from}),
  hand beam factor on yield at least 2.5 for a load along Y and along X; then the lower sharp_per_area, A on a tie.
- **Chosen: {chosen}** ({why}).
- Checkpoint 1: {cp[0]['minutes_since_c2_start'] if cp else 'NOT MADE'} min after C2 start, `pictures/checkpoint_01.png`.
  Still missing against the request: {cp[0]['missing'] if cp else 'idea A did not build'}.
- What I see in idea_a.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE
- What I see in idea_b.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE
""")
print('CHOSEN', chosen, table_name, why, flush=True)
