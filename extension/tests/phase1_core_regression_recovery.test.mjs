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
]) {
  vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), ctx, { filename: file });
}

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

function plain(value) {
  return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
}
function codeIs(code) {
  return (error) => error?.code === code;
}
function command(method, extra = {}) {
  return `WORDSTAT_API_V1 ${JSON.stringify({ method, ...extra })}`;
}

// Conversation identity / ownership primitives.
test('conversation identity accepts only ChatGPT origins', () => {
  assert.equal(identity.normalizeOrigin('https://chatgpt.com/c/x'), 'https://chatgpt.com');
  assert.equal(identity.normalizeOrigin('https://chat.openai.com/c/x'), 'https://chat.openai.com');
  assert.equal(identity.normalizeOrigin('https://evil.example/c/x'), '');
  assert.equal(identity.normalizeOrigin('not a url'), '');
});

test('conversation identity confirms UUID conversation from chatgpt.com path', () => {
  const result = identity.identityFromUrl(`https://chatgpt.com/c/${CID}?x=1#y`);
  assert.equal(result.status, 'confirmed');
  assert.equal(result.origin, 'https://chatgpt.com');
  assert.equal(result.conversation_id, CID);
  assert.equal(result.conversation_key, KEY);
});

test('conversation identity lowercases UUID and supports legacy chat.openai.com', () => {
  const upper = CID.toUpperCase();
  const result = identity.identityFromUrl(`https://chat.openai.com/c/${upper}`);
  assert.equal(result.status, 'confirmed');
  assert.equal(result.conversation_id, CID);
  assert.equal(result.conversation_key, `https://chat.openai.com|${CID}`);
});

test('conversation identity fails closed for missing or malformed conversation id', () => {
  assert.equal(identity.identityFromUrl('https://chatgpt.com/').status, 'unconfirmed');
  assert.equal(identity.identityFromUrl('https://chatgpt.com/c/not-a-uuid').conversation_key, '');
  assert.equal(identity.identityFromUrl('%%%').status, 'unavailable');
});

test('conversation key normalization rejects foreign origins and malformed ids', () => {
  assert.equal(identity.normalizeConversationKey(KEY), KEY);
  assert.equal(identity.normalizeConversationKey(`https://evil.example|${CID}`), '');
  assert.equal(identity.normalizeConversationKey('https://chatgpt.com|broken'), '');
  assert.throws(() => identity.normalizeConversationKey('broken', { required: true }), codeIs('CONVERSATION_KEY_INVALID'));
});

test('sameConversation compares normalized origin plus UUID', () => {
  assert.equal(identity.sameConversation(KEY, `https://chatgpt.com|${CID.toUpperCase()}`), true);
  assert.equal(identity.sameConversation(KEY, `https://chat.openai.com|${CID}`), false);
  assert.equal(identity.sameConversation('', ''), false);
});

// Service registry / block discovery / run context.
test('service registry exposes exactly Wordstat and synchronous Search prefixes', () => {
  assert.deepEqual(plain(registry.DEFINITIONS), [
    { service: 'wordstat', prefix: 'WORDSTAT_API_V1' },
    { service: 'search', prefix: 'SEARCH_API_V1' }
  ]);
});

test('service registry detects Wordstat/Search with surrounding whitespace and NBSP', () => {
  assert.equal(registry.detect('  WORDSTAT_API_V1 {}')?.service, 'wordstat');
  assert.equal(registry.detect('\u00a0SEARCH_API_V1 {}')?.service, 'search');
  assert.equal(registry.detect('OTHER_API_V1 {}'), null);
});

test('service registry known-service and lookup helpers fail closed', () => {
  assert.equal(registry.isKnownService('wordstat'), true);
  assert.equal(registry.isKnownService('search'), true);
  assert.equal(registry.isKnownService('images'), false);
  assert.equal(registry.definitionForService('search')?.prefix, 'SEARCH_API_V1');
  assert.equal(registry.definitionForService('images'), null);
});

test('block discovery preserves command source order across services', () => {
  const found = discovery.discover(`before SEARCH_API_V1 {"method":"search","queryText":"one"}\nmid WORDSTAT_API_V1 {"method":"getRegionsTree"}`);
  assert.equal(found.length, 2);
  assert.deepEqual(plain(found.map((item) => [item.service, item.ok])), [['search', true], ['wordstat', true]]);
  assert.ok(found[0].index < found[1].index);
});

