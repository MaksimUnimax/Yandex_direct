import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const popupSource = fs.readFileSync(path.join(root, 'popup.js'), 'utf8');
const popupHtml = fs.readFileSync(path.join(root, 'popup.html'), 'utf8');
const identitySource = fs.readFileSync(path.join(root, 'shared/conversation_identity.js'), 'utf8');
const CID = '99999999-8888-4777-8666-555555555555';
const KEY = `https://chatgpt.com|${CID}`;
const PROJECT_URL = `https://chatgpt.com/g/g-p-example-project/project-name/c/${CID}`;

class FakeElement {
  constructor(id='') { this.id=id; this.value=''; this.checked=false; this.disabled=false; this.textContent=''; this.placeholder=''; this.dataset={}; this.listeners=new Map(); }
  addEventListener(type,fn){ const list=this.listeners.get(type)||[]; list.push(fn); this.listeners.set(type,list); }
}

function identityFor(url) {
  const ctx = vm.createContext({ URL, console });
  ctx.globalThis = ctx;
  vm.runInContext(identitySource, ctx, { filename:'conversation_identity.js' });
  return ctx.BB2ConversationIdentity.identityFromUrl(url);
}

function baseState() {
  return {
    product_version:'0.1.1', has_api_key:false, folder_id:'', auto_send:true, debug_mode:false,
    binding:null, manual_mode:false, manual_operation:null,
    service_context:{active_service:'wordstat'}, auto_run:null,
    auto_start_prompt:{text:'START',is_default:true,service:'wordstat'},
    report_prefix:{enabled:false,text:'',interval:1,delivered_count:0,last_applied_at_count:0},
    wordstat_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['getTop','getDynamics','getRegionsDistribution','getRegionsTree'],max_requests_per_run:100,max_cost_rub_per_run:10,method_cost_rub:{getTop:.02,getDynamics:.02,getRegionsDistribution:.05,getRegionsTree:0}},
    search_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['search'],max_requests_per_run:100,max_cost_rub_per_run:10,method_cost_rub:{search:.488}}
  };
}

function harness() {
  const ids=[...popupHtml.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);
  const elements=Object.fromEntries(ids.map(id=>[id,new FakeElement(id)]));
  const calls=[];
  const identity=identityFor(PROJECT_URL);
  const state=baseState();
  const document={ getElementById(id){return elements[id]||null;}, createElement(){return new FakeElement();} };
  const chrome={
    runtime:{lastError:null,sendMessage(message,cb){
      calls.push({channel:'runtime',message:structuredClone(message)});
      if(message.type==='WS_GET_STATE') queueMicrotask(()=>cb({ok:true,state:structuredClone(state)}));
      else if(message.type==='WS_GET_DIAGNOSTICS') queueMicrotask(()=>cb({ok:true,diagnostics:[]}));
      else queueMicrotask(()=>cb({ok:true,state:structuredClone(state)}));
    }},
    tabs:{
      query(_q,cb){ calls.push({channel:'tabs.query'}); queueMicrotask(()=>cb([{id:7,url:PROJECT_URL}])) },
      sendMessage(tabId,message,cb){
        calls.push({channel:'tab',tabId,message:structuredClone(message)});
        if(message.type==='WS_GET_IDENTITY') queueMicrotask(()=>cb({ok:true,conversation_key:identity.conversation_key,identity}));
        else queueMicrotask(()=>cb({ok:true}));
      }
    }
  };
  class TestURL extends URL { static createObjectURL(){return 'blob:test';} static revokeObjectURL(){} }
  const ctx=vm.createContext({console,document,chrome,URL:TestURL,Blob,Date,setTimeout,clearTimeout,queueMicrotask,structuredClone,confirm:()=>true,__YMB_POPUP_TEST__:true});
  ctx.globalThis=ctx;
  vm.runInContext(popupSource,ctx,{filename:'popup.js'});
  return {elements,calls,settle:()=>new Promise(r=>setTimeout(r,20))};
}

test('popup initializes on ChatGPT Project/Work nested conversation route', async () => {
  const h=harness();
  await h.settle();
  assert.equal(h.elements.conversationMeta.textContent, KEY);
  assert.equal(h.elements.activeService.disabled, false);
  assert.equal(h.elements.bindConversation.disabled, false);
  assert.equal(h.elements.manualMode.disabled, false);
  assert.ok(h.calls.some(c=>c.channel==='tab' && c.message?.type==='WS_GET_IDENTITY'));
  assert.ok(h.calls.some(c=>c.channel==='runtime' && c.message?.type==='WS_GET_STATE' && c.message?.conversation_key===KEY));
  assert.equal(h.calls.some(c=>c.message?.type==='WS_GET_GLOBAL_STATE'), false);
});
