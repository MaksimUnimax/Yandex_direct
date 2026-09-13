"""B19 classification campaign against canonical extension/src 0.1.6.
Reuses preserved B18/B13 executable suites without changing behavioral assertions.
Expected first use may return REQUIRES_CLASSIFICATION for intentional version/permission deltas.
No browser and no real provider traffic.
Usage: b19_node_campaign.py REPO OWNER014 READY_B17 READY_B14 EMPTY_OUT
"""
from pathlib import Path,PurePosixPath
import hashlib,importlib.util,json,os,re,shutil,subprocess,sys,tarfile
H=lambda b:hashlib.sha256(b).hexdigest()
TARGET='b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86'
B13_TARGET='f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47'
RUNNER_SHA='79a48c45900c9587c9f11d696065f8501a9cbc3d9f28c73ec8d764310cc92651'

def sha(b):return hashlib.sha256(b).hexdigest()
def tree(root):return sha(''.join(sha(p.read_bytes())+'  '+p.relative_to(root).as_posix()+'\n' for p in sorted(root.rglob('*')) if p.is_file()).encode())
def check_artifact(root):
 seen=set()
 for line in (root/'SHA256SUMS').read_text().splitlines():
  d,n=line.split('  ',1);p=PurePosixPath(n)
  if n in seen or p.is_absolute() or '..' in p.parts or H((root/n).read_bytes())!=d:raise ValueError('artifact '+n)
  seen.add(n)
 return len(seen)
def invoke(command,env,path,timeout):
 try:r=subprocess.run(command,env=env,capture_output=True,timeout=timeout);rc,out,err=r.returncode,r.stdout,r.stderr
 except subprocess.TimeoutExpired as e:rc,out,err=124,e.stdout or b'',e.stderr or b''
 path.write_bytes(out);path.with_suffix('.stderr').write_bytes(err)
 footer=dict(re.findall(r'^# (tests|pass|fail|skipped|cancelled) (\d+)$',out.decode(errors='replace'),re.M))
 return {'returncode':rc,'footer':footer,'failed_names':re.findall(r'^not ok \d+ - (.*)$',out.decode(errors='replace'),re.M),'stdout_sha256':H(out),'stderr_sha256':H(err)}
def main():
 if len(sys.argv)!=6:raise SystemExit(__doc__)
 repo,owner,b17,b14,out=map(lambda s:Path(s).resolve(),sys.argv[1:]);source=repo;product=repo/'extension/src'
 if tree(product)!=TARGET:raise ValueError('Wrong B19 product tree')
 if out.exists():raise ValueError('output exists')
 counts={'B17':check_artifact(b17),'B14':check_artifact(b14)}
 runner=repo/'extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/qa/b13_available_campaign.py';raw=runner.read_bytes()
 if H(raw)!=RUNNER_SHA or raw.decode().count(B13_TARGET)!=1:raise ValueError('Preserved runner changed')
 body=raw.decode().replace(B13_TARGET,TARGET)
 with tarfile.open(b14/'exact-qa-workspace.tar.xz') as t:
  qa_files={}
  for m in t.getmembers():
   p=PurePosixPath(m.name)
   if p.is_absolute() or '..' in p.parts or (not m.isfile() and not m.isdir()):raise ValueError('unsafe QA')
   if m.isfile():qa_files[m.name]=t.extractfile(m).read()
 qa_files={n:b for n,b in qa_files.items() if not n.startswith('qa/candidate/full/')}
 out.mkdir(parents=True)
 for n,b in qa_files.items():p=out/'qa_workspace'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 qa=out/'qa_workspace/qa';full=qa/'candidate/full';full.mkdir(parents=True)
 for p in product.rglob('*'):
  if p.is_file():q=full/p.relative_to(product);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
 tests=out/'tests';tests.mkdir()
 for n in ('b17_worker.test.mjs','b17_content.test.mjs'):shutil.copyfile(b17/'qa_inputs'/n,tests/n)
 for n in ('b15_send_race.test.mjs','b16_context.test.mjs'):shutil.copyfile(b17/'tests'/n,tests/n)
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','YMB_FULL':str(full),'YMB_FILE_CONTENT':str(full/'file_delivery_content.js'),'YMB_HARNESS':str(qa/'qa/b10_full_worker_harness.mjs'),'YMB_IDB_FIXTURE':str(qa/'qa/idb_artifact_fixture.mjs'),'NODE_OPTIONS':'--max-old-space-size=256 --require='+str(qa/'qa/b13_network_guard.cjs')}
 wrapper='import sys\nsys.argv='+repr(['campaign',str(repo),str(owner),str(qa),str(out/'base_campaign')])+'\nexec(compile('+repr(body)+','+repr(str(runner))+',"exec"),{"__name__":"__main__","__file__":'+repr(str(runner))+'})'
 base=invoke([sys.executable,'-c',wrapper],env,out/'BASE.stdout',180)
 base_result=json.loads((out/'base_campaign/RESULT.json').read_text()) if (out/'base_campaign/RESULT.json').exists() else {'status':'FAIL_HARNESS'}
 exact=invoke(['node','--test','--test-timeout=10000',*[str(p) for p in sorted(tests.glob('*.test.mjs'))],str(qa/'qa/b9_full_worker.test.mjs')],env,out/'DELIVERY_69.tap',60)
 result={'product_tree':TARGET,'artifact_members':counts,'base_process':base,'base_result':base_result,'delivery69':exact,'candidate_unchanged':tree(full)==TARGET,'real_provider_calls':0,'browser':'NOT_RUN','first_classification':True}
 okay=base['returncode']==0 and base_result.get('status')=='PASS_AVAILABLE_SCOPE' and exact['returncode']==0 and exact['footer']=={'tests':'69','pass':'69','fail':'0','cancelled':'0','skipped':'0'} and result['candidate_unchanged']
 result['status']='PASS_AVAILABLE_NODE_SCOPE' if okay else 'REQUIRES_CLASSIFICATION'
 (out/'RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0 if okay else 2)
if __name__=='__main__':main()
