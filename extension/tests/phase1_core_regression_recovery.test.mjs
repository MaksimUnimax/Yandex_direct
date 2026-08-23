import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const ctx = vm.createContext({ console, URL, Date, Math, crypto: webcrypto, structuredClone });
ctx.globalThis = ctx;
for (const file of [
  'shared/product.js',
  'shared/conversation_identity.js',
  'shared/service_registry.js',
  'shared/block_command_discovery.js',
  'shared/run_context_model.js',
  'shared/credential_registry.js',
  'shared/policy_model.js',
  'shared/cost_ledger_model.js',
  'shared/wordstat_protocol.js',
  'shared/autorun_model.js',
  'shared/manual_controls.js'
]) vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), ctx, { filename: file });

const identity = ctx.BB2ConversationIdentity;
const registry = ctx.YMBServiceRegistry;
const discovery = ctx.YMBBlockCommandDiscovery;
const runContext = ctx.YMBRunContextModel;
const credentials = ctx.YMBCredentialRegistry;
const policy = ctx.YMBPolicyModel;
const ledger = ctx.YMBCostLedgerModel;
const wordstat = ctx.WordstatProtocol;
const autorun = ctx.MarketingAutorunModel;
const manual = ctx.BB2ManualControls;
const CID = 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa';
const KEY = `https://chatgpt.com|${CID}`;

const plain = (value) => value === undefined ? undefined : JSON.parse(JSON.stringify(value));
const codeIs = (code) => (error) => error?.code === code;
const command = (method, extra = {}) => `WORDSTAT_API_V1 ${JSON.stringify({ method, ...extra })}`;

// Identity, ownership and service routing.
test('conversation identity accepts only supported ChatGPT origins', () => {
  assert.equal(identity.normalizeOrigin('https://chatgpt.com/c/x'), 'https://chatgpt.com');
  assert.equal(identity.normalizeOrigin('https://chat.openai.com/c/x'), 'https://chat.openai.com');
  assert.equal(identity.normalizeOrigin('https://evil.example/c/x'), '');
  assert.equal(identity.normalizeOrigin('not a url'), '');
});

test('conversation identity confirms UUID paths and normalizes case', () => {
  const current = identity.identityFromUrl(`https://chatgpt.com/c/${CID}?x=1`);
  assert.equal(current.status, 'confirmed');
  assert.equal(current.conversation_key, KEY);
  const legacy = identity.identityFromUrl(`https://chat.openai.com/c/${CID.toUpperCase()}`);
  assert.equal(legacy.status, 'confirmed');
  assert.equal(legacy.conversation_id, CID);
});

test('conversation identity fails closed for missing, malformed and foreign conversation keys', () => {
  assert.equal(identity.identityFromUrl('https://chatgpt.com/').status, 'unconfirmed');
  assert.equal(identity.identityFromUrl('https://chatgpt.com/c/not-a-uuid').conversation_key, '');
  assert.equal(identity.identityFromUrl('%%%').status, 'unavailable');
  assert.equal(identity.normalizeConversationKey(`https://evil.example|${CID}`), '');
  assert.throws(() => identity.normalizeConversationKey('broken', { required: true }), codeIs('CONVERSATION_KEY_INVALID'));
});

test('sameConversation compares both allowed origin and UUID', () => {
  assert.equal(identity.sameConversation(KEY, `https://chatgpt.com|${CID.toUpperCase()}`), true);
  assert.equal(identity.sameConversation(KEY, `https://chat.openai.com|${CID}`), false);
  assert.equal(identity.sameConversation('', ''), false);
});

test('service registry exposes only Wordstat and synchronous Search', () => {
  assert.deepEqual(plain(registry.DEFINITIONS), [
    { service: 'wordstat', prefix: 'WORDSTAT_API_V1' },
    { service: 'search', prefix: 'SEARCH_API_V1' }
  ]);
  assert.equal(registry.isKnownService('wordstat'), true);
  assert.equal(registry.isKnownService('search'), true);
  assert.equal(registry.isKnownService('images'), false);
});

test('service registry detects protocol markers and rejects unknown markers', () => {
  assert.equal(registry.detect('  WORDSTAT_API_V1 {}')?.service, 'wordstat');
  assert.equal(registry.detect('\u00a0SEARCH_API_V1 {}')?.service, 'search');
  assert.equal(registry.detect('OTHER_API_V1 {}'), null);
  assert.equal(registry.definitionForService('search')?.prefix, 'SEARCH_API_V1');
});

