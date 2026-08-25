#!/usr/bin/env python3
import ast
import os
from pathlib import Path
import subprocess
import sys
import tempfile

repo = Path.cwd().resolve()
source_path = repo / "qa" / "run_phase2_context_recovery_complete_gate_windows.py"
tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))

fixes = {
    "SOURCE_PASS_COUNT": (
        'bool(re.search(r"(?:#\\s*)?pass\\s+234\\b", out, re.I))',
        'bool(re.search(r"(?:#\\s*)?pass\\s+239\\b", out, re.I))',
    ),
    "PACKAGED_PASS_COUNT": (
        'bool(re.search(r"(?:#\\s*)?pass\\s+234\\b", out, re.I))',
        'bool(re.search(r"(?:#\\s*)?pass\\s+239\\b", out, re.I))',
    ),
    "PASS_MARKER_NAME": (
        'print("PHASE2_POPUP_FIX_COMPLETE_GATE_PASS", flush=True)',
        'print("PHASE2_CONTEXT_RECOVERY_COMPLETE_GATE_PASS", flush=True)',
    ),
}

seen = set()
for node in ast.walk(tree):
    if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != "replace_once" or len(node.args) < 4:
        continue
    label_node = node.args[3]
    if not isinstance(label_node, ast.Constant) or not isinstance(label_node.value, str):
        continue
    label = label_node.value
    if label not in fixes:
        continue
    old, new = fixes[label]
    node.args[1] = ast.Constant(value=old)
    node.args[2] = ast.Constant(value=new)
    seen.add(label)

missing = sorted(set(fixes) - seen)
if missing:
    raise SystemExit("VALIDATED_WRAPPER_LABELS_MISSING " + ",".join(missing))

ast.fix_missing_locations(tree)
validated_source = ast.unparse(tree) + "\n"
compile(validated_source, "<validated-context-gate-wrapper>", "exec")
print("CONTEXT_GATE_WRAPPER_AST_VALIDATION_PASS")
print("CONTEXT_GATE_REGEX_ANCHORS_CORRECTED_PASS")
print("CONTEXT_GATE_PASS_MARKER_ANCHOR_CORRECTED_PASS")

runner_temp = Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir())).resolve()
validated = runner_temp / "run_phase2_context_recovery_complete_gate_windows_validated_effective.py"
validated.write_text(validated_source, encoding="utf-8", newline="\n")
proc = subprocess.run([sys.executable, str(validated)], cwd=str(repo), env=os.environ.copy())
raise SystemExit(proc.returncode)
