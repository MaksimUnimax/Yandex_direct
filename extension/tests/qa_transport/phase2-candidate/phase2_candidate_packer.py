#!/usr/bin/env python3
import argparse, hashlib, json, shutil, stat, zipfile
from pathlib import Path

ROOT_NAME = "yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate"
FIXED_DT = (2025, 12, 31, 19, 0, 0)
EXPECTED_ZIP_SHA256 = "d74c4fc805b9e92a76044b88505ea792d90761b66f0e817ac9b0cbdacd42b04e"
EXPECTED_ZIP_BYTES = 139422
EXPECTED_FILES = 54
EXPECTED_ENTRIES = 57
FROZEN_MANIFEST_REL = Path("extension/tests/qa_transport/phase2-candidate/EXACT_CANDIDATE_MANIFEST_2026-08-23.json")

def sha256_bytes(data): return hashlib.sha256(data).hexdigest()

def zipinfo(name, is_dir):
    zi=zipfile.ZipInfo(name,FIXED_DT); zi.create_system=3; zi.create_version=20; zi.extract_version=20
    zi.flag_bits=0; zi.internal_attr=0; zi.extra=b""; zi.comment=b""
    if is_dir:
        zi.compress_type=zipfile.ZIP_STORED; zi.external_attr=((stat.S_IFDIR|0o755)<<16)|0x10
    else:
        zi.compress_type=zipfile.ZIP_DEFLATED; zi.external_attr=(stat.S_IFREG|0o644)<<16
    return zi

def selected_files(repo):
    src=repo/'extension'/'src'; tests=repo/'extension'/'tests'; rows=[]
    for file in sorted(p for p in src.rglob('*') if p.is_file()): rows.append((file.relative_to(src).as_posix(),file))
    for file in sorted(tests.glob('*.test.mjs')): rows.append((f'tests/{file.name}',file))
    return rows

def payload_manifest(rows):
    out=[]
    for rel,file in rows:
        data=file.read_bytes(); out.append({'path':rel,'bytes':len(data),'sha256':sha256_bytes(data)})
    return out

def load_frozen_manifest(repo):
    frozen=json.loads((repo/FROZEN_MANIFEST_REL).read_text(encoding='utf-8'))
    if frozen.get('root_name')!=ROOT_NAME: raise SystemExit('FROZEN_MANIFEST_ROOT_FAIL')
    if frozen.get('sha256')!=EXPECTED_ZIP_SHA256 or int(frozen.get('bytes',-1))!=EXPECTED_ZIP_BYTES: raise SystemExit('FROZEN_MANIFEST_ARTIFACT_IDENTITY_FAIL')
    if int(frozen.get('files',-1))!=EXPECTED_FILES or int(frozen.get('entries',-1))!=EXPECTED_ENTRIES: raise SystemExit('FROZEN_MANIFEST_COUNT_FAIL')
    if len(frozen.get('payload') or [])!=EXPECTED_FILES: raise SystemExit('FROZEN_MANIFEST_PAYLOAD_COUNT_FAIL')
    return frozen

def verify_source_against_frozen(repo,rows):
    frozen=load_frozen_manifest(repo); expected={x['path']:x for x in frozen['payload']}; actual={x['path']:x for x in payload_manifest(rows)}
    if set(actual)!=set(expected): raise SystemExit(f"FROZEN_SOURCE_PATH_SET_FAIL missing={sorted(set(expected)-set(actual))} extra={sorted(set(actual)-set(expected))}")
    for rel in sorted(expected):
        if actual[rel]!=expected[rel]: raise SystemExit(f'FROZEN_SOURCE_IDENTITY_FAIL {rel}: {actual[rel]} != {expected[rel]}')
    return frozen

def build(repo,output,manifest_output=None,discover=False):
    rows=selected_files(repo); frozen=None if discover else verify_source_against_frozen(repo,rows); manifest=payload_manifest(rows)
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
        z.comment=b''
        for d in sorted({ROOT_NAME+'/',ROOT_NAME+'/shared/',ROOT_NAME+'/tests/'}): z.writestr(zipinfo(d,True),b'')
        for rel,file in sorted(rows,key=lambda x:x[0]): z.writestr(zipinfo(f'{ROOT_NAME}/{rel}',False),file.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    data=output.read_bytes()
    with zipfile.ZipFile(output,'r') as z:
        bad=z.testzip(); files=sum(1 for i in z.infolist() if not i.filename.endswith('/')); entries=len(z.infolist())
    result={'root_name':ROOT_NAME,'sha256':sha256_bytes(data),'bytes':len(data),'files':files,'entries':entries,'zip_test':bad or 'PASS','payload':manifest}
    if manifest_output: manifest_output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if bad is not None: raise SystemExit(f'ZIP_INTEGRITY_FAIL: {bad}')
    if not discover:
        if result['sha256']!=EXPECTED_ZIP_SHA256 or result['bytes']!=EXPECTED_ZIP_BYTES: raise SystemExit(f"EXACT_ARTIFACT_HASH_FAIL {result['sha256']}/{result['bytes']}")
        if result['files']!=EXPECTED_FILES or result['entries']!=EXPECTED_ENTRIES: raise SystemExit(f"EXACT_ARTIFACT_COUNT_FAIL {result['files']}/{result['entries']}")
        if result['payload']!=frozen['payload']: raise SystemExit('EXACT_ARTIFACT_PAYLOAD_MANIFEST_FAIL')
    return result

def verify_extraction(repo,archive,extract_dir,manifest):
    if extract_dir.exists(): shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True)
    with zipfile.ZipFile(archive,'r') as z: z.extractall(extract_dir)
    root=extract_dir/ROOT_NAME; expected={x['path']:x for x in manifest['payload']}; actual={}
    for file in sorted(p for p in root.rglob('*') if p.is_file()):
        rel=file.relative_to(root).as_posix(); data=file.read_bytes(); actual[rel]={'path':rel,'bytes':len(data),'sha256':sha256_bytes(data)}
    if set(actual)!=set(expected): raise SystemExit(f"PACKAGE_PATH_SET_FAIL missing={sorted(set(expected)-set(actual))} extra={sorted(set(actual)-set(expected))}")
    for rel in sorted(expected):
        if actual[rel]!=expected[rel]: raise SystemExit(f'PACKAGE_BYTE_IDENTITY_FAIL {rel}: {actual[rel]} != {expected[rel]}')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',required=True); ap.add_argument('--output',required=True); ap.add_argument('--manifest-output'); ap.add_argument('--verify-extract'); ap.add_argument('--discover',action='store_true'); args=ap.parse_args()
    repo=Path(args.repo_root).resolve(); output=Path(args.output).resolve(); manifest_path=Path(args.manifest_output).resolve() if args.manifest_output else None
    result=build(repo,output,manifest_path,args.discover)
    if args.verify_extract: verify_extraction(repo,output,Path(args.verify_extract).resolve(),result if args.discover else load_frozen_manifest(repo))
    print(f"artifact={output}"); print(f"sha256={result['sha256']}"); print(f"bytes={result['bytes']}"); print(f"files={result['files']}"); print(f"entries={result['entries']}"); print(f"zip_test={result['zip_test']}")
    print('DISCOVERED_CANDIDATE_IDENTITY' if args.discover else 'EXACT_ARTIFACT_IDENTITY_PASS')
    if args.verify_extract: print('SOURCE_PACKAGE_IDENTITY_PASS')
if __name__=='__main__': main()
