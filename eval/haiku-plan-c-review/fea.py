import sys, json
sys.path.insert(0,'review_work'); from judge_copy import judge
ALLOW=dict(vm=45.0, layer=22.5, shear=13.0)
def run(path, label):
    rows=json.load(open(path))
    print('=====',label, sorted(rows))
    out={}
    for d in 'XYZ':
        series={}; limits={}; where={}
        for case in ['+X','-X','+Y']:
            for m in ALLOW:
                k=f'{case}, {m}'
                series[k]=[rows[f'{case}@{el}']['by_print_direction'][d][m] for el in ('4.0','3.0','2.3')]
                limits[k]=ALLOW[m]; where[k]=rows[f'{case}@2.3']['by_print_direction'][d][m+'_at']
        j=judge(series,limits)
        print(f'-- layers along {d}: verdict {j["verdict"]}, lowest {j["lowest_factor"]} at {j["lowest_entry"]} at {where[j["lowest_entry"]]}')
        for r in j['rows']:
            print(f'   {r["entry"]:10s} {r["values"]} f={r["factor"]} conv={r["converged"]} step%={r["last_step_pct"]} before%={r["step_before_pct"]} growing={r["step_growing"]} f2more={r["factor_after_two_more_steps"]} {r["state"]}  at {where[r["entry"]]}')
        out[d]=j
    for k in rows:
        if 'rigid' in k or k not in [f'{c}@{e}' for c in ['+X','-X','+Y'] for e in ('4.0','3.0','2.3')]:
            r=rows[k]; print('other row',k,{d:{m:r['by_print_direction'][d][m] for m in ALLOW} for d in 'XYZ'} if 'by_print_direction' in r else list(r))
    r=rows['+Y@2.3']; print({k:v for k,v in r.items() if k not in('by_print_direction','Y')})
    return out
run('eval/haiku-plan-c/fea_rows.json','final (STEM_A2)')
run('eval/haiku-plan-c/backup_STEM_A/fea_rows.json','backup STEM_A')
run('eval/haiku-plan-c/backup_STEM_A2/fea_rows.json','backup_STEM_A2 folder')
