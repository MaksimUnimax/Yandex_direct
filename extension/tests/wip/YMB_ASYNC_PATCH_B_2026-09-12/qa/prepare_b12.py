"""Restore exact B12 QA from exact B11. No release ZIP or installed extension.
Usage: python qa/prepare_b12.py EXACT_B11_QA EMPTY_OUTPUT
"""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def tree(root):
    if not root.is_dir() or any(p.is_symlink() for p in root.rglob('*')):raise ValueError('Missing/unsafe tree')
    files={p.relative_to(root).as_posix():p.read_bytes() for p in sorted(root.rglob('*')) if p.is_file()}
    return files,sha(''.join(sha(v)+'  '+n+'\n' for n,v in files.items()).encode())
def checked(path,expected):
    data=path.read_bytes()
    if sha(data)!=expected:raise ValueError('Input changed: '+str(path))
    return data

def main():
    if len(sys.argv)!=3:raise SystemExit(__doc__)
    prior,out=map(lambda p:Path(p).resolve(),sys.argv[1:])
    if out.exists() and (not out.is_dir() or any(out.iterdir())):raise ValueError('Refusing nonempty output')
    m=json.loads(checked(ROOT/'evidence/B12_INPUTS.json',MANIFEST_SHA))
    files,identity=tree(prior/'candidate/full')
    if identity!=m['baseline_b11_tree_sha256']:raise ValueError('Wrong B11')
    data={n:checked(ROOT/n,h) for n,h in m['inputs'].items()}
    qa={n:checked(prior/'qa'/n,h) for n,h in m['inherited_qa'].items()}
    inputs={n:checked(prior/'inputs'/n,h) for n,h in m['inherited_inputs'].items()}
    for n in m['changed_files']:files[n]=data['candidate/b12/'+n]
    final=sha(''.join(sha(v)+'  '+n+'\n' for n,v in sorted(files.items())).encode())
    if final!=m['candidate_b12_tree_sha256'] or len(files)!=m['candidate_count']:raise ValueError('B12 postimage mismatch')
    outputs={**{'candidate/full/'+n:v for n,v in files.items()},**{'qa/'+n:v for n,v in qa.items()},**{'inputs/'+n:v for n,v in inputs.items()},'qa/b12_contract.test.mjs':data['qa/b12_contract.test.mjs']}
    for name,value in outputs.items():
        p=out/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(value)
    (out/'evidence').mkdir(exist_ok=True)
    (out/'evidence/B12_TREE_SHA256.txt').write_bytes(''.join(sha(v)+'  '+n+'\n' for n,v in sorted(files.items())).encode())
    print('Exact B12 QA restored: 67 files, two documentation changes, 61 JS unchanged. NO ZIP.')
MANIFEST_SHA='c1b6478ef9fd6807576f29bd08fbbc3c41577b3f244b0b6f4c885bafec55debe'
if __name__=='__main__':main()
