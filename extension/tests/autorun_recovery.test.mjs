import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';
import { performance } from 'node:perf_hooks';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const workerSource = fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8');
const FN_NAMES = [...workerSource.matchAll(/^(?:async )?function\s+([A-Za-z0-9_]+)/gm)].map((m) => m[1]);
const CID = '99999999-8888-4777-8666-555555555555';
const ORIGIN = 'https://chatgpt.com';
const CKEY = `${ORIGIN}|${CID}`;
const IDENTITY = { origin: ORIGIN, conversation_id: CID, status: 'confirmed', source: 'path', chat_path: `/c/${CID}` };
function binding() { return { binding_id:'b-search', revision:1, origin:ORIGIN, conversation_id:CID, conversation_key:CKEY, bound_at:'2026-08-20T00:00:00Z', updated_at:'2026-08-20T00:00:00Z' }; }
function run(status='waiting_command', extra={}) { return {
  run_id:'search-run', active_service:'search', permission_profile:'SEARCH', requests_attempted:2, requests_executed:1, requests_skipped:0, estimated_cost_rub:0.488,
  conversation_key:CKEY, origin:ORIGIN, conversation_id:CID, binding_snapshot:binding(), tab_id:1,
  status, sequence:0, pause_requested:false, finish_requested:false, assistant_baseline_ids:[], watch_id:'watch-search', start_delivery:{phase:'confirmed',message_text:'START'}, delivery:null,
  ...extra
}; }
function clone(value) { return value === undefined ? undefined : structuredClone(value); }
function searchCommand(queryText='оберег в машину') { return `SEARCH_API_V1\n${JSON.stringify({method:'search',queryText})}`; }
function searchXmlBase64() { return Buffer.from('<?xml version="1.0"?><yandexsearch><response><results><grouping><group><doc><url>https://example.test/a</url><title>A</title></doc></group></grouping></results></response></yandexsearch>','utf8').toString('base64'); }

function harness(initial={}, opts={}) {
  const store=clone(initial); let listener=null;
  let fetchImpl=opts.fetchImpl || (async()=>new Response(JSON.stringify({rawData:searchXmlBase64()}),{status:200}));
  const fetchCalls=[];
  const storage={
    async get(keys){ if(keys==null)return clone(store); if(typeof keys==='string')return Object.hasOwn(store,keys)?{[keys]:clone(store[keys])}:{}; if(Array.isArray(keys)){const out={}; for(const k of keys)if(Object.hasOwn(store,k))out[k]=clone(store[k]); return out;} if(typeof keys==='object'){const out=clone(keys); for(const k of Object.keys(keys))if(Object.hasOwn(store,k))out[k]=clone(store[k]); return out;} return {}; },
    async set(values){Object.assign(store,clone(values));}, async remove(keys){for(const k of(Array.isArray(keys)?keys:[keys]))delete store[k];}
  };
  const chrome={storage:{local:storage},runtime:{id:'test-extension',lastError:null,onMessage:{addListener(fn){listener=fn;}}},tabs:{
    async query(){return[{id:1,url:`${ORIGIN}/c/${CID}`}];}, async get(id){return Number(id)===1?{id:1,url:`${ORIGIN}/c/${CID}`}:null;},
    sendMessage(_id,message,cb){ if(['WS_GET_IDENTITY','WS_PAGE_CONTEXT'].includes(message?.type)) return cb({ok:true,identity:IDENTITY,conversation_key:CKEY}); cb({ok:true}); }
  }};
  const ctx=vm.createContext({console,chrome,crypto:webcrypto,TextEncoder,TextDecoder,AbortController,performance,setTimeout,clearTimeout,URL,structuredClone,Response,Request,Headers,ReadableStream,Buffer,fetch:async(...args)=>{fetchCalls.push(args); return fetchImpl(...args);},importScripts:()=>{}});
  ctx.globalThis=ctx;
  for(const file of ['shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js','shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js','shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js']) vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
  vm.runInContext(workerSource,ctx,{filename:'service_worker.js'});
  assert.equal(typeof listener,'function');
  vm.runInContext(`globalThis.__API=Object.freeze({${FN_NAMES.join(',')},KEYS});`,ctx);
  return {api:ctx.__API,ctx,store,fetchCalls,setFetch(fn){fetchImpl=fn;}};
}

