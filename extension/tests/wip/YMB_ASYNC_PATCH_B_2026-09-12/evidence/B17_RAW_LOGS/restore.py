"""Restore exact B17 raw evidence from four published binary parts, not a build.
Usage: python restore.py NEW_OUTPUT.tar.xz
No network, product execution, overwrite or filesystem extraction.
"""
from pathlib import Path, PurePosixPath
import hashlib
import io
import json
import sys
import tarfile

EXPECTED_SHA = '62b7511def54cd6f1261b2becd9810c1e32cafb397ae24ccf72fa4aedb222a7d'
EXPECTED_BYTES = 36696

def sha(data):
    return hashlib.sha256(data).hexdigest()

def restore(out):
    root = Path(__file__).resolve().parent
    if out.exists():
        raise ValueError('Refusing existing output')
    manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
    if (manifest['sha256'], manifest['bytes']) != (EXPECTED_SHA, EXPECTED_BYTES):
        raise ValueError('Wrong frozen archive identity')
    names = [f'part-{i:03d}.bin' for i in range(1, 5)]
    if [p['name'] for p in manifest['parts']] != names:
        raise ValueError('Wrong ordered part set')
    parts = []
    for item in manifest['parts']:
        source = root / item['name']
        if source.is_symlink():
            raise ValueError('Symlink input refused')
        data = source.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if len(data) != item['bytes'] or sha(data) != item['sha256'] or blob != item['git_blob']:
            raise ValueError('Corrupt part: ' + item['name'])
        parts.append(data)
    data = b''.join(parts)
    if len(data) != EXPECTED_BYTES or sha(data) != EXPECTED_SHA:
        raise ValueError('Archive identity failed')
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:xz') as archive:
        files = {}
        for member in archive.getmembers():
            name = PurePosixPath(member.name)
            if not member.isfile() or name.is_absolute() or '..' in name.parts or member.name in files:
                raise ValueError('Unsafe/duplicate archive member')
            files[member.name] = archive.extractfile(member).read()
    if len(files) != 55 or manifest['members'] != 55:
        raise ValueError('Member count failed')
    checked = set()
    for line in files['MASTER_SHA256SUMS'].decode('utf-8').splitlines():
        digest, name = line.split('  ', 1)
        if name in checked or name not in files or sha(files[name]) != digest:
            raise ValueError('Member checksum failed: ' + name)
        checked.add(name)
    if checked != set(files) - {'MASTER_SHA256SUMS'} or len(checked) != 54 or manifest['member_checksums'] != 54:
        raise ValueError('Incomplete internal checksum coverage')
    # Exclusive creation only after all input and consumer checks succeed.
    with out.open('xb') as handle:
        handle.write(data)
    print(json.dumps({'status':'PASS', 'bytes':len(data), 'sha256':sha(data), 'members':55,
                      'member_checksums':54, 'product_executed':False, 'release_allowed':False}))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    restore(Path(sys.argv[1]))
