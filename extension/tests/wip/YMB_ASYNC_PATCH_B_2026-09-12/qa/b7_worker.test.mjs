import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const workerSource=fs.readFileSync(new URL('../candidate/b7/search_async_worker_transport.js',import.meta.url),'utf8');
const discoverySource=fs.readFileSync(new URL('./block_command_discovery.js',import.meta.url),'utf8');
const context=vm.createContext({console});context.globalThis=context;vm.runInContext(discoverySource,context);vm.runInContext(workerSource,context);
const F=context.YMBSearchAsyncWorkerTransport;
const KEY='https://chatgpt.com|11111111-1111-4111-8111-111111111111';const CID='11111111-1111-4111-8111-111111111111';
const commandText=raw=>`SEARCH_ASYNC_BATCH_API_V1\n${JSON.stringify(raw)}`;
function startCommand(extra={}){return {action:'start',jobId:'job-1',queries:['браслет','подвеска'],parameters:{region:'225'},maxRequests:2,maxCostMicrorub:61000,...extra};}
function normalized(raw){
 if(!raw||typeof raw!=='object')throw Object.assign(new Error('bad'),{code:'BAD'});
 if(raw.action==='start')return Object.freeze(startCommand(raw));
 if(['submitN','collectN'].includes(raw.action))return Object.freeze({action:raw.action,jobId:raw.jobId,count:raw.count??1});
 if(raw.action==='itemsPage')return Object.freeze({action:'itemsPage',jobId:raw.jobId,after:raw.after??-1,limit:raw.limit??100});
 if(['status','pause','resume','cancelPending'].includes(raw.action))return Object.freeze({action:raw.action,jobId:raw.jobId});
 throw Object.assign(new Error('bad action'),{code:'ASYNC_ACTION_INVALID'});
}
function harness(overrides={}){
 const state={manual:true,service:'search',binding:{conversation_key:KEY,conversation_id:CID},run:null,operation:null,outbox:null,providerEnabled:false,settings:{credentials:{search:{api_key:'secret',folder_id:'folder'}}},...overrides};
 const calls={base:0,bind:[],create:[],runtime:[],control:[],normalize:[],outbox:[],setop:[],resolve:[],prefix:0};
 const summary={job_id:'job-1',control:'RUNNING',total:2,counts:{PENDING:2,WAITING:0,RESULT_SAVED:0,SUCCEEDED:0,UNKNOWN:0,FAILED:0,CANCELLED:0,SUBMITTING:0,COLLECTING:0,PARSE_FAILED:0},requests_started:0,operations_accepted:0,polls_started:0,unresolved:2,all_successful:false,busy:false,revision:1};
 const store={
  async createJob(a){calls.create.push(a);return structuredClone(summary);},
  async getSummary(){return structuredClone(summary);},
  async pageItems(){return {rows:Array.from({length:100},(_,i)=>({index:i,query:'x'.repeat(800),state:'WAITING',operation_id:`op-${i}`,poll_count:1,secret_raw:'NO'})),next_after:99};}
 };
 const runtime={
  async step(a){calls.runtime.push(a);return overrides.stepResult?await overrides.stepResult(a,calls.runtime.length):{ok:true,stop:false,outcome:a.kind==='submit'?'accepted':'waiting',request_executed:true,index:calls.runtime.length-1,operation_id:`op-${calls.runtime.length}`};},
  async recover(a){calls.runtime.push({recover:a});return {ok:true};},
  async control(a){calls.control.push(a);return {...summary,control:a.action==='pause'?'PAUSED':a.action==='cancelPending'?'CANCELLED':'RUNNING'};},
  async normalizeSaved(a){calls.normalize.push(a);return {ok:true};}
 };
 const policy={async bindJob(a){calls.bind.push(a);return {bound:true};}};
 const binding={ready:true,policy,async resolveContext(a){calls.resolve.push(a);return {authorized:true,owner:KEY,channel:'manual'};}};
 let seq=0;
 const worker=F.create({
  baseExecuteManualBlock:async()=>{calls.base++;return{ok:true,legacy:true};},protocol:{normalizeCommand:normalized},store,runtime,admissionBinding:binding,asyncPolicyFactory:{PRICE_MICRORUB:30500},
  getSettings:async()=>state.settings,getBinding:async()=>state.binding,getManualMode:async()=>state.manual,getServiceContext:async()=>({active_service:state.service}),getAutoRun:async()=>state.run,
  getManualOperation:async()=>state.operation,setManualOperation:async(_k,v)=>{state.operation=v;calls.setop.push(structuredClone(v));return v;},getConversationOutbox:async()=>state.outbox,
  assertTabConversation:async(tab,key)=>{if(tab!==7||key!==KEY)throw Object.assign(new Error('owner'),{code:'OWNER'});return{conversation_key:KEY,conversation_id:CID};},normalizeConversationKey:v=>{if(v!==KEY)throw new Error('key');return v;},
  blockDiscovery:context.YMBBlockCommandDiscovery,ordinaryDiscovery:overrides.ordinaryDiscovery||(()=>[]),putOutbox:async(_k,v)=>{state.outbox=v;calls.outbox.push(structuredClone(v));return v;},
  formatBridgeError:o=>`ERR:${o.code}:${o.requestExecuted}`,applyPrefixToReport:async(_k,t)=>{calls.prefix++;return{text:'PREFIX\n'+t,applied:true};},uid:p=>`${p}-${++seq}`,nowIso:()=>`2026-09-12T00:00:0${seq}Z`,
  runContextModel:{assertServiceMatch:(a,b)=>{if(a!==b)throw Object.assign(new Error('service'),{code:'SERVICE'});}},autorunModel:{RUN_STATUSES:{PAUSED:'paused'},isTerminalStatus:s=>['stopped','error'].includes(s)},
  workerId:'worker-async',providerEnabled:state.providerEnabled,now:()=>1000
 });
 return{state,calls,worker,summary,binding,runtime,store};
}
async function manual(h,raw,token='token-1'){return h.worker.executeManual(commandText(raw),KEY,{tab:{id:7}},token);}

