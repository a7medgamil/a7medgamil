#!/usr/bin/env python3
"""Original premium isometric cube architecture for Ahmed's GitHub profile.
Native SVG/SMIL only: no external image hosts, JavaScript, or copied artwork.
Large modular blocks, precise three-face projection, architectural lighting.
"""
from pathlib import Path
from html import escape
import math, re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets'/'isometric-cubes'
OUT.mkdir(parents=True,exist_ok=True)
KX=math.cos(math.radians(30))
KY=.34
KZ=.76
PALETTE={
 'violet':'#8066FF','blue':'#397CF6','cyan':'#31C9E8','teal':'#22B8A5',
 'gold':'#D7B16D','ice':'#9CDDF5','indigo':'#5869D9','emerald':'#28B98C',
 'rose':'#B77DDB','white':'#DDE8F8'
}
def rgb(h): return tuple(int(h.lstrip('#')[i:i+2],16) for i in (0,2,4))
def shade(h,f):
    return '#'+''.join(f'{max(0,min(255,int(v*f))):02x}' for v in rgb(h))
def mix(a,b,t):
    aa,bb=rgb(a),rgb(b)
    return '#'+''.join(f'{int(x+(y-x)*t):02x}' for x,y in zip(aa,bb))
def P(x,y,z,s,ox,oy):
    return (ox+(x-y)*KX*s, oy+(x+y)*KY*s-z*KZ*s)
def pts(seq):
    return ' '.join(f'{x:.1f},{y:.1f}' for x,y in seq)
def path(seq):
    return 'M '+' L '.join(f'{x:.1f} {y:.1f}' for x,y in seq)
def text(x,y,t,size=14,fill='#E7EDFA',anchor='middle',font='Inter,Segoe UI,Arial,sans-serif',weight=600,spacing=0,opacity=1):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{spacing}" opacity="{opacity}">{escape(t)}</text>')
def defs(tag, mobile=False):
    return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
 <stop offset="0" stop-color="#070D1B"/><stop offset=".52" stop-color="#0B1023"/><stop offset="1" stop-color="#11132B"/>
</linearGradient>
<radialGradient id="glowV"><stop offset="0" stop-color="#745BFF" stop-opacity=".25"/><stop offset="1" stop-color="#745BFF" stop-opacity="0"/></radialGradient>
<radialGradient id="glowC"><stop offset="0" stop-color="#28C9E8" stop-opacity=".18"/><stop offset="1" stop-color="#28C9E8" stop-opacity="0"/></radialGradient>
<radialGradient id="glowG"><stop offset="0" stop-color="#D7B16D" stop-opacity=".13"/><stop offset="1" stop-color="#D7B16D" stop-opacity="0"/></radialGradient>
<linearGradient id="edgeLight" x1="0" y1="0" x2="1" y2="1">
 <stop offset="0" stop-color="#E4D2A2"/><stop offset=".42" stop-color="#72D9F0"/><stop offset="1" stop-color="#8A70FF"/>

</linearGradient>
<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
 <stop offset="0" stop-color="#A99BFF"/><stop offset=".48" stop-color="#66D9EE"/><stop offset="1" stop-color="#D8B779"/>


</linearGradient>
<filter id="glow" x="-80%" y="-80%" width="260%" height="260%">
 <feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="softShadow" x="-60%" y="-60%" width="220%" height="220%">
 <feGaussianBlur stdDeviation="9"/>
</filter>
<pattern id="microgrid" width="38" height="38" patternUnits="userSpaceOnUse">
 <path d="M38 0H0V38" fill="none" stroke="#7E8DB8" stroke-opacity=".055" stroke-width=".8"/>
