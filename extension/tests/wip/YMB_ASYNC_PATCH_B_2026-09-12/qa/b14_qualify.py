"""Internal B13 package qualification, NOT independent acceptance or owner release.
Usage: b14_qualify.py SOURCE_REPO NEW_EMPTY_OUTPUT [--run-tests]
Produces one exact QA artifact with the known executable packer. No browser launch,
provider calls, credentials, source edits or owner file handling. Rejects wrong inputs.
"""
from pathlib import Path, PurePosixPath
import hashlib, importlib.util, io, json, os, shutil, stat, subprocess, sys, tarfile, zipfile
HERE = Path(__file__).resolve().parent
WIP = 'extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12'
A = 'extension/tests/wip/YMB_FILE_DELIVERY_PATCH_A_2026-09-12'
TARGET = 'f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47'
PACKER_SHA = 'fc0555f8ae60b67e2128e994127398ee0ccd9438b13b57fffd80b1834b62dd62'
ROOT_NAME = 'ymb-b13-internal-qa-not-for-installation'
ZIP_SHA = 'e260f35b1d7decf02c18c46103b4072de68270c2bce09e2f51f7462941c48f97'
ZIP_BYTES = 223380
PREPARERS = {
  9:'a1b2328e967ac79a06597be45961ca7432e9aa9d702685045fea0ec2d271dd8a',
  10:'1116f7b5a9393a278849d184722c614a057db4aec56e9ebd2ef6cc85e672393e',
  11:'60bf9c8f61f806390612fca0cf7a92e3428888c72642449dc3cd0e7f41a0bb11',
  12:'4d336a81356ee6186d90e330cab9a4f87eb614e493978e07ef02c08b03b761c5',
  13:'97beb82b83fef17b54662f39b8e7a245b015403341d2fa4a4756780cb328864c'
}
sha = lambda b: hashlib.sha256(b).hexdigest()
def checked(p, expected):
    data = p.read_bytes()
    if p.is_symlink() or sha(data) != expected: raise ValueError('Input identity: '+str(p))
    return data

def inventory(root):
    if not root.is_dir() or root.is_symlink() or any(p.is_symlink() for p in root.rglob('*')): raise ValueError('Unsafe source tree')
    return {p.relative_to(root).as_posix():p.read_bytes() for p in sorted(root.rglob('*')) if p.is_file()}

def identity(data): return sha(''.join(sha(v)+'  '+k+'\n' for k,v in sorted(data.items())).encode())

def load_inputs(repo):
    packer = checked(HERE/'b14_canonical_packer_exact.py', PACKER_SHA)
    manifest = checked(repo/A/'BASELINE_TREE_SHA256.txt', '1ef7d90e1e07088d82b874b5ab888579f50050b0baa7ebd39dfce1e08950d4db')
    expected = {n.removeprefix('./'):h for h,n in (line.split('  ',1) for line in manifest.decode().splitlines())}
    base = inventory(HERE/'b14_inputs/owner014')
    if len(base)!=53 or set(base)!=set(expected) or any(sha(v)!=expected[n] for n,v in base.items()): raise ValueError('Wrong exact owner014 bytes')
    for i,h in PREPARERS.items(): checked(repo/WIP/f'qa/prepare_b{i}.py',h)
    return base,packer

def verify_package(path, source, expected_sha=ZIP_SHA, expected_bytes=ZIP_BYTES):
    raw = path.read_bytes()
    if (expected_sha is not None and sha(raw)!=expected_sha) or (expected_bytes is not None and len(raw)!=expected_bytes): raise ValueError('Archive identity mismatch')
    if len(source)!=67 or identity(source)!=TARGET: raise ValueError('Wrong source identity')
    dirs = sorted({str(PurePosixPath(n).parent) for n in source if str(PurePosixPath(n).parent)!='.'})
    expected = [ROOT_NAME+'/']+[ROOT_NAME+'/'+n+'/' for n in dirs]+[ROOT_NAME+'/'+n for n in sorted(source)]
    recovered = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if z.comment or z.namelist()!=expected or len(set(z.namelist()))!=len(expected): raise ValueError('Unexpected archive paths/order')
        for e in z.infolist():
            isdir = e.is_dir()
            attr = ((stat.S_IFDIR|0o755)<<16)|0x10 if isdir else (stat.S_IFREG|0o644)<<16
            if e.create_system!=3 or e.external_attr!=attr or e.date_time!=(2025,12,31,19,0,0) or e.extra or e.comment or e.flag_bits!=0 or e.internal_attr!=0 or e.volume!=0 or e.reserved!=0 or e.create_version!=20 or e.extract_version!=20: raise ValueError('ZIP metadata mismatch')
            if e.compress_type!=(zipfile.ZIP_STORED if isdir else zipfile.ZIP_DEFLATED): raise ValueError('Wrong compression')
            if isdir:
                if e.file_size!=0: raise ValueError('Nonempty directory entry')
            else:
                name = e.filename[len(ROOT_NAME)+1:]
                if e.file_size!=len(source[name]): raise ValueError('File size mismatch')
                b = z.read(e)
                if b!=source[name]: raise ValueError('File bytes mismatch')
                recovered[name]=b
        if z.testzip() is not None: raise ValueError('Corrupt ZIP')
    return recovered

