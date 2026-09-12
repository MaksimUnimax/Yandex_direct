"""Restore the exact B5 QA tree, not an installable extension.
Usage: python qa/prepare_b5.py EXTRACTED_OWNER_014_BASELINE EMPTY_OUTPUT_DIR
Saved inputs are read from this Patch B subtree. No network or provider calls.
"""
from pathlib import Path
import hashlib
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
BASE_TREE = '6092555d37a1fa0145d71ae0bf0f76eb0b9c9596a4be7a1e0e7c2a0b9325aa36'
INPUTS = {
    'candidate/b5/search_async_policy.js': 'ba5bc8de08eb62e422906a06d916e30ee00e088e008bbf408615a77e0c6b3e10',
    'candidate/b5/search_legacy_admission.js': '6ac3274bb35d6b10676ff49d96e13a3921cfeb1f71a9aff2d7f6a7ff7c7ab0c3',
    'evidence/B5_LEGACY_DELTA.diff': '4d526e83814ce792c00bf752a9a0ef61470fc81160c106c6f084007331826041',
    'qa/b5_callers.test.mjs': 'e769f93910a4ba8a29726e27abe898cfcc9d75f63e3cdb28420cdbcddf10b1b8',
    'qa/b5_legacy.test.mjs': 'dabe61e03a6fa158c3561a69d09125da4ecbcb9aff84c27c048c1819fe5d300f',
    'qa/b5_policy.test.mjs': '740cb2fc3cafb2b90cf8b32ca857dedab11ca77ff351b56baa88f5fc0228a0c4',
    'qa/idb_test_double.mjs': '1327c21fca17b0a34ebec3a8234c9721d1f09192f00bd862cffdbf1548d025af',
}
POSTIMAGES = {
    'search_batch_worker_transport.js': 'b2adca7ec2e75ca18eb660e7335373cd47f027c48239f496914a5380a972bafe',
    'service_worker.js': '0a00d57a222259e2c5501394b5856ffee90b7660f276ea1b25ddbade883070f6',
    'shared/phase3_provider_runtime.js': 'ba63d2bce1778d41962c3ea3cbc2586c8ac742e1415bb5d5686b2b338fa4aecc',
    'wordstat_batch_worker_integration.js': '4607e35e08064af90cfdad98bbeaa2d5431289ab2a104e3cf8fc6e5b33621b74',
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def apply_exact(old_bytes, lines):
    old = old_bytes.decode('utf-8').splitlines(keepends=True)
    result = []
    cursor = pos = 0
    while pos < len(lines):
        match = re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n', lines[pos])
        if not match:
            raise ValueError('Malformed hunk header')
        start, old_count, new_start, new_count = [int(x or 1) for x in match.groups()]
        if start - 1 < cursor:
            raise ValueError('Overlapping hunks')
        result.extend(old[cursor:start - 1])
        cursor = start - 1
        if len(result) != new_start - 1:
            raise ValueError('Wrong postimage offset')
        consumed = emitted = 0
        pos += 1
        while pos < len(lines) and not lines[pos].startswith('@@ '):
            line = lines[pos]
            if not line or line[0] not in ' +-':
                raise ValueError('Unexpected hunk line')
            if line[0] in ' -':
                if cursor >= len(old) or old[cursor] != line[1:]:
                    raise ValueError('Exact preimage mismatch')
                cursor += 1
                consumed += 1
            if line[0] in ' +':
                result.append(line[1:])
                emitted += 1
            pos += 1
        if (consumed, emitted) != (old_count, new_count):
            raise ValueError('Hunk count mismatch')
    result.extend(old[cursor:])
    return ''.join(result).encode('utf-8')

def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    baseline, output = [Path(x).resolve() for x in sys.argv[1:]]
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise SystemExit('Refusing to overwrite nonempty output')
    files = sorted(p for p in baseline.rglob('*') if p.is_file())
    if any(p.is_symlink() for p in baseline.rglob('*')):
        raise SystemExit('Symlink baseline is not accepted')
    tree_manifest = ''.join(f'{sha(p.read_bytes())}  {p.relative_to(baseline).as_posix()}\n' for p in files)
    if len(files) != 53 or sha(tree_manifest.encode('utf-8')) != BASE_TREE:
        raise SystemExit('Wrong exact owner 0.1.4 baseline tree')
    values = {}
    for relative, expected in INPUTS.items():
        data = (ROOT / relative).read_bytes()
        if sha(data) != expected:
            raise SystemExit('Wrong saved B5 bytes: ' + relative)
        values[relative] = data
    lines = values['evidence/B5_LEGACY_DELTA.diff'].decode('utf-8').splitlines(keepends=True)
    post = {}
    pos = 0
    while pos < len(lines):
        if not lines[pos].startswith('--- a/'):
            raise ValueError('Missing delta target')
        name = lines[pos][6:].rstrip('\n')
        if name not in POSTIMAGES or name in post or lines[pos + 1] != '+++ b/' + name + '\n':
            raise ValueError('Unexpected or repeated delta target')
        end = pos + 2
        while end < len(lines) and not lines[end].startswith('--- a/'):
            end += 1
        result = apply_exact((baseline / name).read_bytes(), lines[pos + 2:end])
        if sha(result) != POSTIMAGES[name]:
            raise ValueError('Wrong postimage: ' + name)
        post[name] = result
        pos = end
    if set(post) != set(POSTIMAGES):
        raise ValueError('Incomplete delta')
    # All hashes/hunks checked before any output. No root extension manifest.
    output.mkdir(parents=True, exist_ok=True)
    for p in files:
        target = output / 'owner014' / p.relative_to(baseline)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
    for relative, data in values.items():
        if relative.startswith('candidate/b5/'):
            relative = relative.replace('candidate/b5/', 'candidate/shared/', 1)
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    for relative, data in post.items():
        target = output / 'candidate/legacy' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    print('EXACT_B5_QA_TREE = PASS; provider calls = 0; no installable package')
    print('Run: node --test ' + str(output / 'qa/b5*.test.mjs'))

if __name__ == '__main__':
    main()
