import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';
import { performance } from 'node:perf_hooks';
import { fileURLToPath } from 'node:url';

// Focused Stage-3 regression: durable content errors must stay on the current runtime owner tab.
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const workerSource = fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8');
const contentSource = fs.readFileSync(path.join(root, 'content_script.js'), 'utf8');
const FN_NAMES = [...workerSource.matchAll(/^(?:async )?function\s+([A-Za-z0-9_]+)/gm)].map((m) => m[1]);
const CID='99999999-8888-4777-8666-555555555555';
const ORIGIN='https://chatgpt.com';
const CKEY=`${ORIGIN}|${CID}`;
const IDENTITY={origin:ORIGIN,conversation_id:CID,status:'confirmed',source:'path',chat_path:`/c/${CID}`};
const binding={binding_id:'b-content',revision:1,origin:ORIGIN,conversation_id:CID,conversation_key:CKEY,bound_at:'2026-08-20T00:00:00Z',updated_at:'2026-08-20T00:00:00Z'};
function clone(v){return v===undefined?undefined:structuredClone(v);}
function harness(initial={}){
  const store=clone(initial); let listener=null; const fetchCalls=[];
  const storage={
    async get(keys){if(keys==null)return clone(store);if(typeof keys==='string')return Object.hasOwn(store,keys)?{[keys]:clone(store[keys])}:{};if(Array.isArray(keys)){const out={};for(const k of keys)if(Object.hasOwn(store,k))out[k]=clone(store[k]);return out;}const out=clone(keys||{});for(const k of Object.keys(keys||{}))if(Object.hasOwn(store,k))out[k]=clone(store[k]);return out;},
    async set(values){Object.assign(store,clone(values));},async remove(keys){for(const k of(Array.isArray(keys)?keys:[keys]))delete store[k];}
  };
  const chrome={storage:{local:storage},runtime:{id:'test-extension',lastError:null,onMessage:{addListener(fn){listener=fn;}}},tabs:{sendMessage(_id,message,cb){if(['WS_GET_IDENTITY','WS_PAGE_CONTEXT'].includes(message?.type))return cb({ok:true,identity:IDENTITY,conversation_key:CKEY});cb({ok:true});}}};
  const ctx=vm.createContext({console,chrome,crypto:webcrypto,TextEncoder,TextDecoder,AbortController,performance,setTimeout,clearTimeout,URL,structuredClone,Response,Request,Headers,ReadableStream,Buffer,fetch:async(...args)=>{fetchCalls.push(args);return new Response('{}',{status:200});},importScripts:()=>{}});ctx.globalThis=ctx;
  for(const file of ['shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js','shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js','shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js'])vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
  vm.runInContext(workerSource,ctx,{filename:'service_worker.js'});assert.equal(typeof listener,'function');vm.runInContext(`globalThis.__API=Object.freeze({${FN_NAMES.join(',')},KEYS});`,ctx);return{api:ctx.__API,store,fetchCalls};
}
function base(){return{wsmb_conversation_bindings:{[CKEY]:binding},ymb_service_contexts:{[CKEY]:{active_service:'search'}}};}
function activeRun(){return{run_id:'run-owner',active_service:'search',permission_profile:'SEARCH',conversation_key:CKEY,origin:ORIGIN,conversation_id:CID,tab_id:1,status:'waiting_command',sequence:0,pause_requested:false,finish_requested:false,requests_attempted:0,requests_executed:0,requests_skipped:0,estimated_cost_rub:0,assistant_baseline_ids:[],watch_id:'watch-owner',start_delivery:{phase:'confirmed',message_text:'START'},delivery:null};}

test('content error is turned into durable YMB_ERROR_V1 outbox with zero provider request',async()=>{
  const h=harness(base());
  const r=await h.api.reportContentError({conversation_key:CKEY,service:'search',channel:'autorun',stage:'WATCHER',code:'WATCHER_ERROR',error:'observer failed',run_id:'run-1',request_executed:false,recoverable:true,autorun_continues:true},{tab:{id:1}});
  assert.equal(r.ok,true);assert.equal(h.fetchCalls.length,0);
  const entry=h.store.wsmb_outbox[CKEY];assert.equal(entry.type,'content_error');assert.equal(entry.phase,'claimed');
  assert.match(entry.report_text,/^YMB_ERROR_V1\n/);
  const payload=JSON.parse(entry.report_text.split('\n').slice(1).join('\n'));
  assert.equal(payload.service,'search');assert.equal(payload.channel,'autorun');assert.equal(payload.stage,'WATCHER');assert.equal(payload.code,'WATCHER_ERROR');assert.equal(payload.request_executed,false);assert.equal(payload.recoverable,true);assert.equal(payload.autorun_continues,true);assert.equal(payload.run_id,'run-1');
});

