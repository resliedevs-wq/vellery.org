from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance
import math, random

W, H = 1600, 1200
S = 2
random.seed(42)

img = Image.new("RGB", (W*S, H*S), "#f2e2cb")
d = ImageDraw.Draw(img, "RGBA")

def X(v):
    return int(round(v*S))

def B(b):
    return tuple(X(v) for v in b)

def P(ps):
    return [(X(x), X(y)) for x,y in ps]

def col(c):
    if isinstance(c, str):
        from PIL import ImageColor
        return ImageColor.getrgb(c)
    return tuple(c[:3])

def fill_alpha(c):
    if c is None:
        return None
    if isinstance(c, str):
        return (*col(c), 255)
    if len(c)==4: return tuple(c)
    return (*tuple(c)[:3], 255)

def line(ps, fill, width=1, joint="curve"):
    d.line(P(ps), fill=fill_alpha(fill), width=max(1, X(width)), joint=joint)

def poly(ps, fill, outline=None, width=1):
    d.polygon(P(ps), fill=fill_alpha(fill))
    if outline:
        d.line(P(ps)+[P(ps)[0]], fill=fill_alpha(outline), width=max(1,X(width)), joint="curve")

def ellipse(b, fill, outline=None, width=1):
    d.ellipse(B(b), fill=fill_alpha(fill))
    if outline:
        d.ellipse(B(b), outline=fill_alpha(outline), width=max(1,X(width)))

def rrect(b, r, fill, outline=None, width=1):
    d.rounded_rectangle(B(b), radius=X(r), fill=fill_alpha(fill))
    if outline:
        d.rounded_rectangle(B(b), radius=X(r), outline=fill_alpha(outline), width=max(1,X(width)))

def rectangle(b, fill, outline=None, width=1):
    d.rectangle(B(b), fill=fill_alpha(fill))
    if outline:
        d.rectangle(B(b), outline=fill_alpha(outline), width=max(1,X(width)))

def lin_gradient(w, h, c0, c1, horizontal=False):
    c0 = col(c0); c1 = col(c1)
    if horizontal:
        im = Image.new("RGB", (w,1))
    else:
        im = Image.new("RGB", (1,h))
    px = im.load()
    n = w if horizontal else h
    for i in range(n):
        t = i/max(1,n-1)
        c = tuple(round(c0[k]*(1-t)+c1[k]*t) for k in range(3))
        if horizontal: px[i,0] = c
        else: px[0,i] = c
    return im.resize((w,h), Image.BILINEAR)

def grad_rect(b, c0, c1, radius=0, horizontal=False, outline=None, width=1):
    x0,y0,x1,y1 = [X(v) for v in b]
    bw,bh = max(1,x1-x0), max(1,y1-y0)
    g = lin_gradient(bw,bh,c0,c1,horizontal)
    mask = Image.new("L",(bw,bh),0)
    md = ImageDraw.Draw(mask)
    if radius>0:
        md.rounded_rectangle((0,0,bw-1,bh-1), radius=X(radius), fill=255)
    else:
        md.rectangle((0,0,bw-1,bh-1), fill=255)
    img.paste(g,(x0,y0),mask)
    if outline:
        d.rounded_rectangle(B(b), radius=X(radius), outline=fill_alpha(outline), width=max(1,X(width)))

def radial_glow(cx, cy, rx, ry, color, alpha=120, blur=18, screen=False):
    x0,y0 = X(cx-rx), X(cy-ry)
    x1,y1 = X(cx+rx), X(cy+ry)
    w,h = max(1,x1-x0), max(1,y1-y0)
    layer = Image.new("L",(w,h),0)
    ld = ImageDraw.Draw(layer)
    ld.ellipse((0,0,w-1,h-1), fill=alpha)
    layer = layer.filter(ImageFilter.GaussianBlur(X(blur)))
    img.paste(col(color),(x0,y0),layer)

def soft_shadow(b, offset=(0,8), blur=10, color=(70,40,20), alpha=80, radius=0):
    x0,y0,x1,y1 = [X(v) for v in b]
    ox,oy = X(offset[0]), X(offset[1])
    pad = X(blur)*2 + 4
    lw,lh = (x1-x0)+2*pad, (y1-y0)+2*pad
    mask = Image.new("L",(lw,lh),0)
    md = ImageDraw.Draw(mask)
    if radius>0:
        md.rounded_rectangle((pad+ox,pad+oy,pad+x1-x0+ox,pad+y1-y0+oy), radius=X(radius), fill=alpha)
    else:
        md.rectangle((pad+ox,pad+oy,pad+x1-x0+ox,pad+y1-y0+oy), fill=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(X(blur)))
    img.paste(col(color),(x0-pad,y0-pad),mask)
    d._image = img

def soft_ellipse_shadow(b, blur=12, color=(60,35,20), alpha=70):
    x0,y0,x1,y1 = [X(v) for v in b]
    pad = X(blur)*2+4
    w,h = x1-x0+2*pad, y1-y0+2*pad
    mask = Image.new("L",(w,h),0)
    ImageDraw.Draw(mask).ellipse((pad,pad,pad+x1-x0,pad+y1-y0), fill=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(X(blur)))
    img.paste(col(color),(x0-pad,y0-pad),mask)
    d._image = img

def radial_rect_glow(b, color, alpha=80, blur=20):
    # soft light inside a rectangular region
    x0,y0,x1,y1 = [X(v) for v in b]
    pad = X(blur)*2
    w,h = x1-x0+2*pad, y1-y0+2*pad
    mask = Image.new("L",(w,h),0)
    ImageDraw.Draw(mask).rounded_rectangle((pad,pad,pad+x1-x0,pad+y1-y0),radius=X(20),fill=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(X(blur)))
    img.paste(col(color),(x0-pad,y0-pad),mask)
    d._image = img

# soft brush helper for highlights
def brush_line(ps, fill, width=6, blur=3):
    layer = Image.new("RGBA", img.size, (0,0,0,0))
    ld = ImageDraw.Draw(layer)
    ld.line(P(ps), fill=fill_alpha(fill), width=max(1,X(width)), joint="curve")
    for p in (ps[0], ps[-1]):
        ld.ellipse((X(p[0]-width/2),X(p[1]-width/2),X(p[0]+width/2),X(p[1]+width/2)), fill=fill_alpha(fill))
    layer = layer.filter(ImageFilter.GaussianBlur(X(blur)))
    img.paste(Image.alpha_composite(img.convert("RGBA"),layer).convert("RGB"))
    d._image = img

# ---------- WALL ----------
wall_grad = lin_gradient(W*S, H*S, "#faefdd", "#e8ceb0")
img.paste(wall_grad,(0,0))
# broad uneven plaster passages
for i in range(35):
    x = random.uniform(-100, W)
    y = random.uniform(-50, 760)
    rx = random.uniform(80, 320); ry = random.uniform(40, 160)
    c = random.choice(["#fff6e7", "#f0d9ba", "#efd7ba"])
    a = random.randint(8, 22)
    radial_glow(x,y,rx,ry,c,a,60)

