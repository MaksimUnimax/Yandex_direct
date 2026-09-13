"""One reproducible B18 Node development campaign against the READY B17 package.
Usage: b18_node_campaign.py SOURCE_REPO ORIGINAL_REPO OWNER014 READY_B17 READY_B14 EMPTY_OUTPUT
SOURCE_REPO holds saved WIP scripts. ORIGINAL_REPO holds original non-WIP suites.
Ready artifact directories must include their SHA256SUMS. No browser, network,
product reconstruction, code repair or independent Codex verdict is performed.
"""
from pathlib import Path, PurePosixPath
import hashlib, json, os, re, shutil, subprocess, sys, tarfile, zipfile
H=lambda b:hashlib.sha256(b).hexdigest()
TARGET='b20b74351d95becd67f32994e3e00899e9208b8c32c778a306f73f6703bfe508'
ZIP_SHA='1560599adfcfdb2c3180ec9103005b1584bcd39709b8fc45e233f6c1bdd11ee1'
B13_TARGET='f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47'
RUNNER_SHA='79a48c45900c9587c9f11d696065f8501a9cbc3d9f28c73ec8d764310cc92651'

def files_identity(files):return H(''.join(H(b)+'  '+n+'\n' for n,b in sorted(files.items())).encode())
def tree(root):
 if any(p.is_symlink() for p in root.rglob('*')):raise ValueError('Symlink')
 return files_identity({p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()})
def check_artifact(root):
 seen=set()
 for line in (root/'SHA256SUMS').read_text().splitlines():
  digest,n=line.split('  ',1);p=PurePosixPath(n)
  if n in seen or p.is_absolute() or '..' in p.parts or H((root/n).read_bytes())!=digest:raise ValueError('Artifact member mismatch '+n)
  seen.add(n)
 return len(seen)
def invoke(command,env,path,timeout):
 try:r=subprocess.run(command,env=env,capture_output=True,timeout=timeout);rc,out,err=r.returncode,r.stdout,r.stderr
 except subprocess.TimeoutExpired as e:rc,out,err=124,e.stdout or b'',e.stderr or b''
 path.write_bytes(out);path.with_suffix('.stderr').write_bytes(err)
 footer=dict(re.findall(r'^# (tests|pass|fail|skipped|cancelled) (\d+)$',out.decode(errors='replace'),re.M))
 return {'returncode':rc,'footer':footer,'stdout_sha256':H(out),'stderr_sha256':H(err)}
