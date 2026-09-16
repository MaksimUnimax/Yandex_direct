"""Candidate-only QA adaptation for the intentional YMB 0.1.7 release version.

Run AFTER b19_final_qa_adapt_v2.py on the candidate QA workspace and AFTER
copying that 0.1.6-adapted workspace to the differential base. Product bytes
are never edited. Only exact version assertions/documentation expectations in
b12_contract.test.mjs move from 0.1.6 to 0.1.7.

Usage: ymb_017_qa_adapt.py QA_DIR
"""
from pathlib import Path
import hashlib
import json
import sys

H = lambda b: hashlib.sha256(b).hexdigest()
root = Path(sys.argv[1]).resolve()
p = root / "b12_contract.test.mjs"
before = p.read_bytes()
s = before.decode()

replacements = [
    ("assert.equal(m.version,'0.1.6');", "assert.equal(m.version,'0.1.7');"),
    (
        "test('saved READMEs describe the real 0.1.6 network-enabled Manual deferred release without background polling claims',()=>{",
        "test('saved READMEs describe the real 0.1.7 network-enabled Manual deferred release without background polling claims',()=>{",
    ),
    ("assert.ok(s.includes('0.1.6'),name);", "assert.ok(s.includes('0.1.7'),name);"),
]
for old, new in replacements:
    if s.count(old) != 1:
        raise ValueError(f"Unexpected 0.1.6 candidate QA preimage for {old!r}: count={s.count(old)}")
    s = s.replace(old, new)

if "assert.equal(m.version,'0.1.6');" in s or "assert.ok(s.includes('0.1.6'),name);" in s:
    raise ValueError("Stale 0.1.6 release assertion remains")

p.write_text(s)
report = {
    "schema_version": 1,
    "kind": "YMB_0_1_7_CANDIDATE_QA_VERSION_ADAPTATION",
    "product_change": False,
    "file": "b12_contract.test.mjs",
    "before_sha256": H(before),
    "after_sha256": H(p.read_bytes()),
    "replacements": len(replacements),
    "expected_version": "0.1.7",
}
(root / "YMB_0_1_7_QA_ADAPTATION.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
