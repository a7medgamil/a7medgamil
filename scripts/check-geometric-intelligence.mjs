import assert from 'node:assert/strict';
import {readFileSync,existsSync,statSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const r=readFileSync(resolve(root,'README.md'),'utf8');
const docs=readFileSync(resolve(root,'docs/GEOMETRIC-INTELLIGENCE-CONTENT-SHA256.txt'),'utf8');
const expected=docs.match(/\b[a-f0-9]{64}\b/)?.[0];
const norm=r.replace(/\r\n/g,'\n').replace(/<picture>[\s\S]*?<\/picture>/g,'<picture/>');
assert.equal(createHash('sha256').update(norm).digest('hex'),expected,'Non-picture README text / links changed!');
let count=0;
for(const family of ['hero','ventures','systems','skills']){
 const blocks=[...r.matchAll(/<picture>[\s\S]*?<\/picture>/g)].map(m=>m[0]).filter(s=>s.includes('assets/geometric-intelligence/'+family+'-desktop.gif'));
 assert.equal(blocks.length,1, 'Exactly one responsive picture required for '+family);
 const block=blocks[0];
 assert.equal((block.match(/prefers-reduced-motion: reduce/g)||[]).length,2,'Missing static accessibility fallback');
 for(const size of ['desktop','mobile']){
   for(const ext of ['gif','webp']){
     const path='assets/geometric-intelligence/'+family+'-'+size+'.'+ext;
     assert.ok(block.includes(path),'Missing README image for '+path);
     const file=resolve(root,path);
     assert.ok(existsSync(file),'Missing generated 3D artwork '+path);
     const data=readFileSync(file);
     if(ext==='gif'){
       assert.equal(data.subarray(0,6).toString('ascii'),'GIF89a','Invalid GIF89a '+path);
       assert.ok(data.includes(Buffer.from('NETSCAPE2.0')),'Nonlooping GIF '+path);
       assert.ok(statSync(file).size<2_000_000,'Oversized animation '+path);
     }else{
       assert.equal(data.toString('ascii',0,4),'RIFF',path);
       assert.equal(data.toString('ascii',8,12),'WEBP',path);
     }
     count++;
   }
 }
 assert.ok(existsSync(resolve(root,'assets/geometric-intelligence/'+family+'-render.png')),'Missing true Blender model render');
 assert.ok(existsSync(resolve(root,'assets/studio3d/'+family+'-render.png')),'Previous studio render was lost');
}
for(let i=1;i<=9;i++)assert.ok(r.includes(String(i).padStart(2,'0')+' / '),'Original section missing '+i);
for(const name of ['Saltrixma LLC','Superior Multiskills Institution','Flunex Institute',
'Gate of Scholarships','QADHA','MIYTO Smart Rooms','AIU Smart HR','Career Timeline',
'Academic Foundation & Journey','Remote Product & Technical Delivery','Selected public case studies']){
 assert.ok(r.includes(name),'Original information missing '+name);
}
console.log('GEOMETRIC INTELLIGENCE VERIFIED: '+count+'/16 render assets, 4 Cycles source renders, preserved original 9 sections and all non-picture text.');
