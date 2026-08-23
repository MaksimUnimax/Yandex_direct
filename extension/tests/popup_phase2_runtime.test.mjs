import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const popupSource = fs.readFileSync(path.join(root, 'popup.js'), 'utf8');
const popupHtml = fs.readFileSync(path.join(root, 'popup.html'), 'utf8');
const CID='99999999-8888-4777-8666-555555555555';
const CKEY=`https://chatgpt.com|${CID}`;

function baseState(overrides={}) {
  return {
    product_version:'0.1.1', has_api_key:true, folder_id:'folder', auto_send:true, debug_mode:false,
    binding:{binding_id:'b1',conversation_key:CKEY}, manual_mode:false, manual_operation:null,
    service_context:{active_service:'search'}, auto_run:null,
    auto_start_prompt:{text:'SEARCH START',is_default:true,service:'search'},
    report_prefix:{enabled:false,text:'',interval:1,delivered_count:0,last_applied_at_count:0},
    wordstat_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['getTop','getDynamics','getRegionsDistribution','getRegionsTree'],max_requests_per_run:100,max_cost_rub_per_run:10,method_cost_rub:{getTop:.02,getDynamics:.02,getRegionsDistribution:.05,getRegionsTree:0},tariff_checked_at:'2026-08-12',tariff_source:'official'},
    search_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['search'],max_requests_per_run:7,max_cost_rub_per_run:3,method_cost_rub:{search:.488},tariff_checked_at:'2026-08-19',tariff_source:'official'},
    ...overrides
  };
}

class FakeElement {
  constructor(id='') { this.id=id; this.value=''; this.checked=false; this.disabled=false; this.textContent=''; this.placeholder=''; this.dataset={}; this.files=[]; this.listeners=new Map(); this.href=''; this.download=''; }
  addEventListener(type, fn) { const a=this.listeners.get(type)||[]; a.push(fn); this.listeners.set(type,a); }
  async dispatch(type) { for (const fn of this.listeners.get(type)||[]) await fn({ target:this, preventDefault(){}, stopPropagation(){} }); await new Promise(r=>setTimeout(r,0)); }
  click() { return this.dispatch('click'); }
}