</pattern>
</defs>'''
def bg(w,h,tag):
    return (f'<rect width="{w}" height="{h}" fill="url(#bg)"/>'
            f'<rect width="{w}" height="{h}" fill="url(#microgrid)"/>'
            f'<ellipse cx="{w*.70:.0f}" cy="{h*.52:.0f}" rx="{w*.37:.0f}" ry="{h*.53:.0f}" fill="url(#glowV)"/>'
            f'<ellipse cx="{w*.87:.0f}" cy="{h*.79:.0f}" rx="{w*.25:.0f}" ry="{h*.32:.0f}" fill="url(#glowC)"/>'
            f'<ellipse cx="{w*.22:.0f}" cy="{h*.88:.0f}" rx="{w*.25:.0f}" ry="{h*.28:.0f}" fill="url(#glowG)"/>'
            f'<path d="M0 {h-1}H{w}" stroke="#65759E" stroke-opacity=".18"/>')
def svg_start(w,h,title,animated):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">Large premium isometric cubic architecture with three dimensional shaded faces, modular block geometry and restrained luminous accents.</desc>',
            defs(title),bg(w,h,title)]
def grid_floor(w,h,s,ox,oy,cols=12,rows=8):
    out=[]
    for i in range(cols+1):
        a=P(i-cols/2, -rows/2,0,s,ox,oy);b=P(i-cols/2,rows/2,0,s,ox,oy)
        out.append(f'<path d="M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}" stroke="#91A4D1" stroke-opacity=".12" stroke-width=".8"/>')
    for j in range(rows+1):
        a=P(-cols/2,j-rows/2,0,s,ox,oy);b=P(cols/2,j-rows/2,0,s,ox,oy)
        out.append(f'<path d="M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}" stroke="#91A4D1" stroke-opacity=".12" stroke-width=".8"/>')
    return ''.join(out)
def cube(x,y,z,w,d,h,color,s,ox,oy,idx,animated=True,stroke=True,detail=True):
    # Three accurately projected faces, with different directional shading.
    a=P(x,y,z+h,s,ox,oy);b=P(x+w,y,z+h,s,ox,oy)
    c=P(x+w,y+d,z+h,s,ox,oy);dd=P(x,y+d,z+h,s,ox,oy)
    ab=P(x+w,y,z,s,ox,oy);cb=P(x+w,y+d,z,s,ox,oy);db=P(x,y+d,z,s,ox,oy)
    top=[a,b,c,dd];right=[b,ab,cb,c];front=[dd,db,cb,c]
    light=mix(color,'#FFFFFF',.25);mid=shade(color,.72);dark=shade(color,.39)
    edge=mix(color,'#DCE8FA',.62) if stroke else color
    sw=1.8 if stroke else .8
    op='1'
    key=f'{idx}-{round(ox)}-{round(oy)}'
    out=[f'<g id="cube-{key}"><defs>'
         f'<linearGradient id="top-{key}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{mix(color,"#FFFFFF",.36)}"/><stop offset=".52" stop-color="{light}"/><stop offset="1" stop-color="{color}"/></linearGradient>'
         f'<linearGradient id="front-{key}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{mid}"/><stop offset="1" stop-color="{shade(color,.30)}"/></linearGradient>'
         f'<linearGradient id="right-{key}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{shade(color,.83)}"/><stop offset="1" stop-color="{shade(color,.45)}"/></linearGradient>'
         '</defs>']
    if animated:
        out.append(f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -2.4;0 0" dur="{7+(idx%4)*.8:.1f}s" begin="{idx*.27:.2f}s" repeatCount="indefinite"/>')
    # cast shadow on the architectural ground
    shadow=P(x+w*.5,y+d*.5,0,s,ox,oy)
    out.append(f'<ellipse cx="{shadow[0]:.1f}" cy="{shadow[1]+8:.1f}" rx="{(w+d)*s*.30:.1f}" ry="{s*.19:.1f}" fill="#02040C" opacity=".48" filter="url(#softShadow)"/>')
    out.append(f'<polygon points="{pts(front)}" fill="url(#front-{key})" stroke="{edge}" stroke-opacity=".46" stroke-width="{sw}" stroke-linejoin="round"/>')
    out.append(f'<polygon points="{pts(right)}" fill="url(#right-{key})" stroke="{edge}" stroke-opacity=".50" stroke-width="{sw}" stroke-linejoin="round"/>')
    out.append(f'<polygon points="{pts(top)}" fill="url(#top-{key})" stroke="{edge}" stroke-opacity=".90" stroke-width="{sw}" stroke-linejoin="round"/>')
    # A recessed architectural top panel and a controlled light edge.
    if detail:
        def inset(polypts,f):
            cx=sum(q[0] for q in polypts)/4;cy=sum(q[1] for q in polypts)/4
            return [(cx+(q[0]-cx)*f,cy+(q[1]-cy)*f) for q in polypts]
        out.append(f'<polygon points="{pts(inset(top,.80))}" fill="none" stroke="#F0F5FF" stroke-opacity=".34" stroke-width="1.05"/>')
        out.append(f'<polygon points="{pts(inset(front,.80))}" fill="#08101F" fill-opacity=".13" stroke="#D9E8FF" stroke-opacity=".19" stroke-width=".85"/>')
        out.append(f'<path d="M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}L{c[0]:.1f} {c[1]:.1f}" fill="none" stroke="url(#edgeLight)" stroke-width="2.2" stroke-linecap="round" opacity=".8"/>')
        # Fine architectural seams create the language of a machined modular structure
        seam0=P(x+w*.52,y+d,z+h*.10,s,ox,oy);seam1=P(x+w*.52,y+d,z+h*.87,s,ox,oy)
        out.append(f'<path d="M{seam0[0]:.1f} {seam0[1]:.1f}L{seam1[0]:.1f} {seam1[1]:.1f}" stroke="#C8D9FA" stroke-opacity=".16" stroke-width=".9"/>')
    # moving light packet travels over one exposed edge
    if animated:
        out.append(f'<path d="M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}L{c[0]:.1f} {c[1]:.1f}" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-dasharray="20 160" opacity=".0"><animate attributeName="stroke-dashoffset" values="180;0" dur="5.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.55;0" dur="5.8s" repeatCount="indefinite"/></path>')
    out.append('</g>')
    return ''.join(out)
def cube_cluster(cx,basey,s,blocks,animated=True):
    # blocks = (dx,dy,dz,w,d,h,color)
    out=[]
    for i,b in enumerate(blocks):
        dx,dy,dz,w,d,h,col=b
        out.append(cube(dx,dy,dz,w,d,h,col,s,cx,basey,i+1,animated))
    return ''.join(out)
def connector(p0,p1,color='#6DD8ED',idx=0,animated=True):
    x0,y0=p0;x1,y1=p1
    out=[f'<path d="M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}" fill="none" stroke="{color}" stroke-width="1.5" stroke-opacity=".45" stroke-dasharray="5 8"/>']
    if animated:
        out.append(f'<path d="M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}" fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="12 180" opacity=".8"><animate attributeName="stroke-dashoffset" values="192;0" dur="{3.8+idx*.4:.1f}s" repeatCount="indefinite"/></path>')
    return ''.join(out)
def cube_center(cx,basey,s,w,d,h,col,idx,animated=True):
    return cube(-w/2,-d/2,0,w,d,h,col,s,cx,basey,idx,animated)
def section_heading(out,w,tag,subtitle,small=False):
    out.append(text(56,48,tag,11,'#83D8EC','start','JetBrains Mono,Consolas,monospace',700,2.2,.95))
    out.append(text(56,76,subtitle,22,'#EAF0FB','start','Inter,Segoe UI,Arial,sans-serif',700,.2,.98))
    out.append(f'<path d="M56 91H{w-56}" stroke="#7788B7" stroke-opacity=".2"/>')
def hero(mobile,animated):
    if mobile:
        w,h=760,650;s=68;ox=390;oy=520
        o=svg_start(w,h,'Ahmed Abdulbari — Executive Isometric Cube Architecture',animated)
        o.append(text(44,65,'AHMED ABDULBARI',31,'url(#shine)','start','Inter,Segoe UI,Arial,sans-serif',800,1.1))
        o.append(text(46,98,'FOUNDER  /  CEO  /  DIGITAL SYSTEMS',12,'#B5C4E2','start','JetBrains Mono,Consolas,monospace',600,1.3))
        o.append(f'<path d="M46 119H290" stroke="url(#edgeLight)" stroke-width="2"/>')
        blocks=[(-1.45,-1.05,0,2.8,2.5,.68,'#273F79'),
                (-1.15,-.75,.68,2.05,2.0,2.2,'#6556CF'),
                (1.02,-.55,.68,1.35,1.65,1.55,'#267DBB'),
                (-1.65,1.05,.68,1.35,1.25,1.25,'#1A8E9C'),
                (.12,1.1,.68,1.55,1.45,1.1,'#8066D8'),
                (-.05,-.3,2.88,1.2,1.2,1.2,'#B08A50'),
                (-2.55,-.55,0,1.35,1.45,1.9,'#4855A8'),
                (2.45,-.55,0,1.35,1.4,2.05,'#246FAD'),
                (-.82,2.18,.68,1.35,1.15,.86,'#187F8D')]
        o.append(cube_cluster(ox,oy,s,blocks,animated))
        # Keep the monumental cube assembly unobstructed on narrow screens.
        o.append('</svg>');return ''.join(o)
    w,h=1200,380;s=68;ox=890;oy=255
    o=svg_start(w,h,'Ahmed Abdulbari — Executive Isometric Cube Architecture',animated)
    o.append(text(64,87,'AHMED ABDULBARI',39,'url(#shine)','start','Inter,Segoe UI,Arial,sans-serif',800,1.0))
    o.append(text(67,119,'FOUNDER  /  CEO  /  DIGITAL SYSTEMS',12,'#B9C7E2','start','JetBrains Mono,Consolas,monospace',650,1.7))
    o.append(f'<path d="M67 142H400" stroke="url(#edgeLight)" stroke-width="2.2"/>')
    o.append(text(67,188,'Strategy translated into',23,'#E8EEF9','start','Inter,Segoe UI,Arial,sans-serif',500,.1))
    o.append(text(67,219,'systems that work.',27,'#D7C08F','start','Inter,Segoe UI,Arial,sans-serif',750,.1))
    o.append(text(68,264,'TECHNOLOGY  ·  INSTITUTIONS  ·  EXECUTION',10,'#8394B8','start','JetBrains Mono,Consolas,monospace',600,1.2))
    o.append(grid_floor(w,h,38,890,340,12,5))
    blocks=[(-1.55,-1.05,0,3.0,2.6,.72,'#263F79'),
            (-1.22,-.78,.72,2.12,2.0,2.2,'#6756D2'),
            (1.00,-.54,.72,1.55,1.68,1.55,'#287FB8'),
            (-1.63,1.05,.72,1.5,1.34,1.32,'#168C98'),
            (.12,1.13,.72,1.72,1.5,1.1,'#7D68C8'),
            (-.06,-.27,2.92,1.22,1.2,1.2,'#B18B4E'),
            (-2.55,-.48,0,1.35,1.4,1.85,'#4A56AD'),
            (2.38,-.55,0,1.4,1.42,2.0,'#246EA9'),
            (-.82,2.18,.72,1.32,1.15,.82,'#168894')]
    o.append(cube_cluster(ox,oy,s,blocks,animated))
    # A quiet architectural floor grid; the cubic structure remains the sole focal point.
    o.append('</svg>');return ''.join(o)
def ventures(mobile,animated):
    if mobile:
        w,h=760,760;s=56
        o=svg_start(w,h,'Leadership and ventures — four isometric cubic monuments',animated);section_heading(o,w,'02 / LEADERSHIP & VENTURES','Four organizations. One operating vision.')
        specs=[('SALTRIXMA LLC','#B48B51','TECHNOLOGY',0),
               ('SMI','#397CF6','EDUCATION',1),
               ('FLUNEX','#22B8C4','INSTITUTIONAL',2),
               ('SCHOLARSHIPS','#8066FF','OPPORTUNITY',3)]
        for i,(name,col,sub,_) in enumerate(specs):
            row=i//2;cx=205+(i%2)*350;by=285+row*220
            blocks=[(-1.02,-.92,0,2.0,1.82,.50,shade(col,.56)),
                    (-.82,-.68,.5,1.52,1.38,1.42,col),
                    (.72,-.28,.5,.95,1.02,.98,shade(col,1.14)),
                    (-.58,.82,.5,1.10,.90,.78,shade(col,.82))]
            o.append(cube_cluster(cx,by,s,blocks,animated))
            o.append(text(cx,by+62,name,12,'#E6ECF8','middle','JetBrains Mono,Consolas,monospace',750,.9))
            o.append(text(cx,by+81,sub,9,'#92A2C2','middle','JetBrains Mono,Consolas,monospace',550,1.1))
        o.append('</svg>');return ''.join(o)
    w,h=1200,410;s=57
    o=svg_start(w,h,'Leadership and ventures — monumental isometric cube architecture',animated);section_heading(o,w,'02 / LEADERSHIP & VENTURES','Four organizations. One operating vision.')
    specs=[('SALTRIXMA LLC','#B48B51','TECHNOLOGY'),
           ('SMI','#397CF6','EDUCATION'),
           ('FLUNEX','#22B8C4','INSTITUTIONAL'),
           ('SCHOLARSHIPS','#8066FF','OPPORTUNITY')]
    for i,(name,col,sub) in enumerate(specs):
        cx=155+i*298;by=290
        blocks=[(-1.12,-.98,0,2.22,1.96,.52,shade(col,.56)),
                (-.86,-.72,.52,1.62,1.50,1.48,col),
                (.76,-.25,.52,.96,1.06,.98,shade(col,1.16)),
                (-.60,.86,.52,1.12,.88,.78,shade(col,.82))]
        o.append(cube_cluster(cx,by,s,blocks,animated))
        o.append(text(cx,by+48,name,12,'#EAF0FA','middle','JetBrains Mono,Consolas,monospace',750,.7))
        o.append(text(cx,by+66,sub,9,'#92A2C2','middle','JetBrains Mono,Consolas,monospace',550,1.1))
    o.append('</svg>');return ''.join(o)
def systems(mobile,animated):
    if mobile:
        w,h=760,790;s=59
        o=svg_start(w,h,'Featured systems — isometric modular product architectures',animated);section_heading(o,w,'03 / FEATURED SYSTEMS','Products built around real operating needs.')
        specs=[('QADHA','#8066FF',0),('MIYTO SMART ROOMS','#C05DAB',1),('SMI OPERATIONS','#278CBB',2),('AIU SMART HR','#279D84',3)]
        for i,(name,col,_) in enumerate(specs):
            row=i//2;cx=205+(i%2)*350;by=300+row*230
            blocks=[(-1.0,-.86,0,1.95,1.72,.48,shade(col,.55)),
                    (-.80,-.62,.48,1.52,1.24,1.34,col),
                    (.74,-.24,.48,.90,.92,.96,shade(col,1.16)),
                    (-.52,.86,.48,1.06,.88,.74,shade(col,.82))]
            o.append(cube_cluster(cx,by,s,blocks,animated))
            o.append(text(cx,by+55,name,10,'#E8EEF9','middle','JetBrains Mono,Consolas,monospace',750,.5))
        o.append('</svg>');return ''.join(o)
    w,h=1200,430;s=57
    o=svg_start(w,h,'Featured systems — large isometric modular cube structures',animated);section_heading(o,w,'03 / FEATURED SYSTEMS','Distinct products. Connected engineering disciplines.')
    specs=[('QADHA','#8066FF'),('MIYTO SMART ROOMS','#C05DAB'),('SMI OPERATIONS','#278CBB'),('AIU SMART HR','#279D84')]
    for i,(name,col) in enumerate(specs):
        cx=155+i*298;by=315
        blocks=[(-1.10,-.96,0,2.15,1.92,.50,shade(col,.56)),
                (-.86,-.70,.50,1.62,1.38,1.42,col),
                (.78,-.24,.50,.96,1.02,.98,shade(col,1.15)),
                (-.60,.82,.50,1.10,.90,.80,shade(col,.83)),
                (-.92,-.88,1.30,1.02,1.00,.88,shade(col,1.28))]
        o.append(cube_cluster(cx,by,s,blocks,animated))
        o.append(text(cx,by+49,name,10,'#EAF0FA','middle','JetBrains Mono,Consolas,monospace',750,.45))
    o.append('</svg>');return ''.join(o)
def capabilities(mobile,animated):
    if mobile:
        w,h=760,690;s=58;ox=380;by=495
        o=svg_start(w,h,'Capabilities — an integrated modular intelligence cube',animated);section_heading(o,w,'04 / CAPABILITIES','Eight disciplines. One coherent architecture.')
        # A 3x3 modular cube assembly, with one central core and six substantial surrounding blocks.
        blocks=[(-1.35,-1.35,0,1.45,1.45,1.25,'#5869D9'),
                (.10,-1.35,0,1.45,1.45,1.05,'#267EB7'),
                (-1.35,.10,0,1.45,1.45,.95,'#278C9A'),
                (.10,.10,0,1.45,1.45,1.3,'#8066FF'),
                (-.62,-.62,1.3,1.45,1.45,1.35,'#B18B4E'),
                (1.62,-.65,0,1.22,1.30,.92,'#2A7DAD'),
                (-1.50,1.72,0,1.25,1.20,.82,'#267E83'),
                (1.08,.95,1.30,1.10,1.05,.92,'#7A65D0')]
        o.append(cube_cluster(ox,by,s,blocks,animated))
        labels=['PRODUCT STRATEGY','SYSTEMS DESIGN','DIGITAL TRANSFORMATION','TECHNICAL DELIVERY',
                'OPERATIONS','GOVERNANCE','ENGINEERING','EVIDENCE']
        o.append(text(380,635,'  ·  '.join(labels[:4]),8,'#A8B8D5','middle','JetBrains Mono,Consolas,monospace',600,.45))
        o.append(text(380,653,'  ·  '.join(labels[4:]),8,'#A8B8D5','middle','JetBrains Mono,Consolas,monospace',600,.45))
        o.append('</svg>');return ''.join(o)
    w,h=1200,430;s=62;ox=620;by=320
    o=svg_start(w,h,'Capabilities — integrated modular intelligence cube architecture',animated);section_heading(o,w,'04 / CAPABILITIES','Eight disciplines. One coherent architecture.')
    # Monumental modular cubic structure, intentionally sparse and architectural.
    blocks=[(-1.55,-1.45,0,1.65,1.55,1.25,'#5869D9'),
            (.10,-1.45,0,1.65,1.55,1.05,'#267EB7'),
            (-1.55,.10,0,1.65,1.55,.95,'#278C9A'),
            (.10,.10,0,1.65,1.55,1.3,'#8066FF'),
            (-.72,-.68,1.3,1.65,1.55,1.35,'#B18B4E'),
            (1.92,-.65,0,1.35,1.35,.88,'#2A7DAD'),
            (-1.58,1.88,0,1.35,1.25,.82,'#267E83'),
            (1.08,1.00,1.30,1.18,1.12,.94,'#7A65D0')]
    o.append(cube_cluster(ox,by,s,blocks,animated))
    # Eight executive disciplines are presented as restrained editorial labels, not badges.
    left=[('PRODUCT STRATEGY',155,210),('SYSTEMS DESIGN',155,258),('DIGITAL TRANSFORMATION',155,306),('OPERATIONS',155,354)]
    right=[('TECHNICAL DELIVERY',1090,210),('GOVERNANCE',1090,258),('ENGINEERING',1090,306),('EVIDENCE & REVIEW',1090,354)]
    for t,x,y in left:
        o.append(text(x,y,t,10,'#B9C9E5','start','JetBrains Mono,Consolas,monospace',650,.7))
        o.append(f'<path d="M155 {y+10}H340" stroke="#7890BC" stroke-opacity=".22"/>')
    for t,x,y in right:
        o.append(text(x,y,t,10,'#B9C9E5','end','JetBrains Mono,Consolas,monospace',650,.7))
        o.append(f'<path d="M860 {y+10}H1090" stroke="#7890BC" stroke-opacity=".22"/>')
    o.append('</svg>');return ''.join(o)
def main():
    scenes={'hero':hero,'ventures':ventures,'systems':systems,'capabilities':capabilities}
    for name,fn in scenes.items():
        for device in ('desktop','mobile'):
            mobile=device=='mobile'
            for mode in ('animated','static'):
                data=fn(mobile,mode=='animated')
                suffix='' if mode=='animated' else '-static'
                path=OUT/f'{name}-{device}{suffix}.svg'
                path.write_text(data,encoding='utf8')
                # Lightweight source assets; GitHub renders the SVG directly.
                assert data.count('<svg ')==1 and data.count('</svg>')==1
                ET.fromstring(data)  # Validate every SVG as well-formed XML before publishing.
                ids=re.findall(r'\bid="([^"]+)"',data)
                assert len(ids)==len(set(ids)),f'duplicate SVG ids in {path.name}'
                assert 'javascript:' not in data.lower() and 'http://' not in data.lower().replace('http://www.w3.org/2000/svg','')
                assert '<animate' not in data if mode=='static' else '<animate' in data
                print(path.name,len(data))
    print('ISOMETRIC_CUBES_COMPLETE',len(list(OUT.glob('*.svg'))))
if __name__=='__main__':main()
