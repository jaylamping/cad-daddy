"""C2, stage 3 (study): 60 N at the wrist in +X, -X and +Y with the elbow mounting face held, three mesh sizes,
the three measures for layers stacked along X, the verdict from swfea.judge().

    python c2_fea.py          # runs the sizes not yet in fea_rows.json, then judges
    python c2_fea.py fresh    # forgets earlier rows first (use after the part was rebuilt)

+X and -X are bearing loads on the two pin holes. +Y runs along the pin, which a bearing load cannot carry
(static() refuses it): the part between the cheeks pushes on the inner face of the +Y cheek, so +Y is 60 N as an even
pressure on that face; it is run a second way at the middle size, as a rigid load on both pin holes at the pin axis.
One SolidWorks instance per mesh size and one for the second way (at most four studies in one instance, 05-fea.md)."""
import json
import shutil
import sys

from common import *

SIZES = (4.0, 3.0, 2.3)                         # mm, coarse to fine
NODES = {4.0: 60000, 3.0: 80000, 2.3: 125000}   # predicted, with the 1.2 mm control on the tunnel and 1.0 on the pin holes
TUNNEL_EL = 1.2                                 # mm, mesh control on the cable tunnel (0.8 mm skins under the hub faces)
DIST = 3.0                                      # mm: nodes nearer than this to the held face or a loaded face are left out
F = 60.0
CASES = ('+X', '-X', '+Y')
DISP = {'+X': 2.5, '-X': 2.5, '+Y': 4.5, '+Y rigid': 4.0}     # mm, hand: F L^3 / 3 E I with L 165 and the waist section
SRC, MODEL = WIP / 'link_organic.SLDPRT', WIP / 'link_organic_fea.SLDPRT'
ROWS = HERE / 'fea_rows.json'
if 'fresh' in sys.argv and ROWS.exists():
    ROWS.unlink()
rows = json.loads(ROWS.read_text(encoding='utf-8')) if ROWS.exists() else {}
stamp(HERE, 'C2 study start')
if not got('C2', 'fixed_items_ok', False):
    log('NOTE: fixed_items_ok is not true in results.json: the study runs, but the part does not pass the gate yet')
shutil.copyfile(SRC, MODEL)                     # the study works on a copy: link_organic.SLDPRT stays as exported
table = TABLES[got('C2', 'table_name', 'STEM_A')]
waist = [r for r in table if r[0] == -115.0][0]
_, zx, zy = section_props(waist)
HAND = {'+X': (F * 85.0 / zy, (waist[1], 0.0, -115.0)), '-X': (F * 85.0 / zy, (-waist[1], 0.0, -115.0)),
        '+Y': (F * 85.0 / zx, (0.0, waist[2], -115.0))}       # plain bending stress at the waist surface, and where


def faces_of(d):
    mount = pick(d, kind='plane', normal=(0, -1, 0), at=(0.0, -4.0, 20.0))
    bores = pick(d, kind='cyl', r=PIN_R, inside=[-5, -23, PIN_Z - 5, 5, 23, PIN_Z + 5])
    thrust = pick(d, kind='plane', normal=(0, -1, 0), at=(9.0, SLOT_HALF, -196.0))
    tunnel = pick(d, kind='cyl', r=CABLE_R, inside=[-4, -4, CABLE_Z1 - 5, 4, 4, CABLE_Z0 + 5])
    must('mounting face', len(mount), 1)
    must('pin hole faces', len(bores), 2)
    must('inner face of the +Y cheek', len(thrust), 1)
    must('cable tunnel face', len(tunnel), 1)
    return mount, bores, thrust, tunnel


