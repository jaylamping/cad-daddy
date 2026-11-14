from pathlib import Path
p=Path('tools/solidworks/playbook/eval/terra-high-b2/REPORT.md'); s=p.read_text(encoding='utf-8').replace('The STA-independent mesh','The exported STL mesh')
s=s.replace('See the individual logs for instance PIDs and times.', 'See the individual logs for instance PIDs and times. Cleanup was checked at 20:43:49: the claim list was empty and `sw_instance.py --status` showed only keeper PID 20496, with no instance from this run.')
p.write_text(s,encoding='utf-8')
