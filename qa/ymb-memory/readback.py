import os,json,hashlib
from pathlib import Path
p=Path(os.environ['YMB_EVIDENCE_ROOT'])/'IDENTITY.json';d=json.loads(p.read_text());root=Path(os.environ['YMB_NEW_ROOT']);actual={str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in root.rglob('*') if f.is_file()};ok=actual==d['source_files'];d['post_test_exact_candidate_readback']=ok;p.write_text(json.dumps(d,indent=2)+'\n');assert ok,'CANDIDATE_BYTES_CHANGED'