test('block discovery handles braces and escapes inside JSON strings', () => {
  const found = discovery.discover('SEARCH_API_V1 {"method":"search","queryText":"a } \\"quoted\\" value"}');
  assert.equal(found.length, 1);
  assert.equal(found[0].ok, true);
  assert.equal(found[0].raw.queryText, 'a } "quoted" value');
});

test('block discovery reports missing and unterminated JSON without inventing a command', () => {
  assert.equal(discovery.discover('SEARCH_API_V1 no-json')[0].code, 'MISSING_JSON');
  assert.equal(discovery.discover('WORDSTAT_API_V1 {"method":"getTop"')[0].code, 'UNTERMINATED_JSON');
});

test('block text fingerprint is deterministic and content-sensitive', () => {
  assert.equal(discovery.textFingerprint('abc'), discovery.textFingerprint('abc'));
  assert.notEqual(discovery.textFingerprint('abc'), discovery.textFingerprint('abd'));
  assert.match(discovery.textFingerprint('abc'), /^[0-9a-f]{8}$/);
});

test('run context normalizes selected service and rejects unknown or missing required service', () => {
  assert.equal(runContext.normalizeActiveService(' Search ', registry), 'search');
  assert.equal(runContext.normalizeActiveService('', registry), '');
  assert.throws(() => runContext.normalizeActiveService('', registry, { required: true }), codeIs('ACTIVE_SERVICE_MISSING'));
  assert.throws(() => runContext.normalizeActiveService('images', registry), codeIs('UNKNOWN_SERVICE'));
});

test('run context rejects wrong-service execution', () => {
  assert.equal(runContext.assertServiceMatch('search', 'search'), true);
  assert.throws(() => runContext.assertServiceMatch('search', 'wordstat'), codeIs('SERVICE_NOT_ACTIVE'));
  assert.deepEqual(plain(runContext.makeRunIdentity({ activeService: 'wordstat', registry })), { active_service: 'wordstat' });
});

// Credential boundaries.
test('credential registry requires both local API key and folder id', () => {
  assert.equal(credentials.wordstatCapability({ apiKey: 'k', folderId: 'f' }).state, 'PRESENT');
  assert.equal(credentials.searchCapability({ apiKey: 'k', folderId: '' }).state, 'MISSING');
  assert.equal(credentials.searchCapability({ apiKey: '', folderId: 'f' }).state, 'MISSING');
});

test('credential registry reports unknown service as NO_ACCESS without exposing credentials', () => {
  const result = credentials.capabilityForService('images', { apiKey: 'secret', folderId: 'folder' });
  assert.deepEqual(plain(result), { state: 'NO_ACCESS', has_api_key: false, has_folder_id: false });
});

// Wordstat protocol matrix.
test('Wordstat recognizes only its protocol marker', () => {
  assert.equal(wordstat.isCommandText(' WORDSTAT_API_V1 {}'), true);
  assert.equal(wordstat.isCommandText('SEARCH_API_V1 {}'), false);
});

test('Wordstat getRegionsTree normalizes to the no-argument operation', () => {
  assert.deepEqual(plain(wordstat.parseCommand(command('getRegionsTree'))), { method: 'getRegionsTree' });
});

test('Wordstat getTop fills stable defaults', () => {
  const parsed = wordstat.parseCommand(command('getTop', { phrase: 'купить ноутбук' }));
  assert.equal(parsed.method, 'getTop');
  assert.equal(parsed.phrase, 'купить ноутбук');
  assert.deepEqual(plain(parsed.regions), ['225']);
  assert.deepEqual(plain(parsed.devices), ['DEVICE_ALL']);
  assert.equal(parsed.numPhrases, 100);
});

test('Wordstat getTop accepts numPhrases boundaries', () => {
  assert.equal(wordstat.parseCommand(command('getTop', { phrase: 'x', numPhrases: 1 })).numPhrases, 1);
  assert.equal(wordstat.parseCommand(command('getTop', { phrase: 'x', numPhrases: 2000 })).numPhrases, 2000);
});

