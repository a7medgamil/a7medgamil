"""Chromatic computational geometry. Physical Blender Cycles renders for GitHub README.
Not a collection of trophies, cups, corporate logos, chrome trinkets or plain orbits.
Original mathematical/architectural compositions with distinct 3D mesh construction.
"""
import sys,math,random
from pathlib import Path
from math import sin,cos,pi,sqrt
from mathutils import Vector
BASE=Path(__file__).resolve().parent
SRC=(BASE/'render-studio3d.py').read_text(encoding='utf8')
# Reuse the verified physically based material, lights, camera and modelling primitives.
exec(compile(SRC[:SRC.rindex('\nsetup()\n')],str(BASE/'render-studio3d.py'),'exec'), globals())
ROOT=BASE.parent
OUTPUT=ROOT/'assets'/'geometric-intelligence'
OUTPUT.mkdir(parents=True,exist_ok=True)
R=random.Random(20261122)

# Saturated intellectual palette: distinct functional hues, consistent optical treatment.
CYAN=material('Spectral electric cyan',(.008,.54,.96),.36,.14,.45,emission=.4,coat=.5)
VIOLET=material('Spectral amethyst',(.37,.08,.88),.32,.15,.44,emission=.55,coat=.57)
MAGENTA=material('Chromatic fuchsia',(.88,.06,.40),.24,.13,.48,emission=.50,coat=.60)
EMERALD=material('Electro emerald',(.02,.75,.45),.35,.17,.44,emission=.38,coat=.55)
ORANGE=material('Amber fluorescence',(1.0,.34,.028),.52,.13,.26,emission=.55,coat=.4)
BLUE=material('Cobalt iridescence',(.04,.24,.97),.45,.14,.42,emission=.35,coat=.56)
LIME=material('Spectral lime',(.56,.89,.04),.22,.16,.30,emission=.35,coat=.50)
PALE=material('Prismatic silver',(.54,.82,1.0),.72,.13,.20,emission=.15,coat=.65)
AURUM=material('Precision gold',(.95,.61,.16),.93,.15,.05,coat=.52)
VOID=material('Black ceramic foundation',(.009,.013,.034),.69,.12,coat=.55)
FLOOR=material('Deep midnight cobalt',(0.008,.011,.041),.60,.18,coat=.52)
GLOW_C=material('Linear cyan light',(.09,.75,1.0),0,.20,emission=3.8)
GLOW_M=material('Linear amethyst light',(.77,.15,1),0,.20,emission=3.8)
GLOW_G=material('Linear mint light',(.03,1,.56),0,.20,emission=3.2)
GLOW_O=material('Linear amber light',(1,.56,.10),0,.2,emission=3.7)
PALETTE=[CYAN,VIOLET,MAGENTA,EMERALD,ORANGE,BLUE,LIME,PALE]
GLOW=[GLOW_C,GLOW_M,GLOW_O,GLOW_G]

def obj_mesh(name, verts, faces, mat, solid=.016, bevel=.008):
    me=bpy.data.meshes.new(name+' mesh')
    me.from_pydata(verts,[],faces);me.update()
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob)
    assign(ob,mat)
    if solid:
        so=ob.modifiers.new('Physical laminar metal thickness','SOLIDIFY');so.thickness=solid
    if bevel:
        be=ob.modifiers.new('Catchlight softening','BEVEL');be.width=bevel;be.segments=2
        ob.modifiers.new('Corner normal weighting','WEIGHTED_NORMAL')
    return ob

def polyhedron(name,pos,r,mat,sub=1,wire=None):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=r,location=pos)
    ob=bpy.context.object;ob.name=name;assign(ob,mat)
    bevel=ob.modifiers.new('Precisely bevel each polygon','BEVEL')
    bevel.width=.025 if sub<=1 else .014;bevel.segments=2
    ob.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    if wire:
        for index,e in enumerate(ob.data.edges):
            p=ob.matrix_world@ob.data.vertices[e.vertices[0]].co
            q=ob.matrix_world@ob.data.vertices[e.vertices[1]].co
            line(name+' • geodesic edge '+str(index),[p,q],.013,wire)
    return ob

