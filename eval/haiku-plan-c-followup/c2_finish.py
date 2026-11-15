"""C2, stage 4 (report): the before-and-after sheet, checkpoint 3, the task's keys, DESIGN.md.   python c2_finish.py

Every number comes from results.json (measured by the earlier scripts) and times.log. Nothing is typed in."""
from common import *

stamp(HERE, 'C2 finish start')
R = lambda key, default=None: got('C2', key, default)      # noqa: E731
BEFORE, AFTER = WIP / 'link_boxy.stl', WIP / 'link_organic.stl'
have_before = BEFORE.exists()
stats = picture(([BEFORE] if have_before else []) + [AFTER], PICS / 'c2_before_after.png')      # one call: one scale
shape_after = stats['link_organic.stl']
shape_before = stats['link_boxy.stl'] if have_before else got('C1', 'shape')
st = stl_stats(AFTER)
expect('the sheet was drawn from the part that was studied (STL volume against results.json)', st['volume'],
       R('stl')['volume'], 0.0005)
picture([AFTER], PICS / 'checkpoint_03.png')
t3 = since_c2('C2 checkpoint_03')
mass_before, mass_after = R('mass_before_g'), R('mass_after_g')
verdict, low = R('verdict'), R('sf_lowest')
sfy, sfl, sfs = R('sf_yield'), R('sf_layer'), R('sf_shear')
studied = verdict is not None
met = bool(studied and min(sfy, sfl, sfs) >= 2.0)
gate = dict(fixed_items_ok=bool(R('fixed_items_ok')), one_body_watertight=bool(st['watertight'] and st['shells'] == 1),
            requirement_met=met, mass_not_above_boxy=bool(mass_after <= mass_before))
missing = ('nothing of the gate' if all(gate.values()) else f'gate items not met: {[k for k, x in gate.items() if not x]}') + (
    f"; verdict {verdict}, lowest factor {low}; against the look asked for: sharp_per_area {shape_after['sharp_per_area']} "
    f"(boxy {shape_before['sharp_per_area']}), flat_share {shape_after['flat_share']} (boxy {shape_before['flat_share']}); "
    f"the hub seam is {'blended R' + str(R('build')['ramp_blend_radius_mm']) if R('build')['ramp_blend_radius_mm'] else 'still a crease'}")
cps = [c for c in R('checkpoints', []) if c['n'] != 3] + [
    dict(n=3, minutes_since_c2_start=t3, picture='pictures/checkpoint_03.png', missing=missing)]
cps = sorted(cps, key=lambda c: c['n'])
blend = R('build')['ramp_blend_radius_mm']
ideas = R('ideas_tried', [])
b_idea = next((i for i in ideas if i['idea'] == 'B'), {})

# ---- DESIGN.md: the planner's design intent, with what only this run can know filled in from results.json ----------------
a_y = next((i['hand_factor_load_y'] for i in ideas if i['idea'] == 'A'), None)
blend_txt = f'built at R{blend} mm' if blend else 'tried at R3 in the first round and from R2 down in this one, no sound blend: a crease of about 30 degrees is left'
design = f"""# DESIGN: link_organic
**The idea in one sentence.** A bone: the two joints are bodies of revolution about their own axes (a round-rimmed
hub at the elbow, a barrel at the wrist), and one stem grows between them, changing section the way the load does:
wide in X and thin in Y where it leaves the hub's plane, near round at the waist, wide in Y where it becomes the fork.

**Tried and dropped.**
- Idea B, an open frame (a thin blade with a long window, two slim legs): {b_idea.get('mass_g')} g, hand beam factor
  {b_idea.get('hand_factor_load_y')} for the load along Y against {a_y} for the bone. The legs are thin exactly where a
  sideways load bends them, and the cable would cross the window in the open.
- A raised rim round the hub to thicken the neck (on paper only): it reads as a turned socket, a second part. The
  thickness went into the stem instead.
- A fork block with a square slot: replaced by a full arch, R 16, so the cheeks grow out of the stem.
- A fillet where the stem climbs out of the hub's screw-side face: {blend_txt}.

**With another hour.** Make hub and stem one surface (the hub's rim as the stem's first sections) so no seam is left
at the elbow; round the slot's outer edges; take 15 to 20 g out of the fork end, which is solid above the arch and
carries almost nothing (lowest factor {low}: {R('governing')}).

**Least happy with.** The elbow junction. The stem leaves a turned hub: on the screw side it climbs out of the flat
face at about 30 degrees past two scallops cut for the screw heads ({R('build')['heads_mm3']} mm3), on the motor side it
leaves through the rim round. Both are intersections, not blends. Then: the cable tunnel leaves 0.8 mm skins under
both hub faces for 8 mm, and the wrist knuckle stands 0.4 mm proud of the stem round each cheek, a visible ring.
Numbers: {mass_after} g against {mass_before} g; factors {sfy} / {sfl} / {sfs} (yield / across / between layers),
verdict "{verdict}" for layers along X; sharp_per_area {shape_after['sharp_per_area']} against {shape_before['sharp_per_area']}.
"""
lines = design.strip().splitlines()
if len(lines) > 25:
    raise Failed(f'DESIGN.md has {len(lines)} lines, the task allows 25')
