"""Restore exact B8 QA from saved repository bytes; NOT an installable extension.
Usage: python qa/prepare_b8.py EXTRACTED_OWNER_014_BASELINE EMPTY_OUTPUT_DIR
Run from the saved YMB_ASYNC_PATCH_B_2026-09-12 subtree with its Patch A sibling.
No network, fuzzy patching, code generation by the model, or provider calls.
"""
from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
A = ROOT.parent / 'YMB_FILE_DELIVERY_PATCH_A_2026-09-12/candidate_changed_files/shared/file_artifact_store.js'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def checked(path, expected):
    data = path.read_bytes()
    if sha(data) != expected:
        raise ValueError('Exact input hash mismatch: ' + str(path))
    return data

def delta(before, patch, target):
    old = before.decode('utf-8').splitlines(keepends=True)
    lines = patch.decode('utf-8').splitlines(keepends=True)
    if lines[:2] != ['--- a/' + target + '\n', '+++ b/' + target + '\n']:
        raise ValueError('Wrong delta target')
    pos, cursor, result = 2, 0, []
    while pos < len(lines):
        m = re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*\n', lines[pos])
        if not m:
            raise ValueError('Malformed delta')
        start, count, new_start, new_count = [int(x or 1) for x in m.groups()]
        if start - 1 < cursor:
            raise ValueError('Overlapping delta')
        result.extend(old[cursor:start - 1]); cursor = start - 1
        if len(result) != new_start - 1:
            raise ValueError('Postimage offset mismatch')
        removed = added = 0; pos += 1
        while pos < len(lines) and not lines[pos].startswith('@@ '):
            line = lines[pos]
            if line[0] in ' -':
                if cursor >= len(old) or old[cursor] != line[1:]:
                    raise ValueError('Preimage mismatch; no fuzz allowed')
                cursor += 1; removed += 1
            if line[0] in ' +':
                result.append(line[1:]); added += 1
            if line[0] not in ' +-':
                raise ValueError('Unknown delta instruction')
            pos += 1
        if (removed, added) != (count, new_count):
            raise ValueError('Hunk count mismatch')
    result.extend(old[cursor:])
    return ''.join(result).encode('utf-8')

