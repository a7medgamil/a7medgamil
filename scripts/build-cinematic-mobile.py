#!/usr/bin/env python3
"""Mobile-first companion scenes with large, readable type and single-column hierarchy."""
from pathlib import Path
import runpy, re, random, html
d=runpy.run_path(str(Path(__file__).parent/'build-cinematic-dossier.py'))
OUT=Path(__file__).resolve().parent.parent/'assets'/'cinematic'
t=d['t'];line=d['line'];rect=d['rect'];monolith=d['monolith'];orbital=d['orbital'];dot=d['dot'];still=d['still']
GOLD=d['GOLD'];WHITE=d['WHITE'];ICE=d['ICE'];COPPER=d['COPPER'];MUTED=d['MUTED']
defs=re.search(r'<defs>[\s\S]+?</defs>',d['base']('mobile vector definitions',900)[0]).group(0)
def paper(title,h):
    w=900;rng=random.Random(h)
    stars=''.join(f'<circle cx="{rng.randrange(20,880)}" cy="{rng.randrange(18,h-15)}" r="{rng.random()*1.1+.4:.1f}" fill="{GOLD}" opacity=".28"/>' for _ in range(100))
    grid=''.join(line(x,0,x,h,'#93B5CE',.07) for x in range(50,900,100))
    grid+=''.join(line(0,y,900,y,'#93B5CE',.05) for y in range(50,h,100))
    p=f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{h}" viewBox="0 0 900 {h}" role="img" aria-label="{html.escape(title,quote=True)}">'+defs+f'<rect width="900" height="{h}" rx="24" fill="url(#cosmos)"/><circle cx="465" cy="600" r="530" fill="url(#halo)"/>'+stars+grid
    end=f'<rect x="1.5" y="1.5" width="897" height="{h-3}" rx="23" fill="none" stroke="{GOLD}" stroke-opacity=".58"/><path d="M42 40h130" stroke="{GOLD}" stroke-width="3"/></svg>'
    return p,end

def hero():
    h=1290;p,q=paper('Ahmed Gamil executive cinematic mobile profile',h)
    s=t(64,116,'EXECUTIVE ENGINEERING ATLAS',33,GOLD,'600',2)
    s+=t(64,262,'AHMED',115,WHITE,'700',-2)
    s+=t(64,385,'GAMIL',123,GOLD,'700',-3)
    s+=t(64,453,'FOUNDER  /  CEO  /  SYSTEMS BUILDER',33,WHITE,'600',.4)
    s+=t(64,510,'Building organizations, digital products',30,MUTED)
    s+=t(64,553,'and systems with operational purpose.',30,MUTED)
    s+=line(64,600,836,600,GOLD,.46,2)
    s+='<ellipse cx="450" cy="875" rx="340" ry="266" fill="#D9B76E" opacity=".14" filter="url(#bigglow)"/>'
    s+=orbital(450,882,338,237,32,20,GOLD)+orbital(450,882,267,303,38,55,ICE)
    s+=monolith(450,897,.87)
    s+=t(450,1207,'SALTRIXMA  •  SMI  •  FLUNEX  •  SCHOLARSHIPS',27,GOLD,'600',.8,'middle')
    return p+s+q

def card(x,y,w,h,title,sub,idx):
    s=rect(x,y,w,h,22,'#112136',GOLD,.58)
    s+=f'<path d="M{x+20} {y+12}h128" stroke="{ICE}" stroke-width="4" />'
    s+=f'<rect x="{x+17}" y="{y+28}" width="94" height="90" rx="18" fill="#1C354B" stroke="{ICE}" stroke-opacity=".53"/>'
    s+=t(x+64,y+85,f'{idx:02d}',35,GOLD,'700',0,'middle')
    s+=t(x+137,y+77,title,37,WHITE,'700',0)
    s+=t(x+137,y+119,sub,27,MUTED)
    s+=f'<circle cx="{x+w-26}" cy="{y+28}" r="6" fill="{ICE}"><animate attributeName="opacity" values=".18;1;.18" dur="{4+idx}s" repeatCount="indefinite"/></circle>'
    return s

def stack():
    h=2300;p,q=paper('Eight engineering capability groups for mobile',h)
    s=t(55,124,'ENGINEERING',75,WHITE,'700',-1)
    s+=t(55,209,'CONSTELLATION',67,GOLD,'700',-1)
    s+=t(55,270,'Eight connected areas of technical delivery.',30,MUTED)
    s+=orbital(450,552,320,220,42,14,ICE)+orbital(450,552,253,290,36,48,GOLD)
    s+=monolith(450,558,.73)
    s+=t(450,853,'CAPABILITIES • ENGINEERING • DELIVERY',27,GOLD,'600',1,'middle')
    data=[
      ('FRONTEND','React  ·  Next.js'),('BACKEND','PHP  ·  Laravel'),
      ('DATA & CLOUD','PostgreSQL  ·  Redis'),('MOBILE','Flutter  ·  Expo'),
      ('INFRASTRUCTURE','Cloudflare  ·  Docker'),('API & INTEGRATIONS','REST  ·  Webhooks'),
      ('SECURITY','Access  ·  Authentication'),('AI & ARCHITECTURE','OpenAI API  ·  n8n')]
    for i,(name,sub) in enumerate(data):
        s+=card(58,913+i*168,784,146,name,sub,i+1)
    return p+s+q

def ventures():
    h=1730;p,q=paper('Four leadership organizations, accessible mobile layout',h)
    s=t(52,116,'FOUR ORGANIZATIONS',61,WHITE,'700',0)
    s+=t(54,181,'ONE CONNECTED DIRECTION',39,GOLD,'600',1)
    s+=t(54,229,'Leadership across technology and education.',28,MUTED)
    organizations=[
       ('SALTRIXMA LLC','CHIEF EXECUTIVE OFFICER','SL'),
       ('SUPERIOR MULTISKILLS','FOUNDER & MANAGING DIRECTOR','SM'),
       ('FLUNEX INSTITUTE','VICE DIRECTOR','FX'),
       ('GATE OF SCHOLARSHIPS','FOUNDER','GS')]
    for i,(name,role,abbr) in enumerate(organizations):
        y=277+i*354
        s+=rect(55,y,790,317,26,'#102035',GOLD,.59)
        s+=f'<rect x="83" y="{y+30}" width="160" height="158" rx="18" fill="url(#glass)" stroke="{ICE}" stroke-opacity=".7"/>'
        s+=f'<polygon points="163,{y+50} 224,{y+83} 224,{y+138} 163,{y+170} 102,{y+138} 102,{y+83}" fill="none" stroke="{GOLD}" stroke-width="3"/>'
        s+=t(163,y+122,abbr,40,WHITE,'700',1,'middle')
        s+=t(279,y+80,f'0{i+1}  /  LEADERSHIP',25,GOLD,'600',1)
        sector=['TECHNOLOGY','EDUCATION','OPERATIONS','OPPORTUNITY'][i]
        s+=t(279,y+143,sector,43,WHITE,'700')
        s+=t(84,y+247,name,46,WHITE,'700')
        s+=t(84,y+286,role,30,MUTED,'500')
        s+=f'<circle cx="811" cy="{y+34}" r="7" fill="{ICE}"><animate attributeName="opacity" values=".2;1;.2" dur="{5+i}s" repeatCount="indefinite"/></circle>'
    return p+s+q

def systems():
    h=1650;p,q=paper('Flagship systems for mobile in an orbital technology arrangement',h)
    s=t(54,111,'SYSTEMS IN',69,WHITE,'700')
    s+=t(54,195,'MOTION',88,GOLD,'700')
    s+=t(55,253,'Strategy  /  technology  /  proof',32,MUTED)
    s+=orbital(450,556,330,225,36,14,ICE)+orbital(450,556,250,280,33,-20,GOLD)
    s+=monolith(450,573,.72)
    s+=t(450,852,'SYSTEMS / PRODUCT PORTFOLIO',31,GOLD,'600',1,'middle')
    projects=[
        ('QADHA','Social product / battle rules','PRODUCT'),
        ('MIYTO','Audio-first learning rooms','EDUCATION'),
        ('SMI DIGITAL OPERATIONS','Connected academic workflows','OPERATIONS'),
        ('AIU SMART HR','Academic HR/NLP design','ACADEMIC')]
    for i,(name,sub,cat) in enumerate(projects):
        y=922+i*181
        s+=rect(54,y,792,159,24,'#0F2034',ICE,.57)
        s+=t(86,y+40,f'0{i+1}  /  {cat}',26,GOLD,'600',1.4)
        s+=t(86,y+96,name,41,WHITE,'700')
        s+=t(86,y+139,sub,29,MUTED)
        s+=f'<circle cx="799" cy="{y+34}" r="7" fill="{ICE}"><animate attributeName="opacity" values=".2;1;.2" dur="{4+i}s" repeatCount="indefinite"/></circle>'
    return p+s+q

for name,fun in [('hero-executive-mobile',hero),('stack-constellation-mobile',stack),('ventures-architected-mobile',ventures),('systems-atlas-mobile',systems)]:
    content=fun()
    (OUT/f'{name}.svg').write_text(content,encoding='utf-8')
    (OUT/f'{name}-still.svg').write_text(still(content),encoding='utf-8')
    print('MOBILE',name,len(content))
