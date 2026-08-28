import test from 'node:test';
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
  const scanAt = content.indexOf('if (run.status === \"waiting_command\") scheduleAutoScan(0);', baselineAt);
  assert.ok(baselineAt >= 0 && statusAt > baselineAt && scanAt > statusAt);
});

test('browser regression explicitly fences stale Manual turn when Direct Autorun starts', () => {
  const addendum = fs.readFileSync(path.resolve(here, 'qa_browser/direct_codex_gate_addendum_v2.mjs'), 'utf8');
  assert.match(addendum, /D16_STALE_MANUAL_TURN_BASELINE_FENCE_PASS/);
  assert.match(addendum, /STALE_MANUAL_TURN_REPLAYED_ON_DIRECT_AUTORUN_START/);
});
