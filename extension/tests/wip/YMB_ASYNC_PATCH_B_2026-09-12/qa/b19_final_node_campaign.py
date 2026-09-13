"""Complete B19 0.1.6 Node/fixture regression on exact canonical production bytes.
Usage: b19_final_node_campaign.py REPO CLASSIFICATION_ARTIFACT EMPTY_OUT
No browser, no owner profile, no real provider traffic. QA-only v3 adaptation is applied to
artifact QA copies after exact preimage validation. Production source is never modified.
"""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess,sys
H=lambda b:hashlib.sha256(b).hexdigest()
TARGET='b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86'

def tree(root):
    return H(''.join(H(p.read_bytes())+'  '+p.relative_to(root).as_posix()+'\n' for p in sorted(root.rglob('*')) if p.is_file()).encode())
def run(cmd,env,out,name,timeout=120):
    try:r=subprocess.run(cmd,env=env,capture_output=True,timeout=timeout);rc,stdout,stderr=r.returncode,r.stdout,r.stderr
    except subprocess.TimeoutExpired as e:rc,stdout,stderr=124,e.stdout or b'',e.stderr or b''
    (out/(name+'.tap')).write_bytes(stdout);(out/(name+'.stderr')).write_bytes(stderr)
    f=dict(re.findall(r'^# (tests|pass|fail|skipped|cancelled) (\d+)$',stdout.decode(errors='replace'),re.M))
    return {'returncode':rc,'footer':f,'failed_names':re.findall(r'^not ok \d+ - (.*)$',stdout.decode(errors='replace'),re.M),'tap_sha256':H(stdout),'stderr_sha256':H(stderr)}
def expect(result,tests):
    f=result['footer'];return result['returncode']==0 and f=={'tests':str(tests),'pass':str(tests),'fail':'0','cancelled':'0','skipped':'0'}
