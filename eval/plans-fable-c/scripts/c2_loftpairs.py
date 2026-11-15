"""Diagnosis only, for the branch "build_form: nothing built the form": loft the stem's sections two at a time in a
scratch part, in each mode, and print which pairs build.   python c2_loftpairs.py [STEM_A]"""
import sys

from common import *

table_name = sys.argv[1] if len(sys.argv) > 1 else got('C2', 'table_name', 'STEM_A')
table = TABLES[table_name]
out = {}
with job(wait_s=1800) as j:
    for mode in ('arcs4', 'closed', 'poly'):
        for k in range(len(table) - 1):
            pair = table[k:k + 2]
            try:
                d = new_part(j.sw, WIP / 'loftpair.SLDPRT')      # closes the pair before
                dv = build_stem(d, pair, mode, name=f'PAIR{k}')
                out[f'{mode} {pair[0][0]} to {pair[1][0]}'] = f'built, {dv:.0f} mm3'
            except Failed as ex:
                out[f'{mode} {pair[0][0]} to {pair[1][0]}'] = f'FAILED: {str(ex)[:100]}'
            print(mode, pair[0][0], pair[1][0], out[f'{mode} {pair[0][0]} to {pair[1][0]}'], flush=True)
put('C2', loft_pairs=out)
