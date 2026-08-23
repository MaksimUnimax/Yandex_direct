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

class FakeElement {
  constructor(id=''){ this.id=id; this.value=''; this.checked=false; this.disabled=false; this.textContent=''; this.placeholder=''; this.dataset={}; this.files=[]; this.listeners=new Map(); this.href=''; this.download=''; }
  addEventListener(type,fn){ const list=this.listeners.get(type)||[]; list.push(fn); this.listeners.set(type,list); }
  async dispatch(type){ for(const fn of this.listeners.get(type)||[]) await fn({target:this,preventDefault(){},stopPropagation(){}}); await new Promise(r=>setTimeout(r,0)); }
}

function baseState(){ return {
  product_version:'0.1.1',has_api_key:true,folder_id:'folder',auto_send:true,debug_mode:false,
  binding:{binding_id:'b1',conversation_key:CKEY},manual_mode:true,manual_operation:null,
  service_context:{active_service:'search'},auto_run:null,
  auto_start_prompt:{text:'SEARCH START',is_default:true,service:'search'},
  report_prefix:{enabled:false,text:'',interval:1,delivered_count:0,last_applied_at_count:0},
  send_button_profile:null,copy_button_profiles:{},
  wordstat_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['getTop','getDynamics','getRegionsDistribution','getRegionsTree'],max_requests_per_run:100,max_cost_rub_per_run:10,method_cost_rub:{getTop:.02,getDynamics:.02,getRegionsDistribution:.05,getRegionsTree:0}},
  search_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['search'],max_requests_per_run:10,max_cost_rub_per_run:10,method_cost_rub:{search:.488}}
}; }

function harness(){
  const ids=[...popupHtml.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);
  const elements=Object.fromEntries(ids.map(id=>[id,new FakeElement(id)]));
  const calls=[];
  let state=structuredClone(baseState());
  const document={getElementById(id){return elements[id]||null;},createElement(tag){return new FakeElement(tag);}};
  const chrome={
    runtime:{lastError:null,sendMessage(message,cb){
      calls.push({channel:'runtime',message:structuredClone(message)});
      let response={ok:true};
      if(message.type==='WS_GET_STATE'||message.type==='WS_GET_GLOBAL_STATE') response={ok:true,state:structuredClone(state)};
      else if(message.type==='WS_GET_DIAGNOSTICS') response={ok:true,diagnostics:[]};
      else if(message.type==='WS_SET_MANUAL_MODE') { state={...state,manual_mode:message.enabled===true}; response={ok:true,enabled:message.enabled===true,state:structuredClone(state)}; }
      queueMicrotask(()=>cb(response));
    }},
    tabs:{
      query(_q,cb){queueMicrotask(()=>cb([{id:1,url:`https://chatgpt.com/c/${CID}`}]))},
      sendMessage(_id,message,cb){
        calls.push({channel:'tab',message:structuredClone(message)});
        if(message.type==='WS_GET_IDENTITY') queueMicrotask(()=>cb({ok:true,conversation_key:CKEY,identity:{conversation_key:CKEY,origin:'https://chatgpt.com',conversation_id:CID}}));
        else if(message.type==='WS_APPLY_MANUAL_MODE') queueMicrotask(()=>cb({ok:false,applied:false,code:'CLEANUP_FAILED',error:'page cleanup failed'}));
        else queueMicrotask(()=>cb({ok:true}));
      }
    }
  };
  class TestURL extends URL { static createObjectURL(){return 'blob:test';} static revokeObjectURL(){} }
  const navigator={clipboard:{async writeText(){}}};
  const ctx=vm.createContext({console,document,chrome,navigator,URL:TestURL,Blob,Date,setTimeout,clearTimeout,queueMicrotask,structuredClone,confirm:()=>true,__YMB_POPUP_TEST__:true}); ctx.globalThis=ctx;
  vm.runInContext(popupSource,ctx,{filename:'popup.js'});
  return {elements,calls,getState:()=>state,settle:()=>new Promise(r=>setTimeout(r,15))};
}

test('failed page cleanup after Manual OFF keeps worker OFF and reports reconciliation failure',async()=>{
  const h=harness(); await h.settle(); h.calls.length=0;
  assert.equal(h.elements.manualMode.checked,true);
  h.elements.manualMode.checked=false;
  await h.elements.manualMode.dispatch('change'); await h.settle();
  const writes=h.calls.filter(c=>c.message?.type==='WS_SET_MANUAL_MODE');
  assert.equal(writes.length,1,'Manual OFF must not be rolled back to ON after page cleanup failure');
  assert.equal(writes[0].message.enabled,false);
  assert.equal(h.getState().manual_mode,false);
  assert.equal(h.elements.manualMode.checked,false);
  assert.equal(h.elements.status.dataset.level,'error');
  assert.match(h.elements.status.textContent,/page cleanup failed|CLEANUP_FAILED/);
});
