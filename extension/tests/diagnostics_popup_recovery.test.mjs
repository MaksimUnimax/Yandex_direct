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
const popupSource = fs.readFileSync(path.join(root, 'popup.js'), 'utf8');
const popupHtml = fs.readFileSync(path.join(root, 'popup.html'), 'utf8');
const FN_NAMES = [...workerSource.matchAll(/^(?:async )?function\s+([A-Za-z0-9_]+)/gm)].map((m) => m[1]);
const CID = '99999999-8888-4777-8666-555555555555';
const CKEY = `https://chatgpt.com|${CID}`;

function clone(value) { return value === undefined ? undefined : structuredClone(value); }
function workerHarness(initial = {}) {
  const store = clone(initial);
  const storage = {
    async get(keys) {
      if (keys == null) return clone(store);
      if (typeof keys === 'string') return Object.hasOwn(store, keys) ? { [keys]: clone(store[keys]) } : {};
      if (Array.isArray(keys)) { const out={}; for (const key of keys) if (Object.hasOwn(store,key)) out[key]=clone(store[key]); return out; }
      const out=clone(keys||{}); for(const key of Object.keys(keys||{})) if(Object.hasOwn(store,key)) out[key]=clone(store[key]); return out;
    },
    async set(values) { Object.assign(store, clone(values)); },
    async remove(keys) { for (const key of (Array.isArray(keys) ? keys : [keys])) delete store[key]; }
  };
  const chrome = { storage:{local:storage}, runtime:{id:'test',lastError:null,onMessage:{addListener(){}}}, tabs:{sendMessage(_id,_m,cb){cb({ok:true});}} };
  const ctx=vm.createContext({console,chrome,crypto:webcrypto,TextEncoder,TextDecoder,AbortController,performance,setTimeout,clearTimeout,URL,structuredClone,Response,Request,Headers,ReadableStream,Buffer,fetch:async()=>new Response('{}',{status:200}),importScripts:()=>{}});
  ctx.globalThis=ctx;
  for(const file of ['shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js','shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js','shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js']) vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
  vm.runInContext(workerSource,ctx,{filename:'service_worker.js'});
  vm.runInContext(`globalThis.__DIAG_API=Object.freeze({${FN_NAMES.join(',')}});`,ctx);
  return {api:ctx.__DIAG_API,store};
}

test('worker diagnostics read path redacts legacy secrets and clear removes all records', async()=>{
  const secret='legacy-secret-key';
  const h=workerHarness({ymb_diagnostics:[
    {ts:'2026-08-20T00:00:00Z',level:'info',code:'ONE',detail:{conversation_key:CKEY,message:'ok'}},
    {ts:'2026-08-20T00:00:01Z',level:'error',code:'TWO',detail:{authorization:`Api-Key ${secret}`,token:secret,secret}}
  ]});
  const records=await h.api.getDiagnostics();
  const json=JSON.stringify(records);
  assert.equal(json.includes(secret),false);
  assert.match(json,/\[REDACTED\]/);
  assert.equal(records.length,2);
  await h.api.clearDiagnostics();
  assert.deepEqual(h.store.ymb_diagnostics,[]);
});

