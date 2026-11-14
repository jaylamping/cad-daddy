import pathlib,re,json
p=pathlib.Path('tools/solidworks/playbook/eval/terra-high-b2'); d=json.loads((p/'results.json').read_text(encoding='utf-8'))
nums=[]
for f in p.glob('*.log'):
 raw=f.read_bytes(); text=raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8',errors='replace')
 nums.extend(int(n) for n in re.findall(r'mesh rc [0-9]+, ([0-9]+) nodes',text))
print('tasks',list(d),'largest logged mesh',max(nums),'number of logged meshes',len(nums))
print('B3',d['B3']['mass_after_g'],d['B3']['saving_pct'],'B4 valid',d['B4']['valid'])