# pale blue-grey undertone in shadows
for (x,y,rx,ry,a) in [(90,760,220,190,22),(1490,720,260,220,28),(250,120,300,160,12)]:
    radial_glow(x,y,rx,ry,"#b9b3a0",a,80)

# wainscot beadboard strips (small, visible at edges)
for x in range(20, 1580, 26):
    line([(x,1088),(x,1092)],"#d8c0a2",1)

# ---------- WINDOW (outside view first) ----------
# wall shadow behind frame
soft_shadow((398,86,902,642), offset=(18,22), blur=26, color=(94,62,35), alpha=80, radius=14)
# outer frame
grad_rect((394,82,906,636), "#d5a064", "#8d5632", radius=14, horizontal=False,
          outline="#744424", width=2)
# frame top highlight
rrect((404,90,896,106), 7, "#e4b77f")
# inner bevel shadow
rrect((414,102,886,620), 9, "#6e4327")
# glass opening
OX0,OY0,OX1,OY1 = 430,118,870,604
grad_rect((OX0,OY0,OX1,OY1), "#a9c4cc", "#f4d3a0", radius=2)

# outside sky
sky = lin_gradient(X(OX1-OX0), X(OY1-OY0), "#86abc1", "#f8d6a0")
# deepen sky top
top_ov = Image.new("RGBA", sky.size,(0,0,0,0))
td = ImageDraw.Draw(top_ov)
for i in range(sky.size[1]):
    pass
img.paste(sky,(X(OX0),X(OY0)))
# clouds
for (cx,cy,rx,ry,a) in [(510,210,60,17,40),(575,178,42,13,28),(760,240,74,19,30),(830,195,50,13,26)]:
    radial_glow(cx,cy,rx,ry,"#f9f4df",a,10)
# sun glow and disc
radial_glow(702,408,190,190,"#ffe6a8",95,55)
radial_glow(702,408,92,92,"#fff0bf",130,24)
ellipse((678,384,726,432),"#fff6d8")
# hills
poly([(430,462),(500,435),(566,452),(620,428),(690,450),(758,430),(820,450),(870,438),(870,510),(430,510)], "#9aa59a")
poly([(430,492),(495,465),(566,484),(620,466),(695,488),(760,468),(820,488),(870,478),(870,560),(430,560)], "#8c997d")
poly([(430,530),(490,506),(560,520),(620,502),(680,526),(750,510),(810,528),(870,513),(870,604),(430,604)], "#67805d")
# distant warm field
poly([(430,532),(520,520),(610,534),(700,519),(790,534),(870,524),(870,580),(430,580)], "#84925f")
# morning haze
radial_glow(680,500,220,100,"#f6d69b",40,30)
# trees / bushes outside
# left tree
line([(482,510),(482,580)],"#4e4933",5)
for (cx,cy,rx,ry,c) in [(468,475,30,32,"#506c49"),(500,470,35,38,"#5f7b50"),(475,500,42,24,"#496340"),(515,500,32,20,"#5d7a4d")]:
    ellipse((cx-rx,cy-ry,cx+rx,cy+ry),c)
# sunlit leaves
for (cx,cy,rx,ry) in [(470,458,10,6),(504,464,12,7),(486,486,10,5),(514,490,8,5)]:
    ellipse((cx-rx,cy-ry,cx+rx,cy+ry),"#a9b774")
# right bushes
for (cx,cy,rx,ry,c) in [(795,530,34,24,"#7b8552"),(830,522,28,20,"#899461"),(858,538,25,18,"#6d7b4c")]:
    ellipse((cx-rx,cy-ry,cx+rx,cy+ry),c)
# tiny fence in distance
for x in range(438,566,18):
    line([(x,548),(x,572)],"#d8c7a2",2)
line([(434,554),(566,554)],"#d8c7a2",2)
# birds
for (bx,by) in [(560,188),(576,180),(835,172)]:
    d.arc(B((bx-7,by-4,bx,by+2)),200,340,fill=(84,87,80,170),width=X(1.5))
    d.arc(B((bx,by-4,bx+7,by+2)),200,340,fill=(84,87,80,170),width=X(1.5))

# glass tint / reflections
glass_ov = Image.new("RGBA",(X(OX1-OX0),X(OY1-OY0)),(150,190,205,16))
img.paste(Image.alpha_composite(img.crop(B((OX0,OY0,OX1,OY1))).convert("RGBA"), glass_ov).convert("RGB"),(X(OX0),X(OY0)))
# reflection stripes
for pts_ in [
    [(450,590),(540,130),(590,130),(500,590)],
    [(690,590),(780,130),(810,130),(720,590)],
    [(800,590),(860,300),(870,340),(815,590)],
]:
    poly(pts_, (255,248,226,18))
# faint distilled glass shading at corners
for pts_ in [[(430,118),(470,118),(430,166)],[(870,118),(830,118),(870,166)]]:
    poly(pts_,(255,255,255,20))

# mullions
for b,r in [((638,118,656,604),3),((430,336,870,354),3)]:
    grad_rect(b,"#e0b079","#a46a3c",radius=r,outline="#7f4b2b",width=1.5)
    if b[2]-b[0] > b[3]-b[1]:
        rrect((b[0]+4,b[1]+3,b[2]-4,b[1]+10),3,"#f0c994")
    else:
        rrect((b[0]+3,b[1]+4,b[0]+10,b[3]-4),3,"#f0c994")
# inner frame shading
d.rectangle(B((430,118,870,604)), outline=(84,52,31,130), width=X(2))
# pane shadows near frame
line([(434,120),(434,600)],"#5f452f",2)
line([(430,120),(866,120)],"#5f452f",2)

# window sill
soft_shadow((380,590,920,646), offset=(0,11), blur=12, color=(84,50,30), alpha=90, radius=6)
grad_rect((374,588,926,612), "#e0ac72", "#b97b46", radius=5, outline="#8c5631", width=2)
grad_rect((380,610,920,640), "#a86e3e", "#7d4a2a", radius=3, outline="#744326", width=1.5)
rrect((388,592,912,600), 3, "#f0c68d")
# sill brackets
for x in (420,858):
    poly([(x-9,638),(x+9,638),(x+5,663),(x-5,663)],"#8f5b35",outline="#6f4428",width=1)

