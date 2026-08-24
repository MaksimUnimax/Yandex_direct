import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../src');
const popupSource=fs.readFileSync(path.join(root,'popup.js'),'utf8');
const transferGuardSource=fs.readFileSync(path.join(root,'popup_transfer_guard.js'),'utf8');
const contextBootstrapSource=fs.readFileSync(path.join(root,'popup_context_bootstrap.js'),'utf8');
const popupHtml=fs.readFileSync(path.join(root,'popup.html'),'utf8');
const CID='99999999-8888-4777-8666-555555555555';
const CKEY=`https://chatgpt.com|${CID}`;

class FakeElement {
  constructor(id=''){ this.id=id; this.value=''; this.checked=false; this.disabled=false; this.textContent=''; this.placeholder=''; this.dataset={}; this.files=[]; this.listeners=new Map(); this.href=''; this.download=''; }
  addEventListener(type,fn,options=false){
    const list=this.listeners.get(type)||[];
    const capture=options===true||options?.capture===true;
    list.push({fn,capture});
    this.listeners.set(type,list);
  }
  async dispatch(type){
    const event={
      target:this,defaultPrevented:false,immediateStopped:false,propagationStopped:false,
      preventDefault(){this.defaultPrevented=true;},
      stopPropagation(){this.propagationStopped=true;},
      stopImmediatePropagation(){this.immediateStopped=true;this.propagationStopped=true;}
    };
    const list=this.listeners.get(type)||[];
    for(const phase of [true,false]){
      for(const entry of list.filter(item=>item.capture===phase)){
        if(event.immediateStopped) break;
        await entry.fn(event);
      }
      if(event.propagationStopped) break;
    }
    await new Promise(r=>setTimeout(r,0));
    return event;
  }
  click(){ return this.dispatch('click'); }
}

function state(){ return {
  product_version:'0.1.1',has_api_key:true,folder_id:'folder',auto_send:true,debug_mode:false,
  binding:{binding_id:'b1',conversation_key:CKEY},manual_mode:false,manual_operation:null,
  service_context:{active_service:'search'},
  auto_run:{run_id:'r1',active_service:'search',status:'waiting_command',tab_id:1,requests_attempted:0,requests_executed:0,requests_skipped:0,estimated_cost_rub:0,sequence:0},
  auto_start_prompt:{text:'SEARCH START',is_default:true,service:'search'},
  report_prefix:{enabled:false,text:'',interval:1,delivered_count:0,last_applied_at_count:0},
  wordstat_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['getTop','getDynamics','getRegionsDistribution','getRegionsTree'],max_requests_per_run:100,max_cost_rub_per_run:10,method_cost_rub:{getTop:.02,getDynamics:.02,getRegionsDistribution:.05,getRegionsTree:0}},
  search_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['search'],max_requests_per_run:10,max_cost_rub_per_run:10,method_cost_rub:{search:.488}}
}; }

function harness(failType=null,{confirmAnswers=[true]}={}){
  const ids=[...popupHtml.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);
  const elements=Object.fromEntries(ids.map(id=>[id,new FakeElement(id)]));
  let current=structuredClone(state());
  const runtimeMessages=[];
  const confirmations=[];
  const answers=[...confirmAnswers];
  const document={getElementById(id){return elements[id]||null;},createElement(tag){return new FakeElement(tag);}};
  const chrome={
    runtime:{lastError:null,sendMessage(message,cb){
      runtimeMessages.push(structuredClone(message));
      let response={ok:true};
      if(message.type==='WS_GET_STATE'||message.type==='WS_GET_GLOBAL_STATE') response={ok:true,state:structuredClone(current)};
      else if(message.type===failType) response={ok:false,code:'CONTROLLED_FAILURE',error:`controlled ${failType} failure`};
      else if(message.type==='WS_EXPORT_BACKUP') response={ok:true,backup:{schema:'YMB_SETTINGS_BACKUP_V2',settings:{}}};
      else if(message.type==='WS_IMPORT_BACKUP') response={ok:true,result:{imported:true},state:structuredClone(current)};
      queueMicrotask(()=>cb(response));
    }},
    tabs:{query(_q,cb){queueMicrotask(()=>cb([{id:1,url:`https://chatgpt.com/c/${CID}`}]))},sendMessage(_id,message,cb){
      if(message.type==='WS_GET_IDENTITY') queueMicrotask(()=>cb({ok:true,conversation_key:CKEY,identity:{conversation_key:CKEY,origin:'https://chatgpt.com',conversation_id:CID}}));
      else queueMicrotask(()=>cb({ok:true,applied:true}));
    }}
  };
  class TestURL extends URL { static createObjectURL(){return 'blob:test';} static revokeObjectURL(){} }
  const ctx=vm.createContext({
    console,document,chrome,URL:TestURL,Blob,Date,setTimeout,clearTimeout,queueMicrotask,structuredClone,
    confirm(message){ confirmations.push(String(message)); return answers.length ? answers.shift() : true; },
    __YMB_POPUP_TEST__:true,__YMB_POPUP_TRANSFER_GUARD_TEST__:true
  });
  ctx.globalThis=ctx;
  vm.runInContext(transferGuardSource,ctx,{filename:'popup_transfer_guard.js'});
  vm.runInContext(popupSource,ctx,{filename:'popup.js'});
  return {elements,runtimeMessages,confirmations,guardApi:ctx.__YMB_POPUP_TRANSFER_GUARD_TEST_API__,settle:()=>new Promise(r=>setTimeout(r,10))};
}

