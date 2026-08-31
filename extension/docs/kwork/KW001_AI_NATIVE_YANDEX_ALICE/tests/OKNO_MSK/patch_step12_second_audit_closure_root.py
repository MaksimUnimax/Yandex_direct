from pathlib import Path
p=Path(__file__).resolve().parent/'step12_close_second_audit.py'
s=p.read_text(encoding='utf-8')
assert 'ROOT=R.parents[2]' in s
s=s.replace('ROOT=R.parents[2]','ROOT=R.parents[1]',1)
p.write_text(s,encoding='utf-8')
print('STEP12_SECOND_AUDIT_CLOSURE_ROOT_FIXED')
