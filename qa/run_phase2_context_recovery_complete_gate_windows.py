#!/usr/bin/env python3
import ast
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile

repo = Path.cwd().resolve()
base_path = repo / "qa" / "phase2_popup_fix_complete_gate.py"
legacy_windows_path = repo / "qa" / "run_phase2_popup_fix_complete_gate_windows.py"
raw = base_path.read_text(encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}_PATCH_ANCHOR_FAIL count={count}")
    return text.replace(old, new, 1)


def assigned_literal(path: Path, name: str) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            value = ast.literal_eval(node.value)
            if not isinstance(value, str):
                raise SystemExit(f"LEGACY_{name.upper()}_NOT_STRING")
            return value
    raise SystemExit(f"LEGACY_{name.upper()}_MISSING")


patched = raw

old_constants = '''SOURCE_COMMIT = "10bb3aca67295e5e515ff2ade8914b23e8458ca7"
TRANSPORT_COMMIT = "cf467d5b2c489dc8931758debbf7bf821abe1d4f"
STAGE4_HARNESS_COMMIT = "667fda2f9a0e4197c4873ea96f27862c8453f2f0"
ARTIFACT_NAME = "yandex-marketing-bridge-0.1.1-phase2-search-popup-fix-candidate.zip"
ARTIFACT_SHA256 = "0186b35d66cf1e7e20a522dc128b3fdd317cd660c665b8294120a1ab8affe91d"
ARTIFACT_BYTES = 171655
ARTIFACT_FILES = 66
ARTIFACT_ENTRIES = 69
MANIFEST_NAME = "EXACT_POPUP_FIX_CANDIDATE_MANIFEST_2026-08-24.json"
MANIFEST_SHA256 = "447bf18e54ba4a728cc6255adff5e13996366b9bf54b2668114110d525501009"
MANIFEST_BYTES = 11601
TRANSPORT_REL = Path("extension/tests/qa_transport/phase2-popup-fix-final-b64")
'''
new_constants = '''SOURCE_COMMIT = "f4aee34c0a3455aa7199f6aa54bd581c71d97337"
TRANSPORT_COMMIT = "7c787eedd9856c3f91fbed85aeaea7f3405ad473"
STAGE4_HARNESS_COMMIT = "667fda2f9a0e4197c4873ea96f27862c8453f2f0"
CONTEXT_HARNESS_COMMIT = "f77e91fcff75b85290e012ffec79123aa7fc9f0e"
ARTIFACT_NAME = "yandex-marketing-bridge-0.1.1-phase2-search-context-recovery-candidate.zip"
ARTIFACT_SHA256 = "739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46"
ARTIFACT_BYTES = 175971
ARTIFACT_FILES = 68
ARTIFACT_ENTRIES = 71
MANIFEST_NAME = "EXACT_CONTEXT_RECOVERY_CANDIDATE_MANIFEST_2026-08-25.json"
MANIFEST_SHA256 = "bbe8b2665c3339f9ac4bc2243b88a4076680a585220d38b224d10ae02cd91478"
MANIFEST_BYTES = 11933
TRANSPORT_REL = Path("extension/tests/qa_transport/phase2-context-recovery-final-b64")
'''
patched = replace_once(patched, old_constants, new_constants, "CURRENT_IDENTITIES")

patched = replace_once(
    patched,
    '    "b04": False,\n    "final_exactness": False,',
    '    "b04": False,\n    "b05": False,\n    "final_exactness": False,',
    "RESULT_B05",
)

old_authority = '''    checkpoint = git_text("show", f"origin/main:extension/tests/PHASE_2_POPUP_FIX_REFROZEN_CANDIDATE_CHECKPOINT_2026-08-24.md")
    b04doc = git_text("show", f"origin/main:extension/docs/CODEX_PRE_DELIVERY_NATIVE_ACTION_POPUP_GEOMETRY_ADDENDUM_2026-08-24.md")
    results["authority"] = all(x in checkpoint for x in [SOURCE_COMMIT, ARTIFACT_SHA256, TRANSPORT_COMMIT, "COMPLETE CODEX RERUN REQUIRED"]) and all(x in b04doc for x in ["B04_NATIVE_ACTION_POPUP_GEOMETRY_PASS", "chrome.action.openPopup()", "430 px", "560 px"])
'''
new_authority = '''    freeze_doc = git_text("show", f"origin/main:extension/tests/PHASE_2_CONTEXT_RECOVERY_FREEZE_PASS_2026-08-25.md")
    transport_doc = git_text("show", f"origin/main:extension/tests/PHASE_2_CONTEXT_RECOVERY_WINDOWS_TRANSPORT_PASS_2026-08-25.md")
    state_doc = git_text("show", f"origin/main:extension/docs/CURRENT_STATE.md")
    results["authority"] = (
        all(x in freeze_doc for x in [SOURCE_COMMIT, ARTIFACT_SHA256, MANIFEST_SHA256, "239/239 PASS", "CONTEXT_RECOVERY_FREEZE_PASS"]) and
        all(x in transport_doc for x in [SOURCE_COMMIT, ARTIFACT_SHA256, MANIFEST_SHA256, TRANSPORT_COMMIT, "WINDOWS_SAFE_EXACT_TRANSPORT_PASS"]) and
        all(x in state_doc for x in [SOURCE_COMMIT, ARTIFACT_SHA256, MANIFEST_SHA256, TRANSPORT_COMMIT, "AUTHORIZED_NEXT_STAGE = COMPLETE_GOVERNED_GATE", "AUTHORIZED_NEXT_ACTION = RUN_COMPLETE_GOVERNED_GATE_ON_739DD5D7", "OWNER_LIVE = BLOCKED"])
    )
'''
patched = replace_once(patched, old_authority, new_authority, "LIVE_AUTHORITY")

