import fs from 'node:fs';import vm from 'node:vm';import crypto from 'node:crypto';import path from 'node:path';import {fileURLToPath}from'node:url';
import * as fake from './idb_test_double.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const source=fs.readFileSync(root+'/candidate/shared/search_async_store.js','utf8');
Object.assign(globalThis,fake,{window:globalThis});
vm.runInThisContext(source,{filename:'search_async_store.js'});
vm.runInThisContext(fs.readFileSync(root+'/qa/store_browser_cases.js','utf8'),{filename:'store_browser_cases.js'});
fs.mkdirSync(root+'/evidence',{recursive:true});
const tag=process.argv[2]||'GREEN';const out=root+'/evidence/STORE_LOGIC_'+tag+'.jsonl';
const emit=v=>{const line=JSON.stringify(v)+'\n';fs.appendFileSync(out,line);process.stdout.write(line);};
emit({venue:'Node '+process.version+'; deterministic IDB TEST DOUBLE only, not browser or real IndexedDB',source_sha256:crypto.createHash('sha256').update(source).digest('hex')});
let failed=0;for(const name of storeCaseNames){const result=await runStoreCase(name);emit(result);failed+=result.status!=='PASS';}
emit({status:failed?'FAIL':'PASS',tests:storeCaseNames.length,failed,browser_resource_proof:'BLOCKED_NOT_SUBSTITUTED',provider_calls:0});process.exitCode=failed?1:0;
