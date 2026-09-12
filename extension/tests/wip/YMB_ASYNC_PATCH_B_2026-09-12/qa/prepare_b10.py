"""Restore exact B10 QA from an already reconstructed B9 tree. NOT a release.
Usage: python qa/prepare_b10.py EXACT_B9_QA_DIR EMPTY_OUTPUT_DIR
No network/provider calls; exact preimage/postimage validation before any write.
"""
from pathlib import Path
import hashlib
import json
import sys
import types
ROOT = Path(__file__).resolve().parent.parent
CONFIG_SHA = '118233317ccd3d8283417b24e1e30d94cfa104e45a8f3aadd3c63e9010c0ec48'
def sha(data):
    return hashlib.sha256(data).hexdigest()
def files(root):
    if not root.is_dir() or root.is_symlink() or any(p.is_symlink() for p in root.rglob('*')):
        raise ValueError('Expected nonsymlink input tree')
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob('*')) if p.is_file()}
def inventory(values):
    return ''.join(sha(v) + '  ' + k + '\n' for k, v in sorted(values.items()))
def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    b9, output = [Path(v).absolute() for v in sys.argv[1:]]
    if output.is_symlink() or (output.exists() and (not output.is_dir() or any(output.iterdir()))):
        raise ValueError('Refusing occupied or symlink output')
    config_bytes = (ROOT / 'evidence/B10_RECONSTRUCTION_INPUTS.json').read_bytes()
    if sha(config_bytes) != CONFIG_SHA:
        raise ValueError('Changed B10 input manifest')
    c = json.loads(config_bytes)
    base = files(b9 / 'candidate/full')
    if len(base) != 67 or sha(inventory(base).encode()) != c['b9_tree']:
        raise ValueError('Not exact combined B9; use saved prepare_b9.py')
    saved = {}
    for rel, expected in c['inputs'].items():
        p = ROOT / rel
        if p.is_symlink() or Path(rel).is_absolute() or '..' in Path(rel).parts:
            raise ValueError('Unsafe input path')
        value = p.read_bytes()
        if sha(value) != expected:
            raise ValueError('Changed saved input: ' + rel)
        saved[rel] = value
    helper = types.ModuleType('b10_delta')
    helper.__file__ = str(ROOT / 'qa/prepare_b6.py')
    exec(compile(saved['qa/prepare_b6.py'], helper.__file__, 'exec'), helper.__dict__)
    result = dict(base)
    seen = set()
    for rel in ['evidence/B10_WORKER_DELTA.diff', 'evidence/B10_SERVICE_DELTA.diff','evidence/B10_CONTENT_DELTA.diff']:
        for name, patch in helper.split_multi_diff(saved[rel]):
            if name not in c['postimages'] or name in seen:
                raise ValueError('Unexpected/duplicate production delta')
            result[name] = helper.apply_exact(base[name], patch, name)
            if sha(result[name]) != c['postimages'][name]:
                raise ValueError('Wrong postimage: ' + name)
            seen.add(name)
    if seen != set(c['postimages']) or sha(inventory(result).encode()) != c['b10_tree']:
        raise ValueError('B10 composition mismatch')
    if result['manifest.json'] != base['manifest.json']:
        raise ValueError('Unexpected permissions/version change')
    harness = helper.apply_exact(saved['qa/b9_full_worker_harness.mjs'], saved['evidence/B10_HARNESS_DELTA.diff'], 'b9_full_worker_harness.mjs')
    if sha(harness) != c['harness_sha256']:
        raise ValueError('Wrong controlled QA harness')
    outputs = {'candidate/full/' + k: v for k, v in result.items()}
    for name in ['b10_deferred.test.mjs', 'b10_legacy.test.mjs', 'b10_content_contract.test.mjs', 'b9_full_worker_harness.mjs', 'b9_full_worker.test.mjs', 'idb_artifact_fixture.mjs']:
        outputs['qa/' + name] = saved['qa/' + name]
    outputs['qa/b10_full_worker_harness.mjs'] = harness
    outputs['inputs/idb_test_double.mjs'] = saved['qa/idb_test_double.mjs']
    outputs['SOURCE_TREE_SHA256.txt'] = inventory(result).encode()
    outputs['RECONSTRUCTION.json'] = (json.dumps({'source_tree_sha256': c['b10_tree'], 'files': 67, 'changed_production_files': sorted(seen), 'provider_calls': 0, 'release_allowed': False}, indent=2) + '\n').encode()
    for rel, value in outputs.items():
        p = output / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(value)
    (output / 'evidence').mkdir(exist_ok=True)
    print('B10 exact QA reconstruction PASS: 67 files; four changed; no ZIP')
if __name__ == '__main__':
    main()
