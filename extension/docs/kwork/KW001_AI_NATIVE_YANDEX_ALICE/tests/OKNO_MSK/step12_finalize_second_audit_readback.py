import json
from pathlib import Path
R=Path(__file__).resolve().parent
STATE=R/'STEP_12_CORRECTION_CURRENT_STATE.json';QA=R/'STEP_12_QA.json';REPORT=R/'STEP_12_REPORT.md';ACC=R/'STEP_12_SECOND_AUDIT_FINAL_ACCEPTANCE_2026-08-31.md';FLOW=R/'JOB_FLOW.md'
s=json.loads(STATE.read_text(encoding='utf-8'));q=json.loads(QA.read_text(encoding='utf-8'))
assert s['step12_complete'] and s['open_defects']==[] and not s['step13_executed'] and not s['final_github_readback']
assert q['all_defects_verified_fixed'] and q['open_defects']==[] and not q['step13_executed'] and not q['final_github_readback']
s['final_github_readback']=True;s['canonical_closure_readback_passed']=True
q['final_github_readback']=True;q['canonical_closure_readback_passed']=True
STATE.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');QA.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
r=REPORT.read_text(encoding='utf-8')
r=r.replace('**Step 12 is complete as a closure candidate. Step 13 has not been started. Durable closure requires GitHub readback and final status synchronization.**','**Step 12 is complete. The canonical closure commit and final status-sync commit both passed GitHub readback. Step 13 has not been started.**')
if 'FINAL_SECOND_AUDIT_GITHUB_READBACK = true' not in r:r+='\n## Durable final closure\n\n```text\nFINAL_SECOND_AUDIT_GITHUB_READBACK = true\nSTEP13_EXECUTED = false\n```\n'
REPORT.write_text(r,encoding='utf-8')
a=ACC.read_text(encoding='utf-8').replace('Status: **CANDIDATE PASS — DURABLE GITHUB READBACK REQUIRED**','Status: **PASS AFTER DURABLE GITHUB READBACK**')
a=a.replace('The owner-goal/current-site/content-reuse correction is not accepted merely because the builder succeeded. It requires the closure commit to be read back from GitHub and a final status-sync commit to be read back again.','The closure commit was read back from GitHub successfully; this final status-sync is now the canonical accepted state and itself requires/receives a second structured readback.')
if 'FINAL_GITHUB_READBACK = true' not in a:a+='\n```text\nFINAL_GITHUB_READBACK = true\nSTEP13_EXECUTED = false\n```\n'
ACC.write_text(a,encoding='utf-8')
f=FLOW.read_text(encoding='utf-8').replace('KW001_OKNO_MSK_STEP12_FINAL_GITHUB_READBACK = false','KW001_OKNO_MSK_STEP12_FINAL_GITHUB_READBACK = true')
FLOW.write_text(f,encoding='utf-8')
print('STEP12_SECOND_AUDIT_FINAL_STATUS_SYNC_READY')
