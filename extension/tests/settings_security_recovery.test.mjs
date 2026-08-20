import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';
import { performance } from 'node:perf_hooks';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const workerSource = fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8');
const FN_NAMES = [...workerSource.matchAll(/^(?:async )?function\s+([A-Za-z0-9_]+)/gm)].map((m) => m[1]);
const CKEY = 'https://chatgpt.com|99999999-8888-4777-8666-555555555555';

function clone(value) { return value === undefined ? undefined : structuredClone(value); }
function harness(initial = {}) {
  const store = clone(initial);
  const storage = {
    async get(keys) {
      if (keys == null) return clone(store);
      if (typeof keys === 'string') return Object.hasOwn(store,keys) ? { [keys]: clone(store[keys]) } : {};
      if (Array.isArray(keys)) { const out={}; for (const key of keys) if (Object.hasOwn(store,key)) out[key]=clone(store[key]); return out; }
      const out=clone(keys || {}); for (const key of Object.keys(keys || {})) if (Object.hasOwn(store,key)) out[key]=clone(store[key]); return out;
    },
    async set(values) { Object.assign(store, clone(values)); },
    async remove(keys) { for (const key of (Array.isArray(keys) ? keys : [keys])) delete store[key]; }
  };
  const chrome = {
    storage:{local:storage},
    runtime:{id:'test',lastError:null,onMessage:{addListener(){}}},
    tabs:{sendMessage(_id,_message,cb){cb({ok:true});}}
  };
  const ctx=vm.createContext({console,chrome,crypto:webcrypto,TextEncoder,TextDecoder,AbortController,performance,setTimeout,clearTimeout,URL,structuredClone,Response,Request,Headers,ReadableStream,Buffer,fetch:async()=>new Response('{}',{status:200}),importScripts:()=>{}});
  ctx.globalThis=ctx;
  for (const file of ['shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js','shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js','shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js']) {
    vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
  }
  vm.runInContext(workerSource,ctx,{filename:'service_worker.js'});
  vm.runInContext(`globalThis.__SECURITY_API=Object.freeze({${FN_NAMES.join(',')}});`,ctx);
  return { api:ctx.__SECURITY_API, store };
}

test('ordinary public state never exposes the saved API key', async()=>{
  const secret='super-secret-api-key';
  const h=harness({wsmb_api_key:secret,wsmb_folder_id:'folder',ymb_debug_mode:true});
  const state=await h.api.publicGlobalSettingsState();
  const json=JSON.stringify(state);
  assert.equal(state.has_api_key,true);
  assert.equal(json.includes(secret),false);
  assert.equal(/authorization/i.test(json),false);
});

test('debug diagnostics redact API key, authorization, token and secret fields', async()=>{
  const secret='super-secret-api-key';
  const h=harness({ymb_debug_mode:true});
  await h.api.diagnostic('SECURITY_TEST',{api_key:secret,authorization:`Api-Key ${secret}`,nested:{token:secret,secret}}, {level:'error'});
  const json=JSON.stringify(h.store.ymb_diagnostics);
  assert.equal(json.includes(secret),false);
  assert.match(json,/\[REDACTED\]/);
});

test('settings import is blocked while Autorun is active and leaves existing secret untouched', async()=>{
  const h=harness({wsmb_api_key:'keep-secret',wsmb_auto_runs:{[CKEY]:{status:'waiting_command'}}});
  const backup={schema:'YMB_SETTINGS_BACKUP_V2',settings:{wordstat:{api_key:'incoming-secret',folder_id:'incoming-folder'}}};
  await assert.rejects(()=>h.api.importSettingsBackup(backup),(error)=>error.code==='IMPORT_ACTIVE_RUN');
  assert.equal(h.store.wsmb_api_key,'keep-secret');
});

test('settings import is blocked while a Manual operation is active and leaves existing secret untouched', async()=>{
  const h=harness({wsmb_api_key:'keep-secret',wsmb_manual_operations:{[CKEY]:{status:'requesting'}}});
  const backup={schema:'YMB_SETTINGS_BACKUP_V2',settings:{wordstat:{api_key:'incoming-secret',folder_id:'incoming-folder'}}};
  await assert.rejects(()=>h.api.importSettingsBackup(backup),(error)=>error.code==='IMPORT_ACTIVE_MANUAL');
  assert.equal(h.store.wsmb_api_key,'keep-secret');
});
