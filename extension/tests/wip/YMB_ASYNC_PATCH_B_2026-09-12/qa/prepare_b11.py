"""Restore exact B11 QA from exact B10; not a release package.
Usage: python qa/prepare_b11.py EXACT_B10_QA EMPTY_OUTPUT
All validation precedes writes; no network/provider calls or fuzzy patching.
"""
from pathlib import Path
import hashlib,json,sys,types
ROOT=Path(__file__).resolve().parent.parent
CONFIG_SHA="bc64fb54aa38e5339240c983981cd62f58ea0c3f442e74518931b05a12b027b2"
sha=lambda b:hashlib.sha256(b).hexdigest()
def tree(root):
    if not root.is_dir() or root.is_symlink() or any(p.is_symlink() for p in root.rglob('*')):
        raise ValueError('Invalid/symlink input tree')
    return {p.relative_to(root).as_posix():p.read_bytes() for p in sorted(root.rglob('*')) if p.is_file()}
def inv(files):
    return ''.join(sha(v)+'  '+k+'\n' for k,v in sorted(files.items()))
def main():
    if len(sys.argv)!=3:raise SystemExit(__doc__)
    base,out=[Path(v).absolute() for v in sys.argv[1:]]
    if out.is_symlink() or (out.exists() and (not out.is_dir() or any(out.iterdir()))):raise ValueError('Output occupied')
    raw=(ROOT/'evidence/B11_INPUTS.json').read_bytes()
    if sha(raw)!=CONFIG_SHA:raise ValueError('Input manifest changed')
    c=json.loads(raw);full=tree(base/'candidate/full')
    if len(full)!=67 or sha(inv(full).encode())!=c['base_tree']:raise ValueError('Not exact B10')
    saved={}
    for rel,expected in c['inputs'].items():
        p=ROOT/rel
        if p.is_symlink() or '..' in Path(rel).parts or Path(rel).is_absolute():raise ValueError('Invalid path')
        b=p.read_bytes()
        if sha(b)!=expected:raise ValueError('Changed saved input '+rel)
        saved[rel]=b
    helper=types.ModuleType('exact_delta');helper.__file__=str(ROOT/'qa/prepare_b6.py')
    exec(compile(saved['qa/prepare_b6.py'],helper.__file__,'exec'),helper.__dict__)
    for n,d in c['deltas'].items():
        full[n]=helper.apply_exact(full[n],saved['evidence/'+d],n)
        if sha(full[n])!=c['postimages'][n]:raise ValueError('Postimage mismatch '+n)
    if sha(inv(full).encode())!=c['tree']:raise ValueError('Combined tree mismatch')
    outputs={'candidate/full/'+k:v for k,v in full.items()}
    for rel,expected in c['carry'].items():
        p=base/rel
        if p.is_symlink():raise ValueError('Symlink dependency')
        b=p.read_bytes()
        if sha(b)!=expected:raise ValueError('Changed B10 QA input '+rel)
        outputs[rel]=b
    for n in ['b11_reparse.test.mjs','b11_batch_faults.test.mjs']:outputs['qa/'+n]=saved['qa/'+n]
    outputs['SOURCE_TREE_SHA256.txt']=inv(full).encode()
    for rel,b in outputs.items():
        p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    (out/'evidence').mkdir(exist_ok=True)
    print('B11 exact QA restored: 67 files, four changes. NO ZIP / RELEASE_ALLOWED=NO')
if __name__=='__main__':main()