test('popup loads transfer guard then context bootstrap, and bootstrap starts its main runtime afterwards',()=>{
  const guardIndex=popupHtml.indexOf('<script src="popup_transfer_guard.js"></script>');
  const contextIndex=popupHtml.indexOf('<script src="popup_context_bootstrap.js"></script>');
  assert.ok(guardIndex>=0);
  assert.ok(contextIndex>guardIndex);
  assert.equal(popupHtml.includes('<script src="popup.js"></script>'),false);
  assert.match(contextBootstrapSource,/chrome\.runtime\.getURL\("popup\.js"\)/);
  assert.match(contextBootstrapSource,/\.finally\(\(\) => loadPopupRuntime\(\)\)/);
});

test('cancelled secret export is stopped before the popup runtime can export credentials',async()=>{
  const h=harness(null,{confirmAnswers:[false]});
  await h.settle();
  const before=h.runtimeMessages.filter(m=>m.type==='WS_EXPORT_BACKUP').length;
  const event=await h.elements.exportSettings.dispatch('click');
  await h.settle();
  const after=h.runtimeMessages.filter(m=>m.type==='WS_EXPORT_BACKUP').length;
  assert.equal(event.defaultPrevented,true);
  assert.equal(after,before);
  assert.match(h.confirmations[0],/API key/);
  assert.equal(h.elements.status.textContent,'Экспорт отменён.');
});

test('oversized settings backup is rejected before JSON parsing or worker import',async()=>{
  const h=harness();
  await h.settle();
  h.elements.importFile.value='selected.json';
  h.elements.importFile.files=[{size:h.guardApi.MAX_BACKUP_BYTES+1,async text(){throw new Error('file must not be read');}}];
  const before=h.runtimeMessages.filter(m=>m.type==='WS_IMPORT_BACKUP').length;
  const event=await h.elements.importFile.dispatch('change');
  await h.settle();
  const after=h.runtimeMessages.filter(m=>m.type==='WS_IMPORT_BACKUP').length;
  assert.equal(event.defaultPrevented,true);
  assert.equal(after,before);
  assert.equal(h.elements.importFile.value,'');
  assert.equal(h.elements.status.dataset.level,'error');
  assert.match(h.elements.status.textContent,/Максимум 5 МБ/);
});

test('cancelled settings import is stopped before the backup reaches the worker',async()=>{
  const h=harness(null,{confirmAnswers:[false]});
  await h.settle();
  h.elements.importFile.value='settings.json';
  h.elements.importFile.files=[{size:100,async text(){return '{}';}}];
  const before=h.runtimeMessages.filter(m=>m.type==='WS_IMPORT_BACKUP').length;
  const event=await h.elements.importFile.dispatch('change');
  await h.settle();
  const after=h.runtimeMessages.filter(m=>m.type==='WS_IMPORT_BACKUP').length;
  assert.equal(event.defaultPrevented,true);
  assert.equal(after,before);
  assert.equal(h.elements.importFile.value,'');
  assert.match(h.confirmations[0],/активный запуск не заменяется/);
  assert.equal(h.elements.status.textContent,'Импорт отменён.');
});

test('failed Pause is shown in popup and Pause button is restored',async()=>{
  const h=harness('WS_PAUSE_AUTORUN');
  await h.settle();
  assert.equal(h.elements.pauseAuto.disabled,false);
  await h.elements.pauseAuto.dispatch('click');
  await h.settle();
  assert.equal(h.elements.pauseAuto.disabled,false);
  assert.equal(h.elements.status.dataset.level,'error');
  assert.match(h.elements.status.textContent,/controlled WS_PAUSE_AUTORUN failure/);
});

test('failed Export is shown in popup and Export button is restored',async()=>{
  const h=harness('WS_EXPORT_BACKUP');
  await h.settle();
  assert.equal(h.elements.exportSettings.disabled,false);
  await h.elements.exportSettings.dispatch('click');
  await h.settle();
  assert.equal(h.elements.exportSettings.disabled,false);
  assert.equal(h.elements.status.dataset.level,'error');
  assert.match(h.elements.status.textContent,/controlled WS_EXPORT_BACKUP failure/);
});