test('block discovery finds multiple service commands in exact source order', () => {
  const found = discovery.discover(`before SEARCH_API_V1 {"method":"search","queryText":"one"}\nmid WORDSTAT_API_V1 {"method":"getRegionsTree"}`);
  assert.equal(found.length, 2);
  assert.deepEqual(plain(found.map((item) => [item.service, item.ok])), [['search', true], ['wordstat', true]]);
  assert.ok(found[0].index < found[1].index);
});

test('block discovery handles quoted braces and fails closed on malformed JSON', () => {
  const good = discovery.discover('SEARCH_API_V1 {"method":"search","queryText":"a } \\"quoted\\" value"}');
  assert.equal(good[0].ok, true);
  assert.equal(good[0].raw.queryText, 'a } "quoted" value');
  assert.equal(discovery.discover('SEARCH_API_V1 no-json')[0].code, 'MISSING_JSON');
  assert.equal(discovery.discover('WORDSTAT_API_V1 {"method":"getTop"')[0].code, 'UNTERMINATED_JSON');
});

test('block fingerprints are deterministic and content-sensitive', () => {
  assert.equal(discovery.textFingerprint('abc'), discovery.textFingerprint('abc'));
  assert.notEqual(discovery.textFingerprint('abc'), discovery.textFingerprint('abd'));
  assert.match(discovery.textFingerprint('abc'), /^[0-9a-f]{8}$/);
});

test('run context accepts registered service and rejects missing/unknown/wrong service', () => {
  assert.equal(runContext.normalizeActiveService(' Search ', registry), 'search');
  assert.throws(() => runContext.normalizeActiveService('', registry, { required: true }), codeIs('ACTIVE_SERVICE_MISSING'));
  assert.throws(() => runContext.normalizeActiveService('images', registry), codeIs('UNKNOWN_SERVICE'));
  assert.equal(runContext.assertServiceMatch('search', 'search'), true);
  assert.throws(() => runContext.assertServiceMatch('search', 'wordstat'), codeIs('SERVICE_NOT_ACTIVE'));
  assert.deepEqual(plain(runContext.makeRunIdentity({ activeService: 'wordstat', registry })), { active_service: 'wordstat' });
});

test('credential registry requires both local API key and folder id and fails unknown service closed', () => {
  assert.equal(credentials.wordstatCapability({ apiKey: 'k', folderId: 'f' }).state, 'PRESENT');
  assert.equal(credentials.searchCapability({ apiKey: 'k', folderId: '' }).state, 'MISSING');
  assert.equal(credentials.searchCapability({ apiKey: '', folderId: 'f' }).state, 'MISSING');
  assert.deepEqual(plain(credentials.capabilityForService('images', { apiKey: 'secret', folderId: 'folder' })), {
    state: 'NO_ACCESS', has_api_key: false, has_folder_id: false
  });
});

// Wordstat protocol and provider-boundary contract.
test('Wordstat recognizes only WORDSTAT_API_V1 and normalizes getRegionsTree', () => {
  assert.equal(wordstat.isCommandText(' WORDSTAT_API_V1 {}'), true);
  assert.equal(wordstat.isCommandText('SEARCH_API_V1 {}'), false);
  assert.deepEqual(plain(wordstat.parseCommand(command('getRegionsTree'))), { method: 'getRegionsTree' });
});

test('Wordstat getTop applies defaults and exact phrase-count boundaries', () => {
  const parsed = wordstat.parseCommand(command('getTop', { phrase: 'купить ноутбук' }));
  assert.equal(parsed.numPhrases, 100);
  assert.deepEqual(plain(parsed.regions), ['225']);
  assert.deepEqual(plain(parsed.devices), ['DEVICE_ALL']);
  assert.equal(wordstat.parseCommand(command('getTop', { phrase: 'x', numPhrases: 1 })).numPhrases, 1);
  assert.equal(wordstat.parseCommand(command('getTop', { phrase: 'x', numPhrases: 2000 })).numPhrases, 2000);
});

