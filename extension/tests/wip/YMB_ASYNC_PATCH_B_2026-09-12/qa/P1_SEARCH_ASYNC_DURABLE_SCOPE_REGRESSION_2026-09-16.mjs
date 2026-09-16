import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const workerSource=fs.readFileSync(new URL('../../../../src/search_async_worker_transport.js',import.meta.url),'utf8');
const exportSource=fs.readFileSync(new URL('../../../../src/shared/search_async_export.js',import.meta.url),'utf8');
const discoverySource=fs.readFileSync(new URL('./block_command_discovery.js',import.meta.url),'utf8');
const ctx=vm.createContext({console});ctx.globalThis=ctx;vm.runInContext(discoverySource,ctx);vm.runInContext(workerSource,ctx);
const F=ctx.YMBSearchAsyncWorkerTransport;
const A='https://chatgpt.com|11111111-1111-4111-8111-111111111111';
const B='https://chatgpt.com|22222222-2222-4222-8222-222222222222';
const CIDS={ [A]:'11111111-1111-4111-8111-111111111111', [B]:'22222222-2222-4222-8222-222222222222' };
const TABS={7:A,8:B};
const text=raw=>`SEARCH_ASYNC_BATCH_API_V1\n${JSON.stringify(raw)}`;
function normalize(raw){
 if(raw.action==='start')return Object.freeze({action:'start',jobId:raw.jobId,queries:raw.queries||['q'],parameters:raw.parameters||{region:'225'},maxRequests:raw.maxRequests||1,maxCostMicrorub:raw.maxCostMicrorub||30500});
 if(['status','pause','resume','cancelPending'].includes(raw.action))return Object.freeze({action:raw.action,jobId:raw.jobId});
 if(raw.action==='itemsPage')return Object.freeze({action:'itemsPage',jobId:raw.jobId,after:raw.after??-1,limit:raw.limit??100});
 if(raw.action==='exportPage')return Object.freeze({action:'exportPage',jobId:raw.jobId,after:raw.after??-1,limit:raw.limit??25,revision:raw.revision??null});
 if(['submitN','collectN'].includes(raw.action))return Object.freeze({action:raw.action,jobId:raw.jobId,count:raw.count??1});
 if(raw.action==='normalizeSaved')return Object.freeze({action:'normalizeSaved',jobId:raw.jobId,index:raw.index});
 throw Object.assign(new Error('bad action'),{code:'ASYNC_ACTION_INVALID'});
}
function summary(jobId='job-1'){return{job_id:jobId,control:'RUNNING',total:1,counts:{PENDING:1,SUBMITTING:0,WAITING:0,COLLECTING:0,RESULT_SAVED:0,SUCCEEDED:0,PARSE_FAILED:0,FAILED:0,UNKNOWN:0,CANCELLED:0},requests_started:0,operations_accepted:0,polls_started:0,unresolved:1,all_successful:false,busy:false,revision:1};}
function harness(){
 const state={folder:'folder',manual:new Map(),outbox:new Map(),runs:new Map(),jobs:new Map()};
 const calls={bind:[],create:[],summary:[],pages:[],runtime:[],exports:[],resolve:[]};let seq=0;
 const guard=(jobId,owner)=>{const job=state.jobs.get(jobId);if(!job)throw Object.assign(new Error('missing'),{code:'ASYNC_JOB_NOT_FOUND'});if(job.owner!==owner)throw Object.assign(new Error('wrong owner'),{code:'ASYNC_WRONG_OWNER'});return job;};
 const store={
  async createJob(a){calls.create.push(structuredClone(a));if(state.jobs.has(a.jobId))throw Object.assign(new Error('exists'),{code:'ASYNC_JOB_ALREADY_EXISTS'});const job={owner:a.owner,folderId:a.folderId,summary:summary(a.jobId)};state.jobs.set(a.jobId,job);return structuredClone(job.summary);},
  async getSummary(jobId,owner){calls.summary.push({jobId,owner});return structuredClone(guard(jobId,owner).summary);},
  async pageItems(jobId,owner,args){guard(jobId,owner);calls.pages.push({jobId,owner,...args});return{rows:[{index:0,state:'WAITING',operation_id:'op-1',poll_count:1}],next_after:0};}
 };
 const runtime={
  async recover(a){guard(a.jobId,a.owner);calls.runtime.push({kind:'recover',...a});return{ok:true};},
  async step(a){guard(a.jobId,a.owner);calls.runtime.push({kind:a.kind,...a});return{ok:true,stop:true,outcome:a.kind==='submit'?'accepted':'waiting',request_executed:true,index:0,operation_id:'op-1'};},
  async control(a){const j=guard(a.jobId,a.owner);calls.runtime.push({kind:'control',...a});return structuredClone(j.summary);},
  async normalizeSaved(a){const j=guard(a.jobId,a.owner);calls.runtime.push({kind:'normalize',...a});return{ok:true,normalized:true,progress:structuredClone(j.summary)};}
 };
 const policy={async bindJob(a){calls.bind.push(structuredClone(a));return{bound:true};}};
 const binding={ready:true,policy,async resolveContext(a){calls.resolve.push(structuredClone(a));return{authorized:true,owner:a.metadata.conversation_key,channel:'manual'};}};
 const exportFactory={create({authorize}){return{async stagePage(a){guard(a.jobId,a.owner);assert.equal(await authorize({jobId:a.jobId,owner:a.owner,action:'exportPage'}),true);calls.exports.push(structuredClone(a));return{descriptor:{artifact_key:`artifact:${a.deliveryId}`,delivery_id:a.deliveryId,status:'ready',byte_length:10},report:{revision:a.revision??1,item_count:1,next_after:0,has_more:false,all_job_items_in_this_file:true}};},async discard(){}};}};
 const worker=F.create({baseExecuteManualBlock:async()=>({ok:true,legacy:true}),protocol:{normalizeCommand:normalize},store,runtime,exportFactory,artifactStore:{},admissionBinding:binding,asyncPolicyFactory:{PRICE_MICRORUB:30500},
  getSettings:async()=>({credentials:{search:{api_key:'secret',folder_id:state.folder}}}),getBinding:async key=>CIDS[key]?{conversation_key:key,conversation_id:CIDS[key]}:null,getManualMode:async()=>true,getServiceContext:async()=>({active_service:'search'}),getAutoRun:async key=>state.runs.get(key)||null,
  getManualOperation:async key=>state.manual.get(key)||null,setManualOperation:async(key,v)=>{state.manual.set(key,structuredClone(v));return v;},getConversationOutbox:async key=>state.outbox.get(key)||null,
  assertTabConversation:async(tab,key)=>{if(TABS[tab]!==key)throw Object.assign(new Error('tab'),{code:'CONVERSATION_MISMATCH'});return{conversation_key:key,conversation_id:CIDS[key]};},normalizeConversationKey:key=>{if(!CIDS[key])throw new Error('key');return key;},
  blockDiscovery:ctx.YMBBlockCommandDiscovery,ordinaryDiscovery:()=>[],putOutbox:async(key,v)=>{state.outbox.set(key,structuredClone(v));return v;},formatBridgeError:o=>`ERR:${o.code}`,applyPrefixToReport:async(_k,t)=>({text:t,applied:false}),uid:p=>`${p}-${++seq}`,nowIso:()=>`2026-09-16T00:00:${String(seq).padStart(2,'0')}Z`,runContextModel:{assertServiceMatch:(a,b)=>assert.equal(a,b)},autorunModel:{RUN_STATUSES:{PAUSED:'paused'},isTerminalStatus:s=>['stopped','error'].includes(s)},workerId:'worker-scope',providerEnabled:true,now:()=>1000});
 return{state,calls,worker};
}
async function manual(h,key,tab,raw,token){return h.worker.executeManual(text(raw),key,{tab:{id:tab}},token||`${key}-${raw.action}-${raw.jobId}`);}
function complete(h,key){h.state.outbox.delete(key);const op=h.state.manual.get(key);if(op)h.state.manual.set(key,{...op,status:'completed'});}
async function startA(h,jobId='job-1'){await manual(h,A,7,{action:'start',jobId,queries:['q'],maxRequests:1,maxCostMicrorub:30500});complete(h,A);}

