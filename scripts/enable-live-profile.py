#!/usr/bin/env python3
"""Swap only existing profile visual references for their real GitHub-safe animated variants.
Preserves sections, names, links, project facts and text 100% verbatim.
Retains original light/dark/mobile artwork for reduced-motion visitors.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent.parent
README=ROOT/'README.md'
text=README.read_text(encoding='utf-8')
categories=['frontend','backend','data','mobile','infrastructure','api','security','architecture']
groups=[
  ('assets/hero','hero-centered','.svg',True),
  ('assets/dossier','profile-card','.svg',True),
  ('assets/dossier','ventures-grid','.webp',False),
  ('assets/dossier','workflow','.svg',True),
]+[('assets/dossier','capability-'+name,'.svg',False) for name in categories]
count=0
for directory,base,ext,has_motion in groups:
    for tone in ['dark','light']:
        for mobile in [True,False]:
            suffix='-mobile' if mobile else ''
            source=directory+'/'+base+'-'+tone+suffix+('-motion' if has_motion else '')+ext
            target='assets/live/'+base+'-'+tone+suffix+'.gif'
            if not (ROOT/target).is_file():
                raise RuntimeError('Missing animated file: '+target)
            if text.count(source)!=1:
                raise RuntimeError('Expected exactly 1 source in README: '+source+' but got '+str(text.count(source)))
            text=text.replace(source,target)
            count+=1

pictures=0
def add_static_fallback(match):
    global pictures
    block=match.group(0)
    m=re.search(r'assets/live/([a-z0-9-]+)-(?:light|dark)(?:-mobile)?\.gif',block)
    if not m:
        return block
    pictures+=1
    base=m.group(1)
    if base=='hero-centered':
        directory='assets/hero';ext='.svg'
    elif base=='ventures-grid':
        directory='assets/dossier';ext='.webp'
    else:
        directory='assets/dossier';ext='.svg'
    fallbacks=[
      ('(prefers-reduced-motion: reduce) and (max-width: 900px) and (prefers-color-scheme: dark)','dark-mobile'),
      ('(prefers-reduced-motion: reduce) and (max-width: 900px)','light-mobile'),
      ('(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)','dark'),
      ('(prefers-reduced-motion: reduce)','light')
    ]
    sources=[]
    for media,suffix in fallbacks:
        static=directory+'/'+base+'-'+suffix+ext
        if not (ROOT/static).is_file():
            raise RuntimeError('Missing static fallback: '+static)
        sources.append('  <source media="'+media+'" srcset="'+static+'">')
    return block.replace('<picture>\n','<picture>\n'+'\n'.join(sources)+'\n',1)
text=re.sub(r'<picture>\n.*?</picture>',add_static_fallback,text,flags=re.S)
if count!=48 or pictures!=12:
    raise RuntimeError('Unexpected replacement counts: '+str((count,pictures)))
README.write_text(text,encoding='utf-8')
print('README animation upgrade applied:',count,'replacements across',pictures,'visual panels; original content preserved')
