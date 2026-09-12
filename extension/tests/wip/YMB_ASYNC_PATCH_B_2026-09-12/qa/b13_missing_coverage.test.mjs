// Pre-freeze development coverage on the exact candidate passed as YMB_FULL.
// Uses the preserved full-worker harness. Chrome/IDB/network remain fixtures.
import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
const {loadWorker,KEY,CID}=await import(pathToFileURL(process.env.YMB_HARNESS));
const full=process.env.YMB_FULL;
const plain=v=>JSON.parse(JSON.stringify(v));
const commands=[
 {method:'getTop',phrase:'браслет',regions:['213'],devices:['DEVICE_DESKTOP'],numPhrases:7},
 {method:'getDynamics',phrase:'браслет',regions:['225'],devices:['DEVICE_PHONE'],period:'PERIOD_MONTHLY',fromDate:'2026-01-01T00:00:00Z',toDate:'2026-02-01T00:00:00Z'},
 {method:'getRegionsDistribution',phrase:'браслет',region:'REGION_CITIES',devices:['DEVICE_ALL']},
 {method:'getRegionsTree'}
];
const endpoints={getTop:'topRequests',getDynamics:'dynamics',getRegionsDistribution:'regions',getRegionsTree:'getRegionsTree'};
const payloads={getTop:{totalCount:42,results:[{phrase:'браслет',count:37}],associations:[{phrase:'камень',count:5}]},getDynamics:{results:[{date:'2026-01-01',count:42}]},getRegionsDistribution:{results:[{regionId:'213',count:42}]},getRegionsTree:{regions:[{id:'225',name:'Россия',children:[]}]}};
const text=c=>'WORDSTAT_API_V1 '+JSON.stringify(c);
const manual=(h,c)=>h.dispatch({type:'WS_EXECUTE_MANUAL_BLOCK',conversation_key:KEY,manual_request_token:crypto.randomUUID(),block_text:typeof c==='string'?c:text(c)});
const envelope=r=>JSON.parse(r.report_text.slice(r.report_text.indexOf('\n')+1));
async function finish(h){const e=h.data.wsmb_outbox?.[KEY];if(e)await h.dispatch({type:'WS_MANUAL_DELIVERY_COMPLETE',conversation_key:KEY,delivery_id:e.delivery_id,delivery_confirmed:true,confirmation_basis:'microphone',composer_empty:true});}
const secrets=['TEST_WORDSTAT_NOT_REAL','TEST_SEARCH_NOT_REAL','TEST_WM_NOT_REAL','TEST_METRIKA_NOT_REAL','TEST_DIRECT_NOT_REAL'];
const noSecrets=v=>{const s=JSON.stringify(v);for(const t of secrets)assert.equal(s.includes(t),false,'secret in public result: '+t);};
for(const command of commands){
 test('Wordstat full Manual '+command.method+' exact fixed request and complete raw JSON',async()=>{
  const requests=[];const body=payloads[command.method];
  const h=await loadWorker(full,{network:async(url,init)=>{requests.push({url:String(url),init});return new Response(JSON.stringify(body),{status:200});}});h.seedBoundChat('wordstat');
  const r=await manual(h,command);assert.equal(r.request_executed,true,r.report_text);assert.equal(requests.length,1);
  const a=requests[0];assert.equal(a.url,'https://searchapi.api.cloud.yandex.net/v2/wordstat/'+endpoints[command.method]);assert.equal(a.init.method,'POST');
  assert.equal(a.init.headers.Authorization,'Api-Key TEST_WORDSTAT_NOT_REAL');assert.equal(a.init.headers['Content-Type'],'application/json');
  const built={...command,folderId:'folder'};delete built.method;assert.deepEqual(JSON.parse(a.init.body),built);
  const e=envelope(r);assert.equal(e.service,'wordstat');assert.equal(e.operation,command.method);assert.equal(e.status,'OK');assert.equal(e.request_executed,true);assert.equal(e.automatic_retry,false);assert.deepEqual(e.result,body);assert.ok(e.request_id);noSecrets(r);await finish(h);assert.equal(h.calls.fetch.length,1);
 });
 for(const status of [401,403,429,500])test('Wordstat full '+command.method+' HTTP '+status+' is not success and never retries',async()=>{
  const h=await loadWorker(full,{network:async()=>new Response(JSON.stringify({code:'CONTROLLED_'+status,message:'controlled error'}),{status})});h.seedBoundChat('wordstat');
  const r=await manual(h,command);const e=envelope(r);assert.equal(e.status,'ERROR');assert.equal(e.http_status,status);assert.equal(e.request_executed,true);assert.equal(e.automatic_retry,false);assert.equal(h.calls.fetch.length,1);noSecrets(r);await finish(h);assert.equal(h.calls.fetch.length,1);
 });
 test('Wordstat full '+command.method+' network failure remains UNKNOWN through delivery',async()=>{
  const h=await loadWorker(full,{network:async()=>{throw new Error('controlled socket error');}});h.seedBoundChat('wordstat');
  const r=await manual(h,command);const e=envelope(r);assert.equal(e.status,'ERROR');assert.equal(e.request_executed,'UNKNOWN');assert.equal(e.automatic_retry,false);assert.equal(h.calls.fetch.length,1);noSecrets(r);await finish(h);assert.equal(h.calls.fetch.length,1);
 });
 test('Wordstat full '+command.method+' malformed successful HTTP body must not be reported as success',async()=>{
  const h=await loadWorker(full,{network:async()=>new Response('{not-json',{status:200})});h.seedBoundChat('wordstat');
  const r=await manual(h,command);const e=envelope(r);assert.equal(e.status,'ERROR');assert.equal(e.request_executed,true);assert.equal(e.automatic_retry,false);assert.equal(h.calls.fetch.length,1);await finish(h);
 });
}
for(const [name,c,code]of [
 ['unsupported method',{method:'deleteEverything'},'UNSUPPORTED_METHOD'],
 ['missing phrase',{method:'getTop'},'MISSING_FIELD'],
 ['oversized phrase',{method:'getTop',phrase:'x'.repeat(401)},'FIELD_TOO_LONG'],
 ['out-of-range count',{method:'getTop',phrase:'x',numPhrases:2001},'INVALID_NUM_PHRASES'],
 ['invalid device',{method:'getTop',phrase:'x',devices:['BAD']},'INVALID_DEVICE'],
 ['invalid period',{method:'getDynamics',phrase:'x',period:'BAD'},'INVALID_PERIOD'],
 ['invalid date',{...commands[1],fromDate:'not-a-date'},'INVALID_DATE'],
 ['invalid region level',{...commands[2],region:'BAD'},'INVALID_REGION_LEVEL']
])test('Wordstat input '+name+' is rejected before network',async()=>{
 const h=await loadWorker(full);h.seedBoundChat('wordstat');const r=await manual(h,c);assert.match(r.report_text,new RegExp(code));assert.equal(r.request_executed,false);assert.equal(h.calls.fetch.length,0);noSecrets(r);
});
test('Wordstat untrusted URL/headers never affect constructed request',async()=>{
 const calls=[];const h=await loadWorker(full,{network:async(url,init)=>{calls.push({url:String(url),init});return new Response('{}');}});h.seedBoundChat('wordstat');
 const r=await manual(h,{...commands[0],url:'https://forbidden.invalid/',headers:{Authorization:'INJECTED'},api_key:'INJECTED',folderId:'injected'});
 assert.equal(calls.length,1);assert.equal(calls[0].url,'https://searchapi.api.cloud.yandex.net/v2/wordstat/topRequests');assert.equal(calls[0].init.headers.Authorization,'Api-Key TEST_WORDSTAT_NOT_REAL');assert.equal(JSON.parse(calls[0].init.body).folderId,'folder');assert.equal(r.report_text.includes('INJECTED'),false);
});
for(const debug of [false,true]){
 for(const [label,command,network]of [['parse','WORDSTAT_API_V1 {',null],['validation',{method:'getTop'},null],['unknown',{method:'getRegionsTree'},async()=>{throw new Error('controlled failure');}]])test('Debug '+debug+' does not hide '+label+' error or leak credentials',async()=>{
  const h=await loadWorker(full,{network});h.seedBoundChat('wordstat');h.data.ymb_debug_mode=debug;const r=await manual(h,command);assert.ok(h.data.wsmb_outbox[KEY]);assert.match(r.report_text,/YMB_ERROR_V1/);assert.equal(envelope(r).status,'ERROR');noSecrets(r);await finish(h);
 });
 test('Debug '+debug+' diagnostic storage is opt-in, bounded and key-redacted',async()=>{
  const h=await loadWorker(full);h.seedBoundChat('wordstat');h.data.ymb_debug_mode=debug;
  await h.run(`diagnostic('B13_CONTROLLED',{api_key:'TEST_WORDSTAT_NOT_REAL',Authorization:'TEST_SEARCH_NOT_REAL',nested:{oauth_token:'TEST_WM_NOT_REAL'},safe:'expected'})`);
  const d=plain(await h.run('getDiagnostics()'));noSecrets(d);if(debug){assert.equal(d.length,1);assert.equal(d[0].detail.api_key,'[REDACTED]');assert.equal(d[0].detail.safe,'expected');}else assert.equal(d.length,0);assert.equal(h.calls.fetch.length,0);
 });
}
async function backup(h){const r=await h.dispatch({type:'WS_EXPORT_BACKUP'},{});assert.equal(r.ok,true);return r.backup;}
async function restored(h,b){return h.dispatch({type:'WS_IMPORT_BACKUP',backup:b},{});}
test('full backup is explicitly secret-bearing while public state stays redacted',async()=>{
 const h=await loadWorker(full);h.seedBoundChat('wordstat');const b=await backup(h);assert.equal(b.contains_secrets,true);assert.equal(b.backup_version,3);assert.equal(b.settings.credentials.search.api_key,'TEST_SEARCH_NOT_REAL');assert.equal(b.settings.credentials.wordstat.api_key,'TEST_WORDSTAT_NOT_REAL');
 assert.match(b.settings_sha256,/^[0-9a-f]{64}$/);assert.equal(b.settings_sha256,await h.context.YMBSettingsBackupV3Runtime.checksum(b.settings));
 noSecrets(await h.dispatch({type:'WS_GET_GLOBAL_STATE'},{}));noSecrets(await h.dispatch({type:'YMB_GET_CREDENTIALS'},{}));assert.equal(h.calls.fetch.length,0);assert.equal(h.data.wsmb_outbox[KEY],undefined);
});
test('valid backup roundtrip restores settings and all five credential records to another worker fixture',async()=>{
 const h=await loadWorker(full);h.seedBoundChat('wordstat');h.data.wsmb_auto_send=false;h.data.ymb_debug_mode=true;h.data.wsmb_report_prefixes={[KEY]:{enabled:true,text:'prefix'}};const b=await backup(h);
 const target=await loadWorker(full);target.seedBoundChat('wordstat');for(const service of Object.keys(target.data.ymb_service_credentials))target.data.ymb_service_credentials[service]={};
 const r=await restored(target,b);assert.equal(r.ok,true,JSON.stringify(r));assert.equal(r.result.imported,true);assert.equal(target.data.wsmb_auto_send,false);assert.equal(target.data.ymb_debug_mode,true);assert.equal(target.data.wsmb_report_prefixes[KEY].text,'prefix');
 for(const service of ['wordstat','search','webmaster','metrika','direct'])assert.deepEqual(plain((await backup(target)).settings.credentials[service]),plain(b.settings.credentials[service]));noSecrets(r);assert.equal(target.calls.fetch.length,0);
});
for(const [label,mutate,code]of [
 ['tampering',b=>b.settings.debug_mode=!b.settings.debug_mode,'BACKUP_CHECKSUM_MISMATCH'],
 ['missing hash',b=>delete b.settings_sha256,'BACKUP_CHECKSUM_MISSING'],
 ['missing secret marker',b=>delete b.contains_secrets,'INVALID_BACKUP_SECRET_MARKER'],
 ['future version',b=>b.backup_version=999,'UNSUPPORTED_BACKUP_VERSION'],
 ['wrong format',b=>b.format='OTHER','UNSUPPORTED_BACKUP_FORMAT']
])test('backup '+label+' rejected without overwriting storage',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();const b=plain(await backup(h));mutate(b);const before=plain(h.data);const r=await restored(h,b);assert.equal(r.ok,false);assert.equal(r.code,code);assert.deepEqual(plain(h.data),before);assert.equal(h.calls.fetch.length,0);noSecrets(r);
});
for(const [kind,status,code]of [['manual','requesting','IMPORT_ACTIVE_MANUAL'],['manual','search_async_requesting','IMPORT_ACTIVE_MANUAL'],['manual','delivering','IMPORT_ACTIVE_MANUAL'],['run','requesting','IMPORT_ACTIVE_RUN'],['run','paused','IMPORT_ACTIVE_RUN']])test('backup refuses active '+kind+' '+status+' without clearing work',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();const b=await backup(h);
 if(kind==='manual')h.data.wsmb_manual_operations[KEY]={status,operation_id:'op',conversation_key:KEY};else h.data.wsmb_auto_runs[KEY]={status,run_id:'run',conversation_key:KEY};
 const before=plain(h.data);const r=await restored(h,b);assert.equal(r.ok,false);assert.equal(r.code,code);assert.deepEqual(plain(h.data),before);assert.equal(h.calls.fetch.length,0);
});
test('legacy wsmb credentials migrate without clearing unrelated service credentials',async()=>{
 const h=await loadWorker(full,{seed:{wsmb_api_key:'LEGACY_WORDSTAT_TEST',wsmb_folder_id:'oldfolder',ymb_service_credentials:{direct:{oauth_token:'DIRECT_KEEP_TEST',client_login:'qa',check_state:'PRESENT'}}}});
 const b=await backup(h);assert.equal(b.settings.credentials.wordstat.api_key,'LEGACY_WORDSTAT_TEST');assert.equal(b.settings.credentials.wordstat.folder_id,'oldfolder');assert.equal(b.settings.credentials.direct.oauth_token,'DIRECT_KEEP_TEST');assert.equal(h.calls.fetch.length,0);
});
test('same fixture persisted settings survive loading the complete worker again without network',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();h.data.wsmb_auto_send=false;const b=await backup(h);
 const fresh=await loadWorker(full,{seed:plain(h.data)});assert.equal((await backup(fresh)).settings_sha256,b.settings_sha256);noSecrets(await fresh.dispatch({type:'WS_GET_GLOBAL_STATE'},{}));assert.equal(fresh.calls.fetch.length,0);
});
for(const body of ['null','[]','123','true','"text"','', '<html>not JSON</html>'])test('Wordstat successful HTTP with invalid object envelope '+JSON.stringify(body),async()=>{
 const h=await loadWorker(full,{network:async()=>new Response(body,{status:200})});h.seedBoundChat('wordstat');const r=await manual(h,{method:'getRegionsTree'});
 assert.equal(envelope(r).status,'ERROR');assert.equal(envelope(r).code,'INVALID_WORDSTAT_RESPONSE');assert.equal(r.request_executed,true);assert.equal(h.calls.fetch.length,1);assert.equal(envelope(r).message,'Wordstat вернул некорректный JSON-ответ.');noSecrets(r);
});
test('Wordstat failed body read after successful headers is not an empty successful result',async()=>{
 const h=await loadWorker(full,{network:async()=>({ok:true,status:200,text:async()=>{throw new Error('controlled read failed');}})});h.seedBoundChat('wordstat');const r=await manual(h,{method:'getRegionsTree'});assert.match(r.report_text,/INVALID_WORDSTAT_RESPONSE/);assert.equal(r.request_executed,true);assert.equal(h.calls.fetch.length,1);
});
test('Wordstat object with omitted optional fields stays accepted; no invented required schema',async()=>{
 const h=await loadWorker(full,{network:async()=>new Response('{}')});h.seedBoundChat('wordstat');const r=await manual(h,{method:'getRegionsTree'});assert.equal(envelope(r).status,'OK');assert.deepEqual(envelope(r).result,{});assert.equal(h.calls.fetch.length,1);
});
test('Wordstat Check malformed response does not falsely validate an invalid key or retry',async()=>{
 const h=await loadWorker(full,{network:async()=>new Response('{bad')});h.seedBoundChat('wordstat');h.data.ymb_service_credentials.wordstat.check_state='INVALID_OR_EXPIRED';const r=await h.dispatch({type:'YMB_CHECK_SERVICE_CREDENTIAL',service:'wordstat'},{});
 assert.equal(r.ok,false);assert.equal(r.code,'INVALID_WORDSTAT_RESPONSE');assert.equal(r.request_executed,true);assert.equal(h.data.ymb_service_credentials.wordstat.check_state,'INVALID_OR_EXPIRED');assert.equal(h.calls.fetch.length,1);noSecrets(r);
});
test('Wordstat batch malformed response marks item failed, not SUCCEEDED with null payload',async()=>{
 const h=await loadWorker(full,{network:async()=>new Response('{bad')});h.seedBoundChat('wordstat');const jobId='ws-'+crypto.randomUUID();
 await manual(h,'WORDSTAT_BATCH_API_V1 '+JSON.stringify({action:'start',jobId,phrases:['one','two'],numPhrases:3,maxRequests:2,maxCostRub:1}));await finish(h);
 const r=await manual(h,'WORDSTAT_BATCH_API_V1 '+JSON.stringify({action:'next',jobId}));assert.equal(h.calls.fetch.length,1);assert.equal(r.request_executed,true);assert.match(r.report_text,/INVALID_WORDSTAT_RESPONSE/);assert.equal(envelope(r).progress.succeeded,0);await finish(h);assert.equal(h.calls.fetch.length,1);
});