test('durable owner is Search folder scope, never ChatGPT conversation key',async()=>{const h=harness();const r=await manual(h,A,7,{action:'start',jobId:'job-1',queries:['q'],maxRequests:1,maxCostMicrorub:30500});assert.equal(r.request_executed,false);assert.equal(h.calls.create[0].owner,'search-folder:folder');assert.equal(h.calls.bind[0].owner,'search-folder:folder');assert.notEqual(h.calls.create[0].owner,A);});
test('chat handoff keeps status on the same durable job without owner bypass',async()=>{const h=harness();await startA(h);const r=await manual(h,B,8,{action:'status',jobId:'job-1'});assert.equal(r.request_executed,false);assert.match(r.report_text,/"job_id":"job-1"/);assert.equal(h.calls.summary.at(-1).owner,'search-folder:folder');});
test('chat handoff keeps itemsPage on the same durable job',async()=>{const h=harness();await startA(h);const r=await manual(h,B,8,{action:'itemsPage',jobId:'job-1',after:-1,limit:100});assert.equal(r.request_executed,false);assert.equal(h.calls.pages.at(-1).owner,'search-folder:folder');assert.match(r.report_text,/"operation_id":"op-1"/);});
test('chat handoff exports through the ordinary exporter with the same durable owner',async()=>{const h=harness();await startA(h);const r=await manual(h,B,8,{action:'exportPage',jobId:'job-1',after:-1,limit:25,revision:1});assert.equal(r.request_executed,false);assert.equal(h.calls.exports.length,1);assert.equal(h.calls.exports[0].owner,'search-folder:folder');assert.equal(h.calls.exports[0].folderId,'folder');});
for(const action of ['pause','resume','cancelPending'])test(`chat handoff local control ${action} keeps durable owner`,async()=>{const h=harness();await startA(h);const r=await manual(h,B,8,{action,jobId:'job-1'});assert.equal(r.request_executed,false);assert.equal(h.calls.runtime.at(-1).owner,'search-folder:folder');assert.equal(h.calls.runtime.at(-1).action,action);});
test('chat handoff normalizeSaved keeps durable owner',async()=>{const h=harness();await startA(h);const r=await manual(h,B,8,{action:'normalizeSaved',jobId:'job-1',index:0});assert.equal(r.request_executed,false);assert.equal(h.calls.runtime.at(-1).kind,'normalize');assert.equal(h.calls.runtime.at(-1).owner,'search-folder:folder');});
test('chat handoff submit provider command uses the same durable owner for recover and step',async()=>{const h=harness();await startA(h);const r=await manual(h,B,8,{action:'submitN',jobId:'job-1',count:1});assert.equal(r.request_executed,true);assert.deepEqual(h.calls.runtime.slice(-2).map(x=>x.owner),['search-folder:folder','search-folder:folder']);});
test('chat handoff collect provider command uses the same durable owner for recover and step',async()=>{const h=harness();await startA(h);const r=await manual(h,B,8,{action:'collectN',jobId:'job-1',count:1});assert.equal(r.request_executed,true);assert.deepEqual(h.calls.runtime.slice(-2).map(x=>x.owner),['search-folder:folder','search-folder:folder']);assert.equal(h.calls.runtime.at(-1).kind,'collect');});
test('worker restart recovery keeps durable owner inside the same current chat authority',async()=>{const h=harness();await startA(h);h.state.manual.set(B,{operation_id:'manual-old',request_token:'old',conversation_key:B,tab_id:8,active_service:'search',run_id:null,status:'search_async_requesting',request_worker_session_id:'old-worker',batch_action:'submitN',batch_job_id:'job-1',folder_id:'folder',request_executed:false});const r=await h.worker.recoverManualOperations({key:B,tabId:8});assert.equal(r.request_executed,false);assert.equal(h.calls.runtime.at(-1).kind,'recover');assert.equal(h.calls.runtime.at(-1).owner,'search-folder:folder');});
test('different Search folder cannot adopt a job created under another credential scope',async()=>{const h=harness();await startA(h);h.state.folder='other-folder';const r=await manual(h,B,8,{action:'status',jobId:'job-1'});assert.match(r.report_text,/ASYNC_WRONG_OWNER/);assert.equal(r.request_executed,false);});
test('paused Autorun mirror keeps conversation owner separate from durable data owner',async()=>{const h=harness();h.state.runs.set(A,{run_id:'run-a',status:'paused',active_service:'search',tab_id:7});await manual(h,A,7,{action:'start',jobId:'job-run',queries:['q'],maxRequests:1,maxCostMicrorub:30500});const b=h.calls.bind.at(-1);assert.equal(b.owner,'search-folder:folder');assert.equal(b.runId,'run-a');assert.equal(b.runOwner,A);});
test('exporter contains no cross-owner recovery path anymore',()=>{for(const token of ['crossOwnerJobReader','readCrossOwnerJob','EXPORT_CROSS_OWNER_'])assert.equal(exportSource.includes(token),false);assert.match(exportSource,/store\.peekNext\(\{ jobId, owner,/);});
test('worker exports one deterministic durable-owner function',()=>{assert.equal(F.durableJobOwner('folder'),'search-folder:folder');assert.throws(()=>F.durableJobOwner(''));assert.match(workerSource,/Durable job ownership is credential-scoped/);});
