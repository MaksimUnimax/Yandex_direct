import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';

const PRODUCT = path.resolve('extension/src');
const popupSource = fs.readFileSync(path.join(PRODUCT, 'popup_search_async_monitor.js'), 'utf8');
const contentSource = fs.readFileSync(path.join(PRODUCT, 'content_script.js'), 'utf8');

function plain(value) { return JSON.parse(JSON.stringify(value)); }
function counts(patch = {}) {
  return { PENDING:0, SUBMITTING:0, WAITING:0, COLLECTING:0, RESULT_SAVED:0, SUCCEEDED:0, PARSE_FAILED:0, FAILED:0, UNKNOWN:0, CANCELLED:0, ...patch };
}

const popupContext = vm.createContext({ console, __YMB_ASYNC_MONITOR_TEST__: true });
vm.runInContext(popupSource, popupContext, { filename: 'popup_search_async_monitor.js' });
const popup = popupContext.__YMB_ASYNC_MONITOR_TEST_API__;
assert.ok(popup, 'popup test API missing');

{
  const m = plain(popup.computeMetrics({ total:100, counts:counts({PENDING:100}) }));
  assert.equal(m.terminal, 0); assert.equal(m.processed_percent, 0); assert.equal(m.success_percent, 0); assert.equal(m.remaining, 100);
}
{
  const m = plain(popup.computeMetrics({ total:100, counts:counts({SUCCEEDED:37, WAITING:63}) }));
  assert.equal(m.terminal, 37); assert.equal(m.processed_percent, 37); assert.equal(m.success_percent, 37); assert.equal(m.remaining, 63);
}
{
  const m = plain(popup.computeMetrics({ total:100, counts:counts({SUCCEEDED:35, FAILED:2, WAITING:63}) }));
  assert.equal(m.terminal, 37); assert.equal(m.processed_percent, 37); assert.equal(m.success_percent, 35); assert.equal(m.remaining, 63);
}
{
  const m = plain(popup.computeMetrics({ total:1, counts:counts({SUCCEEDED:1}), result_row_count:0, normalized_items:1 }));
  assert.equal(m.state, 'Готово'); assert.equal(m.processed_percent, 100); assert.equal(m.success_percent, 100); assert.equal(m.result_row_count, 0);
}
{
  const m = plain(popup.computeMetrics({ total:100, counts:counts({SUCCEEDED:100}) }));
  assert.equal(m.processed_percent, 100); assert.equal(m.success_percent, 100); assert.equal(m.remaining, 0);
}
{
  const m = plain(popup.computeMetrics({ total:1, counts:counts({UNKNOWN:1}) }));
  assert.equal(m.terminal, 0); assert.equal(m.processed_percent, 0); assert.equal(m.state, 'Требует проверки');
}
{
  const now = 1_700_000_000_000;
  const future = plain(popup.actionAvailability({ job_id:'j', total:1, counts:counts({WAITING:1}), due_count:0, next_poll_at:now+61_000 }, now, false));
  assert.equal(future.collect_enabled, false); assert.match(future.collect_label, /^Проверить можно через /); assert.equal(future.export_enabled, false);
  const due = plain(popup.actionAvailability({ job_id:'j', total:1, counts:counts({WAITING:1}), due_count:1, next_poll_at:now }, now, false));
  assert.equal(due.collect_enabled, true);
  const complete = plain(popup.actionAvailability({ job_id:'j', total:1, counts:counts({SUCCEEDED:1}), due_count:0 }, now, false));
  assert.equal(complete.collect_enabled, false); assert.equal(complete.export_enabled, true);
  const missing = plain(popup.actionAvailability(null, now, false));
  assert.equal(missing.collect_enabled, false); assert.equal(missing.export_enabled, false);
}
{
  assert.deepEqual(plain(popup.buildActionMessage('collect_one', {job_id:'j',revision:7}, 'owner')), {type:'YMB_ASYNC_POPUP_ACTION',action:'collect_one',conversation_key:'owner',job_id:'j'});
  assert.deepEqual(plain(popup.buildActionMessage('export_page', {job_id:'j',revision:7}, 'owner')), {type:'YMB_ASYNC_POPUP_ACTION',action:'export_page',conversation_key:'owner',job_id:'j',revision:7});
}

const marker = '\n;(() => {\n  "use strict";\n\n  const MESSAGE_TYPE = "YMB_ASYNC_POPUP_ACTION";';
const at = contentSource.lastIndexOf(marker);
assert.ok(at >= 0, 'Stage B content ingress marker missing');
const ingressSource = contentSource.slice(at + 1);
for (const forbidden of ['searchapi.api.cloud.yandex.net', 'operation.api.cloud.yandex.net', 'XMLHttpRequest', 'fetch(']) assert.equal(ingressSource.includes(forbidden), false, `direct provider primitive in Stage B ingress: ${forbidden}`);

