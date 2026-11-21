#!/usr/bin/env python3
"""Original cinematic SVG scenes for Ahmed Gamil's GitHub profile.
No proprietary visuals, logos or private data. 100% vector and reproducible.
"""
from __future__ import annotations
import math, html, re, random
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets'/'cinematic'
OUT.mkdir(parents=True,exist_ok=True)

GOLD='#F7D69A'
COPPER='#D69B66'
ICE='#91DCEC'
WHITE='#F5F1E8'
MUTED='#ACBBCB'

def t(x,y,s,size=24,fill=WHITE,weight='400',spacing=0,anchor='start',family='Segoe UI,Arial,sans-serif'):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" letter-spacing="{spacing}" text-anchor="{anchor}">{html.escape(s)}</text>'

def line(x1,y1,x2,y2,c=GOLD,o=.22,w=1):
    return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{c}" stroke-opacity="{o}" stroke-width="{w}"/>'

def rect(x,y,w,h,rx=14,fill='#101927',stroke=GOLD,opacity=.5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity=".93" stroke="{stroke}" stroke-opacity="{opacity}" stroke-width="1.6"/>'

def base(title,h):
    w=1600
    rng=random.Random(75+h)
    stars=''
    for i in range(155):
        x=rng.randrange(14,1587);y=rng.randrange(22,h-20)
        r=.5+rng.random()*1.55
        opacity=round(.11+rng.random()*.43,2)
        stars+=f'<circle cx="{x}" cy="{y}" r="{r:.2f}" fill="{ICE if i%6==0 else GOLD}" opacity="{opacity}"/>'
    grid=''
    for i in range(1,17):
        x=i*100
        grid+=line(x,0,x,h,'#94B8C7',.055)
    for y in range(32,h,85):
        grid+=line(0,y,1600,y,'#94B8C7',.05)
    # perspective lines add a distinct architectural depth layer
    horizon=int(h*.36)
    for x in range(-800,2401,160):
        grid+=line(1070,horizon,x,h,'#E6A970',.08)
    for i in range(5):
        y=int(horizon+(h-horizon)*((i+1)/6)**1.7)
        grid+=line(0,y,1600,y,'#E6A970',.085)
    defs='''<defs>
<linearGradient id="cosmos" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#060B17"/><stop offset=".53" stop-color="#0B1424"/><stop offset="1" stop-color="#060911"/></linearGradient>
<radialGradient id="halo"><stop stop-color="#DAA96F" stop-opacity=".36"/><stop offset=".5" stop-color="#577C9D" stop-opacity=".1"/><stop offset="1" stop-color="#0A0E19" stop-opacity="0"/></radialGradient>
<linearGradient id="aurum" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#FFF2CA"/><stop offset=".42" stop-color="#D9A977"/><stop offset=".75" stop-color="#815736"/><stop offset="1" stop-color="#F2C686"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#274A66" stop-opacity=".9"/><stop offset=".52" stop-color="#13273C" stop-opacity=".83"/><stop offset="1" stop-color="#060B17" stop-opacity=".8"/></linearGradient>
<linearGradient id="gemLeft" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#8DC9D7"/><stop offset=".55" stop-color="#2B6781"/><stop offset="1" stop-color="#0C243A"/></linearGradient>
<linearGradient id="gemRight" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#DEB171"/><stop offset=".5" stop-color="#976342"/><stop offset="1" stop-color="#302338"/></linearGradient>
<filter id="glow" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="bigglow" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="32"/></filter>
<clipPath id="rounded"><rect width="1600" height="''' + str(h) + '''" rx="22"/></clipPath>
</defs>'''
    prefix=f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{h}" viewBox="0 0 1600 {h}" role="img" aria-label="{html.escape(title,quote=True)}">'+defs+'<g clip-path="url(#rounded)">'+f'<rect width="1600" height="{h}" fill="url(#cosmos)"/>'+f'<circle cx="1100" cy="{int(h*.42)}" r="{int(h*.67)}" fill="url(#halo)"/>'+stars+grid
    suffix=f'<rect x="1" y="1" width="1598" height="{h-2}" rx="21" fill="none" stroke="#B28B60" stroke-opacity=".49"/><path d="M36 36h126M1438 {h-36}h126" stroke="{GOLD}" stroke-width="3" stroke-opacity=".7"/></g></svg>'
    return prefix,suffix

def twinkle(x,y,r=5,offset=0):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD}" opacity=".9"><animate attributeName="opacity" values=".23;.98;.23" dur="{4+offset}s" repeatCount="indefinite"/></circle>'

def orbital(cx,cy,rx,ry,duration,angle=0,color=GOLD):
    return (f'<g transform="rotate({angle} {cx} {cy})">'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{color}" stroke-opacity=".55" stroke-dasharray="8 15" stroke-width="1.6">'
            f'<animateTransform attributeName="transform" additive="sum" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{duration}s" repeatCount="indefinite"/></ellipse></g>')

def monolith(cx,cy,scale=1):
    # Stylized isometric prism, layered physical facets; original iconography rather than generic coding cartoon
    s=f'<g transform="translate({cx} {cy}) scale({scale})">'
    s+='<g><animateTransform attributeName="transform" type="translate" values="0 5;0 -14;0 5" dur="7s" repeatCount="indefinite"/>'
    for m in range(4,0,-1):
        y=m*24
        s+=f'<polygon points="0,{-165+y} 135,{-82+y} 0,{12+y} -135,{-82+y}" fill="#3C7895" fill-opacity="{.04+m*.025:.2f}" stroke="{GOLD}" stroke-opacity="{.07+m*.055:.2f}"/>'
    s+='<polygon points="0,-170 135,-92 0,-11 -135,-92" fill="url(#gemLeft)" stroke="#D6C5A6" stroke-width="2.5"/>'
    s+='<polygon points="-135,-92 0,-11 0,155 -135,74" fill="#163550" fill-opacity=".9" stroke="#91CAD7" stroke-width="2.5"/>'
    s+='<polygon points="135,-92 0,-11 0,155 135,74" fill="url(#gemRight)" stroke="#D5A775" stroke-width="2.5"/>'
    s+='<polygon points="0,-131 94,-78 0,-28 -94,-78" fill="none" stroke="#E5D5BD" stroke-opacity=".86" stroke-width="2"/>'
    s+='<path d="M0 -11V155M-135 -92L0 -11L135 -92M0 -170V-11" fill="none" stroke="#F8D6A1" stroke-opacity=".65" stroke-width="2"/>'
    s+='<circle cx="0" cy="-92" r="20" fill="#FFD9A6" opacity=".55" filter="url(#glow)"/>'
    s+='<circle cx="0" cy="-92" r="8" fill="#F7D6A1"/>'
    s+='</g></g>'
    return s

def tag(x,y,s):
    w=12+len(s)*12
    return rect(x,y,w,38,19,'#102035',GOLD,.55)+t(x+16,y+25,s,17,WHITE,'600',1)

def dot(x,y,c=GOLD,r=5):
    return f'<circle cx="{x}" cy="{y}" r="{r*3}" fill="{c}" opacity=".18" filter="url(#glow)"/><circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'

def hero():
    h=810
    p,q=base("Ahmed Gamil: cinematic founder and executive technology profile",h)
    c=''
    c+='<ellipse cx="1160" cy="376" rx="350" ry="285" fill="#D69B66" opacity=".16" filter="url(#bigglow)"/>'
    c+=orbital(1160,378,344,230,44,-25,ICE)
    c+=orbital(1160,378,295,272,34,46,GOLD)
    c+=orbital(1160,378,258,205,28,72,COPPER)
    c+=monolith(1160,390,.95)
    # architectural perspective accents and moving beacons
    c+=line(950,644,1530,644,GOLD,.52,2)
    c+=line(980,662,1500,662,ICE,.2,1)
    c+=twinkle(1440,170,5,2)+twinkle(910,247,4,3)+twinkle(1375,604,4,1)
    c+=t(120,103,'THE EXECUTIVE ENGINEERING ATLAS',24,GOLD,'600',4)
    c+=line(120,130,785,130,GOLD,.66,2)
    c+=t(113,303,'AHMED',126,WHITE,'700',-3)
    c+=t(113,438,'GAMIL',135,GOLD,'700',-4)
    c+=t(120,503,'FOUNDER  /  CEO  /  DIGITAL SYSTEMS BUILDER',28,WHITE,'600',1)
    c+=t(120,554,'Building organizations, products and operating systems.',23,MUTED)
    c+=t(120,593,'Where strategy, technology and execution converge.',23,MUTED)
    c+=line(120,623,758,623,ICE,.3,2)
    c+=tag(120,660,'STRATEGY')+tag(301,660,'SYSTEMS')+tag(469,660,'EXECUTION')
    c+=t(120,764,'SALTRIXMA LLC   •   SMI   •   FLUNEX   •   GATE OF SCHOLARSHIPS',18,GOLD,'500',1.3)
    c+=rect(1031,87,262,44,22,'#0C1B2D',GOLD,.65)+t(1162,116,'A LIVING SYSTEM',18,GOLD,'600',3,'middle')
    c+=t(1160,701,'CREATING STRUCTURE FROM COMPLEXITY',17,WHITE,'600',2,'middle')
    c+=twinkle(1160,92,3,4)
    return p+c+q

def info_card(x,y,w,h,title,subtitle,index):
    b=rect(x,y,w,h,19,'#101E30',COPPER,.57)
    b+=f'<path d="M{x+18} {y+12}h84" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>'
    b+=f'<circle cx="{x+w-42}" cy="{y+39}" r="22" fill="{ICE}" fill-opacity=".08" stroke="{ICE}" stroke-opacity=".5"/>'
    b+=t(x+w-42,y+46,f'{index:02d}',17,ICE,'700',0,'middle')
    fontsize=22 if len(title)>17 else (25 if len(title)>14 else 28)
    b+=t(x+26,y+58,title,fontsize,WHITE,'700',.35)
    b+=t(x+26,y+94,subtitle,19,MUTED,'400',0)
    b+=f'<path d="M{x+20} {y+h-18}h{w-40}" stroke="{GOLD}" stroke-opacity=".18"/>'
    b+=f'<path d="M{x+22} {y+h-18}h108" stroke="{ICE}" stroke-width="3" stroke-opacity=".8"><animate attributeName="stroke-opacity" values=".2;.9;.2" dur="{4+index}s" repeatCount="indefinite"/></path>'
    return b

def stack():
    h=785
    p,q=base('Eight engineering capability groups orbiting a central technology core',h)
    c=t(88,85,'THE TECHNOLOGY CONSTELLATION',38,WHITE,'700',1.5)
    c+=t(91,121,'Eight connected disciplines. One operating mindset.',21,MUTED)
    cx,cy=802,427
    c+='<circle cx="802" cy="427" r="248" fill="#70ADBF" opacity=".13" filter="url(#bigglow)"/>'
    c+=orbital(cx,cy,268,190,52,28,GOLD)+orbital(cx,cy,213,222,39,-35,ICE)
    # multi-plate visual with floating wire-frame
    c+=monolith(cx,cy,0.66)
    c+=t(cx,637,'CAPABILITIES',28,WHITE,'700',3,'middle')
    c+=t(cx,671,'ARCHITECTURE • DELIVERY • OPERATIONS',16,GOLD,'600',1,'middle')
    data=[
        ('FRONTEND','React  ·  Next.js'),
        ('BACKEND','PHP  ·  Laravel'),
        ('DATA & CLOUD','PostgreSQL  ·  Redis'),
        ('MOBILE','Flutter  ·  Expo'),
        ('INFRASTRUCTURE','Cloudflare  ·  Docker'),
        ('API & INTEGRATIONS','REST  ·  Webhooks'),
        ('SECURITY','Access  ·  Authentication'),
        ('AI & ARCHITECTURE','OpenAI API  ·  n8n'),
    ]
    leftx=72;rightx=1170
    for j,(title,sub) in enumerate(data):
        side=j%2
        k=j//2
        x=leftx if side==0 else rightx
        y=166+k*146
        w=360
        liney=y+56
        xx=x+w if side==0 else x
        destx=665 if side==0 else 940
        c+=f'<path d="M{xx} {liney}Q{(xx+destx)/2:.1f} {liney-24} {destx} {cy}" stroke="{GOLD if side==0 else ICE}" stroke-opacity=".32" fill="none" stroke-dasharray="3 9"/>'
        c+=info_card(x,y,w,114,title,sub,j+1)
        c+=dot(xx,liney,ICE if side else GOLD,3)
    return p+c+q

def venture_card(x,y,w,h,title,role,num,code):
    o=rect(x,y,w,h,22,'#101E2B',GOLD,.49)
    o+=f'<rect x="{x+17}" y="{y+18}" width="124" height="{h-36}" rx="15" fill="url(#glass)" stroke="{ICE}" stroke-opacity=".48"/>'
    # gem-like identity mark
    cx=x+79;cy=y+h/2
    o+=f'<polygon points="{cx},{cy-43} {cx+42},{cy-18} {cx+42},{cy+27} {cx},{cy+48} {cx-42},{cy+27} {cx-42},{cy-18}" fill="none" stroke="{GOLD}" stroke-width="2.4"/>'
    o+=t(cx,cy+12,code,26,WHITE,'700',1,'middle')
    o+=t(x+172,y+53,role,18,GOLD,'600',2)
    o+=t(x+172,y+112,title,30,WHITE,'700')
    o+=t(x+172,y+151,f'LEADERSHIP DOMAIN  /  {num:02d}',16,MUTED,'500',1)
    o+=f'<path d="M{x+172} {y+171}h{w-210}" stroke="{ICE}" stroke-opacity=".3" stroke-width="2"/>'
    o+=f'<circle cx="{x+w-29}" cy="{y+31}" r="6" fill="{GOLD}"><animate attributeName="opacity" values=".25;1;.25" dur="{5+num}s" repeatCount="indefinite"/></circle>'
    return o

def ventures():
    h=654
    p,q=base('Leadership at Saltrixma, SMI, Flunex, and Gate of Scholarships',h)
    c=t(88,82,'FOUR ORGANIZATIONS. CONNECTED LEADERSHIP.',38,WHITE,'700',1)
    c+=t(90,123,'From institutional strategy to digital product delivery.',20,MUTED)
    cards=[
      (85,159,'SALTRIXMA LLC','CHIEF EXECUTIVE OFFICER','SL'),
      (831,159,'SUPERIOR MULTISKILLS','FOUNDER & MANAGING DIRECTOR','SM'),
      (85,392,'FLUNEX INSTITUTE','VICE DIRECTOR','FX'),
      (831,392,'GATE OF SCHOLARSHIPS','FOUNDER','GS'),
    ]
    for i,(x,y,name,role,code) in enumerate(cards):
        c+=venture_card(x,y,681,194,name,role,i+1,code)
    c+=line(798,175,798,586,GOLD,.22,2)
    c+=twinkle(798,358,4,2)
    return p+c+q

def system_card(x,y,title,sub,kind,idx):
    w=355;h=154
    s=rect(x,y,w,h,18,'#101F30',ICE,.42)
    s+=f'<polygon points="{x+w-88},{y+24} {x+w-39},{y+53} {x+w-88},{y+82} {x+w-137},{y+53}" fill="url(#glass)" stroke="{GOLD}" stroke-opacity=".63" stroke-width="1.7"/>'
    s+=f'<path d="M{x+w-137} {y+53}v27l49 28 49-28v-27" fill="none" stroke="{ICE}" stroke-opacity=".48" stroke-width="1.7"/>'
    s+=t(x+24,y+44,f'0{idx}   /   {kind}',15,GOLD,'600',1.7)
    s+=t(x+24,y+92,title,27,WHITE,'700')
    s+=t(x+24,y+126,sub,17,MUTED)
    s+=f'<circle cx="{x+20}" cy="{y+20}" r="4" fill="{GOLD}"><animate attributeName="opacity" values=".25;1;.25" dur="{4+idx}s" repeatCount="indefinite"/></circle>'
    return s

def systems():
    h=692
    p,q=base('Four featured systems: QADHA, MIYTO, SMI Digital Operations, AIU Smart HR',h)
    c=t(88,81,'SYSTEMS IN MOTION',39,WHITE,'700',2)
    c+=t(88,118,'Product direction, educational operations, architecture and accountable delivery.',20,MUTED)
    cx,cy=802,389
    c+='<circle cx="802" cy="389" r="238" fill="#D9B76E" opacity=".1" filter="url(#bigglow)"/>'
    c+=orbital(cx,cy,230,151,40,-22,GOLD)+orbital(cx,cy,176,213,33,30,ICE)
    c+=monolith(cx,cy,.61)
    c+=t(cx,619,'STRATEGY → SYSTEMS → EVIDENCE',18,GOLD,'600',2,'middle')
    records=[
        (90,190,'QADHA','Social product / battle rules','PRODUCT'),
        (1155,190,'MIYTO','Audio-first learning rooms','EDUCATION'),
        (90,432,'SMI OPERATIONS','Connected academic workflows','OPERATIONS'),
        (1155,432,'AIU SMART HR','Academic HR/NLP design','ACADEMIC'),
    ]
    for i,(x,y,title,sub,kind) in enumerate(records):
        c+=system_card(x,y,title,sub,kind,i+1)
        start=x+355 if x<800 else x
        finish=660 if x<800 else 944
        c+=f'<path d="M{start} {y+77}Q{(start+finish)/2} {y+77} {finish} {cy}" stroke="{GOLD if x<800 else ICE}" stroke-opacity=".4" stroke-width="2" fill="none"/>'
        c+=dot(start,y+77,ICE if x>800 else GOLD,3)
    return p+c+q

def still(svg):
    # motion-safe asset; preserve the original composition but remove SMIL nodes.
    return re.sub(r'<animate(?:Transform|Motion)?\b[^>]*/>', '', svg)

for name,render in [('hero-executive',hero),('stack-constellation',stack),('ventures-architected',ventures),('systems-atlas',systems)]:
    s=render()
    (OUT/f'{name}.svg').write_text(s,encoding='utf-8')
    (OUT/f'{name}-still.svg').write_text(still(s),encoding='utf-8')
    print(name, 'dynamic bytes',len(s), 'still bytes',len(still(s)))
print('CREATED:',len(list(OUT.glob('*.svg'))),'original vector assets')