def helical(name,center,r0,r1,z0,z1,turns,mat,thickness=.02,phase=0,segments=270):
    ps=[]
    for i in range(segments+1):
        t=i/segments
        r=r0+(r1-r0)*t
        a=turns*2*pi*t+phase
        ps.append((center[0]+r*cos(a),center[1]+r*sin(a)*.45,center[2]+z0+(z1-z0)*t))
    return line(name,ps,thickness,mat)

def ribbon(name,center,radius,width,height,material,turns=2,phase=0):
    v=[];f=[];N=160
    for i in range(N+1):
        t=i/N;a=turns*2*pi*t+phase;r=radius*(.75+.28*sin(2*pi*t))
        mid=Vector((center[0]+r*cos(a),center[1]+r*sin(a)*.48,center[2]+height*(t-.5)))
        tang=Vector((-.86*sin(a),.44*cos(a),height/(max(1,turns)*2*pi)));tang.normalize()
        normal=tang.cross(Vector((.1,.7,.6)));normal.normalize()
        w=width*(.4+.6*sin(pi*t)**.8)
        a1=mid+normal*w;a2=mid-normal*w
        v.extend([tuple(a1),tuple(a2)])
        if i<N:f.append((2*i,2*i+1,2*i+3,2*i+2))
    return obj_mesh(name,v,f,material,.038,.012)

def cube_frame(name,loc,dims,mat,beam=.016):
    x,y,z=loc;dx,dy,dz=[p/2 for p in dims]
    vv=[(x+sx*dx,y+sy*dy,z+sz*dz) for sx in [-1,1] for sy in [-1,1] for sz in [-1,1]]
    edges=[]
    for i in range(8):
        for j in range(i+1,8):
            if sum(a!=b for a,b in zip([i>>2&1,i>>1&1,i&1],[j>>2&1,j>>1&1,j&1]))==1:
                edges.append((i,j))
    for n,(i,j) in enumerate(edges):
        line(name+' precision extrusion '+str(n),[vv[i],vv[j]],beam,mat)

def lattice(name,center,rings,vertices,mat,level=.18):
    for k in range(rings):
        z=center[2]+(k-(rings-1)/2)*level
        ps=[]
        radius=.58+.10*sin(pi*k/max(1,rings-1))
        for j in range(vertices+1):
            a=j*2*pi/vertices+.10*k
            ps.append((center[0]+radius*cos(a),center[1]+radius*sin(a),z))
        line(name+' ring '+str(k),ps,.014,mat)
    for j in range(vertices):
        ps=[]
        for k in range(rings):
            a=j*2*pi/vertices+.10*k;rad=.58+.10*sin(pi*k/max(1,rings-1))
            z=center[2]+(k-(rings-1)/2)*level
            ps.append((center[0]+rad*cos(a),center[1]+rad*sin(a),z))
        line(name+' longitudinal arc '+str(j),ps,.014,mat)

def toroid_chromatic(name,loc,r,mat,rotation=(.7,.3,.2),minor=.048):
    return torus(name,loc,r,minor,mat,rot=rotation)

def bezel(name,loc,r,mat,glow):
    x,y,z=loc
    cyl(name+' graphite architectural plinth',(x,y,z-.16),r,.24,VOID,bevel=.07)
    torus(name+' illuminated edge',(x,y,z-.02),r*.90,.022,glow)
    torus(name+' satin gold fastening',(x,y,z+.04),r*.77,.014,AURUM)
    cyl(name+' stepped insert',(x,y,z+.02),r*.79,.10,mat,bevel=.027)

def floating_particles(center,seed,n=22,rr=2.2):
    rng=random.Random(seed)
    for i in range(n):
        a=rng.random()*2*pi;v=(rng.random()-.5)*2
        radius=rr*(.52+.57*rng.random())
        pos=(center[0]+radius*cos(a),center[1]+radius*sin(a)*.53,center[2]+v*1.35)
        sphere('Floating information mote '+str(seed)+' '+str(i),pos,.025+.022*rng.random(),GLOW[i%4],12)

