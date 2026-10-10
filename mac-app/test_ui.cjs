// Exercise real page deletion handlers with mocked API calls, never real tasks.
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const source=fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
class Element{
 constructor(){this.children=[];this.style={};this.className='';this._text='';}
 set textContent(s){this._text=s;this.children=[];}get textContent(){return this._text+this.children.map(x=>x.textContent).join('');}
 append(x){this.children.push(x);}replaceChildren(){this._text='';this.children=[];}setAttribute(){}querySelector(){return null;}
}
async function run(confirmed,fail=false){
 const msg=new Element(),card=new Element(),remove=new Element(),calls=[];let removed=false;
 const report={status:'success',elements:[{label:'工具任务列表记录',status:'success',detail:'删除成功'},{label:'本机文稿及任务文件',status:'success',detail:'删除成功'},{label:'对应的千问记录',status:'success',detail:'未找到对应千问记录'}]};
 const c={j:{id:'a12345678901',title:'临时测试'},msg,card,remove,deletionResults:new Map(),deletedTaskIds:new Set(),refreshSequence:0,deleteNoticeTimer:null,
 document:{createElement:()=>new Element(),querySelectorAll:()=>[{remove:()=>{removed=true;}}]},confirm:()=>confirmed,
 fetch:async()=>({json:async()=>({cloud_delete:true})}),requireControls:async()=>{},refresh:async()=>{},
 post:async(url)=>{calls.push(url);if(fail){const e=Error('模拟千问错误');e.deletionResult={status:'failed',elements:report.elements.map(x=>({...x,status:'failed',detail:'未删除'}))};throw e;}return {deletion_result:report};},
 setTimeout:(fn,delay)=>{c.delay=delay;c.timer=fn;return 1;},clearTimeout:()=>{}};
 vm.createContext(c);
 const render=source.slice(source.indexOf('function renderDeletionResult('),source.indexOf('const deletedTaskIds='));vm.runInContext(render,c);
 const start=source.indexOf('remove.onclick=async()=>{');const end=source.indexOf(';if(j.has_document)',start);
 vm.runInContext(source.slice(start,end),c);await remove.onclick();
 if(!confirmed){assert.equal(calls.length,0);assert(!removed);return;}
 assert.deepEqual(calls,['/delete/a12345678901']);
 if(fail){assert(!removed);assert.equal(msg.className,'failure');assert(msg.children.slice(1).every(x=>x.style.color==='#a52222'));}
 else{assert(removed);assert(c.deletedTaskIds.has(c.j.id));assert.equal(c.delay,3000);assert(msg.children.slice(1).every(x=>x.style.color==='#176538'));c.timer();assert.equal(msg.textContent,'');}
}
(async()=>{await run(false);await run(true);await run(true,true);console.log('PASS: cancellation sends no request; confirmation deletes card; three result colors; 3-second success notice; failure retains card');})().catch(e=>{console.error(e);process.exit(1);});