test('Wordstat batch uses current isolated credential, never an obsolete legacy cloud key',async()=>{
 const requests=[];const h=await loadWorker(full,{seed:{wsmb_api_key:'OBSOLETE_CLOUD_KEY',wsmb_folder_id:'old-folder'},network:async(url,init)=>{requests.push({url:String(url),init});return new Response(JSON.stringify(payloads.getTop));}});h.seedBoundChat('wordstat');const jobId='ws-current-'+crypto.randomUUID();
 await manual(h,'WORDSTAT_BATCH_API_V1 '+JSON.stringify({action:'start',jobId,phrases:['one'],maxRequests:1,maxCostRub:1}));await finish(h);
 const r=await manual(h,'WORDSTAT_BATCH_API_V1 '+JSON.stringify({action:'next',jobId}));assert.equal(requests.length,1,r.report_text);assert.equal(requests[0].init.headers.Authorization,'Api-Key TEST_WORDSTAT_NOT_REAL');assert.equal(JSON.parse(requests[0].init.body).folderId,'folder');assert.equal(envelope(r).progress.succeeded,1);await finish(h);assert.equal(requests.length,1);noSecrets(r);
});
test('Debug diagnostic limit keeps latest 200 entries and clears without changing credentials',async()=>{
 const h=await loadWorker(full);h.seedBoundChat('wordstat');h.data.ymb_debug_mode=true;const credentials=plain(h.data.ymb_service_credentials);
 await h.run(`(async()=>{for(let i=0;i<205;i++)await diagnostic('B13_LIMIT_'+i,{api_key:'TEST_WORDSTAT_NOT_REAL'});})()`);
 const d=plain(await h.run('getDiagnostics()'));assert.equal(d.length,200);assert.equal(d[0].code,'B13_LIMIT_5');assert.equal(d.at(-1).code,'B13_LIMIT_204');noSecrets(d);assert.equal((await h.dispatch({type:'WS_CLEAR_DIAGNOSTICS'},{})).diagnostics.length,0);assert.deepEqual(plain(h.data.ymb_service_credentials),credentials);assert.equal(h.calls.fetch.length,0);
});