# ---------- BACKSPLASH ----------
# glaze tiles, low contrast
rectangle((0,650,1600,817),"#e6d3b8")
# tile grid
tile_w, tile_h = 64, 54
start_y = 656
for row,ty in enumerate(range(start_y, 817, tile_h)):
    off = 32 if row%2 else 0
    for tx in range(-tile_w+off, 1600, tile_w):
        c = ["#eee0c9","#ead9bf","#f2e5d0","#e9d7bd"][(row*3 + (tx//tile_w))%4]
        rectangle((tx+2,ty+2,tx+tile_w-3,ty+tile_h-3), c)
        # glaze streak
        line([(tx+9,ty+9),(tx+tile_w-10,ty+7)],(255,255,255,26),1)
        line([(tx+12,ty+tile_h-9),(tx+tile_w-14,ty+tile_h-12)],(140,110,80,20),1)
# tile grout
for ty in range(start_y,818,tile_h):
    line([(0,ty),(1600,ty)],"#cdb494",2)
for row,ty in enumerate(range(start_y, 817, tile_h)):
    off = 32 if row%2 else 0
    for tx in range(-tile_w+off,1600,tile_w):
        line([(tx,ty),(tx,ty+tile_h)],"#cdb494",2)
# soft ambient shading over backsplash
radial_rect_glow((0,650,1600,820),"#8b5738",24,70)
radial_glow(650,690,400,90,"#fff6df",34,45)

# decorative tile band under sill? subtle
line([(0,650),(1600,650)],"#b79067",3)

# ---------- LEFT SHELVES ----------
def shelf(x0,x1,y,depth=16):
    soft_shadow((x0,y,x1,y+depth+5), offset=(0,10), blur=12, color=(80,45,25), alpha=80)
    grad_rect((x0,y,x1,y+depth), "#c78e55", "#8e5a33", radius=2, outline="#714125", width=1.5)
    rrect((x0+5,y+2,x1-5,y+7),2,"#e3b67d")
    # brackets
    for bx in (x0+24,x1-24):
        poly([(bx-9,y+depth),(bx+9,y+depth),(bx,y+depth+24)],"#80502e",outline="#643d23",width=1)

shelf(66,352,352)
shelf(66,352,522)

# objects: upper shelf
# stack of bowls
for i,(yy,ww,c) in enumerate([(342,66,"#eadcc5"),(327,58,"#f2e6d3"),(313,50,"#dfcfb8")]):
    ellipse((100-ww/2,yy-18,100+ww/2,yy+4),c,outline="#bfae96",width=1)
    ellipse((100-ww/2+4,yy-17,100+ww/2-4,yy-7),None,outline="#fff8e8",width=1)
# pitcher
soft_shadow((164,268,234,352),offset=(0,5),blur=6,color=(60,40,25),alpha=70)
rrect((166,284,230,347),16,"#dfe1d2",outline="#a8aa96",width=1.5)
ellipse((166,272,230,296),"#eef0e3",outline="#a8aa96",width=1.5)
ellipse((170,275,226,289),"#c9cbb8")
# handle
d.arc(B((224,294,252,336)),270,110,fill=(168,170,150,255),width=X(6))
line([(228,298),(236,298)],"#eef0e3",5)
# spout
poly([(165,302),(151,294),(156,312),(166,314)],"#dfe1d2",outline="#a8aa96",width=1)
# little green stripe
line([(174,310),(222,310)],"#7d9880",3)
# plant
soft_shadow((256,300,326,352),offset=(0,5),blur=7,color=(60,40,25),alpha=70)
rrect((272,318,312,347),5,"#b9714d",outline="#8e5137",width=1.5)
rrect((268,312,316,323),4,"#cf8861",outline="#8e5137",width=1)
for (sx,sy,tx,ty) in [(292,316,274,286),(294,316,306,281),(288,316,286,274),(299,315,318,293)]:
    line([(sx,sy),(tx,ty)],"#4e6b45",3)
    ellipse((tx-10,ty-8,tx+10,ty+8),"#6e8d5b")
    ellipse((tx-6,ty-5,tx+2,ty+3),"#92aa76")

# lower shelf: books and jars
for i,(bx,by,bw,bh,c) in enumerate([(84,440,20,80,"#9c6b54"),(106,450,18,70,"#7c8a72"),(126,446,22,74,"#c2a46f")]):
    rrect((bx,by,bx+bw,by+bh),2,c,outline="#6d553d",width=1)
    line([(bx+4,by+12),(bx+bw-4,by+12)],"#e9dcc3",2)
# jam jars
for (bx,bw,bh,c) in [(168,38,54,"#c96e48"),(214,34,64,"#d7a85e")]:
    soft_shadow((bx,522-bh,bx+bw,522),offset=(0,4),blur=5,color=(50,30,15),alpha=55)
    rrect((bx,522-bh,bx+bw,520),5,"#d9d2c0",outline="#9e9582",width=1.5)
    rrect((bx+3,522-bh+10,bx+bw-3,522-4),4,c)
    rrect((bx+5,522-bh-4,bx+bw-5,522-bh+7),3,"#efe7d7",outline="#9e9582",width=1)
    line([(bx+bw/2,522-bh-2),(bx+bw/2,516)],"#8b6b50",2)
# crock with utensils
rrect((258,470,314,520),8,"#e4ded0",outline="#a69c88",width=1.5)
ellipse((258,466,314,484),"#f0eadc",outline="#a69c88",width=1.5)
line([(276,468),(270,424)],"#a77948",4)
ellipse((263,412,278,428),"#b98952")
line([(293,468),(303,430)],"#8b8f77",4)
ellipse((299,420,310,434),"#aeb29a")
line([(304,468),(319,440)],"#b78350",3)

# hanging garlic braid between shelf and counter
line([(202,548),(202,566)],"#8a744f",3)
for i in range(3):
    y = 566+i*25
    ellipse((188,y,216,y+22),"#eee2c7",outline="#c9b794",width=1)
    line([(195,y+4),(198,y+15)],"#d2c09d",2)
    line([(209,y+5),(207,y+16)],"#d2c09d",2)
# little dried chili string
line([(260,548),(260,560)],"#7d5f3e",2)
for i in range(3):
    ellipse((250,560+i*19,270,581+i*19),"#b34f37",outline="#863625",width=1)
    poly([(260,578+i*19),(256,589+i*19),(264,589+i*19)],"#8e3526")

# ---------- RIGHT SHELF + WALL CLOCK ----------
shelf(1044,1530,386)
# clock
soft_shadow((1300,166,1422,288),offset=(0,6),blur=10,color=(80,50,30),alpha=55)
ellipse((1304,168,1418,282),"#b87b47",outline="#744629",width=3)
ellipse((1314,178,1408,272),"#f1e3c9",outline="#c8a376",width=2)
ellipse((1320,184,1402,266),None,outline="#ddc7a5",width=1)
for a in range(0,360,30):
    r1 = 80 if a%90==0 else 85
    x1 = 1361+math.cos(math.radians(a))*r1
    y1 = 225+math.sin(math.radians(a))*r1
    x2 = 1361+math.cos(math.radians(a))*91
    y2 = 225+math.sin(math.radians(a))*91
    line([(x1,y1),(x2,y2)],"#8e6a45",2 if a%90==0 else 1)
# hands at 7:05
line([(1361,225),(1327,252)],"#5e4834",5)
line([(1361,225),(1386,190)],"#5e4834",4)
ellipse((1356,220,1366,230),"#8f6037")
# glass highlight
d.arc(B((1320,182,1400,250)),200,320,fill=(255,255,255,50),width=X(4))

# shelf objects
# plates standing
for i,(cx,w,h,c) in enumerate([(1083,48,66,"#f2e8d7"),(1124,48,66,"#dfd4bf")]):
    ellipse((cx-w/2,386-h,cx+w/2,386-4),c,outline="#b8a88f",width=1.5)
    ellipse((cx-w/2+6,386-h+7,cx+w/2-6,386-13),None,outline="#fffaf0",width=1.5)
    ellipse((cx-8,386-47,cx+8,386-35),None,outline="#c2b298",width=1)
# jars
jar_data=[(1160,42,56,"#c8b58f","#8d7652"),(1210,38,70,"#d4c8ad","#8f7d5e"),(1258,44,48,"#b98a58","#7d5834")]
for (jx,jw,jh,c,lid) in jar_data:
    soft_shadow((jx,386-jh,jx+jw,386),offset=(0,4),blur=4,color=(50,30,15),alpha=50)
    rrect((jx,386-jh,jx+jw,386),5,c,outline=lid,width=1.5)
    rrect((jx+4,386-jh-5,jx+jw-4,386-jh+8),3,lid)
    rectangle((jx+7,386-jh+15,jx+jw-7,386-8),(255,255,255,28))
# stack bowls
for i,(yy,ww,c) in enumerate([(380,66,"#e5d9c3"),(364,58,"#f2e8d5"),(349,50,"#d8cbb4")]):
    ellipse((1388-ww/2,yy-18,1388+ww/2,yy+4),c,outline="#b9a78f",width=1)
# pothos plant trailing
soft_shadow((1444,300,1518,386),offset=(0,5),blur=7,color=(50,35,20),alpha=65)
rrect((1462,342,1506,382),7,"#c78362",outline="#9b6046",width=1.5)
rrect((1458,336,1510,348),4,"#d99a78",outline="#9b6046",width=1)
line([(1484,340),(1474,306)],"#4d6b43",3)
for (tx,ty) in [(1466,320),(1483,304),(1498,316),(1452,344),(1512,352),(1478,372)]:
    ellipse((tx-9,ty-6,tx+9,ty+6),"#6f8d5b")
    ellipse((tx-5,ty-4,tx+1,ty+1),"#93ad77")
# trailing vine down shelf
for (sx,sy,tx,ty) in [(1504,380,1522,430),(1522,430,1500,472),(1500,472,1526,500)]:
    line([(sx,sy),(tx,ty)],"#526e45",3)
    ellipse((tx-10,ty-6,tx+10,ty+7),"#6d8c5a")
# mugs hanging beneath shelf
for i,(mx,c) in enumerate([(1110,"#e8dfcf"),(1160,"#aab6a4"),(1210,"#d2a07c")]):
    line([(mx,408),(mx,424)],"#7a674f",2)
    d.arc(B((mx-22,430,mx+22,462)),0,180,fill=(80,80,70,220),width=X(2))
    rrect((mx-19,422,mx+19,458),7,c,outline="#988d7c",width=1.2)
    ellipse((mx-16,422,mx+16,432),None,outline="#f6efe2",width=1.2)
    d.arc(B((mx+16,430,mx+33,452)),270,90,fill=(150,140,125,255),width=X(4))

# copper pans hanging between window and shelf
for (cx,cy,r) in [(960,266,40),(1004,326,32)]:
    line([(cx,180),(cx,cy-r+6)],"#7d6a52",2)
    line([(cx,180),(cx,201)],"#5f503d",4)
    ellipse((cx-r,cy-r,cx+r,cy+r),"#b8673e",outline="#7c3c24",width=3)
    ellipse((cx-r+8,cy-r+8,cx+r-8,cy+r-8),"#cf7e4d",outline="#8f472a",width=2)
    ellipse((cx-r+16,cy-r+16,cx+r-16,cy+r-16),"#a95b37")
    # rim highlight
    d.arc(B((cx-r+5,cy-r+5,cx+r-5,cy+r-5)),200,320,fill=(245,190,140,170),width=X(3))
    line([(cx+r-5,cy),(cx+r+22,cy+2)],"#a45b36",7)
# small hanging copper lid
ellipse((1036,240,1084,288),"#ba6d44",outline="#7c3c24",width=2)
ellipse((1044,248,1076,280),"#d58b59",outline="#8f472a",width=1.5)
line([(1060,240),(1060,196)],"#7d6a52",2)

# ---------- CABINETS & COUNTER ----------
# floor first visible below
# base floor
grad_rect((0,1080,1600,1200), "#9d5f45", "#c4825d")
# floor perspective checker
vp = (800,682)
ys = [1080,1104,1136,1175,1210]
xs_bottom = [i*160 for i in range(-1,12)]
# radial seams (clipped to the floor so they do not cross the room)
for xb in xs_bottom:
    t = (1080-vp[1])/(1200-vp[1])
    xt = vp[0] + (xb-vp[0])*t
    line([(xt,1080),(xb,1200)],"#e0b590",2)
for y in ys:
    line([(0,y),(1600,y)],"#e0b590",2)
# cell shading
for i in range(len(xs_bottom)-1):
    for j in range(len(ys)-1):
        if (i+j)%2==0:
            xb0,xb1 = xs_bottom[i],xs_bottom[i+1]
            # compute x at y levels along rays
            def rayx(xb,y):
                t = (y-vp[1])/(1200-vp[1])
                return vp[0] + (xb-vp[0])*t
            y0,y1 = ys[j],ys[j+1]
            pts_ = [(rayx(xb0,y0),y0),(rayx(xb1,y0),y0),(rayx(xb1,y1),y1),(rayx(xb0,y1),y1)]
            poly(pts_,(186,117,84,150))
# floor ambient
radial_rect_glow((0,1080,1600,1200),"#7d3f2e",35,60)
# large sun patch on floor later

# cabinetry shadow on floor
soft_shadow((55,1060,1545,1110),offset=(0,12),blur=22,color=(60,31,20),alpha=110)
# cabinet body
grad_rect((58,842,1544,1088), "#8fa084", "#64775f", radius=4, outline="#4e5f4a", width=2)
# top rail / drawer row
rectangle((58,842,1544,858),"#a5b498")
grad_rect((58,858,1544,918), "#8fa084", "#788b70", outline="#5b6d56", width=1)
# toe kick
rectangle((58,1058,1544,1088),"#4e5e49")
rectangle((58,1058,1544,1066),"#3e4d3b")
# vertical cabinet divisions & doors
def cabinet_door(x0,y0,x1,y1, handle_side="right", pull="knob"):
    grad_rect((x0,y0,x1,y1), "#8fa286", "#6f8269", radius=3, outline="#586b54", width=2)
    # recessed panel
    m = 9
    grad_rect((x0+m,y0+m,x1-m,y1-m), "#7f9377", "#6a7d63", radius=2, outline="#596d56", width=1.5)
    rrect((x0+m+4,y0+m+4,x1-m-4,y1-m-4),2,None,outline="#a3b399",width=1)
    # subtle highlight edge
    line([(x0+3,y0+3),(x1-3,y0+3)],(255,255,255,35),2)
    line([(x0+3,y0+3),(x0+3,y1-3)],(20,30,20,35),2)
    # handle
    if pull=="knob":
        hx = x1-18 if handle_side=="right" else x0+18
        hy = (y0+y1)/2
        ellipse((hx-5,hy-5,hx+5,hy+5),"#d4aa5e",outline="#8c642c",width=1)
        ellipse((hx-2.5,hy-3,hx+1,hy),"#f4de9b")
    else:
        hx = x1-30 if handle_side=="right" else x0+14
        hy = (y0+y1)/2
        rrect((hx,hy-3,hx+16,hy+3),3,"#d0a558",outline="#8d652d",width=1)
        line([(hx+3,hy-1),(hx+13,hy-1)],(255,240,180,180),1)

# left cabinets
for x0,x1 in [(72,262),(270,458)]:
    grad_rect((x0,862,x1-8,914), "#93a58a", "#7b8e76", radius=2, outline="#5b6d56", width=1.5)
    rrect((x0+19,876,x1-27,901),2,None,outline="#aab99f",width=1)
    ellipse((x1-28,884,(x1-28)+9,893),"#d4aa5e",outline="#8c642c",width=1)
    cabinet_door(x0,922,x1-8,1052,"right")
# under sink cabinet
cabinet_door(474,958,650,1052,"right")
cabinet_door(658,958,834,1052,"left")
# right cabinets
for x0,x1 in [(850,1018),(1026,1188)]:
    grad_rect((x0,862,x1-8,914), "#93a58a", "#7b8e76", radius=2, outline="#5b6d56", width=1.5)
    rrect((x0+19,876,x1-27,901),2,None,outline="#aab99f",width=1)
    ellipse((x1-28,884,(x1-28)+9,893),"#d4aa5e",outline="#8c642c",width=1)
    cabinet_door(x0,922,x1-8,1052,"right")
# thin shadow under drawer rail
line([(62,917),(1540,917)],"#4e604b",3)

# counter top (butcher block)
soft_shadow((40,790,1560,855),offset=(0,12),blur=12,color=(58,35,20),alpha=100,radius=4)
grad_rect((42,794,1558,832), "#d7a16b", "#b97948", radius=3, outline="#8b552f", width=2)
# top sheen
rrect((50,796,1550,805),3,"#eec18a")
# front edge grain
grad_rect((42,832,1558,852), "#b47745", "#8f5933", radius=1, outline="#784628", width=1.5)
for i in range(26):
    x=random.uniform(55,1540)
    line([(x,835),(x+random.uniform(-7,7),849)],random.choice(["#a5683c","#c28853","#9b6038"]),1)
# end grain marks
for x in range(58,1550,44):
    line([(x,833),(x,851)],(70,42,24,55),1)
# counter reflection from window
radial_rect_glow((430,792,980,835),"#fff4d9",110,25)

# farmhouse sink
# apron shadow
soft_shadow((480,806,826,958),offset=(0,10),blur=12,color=(55,35,22),alpha=85,radius=12)
# body
grad_rect((482,810,824,952), "#f6efe0", "#d8c8b2", radius=13, outline="#b7a48e", width=2)
# side shading
rrect((490,820,505,944),7,"#e7dac7")
rrect((800,820,816,944),7,"#cbb8a2")
# front curve lines
for x in (540,590,640,690,740,790):
    line([(x,828),(x,927)],(205,188,165,45),1)
# apron panel recess
rrect((510,846,796,932),8,None,outline="#cdbba5",width=2)
rrect((516,852,790,926),6,None,outline=(255,255,255,95),width=1.5)
# sink top rim
grad_rect((476,792,830,818), "#fbf6ea", "#e9ddcb", radius=12, outline="#b8a48c", width=2)
# basin opening
ellipse((500,796,806,820),"#c9c7bd",outline="#9f9b90",width=2)
grad_rect((504,798,802,817), "#a8aaa3", "#d4d1c7", radius=8)
# inner wall hint
d.arc(B((502,797,804,830)),0,180,fill=(255,255,255,120),width=X(3))
# drain
ellipse((642,807,660,813),"#777d79",outline="#5e6460",width=1)

# faucet
soft_shadow((626,648,728,792),offset=(0,9),blur=7,color=(60,40,20),alpha=70)
# base plate
ellipse((630,786,674,803),"#dfcdb4",outline="#b29e86",width=1.5)
ellipse((637,789,667,798),"#c6b096")
# column
line([(652,790),(652,678)],(151,105,51,255),12)
line([(650,790),(650,678)],(208,158,89,255),6)
line([(646,780),(646,686)],(245,204,137,160),2)
# arc
d.arc(B((652,646,738,734)),180,360,fill=(145,99,47,255),width=X(13))
d.arc(B((652,646,738,734)),180,360,fill=(201,151,83,255),width=X(8))
d.arc(B((655,650,731,728)),190,330,fill=(247,210,149,140),width=X(2))
# spout down
line([(730,689),(730,735)],(145,99,47,255),12)
line([(730,689),(730,735)],(201,151,83,255),7)
# tip
ellipse((722,731,738,745),"#b37b3b",outline="#7c5429",width=1.5)
ellipse((725,733,735,741),"#8a5c2b")
# handles, mounted on the sink rim
for hx in (604,700):
    ellipse((hx-13,784,hx+13,800),"#d9c6ad",outline="#b19c82",width=1.5)
    line([(hx,772),(hx,789)],"#9d6f35",6)
    ellipse((hx-11,758,hx+11,778),"#c7954d",outline="#8d5e2b",width=1.5)
    ellipse((hx-7,761,hx-2,767),"#efd391")
    ellipse((hx-12,756,hx+12,775),None,outline=(250,216,150,110),width=1.5)

# ---------- RANGE ----------
RX0,RX1 = 1206,1524
soft_shadow((1204,795,1528,1090),offset=(0,14),blur=20,color=(52,32,20),alpha=110,radius=5)
# backguard
grad_rect((1208,748,1522,806), "#f3e8d5", "#d9c8b1", radius=4, outline="#ad9981", width=2)
rrect((1226,764,1504,782),4,None,outline="#c0ad94",width=2)
line([(1226,772),(1504,772)],"#b29e85",2)
# top rail / stovetop
grad_rect((1206,796,1524,844), "#443f38", "#292824", radius=4, outline="#1e1d1a", width=2)
# cooktop surface
grad_rect((1220,802,1510,838), "#4b4740", "#35332e", radius=3)
# burners
for (bx,by,rx,ry) in [(1266,820,34,13),(1338,820,34,13),(1420,820,30,12),(1478,820,24,10)]:
    ellipse((bx-rx,by-ry,bx+rx,by+ry),"#211f1d",outline="#7c7469",width=2)
    ellipse((bx-rx*0.65,by-ry*0.55,bx+rx*0.65,by+ry*0.55),None,outline="#5b554d",width=2)
    for a in range(0,360,45):
        x1=bx+math.cos(math.radians(a))*rx*0.36; y1=by+math.sin(math.radians(a))*ry*0.38
        x2=bx+math.cos(math.radians(a))*rx*0.62; y2=by+math.sin(math.radians(a))*ry*0.64
        line([(x1,y1),(x2,y2)],"#5c554b",2)
# range body
grad_rect((1212,842,1520,1084), "#f0e3cf", "#cdbba3", radius=5, outline="#a99278", width=2)
# oven door
soft_shadow((1234,888,1498,1034),offset=(0,5),blur=7,color=(80,60,40),alpha=55,radius=5)
grad_rect((1232,884,1500,1034), "#f7eddc", "#dccbb4", radius=7, outline="#b09a80", width=2)
rrect((1248,900,1484,1018),6,"#b4aa9b",outline="#8e8375",width=1)
grad_rect((1256,908,1476,1010), "#322f2b", "#5d554c", radius=4)
# window reflection
poly([(1260,1008),(1340,910),(1382,910),(1302,1008)],(255,244,214,25))
# handle
rrect((1252,870,1480,882),5,"#c39a55",outline="#88602d",width=1.5)
rrect((1260,872,1472,877),3,"#e6c47f")
# knobs
for kx in (1248,1284,1370,1448,1484):
    ellipse((kx-8,854,kx+8,868),"#b28a4d",outline="#79542a",width=1.5)
    ellipse((kx-5,856,kx+2,862),"#e9cb8b")
# lower drawer
rrect((1232,1042,1500,1072),4,None,outline="#b09a80",width=1.5)
rrect((1340,1048,1392,1056),3,"#b28a4d",outline="#79542a",width=1)
# side shading
rectangle((1212,842,1222,1084),(255,255,255,45))
rectangle((1510,842,1520,1084),(80,60,40,40))
# enamel speckles
for i in range(90):
    x=random.uniform(1220,1510); y=random.uniform(846,1080)
    d.point((X(x),X(y)), fill=random.choice([(110,90,70,35),(255,255,255,38)]))
# towel on handle
soft_shadow((1284,882,1366,974),offset=(0,5),blur=6,color=(80,55,35),alpha=50)
poly([(1290,884),(1360,884),(1352,970),(1298,970)],"#e9e2d2",outline="#b9ac98",width=1.5)
for i in range(4):
    line([(1294,898+i*17),(1357,898+i*17)],"#b56f5e" if i%2 else "#8fa39a",3)
# towel folds
line([(1322,886),(1316,968)],(180,165,145,90),2)

# ---------- KETTLE & POT ON RANGE ----------
# kettle shadow
soft_ellipse_shadow((1254,812,1372,836),blur=5,alpha=100)
# body
ellipse((1260,690,1370,822),"#b9643d",outline="#71381f",width=3)
radial_glow(1306,742,44,30,"#f1a56e",55,12)
# belly shading
d.arc(B((1266,698,1364,818)),200,340,fill=(240,155,104,135),width=X(5))
d.arc(B((1264,694,1366,820)),20,140,fill=(95,48,27,90),width=X(8))
# lid
ellipse((1280,678,1350,706),"#c8794e",outline="#71381f",width=2.5)
ellipse((1290,682,1340,698),"#d9905f")
ellipse((1306,670,1324,684),"#8d5c33",outline="#633b21",width=1.5)
# spout
poly([(1268,724),(1232,700),(1238,730),(1266,748)],"#b9643d",outline="#71381f",width=2)
poly([(1262,728),(1240,710),(1243,724),(1261,738)],"#d48255")
# handle
d.arc(B((1268,646,1364,760)),190,350,fill=(67,63,53,255),width=X(7))
d.arc(B((1268,646,1364,760)),195,345,fill=(121,109,89,255),width=X(2))
# highlight
d.arc(B((1274,704,1354,812)),200,330,fill=(255,220,170,100),width=X(3))
# small copper pot
soft_ellipse_shadow((1400,802,1488,826),blur=4,alpha=85)
rrect((1406,744,1482,810),8,"#b76b45",outline="#713b22",width=2)
ellipse((1402,736,1486,762),"#ca8051",outline="#713b22",width=2)
ellipse((1410,740,1478,754),"#a95b38")
rrect((1478,758,1508,770),5,"#8c512f",outline="#64371f",width=1.5)
rrect((1400,802,1488,812),5,"#7a4528")
# steam placeholder drawn later

# ---------- SINK-SIDE ITEMS ----------
# lemon bowl
soft_ellipse_shadow((290,792,438,830),blur=9,alpha=70)
ellipse((296,772,430,820),"#e7ddca",outline="#b7a68c",width=2)
ellipse((306,776,420,806),"#d7c9b1")
# lemons
for (lx,ly,r) in [(330,779,19),(362,772,21),(394,780,18)]:
    ellipse((lx-r,ly-r*0.8,lx+r,ly+r*0.8),"#e7bc46",outline="#b58a27",width=1.5)
    d.arc(B((lx-r+4,ly-r*0.8+3,lx+r-4,ly+r*0.8-3)),200,340,fill=(255,235,140,160),width=X(2))
    ellipse((lx+r-3,ly-2,lx+r+2,ly+3),"#b08a2e")
# bowl rim highlight
d.arc(B((298,772,428,820)),200,340,fill=(255,252,235,180),width=X(3))

# board with bread
soft_shadow((108,748,290,826),offset=(0,8),blur=8,color=(70,42,25),alpha=65)
# board leans slightly; drawn as rounded rectangle
rrect((110,692,284,818),9,"#b77b47",outline="#7d4c2a",width=2)
rrect((120,702,274,808),6,"#c98d56")
line([(129,716),(260,716)],(92,55,31,70),2)
line([(124,744),(267,744)],(92,55,31,45),2)
line([(127,786),(263,786)],(92,55,31,45),2)
# handle hole
ellipse((184,700,210,724),"#9a6035",outline="#704427",width=1)
ellipse((188,704,206,720),"#7d4b29")
# loaf
soft_ellipse_shadow((142,764,258,824),blur=6,alpha=75)
ellipse((140,724,262,810),"#c38345",outline="#8c552b",width=2)
ellipse((148,730,254,795),"#d99a5b")
# score marks
for i in range(3):
    d.arc(B((160+i*28,736,206+i*28,778)),200,330,fill=(137,79,40,210),width=X(3))
# flour dusting
for i in range(20):
    x=random.uniform(155,248); y=random.uniform(738,790)
    d.ellipse((X(x),X(y),X(x+2),X(y+2)),fill=(255,239,210,70))
# small pat of butter on bread? maybe
rrect((188,744,216,758),3,"#f1ca62",outline="#c49a34",width=1)

# jam jar left of board
soft_ellipse_shadow((82,760,148,824),blur=6,alpha=65)
rrect((86,730,144,818),6,"#dbcdb8",outline="#a89782",width=1.5)
rrect((92,748,138,810),4,"#a83e36")
rrect((90,742,140,754),4,"#8a2f2b")
rrect((86,722,144,742),5,"#e7dcc9",outline="#ad9c85",width=1.5)
# cloth cover and tie
rrect((84,720,146,735),4,"#e6e1d1",outline="#b7ab97",width=1)
line([(86,736),(144,736)],"#8f6549",3)
# check pattern on cloth
for x in range(90,145,14):
    line([(x,720),(x,735)],"#b77e6b",1)
# label
rrect((98,768,132,798),3,"#f1e7d4",outline="#c9b89e",width=1)
line([(104,778),(126,778)],"#9a7c5e",2)
line([(104,787),(121,787)],"#b39a7f",1)

# mug right of sink
soft_ellipse_shadow((886,794,972,828),blur=8,alpha=80)
# saucer
ellipse((880,796,978,822),"#e7dcc8",outline="#b6a58e",width=1.5)
grad_rect((894,734,958,804), "#f3e9d7", "#d7c7b1", radius=8, outline="#ab9983", width=1.5)
# rim
ellipse((894,728,958,748),"#f8f1e4",outline="#ab9983",width=1.5)
ellipse((900,732,952,744),"#6b4735")
# coffee surface
ellipse((903,733,949,743),"#75503c")
ellipse((908,734,930,739),"#9a7055")
# handle
d.arc(B((950,744,990,790)),270,90,fill=(171,153,131,255),width=X(6))
d.arc(B((950,744,990,790)),275,85,fill=(236,225,207,255),width=X(2))
# little heart on mug? no, keep simple stripe
line([(900,772),(952,772)],"#8ea090",3)
line([(900,780),(952,780)],"#b17662",2)
# steam later

# utensil crock
soft_ellipse_shadow((1020,790,1108,826),blur=8,alpha=70)
rrect((1024,738,1104,818),8,"#d7cdb9",outline="#9f927e",width=2)
ellipse((1024,730,1104,754),"#e8dfcd",outline="#9f927e",width=2)
ellipse((1032,734,1096,748),"#a9a08e")
for (sx,sy,tx,ty,c) in [(1042,738,1028,672,"#a87945"),(1062,738,1058,658,"#8e8f77"),(1084,738,1102,676,"#b68651"),(1074,738,1088,690,"#7c8e6a")]:
    line([(sx,sy),(tx,ty)],c,4)
    ellipse((tx-8,ty-6,tx+2,ty+3),c)
# herb pot on counter
soft_ellipse_shadow((1110,790,1182,826),blur=8,alpha=65)
rrect((1128,756,1170,816),6,"#c07b57",outline="#8f573c",width=1.5)
rrect((1124,748,1174,762),4,"#d28d66",outline="#8f573c",width=1)
for (sx,sy,tx,ty) in [(1148,752,1132,720),(1150,752,1148,704),(1150,752,1164,716),(1146,752,1178,736)]:
    line([(sx,sy),(tx,ty)],"#4e6a44",3)
    ellipse((tx-11,ty-8,tx+11,ty+8),"#6c8b59")
    ellipse((tx-5,ty-5,tx+3,ty+2),"#95ad78")

# ---------- HERBS ON WINDOW SILL ----------
def sill_pot(x, base_y, w, h, pot_col, leaf_col):
    soft_ellipse_shadow((x-w/2,base_y-6,x+w/2,base_y+6),blur=5,alpha=60)
    # pot
    poly([(x-w/2,base_y-h),(x+w/2,base_y-h),(x+w/2-5,base_y),(x-w/2+5,base_y)],pot_col,outline="#8f5138",width=1.5)
    rrect((x-w/2-3,base_y-h-3,x+w/2+3,base_y-h+7),3,pot_col,outline="#8f5138",width=1.2)
    # leaves
    for i in range(9):
        a = random.uniform(math.pi*1.06, math.pi*1.94)
        r = random.uniform(15, n if False else 20)
        tx = x + math.cos(a)*random.uniform(8,28)
        ty = base_y-h-6 + math.sin(a)*random.uniform(12,34)
        line([(x,base_y-h-2),(tx,ty)],leaf_col,2)
        ellipse((tx-5,ty-3,tx+5,ty+3),leaf_col)
        ellipse((tx-2,ty-2,tx+1,ty+1),"#9cb47c")

sill_pot(466,591,34,31,"#b96f4d","#557549")
sill_pot(517,591,28,26,"#c98662","#607f4f")
# little jar between
rrect((542,560,562,590),4,"#e7ddc9",outline="#b4a58f",width=1)
rrect((540,553,564,563),3,"#c6a16f",outline="#947447",width=1)

# ---------- SLEEPING GINGER CAT ON SILL ----------
cat_y = 586
# tail curling behind
brush_line([(828,584),(856,586),(870,574),(870,558),(860,550)], (98,54,32,235), 16, 1)
brush_line([(828,584),(856,586),(870,574),(870,558),(860,550)], (196,121,66,255), 12, 0.7)
# body
ellipse((780,534,866,596),"#d18a51",outline="#9b5a32",width=2)
# haunch shading
ellipse((826,548,866,594),"#bd7743")
# chest/head
ellipse((742,540,808,596),"#d99258",outline="#9b5a32",width=2)
# head top shading
radial_glow(780,554,24,13,"#eaaa70",80,8)
# ears
for pts_ in [[(750,552),(754,527),(776,546)],[(792,544),(810,528),(810,555)]]:
    poly(pts_,"#cf8751",outline="#96552f",width=1.5)
    inner = [(pts_[0][0]+5,pts_[0][1]-7),(pts_[1][0]+1,pts_[1][1]+6),(pts_[2][0]-5,pts_[2][1]-2)]
    poly(inner,"#dda092")
# stripes on body
for (sx,sy,tx,ty) in [(804,544,812,564),(818,541,826,561),(832,544,840,562),(846,548,852,566)]:
    d.arc(B((min(sx,tx)-3,sy,max(sx,tx)+3,ty+6)),20,160,fill=(150,78,43,210),width=X(3))
# face markings
line([(762,549),(766,565)],"#ac6439",2)
line([(780,545),(780,560)],"#ac6439",2)
line([(792,550),(790,562)],"#ac6439",2)
# muzzle
ellipse((758,568,790,588),"#f0d3b0")
ellipse((774,570,796,590),"#f2d9b8")
# closed eyes
d.arc(B((756,561,774,573)),10,170,fill=(79,51,35,255),width=X(2))
d.arc(B((782,561,800,573)),10,170,fill=(79,51,35,255),width=X(2))
# nose
poly([(772,574),(780,574),(776,580)],"#b56e5e")
# mouth
d.arc(B((771,577,777,585)),0,180,fill=(119,72,55,220),width=X(1.2))
d.arc(B((777,577,783,585)),0,180,fill=(119,72,55,220),width=X(1.2))
# whiskers
for yy in (577,580,583):
    line([(762,yy),(740,yy+random.uniform(-2,2))],(255,244,225,150),1)
    line([(790,yy),(814,yy+random.uniform(-2,2))],(255,244,225,150),1)
# front paws
ellipse((750,584,786,596),"#ead0ad",outline="#b7845d",width=1)
ellipse((788,586,820,597),"#e7cba6",outline="#b7845d",width=1)
line([(758,589),(764,589)],"#c69673",1.5)
line([(796,590),(802,590)],"#c69673",1.5)
# tail tip cream
ellipse((854,546,868,562),"#e9cba3")
# whisker shine
brush_line([(748,548),(762,543)],(255,234,205,100),2,0.6)

# ---------- STEAM ----------
def steam_path(points, color=(255,255,248), alpha=90, width=5, blur=4):
    layer = Image.new("RGBA", img.size, (0,0,0,0))
    ld = ImageDraw.Draw(layer)
    ld.line(P(points), fill=(*col(color),alpha), width=X(width), joint="curve")
    for p in (points[0], points[-1]):
        r=X(width/2)
        ld.ellipse((X(p[0])-r,X(p[1])-r,X(p[0])+r,X(p[1])+r),fill=(*col(color),alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(X(blur)))
    img.paste(Image.alpha_composite(img.convert("RGBA"),layer).convert("RGB"))
    d._image = img

steam_path([(925,720),(916,700),(928,682),(914,664),(920,646)],(255,255,250),45,5,5)
steam_path([(936,716),(941,694),(930,674),(940,652)],(255,255,250),38,4,5)
steam_path([(1315,663),(1302,640),(1318,620),(1304,594),(1312,568)],(255,255,248),55,7,7)
steam_path([(1332,663),(1342,636),(1328,612),(1340,586)],(255,255,248),42,5,7)
# faint heat above range
radial_glow(1330,650,84,42,"#fff9e7",22,22)

# ---------- WARM MORNING LIGHT ----------
# big bloom from window
radial_glow(650,360,470,360,"#ffe3a8",26,80)
radial_glow(700,410,210,190,"#fff0c6",34,45)
# Soft, broad morning beams -- no hard fan lines
ray_layer = Image.new("RGBA", img.size, (0,0,0,0))
rd = ImageDraw.Draw(ray_layer)
rays = [
    [(430,120),(590,120),(1130,1090),(865,1110)],
    [(650,120),(820,120),(1460,1030),(1160,1070)],
]
for i,pts_ in enumerate(rays):
    rd.polygon(P(pts_),(255,232,176, 10 if i else 13))
ray_layer = ray_layer.filter(ImageFilter.GaussianBlur(X(34)))
img.paste(Image.alpha_composite(img.convert("RGBA"),ray_layer).convert("RGB"))
d._image = img
# haze in the room
radial_glow(820,630,540,350,"#ffe2a9",16,90)
# sun patch on counter
sun_layer = Image.new("RGBA", img.size,(0,0,0,0))
sd = ImageDraw.Draw(sun_layer)
sd.polygon(P([(760,800),(1008,800),(1120,848),(818,852)]),(255,226,160,62))
sd.polygon(P([(1030,802),(1170,802),(1260,850),(1080,852)]),(255,228,164,42))
sun_layer = sun_layer.filter(ImageFilter.GaussianBlur(X(10)))
img.paste(Image.alpha_composite(img.convert("RGBA"),sun_layer).convert("RGB"))
d._image=img
# sun patch on floor
sun_layer = Image.new("RGBA", img.size,(0,0,0,0))
sd = ImageDraw.Draw(sun_layer)
sd.polygon(P([(690,1084),(1030,1084),(1240,1200),(820,1200)]),(255,219,152,68))
sd.polygon(P([(1010,1084),(1170,1084),(1360,1200),(1120,1200)]),(255,220,154,38))
sun_layer = sun_layer.filter(ImageFilter.GaussianBlur(X(18)))
img.paste(Image.alpha_composite(img.convert("RGBA"),sun_layer).convert("RGB"))
d._image=img

# ---------- DUST MOTES ----------
for i in range(110):
    t = random.random()
    # distribute along diagonal beam
    y = random.uniform(380,1150)
    x = 520 + (y-380)*0.86 + random.uniform(-180,180)
    if not (80<x<1520 and 320<y<1180):
        continue
    r = random.uniform(0.6,2.8)
    a = random.randint(16,85)
    if r>2.0:
        radial_glow(x,y,r*2.8,r*2.8,"#fff2c9",a,2.5)
    else:
        d.ellipse(B((x-r,y-r,x+r,y+r)),(255,240,194,a))
# a few bright sparkles
for (x,y) in [(892,592),(1040,720),(700,470),(1210,930),(960,842)]:
    d.line(P([(x-5,y),(x+5,y)]),fill=(255,246,210,110),width=X(1))
    d.line(P([(x,y-5),(x,y+5)]),fill=(255,246,210,110),width=X(1))
    radial_glow(x,y,9,9,"#fff0c0",38,4)

# ---------- EXTRA COZY DETAILS ----------
# flour dust / crumbs on counter
for i in range(70):
    x=random.uniform(80,1180); y=random.uniform(800,824)
    d.ellipse(B((x,y,x+random.uniform(0.5,1.8),y+random.uniform(0.5,1.5))),(247,233,207,random.randint(30,80)))

# folds in linen towel on range
line([(1300,884),(1298,966)],(255,255,255,50),2)
line([(1346,886),(1342,968)],(110,95,78,55),2)

# shadow under cat on sill
soft_ellipse_shadow((742,585,872,601),blur=5,alpha=55)

# subtle backlighting on cat
brush_line([(756,543),(776,535),(798,541)],(255,224,171,90),3,1.2)
brush_line([(850,578),(866,570),(870,556)],(255,218,161,70),3,1.5)

# tiny heart in steam? no.

# ---------- FINAL COLOR / TEXTURE ----------
# painterly grain at reduced resolution
small = img.resize((W, H), Image.LANCZOS)
small = ImageEnhance.Color(small).enhance(1.04)
small = ImageEnhance.Contrast(small).enhance(1.025)
grain = Image.effect_noise((W, H), 19).convert("L")
grain_rgb = Image.merge("RGB",(grain,grain,grain))
painted = ImageChops.overlay(small, grain_rgb)
small = Image.blend(small, painted, 0.075)

# fine canvas grain
grain2 = Image.effect_noise((W//2, H//2), 8).convert("L").resize((W,H),Image.BILINEAR)
grain2_rgb = Image.merge("RGB",(grain2,grain2,grain2))
small = Image.blend(small, ImageChops.overlay(small, grain2_rgb), 0.045)

# very subtle paper flecks
fd = ImageDraw.Draw(small, "RGBA")
for i in range(2600):
    x=random.uniform(0,W); y=random.uniform(0,H)
    v=random.choice([(255,248,230,random.randint(4,13)),(85,63,44,random.randint(3,10))])
    fd.point((x,y),fill=v)

# vignette
vw,vh = W//4, H//4
vmask = Image.new("L",(vw,vh),0)
vd = ImageDraw.Draw(vmask)
vd.ellipse((-vw*0.12,-vh*0.10,vw*1.12,vh*1.10),fill=255)
vmask = vmask.filter(ImageFilter.GaussianBlur(26)).resize((W,H),Image.BILINEAR)
# invert selection for corners
inv = vmask.point(lambda v: max(0, int((255-v)*0.40)))
small.paste((72,47,31), (0,0), inv)

# final gentle bloom
bloom = small.filter(ImageFilter.GaussianBlur(2.0))
small = Image.blend(small, ImageChops.screen(small,bloom), 0.10)

# save
out = "/tmp/vellery-la2gxpdr/work/cozy_kitchen_morning.png"
small.save(out, "PNG", optimize=True)
print("saved", out, small.size)
