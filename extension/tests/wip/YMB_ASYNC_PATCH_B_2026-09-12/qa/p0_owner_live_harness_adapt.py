#!/usr/bin/env python3
from pathlib import Path
import sys, json, hashlib


def replace_case(text, start_marker, next_marker, replacement):
    start = text.find(start_marker)
    if start < 0:
        raise SystemExit(f"missing start marker: {start_marker}")
    end = text.find(next_marker, start + len(start_marker))
    if end < 0:
        raise SystemExit(f"missing next marker after: {start_marker}")
    return text[:start] + replacement.rstrip() + "\n" + text[end:]


def adapt_b15(path):
    p = Path(path)
    s = p.read_text()
    start = " await runCase('occupied_composer_preserved_then_manual_send',async()=>{"
    nxt = " // Actual worker termination uses official WebWorker.close(), not a substituted ID."
    repl = r""" await runCase('occupied_composer_preserved_then_explicit_resume_manual_send',async()=>{
  await resetDelivery();await w.evaluate(()=>chrome.storage.local.set({wsmb_auto_send:false}));await page.evaluate(()=>{const e=document.getElementById('prompt-textarea');e.value='USER_TEXT_KEEP';e.dispatchEvent(new Event('input',{bubbles:true}));});const before=await fx();const d=await stageFile(1,'occupied');
  await until(async()=>w.evaluate(async key=>{const e=await getConversationOutbox(key);return e?.delivery_paused===true&&e.phase==='claimed';},KEY),'OCCUPIED_DURABLE_PAUSE_MISSING');assert.equal((await fx()).text,'USER_TEXT_KEEP');assert.equal((await fx()).changes,before.changes);
  await page.evaluate(()=>{const e=document.getElementById('prompt-textarea');e.value='';e.dispatchEvent(new Event('input',{bubbles:true}));});await delay(1800);assert.equal((await outbox()).phase,'claimed');assert.equal(await w.evaluate(async key=>(await getConversationOutbox(key))?.delivery_paused===true,KEY),true);assert.equal((await fx()).sends.length,before.sends.length);
  await until(async()=>page.$eval('#ymb-file-delivery-control',b=>!b.disabled&&b.textContent.includes('Продолжить')).catch(()=>false),'EXPLICIT_RESUME_CONTROL_MISSING');await page.click('#ymb-file-delivery-control');await until(async()=>(await outbox())?.phase==='attachment_ready','MANUAL_ATTACHMENT_NOT_READY_AFTER_EXPLICIT_RESUME');await delay(1200);assert.equal((await fx()).sends.length,before.sends.length);await page.click('#composer-submit-button');await until(async()=>!(await outbox()),'MANUAL_ATTACHMENT_NOT_CONFIRMED');assert.equal((await fx()).sends.length,before.sends.length+1);assert.deepEqual(await artifactGone(d.key),{remaining:0,meta:false});await w.evaluate(()=>chrome.storage.local.set({wsmb_auto_send:true}));return{user_text_preserved:true,durable_pause:true,resurrection_after_clear:0,explicit_resume:1,automatic_send_while_disabled:0,manual_send:1};
 });"""
    p.write_text(replace_case(s, start, nxt, repl))


