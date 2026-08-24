#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(message: str):
    raise SystemExit(message)


def safe_member_path(name: str):
    p = PurePosixPath(name)
    if p.is_absolute() or ".." in p.parts:
        fail(f"PACKAGE_UNSAFE_PATH {name!r}")


def verify_archive(archive: Path, manifest: dict):
    actual_sha = sha256_file(archive)
    actual_bytes = archive.stat().st_size
    if actual_sha != manifest.get("sha256"):
        fail(f"PACKAGE_SHA256_FAIL {actual_sha} != {manifest.get('sha256')}")
    if actual_bytes != manifest.get("bytes"):
        fail(f"PACKAGE_BYTES_FAIL {actual_bytes} != {manifest.get('bytes')}")

    root_name = str(manifest.get("root_name") or "")
    if not root_name:
        fail("PACKAGE_ROOT_NAME_MISSING")

    expected_payload = {row["path"]: row for row in manifest.get("payload", [])}
    if len(expected_payload) != manifest.get("files"):
        fail(f"PACKAGE_MANIFEST_FILE_COUNT_FAIL {len(expected_payload)} != {manifest.get('files')}")

    with zipfile.ZipFile(archive, "r") as z:
        if z.testzip() is not None:
            fail("PACKAGE_ZIP_INTEGRITY_FAIL")
        infos = z.infolist()
        if len(infos) != manifest.get("entries"):
            fail(f"PACKAGE_ENTRY_COUNT_FAIL {len(infos)} != {manifest.get('entries')}")
        actual_payload = {}
        prefix = root_name.rstrip("/") + "/"
        for info in infos:
            safe_member_path(info.filename)
            if info.is_dir():
                continue
            if not info.filename.startswith(prefix):
                fail(f"PACKAGE_ROOT_MISMATCH {info.filename!r}")
            rel = info.filename[len(prefix):]
            data = z.read(info)
            actual_payload[rel] = {
                "path": rel,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }

    if actual_payload != expected_payload:
        missing = sorted(set(expected_payload) - set(actual_payload))
        extra = sorted(set(actual_payload) - set(expected_payload))
        fail(f"PACKAGE_PAYLOAD_MANIFEST_FAIL missing={missing} extra={extra}")
    print("PACKAGE_EXACT_IDENTITY_PASS")


def fresh_extract(archive: Path, manifest: dict, extract_dir: Path) -> Path:
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True)
    with zipfile.ZipFile(archive, "r") as z:
        for info in z.infolist():
            safe_member_path(info.filename)
        z.extractall(extract_dir)
    root = extract_dir / str(manifest["root_name"])
    if not root.is_dir():
        fail(f"PACKAGE_EXTRACT_ROOT_MISSING {root}")
    return root


def stage_repository_layout(package_root: Path, stage_dir: Path, manifest: dict):
    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    src_dir = stage_dir / "src"
    tests_dir = stage_dir / "tests"
    src_dir.mkdir(parents=True)
    tests_dir.mkdir(parents=True)

    expected_payload = {row["path"]: row for row in manifest["payload"]}
    copied = {}
    for rel, row in sorted(expected_payload.items()):
        source = package_root / PurePosixPath(rel)
        if not source.is_file():
            fail(f"PACKAGE_STAGING_SOURCE_MISSING {rel}")
        target = (tests_dir / PurePosixPath(rel).relative_to("tests")) if rel.startswith("tests/") else (src_dir / PurePosixPath(rel))
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        copied_data = target.read_bytes()
        copied[rel] = {
            "path": rel,
            "bytes": len(copied_data),
            "sha256": hashlib.sha256(copied_data).hexdigest(),
        }
        if copied[rel] != row:
            fail(f"PACKAGE_STAGING_BYTE_IDENTITY_FAIL {rel}")

    if copied != expected_payload:
        fail("PACKAGE_STAGING_MANIFEST_FAIL")
    print("PACKAGED_SUITE_LAYOUT_IDENTITY_PASS")
    return src_dir, tests_dir


def run_checked(argv, cwd=None):
    shown = " ".join(str(x) for x in argv)
    print(f"+ {shown}")
    completed = subprocess.run([str(x) for x in argv], cwd=cwd, check=False)
    if completed.returncode != 0:
        fail(f"COMMAND_FAIL rc={completed.returncode}: {shown}")


def run_static_checks(node: str, src_dir: Path, tests_dir: Path):
    scripts = sorted(src_dir.rglob("*.js")) + sorted(tests_dir.rglob("*.mjs"))
    for script in scripts:
        run_checked([node, "--check", script])

    for json_file in [src_dir / "manifest.json", src_dir / "package.json"]:
        if not json_file.is_file():
            fail(f"PACKAGE_JSON_MISSING {json_file.name}")
        json.loads(json_file.read_text(encoding="utf-8"))
    print(f"PACKAGED_SYNTAX_PASS count={len(scripts)}")
    print("PACKAGED_JSON_PASS count=2")


def run_suite(node: str, tests_dir: Path):
    tests = sorted(tests_dir.glob("*.test.mjs"))
    if not tests:
        fail("PACKAGED_SUITE_NO_TEST_FILES")
    run_checked([node, "--test", *tests], cwd=tests_dir.parent)
    print(f"PACKAGED_SUITE_PASS files={len(tests)}")


def main():
    parser = argparse.ArgumentParser(description="Run the governed full suite against exact frozen package bytes without changing the package.")
    parser.add_argument("--archive", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--work-dir", required=True)
    parser.add_argument("--node", default="node")
    args = parser.parse_args()

    archive = Path(args.archive).resolve()
    manifest_path = Path(args.manifest).resolve()
    work_dir = Path(args.work_dir).resolve()
    if not archive.is_file():
        fail(f"PACKAGE_ARCHIVE_MISSING {archive}")
    if not manifest_path.is_file():
        fail(f"PACKAGE_MANIFEST_MISSING {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("format") != "YMB_PHASE2_EXACT_CANDIDATE_V1":
        fail(f"PACKAGE_MANIFEST_FORMAT_FAIL {manifest.get('format')!r}")

    verify_archive(archive, manifest)
    package_root = fresh_extract(archive, manifest, work_dir / "extract")
    src_dir, tests_dir = stage_repository_layout(package_root, work_dir / "repo-layout", manifest)
    run_static_checks(args.node, src_dir, tests_dir)
    run_suite(args.node, tests_dir)
    print("PACKAGED_PREDELIVERY_PREFLIGHT_PASS")


if __name__ == "__main__":
    main()