for(const [label,network,expected] of [
 ['success',async()=>new Response(JSON.stringify(payloads.getTop)),true],
 ['invalid JSON',async()=>new Response('{invalid'),true],
 ['network UNKNOWN',async()=>{throw new Error('controlled failure');},'UNKNOWN']
])test('Wordstat full batch Autorun '+label+' retains lifecycle and one boundary with dedicated credentials',async()=>{
 const h=await loadWorker(full,{network});h.seedBoundChat('wordstat');const jobId='ws-auto-'+crypto.randomUUID();
 await manual(h,'WORDSTAT_BATCH_API_V1 '+JSON.stringify({action:'start',jobId,phrases:['one'],maxRequests:1,maxCostRub:1}));await finish(h);h.data.wsmb_manual_modes[KEY]=false;
 const run={run_id:'run-'+crypto.randomUUID(),active_service:'wordstat',conversation_key:KEY,conversation_id:CID,tab_id:7,status:'waiting_command',requests_attempted:0,requests_executed:0,requests_skipped:0,estimated_cost_rub:0,sequence:0,permission_profile:'WORDSTAT',pause_requested:false,finish_requested:false};h.data.wsmb_auto_runs[KEY]=run;h.data.ymb_wordstat_policy={autorun_enabled:true,manual_enabled:true,max_requests_per_run:10,max_cost_rub_per_run:10};
 const r=await h.dispatch({type:'WS_AUTO_COMMAND',conversation_key:KEY,run_id:run.run_id,assistant_turn_id:'turn-'+crypto.randomUUID(),command_text:'WORDSTAT_BATCH_API_V1 '+JSON.stringify({action:'next',jobId})});
 assert.equal(h.calls.fetch.length,1,JSON.stringify(r));assert.equal(r.result.request_executed,expected);assert.equal(h.data.wsmb_auto_runs[KEY].requests_attempted,1);assert.equal(h.data.wsmb_auto_runs[KEY].requests_executed,1);
 const e=h.data.wsmb_outbox[KEY];const report=JSON.parse(e.report_text.slice(e.report_text.indexOf('\n')+1));assert.equal(report.progress.succeeded,label==='success'?1:0);noSecrets(e.report_text);
 await h.dispatch({type:'WS_AUTO_DELIVERY_COMPLETE',conversation_key:KEY,delivery_id:e.delivery_id,delivery_confirmed:true,confirmation_basis:'microphone',composer_empty:true});assert.equal(h.calls.fetch.length,1);
 if(expected==='UNKNOWN'){assert.equal(h.data.wsmb_auto_runs[KEY].status,'paused');}
});
for(const status of [401,429,500])test('Wordstat full batch HTTP '+status+' preserves failure and no implicit retry',async()=>{
 const h=await loadWorker(full,{network:async()=>new Response(JSON.stringify({code:'CONTROLLED',message:'controlled'}),{status})});h.seedBoundChat('wordstat');const jobId='ws-http-'+crypto.randomUUID();
 await manual(h,'WORDSTAT_BATCH_API_V1 '+JSON.stringify({action:'start',jobId,phrases:['one'],maxRequests:1,maxCostRub:1}));await finish(h);const r=await manual(h,'WORDSTAT_BATCH_API_V1 '+JSON.stringify({action:'next',jobId}));assert.equal(r.request_executed,true);assert.equal(h.calls.fetch.length,1);assert.equal(envelope(r).progress.succeeded,0);assert.equal(envelope(r).progress.failed_terminal,1);await finish(h);assert.equal(h.calls.fetch.length,1);noSecrets(r);
});
