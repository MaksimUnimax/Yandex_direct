from pathlib import Path
p=Path(__file__).resolve().parent/'step12_apply_third_audit_method_patch.py'
s=p.read_text(encoding='utf-8')
old='ROOT=R.parents[2]'
new='ROOT=R.parents[1]'
assert old in s and new not in s
p.write_text(s.replace(old,new,1),encoding='utf-8')
print('STEP12_THIRD_AUDIT_METHOD_ROOT_FIXED')
