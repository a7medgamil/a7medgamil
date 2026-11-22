import assert from 'node:assert/strict';
import {existsSync,readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const readme=readFileSync(resolve(root,'README.md'),'utf8');
const names=['hero-executive','ventures-architected','systems-atlas','stack-constellation'];
let preserved=0;
for(const family of names){
 for(const suffix of ['','-mobile']){
  for(const tail of ['.svg','-still.svg','.gif']){
   const file=resolve(root,'assets/cinematic/'+family+suffix+tail);
   assert.ok(existsSync(file),'Original source artwork unexpectedly removed: '+file);
   preserved++;
  }
 }
}
for(let i=1;i<=9;i++)assert.ok(readme.includes(String(i).padStart(2,'0')+' / '),'Missing original executive narrative section '+i);
for(const id of ['hero','ventures','systems','skills']){
 assert.ok(readme.includes('assets/geometric-intelligence/'+id+'-desktop.gif'),'New chromatic 3D geometry not active: '+id);
}
console.log('CINEMATIC LEGACY QA: '+preserved+' original and fallback assets preserved; all 9 sections and 4 new 3D panels present.');
