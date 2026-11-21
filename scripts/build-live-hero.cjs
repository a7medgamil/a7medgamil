/* Luminous CEO hero and executive cards, rendered from existing original SVG, not redrawn. */
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const sharp=require('sharp'); // install optional build dependencies in scripts/ with npm ci
sharp.cache(false);sharp.concurrency(2);
const root=path.resolve(__dirname,'..'),dest=path.join(root,'assets','live');
fs.mkdirSync(dest,{recursive:true});
const N=16,FPS=7,colors={dark:['#F6D396','#6EE5F3'],light:['#A9773E','#3295A7']};
const n=v=>Number(v).toFixed(2);
function hero(svg,f,tone){
 const m=svg.match(/viewBox="0 0 (\d+) (\d+)"/),w=+m[1],h=+m[2];
 const a=svg.match(/translate\(([\d.]+) ([\d.]+)\)/),cx=a?+a[1]:w/2,cy=a?+a[2]:h*.25;
 const r=w>1000?145:150,t=f/N*2*Math.PI,c=colors[tone],x=cx+Math.cos(t)*r,y=cy+Math.sin(t)*r;
 const arc='<g aria-hidden="true" fill="none"><circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" stroke="'+c[0]+'" stroke-width="2" stroke-dasharray="42 50" opacity=".57" transform="rotate('+n(360*f/N)+' '+cx+' '+cy+')"/><circle cx="'+n(x)+'" cy="'+n(y)+'" r="5" fill="'+c[1]+'" stroke="'+c[0]+'" stroke-width="2"/></g>';
 const lineY=w>1000?103:132,p=85+(w-170)*f/N,beam='<path d="M'+n(Math.max(85,p-160))+' '+lineY+'H'+n(p)+'" stroke="'+c[1]+'" stroke-width="3.2" stroke-opacity=".68"/>';
 return svg.replace(/<\/svg>\s*$/,arc+beam+'</svg>');
}
function profile(svg,f,tone){
 const c=colors[tone],t=f/N*2*Math.PI,shapes=[];
 const rx=/<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" rx="20"/g;let i=0;
 for(const m of svg.matchAll(rx)){
  if(+m[3]<300)continue;
  const x=+m[1],y=+m[2],w=+m[3],h=+m[4],k=(1+Math.sin(t+i*1.8))/2;
  shapes.push('<rect x="'+(x+3)+'" y="'+(y+3)+'" width="'+(w-6)+'" height="'+(h-6)+'" rx="18" fill="none" stroke="'+c[i%2]+'" stroke-opacity="'+n(.17+.65*k)+'" stroke-width="'+n(1+k*2.5)+'"/>');
  shapes.push('<path d="M'+(x+23)+' '+(y+5)+'h'+n(w*(.11+k*.29))+'" stroke="'+c[1]+'" stroke-opacity="'+n(.2+.73*k)+'" stroke-width="4" stroke-linecap="round"/>');
  i++;
 }
 return svg.replace(/<\/svg>\s*$/,shapes.join('')+'</svg>');
}
function gif(frames,w,h,file){
 const args=['-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgba','-video_size',w+'x'+h,'-framerate',String(FPS),'-i','pipe:0','-filter_complex',
 '[0:v]split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4[v]','-map','[v]','-loop','0',file];
 const res=cp.spawnSync('ffmpeg',args,{input:Buffer.concat(frames),timeout:60000,maxBuffer:3000000});
 if(res.status!==0)throw Error(res.stderr.toString());
 return fs.statSync(file).size;
}
(async()=>{
 for(const kind of ['hero','profile-card'])for(const tone of ['dark','light'])for(const mobile of [false,true]){
  const source=(kind==='hero'?'assets/hero/hero-centered-':'assets/dossier/profile-card-')+tone+(mobile?'-mobile':'')+'.svg';
  const xml=fs.readFileSync(path.join(root,source),'utf8');
  const view=xml.match(/viewBox="0 0 (\d+) (\d+)"/),w=mobile?560:1056,h=Math.round(w*(+view[2])/(+view[1]));
  const frames=[];
  for(let i=0;i<N;i++){
   const data=Buffer.from(kind==='hero'?hero(xml,i,tone):profile(xml,i,tone));
   const r=await sharp(data).resize({width:w}).ensureAlpha().raw().toBuffer({resolveWithObject:true});
   if(r.info.height!==h)throw Error('frame size mismatch '+source);
   frames.push(r.data);
  }
  const output=path.join(dest,(kind==='hero'?'hero-centered':'profile-card')+'-'+tone+(mobile?'-mobile':'')+'.gif');
  console.log(source, gif(frames,w,h,output));
 }
 console.log('DONE hero/profile animations');
})().catch(e=>{console.error(e);process.exit(1)});