test('Wordstat getTop rejects invalid phrase count, phrase, device and oversized regions', () => {
  assert.throws(() => wordstat.parseCommand(command('getTop', { phrase: 'x', numPhrases: 0 })), codeIs('INVALID_NUM_PHRASES'));
  assert.throws(() => wordstat.parseCommand(command('getTop', { phrase: 'x', numPhrases: 2001 })), codeIs('INVALID_NUM_PHRASES'));
  assert.throws(() => wordstat.parseCommand(command('getTop', { phrase: '' })), codeIs('MISSING_FIELD'));
  assert.throws(() => wordstat.parseCommand(command('getTop', { phrase: 'x'.repeat(401) })), codeIs('FIELD_TOO_LONG'));
  assert.throws(() => wordstat.parseCommand(command('getTop', { phrase: 'x', devices: ['WATCH'] })), codeIs('INVALID_DEVICE'));
  assert.throws(() => wordstat.parseCommand(command('getTop', { phrase: 'x', regions: Array.from({ length: 101 }, (_, i) => String(i + 1)) })), codeIs('TOO_MANY_ITEMS'));
});

test('Wordstat getDynamics requires period and valid RFC3339 dates', () => {
  const parsed = wordstat.parseCommand(command('getDynamics', {
    phrase: 'x', period: 'PERIOD_DAILY', fromDate: '2026-08-01T00:00:00Z', toDate: '2026-08-20T00:00:00Z'
  }));
  assert.equal(parsed.period, 'PERIOD_DAILY');
  assert.deepEqual(plain(parsed.regions), ['225']);
  assert.throws(() => wordstat.parseCommand(command('getDynamics', {
    phrase: 'x', period: 'PERIOD_DAILY', fromDate: 'bad', toDate: '2026-08-20T00:00:00Z'
  })), codeIs('INVALID_DATE'));
  assert.throws(() => wordstat.parseCommand(command('getDynamics', {
    phrase: 'x', period: 'YEARLY', fromDate: '2026-08-01T00:00:00Z', toDate: '2026-08-20T00:00:00Z'
  })), codeIs('INVALID_PERIOD'));
  assert.throws(() => wordstat.parseCommand(command('getDynamics', {
    phrase: 'x', fromDate: '2026-08-01T00:00:00Z', toDate: '2026-08-20T00:00:00Z'
  })), codeIs('MISSING_FIELD'));
});

test('Wordstat getRegionsDistribution uses region enum plus device defaults', () => {
  const parsed = wordstat.parseCommand(command('getRegionsDistribution', { phrase: 'x' }));
  assert.equal(parsed.region, 'REGION_ALL');
  assert.deepEqual(plain(parsed.devices), ['DEVICE_ALL']);
  assert.equal(Object.hasOwn(parsed, 'regions'), false);
  assert.throws(() => wordstat.parseCommand(command('getRegionsDistribution', { phrase: 'x', region: 'COUNTRIES' })), codeIs('INVALID_REGION_LEVEL'));
  for (const region of ['REGION_ALL', 'REGION_CITIES', 'REGION_REGIONS']) {
    assert.equal(wordstat.parseCommand(command('getRegionsDistribution', { phrase: 'x', region })).region, region);
  }
});

test('Wordstat buildRequest maps all four methods to official host and keeps folderId local', () => {
  const cases = [
    ['getTop', { phrase: 'x' }, '/v2/wordstat/topRequests'],
    ['getDynamics', { phrase: 'x', period: 'PERIOD_DAILY', fromDate: '2026-08-01T00:00:00Z', toDate: '2026-08-20T00:00:00Z' }, '/v2/wordstat/dynamics'],
    ['getRegionsDistribution', { phrase: 'x' }, '/v2/wordstat/regions'],
    ['getRegionsTree', {}, '/v2/wordstat/getRegionsTree']
  ];
  for (const [method, extra, endpoint] of cases) {
    const normalized = wordstat.normalizeCommand({ method, ...extra });
    const request = wordstat.buildRequest(normalized, 'folder-1');
    assert.equal(request.url, `https://searchapi.api.cloud.yandex.net${endpoint}`);
    assert.equal(request.body.folderId, 'folder-1');
    assert.equal(Object.hasOwn(request.body, 'method'), false);
  }
  assert.throws(() => wordstat.buildRequest({ method: 'getRegionsTree' }, ''), codeIs('MISSING_FIELD'));
});

