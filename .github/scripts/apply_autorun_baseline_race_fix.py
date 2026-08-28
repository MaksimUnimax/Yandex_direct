#!/usr/bin/env python3
from pathlib import Path

content = Path('extension/src/content_script.js')
source = content.read_text(encoding='utf-8')
old = '''        if (activeAutoWatch) {
          activeAutoWatch.status = run.status;
          activeAutoWatch.paused = run.status === "paused";
          if (run.status === "waiting_command") scheduleAutoScan(0);
        }'''
new = '''        if (activeAutoWatch) {
          // The worker owns the authoritative baseline. A watch can be created while
          // the run is still STARTING with an empty baseline; when start delivery is
          // confirmed the same run_id receives the real assistant baseline. Refresh
          // it before enabling WAITING_COMMAND scanning so pre-start turns can never
          // be replayed as fresh Autorun commands.
          activeAutoWatch.assistant_baseline_ids = new Set((run.assistant_baseline_ids || []).map(String));
          activeAutoWatch.watch_id = run.watch_id || null;
          activeAutoWatch.status = run.status;
          activeAutoWatch.paused = run.status === "paused";
          if (run.status === "waiting_command") scheduleAutoScan(0);
        }'''
assert source.count(old) == 1, 'content sync authority block changed'
content.write_text(source.replace(old, new, 1), encoding='utf-8', newline='\n')

addendum = Path('extension/tests/qa_browser/direct_codex_gate_addendum_v2.mjs')
source = addendum.read_text(encoding='utf-8')
old = "  assert.equal((await runtimeSend(extensionPage,{type:'YMB_SAVE_DIRECT_POLICY',policy:{manual_enabled:true,autorun_enabled:true,max_requests_per_run:20,max_page_size:1000,max_report_days:31,max_report_rows:1000}}))?.ok,true);started=await runtimeSend(extensionPage,{type:'WS_START_AUTORUN',conversation_key:KEY,tab_id:chatTabId});assert.equal(started?.ok,true,`DIRECT_START_FAIL ${JSON.stringify(started)}`);state=await waitRun(extensionPage,'waiting_command');assert.equal(state.auto_run.active_service,'direct');"
new = "  assert.equal((await runtimeSend(extensionPage,{type:'YMB_SAVE_DIRECT_POLICY',policy:{manual_enabled:true,autorun_enabled:true,max_requests_per_run:20,max_page_size:1000,max_report_days:31,max_report_rows:1000}}))?.ok,true);const beforeDirectAutorunStart=providerHits.length;started=await runtimeSend(extensionPage,{type:'WS_START_AUTORUN',conversation_key:KEY,tab_id:chatTabId});assert.equal(started?.ok,true,`DIRECT_START_FAIL ${JSON.stringify(started)}`);state=await waitRun(extensionPage,'waiting_command');assert.equal(state.auto_run.active_service,'direct');await delay(3200);assert.equal(providerHits.length,beforeDirectAutorunStart,'STALE_MANUAL_TURN_REPLAYED_ON_DIRECT_AUTORUN_START');console.log('D16_STALE_MANUAL_TURN_BASELINE_FENCE_PASS');"
assert source.count(old) == 1, 'Direct addendum start block changed'
addendum.write_text(source.replace(old, new, 1), encoding='utf-8', newline='\n')

test = Path('extension/tests/autorun_baseline_sync.test.mjs')
test.write_text("""import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const content = fs.readFileSync(path.resolve(here, '../src/content_script.js'), 'utf8');

test('same-run state sync refreshes authoritative assistant baseline before WAITING_COMMAND scan', () => {
  const marker = 'activeAutoWatch.assistant_baseline_ids = new Set((run.assistant_baseline_ids || []).map(String));';
  assert.equal(content.split(marker).length - 1, 1);
  const baselineAt = content.indexOf(marker);
  const statusAt = content.indexOf('activeAutoWatch.status = run.status;', baselineAt);
  const scanAt = content.indexOf('if (run.status === \\\"waiting_command\\\") scheduleAutoScan(0);', baselineAt);
  assert.ok(baselineAt >= 0 && statusAt > baselineAt && scanAt > statusAt);
});

test('browser regression explicitly fences stale Manual turn when Direct Autorun starts', () => {
  const addendum = fs.readFileSync(path.resolve(here, 'qa_browser/direct_codex_gate_addendum_v2.mjs'), 'utf8');
  assert.match(addendum, /D16_STALE_MANUAL_TURN_BASELINE_FENCE_PASS/);
  assert.match(addendum, /STALE_MANUAL_TURN_REPLAYED_ON_DIRECT_AUTORUN_START/);
});
""", encoding='utf-8', newline='\n')

print('AUTORUN_BASELINE_FIX_APPLIED')