def main():
    if len(sys.argv)!=4:raise SystemExit(__doc__)
    repo,classification,out=map(lambda p:Path(p).resolve(),sys.argv[1:])
    if out.exists():raise ValueError('Output already exists')
    out.mkdir(parents=True)
    product=repo/'extension/src';qa_root=classification/'qa_workspace/qa';qa=qa_root/'qa';artifact_product=qa_root/'candidate/full'
    if tree(product)!=TARGET or tree(artifact_product)!=TARGET:raise ValueError('Exact B19 product required')
    if len([p for p in product.rglob('*') if p.is_file()])!=67:raise ValueError('Unexpected product file count')
    # Artifact QA is disposable. Original classifier remains immutable evidence.
    adapt=repo/'extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/qa/b19_final_qa_adapt_v3.py'
    a=subprocess.run([sys.executable,str(adapt),str(qa)],capture_output=True,timeout=20)
    (out/'QA_ADAPT.stdout').write_bytes(a.stdout);(out/'QA_ADAPT.stderr').write_bytes(a.stderr)
    if a.returncode:raise RuntimeError('QA adaptation failed')
    shutil.copyfile(qa/'B19_QA_ADAPTATION.json',out/'B19_QA_ADAPTATION.json')
    guard=str(qa/'b13_network_guard.cjs')
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','NODE_OPTIONS':'--max-old-space-size=256 --require='+guard,'YMB_FULL':str(artifact_product),'YMB_HARNESS':str(qa/'b10_full_worker_harness.mjs'),'YMB_IDB_FIXTURE':str(qa/'idb_artifact_fixture.mjs')}
    # 1) Complete original source regression, already adapted by the governed B13 view.
    original=classification/'base_campaign/original_view/extension/tests'
    paths=sorted(original.glob('*.test.mjs'))+[original/'qa_phase5_codex/direct_addendum_coverage.test.mjs']
    if len(paths)!=19:raise ValueError('Unexpected original test-file count')
    results={}
    results['ORIGINAL_132']=run(['node','--test','--test-timeout=10000',*[str(p) for p in paths]],env,out,'ORIGINAL_132',60)
    # 2) Missing Wordstat/Debug/backup coverage remains a separate 78-assertion suite.
    results['MISSING_78']=run(['node','--test','--test-timeout=10000',str(qa/'b13_missing_coverage.test.mjs')],env,out,'MISSING_78',60)
    # 3) Full contract: deliberately exclude the separate 78-suite (same B12 contract definition).
    full_tests=[p for p in sorted(qa.glob('*.test.mjs')) if p.name!='b13_missing_coverage.test.mjs']
    results['FULL_99']=run(['node','--test','--test-timeout=10000',*[str(p) for p in full_tests]],env,out,'FULL_99',60)
    # 4) Preserved module regressions retarget only the exact candidate-tree guard.
    root=repo/'extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12';script=root/'qa/b9_regression_campaign.py';text=script.read_text();old='d1fc4f49718f023f1bc1a6a3ec921fa7253d63b805cedadff6fbcf2e70180612'
    if text.count(old)!=1:raise ValueError('Module runner target guard changed')
    body=text.replace(old,TARGET).replace('Wrong B9 candidate','Wrong B19 candidate')
    module_out=out/'MODULE_WORK';args=['runner',str(root/'qa/b14_inputs/owner014'),str(qa_root),str(module_out)]
    wrapper='import sys\nsys.argv='+repr(args)+'\nexec(compile('+repr(body)+','+repr(str(script))+',"exec"),{"__name__":"__main__","__file__":'+repr(str(script))+'})'
    mr=subprocess.run([sys.executable,'-c',wrapper],capture_output=True,timeout=90)
    (out/'MODULE_RUNNER.stdout').write_bytes(mr.stdout);(out/'MODULE_RUNNER.stderr').write_bytes(mr.stderr)
    mtap=(module_out/'MODULE_REGRESSION.tap').read_bytes() if (module_out/'MODULE_REGRESSION.tap').exists() else b''
    (out/'MODULE_254.tap').write_bytes(mtap);(out/'MODULE_254.stderr').write_bytes((module_out/'MODULE_REGRESSION.stderr').read_bytes() if (module_out/'MODULE_REGRESSION.stderr').exists() else b'')
    mf=dict(re.findall(r'^# (tests|pass|fail|skipped|cancelled) (\d+)$',mtap.decode(errors='replace'),re.M));results['MODULE_254']={'returncode':mr.returncode,'footer':mf,'tap_sha256':H(mtap)}
    # 5) Export/file module suite from the classification artifact, refreshed with exact B19 product files.
    e=classification/'base_campaign/patch/export'
    for src,dst in [('search_async_worker_transport.js','candidate/b8/search_async_worker_transport.js'),('search_async_worker_transport.js','candidate/b7/search_async_worker_transport.js'),('shared/search_async_protocol.js','candidate/b8/search_async_protocol.js'),('shared/search_async_export.js','candidate/b8/search_async_export.js')]:shutil.copyfile(product/src,e/dst)
    export_tests=[e/'qa/b7_worker.test.mjs',*sorted((e/'qa').glob('b8*.test.mjs'))]
    results['EXPORT_84']=run(['node','--test','--test-timeout=10000',*[str(p) for p in export_tests]],{**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},out,'EXPORT_84',60)
    # 6) Delivery/recovery contour with the adapted full-worker network expectation.
    delivery=[classification/'tests/b17_worker.test.mjs',classification/'tests/b17_content.test.mjs',classification/'tests/b15_send_race.test.mjs',classification/'tests/b16_context.test.mjs',qa/'b9_full_worker.test.mjs']
    results['DELIVERY_69']=run(['node','--test','--test-timeout=10000',*[str(p) for p in delivery]],env,out,'DELIVERY_69',60)
    # 7) Syntax/JSON/version/permission and exact-byte source identity.
    syntax=[]
    for p in sorted(product.rglob('*.js')):
        r=subprocess.run(['node','--check',str(p)],capture_output=True,timeout=10);syntax.append({'path':p.relative_to(product).as_posix(),'returncode':r.returncode})
    for p in product.rglob('*.json'):json.loads(p.read_text())
    manifest=json.loads((product/'manifest.json').read_text());pkg=json.loads((product/'package.json').read_text())
    static_ok=len(syntax)==61 and all(x['returncode']==0 for x in syntax) and manifest['version']==pkg['version']=='0.1.6' and manifest['host_permissions'].count('https://operation.api.cloud.yandex.net/*')==1 and manifest['host_permissions'].count('https://searchapi.api.cloud.yandex.net/*')==1 and 'alarms' not in manifest['permissions'] and tree(product)==TARGET
    expected={'ORIGINAL_132':132,'MISSING_78':78,'FULL_99':99,'MODULE_254':254,'EXPORT_84':84,'DELIVERY_69':69}
    suite_ok={k:expect(results[k],n) for k,n in expected.items()}
    result={'schema_version':1,'date':'2026-09-13','product_tree':TARGET,'version':'0.1.6','files':67,'operation_host_enabled':True,'alarms_permission':False,'real_provider_calls':0,'controlled_provider_responses_only':True,'qa_adaptation':json.loads((qa/'B19_QA_ADAPTATION.json').read_text()),'suites':results,'suite_pass':suite_ok,'syntax':{'count':len(syntax),'pass':sum(x['returncode']==0 for x in syntax)},'static_pass':static_ok,'candidate_unchanged':tree(product)==TARGET}
    result['status']='PASS_AVAILABLE_NODE_SCOPE' if static_ok and all(suite_ok.values()) else 'REQUIRES_CLASSIFICATION'
    (out/'RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (out/'SHA256SUMS').write_text(''.join(H(p.read_bytes())+'  '+p.relative_to(out).as_posix()+'\n' for p in sorted(out.rglob('*')) if p.is_file() and p.name!='SHA256SUMS'))
    print(json.dumps({'status':result['status'],'suite_pass':suite_ok,'syntax':result['syntax'],'static_pass':static_ok},indent=2))
    raise SystemExit(0 if result['status']=='PASS_AVAILABLE_NODE_SCOPE' else 2)
if __name__=='__main__':main()
