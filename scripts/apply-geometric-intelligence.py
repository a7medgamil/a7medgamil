#!/usr/bin/env python3
"""Replace only four prior art blocks with sophisticated chromatic geometry.
Every existing non-picture character is protected by a SHA256 invariant.
"""
from pathlib import Path
from hashlib import sha256
import re
root=Path(__file__).resolve().parent.parent
p=root/'README.md'
text=p.read_text(encoding='utf8')
def without_pictures(s):
    return re.sub(r'<picture>[\s\S]*?</picture>','<picture/>',s)
baseline=sha256(without_pictures(text).encode()).hexdigest()
new=text
names={
 'hero':'hero',
 'ventures':'ventures',
 'systems':'systems',
 'skills':'skills',
}
for name in names:
    pics=[m for m in re.finditer(r'<picture>[\s\S]*?</picture>',new)
          if 'assets/studio3d/'+name+'-desktop.gif' in m.group(0)]
    assert len(pics)==1, f'Expected exactly one old {name} picture; got {len(pics)}'
    previous=pics[0].group(0)
    art=f"""<picture>
  <source media="(prefers-reduced-motion: reduce) and (max-width: 900px)" srcset="assets/geometric-intelligence/{name}-mobile.webp" />
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/geometric-intelligence/{name}-desktop.webp" />
  <source media="(max-width: 900px)" srcset="assets/geometric-intelligence/{name}-mobile.gif" />
  <img src="assets/geometric-intelligence/{name}-desktop.gif" width="100%" alt="Original multicolor computational geometry, physically rendered in Blender for the {name} section; precise accessible desktop and mobile variants." />
</picture>"""
    new=new.replace(previous,art,1)
assert sha256(without_pictures(new).encode()).hexdigest()==baseline, 'README text or links were changed!'
assert new.count('assets/geometric-intelligence/')==16
assert all(f'{i:02d} / ' in new for i in range(1,10))
p.write_text(new,encoding='utf8')
(root/'docs'/'GEOMETRIC-INTELLIGENCE-CONTENT-SHA256.txt').write_text(
    'README SHA-256 with each picture element reduced to <picture/>:\n'+baseline+'\nAll original text, links, project descriptions and evidence remain unchanged.\n',
    encoding='utf8')
print('GEO_PROFILE_TEXT_100_PERCENT_UNCHANGED',baseline)