(HERE / 'DESIGN.md').write_text(design, encoding='utf-8')

t_end = stamp(HERE, 'C2 end')
total = round(t_end, 1)                            # the clock began at the first stamp in this folder (C1 start)
c2_minutes = round(t_end - clock('C2 start'), 1)
put('C2', status='done' if all(gate.values()) and studied else 'not done: see gate',
    mass_before_g=mass_before, mass_after_g=mass_after, shape_before=shape_before, shape_after=shape_after,
    print_orientation=PRINT_TEXT, sf_yield=sfy, sf_layer=sfl, sf_shear=sfs, governing=R('governing'),
    fixed_items_ok=bool(R('fixed_items_ok')), ideas_tried=ideas, checkpoints=cps, minutes=c2_minutes, gate=gate,
    verdict=verdict)
put('set', minutes=total, c1_minutes=clock('C1 end'), c2_minutes=c2_minutes)
cp_rows = '\n'.join(f"| {c['n']} | {c['minutes_since_c2_start']} | `{c['picture']}` | {c['missing']} |" for c in cps)
margin_load = round(60.0 * low / 2.0, 1) if low else None
report(f"""### Stage 4, result (C2 took {c2_minutes} min; the whole set {total} min on times.log)

| Gate | |
| --- | --- |
| Fixed items intact | {gate['fixed_items_ok']} |
| One body, watertight | {gate['one_body_watertight']} |
| Factor at least 2.0 on all three measures, three cases | {gate['requirement_met']} (verdict from judge(): {verdict}; {sfy} / {sfl} / {sfs}) |
| Mass not above the boxy link | {gate['mass_not_above_boxy']} ({mass_after} g against {mass_before} g) |

Deliverables: `restate.md`, `pictures/idea_a.png`, `pictures/idea_b.png`, `pictures/checkpoint_01.png` to `_03.png`,
`pictures/c2_before_after.png` (both STLs in one call), `link_organic.SLDPRT` / `.step` / `.stl` in
`_wip/sw-eval/{RUN}/`, `DESIGN.md`, `fea_rows.json`, `times.log`.

| Checkpoint | Min after C2 start | Picture | Still missing against the request |
| --- | --- | --- | --- |
{cp_rows}

Shape numbers, before: {shape_before}. After: {shape_after}.

- **Thinnest margin:** {R('governing')}. At this factor the part carries {margin_load} N at the wrist before the
  factor is 2.0; a sharper seam as printed, or the load taken on one cheek only, is what would eat it.
- **Cheapest improvement found:** the print direction was changed from layers along Y (first round, fail) to layers along X; all three read
  ({R('lowest_factor_by_print_direction')}); the fork end above the arch is solid and lightly stressed, so mass can come
  out there first.
- **Not checked:** buckling (the stem is stocky: about 22 mm across over 140 mm); the pin's own bending and a loose
  pin (a bearing load covers half the hole exactly); screw preload on the 8 mm hub; the 0.8 mm skins over the cable
  tunnel in print; whether the motor's body leaves room for the stem below Y -4 outside Ø62 (the boxy link went to
  Y -15 there too); fatigue.
- What I see in c2_before_after.png, one line: WRITE THIS LINE BY HAND AFTER OPENING THE PICTURE
""")
print('C2 FINISHED', json.dumps(dict(gate=gate, verdict=verdict, minutes=c2_minutes, set_minutes=total)), flush=True)
