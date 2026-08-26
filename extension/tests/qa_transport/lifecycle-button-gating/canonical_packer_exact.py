#!/usr/bin/env python3
from pathlib import Path
import sys, zipfile, hashlib, stat

ROOT_NAME = "yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate"
FIXED_DT = (2025, 12, 31, 19, 0, 0)
EXPECTED_SHA256 = "0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262"
EXPECTED_BYTES = 179877
EXPECTED_FILES = 69
EXPECTED_ENTRIES = 72

def sha256_bytes(data): return hashlib.sha256(data).hexdigest()
def source_path(repo, rel):
    if rel.startswith("tests/"):
        return repo / "extension" / rel
    return repo / "extension" / "src" / rel

def load_manifest(path):
    rows=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        sha,size,rel=line.split("\t",2)
        rows.append((rel,int(size),sha))
    return rows

def zi(name, is_dir):
    z=zipfile.ZipInfo(name, FIXED_DT)
    z.create_system=3
    z.create_version=20
    z.extract_version=20
    z.flag_bits=0
    z.extra=b""
    z.comment=b""
    if is_dir:
        z.compress_type=zipfile.ZIP_STORED
        z.external_attr=((stat.S_IFDIR | 0o755)<<16) | 0x10
    else:
        z.compress_type=zipfile.ZIP_DEFLATED
        z.external_attr=((stat.S_IFREG | 0o644)<<16)
    return z

def main():
    if len(sys.argv)!=4:
        raise SystemExit("usage: canonical_packer_exact.py <repo-root> <target-tree-sha256.tsv> <output.zip>")
    repo=Path(sys.argv[1]).resolve(); manifest=Path(sys.argv[2]).resolve(); output=Path(sys.argv[3]).resolve()
    rows=load_manifest(manifest)
    if len(rows)!=EXPECTED_FILES: raise SystemExit(f"manifest files {len(rows)} != {EXPECTED_FILES}")
    payload={}
    for rel,size,sha in rows:
        p=source_path(repo,rel)
        data=p.read_bytes()
        if len(data)!=size or sha256_bytes(data)!=sha:
            raise SystemExit(f"tree mismatch: {rel}")
        payload[rel]=data
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output,"w") as z:
        z.writestr(zi(ROOT_NAME+"/",True),b"")
        z.writestr(zi(ROOT_NAME+"/shared/",True),b"")
        z.writestr(zi(ROOT_NAME+"/tests/",True),b"")
        for rel in sorted(payload):
            z.writestr(zi(ROOT_NAME+"/"+rel,False),payload[rel],compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    data=output.read_bytes(); actual=sha256_bytes(data)
    with zipfile.ZipFile(output) as z:
        if z.testzip() is not None: raise SystemExit("ZIP integrity fail")
        entries=len(z.infolist()); files=sum(not i.is_dir() for i in z.infolist())
    if actual!=EXPECTED_SHA256 or len(data)!=EXPECTED_BYTES or files!=EXPECTED_FILES or entries!=EXPECTED_ENTRIES:
        raise SystemExit(f"artifact mismatch sha={actual} bytes={len(data)} files={files} entries={entries}")
    print(f"PASS sha256={actual} bytes={len(data)} files={files} entries={entries}")
if __name__=="__main__": main()