test('Wordstat getTop rejects out-of-range phrase count', () => {
  assert.throws(() => wordstat.parseCommand(command('getTop', { phrase: 'x', numPhrases: 0 })), codeIs('INVALID_NUM_PHRASES'));
  assert.throws(() => wordstat.parseCommand(command('getTop', { phrase: 'x', numPhrases: 2001 })), codeIs('INVALID_NUM_PHRASES'));
});

test('Wordstat rejects empty or oversized phrases', () => {
  assert.throws(() => wordstat.parseCommand(command('getTop', { phrase: '' })), codeIs('MISSING_FIELD'));
  assert.throws(() => wordstat.parseCommand(command('getTop', { phrase: 'x'.repeat(401) })), codeIs('FIELD_TOO_LONG'));
});

test('Wordstat validates devices and region list size', () => {
  assert.throws(() => wordstat.parseCommand(command('getTop', { phrase: 'x', devices: ['WATCH'] })), codeIs('INVALID_DEVICE'));
  assert.throws(() => wordstat.parseCommand(command('getTop', { phrase: 'x', regions: Array.from({ length: 101 }, (_, i) => String(i + 1)) })), codeIs('TOO_MANY_REGIONS'));
});

test('Wordstat getDynamics validates period and RFC3339 dates', () => {
  const parsed = wordstat.parseCommand(command('getDynamics', { phrase: 'x', fromDate: '2026-08-01T00:00:00Z', toDate: '2026-08-20T00:00:00Z', period: 'PERIOD_DAILY' }));
  assert.equal(parsed.period, 'PERIOD_DAILY');
  assert.throws(() => wordstat.parseCommand(command('getDynamics', { phrase: 'x', fromDate: 'bad', toDate: '2026-08-20T00:00:00Z' })), codeIs('INVALID_DATE'));
  assert.throws(() => wordstat.parseCommand(command('getDynamics', { phrase: 'x', fromDate: '2026-08-01T00:00:00Z', toDate: '2026-08-20T00:00:00Z', period: 'YEARLY' })), codeIs('INVALID_PERIOD'));
});

test('Wordstat getRegionsDistribution applies region/device defaults', () => {
  const parsed = wordstat.parseCommand(command('getRegionsDistribution', { phrase: 'x' }));
  assert.deepEqual(plain(parsed.regions), ['225']);
  assert.deepEqual(plain(parsed.devices), ['DEVICE_ALL']);
  assert.equal(parsed.regionLevel, 'REGION_LEVEL_ALL');
});

test('Wordstat getRegionsDistribution rejects unknown region level', () => {
  assert.throws(() => wordstat.parseCommand(command('getRegionsDistribution', { phrase: 'x', regionLevel: 'COUNTRIES' })), codeIs('INVALID_REGION_LEVEL'));
});

test('Wordstat buildRequest maps every operation to the official API host and path', () => {
  const cases = [
    ['getTop', { phrase: 'x' }, '/v2/wordstat/topRequests'],
    ['getDynamics', { phrase: 'x', fromDate: '2026-08-01T00:00:00Z', toDate: '2026-08-20T00:00:00Z' }, '/v2/wordstat/dynamics'],
    ['getRegionsDistribution', { phrase: 'x' }, '/v2/wordstat/regions'],
    ['getRegionsTree', {}, '/v2/wordstat/getRegionsTree']
  ];
  for (const [method, extra, endpoint] of cases) {
    const request = wordstat.buildRequest(wordstat.normalizeCommand({ method, ...extra }), 'folder-1');
    assert.equal(request.url, `https://searchapi.api.cloud.yandex.net${endpoint}`);
    assert.equal(request.body.folderId, 'folder-1');
  }
});

test('Wordstat command fingerprint is stable for normalized command and changes with input', () => {
  const a = wordstat.parseCommand(command('getTop', { phrase: 'x' }));
  const b = wordstat.parseCommand(command('getTop', { phrase: 'x' }));
  const c = wordstat.parseCommand(command('getTop', { phrase: 'y' }));
  assert.equal(wordstat.commandFingerprint(a), wordstat.commandFingerprint(b));
  assert.notEqual(wordstat.commandFingerprint(a), wordstat.commandFingerprint(c));
});

