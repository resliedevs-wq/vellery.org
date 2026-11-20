from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageChops
import math, random

random.seed(11)
S = 2
W, H = 1600, 1200
CW, CH = W*S, H*S

def P(x, y): return (x*S, y*S)
def B(x0,y0,x1,y1): return (x0*S, y0*S, x1*S, y1*S)
def V(v): return int(round(v*S))

def rgba(hexstr, a=255):
    if isinstance(hexstr, tuple):
        return (hexstr[0], hexstr[1], hexstr[2], a)
    hexstr = hexstr.lstrip('#')
    return (int(hexstr[0:2],16), int(hexstr[2:4],16), int(hexstr[4:6],16), a)

def mix(c1, c2, t):
    return tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3))

def grad_rect(im, box, top, bottom, radius=0):
    x0,y0,x1,y1 = [int(v) for v in (box[0]*S, box[1]*S, box[2]*S, box[3]*S)]
    w,h = max(1,x1-x0), max(1,y1-y0)
    g = Image.linear_gradient('L').resize((w,h), Image.Resampling.BILINEAR)
    col = ImageOps.colorize(g, black=top, white=bottom).convert('RGBA')
    mask = Image.new('L', (w,h), 0)
    md = ImageDraw.Draw(mask)
    if radius:
        md.rounded_rectangle((0,0,w-1,h-1), radius=radius*S, fill=255)
    else:
        md.rectangle((0,0,w,h), fill=255)
    im.alpha_composite(col, (x0,y0)) if False else im.paste(col, (x0,y0), mask)

def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(B(*box), radius=V(r), fill=fill, outline=outline, width=V(width))

def ell(d, box, fill=None, outline=None, width=1):
    d.ellipse(B(*box), fill=fill, outline=outline, width=V(max(1,width)))

def rect(d, box, fill=None, outline=None, width=1):
    d.rectangle(B(*box), fill=fill, outline=outline, width=V(max(1,width)))

def poly(d, pts, fill=None, outline=None, width=1):
    d.polygon([P(x,y) for x,y in pts], fill=fill, outline=outline, width=V(max(1,width)) if outline else 1)

def line(d, pts, fill, width=1, joint='curve'):
    d.line([P(x,y) for x,y in pts], fill=fill, width=V(width), joint=joint)

def soft_shadow(im, box, blur=10, alpha=60, ellipse=True):
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    ld = ImageDraw.Draw(layer)
    if ellipse:
        ld.ellipse(B(*box), fill=(52,36,24,alpha))
    else:
        ld.rounded_rectangle(B(*box), radius=V(8), fill=(52,36,24,alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(V(blur)))
    im.alpha_composite(layer)

def shadow_poly(im, pts, blur=8, alpha=55):
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    ld = ImageDraw.Draw(layer)
    ld.polygon([P(x,y) for x,y in pts], fill=(52,36,24,alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(V(blur)))
    im.alpha_composite(layer)

def bez(p0,p1,p2,p3,n=32):
    out=[]
    for i in range(n+1):
        t=i/n; u=1-t
        x=u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0]
        y=u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]
        out.append((x,y))
    return out

def glow(im, cx, cy, rx, ry, color, alpha=90, blur=60):
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    ld = ImageDraw.Draw(layer)
    for i in range(10,0,-1):
        a = int(alpha*(1-i/11)**1.7)
        ld.ellipse((V(cx-rx*i/10), V(cy-ry*i/10), V(cx+rx*i/10), V(cy+ry*i/10)), fill=(*color, a))
    layer = layer.filter(ImageFilter.GaussianBlur(V(blur)))
    im.alpha_composite(layer)

def texture(im, sigma=14, alpha=13):
    noise = Image.effect_noise((CW,CH), sigma).convert('RGB')
    n = noise.convert('RGBA')
    n.putalpha(alpha)
    im.alpha_composite(n)

def leaf(d, x, y, dx, dy, w, fill, ang=0):
    # simple leaf as polygon around a spine
    cx, cy = x+dx, y+dy
    ux, uy = -dy, dx
    ln = math.hypot(ux,uy) or 1
    ux, uy = ux/ln*w, uy/ln*w
    pts = [(x,y),(x+dx*.45+ux, y+dy*.45+uy),(cx,cy),(x+dx*.45-ux, y+dy*.45-uy)]
    poly(d, pts, fill=fill)

im = Image.new('RGBA', (CW,CH), (0,0,0,0))
d = ImageDraw.Draw(im)

# ---------- wall ----------
grad_rect(im, (0,0,W,1090), rgba('#f6ead5'), rgba('#e6cfad'))
# broad morning warmth on wall
glow(im, 820, 360, 470, 390, (255,224,166), 85, 80)

# crown / ceiling shadow
grad_rect(im, (0,0,W,34), rgba('#8f6e50',75), rgba('#8f6e50',0))

# ---------- floor ----------
grad_rect(im, (0,1065,W,H), rgba('#bd895e'), rgba('#8d5c3d'))
# floor boards
for y in [1090,1118,1148,1180]:
    line(d, [(0,y),(1600,y+3)], rgba('#7a4b31',75), 2)
for x in [80, 250, 430, 610, 800, 990, 1180, 1370, 1550]:
    line(d, [(x,1068),(x-55,1200)], rgba('#6f422c',55), 2)
# long light on floor
poly(d, [(660,1070),(1290,1070),(1510,1200),(610,1200)], rgba('#f6c77f',48))
# baseboard
rect(d, (0,1040,1600,1072), rgba('#ead8ba'))
rect(d, (0,1040,1600,1048), rgba('#b99a73',70))
rect(d, (0,1064,1600,1072), rgba('#8f6b4d',45))

# braided rug
soft_shadow(im, (445,1100,1135,1210), 12, 50)
ell(d, (430,1080,1140,1215), fill=rgba('#8b4b42'))
ell(d, (455,1092,1115,1208), fill=rgba('#b86b56'))
ell(d, (480,1104,1090,1200), fill=rgba('#d8a06f'))
ell(d, (510,1116,1060,1193), fill=rgba('#8c5b58'))
for i in range(12):
    x = 485 + i*51
    line(d, bez((x,1105),(x+12,1130),(x-12,1165),(x+6,1200)), rgba('#7d4b45',80), 3)

