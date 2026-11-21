#!/usr/bin/env python3
"""Size-limit animated GitHub profile assets while preserving original visuals."""
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parent.parent
folder=ROOT/'assets'/'live'
files=sorted(folder.glob('*.gif'))
if len(files)!=48:
    raise SystemExit('Unexpected file count; expected 48 GIFs, got '+str(len(files)))
before=sum(p.stat().st_size for p in files)
changed=0
for num,p in enumerate(files,1):
    tmp=p.with_name(p.stem+'-optimizing.gif')
    colors=96 if ('hero' in p.name or 'ventures' in p.name) else 80
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p),
         '-filter_complex',f'[0:v]fps=6,split[a][b];[a]palettegen=max_colors={colors}:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4[v]',
         '-map','[v]','-loop','0',str(tmp)]
    process=subprocess.run(cmd,capture_output=True,timeout=90)
    if process.returncode:
        raise RuntimeError('Failed optimizing '+p.name+': '+process.stderr.decode(errors='replace')[:350])
    if tmp.stat().st_size < p.stat().st_size:
        tmp.replace(p)
        changed+=1
    else:
        tmp.unlink()
    if num%8==0:
        print(f'{num}/{len(files)} GIFs optimized')
after=sum(p.stat().st_size for p in files)
print(f'OPTIMIZATION COMPLETE; {changed} compressed; before={before/1048576:.2f}MiB; after={after/1048576:.2f}MiB; saved={(before-after)/1048576:.2f}MiB')
