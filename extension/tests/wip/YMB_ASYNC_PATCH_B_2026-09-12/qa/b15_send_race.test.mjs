// Execute exact production functions in VM; supplemental to real browser RED/GREEN.
import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';
const source=fs.readFileSync(process.env.YMB_FILE_CONTENT,'utf8');
function fixture(){
 const pending=[],buttons=[],calls=[];const node={isConnected:true,style:{},textContent:'',remove(){this.isConnected=false;}};
 const ctx=vm.createContext({console,Set,HTMLElement:Object,document:{getElementById:()=>node},setTimeout:()=>1,clearTimeout:()=>{},chrome:{runtime:{sendMessage(m,cb){calls.push(m);pending.push(cb);},lastError:null}}});ctx.globalThis=ctx;
 const marker='  runtime.timer = setTimeout(poll, 250);';assert.equal(source.split(marker).length,2);
 vm.runInContext(source.replace(marker,'  globalThis.__sendTest = {commitAndClick,runtime};'),ctx);
 const button={isConnected:true,clicks:0,click(){this.clicks++;},removeEventListener(){}};
 const entry={delivery_id:'d',conversation_key:'c'};
 return{ctx,button,entry,calls,pending,run:()=>ctx.__sendTest.commitAndClick(entry,button),reply:(r={ok:true})=>pending.shift()(r)};
}
test('one durable send acknowledgement produces one click',async()=>{const f=fixture(),p=f.run();assert.equal(f.calls.length,1);f.reply();await p;assert.equal(f.button.clicks,1);});
test('concurrent duplicate send intent cannot issue a second commit or click',async()=>{const f=fixture(),a=f.run(),b=f.run();const count=f.calls.length;while(f.pending.length)f.reply();await Promise.all([a,b]);assert.equal(count,1);assert.equal(f.button.clicks,1);});
test('already committed acknowledgement is observation only, never another click',async()=>{const f=fixture(),p=f.run();f.reply({ok:true,already_committed:true});await p;assert.equal(f.button.clicks,0);});
test('rejected commit is surfaced and sends nothing',async()=>{const f=fixture(),p=f.run();f.reply({ok:false,code:'NOT_OWNER'});await assert.rejects(p,e=>e.code==='NOT_OWNER');assert.equal(f.button.clicks,0);});
test('explicit later action is possible after a denied uncommitted request; no automatic retry',async()=>{const f=fixture(),p=f.run();f.reply({ok:false,code:'NOT_READY'});await assert.rejects(p);assert.equal(f.calls.length,1);const q=f.run();f.reply();await q;assert.equal(f.calls.length,2);assert.equal(f.button.clicks,1);});
test('disposed content never clicks after a delayed committed reply',async()=>{const f=fixture(),p=f.run();f.ctx.__sendTest.runtime.disposed=true;f.reply();await p;assert.equal(f.button.clicks,0);});
test('disconnected Send button never receives synthetic click',async()=>{const f=fixture(),p=f.run();f.button.isConnected=false;f.reply();await p;assert.equal(f.button.clicks,0);});
test('disposed runtime does not initiate a send commit',async()=>{const f=fixture();f.ctx.__sendTest.runtime.disposed=true;const p=f.run();if(f.pending.length)f.reply();await p;assert.equal(f.calls.length,0);});
test('in-flight metadata cleared after repeated explicit sends',async()=>{const f=fixture();for(let i=0;i<20;i++){const p=f.run();f.reply();await p;}assert.equal(f.button.clicks,20);assert.equal(f.ctx.__sendTest.runtime.send_in_flight.size,0);});