test('Wordstat HTTP error payload prefers structured provider fields and truncates safely', () => {
  const structured = wordstat.safeErrorPayload(403, 'raw', { code: 'DENIED', message: 'no access' });
  assert.deepEqual(plain(structured), { http_status: 403, code: 'DENIED', message: 'no access' });
  const fallback = wordstat.safeErrorPayload(500, 'plain failure', null);
  assert.equal(fallback.code, 'YANDEX_API_ERROR');
  assert.equal(fallback.message, 'plain failure');
});

test('Wordstat result envelope exposes truth fields without hiding request execution metadata', () => {
  const parsed = wordstat.parseCommand(command('getRegionsTree'));
  const envelope = wordstat.buildResultEnvelope({
    requestId: 'req-1', command: parsed, httpStatus: 200, result: { ok: true }, elapsedMs: 12,
    metadata: { run_id: 'run-1', request_executed: true, automatic_retry: false }
  });
  assert.equal(envelope.bridge, 'yandex-marketing-bridge');
  assert.equal(envelope.version, '0.1.1');
  assert.equal(envelope.service, 'wordstat');
  assert.equal(envelope.operation, 'getRegionsTree');
  assert.equal(envelope.request_executed, true);
  assert.equal(envelope.automatic_retry, false);
  assert.match(wordstat.formatResultEnvelope(envelope), /^WORDSTAT_RESULT_V1\n/);
});

test('Wordstat skipped envelope states zero request execution and zero retry by default', () => {
  const parsed = wordstat.parseCommand(command('getRegionsTree'));
  const envelope = wordstat.buildSkippedEnvelope({ requestId: 'skip-1', command: parsed, reason: 'NO_CREDENTIALS' });
  assert.equal(envelope.status, 'SKIPPED');
  assert.equal(envelope.reason, 'NO_CREDENTIALS');
  assert.equal(envelope.http_status, 0);
  assert.equal(envelope.request_executed, false);
  assert.equal(envelope.automatic_retry, false);
  assert.equal(envelope.result.skipped, true);
});

// Policy and cost guard matrix.
test('Wordstat policy defaults preserve all four methods and conservative disabled Autorun', () => {
  const p = policy.normalizeWordstatPolicy({});
  assert.equal(p.autorun_enabled, false);
  assert.equal(p.manual_enabled, true);
  assert.deepEqual(plain(p.allowed_methods), ['getTop', 'getDynamics', 'getRegionsDistribution', 'getRegionsTree']);
  assert.deepEqual(plain(p.method_cost_rub), { getTop: 0.02, getDynamics: 0.02, getRegionsDistribution: 0.05, getRegionsTree: 0 });
});

test('Search policy defaults remain separate with one synchronous method at 0.488 RUB guard', () => {
  const p = policy.normalizeSearchPolicy({});
  assert.deepEqual(plain(p.allowed_methods), ['search']);
  assert.equal(p.method_cost_rub.search, 0.488);
  assert.equal(p.tariff_checked_at, '2026-08-19');
});

test('policy normalization removes unknown methods and duplicate methods', () => {
  const p = policy.normalizeWordstatPolicy({ allowed_methods: ['getTop', 'unknown', 'getTop', 'getRegionsTree'] });
  assert.deepEqual(plain(p.allowed_methods), ['getTop', 'getRegionsTree']);
});

test('policy normalization rejects invalid numeric overrides by falling back safely', () => {
  const p = policy.normalizeSearchPolicy({ max_requests_per_run: 0, max_cost_rub_per_run: -1, method_cost_rub: { search: -7 } });
  assert.equal(p.max_requests_per_run, 100);
  assert.equal(p.max_cost_rub_per_run, 10);
  assert.equal(p.method_cost_rub.search, 0.488);
});

test('policy denies missing credentials before channel/method limits', () => {
  const p = policy.normalizeSearchPolicy({ autorun_enabled: true });
  assert.equal(policy.searchDecision({ policy: p, channel: 'autorun', method: 'search', credentialState: 'MISSING' }).reason, 'NO_CREDENTIALS');
  assert.equal(policy.searchDecision({ policy: p, channel: 'autorun', method: 'search', credentialState: 'NO_ACCESS' }).reason, 'CREDENTIAL_NO_ACCESS');
});