const baseStore=()=>({
  wsmb_api_key:'ascii-key', wsmb_folder_id:'folder',
  wsmb_conversation_bindings:{[CKEY]:binding()},
  ymb_service_contexts:{[CKEY]:{active_service:'search'}},
  ymb_search_policy:{autorun_enabled:true,manual_enabled:true,max_requests_per_run:10,max_cost_rub_per_run:10}
});

test('Pause while waiting is immediate and preserves Search service and counters', async()=>{
  const h=harness({...baseStore(),wsmb_auto_runs:{[CKEY]:run('waiting_command')}});
  const paused=await h.api.pauseAutoRun(CKEY);
  assert.equal(paused.status,'paused');
  assert.equal(paused.active_service,'search');
  assert.equal(paused.requests_executed,1);
  assert.equal(paused.estimated_cost_rub,0.488);
});

test('Pause and Finish are deferred across in-flight delivery and applied only after confirmation', async()=>{
  const deliveryId='delivery-1';
  const h=harness({...baseStore(),wsmb_auto_runs:{[CKEY]:run('delivering',{delivery:{delivery_id:deliveryId,phase:'claimed'}})},wsmb_outbox:{[CKEY]:{delivery_id:deliveryId,type:'autorun',run_id:'search-run',tab_id:1,report_text:'SEARCH_RESULT_V1\n{}',phase:'claimed'}}});
  const pauseRequested=await h.api.pauseAutoRun(CKEY);
  assert.equal(pauseRequested.status,'delivering');
  assert.equal(pauseRequested.pause_requested,true);
  await h.api.completeDelivery({conversation_key:CKEY,delivery_id:deliveryId,confirmation_basis:'microphone'});
  assert.equal(h.store.wsmb_auto_runs[CKEY].status,'paused');

  h.store.wsmb_auto_runs[CKEY]=run('delivering',{delivery:{delivery_id:'delivery-2',phase:'claimed'}});
  h.store.wsmb_outbox={[CKEY]:{delivery_id:'delivery-2',type:'autorun',run_id:'search-run',tab_id:1,report_text:'SEARCH_RESULT_V1\n{}',phase:'claimed'}};
  const finishRequested=await h.api.finishAutoRun(CKEY);
  assert.equal(finishRequested.status,'delivering');
  assert.equal(finishRequested.finish_requested,true);
  await h.api.completeDelivery({conversation_key:CKEY,delivery_id:'delivery-2',confirmation_basis:'microphone'});
  assert.equal(h.store.wsmb_auto_runs[CKEY].status,'stopped');
});

test('Resume is allowed only from pause and keeps immutable service/budget', async()=>{
  const h=harness({...baseStore(),wsmb_auto_runs:{[CKEY]:run('paused')}});
  const resumed=await h.api.resumeAutoRun(CKEY);
  assert.equal(resumed.status,'waiting_command');
  assert.equal(resumed.active_service,'search');
  assert.equal(resumed.requests_executed,1);
  h.store.wsmb_auto_runs[CKEY]=run('waiting_command');
  await assert.rejects(()=>h.api.resumeAutoRun(CKEY),e=>e.code==='AUTO_RUN_NOT_PAUSED');
});

test('A second distinct Search command cannot start while previous result is still being delivered', async()=>{
  const h=harness({...baseStore(),wsmb_auto_runs:{[CKEY]:run('delivering',{delivery:{delivery_id:'delivery-1',phase:'claimed'}})}});
  const response=await h.api.handleAutoCommand({conversation_key:CKEY,run_id:'search-run',assistant_turn_id:'turn-2',command_text:searchCommand('второй запрос')},{tab:{id:1}});
  assert.equal(response.accepted,false);
  assert.equal(response.busy,true);
  assert.equal(response.status,'delivering');
  assert.equal(h.fetchCalls.length,0);
});