# ---------- window ----------
# outer shadow
soft_shadow(im, (505,82,1094,615), 16, 80, ellipse=False)
# frame
rrect(d, (512,86,1088,608), 16, fill=rgba('#ead6b4'), outline=rgba('#b28e68'), width=3)
rrect(d, (526,100,1074,594), 10, fill=rgba('#8f6b4d'))
# recess shadow
rrect(d, (538,112,1062,582), 6, fill=rgba('#6b4f39'))
# glazing area
rrect(d, (548,118,1052,574), 2, fill=rgba('#f8dba6'))

# sky
grad_rect(im, (548,118,1052,574), rgba('#bcd8e2'), rgba('#ffe1ac'))
# sun glow outside
glow(im, 612, 198, 175, 155, (255,244,196), 95, 34)
ell(d, (588,174,612,198), fill=rgba('#fff9db',82))
# distant hills / trees
poly(d, [(548,420),(620,382),(710,410),(790,374),(900,402),(980,370),(1052,398),(1052,574),(548,574)], fill=rgba('#b7c2a0'))
poly(d, [(548,470),(610,430),(690,455),(760,420),(850,452),(940,424),(1052,458),(1052,574),(548,574)], fill=rgba('#8fa184'))
# tree clusters, soft
for cx,cy,r,col in [(610,398,42,'#7f9878'),(682,380,34,'#94a987'),(935,372,50,'#8da282'),(1008,405,45,'#7d9675')]:
    ell(d, (cx-r,cy-r,cx+r,cy+r), fill=rgba(col))
    ell(d, (cx-r*.7,cy-r*1.1,cx+r*.5,cy-r*.1), fill=rgba(mix(rgba(col)[:3],(255,239,190),.18)))
# little meadow
rect(d, (548,520,1052,574), fill=rgba('#c6c690'))
for i in range(90):
    x=random.uniform(552,1048); y=random.uniform(525,572)
    line(d, [(x,y),(x+random.uniform(-2,2),y-random.uniform(3,10))], rgba('#7c8c5d',random.randint(50,100)), 1)
# birds
for x,y,s in [(730,240,7),(760,225,5),(1000,260,6)]:
    d.arc((V(x-s),V(y-s),V(x),V(y)), 200, 340, fill=rgba('#6f6759',140), width=V(2))
    d.arc((V(x),V(y-s),V(x+s),V(y)), 200, 340, fill=rgba('#6f6759',140), width=V(2))

# glass reflection
poly(d, [(560,120),(606,120),(570,572),(548,572)], rgba('#ffffff',13))
poly(d, [(694,120),(710,120),(642,572),(622,572)], rgba('#ffffff',8))

# muntins
for x in [798]:
    rect(d, (x-5,112,x+5,582), rgba('#f2dfbd'))
    rect(d, (x-3,112,x-1,582), rgba('#fff4d9',180))
for y in [268,422]:
    rect(d, (538,y-5,1062,y+5), rgba('#f2dfbd'))
    rect(d, (538,y-4,1062,y-2), rgba('#fff4d9',180))
# frame inner highlight
rrect(d, (538,112,1062,582), 6, outline=rgba('#f7e8c9'), width=3)
# latch
rrect(d, (792,412,808,438), 5, fill=rgba('#c6984e'), outline=rgba('#8d642c'), width=2)
ell(d, (796,418,804,426), fill=rgba('#f4d896'))

# window sill
soft_shadow(im, (490,596,1110,638), 7, 70, ellipse=False)
rrect(d, (492,594,1108,622), 5, fill=rgba('#f0ddbc'), outline=rgba('#b68e64'), width=2)
rect(d, (498,600,1102,606), rgba('#fff5db',160))
rect(d, (500,618,1100,628), rgba('#a87c54'))

# ---------- curtains ----------
# brass rod
soft_shadow(im, (476,62,1124,80), 6, 65, ellipse=False)
rect(d, (482,66,1118,77), rgba('#b98235'))
rect(d, (482,68,1118,72), rgba('#e7bb6b'))
ell(d, (470,60,490,84), fill=rgba('#ba8438'))
ell(d, (1110,60,1130,84), fill=rgba('#ba8438'))
for cx in [490, 1120]:
    ell(d, (cx-6,64,cx+6,80), fill=rgba('#f0c571'))

def curtain(side):
    if side=='L':
        pts=[(494,84),(562,84),(570,142),(558,226),(568,320),(552,390),(568,470),(560,596),(542,604),(510,596),(502,500),(514,402),(500,332),(508,240),(496,150)]
        folds=[506,520,536]
        tie=(502,382,566,402)
    else:
        pts=[(1106,84),(1038,84),(1030,142),(1042,226),(1032,320),(1048,390),(1032,470),(1040,596),(1058,604),(1090,596),(1098,500),(1086,402),(1100,332),(1092,240),(1104,150)]
        folds=[1094,1080,1064]
        tie=(1034,382,1098,402)
    poly(d, pts, fill=rgba('#f6e5c6'))
    # soft inner shading
    if side=='L':
        poly(d, [(558,92),(570,142),(558,226),(568,320),(552,390),(568,470),(560,596),(550,598),(556,470),(544,390),(558,320),(548,226),(558,142)], fill=rgba('#d8b98e',44))
        for i,x in enumerate(folds):
            line(d, bez((x,96),(x+4,210),(x-5,400),(x+2,592)), rgba('#b9946a',34 if i%2 else 22), 2)
        line(d, [(502,150),(500,332),(510,420),(506,560)], rgba('#fff7e4',70), 2)
    else:
        poly(d, [(1042,92),(1030,142),(1042,226),(1032,320),(1048,390),(1032,470),(1040,596),(1050,598),(1044,470),(1056,390),(1042,320),(1052,226),(1042,142)], fill=rgba('#d8b98e',44))
        for i,x in enumerate([1094,1080,1064]):
            line(d, bez((x,96),(x-4,210),(x+5,400),(x-2,592)), rgba('#b9946a',34 if i%2 else 22), 2)
        line(d, [(1098,150),(1100,332),(1090,420),(1094,560)], rgba('#fff7e4',70), 2)
    # tieback
    rrect(d, tie, 8, fill=rgba('#d9bb90'), outline=rgba('#b08b60'), width=2)
    rect(d, (tie[0]+8,tie[1]+5,tie[2]-8,tie[1]+9), rgba('#f2d7ad',80))
