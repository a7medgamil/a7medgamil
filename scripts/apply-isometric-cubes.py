#!/usr/bin/env python3
"""Switch only the four README visual panels to premium isometric cube SVGs.
All prose, links, headings and evidence are SHA256-guarded and remain unchanged.
"""
from pathlib import Path
from hashlib import sha256
import re
ROOT=Path(__file__).resolve().parent.parent
README=ROOT/'README.md'
DOC=ROOT/'docs'/'GEOMETRIC-INTELLIGENCE-CONTENT-SHA256.txt'
text=README.read_text(encoding='utf8')
expected=re.search(r'\b[a-f0-9]{64}\b',DOC.read_text(encoding='utf8')).group(0)
def normalized(s):
    return re.sub(r'<picture>[\s\S]*?</picture>','<picture/>',s)
before=sha256(normalized(text).encode()).hexdigest()
assert before==expected,'README prose differs from the last approved content baseline; refusing to change it.'
new=text
for family in ['hero','ventures','systems','capabilities']:
    current=[m.group(0) for m in re.finditer(r'<picture>[\s\S]*?</picture>',new)
             if f'assets/isometric-cubes/{family}-desktop.svg' in m.group(0)]
    if len(current)==1:
        continue  # Idempotent: this panel already uses the approved cube artwork.
    assert not current,f'Duplicate active {family} cube panels: {len(current)}'
    legacy='skills' if family=='capabilities' else family
    matches=[m.group(0) for m in re.finditer(r'<picture>[\s\S]*?</picture>',new)
             if f'assets/geometric-intelligence/{legacy}-desktop.gif' in m.group(0)]
    assert len(matches)==1,f'Expected exactly one old {family} picture, got {len(matches)}'
    old=matches[0]
    alt={
      'hero':'Large animated isometric cubic architecture, built from monumental shaded blocks for Ahmed Abdulbari executive profile',
      'ventures':'Four large isometric cubic architectures representing Saltrixma, SMI, Flunex and scholarship initiatives',
      'systems':'Distinct large modular isometric cube structures representing QADHA, MIYTO, SMI operations and AIU Smart HR',
      'capabilities':'An integrated monumental modular cube architecture representing eight executive and technical disciplines'
    }[family]
    replacement=f"""<picture>
  <source media="(prefers-reduced-motion: reduce) and (max-width: 900px)" srcset="assets/isometric-cubes/{family}-mobile-static.svg" />
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/isometric-cubes/{family}-desktop-static.svg" />
  <source media="(max-width: 900px)" srcset="assets/isometric-cubes/{family}-mobile.svg" />
  <img src="assets/isometric-cubes/{family}-desktop.svg" width="100%" alt="{alt}" />
</picture>"""
    new=new.replace(old,replacement,1)
assert sha256(normalized(new).encode()).hexdigest()==expected,'Non-picture README content changed; refusing to write.'
for family in ['hero','ventures','systems','capabilities']:
    block=[m.group(0) for m in re.finditer(r'<picture>[\s\S]*?</picture>',new)
           if f'assets/isometric-cubes/{family}-desktop.svg' in m.group(0)]
    assert len(block)==1
    for filename in [f'{family}-desktop.svg',f'{family}-desktop-static.svg',f'{family}-mobile.svg',f'{family}-mobile-static.svg']:
        assert (ROOT/'assets'/'isometric-cubes'/filename).is_file(),filename
README.write_text(new,encoding='utf8')
print('ISOMETRIC CUBE PANELS APPLIED: 4/4. README narrative SHA256 unchanged:',expected)