class FakeElement {
  constructor(id=''){ this.id=id; this.value=''; this.checked=false; this.disabled=false; this.textContent=''; this.placeholder=''; this.dataset={}; this.files=[]; this.listeners=new Map(); this.href=''; this.download=''; }
  addEventListener(type,fn){ const list=this.listeners.get(type)||[]; list.push(fn); this.listeners.set(type,list); }
  async dispatch(type){ for(const fn of this.listeners.get(type)||[]) await fn({target:this,preventDefault(){},stopPropagation(){}}); await new Promise(r=>setTimeout(r,0)); }
  click(){ return this.dispatch('click'); }
}
function popupState(){ return {
  product_version:'0.1.1',has_api_key:true,folder_id:'folder',auto_send:true,debug_mode:true,binding:{binding_id:'b1',conversation_key:CKEY},manual_mode:false,manual_operation:null,
  service_context:{active_service:'search'},auto_run:null,auto_start_prompt:{text:'SEARCH START',is_default:true,service:'search'},report_prefix:{enabled:false,text:'',interval:1},
  send_button_profile:null,copy_button_profiles:{},
  wordstat_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['getTop','getDynamics','getRegionsDistribution','getRegionsTree'],max_requests_per_run:100,max_cost_rub_per_run:10,method_cost_rub:{getTop:.02,getDynamics:.02,getRegionsDistribution:.05,getRegionsTree:0}},
  search_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['search'],max_requests_per_run:10,max_cost_rub_per_run:10,method_cost_rub:{search:.488}}
}; }
function popupHarness({clipboardThrows=false,clearFails=false}={}){
  const ids=[...popupHtml.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);
  const elements=Object.fromEntries(ids.map(id=>[id,new FakeElement(id)]));
  const messages=[]; let clipboard='';
  const diagnostics=[
    {ts:'2026-08-20T00:00:00Z',level:'info',code:'CURRENT',detail:{conversation_key:CKEY,message:'current'}},
    {ts:'2026-08-20T00:00:01Z',level:'error',code:'OTHER_ERROR',detail:{conversation_key:'https://chatgpt.com|other',message:'failed'}}
  ];
  const chrome={
    runtime:{lastError:null,sendMessage(message,cb){ messages.push(clone(message)); let response={ok:true};
      if(message.type==='WS_GET_STATE'||message.type==='WS_GET_GLOBAL_STATE') response={ok:true,state:popupState()};
      else if(message.type==='WS_GET_DIAGNOSTICS') response={ok:true,diagnostics:clone(diagnostics)};
      else if(message.type==='WS_CLEAR_DIAGNOSTICS') response=clearFails?{ok:false,error:'clear rejected'}:{ok:true,diagnostics:[]};
      queueMicrotask(()=>cb(response));
    }},
    tabs:{query(_q,cb){queueMicrotask(()=>cb([{id:1,url:`https://chatgpt.com/c/${CID}`}]))},sendMessage(_id,message,cb){ if(message.type==='WS_GET_IDENTITY') queueMicrotask(()=>cb({ok:true,conversation_key:CKEY,identity:{conversation_key:CKEY,origin:'https://chatgpt.com',conversation_id:CID}})); else queueMicrotask(()=>cb({ok:true,applied:true})); }}
  };
  class TestURL extends URL { static createObjectURL(){return 'blob:test';} static revokeObjectURL(){} }
  const navigator={clipboard:{async writeText(value){ if(clipboardThrows) throw new Error('clipboard denied'); clipboard=String(value); }}};
  const document={getElementById(id){return elements[id]||null;},createElement(tag){return new FakeElement(tag);}};
  const ctx=vm.createContext({console,document,chrome,navigator,URL:TestURL,Blob,Date,setTimeout,clearTimeout,queueMicrotask,structuredClone,confirm:()=>true,__YMB_POPUP_TEST__:true}); ctx.globalThis=ctx;
  vm.runInContext(popupSource,ctx,{filename:'popup.js'});
  return {elements,messages,get clipboard(){return clipboard;},settle:()=>new Promise(r=>setTimeout(r,15))};
}

test('popup loads diagnostics, filters them and copies visible diagnostics', async()=>{
  const h=popupHarness(); await h.settle();
  assert.match(h.elements.diagnosticsText.value,/CURRENT/);
  assert.match(h.elements.diagnosticsText.value,/OTHER_ERROR/);
  h.elements.diagnosticsFilter.value='error'; await h.elements.diagnosticsFilter.dispatch('change');
  assert.doesNotMatch(h.elements.diagnosticsText.value,/CURRENT/);
  assert.match(h.elements.diagnosticsText.value,/OTHER_ERROR/);
  await h.elements.copyDiagnostics.dispatch('click'); await h.settle();
  assert.match(h.clipboard,/OTHER_ERROR/);
  assert.equal(h.elements.copyDiagnostics.disabled,false);
});

test('diagnostics clear and clipboard failures stay inside popup and buttons recover', async()=>{
  const clear=popupHarness({clearFails:true}); await clear.settle(); await clear.elements.clearDiagnostics.dispatch('click'); await clear.settle();
  assert.equal(clear.elements.clearDiagnostics.disabled,false);
  assert.equal(clear.elements.status.dataset.level,'error');
  assert.match(clear.elements.status.textContent,/clear rejected/);
  const copy=popupHarness({clipboardThrows:true}); await copy.settle(); await copy.elements.copyDiagnostics.dispatch('click'); await copy.settle();
  assert.equal(copy.elements.copyDiagnostics.disabled,false);
  assert.equal(copy.elements.status.dataset.level,'error');
  assert.match(copy.elements.status.textContent,/clipboard denied/);
});