curtain('L'); curtain('R')

# ---------- backsplash tiles ----------
rect(d, (0,626,1600,755), fill=rgba('#e6d4b7'))
# tile grid - soft zellige
for row in range(3):
    y0=628+row*42
    for col in range(0,22):
        x0=col*78 + (38 if row%2 else 0) - 40
        shade = random.choice(['#ecdbc0','#e7d4b6','#efdec4','#e3cfae'])
        rrect(d, (x0+1.5,y0+1.5,x0+76.5,y0+40.5), 3, fill=rgba(shade))
        # glaze highlight
        line(d, [(x0+10,y0+8),(x0+68,y0+7)], rgba('#fff6e2',38), 2)
        line(d, [(x0+8,y0+36),(x0+70,y0+36)], rgba('#b99b78',22), 2)
# grout shadow under counter
grad_rect(im, (0,736,1600,755), rgba('#8f6c4b',0), rgba('#8f6c4b',38))

# ---------- shelf / cabinet shadows on wall ----------
soft_shadow(im, (105,306,470,326), 8, 50, ellipse=False)
soft_shadow(im, (1130,306,1490,326), 8, 50, ellipse=False)

# ---------- shelves (left) ----------
# brackets
for x in [145, 430]:
    poly(d, [(x-16,322),(x+16,322),(x+9,382),(x-7,382)], fill=rgba('#9c713f'))
    ell(d, (x-5,318,x+5,328), fill=rgba('#d9ae6a'))
# boards
for y in [304, 478]:
    rect(d, (108,y,470,y+16), rgba('#a66d43'))
    rect(d, (112,y+2,466,y+8), rgba('#d19a63'))
    rect(d, (108,y+12,470,y+18), rgba('#7f4f31'))

# plates stack on left upper
for i,(yy,ww) in enumerate([(286,112),(278,103),(270,94)]):
    ell(d, (150+ (112-ww)/2, yy-10, 150+(112+ww)/2, yy+12), fill=rgba('#f8efdb'), outline=rgba('#b8a07b'), width=2)
    ell(d, (162+(112-ww)/2, yy-6, 150+(106+ww)/2, yy+8), outline=rgba('#89a4a8'), width=2)
# jar
rrect(d, (300,242,344,304), 8, fill=rgba('#e9e0cc'), outline=rgba('#b9a486'), width=2)
rect(d, (306,258,338,302), rgba('#d8e0d5'))
rect(d, (303,236,341,250), rgba('#b98c51'))
ell(d, (309,242,335,248), fill=rgba('#8f693c'))
# label
rect(d, (312,270,332,286), rgba('#f9f0d9'))
line(d, [(316,276),(328,276)], rgba('#9c7b57',140), 2)
# trailing plant upper right
soft_shadow(im, (346,288,424,306), 4, 40)
poly(d, [(350,304),(356,270),(410,270),(416,304)], fill=rgba('#c27a55'))
rect(d, (351,266,415,280), rgba('#d58d66'))
for i in range(9):
    a = -math.pi + i*math.pi/8
    x=382+math.cos(a)*random.uniform(18,40); y=268+math.sin(a)*random.uniform(15,35)
    leaf(d, 382,272, x-382, y-272, 10, rgba('#5c7a50'))
# trailing vine
vine = bez((406,280),(430,320),(390,350),(420,420))
line(d, vine, rgba('#4f6d47'), 3)
for i in range(9):
    x,y=vine[i*3 % len(vine)]
    leaf(d, x,y, random.uniform(-12,14), random.uniform(4,15), 7, rgba('#6d8b5b'))
# small blue jug lower left
soft_shadow(im, (132,460,212,482), 4, 35)
rrect(d, (150,424,202,478), 10, fill=rgba('#dfe9e6'), outline=rgba('#9bb3b1'), width=2)
rrect(d, (160,410,192,430), 6, fill=rgba('#c9d9d6'))
ell(d, (176,406,196,424), outline=rgba('#8ba4a2'), width=3)
# books
for i,(x0,col) in enumerate([(230,'#b96a53'),(247,'#7c8d7c'),(264,'#d0aa6e')]):
    rrect(d, (x0,432-i*2,x0+22,478), 2, fill=rgba(col), outline=rgba('#6e5138'), width=2)
    line(d, [(x0+4,444-i*2),(x0+18,444-i*2)], rgba('#f4e6ca',120), 2)
# lemon bowl
ell(d, (310,454,388,482), fill=rgba('#e5d3b0'), outline=rgba('#b08e66'), width=2)
for x,y in [(326,452),(346,448),(364,454)]:
    ell(d, (x-12,y-8,x+12,y+10), fill=rgba('#e9c455'))
    ell(d, (x-10,y-7,x-2,y-1), fill=rgba('#f7e079'))
# lower shelf edge
rect(d, (108,494,470,500), rgba('#7f4f31'))

# ---------- shelves (right) ----------
for x in [1165, 1450]:
    poly(d, [(x-16,322),(x+16,322),(x+9,382),(x-7,382)], fill=rgba('#9c713f'))
    ell(d, (x-5,318,x+5,328), fill=rgba('#d9ae6a'))
for y in [304, 478]:
    rect(d, (1130,y,1490,y+16), rgba('#a66d43'))
    rect(d, (1134,y+2,1486,y+8), rgba('#d19a63'))
    rect(d, (1130,y+12,1490,y+18), rgba('#7f4f31'))
# jug
rrect(d, (1160,250,1210,304), 9, fill=rgba('#f4ecd9'), outline=rgba('#b5a17f'), width=2)
rect(d, (1168,266,1202,300), rgba('#8ba5aa'))
ell(d, (1182,244,1198,260), fill=rgba('#f4ecd9'), outline=rgba('#b5a17f'), width=2)
# plates leaning
for i,col in enumerate(['#dfe9e5','#f3e6cf','#b7c8c8']):
    x0=1240+i*8
    ell(d, (x0,222,x0+55,302), fill=rgba(col), outline=rgba('#a98e6d'), width=2)
    ell(d, (x0+12,236,x0+43,288), outline=rgba('#7f9a9b'), width=2)
