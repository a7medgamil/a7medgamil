#!/usr/bin/env python3
"""Replace ONLY four existing <picture> artworks with studio-rendered 3D scenes.
Content fidelity guarantee: all text, links, project notes and other images stay byte-for-byte intact.
"""
import re,hashlib,pathlib
root=pathlib.Path(__file__).resolve().parent.parent
readme=root/'README.md'
original=readme.read_text(encoding='utf-8')
families={'hero-executive':'hero','ventures-architected':'ventures',
          'systems-atlas':'systems','stack-constellation':'skills'}
def nonvisual(s):
    return re.sub(r'<picture>[\s\S]*?</picture>', '<picture/>',s)
before=hashlib.sha256(nonvisual(original).encode()).hexdigest()
new=original
for old,newname in families.items():
    matched=[m for m in re.finditer(r'<picture>[\s\S]*?</picture>',new)
             if f'assets/cinematic/{old}.gif' in m.group(0)]
    assert len(matched)==1, f'Expected exactly one original {old} picture, found {len(matched)}'
    art=f"""<picture>
  <source media="(prefers-reduced-motion: reduce) and (max-width: 900px)" srcset="assets/studio3d/{newname}-mobile.webp" />
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/studio3d/{newname}-desktop.webp" />
  <source media="(max-width: 900px)" srcset="assets/studio3d/{newname}-mobile.gif" />
  <img src="assets/studio3d/{newname}-desktop.gif" width="100%" alt="Original genuine Blender-rendered 3D executive artwork for the {newname} section, with a mobile layout and reduced-motion still." />
</picture>"""
    new=new.replace(matched[0].group(0),art,1)
after=hashlib.sha256(nonvisual(new).encode()).hexdigest()
assert before==after, f'Non-visual README content was modified! {before} != {after}'
assert new.count('assets/studio3d/')==16
for i in range(1,10):
    assert f'{i:02d} / ' in new, f'Original section {i} missing'
readme.write_text(new,encoding='utf-8')
(root/'docs'/'STUDIO3D-CONTENT-CHECK.txt').write_text(
 'SHA-256 of README with all <picture> elements normalized to <picture/>:\n'+
 before+'\nEvery non-picture byte remained unchanged during the visual replacement.\n',
 encoding='utf-8'
)
print('PRESERVED_ALL_TEXT_AND_LINKS',before,'Replaced four image components only')
