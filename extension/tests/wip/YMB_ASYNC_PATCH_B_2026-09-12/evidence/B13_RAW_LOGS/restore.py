"""Verify eight saved evidence parts and write the exact original log archive.
Usage: python restore.py NEW_OUTPUT.tar.xz
No extraction, product execution, network, or overwrite.
"""
from pathlib import Path, PurePosixPath
import hashlib, io, json, sys, tarfile
ROOT = Path(__file__).resolve().parent
EXPECTED = 'abd3a1c68e1e356afda0b8cf7d3863de83849d4515ca8d63219affc810a9b019'
sha = lambda b: hashlib.sha256(b).hexdigest()
def main():
    if len(sys.argv) != 2: raise SystemExit(__doc__)
    output = Path(sys.argv[1])
    if output.exists() or output.is_symlink(): raise ValueError('Output already exists')
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    rows = manifest['parts']
    if [r['name'] for r in rows] != [f'part-{i:03d}.bin' for i in range(1, 9)]: raise ValueError('Part order mismatch')
    parts = []
    for row in rows:
        p = ROOT / row['name']
        if p.is_symlink() or p.stat().st_size != row['bytes'] or row['bytes'] > 6000: raise ValueError('Invalid part size/path')
        b = p.read_bytes()
        if sha(b) != row['sha256']: raise ValueError('Part checksum mismatch')
        parts.append(b)
    data = b''.join(parts)
    if len(data) != 45312 or sha(data) != EXPECTED or manifest['sha256'] != EXPECTED: raise ValueError('Archive identity mismatch')
    members = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:xz') as archive:
        total = 0
        for entry in archive:
            p = PurePosixPath(entry.name)
            total += entry.size
            if not entry.isfile() or p.is_absolute() or '..' in p.parts or entry.name in members or total > 1000000: raise ValueError('Unsafe archive')
            members[entry.name] = archive.extractfile(entry).read()
    if len(members) != 168: raise ValueError('Member count mismatch')
    checks = {}
    for line in members['SHA256SUMS'].decode('utf-8').splitlines():
        digest, name = line.split('  ', 1)
        if name in checks: raise ValueError('Duplicate checksum entry')
        checks[name] = digest
    if len(checks) != 167 or set(checks) != set(members) - {'SHA256SUMS'}: raise ValueError('Incomplete checksum inventory')
    for name, digest in checks.items():
        if sha(members[name]) != digest: raise ValueError('Inner checksum mismatch: ' + name)
    with output.open('xb') as f: f.write(data)
    print('PASS: 8 parts, 45312 bytes, 168 members, 167 inner checksums; evidence only')
if __name__ == '__main__': main()
