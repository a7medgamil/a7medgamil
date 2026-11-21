/* Frame-rendered, real looping GIFs for GitHub; dynamic SVGs remain editable. */
const fs=require('node:fs');
const path=require('node:path');
const cp=require('node:child_process');
const sharp=require('sharp'); // npm ci in scripts/ (see scripts/package.json)
sharp.cache(false);sharp.concurrency(2);
const root=path.resolve(__dirname,'..');
const dir=path.join(root,'assets','cinematic');
const scenes=['hero-executive','ventures-architected','systems-atlas','stack-constellation',
              'hero-executive-mobile','ventures-architected-mobile','systems-atlas-mobile','stack-constellation-mobile'];
const FRAMES=20, FPS=8, WIDTH=1056;
function frame(svg,i){
  const phase=i/FRAMES*2*Math.PI;
  let n=0;
  // Inline a different perspective rotation at every frame.
  svg=svg.replace(/<ellipse([^>]*)><animateTransform[^>]*from="0 ([\d.]+) ([\d.]+)"[^>]*\/><\/ellipse>/g,(_,attrs,cx,cy)=>{
    const direction=n++%2===0?1:-1;
    const angle=(i/FRAMES*360*direction).toFixed(2);
    return '<ellipse'+attrs+' transform="rotate('+angle+' '+cx+' '+cy+')" />';
  });
  const floatY=(6-16*(.5+.5*Math.sin(phase))).toFixed(2);
  svg=svg.replace(/<g><animateTransform attributeName="transform" type="translate" values="0 5;0 -14;0 5" dur="7s" repeatCount="indefinite"\/>/g,
                   '<g transform="translate(0 '+floatY+')">');
  svg=svg.replace(/<animate(?:Transform|Motion)?\b[^>]*\/>/g,'');
  return svg;
}
async function build(name){
  const input=fs.readFileSync(path.join(dir,name+'.svg'),'utf8');
  const frames=[];
  let width,height;
  for(let i=0;i<FRAMES;i++){
    const buf=Buffer.from(frame(input,i));
    const targetWidth=name.endsWith('-mobile')?720:WIDTH;
    const r=await sharp(buf).resize({width:targetWidth}).ensureAlpha().raw().toBuffer({resolveWithObject:true});
    width=r.info.width;height=r.info.height;
    frames.push(r.data);
  }
  const dst=path.join(dir,name+'.gif');
  const ff=[
    '-hide_banner','-loglevel','error','-y','-f','rawvideo',
    '-pixel_format','rgba','-video_size',width+'x'+height,
    '-framerate',String(FPS),'-i','pipe:0','-filter_complex',
    '[0:v]split[a][b];[a]palettegen=max_colors=192:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4[v]',
    '-map','[v]','-loop','0',dst
  ];
  const res=cp.spawnSync('ffmpeg',ff,{input:Buffer.concat(frames),timeout:140000,maxBuffer:8000000});
  if(res.status!==0)throw new Error('ffmpeg '+name+' '+res.stderr.toString());
  console.log(name+' '+width+'x'+height+' '+FRAMES+' frames '+fs.statSync(dst).size+' bytes');
}
(async()=>{const individual=process.argv.find(s=>s.startsWith('--scene='));const selected=individual?[individual.split('=')[1]]:(process.argv.includes('--mobile-only')?scenes.filter(s=>s.endsWith('-mobile')):scenes);for(const s of selected){if(!scenes.includes(s))throw Error('Unknown scene: '+s);await build(s)}console.log('ALL_GIFS_DONE')})().catch(e=>{console.error(e.stack||e);process.exitCode=1});