def main():
    if len(sys.argv) not in (3,4) or (len(sys.argv)==4 and sys.argv[3]!='--run-tests'): raise SystemExit(__doc__)
    repo,out = [Path(x).absolute() for x in sys.argv[1:3]]
    if out.is_symlink() or (out.exists() and (not out.is_dir() or any(out.iterdir()))): raise ValueError('Refusing existing work')
    base,packer_bytes = load_inputs(repo)
    out.mkdir(parents=True,exist_ok=True);work=out/'work';work.mkdir();payload=out/'payload';payload.mkdir()
    def write_tree(root,data):
        for n,b in data.items(): p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    owner=work/'owner014';write_tree(owner,base)
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    prev=owner
    for i in PREPARERS:
        dest=work/f'b{i}'
        cp=subprocess.run([sys.executable,str(repo/WIP/f'qa/prepare_b{i}.py'),str(prev),str(dest)],capture_output=True,env=env,timeout=30)
        (work/f'prepare{i}.stdout').write_bytes(cp.stdout);(work/f'prepare{i}.stderr').write_bytes(cp.stderr)
        if cp.returncode: raise ValueError('Saved materializer failed '+str(i)+': '+cp.stderr.decode(errors='replace'))
        prev=dest
    source=inventory(prev/'candidate/full')
    if identity(source)!=TARGET: raise ValueError('Candidate changed')
    packer_path=work/'canonical_packer_exact.py';packer_path.write_bytes(packer_bytes)
    spec=importlib.util.spec_from_file_location('preserved_packer',packer_path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    # Only candidate-specific parameters change; pack/make_info implementation is byte-identical.
    m.ROOT=ROOT_NAME;m.EXPECTED_FILES=67
    staging=work/ROOT_NAME;write_tree(staging,source)
    artifact=payload/'candidate-internal-qa.zip'
    m.pack(staging,artifact);m.pack(staging,work/'repeat.zip')
    if artifact.read_bytes()!=(work/'repeat.zip').read_bytes(): raise ValueError('Non-deterministic package')
    fresh=verify_package(artifact,source)
    freshqa=out/'fresh_qa';write_tree(freshqa/'candidate/full',fresh)
    for d in ['qa','inputs']: shutil.copytree(prev/d,freshqa/d)
    for p in prev.iterdir():
        if p.is_file(): shutil.copyfile(p,freshqa/p.name)
    package={'schema':1,'candidate_tree_sha256':TARGET,'sha256':sha(artifact.read_bytes()),'bytes':artifact.stat().st_size,'files':67,'archive_root':ROOT_NAME,'canonical_packer_sha256':PACKER_SHA,'source_head':'c828c2ea2a7e412207f7cf7078f48b30919435c5','compression':'ZIP_DEFLATED level 9; directories ZIP_STORED','stamp':[2025,12,31,19,0,0],'entries':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in sorted(source.items())],'not_for_owner_installation':True,'release_allowed':False}
    (payload/'PACKAGE_IDENTITY.json').write_text(json.dumps(package,indent=2)+'\n')
    if '--run-tests' in sys.argv:
        campaign=repo/WIP/'qa/b13_available_campaign.py';checked(campaign,'79a48c45900c9587c9f11d696065f8501a9cbc3d9f28c73ec8d764310cc92651')
        cp=subprocess.run([sys.executable,str(campaign),str(repo),str(owner),str(freshqa),str(out/'packaged_test_logs')],capture_output=True,env=env,timeout=180)
        (out/'campaign.stdout').write_bytes(cp.stdout);(out/'campaign.stderr').write_bytes(cp.stderr)
        if cp.returncode: raise ValueError('Packaged campaign failed: '+cp.stderr.decode(errors='replace'))
    if inventory(freshqa/'candidate/full')!=source or inventory(staging)!=source: raise ValueError('Mutation during qualification')
    print(json.dumps({k:v for k,v in package.items() if k!='entries'},indent=2))
if __name__=='__main__': sys.dont_write_bytecode=True;main()
