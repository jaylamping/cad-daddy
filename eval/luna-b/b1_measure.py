"""Measure dimensions on the finished B1 solid after reopen."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CAD = ROOT / 'cad' / '_wip' / 'sw-eval' / 'luna-b'
sys.path.insert(0, str(ROOT / 'tools' / 'solidworks'))
from swkit import expect, face_info, job, open_doc, pick, volume, bbox, feature_errors, single_body, bodies, close  # noqa: E402


def main():
    with job(wait_s=1800) as j:
        d = open_doc(j.sw, CAD / 'hub.SLDPRT')
        d.ForceRebuild3(False)
        if feature_errors(d):
            raise RuntimeError(f'feature errors after reopen: {feature_errors(d)}')
        single_body(d)
        flange = pick(d, kind='cyl', r=30.0)
        boss = pick(d, kind='cyl', r=13.0)
        bore = pick(d, kind='cyl', r=5.0)
        screw = pick(d, kind='cyl', r=2.0)
        expect('outer flange cylinder', len(flange), 1, 0)
        expect('boss cylinder', len(boss), 1, 0)
        expect('bore cylinder face(s)', len(bore), 1, 0)
        expect('set-screw cylinder face', len(screw), 1, 0)
        fi, bi, boi, si = [face_info(fs[0]) for fs in (flange, boss, bore, screw)]
        expect('flange thickness from finished cylindrical face', fi['box'][5] - fi['box'][2], 5.0, 0.01)
        expect('boss height from finished cylindrical face', bi['box'][5] - bi['box'][2], 20.0, 0.01)
        expect('boss radius from finished face', bi['r'], 13.0, 0.01)
        expect('bore radius from finished face', boi['r'], 5.0, 0.01)
        flange_top = pick(d, kind='plane', at=(27, 0, 5))
        boss_top = pick(d, kind='plane', at=(10, 0, 25))
        expect('flange top face at Z5', len(flange_top), 1, 0)
        expect('boss top face at Z25', len(boss_top), 1, 0)
        key = pick(d, kind='plane', at=(6.4, 0, 12.5))
        expect('keyway floor face', len(key), 1, 0)
        ki = face_info(key[0])['box']
        expect('keyway length from finished face', ki[5] - ki[2], 25.0, 0.02)
        b = bbox(d)
        result = {
            'flange_outer_face': fi, 'boss_outer_face': bi, 'bore_face': boi,
            'set_screw_face': si, 'keyway_floor_box': ki,
            'flange_top_z_mm': face_info(flange_top[0])['box'][5],
            'boss_top_z_mm': face_info(boss_top[0])['box'][5],
            'bbox_mm': b, 'volume_mm3': volume(d), 'bodies': bodies(d),
        }
        (RUN / 'b1_dimensional_checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(json.dumps(result, indent=2), flush=True)
        close(j.sw, d)


if __name__ == '__main__':
    main()
