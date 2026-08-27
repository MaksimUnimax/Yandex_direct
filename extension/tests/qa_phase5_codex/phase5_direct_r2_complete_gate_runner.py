#!/usr/bin/env python3
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
EXPECTED_SOURCE = "841a1e2c1a503c4a05572a957ba97c55b9b60c52"
EXPECTED_TREE = "edf1c2d3494ebbc53ae778d23be1457eb885b605"
EXPECTED_ZIP_SHA = "ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b"
EXPECTED_ZIP_BYTES = 406656
EXPECTED_FILES = 39
FREEZE_RUN = "33037955943"
ARTIFACT_NAME = "phase5-direct-r2-frozen-candidate-841a1e2"
ZIP_NAME = "yandex-marketing-bridge-0.1.1-phase5-direct-first-slice-r2-candidate.zip"
MANIFEST_NAME = "PHASE5_DIRECT_R2_EXACT_CANDIDATE_MANIFEST_2026-08-27.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(root: Path):
    rows = {}
    if not root.exists():
        return rows
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        rel = p.relative_to(root).as_posix()
        rows[rel] = (p.stat().st_size, sha256_file(p))
    return rows


def exe(name: str) -> str:
    found = shutil.which(name)
    if found:
        return found
    if os.name == "nt":
        found = shutil.which(name + ".cmd") or shutil.which(name + ".exe")
        if found:
            return found
    return name


def run(cmd, cwd=REPO, env=None, capture=False, check=True):
    printable = " ".join(str(x) for x in cmd)
    print(f"+ {printable}", flush=True)
    if capture:
        cp = subprocess.run(cmd, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, check=False)
        print(cp.stdout, end="", flush=True)
    else:
        cp = subprocess.run(cmd, cwd=cwd, env=env, text=True, check=False)
    if check and cp.returncode != 0:
        raise RuntimeError(f"command failed rc={cp.returncode}: {printable}")
    return cp


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def parse_tap_counts(text: str):
    tests = re.findall(r"^# tests (\d+)\s*$", text, flags=re.M)
    passed = re.findall(r"^# pass (\d+)\s*$", text, flags=re.M)
    failed = re.findall(r"^# fail (\d+)\s*$", text, flags=re.M)
    if not tests or not passed or not failed:
        return None
    return int(passed[-1]), int(tests[-1]), int(failed[-1])


def node_suite(root: Path, label: str):
    tests = sorted((root / "extension" / "tests").glob("*.test.mjs"))
    require(tests, f"{label}: no top-level tests found")
    rels = [str(p.relative_to(root)) for p in tests]
    cp = run([exe("node"), "--test", *rels], cwd=root, capture=True)
    counts = parse_tap_counts(cp.stdout)
    require(counts is not None, f"{label}: unable to parse TAP counts")
    passed, total, failed = counts
    require(failed == 0 and passed == total, f"{label}: {passed}/{total}, fail={failed}")
    print(f"{label.upper()}={passed}/{total}")
    return passed, total, cp.stdout


def syntax_json(root: Path, label: str):
    src = root / "extension" / "src"
    js_files = sorted([p for p in src.rglob("*") if p.is_file() and p.suffix in {".js", ".mjs"}])
    for p in js_files:
        run([exe("node"), "--check", str(p)], cwd=root, capture=True)
    json_files = sorted([p for p in src.rglob("*.json") if p.is_file()])
    for p in json_files:
        json.loads(p.read_text(encoding="utf-8"))
    require((src / "manifest.json").exists(), f"{label}: manifest missing")
    manifest = json.loads((src / "manifest.json").read_text(encoding="utf-8"))
    require(manifest.get("manifest_version") == 3, f"{label}: MV3 manifest expected")
    print(f"{label.upper()}_SYNTAX={len(js_files)}/{len(js_files)}")
    print(f"{label.upper()}_JSON={len(json_files)}/{len(json_files)}")
    return len(js_files), len(json_files)


def acquire_transport(target: Path):
    target.mkdir(parents=True, exist_ok=True)
    zip_path = target / ZIP_NAME
    manifest_path = target / MANIFEST_NAME
    if zip_path.exists() and manifest_path.exists():
        return zip_path, manifest_path
    gh = exe("gh")
    run([gh, "run", "download", FREEZE_RUN,
         "--repo", "MaksimUnimax/Yandex_direct",
         "--name", ARTIFACT_NAME,
         "--dir", str(target)], cwd=REPO)
    require(zip_path.exists() and manifest_path.exists(), "artifact download did not materialize expected files")
    return zip_path, manifest_path