test('policy independently gates Autorun and Manual channels', () => {
  const offAuto = policy.normalizeSearchPolicy({ autorun_enabled: false, manual_enabled: true });
  assert.equal(policy.searchDecision({ policy: offAuto, channel: 'autorun', method: 'search', credentialState: 'PRESENT' }).reason, 'AUTORUN_DISABLED');
  const offManual = policy.normalizeSearchPolicy({ autorun_enabled: true, manual_enabled: false });
  assert.equal(policy.searchDecision({ policy: offManual, channel: 'manual', method: 'search', credentialState: 'PRESENT' }).reason, 'MANUAL_DISABLED');
});

test('policy blocks disabled operations before provider execution', () => {
  const p = policy.normalizeWordstatPolicy({ allowed_methods: ['getTop'] });
  assert.equal(policy.wordstatDecision({ policy: p, channel: 'manual', method: 'getDynamics', credentialState: 'PRESENT' }).reason, 'OPERATION_DISABLED');
});

test('policy enforces request count at the current-run boundary', () => {
  const p = policy.normalizeSearchPolicy({ autorun_enabled: true, max_requests_per_run: 2 });
  assert.equal(policy.searchDecision({ policy: p, channel: 'autorun', method: 'search', credentialState: 'PRESENT', run: { requests_executed: 2 } }).reason, 'REQUEST_LIMIT');
});

test('policy enforces estimated run cost before a provider request starts', () => {
  const p = policy.normalizeSearchPolicy({ autorun_enabled: true, max_cost_rub_per_run: 0.5 });
  const result = policy.searchDecision({ policy: p, channel: 'autorun', method: 'search', credentialState: 'PRESENT', run: { estimated_cost_rub: 0.1 } });
  assert.equal(result.allow, false);
  assert.equal(result.reason, 'COST_LIMIT');
  assert.equal(result.estimated_cost_rub, 0.488);
});

test('policy allows a valid request and returns its exact estimated cost', () => {
  const p = policy.normalizeWordstatPolicy({ autorun_enabled: true, max_cost_rub_per_run: 5 });
  const result = policy.wordstatDecision({ policy: p, channel: 'autorun', method: 'getTop', credentialState: 'PRESENT', run: {} });
  assert.equal(result.allow, true);
  assert.equal(result.reason, 'ALLOW');
  assert.equal(result.estimated_cost_rub, 0.02);
});

test('policy unknown service fails closed', () => {
  const result = policy.decisionForService('images', { channel: 'manual', method: 'image', credentialState: 'PRESENT' });
  assert.equal(result.allow, false);
  assert.equal(result.reason, 'SERVICE_NOT_AVAILABLE');
  assert.throws(() => policy.normalizePolicyForService('images', {}), codeIs('UNKNOWN_SERVICE'));
});

test('cost ledger normalizes negative and non-finite totals to zero', () => {
  assert.deepEqual(plain(ledger.normalizeTotals({ requests_attempted: -2, requests_executed: 'bad', requests_skipped: -1, estimated_cost_rub: -5 })), {
    requests_attempted: 0, requests_executed: 0, requests_skipped: 0, estimated_cost_rub: 0
  });
});

test('cost ledger records attempts, executions and skips independently', () => {
  let totals = ledger.normalizeTotals({});
  totals = ledger.noteAttempt(totals);
  totals = ledger.noteExecuted(totals, 0.488);
  totals = ledger.noteSkipped(totals);
  assert.deepEqual(plain(totals), { requests_attempted: 1, requests_executed: 1, requests_skipped: 1, estimated_cost_rub: 0.488 });
});

test('cost ledger rounds accumulated estimated cost to six decimals and never subtracts negative cost', () => {
  let totals = ledger.noteExecuted({}, 0.1234567);
  assert.equal(totals.estimated_cost_rub, 0.123457);
  totals = ledger.noteExecuted(totals, -100);
  assert.equal(totals.estimated_cost_rub, 0.123457);
});