def solve(j, d, case, el):
    """One study. Picks its faces afresh. Returns the Result; raises Failed if a check of the solve itself fails."""
    d.ForceRebuild3(False)
    mount, bores, thrust, tunnel = faces_of(d)
    if case == '+X':
        loads, want = [('bearing', bores, (F, 0.0, 0.0))], (-F, 0.0, 0.0)
    elif case == '-X':
        loads, want = [('bearing', bores, (-F, 0.0, 0.0))], (F, 0.0, 0.0)
    elif case == '+Y':
        loads, want = [('normal', thrust, F)], (0.0, -F, 0.0)
    else:                                          # '+Y rigid'
        loads, want = [('remote', bores, (0.0, 0.0, PIN_Z), (0.0, F, 0.0), (0.0, 0.0, 0.0))], (0.0, -F, 0.0)
    name = f"{case.replace('+', 'P').replace('-', 'M').replace(' ', '_')}_{int(el * 10)}"
    predict(name, NODES[el], DISP[case], 'the neck, Z -25 to -45, where the stem leaves the hub')
    # loose_ok=True: this is one body held on a whole face, and it bends by millimetres over 250 mm; on such a part
    # the solver's "excessive displacements" prompt is harmless (05-fea.md, contact item 8) and static() would
    # otherwise raise on it. Nothing is loose if the reaction equals the load and the displacement is near the hand
    # value: both are checked below, and r.excessive is recorded.
    r = static(j, d, name, PETG, fixtures=[('fixed', mount)], loads=loads, el=el, ctrl=[(tunnel, TUNNEL_EL), (bores, 1.0)],
               max_nodes=195000, loose_ok=True)
    if r.excessive:
        log(f'{name}: the solver asked about excessive displacements; answered No, linear result kept')
    log(r.summary())
    for k in range(3):                             # check 1: reaction equals load, component by component
        expect(f'{name}: reaction {"XYZ"[k]} N', r.reaction[k], want[k], 0.01 if want[k] else 0, abs_tol=0.6)
    if not compare(name, r, NODES[el], DISP[case]):
        raise Failed(f'{name}: nodes or displacement far from the prediction: C_C2.md, Branches, "prediction missed"')
    return r


def read(r, case):
    """Everything kept from one result (plain numbers, so it can go to fea_rows.json)."""
    keep = r.away(dist=DIST)
    out = dict(el=r.el, excessive_prompt=bool(r.excessive), nodes=r.nodes, elements=r.elements, solve_s=round(r.seconds), reaction_N=r.reaction,
               max_disp_mm=round(r.max_disp(), 3), peak_vm_everywhere=round(float(r.vm.max()), 3),
               chosen=measures(r, keep), by_print_direction=direction_table(r, keep),
               peak_vm_outside_mm={str(dd): round(r.peak(r.away(dist=dd))[0], 3) for dd in (2.0, 3.0, 5.0)})
    out['chosen_outside_mm'] = {str(dd): measures(r, r.away(dist=dd)) for dd in (2.0, 3.0, 5.0)}
    if r.loaded_pts is not None and len(r.loaded_pts):
        on = r.near(r.loaded_pts, 0.1)
        out['peak_vm_on_loaded_faces'] = round(r.peak(on)[0], 3)
    if case in HAND:
        hand, at = HAND[case]
        got_, n = r.average(at, 2.0)
        out['waist'] = dict(hand_mpa=round(hand, 2), mean_vm_2mm=round(got_, 2), nodes=n, at=at)
        expect(f'{r.name}: plain bending stress at the waist against the hand value', got_, hand, 0.25)
    at = out['chosen']['vm_at']
    out['peak_averages'] = {str(rad): [round(v, 2) for v in r.average(at, rad)] for rad in (0.5, 1.0, 2.0)}
    return out


