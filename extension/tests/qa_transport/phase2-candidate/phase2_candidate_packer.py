#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
import stat
import zipfile
from pathlib import Path

ROOT_NAME = "yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate"
FIXED_DT = (2025, 12, 31, 19, 0, 0)
EXPECTED_ZIP_SHA256 = "874cff11de034d0347db9216447869594f88d18207cf2e7e3b15fad5af1eac47"
EXPECTED_ZIP_BYTES = 141507
EXPECTED_FILES = 55
EXPECTED_ENTRIES = 58
FROZEN_MANIFEST_REL = Path("extension/tests/qa_transport/phase2-candidate/EXACT_CANDIDATE_MANIFEST_2026-08-23.json")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def zipinfo(name, is_dir):
    zi = zipfile.ZipInfo(name, FIXED_DT)
    zi.create_system = 3
    zi.create_version = 20
    zi.extract_version = 20
    zi.flag_bits = 0
    zi.internal_attr = 0
    zi.extra = b""
    zi.comment = b""
    if is_dir:
        zi.compress_type = zipfile.ZIP_STORED
        zi.external_attr = ((stat.S_IFDIR | 0o755) << 16) | 0x10
    else:
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = (stat.S_IFREG | 0o644) << 16
    return zi


def selected_files(repo):
    src = repo / "extension" / "src"
    tests = repo / "extension" / "tests"
    rows = []
    for file in sorted(p for p in src.rglob("*") if p.is_file()):
        rows.append((file.relative_to(src).as_posix(), file))
    for file in sorted(tests.glob("*.test.mjs")):
        rows.append((f"tests/{file.name}", file))
    return rows


def payload_manifest(rows):
    out = []
    for rel, file in rows:
        data = file.read_bytes()
        out.append({"path": rel, "bytes": len(data), "sha256": sha256_bytes(data)})
    return out


def load_frozen_identity(repo):
    frozen = json.loads((repo / FROZEN_MANIFEST_REL).read_text(encoding="utf-8"))
    expected = {
        "root_name": ROOT_NAME,
        "sha256": EXPECTED_ZIP_SHA256,
        "bytes": EXPECTED_ZIP_BYTES,
        "files": EXPECTED_FILES,
        "entries": EXPECTED_ENTRIES,
    }
    for key, value in expected.items():
        if frozen.get(key) != value:
            raise SystemExit(f"FROZEN_MANIFEST_IDENTITY_FAIL {key}: {frozen.get(key)!r} != {value!r}")
    return frozen


def build(repo, output, manifest_output=None):
    load_frozen_identity(repo)
    rows = selected_files(repo)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, strict_timestamps=True) as z:
        z.comment = b""
        for directory in sorted({ROOT_NAME + "/", ROOT_NAME + "/shared/", ROOT_NAME + "/tests/"}):
            z.writestr(zipinfo(directory, True), b"")
        for rel, file in sorted(rows, key=lambda item: item[0]):
            z.writestr(
                zipinfo(f"{ROOT_NAME}/{rel}", False),
                file.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )
    data = output.read_bytes()
    with zipfile.ZipFile(output, "r") as z:
        bad = z.testzip()
        files = sum(1 for item in z.infolist() if not item.filename.endswith("/"))
        entries = len(z.infolist())
    result = {
        "root_name": ROOT_NAME,
        "sha256": sha256_bytes(data),
        "bytes": len(data),
        "files": files,
        "entries": entries,
        "zip_test": bad or "PASS",
        "payload": payload_manifest(rows),
    }
    if bad is not None:
        raise SystemExit(f"ZIP_INTEGRITY_FAIL: {bad}")
    if result["sha256"] != EXPECTED_ZIP_SHA256 or result["bytes"] != EXPECTED_ZIP_BYTES:
        raise SystemExit(f"EXACT_ARTIFACT_HASH_FAIL {result['sha256']}/{result['bytes']}")
    if result["files"] != EXPECTED_FILES or result["entries"] != EXPECTED_ENTRIES:
        raise SystemExit(f"EXACT_ARTIFACT_COUNT_FAIL {result['files']}/{result['entries']}")
    if manifest_output:
        manifest_output.parent.mkdir(parents=True, exist_ok=True)
        manifest_output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def verify_extraction(repo, archive, extract_dir):
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True)
    with zipfile.ZipFile(archive, "r") as z:
        z.extractall(extract_dir)
    root = extract_dir / ROOT_NAME
    expected = {row["path"]: row for row in payload_manifest(selected_files(repo))}
    actual = {}
    for file in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = file.relative_to(root).as_posix()
        data = file.read_bytes()
        actual[rel] = {"path": rel, "bytes": len(data), "sha256": sha256_bytes(data)}
    if set(actual) != set(expected):
        raise SystemExit(f"PACKAGE_PATH_SET_FAIL missing={sorted(set(expected)-set(actual))} extra={sorted(set(actual)-set(expected))}")
    for rel in sorted(expected):
        if actual[rel] != expected[rel]:
            raise SystemExit(f"PACKAGE_BYTE_IDENTITY_FAIL {rel}: {actual[rel]} != {expected[rel]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--manifest-output")
    parser.add_argument("--verify-extract")
    args = parser.parse_args()
    repo = Path(args.repo_root).resolve()
    output = Path(args.output).resolve()
    manifest_output = Path(args.manifest_output).resolve() if args.manifest_output else None
    result = build(repo, output, manifest_output)
    if args.verify_extract:
        verify_extraction(repo, output, Path(args.verify_extract).resolve())
    print(f"artifact={output}")
    print(f"sha256={result['sha256']}")
    print(f"bytes={result['bytes']}")
    print(f"files={result['files']}")
    print(f"entries={result['entries']}")
    print(f"zip_test={result['zip_test']}")
    print("EXACT_ARTIFACT_IDENTITY_PASS")
    if args.verify_extract:
        print("SOURCE_PACKAGE_IDENTITY_PASS")


if __name__ == "__main__":
    main()
