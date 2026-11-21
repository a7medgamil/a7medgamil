#!/usr/bin/env python3
"""Integrate cinematic artwork into the existing executive dossier without removing content."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent.parent
P=ROOT/'README.md'
source=P.read_text(encoding='utf-8')
if 'assets/cinematic/hero-executive.gif' in source:
    raise SystemExit('Cinematic README already applied; no duplicate insertion.')
original_heads=[f'{i:02d} / ' for i in range(1,10)]
assert all(x in source for x in original_heads)
def picture(stem,description):
    return f'''<picture>
  <source media="(prefers-reduced-motion: reduce) and (max-width: 900px)" srcset="assets/cinematic/{stem}-mobile-still.svg" />
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/cinematic/{stem}-still.svg" />
  <source media="(max-width: 900px)" srcset="assets/cinematic/{stem}-mobile.gif" />
  <img src="assets/cinematic/{stem}.gif" width="100%" alt="{description}" />
</picture>'''
def centered(stem,description):
    return '<p align="center">\n'+picture(stem,description)+'\n</p>\n'
hero_re=re.compile(r'\A<p align="center">\s*<picture>[\s\S]*?</picture>\s*</p>')
hero_txt=centered('hero-executive','Cinematic orbital executive introduction for Ahmed Gamil, Founder and CEO, displaying strategy, execution and connected systems.').strip()
source,n=hero_re.subn(hero_txt,source,count=1)
assert n==1,'Expected one original hero.'
all_picture=[m.group(0) for m in re.finditer(r'<picture>[\s\S]*?</picture>',source)]
venture=[x for x in all_picture if 'ventures-grid-' in x]
assert len(venture)==1,'One leadership visual expected'
source=source.replace(venture[0],picture('ventures-architected','Four institutional leadership cards: Saltrixma LLC, SMI, Flunex Institute, Gate of Scholarships.'),1)
sys_head='<h2 align="center"><img src="assets/dossier/section-03.svg" width="28" alt=""> 03 / Featured Systems</h2>'
stack_head='<h2 align="center"><img src="assets/dossier/section-04.svg" width="28" alt=""> 04 / Technical Operating Stack</h2>'
assert source.count(sys_head)==1 and source.count(stack_head)==1
source=source.replace(sys_head,sys_head+'\n\n'+centered('systems-atlas','Animated four-system portfolio connecting QADHA, MIYTO, SMI Digital Operations and AIU Smart HR.'),1)
source=source.replace(stack_head,stack_head+'\n\n'+centered('stack-constellation','Animated orbital engineering constellation covering eight technical capability groups.'),1)
assert all(x in source for x in original_heads)
for key in ['Remote Product & Technical Delivery','Academic Foundation & Journey','Career Timeline','Operating Principles','Selected public case studies','Discuss a Partnership','GitHub Activity']:
    assert key in source, key
P.write_text(source,encoding='utf-8')
print('README cinematic integration complete; preserved nine executive sections and all original narrative sections.')