JOBS = [(el, CASES) for el in SIZES] + [(SIZES[1], ('+Y rigid',))]      # the second way to load +Y has its own instance
for el, cases in JOBS:
    todo = [c for c in cases if f'{c}@{el}' not in rows]
    if not todo:
        continue
    try:
        with job(wait_s=1800) as j:
            j.simulation()                         # Simulation first, then open, rebuild, pick, solve (05-fea.md)
            d = open_doc(j.sw, MODEL)
            d.ForceRebuild3(False)
            expect('the study copy is the exported part', volume(d), got('C2', 'volume_after_mm3'), 0.001)
            for case in todo:
                r = solve(j, d, case, el)
                rows[f'{case}@{el}'] = read(r, case)
                ROWS.write_text(json.dumps(rows, indent=1, default=float), encoding='utf-8')
                stamp(HERE, f'C2 study {case} at {el} mm solved')
            close(j.sw, d)
    except Failed as ex:
        if cases != ('+Y rigid',):
            raise                                  # a required case: stop here, read C_C2.md Branches, run again
        log(f'the second way to load +Y did not solve ({ex}): the verdict stands on the pressure load alone, and the report says so')

# ---- the verdict: judge() only -----------------------------------------------------------------------------------------
series = {f'{case}, {m}': [rows[f'{case}@{el}']['chosen'][m] for el in SIZES] for case in CASES for m in ALLOW}
limits = {k: ALLOW[k.split(', ')[1]] for k in series}
v = judge(series, limits, need=2.0)
fine = {case: rows[f'{case}@{SIZES[-1]}'] for case in CASES}
sf = {m: min(ALLOW[m] / fine[c]['chosen'][m] if fine[c]['chosen'][m] > 0 else 999.0 for c in CASES) for m in ALLOW}
mid, rigid = rows[f'+Y@{SIZES[1]}'], rows.get(f'+Y rigid@{SIZES[1]}')
second = {m: round(rigid['chosen'][m] / mid['chosen'][m], 3) if rigid and mid['chosen'][m] > 0 else None for m in ALLOW}   # rigid over pressure, same mesh
for m in ALLOW:                                    # report the higher of the two ways to load +Y (07-done.md, study item 3)
    if second[m] and second[m] > 1.0 and fine['+Y']['chosen'][m] > 0:
        sf[m] = min(sf[m], ALLOW[m] / (fine['+Y']['chosen'][m] * second[m]))
low_case, low_m = v['lowest_entry'].split(', ')
where = fine[low_case]['chosen'][low_m + '_at']
best = {}
for c in CASES:                                    # the same results read for the other print directions
    for dname, mm in fine[c]['by_print_direction'].items():
        f_ = min(ALLOW[m] / mm[m] if mm[m] > 0 else 999.0 for m in ALLOW)
        best[dname] = min(best.get(dname, 999.0), f_)
mirror = abs(fine['+X']['chosen']['vm'] - fine['-X']['chosen']['vm']) / fine['+X']['chosen']['vm']
not_conv = [dict(entry=r['entry'], values=r['values'], last_step_pct=r['last_step_pct'], state=r['state'])
            for r in v['rows'] if not r['converged']]
t3 = since_c2('C2 study end')
put('C2', verdict=v['verdict'], sf_lowest=v['lowest_factor'], judge=v, sf_yield=round(sf['vm'], 2), sf_layer=round(sf['layer'], 2),
    sf_shear=round(sf['shear'], 2), governing=f"{v['lowest_entry']} at {where} (factor {v['lowest_factor']})",
    requirement_met=bool(min(sf.values()) >= 2.0), not_converged=not_conv, fea_rows=rows, mesh_sizes_mm=list(SIZES),
    exclusion_mm=DIST, lowest_factor_by_print_direction={k: round(x, 2) for k, x in best.items()},
    load_y_second_way_ratio=second, mirror_check_vm_diff=round(mirror, 4), study_minutes_since_c2_start=t3)
tab = '\n'.join(
    f"| {c} | {el} | {rows[f'{c}@{el}']['nodes']} | {rows[f'{c}@{el}']['chosen']['vm']} | {rows[f'{c}@{el}']['chosen']['layer']} | "
    f"{rows[f'{c}@{el}']['chosen']['shear']} | {rows[f'{c}@{el}']['max_disp_mm']} | {rows[f'{c}@{el}']['reaction_N'][:3]} | "
    f"{rows[f'{c}@{el}']['chosen']['vm_at']} |" for c in CASES for el in SIZES)