function popupHarness(state=baseState(), { applyManualOk=true }={}) {
  const ids=[...popupHtml.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);
  const elements=Object.fromEntries(ids.map(id=>[id,new FakeElement(id)]));
  const calls=[];
  let currentState=structuredClone(state);
  const document={
    getElementById(id){ return elements[id] || null; },
    createElement(tag){ return new FakeElement(tag); }
  };
  const chrome={
    runtime:{
      lastError:null,
      sendMessage(message,cb){
        calls.push({channel:'runtime',message:structuredClone(message)});
        let response={ok:true};
        if(message.type==='WS_GET_STATE') response={ok:true,state:structuredClone(currentState)};
        else if(message.type==='WS_GET_GLOBAL_STATE') response={ok:true,state:structuredClone(currentState)};
        else if(message.type==='WS_SET_MANUAL_MODE') { currentState={...currentState,manual_mode:message.enabled===true}; response={ok:true,enabled:message.enabled===true,state:structuredClone(currentState)}; }
        else if(message.type==='WS_PATCH_TOGGLES') {
          if(Object.hasOwn(message,'auto_send')) currentState.auto_send=message.auto_send===true;
          if(Object.hasOwn(message,'debug_mode')) currentState.debug_mode=message.debug_mode===true;
          if(Object.hasOwn(message,'wordstat_autorun_enabled')) currentState.wordstat_policy={...currentState.wordstat_policy,autorun_enabled:message.wordstat_autorun_enabled===true};
          if(Object.hasOwn(message,'search_autorun_enabled')) currentState.search_policy={...currentState.search_policy,autorun_enabled:message.search_autorun_enabled===true};
          if(Object.hasOwn(message,'report_prefix_enabled')) currentState.report_prefix={...currentState.report_prefix,enabled:message.report_prefix_enabled===true};
          response={ok:true,state:structuredClone(currentState)};
        } else if(message.type==='WS_SAVE_SETTINGS') {
          if(message.active_service) currentState.service_context={active_service:message.active_service};
          if(message.search_policy) currentState.search_policy=structuredClone(message.search_policy);
          if(message.wordstat_policy) currentState.wordstat_policy=structuredClone(message.wordstat_policy);
          if(message.report_prefix) currentState.report_prefix={...currentState.report_prefix,...structuredClone(message.report_prefix)};
          response={ok:true,state:structuredClone(currentState)};
        } else if(message.type==='WS_BIND_CONVERSATION') response={ok:true,binding:currentState.binding,conversation_key:CKEY};
        else if(message.type==='WS_START_AUTORUN') { currentState.auto_run={run_id:'r1',active_service:currentState.service_context.active_service,status:'starting'}; response={ok:true,run:structuredClone(currentState.auto_run)}; }
        else if(message.type==='WS_PAUSE_AUTORUN') { currentState.auto_run={...(currentState.auto_run||{}),status:'paused'}; response={ok:true,run:structuredClone(currentState.auto_run)}; }
        else if(message.type==='WS_RESUME_AUTORUN') { currentState.auto_run={...(currentState.auto_run||{}),status:'waiting_command'}; response={ok:true,run:structuredClone(currentState.auto_run)}; }
        else if(message.type==='WS_FINISH_AUTORUN') { currentState.auto_run={...(currentState.auto_run||{}),status:'stopped'}; response={ok:true,run:structuredClone(currentState.auto_run)}; }
        else if(message.type==='WS_SAVE_AUTO_START_PROMPT') response={ok:true,auto_start_prompt:{text:message.text,is_default:false,service:message.active_service}};
        else if(message.type==='WS_RESET_AUTO_START_PROMPT') response={ok:true,auto_start_prompt:{text:'DEFAULT',is_default:true,service:message.active_service}};
        else if(message.type==='WS_EXPORT_BACKUP') response={ok:true,backup:{schema:'YMB_SETTINGS_BACKUP_V2',settings:{}}};
        else if(message.type==='WS_IMPORT_BACKUP') response={ok:true,result:{imported:true},state:structuredClone(currentState)};
        queueMicrotask(()=>cb(response));
      }
    },
    tabs:{
      query(_query,cb){ calls.push({channel:'tabs.query'}); queueMicrotask(()=>cb([{id:1,url:`https://chatgpt.com/c/${CID}`}])) },
      sendMessage(tabId,message,cb){
        calls.push({channel:'tab',tabId,message:structuredClone(message)});
        let response={ok:true};
        if(message.type==='WS_GET_IDENTITY') response={ok:true,conversation_key:CKEY,identity:{conversation_key:CKEY,origin:'https://chatgpt.com',conversation_id:CID}};
        else if(message.type==='WS_APPLY_MANUAL_MODE') response=applyManualOk?{ok:true,applied:true}:{ok:false,applied:false,code:'APPLY_FAILED'};
        queueMicrotask(()=>cb(response));
      }
    }
  };
  class TestURL extends URL { static createObjectURL(){ return 'blob:test'; } static revokeObjectURL(){} }
  const ctx=vm.createContext({console,document,chrome,URL:TestURL,Blob,Date,setTimeout,clearTimeout,queueMicrotask,structuredClone,confirm:()=>true,__YMB_POPUP_TEST__:true});
  ctx.globalThis=ctx;
  vm.runInContext(popupSource,ctx,{filename:'popup.js'});
  return {ctx,elements,calls,getState:()=>currentState,settle:()=>new Promise(r=>setTimeout(r,10))};
}

test('popup exposes Wordstat/Search controls, Search Manual permission, never renders saved API key, and uses current worker state messages', async()=>{
  const h=popupHarness(); await h.settle();
  assert.match(popupHtml,/option value="wordstat"/);
  assert.match(popupHtml,/option value="search"/);
  assert.match(popupHtml,/id="searchManualEnabled"/);
  assert.equal(h.elements.activeService.value,'search');
  assert.equal(h.elements.searchManualEnabled.checked,true);
  assert.equal(h.elements.apiKey.value,'');
  assert.match(h.elements.apiKey.placeholder,/Ключ сохранён/);
  assert.equal(h.elements.costSearch.value,'0.488');
  assert.ok(h.calls.some(c=>c.message?.type==='WS_GET_STATE'));
  assert.doesNotMatch(popupSource,/WS_GET_POPUP_STATE|WS_SAVE_CREDENTIALS|YMB_SET_ACTIVE_SERVICE|WS_AUTO_START|YMB_EXPORT_SETTINGS/);
});

test('Search Manual policy OFF disables enabling conversation Manual mode and explains policy block', async()=>{
  const h=popupHarness(baseState({
    manual_mode:false,
    search_policy:{...baseState().search_policy,manual_enabled:false}
  }));
  await h.settle();
  assert.equal(h.elements.searchManualEnabled.checked,false);
  assert.equal(h.elements.manualMode.checked,false);
  assert.equal(h.elements.manualMode.disabled,true);
  assert.match(h.elements.manualModeMeta.textContent,/запрещён политикой/i);
});

test('Search Manual policy OFF still leaves active Manual mode switch available so operator can turn it off', async()=>{
  const h=popupHarness(baseState({
    manual_mode:true,
    search_policy:{...baseState().search_policy,manual_enabled:false}
  }));
  await h.settle();
  assert.equal(h.elements.searchManualEnabled.checked,false);
  assert.equal(h.elements.manualMode.checked,true);
  assert.equal(h.elements.manualMode.disabled,false);
});

