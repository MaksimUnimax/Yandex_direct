"""Restore exact B6 QA/full-candidate tree from owner 0.1.4 + saved B5/B6 artifacts.
Usage: python qa/prepare_b6.py EXTRACTED_OWNER_014_BASELINE EMPTY_OUTPUT_DIR
No provider/network calls. Output is QA candidate, NOT an accepted release.
"""
from pathlib import Path
import hashlib, re, shutil, sys

ROOT = Path(__file__).resolve().parent.parent
BASE_TREE = '6092555d37a1fa0145d71ae0bf0f76eb0b9c9596a4be7a1e0e7c2a0b9325aa36'
BASE_FILES = 53
B5_INPUTS = {
    'candidate/b5/search_async_policy.js': 'ba5bc8de08eb62e422906a06d916e30ee00e088e008bbf408615a77e0c6b3e10',
    'candidate/b5/search_legacy_admission.js': '6ac3274bb35d6b10676ff49d96e13a3921cfeb1f71a9aff2d7f6a7ff7c7ab0c3',
    'evidence/B5_LEGACY_DELTA.diff': '4d526e83814ce792c00bf752a9a0ef61470fc81160c106c6f084007331826041',
}
B5_POST = {
    'search_batch_worker_transport.js': 'b2adca7ec2e75ca18eb660e7335373cd47f027c48239f496914a5380a972bafe',
    'service_worker.js': '0a00d57a222259e2c5501394b5856ffee90b7660f276ea1b25ddbade883070f6',
    'shared/phase3_provider_runtime.js': 'ba63d2bce1778d41962c3ea3cbc2586c8ac742e1415bb5d5686b2b338fa4aecc',
    'wordstat_batch_worker_integration.js': '4607e35e08064af90cfdad98bbeaa2d5431289ab2a104e3cf8fc6e5b33621b74',
}
B6_INPUTS = {
    'candidate/b6/search_admission_worker_binding.js': 'a8e383d73a8d8b9e7b59e914bf519e4b0bccfff2e5ee365a57d8132e27d1ed6f',
    'evidence/B6_BOOTSTRAP_DELTA.diff': 'ad03eaa500a546c481092f55c9e4752c2a3a75fc80b34490002f5a71478e1eb2',
    'qa/b6_binding.test.mjs': 'de7ddd10cf4420e2a5a7755803a5082fc46be3809d8c2a52476fa232254e9808',
    'qa/b6_real_composition.test.mjs': 'cf84b1b3c9f02b82de311838b263cb6d671c8b3a22656eb51a11d65866a1a84c',
    'qa/idb_test_double.mjs': '1327c21fca17b0a34ebec3a8234c9721d1f09192f00bd862cffdbf1548d025af',
    'qa/b6_bootstrap.test.mjs': '581bbb3702a80a0ef0123bc852c500864e121b1b885bb3a38accf7b58e10e285',
}
B6_BOOTSTRAP_POST = '6bbd3d52d41d52e1f5d6c4f724dbbb9450dec2012ec99712b127a0d063a2c7b5'


def sha(data): return hashlib.sha256(data).hexdigest()

def apply_exact(old_bytes, diff_bytes, expected_name):
    old = old_bytes.decode('utf-8').splitlines(keepends=True)
    lines = diff_bytes.decode('utf-8').splitlines(keepends=True)
    if len(lines) < 2 or lines[0] != f'--- a/{expected_name}\n' or lines[1] != f'+++ b/{expected_name}\n':
        raise ValueError('Unexpected delta target: ' + expected_name)
    pos, cursor, out = 2, 0, []
    while pos < len(lines):
        m = re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n', lines[pos])
        if not m: raise ValueError('Malformed hunk')
        start, old_count, new_start, new_count = [int(v or 1) for v in m.groups()]
        if start - 1 < cursor: raise ValueError('Overlapping hunk')
        out.extend(old[cursor:start-1]); cursor = start-1
        if len(out) != new_start - 1: raise ValueError('Postimage offset mismatch')
        consumed = emitted = 0; pos += 1
        while pos < len(lines) and not lines[pos].startswith('@@ '):
            line = lines[pos]
            if not line or line[0] not in ' +-': raise ValueError('Bad hunk line')
            if line[0] in ' -':
                if cursor >= len(old) or old[cursor] != line[1:]: raise ValueError('Exact preimage mismatch')
                cursor += 1; consumed += 1
            if line[0] in ' +': out.append(line[1:]); emitted += 1
            pos += 1
        if (consumed, emitted) != (old_count, new_count): raise ValueError('Hunk count mismatch')
    out.extend(old[cursor:])
    return ''.join(out).encode('utf-8')

