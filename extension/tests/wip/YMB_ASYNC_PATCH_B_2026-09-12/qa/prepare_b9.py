"""Restore exact A+B9 QA tree; never a release package.
Usage: python qa/prepare_b9.py EXTRACTED_OWNER_014_BASELINE EMPTY_OUTPUT_DIR
No network, secrets, provider calls, fuzzy patching or overwrite of existing work.
"""
from pathlib import Path
import hashlib
import json
import sys
import types

ROOT = Path(__file__).resolve().parent.parent
A_ROOT = ROOT.parent / 'YMB_FILE_DELIVERY_PATCH_A_2026-09-12'
MANIFEST_SHA = '7ddd7e15e4845271f35e50d1c64682f25df7becdecbfc487989799fcaf72169e'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inventory(data):
    return ''.join(sha(value) + '  ' + name + '\n' for name, value in sorted(data.items()))

def files_under(root):
    if not root.is_dir() or root.is_symlink():
        raise ValueError('Expected real directory: ' + str(root))
    paths = sorted(root.rglob('*'))
    if any(p.is_symlink() for p in paths):
        raise ValueError('Symlink input rejected')
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in paths if p.is_file()}

def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    baseline, output = [Path(p).absolute() for p in sys.argv[1:]]
    if output.is_symlink() or (output.exists() and (not output.is_dir() or any(output.iterdir()))):
        raise ValueError('Refusing nonempty or symlink output')
    manifest_bytes = (ROOT / 'evidence/B9_INPUTS_SHA256.json').read_bytes()
    if sha(manifest_bytes) != MANIFEST_SHA:
        raise ValueError('Wrong saved B9 input manifest')
    config = json.loads(manifest_bytes)
    base = files_under(baseline)
    if len(base) != config['baseline_files'] or sha(inventory(base).encode()) != config['baseline_tree_sha256']:
        raise ValueError('Wrong exact 53-file owner 0.1.4 baseline')
    saved = {}
    for name, expected in config['inputs'].items():
        prefix, rel = name.split('/', 1)
        if prefix not in ('A', 'B') or Path(rel).is_absolute() or '..' in Path(rel).parts:
            raise ValueError('Unsafe input path')
        path = (A_ROOT if prefix == 'A' else ROOT) / rel
        if path.is_symlink():
            raise ValueError('Symlink input rejected')
        value = path.read_bytes()
        if sha(value) != expected:
            raise ValueError('Saved input hash mismatch: ' + name)
        saved[name] = value
    # Reuse the already saved exact-delta parser only AFTER its hash was checked.
    helper = types.ModuleType('b9_exact_delta_helper')
    helper.__file__ = str(ROOT / 'qa/prepare_b6.py')
    exec(compile(saved['B/qa/prepare_b6.py'], helper.__file__, 'exec'), helper.__dict__)
    result = dict(base)
    for name, value in saved.items():
        if name.startswith('A/candidate_changed_files/') and not name.endswith('.patch'):
            result[name.removeprefix('A/candidate_changed_files/')] = value
    patch = saved['A/candidate_changed_files/content_script.patch'].splitlines(keepends=True)
    result['content_script.js'] = helper.apply_exact(base['content_script.js'], b'--- a/content_script.js\n+++ b/content_script.js\n' + b''.join(patch[2:]), 'content_script.js')
    expected_a = {name.removeprefix('./'): digest for digest, name in [line.split('  ', 1) for line in saved['A/CANDIDATE2_TREE_SHA256.txt'].decode().splitlines()]}
    # Explicit known identity discrepancy: stored A bootstrap has exactly one extra LF.
    boot = 'phase3_service_worker_bootstrap.js'
    repaired_a_lf = False
    if sha(result[boot]) != expected_a[boot]:
        if not result[boot].endswith(b'\n') or sha(result[boot][:-1]) != expected_a[boot]:
            raise ValueError('Unreconciled Patch A bootstrap identity')
        result[boot] = result[boot][:-1]
        repaired_a_lf = True
    if set(result) != set(expected_a) or any(sha(v) != expected_a[k] for k, v in result.items()):
        raise ValueError('Patch A exact 57-file verification failed')
    for name, patch in helper.split_multi_diff(saved['B/evidence/B5_LEGACY_DELTA.diff']):
        result[name] = helper.apply_exact(base[name], patch, name)
        if sha(result[name]) != helper.B5_POST[name]:
            raise ValueError('Legacy postimage mismatch')
    for name in ['search_async_policy.js', 'search_legacy_admission.js']:
        result['shared/' + name] = saved['B/candidate/b5/' + name]
    for name in ['search_async_transport.js', 'search_async_runtime.js', 'search_async_normalizer.js']:
        result['shared/' + name] = saved['B/candidate/shared/' + name]
    result['shared/search_async_store.js'] = helper.apply_exact(saved['B/candidate/shared/search_async_store.js'], saved['B/evidence/B3_STORE_DELTA.diff'], 'search_async_store.js')
    result['shared/search_async_protocol.js'] = helper.apply_exact(saved['B/candidate/shared/search_async_protocol.js'], saved['B/evidence/B8_search_async_protocol.js.diff'], 'search_async_protocol.js')
    result['search_async_worker_transport.js'] = helper.apply_exact(saved['B/candidate/b7/search_async_worker_transport.js'], saved['B/evidence/B8_search_async_worker_transport.js.diff'], 'search_async_worker_transport.js')
    result['search_admission_worker_binding.js'] = helper.apply_exact(saved['B/candidate/b6/search_admission_worker_binding.js'], saved['B/evidence/B7_BINDING_DELTA.diff'], 'search_admission_worker_binding.js')
    result['shared/search_async_export.js'] = saved['B/candidate/b8/search_async_export.js']
    result[boot] = saved['B/candidate/b9/' + boot]
    full_manifest = inventory(result)
    if len(result) != config['candidate_files'] or sha(full_manifest.encode()) != config['candidate_tree_sha256']:
        raise ValueError('Combined candidate inventory/hash mismatch')
    manifest = json.loads(result['manifest.json'])
    refs = [manifest['background']['service_worker']]
    for group in manifest['content_scripts']:
        refs.extend(group.get('js', [])); refs.extend(group.get('css', []))
    if any(p not in result for p in refs):
        raise ValueError('Manifest references missing file')
    if 'https://operation.api.cloud.yandex.net/*' in manifest['host_permissions'] or 'alarms' in manifest['permissions']:
        raise ValueError('Unexpected capability enablement')
    outputs = {'candidate/full/' + k: v for k, v in result.items()}
    for name in ['b9_full_worker_harness.mjs', 'b9_full_worker.test.mjs', 'idb_artifact_fixture.mjs']:
        outputs['qa/' + name] = saved['B/qa/' + name]
    outputs['inputs/idb_test_double.mjs'] = saved['B/qa/idb_test_double.mjs']
    outputs['SOURCE_TREE_SHA256.txt'] = full_manifest.encode()
    outputs['RECONSTRUCTION.json'] = (json.dumps({'candidate_files': len(result), 'source_tree_sha256': config['candidate_tree_sha256'], 'patch_a_files_verified': 57, 'known_patch_a_extra_final_lf_reconciled': repaired_a_lf, 'inputs_verified': len(saved), 'release_allowed': False}, indent=2) + '\n').encode()
    # All input, delta and output verification completes before the first file write.
    for name, value in outputs.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value)
    print('B9_EXACT_QA_COMPOSITION=PASS; 67 candidate files; NO ZIP; RELEASE_ALLOWED=NO')
    print('YMB_FULL=' + str(output / 'candidate/full') + ' YMB_IDB_FIXTURE=' + str(output / 'qa/idb_artifact_fixture.mjs') + ' node --test ' + str(output / 'qa/b9_full_worker.test.mjs'))

if __name__ == '__main__':
    main()