# small plant
soft_shadow(im, (1380,290,1460,306), 4, 35)
poly(d, [(1395,304),(1400,274),(1448,274),(1454,304)], fill=rgba('#cf8962'))
for i in range(12):
    a=-math.pi*0.9 + i*math.pi*0.15
    x=1424+math.cos(a)*random.uniform(16,34); y=272+math.sin(a)*random.uniform(24,52)
    leaf(d, 1424,274, x-1424, y-274, 9, rgba(random.choice(['#54744f','#6f8b5c','#7f9870'])))
# canisters lower right
for i,(x0,h) in enumerate([(1148,46),(1198,38),(1248,52)]):
    y=478-h
    rrect(d, (x0,y,x0+40,478), 5, fill=rgba('#e8ddc7'), outline=rgba('#b7a384'), width=2)
    rect(d, (x0+3,y+10,x0+37,478-3), rgba(['#c6d4c6','#dccaa9','#d5b59a'][i]))
    rect(d, (x0+1,y-6,x0+39,y+6), rgba('#a98351'))
    ell(d, (x0+8,y-4,x0+32,y+2), fill=rgba('#caa267'))
    rect(d, (x0+8,y+20,x0+32,y+32), rgba('#f7eedb'))
# stack bowls
for i,yy in enumerate([458,448,438]):
    ell(d, (1308,yy-12,1380,yy+12), fill=rgba(['#e7dcc4','#d7e2dd','#f4ead4'][i]), outline=rgba('#af9774'), width=2)
# mug rail under shelf
rect(d, (1160,506,1460,514), rgba('#a97739'))
rect(d, (1160,506,1460,509), rgba('#e0b467'))
for x in [1190,1270,1350,1430]:
    d.arc((V(x-5),V(512),V(x+5),V(524)), 0, 180, fill=rgba('#a97739'), width=V(2))
# mugs
for x,col in [(1190,'#c46f55'),(1270,'#e4d6bd'),(1350,'#8ca09b'),(1430,'#d9a45b')]:
    y=522
    rrect(d, (x-16,y,x+16,y+40), 7, fill=rgba(col), outline=rgba('#856344'), width=2)
    d.arc((V(x+13),V(y+8),V(x+30),V(y+30)), 270, 90, fill=rgba('#856344'), width=V(4))
    ell(d, (x-16,y-5,x+16,y+7), fill=rgba(mix(rgba(col)[:3],(255,255,255),.15)))
    line(d, [(x-10,y+8),(x-10,y+32)], rgba('#ffffff',45), 3)

# frame shadow under shelves
soft_shadow(im, (112,500,470,518), 8, 38, ellipse=False)
soft_shadow(im, (1130,500,1490,518), 8, 38, ellipse=False)

# ---------- hanging copper pans (right) ----------
# rail
soft_shadow(im, (1155,536,1470,548), 4, 45, ellipse=False)
rect(d, (1150,538,1472,546), rgba('#8f622b'))
rect(d, (1150,539,1472,542), rgba('#e5b766'))
for x in [1180,1260,1340,1420]:
    rect(d, (x-2,546,x+2,562), rgba('#8f622b'))
    d.arc((V(x-8),V(558),V(x+8),V(574)), 0, 180, fill=rgba('#b98338'), width=V(3))

def copper_pan(cx, top, w, h, col='#c47a3d'):
    # handle
    line(d, [(cx,top),(cx,top-30)], rgba('#b2803c'), 7)
    ell(d, (cx-7,top-40,cx+7,top-28), outline=rgba('#b2803c'), width=5)
    # body
    soft_shadow(im, (cx-w/2+4,top+h-6,cx+w/2+10,top+h+12), 6, 40)
    ell(d, (cx-w/2,top,cx+w/2,top+h), fill=rgba(col), outline=rgba('#8f5426'), width=3)
    ell(d, (cx-w/2+10,top+7,cx+w/2-10,top+h-8), fill=rgba(mix(rgba(col)[:3],(255,214,150),.45)))
    ell(d, (cx-w/2+22,top+8,cx+w/2-30,top+h-12), fill=rgba('#9d5b2b'))
    # shine
    d.arc((V(cx-w/2+16),V(top+14),V(cx+w/2-24),V(top+h-16)), 195, 320, fill=rgba('#f6d191',160), width=V(4))
    ell(d, (cx-w/4,top+9,cx+w/4,top+h-18), outline=rgba('#8f5426',130), width=2)

copper_pan(1195, 600, 86, 34)
copper_pan(1290, 620, 98, 38, '#b96c35')
copper_pan(1395, 588, 82, 33, '#cf8647')
# small copper kettle hanging
line(d, [(1450,546),(1450,574)], rgba('#b2803c'), 4)
rr = 28
ell(d, (1450-rr,570,1450+rr,570+44), fill=rgba('#b96c35'), outline=rgba('#8f5426'), width=3)
ell(d, (1450-rr+8,575,1450+rr-8,570+36), fill=rgba('#d89051'))
ell(d, (1438,566,1462,578), fill=rgba('#c47a3d'), outline=rgba('#8f5426'), width=2)
line(d, [(1424,582),(1408,568)], rgba('#b2803c'), 5)
line(d, [(1476,582),(1490,566)], rgba('#b2803c'), 5)

# ---------- upper wall details ----------
# tiny frame between shelves and window? keep clean
# hanging herbs left of window
soft_shadow(im, (460,300,520,520), 10, 30)
line(d, [(488,296),(488,330)], rgba('#8b6c4a'), 3)
for i in range(5):
    x=480+i*5
    line(d, [(488,330),(x,430+random.uniform(-8,8))], rgba('#6d7a4e'), 3)
    for j in range(12):
        t=(j+1)/13
        xx=488+(x-488)*t; yy=330+100*t
        leaf(d, xx,yy, random.uniform(-7,7), random.uniform(3,9), 4.5, rgba(random.choice(['#6c8054','#7e9160','#596d47'])))
    rect(d, (x-3,425,x+3,440), rgba('#b98356'))