def verify_transport(zip_path: Path, manifest_path: Path, extract_to: Path):
    require(zip_path.stat().st_size == EXPECTED_ZIP_BYTES, "inner ZIP byte count mismatch")
    require(sha256_file(zip_path) == EXPECTED_ZIP_SHA, "inner ZIP SHA-256 mismatch")
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(m.get("source_commit") == EXPECTED_SOURCE, "manifest source_commit mismatch")
    require(m.get("product_tree") == EXPECTED_TREE, "manifest product_tree mismatch")
    require(m.get("preflight_run_id") == 33037727189, "manifest preflight_run_id mismatch")
    require(m.get("sha256") == EXPECTED_ZIP_SHA, "manifest SHA mismatch")
    require(m.get("bytes") == EXPECTED_ZIP_BYTES, "manifest bytes mismatch")
    require(m.get("files") == EXPECTED_FILES, "manifest files mismatch")
    require(m.get("zip_test") == "PASS", "manifest zip_test mismatch")
    require(m.get("real_yandex_requests") == 0, "manifest real_yandex_requests mismatch")
    if extract_to.exists():
        shutil.rmtree(extract_to)
    extract_to.mkdir(parents=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        require(zf.testzip() is None, "ZIP integrity failure")
        require(zf.namelist() == [row["path"] for row in m["entries"]], "ZIP entry order/path mismatch")
        zf.extractall(extract_to)
    actual = sorted(p for p in extract_to.rglob("*") if p.is_file())
    expected_paths = [row["path"] for row in m["entries"]]
    require([p.relative_to(extract_to).as_posix() for p in actual] == expected_paths, "extracted path set mismatch")
    for row in m["entries"]:
        p = extract_to / row["path"]
        data = p.read_bytes()
        require(len(data) == row["bytes"], f"byte mismatch: {row['path']}")
        require(sha256_bytes(data) == row["sha256"], f"hash mismatch: {row['path']}")
    print("D00_ARTIFACT_TRANSPORT_ROUNDTRIP_PASS")
    return m


def browser_cmd(script: Path):
    base = [exe("node"), str(script)]
    if os.name != "nt" and not os.environ.get("DISPLAY"):
        xvfb = shutil.which("xvfb-run")
        require(xvfb is not None, "Linux headful browser gate requires DISPLAY or xvfb-run")
        return [xvfb, "-a", *base]
    return base


def run_browser(script_rel: str, markers, label: str):
    script = REPO / script_rel
    require(script.exists(), f"missing browser harness: {script_rel}")
    cp = run(browser_cmd(script), cwd=REPO, capture=True)
    for marker in markers:
        require(marker in cp.stdout, f"{label}: missing marker {marker}")
    print(f"{label}=PASS")
    return cp.stdout


def git_status_clean(root: Path, label: str):
    cp = run([exe("git"), "status", "--porcelain"], cwd=root, capture=True)
    require(cp.stdout.strip() == "", f"{label} not clean:\n{cp.stdout}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transport-dir", default=None,
                    help="Existing directory containing the exact Actions artifact contents; if omitted, gh run download is used")
    args = ap.parse_args()

    os.chdir(REPO)
    node = exe("node")
    npm = exe("npm")
    npx = exe("npx")
    run([node, "--version"], capture=True)
    run([exe("git"), "rev-parse", "--show-toplevel"], capture=True)

    # Runner must execute from a clean committed QA workspace.
    git_status_clean(REPO, "QA workspace at start")
    tests_before = snapshot(REPO / "extension" / "tests")
    harness_before = snapshot(REPO / "extension" / "tests" / "qa_browser")

    tree = run([exe("git"), "rev-parse", f"{EXPECTED_SOURCE}:extension/src"], capture=True).stdout.strip()
    require(tree == EXPECTED_TREE, f"source product tree mismatch: {tree}")
    print("STEP0_AUTHORITY_PASS")

    work = Path(tempfile.mkdtemp(prefix="ymb-phase5-codex-r2-"))
    source_wt = work / "source"
    transport_dir = Path(args.transport_dir).resolve() if args.transport_dir else (work / "transport")
    source_added = False
    node_modules = REPO / "node_modules"
    node_modules_preexisted = node_modules.exists()
    try:
        # Independent exact source suite.
        run([exe("git"), "worktree", "add", "--detach", str(source_wt), EXPECTED_SOURCE])
        source_added = True
        source_pass, source_total, _ = node_suite(source_wt, "source_suite")
        source_syntax, source_json = syntax_json(source_wt, "source")
        focused = run([node, "--test", "extension/tests/credential_runtime_concurrency.test.mjs"], cwd=source_wt, capture=True)
        for text in [
            "stale migration cannot erase a concurrent Direct credential save",
            "concurrent Direct and Metrika saves preserve both independent records",
            "backup runtime participates in the same credential mutation lock",
        ]:
            require(text in focused.stdout, f"missing concurrency assertion: {text}")
        print("CREDENTIAL_CONCURRENCY_REGRESSION=PASS")
        git_status_clean(source_wt, "exact source worktree")

        # Independent exact artifact acquisition and verification.
        zip_path, manifest_path = acquire_transport(transport_dir)
        transport_before = snapshot(transport_dir)
        extracted = work / "exact-extracted"
        manifest = verify_transport(zip_path, manifest_path, extracted)
        print("TRANSPORT=PASS")

        # Stage the exact transported package as extension/src in the immutable QA harness workspace.
        src = REPO / "extension" / "src"
        if src.exists():
            shutil.rmtree(src)
        shutil.copytree(extracted, src)
        actual = snapshot(src)
        expected = {row["path"]: (row["bytes"], row["sha256"]) for row in manifest["entries"]}
        require(actual == expected, "staged packaged product differs from manifest")
        run([exe("git"), "diff", "--exit-code", "--", "extension/src"], capture=True)
        product_before = snapshot(src)
        print("FROZEN_PRODUCT_INSTALLED_EXACTLY_PASS")

        packaged_pass, packaged_total, full_node = node_suite(REPO, "packaged_suite")
        packaged_syntax, packaged_json = syntax_json(REPO, "packaged")
        direct_add = run([node, "--test", "extension/tests/qa_phase5_codex/direct_addendum_coverage.test.mjs"], capture=True)
        concurrency = run([node, "--test", "extension/tests/credential_runtime_concurrency.test.mjs"], capture=True)
        combined = full_node + "\n" + direct_add.stdout + "\n" + concurrency.stdout
        for gate in ["D-01","D-02","D-03","D-04","D-05","D-06","D-07","D-08","D-09","D-10","D-11","D-12","D-13","D-14","D-15","D-16","D-17","D-21"]:
            require(gate in combined, f"packaged Node evidence missing {gate}")
        for text in [
            "stale migration cannot erase a concurrent Direct credential save",
            "concurrent Direct and Metrika saves preserve both independent records",
            "backup runtime participates in the same credential mutation lock",
        ]:
            require(text in concurrency.stdout, f"packaged concurrency evidence missing: {text}")
        print("FROZEN_NODE_D01_D17_D21_PASS")

        # Install only external browser driver dependency; no tracked package state.
        run([npm, "install", "--no-save", "--package-lock=false", "puppeteer@24"], capture=True)
        run([npx, "puppeteer", "browsers", "install", "chrome"], capture=True)

        d18 = run_browser(
            "extension/tests/qa_browser/direct_popup_d18.mjs",
            ["D18_POPUP_430X560_PASS", "D18_TOP_BOTTOM_COMMON_SAVE_EQUIVALENT_PASS", "PHASE5_DIRECT_POPUP_D18_PASS"],
            "BROWSER_DIRECT_POPUP_D18")
        manual = run_browser(
            "extension/tests/qa_browser/direct_manual_worker_lifecycle.mjs",
            ["D17_DIRECT_MANUAL_LIST_AUTOSEND_FALSE_PASS", "D17_DIRECT_MANUAL_REPORT_AUTOSEND_TRUE_PASS",
             "D17_DIRECT_REMOUNT_NO_REPLAY_PASS", "D17_DIRECT_NO_DUPLICATE_PROVIDER_PASS",
             "D20_DIRECT_LIFECYCLE_REAL_YANDEX_REQUESTS=0", "PHASE5_DIRECT_MANUAL_LIFECYCLE_PASS"],
            "BROWSER_DIRECT_MANUAL_LIFECYCLE")
        addendum = run_browser(
            "extension/tests/qa_browser/direct_codex_gate_addendum_v2.mjs",
            ["D19_FIVE_SERVICE_BACKUP_UI_MAPPING_PASS", "D17_MANUAL_BUSY_FENCE_SINGLE_PROVIDER_PASS",
             "D16_NON_DIRECT_ACTIVE_DIRECT_PREFIX_ZERO_TRAFFIC_PASS", "D20_DIRECT_AUTORUN_DEFAULT_DISABLED_LOCAL_PASS",
             "D16_DIRECT_ACTIVE_OTHER_PREFIXES_ZERO_TRAFFIC_PASS",
             "D20_DIRECT_AUTORUN_ONE_FINGERPRINT_ONE_PROVIDER_ONE_DELIVERY_PASS",
             "D20_DIRECT_AUTORUN_PAUSE_RESUME_FINISH_PASS", "DIRECT_REAL_YANDEX_REQUESTS=0",
             "PHASE5_DIRECT_CODEX_BROWSER_ADDENDUM_PASS"],
            "BROWSER_DIRECT_ADDENDUM")
        compat = run_browser(
            "extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_compat_gate.mjs",
            ["B01_PROJECT_WORK_IDENTITY_PASS", "B01_BINDING_PASS", "B02_MANUAL_RESYNC_SINGLE_ACTION_PASS",
             "B02_MANUAL_REMOUNT_NO_REPLAY_PASS", "B02_MANUAL_ON_OFF_TRANSACTION_PASS",
             "B03_NON_OWNER_CONTROL_FENCE_PASS", "B03_SEARCH_AUTORUN_PASS",
             "BROWSER_GATE_REAL_YANDEX_REQUESTS=0", "PHASE2_STAGE4_COMPAT_BROWSER_GATE_PASS"],
            "BROWSER_PRIOR_PHASE_COMPATIBILITY")

        m = re.search(r"DIRECT_CONTROLLED_PROVIDER_REQUESTS=(\d+)", addendum)
        require(m is not None, "Direct controlled provider request count missing")
        direct_requests = int(m.group(1))
        require(direct_requests == 2, f"unexpected Direct controlled provider request count: {direct_requests}")
        m = re.search(r"BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=(\d+)", compat)
        require(m is not None, "Search controlled stub request count missing")
        search_requests = int(m.group(1))
        require(search_requests == 1, f"unexpected Search controlled request count: {search_requests}")

        # Clean npm-only untracked runtime dependency before final immutability audit.
        if node_modules.exists() and not node_modules_preexisted:
            shutil.rmtree(node_modules)

        require(snapshot(src) == product_before, "PRODUCT_BYTES_POST_TEST changed")
        require(snapshot(REPO / "extension" / "tests") == tests_before, "package tests changed during gate")
        require(snapshot(REPO / "extension" / "tests" / "qa_browser") == harness_before, "browser harness changed during gate")
        require(snapshot(transport_dir) == transport_before, "transport bytes changed during gate")
        require(sha256_file(zip_path) == EXPECTED_ZIP_SHA and zip_path.stat().st_size == EXPECTED_ZIP_BYTES,
                "final artifact identity mismatch")
        run([exe("git"), "diff", "--exit-code", "--", "extension/src", "extension/tests"], capture=True)
        git_status_clean(REPO, "QA workspace at final audit")

        print("D-22: PASS")
        print("PRODUCT_BYTES_POST_TEST=IDENTICAL")
        print("production_modified_during_gate=NO")
        print("package_tests_modified_during_gate=NO")
        print("direct_harness_modified_during_gate=NO")
        print("compatibility_harness_modified_during_gate=NO")
        print("source_workspace_clean=PASS")
        print("transport_workspace_clean=PASS")
        print("browser_harness_workspaces_clean=PASS")
        print("real_credentials_used=NO")
        print("real_yandex_direct_requests=0")
        print("real_yandex_requests=0")
        print("enabled_not_run_sections=0")
        print("NOT_RUN_COUNT=0")
        print(f"direct_controlled_provider_requests={direct_requests}")
        print(f"controlled_search_stub_requests={search_requests}")
        print(f"source_suite={source_pass}/{source_total}")
        print(f"packaged_suite={packaged_pass}/{packaged_total}")
        print(f"source_syntax={source_syntax}/{source_syntax}")
        print(f"packaged_syntax={packaged_syntax}/{packaged_syntax}")
        print(f"source_json={source_json}/{source_json}")
        print(f"packaged_json={packaged_json}/{packaged_json}")
        for n in range(23):
            print(f"D-{n:02d}: PASS")
        print("PHASE5_DIRECT_R2_INDEPENDENT_RUNNER_PASS")
    finally:
        if node_modules.exists() and not node_modules_preexisted:
            shutil.rmtree(node_modules, ignore_errors=True)
        if source_added:
            subprocess.run([exe("git"), "worktree", "remove", "--force", str(source_wt)], cwd=REPO,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"PHASE5_DIRECT_R2_INDEPENDENT_RUNNER_FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
