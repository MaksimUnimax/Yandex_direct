// Complete saved worker scripts; Chrome/IndexedDB/network are controlled fixtures.
// This is not Chromium, DOM, MV3 termination, durability or resource proof.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
const fixture = process.env.YMB_IDB_FIXTURE;
if (!fixture) throw new Error('YMB_IDB_FIXTURE is required');
const fake = await import(pathToFileURL(path.resolve(fixture)));
export const KEY='https://chatgpt.com|11111111-1111-4111-8111-111111111111';
export const CID='11111111-1111-4111-8111-111111111111';
export async function loadWorker(full, {network, seed={}}={}) {
  const root=path.resolve(full), data=structuredClone(seed), calls={fetch:[],imports:[],storageGets:[],storageWrites:0}, listeners=[];
  const event=()=>({addListener(){},removeListener(){}});
  const local={async get(keys){calls.storageGets.push(keys);if(keys==null)return structuredClone(data);if(typeof keys==='string')return{[keys]:structuredClone(data[keys])};if(Array.isArray(keys))return Object.fromEntries(keys.map(k=>[k,structuredClone(data[k])]));return Object.fromEntries(Object.entries(keys).map(([k,v])=>[k,structuredClone(data[k]??v)]));},async set(values){Object.assign(data,structuredClone(values));calls.storageWrites++;},async remove(keys){for(const k of Array.isArray(keys)?keys:[keys])delete data[k];}};
  const identity={origin:'https://chatgpt.com',conversation_key:KEY,conversation_id:CID};
  const chrome={runtime:{id:'qa-extension',lastError:null,getManifest:()=>JSON.parse(fs.readFileSync(path.join(root,'manifest.json'),'utf8')),getURL:p=>'chrome-extension://qa-extension/'+p,onMessage:{addListener:l=>listeners.push(l),removeListener:l=>{const i=listeners.indexOf(l);if(i>=0)listeners.splice(i,1);}},onInstalled:event(),onStartup:event()},storage:{local,onChanged:event()},tabs:{async get(id){return{id,url:'https://chatgpt.com/c/'+CID};},async query(){return[{id:7,url:'https://chatgpt.com/c/'+CID}];},sendMessage(tab,m,cb){const r=m.type==='WS_GET_IDENTITY'?{identity:tab===7?identity:{...identity,conversation_id:'other',conversation_key:'https://chatgpt.com|22222222-2222-4222-8222-222222222222'}}:{ok:true};if(cb){cb(r);return;}return Promise.resolve(r);},onRemoved:event(),onUpdated:event()},scripting:{async executeScript(){return[];}}};
  const context=vm.createContext({...fake,console,crypto:crypto.webcrypto,structuredClone,TextEncoder,TextDecoder,Uint8Array,ArrayBuffer,URL,URLSearchParams,AbortController,AbortSignal,Response,Request,Headers,Blob,atob,btoa,setTimeout,clearTimeout,setInterval,clearInterval,performance,chrome,
    fetch:async(url,init)=>{calls.fetch.push({url:String(url),method:init?.method||'GET'});if(!network)throw new Error('UNEXPECTED_PROVIDER_ATTEMPT');return network(url,init);}});
  context.globalThis=context;context.self=context;
  context.importScripts=(...files)=>{for(const name of files){const file=path.resolve(root,name);if(!file.startsWith(root+path.sep))throw new Error('IMPORT_OUTSIDE_CANDIDATE');calls.imports.push(name);vm.runInContext(fs.readFileSync(file,'utf8'),context,{filename:name});}};
  vm.runInContext(fs.readFileSync(path.join(root,'phase3_service_worker_bootstrap.js'),'utf8'),context,{filename:'phase3_service_worker_bootstrap.js'});
  // Settle startup microtasks without generating a provider/UI action.
  for(let i=0;i<40;i++)await new Promise(r=>setImmediate(r));
  function seedBoundChat(service='search'){
    data.wsmb_conversation_bindings={[KEY]:{conversation_key:KEY,conversation_id:CID}};
    data.wsmb_manual_modes={[KEY]:true};data.ymb_service_contexts={[KEY]:{active_service:service}};
    data.wsmb_manual_operations={};data.wsmb_auto_runs={};data.wsmb_outbox={};
    data.ymb_service_credentials={wordstat:{api_key:'TEST_WORDSTAT_NOT_REAL',folder_id:'folder',check_state:'PRESENT'},search:{api_key:'TEST_SEARCH_NOT_REAL',folder_id:'folder',check_state:'PRESENT'},webmaster:{oauth_token:'TEST_WM_NOT_REAL',user_id:'1',check_state:'PRESENT'},metrika:{oauth_token:'TEST_METRIKA_NOT_REAL',check_state:'PRESENT'},direct:{oauth_token:'TEST_DIRECT_NOT_REAL',client_login:'qa',check_state:'PRESENT'}};
    data.ymb_settings_schema_version=5;
  }
  async function dispatch(message,sender={tab:{id:7}}){
    let outputs=[];
    await Promise.all(listeners.map(listener=>new Promise(resolve=>{let answered=false;const cb=v=>{outputs.push(v);answered=true;resolve();};const ret=listener(message,sender,cb);if(ret!==true&&!answered)resolve();})));
    if(outputs.length!==1)throw new Error('RESPONSE_COUNT_'+outputs.length);
    return outputs[0];
  }
  return{context,data,calls,listeners,seedBoundChat,dispatch,run:source=>vm.runInContext(source,context)};
}
