"""Reconstruct the exact B3 QA tree, not an installable extension.
Usage: python qa/prepare_b3.py EXTRACTED_OWNER_014_BASELINE EMPTY_OUTPUT_DIR
Run from the saved B1/B2/B3 repository subtree. No network or provider calls.
"""
from pathlib import Path
import hashlib
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
BEFORE = '4145cbc91865c3151a34f8958640c6351bf6cb23a3a74441920d3517d483cba4'
AFTER = '465645a993568e57afc88553c242703e77aab5eca19b37133dbc20c439d2c6f5'
EXPECTED = {
    'search_async_store.js': AFTER,
    'search_async_protocol.js': 'f4b8dbfced3ed1136355c805bb5fc83cd39472b44e91faf0639ec766f9c0ffec',
    'search_async_transport.js': '1e042fb061e1069a1c73fc73810079ff738b703015a52ada4dd501da6344935f',
    'search_async_runtime.js': 'e8be98e7bd692321e44ff3af147415f235c9e4367de508982dc60f88b596de6f',
}
BASELINE_PROTOCOL = '48cb17f0a846f87e2057d65945dce23788e5c3c90810b7542557d762c2f301b7'
DELTA = '17590a53467778f74d28b3bf6ec88b486d076c224e07fdc548ea790c1cfa0de9'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def exact_delta(before, delta):
    """Apply this unified diff with exact preimages and no fuzz/EOL conversions."""
    old = before.decode('utf-8').splitlines(keepends=True)
    lines = delta.decode('utf-8').splitlines(keepends=True)
    if lines[:2] != ['--- a/search_async_store.js\n', '+++ b/search_async_store.js\n']:
        raise ValueError('Unexpected delta target')
    pos = 2
    cursor = 0
    result = []
    while pos < len(lines):
        match = re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n', lines[pos])
        if not match:
            raise ValueError('Malformed hunk')
        start, old_count, new_start, new_count = [int(value or 1) for value in match.groups()]
        if start - 1 < cursor:
            raise ValueError('Overlapping hunk')
        result.extend(old[cursor:start - 1])
        cursor = start - 1
        if len(result) != new_start - 1:
            raise ValueError('Postimage offset mismatch')
        deleted = added = 0
        pos += 1
        while pos < len(lines) and not lines[pos].startswith('@@ '):
            line = lines[pos]
            if line[0] in ' -':
                if cursor >= len(old) or old[cursor] != line[1:]:
                    raise ValueError('Exact preimage mismatch')
                cursor += 1
                deleted += 1
            if line[0] in ' +':
                result.append(line[1:])
                added += 1
            if line[0] not in ' +-':
                raise ValueError('Unknown delta line')
            pos += 1
        if (deleted, added) != (old_count, new_count):
            raise ValueError('Hunk size mismatch')
    result.extend(old[cursor:])
    return ''.join(result).encode('utf-8')

def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    baseline, output = (Path(p).resolve() for p in sys.argv[1:])
    if output.exists() and any(output.iterdir()):
        raise SystemExit('Refusing to overwrite nonempty output')
    base = (baseline / 'shared/search_protocol.js').read_bytes()
    if digest(base) != BASELINE_PROTOCOL:
        raise SystemExit('Wrong owner baseline SearchProtocol')
    original = (ROOT / 'candidate/shared/search_async_store.js').read_bytes()
    patch = (ROOT / 'evidence/B3_STORE_DELTA.diff').read_bytes()
    if digest(original) != BEFORE or digest(patch) != DELTA:
        raise SystemExit('Wrong B1 store/delta; do not regenerate from memory')
    store = exact_delta(original, patch)
    data = {'search_async_store.js': store}
    for name in EXPECTED:
        if name not in data:
            data[name] = (ROOT / 'candidate/shared' / name).read_bytes()
        if digest(data[name]) != EXPECTED[name]:
            raise SystemExit(f'Postimage mismatch: {name}')
    (output / 'candidate/shared').mkdir(parents=True, exist_ok=True)
    for name, value in data.items():
        (output / 'candidate/shared' / name).write_bytes(value)
    (output / 'baseline/shared').mkdir(parents=True, exist_ok=True)
    (output / 'baseline/shared/search_protocol.js').write_bytes(base)
    (output / 'qa').mkdir(exist_ok=True)
    for name in ['idb_test_double.mjs', 'b3_store_regression.test.mjs', 'b3_store_edge.test.mjs', 'b3_runtime.test.mjs']:
        shutil.copyfile(ROOT / 'qa' / name, output / 'qa' / name)
    print('EXACT_B3_QA_TREE = PASS; no installable build created')
    print('Run: node --test ' + str(output / 'qa') + '/b3*.test.mjs')

if __name__ == '__main__':
    main()
