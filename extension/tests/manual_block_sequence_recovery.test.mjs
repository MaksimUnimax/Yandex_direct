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

function harness(fetchImpl){
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
  const chrome={
    storage:{local:storage},
    runtime:{id:'test-extension',lastError:null,onMessage:{addListener(){}}},
    tabs:{
      async query(){return[{id:1,url:`${ORIGIN}/c/${CID}`}]},
      async get(id){return Number(id)===1?{id:1,url:`${ORIGIN}/c/${CID}`}:null;},
      sendMessage(_id,message,cb){
        if(['WS_GET_IDENTITY','WS_PAGE_CONTEXT'].includes(message?.type))return cb({ok:true,identity:IDENTITY,conversation_key:CKEY});
        cb({ok:true});
      }
    }
  };
  const ctx=vm.createContext({console,chrome,crypto:webcrypto,TextEncoder,TextDecoder,AbortController,performance,setTimeout,clearTimeout,URL,structuredClone,Response,Request,Headers,ReadableStream,Buffer,fetch:async(...args)=>{fetchCalls.push(args);return fetchImpl(...args);},importScripts:()=>{}});
  ctx.globalThis=ctx;
  for(const file of ['shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js','shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js','shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js']) vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
  vm.runInContext(workerSource,ctx,{filename:'service_worker.js'});
  vm.runInContext(`globalThis.__SEQ_API=Object.freeze({${fnNames.join(',')}});`,ctx);
  return{api:ctx.__SEQ_API,store,fetchCalls};
}

test('two Search commands in one Manual block execute serially in source order and create one delivery',async()=>{
  const seen=[];
  const h=harness(async(_url,init)=>{
    const body=JSON.parse(init.body); seen.push(body.query.queryText);
    return new Response(JSON.stringify({rawData:xml64()}),{status:200});
  });
  const block=`Текст до\n${command('первый запрос')}\nтекст между\n${command('второй запрос')}\nтекст после`;
  const r=await h.api.executeManualBlock(block,CKEY,{tab:{id:1}},'multi-ok');
  assert.equal(r.accepted,true);
  assert.deepEqual(seen,['первый запрос','второй запрос']);
  assert.equal(h.fetchCalls.length,2);
  assert.equal(h.store.wsmb_outbox[CKEY].provider_executions,2);
  assert.equal((r.report_text.match(/SEARCH_RESULT_V1/g)||[]).length,2);
});

test('UNKNOWN outcome of first Manual command stops every later provider initiation',async()=>{
  let attempt=0;
  const h=harness(async()=>{
    attempt+=1;
    if(attempt===1)throw new TypeError('connection lost after initiation');
    return new Response(JSON.stringify({rawData:xml64()}),{status:200});
  });
  const block=`${command('неизвестный исход')}\n${command('не запускать')}`;
  const r=await h.api.executeManualBlock(block,CKEY,{tab:{id:1}},'multi-unknown');
  assert.equal(r.accepted,true);
  assert.equal(h.fetchCalls.length,1,'second paid request must not start after UNKNOWN outcome');
  assert.match(r.report_text,/REQUEST_OUTCOME_UNKNOWN_NO_RETRY/);
  assert.doesNotMatch(r.report_text,/не запускать/);
});
