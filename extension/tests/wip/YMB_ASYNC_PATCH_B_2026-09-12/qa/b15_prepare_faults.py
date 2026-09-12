"""QA-only supplemental cases; reuse exact proven single-install B15 venue.
Keeps original failing script and original primary successful cases immutable.
No extension source, assertion relaxation or package rebuild.
"""
from pathlib import Path
import hashlib
q=Path(__file__).parent
b=(q/'b15_browser_qualification.mjs').read_bytes()
assert hashlib.sha256(b).hexdigest()=='b464224139ac2fe0ff7e194f76d4e38e1c5ec9ef144f075df3aafb9d3ec9423d'
s=b.decode().replace('enableExtensions:[root],protocolTimeout:120000','enableExtensions:true,protocolTimeout:120000',1)
start=s.index(' const domReady=await runCase(')
end=s.index(' assert.equal(tree(),target);emit({case:',start)
s=s[:start]+(q/'b15_fault_cases.inc.mjs').read_text()+s[end:]
out=q/'b15_browser_faults.mjs'
with out.open('x') as f:f.write(s)
print('B15_SUPPLEMENT_QA_SHA256='+hashlib.sha256(out.read_bytes()).hexdigest())