def adapt_b17(path):
    p = Path(path)
    s = p.read_text()
    cases = [
        (
            "await runCase('explicit_pause_claimed_preserves_evidence_and_resume_delivers_once',async()=>{",
            "for(const mib of [1,10,32,64])await runCase('pause_inflight_",
            r"""await runCase('preexisting_draft_pause_preserves_evidence_and_explicit_resume_delivers_once',async()=>{
 await resetDelivery();await page.$eval('#prompt-textarea',e=>{e.value='KEEP_USER_TEXT';e.dispatchEvent(new Event('input',{bubbles:true}));});const d=await stageFile(1,'b17-before');const before=await fx();
 await until(async()=>(await pausedState())?.paused,'AUTO_PAUSE_NOT_DURABLE');assert.equal((await pausedState()).phase,'claimed');
 await page.$eval('#prompt-textarea',e=>{e.value='';e.dispatchEvent(new Event('input',{bubbles:true}));});await delay(1800);assert.equal((await fx()).changes,before.changes);assert.equal((await pausedState()).paused,true);assert.equal((await artifactGone(d.key)).meta,true);
 await clickControl();await until(async()=>(await fx()).sends.length===before.sends.length+1,'EXPLICIT_RESUME_NOT_DELIVERED');await until(async()=>!(await outbox()),'RESUME_NOT_ACKED');assert.deepEqual(await artifactGone(d.key),{remaining:0,meta:false});
 return{provider_cancelled:false,evidence_kept_while_paused:true,resurrection_after_clear:0,explicit_resume_send:1};
});"""
        ),
        (
            "await runCase('durable_pause_survives_page_reload_without_reads_or_send',async()=>{",
            "await runCase('pause_write_failure_is_locally_stopped_not_false_durable_success',async()=>{",
            r"""await runCase('durable_pause_survives_page_reload_without_reads_or_send',async()=>{
 await resetDelivery();await page.$eval('#prompt-textarea',e=>{e.value='HOLD';e.dispatchEvent(new Event('input',{bubbles:true}));});const beforePoll=(await messageCounts()).WS_GET_OUTBOX||0;const d=await stageFile(10,'b17-reload');
 await until(async()=>{const e=await pausedState(),c=await messageCounts();return e?.id===d.id&&e.paused===true&&e.phase==='claimed'&&(c.WS_GET_OUTBOX||0)>beforePoll;},'PRE_RELOAD_AUTO_PAUSE_MISSING');const counts=await messageCounts();await page.reload({waitUntil:'domcontentloaded'});await delay(2000);
 assert.equal((await pausedState()).paused,true);assert.equal((await fx()).changes,0);assert.equal((await fx()).sends.length,0);assert.equal((await messageCounts()).WS_GET_OUTBOX_ARTIFACT_CHUNK||0,counts.WS_GET_OUTBOX_ARTIFACT_CHUNK||0);assert.equal((await artifactGone(d.key)).meta,true);await resetDelivery();return{reload_pause_retained:true,automatic_materialization:0,artifact_deleted:false,preexisting_draft_pause:true};
});"""
        ),
        (
            "await runCase('foreign_tab_pause_denied_and_source_operation_not_erased',async()=>{",
            "\n\n assert.equal(tree(),target);",
            r"""await runCase('foreign_tab_pause_denied_and_source_operation_not_erased',async()=>{
 await resetDelivery();await w.evaluate(()=>chrome.storage.local.set({wsmb_auto_send:false}));const d=await stageFile(1,'b17-owner');await until(async()=>(await outbox())?.phase==='attachment_ready','FOREIGN_TEST_ATTACHMENT_NOT_READY');const p=await browser.newPage();await p.setRequestInterception(true);p.on('request',r=>{if(r.isNavigationRequest()&&r.url()===PAGE_URL)void r.respond({status:200,contentType:'text/html',body:fixture});else void r.abort();});await p.goto(PAGE_URL,{waitUntil:'domcontentloaded'});
 try{await delay(500);const r=await(await extensionRealm(p)).evaluate(({key,id})=>new Promise(ok=>chrome.runtime.sendMessage({type:'WS_SET_ATTACHMENT_PAUSED',conversation_key:key,delivery_id:id,paused:true},ok)),{key:KEY,id:d.id});assert.equal(r.ok,false);assert.equal(r.code,'AUTO_NON_OWNER_TAB');assert.equal((await pausedState()).paused,false);}finally{await p.close();await w.evaluate(()=>chrome.storage.local.set({wsmb_auto_send:true}));}
 await resetDelivery();return{foreign_control_denied:true,stable_phase:'attachment_ready'};
});"""
        )
    ]
    for start, nxt, repl in cases:
        s = replace_case(s, start, nxt, repl)
    p.write_text(s)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: p0_owner_live_harness_adapt.py B15_QUAL B17")
    before = {arg: hashlib.sha256(Path(arg).read_bytes()).hexdigest() for arg in sys.argv[1:]}
    adapt_b15(sys.argv[1])
    adapt_b17(sys.argv[2])
    after = {arg: hashlib.sha256(Path(arg).read_bytes()).hexdigest() for arg in sys.argv[1:]}
    print(json.dumps({
        "product_change": False,
        "qa_semantics": "preexisting draft causes durable pause; clearing composer never resumes; explicit Resume required",
        "before": before,
        "after": after
    }, indent=2))


if __name__ == "__main__":
    main()