def intelligence_hero():
    p=(2.65,0,.42)
    # Geometrically complex 'thinking machine': multiple actual nested polyhedral cages
    bezel('Intelligence platform',(p[0],.32,-1.52),1.47,BLUE,GLOW_C)
    for i,mat in enumerate([VIOLET,CYAN,MAGENTA,PALE]):
        o=polyhedron('Recursive nested Platonic intelligence mesh '+str(i),
            (p[0],p[1],p[2]),1.58-i*.30,mat if i==3 else glass,sub=1,wire=[GLOW_M,GLOW_C,GLOW_O,AURUM][i])
        o.rotation_euler=(.1+i*.12,.18+i*.22,.20+i*.37)
    crystal('Inner amethyst computation shard',(p[0],-.12,p[2]),.57,1.76,VIOLET,8)
    sphere('Gold cognitive singularity',(p[0],-.40,p[2]),.27,GLOW_O)
    for i in range(6):
        m=[CYAN,VIOLET,MAGENTA,EMERALD,ORANGE,BLUE][i]
        phase=i*pi/3
        g=crystal('Spectral folding blade '+str(i),(p[0]+1.9*cos(phase),0.18+1.12*sin(phase),p[2]+.69*sin(phase*2)),.30,.98,m,6)
        g.rotation_euler=(.25, .2,i*pi/6)
        line('Cognitive graph edge '+str(i),[(p[0],-.15,p[2]),g.location],.018,[GLOW_C,GLOW_M,GLOW_O,GLOW_G][i%4])
    for i,m in enumerate([CYAN,MAGENTA,AURUM]):
        ribbon('Physical prismatic ribbon '+str(i),p,2.06+i*.20,.16,.72,m,turns=1.7,phase=i*1.8)
    for i in range(2):
        toroid_chromatic('Physical elliptic architecture '+str(i),p,2.24+i*.26,[AURUM,GLOW_C][i],(.9+i*.14,.22,.4+i*.88),.027)
    helical('Recursive DNA / algorithm helix',p,.60,1.7,-1.28,1.24,2.1,GLOW_M,.022)
    helical('Counterphase algorithm helix',p,1.7,.60,-1.22,1.22,-2.1,GLOW_C,.023,phase=pi)
    floating_particles(p,11,30,2.6)

def monument(x,idx):
    p=(x,0,.27)
    mat=[ORANGE,VIOLET,CYAN,EMERALD][idx]
    glow=[GLOW_O,GLOW_M,GLOW_C,GLOW_G][idx]
    bezel('Organization datum '+str(idx),(x,.1,-1.53),1.00,mat,glow)
    if idx==0:
        # Saltrixma — computational invention: interlocked asymmetric icosahedra
        for k in range(3):
            v=polyhedron('Saltrixma fractured architectural topology '+str(k),
             (x+(.16*k-.18),0,.1+k*.25),1.04-.23*k,[ORANGE,VIOLET,PALE][k],sub=1,wire=[AURUM,GLOW_O,GLOW_M][k])
            v.rotation_euler=(.12+k*.28,.33+k*.17,.25+k*.63)
        ribbon('Signal to system transformation',p,1.32,.14,1.2,AURUM,turns=1.6)
    if idx==1:
        # SMI — layered academia as multifaceted knowledge convergence
        crystal('Sapphire education knowledge prism',(x,0,.22),1.10,3.18,BLUE,10)
        for k in range(3):
            cube_frame('Education knowledge scaffold '+str(k),
                (x,0,.24),(.85+k*.42,.85+k*.42,2.25-k*.42),[GLOW_C,GLOW_M,AURUM][k],.018)
        toroid_chromatic('Academic light ring',p,1.3,AURUM,(.63,.14,.13),.038)
        polyhedron('Mentorship nucleus',p,.46,PALE,1,wire=GLOW_M)
    if idx==2:
        # Flunex — continuous parametric folded metal architecture
        for k in range(3):
            ribbon('Algorithmic sculpted parametric flow '+str(k),
                (x,0,.25),1.12+k*.16,.26,1.66,[CYAN,PALE,BLUE][k],turns=1.1,phase=k*1.5)
        for j in range(3):
            helical('Flunex optimization filament '+str(j),p,.48,1.08,-1.0,1,1.8,GLOW_C,.018,phase=j*2*pi/3)
        sphere('Flunex technological nucleus',(x,0,.25),.46,VIOLET)
    if idx==3:
        # Scholarship Gateway — 3D mathematically nested portals
        for k in range(4):
            oo=cube('Nested educational gateway '+str(k),(x,.05*k,.26),(1.52-.27*k,.12,2.44-.35*k),
                [EMERALD,PALE,CYAN,AURUM][k],.035)
            oo.rotation_euler[1]=k*.08
            cube_frame('Prismatic gateway extrusion '+str(k),(x,-.2*k,.25),
                (1.5-.19*k,.7,2.35-.27*k),[GLOW_G,GLOW_C,AURUM,EMERALD][k],.022)
        crystal('Opportunity core',(x,-.40,.15),.43,1.20,GLOW_G,6)
    floating_particles(p,100+idx,9,1.25)

