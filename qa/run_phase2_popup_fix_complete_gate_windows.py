#!/usr/bin/env python3
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile

repo = Path.cwd().resolve()
source = repo / "qa" / "phase2_popup_fix_complete_gate.py"
raw = source.read_text(encoding="utf-8")

old = '''for name, path, commit in [
    ("worktree_source", source_wt, SOURCE_COMMIT),
    ("worktree_transport", transport_wt, TRANSPORT_COMMIT),
    ("worktree_stage4", stage4_wt, STAGE4_HARNESS_COMMIT),
]:
    rc, out = run(name, ["git", "worktree", "add", "--detach", str(path), commit], timeout=300)
    if rc != 0:
        append_master(f"WORKTREE_SETUP_FAIL {name}\\n")
'''

new = '''for name, path, commit in [
    ("worktree_source", source_wt, SOURCE_COMMIT),
    ("worktree_transport", transport_wt, TRANSPORT_COMMIT),
    ("worktree_stage4", stage4_wt, STAGE4_HARNESS_COMMIT),
]:
    if name == "worktree_source":
        worktree_cmd = ["git", "-c", "core.autocrlf=false", "-c", "core.eol=lf", "worktree", "add", "--detach", str(path), commit]
    else:
        worktree_cmd = ["git", "worktree", "add", "--detach", str(path), commit]
    rc, out = run(name, worktree_cmd, timeout=300)
    if rc != 0:
        append_master(f"WORKTREE_SETUP_FAIL {name}\\n")
'''

if raw.count(old) != 1:
    raise SystemExit("WINDOWS_SOURCE_WORKTREE_PATCH_ANCHOR_FAIL")
patched = raw.replace(old, new, 1)

base_sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
patched_sha = hashlib.sha256(patched.encode("utf-8")).hexdigest()
print(f"WINDOWS_GATE_BASE_EXECUTOR_SHA256={base_sha}")
print(f"WINDOWS_GATE_EFFECTIVE_EXECUTOR_SHA256={patched_sha}")
print("WINDOWS_EXACT_SOURCE_WORKTREE_COMMAND=git -c core.autocrlf=false -c core.eol=lf worktree add --detach")
print("WINDOWS_QA_CHECKOUT_CONFIG_UNCHANGED_PASS")

runner_temp = Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir())).resolve()
effective = runner_temp / "phase2_popup_fix_complete_gate_windows_effective.py"
effective.write_text(patched, encoding="utf-8", newline="\n")

proc = subprocess.run([sys.executable, str(effective)], cwd=str(repo), env=os.environ.copy())
raise SystemExit(proc.returncode)
