"""Candidate-only QA adaptation for YMB 0.1.9 durable deferred Search ownership.

The differential base remains on the preserved B19/0.1.6 expectations. This
script updates only intentional candidate expectations:
- release version text 0.1.6 -> 0.1.9;
- direct deferred Search store fixtures use the durable Search-folder owner;
- preserved export fixtures expect the same durable owner.

ChatGPT conversation KEY usages for binding, tab authority, Manual state, outbox
and delivery remain unchanged. The adapter never rewrites those authority paths.

The historical filename is retained because the qualification workflow already
uses it; the target release identity is authoritative in this file and report.

Usage:
  ymb_018_qa_adapt.py CONTRACT_QA_DIR [EXPORT_QA_DIR_OR_B7_TEST]
"""
from pathlib import Path
import hashlib
import json
import re
import sys

H = lambda b: hashlib.sha256(b).hexdigest()
JOB_OWNER = "'search-folder:folder'"
if len(sys.argv) not in (2, 3):
    raise SystemExit(__doc__)
root = Path(sys.argv[1]).resolve()
report = {
    "schema_version": 4,
    "kind": "YMB_0_1_9_CANDIDATE_QA_ADAPTATION",
    "product_change": False,
    "expected_version": "0.1.9",
    "durable_job_owner": "search-folder:folder",
    "conversation_authority_rewritten": False,
    "files": {},
}

def write_patch(path, transform, label):
    path = Path(path).resolve()
    before = path.read_bytes()
    text = before.decode()
    new, counts = transform(text)
    if new == text:
        raise ValueError(f"No QA adaptation applied for {path.name}: {label}")
    path.write_text(new)
    report["files"][path.name] = {
        "before_sha256": H(before),
        "after_sha256": H(path.read_bytes()),
        "changes": counts,
        "label": label,
    }


def contract_version(text):
    replacements = [
        ("assert.equal(m.version,'0.1.6');", "assert.equal(m.version,'0.1.9');"),
        (
            "test('saved READMEs describe the real 0.1.6 network-enabled Manual deferred release without background polling claims',()=>{",
            "test('saved READMEs describe the real 0.1.9 network-enabled Manual deferred release without background polling claims',()=>{",
        ),
        ("assert.ok(s.includes('0.1.6'),name);", "assert.ok(s.includes('0.1.9'),name);"),
    ]
    counts = {}
    for old, new in replacements:
        count = text.count(old)
        if count != 1:
            raise ValueError(f"Unexpected contract QA preimage for {old!r}: count={count}")
        text = text.replace(old, new)
        counts[old] = count
    return text, counts

write_patch(root / "b12_contract.test.mjs", contract_version, "release-version")

# These files directly inspect or seed deferred Search store state. Rewrite only
# durable-store owner positions; conversation KEY authority remains untouched.
def durable_store_owner(text):
    counts = {}
    text, n = re.subn(r"owner:KEY", f"owner:{JOB_OWNER}", text)
    counts["owner:KEY"] = n
    text, n2 = re.subn(r"owner=KEY", f"owner={JOB_OWNER}", text)
    counts["owner=KEY"] = n2
    # Store read APIs use owner as the second positional argument. Preserve the
    # whole call prefix and replace only the literal `,KEY` suffix.
    pattern = r"(\.(?:getSummary|readResult|readItem|pageItems)\([^,\n]+),KEY(?=[,)])"
    text, n3 = re.subn(pattern, lambda m: m.group(1) + "," + JOB_OWNER, text)
    counts["store-second-arg-KEY"] = n3
    if sum(counts.values()) == 0:
        raise ValueError("No deferred store owner positions found")
    return text, counts

for name in [
    "b10_deferred.test.mjs",
    "b11_reparse.test.mjs",
    "b12_contract.test.mjs",
    "b9_full_worker.test.mjs",
]:
    path = root / name
    before = path.read_bytes()
    text = before.decode()
    new, counts = durable_store_owner(text)
    if new == text:
        raise ValueError(f"No durable owner adaptation for {name}")
    path.write_text(new)
    prior = report["files"].get(name)
    entry = {
        "before_sha256": prior["before_sha256"] if prior else H(before),
        "after_sha256": H(path.read_bytes()),
        "changes": {**(prior.get("changes", {}) if prior else {}), **counts},
        "label": "release-version+durable-store-owner" if prior else "durable-store-owner",
    }
    report["files"][name] = entry

if len(sys.argv) == 3:
    supplied = Path(sys.argv[2]).resolve()
    export_dir = supplied if supplied.is_dir() else supplied.parent

    p = export_dir / "b7_worker.test.mjs"
    def b7_owner(text):
        old = "assert.equal(h.calls.create[0].owner,KEY);"
        new = "assert.equal(h.calls.create[0].owner,'search-folder:folder');"
        count = text.count(old)
        if count != 1:
            raise ValueError(f"Unexpected B7 owner QA preimage: count={count}")
        return text.replace(old, new), {old: count}
    write_patch(p, b7_owner, "B7 durable owner expectation")

    p = export_dir / "b8_worker.test.mjs"
    def b8_owner(text):
        changes = {}
        old = "assert.equal(o,KEY);"
        count = text.count(old)
        if count != 1:
            raise ValueError(f"Unexpected B8 read owner preimage: count={count}")
        text = text.replace(old, "assert.equal(o,'search-folder:folder');")
        changes[old] = count
        old2 = "h.store.readResult('job-1',KEY,0)"
        count2 = text.count(old2)
        if count2 != 1:
            raise ValueError(f"Unexpected B8 readResult owner preimage: count={count2}")
        text = text.replace(old2, "h.store.readResult('job-1','search-folder:folder',0)")
        changes[old2] = count2
        return text, changes
    write_patch(p, b8_owner, "B8 durable owner fixture")

# Prove actual conversation-authority fields were not rewritten.
for name in ["b10_deferred.test.mjs", "b11_reparse.test.mjs", "b12_contract.test.mjs"]:
    text = (root / name).read_text()
    if "conversation_key:KEY" not in text:
        raise ValueError(f"Conversation authority marker unexpectedly absent in {name}")

out = root / "YMB_0_1_9_QA_ADAPTATION.json"
out.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