def institutions():
    for idx,x in enumerate([-4.55,-1.53,1.53,4.55]):monument(x,idx)

def system_design(x,idx):
    p=(x,0,.33);c=[BLUE,MAGENTA,EMERALD,VIOLET][idx];g=[GLOW_C,GLOW_M,GLOW_G,GLOW_O][idx]
    bezel('System node '+str(idx),(x,.05,-1.55),1.00,c,g)
    if idx==0:
        # QADHA: game mechanics / social interactions. No legal imagery or invented claims.
        polyhedron('Social system modular polyhedron',p,1.03,BLUE,1,wire=GLOW_C)
        for k in range(3):
            toroid_chromatic('Competitive mechanics orbital '+str(k),p,1.17+k*.11,[ORANGE,GLOW_C,AURUM][k],(.75,.35,.6+k*.81),.026)
        for k in range(6):
            a=k*pi/3;sphere('Social activity node',(x+.84*cos(a),-.35,.33+.84*sin(a)),.085,[ORANGE,PALE][k%2],14)
    if idx==1:
        sphere('Audio room nucleus',p,.93,MAGENTA)
        for k in range(4):
            toroid_chromatic('Communication resonance waveform '+str(k),p,.88+k*.19,
            [GLOW_M,PALE,GLOW_C,AURUM][k],(pi/2+.1*k,.0,.02*k),.025)
        for j in range(14):
            a=j*2*pi/14;h=.42+.30*sin(j*3.2)**2
            crystal('Sound intensity frequency bar '+str(j),(x+1.1*cos(a),.05,.32+1.1*sin(a)),.060,h,
                    [MAGENTA,CYAN,PALE][j%3],5)
    if idx==2:
        for i in range(3):
            for j in range(3):
                q=(x+(i-1)*.58,.12+(j-1)*.32,.30+(i+j)*.19)
                cube('Academic process cell '+str(i)+str(j),q,(.42,.40,.42),
                    [EMERALD,CYAN,PALE][(i+j)%3],.045)
                cube_frame('Digital operations data bus '+str(i)+str(j),q,(.48,.48,.49),GLOW_G,.013)
        for k in range(3):
            helical('Infrastructure choreography '+str(k),p,.9,.63,-.5,.65,1.4,[GLOW_G,GLOW_C,AURUM][k],.014,phase=k*2*pi/3)
    if idx==3:
        polyhedron('AIU decision nucleus',p,.70,VIOLET,2,wire=PALE)
        # neural network: graph with three layers of true geometry
        L=[]
        for i,(n,z) in enumerate([(4,-.78),(6,.18),(4,1.06)]):
            for j in range(n):
                a=2*pi*j/n
                xx=x+.86*cos(a);yy=.24+.50*sin(a)
                pos=(xx,yy,z+.12)
                sphere('AI reasoning token '+str(i)+' '+str(j),pos,.12,[MAGENTA,CYAN,PALE][i],16)
                L.append(pos)
                if i>0:
                    line('Reasoning network connection',[(x,-.1,.3),pos],.012,GLOW_M)
        toroid_chromatic('Learning representation ring',p,1.34,GLOW_M,(.75,.2,.1),.018)
    floating_particles(p,200+idx,6,1.3)

