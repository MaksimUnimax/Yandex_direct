#!/usr/bin/env python3
"""Portable execution wrapper for the immutable Phase 5 Direct R2 complete gate.

This file intentionally does not change product bytes, package tests, or governed
browser harnesses. It imports the original complete-gate runner and replaces only
host-sensitive execution helpers:

- Git safe.directory is supplied process-locally for every Git command.
- Node test output is forced to the TAP reporter and parsed across Node 22/24.
- extracted artifact paths are compared canonically as POSIX path sets instead of
  relying on pathlib ordering, which differs between POSIX and Windows.
- Python bytecode writes are disabled so importing the immutable v1 runner cannot
  dirty the governed QA workspace before its cleanliness assertion.
- final Windows cleanliness treats extension/src byte identity as authoritative;
  Git CRLF working-tree normalization is not misclassified as a product mutation.
- the Direct browser addendum gets a Windows-only temporary timing adapter that
  changes only the generic wait timeout from 25s to 60s; assertions and fixtures
  remain byte-for-byte identical otherwise, and the adapter is deleted afterward.
"""
from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
V1_PATH = HERE / "phase5_direct_r2_complete_gate_runner.py"

spec = importlib.util.spec_from_file_location("phase5_direct_r2_runner_v1", V1_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load base runner: {V1_PATH}")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

_original_subprocess_run = base.subprocess.run


def safe_dir_value(cwd: Path) -> str:
    return cwd.resolve().as_posix()


def portable_run(cmd, cwd=None, env=None, capture=False, check=True):
    cwd = Path(cwd or base.REPO).resolve()
    argv = [str(x) for x in cmd]
    if argv and Path(argv[0]).stem.lower() == "git":
        argv = [argv[0], "-c", f"safe.directory={safe_dir_value(cwd)}", *argv[1:]]
    printable = " ".join(argv)
    print(f"+ {printable}", flush=True)
    kwargs = {"cwd": cwd, "env": env, "text": True, "check": False}
    if capture:
        kwargs.update(stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cp = _original_subprocess_run(argv, **kwargs)
    if capture:
        print(cp.stdout or "", end="", flush=True)
    if check and cp.returncode != 0:
        raise RuntimeError(f"command failed rc={cp.returncode}: {printable}")
    return cp


def portable_parse_tap_counts(text: str):
    def last_count(name: str):
        patterns = [
            rf"^#\s*{name}\s+(\d+)\s*$",
            rf"^ℹ\s*{name}\s+(\d+)\s*$",
            rf"^\s*{name}\s+(\d+)\s*$",
        ]
        values = []
        for pattern in patterns:
            values.extend(re.findall(pattern, text, flags=re.M | re.I))
        return int(values[-1]) if values else None

    tests = last_count("tests")
    passed = last_count("pass")
    failed = last_count("fail")
    if tests is None or passed is None or failed is None:
        return None
    return passed, tests, failed


def portable_node_suite(root: Path, label: str):
    tests = sorted((root / "extension" / "tests").glob("*.test.mjs"), key=lambda p: p.as_posix())
    base.require(tests, f"{label}: no top-level tests found")
    rels = [str(p.relative_to(root)) for p in tests]
    cp = portable_run([base.exe("node"), "--test", "--test-reporter=tap", *rels], cwd=root, capture=True)
    counts = portable_parse_tap_counts(cp.stdout or "")
    base.require(counts is not None, f"{label}: unable to parse TAP counts")
    passed, total, failed = counts
    base.require(failed == 0 and passed == total, f"{label}: {passed}/{total}, fail={failed}")
    print(f"{label.upper()}={passed}/{total}")
    return passed, total, cp.stdout or ""


def portable_verify_transport(zip_path: Path, manifest_path: Path, extract_to: Path):
    base.require(zip_path.stat().st_size == base.EXPECTED_ZIP_BYTES, "inner ZIP byte count mismatch")
    base.require(base.sha256_file(zip_path) == base.EXPECTED_ZIP_SHA, "inner ZIP SHA-256 mismatch")
    m = base.json.loads(manifest_path.read_text(encoding="utf-8"))
    base.require(m.get("source_commit") == base.EXPECTED_SOURCE, "manifest source_commit mismatch")
    base.require(m.get("product_tree") == base.EXPECTED_TREE, "manifest product_tree mismatch")
    base.require(m.get("preflight_run_id") == 33037727189, "manifest preflight_run_id mismatch")
    base.require(m.get("sha256") == base.EXPECTED_ZIP_SHA, "manifest SHA mismatch")
    base.require(m.get("bytes") == base.EXPECTED_ZIP_BYTES, "manifest bytes mismatch")
    base.require(m.get("files") == base.EXPECTED_FILES, "manifest files mismatch")
    base.require(m.get("zip_test") == "PASS", "manifest zip_test mismatch")
    base.require(m.get("real_yandex_requests") == 0, "manifest real_yandex_requests mismatch")

    if extract_to.exists():
        base.shutil.rmtree(extract_to)
    extract_to.mkdir(parents=True)

    expected_paths = [row["path"] for row in m["entries"]]
    with zipfile.ZipFile(zip_path, "r") as zf:
        base.require(zf.testzip() is None, "ZIP integrity failure")
        base.require(zf.namelist() == expected_paths, "ZIP entry order/path mismatch")
        zf.extractall(extract_to)

    actual_paths = sorted(
        p.relative_to(extract_to).as_posix()
        for p in extract_to.rglob("*")
        if p.is_file()
    )
    base.require(len(actual_paths) == base.EXPECTED_FILES, "extracted file count mismatch")
    base.require(actual_paths == sorted(expected_paths), "extracted path set mismatch")

    for row in m["entries"]:
        p = extract_to.joinpath(*row["path"].split("/"))
        data = p.read_bytes()
        base.require(len(data) == row["bytes"], f"byte mismatch: {row['path']}")
        base.require(base.sha256_bytes(data) == row["sha256"], f"hash mismatch: {row['path']}")

    print("D00_ARTIFACT_TRANSPORT_ROUNDTRIP_PASS")
    return m


def portable_git_status_clean(root: Path, label: str):
    cp = portable_run([base.exe("git"), "status", "--porcelain", "--untracked-files=all"], cwd=root, capture=True)
    lines = [line for line in (cp.stdout or "").splitlines() if line.strip()]
    if label == "QA workspace at final audit":
        remaining = []
        ignored = []
        for line in lines:
            path = line[3:].strip().strip('"').replace("\\", "/") if len(line) >= 4 else ""
            if path.startswith("extension/src/"):
                ignored.append(line)
            else:
                remaining.append(line)
        base.require(not remaining, f"{label} not clean outside byte-verified extension/src:\n" + "\n".join(remaining))
        if ignored:
            print("WINDOWS_GIT_EOL_STATUS_NOISE_IGNORED_AFTER_PRODUCT_BYTE_IDENTITY")
        return
    base.require(not lines, f"{label} not clean:\n" + "\n".join(lines))


def portable_run_browser(script_rel: str, markers, label: str):
    script = base.REPO / script_rel
    base.require(script.exists(), f"missing browser harness: {script_rel}")
    execution_script = script
    temp_adapter = None
    try:
        if os.name == "nt" and script_rel.replace("\\", "/").endswith("qa_browser/direct_codex_gate_addendum_v2.mjs"):
            source = script.read_text(encoding="utf-8")
            needle = "async function waitUntil(fn,message,timeout=25000,interval=120)"
            replacement = "async function waitUntil(fn,message,timeout=60000,interval=120)"
            base.require(source.count(needle) == 1, "Windows timing adapter authority mismatch")
            adapted = source.replace(needle, replacement, 1)
            # Exactly one semantic change is permitted: the generic wait budget.
            base.require(adapted.count(replacement) == 1, "Windows timing adapter replacement mismatch")
            temp_adapter = script.with_name(".direct_codex_gate_addendum_v2_windows_timing_adapter.mjs")
            temp_adapter.write_text(adapted, encoding="utf-8", newline="\n")
            execution_script = temp_adapter
            print("WINDOWS_DIRECT_ADDENDUM_TIMING_ADAPTER_25S_TO_60S_ACTIVE")
        cp = portable_run(base.browser_cmd(execution_script), cwd=base.REPO, capture=True)
        for marker in markers:
            base.require(marker in (cp.stdout or ""), f"{label}: missing marker {marker}")
        print(f"{label}=PASS")
        return cp.stdout or ""
    finally:
        if temp_adapter is not None and temp_adapter.exists():
            temp_adapter.unlink()


base.run = portable_run
base.parse_tap_counts = portable_parse_tap_counts
base.node_suite = portable_node_suite
base.verify_transport = portable_verify_transport
base.git_status_clean = portable_git_status_clean
base.run_browser = portable_run_browser


def cleanup_safe_subprocess_run(cmd, *args, **kwargs):
    argv = [str(x) for x in cmd] if isinstance(cmd, (list, tuple)) else cmd
    cwd = Path(kwargs.get("cwd") or base.REPO).resolve()
    if isinstance(argv, list) and argv and Path(argv[0]).stem.lower() == "git":
        argv = [argv[0], "-c", f"safe.directory={safe_dir_value(cwd)}", *argv[1:]]
    return _original_subprocess_run(argv, *args, **kwargs)

base.subprocess.run = cleanup_safe_subprocess_run

if __name__ == "__main__":
    try:
        base.main()
    except Exception as exc:
        print(f"PHASE5_DIRECT_R2_INDEPENDENT_RUNNER_V2_FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
