import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const composerSource = fs.readFileSync(path.join(root, 'shared/composer_send.js'), 'utf8');
const contentSource = fs.readFileSync(path.join(root, 'content_script.js'), 'utf8');
const popupSource = fs.readFileSync(path.join(root, 'popup.js'), 'utf8');
const popupHtml = fs.readFileSync(path.join(root, 'popup.html'), 'utf8');
const workerSource = fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8');
const CID='99999999-8888-4777-8666-555555555555';
const CKEY=`https://chatgpt.com|${CID}`;

function plain(value){ return value === undefined ? undefined : JSON.parse(JSON.stringify(value)); }

test('saved Send profile is tried before generic Send selectors',()=>{
  const custom={disabled:false};
  const generic={disabled:false};
  const queries=[];
  const doc={querySelector(selector){ queries.push(selector); if(selector==='#learned-send') return custom; if(selector==='button[data-testid="send-button"]') return generic; return null; }};
  const ctx=vm.createContext({console}); ctx.globalThis=ctx;
  vm.runInContext(composerSource,ctx,{filename:'composer_send.js'});
  assert.equal(ctx.BB2ComposerSend.findSendButton(doc,{selector:'#learned-send'}),custom);
  assert.equal(queries[0],'#learned-send');
});

test('content script owns one-shot Send/Copy picker messages and saves selected profiles through worker',()=>{
  assert.match(contentSource,/WS_START_SEND_BUTTON_PICKER/);
  assert.match(contentSource,/WS_START_COPY_BUTTON_PICKER/);
  assert.match(contentSource,/WS_SAVE_SEND_BUTTON_PROFILE/);
  assert.match(contentSource,/WS_SAVE_COPY_BUTTON_PROFILE/);
  assert.match(contentSource,/preventDefault\(\)/);
  assert.match(contentSource,/stopImmediatePropagation\(\)/);
});

test('worker accepts one selected Copy profile without disturbing Send profile support',()=>{
  assert.match(workerSource,/case "WS_SAVE_COPY_BUTTON_PROFILE"/);
  assert.match(workerSource,/saveCopyButtonProfile/);
  assert.match(workerSource,/case "WS_CLEAR_SEND_BUTTON_PROFILE"/);
  assert.match(workerSource,/case "WS_CLEAR_COPY_BUTTON_PROFILES"/);
});

class FakeElement {
  constructor(id=''){ this.id=id; this.value=''; this.checked=false; this.disabled=false; this.textContent=''; this.placeholder=''; this.dataset={}; this.files=[]; this.listeners=new Map(); this.href=''; this.download=''; }
  addEventListener(type,fn){ const list=this.listeners.get(type)||[]; list.push(fn); this.listeners.set(type,list); }
  async dispatch(type){ for(const fn of this.listeners.get(type)||[]) await fn({target:this,preventDefault(){},stopPropagation(){}}); await new Promise(r=>setTimeout(r,0)); }
  click(){ return this.dispatch('click'); }
}
function popupState(){ return {
  product_version:'0.1.1',has_api_key:true,folder_id:'folder',auto_send:true,debug_mode:false,binding:{binding_id:'b1',conversation_key:CKEY},manual_mode:false,manual_operation:null,
  service_context:{active_service:'search'},auto_run:null,auto_start_prompt:{text:'SEARCH START',is_default:true,service:'search'},report_prefix:{enabled:false,text:'',interval:1},
  send_button_profile:{selector:'#saved-send'},copy_button_profiles:[{selector:'#saved-copy'}],
  wordstat_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['getTop','getDynamics','getRegionsDistribution','getRegionsTree'],max_requests_per_run:100,max_cost_rub_per_run:10,method_cost_rub:{getTop:.02,getDynamics:.02,getRegionsDistribution:.05,getRegionsTree:0}},
  search_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['search'],max_requests_per_run:10,max_cost_rub_per_run:10,method_cost_rub:{search:.488}}
}; }
function popupHarness(){
  const ids=[...popupHtml.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);
  const elements=Object.fromEntries(ids.map(id=>[id,new FakeElement(id)]));
  const runtimeMessages=[]; const tabMessages=[];
  const chrome={
    runtime:{lastError:null,sendMessage(message,cb){runtimeMessages.push(plain(message)); let response={ok:true}; if(message.type==='WS_GET_STATE'||message.type==='WS_GET_GLOBAL_STATE') response={ok:true,state:popupState()}; else if(message.type==='WS_GET_DIAGNOSTICS') response={ok:true,diagnostics:[]}; else if(message.type==='WS_CLEAR_SEND_BUTTON_PROFILE'||message.type==='WS_CLEAR_COPY_BUTTON_PROFILES') response={ok:true,state:popupState()}; queueMicrotask(()=>cb(response));}},
    tabs:{query(_q,cb){queueMicrotask(()=>cb([{id:1,url:`https://chatgpt.com/c/${CID}`}]))},sendMessage(_id,message,cb){tabMessages.push(plain(message)); if(message.type==='WS_GET_IDENTITY') queueMicrotask(()=>cb({ok:true,conversation_key:CKEY,identity:{conversation_key:CKEY,origin:'https://chatgpt.com',conversation_id:CID}})); else queueMicrotask(()=>cb({ok:true,started:true}));}}
  };
  class TestURL extends URL { static createObjectURL(){return 'blob:test';} static revokeObjectURL(){} }
  const document={getElementById(id){return elements[id]||null;},createElement(tag){return new FakeElement(tag);}};
  const navigator={clipboard:{async writeText(){}}};
  const ctx=vm.createContext({console,document,chrome,navigator,URL:TestURL,Blob,Date,setTimeout,clearTimeout,queueMicrotask,structuredClone,confirm:()=>true,__YMB_POPUP_TEST__:true}); ctx.globalThis=ctx;
  vm.runInContext(popupSource,ctx,{filename:'popup.js'});
  return {elements,runtimeMessages,tabMessages,settle:()=>new Promise(r=>setTimeout(r,15))};
}

test('popup restores exact legacy picker/clear controls and routes them to page/worker',async()=>{
  const h=popupHarness(); await h.settle();
  assert.match(h.elements.sendProfileMeta.textContent,/настроен/i);
  assert.match(h.elements.copyProfileMeta.textContent,/1/);
  await h.elements.pickSend.dispatch('click'); await h.settle();
  assert.equal(h.tabMessages.some(m=>m.type==='WS_START_SEND_BUTTON_PICKER'),true);
  await h.elements.pickCopy.dispatch('click'); await h.settle();
  assert.equal(h.tabMessages.some(m=>m.type==='WS_START_COPY_BUTTON_PICKER'),true);
  await h.elements.clearSend.dispatch('click'); await h.settle();
  assert.equal(h.runtimeMessages.some(m=>m.type==='WS_CLEAR_SEND_BUTTON_PROFILE'),true);
  await h.elements.clearCopy.dispatch('click'); await h.settle();
  assert.equal(h.runtimeMessages.some(m=>m.type==='WS_CLEAR_COPY_BUTTON_PROFILES'),true);
  for(const id of ['pickSend','pickCopy','clearSend','clearCopy']) assert.equal(h.elements[id].disabled,false);
});
