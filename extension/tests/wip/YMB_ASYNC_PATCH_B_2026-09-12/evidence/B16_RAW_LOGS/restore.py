"""Reassemble the exact B16 raw log archive. Never overwrite output; no extraction.
Usage: python restore.py NEW_OUTPUT.tar.xz
"""
from pathlib import Path,PurePosixPath
import hashlib,io,json,sys,tarfile
root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text())
h=lambda b:hashlib.sha256(b).hexdigest()
parts=[]
for r in m['parts']:
 assert len(PurePosixPath(r['name']).parts)==1
 b=(root/r['name']).read_bytes();assert len(b)==r['bytes'] and h(b)==r['sha256']
 parts.append(b)
b=b''.join(parts);assert len(b)==m['bytes'] and h(b)==m['sha256']
with tarfile.open(fileobj=io.BytesIO(b),mode='r:xz') as t:
 rows=t.getmembers();assert len(rows)==m['members'] and len({x.name for x in rows})==len(rows)
 for x in rows:assert x.isfile() and not PurePosixPath(x.name).is_absolute() and '..' not in PurePosixPath(x.name).parts
 files={x.name:t.extractfile(x).read() for x in rows}
checks=files['SHA256SUMS'].decode().splitlines();assert len(checks)==m['member_checksums']
for line in checks:
 digest,name=line.split('  ',1);assert h(files[name])==digest
out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
with out.open('xb') as f:f.write(b)
print('PASS',h(b),len(b),'bytes;',len(checks),'member hashes; no installable code')
