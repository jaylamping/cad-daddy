# DESIGN: link_organic
**The idea in one sentence.** A bone: the two joints are bodies of revolution about their own axes (a round-rimmed
hub at the elbow, a barrel at the wrist), and one stem grows between them, changing section the way the load does:
wide in X and thin in Y where it leaves the hub's plane, near round at the waist, wide in Y where it becomes the fork.

**Tried and dropped.**
- Idea B, an open frame (a thin blade with a long window, two slim legs): None g, hand beam factor
  0.89 for the load along Y against 3.61 for the bone. The legs are thin exactly where a
  sideways load bends them, and the cable would cross the window in the open.
- A raised rim round the hub to thicken the neck (on paper only): it reads as a turned socket, a second part. The
  thickness went into the stem instead.
- A fork block with a square slot: replaced by a full arch, R 16, so the cheeks grow out of the stem.
- A fillet where the stem climbs out of the hub's screw-side face: tried at R3 in the first round and from R2 down in this one, no sound blend: a crease of about 30 degrees is left.

**With another hour.** Make hub and stem one surface (the hub's rim as the stem's first sections) so no seam is left
at the elbow; round the slot's outer edges; take 15 to 20 g out of the fork end, which is solid above the arch and
carries almost nothing (lowest factor 1.57: +Y, layer at [0.28, -3.19, -34.48] (factor 1.57)).

**Least happy with.** The elbow junction. The stem leaves a turned hub: on the screw side it climbs out of the flat
face at about 30 degrees past two scallops cut for the screw heads (19.49 mm3), on the motor side it
leaves through the rim round. Both are intersections, not blends. Then: the cable tunnel leaves 0.8 mm skins under
both hub faces for 8 mm, and the wrist knuckle stands 0.4 mm proud of the stem round each cheek, a visible ring.
Numbers: 124.53 g against 261.13 g; factors 2.98 / 1.54 / 1.78 (yield / across / between layers),
verdict "fail" for the print tilted 30 degrees; sharp_per_area 5.1 against 12.3. Earlier rounds: the loft was twisted a quarter turn above Z -85 and pinched the stem to 8.6 mm; fixed by picking every section at the same corner (now 12.2 mm).