# ---------- counter ----------
# shadow of counter on cabinets
soft_shadow(im, (55,812,1545,850), 10, 90, ellipse=False)
# countertop
grad_rect(im, (56,748,1544,808), rgba('#d8a26b'), rgba('#b17645'))
# board strips
for i in range(7):
    y=750+i*8
    line(d, [(60,y),(1540,y+2)], rgba('#8d5732',40), 2)
# grain
for i in range(18):
    y=random.uniform(753,803)
    pts=[(60,y)]
    for x in range(160,1540,160):
        pts.append((x, y+random.uniform(-2.0,2.0)))
    line(d, pts, rgba('#7e4b2b',random.randint(12,26)), 1)
# vertical joints
for x in [300, 560, 920, 1220, 1450]:
    line(d, [(x,750),(x,806)], rgba('#7d4a2c',35), 1)
# front edge
grad_rect(im, (56,806,1544,830), rgba('#a86b3f'), rgba('#87512f'))
rect(d, (56,806,1544,810), rgba('#e0ad75',120))
rect(d, (56,826,1544,832), rgba('#6f432b',160))
# warm sun on counter right
sunpatch = Image.new('RGBA', im.size, (0,0,0,0))
spd = ImageDraw.Draw(sunpatch)
spd.polygon([P(1010,750),P(1510,750),P(1544,830),P(960,830)], fill=(255,216,150,30))
sunpatch = sunpatch.filter(ImageFilter.GaussianBlur(V(18)))
im.alpha_composite(sunpatch)

# ---------- lower cabinets ----------
# main body
grad_rect(im, (76,828,1524,1050), rgba('#7f9775'), rgba('#657e61'))
# top rail shadows
grad_rect(im, (76,828,1524,850), rgba('#4f654c',85), rgba('#4f654c',0))
# doors helper
def shaker_door(x0,y0,x1,y1, knob='right'):
    rrect(d, (x0,y0,x1,y1), 4, fill=rgba('#7d9573'), outline=rgba('#5b7158'), width=2)
    rrect(d, (x0+12,y0+14,x1-12,y1-14), 3, fill=rgba('#8aa080'), outline=rgba('#5d7460'), width=2)
    # inner panel highlight / shadow
    line(d, [(x0+14,y0+17),(x1-14,y0+17)], rgba('#a4b599',90), 2)
    rect(d, (x0+14,y1-20,x1-14,y1-16), rgba('#4e644d',30))
    # knob
    cx = x1-24 if knob=='right' else x0+24
    cy = y0+40
    ell(d, (cx-7,cy-7,cx+7,cy+7), fill=rgba('#cb9a4f'), outline=rgba('#8e642f'), width=2)
    ell(d, (cx-5,cy-5,cx+1,cy-1), fill=rgba('#f0c97d'))

# left doors
for x0 in [92, 286, 480]:
    shaker_door(x0,850,x0+180,1038,'right')
# right doors
for x0 in [956, 1150, 1344]:
    shaker_door(x0,850,x0+180,1038,'left')
# sink base doors
shaker_door(688,922,794,1038,'right')
shaker_door(802,922,914,1038,'left')
# side panels
grad_rect(im, (56,820,78,1050), rgba('#6d8464'), rgba('#53694f'))
grad_rect(im, (1522,820,1544,1050), rgba('#60765b'), rgba('#4b5f48'))
# toe kick
rect(d, (80,1038,1520,1050), rgba('#4d604a'))
grad_rect(im, (80,1050,1520,1066), rgba('#3f503d'), rgba('#2f3d2f'))

# ---------- sink ----------
# shadow
soft_shadow(im, (660,760,940,910), 12, 60)
# opening
rrect(d, (672,742,928,806), 20, fill=rgba('#7f7a6b'))
# inner basin
ell(d, (676,744,924,798), fill=rgba('#b9b5a8'))
ell(d, (684,750,916,792), fill=rgba('#d6d1c2'))
ell(d, (690,754,910,788), fill=rgba('#efe9d9'))
# water / shadow inside
ell(d, (714,768,886,792), fill=rgba('#c6c8bd'))
d.arc((V(714),V(760),V(886),V(792)), 0, 180, fill=rgba('#fdf8e9',180), width=V(5))
# drain
ell(d, (792,780,808,788), fill=rgba('#8e8d82'))
# farmhouse apron
grad_rect(im, (674,788,926,902), rgba('#fffaf0'), rgba('#dfd6c2'))
rrect(d, (674,786,926,902), 16, fill=None, outline=rgba('#b8ad99'), width=2)
for i in range(7):
    x=684+i*35
    line(d, [(x,796),(x-2,892)], rgba('#c7bda9',60), 3)
    line(d, [(x+4,796),(x+2,892)], rgba('#ffffff',75), 2)
line(d, [(690,892),(910,892)], rgba('#b7ac98',65), 3)
# highlight
rect(d, (688,794,904,802), rgba('#ffffff',90))
# faucet shadow on backsplash
soft_shadow(im, (770,660,900,760), 8, 45)
# faucet
brass_dark=rgba('#8a5b28'); brass=rgba('#c18d3f'); brass_l=rgba('#f1cd84')
line(d, [(800,752),(800,684)], brass_dark, 13)
line(d, [(800,750),(800,686)], brass, 9)
line(d, [(797,748),(797,690)], brass_l, 3)
arch = bez((800,684),(800,640),(870,638),(870,682),40)
line(d, arch, brass_dark, 14)
line(d, arch, brass, 10)
line(d, [(p[0]-2,p[1]-2) for p in arch], brass_l, 3)
line(d, [(870,678),(870,706)], brass_dark, 13)
line(d, [(870,678),(870,704)], brass, 9)
rrect(d, (858,700,882,714), 5, fill=rgba('#b27a32'), outline=rgba('#7f5527'), width=2)
ell(d, (864,710,876,718), fill=rgba('#d9a956'))
# handle
line(d, [(786,722),(760,722)], brass_dark, 8)
line(d, [(786,722),(762,722)], brass, 5)
ell(d, (752,716,764,728), fill=rgba('#c99a4c'), outline=rgba('#815a2b'), width=2)
# base plate
ell(d, (788,744,812,756), fill=rgba('#b9853b'), outline=rgba('#7f5527'), width=2)

