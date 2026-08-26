#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
import stat
import zipfile
from pathlib import Path

ROOT_NAME = "yandex-marketing-bridge-0.1.1-phase3-webmaster-first-slice-candidate"
FORMAT = "YMB_PHASE3_WEBMASTER_EXACT_CANDIDATE_V1"
FIXED_DT = (2025, 12, 31, 19, 0, 0)


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
    if not src.is_dir() or not tests.is_dir():
        raise SystemExit("PHASE3_SOURCE_LAYOUT_MISSING")
    rows = []
    for file in sorted(p for p in src.rglob("*") if p.is_file()):
        rows.append((file.relative_to(src).as_posix(), file))
    for file in sorted(tests.glob("*.test.mjs")):
        rows.append((f"tests/{file.name}", file))
    helpers = tests / "helpers"
    if helpers.is_dir():
        for file in sorted(p for p in helpers.rglob("*") if p.is_file()):
            rows.append((f"tests/helpers/{file.relative_to(helpers).as_posix()}", file))
    return rows


def payload_manifest(rows):
    out = []
    for rel, file in rows:
        data = file.read_bytes()
        out.append({"path": rel, "bytes": len(data), "sha256": sha256_bytes(data)})
    return out


def build(repo, output):
    rows = selected_files(repo)
    output.parent.mkdir(parents=True, exist_ok=True)
    directories = {ROOT_NAME + "/"}
    for rel, _file in rows:
        parent = Path(rel).parent
        while str(parent) not in (".", ""):
            directories.add(ROOT_NAME + "/" + parent.as_posix().rstrip("/") + "/")
            parent = parent.parent
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, strict_timestamps=True) as z:
        z.comment = b""
        for directory in sorted(directories):
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
        "format": FORMAT,
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
    return result


def verify_expected(result, expected):
    for key in ("format", "root_name", "sha256", "bytes", "files", "entries", "zip_test"):
        if result.get(key) != expected.get(key):
            raise SystemExit(f"EXACT_ARTIFACT_IDENTITY_FAIL {key}: {result.get(key)!r} != {expected.get(key)!r}")
    if result.get("payload") != expected.get("payload"):
        raise SystemExit("EXACT_PAYLOAD_MANIFEST_FAIL")


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


def write_manifest(path, result, source_ref=None, source_commit=None):
    manifest = dict(result)
    manifest["source_ref"] = source_ref
    manifest["source_commit"] = source_commit
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--freeze-manifest-output")
    parser.add_argument("--verify-manifest")
    parser.add_argument("--verify-extract")
    parser.add_argument("--source-ref")
    parser.add_argument("--source-commit")
    args = parser.parse_args()

    if bool(args.freeze_manifest_output) == bool(args.verify_manifest):
        raise SystemExit("Choose exactly one of --freeze-manifest-output or --verify-manifest")

    repo = Path(args.repo_root).resolve()
    output = Path(args.output).resolve()
    result = build(repo, output)

    if args.freeze_manifest_output:
        write_manifest(Path(args.freeze_manifest_output).resolve(), result, source_ref=args.source_ref, source_commit=args.source_commit)
        print("PHASE3_EXACT_ARTIFACT_FREEZE_PASS")
    else:
        expected = json.loads(Path(args.verify_manifest).read_text(encoding="utf-8"))
        if expected.get("format") != FORMAT:
            raise SystemExit(f"PHASE3_MANIFEST_FORMAT_FAIL {expected.get('format')!r}")
        verify_expected(result, expected)
        if args.source_commit and expected.get("source_commit") != args.source_commit:
            raise SystemExit(f"SOURCE_COMMIT_IDENTITY_FAIL {expected.get('source_commit')!r} != {args.source_commit!r}")
        print("PHASE3_EXACT_ARTIFACT_IDENTITY_PASS")

    if args.verify_extract:
        verify_extraction(repo, output, Path(args.verify_extract).resolve())
        print("PHASE3_SOURCE_PACKAGE_IDENTITY_PASS")

    print(f"artifact={output}")
    print(f"sha256={result['sha256']}")
    print(f"bytes={result['bytes']}")
    print(f"files={result['files']}")
    print(f"entries={result['entries']}")
    print(f"zip_test={result['zip_test']}")


if __name__ == "__main__":
    main()