def systems():
    for idx,x in enumerate([-4.55,-1.53,1.53,4.55]):system_design(x,idx)

def capability_orbit():
    p=(2.48,0,.36)
    bezel('Integrated engineering platform',(p[0],0,-1.57),1.55,BLUE,GLOW_C)
    polyhedron('Architecture computational network',p,1.22,VIOLET,2,wire=GLOW_C)
    polyhedron('Convergent decision model',p,.74,EMERALD,1,wire=AURUM)
    sphere('Computationally active core',(p[0],-.4,p[2]),.32,GLOW_O)
    n=8
    for i in range(n):
        a=i*2*pi/n
        x=p[0]+2.10*cos(a)
        y=.04+.85*sin(a)
        z=p[2]+1.40*sin(a+.32)
        q=(x,y,z)
        g=polyhedron('Distinct skill code-cell '+str(i),q,.36,[CYAN,BLUE,VIOLET,MAGENTA,ORANGE,EMERALD,LIME,PALE][i],1,wire=[AURUM,GLOW_M,GLOW_C,GLOW_G][i%4])
        g.rotation_euler=(.12*i,.09*i,.29*i)
        line('Knowledge network path '+str(i),[(p[0],p[1],p[2]),q],.015,[GLOW_M,GLOW_C,GLOW_G,GLOW_O][i%4])
        sphere('Independent illuminated intelligence point '+str(i),q,.073,GLOW[i%4],16)
    for k in range(3):
        ribbon('Synthesis of disciplines geometric surface '+str(k),p,2.15+k*.12,.15,.85,
               [CYAN,VIOLET,AURUM][k],turns=1.2,phase=2*pi*k/3)
    floating_particles(p,314,24,2.3)

def setup_chromatic():
    setup()
    scene=bpy.context.scene
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGB'
    scene.render.filepath=str(OUTPUT/(SCENE+'-render.png'))
    scene.render.image_settings.color_depth='8'
    # clear studio color language, saturated color with realistic metal and glass
    for ob in list(bpy.data.objects):
        if ob.name.startswith('Polished midnight mirror floor') and ob.type=='MESH':
            ob.data.materials.clear();assign(ob,FLOOR)
    scene.world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.006,.009,.035,1)
    area('Blue architectural softbox',(0,-4,7),1350,(.12,.48,1),7)
    area('Violet optical rim',(6,3,4),1350,(.71,.19,1),5)
    area('Emerald fill',(-5,0,3),800,(.06,1,.62),5)
    area('Warm cinematic key',(0,1,9),950,(1,.65,.33),7)
    cam=scene.camera
    cam.data.ortho_scale=13.7
    scene.render.resolution_y=round(WIDTH*.51)
    scene.cycles.samples=SAMPLES
    scene.cycles.use_denoising=True
    print('CHROMATIC_STUDIO_SETUP',SCENE,'materials',len(bpy.data.materials))

setup_chromatic()
if SCENE=='hero':intelligence_hero()
elif SCENE=='ventures':institutions()
elif SCENE=='systems':systems()
elif SCENE=='skills':capability_orbit()
else:raise ValueError(SCENE)
bpy.ops.render.render(write_still=True)
print('GEOMETRIC_INTELLIGENCE_RENDER_COMPLETE',SCENE,bpy.context.scene.render.filepath)
