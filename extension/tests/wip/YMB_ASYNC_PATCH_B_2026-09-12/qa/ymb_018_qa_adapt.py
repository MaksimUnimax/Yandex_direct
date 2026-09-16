"""Candidate-only QA adaptation for YMB 0.1.8 durable deferred Search ownership.

The differential base remains on the preserved B19/0.1.6 expectations. This
script updates only intentional candidate expectations: release version text
and the B7 start assertion that a durable job owner is the Search folder scope,
not the ChatGPT conversation key.

Usage:
  ymb_018_qa_adapt.py CONTRACT_QA_DIR [EXPORT_B7_TEST]
"""
from pathlib import Path
import hashlib
import json
import sys

H = lambda b: hashlib.sha256(b).hexdigest()
if len(sys.argv) not in (2, 3):
    raise SystemExit(__doc__)
root = Path(sys.argv[1]).resolve()
report = {
    "schema_version": 1,
    "kind": "YMB_0_1_8_CANDIDATE_QA_ADAPTATION",
    "product_change": False,
    "expected_version": "0.1.8",
    "files": {},
}

p = root / "b12_contract.test.mjs"
before = p.read_bytes()
s = before.decode()
replacements = [
    ("assert.equal(m.version,'0.1.6');", "assert.equal(m.version,'0.1.8');"),
    (
        "test('saved READMEs describe the real 0.1.6 network-enabled Manual deferred release without background polling claims',()=>{",
        "test('saved READMEs describe the real 0.1.8 network-enabled Manual deferred release without background polling claims',()=>{",
    ),
    ("assert.ok(s.includes('0.1.6'),name);", "assert.ok(s.includes('0.1.8'),name);"),
]
for old, new in replacements:
    if s.count(old) != 1:
        raise ValueError(f"Unexpected contract QA preimage for {old!r}: count={s.count(old)}")
    s = s.replace(old, new)
p.write_text(s)
report["files"][p.name] = {
    "before_sha256": H(before),
    "after_sha256": H(p.read_bytes()),
    "replacements": len(replacements),
}

if len(sys.argv) == 3:
    p = Path(sys.argv[2]).resolve()
    before = p.read_bytes()
    s = before.decode()
    old = "assert.equal(h.calls.create[0].owner,KEY);"
    new = "assert.equal(h.calls.create[0].owner,'search-folder:folder');"
    if s.count(old) != 1:
        raise ValueError(f"Unexpected B7 owner QA preimage: count={s.count(old)}")
    s = s.replace(old, new)
    p.write_text(s)
    report["files"][p.name] = {
        "before_sha256": H(before),
        "after_sha256": H(p.read_bytes()),
        "replacements": 1,
    }

out = root / "YMB_0_1_8_QA_ADAPTATION.json"
out.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
