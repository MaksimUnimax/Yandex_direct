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
    product_version:'0.1.1', auto_send:true, debug_mode:false, settings_schema_version:3,
    binding:{binding_id:'b1',conversation_key:CKEY}, manual_mode:false, manual_operation:null,
    service_context:{active_service:'search'}, auto_run:null,
    auto_start_prompt:{text:'SEARCH START',is_default:true,service:'search'},
    report_prefix:{enabled:false,text:'',interval:1,delivered_count:0,last_applied_at_count:0},
    credential_status:{
      wordstat:{has_api_key:true,has_folder_id:true,folder_id:'word-folder',checked_at:'2026-08-26T00:00:00.000Z',check_state:'PRESENT'},
      search:{has_api_key:true,has_folder_id:true,folder_id:'search-folder',checked_at:null,check_state:'NOT_CHECKED'},
      webmaster:{has_oauth_token:true,has_user_id:true,user_id:'42',verified_at:'2026-08-26T00:00:00.000Z',check_state:'PRESENT'}
    },
    wordstat_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['getTop','getDynamics','getRegionsDistribution','getRegionsTree'],max_requests_per_run:100,max_cost_rub_per_run:10,method_cost_rub:{getTop:.02,getDynamics:.02,getRegionsDistribution:.05,getRegionsTree:0},tariff_checked_at:'2026-08-12',tariff_source:'official'},
    search_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['search'],max_requests_per_run:7,max_cost_rub_per_run:3,method_cost_rub:{search:.488},tariff_checked_at:'2026-08-19',tariff_source:'official'},
    webmaster_policy:{autorun_enabled:false,manual_enabled:true,allowed_methods:['listHosts','getSummary','getDiagnostics','getPopularQueries'],max_requests_per_run:50,max_cost_rub_per_run:0,method_cost_rub:{listHosts:0,getSummary:0,getDiagnostics:0,getPopularQueries:0}},
    ...overrides
  };
}

class FakeElement {
  constructor(id='') { this.id=id; this.value=''; this.checked=false; this.disabled=false; this.textContent=''; this.placeholder=''; this.dataset={}; this.files=[]; this.listeners=new Map(); this.href=''; this.download=''; this.open=false; }
  addEventListener(type, fn) { const a=this.listeners.get(type)||[]; a.push(fn); this.listeners.set(type,a); }
  async dispatch(type) { for (const fn of this.listeners.get(type)||[]) await fn({ target:this, preventDefault(){}, stopPropagation(){} }); await new Promise(r=>setTimeout(r,0)); }
  click() { return this.dispatch('click'); }
}