test('Autorun validation error is delivered as YMB_ERROR_V1 with zero provider requests and then safely continues', async()=>{
  const h=harness({...baseStore(),wsmb_auto_runs:{[CKEY]:run('waiting_command')}});
  const response=await h.api.handleAutoCommand({conversation_key:CKEY,run_id:'search-run',assistant_turn_id:'bad-turn',command_text:'SEARCH_API_V1\n{"method":"search","queryText":""}'},{tab:{id:1}});
  assert.equal(response.accepted,true);
  assert.equal(response.error_delivery,true);
  assert.match(response.report_text,/^YMB_ERROR_V1\n/);
  assert.equal(h.fetchCalls.length,0);
  const outbox=h.store.wsmb_outbox[CKEY];
  assert.equal(outbox.phase,'claimed');
  assert.match(outbox.report_text,/"request_executed":\s*false/);
  const errorPayload=JSON.parse(outbox.report_text.split('\n').slice(1).join('\n'));
  assert.equal(errorPayload.service,'search');
  assert.equal(errorPayload.channel,'autorun');
  assert.equal(errorPayload.stage,'COMMAND_VALIDATION');
  assert.equal(errorPayload.recoverable,true);
  assert.equal(errorPayload.request_executed,false);
  assert.equal(errorPayload.automatic_retry,false);
  assert.equal(errorPayload.run_id,'search-run');
  assert.equal(errorPayload.autorun_continues,true);
  assert.match(errorPayload.timestamp,/^\d{4}-\d{2}-\d{2}T/);
  await h.api.completeDelivery({conversation_key:CKEY,delivery_id:outbox.delivery_id,confirmation_basis:'microphone'});
  assert.equal(h.store.wsmb_auto_runs[CKEY].status,'waiting_command');
  assert.equal(h.store.wsmb_auto_runs[CKEY].last_assistant_turn_id,'bad-turn');
});

test('Unknown provider outcome is delivered once, does not retry, and same fingerprint remains fenced after delivery', async()=>{
  const h=harness({...baseStore(),wsmb_auto_runs:{[CKEY]:run('waiting_command')}},{fetchImpl:async()=>{throw new TypeError('connection lost');}});
  const command=searchCommand('не повторять');
  const first=await h.api.handleAutoCommand({conversation_key:CKEY,run_id:'search-run',assistant_turn_id:'turn-unknown',command_text:command},{tab:{id:1}});
  assert.equal(first.error_delivery,true);
  assert.equal(first.code,'REQUEST_OUTCOME_UNKNOWN_NO_RETRY');
  assert.equal(h.fetchCalls.length,1);
  assert.match(first.report_text,/^YMB_ERROR_V1\n/);
  assert.match(first.report_text,/"request_executed":\s*"UNKNOWN"/);
  const errorPayload=JSON.parse(first.report_text.split('\n').slice(1).join('\n'));
  assert.equal(errorPayload.channel,'autorun');
  assert.equal(errorPayload.operation,'search');
  assert.equal(errorPayload.recoverable,false);
  assert.equal(errorPayload.autorun_continues,true);
  const delivery=h.store.wsmb_outbox[CKEY];
  await h.api.completeDelivery({conversation_key:CKEY,delivery_id:delivery.delivery_id,confirmation_basis:'microphone'});
  assert.equal(h.store.wsmb_auto_runs[CKEY].status,'waiting_command');
  const second=await h.api.handleAutoCommand({conversation_key:CKEY,run_id:'search-run',assistant_turn_id:'turn-unknown-2',command_text:command},{tab:{id:1}});
  assert.equal(second.accepted,false);
  assert.equal(second.code,'REQUEST_OUTCOME_UNKNOWN_NO_RETRY');
  assert.equal(h.fetchCalls.length,1);
});

test('Worker restart converts abandoned REQUESTING into UNKNOWN error delivery without a new provider call', async()=>{
  const fingerprint='old-fingerprint';
  const h=harness({...baseStore(),wsmb_auto_runs:{[CKEY]:run('requesting',{request_worker_session_id:'worker-old',last_assistant_turn_id:'turn-old',last_command_fingerprint:fingerprint})}});
  await new Promise(resolve=>setTimeout(resolve,0));
  const recovered=h.store.wsmb_auto_runs[CKEY];
  assert.equal(recovered.status,'delivering');
  assert.equal(recovered.last_error.code,'REQUEST_OUTCOME_UNKNOWN_NO_RETRY');
  assert.equal(recovered.last_error.request_executed,'UNKNOWN');
  assert.equal(recovered.last_command_fingerprint,fingerprint);
  assert.equal(h.fetchCalls.length,0);
  assert.match(h.store.wsmb_outbox[CKEY].report_text,/^YMB_ERROR_V1\n/);
  assert.match(h.store.wsmb_outbox[CKEY].report_text,/"request_executed":\s*"UNKNOWN"/);
});