old_worktrees = '''# Fresh detached worktrees.
work_root = RUNNER_TEMP / "ymb-complete-gate-0186"
if work_root.exists():
    shutil.rmtree(work_root, ignore_errors=True)
work_root.mkdir(parents=True, exist_ok=True)
source_wt = work_root / "source"
transport_wt = work_root / "transport"
stage4_wt = work_root / "stage4-harness"
artifact_dir = work_root / "artifact"
artifact_dir.mkdir(parents=True, exist_ok=True)
zip_path = artifact_dir / ARTIFACT_NAME
extract_root = artifact_dir / "extract"

for name, path, commit in [
    ("worktree_source", source_wt, SOURCE_COMMIT),
    ("worktree_transport", transport_wt, TRANSPORT_COMMIT),
    ("worktree_stage4", stage4_wt, STAGE4_HARNESS_COMMIT),
]:
    rc, out = run(name, ["git", "worktree", "add", "--detach", str(path), commit], timeout=300)
    if rc != 0:
        append_master(f"WORKTREE_SETUP_FAIL {name}\\n")
'''
new_worktrees = '''# Fresh detached worktrees.
work_root = RUNNER_TEMP / "ymb-complete-gate-739dd5d"
if work_root.exists():
    shutil.rmtree(work_root, ignore_errors=True)
work_root.mkdir(parents=True, exist_ok=True)
source_wt = work_root / "source"
transport_wt = work_root / "transport"
stage4_wt = work_root / "stage4-harness"
context_wt = work_root / "context-harness"
artifact_dir = work_root / "artifact"
artifact_dir.mkdir(parents=True, exist_ok=True)
zip_path = artifact_dir / ARTIFACT_NAME
extract_root = artifact_dir / "extract"

for name, path, commit in [
    ("worktree_source", source_wt, SOURCE_COMMIT),
    ("worktree_transport", transport_wt, TRANSPORT_COMMIT),
    ("worktree_stage4", stage4_wt, STAGE4_HARNESS_COMMIT),
    ("worktree_context", context_wt, CONTEXT_HARNESS_COMMIT),
]:
    if name == "worktree_source":
        worktree_cmd = ["git", "-c", "core.autocrlf=false", "-c", "core.eol=lf", "worktree", "add", "--detach", str(path), commit]
    else:
        worktree_cmd = ["git", "worktree", "add", "--detach", str(path), commit]
    rc, out = run(name, worktree_cmd, timeout=300)
    if rc != 0:
        append_master(f"WORKTREE_SETUP_FAIL {name}\\n")
'''
patched = replace_once(patched, old_worktrees, new_worktrees, "CURRENT_WORKTREES_AND_WINDOWS_LF")

patched = replace_once(
    patched,
    r'bool(re.search(r"(?:#\s*)?pass\s+234\b", out, re.I))',
    r'bool(re.search(r"(?:#\s*)?pass\s+239\b", out, re.I))',
    "SOURCE_PASS_COUNT",
)
patched = replace_once(patched, '"PACKAGED_SYNTAX_PASS count=60" in out', '"PACKAGED_SYNTAX_PASS count=62" in out', "PACKAGED_SYNTAX_RESULT")
patched = replace_once(
    patched,
    '"PACKAGED_SYNTAX_PASS count=60", "PACKAGED_JSON_PASS count=2",\n        "PACKAGED_SUITE_PASS files=39", "PACKAGED_PREDELIVERY_PREFLIGHT_PASS"',
    '"PACKAGED_SYNTAX_PASS count=62", "PACKAGED_JSON_PASS count=2",\n        "PACKAGED_SUITE_PASS files=40", "PACKAGED_PREDELIVERY_PREFLIGHT_PASS"',
    "PACKAGED_MARKERS",
)
patched = replace_once(
    patched,
    r'bool(re.search(r"(?:#\s*)?pass\s+234\b", out, re.I))',
    r'bool(re.search(r"(?:#\s*)?pass\s+239\b", out, re.I))',
    "PACKAGED_PASS_COUNT",
)

