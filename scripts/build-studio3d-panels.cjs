/**
 * Premium editorial compositor for genuine Blender 4.5 Cycles 3D source renders.
 * Text is authored in SVG overlay with measured safe bounds, and in README remains
 * real text. Exports 4 desktop + 4 mobile stills, plus low-motion animated loops.
 * Install: npm ci --prefix scripts, requires ffmpeg on PATH.
 */
const fs=require('node:fs');
const path=require('node:path');
const cp=require('node:child_process');
const sharp=require('sharp');
sharp.cache(false);sharp.concurrency(2);
const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'assets','studio3d');
const W=1600,H=760, MW=900, MH=1320;
const DARK='#070D19', GOLD='#EBC992', LIGHT='#F8F2E7', MUTE='#B1C3CF';
const projects={
  hero:{
    name:'hero',caption:'EXECUTIVE SYSTEMS / 01',
    alt:'Actual physically rendered 3D smoked-glass and champagne-gold executive sculpture, introducing Ahmed Gamil as founder, CEO and systems builder.'
  },
  ventures:{
    name:'ventures',caption:'INSTITUTIONAL LEADERSHIP / 02',
    alt:'Four distinct, physically rendered 3D sculptures representing Saltrixma LLC, Superior Multiskills Institution, Flunex Institute and Gate of Scholarships.'
  },
  systems:{
    name:'systems',caption:'FEATURED SYSTEMS / 03',
    alt:'Four actual three-dimensional product sculptures representing QADHA, MIYTO, SMI Digital Operations and AIU Smart HR.'
  },
  skills:{
    name:'skills',caption:'TECHNOLOGY / 04',
    alt:'Physically rendered 3D orbital constellation with eight individual faceted gems connected around a central architecture core.'
  }
};
const escape=(s)=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const labels={
 ventures:[
  {title:['SALTRIXMA LLC'],sub:['CEO']},
  {title:['SUPERIOR MULTISKILLS','INSTITUTION'],sub:['Founder & Managing Director']},
  {title:['FLUNEX INSTITUTE'],sub:['Vice Director']},
  {title:['GATE OF SCHOLARSHIPS'],sub:['Founder']}
 ],
 systems:[
  {title:['QADHA'],sub:['Flagship digital product']},
  {title:['MIYTO'],sub:['Smart Rooms / Audio learning']},
  {title:['SMI OPERATIONS'],sub:['Institutional digital systems']},
  {title:['AIU SMART HR'],sub:['Academic HR / NLP design']}
 ]
};
function txt(x,y,str,size=25,color=LIGHT,weight=600,letter=0,anchor='start'){
 return '<text x="'+x+'" y="'+y+'" fill="'+color+'" font-family="Arial,Segoe UI,sans-serif" font-size="'+size+'" font-weight="'+weight+'" letter-spacing="'+letter+'" text-anchor="'+anchor+'">'+escape(str)+'</text>';
}
function svg(content,w=W,h=H){
 const def='<defs><linearGradient id="left" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#050A14" stop-opacity=".99"/><stop offset=".65" stop-color="#070E1A" stop-opacity=".91"/><stop offset="1" stop-color="#070E1A" stop-opacity="0"/></linearGradient><linearGradient id="bottom" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#060B15" stop-opacity="0"/><stop offset=".45" stop-color="#070D18" stop-opacity=".90"/><stop offset="1" stop-color="#050A13" stop-opacity=".98"/></linearGradient><linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050A14" stop-opacity=".89"/><stop offset="1" stop-color="#060B15" stop-opacity="0"/></linearGradient></defs>';
 return Buffer.from('<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'" viewBox="0 0 '+w+' '+h+'">'+def+content+'</svg>');
}
function ornament(caption){
 return '<path d="M78 87H248" fill="none" stroke="'+GOLD+'" stroke-width="2"/>'+
 txt(80,122,caption,22,GOLD,600,2.1);
}
function desktopOverlay(k){
 if(k==='hero'){
   return svg(
     '<rect x="0" y="0" width="990" height="'+H+'" fill="url(#left)"/>'+
     '<path d="M86 118H625" stroke="'+GOLD+'" stroke-opacity=".65" stroke-width="2"/>'+
     txt(85,89,'THE EXECUTIVE EDITION',23,GOLD,650,4)+
     txt(78,332,'AHMED',153,LIGHT,800,-3)+txt(78,494,'GAMIL',154,GOLD,800,-4)+
     txt(86,566,'FOUNDER  /  CEO  /  SYSTEMS BUILDER',29,LIGHT,700,.7)+
     txt(86,617,'Organizations. Technology. Execution.',23,MUTE,450,.2)+
     '<path d="M86 655H745" stroke="'+GOLD+'" stroke-opacity=".35" stroke-width="2"/>'+
     txt(86,703,'SALTRIXMA   •   SMI   •   FLUNEX   •   SCHOLARSHIPS',20,GOLD,600,1.3)+
     '<path d="M1398 55H1518V175" fill="none" stroke="'+GOLD+'" stroke-opacity=".65" stroke-width="2"/>'
   );
 }
 if(k==='skills'){
   return svg(
     '<rect x="0" y="0" width="900" height="'+H+'" fill="url(#left)"/>'+
     ornament('TECHNOLOGY CONSTELLATION  /  04')+
     txt(80,269,'ENGINEERING',94,LIGHT,790,-1.6)+
     txt(80,364,'CAPABILITIES',90,GOLD,790,-1.4)+
     txt(83,438,'Eight connected disciplines',29,LIGHT,550)+
     txt(83,479,'across product and institutional systems.',25,MUTE,450)+
     '<path d="M85 531H695" stroke="'+GOLD+'" stroke-opacity=".5" stroke-width="2"/>'+
     txt(84,583,'FRONTEND    BACKEND    CLOUD    MOBILE',19,LIGHT,600,1)+
     txt(84,627,'SECURITY    INTEGRATIONS    AI    ARCHITECTURE',19,LIGHT,600,.4)+
     txt(84,710,'FROM REQUIREMENTS TO DELIVERY',18,GOLD,600,2)
   );
 }
 let out='<rect x="0" y="0" width="1600" height="225" fill="url(#top)"/>'+
         '<rect x="0" y="425" width="1600" height="335" fill="url(#bottom)"/>'+
         txt(75,81,k==='ventures'?'LEADERSHIP / VENTURES':'PRODUCTS / SYSTEMS',47,LIGHT,800,1.7)+
         txt(80,124,k==='ventures'?'Four organizations. One operating vision.':'From product direction to operational systems.',23,GOLD,540,.3)+
         '<path d="M77 152H1523" stroke="'+GOLD+'" stroke-opacity=".32" stroke-width="2"/>';
 const set=labels[k];
 for(let i=0;i<4;i++){
   const x=50+i*393;
   const label=set[i];
   out+='<path d="M'+(x+1)+' 560V714" stroke="'+GOLD+'" stroke-opacity=".48" stroke-width="2"/>'+
     txt(x+13,583,('0'+(i+1))+'  /  '+(k==='ventures'?'LEADERSHIP':'ENGINEERING'),17,GOLD,700,1.2);
   let y=629;
   for(const title of label.title){out+=txt(x+13,y,title,title.length>19?25:30,LIGHT,780,.35);y+=35;}
   for(const sub of label.sub){out+=txt(x+13,715,sub,sub.length>21?19:22,MUTE,530);}
 }
 return svg(out);
}
async function fullRaw(k){
 const input=path.join(OUT,k+'-render.png');
 if(!fs.existsSync(input))throw new Error('Missing Blender Cycles scene: '+input);
 return sharp(input).resize(W,H,{fit:'cover',position:'center'}).png().toBuffer();
}
async function desktop(k,raw){
 const composed=await sharp(raw).composite([{input:desktopOverlay(k)}]).png().toBuffer();
 await sharp(composed).webp({quality:89,effort:5}).toFile(path.join(OUT,k+'-desktop.webp'));
 return composed;
}
function mobileTop(k){
 if(k==='hero'){
  return svg(
    txt(53,98,'THE EXECUTIVE EDITION',27,GOLD,700,3)+
    '<path d="M53 119H746" stroke="'+GOLD+'" stroke-opacity=".55" stroke-width="2"/>'+
    txt(48,283,'AHMED',132,LIGHT,800,-2)+txt(48,427,'GAMIL',136,GOLD,800,-2)+
    txt(54,507,'FOUNDER   /   CEO',44,LIGHT,770,.5)+
    txt(54,558,'SYSTEMS BUILDER',42,LIGHT,770,.5)+
    txt(54,631,'Building organizations and digital products.',28,MUTE,470)+
    txt(54,678,'From strategy through execution.',28,MUTE,470)+
    txt(450,1247,'SALTRIXMA  •  SMI  •  FLUNEX  •  SCHOLARSHIPS',21,GOLD,650,.3,'middle')
  ,MW,MH);
 }
 return svg(
   txt(52,108,'ENGINEERING',80,LIGHT,790,-1.0)+
   txt(52,197,'CAPABILITIES',76,GOLD,790,-.9)+
   txt(54,264,'Eight connected technology disciplines.',28,MUTE,500)+
   '<path d="M53 292H850" stroke="'+GOLD+'" stroke-opacity=".50" stroke-width="2"/>'+
   txt(50,1027,'FRONTEND     BACKEND     CLOUD     MOBILE',25,LIGHT,650,.3)+
   txt(50,1072,'SECURITY     INTEGRATIONS     AI',25,LIGHT,650,.3)+
   txt(50,1117,'ARCHITECTURE     TECHNICAL DELIVERY',25,GOLD,650,.3)+
   txt(50,1247,'STRATEGY  •  ENGINEERING  •  EXECUTION',23,MUTE,600,1.2)
 ,MW,MH);
}
function gridOverlay(k){
 let out=txt(44,90,k==='ventures'?'LEADERSHIP / VENTURES':'FEATURED / SYSTEMS',48,LIGHT,770,.2)+
 txt(47,137,k==='ventures'?'Four organizations. One operating vision.':'Four systems. Direction, delivery, evidence.',27,GOLD,530)+
 '<path d="M43 170H858" stroke="'+GOLD+'" stroke-opacity=".45"/>';
 const positions=[[31,205],[459,205],[31,755],[459,755]];
 labels[k].forEach((d,i)=>{
   const [x,y]=positions[i];
   out+='<rect x="'+x+'" y="'+y+'" width="410" height="530" rx="16" fill="none" stroke="'+GOLD+'" stroke-opacity=".54" stroke-width="1.4"/>'+
   '<rect x="'+(x+12)+'" y="'+(y+374)+'" width="385" height="138" rx="9" fill="#070D18" fill-opacity=".91"/>'+
   txt(x+22,y+404,('0'+(i+1))+' / '+(k==='ventures'?'VENTURE':'SYSTEM'),20,GOLD,700,1.3);
   let start=y+445;
   for(const [j,title] of d.title.entries()){out+=txt(x+22,start+j*30,title,title.length>19?22:30,LIGHT,790);}
   out+=txt(x+22,y+500,d.sub[0],d.sub[0].length>21?19:22,MUTE,520);
 });
 return svg(out,MW,MH);
}
async function mobile(k,raw){
 let pieces=[];
 const bg=await sharp({create:{width:MW,height:MH,channels:4,background:DARK}}).png().toBuffer();
 if(k==='hero'||k==='skills'){
  // Actual photographed sculpture is shown large, never downscaled to unreadability.
  const sourceCrop=k==='hero'?{left:785,top:25,width:790,height:735}:{left:730,top:15,width:830,height:745};
  const art=await sharp(raw).extract(sourceCrop).resize(900,650,{fit:'cover'}).png().toBuffer();
  const alpha=svg('<defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="white" stop-opacity="0"/><stop offset=".15" stop-color="white" stop-opacity="1"/><stop offset=".80" stop-color="white" stop-opacity="1"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient></defs><rect width="900" height="650" fill="url(#fade)"/>',900,650);
  const faded=await sharp(art).composite([{input:alpha,blend:'dest-in'}]).png().toBuffer();
  pieces.push({input:faded,left:0,top:k==='hero'?658:322});
  pieces.push({input:mobileTop(k)});
 }else{
  const pos=[[31,205],[459,205],[31,755],[459,755]];
  for(let i=0;i<4;i++){
   const source=await sharp(raw).extract({left:i*400+20,top:25,width:360,height:635}).resize(390,354,{fit:'cover'}).toBuffer();
   pieces.push({input:source,left:pos[i][0]+10,top:pos[i][1]+11});
  }
  pieces.push({input:gridOverlay(k)});
 }
 const result=await sharp(bg).composite(pieces).png().toBuffer();
 await sharp(result).webp({quality:88,effort:5}).toFile(path.join(OUT,k+'-mobile.webp'));
 return result;
}
async function gif(k,image,mobile){
 const w=mobile?660:990, h=mobile?968:470;
 const base=await sharp(image).resize(w,h,{fit:'fill'}).png().toBuffer();
 const frames=[];
 for(let i=0;i<16;i++){
   const t=2*Math.PI*i/16;
   const cx=mobile? (k==='hero'||k==='skills'? 335:200) : (k==='hero'||k==='skills'?730:220);
   const cy=mobile? (k==='hero'||k==='skills'? 670:390) : (k==='hero'||k==='skills'?260:235);
   const x=cx+(mobile?70:115)*Math.cos(t);
   const y=cy+(mobile?60:105)*Math.sin(t);
   const shimmer=svg(
      '<circle cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="'+(mobile?3:3.5)+'" fill="#F6E0B0" opacity="'+(.35+.35*Math.sin(t)*Math.sin(t)).toFixed(2)+'"/>'+
      '<circle cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="11" fill="none" stroke="#F6D6A0" stroke-opacity=".22"/>'
   ,w,h);
   const frame=await sharp(base).composite([{input:shimmer}]).ensureAlpha().raw().toBuffer({resolveWithObject:true});
   frames.push(frame.data);
 }
 const target=path.join(OUT,k+(mobile?'-mobile':'-desktop')+'.gif');
 const args=['-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgba',
             '-video_size',w+'x'+h,'-framerate','8','-i','pipe:0',
             '-filter_complex','[0:v]split[a][b];[a]palettegen=max_colors=160:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4[v]',
             '-map','[v]','-loop','0',target];
 const res=cp.spawnSync('ffmpeg',args,{input:Buffer.concat(frames),timeout:90000,maxBuffer:6000000});
 if(res.status!==0)throw Error(res.stderr.toString());
 console.log('GIF',target,fs.statSync(target).size);
}
(async()=>{
 const scenes=process.argv.slice(2);
 for(const k of (scenes.length?scenes:Object.keys(projects))){
   if(!projects[k])throw Error('Unknown scene '+k);
   const raw=await fullRaw(k);
   const d=await desktop(k,raw);
   const m=await mobile(k,raw);
   await gif(k,d,false);
   await gif(k,m,true);
   console.log('STUDIO3D_PANEL_READY',k);
 }
})().catch(e=>{console.error(e.stack||e);process.exitCode=1});