# soap + sponge
soft_shadow(im, (928,730,976,760), 4, 45)
rrect(d, (936,712,964,752), 7, fill=rgba('#d9b46b'), outline=rgba('#a77b3f'), width=2)
rect(d, (942,704,958,718), rgba('#9c7136'))
rect(d, (940,722,960,740), rgba('#f8efd8'))
line(d, [(944,730),(956,730)], rgba('#b58b53'), 2)
# sponge
rrect(d, (920,744,958,760), 4, fill=rgba('#e4c75c'), outline=rgba('#b29442'), width=2)
rect(d, (920,744,958,750), rgba('#7e9c63'))

# ---------- left counter objects ----------
# cutting board
soft_shadow(im, (140,744,400,768), 6, 55)
rrect(d, (148,712,392,753), 12, fill=rgba('#c68b55'), outline=rgba('#8e5a33'), width=2)
rrect(d, (158,718,382,747), 9, fill=rgba('#d9a46a'))
# board grain
for i in range(6):
    y=722+i*4
    line(d, [(166,y),(374,y+1)], rgba('#a76c3e',55), 1)
# bread
soft_shadow(im, (200,698,320,748), 6, 50)
poly(d, [(206,740),(210,710),(232,694),(282,694),(310,710),(314,740)], fill=rgba('#c98343'))
poly(d, [(214,734),(218,714),(238,702),(276,702),(300,714),(304,734)], fill=rgba('#e0a55e'))
# scoring
for x in [232,252,272]:
    d.arc((V(x-12),V(700),V(x+12),V(722)), 200, 340, fill=rgba('#f6d49a'), width=V(3))
# slices
ell(d, (320,724,356,748), fill=rgba('#e6b06b'), outline=rgba('#a36b3e'), width=2)
ell(d, (326,728,350,744), fill=rgba('#f6dba1'))
# orange
ell(d, (350,716,388,748), fill=rgba('#d9823d'), outline=rgba('#a65c2e'), width=2)
for a in range(0,360,60):
    x=369+math.cos(math.radians(a))*8; y=732+math.sin(math.radians(a))*8
    ell(d, (x-2,y-2,x+2,y+2), fill=rgba('#f6c46b'))
# knife
poly(d, [(182,706),(280,700),(286,706),(186,712)], fill=rgba('#c9c6ba'))
poly(d, [(180,706),(210,704),(210,712),(180,712)], fill=rgba('#7b5334'))
line(d, [(188,705),(278,701)], rgba('#f6f2e9',180), 2)

# kettle
soft_shadow(im, (414,742,582,768), 9, 70)
# rounded enamel body
ell(d, (430,660,558,754), fill=rgba('#efe1c7'), outline=rgba('#a98c68'), width=2)
ell(d, (502,670,552,748), fill=rgba('#d9c19f',110))
ell(d, (438,670,478,748), fill=rgba('#fcf3e0',90))
ell(d, (446,680,466,724), fill=rgba('#fff9ea',80))
# base band
rrect(d, (426,736,560,756), 9, fill=rgba('#c49a5a'), outline=rgba('#8f6737'), width=2)
rect(d, (432,740,554,744), rgba('#e8c785'))
rect(d, (432,750,554,753), rgba('#84602f',80))
# lid
ell(d, (458,646,530,674), fill=rgba('#d9b576'), outline=rgba('#8f6737'), width=2)
ell(d, (472,651,516,666), fill=rgba('#efd49a'))
ell(d, (486,640,500,654), fill=rgba('#b9853b'), outline=rgba('#7e5728'), width=2)
# spout
poly(d, [(438,686),(402,666),(396,682),(436,708)], fill=rgba('#e9d9bc'), outline=rgba('#a98c68'))
line(d, [(434,687),(402,670)], rgba('#fff8e8',90), 3)
ell(d, (394,676,406,687), fill=rgba('#7c5a34'))
# handle arch
d.arc((V(410),V(648),V(578),V(744)), 180, 360, fill=rgba('#8f6737'), width=V(12))
d.arc((V(410),V(648),V(578),V(744)), 180, 360, fill=rgba('#c49a5a'), width=V(8))
d.arc((V(414),V(652),V(574),V(740)), 190, 350, fill=rgba('#e8c785'), width=V(2))
ell(d, (404,702,420,718), fill=rgba('#a97b3e'), outline=rgba('#7e5728'), width=2)
ell(d, (568,702,584,718), fill=rgba('#a97b3e'), outline=rgba('#7e5728'), width=2)
# painted blue sprigs
for x,y in [(476,708),(503,724),(528,704)]:
    line(d, [(x,y-5),(x,y+9)], rgba('#6f8d7c',140), 2)
    for dx,dy in [(-7,2),(7,2),(-5,8),(5,8)]:
        leaf(d, x,y, dx,dy, 4, rgba('#8aa79a',140))
    ell(d, (x-2.5,y-7,x+2.5,y-2), fill=rgba('#7c9cba',170))
# steam from spout
for i in range(2):
    pts=bez((398+i*5,662),(382+i*10,632),(410+i*8,614),(394+i*9,588),30)
    line(d, pts, rgba('#fff8e7',85), 3)
    line(d, pts, rgba('#fff8e7',45), 6)

# mug beside kettle
soft_shadow(im, (596,742,654,762), 4, 45)
rrect(d, (602,694,646,752), 9, fill=rgba('#879d95'), outline=rgba('#61756e'), width=2)
ell(d, (602,688,646,702), fill=rgba('#c8d2c9'))
ell(d, (608,691,640,699), fill=rgba('#5d4a39'))
d.arc((V(641),V(706),V(666),V(734)), 270, 90, fill=rgba('#61756e'), width=V(5))
rect(d, (608,704,640,710), rgba('#f5efdf',55))
# steam
for i in range(2):
    pts=bez((616+i*12,688),(602+i*15,658),(634+i*12,642),(616+i*12,616),35)
    line(d, pts, rgba('#fff7e5',100), 3)
    line(d, pts, rgba('#fff7e5',60), 7)

