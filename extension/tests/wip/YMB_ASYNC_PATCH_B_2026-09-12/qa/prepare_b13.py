"""Restore exact B13 QA from B12. Usage: prepare_b13.py B12_QA EMPTY_OUTPUT.
No provider calls, browser launch or installable packaging. Checks all inputs first.
"""
from pathlib import Path, PurePosixPath
import hashlib, importlib.util, io, json, sys, tarfile
ROOT = Path(__file__).resolve().parent.parent
BASE = '73e6ed85bfd843bf2590a2d1a44a9d04224ce5f63563d127bcd35c2ad092eeec'
TARGET = 'f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47'
sha = lambda b: hashlib.sha256(b).hexdigest()
def checked(p, expected):
    data = p.read_bytes()
    if sha(data) != expected: raise ValueError('Input hash mismatch: ' + str(p))
    return data

def files(root):
    if not root.is_dir() or any(p.is_symlink() for p in root.rglob('*')): raise ValueError('Missing/unsafe tree')
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob('*')) if p.is_file()}
def identity(data):
    return sha(''.join(sha(v)+'  '+n+'\n' for n,v in sorted(data.items())).encode())

def delta_function():
    helper = ROOT / 'qa/prepare_b8.py'
    checked(helper, 'faa185b98f010d672b2f87b9b928b3dd2c82ac5842b4ad054a3c227cc4a797b6')
    spec=importlib.util.spec_from_file_location('b13_preserved_delta', helper)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.delta

def main():
    if len(sys.argv)!=3: raise SystemExit(__doc__)
    sys.dont_write_bytecode=True
    prior,out=map(lambda p:Path(p).resolve(),sys.argv[1:])
    if out.exists() and (not out.is_dir() or any(out.iterdir())): raise ValueError('Nonempty output')
    full=files(prior/'candidate/full')
    if identity(full)!=BASE or len(full)!=67: raise ValueError('Wrong B12 input')
    qa=files(prior/'qa'); inputs=files(prior/'inputs')
    m=json.loads(checked(ROOT/'evidence/B13_INPUTS.json',MANIFEST_SHA))
    if {n:sha(v) for n,v in qa.items()}!=m['inherited_qa'] or {n:sha(v) for n,v in inputs.items()}!=m['inherited_inputs']: raise ValueError('Changed inherited QA')
    delta=delta_function()
    for name,c in m['production_changes'].items():
        if sha(full[name])!=c['before']: raise ValueError('Preimage mismatch')
        patch=checked(ROOT/c['delta'],c['delta_sha256']);full[name]=delta(full[name],patch,name)
        if sha(full[name])!=c['after']: raise ValueError('Postimage mismatch')
    if identity(full)!=TARGET: raise ValueError('Wrong resulting B13')
    archive=checked(ROOT/'qa/B13_QA_INPUTS.tar.xz',m['qa_archive_sha256'])
    members={}
    with tarfile.open(fileobj=io.BytesIO(archive),mode='r:xz') as tar:
        for e in tar:
            path=PurePosixPath(e.name)
            if not e.isfile() or path.is_absolute() or '..' in path.parts or e.name in members or e.size>1000000: raise ValueError('Unsafe QA archive')
            members[e.name]=tar.extractfile(e).read()
    if {n:sha(v) for n,v in members.items()}!=m['qa_archive_members']: raise ValueError('QA archive member mismatch')
    output={**{'candidate/full/'+n:v for n,v in full.items()},**{'qa/'+n:v for n,v in qa.items()},**{'inputs/'+n:v for n,v in inputs.items()},**members}
    output['evidence/B13_TREE_SHA256.txt']=''.join(sha(v)+'  '+n+'\n' for n,v in sorted(full.items())).encode()
    for n,v in output.items():
        dest=out/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(v)
    print('Exact B13 QA restored: 67 production files, 2 changed; no ZIP. '+TARGET)
MANIFEST_SHA = 'd9ba56c114becbd0945e20de523f1a53dd6150d94a7ec17f1fd5b6b88ac7d3a8'
if __name__=='__main__': main()