test('Wordstat fingerprint and error/result envelopes preserve truth', () => {
  const a = wordstat.parseCommand(command('getTop', { phrase: 'x' }));
  const b = wordstat.parseCommand(command('getTop', { phrase: 'x' }));
  const c = wordstat.parseCommand(command('getTop', { phrase: 'y' }));
  assert.equal(wordstat.commandFingerprint(a), wordstat.commandFingerprint(b));
  assert.notEqual(wordstat.commandFingerprint(a), wordstat.commandFingerprint(c));
  assert.deepEqual(plain(wordstat.safeErrorPayload(403, 'raw', { code: 'DENIED', message: 'no access' })), {
    http_status: 403, code: 'DENIED', message: 'no access'
  });
  const envelope = wordstat.buildResultEnvelope({
    requestId: 'req-1', command: wordstat.parseCommand(command('getRegionsTree')), httpStatus: 200,
    result: { ok: true }, elapsedMs: 12, metadata: { run_id: 'run-1', request_executed: true, automatic_retry: false }
  });
  assert.equal(envelope.service, 'wordstat');
  assert.equal(envelope.request_executed, true);
  assert.equal(envelope.automatic_retry, false);
  assert.match(wordstat.formatResultEnvelope(envelope), /^WORDSTAT_RESULT_V1\n/);
});

test('Wordstat skipped envelope explicitly states no provider request and no automatic retry', () => {
  const envelope = wordstat.buildSkippedEnvelope({
    requestId: 'skip-1', command: wordstat.parseCommand(command('getRegionsTree')), reason: 'NO_CREDENTIALS'
  });
  assert.equal(envelope.status, 'SKIPPED');
  assert.equal(envelope.reason, 'NO_CREDENTIALS');
  assert.equal(envelope.http_status, 0);
  assert.equal(envelope.request_executed, false);
  assert.equal(envelope.automatic_retry, false);
  assert.equal(envelope.result.skipped, true);
});

// Policy, credentials and cost accounting.
test('Wordstat and Search policy defaults stay isolated', () => {
  const wp = policy.normalizeWordstatPolicy({});
  const sp = policy.normalizeSearchPolicy({});
  assert.equal(wp.autorun_enabled, false);
  assert.equal(wp.manual_enabled, true);
  assert.deepEqual(plain(wp.allowed_methods), ['getTop', 'getDynamics', 'getRegionsDistribution', 'getRegionsTree']);
  assert.equal(wp.method_cost_rub.getTop, 0.02);
  assert.deepEqual(plain(sp.allowed_methods), ['search']);
  assert.equal(sp.method_cost_rub.search, 0.488);
  assert.equal(sp.tariff_checked_at, '2026-08-19');
});

test('policy normalization filters methods and invalid numeric overrides safely', () => {
  const wp = policy.normalizeWordstatPolicy({ allowed_methods: ['getTop', 'unknown', 'getTop', 'getRegionsTree'] });
  assert.deepEqual(plain(wp.allowed_methods), ['getTop', 'getRegionsTree']);
  const sp = policy.normalizeSearchPolicy({ max_requests_per_run: 0, max_cost_rub_per_run: -1, method_cost_rub: { search: -7 } });
  assert.equal(sp.max_requests_per_run, 100);
  assert.equal(sp.max_cost_rub_per_run, 10);
  assert.equal(sp.method_cost_rub.search, 0.488);
});

test('policy denial reasons cover credential, channel, operation, request and cost gates', () => {
  const searchOn = policy.normalizeSearchPolicy({ autorun_enabled: true, max_requests_per_run: 2, max_cost_rub_per_run: 0.5 });
  assert.equal(policy.searchDecision({ policy: searchOn, channel: 'autorun', method: 'search', credentialState: 'MISSING' }).reason, 'NO_CREDENTIALS');
  assert.equal(policy.searchDecision({ policy: searchOn, channel: 'autorun', method: 'search', credentialState: 'NO_ACCESS' }).reason, 'CREDENTIAL_NO_ACCESS');
  assert.equal(policy.searchDecision({ policy: policy.normalizeSearchPolicy({ autorun_enabled: false }), channel: 'autorun', method: 'search', credentialState: 'PRESENT' }).reason, 'AUTORUN_DISABLED');
  assert.equal(policy.searchDecision({ policy: policy.normalizeSearchPolicy({ manual_enabled: false }), channel: 'manual', method: 'search', credentialState: 'PRESENT' }).reason, 'MANUAL_DISABLED');
  assert.equal(policy.wordstatDecision({ policy: policy.normalizeWordstatPolicy({ allowed_methods: ['getTop'] }), channel: 'manual', method: 'getDynamics', credentialState: 'PRESENT' }).reason, 'OPERATION_DISABLED');
  assert.equal(policy.searchDecision({ policy: searchOn, channel: 'autorun', method: 'search', credentialState: 'PRESENT', run: { requests_executed: 2 } }).reason, 'REQUEST_LIMIT');
  assert.equal(policy.searchDecision({ policy: searchOn, channel: 'autorun', method: 'search', credentialState: 'PRESENT', run: { estimated_cost_rub: 0.1 } }).reason, 'COST_LIMIT');
});

