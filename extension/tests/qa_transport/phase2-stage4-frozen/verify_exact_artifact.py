#!/usr/bin/env python3
import hashlib, json, zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
ZIP = BASE / "yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip"
MANIFEST = BASE / "EXACT_CANDIDATE_MANIFEST_2026-08-24.json"
EXPECTED_SHA = "0f0b035c6bc04da841d549182c3dcea6e7cf10074eddebafdf1c3a4c21c98411"
EXPECTED_BYTES = 170726
EXPECTED_FILES = 65
EXPECTED_ENTRIES = 68

data = ZIP.read_bytes()
if hashlib.sha256(data).hexdigest() != EXPECTED_SHA or len(data) != EXPECTED_BYTES:
    raise SystemExit("EXACT_ZIP_IDENTITY_FAIL")
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest["sha256"] != EXPECTED_SHA or manifest["bytes"] != EXPECTED_BYTES:
    raise SystemExit("MANIFEST_ARTIFACT_IDENTITY_FAIL")

with zipfile.ZipFile(ZIP) as z:
    if z.testzip() is not None:
        raise SystemExit("ZIP_INTEGRITY_FAIL")
    infos = z.infolist()
    files = [i for i in infos if not i.is_dir()]
    if len(files) != EXPECTED_FILES or len(infos) != EXPECTED_ENTRIES:
        raise SystemExit("ZIP_COUNT_FAIL")
    root = manifest["root_name"].rstrip("/") + "/"
    actual = {}
    for info in files:
        if not info.filename.startswith(root):
            raise SystemExit("ZIP_ROOT_FAIL")
        rel = info.filename[len(root):]
        payload = z.read(info)
        actual[rel] = {"path": rel, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}

expected = {row["path"]: row for row in manifest["payload"]}
if actual != expected:
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    raise SystemExit(f"PAYLOAD_MANIFEST_FAIL missing={missing} extra={extra}")

print("EXACT_ZIP_IDENTITY_PASS")
print("ZIP_INTEGRITY_PASS")
print("ROUNDTRIP_PAYLOAD_MANIFEST_PASS")
print(f"sha256={EXPECTED_SHA}")
print(f"bytes={EXPECTED_BYTES}")
print(f"files={EXPECTED_FILES}")
print(f"entries={EXPECTED_ENTRIES}")
