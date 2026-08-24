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
const contentSource = fs.readFileSync(path.join(root, 'content_script.js'), 'utf8');
const FN_NAMES = [...workerSource.matchAll(/^(?:async )?function\s+([A-Za-z0-9_]+)/gm)].map((m) => m[1]);
const CID = '99999999-8888-4777-8666-555555555555';
const ORIGIN = 'https://chatgpt.com';
const CKEY = `${ORIGIN}|${CID}`;
const IDENTITY = { origin: ORIGIN, conversation_id: CID, status: 'confirmed', source: 'path', chat_path: `/c/${CID}` };

function binding() {
  return { binding_id:'b-outbox', revision:1, origin:ORIGIN, conversation_id:CID, conversation_key:CKEY, bound_at:'2026-08-24T00:00:00Z', updated_at:'2026-08-24T00:00:00Z' };
}
function run(status='waiting_command') {
  return {
    run_id:'outbox-run', active_service:'search', permission_profile:'SEARCH', requests_attempted:0, requests_executed:0, requests_skipped:0, estimated_cost_rub:0,
    conversation_key:CKEY, origin:ORIGIN, conversation_id:CID, binding_snapshot:binding(), tab_id:1,
    status, sequence:0, pause_requested:false, finish_requested:false, assistant_baseline_ids:[], watch_id:'watch-outbox', start_delivery:{phase:'confirmed',message_text:'START'}, delivery:null
  };
}
function busyOutbox() {
  return { delivery_id:'content-busy', type:'content_error', tab_id:1, run_id:null, conversation_key:CKEY, report_text:'YMB_ERROR_V1\n{}', phase:'claimed', report_prefix_applied:false, created_at:'2026-08-24T00:00:00Z' };
}
function searchCommand(queryText='не затирать доставку') {
  return `SEARCH_API_V1\n${JSON.stringify({method:'search', queryText})}`;
}
function searchXmlBase64() {
  return Buffer.from('<?xml version="1.0"?><yandexsearch><response><results><grouping><group><doc><url>https://example.test/a</url><title>A</title></doc></group></grouping></results></response></yandexsearch>','utf8').toString('base64');
}
function clone(value) { return value === undefined ? undefined : structuredClone(value); }

function harness(initial={}) {
  const store=clone(initial); let listener=null; const fetchCalls=[];
  const storage={
    async get(keys){
      if(keys==null)return clone(store);
      if(typeof keys==='string')return Object.hasOwn(store,keys)?{[keys]:clone(store[keys])}:{};
      if(Array.isArray(keys)){const out={};for(const k of keys)if(Object.hasOwn(store,k))out[k]=clone(store[k]);return out;}
      if(typeof keys==='object'){const out=clone(keys);for(const k of Object.keys(keys))if(Object.hasOwn(store,k))out[k]=clone(store[k]);return out;}
      return {};
    },
    async set(values){Object.assign(store,clone(values));},
    async remove(keys){for(const k of(Array.isArray(keys)?keys:[keys]))delete store[k];}
  };
  const chrome={
    storage:{local:storage},
    runtime:{id:'test-extension',lastError:null,onMessage:{addListener(fn){listener=fn;}}},
    tabs:{
      async query(){return[{id:1,url:`${ORIGIN}/c/${CID}`}];},
      async get(id){return Number(id)===1?{id:1,url:`${ORIGIN}/c/${CID}`}:null;},
      sendMessage(_id,message,cb){if(['WS_GET_IDENTITY','WS_PAGE_CONTEXT'].includes(message?.type))return cb({ok:true,identity:IDENTITY,conversation_key:CKEY});cb({ok:true});}
    }
  };
  const ctx=vm.createContext({console,chrome,crypto:webcrypto,TextEncoder,TextDecoder,AbortController,performance,setTimeout,clearTimeout,URL,structuredClone,Response,Request,Headers,ReadableStream,Buffer,fetch:async(...args)=>{fetchCalls.push(args);return new Response(JSON.stringify({rawData:searchXmlBase64()}),{status:200});},importScripts:()=>{}});
  ctx.globalThis=ctx;
  for(const file of ['shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js','shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js','shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js']) vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
  vm.runInContext(workerSource,ctx,{filename:'service_worker.js'});
  assert.equal(typeof listener,'function');
  vm.runInContext(`globalThis.__API=Object.freeze({${FN_NAMES.join(',')},KEYS});`,ctx);
  return {api:ctx.__API,store,fetchCalls};
}

function baseStore() {
  return {
    wsmb_api_key:'ascii-key',
    wsmb_folder_id:'folder',
    wsmb_conversation_bindings:{[CKEY]:binding()},
    ymb_service_contexts:{[CKEY]:{active_service:'search'}},
    ymb_search_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['search'],max_requests_per_run:10,max_cost_rub_per_run:10,method_cost_rub:{search:0.488}},
    wsmb_outbox:{[CKEY]:busyOutbox()}
  };
}

test('Autorun start cannot overwrite an already occupied conversation outbox', async()=>{
  const h=harness(baseStore());
  await assert.rejects(() => h.api.startAutoRun(CKEY,1), (error) => error?.code === 'DELIVERY_IN_PROGRESS');
  assert.equal(h.store.wsmb_auto_runs?.[CKEY],undefined);
  assert.deepEqual(h.store.wsmb_outbox[CKEY],busyOutbox());
  assert.equal(h.fetchCalls.length,0);
});

test('Manual action is rejected before operation claim or provider call while outbox is occupied', async()=>{
  const h=harness({...baseStore(),wsmb_manual_modes:{[CKEY]:true}});
  const response=await h.api.executeManualBlock(searchCommand('manual blocked'),CKEY,{tab:{id:1}},'manual-outbox-token');
  assert.equal(response.accepted,false);
  assert.equal(response.code,'DELIVERY_IN_PROGRESS');
  assert.equal(h.store.wsmb_manual_operations?.[CKEY],undefined);
  assert.deepEqual(h.store.wsmb_outbox[CKEY],busyOutbox());
  assert.equal(h.fetchCalls.length,0);
});

test('Autorun command returns retryable busy before provider call while outbox is occupied', async()=>{
  const h=harness({...baseStore(),wsmb_auto_runs:{[CKEY]:run('waiting_command')}});
  const response=await h.api.handleAutoCommand({conversation_key:CKEY,run_id:'outbox-run',assistant_turn_id:'turn-outbox',command_text:searchCommand('autorun blocked')},{tab:{id:1}});
  assert.equal(response.accepted,false);
  assert.equal(response.busy,true);
  assert.equal(response.code,'DELIVERY_IN_PROGRESS');
  assert.equal(h.store.wsmb_auto_runs[CKEY].status,'waiting_command');
  assert.equal(h.store.wsmb_auto_runs[CKEY].requests_attempted,0);
  assert.deepEqual(h.store.wsmb_outbox[CKEY],busyOutbox());
  assert.equal(h.fetchCalls.length,0);
});

test('content script retries a busy Autorun assistant turn after the delivery slot is released',()=>{
  assert.match(contentSource,/if\s*\(response\?\.busy\)\s*autorunSeen\.delete\(turnId\)/);
});
