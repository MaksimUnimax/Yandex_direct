import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const sourcePath = path.resolve(here, '../src/shared/policy_model.js');

function loadPolicyModel() {
  const context = { console };
  context.globalThis = context;
  vm.createContext(context);
  vm.runInContext(fs.readFileSync(sourcePath, 'utf8'), context, { filename: sourcePath });
  return context.YMBPolicyModel;
}

test('popup-shaped current Search save does not silently disable GenSearch', () => {
  const policy = loadPolicyModel();
  const popupShapedSave = {
    autorun_enabled: false,
    manual_enabled: true,
    allowed_methods: ['search'],
    max_requests_per_run: 100,
    max_cost_rub_per_run: 10,
    method_cost_rub: { search: 0.488 },
    tariff_checked_at: '2026-08-28',
    tariff_source: 'https://aistudio.yandex.ru/docs/ru/search-api/pricing.html'
  };

  const normalized = policy.normalizeSearchPolicy(popupShapedSave);
  assert.deepEqual(JSON.parse(JSON.stringify(normalized.allowed_methods)), ['search', 'genSearch']);
  assert.equal(normalized.method_cost_rub.search, 0.488);
  assert.equal(normalized.method_cost_rub.genSearch, 5.08);

  const decision = policy.searchDecision({
    policy: popupShapedSave,
    channel: 'manual',
    method: 'genSearch',
    credentialState: 'PRESENT',
    run: { requests_executed: 0, estimated_cost_rub: 0 }
  });
  assert.equal(decision.allow, true);
  assert.equal(decision.estimated_cost_rub, 5.08);
});

test('normalized explicit GenSearch disable remains fail-closed after popup-save migration fix', () => {
  const policy = loadPolicyModel();
  const explicitlyDisabled = {
    autorun_enabled: false,
    manual_enabled: true,
    allowed_methods: ['search'],
    max_requests_per_run: 100,
    max_cost_rub_per_run: 10,
    method_cost_rub: { search: 0.488, genSearch: 5.08 },
    tariff_checked_at: '2026-08-28',
    tariff_source: 'https://aistudio.yandex.ru/docs/ru/search-api/pricing.html'
  };

  const normalized = policy.normalizeSearchPolicy(explicitlyDisabled);
  assert.deepEqual(JSON.parse(JSON.stringify(normalized.allowed_methods)), ['search']);
  const decision = policy.searchDecision({
    policy: explicitlyDisabled,
    channel: 'manual',
    method: 'genSearch',
    credentialState: 'PRESENT',
    run: { requests_executed: 0, estimated_cost_rub: 0 }
  });
  assert.equal(decision.allow, false);
  assert.equal(decision.reason, 'OPERATION_DISABLED');
});

test('unmarked custom Search allowlist is not treated as a migration candidate', () => {
  const policy = loadPolicyModel();
  const custom = policy.normalizeSearchPolicy({
    allowed_methods: ['search'],
    method_cost_rub: { search: 0.25 }
  });
  assert.deepEqual(JSON.parse(JSON.stringify(custom.allowed_methods)), ['search']);
  assert.equal(custom.method_cost_rub.genSearch, 5.08);
});
