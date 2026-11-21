import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { resolve, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const root=fileURLToPath(new URL('../',import.meta.url));
const readme=readFileSync(resolve(root,'README.md'),'utf8');
const names=['hero-centered','profile-card','ventures-grid','workflow',...[
'frontend','backend','data','mobile','infrastructure','api','security','architecture'].map(x=>'capability-'+x)];
const cases=['dark','light','dark-mobile','light-mobile'];
const files=readdirSync(resolve(root,'assets/live')).filter(x=>x.endsWith('.gif')).sort();
assert.equal(files.length,48,'Expected twelve graphic families with four GIF theme/viewport variants');
const pictureBlocks=[...readme.matchAll(/<picture>\s*([\s\S]*?)<\/picture>/g)].map(m=>m[0]);
let checked=0;
for(const family of names) {
  const associated=pictureBlocks.filter(p=>p.includes('assets/live/'+family+'-'));
  assert.equal(associated.length,1,'Exactly one README picture for '+family);
  const pic=associated[0];
  const reduced=(pic.match(/media="\([^"]*prefers-reduced-motion: reduce[^"]*"/g)||[]).length;
  assert.equal(reduced,4,'Four matching static fallbacks required for '+family);
  for(const tone of cases) {
    const src='assets/live/'+family+'-'+tone+'.gif';
    assert.equal((readme.match(new RegExp(src.replaceAll('.','\\.').replaceAll('/','\\/'),'g'))||[]).length,1,'Missing/duplicate animation '+src);
    const file=resolve(root,src);
    assert.ok(existsSync(file),'Missing animation '+src);
    const bytes=readFileSync(file);
    assert.equal(bytes.subarray(0,6).toString('ascii'),'GIF89a','Must be an animated GIF '+src);
    assert.ok(bytes.includes(Buffer.from('NETSCAPE2.0')),'GIF should loop '+src);
    const size=statSync(file).size;
    assert.ok(size>10000 && size<2500000,'Suspicious or oversized GIF '+src+': '+size);
    checked++;
  }
}
for(let i=1;i<=9;i++) {
  assert.ok(readme.includes(String(i).padStart(2,'0')+' / '),'Original executive dossier section missing: '+i);
}
console.log('LIVE PROFILE AUDIT: '+checked+'/48 verified autonomous GIFs, 12/12 responsive visual groups, four reduced-motion fallbacks per group; all 9 original sections retained.');
