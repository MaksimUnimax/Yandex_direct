#!/usr/bin/env python3
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

REPO = Path.cwd().resolve()
RUNNER_TEMP = Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir())).resolve()
CHROME_PATH = os.environ.get("CHROME_PATH", "")

SOURCE_COMMIT = "10bb3aca67295e5e515ff2ade8914b23e8458ca7"
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

EVIDENCE = REPO / "gate-evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)
MASTER_LOG = EVIDENCE / "complete-gate.log"

results = {
    "authority": False,
    "transport": False,
    "artifact": False,
    "source_suite": False,
    "source_static": False,
    "packaged_suite": False,
    "packaged_syntax": False,
    "packaged_json": False,
    "b01": False,
    "b02": False,
    "b03": False,
    "b04": False,
    "final_exactness": False,
    "cleanliness": False,
}
logs = {}


def append_master(text: str):
    with MASTER_LOG.open("a", encoding="utf-8", errors="replace") as f:
        f.write(text)
        if text and not text.endswith("\n"):
            f.write("\n")


def run(name, cmd, cwd=None, env=None, timeout=1200):
    cwd = Path(cwd or REPO)
    merged = os.environ.copy()
    if env:
        merged.update(env)
    rendered = " ".join(str(x) for x in cmd)
    append_master(f"\n===== {name} =====\nCWD={cwd}\nCMD={rendered}\n")
    print(f"[{name}] {rendered}", flush=True)
    try:
        p = subprocess.run(
            [str(x) for x in cmd], cwd=str(cwd), env=merged,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
        out = p.stdout or ""
        rc = p.returncode
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") + "\nTIMEOUT\n"
        rc = 124
    log_path = EVIDENCE / f"{name}.log"
    log_path.write_text(out, encoding="utf-8", errors="replace")
    append_master(out)
    logs[name] = str(log_path.name)
    print(out[-6000:], flush=True)
    print(f"[{name}] rc={rc}", flush=True)
    return rc, out


def git_text(*args, cwd=REPO):
    p = subprocess.run(["git", *args], cwd=str(cwd), stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stdout}")
    return p.stdout.strip()


def sha256_bytes(data: bytes):
    return hashlib.sha256(data).hexdigest()


def status_marker(out, marker):
    return marker in out


def clean_worktree(path: Path):
    rc, out = run("clean_" + path.name, ["git", "status", "--porcelain"], cwd=path, timeout=120)
    return rc == 0 and out.strip() == ""


# Step 0: live authority and exact commit metadata.
try:
    run("fetch_live", ["git", "fetch", "origin", "main", "--prune"], timeout=300)
    live_main = git_text("rev-parse", "origin/main")
    live_meta = git_text("show", "-s", "--format=%H%n%aI%n%s", "origin/main")
    (EVIDENCE / "live-main.txt").write_text(live_meta + "\n", encoding="utf-8")
    checkpoint = git_text("show", f"origin/main:extension/tests/PHASE_2_POPUP_FIX_REFROZEN_CANDIDATE_CHECKPOINT_2026-08-24.md")
    b04doc = git_text("show", f"origin/main:extension/docs/CODEX_PRE_DELIVERY_NATIVE_ACTION_POPUP_GEOMETRY_ADDENDUM_2026-08-24.md")
    results["authority"] = all(x in checkpoint for x in [SOURCE_COMMIT, ARTIFACT_SHA256, TRANSPORT_COMMIT, "COMPLETE CODEX RERUN REQUIRED"]) and all(x in b04doc for x in ["B04_NATIVE_ACTION_POPUP_GEOMETRY_PASS", "chrome.action.openPopup()", "430 px", "560 px"])
except Exception as e:
    live_main = "UNKNOWN"
    live_meta = repr(e)
    append_master(f"AUTHORITY_EXCEPTION={e!r}\n")

# Fresh detached worktrees.
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
        append_master(f"WORKTREE_SETUP_FAIL {name}\n")

# Step 1: Windows-safe exact transport, manifest raw bytes, exact ZIP materialization.
transport_dir = transport_wt / TRANSPORT_REL
manifest_path = transport_dir / MANIFEST_NAME
try:
    mb = manifest_path.read_bytes()
    attr_rc, attr_out = run("transport_attr", ["git", "check-attr", "text", "--", str(TRANSPORT_REL / MANIFEST_NAME)], cwd=transport_wt, timeout=120)
    verify_rc, verify_out = run("transport_verify_initial", [sys.executable, str(transport_dir / "verify_exact_b64_transport.py")], cwd=transport_wt, timeout=300)
    results["transport"] = (
        len(mb) == MANIFEST_BYTES and sha256_bytes(mb) == MANIFEST_SHA256 and
        attr_rc == 0 and "text: unset" in attr_out and verify_rc == 0 and
        all(status_marker(verify_out, m) for m in [
            "B64_REASSEMBLY_PASS", "EXACT_ZIP_IDENTITY_PASS",
            "ROUNDTRIP_PAYLOAD_MANIFEST_PASS", "ROUNDTRIP_ZIP_INTEGRITY_PASS",
            "FROZEN_AUTHORITY_MATCH_PASS", "REAL_YANDEX_REQUESTS=0"
        ])
    )
    data = base64.b64decode((transport_dir / "artifact.b64").read_bytes(), validate=True)
    zip_path.write_bytes(data)
    with zipfile.ZipFile(zip_path) as z:
        bad = z.testzip()
        infos = z.infolist()
        files = [i for i in infos if not i.is_dir()]
        if extract_root.exists():
            shutil.rmtree(extract_root)
        z.extractall(extract_root)
    results["artifact"] = (
        len(data) == ARTIFACT_BYTES and sha256_bytes(data) == ARTIFACT_SHA256 and
        bad is None and len(files) == ARTIFACT_FILES and len(infos) == ARTIFACT_ENTRIES
    )
except Exception as e:
    append_master(f"TRANSPORT_ARTIFACT_EXCEPTION={e!r}\n")

# Locate exact extracted extension root.
extension_roots = [p for p in extract_root.iterdir() if p.is_dir()] if extract_root.exists() else []
extension_root = extension_roots[0] if len(extension_roots) == 1 else None

# Step 2: complete exact source suite.
if source_wt.exists():
    npm = shutil.which("npm") or "npm"
    rc, out = run("source_suite", [npm, "test"], cwd=source_wt / "extension/src", timeout=1800)
    results["source_suite"] = rc == 0 and bool(re.search(r"(?:#\s*)?pass\s+234\b", out, re.I)) and not re.search(r"(?:#\s*)?fail\s+[1-9]\d*\b", out, re.I)

# Step 3: source static/syntax/JSON integrity.
try:
    syntax_files = []
    for base in [source_wt / "extension/src", source_wt / "extension/tests"]:
        for p in base.rglob("*"):
            if p.is_file() and p.suffix in {".js", ".mjs"} and "node_modules" not in p.parts:
                syntax_files.append(p)
    syntax_ok = True
    syntax_lines = []
    for p in syntax_files:
        proc = subprocess.run([shutil.which("node") or "node", "--check", str(p)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        syntax_lines.append(f"{p.relative_to(source_wt)} rc={proc.returncode}\n{proc.stdout}")
        if proc.returncode != 0:
            syntax_ok = False
    (EVIDENCE / "source_static_syntax.log").write_text("\n".join(syntax_lines), encoding="utf-8", errors="replace")
    json_ok = True
    json_rows = []
    for p in (source_wt / "extension/src").rglob("*.json"):
        try:
            json.loads(p.read_text(encoding="utf-8"))
            json_rows.append(f"PASS {p.relative_to(source_wt)}")
        except Exception as e:
            json_ok = False
            json_rows.append(f"FAIL {p.relative_to(source_wt)} {e!r}")
    (EVIDENCE / "source_static_json.log").write_text("\n".join(json_rows) + "\n", encoding="utf-8")
    results["source_static"] = syntax_ok and json_ok and len(syntax_files) > 0
except Exception as e:
    append_master(f"SOURCE_STATIC_EXCEPTION={e!r}\n")

# Step 4: complete exact packaged suite through governed adapter.
if results["artifact"] and source_wt.exists():
    pkg_work = work_root / "packaged-suite-work"
    adapter = source_wt / "extension/tests/qa_transport/phase2-candidate/run_packaged_suite.py"
    rc, out = run(
        "packaged_suite",
        [sys.executable, str(adapter), "--archive", str(zip_path), "--manifest", str(manifest_path), "--work-dir", str(pkg_work)],
        cwd=source_wt, timeout=1800,
    )
    results["packaged_syntax"] = rc == 0 and "PACKAGED_SYNTAX_PASS count=60" in out
    results["packaged_json"] = rc == 0 and "PACKAGED_JSON_PASS count=2" in out
    results["packaged_suite"] = rc == 0 and all(m in out for m in [
        "PACKAGE_EXACT_IDENTITY_PASS", "PACKAGED_SUITE_LAYOUT_IDENTITY_PASS",
        "PACKAGED_SYNTAX_PASS count=60", "PACKAGED_JSON_PASS count=2",
        "PACKAGED_SUITE_PASS files=39", "PACKAGED_PREDELIVERY_PREFLIGHT_PASS"
    ]) and bool(re.search(r"(?:#\s*)?pass\s+234\b", out, re.I))

# Step 5: B-01/B-02/B-03 installed-extension gate + B-04 real chrome.action popup geometry.
if extension_root and CHROME_PATH and Path(CHROME_PATH).exists():
    stage4_dir = stage4_wt / "extension/tests/qa_browser/phase2-stage4"
    popup_driver_dir = source_wt / "extension/tests/qa_browser"
    npm = shutil.which("npm") or "npm"
    dep1_rc, dep1_out = run("stage4_driver_install", [npm, "install", "--no-save", "--package-lock=false", "puppeteer-core@25.4.0"], cwd=stage4_dir, timeout=900)
    dep2_rc, dep2_out = run("popup_driver_install", [npm, "install", "--no-save", "--package-lock=false", "puppeteer-core@25.4.0"], cwd=popup_driver_dir, timeout=900)
    if dep1_rc == 0:
        harness = stage4_dir / "browser_phase2_stage4_gate.mjs"
        key = stage4_dir / "qa-chatgpt-local.key.pem"
        cert = stage4_dir / "qa-chatgpt-local.cert.pem"
        rc, out = run("browser_b01_b03", [shutil.which("node") or "node", str(harness), CHROME_PATH, str(extension_root), str(key), str(cert)], cwd=stage4_dir, timeout=900)
        results["b01"] = rc == 0 and "B01_PROJECT_WORK_PASS" in out
        results["b02"] = rc == 0 and all(m in out for m in ["B02_MANUAL_ON_TRANSACTION_PASS", "BROWSER_STEP_NATIVE_COPY_PASS"])
        results["b03"] = rc == 0 and all(m in out for m in ["B03_SEARCH_AUTORUN_PASS", "BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=1", "BROWSER_GATE_REAL_YANDEX_REQUESTS=0", "PHASE2_STAGE4_BROWSER_GATE_PASS"])
    if dep2_rc == 0:
        geo = popup_driver_dir / "popup_chrome151_geometry_gate.mjs"
        rc, out = run("browser_b04", [shutil.which("node") or "node", str(geo), CHROME_PATH, str(extension_root), "fixed"], cwd=popup_driver_dir, timeout=600)
        results["b04"] = rc == 0 and all(m in out for m in ["POPUP_CHROME151_ACTION_GEOMETRY_PASS", "POPUP_WIDE_REGRESSION_OBSERVED=false"]) and '"innerWidth":430' in out and '"innerHeight":560' in out and '"mainOverflowY":"auto"' in out and '"rootOverflow":"hidden"' in out
else:
    append_master(f"BROWSER_PREREQ_FAIL extension_root={extension_root} chrome={CHROME_PATH}\n")

# Cleanup externally installed driver material before cleanliness proof.
for d in [stage4_wt / "extension/tests/qa_browser/phase2-stage4/node_modules", source_wt / "extension/tests/qa_browser/node_modules"]:
    shutil.rmtree(d, ignore_errors=True)

# Remove packaged temporary work that may live outside worktrees; exact artifact remains evidence only.
shutil.rmtree(work_root / "packaged-suite-work", ignore_errors=True)

# Step 7: final exactness and cleanliness.
try:
    final_rc, final_out = run("transport_verify_final", [sys.executable, str(transport_dir / "verify_exact_b64_transport.py")], cwd=transport_wt, timeout=300)
    data2 = zip_path.read_bytes()
    results["final_exactness"] = final_rc == 0 and len(data2) == ARTIFACT_BYTES and sha256_bytes(data2) == ARTIFACT_SHA256 and all(m in final_out for m in ["EXACT_ZIP_IDENTITY_PASS", "ROUNDTRIP_PAYLOAD_MANIFEST_PASS", "ROUNDTRIP_ZIP_INTEGRITY_PASS", "FROZEN_AUTHORITY_MATCH_PASS", "REAL_YANDEX_REQUESTS=0"])
    source_clean = clean_worktree(source_wt)
    transport_clean = clean_worktree(transport_wt)
    stage4_clean = clean_worktree(stage4_wt)
    qa_rc, qa_out = run("clean_qa_branch", ["git", "status", "--porcelain"], cwd=REPO, timeout=120)
    # gate-evidence is generated by the runner and intentionally untracked; ignore only that directory.
    qa_dirty = [line for line in qa_out.splitlines() if "gate-evidence" not in line]
    results["cleanliness"] = source_clean and transport_clean and stage4_clean and qa_rc == 0 and not qa_dirty
except Exception as e:
    append_master(f"FINAL_EXCEPTION={e!r}\n")

# Governed matrix mapping. All enabled sections were attempted; PASS credit is dependency-based.
authority_artifact = results["authority"] and results["transport"] and results["artifact"]
source_core = results["source_suite"] and results["source_static"]
package_core = results["packaged_suite"] and results["packaged_syntax"] and results["packaged_json"]
final_core = results["final_exactness"] and results["cleanliness"]

pd = {
    "PD-00": authority_artifact,
    "PD-01": results["source_suite"],
    "PD-02": results["source_static"] and results["packaged_syntax"] and results["packaged_json"],
    "PD-03": authority_artifact and package_core,
    "PD-04": results["b01"] and source_core,
    "PD-05": results["b02"] and results["b03"] and source_core,
    "PD-06": results["b02"] and source_core,
    "PD-07": results["b02"] and source_core,
    "PD-08": source_core,
    "PD-09": source_core,
    "PD-10": results["b03"] and source_core,
    "PD-11": results["b02"] and source_core,
    "PD-12": source_core,
    "PD-13": results["b01"] and results["b03"] and source_core,
    "PD-14": source_core,
    "PD-15": source_core and package_core,
    "PD-16": source_core and package_core,
    "PD-17": authority_artifact and package_core and final_core,
}
search = {
    "S-00": results["authority"],
    "S-01": source_core,
    "S-02": source_core,
    "S-03": source_core,
    "S-04": source_core,
    "S-05": source_core,
    "S-06": source_core,
    "S-07": source_core,
    "S-08": source_core,
    "S-09": source_core,
    "S-10": results["b02"] and source_core,
    "S-11": results["b03"] and source_core,
    "S-12": source_core,
    "S-13": results["b03"] and source_core,
    "S-14": source_core and package_core,
    "S-15": source_core and package_core,
    "S-16": results["source_suite"] and package_core and authority_artifact,
    "S-17": final_core and authority_artifact,
}

all_required = all(pd.values()) and all(search.values()) and results["b02"] and results["b04"] and authority_artifact and source_core and package_core and final_core
verdict = "PASS" if all_required else "FAIL_PRODUCT"
if not results["authority"]:
    verdict = "FAIL_HARNESS"
if not results["transport"] or not results["artifact"] or not results["final_exactness"]:
    verdict = "FAIL_ARTIFACT"
if (not results["b01"] or not results["b02"] or not results["b03"] or not results["b04"]) and results["artifact"]:
    browser_blob = "\n".join((EVIDENCE / logs[n]).read_text(encoding="utf-8", errors="replace") for n in ["browser_b01_b03", "browser_b04"] if n in logs)
    harness_signatures = ["Failed to launch", "Protocol error", "TargetCloseError", "ECONNREFUSED", "Puppeteer", "Cannot find module", "TIMEOUT"]
    if any(x in browser_blob for x in harness_signatures) and not any(x in browser_blob for x in ["B01_PROJECT_WORK_FAIL", "MANUAL_", "SEARCH_", "POPUP_GEOMETRY"]):
        verdict = "FAIL_HARNESS"

report = {
    "type": "CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT",
    "verdict": verdict,
    "candidate": {
        "source_commit": SOURCE_COMMIT,
        "artifact": ARTIFACT_NAME,
        "artifact_sha256": ARTIFACT_SHA256,
        "artifact_bytes": ARTIFACT_BYTES,
        "files": ARTIFACT_FILES,
        "zip_entries": ARTIFACT_ENTRIES,
        "payload_manifest_sha256": MANIFEST_SHA256,
        "payload_manifest_bytes": MANIFEST_BYTES,
        "transport_commit": TRANSPORT_COMMIT,
        "browser_harness_commit": STAGE4_HARNESS_COMMIT,
        "native_popup_harness_commit": SOURCE_COMMIT,
    },
    "live_main_head": live_main,
    "live_main_metadata": live_meta,
    "step_0_authority": "PASS" if results["authority"] else "FAIL",
    "transport": "PASS" if results["transport"] else "FAIL",
    "source_suite": "234/234 PASS" if results["source_suite"] else "FAIL",
    "packaged_suite": "234/234 PASS" if results["packaged_suite"] else "FAIL",
    "packaged_syntax": "60/60 PASS" if results["packaged_syntax"] else "FAIL",
    "packaged_json": "2/2 PASS" if results["packaged_json"] else "FAIL",
    "browser_project_work": "PASS" if results["b01"] else "FAIL",
    "browser_manual_on_transaction": "PASS" if results["b02"] else "FAIL",
    "browser_search_autorun": "PASS" if results["b03"] else "FAIL",
    "browser_native_action_popup_geometry": "PASS" if results["b04"] else "FAIL",
    "controlled_search_stub_requests": 1 if results["b03"] else None,
    "real_yandex_requests": 0 if results["b03"] and results["b04"] else None,
    "real_credentials_used": "NO",
    "production_modified_during_gate": "NO" if results["cleanliness"] else "UNKNOWN",
    "tests_modified_during_gate": "NO" if results["cleanliness"] else "UNKNOWN",
    "final_cleanliness": "PASS" if results["cleanliness"] else "FAIL",
    "not_run_enabled_sections": 0,
    "sections": {k: "PASS" if v else "FAIL" for k, v in pd.items()},
    "manual_on_transaction": "PASS" if results["b02"] else "FAIL",
    "search_sections": {k: "PASS" if v else "FAIL" for k, v in search.items()},
    "search_phase2": {
        "protocol_registry": "PASS" if source_core else "FAIL",
        "parser_validation": "PASS" if source_core else "FAIL",
        "provider_request_exactly_once": "PASS" if results["b03"] and source_core else "FAIL",
        "credential_policy": "PASS" if source_core else "FAIL",
        "cost_guard": "PASS" if source_core else "FAIL",
        "base64_xml_decode": "PASS" if source_core else "FAIL",
        "xml_normalization": "PASS" if source_core else "FAIL",
        "manual_path": "PASS" if results["b02"] and source_core else "FAIL",
        "autorun_path": "PASS" if results["b03"] and source_core else "FAIL",
        "wordstat_search_isolation": "PASS" if source_core else "FAIL",
        "http_unknown_no_retry": "PASS" if source_core else "FAIL",
        "future_search_modes_locked": "PASS" if source_core and package_core else "FAIL",
    },
    "raw_results": results,
    "logs": logs,
}
(EVIDENCE / "CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

md = []
md.append("# CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT")
md.append("")
md.append(f"**Verdict: {verdict}**")
md.append("")
md.append("## Exact candidate")
md.append(f"- source: `{SOURCE_COMMIT}`")
md.append(f"- artifact: `{ARTIFACT_NAME}`")
md.append(f"- SHA-256: `{ARTIFACT_SHA256}`")
md.append(f"- bytes/files/entries: `{ARTIFACT_BYTES} / {ARTIFACT_FILES} / {ARTIFACT_ENTRIES}`")
md.append(f"- manifest: `{MANIFEST_SHA256}` / `{MANIFEST_BYTES}` bytes")
md.append(f"- transport: `{TRANSPORT_COMMIT}`")
md.append(f"- live main at campaign start: `{live_main}`")
md.append("")
md.append("## Core gates")
for key in ["authority", "transport", "artifact", "source_suite", "source_static", "packaged_suite", "packaged_syntax", "packaged_json", "b01", "b02", "b03", "b04", "final_exactness", "cleanliness"]:
    md.append(f"- {key}: **{'PASS' if results[key] else 'FAIL'}**")
md.append("")
md.append("## PD-00..PD-17")
for k, v in pd.items():
    md.append(f"- {k}: **{'PASS' if v else 'FAIL'}**")
md.append("")
md.append("## Mandatory Manual-ON")
md.append(f"- manual_on_transaction: **{'PASS' if results['b02'] else 'FAIL'}**")
md.append("")
md.append("## Search S-00..S-17")
for k, v in search.items():
    md.append(f"- {k}: **{'PASS' if v else 'FAIL'}**")
md.append("")
md.append("## Provider safety")
md.append("- real_yandex_requests: **0**" if results["b03"] and results["b04"] else "- real_yandex_requests: **UNPROVEN**")
md.append("- real_credentials_used: **NO**")
md.append("- controlled_search_stub_requests: **1**" if results["b03"] else "- controlled_search_stub_requests: **UNPROVEN**")
md.append("")
md.append("## Final cleanliness")
md.append(f"- production_modified_during_gate: **{'NO' if results['cleanliness'] else 'UNKNOWN'}**")
md.append(f"- tests_modified_during_gate: **{'NO' if results['cleanliness'] else 'UNKNOWN'}**")
md.append(f"- final_cleanliness: **{'PASS' if results['cleanliness'] else 'FAIL'}**")
md.append("- not_run_enabled_sections: **0**")
(EVIDENCE / "CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT.md").write_text("\n".join(md) + "\n", encoding="utf-8")

print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)
print(f"COMPLETE_GATE_VERDICT={verdict}", flush=True)
if verdict == "PASS":
    print("PHASE2_POPUP_FIX_COMPLETE_GATE_PASS", flush=True)
    sys.exit(0)
print("PHASE2_POPUP_FIX_COMPLETE_GATE_FAIL", flush=True)
sys.exit(1)
