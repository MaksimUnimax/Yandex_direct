#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import stat
import sys
import zipfile
from pathlib import Path

EXPECTED_SHA256 = "e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65"
EXPECTED_BYTES = 209505
EXPECTED_FILES = 45
EXPECTED_ENTRIES = 48
ROOT = "yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate"
STAMP = (2025, 12, 31, 19, 0, 0)


def make_info(name: str, is_dir: bool) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=STAMP)
    info.create_system = 3  # UNIX
    info.extra = b""
    info.comment = b""
    if is_dir:
        info.compress_type = zipfile.ZIP_STORED
        info.external_attr = ((stat.S_IFDIR | 0o755) << 16) | 0x10
    else:
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = (stat.S_IFREG | 0o644) << 16
    return info


def pack(source_root: Path, output_zip: Path) -> None:
    source_root = source_root.resolve()
    if source_root.name != ROOT:
        raise SystemExit(f"source root basename must be {ROOT!r}, got {source_root.name!r}")

    dirs = sorted(
        (p for p in source_root.rglob("*") if p.is_dir()),
        key=lambda p: p.relative_to(source_root).as_posix(),
    )
    files = sorted(
        (p for p in source_root.rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(source_root).as_posix(),
    )
    if len(files) != EXPECTED_FILES:
        raise SystemExit(f"expected {EXPECTED_FILES} files, got {len(files)}")

    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        output_zip,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        archive.writestr(make_info(ROOT + "/", True), b"")
        for directory in dirs:
            rel = directory.relative_to(source_root).as_posix()
            archive.writestr(make_info(f"{ROOT}/{rel}/", True), b"")
        for file_path in files:
            rel = file_path.relative_to(source_root).as_posix()
            archive.writestr(
                make_info(f"{ROOT}/{rel}", False),
                file_path.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )


def verify(output_zip: Path) -> None:
    data = output_zip.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != EXPECTED_BYTES:
        raise SystemExit(f"byte count mismatch: expected {EXPECTED_BYTES}, got {len(data)}")
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"SHA-256 mismatch: expected {EXPECTED_SHA256}, got {digest}")
    with zipfile.ZipFile(output_zip, "r") as archive:
        if archive.testzip() is not None:
            raise SystemExit("ZIP integrity check failed")
        infos = archive.infolist()
        file_count = sum(not info.is_dir() for info in infos)
        if file_count != EXPECTED_FILES:
            raise SystemExit(f"file count mismatch: expected {EXPECTED_FILES}, got {file_count}")
        if len(infos) != EXPECTED_ENTRIES:
            raise SystemExit(f"entry count mismatch: expected {EXPECTED_ENTRIES}, got {len(infos)}")
    print(f"PASS {digest} {len(data)} bytes {EXPECTED_FILES} files {EXPECTED_ENTRIES} entries")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root", type=Path)
    parser.add_argument("output_zip", type=Path)
    args = parser.parse_args()
    pack(args.source_root, args.output_zip)
    verify(args.output_zip)
    return 0


if __name__ == "__main__":
    sys.exit(main())
