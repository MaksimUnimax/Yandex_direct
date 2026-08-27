#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
EXPECTED_SOURCE = "34f50688268970f4863dddb2089a33d891b91372"
EXPECTED_TREE = "adab628a8ec328fa5079ae35f45005a0ee7de2c1"
EXPECTED_FREEZE_TRIGGER = "a837baac899d0e945a015f7a1980c6a13d874f88"
EXPECTED_FREEZE_RUN = 33078753960
EXPECTED_ARTIFACT_ID = 9649039904
EXPECTED_ARTIFACT_NAME = "phase6-wordstat-batch-frozen-candidate-34f5068"
EXPECTED_WRAPPER_SHA = "bcc33634c1673170c71e979f9e1412c944d372ebd7e351b5a3b31c973762f478"
EXPECTED_ZIP_SHA = "05d587b02f5fc08c64ebbf1fbd5d14765491c7b9931195c23262e1f42d692c2f"
EXPECTED_ZIP_BYTES = 133127
EXPECTED_FILES = 47
EXPECTED_TESTS = 81
EXPECTED_SYNTAX = 41
EXPECTED_JSON = 2
ZIP_NAME = "yandex-marketing-bridge-0.1.1-phase6-wordstat-batch-first-slice-candidate.zip"
MANIFEST_NAME = "PHASE6_WORDSTAT_BATCH_EXACT_CANDIDATE_MANIFEST_2026-08-27.json"

FOCUSED_TESTS = [
    "extension/tests/provider_batch_job_model.test.mjs",
    "extension/tests/wordstat_batch_durability_safety.test.mjs",
    "extension/tests/wordstat_batch_policy_guard.test.mjs",
    "extension/tests/wordstat_batch_protocol.test.mjs",
    "extension/tests/wordstat_batch_runtime.test.mjs",
    "extension/tests/wordstat_batch_transport.test.mjs",
    "extension/tests/wordstat_batch_worker_adapter.test.mjs",
    "extension/tests/wordstat_batch_worker_lifecycle.test.mjs",
]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def exe(name: str) -> str:
    found = shutil.which(name)
    if found:
        return found
    return name


def run(cmd, cwd=REPO, capture=False, check=True, env=None):
    argv = [str(x) for x in cmd]
    print("+ " + " ".join(argv), flush=True)
    kwargs = dict(cwd=cwd, env=env, text=True, check=False)
    if capture:
        kwargs.update(stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cp = subprocess.run(argv, **kwargs)
    if capture:
        print(cp.stdout or "", end="", flush=True)
    if check and cp.returncode != 0:
        raise RuntimeError(f"command failed rc={cp.returncode}: {' '.join(argv)}")
    return cp


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(root: Path):
    if not root.exists():
        return {}
    rows = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rows[path.relative_to(root).as_posix()] = (path.stat().st_size, sha256_file(path))
    return rows


def parse_tap_counts(text: str):
    def last(name):
        patterns = [rf"^#\s*{name}\s+(\d+)\s*$", rf"^ℹ\s*{name}\s+(\d+)\s*$"]
        values = []
        for pattern in patterns:
            values.extend(re.findall(pattern, text, flags=re.M | re.I))
        return int(values[-1]) if values else None
    tests, passed, failed = last("tests"), last("pass"), last("fail")
    return None if None in (tests, passed, failed) else (passed, tests, failed)


def node_suite(root: Path, label: str, expected=None):
    tests = sorted((root / "extension" / "tests").glob("*.test.mjs"), key=lambda p: p.as_posix())
    require(tests, f"{label}: no top-level tests")
    rels = [p.relative_to(root).as_posix() for p in tests]
    cp = run([exe("node"), "--test", "--test-reporter=tap", *rels], cwd=root, capture=True)
    counts = parse_tap_counts(cp.stdout or "")
    require(counts is not None, f"{label}: TAP counts unavailable")
    passed, total, failed = counts
    require(failed == 0 and passed == total, f"{label}: {passed}/{total}, fail={failed}")
    if expected is not None:
        require(total == expected, f"{label}: expected {expected} tests, got {total}")
    print(f"{label.upper()}={passed}/{total}")
    return passed, total


def focused_suite(root: Path, label: str):
    for rel in FOCUSED_TESTS:
        require((root / rel).exists(), f"{label}: missing {rel}")
    cp = run([exe("node"), "--test", "--test-reporter=tap", *FOCUSED_TESTS], cwd=root, capture=True)
    counts = parse_tap_counts(cp.stdout or "")
    require(counts is not None, f"{label}: TAP counts unavailable")
    passed, total, failed = counts
    require(failed == 0 and passed == total, f"{label}: {passed}/{total}, fail={failed}")
    print(f"{label.upper()}={passed}/{total}")
    return passed, total


def syntax_json(root: Path, label: str):
    src = root / "extension" / "src"
    js = sorted([p for p in src.rglob("*") if p.is_file() and p.suffix in {".js", ".mjs"}], key=lambda p: p.as_posix())
    for path in js:
        run([exe("node"), "--check", str(path)], cwd=root, capture=True)
    json_files = sorted(src.rglob("*.json"), key=lambda p: p.as_posix())
    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))
    require(len(js) == EXPECTED_SYNTAX, f"{label}: syntax count {len(js)} != {EXPECTED_SYNTAX}")
    require(len(json_files) == EXPECTED_JSON, f"{label}: JSON count {len(json_files)} != {EXPECTED_JSON}")
    print(f"{label.upper()}_SYNTAX={len(js)}/{len(js)}")
    print(f"{label.upper()}_JSON={len(json_files)}/{len(json_files)}")


