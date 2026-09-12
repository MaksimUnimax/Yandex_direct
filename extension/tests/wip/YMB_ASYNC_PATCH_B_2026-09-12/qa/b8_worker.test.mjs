// Uses the preserved B7 Manual harness, actual B8 protocol/export/worker and actual
// Patch A binary store. IndexedDB, tab/settings/run and provider runtime are fixtures.
import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';import crypto from 'node:crypto';
import {harness,manual,KEY,context,F} from './harness_b8.mjs';
import * as fake from './idb_artifact_fixture.mjs';
Object.assign(context,fake,{crypto:crypto.webcrypto,TextEncoder,ArrayBuffer,Uint8Array,TextDecoder});
for(const path of ['../baseline/shared/search_protocol.js','../inputs/file_artifact_store.js','../candidate/b8/search_async_protocol.js','../candidate/b8/search_async_export.js'])vm.runInContext(fs.readFileSync(new URL(path,import.meta.url),'utf8'),context);
const A=context.YMBFileArtifactStore,P=context.SearchAsyncProtocol;let seq=0;
function setup(options={}){
 const h=harness(options),n=++seq;const originalUid=h.deps.uid;
 h.summary.counts={SUCCEEDED:2};h.summary.revision=7;
 h.store.peekNext=async()=>({folder_id:'folder',parameters:{region:'225'},progress:{...h.summary}});
 h.store.readItem=async(j,o,i)=>{assert.equal(o,KEY);return{job_id:j,index:i,query:'полный запрос '+i,state:'SUCCEEDED',operation_id:'op-'+i};};
 h.store.readResult=async(j,o,i)=>({job_id:j,index:i,operation_id:'op-'+i,raw_text:'original-provider-data-'+i,normalized:{results:[{rank:1,url:'https://example.test/'+i,title:'полный результат'}]}});
 const deps={...h.deps,protocol:P,artifactStore:A,exportFactory:context.YMBSearchAsyncExport,uid:p=>originalUid(p)+'-'+n,...options.deps};
 h.worker=F.create(deps);return{...h,deps};
}
const exportCommand=(extra={})=>({action:'exportPage',jobId:'job-1',...extra});
const unwrap=r=>JSON.parse(r.report_text.slice(r.report_text.indexOf('\n')+1));
const cleanup=async h=>{for(const d of h.state.outbox?.artifact_descriptors||[])await A.deleteArtifact(d.artifact_key);};
test('exportPage is local with operation host disabled, stages one file via A, returns no raw content',async()=>{
 const h=setup();const r=await manual(h,exportCommand());assert.equal(r.accepted,true);assert.equal(r.request_executed,false);assert.equal(h.calls.runtime.length,0);assert.equal(h.calls.prefix,0);assert.equal(h.calls.bind.length,0);
 const e=unwrap(r).export_page;assert.equal(e.item_count,2);assert.equal(e.result_row_count,2);assert.equal(h.state.outbox.delivery_mode,'attachment_v2');assert.equal(h.state.outbox.artifact_descriptors.length,1);
 const d=h.state.outbox.artifact_descriptors[0];assert.equal(d.delivery_id,r.delivery_id);assert.equal(d.byte_length,e.bytes);assert.equal((await A.getMeta(d.artifact_key)).status,'ready');assert.equal(h.state.operation.status,'delivering');
 for(const value of ['original-provider-data','полный запрос','полный результат','chunk_manifest','artifact_descriptors'])assert.equal(JSON.stringify(r).includes(value),false);await cleanup(h);
});
test('missing artifact dependency is local explicit error, old commands remain available',async()=>{
 const h=setup({deps:{artifactStore:null}});const r=await manual(h,exportCommand());assert.match(r.report_text,/ASYNC_EXPORT_NOT_READY/);assert.equal(h.calls.runtime.length,0);assert.equal(h.state.outbox.artifact_descriptors,undefined);
 const s=setup({deps:{artifactStore:null}});assert.match((await manual(s,{action:'status',jobId:'job-1'})).report_text,/"total":2/);
});
for(const [name,change,code] of [['manual off',{manual:false},'MANUAL_MODE_DISABLED'],['other service',{service:'wordstat'},'SERVICE_NOT_ACTIVE'],['outbox occupied',{outbox:{delivery_id:'prior'}},'DELIVERY_IN_PROGRESS'],['unbound',{binding:null},'CONVERSATION_NOT_BOUND']])test('export guard '+name,async()=>{
 const h=setup(change);const r=await manual(h,exportCommand());assert.equal(r.code,code);assert.equal(h.calls.runtime.length,0);assert.equal(h.calls.outbox.length,0);
});
test('bad revision, page limit and credential injection rejected before export',async()=>{
 for(const extra of [{after:0},{revision:-1},{limit:26},{url:'https://evil.invalid'},{api_key:'inject'},{folderId:'other'}]){
  const h=setup();const r=await manual(h,exportCommand(extra));assert.match(r.report_text,/ERR:/);assert.equal(h.state.outbox.artifact_descriptors,undefined);assert.equal(h.calls.runtime.length,0);
 }
});
test('stale revision rejected, no descriptor in error outbox',async()=>{const h=setup();const r=await manual(h,exportCommand({revision:6}));assert.match(r.report_text,/EXPORT_REVISION_CHANGED/);assert.equal(h.state.outbox.artifact_descriptors,undefined);});
test('duplicate simultaneous Manual actions cannot overwrite operation or produce second file',async()=>{
 const h=setup();let release;h.store.peekNext=async()=>{await new Promise(r=>release=r);return{folder_id:'folder',parameters:{region:'225'},progress:{...h.summary}};};
 const first=manual(h,exportCommand(),'one');await new Promise(r=>setImmediate(r));const second=await manual(h,exportCommand(),'two');assert.equal(second.code,'MANUAL_OPERATION_ACTIVE');release();const r=await first;assert.equal(r.accepted,true);assert.equal(h.calls.outbox.length,1);await cleanup(h);
});
test('definite outbox write failure removes only export artifact',async()=>{
 const h=setup({deps:{putOutbox:async()=>{throw new Error('disk');}}});await assert.rejects(()=>manual(h,exportCommand()));
 const k='async-export:delivery-2-'+seq;assert.equal(await A.getMeta(k),undefined);assert.equal((await h.store.readResult('job-1',KEY,0)).raw_text,'original-provider-data-0');
});
test('outbox committed but write response fails: retain artifact for existing recovery, never regenerate',async()=>{
 const h=setup();const put=async(k,v)=>{h.state.outbox=v;throw new Error('response lost');};h.worker=F.create({...h.deps,putOutbox:put});await assert.rejects(()=>manual(h,exportCommand()));
 const d=h.state.outbox.artifact_descriptors[0];assert.equal((await A.getMeta(d.artifact_key)).status,'ready');const r=await manual(h,exportCommand());assert.equal(r.accepted,false);await cleanup(h);
});
test('manual-state write failure after durable outbox does not delete ready export',async()=>{
 const h=setup();const base=h.deps.setManualOperation;h.worker=F.create({...h.deps,setManualOperation:async(k,v)=>{if(v.status==='delivering')throw new Error('disk');return base(k,v);}});await assert.rejects(()=>manual(h,exportCommand()));
 assert.ok(h.state.outbox.artifact_descriptors);assert.ok(await A.getMeta(h.state.outbox.artifact_descriptors[0].artifact_key));await cleanup(h);
});
test('B2 existing command and provider URL behavior unchanged by export schema',()=>{
 const old=vm.createContext({SearchProtocol:context.SearchProtocol});old.globalThis=old;vm.runInContext(fs.readFileSync(new URL('../inputs/search_async_protocol.js',import.meta.url),'utf8'),old);
 for(const action of ['status','pause','resume','cancelPending','submit','submitN','collect','collectN','collectReady','itemsPage'])assert.equal(JSON.stringify(P.normalizeCommand({action,jobId:'job'})),JSON.stringify(old.SearchAsyncProtocol.normalizeCommand({action,jobId:'job'})));
 const args=['браслет',{region:'225'},'folder'];assert.equal(JSON.stringify(P.buildSubmitRequest(...args)),JSON.stringify(old.SearchAsyncProtocol.buildSubmitRequest(...args)));assert.equal(JSON.stringify(P.buildGetRequest('op')),JSON.stringify(old.SearchAsyncProtocol.buildGetRequest('op')));
});
function installerSource(source){
 const h=setup();const c=vm.createContext({...context,...h.deps});c.globalThis=c;
 c.YMBSearchAdmissionBinding=h.binding;c.executeManualBlock=h.deps.baseExecuteManualBlock;c.YMBSearchAsyncStore=h.store;
 c.YMBSearchAsyncRuntime={create:()=>h.runtime};c.YMBSearchAsyncTransport={create:()=>({})};c.YMBSearchAsyncNormalizer={create:()=>()=>({})};c.YMBSearchXml={};
 c.YMBSearchAsyncPolicy={PRICE_MICRORUB:30500};c.YMBRunContextModel=h.deps.runContextModel;c.WordstatAutorunModel=h.deps.autorunModel;
 c.chrome={runtime:{getManifest:()=>({host_permissions:[]})}};c.KEYS={MANUAL_OPERATIONS:'ops'};c.storageGet=async()=>({});c.storageSet=async()=>{};c.WORKER_SESSION_ID='worker-11111111-1111-4111-8111-111111111111';c.fetch=async()=>{throw new Error('no network');};
 vm.runInContext(source,c);return c.YMBSearchAsyncWorkerIntegration;
}
test('saved B7 autoInstall workerId delimiter failure reproduced; B8 exact initializer no longer rejects its own ID',()=>{
 const old=installerSource(fs.readFileSync(new URL('../inputs/search_async_worker_transport.js',import.meta.url),'utf8'));assert.equal(old.ready,false);assert.equal(old.code,'ASYNC_WORKER_ID_INVALID');
 const fixed=installerSource(fs.readFileSync(new URL('../candidate/b8/search_async_worker_transport.js',import.meta.url),'utf8'));assert.equal(fixed.ready,true);assert.equal(fixed.providerEnabled,false);
});
