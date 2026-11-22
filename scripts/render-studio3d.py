"""Actual Blender 4.5 physically rendered 3D artwork for Ahmed's GitHub.
Use: blender -b --python scripts/render-studio3d.py -- hero 1200 22
No outside models or brands, no private data.
"""
import bpy, math, random, os, sys
from mathutils import Vector
from pathlib import Path
from math import pi, sin, cos

ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
SCENE=ARGS[0] if ARGS else 'hero'
WIDTH=int(ARGS[1]) if len(ARGS)>1 else 1280
SAMPLES=int(ARGS[2]) if len(ARGS)>2 else 16
OUTPUT=Path(__file__).resolve().parent.parent/'assets'/'studio3d'
OUTPUT.mkdir(parents=True,exist_ok=True)
R=random.Random(7484)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def material(name, color, metallic=0.0, roughness=.3, transmission=0, emission=0, coat=0):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metallic
    bs.inputs['Roughness'].default_value=roughness
    if 'Transmission Weight' in bs.inputs: bs.inputs['Transmission Weight'].default_value=transmission
    if 'Coat Weight' in bs.inputs: bs.inputs['Coat Weight'].default_value=coat
    if emission:
        bs.inputs['Emission Color'].default_value=(*color,1)
        bs.inputs['Emission Strength'].default_value=emission
    return m

black=material('obsidian ceramic',(.014,.022,.037),.62,.16,coat=.48)
graphite=material('smoked chrome',(.052,.075,.099),.95,.18)
chrome=material('brushed platinum',(.64,.72,.74),.93,.15)
gold=material('Champagne gold',(.74,.47,.20),1,.19)
pale=material('Highlight champagne metal',(.98,.77,.39),.84,.11)
rose=material('warm bronze',(.42,.21,.115),.88,.23)
glass=material('smoked sapphire crystal',(.10,.27,.37),.08,.06,.70,coat=.46)
clear=material('Icy cast glass',(.34,.68,.78),.04,.08,.84,coat=.65)
navy=material('polished midnight floor',(.009,.017,.032),.44,.24,coat=.35)
blue_em=material('Ice emissive',(.20,.70,.96),.16,.26,emission=2.2)
gold_em=material('Warm emissive',(.99,.53,.17),.13,.28,emission=3.2)

def set_smooth(o):
    if o.type=='MESH':
        for poly in o.data.polygons: poly.use_smooth=True
    return o

def assign(o,mat): o.data.materials.append(mat);return o

def cube(name,loc,scale,mat,bevel=.05):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object;o.name=name
    o.dimensions=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel>0:
        mod=o.modifiers.new('Light-catching machined edges','BEVEL');mod.width=bevel;mod.segments=4
        mod.affect='EDGES'
        o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    assign(o,mat)
    return o

def cyl(name,loc,r,depth,mat,vertices=96,bevel=.03):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=loc)
    o=bpy.context.object;o.name=name;assign(o,mat)
    if bevel:
        m=o.modifiers.new('Turned bevel','BEVEL');m.width=bevel;m.segments=3
        o.modifiers.new('Weighted surface normals','WEIGHTED_NORMAL')
    return set_smooth(o)

def sphere(name,loc,r,mat,segments=64):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=32,radius=r,location=loc)
    o=bpy.context.object;o.name=name;assign(o,mat);return set_smooth(o)

def torus(name,loc,major,minor,mat,rot=(0,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_segments=128,minor_segments=14,location=loc,
                                      major_radius=major,minor_radius=minor,rotation=rot)
    o=bpy.context.object;o.name=name;assign(o,mat);return set_smooth(o)

def crystal(name,loc,rad,height,mat,facets=8):
    # truly modelled double-ended faceted gemstone
    verts=[]
    z=loc[2]
    verts.append((loc[0],loc[1],z+height*.55))
    for h,ratio in [(height*.22,.68),(-height*.18,1)]:
        for i in range(facets):
            a=(i+.25)*2*pi/facets
            verts.append((loc[0]+rad*ratio*cos(a),loc[1]+rad*ratio*sin(a),z+h))
    verts.append((loc[0],loc[1],z-height*.56))
    faces=[]
    for i in range(facets):faces.append((0,1+i,1+(i+1)%facets))
    for i in range(facets):faces.append((1+i,facets+1+i,facets+1+(i+1)%facets,1+(i+1)%facets))
    last=1+2*facets
    for i in range(facets):faces.append((last,1+facets+(i+1)%facets,1+facets+i))
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o)
    assign(o,mat)
    return o