def verify_transport(transport: Path, extract_to: Path):
    zip_path = transport / ZIP_NAME
    manifest_path = transport / MANIFEST_NAME
    require(zip_path.exists(), f"missing inner ZIP: {zip_path}")
    require(manifest_path.exists(), f"missing manifest: {manifest_path}")
    require(zip_path.stat().st_size == EXPECTED_ZIP_BYTES, "inner ZIP byte count mismatch")
    require(sha256_file(zip_path) == EXPECTED_ZIP_SHA, "inner ZIP SHA-256 mismatch")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = {
        "schema": "PHASE6_WORDSTAT_BATCH_EXACT_CANDIDATE_V1",
        "source_commit": EXPECTED_SOURCE,
        "product_tree": EXPECTED_TREE,
        "preflight_run_id": 33078276993,
        "freeze_run_id": EXPECTED_FREEZE_RUN,
        "freeze_trigger_commit": EXPECTED_FREEZE_TRIGGER,
        "artifact_name": EXPECTED_ARTIFACT_NAME,
        "zip_name": ZIP_NAME,
        "sha256": EXPECTED_ZIP_SHA,
        "bytes": EXPECTED_ZIP_BYTES,
        "files": EXPECTED_FILES,
        "zip_test": "PASS",
        "deterministic_rebuild": "BYTE_IDENTICAL",
        "real_yandex_requests": 0,
        "real_credentials_used": "NO",
    }
    for key, value in expected.items():
        require(manifest.get(key) == value, f"manifest {key} mismatch: {manifest.get(key)!r}")
    entries = manifest.get("entries") or []
    require(len(entries) == EXPECTED_FILES, "manifest entry count mismatch")
    if extract_to.exists():
        shutil.rmtree(extract_to)
    extract_to.mkdir(parents=True)
    expected_paths = [row["path"] for row in entries]
    with zipfile.ZipFile(zip_path) as zf:
        require(zf.testzip() is None, "inner ZIP integrity failure")
        require(zf.namelist() == expected_paths, "inner ZIP path/order mismatch")
        zf.extractall(extract_to)
    actual_paths = sorted(p.relative_to(extract_to).as_posix() for p in extract_to.rglob("*") if p.is_file())
    require(actual_paths == sorted(expected_paths), "extracted path set mismatch")
    for row in entries:
        path = extract_to / row["path"]
        require(path.stat().st_size == row["bytes"], f"byte mismatch: {row['path']}")
        require(sha256_file(path) == row["sha256"], f"hash mismatch: {row['path']}")
    print("PHASE6_ARTIFACT_TRANSPORT_ROUNDTRIP_PASS")
    return manifest


def browser_cmd(script: Path):
    base = [exe("node"), str(script)]
    if os.name != "nt" and not os.environ.get("DISPLAY"):
        xvfb = shutil.which("xvfb-run")
        require(xvfb is not None, "browser gate requires DISPLAY or xvfb-run")
        return [xvfb, "-a", *base]
    return base


def browser_gate(root: Path, rel: str, markers, label: str):
    script = root / rel
    require(script.exists(), f"missing browser harness: {rel}")
    cp = run(browser_cmd(script), cwd=root, capture=True)
    out = cp.stdout or ""
    for marker in markers:
        require(marker in out, f"{label}: missing marker {marker}")
    print(f"{label}=PASS")
    return out