test('policy allows valid request with exact cost and rejects unknown service', () => {
  const allowed = policy.wordstatDecision({
    policy: policy.normalizeWordstatPolicy({ autorun_enabled: true, max_cost_rub_per_run: 5 }),
    channel: 'autorun', method: 'getTop', credentialState: 'PRESENT', run: {}
  });
  assert.equal(allowed.allow, true);
  assert.equal(allowed.reason, 'ALLOW');
  assert.equal(allowed.estimated_cost_rub, 0.02);
  assert.equal(policy.decisionForService('images', {}).reason, 'SERVICE_NOT_AVAILABLE');
  assert.throws(() => policy.normalizePolicyForService('images', {}), codeIs('UNKNOWN_SERVICE'));
});

test('cost ledger normalizes unsafe values and records attempts/executions/skips independently', () => {
  assert.deepEqual(plain(ledger.normalizeTotals({ requests_attempted: -2, requests_executed: 'bad', requests_skipped: -1, estimated_cost_rub: -5 })), {
    requests_attempted: 0, requests_executed: 0, requests_skipped: 0, estimated_cost_rub: 0
  });
  let totals = ledger.noteAttempt({});
  totals = ledger.noteExecuted(totals, 0.488);
  totals = ledger.noteSkipped(totals);
  assert.deepEqual(plain(totals), { requests_attempted: 1, requests_executed: 1, requests_skipped: 1, estimated_cost_rub: 0.488 });
  assert.equal(ledger.noteExecuted({}, 0.1234567).estimated_cost_rub, 0.123457);
  assert.equal(ledger.noteExecuted({ estimated_cost_rub: 1 }, -100).estimated_cost_rub, 1);
});

// Autorun lifecycle, prefix counters and restart safety.
test('Autorun ID and report-prefix normalization are deterministic', () => {
  assert.deepEqual(plain(autorun.normalizeIdList([' a ', '', 'a', 'b'])), ['a', 'b']);
  assert.throws(() => autorun.normalizePrefixRecord({ enabled: true, text: '   ' }), codeIs('EMPTY_REPORT_PREFIX'));
  const record = autorun.normalizePrefixRecord({ enabled: true, text: 'PREFIX', interval: 3, delivered_count: 2, last_applied_at_count: 0 });
  assert.equal(autorun.reportPrefixIsDue(record), true);
  assert.deepEqual(plain(autorun.applyReportPrefix('RESULT', record)), { text: 'PREFIX\n\nRESULT', applied: true });
});

test('report-prefix confirmation is idempotent for a delivery id', () => {
  const base = autorun.normalizePrefixRecord({ enabled: true, text: 'P', interval: 1, delivered_count: 0 });
  const first = autorun.noteConfirmedPrefix(base, true, 'delivery-1');
  const again = autorun.noteConfirmedPrefix(first, true, 'delivery-1');
  assert.equal(first.delivered_count, 1);
  assert.equal(again.delivered_count, 1);
  assert.equal(again.last_applied_at_count, 1);
});

test('Autorun status helpers enforce Manual safety and pause semantics', () => {
  for (const status of ['starting', 'waiting_command', 'requesting', 'delivering']) {
    assert.equal(autorun.isBusyStatus(status), true);
    assert.equal(autorun.canEnableManualMode(status), false);
  }
  assert.equal(autorun.canEnableManualMode('paused'), true);
  assert.equal(autorun.canEnableManualMode('stopped'), true);
  assert.equal(autorun.canEnableManualMode('error'), true);
  assert.equal(autorun.pauseDecision('waiting_command'), 'immediate');
  assert.equal(autorun.pauseDecision('requesting'), 'deferred');
  assert.equal(autorun.pauseDecision('paused'), 'already_paused');
  assert.equal(autorun.pauseDecision('stopped'), 'not_active');
});

test('Autorun start commit is single-shot and confirmation chooses watch/pause/finish', () => {
  const run = { status: 'starting', start_delivery: { phase: 'none' } };
  const committed = autorun.commitStart(run, { baselineUserTurnIds: ['u1', 'u1', 'u2'], actorId: 'actor' });
  assert.equal(committed.start_delivery.phase, 'committed');
  assert.deepEqual(plain(committed.start_delivery.baseline_user_turn_ids), ['u1', 'u2']);
  assert.strictEqual(autorun.commitStart(committed, { baselineUserTurnIds: ['x'] }), committed);
  const watching = autorun.afterConfirmedStart(committed, ['a1']);
  assert.equal(watching.status, 'waiting_command');
  assert.deepEqual(plain(watching.assistant_baseline_ids), ['a1']);
  assert.match(watching.watch_id, /^watch-/);
  assert.equal(autorun.afterConfirmedStart({ status: 'starting', pause_requested: true, start_delivery: {} }).status, 'paused');
  assert.equal(autorun.afterConfirmedStart({ status: 'starting', finish_requested: true, start_delivery: {} }).status, 'stopped');
});

