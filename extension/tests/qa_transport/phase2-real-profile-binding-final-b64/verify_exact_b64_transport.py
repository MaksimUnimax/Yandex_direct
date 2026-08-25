#!/usr/bin/env python3
import base64,hashlib,json,tempfile,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
T=json.loads((BASE/'TRANSPORT_MANIFEST_2026-08-25.json').read_text(encoding='utf-8'))
MB=(BASE/'EXACT_REAL_PROFILE_BINDING_REPAIR_CANDIDATE_MANIFEST_2026-08-25.json').read_bytes()
if len(MB)!=T['payload_manifest_bytes'] or hashlib.sha256(MB).hexdigest()!=T['payload_manifest_sha256']: raise SystemExit('PAYLOAD_MANIFEST_IDENTITY_FAIL')
M=json.loads(MB)
if M['source_commit']!=T['frozen_source_commit'] or M['sha256']!=T['artifact_sha256'] or M['bytes']!=T['artifact_bytes']: raise SystemExit('FROZEN_AUTHORITY_MANIFEST_FAIL')
parts=[]
for row in T['chunks']:
    raw=(BASE/row['path']).read_bytes()
    if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']: raise SystemExit('CHUNK_IDENTITY_FAIL '+row['path'])
    parts.append(raw.decode('ascii'))
text=''.join(parts)
if len(text)!=T['base64_length']: raise SystemExit('B64_LENGTH_FAIL')
data=base64.b64decode(text,validate=True)
if len(data)!=T['artifact_bytes'] or hashlib.sha256(data).hexdigest()!=T['artifact_sha256']: raise SystemExit('EXACT_ZIP_IDENTITY_FAIL')
with tempfile.TemporaryDirectory() as td:
    zp=Path(td)/T['artifact_filename']; zp.write_bytes(data)
    with zipfile.ZipFile(zp) as z:
        if z.testzip() is not None: raise SystemExit('ZIP_INTEGRITY_FAIL')
        infos=z.infolist(); files=[i for i in infos if not i.is_dir()]
        if len(files)!=T['files'] or len(infos)!=T['zip_entries']: raise SystemExit('ZIP_COUNT_FAIL')
        root=M['root_name'].rstrip('/')+'/'
        actual={}
        for info in files:
            if not info.filename.startswith(root): raise SystemExit('ZIP_ROOT_FAIL')
            rel=info.filename[len(root):]; payload=z.read(info)
            actual[rel]={'path':rel,'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest()}
expected={r['path']:r for r in M['payload']}
if actual!=expected: raise SystemExit('ROUNDTRIP_PAYLOAD_MANIFEST_FAIL')
print('B64_REASSEMBLY_PASS')
print('EXACT_ZIP_IDENTITY_PASS')
print('ROUNDTRIP_PAYLOAD_MANIFEST_PASS')
print('ROUNDTRIP_ZIP_INTEGRITY_PASS')
print('FROZEN_AUTHORITY_MATCH_PASS')
print('REAL_YANDEX_REQUESTS=0')
