import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';
import { performance } from 'node:perf_hooks';
import { fileURLToPath } from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../src');
const workerSource=fs.readFileSync(path.join(root,'service_worker.js'),'utf8');
const fnNames=[...workerSource.matchAll(/^(?:async )?function\s+([A-Za-z0-9_]+)/gm)].map(m=>m[1]);
const CID='99999999-8888-4777-8666-555555555555';
const ORIGIN='https://chatgpt.com';
const CKEY=`${ORIGIN}|${CID}`;
const IDENTITY={origin:ORIGIN,conversation_id:CID,status:'confirmed',source:'path',chat_path:`/c/${CID}`};
const binding={binding_id:'b1',revision:1,origin:ORIGIN,conversation_id:CID,conversation_key:CKEY,bound_at:'2026-08-20T00:00:00Z',updated_at:'2026-08-20T00:00:00Z'};
const clone=v=>v===undefined?undefined:structuredClone(v);
const command=q=>`SEARCH_API_V1\n${JSON.stringify({method:'search',queryText:q})}`;
const xml64=()=>Buffer.from('<?xml version="1.0"?><yandexsearch><response><results><grouping><group><doc><url>https://example.test/</url><title>ok</title></doc></group></grouping></results></response></yandexsearch>','utf8').toString('base64');

function harness(){
  const store={
    wsmb_api_key:'ascii-key',
    wsmb_folder_id:'folder',
    wsmb_conversation_bindings:{[CKEY]:binding},
    wsmb_manual_modes:{[CKEY]:true},
    ymb_service_contexts:{[CKEY]:{active_service:'search'}},
    ymb_search_policy:{manual_enabled:true,autorun_enabled:false,allowed_methods:['search'],max_requests_per_run:10,max_cost_rub_per_run:10,method_cost_rub:{search:0.488}}
  };
  const fetchCalls=[];
  const storage={
    async get(keys){
      if(keys==null)return clone(store);
      if(typeof keys==='string')return Object.hasOwn(store,keys)?{[keys]:clone(store[keys])}:{};
      if(Array.isArray(keys)){const out={};for(const k of keys)if(Object.hasOwn(store,k))out[k]=clone(store[k]);return out;}
      const out=clone(keys||{});for(const k of Object.keys(keys||{}))if(Object.hasOwn(store,k))out[k]=clone(store[k]);return out;
    },
    async set(values){Object.assign(store,clone(values));},
    async remove(keys){for(const k of (Array.isArray(keys)?keys:[keys]))delete store[k];}
  };
  let listener=null;
  const chrome={
    storage:{local:storage},
    runtime:{id:'test-extension',lastError:null,onMessage:{addListener(fn){listener=fn;}}},
    tabs:{
      async query(){return[{id:1,url:`${ORIGIN}/c/${CID}`}]},
      async get(id){return Number(id)===1?{id:1,url:`${ORIGIN}/c/${CID}`}:null;},
      sendMessage(_id,message,cb){
        if(['WS_GET_IDENTITY','WS_PAGE_CONTEXT'].includes(message?.type))return cb({ok:true,identity:IDENTITY,conversation_key:CKEY});
        cb({ok:true});
      }
    }
  };
  const ctx=vm.createContext({console,chrome,crypto:webcrypto,TextEncoder,TextDecoder,AbortController,performance,setTimeout,clearTimeout,URL,structuredClone,Response,Request,Headers,ReadableStream,Buffer,fetch:async(...args)=>{fetchCalls.push(args);return new Response(JSON.stringify({rawData:xml64()}),{status:200});},importScripts:()=>{}});
  ctx.globalThis=ctx;
  for(const file of ['shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js','shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js','shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js']) vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
  vm.runInContext(workerSource,ctx,{filename:'service_worker.js'});
  assert.equal(typeof listener,'function');
  vm.runInContext(`globalThis.__DELIVERY_API=Object.freeze({${fnNames.join(',')}});`,ctx);
  return{api:ctx.__DELIVERY_API,store,fetchCalls};
}

test('confirmed Manual delivery clears outbox, releases lock, and allows a later distinct Search action',async()=>{
  const h=harness();
  const first=await h.api.executeManualBlock(command('первый'),CKEY,{tab:{id:1}},'delivery-1');
  assert.equal(first.accepted,true);
  assert.equal(h.fetchCalls.length,1);
  assert.equal(h.store.wsmb_outbox[CKEY].phase,'claimed');
  assert.equal(h.store.wsmb_manual_operations[CKEY].status,'delivering');

  const committed=await h.api.handleMessage({type:'WS_MARK_DELIVERY_COMMITTED',conversation_key:CKEY,delivery_id:first.delivery_id},{tab:{id:1}});
  assert.equal(committed.ok,true);
  assert.equal(h.store.wsmb_outbox[CKEY].phase,'committed');

  const completed=await h.api.handleMessage({type:'WS_MANUAL_DELIVERY_COMPLETE',conversation_key:CKEY,delivery_id:first.delivery_id,confirmation_basis:'microphone'},{tab:{id:1}});
  assert.equal(completed.ok,true);
  assert.equal(h.store.wsmb_outbox[CKEY],undefined);
  assert.equal(h.store.wsmb_manual_operations[CKEY].status,'completed');
  assert.equal(h.store.wsmb_manual_operations[CKEY].delivery_confirmed,true);

  const second=await h.api.executeManualBlock(command('второй'),CKEY,{tab:{id:1}},'delivery-2');
  assert.equal(second.accepted,true);
  assert.equal(h.fetchCalls.length,2);
});

test('wrong delivery id cannot clear outbox or release Manual single-flight lock',async()=>{
  const h=harness();
  const first=await h.api.executeManualBlock(command('первый'),CKEY,{tab:{id:1}},'delivery-lock-1');
  const wrong=await h.api.handleMessage({type:'WS_MANUAL_DELIVERY_COMPLETE',conversation_key:CKEY,delivery_id:'wrong-delivery',confirmation_basis:'microphone'},{tab:{id:1}});
  assert.equal(wrong.ok,false);
  assert.equal(wrong.code,'DELIVERY_NOT_FOUND');
  assert.equal(h.store.wsmb_outbox[CKEY].delivery_id,first.delivery_id);
  assert.equal(h.store.wsmb_manual_operations[CKEY].status,'delivering');

  const blocked=await h.api.executeManualBlock(command('второй'),CKEY,{tab:{id:1}},'delivery-lock-2');
  assert.equal(blocked.accepted,false);
  assert.equal(blocked.code,'MANUAL_OPERATION_ACTIVE');
  assert.equal(h.fetchCalls.length,1);
});