test('Autorun delivery claim/commit keeps one delivery identity and wrong id cannot commit', () => {
  const claimed = autorun.claimDelivery({ status: 'requesting' }, {
    deliveryId: 'd1', requestId: 'r1', outgoingText: 'text', outgoingHash: 'hash', reportPrefixApplied: true
  });
  assert.equal(claimed.status, 'delivering');
  assert.equal(claimed.delivery.phase, 'claimed');
  assert.strictEqual(autorun.commitDelivery(claimed, { deliveryId: 'wrong' }), claimed);
  const committed = autorun.commitDelivery(claimed, { deliveryId: 'd1', baselineUserTurnIds: ['u1'], actorId: 'actor' });
  assert.equal(committed.delivery.phase, 'committed');
  assert.deepEqual(plain(committed.delivery.baseline_user_turn_ids), ['u1']);
  assert.equal(committed.delivery.commit_actor_id, 'actor');
});

test('Autorun restart maps stable persisted states to deterministic recovery actions', () => {
  assert.equal(autorun.recoveryDecision({ status: 'waiting_command' }).type, 'watch');
  assert.equal(autorun.recoveryDecision({ status: 'paused' }).type, 'paused');
  assert.equal(autorun.recoveryDecision({ status: 'starting', start_delivery: { phase: 'none' } }).type, 'dispatch_start');
  assert.equal(autorun.recoveryDecision({ status: 'starting', start_delivery: { phase: 'committed' } }).type, 'reconcile_start');
  assert.equal(autorun.recoveryDecision({ status: 'delivering', delivery: { phase: 'claimed' } }).type, 'deliver_claimed');
  assert.equal(autorun.recoveryDecision({ status: 'delivering', delivery: { phase: 'committed' } }).type, 'reconcile_delivery');
});

test('Autorun restart during provider request with another worker session becomes UNKNOWN without retry', () => {
  const unknown = autorun.recoveryDecision({ status: 'requesting', request_worker_session_id: 'old' }, 'new');
  assert.equal(unknown.type, 'unsafe_request_outcome');
  assert.equal(unknown.code, 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY');
  assert.equal(autorun.recoveryDecision({ status: 'requesting', request_worker_session_id: 'same' }, 'same').type, 'request_in_progress');
});

test('Autorun unknown persisted phases/statuses fail closed', () => {
  assert.deepEqual(plain(autorun.recoveryDecision({ status: 'starting', start_delivery: { phase: 'mystery' } })), { type: 'blocked', code: 'UNKNOWN_START_PHASE' });
  assert.deepEqual(plain(autorun.recoveryDecision({ status: 'delivering', delivery: { phase: 'mystery' } })), { type: 'blocked', code: 'UNKNOWN_DELIVERY_PHASE' });
  assert.deepEqual(plain(autorun.recoveryDecision({ status: 'mystery' })), { type: 'blocked', code: 'UNKNOWN_RUN_STATUS' });
});

test('confirmed delivery increments sequence once and applies deferred pause/finish only afterwards', () => {
  const next = autorun.afterConfirmedDelivery({ status: 'delivering', sequence: 4 });
  assert.equal(next.sequence, 5);
  assert.equal(next.status, 'waiting_command');
  const paused = autorun.afterConfirmedDelivery({ status: 'delivering', sequence: 1, pause_requested: true });
  assert.equal(paused.sequence, 2);
  assert.equal(paused.status, 'paused');
  const stopped = autorun.afterConfirmedDelivery({ status: 'delivering', sequence: 1, finish_requested: true });
  assert.equal(stopped.sequence, 2);
  assert.equal(stopped.status, 'stopped');
});

test('Manual control primitives remain Bridge-owned and separate from native Copy', () => {
  assert.equal(manual.ACTION_LABEL, 'Яндекс');
  assert.equal(manual.ACTION_ATTR, 'data-ymb-manual-action');
  assert.equal(manual.BLOCK_ATTR, 'data-ymb-block-id');
  assert.match(manual.makeId('block'), /^block-/);
});