function popupHarness(state=baseState(), { applyManualOk=true, confirmResult=true }={}) {
  const ids=[...popupHtml.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);
  const elements=Object.fromEntries(ids.map(id=>[id,new FakeElement(id)]));
  const calls=[];
  const confirmCalls=[];
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
        else if(message.type==='WS_GET_DIAGNOSTICS') response={ok:true,diagnostics:[]};
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
        } else if(message.type==='YMB_SAVE_WEBMASTER_POLICY') {
          currentState.webmaster_policy=structuredClone(message.policy);
          response={ok:true,policy:structuredClone(currentState.webmaster_policy)};
        } else if(message.type==='YMB_SAVE_SERVICE_CREDENTIAL') {
          const service=message.service;
          const prior=currentState.credential_status?.[service]||{};
          if(service==='webmaster') {
            currentState.credential_status={...currentState.credential_status,webmaster:{...prior,has_oauth_token:prior.has_oauth_token||Boolean(message.credential?.oauth_token),user_id:message.credential?.oauth_token?'':prior.user_id,has_user_id:message.credential?.oauth_token?false:prior.has_user_id,check_state:'NOT_CHECKED',verified_at:null}};
          } else {
            currentState.credential_status={...currentState.credential_status,[service]:{...prior,has_api_key:prior.has_api_key||Boolean(message.credential?.api_key),has_folder_id:Boolean(message.credential?.folder_id),folder_id:message.credential?.folder_id??prior.folder_id,check_state:'NOT_CHECKED',checked_at:null}};
          }
          response={ok:true,service,credential:structuredClone(currentState.credential_status[service]),changed:true};
        } else if(message.type==='YMB_CHECK_SERVICE_CREDENTIAL') {
          if(message.service==='webmaster') {
            currentState.credential_status={...currentState.credential_status,webmaster:{...currentState.credential_status.webmaster,has_user_id:true,user_id:'777',check_state:'PRESENT',verified_at:'2026-08-26T01:00:00.000Z'}};
            response={ok:true,service:'webmaster',state:'PRESENT',user_id:'777',request_executed:true,automatic_retry:false};
          } else {
            currentState.credential_status={...currentState.credential_status,[message.service]:{...currentState.credential_status[message.service],check_state:'PRESENT',checked_at:'2026-08-26T01:00:00.000Z'}};
            response={ok:true,service:message.service,state:'PRESENT',request_executed:true,automatic_retry:false};
          }
        } else if(message.type==='WS_BIND_CONVERSATION') response={ok:true,binding:currentState.binding,conversation_key:CKEY};
        else if(message.type==='WS_START_AUTORUN') { currentState.auto_run={run_id:'r1',active_service:currentState.service_context.active_service,status:'starting'}; response={ok:true,run:structuredClone(currentState.auto_run)}; }
        else if(message.type==='WS_PAUSE_AUTORUN') { currentState.auto_run={...(currentState.auto_run||{}),status:'paused'}; response={ok:true,run:structuredClone(currentState.auto_run)}; }
        else if(message.type==='WS_RESUME_AUTORUN') { currentState.auto_run={...(currentState.auto_run||{}),status:'waiting_command'}; response={ok:true,run:structuredClone(currentState.auto_run)}; }
        else if(message.type==='WS_FINISH_AUTORUN') { currentState.auto_run={...(currentState.auto_run||{}),status:'stopped'}; response={ok:true,run:structuredClone(currentState.auto_run)}; }
        else if(message.type==='WS_SAVE_AUTO_START_PROMPT') response={ok:true,auto_start_prompt:{text:message.text,is_default:false,service:message.active_service}};
        else if(message.type==='WS_RESET_AUTO_START_PROMPT') response={ok:true,auto_start_prompt:{text:'DEFAULT',is_default:true,service:message.active_service}};
        else if(message.type==='WS_EXPORT_BACKUP') response={ok:true,backup:{schema:'YMB_SETTINGS_BACKUP_V3',backup_version:3,settings:{}}};
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
  const confirm=(text)=>{ confirmCalls.push(String(text)); return confirmResult; };
  const ctx=vm.createContext({console,document,chrome,URL:TestURL,Blob,Date,setTimeout,clearTimeout,queueMicrotask,structuredClone,confirm,__YMB_POPUP_TEST__:true});
  ctx.globalThis=ctx;
  vm.runInContext(popupSource,ctx,{filename:'popup.js'});
  return {ctx,elements,calls,confirmCalls,getState:()=>currentState,settle:()=>new Promise(r=>setTimeout(r,10))};
}

test('popup exposes three service credentials without rendering saved secrets', async()=>{
  const h=popupHarness(); await h.settle();
  assert.match(popupHtml,/option value="wordstat"/);
  assert.match(popupHtml,/option value="search"/);
  assert.match(popupHtml,/option value="webmaster"/);
  assert.match(popupHtml,/id="searchManualEnabled"/);
  assert.match(popupHtml,/id="webmasterOauthToken" type="password"/);
  assert.equal(h.elements.activeService.value,'search');
  assert.equal(h.elements.searchManualEnabled.checked,true);
  assert.equal(h.elements.wordstatApiKey.value,'');
  assert.equal(h.elements.searchApiKey.value,'');
  assert.equal(h.elements.webmasterOauthToken.value,'');
  assert.match(h.elements.wordstatApiKey.placeholder,/сохранён/i);
  assert.match(h.elements.searchApiKey.placeholder,/сохранён/i);
  assert.match(h.elements.webmasterOauthToken.placeholder,/сохранён/i);
  assert.equal(h.elements.wordstatFolderId.value,'word-folder');
  assert.equal(h.elements.searchFolderId.value,'search-folder');
  assert.equal(h.elements.webmasterUserId.textContent,'42');
  assert.equal(h.elements.costSearch.value,'0.488');
  assert.equal(h.elements.webmasterMaxRequestsRun.value,'50');
  assert.ok(h.calls.some(c=>c.message?.type==='WS_GET_STATE'));
  assert.doesNotMatch(popupSource,/WS_GET_POPUP_STATE|WS_SAVE_CREDENTIALS|YMB_SET_ACTIVE_SERVICE|WS_AUTO_START|YMB_EXPORT_SETTINGS/);
});

