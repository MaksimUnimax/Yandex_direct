from pathlib import Path
p=Path(__file__).resolve().parent/'step12_build_third_audit_v4.py'
s=p.read_text(encoding='utf-8')
old="        if 'PENDING_STEP13' in (r.get('recommendation_maturity') or ''):reasons.add('CONTRIBUTING_UNIT_ALREADY_SEARCH_PROVISIONAL')\n"
assert old in s
s=s.replace(old,"        # Prior recommendation maturity is downstream state, not independent evidence; do not use it to trigger Step-13 search.\n",1)
p.write_text(s,encoding='utf-8')
print('STEP12_V4_PAIR_TRIGGER_CIRCULARITY_FIXED')
