"""Re-run preserved module tests on exact B9 bytes. NO browser or provider traffic.
Usage: python qa/b9_regression_campaign.py OWNER014_BASELINE B9_QA_DIR EMPTY_LOG_DIR
First restore B9_QA_DIR with prepare_b9.py. Never writes into an installed extension.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys
ROOT = Path(__file__).resolve().parent.parent
TESTS = {
    'b3_runtime.test.mjs': 'b3c0f1917de31bcb98a38b522ebc02fbd467566d548eaadc8a23b3a8b68d76e3',
    'b3_store_edge.test.mjs': '8e5901ae35aca7a29ac649e33679bcf7b875467dd9736c0817c0780d1b3b33ed',
    'b3_store_regression.test.mjs': '82f69cc166373791c3ea19bec1d04263ad7012d0fd4f9bbc4670af60b26b29de',
    'b4_normalizer.test.mjs': '8e9365938f88cc2a58abc9a07045fb017192a036a51a0af5c89acf22550a05f9',
    'b5_callers.test.mjs': 'e769f93910a4ba8a29726e27abe898cfcc9d75f63e3cdb28420cdbcddf10b1b8',
    'b5_legacy.test.mjs': 'dabe61e03a6fa158c3561a69d09125da4ecbcb9aff84c27c048c1819fe5d300f',
    'b5_policy.test.mjs': '740cb2fc3cafb2b90cf8b32ca857dedab11ca77ff351b56baa88f5fc0228a0c4',
    'b6_binding.test.mjs': 'de7ddd10cf4420e2a5a7755803a5082fc46be3809d8c2a52476fa232254e9808',
    'protocol.test.mjs': '8ec6ea1acc9bf0721d499caea1514f036a8f4e57ace8caf4b0ccd245bb710718',
    'transport.test.mjs': '429e280f9ecd3dfa2e8359c55310f24200d1e44a8e960a8ace68fef83808117d',
}
FIXTURE_SHA = '1327c21fca17b0a34ebec3a8234c9721d1f09192f00bd862cffdbf1548d025af'
def sha(b):
    return hashlib.sha256(b).hexdigest()
def tree_sha(root):
    if any(p.is_symlink() for p in root.rglob('*')):
        raise ValueError('Symlink tree rejected')
    paths = sorted(p for p in root.rglob('*') if p.is_file())
    return sha(''.join(sha(p.read_bytes()) + '  ' + p.relative_to(root).as_posix() + '\n' for p in paths).encode())
def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    baseline, qa_root, logs = map(lambda p: Path(p).resolve(), sys.argv[1:])
    if logs.exists() and (not logs.is_dir() or any(logs.iterdir())):
        raise ValueError('Refusing nonempty logs/output')
    full = qa_root / 'candidate/full'
    if tree_sha(baseline) != '6092555d37a1fa0145d71ae0bf0f76eb0b9c9596a4be7a1e0e7c2a0b9325aa36':
        raise ValueError('Wrong baseline')
    if tree_sha(full) != 'd1fc4f49718f023f1bc1a6a3ec921fa7253d63b805cedadff6fbcf2e70180612':
        raise ValueError('Wrong B9 candidate')
    for name, expected in {**TESTS, 'idb_test_double.mjs': FIXTURE_SHA}.items():
        if sha((ROOT / 'qa' / name).read_bytes()) != expected:
            raise ValueError('Test input changed: ' + name)
    work = logs / 'modules'
    (work / 'qa').mkdir(parents=True)
    for name in [*TESTS, 'idb_test_double.mjs']:
        shutil.copyfile(ROOT / 'qa' / name, work / 'qa' / name)
    shutil.copytree(baseline, work / 'baseline')
    shutil.copytree(baseline, work / 'owner014')
    shutil.copytree(full / 'shared', work / 'candidate/shared')
    shutil.copytree(full, work / 'candidate/legacy')
    shutil.copyfile(full / 'search_admission_worker_binding.js', work / 'candidate/search_admission_worker_binding.js')
    command = ['node', '--test', *[str(work / 'qa' / name) for name in TESTS]]
    status = {'venue': 'Node; preserved IDB and network fixtures; not Chrome', 'candidate_tree_sha256': tree_sha(full), 'tests_sha256': TESTS, 'provider_calls': 0, 'release_allowed': False}
    try:
        result = subprocess.run(command, capture_output=True, timeout=60)
        (logs / 'MODULE_REGRESSION.tap').write_bytes(result.stdout)
        (logs / 'MODULE_REGRESSION.stderr').write_bytes(result.stderr)
        footer = dict(re.findall(r'^# (tests|pass|fail|skipped|cancelled|duration_ms) (.+)$', result.stdout.decode(), re.M))
        status.update(returncode=result.returncode, footer=footer, tap_sha256=sha(result.stdout), tap_bytes=len(result.stdout))
        passed = result.returncode == 0 and footer.get('tests') == '254' and footer.get('pass') == '254' and footer.get('fail') == '0' and footer.get('skipped') == '0'
        status['status'] = 'PASS' if passed else 'FAIL'
    except subprocess.TimeoutExpired as e:
        (logs / 'MODULE_REGRESSION.partial.tap').write_bytes(e.stdout or b'')
        status.update(status='BLOCKED_TIMEOUT', timeout_seconds=60)
        passed = False
    (logs / 'RESULT.json').write_text(json.dumps(status, indent=2) + '\n')
    print(json.dumps({k: v for k, v in status.items() if k != 'tests_sha256'}, indent=2))
    raise SystemExit(0 if passed else 1)
if __name__ == '__main__':
    main()