test('non-async block delegates unchanged base Manual handler',async()=>{const h=harness();const r=await h.worker.executeManual('SEARCH_API_V1 {}',KEY,{tab:{id:7}},'t');assert.equal(r.legacy,true);assert.equal(h.calls.base,1);});
test('factory fails closed when shared admission is not ready',()=>{const h=harness();assert.throws(()=>F.create({baseExecuteManualBlock:async()=>{},protocol:{},store:{},runtime:{},admissionBinding:{ready:false}}),e=>['ASYNC_WORKER_DEPENDENCY_REQUIRED','ASYNC_SHARED_ADMISSION_NOT_READY'].includes(e.code));});
test('multiple async commands rejected without runtime/provider',async()=>{const h=harness();const text=commandText(startCommand())+'\n'+commandText({action:'status',jobId:'job-1'});const r=await h.worker.executeManual(text,KEY,{tab:{id:7}},'t');assert.match(r.report_text,/ASYNC_SINGLE_COMMAND_REQUIRED/);assert.equal(h.calls.runtime.length,0);});
test('mixed ordinary+async command rejected without runtime/provider',async()=>{const h=harness({ordinaryDiscovery:()=>[{service:'search'}]});const r=await manual(h,startCommand());assert.match(r.report_text,/ASYNC_SINGLE_COMMAND_REQUIRED/);assert.equal(h.calls.runtime.length,0);});
test('Manual disabled rejects before job or runtime',async()=>{const h=harness({manual:false});const r=await manual(h,startCommand());assert.equal(r.code,'MANUAL_MODE_DISABLED');assert.equal(h.calls.create.length,0);});
test('wrong active service rejects before job or runtime',async()=>{const h=harness({service:'wordstat'});const r=await manual(h,startCommand());assert.equal(r.code,'SERVICE_NOT_ACTIVE');});
test('unbound or wrong live tab rejects before job',async()=>{const h=harness({binding:null});const r=await manual(h,startCommand());assert.equal(r.code,'CONVERSATION_NOT_BOUND');assert.equal(h.calls.create.length,0);});
test('non-paused active Autorun blocks Manual deferred command',async()=>{const h=harness({run:{run_id:'r',status:'waiting_command',active_service:'search',tab_id:7}});const r=await manual(h,startCommand());assert.equal(r.code,'AUTORUN_NOT_PAUSED');});
test('active Manual operation blocks another deferred command',async()=>{const h=harness({operation:{status:'search_async_requesting'}});const r=await manual(h,startCommand());assert.equal(r.code,'MANUAL_OPERATION_ACTIVE');});
test('existing outbox blocks command',async()=>{const h=harness({outbox:{delivery_id:'d'}});const r=await manual(h,startCommand());assert.equal(r.code,'DELIVERY_IN_PROGRESS');});
test('start binds policy then creates per-item job without provider call',async()=>{const h=harness();const r=await manual(h,startCommand());assert.equal(r.request_executed,false);assert.equal(h.calls.bind.length,1);assert.equal(h.calls.create.length,1);assert.equal(h.calls.runtime.length,0);assert.equal(h.calls.bind[0].jobId,'job-1');assert.equal(h.calls.create[0].owner,KEY);assert.equal(h.calls.create[0].unitCostMicrorub,30500);assert.equal(h.calls.outbox.length,1);assert.match(r.report_text,/SEARCH_ASYNC_BATCH_RESULT_V1/);});
test('start records durable search_async_requesting operation before authority check',async()=>{const h=harness();await manual(h,startCommand());assert.equal(h.calls.setop[0].status,'search_async_requesting');assert.equal(h.calls.resolve.length,1);assert.equal(h.calls.resolve[0].metadata.conversation_key,KEY);});
test('status uses owner-bound job and no provider call',async()=>{const h=harness();const r=await manual(h,{action:'status',jobId:'job-1'});assert.equal(r.request_executed,false);assert.equal(h.calls.runtime.length,0);assert.match(r.report_text,/"total":2/);});
test('itemsPage strips query/raw fields and stays compact at 100 rows',async()=>{const h=harness();const r=await manual(h,{action:'itemsPage',jobId:'job-1',after:-1,limit:100});assert.ok(r.report_text.length<20000);assert.equal(r.report_text.includes('x'.repeat(50)),false);assert.equal(r.report_text.includes('secret_raw'),false);assert.match(r.report_text,/"operation_id":"op-0"/);});
for(const action of ['pause','resume','cancelPending'])test(`${action} is local control with zero provider calls`,async()=>{const h=harness();const r=await manual(h,{action,jobId:'job-1'});assert.equal(r.request_executed,false);assert.equal(h.calls.control.length,1);assert.equal(h.calls.runtime.filter(v=>v.kind).length,0);});
test('submitN fails closed before runtime when operation-host capability is disabled',async()=>{const h=harness({providerEnabled:false});const r=await manual(h,{action:'submitN',jobId:'job-1',count:2});assert.match(r.report_text,/ASYNC_PROVIDER_PERMISSION_REQUIRED/);assert.equal(h.calls.runtime.length,0);});
test('collectN fails closed before runtime when operation-host capability is disabled',async()=>{const h=harness({providerEnabled:false});const r=await manual(h,{action:'collectN',jobId:'job-1',count:2});assert.match(r.report_text,/ASYNC_PROVIDER_PERMISSION_REQUIRED/);assert.equal(h.calls.runtime.length,0);});
test('submitN provider-enabled executes bounded requested count and compact result',async()=>{const h=harness({providerEnabled:true});const r=await manual(h,{action:'submitN',jobId:'job-1',count:2});assert.equal(h.calls.runtime.filter(v=>v.kind==='submit').length,2);assert.equal(h.calls.prefix,1);assert.equal(r.request_executed,true);assert.ok(r.report_text.length<5000);});
test('collectN normalizes each received result locally',async()=>{const h=harness({providerEnabled:true,stepResult:async(a,n)=>({ok:true,stop:false,outcome:'received',request_executed:true,index:n-1,operation_id:`op-${n}`})});const r=await manual(h,{action:'collectN',jobId:'job-1',count:2});assert.equal(h.calls.runtime.filter(v=>v.kind==='collect').length,2);assert.equal(h.calls.normalize.length,2);assert.equal(r.request_executed,true);});
test('UNKNOWN network outcome stops same command without replay',async()=>{const h=harness({providerEnabled:true,stepResult:async()=>({ok:false,stop:true,outcome:'unknown',request_executed:'UNKNOWN',index:0,code:'NET'})});const r=await manual(h,{action:'submitN',jobId:'job-1',count:25});assert.equal(h.calls.runtime.filter(v=>v.kind==='submit').length,1);assert.equal(r.request_executed,'UNKNOWN');assert.equal(h.calls.outbox[0].provider_executions,null);});
test('provider command performs local recover before first network step',async()=>{const h=harness({providerEnabled:true});await manual(h,{action:'submitN',jobId:'job-1',count:1});assert.ok(h.calls.runtime[0].recover);assert.equal(h.calls.runtime[1].kind,'submit');});
test('compact report does not expose raw response arrays or query list',async()=>{const h=harness({providerEnabled:true,stepResult:async()=>({ok:true,stop:true,outcome:'accepted',request_executed:true,index:0,operation_id:'op',raw_text:'SECRET_RAW',results:[1,2,3]})});const r=await manual(h,{action:'submitN',jobId:'job-1',count:1});assert.equal(r.report_text.includes('SECRET_RAW'),false);assert.equal(r.report_text.includes('results'),false);});
test('source has no background alarm/interval/polling scheduler',()=>{for(const token of ['chrome.alarms','setInterval(','setTimeout('])assert.equal(workerSource.includes(token),false);});
test('B7 wrapper does not replace Autorun handler',()=>{assert.equal(workerSource.includes('handleAutoCommand ='),false);assert.equal(workerSource.includes('WS_AUTO'),false);});
