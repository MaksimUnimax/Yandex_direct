import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const source = fs.readFileSync(path.join(root, 'shared/conversation_identity.js'), 'utf8');

function api() {
  const context = vm.createContext({ URL, console });
  context.globalThis = context;
  vm.runInContext(source, context, { filename: 'conversation_identity.js' });
  return context.BB2ConversationIdentity;
}

const ID = '12345678-1234-4123-8123-123456789abc';
const KEY = `https://chatgpt.com|${ID}`;

test('direct ChatGPT /c conversation remains confirmed', () => {
  const identity = api().identityFromUrl(`https://chatgpt.com/c/${ID}`);
  assert.equal(identity.status, 'confirmed');
  assert.equal(identity.conversation_id, ID);
  assert.equal(identity.conversation_key, KEY);
});

test('ChatGPT Project conversation /g/.../c/<uuid> is confirmed as the same conversation', () => {
  const identity = api().identityFromUrl(`https://chatgpt.com/g/g-p-example-project/project-name/c/${ID}`);
  assert.equal(identity.status, 'confirmed');
  assert.equal(identity.conversation_id, ID);
  assert.equal(identity.conversation_key, KEY);
  assert.equal(identity.chat_path, `/c/${ID}`);
});

test('custom GPT conversation /g/.../c/<uuid> is confirmed without trusting the GPT slug', () => {
  const identity = api().identityFromUrl(`https://chatgpt.com/g/g-example-custom-gpt/c/${ID}?model=auto`);
  assert.equal(identity.status, 'confirmed');
  assert.equal(identity.conversation_key, KEY);
});

test('Project root without a concrete /c/<uuid> remains unconfirmed', () => {
  const identity = api().identityFromUrl('https://chatgpt.com/g/g-p-example-project/project');
  assert.equal(identity.status, 'unconfirmed');
  assert.equal(identity.conversation_key, '');
});

test('foreign origin with a nested /c/<uuid> still fails closed', () => {
  const identity = api().identityFromUrl(`https://example.com/g/project/c/${ID}`);
  assert.equal(identity.status, 'unconfirmed');
  assert.equal(identity.conversation_key, '');
});