# ---------- right counter objects ----------
# plate stack
soft_shadow(im, (966,742,1080,766), 5, 45)
for i,yy in enumerate([744,736,728,720]):
    ell(d, (972,yy-10,1074,yy+8), fill=rgba(['#f6ecda','#e8e4d6','#f2e4cc','#dce7df'][i]), outline=rgba('#b29a77'), width=2)
ell(d, (998,704,1046,730), fill=rgba('#e8b36b'), outline=rgba('#a87540'), width=2)
ell(d, (1006,710,1038,726), fill=rgba('#f6d69c'))
# croissant cut
for i in range(3):
    d.arc((V(1000+i*4),V(700),V(1040-i*4),V(728)), 200, 340, fill=rgba('#b77e43'), width=V(2))

# utensil crock
soft_shadow(im, (1090,742,1168,766), 5, 45)
rrect(d, (1098,684,1160,752), 10, fill=rgba('#c9926b'), outline=rgba('#946142'), width=2)
rect(d, (1104,700,1154,748), rgba('#b97c58'))
# utensils
for i,(x,dx) in enumerate([(1112,-6),(1128,4),(1144,-3)]):
    line(d, [(x,692),(x+dx,646)], rgba('#8c6b46'), 5)
    ell(d, (x+dx-7,638,x+dx+7,654), fill=rgba('#c7b18e'), outline=rgba('#8c6b46'), width=2)
# wooden spoon
line(d, [(1140,694),(1150,650)], rgba('#b4834f'), 5)
ell(d, (1142,642,1160,658), fill=rgba('#c7955b'))

# fruit bowl
soft_shadow(im, (1176,740,1322,766), 6, 50)
ell(d, (1182,720,1316,758), fill=rgba('#e8ddc8'), outline=rgba('#b59a75'), width=2)
for x,y,col in [(1210,718,'#d9823d'),(1246,712,'#df9f3e'),(1282,720,'#cf7434'),(1232,724,'#e8b14b')]:
    ell(d, (x-16,y-14,x+16,y+14), fill=rgba(col), outline=rgba('#a85e2d'), width=2)
    ell(d, (x-11,y-10,x-2,y-2), fill=rgba('#f3c26b',180))
    leaf(d, x+4,y-14, 6,-6, 5, rgba('#5f7e4d'))
# orange slice on board? already.

# potted herb far right
soft_shadow(im, (1388,742,1490,768), 6, 50)
poly(d, [(1402,752),(1410,680),(1472,680),(1480,752)], fill=rgba('#c17853'), outline=rgba('#98583a'))
rect(d, (1404,676,1478,692), rgba('#d28b62'))
for i in range(18):
    a=-math.pi*0.92 + i*math.pi*0.08
    x=1441+math.cos(a)*random.uniform(20,58); y=676+math.sin(a)*random.uniform(22,70)
    leaf(d, 1441,678, x-1441, y-678, 8, rgba(random.choice(['#4f7049','#648658','#78946b'])))

# small butter dish between utensil and fruit
soft_shadow(im, (1162,744,1208,762), 4, 35)
rrect(d, (1160,732,1204,752), 6, fill=rgba('#f2e7d0'), outline=rgba('#b49a79'), width=2)
rrect(d, (1166,726,1198,736), 4, fill=rgba('#e5d3ae'))
ell(d, (1172,728,1192,733), fill=rgba('#f8df7d'))

# ---------- stool with sleeping cat ----------
# stool shadow
soft_shadow(im, (1252,1160,1442,1205), 14, 60)
# legs
for x in [1280,1396]:
    rrect(d, (x-6,1056,x+6,1178), 4, fill=rgba('#95613e'))
    rrect(d, (x-4,1058,x+1,1178), 2, fill=rgba('#c08b5d'))
    line(d, [(x-2,1080),(x+2,1160)], rgba('#7a4b30',90), 2)
# cross bars
rrect(d, (1280,1112,1402,1120), 3, fill=rgba('#a46d45'))
# seat
soft_shadow(im, (1262,1032,1424,1074), 8, 55)
rrect(d, (1266,1028,1420,1056), 14, fill=rgba('#a86f45'), outline=rgba('#7e4e2e'), width=2)
rect(d, (1270,1032,1416,1040), rgba('#ce9564'))
# cushion
rrect(d, (1278,1006,1408,1042), 16, fill=rgba('#c98865'), outline=rgba('#9c5f45'), width=2)
rrect(d, (1286,1012,1400,1032), 10, fill=rgba('#d99a73'))
for x in [1308,1360]:
    line(d, [(x,1008),(x,1040)], rgba('#a9654b',70), 2)
# cat curled
soft_shadow(im, (1290,990,1403,1036), 8, 50)
ell(d, (1292,978,1400,1035), fill=rgba('#d88444'))
ell(d, (1300,986,1394,1030), fill=rgba('#e9a15e'))
# striping
for i in range(4):
    d.arc((V(1310+i*12),V(984),V(1372+i*8),V(1028)), 250, 320, fill=rgba('#bd6a32'), width=V(4))
# tail
curve=bez((1380,1018),(1424,1014),(1420,1060),(1370,1048),30)
line(d, curve, rgba('#c87638'), 13)
line(d, curve, rgba('#e2a15f'), 8)
# head
ell(d, (1280,994,1322,1032), fill=rgba('#e9a15e'))
poly(d, [(1283,1000),(1286,980),(1301,994)], fill=rgba('#d88444'))
poly(d, [(1304,994),(1318,980),(1318,1002)], fill=rgba('#d88444'))
poly(d, [(1286,999),(1288,987),(1297,996)], fill=rgba('#efb27a'))
poly(d, [(1307,996),(1315,987),(1315,1000)], fill=rgba('#efb27a'))
# closed eyes
d.arc((V(1288),V(1006),V(1298),V(1018)), 200, 340, fill=rgba('#7b4b2c'), width=V(2))
d.arc((V(1303),V(1006),V(1313),V(1018)), 200, 340, fill=rgba('#7b4b2c'), width=V(2))
ell(d, (1295,1016,1300,1021), fill=rgba('#b96d50'))
# muzzle
ell(d, (1291,1016,1308,1029), fill=rgba('#f4c48f'))
# paws
ell(d, (1294,1022,1310,1035), fill=rgba('#f0b77e'))
# whiskers
for dy in [-2,2]:
    line(d, [(1286,1018),(1272,1016+dy)], rgba('#fff3dc',120), 1)
    line(d, [(1313,1018),(1327,1016+dy)], rgba('#fff3dc',120), 1)

