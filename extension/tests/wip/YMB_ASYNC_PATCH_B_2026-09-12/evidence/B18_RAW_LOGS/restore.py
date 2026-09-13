#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,sys,lzma,tarfile,io
root=Path(__file__).resolve().parent;m=json.loads((root/"MANIFEST.json").read_text());out=Path(sys.argv[1]);
if out.exists(): raise SystemExit("output exists")
b=bytearray()
for p in m["parts"]:
 d=(root/p["name"]).read_bytes();assert len(d)==p["bytes"] and hashlib.sha256(d).hexdigest()==p["sha256"];b.extend(d)
assert len(b)==m["archive_bytes"] and hashlib.sha256(b).hexdigest()==m["archive_sha256"]
with tarfile.open(fileobj=io.BytesIO(bytes(b)),mode="r:xz") as tf:
 for x in tf.getmembers():
  if not x.isfile() or x.name.startswith("/") or ".." in Path(x.name).parts: raise SystemExit("unsafe archive")
out.write_bytes(b);print("PASS",m["archive_sha256"],len(b),m["archive_members"])
