"""Last SolidWorks job: confirm the deliverable bracket_c.SLDPRT opens clean with the recorded volume, and export the T6 model for a picture."""
import math
from lib3 import *

with job(wait_s=1800) as j:
    stamp(RUN, 'final checks start')
    sw = j.sw
    d = open_doc(sw, WIP / 'bracket_c.SLDPRT')
    d.ForceRebuild3(False)
    v = volume(d)
    bb = bbox(d)
    log('bracket_c volume', v, 'box', bb, 'bodies', len(bodies(d)), 'errors', feature_errors(d))
    expect('bracket_c volume', v, 35331.71 + 0.0, 0.001)
    expect('bracket_c bodies', len(bodies(d)), 1, 0)
    expect('bracket_c errors', len(feature_errors(d)), 0, 0)
    expect('mass cap 43.16 g', float(v * 1.19e-3 <= 1.1 * 32974.02 * 1.19e-3), 1.0, 0)
    close(sw, d)
    d = open_doc(sw, WIP / 'bracket_sharp.SLDPRT')
    log('bracket_sharp volume', volume(d))
    close(sw, d)
    d = open_doc(sw, WIP / 'bracket_b.SLDPRT')
    log('bracket_b volume', volume(d))
    close(sw, d)
    d = open_doc(sw, WIP / 't6b' / 'tp_all.SLDPRT')
    log('tp_all bodies', bodies(d))
    export(sw, d, WIP / 't6b' / 'tp_all.stl')
    close(sw, d)
    put('T5', final_check_volume_mm3=round(v, 2))
    stamp(RUN, 'final checks end')
