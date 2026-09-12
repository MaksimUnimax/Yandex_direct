"""B13 feasible development campaign, NOT independent Codex/Chrome acceptance.
Usage: b13_available_campaign.py SOURCE_REPO OWNER014 B13_QA EMPTY_LOGS
No browser or real provider traffic. New original-suite adapters are explicit diffs.
"""
from pathlib import Path
import concurrent.futures, hashlib, importlib.util, json, os, re, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parent.parent
TARGET='f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47'
sha=lambda b:hashlib.sha256(b).hexdigest()
def tree(root):return sha(''.join(sha(p.read_bytes())+'  '+p.relative_to(root).as_posix()+'\n' for p in sorted(root.rglob('*')) if p.is_file()).encode())
def run(command, stdout_path, env, timeout=25):
    try:
        r=subprocess.run(command,capture_output=True,env=env,timeout=timeout);out,err,rc=r.stdout,r.stderr,r.returncode
    except subprocess.TimeoutExpired as e: out,err,rc=e.stdout or b'',e.stderr or b'',124
    stdout_path.write_bytes(out);stdout_path.with_suffix('.stderr').write_bytes(err)
    f=dict(re.findall(r'^# (tests|pass|fail|cancelled|skipped|duration_ms) (.+)$',out.decode(errors='replace'),re.M))
    return {'exit_code':rc,'footer':f,'tap_sha256':sha(out),'failed_names':re.findall(r'^not ok \d+ - (.*)$',out.decode(errors='replace'),re.M),'status':'PASS' if rc==0 and f.get('fail')=='0' and f.get('skipped')=='0' and f.get('cancelled')=='0' else 'REQUIRES_CLASSIFICATION'}