def line(name,pts,radius,mat):
    curve=bpy.data.curves.new(name,'CURVE')
    curve.dimensions='3D';curve.resolution_u=24;curve.bevel_depth=radius;curve.bevel_resolution=4
    spline=curve.splines.new('POLY');spline.points.add(len(pts)-1)
    for i,p in enumerate(pts):spline.points[i].co=(*p,1)
    obj=bpy.data.objects.new(name,curve);bpy.context.collection.objects.link(obj);assign(obj,mat)
    return obj

def arc(name,origin,r,a0,a1,plane,material=gold,thickness=.028,steps=96):
    x,y,z=origin
    ps=[]
    for i in range(steps+1):
        ang=a0+(a1-a0)*i/steps
        if plane=='xz':ps.append((x+r*cos(ang),y,z+r*sin(ang)))
        elif plane=='yz':ps.append((x,y+r*cos(ang),z+r*sin(ang)))
        else:ps.append((x+r*cos(ang),y+r*sin(ang),z))
    return line(name,ps,thickness,material)

def frame_prism(x,y,z,w,d,h):
    obj=cube('Smoked diamond core',(x,y,z),(w,d,h),glass,bevel=.17)
    cube('Front energy spine',(x,y-d/2-.018,z),(.035,.04,h*.86),gold_em,bevel=.006)
    cube('Upper machined collar',(x,y,z+h*.45),(w*1.12,d*1.12,.08),gold,bevel=.022)
    cube('Lower machined collar',(x,y,z-h*.45),(w*1.12,d*1.12,.09),gold,bevel=.022)
    return obj

def platform(x,y,width=1.2,height=.27):
    cyl('Floating base - obsidian',(x,y,-1.52),width,height,black,vertices=96,bevel=.07)
    cyl('Gold mechanical inset',(x,y,-1.36),width*.91,.055,gold,bevel=.019)
    cyl('Raised base glass',(x,y,-1.29),width*.83,.13,graphite,bevel=.03)
    torus('trim circumference',(x,y,-1.23),width*.80,.022,pale)

def actual_metal_ribbon(cx,cy,cz,rad=1.3):
    verts=[];faces=[];n=120
    for i in range(n+1):
        a=2*pi*i/n
        mid=(cx+rad*cos(a),cy+.23*sin(2*a),cz+rad*.73*sin(a))
        w=(.16+.055*sin(3*a))
        verts.append((mid[0]+w*cos(a/2),mid[1],mid[2]+w*sin(a/2)))
        verts.append((mid[0]-w*cos(a/2),mid[1],mid[2]-w*sin(a/2)))
        if i<n:faces.append((2*i,2*i+1,2*i+3,2*i+2))
    mesh=bpy.data.meshes.new('Sculpted ribbon mesh')
    mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new('Brushed sculptural metal ribbon',mesh)
    bpy.context.collection.objects.link(o);assign(o,chrome)
    sol=o.modifiers.new('Metal wall thickness','SOLIDIFY');sol.thickness=.075
    bev=o.modifiers.new('Soft machined edge','BEVEL');bev.width=.025;bev.segments=3
    return o