jt = '\n'.join(f"| {r['entry']} | {r['values']} | {r['factor']} | {r['last_step_pct']} | {r['state']} |" for r in v['rows'])
dt = '\n'.join(f"| {c} | {dn} | {mm['vm']} | {mm['layer']} | {mm['shear']} |" for c in CASES
               for dn, mm in fine[c]['by_print_direction'].items())
report(f"""### Stage 3, study (stage ended {t3} min after C2 start)

Model `_wip/sw-eval/{RUN}/link_organic_fea.SLDPRT`, a copy of the exported part (volume checked). Printed PETG. Held:
the mounting face (the flat ring at Y -4, Ø30 to Ø63). Loads: 60 N; +X and -X as bearing loads on the two pin holes;
+Y as an even pressure on the inner face of the +Y cheek, because a force along the pin is not a bearing load on its
holes (`static()` refuses it): the part between the cheeks pushes on that face. Layers stacked along X. Peaks are read
at least {DIST} mm from the held face and from the loaded faces. Global element sizes {list(SIZES)} mm, {TUNNEL_EL} mm on the
cable tunnel and 1.0 mm on the pin holes at every size.

| Case | el mm | Nodes | von Mises MPa | Across layers MPa | Between layers MPa | Max disp mm | Reaction N | von Mises peak at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
{tab}

Verdict from `swfea.judge()`, need 2.0: **{v['verdict']}**, lowest factor **{v['lowest_factor']}** at "{v['lowest_entry']}", place {where}.

| Entry | Values coarse to fine MPa | Factor | Last step % | State |
| --- | --- | --- | --- | --- |
{jt}

- Keys: sf_yield {sf['vm']:.2f}, sf_layer {sf['layer']:.2f}, sf_shear {sf['shear']:.2f} (lowest of the three cases at
  {SIZES[-1]} mm, and for +Y the higher of the two ways to load it).
- Not converged: {not_conv if not_conv else 'nothing: every entry settled'}.
- +Y loaded a second way at {SIZES[1]} mm (rigid, on both pin holes at the pin axis): rigid over pressure
  {second} (von Mises, across layers, between layers).
- Hand check at the waist (Z -115), mean over 2 mm against M / Z: {[(c, fine[c].get('waist')) for c in CASES]}.
- Reaction equals load in every study (table). -X against +X, von Mises: {mirror * 100:.2f} % apart (the part is
  symmetric about X = 0, so they must agree).
- Excluded: the peak anywhere, including the held edge and the loaded faces, at {SIZES[-1]} mm:
  {[(c, fine[c]['peak_vm_everywhere']) for c in CASES]} MPa; on the loaded faces themselves
  {[(c, fine[c].get('peak_vm_on_loaded_faces')) for c in CASES]} MPa. Peak outside 2, 3 and 5 mm:
  {[(c, fine[c]['peak_vm_outside_mm']) for c in CASES]}.
- At the governing peak, mean von Mises over 0.5, 1 and 2 mm (value, nodes): {fine[low_case]['peak_averages']}.
- The same results read for the other print directions ({SIZES[-1]} mm), lowest factor of the three measures and three
  cases: {dict((k, round(x, 2)) for k, x in best.items())}.

| Case | Layers along | von Mises | Across layers | Between layers |
| --- | --- | --- | --- | --- |
{dt}

- Load path: the pin presses on the two pin holes (or, for +Y, the swinging part on the +Y cheek), the cheeks carry
  it up either side of the arch into the stem, the stem bends, and the neck hands it to the hub over the held ring.
""")
report('- The three measures for layers along X at the finest mesh, read outside 2, 3 and 5 mm from the held and '
       f'loaded faces (the verdict uses {DIST} mm): '
       + str([(c, {dd: {m: mm[m] for m in ALLOW} for dd, mm in fine[c]['chosen_outside_mm'].items()}) for c in CASES]))
print('VERDICT', v['verdict'], 'lowest', v['lowest_factor'], v['lowest_entry'], 'sf', sf, flush=True)