// Autorun lifecycle / restart safety.
test('Autorun id normalization trims, deduplicates and removes empty ids', () => {
  assert.deepEqual(plain(autorun.normalizeIdList([' a ', '', 'a', 'b'])), ['a', 'b']);
});

test('enabled empty report prefix is rejected and disabled empty prefix is allowed', () => {
  assert.throws(() => autorun.normalizePrefixRecord({ enabled: true, text: '   ' }), codeIs('EMPTY_REPORT_PREFIX'));
  assert.equal(autorun.normalizePrefixRecord({ enabled: false, text: '' }).enabled, false);
});

test('report prefix schedule and application are deterministic', () => {
  const record = autorun.normalizePrefixRecord({ enabled: true, text: 'PREFIX', interval: 3, delivered_count: 2, last_applied_at_count: 0 });
  assert.equal(autorun.reportPrefixIsDue(record), true);
  assert.deepEqual(plain(autorun.applyReportPrefix('RESULT', record)), { text: 'PREFIX\n\nRESULT', applied: true });
});

test('report prefix confirmation is idempotent for the same delivery id', () => {
  const base = autorun.normalizePrefixRecord({ enabled: true, text: 'P', interval: 1, delivered_count: 0 });
  const first = autorun.noteConfirmedPrefix(base, true, 'delivery-1');
  const again = autorun.noteConfirmedPrefix(first, true, 'delivery-1');
  assert.equal(first.delivered_count, 1);
  assert.equal(again.delivered_count, 1);
  assert.equal(again.last_applied_at_count, 1);
});

test('Autorun status helpers keep Manual disabled during busy states and allow it on pause/terminal', () => {
  for (const status of ['starting', 'waiting_command', 'requesting', 'delivering']) {
    assert.equal(autorun.isBusyStatus(status), true);
    assert.equal(autorun.canEnableManualMode(status), false);
  }
  assert.equal(autorun.canEnableManualMode('paused'), true);
  assert.equal(autorun.canEnableManualMode('stopped'), true);
  assert.equal(autorun.canEnableManualMode('error'), true);
  assert.equal(autorun.isTerminalStatus('stopped'), true);
  assert.equal(autorun.isTerminalStatus('error'), true);
});

test('Autorun pause decision distinguishes immediate, deferred and inactive states', () => {
  assert.equal(autorun.pauseDecision('waiting_command'), 'immediate');
  assert.equal(autorun.pauseDecision('starting'), 'deferred');
  assert.equal(autorun.pauseDecision('requesting'), 'deferred');
  assert.equal(autorun.pauseDecision('delivering'), 'deferred');
  assert.equal(autorun.pauseDecision('paused'), 'already_paused');
  assert.equal(autorun.pauseDecision('stopped'), 'not_active');
});

test('Autorun start commit is single-shot and records baseline plus actor', () => {
  const run = { status: 'starting', start_delivery: { phase: 'none' } };
  const committed = autorun.commitStart(run, { baselineUserTurnIds: ['u1', 'u1', 'u2'], actorId: 'actor' });
  assert.equal(committed.start_delivery.phase, 'committed');
  assert.deepEqual(plain(committed.start_delivery.baseline_user_turn_ids), ['u1', 'u2']);
  assert.equal(committed.start_delivery.commit_actor_id, 'actor');
  assert.strictEqual(autorun.commitStart(committed, { baselineUserTurnIds: ['x'] }), committed);
});

test('confirmed Autorun start normally begins command watching', () => {
  const run = { status: 'starting', start_delivery: { phase: 'committed' }, sequence: 0 };
  const next = autorun.afterConfirmedStart(run, ['a1']);
  assert.equal(next.status, 'waiting_command');
  assert.equal(next.start_delivery.phase, 'confirmed');
  assert.deepEqual(plain(next.assistant_baseline_ids), ['a1']);
  assert.match(next.watch_id, /^watch-/);
});

test('deferred pause or finish requested during start is applied after confirmation', () => {
  assert.equal(autorun.afterConfirmedStart({ status: 'starting', pause_requested: true, start_delivery: {} }).status, 'paused');
  assert.equal(autorun.afterConfirmedStart({ status: 'starting', finish_requested: true, start_delivery: {} }).status, 'stopped');
});

