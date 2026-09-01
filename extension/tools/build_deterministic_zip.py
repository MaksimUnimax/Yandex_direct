#!/usr/bin/env python3
import argparse, hashlib, json, stat, zipfile
from pathlib import Path

FIXED_TIME = (2026, 1, 1, 0, 0, 0)

def sha256_bytes(data): return hashlib.sha256(data).hexdigest()

def build(source: Path, output: Path):
    source = source.resolve()
    files = sorted((p for p in source.rglob('*') if p.is_file()), key=lambda p: p.relative_to(source).as_posix())
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w') as zf:
        zf.comment = b''
        for path in files:
            rel = path.relative_to(source).as_posix()
            data = path.read_bytes()
            info = zipfile.ZipInfo(rel, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.create_version = 20
            info.extract_version = 20
            info.flag_bits = 0
            info.internal_attr = 0
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.extra = b''
            info.comment = b''
            zf.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    package = output.read_bytes()
    return {
        'format': 'YMB_DETERMINISTIC_ZIP_V1',
        'archive_root': 'extension/src contents',
        'directory_entries': False,
        'entry_order': 'POSIX_PATH_ASC',
        'timestamp': '2026-01-01T00:00:00 ZIP local fields',
        'compression': 'DEFLATE level 9',
        'create_system': 3,
        'file_mode': '0100644',
        'file_count': len(files),
        'source_bytes': sum(p.stat().st_size for p in files),
        'package_filename': output.name,
        'package_bytes': len(package),
        'package_sha256': sha256_bytes(package),
        'files': [{'path': p.relative_to(source).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha256_bytes(p.read_bytes())} for p in files]
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source', default='extension/src')
    ap.add_argument('--output', required=True)
    ap.add_argument('--manifest')
    args=ap.parse_args()
    manifest=build(Path(args.source), Path(args.output))
    if args.manifest:
        Path(args.manifest).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:manifest[k] for k in ['file_count','package_bytes','package_sha256']},ensure_ascii=False))
if __name__=='__main__': main()