def assemble_hero():
    x=2.75
    platform(x,.28,1.45,.23)
    # iridescent crystalline core surrounded by actual metal frames
    crystal('Main crystal', (x,0,.18),.91,3.40,clear,10)
    crystal('Warm metallic central core',(x,0,.18),.32,2.04,gold,8)
    frame_prism(x,0,.08,1.48,1.4,2.45)
    for z in [-1.10,1.16]:
        torus('rotated steel halo',(x,0,z),.91,.026,chrome)
    for k,(p,r,mat) in enumerate([(0.17,2.23,gold),(-0.25,2.58,chrome),(.6,1.95,pale)]):
        torus('Actual floating orbit '+str(k),(x,0,.25+p),r,.038 if k==0 else .020,mat,
              rot=(1.15+.23*k,.14+.32*k,.48+.7*k))
    arc('Gold orbital segment',(x,0,.20),2.38,-.6,2.1,'xz',gold_em,.020)
    arc('Icy arc flourish',(x,0,.36),2.73,2.6,5.25,'xz',blue_em,.012)
    sphere('Heart of light',(x,0,.23),.19,gold_em)
    for i in range(10):
        a=i*2*pi/10
        sphere('gold orbit bead', (x+2.10*cos(a),.18+1.5*sin(a),.14+(.5*sin(2*a))),.038,gold_em,16)

def assemble_ventures():
    pts=[-4.45,-1.45,1.45,4.45]
    for i,x in enumerate(pts):
        platform(x,.4,.91,.22)
        if i==0:
            frame_prism(x,0,.0,1.08,1.02,2.95)
            for q in range(3): torus('strategic ring',(x,0,-.25+q*.65),.83,.027,gold,rot=(.26,0,.2*q))
            crystal('Saltrixma dark core',(x,0,.35),.44,2.4,chrome)
        elif i==1:
            # floating crystal academic prism, sculpted
            crystal('SMI glass pillar',(x,0,.10),.9,3.3,clear,6)
            crystal('Inner knowledge source',(x,0,.2),.38,2.4,gold,6)
            torus('education orbit',(x,.1,.20),1.32,.035,pale,rot=(1.15,.24,0))
            arc('education energy crown',(x,.1,.1),1.5,.35,2.7,'xz',blue_em,.018)
        elif i==2:
            actual_metal_ribbon(x,0,.18,1.24)
            sphere('Flunex center',(x,0,.2),.54,black)
            crystal('Innovation jewel',(x,-.22,.1),.41,1.5,glass,12)
            torus('Flunex thin accent',(x,.10,.18),1.38,.020,gold,rot=(.9,.21,.14))
        elif i==3:
            torus('Gate of opportunity',(x,0,.20),1.3,.18,gold,rot=(pi/2-.08,.08,.03))
            torus('Gate inset',(x,0,.2),1.01,.065,chrome,rot=(pi/2-.08,.08,.03))
            sphere('Luminous scholarship portal',(x,0,.20),.69,glass)
            crystal('Opportunity source',(x,-.2,.2),.44,1.32,pale,6)
            arc('gateway starlight',(x,0,.2),1.5,-.6,1.3,'xz',blue_em,.021)

