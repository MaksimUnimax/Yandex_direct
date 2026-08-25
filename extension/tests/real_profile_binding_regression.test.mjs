import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const identitySource = fs.readFileSync(path.join(root, 'shared/conversation_identity.js'), 'utf8');
const contentSource = fs.readFileSync(path.join(root, 'content_script.js'), 'utf8');
const bootstrapSource = fs.readFileSync(path.join(root, 'popup_context_bootstrap.js'), 'utf8');
const popupSource = fs.readFileSync(path.join(root, 'popup.js'), 'utf8');

const REAL_PROFILE_ID = '6a82924e-5ed0-83eb-84a2-851ddad40c88';
const REAL_PROFILE_URL = `https://chatgpt.com/c/${REAL_PROFILE_ID}`;
const REAL_PROFILE_KEY = `https://chatgpt.com|${REAL_PROFILE_ID}`;

function identityApi() {
  const context = vm.createContext({ URL, console });
  context.globalThis = context;
  vm.runInContext(identitySource, context, { filename: 'conversation_identity.js' });
  return context.BB2ConversationIdentity;
}

function manualHandlerSource() {
  const start = popupSource.indexOf('$("manualMode").addEventListener("change"');
  assert.notEqual(start, -1, 'Manual change handler must exist');
  const end = popupSource.indexOf('\n  for (const [id, key]', start);
  assert.notEqual(end, -1, 'Manual change handler end must be locatable');
  return popupSource.slice(start, end);
}

test('factual owner real-profile ChatGPT conversation id is confirmed without RFC UUID-version filtering', () => {
  const identity = identityApi().identityFromUrl(REAL_PROFILE_URL);
  assert.equal(identity.status, 'confirmed');
  assert.equal(identity.conversation_id, REAL_PROFILE_ID);
  assert.equal(identity.conversation_key, REAL_PROFILE_KEY);
  assert.equal(identityApi().normalizeConversationKey(REAL_PROFILE_KEY, { required: true }), REAL_PROFILE_KEY);
});

test('conversation identity can fall back to a trusted canonical /c URL and fails closed on conflicting confirmed identities', () => {
  const api = identityApi();
  assert.equal(typeof api.identityFromCandidates, 'function', 'shared identity module must expose deterministic candidate resolution');

  const fromCanonical = api.identityFromCandidates([
    'https://chatgpt.com/g/g-p-project/project-name',
    REAL_PROFILE_URL
  ]);
  assert.equal(fromCanonical.status, 'confirmed');
  assert.equal(fromCanonical.conversation_key, REAL_PROFILE_KEY);

  const conflict = api.identityFromCandidates([
    REAL_PROFILE_URL,
    'https://chatgpt.com/c/11111111-2222-8333-8444-555555555555'
  ]);
  assert.equal(conflict.status, 'conflict');
  assert.equal(conflict.conversation_key, '');
});

test('content identity refresh restores trusted canonical fallback instead of relying on location.href only', () => {
  assert.match(contentSource, /link\[rel=["']canonical["']\]/, 'content runtime must inspect the trusted canonical URL');
  assert.match(contentSource, /identityFromCandidates\(/, 'content runtime must use shared multi-candidate identity resolution');
});

test('a delivered WS_GET_IDENTITY response with empty/unconfirmed identity is not bootstrap success', () => {
  assert.doesNotMatch(
    bootstrapSource,
    /if \(probe\.delivered\) return/,
    'Chrome message delivery alone must never mean confirmed ChatGPT context'
  );
  assert.match(bootstrapSource, /usableIdentityProbe|isUsableIdentityProbe/, 'bootstrap must validate the returned identity/key before success');
  assert.match(bootstrapSource, /conversation_key/, 'bootstrap validity must include a confirmed conversation key');
});

test('Manual ON preserves the proven content-acknowledgement-before-worker-authorization transaction order', () => {
  const source = manualHandlerSource();
  const contentOn = source.indexOf('type: "WS_APPLY_MANUAL_MODE"');
  const workerOn = source.indexOf('type: "WS_SET_MANUAL_MODE"');
  assert.ok(contentOn >= 0, 'Manual ON content apply must exist');
  assert.ok(workerOn > contentOn, `Manual ON must apply content before worker authorization; got content=${contentOn}, worker=${workerOn}`);
  assert.match(source, /applied\.applied\s*!==\s*true|applied\?\.applied\s*!==\s*true/);
});