test('Manual ON commits worker state before applying page mode and sends active Search service', async()=>{
  const h=popupHarness(); await h.settle(); h.calls.length=0;
  h.elements.manualMode.checked=true;
  await h.elements.manualMode.dispatch('change'); await h.settle();
  const workerIndex=h.calls.findIndex(c=>c.message?.type==='WS_SET_MANUAL_MODE');
  const pageIndex=h.calls.findIndex(c=>c.message?.type==='WS_APPLY_MANUAL_MODE');
  assert.ok(workerIndex>=0 && pageIndex>workerIndex,`order ${workerIndex}/${pageIndex}`);
  assert.equal(h.calls[pageIndex].message.active_service,'search');
});

test('failed page Manual apply rolls worker state back', async()=>{
  const h=popupHarness(baseState(),{applyManualOk:false}); await h.settle(); h.calls.length=0;
  h.elements.manualMode.checked=true;
  await h.elements.manualMode.dispatch('change'); await h.settle();
  const manualCalls=h.calls.filter(c=>c.message?.type==='WS_SET_MANUAL_MODE');
  assert.equal(manualCalls.length,2);
  assert.equal(manualCalls[0].message.enabled,true);
  assert.equal(manualCalls[1].message.enabled,false);
  assert.equal(h.elements.manualMode.checked,false);
});

test('Search autorun toggle persists only the toggle and does not commit unsaved credentials/text fields', async()=>{
  const h=popupHarness(); await h.settle(); h.calls.length=0;
  h.elements.apiKey.value='UNSAVED-SECRET'; h.elements.reportPrefixText.value='UNSAVED-TEXT';
  h.elements.searchAutorunEnabled.checked=false;
  await h.elements.searchAutorunEnabled.dispatch('change'); await h.settle();
  const runtime=h.calls.filter(c=>c.channel==='runtime').map(c=>c.message);
  assert.equal(runtime[0].type,'WS_PATCH_TOGGLES');
  assert.equal(runtime[0].search_autorun_enabled,false);
  assert.equal(runtime.some(m=>m.type==='WS_SAVE_SETTINGS'),false);
  assert.equal(JSON.stringify(runtime).includes('UNSAVED-SECRET'),false);
  assert.equal(JSON.stringify(runtime).includes('UNSAVED-TEXT'),false);
});

test('explicit Save persists operator-selected Search Manual permission with separate Search policy', async()=>{
  const h=popupHarness(); await h.settle(); h.calls.length=0;
  h.elements.activeService.value='search'; h.elements.apiKey.value='';
  h.elements.searchManualEnabled.checked=false;
  h.elements.searchMaxRequestsRun.value='9'; h.elements.searchMaxCostRun.value='4.5'; h.elements.costSearch.value='0.488';
  h.elements.reportPrefixEnabled.checked=true; h.elements.reportPrefixText.value='PREFIX';
  await h.ctx.__YMB_POPUP_TEST_API__.saveAll(); await h.settle();
  const msg=h.calls.find(c=>c.message?.type==='WS_SAVE_SETTINGS')?.message;
  assert.ok(msg);
  assert.equal(msg.active_service,'search');
  assert.equal(msg.search_policy.manual_enabled,false);
  assert.equal(msg.search_policy.max_requests_per_run,9);
  assert.equal(msg.search_policy.max_cost_rub_per_run,4.5);
  assert.equal(msg.search_policy.method_cost_rub.search,0.488);
  assert.equal(msg.wordstat_policy.allowed_methods.includes('getTop'),true);
  assert.deepEqual(msg.report_prefix,{enabled:true,text:'PREFIX',interval:1});
  assert.equal(Object.hasOwn(msg,'api_key'),false);
  assert.equal(h.getState().search_policy.manual_enabled,false);
});

test('Search start saves selected service/settings before starting and uses current run message names', async()=>{
  const h=popupHarness(); await h.settle(); h.calls.length=0;
  h.elements.activeService.value='search';
  await h.elements.startAuto.dispatch('click'); await h.settle();
  const saveIndex=h.calls.findIndex(c=>c.message?.type==='WS_SAVE_SETTINGS');
  const startIndex=h.calls.findIndex(c=>c.message?.type==='WS_START_AUTORUN');
  assert.ok(saveIndex>=0 && startIndex>saveIndex,`order ${saveIndex}/${startIndex}`);
  assert.equal(h.calls[saveIndex].message.active_service,'search');
  assert.equal(h.calls[startIndex].message.conversation_key,CKEY);
  assert.equal(h.calls[startIndex].message.tab_id,1);
  for(const current of ['WS_PAUSE_AUTORUN','WS_RESUME_AUTORUN','WS_FINISH_AUTORUN','WS_EXPORT_BACKUP','WS_IMPORT_BACKUP','WS_SAVE_AUTO_START_PROMPT','WS_RESET_AUTO_START_PROMPT']) assert.match(popupSource,new RegExp(current));
});
