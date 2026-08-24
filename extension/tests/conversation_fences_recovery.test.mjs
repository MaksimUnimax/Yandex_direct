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
const OTHER = '11111111-2222-4333-8444-555555555555';
const ORIGIN = 'https://chatgpt.com';
const CKEY = `${ORIGIN}|${CID}`;

function clone(value) { return value === undefined ? undefined : structuredClone(value); }
function searchCommand() { return 'SEARCH_API_V1\n{"method":"search","queryText":"owner fence"}'; }
function run() {
  return {
    run_id:'r-fence', active_service:'search', permission_profile:'SEARCH',
    requests_attempted:0, requests_executed:0, requests_skipped:0, estimated_cost_rub:0,
    conversation_key:CKEY, origin:ORIGIN, conversation_id:CID,
    binding_snapshot:{binding_id:'b1',revision:1,origin:ORIGIN,conversation_id:CID,conversation_key:CKEY},
    tab_id:1, status:'waiting_command', sequence:0, pause_requested:false, finish_requested:false,
    assistant_baseline_ids:[], watch_id:'w1', start_delivery:{phase:'confirmed',message_text:'START'}, delivery:null
  };
}
function outboxEntry() {
  return {
    delivery_id:'d-fence', type:'autorun', run_id:'r-fence', tab_id:1,
    report_text:'SEARCH_RESULT_V1\n{}', phase:'claimed', report_prefix_applied:false,
    conversation_key:CKEY, created_at:'2026-08-24T00:00:00Z', updated_at:'2026-08-24T00:00:00Z'
  };
}

function harness({ identityConversationId = CID } = {}) {
  const store = {
    wsmb_auto_runs:{[CKEY]:run()},
    wsmb_outbox:{[CKEY]:outboxEntry()},
    wsmb_manual_modes:{[CKEY]:false},
    ymb_service_contexts:{[CKEY]:{active_service:'search'}},
    ymb_search_policy:{autorun_enabled:true,manual_enabled:true,max_requests_per_run:10,max_cost_rub_per_run:10,allowed_methods:['search'],method_cost_rub:{search:0.488}},
    wsmb_api_key:'k', wsmb_folder_id:'folder'
  };
  const fetchCalls=[];
  let listener=null;
  const storage={
    async get(keys){
      if(keys==null) return clone(store);
      if(typeof keys==='string') return Object.hasOwn(store,keys)?{[keys]:clone(store[keys])}:{};
      if(Array.isArray(keys)){ const out={}; for(const k of keys) if(Object.hasOwn(store,k)) out[k]=clone(store[k]); return out; }
      const out=clone(keys||{}); for(const k of Object.keys(keys||{})) if(Object.hasOwn(store,k)) out[k]=clone(store[k]); return out;
    },
    async set(values){ Object.assign(store,clone(values)); },
    async remove(keys){ for(const k of (Array.isArray(keys)?keys:[keys])) delete store[k]; }
  };
  const chrome={
    storage:{local:storage},
    runtime:{id:'test',lastError:null,onMessage:{addListener(fn){listener=fn;}}},
    tabs:{
      sendMessage(_tabId,message,cb){
        if(message?.type==='WS_GET_IDENTITY') {
          const key=`${ORIGIN}|${identityConversationId}`;
          cb({ok:true,conversation_key:key,identity:{origin:ORIGIN,conversation_id:identityConversationId,conversation_key:key}});
          return;
        }
        cb({ok:true});
      }
    }
  };
  const ctx=vm.createContext({console,chrome,crypto:webcrypto,TextEncoder,TextDecoder,AbortController,performance,setTimeout,clearTimeout,URL,structuredClone,Response,Request,Headers,ReadableStream,Buffer,fetch:async(...args)=>{fetchCalls.push(args); return new Response('{}',{status:200});},importScripts:()=>{}});
  ctx.globalThis=ctx;
  for(const file of ['shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js','shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js','shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js']) {
    vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
  }
  vm.runInContext(workerSource,ctx,{filename:'service_worker.js'});
  assert.equal(typeof listener,'function');
  vm.runInContext(`globalThis.__FENCE_API=Object.freeze({${FN_NAMES.join(',')}});`,ctx);
  return {api:ctx.__FENCE_API,fetchCalls,store};
}

test('Autorun rejects a Search command from a non-owner tab before provider request', async()=>{
  const h=harness();
  const result=await h.api.handleAutoCommand({conversation_key:CKEY,run_id:'r-fence',assistant_turn_id:'t1',command_text:searchCommand()},{tab:{id:2}});
  assert.equal(result.accepted,false);
  assert.equal(result.code,'AUTO_NON_OWNER_TAB');
  assert.equal(h.fetchCalls.length,0);
});

test('Autorun rejects a command when the owner tab is now showing another conversation', async()=>{
  const h=harness({identityConversationId:OTHER});
  const result=await h.api.handleAutoCommand({conversation_key:CKEY,run_id:'r-fence',assistant_turn_id:'t1',command_text:searchCommand()},{tab:{id:1}});
  assert.equal(result.accepted,false);
  assert.equal(result.code,'CONVERSATION_MISMATCH');
  assert.equal(h.fetchCalls.length,0);
});

test('Outbox is not exposed to a non-owner tab for the same conversation', async()=>{
  const h=harness();
  const response=await h.api.handleMessage({type:'WS_GET_OUTBOX',conversation_key:CKEY},{tab:{id:2}});
  assert.equal(response.ok,false);
  assert.equal(response.code,'AUTO_NON_OWNER_TAB');
  assert.equal(response.outbox,undefined);
  assert.equal(h.store.wsmb_outbox[CKEY].phase,'claimed');
});

test('Non-owner tab cannot commit or complete another tab delivery', async()=>{
  const h=harness();
  const committed=await h.api.handleMessage({type:'WS_MARK_DELIVERY_COMMITTED',conversation_key:CKEY,delivery_id:'d-fence'},{tab:{id:2}});
  assert.equal(committed.ok,false);
  assert.equal(committed.code,'AUTO_NON_OWNER_TAB');
  assert.equal(h.store.wsmb_outbox[CKEY].phase,'claimed');

  const completed=await h.api.handleMessage({type:'WS_AUTO_DELIVERY_COMPLETE',conversation_key:CKEY,delivery_id:'d-fence',confirmation_basis:'microphone'},{tab:{id:2}});
  assert.equal(completed.ok,false);
  assert.equal(completed.code,'AUTO_NON_OWNER_TAB');
  assert.equal(h.store.wsmb_outbox[CKEY].delivery_id,'d-fence');
});

test('Owner tab can read its own claimed outbox', async()=>{
  const h=harness();
  const response=await h.api.handleMessage({type:'WS_GET_OUTBOX',conversation_key:CKEY},{tab:{id:1}});
  assert.equal(response.ok,true);
  assert.equal(response.outbox.delivery_id,'d-fence');
});
