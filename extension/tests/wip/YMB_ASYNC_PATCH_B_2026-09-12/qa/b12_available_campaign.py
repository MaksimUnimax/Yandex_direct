"""Run AVAILABLE B12 development checks, NOT the independent PD-00..PD-17 gate.
Usage: python qa/b12_available_campaign.py OWNER014 EXACT_B12_QA EMPTY_LOGS
No browser launch, real credentials, provider calls or installable packaging.
"""
from pathlib import Path
import hashlib,json,os,re,subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
TARGET='73e6ed85bfd843bf2590a2d1a44a9d04224ce5f63563d127bcd35c2ad092eeec'
sha=lambda b:hashlib.sha256(b).hexdigest()
def tree(root):
    if any(p.is_symlink() for p in root.rglob('*')):raise ValueError('Symlink input')
    return sha(''.join(sha(p.read_bytes())+'  '+p.relative_to(root).as_posix()+'\n' for p in sorted(root.rglob('*')) if p.is_file()).encode())
def run(command,logs,name,expected,env=None):
    try:
        r=subprocess.run(command,capture_output=True,timeout=60,env=env)
        (logs/(name+'.tap')).write_bytes(r.stdout);(logs/(name+'.stderr')).write_bytes(r.stderr)
        f=dict(re.findall(r'^# (tests|pass|fail|cancelled|skipped|duration_ms) (.+)$',r.stdout.decode(errors='replace'),re.M))
        passed=r.returncode==0 and f.get('tests')==str(expected) and f.get('pass')==str(expected) and f.get('fail')=='0' and f.get('skipped')=='0'
        return dict(status='PASS' if passed else 'FAIL',returncode=r.returncode,footer=f,tap_sha256=sha(r.stdout))
    except subprocess.TimeoutExpired as e:
        (logs/(name+'.partial.tap')).write_bytes(e.stdout or b'');return dict(status='BLOCKED_TIMEOUT')
def main():
    if len(sys.argv)!=4:raise SystemExit(__doc__)
    owner,qa,logs=map(lambda p:Path(p).resolve(),sys.argv[1:]);full=qa/'candidate/full'
    if tree(full)!=TARGET:raise ValueError('Wrong B12')
    if logs.exists() and (not logs.is_dir() or any(logs.iterdir())):raise ValueError('Nonempty logs')
    m=json.loads((ROOT/'evidence/B12_INPUTS.json').read_text())
    for n,h in {**m['inherited_qa'],'b12_contract.test.mjs':m['inputs']['qa/b12_contract.test.mjs']}.items():
        if sha((qa/'qa'/n).read_bytes())!=h:raise ValueError('Changed QA '+n)
    logs.mkdir(parents=True)
    env={**os.environ,'YMB_FULL':str(full),'YMB_IDB_FIXTURE':str(qa/'qa/idb_artifact_fixture.mjs')}
    tests=sorted(str(p) for p in (qa/'qa').glob('*.test.mjs'))
    results={'venue':'Node 22; actual JS, controlled Chrome/IDB/network. Not Chrome or independent final gate.','candidate_tree_sha256':TARGET,'provider_calls':0,'release_allowed':False}
    results['full_contract']=run(['node','--test',*tests],logs,'FULL_99',99,env)
    # Reuse the existing runner verbatim except its exact target tree identity.
    module_script=(ROOT/'qa/b9_regression_campaign.py').read_bytes()
    if sha(module_script)!='d3749aa59ab394ba2595337fb760dfc3e0cdcb926f7c7a2206f53e6252ca3d09':raise ValueError('Preserved runner changed')
    old='d1fc4f49718f023f1bc1a6a3ec921fa7253d63b805cedadff6fbcf2e70180612'
    text=module_script.decode()
    if text.count(old)!=1:raise ValueError('Unexpected target guard')
    body=text.replace(old,TARGET).replace('Wrong B9 candidate','Wrong B12 candidate')
    wrapper='import sys\nsys.argv='+repr(['runner',str(owner),str(qa),str(logs/'modules')])+'\nexec(compile('+repr(body)+','+repr(str(ROOT/'qa/b9_regression_campaign.py'))+',"exec"), {"__name__":"__main__","__file__":'+repr(str(ROOT/'qa/b9_regression_campaign.py'))+'})'
    r=subprocess.run([sys.executable,'-c',wrapper],capture_output=True,timeout=70)
    (logs/'module_runner.stdout').write_bytes(r.stdout);(logs/'module_runner.stderr').write_bytes(r.stderr)
    results['modules']=json.loads((logs/'modules/RESULT.json').read_text()) if (logs/'modules/RESULT.json').exists() else {'status':'FAIL_HARNESS','returncode':r.returncode}
    # Existing export harness, same assertions; copy exact B12 executable inputs.
    p=subprocess.run([sys.executable,str(ROOT/'qa/prepare_b8.py'),str(owner),str(logs/'export')],capture_output=True,timeout=30)
    (logs/'export_prepare.stdout').write_bytes(p.stdout);(logs/'export_prepare.stderr').write_bytes(p.stderr)
    if p.returncode==0:
        e=logs/'export'
        for name,source in [('search_async_worker_transport.js','search_async_worker_transport.js'),('search_async_protocol.js','shared/search_async_protocol.js'),('search_async_export.js','shared/search_async_export.js')]:
            (e/'candidate/b8'/name).write_bytes((full/source).read_bytes())
        (e/'candidate/b7/search_async_worker_transport.js').write_bytes((full/'search_async_worker_transport.js').read_bytes())
        results['export']=run(['node','--test',str(e/'qa/b7_worker.test.mjs'),*[str(x) for x in sorted((e/'qa').glob('b8*.test.mjs'))]],logs,'EXPORT_84',84)
    else:results['export']={'status':'FAIL_HARNESS','returncode':p.returncode}
    checks=[]
    for p in sorted(full.rglob('*.js')):
        r=subprocess.run(['node','--check',str(p)],capture_output=True,timeout=10);checks.append({'path':p.relative_to(full).as_posix(),'returncode':r.returncode})
    for n in ['manifest.json','package.json']:json.loads((full/n).read_text())
    results['syntax']={'status':'PASS' if all(x['returncode']==0 for x in checks) and len(checks)==61 else 'FAIL','checks':checks,'json_count':2}
    results['candidate_unchanged']=tree(full)==TARGET
    results['status']='PASS_AVAILABLE_SCOPE' if results['candidate_unchanged'] and all(results[k].get('status')=='PASS' for k in ['full_contract','modules','export','syntax']) else 'FAIL'
    (logs/'RESULT.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k not in ['modules','syntax']},indent=2));raise SystemExit(0 if results['status']=='PASS_AVAILABLE_SCOPE' else 1)
if __name__=='__main__':main()