test('Search Manual policy OFF disables enabling conversation Manual mode and explains policy block', async()=>{
  const h=popupHarness(baseState({manual_mode:false,search_policy:{...baseState().search_policy,manual_enabled:false}}));
  await h.settle();
  assert.equal(h.elements.searchManualEnabled.checked,false);
  assert.equal(h.elements.manualMode.checked,false);
  assert.equal(h.elements.manualMode.disabled,true);
  assert.match(h.elements.manualModeMeta.textContent,/запрещён политикой/i);
});

test('Search Manual policy OFF still leaves active Manual mode switch available so operator can turn it off', async()=>{
  const h=popupHarness(baseState({manual_mode:true,search_policy:{...baseState().search_policy,manual_enabled:false}}));
  await h.settle();
  assert.equal(h.elements.searchManualEnabled.checked,false);
  assert.equal(h.elements.manualMode.checked,true);
  assert.equal(h.elements.manualMode.disabled,false);
});

test('active Manual mode locks active-service selector until Manual is turned off', async()=>{
  const h=popupHarness(baseState({manual_mode:true,service_context:{active_service:'search'}}));
  await h.settle();
  assert.equal(h.elements.activeService.value,'search');
  assert.equal(h.elements.activeService.disabled,true);
  assert.equal(h.elements.manualMode.checked,true);
  assert.equal(h.elements.manualMode.disabled,false);
});

test('unsaved active-service selection cannot drive Manual mode or page service', async()=>{
  const h=popupHarness(baseState({service_context:{active_service:'wordstat'}}));
  await h.settle(); h.calls.length=0;
  h.elements.activeService.value='search';
  h.elements.manualMode.checked=true;
  await h.elements.manualMode.dispatch('change'); await h.settle();
  assert.equal(h.calls.some(c=>c.message?.type==='WS_SET_MANUAL_MODE'),false);
  assert.equal(h.calls.some(c=>c.message?.type==='WS_APPLY_MANUAL_MODE'),false);
  assert.equal(h.elements.manualMode.checked,false);
  assert.match(h.elements.status.textContent,/Сначала сохраните выбранный активный сервис/i);
});

test('Manual ON applies page mode before committing worker state and sends active Search service', async()=>{
  const h=popupHarness(); await h.settle(); h.calls.length=0;
  h.elements.manualMode.checked=true;
  await h.elements.manualMode.dispatch('change'); await h.settle();
  const workerIndex=h.calls.findIndex(c=>c.message?.type==='WS_SET_MANUAL_MODE');
  const pageIndex=h.calls.findIndex(c=>c.message?.type==='WS_APPLY_MANUAL_MODE');
  assert.ok(pageIndex>=0 && workerIndex>pageIndex,`order ${pageIndex}/${workerIndex}`);
  assert.equal(h.calls[pageIndex].message.enabled,true);
  assert.equal(h.calls[pageIndex].message.active_service,'search');
  assert.equal(h.calls[workerIndex].message.enabled,true);
});