# Reuse the exact Stage-4 tab-identity stabilization that produced the previous complete PASS.
browser_old = assigned_literal(legacy_windows_path, "browser_old")
browser_new = assigned_literal(legacy_windows_path, "browser_new")
patched = replace_once(patched, browser_old, browser_new, "STAGE4_TAB_IDENTITY_STABILIZATION")

b05_block = '''# Step 6: B-05 already-open ChatGPT context-recovery gate against the same exact extracted artifact.
if extension_root and CHROME_PATH and Path(CHROME_PATH).exists() and context_wt.exists():
    context_driver_dir = context_wt / "extension/tests/qa_browser"
    npm = shutil.which("npm") or "npm"
    dep5_rc, dep5_out = run("context_driver_install", [npm, "install", "--no-save", "--package-lock=false", "puppeteer-core@25.4.0"], cwd=context_driver_dir, timeout=900)
    if dep5_rc == 0:
        context_harness = context_driver_dir / "popup_context_recovery_gate.mjs"
        rc, out = run("browser_b05", [shutil.which("node") or "node", str(context_harness), CHROME_PATH, str(extension_root)], cwd=context_driver_dir, timeout=900)
        results["b05"] = rc == 0 and all(m in out for m in [
            "CONTEXT_RECOVERY_CHAT_PAGE_REMAINED_OPEN_PASS",
            "CONTEXT_RECOVERY_NATIVE_ACTION_TRIGGER_PASS",
            "CONTEXT_RECOVERY_NATIVE_ACTION_POPUP_OPEN_PASS",
            "CONTEXT_RECOVERY_MISSING_RECEIVER_REPRODUCED_PASS",
            "POPUP_CONTEXT_SELF_RECOVERY_PASS",
            "CONTEXT_RECOVERY_BIND_PASS",
            "CONTEXT_RECOVERY_MANUAL_ON_PASS",
            "CONTEXT_RECOVERY_ALREADY_OPEN_CHATGPT_PASS",
            "REAL_YANDEX_REQUESTS=0",
        ])
else:
    append_master(f"B05_BROWSER_PREREQ_FAIL extension_root={extension_root} chrome={CHROME_PATH} context_wt={context_wt}\\n")

'''
patched = replace_once(
    patched,
    '# Cleanup externally installed driver material before cleanliness proof.\n',
    b05_block + '# Cleanup externally installed driver material before cleanliness proof.\n',
    "B05_INSERT",
)
patched = replace_once(
    patched,
    'for d in [stage4_wt / "extension/tests/qa_browser/phase2-stage4/node_modules", source_wt / "extension/tests/qa_browser/node_modules"]:',
    'for d in [stage4_wt / "extension/tests/qa_browser/phase2-stage4/node_modules", source_wt / "extension/tests/qa_browser/node_modules", context_wt / "extension/tests/qa_browser/node_modules"]:',
    "B05_CLEANUP",
)
patched = replace_once(
    patched,
    '''    stage4_clean = clean_worktree(stage4_wt)
    qa_rc, qa_out = run("clean_qa_branch", ["git", "status", "--porcelain"], cwd=REPO, timeout=120)
''',
    '''    stage4_clean = clean_worktree(stage4_wt)
    context_clean = clean_worktree(context_wt)
    qa_rc, qa_out = run("clean_qa_branch", ["git", "status", "--porcelain"], cwd=REPO, timeout=120)
''',
    "B05_CLEAN_STATUS",
)
patched = replace_once(
    patched,
    '    results["cleanliness"] = source_clean and transport_clean and stage4_clean and qa_rc == 0 and not qa_dirty',
    '    results["cleanliness"] = source_clean and transport_clean and stage4_clean and context_clean and qa_rc == 0 and not qa_dirty',
    "B05_CLEAN_REQUIREMENT",
)

patched = replace_once(
    patched,
    'all_required = all(pd.values()) and all(search.values()) and results["b02"] and results["b04"] and authority_artifact and source_core and package_core and final_core',
    'all_required = all(pd.values()) and all(search.values()) and results["b02"] and results["b04"] and results["b05"] and authority_artifact and source_core and package_core and final_core',
    "B05_ALL_REQUIRED",
)
patched = replace_once(
    patched,
    'if (not results["b01"] or not results["b02"] or not results["b03"] or not results["b04"]) and results["artifact"]:',
    'if (not results["b01"] or not results["b02"] or not results["b03"] or not results["b04"] or not results["b05"]) and results["artifact"]:',
    "B05_BROWSER_FAIL_CONDITION",
)
patched = replace_once(
    patched,
    '["browser_b01_b03", "browser_b04"] if n in logs',
    '["browser_b01_b03", "browser_b04", "browser_b05"] if n in logs',
    "B05_BROWSER_FAIL_LOGS",
)
patched = replace_once(
    patched,
    '["B01_PROJECT_WORK_FAIL", "MANUAL_", "SEARCH_", "POPUP_GEOMETRY"]',
    '["B01_PROJECT_WORK_FAIL", "MANUAL_", "SEARCH_", "POPUP_GEOMETRY", "CONTEXT_RECOVERY", "POPUP_CONTEXT"]',
    "B05_PRODUCT_FAILURE_SIGNATURES",
)

