/* Make original technology logos visibly bob, glow and orbit in GitHub-safe GIFs.
   Original SVG/WEBP assets remain untouched. Generated GIFs are for README only. */
const fs=require('node:fs');
const path=require('node:path');
const child=require('node:child_process');
const sharp=require('sharp'); // install optional build dependencies in scripts/ with npm ci
sharp.cache(false);sharp.concurrency(2);
const root=path.resolve(__dirname,'..');
const out=path.join(root,'assets','live');
fs.mkdirSync(out,{recursive:true});
const TYPES=['frontend','backend','data','mobile','infrastructure','api','security','architecture'];
const FRAMES=14, FPS=7;
const selected=process.argv.slice(2);
const tasks=selected.length?selected:['tech','venture','workflow'];
const fmt=n=>Number(n).toFixed(2);
function palette(t){return t==='dark'?['#F5CC82','#6DE5ED']:['#B2783D','#167D91'];}
function boostTech(svg,step,tone){
 const colors=palette(tone),p=step/FRAMES*Math.PI*2;let i=0;
 let output=svg.replace(/<svg x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"/g,function(all,xs,ys,ws,hs){
   const x=+xs,y=+ys,w=+ws,h=+hs,z=i++,k=(Math.sin(p+z*1.31)+1)/2;
   const dy=Math.sin(p+z*.93)*5, dx=Math.sin(p+z*1.09)*2.4;
   const cx=x+w/2,cy=y+h/2;
   return '<g aria-hidden="true"><circle cx="'+fmt(cx)+'" cy="'+fmt(cy)+'" r="'+fmt(43+k*5)+'" fill="none" stroke="'+colors[z%2]+'" stroke-opacity="'+fmt(.23+k*.6)+'" stroke-width="2" stroke-dasharray="26 36" transform="rotate('+fmt(step*360/FRAMES+z*40)+' '+fmt(cx)+' '+fmt(cy)+')"/><circle cx="'+fmt(cx)+'" cy="'+fmt(cy)+'" r="34" fill="'+colors[0]+'" fill-opacity="'+fmt(.12+k*.19)+'" filter="url(#live-glow)"/></g><svg x="'+fmt(x+dx)+'" y="'+fmt(y+dy)+'" width="'+ws+'" height="'+hs+'"';
 });
 if(!i)throw Error('No original logo icons in SVG');
 output=output.replace('</defs>','<filter id="live-glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="9"/></filter></defs>');
 const m=output.match(/viewBox="0 0 (\d+) (\d+)"/);
 const w=+m[1],h=+m[2],sx=40+(w-80)*step/FRAMES;
 const scan='<path d="M'+fmt(Math.max(40,sx-120))+' '+(h-10)+'H'+fmt(sx)+'" stroke="'+colors[1]+'" stroke-width="3" opacity=".68"/><circle cx="'+fmt(sx)+'" cy="'+(h-10)+'" r="3" fill="'+colors[0]+'" />';
 return output.replace(/<\/svg>\s*$/,scan+'</svg>');
}
function boostWorkflow(svg,step,tone){
 const c=palette(tone),p=step/FRAMES*Math.PI*2;
 const m=svg.match(/viewBox="0 0 (\d+) (\d+)"/);
 let shapes='',n=0;
 for(const hit of svg.matchAll(/<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" rx="8"/g)){
  const x=+hit[1],y=+hit[2],w=+hit[3],h=+hit[4];if(w<110||h<100)continue;
  const v=Math.pow(Math.max(0,Math.cos(p-n*.85)),3);n++;
  shapes+='<rect x="'+(x+2)+'" y="'+(y+2)+'" width="'+(w-4)+'" height="'+(h-4)+'" rx="7" fill="none" stroke="'+c[n%2]+'" stroke-width="'+fmt(1+v*2.5)+'" stroke-opacity="'+fmt(.17+.74*v)+'"/>';
 }
 const travel=64+(+m[1]-128)*step/FRAMES, y=+m[2]-29;
 shapes+='<path d="M64 '+y+'H'+fmt(travel)+'" stroke="'+c[1]+'" stroke-width="3" opacity=".86"/><circle cx="'+fmt(travel)+'" cy="'+y+'" r="5" fill="'+c[0]+'"/>';
 return svg.replace(/<\/svg>\s*$/,shapes+'</svg>');
}
function overlayVenture(tone,w,h,step){
 const c=palette(tone),phase=step/FRAMES*Math.PI*2;
 let s='<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'" viewBox="0 0 '+w+' '+h+'">';
 for(let n=0;n<4;n++){const col=n%2,row=Math.floor(n/2);
  const x=col*w/2+10,y=row*h/2+10,cw=w/2-20,ch=h/2-20,k=(Math.sin(phase+n*1.5)+1)/2;
  s+='<rect x="'+fmt(x)+'" y="'+fmt(y)+'" width="'+fmt(cw)+'" height="'+fmt(ch)+'" rx="7" fill="none" stroke="'+c[n%2]+'" stroke-width="'+fmt(1+k*1.6)+'" stroke-opacity="'+fmt(.26+k*.6)+'"/>';
  s+='<path d="M'+fmt(x+10)+' '+fmt(y+3)+'h'+fmt(cw*(.14+k*.3))+'" stroke="'+c[n%2]+'" stroke-width="3" stroke-opacity="'+fmt(.28+k*.62)+'"/>';
  s+='<circle cx="'+fmt(x+cw-17)+'" cy="'+fmt(y+17)+'" r="'+fmt(2.5+k*2.4)+'" fill="'+c[0]+'" opacity="'+fmt(.3+k*.65)+'"/>';
 }
 return Buffer.from(s+'</svg>');
}
async function rawSvg(svg,width){
 const r=await sharp(Buffer.from(svg)).resize({width}).ensureAlpha().raw().toBuffer({resolveWithObject:true});
 return r;
}
function encode(frames,w,h,file){
 const args=['-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgba','-video_size',w+'x'+h,'-framerate',String(FPS),'-i','pipe:0','-filter_complex',
 '[0:v]split[a][b];[a]palettegen=max_colors=112:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4[v]',
 '-map','[v]','-loop','0',file];
 const p=child.spawnSync('ffmpeg',args,{input:Buffer.concat(frames),timeout:60000,maxBuffer:3000000});
 if(p.status!==0)throw Error('FFmpeg '+p.stderr.toString());
 return fs.statSync(file).size;
}
async function animateSvg(kind,type,tone,mobile){
 const source='assets/dossier/'+(kind==='tech'?'capability-'+type:kind)+'-'+tone+(mobile?'-mobile':'')+'.svg';
 const svg=fs.readFileSync(path.join(root,source),'utf8'),m=svg.match(/viewBox="0 0 (\d+) (\d+)"/);
 const w=mobile?640:1056, h=Math.round(w*Number(m[2])/Number(m[1])),frames=[];
 for(let i=0;i<FRAMES;i++){
  const img=kind==='tech'?boostTech(svg,i,tone):boostWorkflow(svg,i,tone);
  const r=await rawSvg(img,w);
  if(r.info.height!==h)throw Error('bad dimensions '+source);
  frames.push(r.data);
 }
 const output=path.join(out,(kind==='tech'?'capability-'+type:'workflow')+'-'+tone+(mobile?'-mobile':'')+'.gif');
 console.log(source,encode(frames,w,h,output));
}
async function animateVenture(tone,mobile){
 const src='assets/dossier/ventures-grid-'+tone+(mobile?'-mobile':'')+'.webp',w=mobile?640:1056;
 const base=await sharp(path.join(root,src)).resize({width:w}).png().toBuffer();
 const md=await sharp(base).metadata(),h=md.height,frames=[];
 for(let i=0;i<FRAMES;i++){
  const glow=overlayVenture(tone,w,h,i);
  const r=await sharp(base).composite([{input:glow}]).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  frames.push(r.data);
 }
 const f=path.join(out,'ventures-grid-'+tone+(mobile?'-mobile':'')+'.gif');
 console.log(src,encode(frames,w,h,f));
}
(async()=>{
 let count=0;
 for(const tone of ['dark','light'])for(const mobile of [false,true]){
  if(tasks.includes('tech'))for(const type of TYPES){await animateSvg('tech',type,tone,mobile);console.log('FINISHED',++count);}
  if(tasks.includes('workflow')){await animateSvg('workflow','',tone,mobile);console.log('FINISHED',++count);}
  if(tasks.includes('venture')){await animateVenture(tone,mobile);console.log('FINISHED',++count);}
 }
 console.log('DONE '+count+' animations');
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