test('Webmaster Manual uses Webmaster service and preserves the proven transaction order', async()=>{
  const h=popupHarness(baseState({service_context:{active_service:'webmaster'},auto_start_prompt:{text:'',is_default:true,service:'webmaster'}}));
  await h.settle(); h.calls.length=0;
  assert.equal(h.elements.activeService.value,'webmaster');
  assert.equal(h.elements.startAuto.disabled,true);
  h.elements.manualMode.checked=true;
  await h.elements.manualMode.dispatch('change'); await h.settle();
  const workerIndex=h.calls.findIndex(c=>c.message?.type==='WS_SET_MANUAL_MODE');
  const pageIndex=h.calls.findIndex(c=>c.message?.type==='WS_APPLY_MANUAL_MODE');
  assert.ok(pageIndex>=0 && workerIndex>pageIndex,`order ${pageIndex}/${workerIndex}`);
  assert.equal(h.calls[pageIndex].message.active_service,'webmaster');
  assert.equal(h.calls.some(c=>c.message?.type==='WS_START_AUTORUN'),false);
});

test('failed page Manual ON acknowledgement never authorizes worker Manual mode', async()=>{
  const h=popupHarness(baseState(),{applyManualOk:false}); await h.settle(); h.calls.length=0;
  h.elements.manualMode.checked=true;
  await h.elements.manualMode.dispatch('change'); await h.settle();
  const manualCalls=h.calls.filter(c=>c.message?.type==='WS_SET_MANUAL_MODE');
  const applyCalls=h.calls.filter(c=>c.message?.type==='WS_APPLY_MANUAL_MODE');
  assert.equal(applyCalls.length,1);
  assert.equal(applyCalls[0].message.enabled,true);
  assert.equal(manualCalls.length,0);
  assert.equal(h.elements.manualMode.checked,false);
});

test('Search autorun toggle persists only the toggle and does not commit unsaved service secrets/text fields', async()=>{
  const h=popupHarness(); await h.settle(); h.calls.length=0;
  h.elements.searchApiKey.value='UNSAVED-SECRET'; h.elements.reportPrefixText.value='UNSAVED-TEXT';
  h.elements.searchAutorunEnabled.checked=false;
  await h.elements.searchAutorunEnabled.dispatch('change'); await h.settle();
  const runtime=h.calls.filter(c=>c.channel==='runtime').map(c=>c.message);
  assert.equal(runtime[0].type,'WS_PATCH_TOGGLES');
  assert.equal(runtime[0].search_autorun_enabled,false);
  assert.equal(runtime.some(m=>m.type==='WS_SAVE_SETTINGS'),false);
  assert.equal(runtime.some(m=>m.type==='YMB_SAVE_SERVICE_CREDENTIAL'),false);
  assert.equal(JSON.stringify(runtime).includes('UNSAVED-SECRET'),false);
  assert.equal(JSON.stringify(runtime).includes('UNSAVED-TEXT'),false);
});

test('explicit common Save persists Search policy and Webmaster policy but no credentials', async()=>{
  const h=popupHarness(); await h.settle(); h.calls.length=0;
  h.elements.activeService.value='search';
  h.elements.searchApiKey.value='UNSAVED-SECRET';
  h.elements.searchManualEnabled.checked=false;
  h.elements.searchMaxRequestsRun.value='9'; h.elements.searchMaxCostRun.value='4.5'; h.elements.costSearch.value='0.488';
  h.elements.webmasterManualEnabled.checked=false; h.elements.webmasterMaxRequestsRun.value='33';
  h.elements.reportPrefixEnabled.checked=true; h.elements.reportPrefixText.value='PREFIX';
  await h.ctx.__YMB_POPUP_TEST_API__.saveAll(); await h.settle();
  const msg=h.calls.find(c=>c.message?.type==='WS_SAVE_SETTINGS')?.message;
  const wm=h.calls.find(c=>c.message?.type==='YMB_SAVE_WEBMASTER_POLICY')?.message;
  assert.ok(msg); assert.ok(wm);
  assert.equal(msg.active_service,'search');
  assert.equal(msg.search_policy.manual_enabled,false);
  assert.equal(msg.search_policy.max_requests_per_run,9);
  assert.equal(msg.search_policy.max_cost_rub_per_run,4.5);
  assert.equal(msg.search_policy.method_cost_rub.search,0.488);
  assert.equal(msg.wordstat_policy.allowed_methods.includes('getTop'),true);
  assert.deepEqual(msg.report_prefix,{enabled:true,text:'PREFIX',interval:1});
  assert.equal(JSON.stringify(msg).includes('UNSAVED-SECRET'),false);
  assert.equal(wm.policy.autorun_enabled,false);
  assert.equal(wm.policy.manual_enabled,false);
  assert.equal(wm.policy.max_requests_per_run,33);
  assert.equal(h.getState().search_policy.manual_enabled,false);
});