# ---------- floor slippers ----------
soft_shadow(im, (160,1150,340,1195), 8, 50)
for i,(x0,y0,col) in enumerate([(174,1128,'#c97862'),(234,1146,'#d48b71')]):
    rrect(d, (x0,y0,x0+86,y0+46), 20, fill=rgba(col), outline=rgba('#935343'), width=2)
    rrect(d, (x0+10,y0+6,x0+76,y0+32), 14, fill=rgba(mix(rgba(col)[:3],(255,239,210),.24)))
    for x in range(x0+18,x0+72,10):
        line(d, [(x,y0+12),(x+2,y0+32)], rgba('#f2cba8',70), 2)
    ell(d, (x0+28,y0+14,x0+58,y0+34), fill=rgba('#f6e3c8',160))

# ---------- pendant lamp ----------
# one copper pendant on left above shelf
soft_shadow(im, (272,168,362,216), 8, 55)
line(d, [(316,0),(316,136)], rgba('#6b4a2e'), 4)
rrect(d, (306,132,326,146), 3, fill=rgba('#9a6e35'))
poly(d, [(280,196),(352,196),(332,150),(300,150)], fill=rgba('#b97738'), outline=rgba('#855124'))
poly(d, [(285,191),(347,191),(331,156),(301,156)], fill=rgba('#d69a52'))
ell(d, (292,188,340,204), fill=rgba('#8f5b2a'))
ell(d, (300,190,332,200), fill=rgba('#ffe6a8'))
glow(im, 316, 210, 115, 100, (255,210,130), 65, 45)
# tiny second pendant right, smaller and farther
line(d, [(1512,0),(1512,84)], rgba('#6b4a2e'), 3)
poly(d, [(1482,132),(1542,132),(1526,92),(1498,92)], fill=rgba('#b97738'), outline=rgba('#855124'))
ell(d, (1494,126,1534,140), fill=rgba('#8f5b2a'))
ell(d, (1501,128,1527,137), fill=rgba('#ffe6a8'))
glow(im, 1512, 140, 80, 70, (255,210,130), 50, 38)

im.save('/tmp/vellery-jehl2kw1/work/debug_beforelight.png')
# ---------- morning light ----------
# soft, diffuse wash of window light spilling into the room
beam = Image.new('RGBA', im.size, (0,0,0,0))
bd = ImageDraw.Draw(beam)
bd.polygon([P(552,122),P(1048,122),P(1560,900),P(930,1200),P(640,1200),P(520,760)], fill=(255,225,162,11))
bd.polygon([P(560,134),P(790,134),P(1210,1040),P(930,1200),P(640,1200),P(520,780)], fill=(255,235,184,8))
beam = beam.filter(ImageFilter.GaussianBlur(V(38)))
im.alpha_composite(beam)
# faint pane-shaped gradients, kept very delicate
for x0,x1 in [(552,792),(806,1046)]:
    b=Image.new('RGBA',im.size,(0,0,0,0)); bd=ImageDraw.Draw(b)
    bd.polygon([P(x0,126),P(x1,126),P(x1+380,980),P(x0+210,1140)], fill=(255,236,190,5))
    b=b.filter(ImageFilter.GaussianBlur(V(30)))
    im.alpha_composite(b)
# warm sunlight pooled on the right of the counter
sunpatch = Image.new('RGBA', im.size, (0,0,0,0))
spd = ImageDraw.Draw(sunpatch)
spd.polygon([P(1000,748),P(1490,748),P(1540,830),P(960,830)], fill=(255,224,164,18))
sunpatch = sunpatch.filter(ImageFilter.GaussianBlur(V(26)))
im.alpha_composite(sunpatch)

# dust motes
mot = Image.new('RGBA', im.size, (0,0,0,0))
md = ImageDraw.Draw(mot)
for i in range(65):
    t=random.random()
    x=580 + t*520 + random.uniform(-100,300)
    y=160 + t*760 + random.uniform(-80,150)
    if x>1560 or y>1100: continue
    r=random.uniform(1.0,3.2)
    a=random.randint(18,75)
    md.ellipse((V(x-r),V(y-r),V(x+r),V(y+r)), fill=(255,242,200,a))
mot=mot.filter(ImageFilter.GaussianBlur(V(1.2)))
im.alpha_composite(mot)

im.save('/tmp/vellery-jehl2kw1/work/debug_beforegrade.png')
# ---------- warmth / grade ----------
# warm veil
warm = Image.new('RGBA', im.size, (255,181,105,12))
im.alpha_composite(warm)
# vignette
vig = Image.radial_gradient('L').resize((CW,CH), Image.Resampling.BILINEAR)
vig = ImageOps.invert(vig)
# radial gradient center white -> edges black? invert to dark edges; compose black alpha
vig = vig.point(lambda v: int(v*0.28))
black = Image.new('RGBA', im.size, (39,26,18,255))
black.putalpha(vig)
im.alpha_composite(black)
# grain
texture(im, 11, 9)
# subtle painted canvas fibers
fib = Image.new('RGBA', im.size, (0,0,0,0))
fd = ImageDraw.Draw(fib)
for i in range(900):
    x=random.uniform(0,CW); y=random.uniform(0,CH)
    fd.line((x,y,x+random.uniform(-6,6),y+random.uniform(4,14)), fill=(255,250,235,random.randint(3,9)), width=1)
im.alpha_composite(fib)

# final downscale
out = im.convert('RGB').resize((W,H), Image.Resampling.LANCZOS)
out.save('/tmp/vellery-jehl2kw1/work/cozy_kitchen_morning.png', quality=95)
im.resize((W,H), Image.Resampling.LANCZOS).save('/tmp/vellery-jehl2kw1/work/cozy_kitchen_morning_preview.png')
print('saved', out.size)