test('Autorun delivery claim and commit preserve one delivery identity', () => {
  const claimed = autorun.claimDelivery({ status: 'requesting' }, { deliveryId: 'd1', requestId: 'r1', outgoingText: 'text', outgoingHash: 'hash', reportPrefixApplied: true });
  assert.equal(claimed.status, 'delivering');
  assert.equal(claimed.delivery.phase, 'claimed');
  const committed = autorun.commitDelivery(claimed, { deliveryId: 'd1', baselineUserTurnIds: ['u1'], actorId: 'actor' });
  assert.equal(committed.delivery.phase, 'committed');
  assert.deepEqual(plain(committed.delivery.baseline_user_turn_ids), ['u1']);
  assert.equal(committed.delivery.commit_actor_id, 'actor');
});

test('Autorun wrong delivery id cannot commit another delivery', () => {
  const claimed = autorun.claimDelivery({ status: 'requesting' }, { deliveryId: 'd1' });
  assert.strictEqual(autorun.commitDelivery(claimed, { deliveryId: 'wrong' }), claimed);
});

test('Autorun restart recovery maps stable states to deterministic actions', () => {
  assert.equal(autorun.recoveryDecision({ status: 'waiting_command' }).type, 'watch');
  assert.equal(autorun.recoveryDecision({ status: 'paused' }).type, 'paused');
  assert.equal(autorun.recoveryDecision({ status: 'starting', start_delivery: { phase: 'none' } }).type, 'dispatch_start');
  assert.equal(autorun.recoveryDecision({ status: 'starting', start_delivery: { phase: 'committed' } }).type, 'reconcile_start');
  assert.equal(autorun.recoveryDecision({ status: 'delivering', delivery: { phase: 'claimed' } }).type, 'deliver_claimed');
  assert.equal(autorun.recoveryDecision({ status: 'delivering', delivery: { phase: 'committed' } }).type, 'reconcile_delivery');
});

test('Autorun restart during provider request with another worker session is UNKNOWN and never auto-retried', () => {
  const decision = autorun.recoveryDecision({ status: 'requesting', request_worker_session_id: 'old' }, 'new');
  assert.equal(decision.type, 'unsafe_request_outcome');
  assert.equal(decision.code, 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY');
  assert.equal(autorun.recoveryDecision({ status: 'requesting', request_worker_session_id: 'same' }, 'same').type, 'request_in_progress');
});

test('Autorun unknown persisted states fail closed instead of guessing recovery', () => {
  assert.deepEqual(plain(autorun.recoveryDecision({ status: 'starting', start_delivery: { phase: 'mystery' } })), { type: 'blocked', code: 'UNKNOWN_START_PHASE' });
  assert.deepEqual(plain(autorun.recoveryDecision({ status: 'delivering', delivery: { phase: 'mystery' } })), { type: 'blocked', code: 'UNKNOWN_DELIVERY_PHASE' });
  assert.deepEqual(plain(autorun.recoveryDecision({ status: 'mystery' })), { type: 'blocked', code: 'UNKNOWN_RUN_STATUS' });
});

test('confirmed delivery increments sequence once and returns to watching', () => {
  const next = autorun.afterConfirmedDelivery({ status: 'delivering', sequence: 4 });
  assert.equal(next.sequence, 5);
  assert.equal(next.status, 'waiting_command');
});

test('deferred pause or finish requested during delivery is applied only after confirmation', () => {
  const paused = autorun.afterConfirmedDelivery({ status: 'delivering', sequence: 1, pause_requested: true });
  assert.equal(paused.sequence, 2);
  assert.equal(paused.status, 'paused');
  const stopped = autorun.afterConfirmedDelivery({ status: 'delivering', sequence: 1, finish_requested: true });
  assert.equal(stopped.sequence, 2);
  assert.equal(stopped.status, 'stopped');
});

test('Manual control constants keep the Bridge-owned Яндекс action separate from native Copy', () => {
  assert.equal(manual.ACTION_LABEL, 'Яндекс');
  assert.equal(manual.ACTION_ATTR, 'data-ymb-manual-action');
  assert.equal(manual.BLOCK_ATTR, 'data-ymb-block-id');
  assert.match(manual.makeId('block'), /^block-/);
});