def main():
 if len(sys.argv)!=7:raise SystemExit(__doc__)
 source,original,owner,b17,b14,out=map(lambda s:Path(s).resolve(),sys.argv[1:])
 if out.exists():raise ValueError('Refusing existing output')
 counts={'B17':check_artifact(b17),'B14':check_artifact(b14)}
 archive=b17/'candidate-b17-internal.zip'
 if archive.stat().st_size!=225660 or H(archive.read_bytes())!=ZIP_SHA:raise ValueError('Exact B17 ZIP required')
 with zipfile.ZipFile(archive) as z:
  if z.testzip() is not None:raise ValueError('Bad ZIP CRC')
  product={}
  for e in z.infolist():
   if e.is_dir():continue
   p=PurePosixPath(e.filename)
   if p.is_absolute() or '..' in p.parts or len(p.parts)<2:raise ValueError('Unsafe path')
   name='/'.join(p.parts[1:])
   if name in product:raise ValueError('Duplicate path')
   product[name]=z.read(e)
 if len(product)!=67 or files_identity(product)!=TARGET:raise ValueError('Wrong product tree')
 runner=source/'extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/qa/b13_available_campaign.py'
 raw=runner.read_bytes()
 if H(raw)!=RUNNER_SHA or raw.decode().count(B13_TARGET)!=1:raise ValueError('Changed preserved runner')
 # Only its published exact-target constant changes, never behavioral assertions.
 body=raw.decode().replace(B13_TARGET,TARGET)
 with tarfile.open(b14/'exact-qa-workspace.tar.xz') as t:
  members=t.getmembers();qa_files={}
  for m in members:
   p=PurePosixPath(m.name)
   if p.is_absolute() or '..' in p.parts or (not m.isfile() and not m.isdir()):raise ValueError('Unsafe QA member')
   if m.isfile():
    if m.name in qa_files:raise ValueError('Duplicate QA member')
    qa_files[m.name]=t.extractfile(m).read()
 # Old production bytes are not used as a candidate or rebuilt via deltas.
 qa_files={n:b for n,b in qa_files.items() if not n.startswith('qa/candidate/full/')}
 out.mkdir(parents=True)
 for n,b in qa_files.items():p=out/'qa_workspace'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 qa=out/'qa_workspace/qa';full=qa/'candidate/full';full.mkdir(parents=True)
 for n,b in product.items():p=full/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 tests=out/'tests';tests.mkdir()
 for n in ('b17_worker.test.mjs','b17_content.test.mjs'):shutil.copyfile(b17/'qa_inputs'/n,tests/n)
 for n in ('b15_send_race.test.mjs','b16_context.test.mjs'):shutil.copyfile(b17/'tests'/n,tests/n)
 inputs={'product_tree':TARGET,'package_sha256':ZIP_SHA,'artifact_member_checks':counts,'preserved_runner_sha256':RUNNER_SHA,'retargeted_runner_sha256':H(body.encode()),'retargeting':'one guard constant only, no assertion edits','newer_tests':{p.name:H(p.read_bytes()) for p in tests.iterdir()},'live_provider_calls':0,'independent_gate':False,'release_allowed':False}
 (out/'INPUTS.json').write_text(json.dumps(inputs,indent=2)+'\n')
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','YMB_FULL':str(full),'YMB_FILE_CONTENT':str(full/'file_delivery_content.js'),'YMB_HARNESS':str(qa/'qa/b10_full_worker_harness.mjs'),'YMB_IDB_FIXTURE':str(qa/'qa/idb_artifact_fixture.mjs'),'NODE_OPTIONS':'--max-old-space-size=256 --require='+str(qa/'qa/b13_network_guard.cjs')}
 wrapper='import sys\nsys.argv='+repr(['campaign',str(original),str(owner),str(qa),str(out/'base_campaign')])+'\nexec(compile('+repr(body)+','+repr(str(runner))+',"exec"),{"__name__":"__main__","__file__":'+repr(str(runner))+'})'
 print('Running original19 + Wordstat/backup78 + full99 + modules254 + export84',flush=True)
 base=invoke([sys.executable,'-c',wrapper],env,out/'BASE.stdout',180)
 print('Base campaign returned',base['returncode'],flush=True)
 result_path=out/'base_campaign/RESULT.json'
 base_result=json.loads(result_path.read_text()) if result_path.exists() else {'status':'FAIL_HARNESS'}
 exact=invoke(['node','--test','--test-timeout=10000',*[str(p) for p in sorted(tests.glob('*.test.mjs'))],str(qa/'qa/b9_full_worker.test.mjs')],env,out/'DELIVERY_69.tap',60)
 exact['status']='PASS' if exact['returncode']==0 and exact['footer']=={'tests':'69','pass':'69','fail':'0','cancelled':'0','skipped':'0'} else 'FAIL'
 unmodified=tree(full)==TARGET
 okay=unmodified and base['returncode']==0 and base_result.get('status')=='PASS_AVAILABLE_SCOPE' and exact['status']=='PASS'
 result={**inputs,'base_process':base,'base_result':base_result,'delivery69':exact,'candidate_unchanged':unmodified,'status':'PASS_AVAILABLE_NODE_SCOPE' if okay else 'REQUIRES_CLASSIFICATION','browser':'NOT_RUN_BY_THIS_EXECUTOR','full_PD_gate':'NOT_RUN','counts_overlap':True}
 (out/'RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(result['status'],exact,flush=True)
 raise SystemExit(0 if okay else 1)
if __name__=='__main__':main()
