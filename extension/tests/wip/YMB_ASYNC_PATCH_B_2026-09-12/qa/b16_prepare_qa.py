"""Reuse B15's exact working browser prelude, fixture and single-install launcher.
QA only. Usage: b16_prepare_qa.py EXTRACTED_B15_ARTIFACT EMPTY_TEST_DIR
No production files are changed. Missing or different inputs fail before writing.
"""
from pathlib import Path
import hashlib,sys,json
H=lambda b:hashlib.sha256(b).hexdigest()
src,out=map(Path,sys.argv[1:])
if out.exists() and any(out.iterdir()): raise ValueError('nonempty QA output')
p=src/'b15_browser_qualification.mjs'; b=p.read_bytes()
assert H(b)=='0d085b321ef89ce671a28967c7d037d5d21844b6d485e8da9b4fa5c0cc5ebe94'
f=(src/'b15_fixture.html').read_bytes(); assert H(f)=='a2fd792336603d09c27fcd2a520a385ec85273f88741adc5cc0fd78047abbe72'
s=b.decode(); pre=s.split('try{\n browser=await puppeteer.launch',1)[0]
assert 'async function resetDelivery' in pre and pre.endswith('\n')
body=Path(__file__).with_name('b16_browser_cases.mjs').read_bytes()
script=pre.encode()+body
out.mkdir(parents=True,exist_ok=True)
(out/'b16.generated.mjs').write_bytes(script)
(out/'b15_fixture.html').write_bytes(f)
(out/'QA_IDENTITY.json').write_text(json.dumps({'prelude_source_sha256':H(b),'body_sha256':H(body),'generated_sha256':H(script),'fixture_sha256':H(f),'production_modified':False},indent=2)+'\n')
print('B16 exact prelude/fixture reused; generated='+H(script))