def assemble_systems():
    pts=[-4.45,-1.48,1.48,4.45]
    for i,x in enumerate(pts):
        platform(x,.4,.86,.21)
        if i==0:
            # media/rules: stepped metal reels
            for k in range(3):
                cube('QADHA split floating screen',(x,0,-.05+k*.42),(1.18,.24,.29),[black,gold,chrome][k],.085)
                torus('media orbit',(x,0,.11),.76+k*.20,.019,gold,rot=(.7+k*.1,.1,.25))
            crystal('QADHA core',(x,0,.95),.37,.95,clear)
        elif i==1:
            sphere('MIYTO room sphere',(x,0,.30),.79,glass)
            for k in range(3):
                torus('MIYTO audio wave',(x,0,.3),1.05+k*.17,.018, [chrome,gold,blue_em][k],rot=(1.12,.12+k*.23,.11))
            sphere('MIYTO conversation focus',(x,-.4,.28),.18,pale)
        elif i==2:
            for k in range(4):
                cube('SMI operations lattice',(x-.32+(k%2)*.64,-.13,(k//2)*.72+.16),(.51,.53,.59),[glass,black,chrome,gold][k],.095)
            torus('SMI structural system',(x,0,.55),1.18,.022,gold,rot=(.8,.14,.09))
        elif i==3:
            sphere('AI decision core',(x,0,.4),.8,black)
            for k in range(9):
                a=k*2*pi/9
                sphere('AI network node',(x+.9*cos(a),-.11,.35+.9*sin(a)),.085,pale)
                line('AI visible data edge',[(x,0,.4),(x+.9*cos(a),-.11,.35+.9*sin(a))],.014,chrome)
            crystal('AI hr internal structure',(x,-.26,.4),.30,1.35,glass,8)

def assemble_stack():
    x=2.50
    platform(x,.4,1.65,.21)
    sphere('Central engineering core',(x,0,.22),1.03,graphite)
    crystal('Architecture spine',(x,-.24,.2),.59,2.2,glass,8)
    for k in range(3):
        torus('System knowledge rings',(x,0,.24),2.2-k*.25,.032,[gold,chrome,rose][k],
              rot=(.7+k*.27,.2+k*.25,.34+k*.57))
    for i in range(8):
        a=i*2*pi/8
        xx=x+2.75*cos(a);yy=.2+.68*sin(a);zz=.22+1.75*sin(a)
        m=gold if i%2==0 else chrome
        crystal('Capability individual crystal '+str(i),(xx,yy,zz),.32,.66, m if i%3==0 else clear,6)
        sphere('Capability illuminated node '+str(i),(xx,yy,zz+.23),.056,gold_em,12)
        line('Architecture connecting spine',[(x,0,.22),(xx,yy,zz)],.012,blue_em)
    sphere('Convergence center',(x,-.75,.22),.28,gold_em)

def area(name,loc,power,color,size=4):
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.color=color
    data.shape='DISK';data.size=size
    o=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(o);o.location=loc
    direction=Vector((0,0,0))-o.location;o.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()

def setup():
    scene=bpy.context.scene
    scene.render.engine='CYCLES'
    scene.cycles.samples=SAMPLES
    scene.cycles.use_denoising=True
    scene.render.resolution_x=WIDTH
    scene.render.resolution_y=round(WIDTH*.49)
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    scene.render.film_transparent=False
    scene.view_settings.view_transform='AgX'
    try:scene.view_settings.look='AgX - Medium High Contrast'
    except Exception:pass
    world=bpy.data.worlds.new('Dark studio environment')
    scene.world=world;world.use_nodes=True
    bg=world.node_tree.nodes.get('Background');bg.inputs[0].default_value=(.018,.027,.048,1);bg.inputs[1].default_value=.32
    bpy.ops.mesh.primitive_plane_add(size=300,location=(0,0,-1.69))
    assign(bpy.context.object,navy);bpy.context.object.name='Polished midnight mirror floor'
    # steel horizon physical backdrop
    cube('Deep infinite background',(0,5,2.1),(24,.06,12),black,.0)
    area('Large warm key',(0,-4,8),950,(1.0,.75,.48),7)
    area('Ice blue rim',(4.7,3,5.8),1300,(.32,.66,1),5.8)
    area('Left pearlescent softbox',(-6,-1,4.8),1050,(.65,.84,1),8)
    area('Gold bounce',(4.4,-3,1.8),560,(1,.45,.20),3.4)
    area('Hard backlight',(-2,3,6),880,(.8,.93,1),3.2)
    # Camera with strict framing: image compositing will keep text in left 50% only on hero
    bpy.ops.object.camera_add(location=(0,-17.3,6.3))
    cam=bpy.context.object;cam.name='Editorial product-cinema camera'
    aim=Vector((0,0,.08));cam.rotation_euler=(aim-cam.location).to_track_quat('-Z','Y').to_euler()
    cam.data.type='ORTHO';cam.data.ortho_scale=13.4
    scene.camera=cam
    scene.render.image_settings.color_mode='RGBA'
    scene.render.filepath=str(OUTPUT/(SCENE+'-render.png'))

setup()
{'hero':assemble_hero,'ventures':assemble_ventures,'systems':assemble_systems,'skills':assemble_stack}[SCENE]()
bpy.ops.render.render(write_still=True)
print('STUDIO3D_RENDERED',SCENE,bpy.context.scene.render.filepath,WIDTH,SAMPLES)
