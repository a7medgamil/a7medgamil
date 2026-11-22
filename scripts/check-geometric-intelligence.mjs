import assert from 'node:assert/strict';
import {readFileSync,existsSync,statSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const readme=readFileSync(resolve(root,'README.md'),'utf8');
const docs=readFileSync(resolve(root,'docs/GEOMETRIC-INTELLIGENCE-CONTENT-SHA256.txt'),'utf8');
const expected=docs.match(/\b[a-f0-9]{64}\b/)?.[0];
const norm=readme.replace(/\r\n/g,'\n').replace(/<picture>[\s\S]*?<\/picture>/g,'<picture/>');
assert.equal(createHash('sha256').update(norm).digest('hex'),expected,'Non-picture README prose, links, and evidence changed!');
let count=0;
for(const family of ['hero','ventures','systems','capabilities']){
 const blocks=[...readme.matchAll(/<picture>[\s\S]*?<\/picture>/g)].map(m=>m[0]).filter(s=>s.includes('assets/isometric-cubes/'+family+'-desktop.svg'));
 assert.equal(blocks.length,1,'Exactly one active cubic picture required for '+family);
 const block=blocks[0];
 assert.equal((block.match(/prefers-reduced-motion: reduce/g)||[]).length,2,'Missing reduced-motion fallbacks for '+family);
 for(const [device,suffix] of [['desktop',''],['desktop','-static'],['mobile',''],['mobile','-static']]){
   const path='assets/isometric-cubes/'+family+'-'+device+suffix+'.svg';
   assert.ok(block.includes(path),'Missing responsive README source '+path);
   const file=resolve(root,path);
   assert.ok(existsSync(file),'Missing generated isometric SVG '+path);
   const data=readFileSync(file,'utf8');
   assert.match(data,/<svg[^>]+viewBox="0 0 \d+ \d+"/,'SVG viewBox missing '+path);
   assert.match(data,/<title\b/,'Accessible title missing '+path);
   assert.match(data,/<desc\b/,'Accessible description missing '+path);
   assert.doesNotMatch(data,/<(?:script|foreignObject|iframe|image)\b/i,'No scripting, embeds or external raster assets '+path);
   assert.doesNotMatch(data,/(?:href|src)=["']https?:/i,'No external image/network sources '+path);
   if(suffix==='-static')assert.doesNotMatch(data,/<animate/i,'Reduced-motion SVG must be still '+path);
   else assert.match(data,/<animate(?:Transform)?\b/i,'Animated SVG must contain native motion '+path);
   assert.ok(statSync(file).size<100000,'Unexpected oversized vector asset '+path);
   count++;
 }
 const oldRender=resolve(root,'assets/geometric-intelligence/'+(family==='capabilities'?'skills':family)+'-render.png');
 assert.ok(existsSync(oldRender),'Previous Blender 3D render should remain archived '+oldRender);
 assert.ok(existsSync(resolve(root,'assets/studio3d/'+(family==='capabilities'?'skills':family)+'-render.png')),'Earlier 3D source render was lost '+family);
}
for(let i=1;i<=9;i++)assert.ok(readme.includes(String(i).padStart(2,'0')+' / '),'Original section missing '+i);
for(const name of ['Saltrixma LLC','Superior Multiskills Institution','Flunex Institute','Gate of Scholarships','QADHA','MIYTO Smart Rooms','AIU Smart HR','Career Timeline','Academic Foundation & Journey','Remote Product & Technical Delivery','Selected public case studies']){
 assert.ok(readme.includes(name),'Original information missing '+name);
}
for(const family of ['hero','ventures','systems','skills'])assert.ok(!readme.includes('assets/geometric-intelligence/'+family+'-desktop.gif'),'Previous experimental art should not remain active in README: '+family);
console.log('ISOMETRIC CUBE PROFILE VERIFIED: '+count+'/16 original responsive SVG assets, animated and static variants, accessible labels, archive retained, all 9 sections and all non-picture README content unchanged.');
