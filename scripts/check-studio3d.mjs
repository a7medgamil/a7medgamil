import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const readme=readFileSync(resolve(root,'README.md'),'utf8');
const oldDocs=readFileSync(resolve(root,'docs/STUDIO3D-CONTENT-CHECK.txt'),'utf8');
const oldSHA=oldDocs.match(/\b[a-f0-9]{64}\b/)?.[0];
const currentSHA=createHash('sha256')
 .update(readme.replace(/\r\n/g,'\n').replace(/<picture>[\s\S]*?<\/picture>/g,'<picture/>'))
 .digest('hex');
assert.equal(currentSHA,oldSHA,'Non-picture information must match the Studio3D baseline');
let n=0;
for(const k of ['hero','ventures','systems','skills']){
  for(const suffix of ['desktop','mobile']){
    for(const ext of ['gif','webp']){
      const pathname=resolve(root,'assets/studio3d/'+k+'-'+suffix+'.'+ext);
      assert.ok(existsSync(pathname),'Legacy physical 3D asset deleted: '+pathname);
      const b=readFileSync(pathname);
      assert.equal(b.toString('ascii',0,4),ext==='gif'?'GIF8':'RIFF');
      n++;
    }
  }
  assert.ok(existsSync(resolve(root,'assets/studio3d/'+k+'-render.png')),'Physical source render deleted');
}
for(let i=1;i<=9;i++)assert.ok(readme.includes(String(i).padStart(2,'0')+' / '));
console.log('STUDIO3D ARCHIVE VERIFIED: '+n+' legacy assets and 4 source renders preserved; README text unchanged.');