patched = replace_once(
    patched,
    '        "native_popup_harness_commit": SOURCE_COMMIT,\n',
    '        "native_popup_harness_commit": SOURCE_COMMIT,\n        "context_recovery_harness_commit": CONTEXT_HARNESS_COMMIT,\n',
    "REPORT_CONTEXT_HARNESS",
)
patched = replace_once(patched, '"source_suite": "234/234 PASS"', '"source_suite": "239/239 PASS"', "REPORT_SOURCE_COUNT")
patched = replace_once(patched, '"packaged_suite": "234/234 PASS"', '"packaged_suite": "239/239 PASS"', "REPORT_PACKAGED_COUNT")
patched = replace_once(patched, '"packaged_syntax": "60/60 PASS"', '"packaged_syntax": "62/62 PASS"', "REPORT_PACKAGED_SYNTAX")
patched = replace_once(
    patched,
    '    "browser_native_action_popup_geometry": "PASS" if results["b04"] else "FAIL",\n',
    '    "browser_native_action_popup_geometry": "PASS" if results["b04"] else "FAIL",\n    "browser_context_recovery": "PASS" if results["b05"] else "FAIL",\n',
    "REPORT_B05",
)
patched = replace_once(
    patched,
    '"real_yandex_requests": 0 if results["b03"] and results["b04"] else None,',
    '"real_yandex_requests": 0 if results["b03"] and results["b04"] and results["b05"] else None,',
    "REPORT_REAL_YANDEX_B05",
)
patched = replace_once(
    patched,
    '["authority", "transport", "artifact", "source_suite", "source_static", "packaged_suite", "packaged_syntax", "packaged_json", "b01", "b02", "b03", "b04", "final_exactness", "cleanliness"]',
    '["authority", "transport", "artifact", "source_suite", "source_static", "packaged_suite", "packaged_syntax", "packaged_json", "b01", "b02", "b03", "b04", "b05", "final_exactness", "cleanliness"]',
    "MD_CORE_B05",
)
patched = replace_once(
    patched,
    'md.append("- real_yandex_requests: **0**" if results["b03"] and results["b04"] else "- real_yandex_requests: **UNPROVEN**")',
    'md.append("- real_yandex_requests: **0**" if results["b03"] and results["b04"] and results["b05"] else "- real_yandex_requests: **UNPROVEN**")',
    "MD_REAL_YANDEX_B05",
)
patched = replace_once(
    patched,
    '        "PHASE2_POPUP_FIX_COMPLETE_GATE_PASS", flush=True)',
    '        "PHASE2_CONTEXT_RECOVERY_COMPLETE_GATE_PASS", flush=True)',
    "PASS_MARKER_NAME",
)
patched = replace_once(
    patched,
    'print("PHASE2_POPUP_FIX_COMPLETE_GATE_FAIL", flush=True)',
    'print("PHASE2_CONTEXT_RECOVERY_COMPLETE_GATE_FAIL", flush=True)',
    "FAIL_MARKER_NAME",
)

base_sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
effective_sha = hashlib.sha256(patched.encode("utf-8")).hexdigest()
print(f"CONTEXT_GATE_BASE_EXECUTOR_SHA256={base_sha}")
print(f"CONTEXT_GATE_EFFECTIVE_EXECUTOR_SHA256={effective_sha}")
print("WINDOWS_EXACT_SOURCE_WORKTREE_COMMAND=git -c core.autocrlf=false -c core.eol=lf worktree add --detach")
print("WINDOWS_QA_CHECKOUT_CONFIG_UNCHANGED_PASS")
print("STAGE4_POPUP_REOPEN_BY_TAB_ID_HARNESS_PATCH_PASS")
print("CONTEXT_RECOVERY_B05_ADDED_PASS")
print("CONTEXT_RECOVERY_CURRENT_IDENTITIES_PINNED_PASS")

runner_temp = Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir())).resolve()
effective = runner_temp / "phase2_context_recovery_complete_gate_windows_effective.py"
effective.write_text(patched, encoding="utf-8", newline="\n")

proc = subprocess.run([sys.executable, str(effective)], cwd=str(repo), env=os.environ.copy())
raise SystemExit(proc.returncode)