def main():
    if len(sys.argv)!=5:raise SystemExit(__doc__)
    repo,owner,qa,logs=map(lambda p:Path(p).resolve(),sys.argv[1:]);full=qa/'candidate/full'
    if tree(full)!=TARGET:raise ValueError('Wrong B13 candidate')
    if logs.exists() and (not logs.is_dir() or any(logs.iterdir())):raise ValueError('Nonempty logs')
    inputs=json.loads((ROOT/'evidence/B13_INPUTS.json').read_text())
    for n,h in inputs['qa_archive_members'].items():
        if sha((qa/n).read_bytes())!=h:raise ValueError('Changed QA input '+n)
    rows=(qa/'qa/original_inventory.tsv').read_text().splitlines()
    inventory=[line.split('\t',1)[1] for line in rows[3:]]
    original=repo/'extension/tests'
    actual={p.relative_to(repo/'extension').as_posix():sha(p.read_bytes()) for p in original.rglob('*') if p.is_file() and 'wip' not in p.relative_to(original).parts}
    if set(actual)!=set(inventory):raise ValueError('Original test inventory changed')
    original_identity=sha(''.join(actual[n]+'  '+n+'\n' for n in sorted(actual)).encode())
    if original_identity!=inputs['original_tree_sha256']:raise ValueError('Original source bytes changed')
    # Reuse exact delta application, not fuzzy text rewriting.
    helper=ROOT/'qa/prepare_b8.py'
    if sha(helper.read_bytes())!='faa185b98f010d672b2f87b9b928b3dd2c82ac5842b4ad054a3c227cc4a797b6':raise ValueError('Helper changed')
    spec=importlib.util.spec_from_file_location('b13_delta',helper);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    logs.mkdir(parents=True);original_logs=logs/'original';original_logs.mkdir()
    view=logs/'original_view';shutil.copytree(full,view/'extension/src')
    shutil.copytree(original,view/'extension/tests',ignore=shutil.ignore_patterns('wip'))
    adaptations=[]
    for patch in sorted((qa/'qa/original_updates').glob('*.diff')):
        name=patch.name[len('B13_'):-len('.diff')];p=view/'extension/tests'/name;before=p.read_bytes();after=mod.delta(before,patch.read_bytes(),name);p.write_bytes(after)
        adaptations.append({'file':name,'before':sha(before),'after':sha(after),'delta':sha(patch.read_bytes())})
    paths=list(sorted((view/'extension/tests').glob('*.test.mjs')))+[view/'extension/tests/qa_phase5_codex/direct_addendum_coverage.test.mjs']
    if len(paths)!=19:raise ValueError('Unexpected original suite count')
    env=dict(os.environ);env['NODE_OPTIONS']='--max-old-space-size=256 --require='+str(qa/'qa/b13_network_guard.cjs')
    def each(p):
        name=p.relative_to(view/'extension/tests').as_posix()
        result=run(['node','--test','--test-timeout=10000',str(p)],original_logs/(name.replace('/','__')+'.tap'),env)
        result['file']=name;result['executed_test_sha256']=sha(p.read_bytes())
        (original_logs/(name.replace('/','__')+'.json')).write_text(json.dumps(result,indent=2)+'\n')
        print(name,result['status'],result['footer'],flush=True);return result
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:original_results=list(pool.map(each,paths))
    (logs/'ORIGINAL_RESULT.json').write_text(json.dumps({'adaptations':adaptations,'results':original_results},indent=2)+'\n')
    env.update(YMB_FULL=str(full),YMB_HARNESS=str(qa/'qa/b10_full_worker_harness.mjs'),YMB_IDB_FIXTURE=str(qa/'qa/idb_artifact_fixture.mjs'))
    missing=run(['node','--test','--test-timeout=10000',str(qa/'qa/b13_missing_coverage.test.mjs')],logs/'MISSING_78.tap',env)
    # Preserved B12 runner has exactly one declared target replaced, no test edits.
    p=ROOT/'qa/b12_available_campaign.py';source=p.read_bytes()
    if sha(source)!='69e82a0f20231391f483615727837fd41b79140c87c4d89539d11dcc54a37404':raise ValueError('Preserved campaign changed')
    old='73e6ed85bfd843bf2590a2d1a44a9d04224ce5f63563d127bcd35c2ad092eeec'
    if source.decode().count(old)!=1:raise ValueError('Target guard changed')
    # It selects all *.test.mjs. Supply only its original 99-assertion suite in this view.
    patchqa=logs/'patch_qa';shutil.copytree(qa,patchqa);(patchqa/'qa/b13_missing_coverage.test.mjs').unlink()
    body=source.decode().replace(old,TARGET)
    wrapper='import sys\nsys.argv='+repr(['campaign',str(owner),str(patchqa),str(logs/'patch')])+'\nexec(compile('+repr(body)+','+repr(str(p))+',"exec"),{"__name__":"__main__","__file__":'+repr(str(p))+'})'
    try:r=subprocess.run([sys.executable,'-c',wrapper],capture_output=True,env=env,timeout=120);rc=r.returncode;stdout=r.stdout;stderr=r.stderr
    except subprocess.TimeoutExpired as e:rc=124;stdout=e.stdout or b'';stderr=e.stderr or b''
    (logs/'PATCH.stdout').write_bytes(stdout);(logs/'PATCH.stderr').write_bytes(stderr)
    patch_result=json.loads((logs/'patch/RESULT.json').read_text()) if (logs/'patch/RESULT.json').exists() else {'status':'FAIL_HARNESS','exit_code':rc}
    unchanged=tree(full)==TARGET and tree(view/'extension/src')==TARGET and tree(patchqa/'candidate/full')==TARGET
    result={'candidate_tree_sha256':TARGET,'venue':'Node v22; complete actual source, controlled Chrome/IndexedDB/network fixtures; not browser or independent QA','original_tests':original_results,'explicit_original_qa_adaptations':adaptations,'new_missing_coverage':missing,'patch_campaign':patch_result,'candidate_unchanged':unchanged,'real_provider_calls':0,'browser_executed':False,'release_allowed':False}
    okay=unchanged and all(r['status']=='PASS' for r in original_results) and missing['status']=='PASS' and missing['footer'].get('pass')=='78' and patch_result['status']=='PASS_AVAILABLE_SCOPE'
    result['status']='PASS_AVAILABLE_SCOPE' if okay else 'REQUIRES_CLASSIFICATION'
    (logs/'RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(result['status']);raise SystemExit(0 if okay else 1)
if __name__=='__main__':sys.dont_write_bytecode=True;main()
