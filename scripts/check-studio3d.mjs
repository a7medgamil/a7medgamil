import assert from 'node:assert/strict';
import {readFileSync,existsSync,statSync} from 'node:fs';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const readme=readFileSync(resolve(root,'README.md'),'utf8');
const types=['hero','ventures','systems','skills'];
const original=['hero-executive','ventures-architected','systems-atlas','stack-constellation'];
const docs=readFileSync(resolve(root,'docs/STUDIO3D-CONTENT-CHECK.txt'),'utf8');
const expected=docs.match(/\b[a-f0-9]{64}\b/)?.[0];
assert.ok(expected,'Missing original non-visual content fingerprint');
const fingerprint=createHash('sha256').update(readme.replace(/\r\n/g,'\n').replace(/<picture>[\s\S]*?<\/picture>/g,'<picture/>')).digest('hex');
assert.equal(fingerprint,expected,'Non-image text, links, facts or tables changed during visual-only redesign');
let n=0;
for(const k of types){
  const pictures=[...readme.matchAll(/<picture>[\s\S]*?<\/picture>/g)].map(x=>x[0])
      .filter(s=>s.includes('assets/studio3d/'+k+'-desktop.gif'));
  assert.equal(pictures.length,1,'Missing or duplicated active 3D image for '+k);
  const p=pictures[0];
  for(const suffix of ['desktop','mobile']){
    for(const ext of ['gif','webp']){
      const name='assets/studio3d/'+k+'-'+suffix+'.'+ext;
      assert.ok(p.includes(name),'README missing 3D image source '+name);
      const full=resolve(root,name);assert.ok(existsSync(full),name+' missing');
      const b=readFileSync(full);
      if(ext==='gif'){
        assert.equal(b.subarray(0,6).toString('ascii'),'GIF89a',name+' corrupt GIF');
        assert.ok(b.includes(Buffer.from('NETSCAPE2.0')),name+' not looping');
        assert.ok(statSync(full).size<2_000_000,'GIF larger than allowed 2MB: '+name);
      } else {
        assert.equal(b.toString('ascii',0,4),'RIFF',name+' invalid RIFF');
        assert.equal(b.toString('ascii',8,12),'WEBP',name+' invalid WebP');
      }
      n++;
    }
    const staticMedia='(prefers-reduced-motion: reduce)'+(suffix==='mobile'?' and (max-width: 900px)':'');
    assert.ok(p.includes(staticMedia),'Reduced motion fallback missing: '+k+' '+suffix);
  }
  assert.ok(existsSync(resolve(root,'assets/studio3d/'+k+'-render.png')),'No physical Blender render for '+k);
}
for(const old of original){
 for(const suffix of ['','-mobile']){
  for(const tail of ['.gif','-still.svg']){
   assert.ok(existsSync(resolve(root,'assets/cinematic/'+old+suffix+tail)),'Legacy original deleted: '+old+suffix+tail);
  }
 }
}
for(let i=1;i<=9;i++)assert.ok(readme.includes(String(i).padStart(2,'0')+' / '),'Missing executive section '+i);
for(const detail of ['Saltrixma LLC','Superior Multiskills Institution','Flunex Institute',
 'Gate of Scholarships','QADHA','MIYTO Smart Rooms','AIU Smart HR','Career Timeline',
 'Academic Foundation & Journey','Remote Product & Technical Delivery','Selected public case studies']){
 assert.ok(readme.includes(detail),'Missing original information: '+detail);
}
console.log('STUDIO3D QA SUCCESS: '+n+'/16 published assets, four physical render sources, 9 sections, content SHA preserved. Original cinematic artwork remains archived.');