test('service credential Save is isolated and blank masked secret is omitted', async()=>{
  const h=popupHarness(); await h.settle(); h.calls.length=0;
  h.elements.searchApiKey.value='';
  h.elements.searchFolderId.value='new-search-folder';
  await h.ctx.__YMB_POPUP_TEST_API__.saveCredential('search'); await h.settle();
  const msg=h.calls.find(c=>c.message?.type==='YMB_SAVE_SERVICE_CREDENTIAL')?.message;
  assert.ok(msg);
  assert.equal(msg.service,'search');
  assert.deepEqual(msg.credential,{folder_id:'new-search-folder'});
  assert.equal(Object.hasOwn(msg.credential,'api_key'),false);
  assert.equal(JSON.stringify(msg).includes('word-folder'),false);
  assert.equal(JSON.stringify(msg).includes('OAuth'),false);
});

test('Webmaster Save sends only new OAuth and never another service credential', async()=>{
  const h=popupHarness(); await h.settle(); h.calls.length=0;
  h.elements.webmasterOauthToken.value='NEW-OAUTH-SECRET';
  await h.ctx.__YMB_POPUP_TEST_API__.saveCredential('webmaster'); await h.settle();
  const msg=h.calls.find(c=>c.message?.type==='YMB_SAVE_SERVICE_CREDENTIAL')?.message;
  assert.deepEqual(msg,{type:'YMB_SAVE_SERVICE_CREDENTIAL',service:'webmaster',credential:{oauth_token:'NEW-OAUTH-SECRET'}});
  assert.equal(h.calls.filter(c=>c.message?.type==='YMB_SAVE_SERVICE_CREDENTIAL').length,1);
});

test('Search Check cancellation performs zero credential-check requests', async()=>{
  const h=popupHarness(baseState(),{confirmResult:false}); await h.settle(); h.calls.length=0;
  const result=await h.ctx.__YMB_POPUP_TEST_API__.checkCredential('search'); await h.settle();
  assert.equal(result.cancelled,true);
  assert.equal(result.request_executed,false);
  assert.equal(h.confirmCalls.length,1);
  assert.equal(h.calls.some(c=>c.message?.type==='YMB_CHECK_SERVICE_CREDENTIAL'),false);
});

test('Search Check after explicit confirmation sends exactly one confirmed check message', async()=>{
  const h=popupHarness(); await h.settle(); h.calls.length=0;
  await h.ctx.__YMB_POPUP_TEST_API__.checkCredential('search'); await h.settle();
  const checks=h.calls.filter(c=>c.message?.type==='YMB_CHECK_SERVICE_CREDENTIAL');
  assert.equal(checks.length,1);
  assert.equal(checks[0].message.service,'search');
  assert.equal(checks[0].message.confirm_billable,true);
});

test('Webmaster Check updates only derived user_id metadata in popup', async()=>{
  const h=popupHarness(); await h.settle(); h.calls.length=0;
  await h.ctx.__YMB_POPUP_TEST_API__.checkCredential('webmaster'); await h.settle();
  const checks=h.calls.filter(c=>c.message?.type==='YMB_CHECK_SERVICE_CREDENTIAL');
  assert.equal(checks.length,1);
  assert.equal(checks[0].message.service,'webmaster');
  assert.equal(Object.hasOwn(checks[0].message,'oauth_token'),false);
  assert.equal(h.elements.webmasterUserId.textContent,'777');
  assert.equal(h.elements.webmasterOauthToken.value,'');
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