def git_clean(root: Path, label: str):
    cp = run([exe("git"), "status", "--porcelain", "--untracked-files=all"], cwd=root, capture=True)
    require(not (cp.stdout or "").strip(), f"{label} not clean:\n{cp.stdout}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport-dir", required=True)
    parser.add_argument("--wrapper", default=None)
    args = parser.parse_args()
    transport = Path(args.transport_dir).resolve()
    wrapper = Path(args.wrapper).resolve() if args.wrapper else None

    run([exe("node"), "--version"], capture=True)
    run([exe("git"), "rev-parse", "--show-toplevel"], capture=True)
    git_clean(REPO, "QA workspace at start")

    if wrapper:
        require(wrapper.exists(), "artifact wrapper missing")
        require(sha256_file(wrapper) == EXPECTED_WRAPPER_SHA, "GitHub artifact wrapper digest mismatch")
        print("PHASE6_ARTIFACT_WRAPPER_DIGEST_PASS")

    qa_product_before = snapshot(REPO / "extension" / "src")
    qa_tests_before = snapshot(REPO / "extension" / "tests")
    current_tree = run([exe("git"), "rev-parse", "HEAD:extension/src"], capture=True).stdout.strip()
    source_tree = run([exe("git"), "rev-parse", f"{EXPECTED_SOURCE}:extension/src"], capture=True).stdout.strip()
    require(current_tree == EXPECTED_TREE, f"QA product tree mismatch: {current_tree}")
    require(source_tree == EXPECTED_TREE, f"source product tree mismatch: {source_tree}")
    print("P6_STEP0_AUTHORITY_PASS")

    work = Path(tempfile.mkdtemp(prefix="ymb-phase6-independent-"))
    source_wt = work / "source"
    package_wt = work / "package"
    extract_to = work / "extracted"
    source_added = False
    package_added = False
    try:
        run([exe("git"), "worktree", "add", "--detach", str(source_wt), EXPECTED_SOURCE])
        source_added = True
        run([exe("git"), "worktree", "add", "--detach", str(package_wt), EXPECTED_SOURCE])
        package_added = True

        source_product_before = snapshot(source_wt / "extension" / "src")
        source_tests_before = snapshot(source_wt / "extension" / "tests")
        node_suite(source_wt, "source_suite", EXPECTED_TESTS)
        focused_suite(source_wt, "source_phase6_focused")
        syntax_json(source_wt, "source")
        require(snapshot(source_wt / "extension" / "src") == source_product_before, "source product mutated by tests")
        require(snapshot(source_wt / "extension" / "tests") == source_tests_before, "source tests mutated by tests")
        git_clean(source_wt, "source worktree")

        manifest = verify_transport(transport, extract_to)
        expected_snapshot = {row["path"]: (row["bytes"], row["sha256"]) for row in manifest["entries"]}
        require(snapshot(source_wt / "extension" / "src") == expected_snapshot, "frozen artifact differs from exact source bytes")
        print("PHASE6_SOURCE_ARTIFACT_BYTE_IDENTITY_PASS")

        packaged_src = package_wt / "extension" / "src"
        shutil.rmtree(packaged_src)
        shutil.copytree(extract_to, packaged_src)
        require(snapshot(packaged_src) == expected_snapshot, "staged packaged bytes differ from manifest")
        diff = run([exe("git"), "diff", "--exit-code", "--", "extension/src"], cwd=package_wt, capture=True, check=False)
        require(diff.returncode == 0, "packaged product differs from frozen source in Git")
        packaged_product_before = snapshot(packaged_src)
        packaged_tests_before = snapshot(package_wt / "extension" / "tests")

        node_suite(package_wt, "packaged_suite", EXPECTED_TESTS)
        focused_suite(package_wt, "packaged_phase6_focused")
        syntax_json(package_wt, "packaged")
        require(snapshot(packaged_src) == packaged_product_before, "packaged product mutated by Node tests")
        require(snapshot(package_wt / "extension" / "tests") == packaged_tests_before, "packaged tests mutated by Node tests")

        node_modules = package_wt / "node_modules"
        require(not node_modules.exists(), "unexpected pre-existing node_modules in package worktree")
        run([exe("npm"), "install", "--no-save", "--package-lock=false", "puppeteer@24"], cwd=package_wt, capture=True)
        run([exe("npx"), "puppeteer", "browsers", "install", "chrome"], cwd=package_wt, capture=True)

        outputs = []
        outputs.append(browser_gate(package_wt, "extension/tests/qa_browser/direct_popup_d18.mjs", [
            "D18_POPUP_430X560_PASS",
            "D18_TOP_BOTTOM_COMMON_SAVE_EQUIVALENT_PASS",
            "PHASE5_DIRECT_POPUP_D18_PASS",
        ], "BROWSER_DIRECT_POPUP_D18"))
        outputs.append(browser_gate(package_wt, "extension/tests/qa_browser/direct_manual_worker_lifecycle.mjs", [
            "D17_DIRECT_MANUAL_LIST_AUTOSEND_FALSE_PASS",
            "D17_DIRECT_MANUAL_REPORT_AUTOSEND_TRUE_PASS",
            "D17_DIRECT_REMOUNT_NO_REPLAY_PASS",
            "D17_DIRECT_NO_DUPLICATE_PROVIDER_PASS",
            "D20_DIRECT_LIFECYCLE_REAL_YANDEX_REQUESTS=0",
            "PHASE5_DIRECT_MANUAL_LIFECYCLE_PASS",
        ], "BROWSER_DIRECT_MANUAL_LIFECYCLE"))
        outputs.append(browser_gate(package_wt, "extension/tests/qa_browser/direct_codex_gate_addendum_v2.mjs", [
            "D19_FIVE_SERVICE_BACKUP_UI_MAPPING_PASS",
            "D17_MANUAL_BUSY_FENCE_SINGLE_PROVIDER_PASS",
            "D16_NON_DIRECT_ACTIVE_DIRECT_PREFIX_ZERO_TRAFFIC_PASS",
            "D20_DIRECT_AUTORUN_DEFAULT_DISABLED_LOCAL_PASS",
            "D16_DIRECT_ACTIVE_OTHER_PREFIXES_ZERO_TRAFFIC_PASS",
            "D20_DIRECT_AUTORUN_ONE_FINGERPRINT_ONE_PROVIDER_ONE_DELIVERY_PASS",
            "D20_DIRECT_AUTORUN_PAUSE_RESUME_FINISH_PASS",
            "DIRECT_REAL_YANDEX_REQUESTS=0",
            "PHASE5_DIRECT_CODEX_BROWSER_ADDENDUM_PASS",
        ], "BROWSER_DIRECT_ADDENDUM"))
        outputs.append(browser_gate(package_wt, "extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_compat_gate.mjs", [
            "B01_PROJECT_WORK_IDENTITY_PASS",
            "B01_BINDING_PASS",
            "B02_MANUAL_RESYNC_SINGLE_ACTION_PASS",
            "B02_MANUAL_REMOUNT_NO_REPLAY_PASS",
            "B02_MANUAL_ON_OFF_TRANSACTION_PASS",
            "B03_NON_OWNER_CONTROL_FENCE_PASS",
            "B03_SEARCH_AUTORUN_PASS",
            "BROWSER_GATE_REAL_YANDEX_REQUESTS=0",
            "PHASE2_STAGE4_COMPAT_BROWSER_GATE_PASS",
        ], "BROWSER_PRIOR_PHASE_COMPATIBILITY"))

        combined = "\n".join(outputs)
        require("REAL_YANDEX_REQUESTS=1" not in combined, "browser harness reported a real Yandex request")
        require("DIRECT_REAL_YANDEX_REQUESTS=0" in combined, "Direct zero-real-request marker missing")
        require("BROWSER_GATE_REAL_YANDEX_REQUESTS=0" in combined, "compat zero-real-request marker missing")

        shutil.rmtree(node_modules, ignore_errors=True)
        require(snapshot(packaged_src) == packaged_product_before, "packaged product mutated by browser tests")
        require(snapshot(package_wt / "extension" / "tests") == packaged_tests_before, "packaged tests/harness mutated by browser tests")
        git_clean(package_wt, "packaged worktree")

        require(snapshot(REPO / "extension" / "src") == qa_product_before, "QA branch product bytes mutated")
        require(snapshot(REPO / "extension" / "tests") == qa_tests_before, "QA tests/harness mutated")
        git_clean(REPO, "QA workspace at final audit")

        print(f"artifact_id={EXPECTED_ARTIFACT_ID}")
        print(f"artifact_wrapper_sha256={EXPECTED_WRAPPER_SHA}")
        print(f"inner_zip_sha256={EXPECTED_ZIP_SHA}")
        print(f"inner_zip_bytes={EXPECTED_ZIP_BYTES}")
        print(f"product_files={EXPECTED_FILES}")
        print("real_credentials_used=NO")
        print("real_yandex_requests=0")
        print("enabled_not_run_sections=0")
        print("NOT_RUN_COUNT=0")
        print("PRODUCT_BYTES_POST_TEST=IDENTICAL")
        print("PHASE6_WORDSTAT_BATCH_INDEPENDENT_RUNNER_PASS")
    finally:
        if package_added:
            subprocess.run([exe("git"), "worktree", "remove", "--force", str(package_wt)], cwd=REPO,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if source_added:
            subprocess.run([exe("git"), "worktree", "remove", "--force", str(source_wt)], cwd=REPO,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"PHASE6_WORDSTAT_BATCH_INDEPENDENT_RUNNER_FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
