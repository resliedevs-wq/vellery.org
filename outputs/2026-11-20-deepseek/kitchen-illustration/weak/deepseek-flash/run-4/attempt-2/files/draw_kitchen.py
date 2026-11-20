from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance
import random, math

random.seed(7)

S = 2
W, H = 1536, 1024
CW, CH = W*S, H*S

# ---------- colour helpers ----------
def hexc(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

def mix(a, b, t):
    a, b = hexc(a), hexc(b)
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def rgba(c, a=255):
    if isinstance(c, str):
        c = hexc(c)
    return (c[0], c[1], c[2], a)

def sc(v):
    return int(round(v*S))

def P(x, y):
    return (x*S, y*S)

def poly(d, pts, fill=None, outline=None, width=1):
    d.polygon([P(x,y) for x,y in pts], fill=fill, outline=outline)
    if outline and width > 1:
        d.line([P(x,y) for x,y in pts] + [P(*pts[0])], fill=outline, width=sc(width), joint='curve')

def ell(d, box, fill=None, outline=None, width=1):
    d.ellipse([sc(box[0]), sc(box[1]), sc(box[2]), sc(box[3])], fill=fill, outline=outline, width=sc(width))

def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle([sc(box[0]), sc(box[1]), sc(box[2]), sc(box[3])], radius=sc(r), fill=fill, outline=outline, width=sc(width))

def line(d, pts, fill, width=1, joint='curve'):
    d.line([P(x,y) for x,y in pts], fill=fill, width=max(1,sc(width)), joint=joint)

def arc(d, box, start, end, fill, width=1):
    d.arc([sc(box[0]), sc(box[1]), sc(box[2]), sc(box[3])], start=start, end=end, fill=fill, width=max(1,sc(width)))

def bez(points, n=100):
    # de casteljau for list of control points
    out=[]
    for i in range(n+1):
        t=i/n
        pts=points[:]
        while len(pts)>1:
            pts=[(pts[j][0]*(1-t)+pts[j+1][0]*t, pts[j][1]*(1-t)+pts[j+1][1]*t) for j in range(len(pts)-1)]
        out.append(pts[0])
    return out

def grad_rect(img, box, stops, horizontal=False):
    x0,y0,x1,y1=[sc(v) for v in box]
    x0=max(0,min(CW-1,x0)); x1=max(0,min(CW,x1))
    y0=max(0,min(CH-1,y0)); y1=max(0,min(CH,y1))
    if x1<=x0 or y1<=y0: return
    w,h=x1-x0,y1-y0
    g=Image.new('RGB',(w,h))
    px=g.load()
    n = w if horizontal else h
    for i in range(n):
        pos=i/max(1,n-1)
        # find stops
        for k in range(len(stops)-1):
            p0,c0=stops[k]; p1,c1=stops[k+1]
            if p0<=pos<=p1 or k==len(stops)-2:
                t=(pos-p0)/max(1e-6,(p1-p0))
                t=max(0,min(1,t))
                col=mix(c0,c1,t)
                break
        if horizontal:
            for y in range(h): px[i,y]=col
        else:
            for x in range(w): px[x,i]=col
    img.paste(g,(x0,y0))

def soft_layer(drawfn, blur=10, opacity=1.0):
    layer=Image.new('RGBA',(CW,CH),(0,0,0,0))
    dd=ImageDraw.Draw(layer,'RGBA')
    drawfn(dd)
    if blur:
        layer=layer.filter(ImageFilter.GaussianBlur(blur*S))
    if opacity<1:
        a=layer.getchannel('A').point(lambda v:int(v*opacity))
        layer.putalpha(a)
    return layer

def add_texture(img, blur=3, amount=0.10):
    # gentle monochrome mottling and film grain
    fine=Image.effect_noise((CW,CH), 18).convert('RGB')
    fine=Image.merge('RGB',(fine.getchannel(0),)*3)
    soft=fine.filter(ImageFilter.GaussianBlur(blur*S))
    img=Image.blend(img, ImageChops.soft_light(img, soft), amount)
    grain=Image.effect_noise((CW,CH), 10).convert('RGB')
    grain=Image.merge('RGB',(grain.getchannel(0),)*3)
    img=Image.blend(img, ImageChops.overlay(img, grain), 0.045)
    return img


def add_radial_glow(img, cx, cy, rx, ry, color='#ffddb0', alpha=80, gamma=1.8):
    n=192
    mask=Image.new('L',(n,n),0)
    px=mask.load()
    half=(n-1)/2
    for yy in range(n):
        dy=(yy-half)/half
        for xx in range(n):
            dx=(xx-half)/half
            dist=min(1.0, math.hypot(dx,dy))
            px[xx,yy]=int(((1.0-dist)**gamma)*alpha)
    size=(max(2,sc(rx*2)), max(2,sc(ry*2)))
    mask=mask.resize(size, Image.Resampling.LANCZOS)
    layer=Image.new('RGBA',(CW,CH),(0,0,0,0))
    col=Image.new('RGBA',size,rgba(color,255)); col.putalpha(mask)
    layer.paste(col,(sc(cx-rx),sc(cy-ry)))
    return Image.alpha_composite(img.convert('RGBA'),layer).convert('RGB')

# ---------- canvas ----------
img=Image.new('RGB',(CW,CH),hexc('#e8d4ba'))
d=ImageDraw.Draw(img,'RGBA')

# wall base
grad_rect(img,(0,0,W,760),[(0,'#e6d1b6'),(0.45,'#efdfc8'),(0.78,'#eed7bc'),(1,'#d9bda0')])
# broad window glow
img=add_radial_glow(img,400,280,440,320,'#ffdc9c',105,2.1)
d=ImageDraw.Draw(img,'RGBA')

# soft wall mottling
mot=Image.effect_noise((CW//4,CH//4), 55).resize((CW,CH),Image.Resampling.BICUBIC).convert('RGB')
mot=Image.merge('RGB',(mot.getchannel(0),)*3).filter(ImageFilter.GaussianBlur(9*S))
img=Image.blend(img, ImageChops.soft_light(img,mot), 0.16)

# subtle sun patch on wall right of window
patch=soft_layer(lambda dd: dd.ellipse([sc(640),sc(100),sc(1240),sc(760)],fill=(255,220,166,45)), blur=70)
img=Image.alpha_composite(img.convert('RGBA'),patch).convert('RGB')
d=ImageDraw.Draw(img,'RGBA')

# ============================================================
# WINDOW
# ============================================================
wx0,wy0,wx1,wy1 = 140,92,660,566
# recessed shadow
sh=soft_layer(lambda dd: dd.rounded_rectangle([sc(wx0-18),sc(wy0-18),sc(wx1+18),sc(wy1+18)],radius=sc(4),fill=(76,48,30,95)),blur=16,opacity=0.85)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB')
d=ImageDraw.Draw(img,'RGBA')

# outer casing cream
rrect(d,(wx0-20,wy0-20,wx1+20,wy1+22),6,'#f3e5cf')
rrect(d,(wx0-20,wy0-20,wx1+20,wy1+22),6,None,'#c8a987',2)
# inner opening
ix0,iy0,ix1,iy1=wx0+16,wy0+16,wx1-16,wy1-16
# sky gradient
grad_rect(img,(ix0,iy0,ix1,iy1),[(0,'#f6c27f'),(0.28,'#f7b184'),(0.55,'#ffd6a2'),(0.78,'#f4d9ad'),(1,'#cfd0a5')])

# local window painter for clipped-ish outside details
def wbox(x0,y0,x1,y1): return (x0,y0,x1,y1)

# sun glow and disc
sun_c=(560,190)
img=add_radial_glow(img,sun_c[0],sun_c[1],150,150,'#fff1bd',190,2.6); d=ImageDraw.Draw(img,'RGBA')
ell(d,(sun_c[0]-23,sun_c[1]-23,sun_c[0]+23,sun_c[1]+23),'#fff4cb')
ell(d,(sun_c[0]-16,sun_c[1]-16,sun_c[0]+16,sun_c[1]+16),'#fffdf1')

# clouds - soft bands
cl=Image.new('RGBA',(CW,CH),(0,0,0,0)); cd=ImageDraw.Draw(cl,'RGBA')
for (cx,cy,rw,rh,a) in [(250,220,120,16,65),(365,265,90,11,55),(570,285,150,17,70),(460,155,95,9,45),(220,320,170,20,35)]:
    cd.ellipse([sc(cx-rw),sc(cy-rh),sc(cx+rw),sc(cy+rh)],fill=(255,232,206,a))
cl=cl.filter(ImageFilter.GaussianBlur(5*S))
img=Image.alpha_composite(img.convert('RGBA'),cl).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# distant hills
poly(d,[(ix0,400),(ix0+70,360),(ix0+145,380),(ix0+230,330),(ix0+315,366),(ix0+405,330),(ix1,370),(ix1,iy1),(ix0,iy1)],'#b7a978')
poly(d,[(ix0,430),(ix0+100,396),(ix0+180,414),(ix0+285,374),(ix0+380,405),(ix0+470,386),(ix1,410),(ix1,iy1),(ix0,iy1)],'#8f9568')
poly(d,[(ix0,462),(ix0+80,442),(ix0+195,450),(ix0+300,420),(ix0+410,446),(ix1,432),(ix1,iy1),(ix0,iy1)],'#6f8059')
# field bands
for i,y in enumerate(range(455,566,14)):
    poly(d,[(ix0,y),(ix1,y+4),(ix1,y+18),(ix0,y+14)], mix('#829261','#b0ab6b', (i%3)*0.22))

# distant farmhouse
fx,fy=300,404
poly(d,[(fx,fy),(fx,fy-25),(fx+20,fy-40),(fx+40,fy-25),(fx+40,fy)],'#e7c69b')
poly(d,[(fx-4,fy-24),(fx+20,fy-45),(fx+44,fy-24)],'#8f5e43')
rrect(d,(fx+8,fy-16,fx+15,fy-7),1,'#6e5238')
rrect(d,(fx+25,fy-18,fx+33,fy-8),1,'#7f6144')
# fence
for x in range(190,360,18):
    line(d,[(x,535),(x,505)],'#7e6243',2)

# geranium window box outside lower-left pane
rrect(d,(222,510,382,536),4,'#8a5a38')
rrect(d,(222,510,382,518),4,'#b97b4d')
rrect(d,(236,532,368,540),3,'#6f452b')
for sx in [238,256,276,296,316,338,358]:
    for k in range(4):
        ox=sx+random.uniform(-10,10); oy=random.uniform(480,514)
        ell(d,(ox-11,oy-8,ox+11,oy+8), random.choice(['#587343','#6a8650','#48633a','#77905a']))
for (fx,fy) in [(244,478),(272,468),(302,482),(330,465),(356,480),(286,492),(346,496)]:
    for j in range(5):
        a=j*math.tau/5 + 0.3
        ex=fx+math.cos(a)*7; ey=fy+math.sin(a)*6
        ell(d,(ex-5,ey-4,ex+5,ey+4),'#cf6f63')
    ell(d,(fx-4,fy-4,fx+4,fy+4),'#f0b06e')
    ell(d,(fx-2,fy-2,fx+2,fy+2),'#b74e48')
# a few trailing leaves over box edge
for x in range(228,380,20):
    ell(d,(x-8,522,x+8,542),'#647f4b')

# tree left
trunk='#6c5038'; leaf='#5d7447' 
line(d,bez([(190,565),(184,500),(204,455),(196,420)],40),trunk,10)
for ang in [-55,-25,5,35,65]:
    end=(196+55*math.cos(math.radians(ang-90)), 440+55*math.sin(math.radians(ang-90)))
    line(d,bez([(196,440),((196+end[0])/2-14,410),(end[0],end[1])],30),trunk,5)
for i in range(70):
    a=random.uniform(0,math.tau); rr=random.uniform(0,62)
    cx=200+math.cos(a)*rr*1.2; cy=365+math.sin(a)*rr*0.75
    ell(d,(cx-9,cy-7,cx+9,cy+7), random.choice(['#57733f','#6c844d','#7c9257','#465f36']))
# birds
for (bx,by) in [(420,180),(445,196),(398,205)]:
    line(d,bez([(bx-7,by),(bx-2,by-5),(bx+3,by-1)],10),'#8b6c58',1)
    line(d,bez([(bx+3,by-1),(bx+7,by-5),(bx+11,by)],10),'#8b6c58',1)

# glass reflections
refl=Image.new('RGBA',(CW,CH),(0,0,0,0)); rd=ImageDraw.Draw(refl,'RGBA')
rd.polygon([P(ix0+30,iy1),P(ix0+120,iy0),P(ix0+190,iy0),P(ix0+80,iy1)],fill=(255,255,245,18))
rd.polygon([P(ix0+220,iy1),P(ix0+310,iy0),P(ix0+345,iy0),P(ix0+255,iy1)],fill=(255,255,245,13))
refl=refl.filter(ImageFilter.GaussianBlur(3*S))
img=Image.alpha_composite(img.convert('RGBA'),refl).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# window inner shadow top/left
sh2=soft_layer(lambda dd: dd.rectangle([sc(ix0),sc(iy0),sc(ix1),sc(iy0+24)],fill=(82,52,34,80)),blur=9)
img=Image.alpha_composite(img.convert('RGBA'),sh2).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# muntins / frame
frame_col='#efe0c9'; edge='#bfa184'
# outer inner frame
rrect(d,(wx0,wy0,wx1,wy1),3,None,edge,8)
rrect(d,(wx0+5,wy0+5,wx1-5,wy1-5),2,None,frame_col,13)
# vertical muntins
for mx in [wx0+178, wx0+346]:
    line(d,[(mx,wy0+8),(mx,wy1-8)],edge,15)
    line(d,[(mx-3,wy0+8),(mx-3,wy1-8)],frame_col,10)
# horizontal muntins
for my in [wy0+155, wy0+310]:
    line(d,[(wx0+7,my),(wx1-7,my)],edge,15)
    line(d,[(wx0+7,my-3),(wx1-7,my-3)],frame_col,10)
# bevel highlights
line(d,[(wx0+10,wy0+8),(wx1-10,wy0+8)],'#fff7e7',3)
# frame shading right/bottom
line(d,[(wx1-7,wy0+8),(wx1-7,wy1-8)],'#9a7b5f',2)
line(d,[(wx0+8,wy1-7),(wx1-8,wy1-7)],'#9a7b5f',2)

# sill
sill_sh=soft_layer(lambda dd: dd.rectangle([sc(105),sc(586),sc(690),sc(620)],fill=(69,44,28,110)),blur=11)
img=Image.alpha_composite(img.convert('RGBA'),sill_sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
rrect(d,(104,560,690,586),4,'#c38e57')
rrect(d,(104,560,690,567),4,'#e0b37a')
rrect(d,(104,586,690,602),4,'#96623a')
rrect(d,(104,560,690,602),4,None,'#6f4729',2)
line(d,[(112,563),(682,563)],'#f3d6a7',3)
# grain on sill
for i in range(11):
    y=567+i*3.1
    line(d,bez([(112,y),(300,y+random.uniform(-1.5,1.5)),(500,y+random.uniform(-1.5,1.5)),(682,y)],30),rgba('#8b5a34',55),1)
# small corbels
for cx in [122,660]:
    poly(d,[(cx,602),(cx+22,602),(cx+16,630),(cx+4,630)],'#a97345', '#7a4d2d',1)

# curtain rod
line(d,[(110,80),(700,80)],'#7e5b2f',7)
line(d,[(110,78),(700,78)],'#c9974e',3)
for cx in [106,704]:
    ell(d,(cx-11,68,cx+11,90),'#b98543')
    ell(d,(cx-6,73,cx+6,85),'#e2b76b')

# curtains
def curtain(x0, side='left'):
    # vertical folds, drawn as broad translucent panels
    pts_top=[(x0,86),(x0+78,86)]
    pts_bot=[(x0+66,594),(x0-6,594)]
    pts=pts_top+[pts_bot[0]]+[pts_bot[1]]
    poly(d,pts,(246,232,205,216), rgba('#b28e68',150),1)
    # folds
    for k in range(4):
        fx=x0+12+k*17
        line(d,bez([(fx,90),(fx-7,250),(fx+5,420),(fx-2,590)],40),rgba('#c0a27c',95),4)
        line(d,bez([(fx+5,90),(fx-2,250),(fx+10,420),(fx+3,590)],40),rgba('#fff9e8',80),2)
    # hem
    line(d,[(x0-5,590),(x0+65,590)],rgba('#9e7e5c',160),2)
curtain(142,'left')
curtain(584,'right')

# tiebacks
for cx,cy in [(196,410),(618,430)]:
    rrect(d,(cx-19,cy-6,cx+19,cy+6),4,'#b98543')
    rrect(d,(cx-19,cy-6,cx+19,cy+6),4,None,'#6e4b28',1)

# ============================================================
# WALL DETAILS, SHELVES, CABINETS
# ============================================================

# left floating shelves
for sy in [250,382]:
    sh=soft_layer(lambda dd,sy=sy: dd.rectangle([sc(15),sc(sy+15),sc(152),sc(sy+44)],fill=(68,44,28,95)),blur=7)
    img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
    rrect(d,(10,sy,150,sy+16),3,'#a86f43')
    rrect(d,(10,sy,150,sy+6),3,'#d5a06b')
    rrect(d,(10,sy+12,150,sy+20),3,'#75482b')
    line(d,[(16,sy+2),(144,sy+2)],'#eac28e',2)
    # brackets
    for bx in [27,121]:
        poly(d,[(bx,sy+20),(bx+13,sy+20),(bx+8,sy+38),(bx+3,sy+38)],'#8b5c36')

# top shelf objects: crock, jars, ivy pot
rrect(d,(28,198,70,250),6,'#d9c6a8'); rrect(d,(28,198,70,205),3,'#efe0c7')
ell(d,(40,190,58,204),'#8d9b7a')
# little labels
rrect(d,(34,218,64,237),2,'#c9b08d')
# jars
for (jx,jw,jh,jc) in [(87,25,52,'#c68c54'),(120,22,60,'#8d9d78')]:
    rrect(d,(jx,250-jh,jx+jw,248),5,jc)
    rrect(d,(jx+2,250-jh+2,jx+jw-2,250-jh+8),2,rgba('#fff8e5',120))
    rrect(d,(jx-2,250-jh-5,jx+jw+2,250-jh+1),3,'#8b5c36')
    rrect(d,(jx+4,250-jh+18,jx+jw-4,250-jh+30),1,rgba('#f4e7cf',150))
# ivy pot atop shelf
poly(d,[(60,138),(96,138),(91,174),(65,174)],'#b47a4e','#75482b',1)
ell(d,(64,132,92,144),'#a86f43')
for k in range(5):
    start=(random.uniform(66,90),140)
    pts=bez([start,(start[0]+random.uniform(-18,18),165),(start[0]+random.uniform(-22,22),195),(start[0]+random.uniform(-26,26),225)],30)
    line(d,pts,'#5e7447',2)
    for j in range(4):
        x,y=pts[random.randint(3,len(pts)-2)]
        ell(d,(x-6,y-4,x+6,y+4), random.choice(['#657c4c','#7b915b','#4f673d']))
# second shelf: plates, bowl, small plant
for i in range(3):
    ell(d,(32+i*2,350+i*0,84-i*2,384),'#e9dcc6')
    ell(d,(39,355,77,379),'#d7c6ab')
ell(d,(100,352,138,383),'#b7c0a8'); ell(d,(103,354,135,380),'#dbe1ce')
# tiny plant
poly(d,[(112,330),(132,330),(129,352),(115,352)],'#bd7e4c')
for k in range(7):
    line(d,bez([(122,332),(122+random.uniform(-12,12),315),(122+random.uniform(-17,17),300)],15),'#617847',2)
# apron hanging left wall
line(d,[(40,430),(40,470)],'#6f4729',3)
poly(d,[(26,468),(58,470),(64,565),(39,584),(20,565)],'#b9a58c', rgba('#7d674f',80),1)
poly(d,[(31,476),(54,478),(52,505),(33,504)],'#a28b72')
line(d,[(33,505),(52,505)],'#8b7259',1)

# ---------- upper cabinet ----------
cab=(800,140,1132,398)
sh=soft_layer(lambda dd: dd.rounded_rectangle([sc(cab[0]+12),sc(cab[1]+18),sc(cab[2]+20),sc(cab[3]+26)],radius=sc(4),fill=(61,40,27,105)),blur=13)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
# crown
rrect(d,(cab[0]-12,cab[1]-14,cab[2]+12,cab[1]+6),3,'#f0e2c9')
rrect(d,(cab[0]-12,cab[1]-14,cab[2]+12,cab[1]+6),3,None,'#c5a887',1)
rrect(d,cab,3,'#72856d')
# frame shading
rrect(d,(cab[0]+8,cab[1]+8,cab[2]-8,cab[3]-8),2,None,'#52634f',3)
# two doors
for (dx0,dx1) in [(812,960),(972,1120)]:
    rrect(d,(dx0,168,dx1,380),4,'#7b8e75')
    rrect(d,(dx0+12,180,dx1-12,368),3,'#6c8068')
    # bevelled inner panel
    rrect(d,(dx0+20,190,dx1-20,356),2,None,'#8fa187',2)
    rrect(d,(dx0+20,190,dx1-20,356),2,None,'#5b6d56',1)
    line(d,[(dx0+23,193),(dx1-23,193)],rgba('#aab99f',110),2)
    line(d,[(dx0+23,353),(dx1-23,353)],rgba('#4b5c47',80),2)
# knobs
for kx in [884,1048]:
    ell(d,(kx-6,300,kx+6,312),'#c3914a'); ell(d,(kx-4,302,kx+4,310),'#f1ca7c')
    ell(d,(kx-2,305,kx+2,308),'#8b622c')
# ---- right-hand glazed display door ----
rrect(d,(972,168,1120,380),4,'#7b8e75')
# shadow of the frame on the interior
rrect(d,(980,176,1112,372),3,'#4a3c2f')
rrect(d,(984,180,1108,368),3,'#6a563f')
grad_rect(img,(986,182,1106,366),[(0,'#7d654a'),(0.45,'#6b5640'),(1,'#4d3c2e')])
# shelves
for sy in [240,300,355]:
    rrect(d,(988,sy,1104,sy+9),2,'#a06d44')
    rrect(d,(988,sy,1104,sy+3),2,'#d09a60')
    line(d,[(990,sy+9),(1102,sy+9)],rgba('#3e2d21',160),2)
# top shelf: plates and a small bowl
for i in range(3):
    ell(d,(998+i*1,215+i*5,1056-i*1,235+i*5),'#e8dbc4')
    ell(d,(1004,218+i*5,1050,231+i*5),'#cdbb9d')
ell(d,(1064,218,1096,238),'#8fa495')
ell(d,(1067,220,1093,236),'#b8c5b4')
# middle shelf: mugs and a honey pot
for (mx,my) in [(1000,262),(1034,266)]:
    rrect(d,(mx,my,mx+25,my+30),5,'#e8dcc7')
    arc(d,(mx+20,my+5,mx+34,my+22),270,90,'#c9b696',3)
    ell(d,(mx,my-1,mx+25,my+7),'#f4ead7')
    ell(d,(mx+3,my+1,mx+22,my+5),'#896544')
    line(d,[(mx+4,my+9),(mx+5,my+25)],rgba('#bda98a',100),1)
rrect(d,(1076,276,1096,298),3,'#c68e4a')
rrect(d,(1078,270,1094,277),2,'#8d5c35')
# lower shelf: stacked bowls
for i in range(3):
    y=324-i*12
    ell(d,(1004,y,1056,y+148-140),'#e5d7be')
    ell(d,(1010,y+2,1050,y+6),'#c5b291')
ell(d,(1066,332,1098,352),'#b0bda9')
# frame rebate highlight
rrect(d,(980,176,1112,372),3,None,'#5c6d56',3)
line(d,[(984,180),(1108,180)],'#a7b69b',2)
line(d,[(984,368),(1108,368)],rgba('#485843',150),2)
# glass pane and its morning reflection
rrect(d,(984,180,1108,368),2,(202,214,198,22))
refl=Image.new('RGBA',(CW,CH),(0,0,0,0)); rd=ImageDraw.Draw(refl,'RGBA')
rd.polygon([P(990,368),P(1038,182),P(1062,182),P(1014,368)],fill=(255,249,228,30))
rd.polygon([P(1072,368),P(1100,254),P(1106,254),P(1080,368)],fill=(255,249,228,18))
refl=refl.filter(ImageFilter.GaussianBlur(2*S))
img=Image.alpha_composite(img.convert('RGBA'),refl).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
# warm interior glow in the display cabinet
img=add_radial_glow(img,1044,265,74,116,'#ffd596',44,2.0); d=ImageDraw.Draw(img,'RGBA')
# faint inner top shadow
shg=soft_layer(lambda dd: dd.rectangle([sc(988),sc(182),sc(1104),sc(214)],fill=(35,25,16,70)),blur=8)
img=Image.alpha_composite(img.convert('RGBA'),shg).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
# little brass knob / latch
ell(d,(986,304,998,316),'#c28e4b'); ell(d,(989,307,995,313),'#f0ca7b')
# bottom molding
rrect(d,(cab[0]-8,cab[3]-8,cab[2]+8,cab[3]+8),3,'#e8d7bd')
rrect(d,(cab[0]-8,cab[3]-8,cab[2]+8,cab[3]+8),3,None,'#bd9d7c',1)
# under cabinet warm light strip
UG=Image.new('RGBA',(CW,CH),(0,0,0,0)); ugd=ImageDraw.Draw(UG,'RGBA')
for i in range(8):
    ugd.rectangle([sc(cab[0]),sc(cab[3]+8+i*8),sc(cab[2]),sc(cab[3]+18+i*8)],fill=(255,213,141,int(42-i*4)))
UG=UG.filter(ImageFilter.GaussianBlur(7*S))
img=Image.alpha_composite(img.convert('RGBA'),UG).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# cabinet door reflections
refl=Image.new('RGBA',(CW,CH),(0,0,0,0)); rd=ImageDraw.Draw(refl,'RGBA')
rd.polygon([P(824,168),P(865,168),P(823,380),P(809,380)],fill=(255,246,220,18))
rd.polygon([P(984,168),P(1010,168),P(968,380),P(956,380)],fill=(255,246,220,13))
img=Image.alpha_composite(img.convert('RGBA'),refl).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# ambient shading on cabinet face
cab_sh=soft_layer(lambda dd: dd.rounded_rectangle([sc(800),sc(310),sc(1132),sc(398)],radius=sc(3),fill=(37,47,37,70)),blur=18)
img=Image.alpha_composite(img.convert('RGBA'),cab_sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
# warm reflected light along window-facing edge
line(d,[(806,154),(806,388)],rgba('#f4d7a8',55),4)
line(d,[(1126,154),(1126,388)],rgba('#3e4d3d',55),3)
# soft shadow cast on tile below
sh=soft_layer(lambda dd: dd.rectangle([sc(806),sc(398),sc(1136),sc(438)],fill=(58,39,24,85)),blur=12)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# ---------- narrow hanging rail between window and cabinet ----------
line(d,[(688,210),(786,210)],'#8a6337',4)
for hx_ in [705,740,775]:
    line(d,[(hx_,210),(hx_,222)],'#6d4c2d',2)
    ell(d,(hx_-4,220,hx_+4,228),'#b4864f')
# utensils
# ladle
line(d,bez([(705,226),(699,250),(705,274)],20),'#b8743f',3)
ell(d,(694,272,716,292),'#b8743f'); ell(d,(698,276,712,288),'#8e5730')
# whisk
line(d,[(740,225),(740,258)],'#8a6337',2)
for k in range(4):
    line(d,bez([(740-k*3,258),(730-k*2,276),(740-k*2,292)],20),'#a7835a',1)
# copper pan
line(d,[(775,224),(775,250)],'#7b542f',2)
ell(d,(760,250,792,284),'#b9683f'); ell(d,(765,255,787,279),'#8f4c2c'); ell(d,(770,259,782,274),'#d28d5b')
# dried herbs bundle
line(d,[(756,230),(756,246)],'#7a5a35',2)
for k in range(15):
    ang=random.uniform(-50,-130)
    line(d,bez([(756,246),(756+random.uniform(-5,5),260),(756+random.uniform(-16,16),284)],15),'#7b8a55',1)

# ============================================================
# BACKSPLASH
# ============================================================
# tile area on right 398..706
def tiles(x0,y0,x1,y1,tw,th):
    # grout field
    d.rectangle([sc(x0),sc(y0),sc(x1),sc(y1)],fill=rgba('#cfb28e',255))
    row=0; y=y0
    while y<y1:
        x=x0 - (tw/2 if row%2 else 0)
        while x<x1:
            xx0=max(x0,x+2); xx1=min(x1,x+tw-2)
            yy0=y+2; yy1=min(y1,y+th-2)
            if xx1>xx0 and yy1>yy0:
                base=random.choice(['#e8d6b9','#e3cfb0','#eedcc1','#ddc7a7','#e6d3b5'])
                d.rectangle([sc(xx0),sc(yy0),sc(xx1),sc(yy1)],fill=base)
                d.line([P(xx0+2,yy0+2),P(xx1-2,yy0+2)],fill=rgba('#fff6e3',115),width=sc(1))
                d.line([P(xx0+2,yy1-2),P(xx1-2,yy1-2)],fill=rgba('#b69874',80),width=sc(1))
            x+=tw
        y+=th; row+=1
tiles(668,400,1536,700,54,32)
# left of window / under sill small painted beadboard
d.rectangle([sc(0),sc(600),sc(668),sc(700)],fill='#ddc5a5')
for x in range(0,668,24):
    line(d,[(x,600),(x,700)],rgba('#b89a77',110),1)
    line(d,[(x+2,600),(x+2,700)],rgba('#f5e6ce',80),1)
# backsplash subtle warm light from under cabinet
# warm glaze across the tiled splashback
warm=Image.new('RGBA',(CW,CH),(0,0,0,0)); wd=ImageDraw.Draw(warm,'RGBA')
wd.rectangle([sc(668),sc(400),sc(1536),sc(700)],fill=(255,196,116,20))
warm=warm.filter(ImageFilter.GaussianBlur(15*S))
img=Image.alpha_composite(img.convert('RGBA'),warm).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# ============================================================
# COUNTER + LOWER CABINETS
# ============================================================
# shadow under counter onto cabinet
sh=soft_layer(lambda dd: dd.rectangle([sc(0),sc(735),sc(1536),sc(770)],fill=(52,33,21,120)),blur=9)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# lower cabinets base
d.rectangle([sc(0),sc(730),sc(1536),sc(960)],fill='#6d8168')
grad_rect(img,(0,730,1536,965),[(0,'#788b72'),(0.5,'#6a7d65'),(1,'#586b55')])
# kick plate
d.rectangle([sc(0),sc(952),sc(1536),sc(976)],fill='#4f5e4b')

# counter top
rrect(d,(-10,696,1546,738),4,'#c18b55')
grad_rect(img,(-10,696,1546,738),[(0,'#d7a76b'),(0.18,'#c79159'),(0.82,'#b57b47'),(1,'#8c592f')])
line(d,[(-8,698),(1544,698)],'#ecc48d',3)
# butcher block grain
for i in range(14):
    y=703+i*2.3
    pts=[]
    for x in range(-10,1546,80):
        pts.append((x,y+random.uniform(-1.2,1.2)))
    line(d,pts,rgba('#8a562f',55),1)
# front edge shadow
rrect(d,(-10,730,1546,740),3,'#734626')
line(d,[(-10,736),(1546,736)],rgba('#4b2c18',160),2)

# vertical cabinet divisions and shaker panels
def lower_door(x0,x1,y0=748,y1=944,handle='cup'):
    rrect(d,(x0,y0,x1,y1),3,'#758971')
    rrect(d,(x0+9,y0+9,x1-9,y1-9),2,'#6b7f68')
    rrect(d,(x0+17,y0+18,x1-17,y1-18),2,None,'#84977d',2)
    rrect(d,(x0+17,y0+18,x1-17,y1-18),2,None,'#576a53',1)
    line(d,[(x0+19,y0+21),(x1-19,y0+21)],rgba('#a5b49b',90),1)
    # handle
    if handle=='cup':
        hx=(x0+x1)/2
        line(d,[(hx-16,776),(hx+16,776)],'#b98543',2)
        rrect(d,(hx-19,770,hx+19,784),4,'#c28e4b')
        rrect(d,(hx-19,770,hx+19,784),4,None,'#75502a',1)
        line(d,[(hx-15,772),(hx+15,772)],'#edc97c',1)
    else:
        hx=(x0+x1)/2
        ell(d,(hx-6,777,hx+6,789),'#c28e4b'); ell(d,(hx-3,779,hx+3,785),'#f1ca7b')

for (a,b) in [(-8,138),(142,292),(300,460),(466,616),(622,772),(778,928),(934,1084),(1090,1168)]:
    lower_door(a,b)
# drawer row above doors
for (a,b) in [(-8,138),(142,292),(466,616),(622,772),(778,928),(934,1084),(1090,1168)]:
    rrect(d,(a+4,742,b-4,786),2,'#7a8e76')
    rrect(d,(a+13,747,b-13,781),2,None,'#687c65',1)
    hx=(a+b)/2
    rrect(d,(hx-17,757,hx+17,770),4,'#c28e4b')
    rrect(d,(hx-17,757,hx+17,770),4,None,'#75502a',1)
    line(d,[(hx-13,759),(hx+13,759)],'#edc97c',1)

# cabinet shadows and light
# left highlight
line(d,[(0,750),(1536,750)],rgba('#98a98e',100),1)
# soft sun patches on cabinet fronts
sp=Image.new('RGBA',(CW,CH),(0,0,0,0)); sd=ImageDraw.Draw(sp,'RGBA')
sd.polygon([P(160,736),P(510,736),P(600,960),P(240,960)],fill=(255,207,135,36))
sd.polygon([P(640,736),P(830,736),P(920,960),P(720,960)],fill=(255,197,118,20))
sp=sp.filter(ImageFilter.GaussianBlur(18*S))
img=Image.alpha_composite(img.convert('RGBA'),sp).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# ============================================================
# FLOOR
# ============================================================
# deep contact shadow beneath the cabinet run
img=add_radial_glow(img,790,1000,780,90,'#3d281b',90,2.2); d=ImageDraw.Draw(img,'RGBA')
# oak boards
grad_rect(img,(0,970,W,1024),[(0,'#8b5a3d'),(0.28,'#a56e49'),(0.72,'#b67d52'),(1,'#94613f')])
d.rectangle([sc(0),sc(970),sc(W),sc(978)],fill='#5a3927')
# board seams with a little perspective
for x in [40,270,500,730,960,1190,1420,1600]:
    line(d,[(x,978),(x-18,1024)],rgba('#5d3a27',120),2)
    line(d,[(x+2,978),(x-15,1024)],rgba('#e0ad7b',50),1)
for y in [998,1014]:
    line(d,bez([(0,y),(260,y+2),(520,y-1),(780,y+2),(1040,y-1),(1300,y+2),(1536,y)],50),rgba('#5d3a27',85),2)
    line(d,bez([(0,y-1),(260,y+1),(520,y-2),(780,y+1),(1040,y-2),(1300,y+1),(1536,y-1)],50),rgba('#e6b783',40),1)
# warm sunlight spilling across the boards
floor_light=soft_layer(lambda dd: dd.polygon([P(180,972),P(570,972),P(660,1024),P(270,1024)],fill=(255,213,145,55)),blur=24)
img=Image.alpha_composite(img.convert('RGBA'),floor_light).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# ============================================================
# FARMHOUSE SINK + FAUCET
# ============================================================
# sink opening / basin, seen from just above
ell(d,(318,677,610,709),rgba('#6b4a32',100))
ell(d,(306,674,620,708),'#f8efdd')
# apron front
rrect(d,(314,700,614,796),14,'#f4ead7')
rrect(d,(314,700,614,796),14,None,'#c8b493',2)
# thick vitreous rim catches the window light
ell(d,(308,674,618,707),'#fbf5e7')
ell(d,(312,676,614,705),'#d6c5a8')
ell(d,(318,678,608,703),'#b6a58a')
# pale ceramic basin with cool reflected sky in its depth
ell(d,(323,680,603,701),'#9fa394')
ell(d,(327,682,599,699),'#b3b6a6')
ell(d,(333,684,593,697),'#a6a997')
ell(d,(345,686,581,696),'#bdc0af')
# far rim highlight and near rim
arc(d,(311,675,615,706),188,352,'#fffaf0',3)
arc(d,(312,677,614,706),8,172,rgba('#a58f72',150),2)
# reflected window light on the inner wall
arc(d,(349,680,577,700),195,345,rgba('#fff7e3',115),3)
ell(d,(388,687,444,696),rgba('#fff5de',75))
# drain
ell(d,(455,690,477,697),rgba('#8d7b62',110))
ell(d,(460,691,472,696),rgba('#6e5e49',110))
# shading down the apron
grad_rect(img,(322,710,606,794),[(0,'#fff9ea'),(0.35,'#f5ead4'),(0.8,'#decaaa'),(1,'#c5ae8b')])
# apron recessed panel
rrect(d,(335,718,593,780),10,None,'#d5c09e',2)
rrect(d,(338,721,590,777),9,None,'#fffaf0',1)
line(d,[(345,724),(583,724)],rgba('#fffdf4',150),2)
# faint vertical highlights
for x in [370,470,550]:
    line(d,[(x,722),(x-4,776)],rgba('#fff9e9',70),2)
# small maker's mark
ell(d,(455,744,470,752),rgba('#b9a27f',70))
# linen towel draped over the left rim of the sink
sh=soft_layer(lambda dd: dd.polygon([P(326,690),P(384,690),P(388,780),P(338,782)],fill=(64,43,27,80)),blur=6)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
poly(d,[(320,683),(372,683),(380,740),(374,776),(352,790),(332,774),(326,736)],'#ded0b7',rgba('#8f7a5e',100),1)
poly(d,[(320,683),(372,683),(373,696),(322,696)],'#f0e4ce')
# sage bands
for (yy,hh) in [(704,5),(720,4),(744,5),(762,4)]:
    line(d,[(325,yy),(377,yy)],'#81917a',hh)
# folds
line(d,bez([(334,698),(332,730),(338,770)],30),rgba('#aa9679',110),2)
line(d,bez([(352,698),(350,730),(354,768)],30),rgba('#fff6e2',95),2)
line(d,bez([(366,698),(367,730),(368,762)],30),rgba('#aa9679',90),2)
# hem
line(d,bez([(332,772),(350,786),(374,770)],20),'#b3a083',2)

# faucet brass bridge
rail='#b98543'; hi='#f0ca7e'; dk='#6c4a26'
# base plates
for bx in [424,504]:
    ell(d,(bx-17,676,bx+17,696),'#c69551')
    ell(d,(bx-13,679,bx+13,693),'#e5b96d')
# vertical supply posts
for bx in [424,504]:
    rrect(d,(bx-5,620,bx+5,682),3,rail)
    line(d,[(bx-3,622),(bx-3,680)],hi,1)
# bridge
line(d,bez([(424,628),(452,600),(476,600),(504,628)],50),rail,6)
line(d,bez([(425,625),(452,597),(476,597),(503,625)],25),hi,2)
# spout arch
line(d,bez([(464,602),(462,576),(438,570),(438,594)],50),rail,6)
line(d,bez([(462,600),(460,579),(441,573),(441,593)],25),hi,2)
# spout tip
rrect(d,(432,590,445,604),4,rail)
line(d,[(435,592),(435,601)],hi,2)
# handles
for bx,ang in [(416,0),(512,0)]:
    line(d,[(bx,644),(bx-20,634)],rail,4)
    ell(d,(bx-27,627,bx-13,641),'#c69551')
    ell(d,(bx-24,630,bx-16,638),'#e8bd71')
# tiny water drip highlight
ell(d,(437,606,440,612),rgba('#d9f0ef',210))

# small soap bottle & brush
rrect(d,(548,650,576,698),7,'#8e9e7e')
rrect(d,(559,636,565,651),2,'#5b4a35')
rrect(d,(554,642,570,648),2,'#b98543')
rrect(d,(536,688,558,700),4,'#c4a16b')
line(d,[(545,676),(547,690)],'#8a6337',2)
for k in range(6):
    line(d,[(544+k*2,660),(540+k*2,676)],'#b9a883',1)

# ============================================================
# COUNTER PROPS
# ============================================================
# cutting board left
sh=soft_layer(lambda dd: dd.ellipse([sc(30),sc(688),sc(244),sc(744)],fill=(68,42,25,80)),blur=6)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
rrect(d,(32,666,244,714),8,'#b47a47')
rrect(d,(40,672,236,706),6,None,'#8d592f',2)
# handle hole
ell(d,(218,680,232,693),'#684226')
# board grain
for i in range(5):
    line(d,bez([(44,676+i*6),(110,674+i*6),(180,678+i*6),(232,676+i*6)],30),rgba('#8f5c34',70),1)
# loaf of bread
poly(d,[(78,666),(88,620),(92,606),(112,594),(142,592),(166,600),(178,616),(182,666)],'#c98a4a')
poly(d,[(88,620),(92,606),(112,594),(142,592),(166,600),(178,616),(172,628),(150,618),(120,622),(98,632)],'#e0a661')
# scoring
for k in range(4):
    line(d,bez([(106+k*16,606),(112+k*16,616),(104+k*16,624)],15),'#a36836',2)
# bread shadow
line(d,[(78,666),(182,666)],rgba('#7e4b26',100),3)
# knife
poly(d,[(190,648),(244,656),(244,664),(190,668)],'#9b9a8d')
poly(d,[(190,648),(222,652),(222,666),(190,668)],'#d6d5c7')
rrect(d,(232,656,262,667),4,'#6f4729')
# honey jar
rrect(d,(36,608,73,666),7,'#d49a4f')
rrect(d,(43,616,66,658),5,rgba('#f4c56e',140))
rrect(d,(39,601,70,615),4,'#8a5b33')
line(d,[(41,605),(68,605)],'#b98543',2)
rrect(d,(47,626,62,648),2,'#f2dfb4')

# bowl of oranges right of sink
sh=soft_layer(lambda dd: dd.ellipse([sc(872),sc(690),sc(1048),sc(742)],fill=(69,42,24,105)),blur=7)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
# bowl body / back rim
ell(d,(884,650,1036,714),'#bca783')
ell(d,(888,648,1032,700),'#e8dcc3')
ell(d,(896,652,1024,690),'#c2ab86')
# inner glaze shadow
ell(d,(898,654,1022,688),'#ab9270')
# oranges tucked inside
for (ox,oy,r) in [(922,660,22),(962,652,24),(996,666,20)]:
    ell(d,(ox-r,oy-r,ox+r,oy+r),'#cf7137')
    ell(d,(ox-r+3,oy-r+4,ox+r-8,oy+r-8),'#e88f4c')
    ell(d,(ox-r+9,oy-r+7,ox-r+20,oy-r+15),rgba('#ffce96',175))
    # dimples
    for k in range(18):
        a=random.uniform(0,math.tau); rr=random.uniform(0.35,0.78)*r
        px_=ox+math.cos(a)*rr; py_=oy+math.sin(a)*rr*0.8
        ell(d,(px_-1,py_-1,px_+1,py_+1),rgba('#b85a2d',60))
    # leaf
    line(d,bez([(ox+3,oy-r+2),(ox+13,oy-r-8),(ox+21,oy-r-5)],15),'#617947',2)
    ell(d,(ox+11,oy-r-12,ox+31,oy-r-1),'#6f874e')
    line(d,[(ox+14,oy-r-3),(ox+27,oy-r-7)],rgba('#4c6438',120),1)
# front of bowl overlays the fruit
poly(d,[(888,680),(1032,680),(1022,708),(998,718),(960,722),(922,718),(898,708)],'#e0d2b7')
poly(d,[(888,680),(1032,680),(1022,700),(898,700)],'#f0e6d1')
poly(d,[(898,700),(1022,700),(1018,708),(998,717),(960,720),(922,716),(902,708)],'#cbb697')
line(d,bez([(890,681),(940,694),(980,696),(1030,681)],40),'#fbf4e3',3)
line(d,bez([(902,709),(940,718),(980,719),(1020,708)],40),rgba('#9e8768',120),2)
# soft reflected orange glow on bowl
glow=soft_layer(lambda dd: dd.ellipse([sc(914),sc(686),sc(1008),sc(712)],fill=(226,134,70,45)),blur=8)
img=Image.alpha_composite(img.convert('RGBA'),glow).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# coffee mug
sh=soft_layer(lambda dd: dd.ellipse([sc(760),sc(686),sc(842),sc(724)],fill=(63,38,22,95)),blur=5)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
rrect(d,(766,642,828,694),10,'#efe2c9')
rrect(d,(766,642,828,694),10,None,'#bda98a',1)
ell(d,(766,641,828,654),'#fff8e9')
ell(d,(772,643,822,652),'#6a4930')
ell(d,(775,644,819,650),'#8b5b37')
# coffee crema highlight
arc(d,(779,644,815,652),200,340,rgba('#c89157',150),2)
# handle
arc(d,(816,653,846,683),270,90,'#cbb695',5)
# mug shading
line(d,[(772,656),(774,686)],rgba('#c7b192',120),2)
line(d,[(818,656),(816,686)],rgba('#fffaf0',80),1)
# little heart? no.
# steam curls
for k,(sx,off) in enumerate([(785,0),(805,8),(795,16)]):
    pts=bez([(sx,634),(sx-12+off,612),(sx+7+off,594),(sx-3+off,570)],60)
    line(d,pts,rgba('#fff8eb',85),3)
    line(d,pts,rgba('#fffdf7',40),1)

# small flower vase
sh=soft_layer(lambda dd: dd.ellipse([sc(1044),sc(686),sc(1116),sc(718)],fill=(63,38,22,90)),blur=5)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
# stems
for k in range(7):
    sx=1062+k*7
    line(d,bez([(sx,676),(sx+random.uniform(-10,10),640),(sx+random.uniform(-20,20),600)],40),'#5e7447',2)
    # leaves
    ell(d,(sx-6,648-k*4,sx+2,654-k*4),'#778b59')
# daisies
for k,(fx,fy) in enumerate([(1052,600),(1073,584),(1098,596),(1112,618),(1084,620),(1062,628),(1105,640)]):
    r=7+random.uniform(-1,1)
    for j in range(8):
        a=j*math.tau/8
        ex=fx+math.cos(a)*r; ey=fy+math.sin(a)*r
        ell(d,(ex-4,ey-3,ex+4,ey+3),'#fff8e6')
    ell(d,(fx-4,fy-4,fx+4,fy+4),'#e0a63c')
# vase
poly(d,[(1058,646),(1110,646),(1102,698),(1066,698)],'#96a282', rgba('#5f7059',120),1)
poly(d,[(1062,650),(1080,650),(1077,694),(1068,694)],rgba('#d9e0cb',90))
ell(d,(1059,642,1109,652),'#b4bea2')

# utensil crock before the range
sh=soft_layer(lambda dd: dd.ellipse([sc(1118),sc(688),sc(1174),sc(720)],fill=(62,38,22,100)),blur=5)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
# spoons
for k,(sx,tx) in enumerate([(1130,1122),(1141,1147),(1152,1158)]):
    line(d,[(sx,666),(tx,612)],'#8d5c34',3)
    ell(d,(tx-7,600,tx+7,618),'#b17b48')
    line(d,[(tx-4,604),(tx+3,613)],rgba('#e4b47e',90),1)
# crock
rrect(d,(1120,650,1172,700),8,'#7f9684')
rrect(d,(1120,650,1172,660),8,'#a8b8a6')
rrect(d,(1125,658,1167,697),6,None,'#5e7464',1)
ell(d,(1122,646,1170,660),'#667d6d')
ell(d,(1126,648,1166,658),'#93a691')
# speckles
for k in range(14):
    x=random.uniform(1127,1165); y=random.uniform(664,693)
    ell(d,(x-1,y-1,x+1,y+1),rgba('#4e6455',90))
# highlight
line(d,[(1128,666),(1128,690)],rgba('#d9e2d2',100),2)

# ============================================================
# RANGE + HOOD
# ============================================================
# hood
sh=soft_layer(lambda dd: dd.rectangle([sc(1194),sc(150),sc(1496),sc(330)],fill=(60,38,24,80)),blur=14)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
poly(d,[(1176,300),(1508,300),(1472,120),(1212,120)],'#e4cfb0')
poly(d,[(1176,300),(1508,300),(1508,318),(1176,318)],'#c9af8c')
poly(d,[(1212,120),(1472,120),(1462,108),(1222,108)],'#b88f62')
# hood shading & panels
line(d,[(1212,120),(1180,300)],'#c3a582',3)
line(d,[(1472,120),(1504,300)],'#f4e6ce',2)
line(d,[(1250,300),(1240,145)],rgba('#b59774',80),2)
line(d,[(1320,300),(1320,150)],rgba('#b59774',55),2)
# wood strap
rrect(d,(1192,156,1492,172),3,'#9d6a3e')
rrect(d,(1192,156,1492,162),3,'#cb9660')
# small rivets
for x in [1208,1244,1280,1316,1352,1388,1424,1460,1476]:
    ell(d,(x-3,160,x+3,168),'#d8a866')
# warm copper trim at the mouth of the hood
rrect(d,(1194,289,1490,301),3,'#a97645')
rrect(d,(1194,289,1490,293),3,'#d5a267')
line(d,[(1198,297),(1486,297)],rgba('#5c3a25',110),1)
# gentle panel shading on the hood face
line(d,[(1240,176),(1218,288)],rgba('#c7a985',65),3)
line(d,[(1320,176),(1320,288)],rgba('#c7a985',45),2)
line(d,[(1402,176),(1424,288)],rgba('#c7a985',55),2)
# under hood light
img=add_radial_glow(img,1342,520,330,270,'#ffd38b',70,1.8); d=ImageDraw.Draw(img,'RGBA')
# warm bulb strip
rrect(d,(1230,310,1454,318),3,'#f4c879')

# hood underside ambient shade
hs=soft_layer(lambda dd: dd.polygon([P(1184,292),P(1502,292),P(1486,332),P(1200,332)],fill=(57,39,25,80)),blur=10)
img=Image.alpha_composite(img.convert('RGBA'),hs).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
# range contact shadow on the boards
sh=soft_layer(lambda dd: dd.ellipse([sc(1150),sc(950),sc(1530),sc(1000)],fill=(39,25,16,140)),blur=12)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
# range body
sh=soft_layer(lambda dd: dd.rectangle([sc(1176),sc(660),sc(1510),sc(975)],fill=(54,35,22,110)),blur=12)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
rrect(d,(1178,640,1506,966),8,'#e8d7ba')
grad_rect(img,(1180,650,1504,960),[(0,'#f2e3c9'),(0.55,'#e2cfae'),(1,'#c9b18d')])
rrect(d,(1178,640,1506,966),8,None,'#b3936d',2)
# top edge / cooktop
rrect(d,(1170,626,1514,658),6,'#3f3d37')
rrect(d,(1170,626,1514,636),6,'#6f6a5c')
# burners/grates
for bx in [1230,1352,1460]:
    ell(d,(bx-40,630,bx+40,652),'#262622')
    for k in range(3):
        line(d,[(bx-36,636+k*5),(bx+36,636+k*5)],'#5a564c',2)
# front controls
rrect(d,(1194,664,1490,690),4,'#d5c29f')
for i in range(4):
    x=1220+i*70
    ell(d,(x-10,669,x+10,689),'#8d7350'); ell(d,(x-8,671,x+8,687),'#d0b27d')
    line(d,[(x,678),(x+5,672)],'#5e452b',2)
# oven door
rrect(d,(1200,700,1484,948),7,'#ead9bc')
rrect(d,(1200,700,1484,948),7,None,'#b6966e',2)
rrect(d,(1214,712,1470,800),5,'#f5e8d0')
rrect(d,(1222,718,1462,794),3,None,'#cbb08a',2)
# glass window
rrect(d,(1226,804,1458,914),7,'#4b4135')
grad_rect(img,(1232,810,1452,908),[(0,'#6d5c44'),(0.4,'#3f382f'),(1,'#2c2a27')])
# reflection on glass
poly(d,[(1244,908),(1310,810),(1342,810),(1276,908)],rgba('#e8ce9e',38))
arc(d,(1226,804,1458,914),20,160,'#b9a17c',2)
# oven handle
rrect(d,(1238,745,1448,758),6,'#b98543')
rrect(d,(1238,745,1448,751),6,'#edc77b')
for hx_ in [1250,1436]:
    rrect(d,(hx_-5,753,hx_+5,765),3,'#7a542c')
# brand plaque
rrect(d,(1310,770,1376,783),2,'#c9a466')
# linen towel hanging on handle
poly(d,[(1268,758),(1310,758),(1318,858),(1302,876),(1276,860)],'#e2d0b3',rgba('#8f7658',80),1)
poly(d,[(1268,758),(1310,758),(1312,780),(1272,780)],'#c8b393')
for k in range(3):
    line(d,[(1274+k*3,787),(1282+k*3,860)],rgba('#b99f7d',80),1)
for y in [822,838,854]:
    line(d,[(1275,y),(1314,y-2)],rgba('#a95b45',150),3)
    line(d,[(1276,y+4),(1314,y+2)],rgba('#f3e1c6',110),2)
# range side highlights
line(d,[(1182,646),(1182,950)],'#fff4dc',3)
line(d,[(1502,646),(1502,950)],rgba('#8e724f',80),2)

# ============================================================
# KETTLE
# ============================================================
# position on right burner
kx,ky=1392,590
# shadow on cooktop
sh=soft_layer(lambda dd: dd.ellipse([sc(kx-56),sc(624),sc(kx+56),sc(650)],fill=(20,17,14,150)),blur=5)
img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
# body
ell(d,(kx-48,558,kx+48,646),'#b6653c')
grad_rect(img,(kx-44,566,kx+44,638),[(0,'#8f4e30'),(0.22,'#cf7f4d'),(0.5,'#b9683d'),(0.8,'#7e432b')])
ell(d,(kx-48,548,kx+48,590),'#c87949')
ell(d,(kx-42,550,kx+38,580),'#d88a55')
ell(d,(kx-40,552,kx+40,586),'#a95e36')
# lid
ell(d,(kx-27,540,kx+27,560),'#c37a48')
ell(d,(kx-22,541,kx+22,556),'#d88e59')
ell(d,(kx-7,530,kx+7,542),'#8b5a32')
ell(d,(kx-4,530,kx+4,538),'#d3a260')
# spout
poly(d,[(kx-44,570),(kx-78,550),(kx-72,565),(kx-42,588)],'#b6653c', rgba('#6f3d26',100),1)
line(d,[(kx-72,555),(kx-48,575)],'#e0a06c',2)
# handle arch
line(d,bez([(kx-28,550),(kx-38,505),(kx+32,505),(kx+28,550)],60),'#5e412b',7)
line(d,bez([(kx-28,546),(kx-34,512),(kx+28,512),(kx+24,546)],30),'#c9974e',2)
# highlights
line(d,[(kx-30,575),(kx-34,612)],rgba('#f4bc86',150),4)
ell(d,(kx-28,578,kx-18,598),rgba('#ffd4a4',90))
# steam
for k,(sx,off) in enumerate([(kx-5,0),(kx+12,9),(kx-18,15)]):
    pts=bez([(sx,522),(sx-12+off,495),(sx+10+off,470),(sx-4+off,440)],70)
    line(d,pts,rgba('#fff8e9',75),3)

# ============================================================
# HANGING PLANT top-left
# ============================================================
# macrame hanger
line(d,[(58,0),(58,60)],'#a98a63',2)
for k in range(4):
    line(d,bez([(46+k*8,28),(58,44),(58,68)],20),'#b99a72',1)
# pot
poly(d,[(38,72),(82,72),(76,104),(44,104)],'#bb7c4d')
poly(d,[(42,76),(78,76),(73,101),(47,101)],'#a96b40')
rrect(d,(36,67,84,78),3,'#d09962')
# trailing vines
for k in range(7):
    start=(44+random.uniform(0,34),78)
    pts=bez([start,(start[0]+random.uniform(-22,22),140),(start[0]+random.uniform(-38,38),200),(start[0]+random.uniform(-40,40),270+random.uniform(0,90))],50)
    line(d,pts,'#4f6a3e',2)
    for j in range(1,len(pts)-2,5):
        x,y=pts[j]
        ell(d,(x-6,y-4,x+6,y+4),random.choice(['#5f7746','#738a50','#47603a']))
# leaves highlight
for k in range(16):
    x=random.uniform(20,110); y=random.uniform(110,310)
    ell(d,(x-3,y-2,x+3,y+2),rgba('#a9bd7e',90))

# ============================================================
# SUNBEAMS + LIGHT
# ============================================================
beams=Image.new('RGBA',(CW,CH),(0,0,0,0)); bd=ImageDraw.Draw(beams,'RGBA')
# broad shafts from window toward lower left/center
for (x0,x1,alpha) in [(180,250,36),(270,330,32),(370,420,28),(470,520,24)]:
    poly(bd,[(x0,130),(x1,130),(x1+150,1000),(x0+60,1000)],fill=(255,224,165,alpha))
# narrower rays
for (x0,x1,alpha) in [(220,232,24),(300,310,24),(390,400,20),(500,508,18)]:
    poly(bd,[(x0,130),(x1,130),(x1+110,1000),(x0+80,1000)],fill=(255,236,185,alpha))
beams=beams.filter(ImageFilter.GaussianBlur(20*S))
img=Image.alpha_composite(img.convert('RGBA'),beams).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# light pool on counter and lower cabinets
pool=Image.new('RGBA',(CW,CH),(0,0,0,0)); pd=ImageDraw.Draw(pool,'RGBA')
pd.polygon([P(260,700),P(560,700),P(690,960),P(330,960)],fill=(255,207,131,34))
pd.ellipse([P(60,690),P(700,760)],fill=(255,220,160,35))
pd.ellipse([P(800,690),P(1180,760)],fill=(255,220,160,24))
pool=pool.filter(ImageFilter.GaussianBlur(24*S))
img=Image.alpha_composite(img.convert('RGBA'),pool).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
# countertop highlights
line(d,[(188,700),(540,700)],rgba('#ffe2ac',110),3)
line(d,[(650,701),(920,701)],rgba('#ffdaa0',70),2)
# sink rim sun
line(d,[(312,690),(420,690)],rgba('#fff7df',130),2)

# cat on windowsill (drawn after light for rim light)
CUSH_Y=568
# cushion
rrect(d,(500,548,650,584),12,'#c26d55')
rrect(d,(506,552,644,578),10,'#d98a6d')
for k in range(5):
    line(d,[(512+k*26,556),(508+k*26,578)],rgba('#a9543f',100),1)
line(d,[(506,552),(644,552)],'#edb092',2)
# cat cast shadow on the cushion
cs=soft_layer(lambda dd: dd.ellipse([sc(536),sc(550),sc(640),sc(580)],fill=(89,45,31,80)),blur=6)
img=Image.alpha_composite(img.convert('RGBA'),cs).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')
# cat body
# tail curl
line(d,bez([(638,562),(634,536),(606,528),(586,544),(580,558)],50),'#d47c3d',10)
line(d,bez([(636,559),(630,540),(608,534),(592,546)],30),'#b76332',3)
# body
ell(d,(548,526,636,568),'#d98242')
ell(d,(556,528,630,559),'#e79a56')
# haunch
ell(d,(600,528,642,566),'#cf7538')
# head
ell(d,(522,524,574,566),'#e08a45')
ell(d,(527,527,570,558),'#eaa362')
# ears
poly(d,[(526,530),(532,512),(544,528)],'#d47c3d','#b76332',1)
poly(d,[(556,526),(566,510),(574,530)],'#d47c3d','#b76332',1)
poly(d,[(531,527),(535,517),(542,528)],'#e8a68b')
poly(d,[(560,525),(566,514),(570,527)],'#e8a68b')
# face shading
ell(d,(531,536,566,557),'#f0aa6c')
# closed eyes
arc(d,(532,538,546,548),200,340,'#5e3a27',2)
arc(d,(551,538,565,548),200,340,'#5e3a27',2)
# nose and mouth
poly(d,[(546,549),(553,549),(550,553)],'#b65c56')
line(d,[(550,553),(550,557)],'#7d4a37',1)
line(d,[(550,557),(545,560)],'#7d4a37',1)
line(d,[(550,557),(555,560)],'#7d4a37',1)
# whiskers
for k in range(3):
    line(d,[(541,552),(517,547+k*4)],rgba('#6e4a35',160),1)
    line(d,[(559,552),(581,547+k*4)],rgba('#6e4a35',160),1)
# stripes
for (sx,sy,ex,ey) in [(560,531,566,544),(572,534,578,547),(584,532,590,547),(599,534,603,550),(618,536,620,552)]:
    line(d,bez([(sx,sy),(sx+2,(sy+ey)/2),(ex,ey)],20),rgba('#a9552d',120),2)
# paws tucked
ell(d,(537,556,558,571),'#f1b47e')
ell(d,(566,558,586,571),'#f0ad72')
line(d,[(542,562),(552,562)],rgba('#b46d4a',100),1)
line(d,[(570,563),(580,563)],rgba('#b46d4a',100),1)
# fur highlight rim
arc(d,(523,525,575,567),185,275,rgba('#ffe0b3',150),2)
arc(d,(548,526,636,568),185,280,rgba('#ffcf92',110),2)
# sleeping z
# (small, subtle)
# fill mouth highlight

# ============================================================
# DUST MOTES in beams
# ============================================================
motes=Image.new('RGBA',(CW,CH),(0,0,0,0)); md=ImageDraw.Draw(motes,'RGBA')
for i in range(62):
    x=random.uniform(170,660); y=random.uniform(120,760)
    # concentrate in the shafts of light
    if random.random()<0.72: x=random.uniform(210,580)
    r=random.uniform(1.0,3.4)
    a=int(random.uniform(35,115))
    md.ellipse([sc(x-r),sc(y-r),sc(x+r),sc(y+r)],fill=(255,238,188,a))
motes=motes.filter(ImageFilter.GaussianBlur(2*S))
img=Image.alpha_composite(img.convert('RGBA'),motes).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# soft morning shafts crossing the room
rays=Image.new('RGBA',(CW,CH),(0,0,0,0)); ryd=ImageDraw.Draw(rays,'RGBA')
for (x0,x1,tx0,tx1,a) in [
    (180,235,40,130,18),
    (300,355,150,245,16),
    (410,458,270,355,13),
    (520,565,430,500,10),
]:
    ryd.polygon([P(x0,120),P(x1,120),P(tx1,1024),P(tx0,1024)],fill=(255,226,166,a))
rays=rays.filter(ImageFilter.GaussianBlur(28*S))
img=Image.alpha_composite(img.convert('RGBA'),rays).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# window bloom
lum=img.convert('L')
mask=lum.point(lambda v: 0 if v<212 else min(255,int((v-212)*2.1)))
mask=mask.filter(ImageFilter.GaussianBlur(13*S)).point(lambda v:int(v*0.55))
bloom=Image.new('RGBA',(CW,CH),(255,235,196,0)); bloom.putalpha(mask)
img=Image.alpha_composite(img.convert('RGBA'),bloom).convert('RGB'); d=ImageDraw.Draw(img,'RGBA')

# ============================================================
# FINAL ATMOSPHERE
# ============================================================
# warm radial light from window
img=add_radial_glow(img,410,330,700,470,'#ffcf87',58,1.7)

# vignette
vig=Image.new('L',(CW,CH),0)
vd=ImageDraw.Draw(vig)
vd.ellipse([sc(-260),sc(-240),sc(W+260),sc(H+240)],fill=255)
vig=vig.filter(ImageFilter.GaussianBlur(110*S))
dark=Image.new('RGBA',(CW,CH),(47,30,20,255))
dark.putalpha(ImageChops.invert(vig).point(lambda v:int(v*0.40)))
img=Image.alpha_composite(img.convert('RGBA'),dark).convert('RGB')

# texture and grade
img=add_texture(img, blur=2.2, amount=0.075)
img=ImageEnhance.Color(img).enhance(1.09)
img=ImageEnhance.Contrast(img).enhance(1.055)
img=ImageEnhance.Brightness(img).enhance(1.02)

# downsample
out=img.resize((W,H),Image.Resampling.LANCZOS)
out.save('/tmp/vellery-2mm31_1h/work/cozy_kitchen_morning.png')
out.save('/tmp/vellery-2mm31_1h/work/cozy_kitchen_morning.jpg',quality=94)
print('saved', out.size)
