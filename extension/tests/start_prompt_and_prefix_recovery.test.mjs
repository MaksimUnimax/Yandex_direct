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
const CKEY = `https://chatgpt.com|${CID}`;

function clone(value) { return value === undefined ? undefined : structuredClone(value); }
function harness(initial={}) {
  const store=clone(initial);
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
    runtime:{id:'test',lastError:null,onMessage:{addListener(){}}},
    tabs:{sendMessage(_id,_message,cb){cb({ok:true});}}
  };
  const ctx=vm.createContext({console,chrome,crypto:webcrypto,TextEncoder,TextDecoder,AbortController,performance,setTimeout,clearTimeout,URL,structuredClone,Response,Request,Headers,ReadableStream,Buffer,fetch:async()=>new Response('{}',{status:200}),importScripts:()=>{}});
  ctx.globalThis=ctx;
  for(const file of ['shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js','shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js','shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js']) {
    vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
  }
  vm.runInContext(workerSource,ctx,{filename:'service_worker.js'});
  vm.runInContext(`globalThis.__PROMPT_API=Object.freeze({${FN_NAMES.join(',')}});`,ctx);
  return {api:ctx.__PROMPT_API,store};
}

test('default Autorun start text is service-aware for Search and Wordstat', async()=>{
  const h=harness();
  const search=await h.api.getAutoStartPrompt(CKEY,{service:'search'});
  const wordstat=await h.api.getAutoStartPrompt(CKEY,{service:'wordstat'});
  assert.equal(search.service,'search');
  assert.match(search.text,/SEARCH_API_V1/);
  assert.doesNotMatch(search.text,/WORDSTAT_API_V1/);
  assert.equal(wordstat.service,'wordstat');
  assert.match(wordstat.text,/WORDSTAT_API_V1/);
});

test('Search start text can be saved and reset back to Search default', async()=>{
  const h=harness();
  const saved=await h.api.saveAutoStartPrompt(CKEY,'CUSTOM SEARCH START',{service:'search'});
  assert.equal(saved.text,'CUSTOM SEARCH START');
  assert.equal(saved.service,'search');
  const current=await h.api.getAutoStartPrompt(CKEY,{service:'search'});
  assert.equal(current.text,'CUSTOM SEARCH START');
  const reset=await h.api.resetAutoStartPrompt(CKEY,{service:'search'});
  assert.equal(reset.service,'search');
  assert.match(reset.text,/SEARCH_API_V1/);
});

test('report prefix is added only when enabled and confirmation advances its counter once', async()=>{
  const h=harness();
  await h.api.saveReportPrefix(CKEY,{enabled:true,text:'PREFIX',interval:1});
  const applied=await h.api.applyPrefixToReport(CKEY,'SEARCH_RESULT_V1\n{}');
  assert.equal(applied.applied,true);
  assert.equal(applied.text,'PREFIX\n\nSEARCH_RESULT_V1\n{}');
  await h.api.noteConfirmedReportPrefix(CKEY,true,'delivery-1');
  await h.api.noteConfirmedReportPrefix(CKEY,true,'delivery-1');
  const state=await h.api.getReportPrefix(CKEY);
  assert.equal(state.delivered_count,1);
  assert.equal(state.last_confirmed_delivery_id,'delivery-1');
});
