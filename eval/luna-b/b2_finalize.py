"""Join the B2 primary study, alternate-support sensitivity and STL/export checks into the task result."""
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
main = json.loads((RUN / 'results.json').read_text(encoding='utf-8'))
b2 = json.loads((RUN / 'b2_result.json').read_text(encoding='utf-8'))
support = json.loads((RUN / 'b2_support_result.json').read_text(encoding='utf-8'))
stl = json.loads((RUN / 'b2_stl_checks.json').read_text(encoding='utf-8'))
b2['support_sensitivity']['wall_face_refined'] = support
b2['support_sensitivity']['wall_face_converged_any_direction'] = support['best_converged_orientation'] is not None
b2['support_sensitivity']['verdict_effect'] = 'not shown: alternate support series did not converge all three measures in any print direction'
b2['stl_checks'] = stl
b2['model_sha256'] = '4082E480916EC8A04FE1AD52ED88AD94FA0CF0342D4B6CA524DAAEF1BF630F72'
b2['notes'] = ('Primary two-hole support case passes the three numerical thresholds in Z orientation and converges; '
               'overall verdict is not shown because the whole-wall support sensitivity case did not converge and '
               'the upper screw hole meets the arm at X=5.')
b2['verdict'] = 'not shown'
main['B2'] = b2
(RUN / 'b2_result.json').write_text(json.dumps(b2, indent=2), encoding='utf-8')
(RUN / 'results.json').write_text(json.dumps(main, indent=2), encoding='utf-8')
print(json.dumps({'B2': b2}, indent=2), flush=True)