def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    baseline, out = map(lambda p: Path(p).resolve(), sys.argv[1:])
    if out.exists() and any(out.iterdir()):
        raise ValueError('Refusing nonempty output')
    data = {}
    # Frozen ACTUAL B7 blob, not the mismatched hash in the old report.
    data['inputs/search_async_worker_transport.js'] = checked(ROOT / 'candidate/b7/search_async_worker_transport.js', '5096aef1c747050a99aebb4e8d16cb9ce14694a111e50a0e33437a601abd107e')
    data['inputs/search_async_protocol.js'] = checked(ROOT / 'candidate/shared/search_async_protocol.js', 'f4b8dbfced3ed1136355c805bb5fc83cd39472b44e91faf0639ec766f9c0ffec')
    data['inputs/file_artifact_store.js'] = checked(A, '6d618f6d7d47490af924a580145d7177ef3128804e202e0dc9c5c2149c609252')
    data['inputs/idb_test_double.mjs'] = checked(ROOT / 'qa/idb_test_double.mjs', '1327c21fca17b0a34ebec3a8234c9721d1f09192f00bd862cffdbf1548d025af')
    data['inputs/b7_worker.test.mjs'] = checked(ROOT / 'qa/b7_worker.test.mjs', '3d0249cd36b45e038c8127bab4e192aae227449d757e38416dbef3efa8430b3c')
    data['baseline/shared/search_protocol.js'] = checked(baseline / 'shared/search_protocol.js', '48cb17f0a846f87e2057d65945dce23788e5c3c90810b7542557d762c2f301b7')
    data['qa/block_command_discovery.js'] = checked(baseline / 'shared/block_command_discovery.js', '179700660b5960adf5bdd352104673166ce7fdc2e0a11ecf78222495642a82d1')
    data['candidate/b8/search_async_export.js'] = checked(ROOT / 'candidate/b8/search_async_export.js', '8adabdea50d497706560f2bd080c9c99ba52bdfbcd23fced0ff24717041eddfc')
    changes = {
        'search_async_worker_transport.js': ('a735623d06a526d6b77a29f2d3d33b9a68eb975e1e294e44e4c86448ece56b71', '11a9e0cfe0e1efdb7b58b883138849ee8ebd2f2102b1a8aad3c3d80889802d13'),
        'search_async_protocol.js': ('71de79532435dfc90b5b0b21a4f0a363175a8aca8f77cb50316fabdec33854ca', '8bcaa1796a6e75ce9c868cce1783e1e416b6f43d8d5208b324f0fdbafbaf6964')
    }
    for name, (patch_hash, post_hash) in changes.items():
        patch = checked(ROOT / 'evidence' / ('B8_' + name + '.diff'), patch_hash)
        post = delta(data['inputs/' + name], patch, name)
        if sha(post) != post_hash:
            raise ValueError('Postimage mismatch: ' + name)
        data['candidate/b8/' + name] = post
    tests = {
        'b8_export.test.mjs': 'e93ece8c97b019b21be3eb805c977c1e59aa6a30d21b5064ba7cadbdb5a0b3a7',
        'b8_artifact.test.mjs': '6a2c967cbfdd642884bdca32bf49ff23bc1ced79bbcb3f8668a0fc252e83d546',
        'b8_worker.test.mjs': 'd1cf8c62ce4796ca22c88832e01bdcda34489a9f359f8a7aa99c08c90a16cf83',
        'idb_artifact_fixture.mjs': 'adf32baf310276ffcf4205f01310129e9ff4b7ee01acabd87c13b6530eafe246',
        'b8_resource.mjs': '39008d7fda6343f72db669d0010dd339012b4287f7b586c67d905ac7b0f45106'
    }
    for name, expected in tests.items():
        data['qa/' + name] = checked(ROOT / 'qa' / name, expected)
    # Run the 26 historical assertions UNCHANGED against the B8 postimage in QA.
    data['candidate/b7/search_async_worker_transport.js'] = data['candidate/b8/search_async_worker_transport.js']
    data['qa/b7_worker.test.mjs'] = data['inputs/b7_worker.test.mjs']
    # Reuse the existing fixture prefix, with explicit dependency injection for new tests.
    helper = data['inputs/b7_worker.test.mjs'].decode().split("test('non-async block delegates")[0]
    helper = helper.replace('const worker=F.create({', 'const deps={', 1)
    helper = helper.replace(' });\n return{state,calls,worker,summary,binding,runtime,store};', ' };\n const worker=F.create({...deps,...(overrides.deps||{})});\n return{state,calls,worker,summary,binding,runtime,store,deps};', 1)
    helper += '\nexport { harness, manual, commandText, KEY, CID, context, F };\n'
    data['qa/harness_b8.mjs'] = helper.encode()
    if sha(data['qa/harness_b8.mjs']) != 'ea11a3043b2c6733872fb9486e1bf8758e2b69e0ef53d35666d29eb39c121516':
        raise ValueError('Harness adaptation mismatch')
    # ALL validation happens before writing the output tree.
    for name, value in data.items():
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(value)
    (out / 'evidence').mkdir(exist_ok=True)
    (out / 'EXACT_TREE_SHA256.txt').write_text(''.join(sha(v) + '  ' + k + '\n' for k, v in sorted(data.items())))
    print('B8 exact QA reconstruction PASS; files=' + str(len(data)) + '; no installable manifest/ZIP')
    print('node --test ' + str(out / 'qa') + '/b7_worker.test.mjs ' + str(out / 'qa') + '/b8*.test.mjs')

if __name__ == '__main__':
    main()