test('content error never overwrites an existing result and is promoted only after result completion',async()=>{
  const h=harness({...base(),wsmb_outbox:{[CKEY]:{delivery_id:'result-1',type:'manual',tab_id:1,conversation_key:CKEY,report_text:'SEARCH_RESULT_V1\n{}',phase:'committed'}}});
  const r=await h.api.reportContentError({conversation_key:CKEY,service:'search',channel:'manual',stage:'DELIVERY',code:'DELIVERY_ERROR',error:'delivery failed',request_executed:false},{tab:{id:1}});
  assert.equal(r.ok,true);assert.equal(h.store.wsmb_outbox[CKEY].delivery_id,'result-1');assert.equal(h.store.ymb_content_error_queue[CKEY].length,1);
  await h.api.completeDelivery({conversation_key:CKEY,delivery_id:'result-1',confirmation_basis:'microphone'},{tab:{id:1}});
  assert.equal(h.store.wsmb_outbox[CKEY].type,'content_error');assert.match(h.store.wsmb_outbox[CKEY].report_text,/DELIVERY_ERROR/);assert.equal(h.store.ymb_content_error_queue?.[CKEY],undefined);
});

test('same content error is deduplicated while pending and while being delivered',async()=>{
  const h=harness({...base(),wsmb_outbox:{[CKEY]:{delivery_id:'busy',type:'manual',tab_id:1,conversation_key:CKEY,report_text:'busy',phase:'claimed'}}});
  const message={conversation_key:CKEY,service:'search',channel:'content',stage:'STATE_SYNC',code:'STATE_SYNC_ERROR',error:'worker restarting',request_executed:false};
  const first=await h.api.reportContentError(message,{tab:{id:1}});const second=await h.api.reportContentError(message,{tab:{id:1}});
  assert.equal(first.duplicate,false);assert.equal(second.duplicate,true);assert.equal(h.store.ymb_content_error_queue[CKEY].length,1);
  await h.api.completeDelivery({conversation_key:CKEY,delivery_id:'busy'},{tab:{id:1}});
  const third=await h.api.reportContentError(message,{tab:{id:1}});assert.equal(third.duplicate,true);assert.equal(h.store.wsmb_outbox[CKEY].type,'content_error');
});

test('content error from a non-owner conversation is rejected before queue mutation',async()=>{
  const h=harness(base());
  const bad=`${ORIGIN}|aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee`;
  const r=await h.api.reportContentError({conversation_key:bad,code:'X',error:'bad'},{tab:{id:1}});
  assert.equal(r.ok,false);assert.equal(h.store.ymb_content_error_queue,undefined);assert.equal(h.store.wsmb_outbox,undefined);assert.equal(h.fetchCalls.length,0);
});

test('same-conversation non-owner tab cannot queue content error while Autorun has an owner tab',async()=>{
  const h=harness({...base(),wsmb_auto_runs:{[CKEY]:activeRun()}});
  const r=await h.api.reportContentError({conversation_key:CKEY,service:'search',channel:'autorun',stage:'STATE_SYNC',code:'STATE_SYNC_ERROR',error:'secondary tab noise',run_id:'run-owner',request_executed:false,autorun_continues:true},{tab:{id:2}});
  assert.equal(r.ok,false);assert.equal(r.code,'AUTO_NON_OWNER_TAB');
  assert.equal(h.store.ymb_content_error_queue,undefined);assert.equal(h.store.wsmb_outbox,undefined);assert.equal(h.fetchCalls.length,0);
});

test('same-conversation non-owner tab cannot queue behind an owner outbox',async()=>{
  const ownerOutbox={delivery_id:'owner-result',type:'autorun',tab_id:1,run_id:'run-owner',conversation_key:CKEY,report_text:'SEARCH_RESULT_V1\n{}',phase:'claimed'};
  const h=harness({...base(),wsmb_outbox:{[CKEY]:ownerOutbox}});
  const r=await h.api.reportContentError({conversation_key:CKEY,service:'search',channel:'content',stage:'OUTBOX_POLL',code:'AUTO_NON_OWNER_TAB',error:'secondary tab cannot read owner outbox',request_executed:false},{tab:{id:2}});
  assert.equal(r.ok,false);assert.equal(r.code,'AUTO_NON_OWNER_TAB');
  assert.equal(h.store.ymb_content_error_queue,undefined);assert.equal(h.store.wsmb_outbox[CKEY].delivery_id,'owner-result');assert.equal(h.fetchCalls.length,0);
});

test('content script durably reports manual, Autorun, state-sync and delivery failures instead of plaque-only handling',()=>{
  assert.match(contentSource,/function queueContentError\(/);
  assert.match(contentSource,/type: "WS_REPORT_CONTENT_ERROR"/);
  assert.match(contentSource,/MANUAL_CONTENT_ERROR/);
  assert.match(contentSource,/AUTORUN_WORKER_TRANSPORT/);
  assert.match(contentSource,/STATE_SYNC_ERROR/);
  assert.match(contentSource,/OUTBOX_POLL_ERROR/);
  assert.match(contentSource,/DELIVERY_COMMIT_REJECTED/);
  assert.match(contentSource,/DELIVERY_COMPLETE_REJECTED/);
  assert.match(contentSource,/reportedContentErrors/);
});
