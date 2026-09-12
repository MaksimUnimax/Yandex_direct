import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';import path from 'node:path';import {fileURLToPath} from 'node:url';import crypto from 'node:crypto';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const baseFile=process.env.YMB_SEARCH_PROTOCOL||(fs.existsSync(root+'/baseline/shared/search_protocol.js')?root+'/baseline/shared/search_protocol.js':path.resolve(root,'../../../src/shared/search_protocol.js'));
assert.equal(crypto.createHash('sha256').update(fs.readFileSync(baseFile)).digest('hex'),'48cb17f0a846f87e2057d65945dce23788e5c3c90810b7542557d762c2f301b7');
const ctx=vm.createContext({URL,TextEncoder,TextDecoder,Uint8Array,AbortController,setTimeout,clearTimeout,console});ctx.globalThis=ctx;
for(const p of [baseFile,root+'/candidate/shared/search_async_protocol.js',root+'/candidate/shared/search_async_transport.js'])vm.runInContext(fs.readFileSync(p,'utf8'),ctx,{filename:p});
const F=ctx.YMBSearchAsyncTransport;const creds={api_key:'SYNTHETIC_KEY_NO_REAL_SECRET_123456',folder_id:'folder-test'};
const opts=extra=>({kind:'submit',query:'тест',parameters:{region:'225'},credential:creds,expectedFolderId:'folder-test',admit:async()=>({allowed:true}),...extra});
const op={id:'operation-123',done:false};
const response=(v=op,status=200)=>new Response(typeof v==='string'?v:JSON.stringify(v),{status,headers:{'content-type':'application/json'}});
const create=(fetchImpl,extra={})=>F.create({fetchImpl,maxResponseBytes:1024*1024,timeoutMs:1000,...extra});
const submit=async(fetchImpl,extra={},config={})=>create(fetchImpl,config).execute(opts(extra));
test('requires explicit bounded trusted memory budget and transport dependency',()=>{
 for(const maxResponseBytes of [undefined,0,-1,NaN,Infinity,'100'])assert.throws(()=>F.create({fetchImpl:async()=>{},maxResponseBytes}));
 assert.throws(()=>create(async()=>{}, {timeoutMs:30000}));assert.throws(()=>F.create({maxResponseBytes:1024}));
});
test('one POST only after durable admission; no implicit GET on pending response',async()=>{
 const events=[];const r=await submit(async(url,init)=>{events.push('fetch');assert.equal(url,ctx.SearchAsyncProtocol.SUBMIT_URL);assert.equal(init.method,'POST');assert.equal(init.headers.Authorization,'Api-Key '+creds.api_key);assert.equal(init.redirect,'error');assert.equal(init.credentials,'omit');assert.equal(init.cache,'no-store');assert.equal(init.referrerPolicy,'no-referrer');assert.equal(JSON.parse(init.body).query.queryText,'тест');return response();},{admit:async()=>{await Promise.resolve();events.push('persisted');return{allowed:true};}});
 assert.deepEqual(events,['persisted','fetch']);assert.equal(r.operation.outcome,'waiting');assert.equal(r.automatic_retry,false);
});
test('GET only same operation with no POST body',async()=>{
 let calls=0;const r=await submit(async(url,init)=>{calls++;assert.equal(url,ctx.SearchAsyncProtocol.OPERATIONS_URL+op.id);assert.equal(init.method,'GET');assert.equal('body'in init,false);return response();},{kind:'collect',operationId:op.id});
 assert.equal(r.ok,true);assert.equal(calls,1);
});
test('missing wrong or newline credentials rejected before admission and fetch',async()=>{
 for(const credential of [null,{...creds,api_key:''},{...creds,api_key:'x\r\ny'},{...creds,folder_id:'other'}]){
  let calls=0,admit=0;const r=await submit(async()=>{calls++;return response();},{credential,admit:async()=>{admit++;return{allowed:true};}});assert.equal(calls,0);assert.equal(admit,0);assert.equal(r.request_executed,false);
 }
});
test('absent denied or failing admission never executes provider',async()=>{
 for(const admit of [null,async()=>({allowed:false}),async()=>{throw new Error(creds.api_key);}]){let calls=0;const r=await submit(async()=>{calls++;return response();},{admit});assert.equal(calls,0);assert.equal(r.request_executed,false);assert.ok(!JSON.stringify(r).includes(creds.api_key));}
});
test('pre-aborted and aborted-during-admission signals grant no network',async()=>{
 const c=new AbortController();c.abort();let calls=0;const r=await submit(async()=>{calls++;},{signal:c.signal});assert.equal(calls,0);assert.equal(r.code,'ASYNC_ABORTED');
 const d=new AbortController();const a=await submit(async()=>{calls++;},{signal:d.signal,admit:async()=>{d.abort();return{allowed:true};}});assert.equal(calls,0);assert.equal(a.code,'ASYNC_ABORTED_AFTER_ADMISSION');
});
test('network error after POST is unknown without retry or secret reflection',async()=>{
 let calls=0;const r=await submit(async()=>{calls++;throw new Error(creds.api_key);});assert.equal(calls,1);assert.equal(r.request_executed,'UNKNOWN');assert.equal(r.outcome,'unknown');assert.equal(r.automatic_retry,false);assert.ok(!JSON.stringify(r).includes(creds.api_key));
});
for(const status of [400,401,403,404,429,500])test(`HTTP ${status} never retries or decodes an error body as Search`,async()=>{
 let calls=0;const r=await submit(async()=>{calls++;return response(creds.api_key,status);});assert.equal(calls,1);assert.equal(r.ok,false);assert.equal(r.http_status,status);assert.equal(r.outcome,status===500?'unknown':'rejected');assert.equal(r.automatic_retry,false);assert.ok(!('raw_text'in r));assert.ok(!JSON.stringify(r).includes(creds.api_key));
});
test('waiting response retains raw text exactly; immediate success is not discarded',async()=>{
 const text=' { "id":"operation-123", "done":true, "response":{"rawData":"dGVzdA=="} }\n';const r=await submit(async()=>response(text));assert.equal(r.operation.outcome,'received');assert.equal(r.raw_text,text);assert.equal(r.byte_length,new TextEncoder().encode(text).length);
});
test('provider operation error is not an empty successful search',async()=>{
 const r=await submit(async()=>response({...op,done:true,error:{code:13,message:'failure'}}));assert.equal(r.ok,true);assert.equal(r.operation.outcome,'provider_error');assert.equal('rawData'in r.operation,false);
});
test('invalid or mismatched Operation never becomes success',async()=>{
 for(const body of ['oops','{}',JSON.stringify({id:'wrong',done:false})]){const r=await submit(async()=>response(body),{kind:'collect',operationId:op.id});assert.equal(r.ok,false);assert.equal(r.outcome,'read_error');}
 const r=await submit(async()=>response('{}'));assert.equal(r.outcome,'unknown');
});
test('arbitrary operation URL and parameter headers rejected without fetch',async()=>{
 let calls=0;const fetch=async()=>{calls++;return response();};const r=await submit(fetch,{kind:'collect',operationId:'https://evil.invalid'});assert.equal(r.request_executed,false);await submit(fetch,{parameters:{headers:{Authorization:'evil'}}});assert.equal(calls,0);
});
test('redirected response fails closed without follow-up request',async()=>{
 let calls=0;const r=await submit(async()=>{calls++;const res=response();Object.defineProperty(res,'redirected',{value:true});return res;});assert.equal(calls,1);assert.equal(r.ok,false);assert.equal(r.code,'ASYNC_RESPONSE_REDIRECTED');
});
test('stalled fetch terminates by bounded timeout',async()=>{
 let captured;const r=await submit(async(_url,init)=>{captured=init.signal;return new Promise(()=>{});},{},{timeoutMs:10});assert.equal(r.code,'ASYNC_TIMEOUT');assert.equal(r.request_executed,'UNKNOWN');assert.equal(captured.aborted,true);
});
test('timeout covers body streaming and cancels reader',async()=>{
 let cancelled=false;const body=new ReadableStream({start(){},cancel(){cancelled=true;}});const r=await submit(async()=>new Response(body),{},{timeoutMs:10});assert.equal(r.code,'ASYNC_TIMEOUT');assert.equal(cancelled,true);
});
test('explicit abort after request is unknown and does not retry',async()=>{
 const ctrl=new AbortController();let calls=0;const r=await submit(async()=>{calls++;queueMicrotask(()=>ctrl.abort());return new Promise(()=>{});},{signal:ctrl.signal});assert.equal(calls,1);assert.equal(r.code,'ASYNC_ABORTED');assert.equal(r.request_executed,'UNKNOWN');
});
test('byte budget checks streaming even without Content-Length and returns no partial success',async()=>{
 let cancelled=false;const body=new ReadableStream({pull(c){c.enqueue(new Uint8Array(100));},cancel(){cancelled=true;}});const r=await submit(async()=>new Response(body),{},{maxResponseBytes:150});assert.equal(r.code,'ASYNC_RESPONSE_TOO_LARGE');assert.equal('raw_text'in r,false);assert.equal(cancelled,true);
});
test('declared oversized body rejected without materializing text',async()=>{
 let reads=0;const r=await submit(async()=>({ok:true,status:200,headers:new Headers({'content-length':'99999'}),body:{getReader(){reads++;throw new Error('not allowed');}}}),{},{maxResponseBytes:1000});assert.equal(reads,0);assert.equal(r.code,'ASYNC_RESPONSE_TOO_LARGE');
});
test('broken UTF8 does not silently mutate raw evidence',async()=>{
 const r=await submit(async()=>new Response(new Uint8Array([0xc3,0x28])));assert.equal(r.code,'ASYNC_INVALID_UTF8');assert.equal(r.ok,false);
});
test('server reflection of actual key is blocked from exported result',async()=>{
 const r=await submit(async()=>response({...op,description:creds.api_key}));assert.equal(r.code,'ASYNC_CREDENTIAL_REFLECTED_IN_RESPONSE');assert.ok(!JSON.stringify(r).includes(creds.api_key));
});
test('chunked UTF8 and detached abort listeners across many chunks and repeats',async()=>{
 const originalAdd=AbortSignal.prototype.addEventListener,originalRemove=AbortSignal.prototype.removeEventListener;
 const active=new Map();let peak=0;
 AbortSignal.prototype.addEventListener=function(type,fn,...rest){if(type==='abort'){if(!active.has(this))active.set(this,new Set());active.get(this).add(fn);peak=Math.max(peak,[...active.values()].reduce((n,s)=>n+s.size,0));}return originalAdd.call(this,type,fn,...rest);};
 AbortSignal.prototype.removeEventListener=function(type,fn,...rest){if(type==='abort')active.get(this)?.delete(fn);return originalRemove.call(this,type,fn,...rest);};
 try{
  for(let run=0;run<3;run++){
   const bytes=new TextEncoder().encode(JSON.stringify({...op,description:'💎'.repeat(1000)}));let offset=0;const body=new ReadableStream({pull(c){if(offset===bytes.length){c.close();return;}c.enqueue(bytes.subarray(offset,++offset));}});const c=new AbortController();const r=await submit(async()=>new Response(body),{signal:c.signal});assert.equal(r.ok,true);assert.equal(r.byte_length,bytes.length);
  }
  assert.ok(peak<=3,`abort listeners grew: ${peak}`);assert.equal([...active.values()].reduce((n,s)=>n+s.size,0),0);
 }finally{AbortSignal.prototype.addEventListener=originalAdd;AbortSignal.prototype.removeEventListener=originalRemove;}
});
