// Executes exact changed counter-boundary fragments, not a full installed worker.
import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';
const original=new URL('../owner014/',import.meta.url),patched=new URL('../candidate/legacy/',import.meta.url);
function snippet(path,type){const s=fs.readFileSync(path,'utf8');if(type==='manual'){
 const start=s.indexOf('if (operation.run_id',s.indexOf('if (!decision.allow)'));
 assert.ok(start>=0);const end=s.indexOf('try {',start);assert.ok(end>start);return s.slice(start,end);
}if(type==='batch'){const start=s.indexOf('  async function noteBatchProviderBoundary');const end=s.indexOf('\n  let batchRuntime',start);assert.ok(start>=0&&end>start);return s.slice(start,end)+'\nawait noteBatchProviderBoundary(metadata, 0.488);';}
 const line=s.split('\n').find(l=>l.includes('run = await patchAutoRun(key')&&l.includes('request_worker_session_id: WORKER_SESSION_ID'));assert.ok(line);return line;
}
async function execute(fragment,{service='search',guard=true,runId='r'}={}){
 let state={run_id:'r',active_service:service,requests_attempted:2,requests_executed:3,estimated_cost_rub:1.464,unchanged:'yes'},calls=0;
 const context=vm.createContext({item:{service},operation:{run_id:runId},key:'owner',run:state,decision:{estimated_cost_rub:.488},metadata:{conversation_key:'owner',run_id:runId,channel:'autorun'},
  normalizeConversationKey:k=>k,WORKER_SESSION_ID:'w',WordstatAutorunModel:{RUN_STATUSES:{REQUESTING:'requesting'}},
  getAutoRun:async()=>state,patchAutoRun:async(k,fn)=>{calls++;state=fn({...state});return state;}});context.globalThis=context;
 if(guard)context.YMBSearchAdmissionGuard={};await vm.runInContext('(async()=>{'+fragment+'})()',context);return JSON.parse(JSON.stringify({state,calls}));
}
for(const [file,type] of [['service_worker.js','manual'],['wordstat_batch_worker_integration.js','manual'],['service_worker.js','auto'],['search_batch_worker_transport.js','batch']]){
 for(const guard of [true,false])test(`${file}/${type}: search accounting ${guard?'shared':'legacy'} preserves lifecycle`,async()=>{
  const old=await execute(snippet(new URL(file,original),type),{guard});const fresh=await execute(snippet(new URL(file,patched),type),{guard});
  assert.equal(fresh.state.requests_attempted,old.state.requests_attempted,'attempt counter must not disappear');assert.equal(fresh.state.unchanged,'yes');
  assert.equal(fresh.state.requests_executed,guard?3:old.state.requests_executed);assert.equal(fresh.state.estimated_cost_rub,guard?1.464:old.state.estimated_cost_rub);
  assert.equal(fresh.state.status,old.state.status);assert.equal(fresh.state.request_worker_session_id,old.state.request_worker_session_id);
 });
 if(type!=='batch')test(`${file}/${type}: Wordstat counters unchanged with Search guard`,async()=>{
  const options={service:'wordstat',guard:true};assert.deepEqual(await execute(snippet(new URL(file,patched),type),options),await execute(snippet(new URL(file,original),type),options));
 });
}
test('batch run mismatch does not change another run',async()=>{const f=snippet(new URL('search_batch_worker_transport.js',patched),'batch');assert.equal((await execute(f,{runId:'other'})).calls,0);});
