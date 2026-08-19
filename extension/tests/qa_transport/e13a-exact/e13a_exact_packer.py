#!/usr/bin/env python3
import argparse, hashlib, os, stat, sys, zipfile
from pathlib import Path

ROOT_NAME = "yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate"
FIXED_DT = (2025, 12, 31, 19, 0, 0)
EXPECTED_ZIP_SHA256 = "e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65"
EXPECTED_ZIP_BYTES = 209505
EXPECTED_FILES = 45


def sha256_bytes(b): return hashlib.sha256(b).hexdigest()

def load_manifest(path):
    rows=[]
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip(): continue
        sha, size, rel = raw.split("\t", 2)
        rows.append((rel, int(size), sha))
    if len(rows) != EXPECTED_FILES:
        raise SystemExit(f"manifest file count {len(rows)} != {EXPECTED_FILES}")
    return rows

def source_path(repo, rel):
    if rel.startswith("tests/"):
        return repo / "extension" / rel
    return repo / "extension" / "src" / rel

def zipinfo(name, is_dir):
    zi=zipfile.ZipInfo(name, FIXED_DT)
    zi.create_system=3
    zi.create_version=20
    zi.extract_version=20
    zi.flag_bits=0
    zi.internal_attr=0
    zi.extra=b""
    zi.comment=b""
    if is_dir:
        zi.compress_type=zipfile.ZIP_STORED
        zi.external_attr=((stat.S_IFDIR | 0o755) << 16) | 0x10
    else:
        zi.compress_type=zipfile.ZIP_DEFLATED
        zi.external_attr=(stat.S_IFREG | 0o644) << 16
    return zi

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--output", required=True)
    args=ap.parse_args()
    repo=Path(args.repo_root).resolve(); manifest=Path(args.manifest).resolve(); out=Path(args.output).resolve()
    rows=load_manifest(manifest)
    payload=[]
    for rel, size, sha in rows:
        src=source_path(repo, rel)
        b=src.read_bytes()
        actual=sha256_bytes(b)
        if len(b)!=size or actual!=sha:
            raise SystemExit(f"source identity FAIL {rel}: bytes {len(b)}/{size}, sha {actual}/{sha}")
        payload.append((rel,b))
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, strict_timestamps=True) as z:
        z.comment=b""
        for d in (ROOT_NAME+"/", ROOT_NAME+"/shared/", ROOT_NAME+"/tests/"):
            z.writestr(zipinfo(d, True), b"")
        for rel,b in sorted(payload, key=lambda x:x[0]):
            z.writestr(zipinfo(ROOT_NAME+"/"+rel, False), b, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    b=out.read_bytes(); actual=sha256_bytes(b)
    with zipfile.ZipFile(out,"r") as z:
        bad=z.testzip(); files=sum(1 for n in z.namelist() if not n.endswith("/")); entries=len(z.infolist())
    print(f"artifact={out}")
    print(f"sha256={actual}")
    print(f"bytes={len(b)}")
    print(f"files={files}")
    print(f"entries={entries}")
    print(f"zip_test={bad or 'PASS'}")
    if actual!=EXPECTED_ZIP_SHA256 or len(b)!=EXPECTED_ZIP_BYTES or files!=EXPECTED_FILES or entries!=48 or bad is not None:
        raise SystemExit("EXACT_ARTIFACT_IDENTITY_FAIL")
    print("EXACT_ARTIFACT_IDENTITY_PASS")

if __name__ == "__main__": main()
