#!/usr/bin/env python3
import argparse
import hashlib
import json
import stat
import zipfile
from pathlib import Path

FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def file_manifest(src: Path):
    out = []
    for path in sorted(p for p in src.rglob('*') if p.is_file()):
        rel = path.relative_to(src).as_posix()
        data = path.read_bytes()
        out.append({'path': rel, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    return out


def build(src: Path, output: Path):
    files = file_manifest(src)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w') as zf:
        zf.comment = b''
        for item in files:
            path = src / item['path']
            info = zipfile.ZipInfo(item['path'], date_time=FIXED_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.extra = b''
            info.comment = b''
            with path.open('rb') as fh:
                zf.writestr(info, fh.read(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(output, 'r') as zf:
        bad = zf.testzip()
        if bad is not None:
            raise SystemExit(f'ZIP integrity failed at {bad}')
        names = zf.namelist()
        if names != [item['path'] for item in files]:
            raise SystemExit('ZIP entry order/path identity mismatch')
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--source-commit', required=True)
    args = ap.parse_args()
    src = Path(args.src).resolve()
    output = Path(args.output).resolve()
    manifest_path = Path(args.manifest).resolve()
    files = build(src, output)
    manifest = {
        'format': 'YMB_EXACT_CANDIDATE_V1',
        'product_version': json.loads((src / 'manifest.json').read_text(encoding='utf-8'))['version'],
        'source_commit': args.source_commit,
        'source_root': 'extension/src',
        'artifact': output.name,
        'sha256': sha256_file(output),
        'bytes': output.stat().st_size,
        'files': len(files),
        'entries': len(files),
        'zip_test': 'PASS',
        'packing': {
            'entry_order': 'lexicographic_relative_path',
            'explicit_directory_entries': False,
            'timestamp': '2026-01-01T00:00:00',
            'compression': 'ZIP_DEFLATED',
            'compression_level': 9,
            'create_system': 3,
            'file_mode': 'S_IFREG|0644',
            'extra': 'empty',
            'entry_comment': 'empty',
            'archive_comment': 'empty'
        },
        'file_manifest': files
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: manifest[k] for k in ('product_version', 'source_commit', 'artifact', 'sha256', 'bytes', 'files', 'entries', 'zip_test')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