def split_multi_diff(diff_bytes):
    lines = diff_bytes.decode('utf-8').splitlines(keepends=True)
    chunks = []
    pos = 0
    while pos < len(lines):
        if not lines[pos].startswith('--- a/'): raise ValueError('Missing delta target')
        name = lines[pos][6:].rstrip('\n')
        end = pos + 2
        while end < len(lines) and not lines[end].startswith('--- a/'): end += 1
        chunks.append((name, ''.join(lines[pos:end]).encode('utf-8')))
        pos = end
    return chunks

def main():
    if len(sys.argv) != 3: raise SystemExit(__doc__)
    baseline, output = [Path(x).resolve() for x in sys.argv[1:]]
    if output.exists() and (not output.is_dir() or any(output.iterdir())): raise SystemExit('Refusing to overwrite nonempty output')
    if any(p.is_symlink() for p in baseline.rglob('*')): raise SystemExit('Symlink baseline rejected')
    files = sorted(p for p in baseline.rglob('*') if p.is_file())
    manifest = ''.join(f'{sha(p.read_bytes())}  {p.relative_to(baseline).as_posix()}\n' for p in files)
    if len(files) != BASE_FILES or sha(manifest.encode()) != BASE_TREE: raise SystemExit('Wrong exact owner baseline tree')
    saved = {}
    for rel, expected in {**B5_INPUTS, **B6_INPUTS}.items():
        data = (ROOT / rel).read_bytes()
        if sha(data) != expected: raise SystemExit('Saved input hash mismatch: ' + rel)
        saved[rel] = data
    b5post = {}
    for name, chunk in split_multi_diff(saved['evidence/B5_LEGACY_DELTA.diff']):
        if name not in B5_POST or name in b5post: raise SystemExit('Unexpected B5 delta target: ' + name)
        data = apply_exact((baseline / name).read_bytes(), chunk, name)
        if sha(data) != B5_POST[name]: raise SystemExit('B5 postimage mismatch: ' + name)
        b5post[name] = data
    if set(b5post) != set(B5_POST): raise SystemExit('Incomplete B5 delta')
    boot = apply_exact((baseline / 'phase3_service_worker_bootstrap.js').read_bytes(), saved['evidence/B6_BOOTSTRAP_DELTA.diff'], 'phase3_service_worker_bootstrap.js')
    if sha(boot) != B6_BOOTSTRAP_POST: raise SystemExit('B6 bootstrap postimage mismatch')
    full = output / 'candidate/full'; full.mkdir(parents=True, exist_ok=True)
    for p in files:
        t = full / p.relative_to(baseline); t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, t)
    for rel, data in b5post.items():
        t = full / rel; t.parent.mkdir(parents=True, exist_ok=True); t.write_bytes(data)
    (full / 'shared/search_async_policy.js').write_bytes(saved['candidate/b5/search_async_policy.js'])
    (full / 'shared/search_legacy_admission.js').write_bytes(saved['candidate/b5/search_legacy_admission.js'])
    (full / 'search_admission_worker_binding.js').write_bytes(saved['candidate/b6/search_admission_worker_binding.js'])
    (full / 'phase3_service_worker_bootstrap.js').write_bytes(boot)
    owner = output / 'owner014'; shutil.copytree(baseline, owner)
    qa = output / 'qa'; qa.mkdir()
    for name in ['b6_binding.test.mjs','b6_real_composition.test.mjs','b6_bootstrap.test.mjs','idb_test_double.mjs']:
        shutil.copyfile(ROOT / 'qa' / name, qa / name)
    c = output / 'candidate'; c.mkdir(exist_ok=True)
    (c / 'search_admission_worker_binding.js').write_bytes(saved['candidate/b6/search_admission_worker_binding.js'])
    (c / 'phase3_service_worker_bootstrap.js').write_bytes(boot)
    cs = c / 'shared'; cs.mkdir(exist_ok=True)
    (cs / 'search_async_policy.js').write_bytes(saved['candidate/b5/search_async_policy.js'])
    (cs / 'search_legacy_admission.js').write_bytes(saved['candidate/b5/search_legacy_admission.js'])
    print('EXACT_B6_QA_TREE = PASS; full candidate built for QA only; provider calls = 0')
    print('candidate/full files =', len([p for p in full.rglob('*') if p.is_file()]))

if __name__ == '__main__': main()