const KEY = 'https://chatgpt.com|qa-stage-b';
let calls = [];
let state = { manual_mode:true, service_context:{active_service:'search'}, auto_run:{status:'paused'} };
let executeResponse = { ok:true, accepted:true, request_executed:true };
let heldStateCallbacks = [];
let holdState = false;
let listener = null;
const runtime = {
  lastError: null,
  onMessage: { addListener(fn) { listener = fn; } },
  sendMessage(message, callback) {
    calls.push(plain(message));
    if (message.type === 'WS_GET_STATE') {
      if (holdState) { heldStateCallbacks.push(callback); return; }
      queueMicrotask(() => callback({ok:true,state}));
      return;
    }
    if (message.type === 'WS_EXECUTE_MANUAL_BLOCK') {
      queueMicrotask(() => callback(executeResponse));
      return;
    }
    queueMicrotask(() => callback({ok:false,code:'UNEXPECTED_TEST_MESSAGE'}));
  }
};
const contentContext = vm.createContext({
  console,
  location:{href:'https://chatgpt.com/c/qa-stage-b'},
  document:{querySelector(){return null;}},
  BB2ConversationIdentity:{identityFromCandidates(){return {conversation_key:KEY};}},
  BB2ManualControls:{makeId(prefix){return `${prefix}-qa-token`; }},
  chrome:{runtime},
  __YMB_ASYNC_POPUP_CONTENT_TEST__:true,
  queueMicrotask
});
vm.runInContext(ingressSource, contentContext, {filename:'content_script.stage_b.js'});
assert.equal(typeof listener, 'function', 'Stage B message listener missing');
const ingress = contentContext.__YMB_ASYNC_POPUP_CONTENT_TEST_API__;
assert.ok(ingress, 'Stage B content test API missing');

function reset(nextState = { manual_mode:true, service_context:{active_service:'search'}, auto_run:{status:'paused'} }) {
  calls = []; state = nextState; executeResponse = {ok:true,accepted:true,request_executed:true}; holdState=false; heldStateCallbacks=[];
}
function executeCalls() { return calls.filter(x => x.type === 'WS_EXECUTE_MANUAL_BLOCK'); }
const collectMessage = {type:'YMB_ASYNC_POPUP_ACTION',action:'collect_one',conversation_key:KEY,job_id:'job-1'};

reset();
{
  const r = plain(await ingress.executePopupAction({...collectMessage,conversation_key:'wrong'}));
  assert.equal(r.code,'ASYNC_POPUP_CONVERSATION_MISMATCH'); assert.equal(calls.length,0); assert.equal(executeCalls().length,0);
}
reset({manual_mode:false,service_context:{active_service:'search'},auto_run:{status:'paused'}});
{
  const r=plain(await ingress.executePopupAction(collectMessage)); assert.equal(r.code,'ASYNC_POPUP_MANUAL_MODE_OFF'); assert.equal(executeCalls().length,0);
}
reset({manual_mode:true,service_context:{active_service:'wordstat'},auto_run:{status:'paused'}});
{
  const r=plain(await ingress.executePopupAction(collectMessage)); assert.equal(r.code,'ASYNC_POPUP_SEARCH_NOT_ACTIVE'); assert.equal(executeCalls().length,0);
}
reset({manual_mode:true,service_context:{active_service:'search'},auto_run:{status:'running'}});
{
  const r=plain(await ingress.executePopupAction(collectMessage)); assert.equal(r.code,'ASYNC_POPUP_AUTORUN_NOT_PAUSED'); assert.equal(executeCalls().length,0);
}
reset();
{
  const r=plain(await ingress.executePopupAction(collectMessage)); assert.equal(r.ok,true); assert.equal(executeCalls().length,1);
  assert.equal(executeCalls()[0].block_text, 'SEARCH_ASYNC_BATCH_API_V1\n'+JSON.stringify({action:'collectN',jobId:'job-1',count:1}));
  assert.equal(executeCalls()[0].conversation_key,KEY); assert.match(executeCalls()[0].manual_request_token,/^popup-async-/);
}
reset();
{
  const r=plain(await ingress.executePopupAction({type:'YMB_ASYNC_POPUP_ACTION',action:'export_page',conversation_key:KEY,job_id:'job-1',revision:9})); assert.equal(r.ok,true); assert.equal(executeCalls().length,1);
  assert.equal(executeCalls()[0].block_text, 'SEARCH_ASYNC_BATCH_API_V1\n'+JSON.stringify({action:'exportPage',jobId:'job-1',after:-1,limit:25,revision:9}));
}
reset();
{
  const r=plain(await ingress.executePopupAction({...collectMessage,action:'arbitrary'})); assert.equal(r.code,'ASYNC_POPUP_ACTION_UNSUPPORTED'); assert.equal(calls.length,0);
}
reset(); holdState=true;
{
  const first=ingress.executePopupAction(collectMessage);
  await new Promise(resolve=>setImmediate(resolve));
  assert.equal(heldStateCallbacks.length,1);
  const second=plain(await ingress.executePopupAction(collectMessage)); assert.equal(second.code,'ASYNC_POPUP_ACTION_IN_FLIGHT'); assert.equal(executeCalls().length,0);
  holdState=false; heldStateCallbacks.shift()({ok:true,state});
  const firstResult=plain(await first); assert.equal(firstResult.ok,true); assert.equal(executeCalls().length,1);
}
reset();
{
  assert.throws(()=>ingress.buildManualBlock({...collectMessage,job_id:'bad\njob'}),/Некорректный deferred Search job/);
}

const result = {
  schema_version:1,
  product_sha:process.env.PRODUCT_SHA || null,
  popup_cases:['0_of_100','37_of_100','35_plus_2','succeeded_zero_serp','100_percent','unknown_nonterminal','future_due_disabled','due_enabled','complete_export','missing_job','structured_messages'],
  ingress_cases:['wrong_conversation_zero_execute','manual_off_zero_execute','search_inactive_zero_execute','autorun_running_zero_execute','collect_exactly_one_manual_block','export_existing_manual_block','unsupported_zero_execute','concurrent_double_click_at_most_one','job_injection_rejected','no_direct_provider_primitive'],
  pass:true
};
const out=process.env.STAGE_B_CONTRACT_EVIDENCE;
if(out){fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'RESULT.json'),JSON.stringify(result,null,2)+'\n');}
console.log(JSON.stringify(result,null,2));
