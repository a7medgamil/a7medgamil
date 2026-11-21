import assert from 'node:assert/strict';
import {readFileSync,existsSync,statSync} from 'node:fs';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const readme=readFileSync(resolve(root,'README.md'),'utf8');
const families=['hero-executive','ventures-architected','systems-atlas','stack-constellation'];
let count=0;
for(const name of families){
  for(const [suffix,type] of [['','.gif'],['-mobile','.gif'],['-still','.svg'],['-mobile-still','.svg']]){
    const file='assets/cinematic/'+name+suffix+type;
    assert.ok(existsSync(resolve(root,file)),'missing '+file);
    assert.ok(readme.includes(file),'README is not using '+file);
    const data=readFileSync(resolve(root,file));
    if(type==='.gif'){
      assert.equal(data.subarray(0,6).toString(),'GIF89a',file+' not an animated GIF89a');
      assert.ok(data.includes(Buffer.from('NETSCAPE2.0')),file+' must loop');
      assert.ok(statSync(resolve(root,file)).size<8_000_000,file+' too big');
    }else{
      const svg=data.toString('utf8');
      assert.match(svg,/xmlns="http:\/\/www.w3.org\/2000\/svg"/,file+' invalid header');
      assert.ok(!svg.includes('<animate'),file+' must respect reduced motion');
    }
    count++;
  }
  const picture=[...readme.matchAll(/<picture>[\s\S]*?<\/picture>/g)]
    .filter(m=>m[0].includes('assets/cinematic/'+name+'.gif'));
  assert.equal(picture.length,1,'exactly one responsive GIF for '+name);
  assert.equal((picture[0][0].match(/prefers-reduced-motion: reduce/g)||[]).length,2,'two static fallbacks for '+name);
}
for(let n=1;n<=9;n++){
 assert.ok(readme.includes(String(n).padStart(2,'0')+' / '),'removed original section '+n);
}
for(const text of ['Saltrixma LLC','Superior Multiskills Institution','Flunex Institute','Gate of Scholarships','QADHA','MIYTO Smart Rooms','AIU Smart HR','Remote Product & Technical Delivery']){
 assert.ok(readme.includes(text),'removed executive content '+text);
}
console.log('CINEMATIC PROFILE QA: '+count+'/'+count+' assets; eight GIF loops; eight reduced-motion variants; 9/9 narrative sections retained.');
