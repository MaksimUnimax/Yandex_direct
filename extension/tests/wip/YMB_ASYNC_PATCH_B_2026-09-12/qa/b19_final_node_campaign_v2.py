"""Execute canonical B19 Node campaign with exact production file_delivery_content.js bound for content regressions.
No production edits. Usage is identical to b19_final_node_campaign.py.
"""
from pathlib import Path
import sys
p=Path(__file__).with_name('b19_final_node_campaign.py')
s=p.read_text()
old="'YMB_IDB_FIXTURE':str(qa/'idb_artifact_fixture.mjs')}"
new="'YMB_IDB_FIXTURE':str(qa/'idb_artifact_fixture.mjs'),'YMB_FILE_CONTENT':str(product/'file_delivery_content.js')}"
if s.count(old)!=1:raise ValueError('Canonical runner env block changed')
s=s.replace(old,new)
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p),'sys':sys})
