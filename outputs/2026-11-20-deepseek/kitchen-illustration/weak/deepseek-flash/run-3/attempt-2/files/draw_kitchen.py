from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math, random
from pathlib import Path

random.seed(7)
W, H = 1600, 1000
S = 2
CW, CH = W * S, H * S

def sc(v): return int(round(v * S))
def pt(p): return (sc(p[0]), sc(p[1]))
def box(x0, y0, x1, y1): return [sc(x0), sc(y0), sc(x1), sc(y1)]
def clamp(v, a=0, b=255): return max(a, min(b, int(v)))

def mix(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def shade(c, f):
    # f < 1 darker, f > 1 lighter
    if f <= 1:
        return tuple(int(v * f) for v in c)
    return tuple(int(v + (255 - v) * (f - 1)) for v in c)

def vgrad(w, h, stops):
    """Vertical gradient RGB, stops = [(pos,color),...]"""
    w, h = max(1, int(w)), max(1, int(h))
    im = Image.new('RGB', (1, h))
    p = im.load()
    for y in range(h):
        t = y / max(1, h - 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i+1]
            if p0 <= t <= p1:
                u = (t - p0) / max(1e-9, p1 - p0)
                p[0, y] = mix(c0, c1, u)
                break
        else:
            p[0, y] = stops[-1][1]
    return im.resize((w, h), Image.Resampling.BILINEAR)

def hgrad(w, h, left, right):
    w, h = max(1, int(w)), max(1, int(h))
    im = Image.new('RGB', (w, 1))
    p = im.load()
    for x in range(w):
        p[x, 0] = mix(left, right, x / max(1, w - 1))
    return im.resize((w, h), Image.Resampling.BILINEAR)

def shape_grad_rect(x0, y0, x1, y1, stops, radius=0, outline=None, width=1):
    x0, y0, x1, y1 = box(x0, y0, x1, y1)
    w, h = x1-x0, y1-y0
    grad = vgrad(w, h, stops)
    mask = Image.new('L', (w, h), 0)
    md = ImageDraw.Draw(mask)
    if radius:
        md.rounded_rectangle([0, 0, w-1, h-1], radius=sc(radius), fill=255)
    else:
        md.rectangle([0, 0, w-1, h-1], fill=255)
    img.paste(grad, (x0, y0), mask)
    if outline:
        d.rounded_rectangle([x0, y0, x1-1, y1-1], radius=sc(radius), outline=outline, width=sc(width))

def rrect(x0, y0, x1, y1, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(box(x0, y0, x1, y1), radius=sc(radius), fill=fill, outline=outline, width=sc(width))

def rect(x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.rectangle(box(x0, y0, x1, y1), fill=fill, outline=outline, width=sc(width))

def ell(x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.ellipse(box(x0, y0, x1, y1), fill=fill, outline=outline, width=sc(width))

def poly(points, fill=None, outline=None, width=1):
    d.polygon([pt(p) for p in points], fill=fill)
    if outline:
        d.line([pt(p) for p in points] + [pt(points[0])], fill=outline, width=sc(width), joint='curve')

def line(points, fill, width=1):
    d.line([pt(p) for p in points], fill=fill, width=sc(width), joint='curve')

def arc(x0, y0, x1, y1, a0, a1, fill, width=1):
    d.arc(box(x0, y0, x1, y1), a0, a1, fill=fill, width=sc(width))

def bezier(points, n=80):
    # de casteljau on list of control points
    out = []
    for i in range(n+1):
        t = i / n
        pts = list(points)
        while len(pts) > 1:
            pts = [(pts[j][0]*(1-t)+pts[j+1][0]*t, pts[j][1]*(1-t)+pts[j+1][1]*t) for j in range(len(pts)-1)]
        out.append(pts[0])
    return out

def glow(cx, cy, rx, ry, color, strength=255, blur=0):
    # radial glow on an overlay, alpha center strength
    size = 512
    g = Image.radial_gradient('L').resize((size, size), Image.Resampling.BILINEAR)
    # center black -> invert to white center
    g = ImageChops.invert(g)
    g = g.point(lambda p: int(p * strength / 255))
    layer = Image.new('RGBA', (sc(rx*2), sc(ry*2)), color + (0,))
    layer.putalpha(g.resize((sc(rx*2), sc(ry*2)), Image.Resampling.BILINEAR))
    if blur:
        layer = layer.filter(ImageFilter.GaussianBlur(sc(blur)))
    img.paste(layer, (sc(cx-rx), sc(cy-ry)), layer)

def soft_shadow(x0, y0, x1, y1, color=(55, 30, 18), alpha=80, blur=12, radius=None):
    layer = Image.new('RGBA', (CW, CH), (0,0,0,0))
    ld = ImageDraw.Draw(layer)
    b = box(x0, y0, x1, y1)
    r = sc(radius) if radius else sc(min(x1-x0, y1-y0)/2)
    ld.rounded_rectangle(b, radius=r, fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(sc(blur)))
    img.alpha_composite(layer) if img.mode == 'RGBA' else img.paste(layer, (0,0), layer)

def shape_shadow(points, color=(55,30,18), alpha=70, blur=10):
    layer = Image.new('RGBA', (CW, CH), (0,0,0,0))
    ld = ImageDraw.Draw(layer)
    ld.polygon([pt(p) for p in points], fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(sc(blur)))
    img.paste(layer, (0,0), layer)

def texture_lines(points_groups, color, width=1, alpha=None):
    for pts in points_groups:
        line(pts, color, width)

# ---------------------------------------------------------------- canvas
img = Image.new('RGB', (CW, CH), (230, 210, 184)).convert('RGBA')
d = ImageDraw.Draw(img)

# ================================================================ WALL
# warm plaster gradient
shape_grad_rect(0, 0, 1600, 620, [
    (0.0, (205, 172, 136)),
    (0.18, (230, 201, 168)),
    (0.52, (242, 219, 187)),
    (0.82, (248, 229, 202)),
    (1.0, (244, 222, 193)),
], radius=0)

# broad pools of light and shade on wall
glow(325, 275, 390, 360, (255, 232, 186), 70, 50)
glow(1320, 260, 420, 330, (255, 224, 174), 34, 55)
glow(60, 350, 220, 500, (90, 58, 40), 50, 55)
glow(1540, 420, 260, 500, (95, 60, 38), 65, 60)
glow(815, 110, 320, 180, (255, 238, 204), 34, 40)

# subtle plaster mottling
for i in range(16):
    x = random.uniform(0, 1600); y = random.uniform(50, 590)
    rx = random.uniform(60, 190); ry = random.uniform(30, 100)
    c = random.choice([(255, 240, 215), (206, 174, 142), (239, 212, 180)])
    glow(x, y, rx, ry, c, random.randint(12, 24), 30)

# ceiling beam
shape_grad_rect(0, 0, 1600, 58, [
    (0, (73, 46, 33)), (0.45, (99, 64, 44)), (0.8, (79, 49, 34)), (1, (58, 37, 26))
], radius=0)
rect(0, 56, 1600, 64, (70, 43, 30, 115))
for i in range(18):
    y = random.uniform(6, 50)
    x0 = random.uniform(-40, 1500); x1 = x0 + random.uniform(60, 260)
    line([(x0, y), (x1, y+random.uniform(-2,2))], (55, 34, 24, 60), random.uniform(0.6,1.4))
# beam shadow
glow(800, 88, 820, 70, (75, 45, 28), 66, 22)
# small ceiling cornice line
rect(0, 58, 1600, 64, (185, 149, 116, 120))

# ================================================================ FLOOR
shape_grad_rect(0, 840, 1600, 1000, [
    (0, (161, 100, 66)), (0.3, (181, 117, 78)), (0.72, (200, 134, 91)), (1, (175, 110, 72))
], radius=0)

# floor boards
board_edges = [850, 873, 897, 923, 952, 983, 1001]
for yy in board_edges:
    line([(0, yy), (1600, yy+random.uniform(-1.5,1.5))], (105, 61, 40, 100), 1.3)
    line([(0, yy+2.5), (1600, yy+2.5)], (225, 163, 115, 36), 1)
# plank seams
for x in [190, 470, 760, 1110, 1370, 1580]:
    y0 = random.choice(board_edges[:-1]); y1 = board_edges[board_edges.index(y0)+1]
    line([(x, y0), (x+random.uniform(-2,2), y1)], (101, 58, 37, 85), 1.1)
# floor grain
for i in range(44):
    yy = random.uniform(852, 1000)
    x0 = random.uniform(-40, 1500)
    ln = random.uniform(40, 210)
    line([(x0, yy), (x0+ln, yy+random.uniform(-1.5,1.5))], (95, 55, 35, random.randint(18, 38)), random.uniform(0.5, 1.2))
# gentle darkening at floor edge and sides
glow(800, 852, 800, 28, (70, 38, 24), 110, 16)
glow(0, 930, 190, 220, (78, 42, 26), 80, 50)
glow(1600, 940, 220, 230, (72, 38, 24), 95, 50)

# ================================================================ WINDOW
# outer wall shadow / reveal
soft_shadow(115, 73, 658, 570, (53, 31, 20), 72, 18, 8)
# outer wood casing
shape_grad_rect(128, 77, 646, 558, [
    (0, (106, 66, 43)), (0.25, (136, 88, 57)), (0.75, (122, 77, 50)), (1, (88, 53, 35))
], radius=5)
# casing highlight and inner bevel
rrect(137, 87, 637, 549, 3, outline=(176, 120, 78, 160), width=2)
rrect(154, 104, 620, 533, 2, outline=(65, 38, 25, 210), width=3)
# dark reveal
rect(158, 108, 616, 530, (38, 26, 20))

# window scene
win_w, win_h = sc(450), sc(408)
scene = Image.new('RGB', (win_w, win_h))
sd = ImageDraw.Draw(scene)
sky = vgrad(win_w, win_h, [
    (0.0, (112, 169, 196)),
    (0.25, (153, 197, 207)),
    (0.52, (216, 222, 198)),
    (0.73, (248, 218, 166)),
    (1.0, (255, 226, 171)),
])
scene.paste(sky, (0,0))
# sun glow and disc
sun_layer = Image.new('RGBA', (win_w, win_h), (0,0,0,0))
sld = ImageDraw.Draw(sun_layer)
for r, a in [(200, 28), (150, 38), (100, 56), (65, 70)]:
    sld.ellipse([sc(115-r), sc(155-r), sc(115+r), sc(155+r)], fill=(255, 239, 183, a))
sld.ellipse([sc(90), sc(130), sc(140), sc(180)], fill=(255, 248, 211, 220))
sun_layer = sun_layer.filter(ImageFilter.GaussianBlur(sc(8)))
scene = Image.alpha_composite(scene.convert('RGBA'), sun_layer)
sd = ImageDraw.Draw(scene)
# distant hills
sd.polygon([(0, sc(318)), (sc(60), sc(286)), (sc(125), sc(304)), (sc(200), sc(270)), (sc(275), sc(300)), (sc(350), sc(283)), (sc(450), sc(307)), (sc(450), sc(408)), (0, sc(408))], fill=(174, 184, 145))
sd.polygon([(0, sc(345)), (sc(80), sc(325)), (sc(165), sc(349)), (sc(250), sc(321)), (sc(335), sc(348)), (sc(430), sc(326)), (sc(450), sc(334)), (sc(450), sc(408)), (0, sc(408))], fill=(137, 157, 117))
# far tree line
sd.polygon([(0, sc(355)), (sc(45), sc(340)), (sc(70), sc(352)), (sc(100), sc(334)), (sc(126), sc(349)), (sc(160), sc(339)), (sc(188), sc(355)), (sc(220), sc(340)), (sc(250), sc(351)), (sc(280), sc(336)), (sc(310), sc(350)), (sc(345), sc(341)), (sc(376), sc(354)), (sc(405), sc(337)), (sc(450), sc(350)), (sc(450), sc(408)), (0, sc(408))], fill=(104, 127, 91))
# tree trunk & branches right side
sd.line([(sc(383), sc(408)), (sc(379), sc(347)), (sc(371), sc(300)), (sc(382), sc(263))], fill=(86, 71, 52), width=sc(5))
for a,b,c in [((379,347),(340,330),(322,298)), ((379,315),(414,295),(430,268)), ((372,286),(350,270),(346,246)), ((381,304),(399,281),(400,258))]:
    q = bezier([a,b,c], 30)
    sd.line([(sc(x),sc(y)) for x,y in q], fill=(84, 68, 50), width=sc(3))
# leaves
for i in range(38):
    ang = random.uniform(0, math.tau); rr = random.uniform(0, 74)
    x = 380 + math.cos(ang)*rr; y = 278 + math.sin(ang)*rr*0.8
    if 300 < x < 450 and 228 < y < 360:
        sd.ellipse([sc(x-7), sc(y-3.5), sc(x+7), sc(y+3.5)], fill=random.choice([(108,132,88),(128,151,101),(89,115,79)]))
# little birds
sd.arc([sc(282), sc(198), sc(300), sc(210)], 200, 340, fill=(80,89,78), width=sc(1.5))
sd.arc([sc(305), sc(213), sc(323), sc(225)], 200, 340, fill=(80,89,78), width=sc(1.5))
# soft light wash in scene
glow_layer = Image.new('RGBA', scene.size, (0,0,0,0))
gd = ImageDraw.Draw(glow_layer)
gd.rectangle([0,0,win_w,win_h], fill=(255, 225, 164, 24))
scene = Image.alpha_composite(scene, glow_layer)
# clip to window inner
mask = Image.new('L', (CW, CH), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle(box(174, 124, 600, 520), radius=sc(2), fill=255)
scene = scene.resize((sc(426), sc(396)), Image.Resampling.LANCZOS)
img.paste(scene, (sc(174), sc(124)), mask.crop(box(174,124,600,520)))
# pane muntins
# vertical
shape_grad_rect(378, 124, 394, 520, [(0,(133,87,56)),(0.5,(166,115,79)),(1,(112,70,45))], radius=0)
rect(376, 124, 379, 520, (60, 36, 23, 100))
rect(394, 124, 398, 520, (219, 167, 121, 70))
# horizontal
shape_grad_rect(174, 311, 600, 326, [(0,(125,81,52)),(0.5,(169,118,80)),(1,(109,68,44))], radius=0)
rect(174, 309, 600, 313, (56, 33, 21, 90))
rect(174, 326, 600, 329, (217, 164, 117, 65))
# inner window shadow top & left
rect(174, 124, 600, 130, (47, 31, 22, 105))
rect(174, 124, 181, 520, (47, 31, 22, 90))
# tiny glints on pane
for q in [(210,165),(425,355),(236,430),(512,180)]:
    line([q, (q[0]+14, q[1]+1)], (255, 247, 220, 55), 1)
# sill
shape_grad_rect(112, 518, 660, 551, [
    (0, (181, 123, 82)), (0.25, (218, 159, 110)), (0.62, (181, 119, 77)), (1, (123, 74, 46))
], radius=3)
rect(112, 518, 660, 522, (247, 194, 143, 95))
rect(112, 550, 660, 558, (84, 49, 31, 180))
# sill shadow on wall
soft_shadow(120, 548, 660, 580, (63, 37, 24), 80, 13, 3)

# curtains / rod
shape_grad_rect(70, 48, 696, 62, [(0,(72,45,31)),(0.5,(128,84,52)),(1,(64,40,28))], radius=4)
ell(62, 44, 81, 66, (135, 90, 53)); ell(685, 44, 704, 66, (135, 90, 53))

def curtain(side='left'):
    x0, x1 = (88, 212) if side == 'left' else (562, 686)
    layer = Image.new('RGBA', (CW, CH), (0,0,0,0))
    ld = ImageDraw.Draw(layer)
    pts = [(x0, 62), (x1, 62), (x1-12 if side=='left' else x1-2, 175), (x1-24 if side=='left' else x1-12, 330), (x1-8 if side=='left' else x1-26, 542), (x0+10, 542), (x0+24, 365), (x0+14, 180)]
    if side == 'right':
        pts = [(x0, 62), (x1, 62), (x1-14, 180), (x1-8, 365), (x1-20, 542), (x0+18, 542), (x0+2, 330), (x0+12, 175)]
    ld.polygon([pt(p) for p in pts], fill=(248, 233, 209, 225))
    # folds
    folds = [(x0+18, 70, x0+30, 535), (x0+45, 70, x0+36, 535), (x0+70, 70, x0+80, 535), (x0+95, 70, x0+88, 535)]
    for fx0, fy0, fx1, fy1 in folds:
        if side == 'right':
            fx0, fx1 = x1 - (fx0 - x0), x1 - (fx1 - x0)
        ld.line([pt((fx0, fy0)), pt(((fx0+fx1)/2+3, 300)), pt((fx1, fy1))], fill=(215, 191, 160, 95), width=sc(4))
        ld.line([pt((fx0+7, fy0)), pt(((fx0+fx1)/2+9, 300)), pt((fx1+7, fy1))], fill=(255, 246, 227, 95), width=sc(3))
    # hem
    ld.rectangle(box(x0+7, 532, x1-7, 546), fill=(232, 212, 182, 210))
    layer = layer.filter(ImageFilter.GaussianBlur(sc(0.5)))
    img.alpha_composite(layer)

curtain('left'); curtain('right')
# curtain rod shadow
soft_shadow(85, 62, 695, 80, (50, 30, 20), 50, 7, 4)

# ================================================================ BACKSPLASH
# zellige tile field behind counter
shape_grad_rect(0, 505, 1600, 600, [
    (0, (226, 211, 187)), (0.55, (239, 225, 202)), (1, (220, 204, 180))
], radius=0)
# tile grid
tile_h = 46
y = 504
row = 0
while y < 600:
    y2 = min(600, y + tile_h)
    offset = 0 if row % 2 == 0 else 44
    x = -44 + offset
    while x < 1600:
        x2 = min(1600, x + 88)
        tint = random.choice([(232, 220, 201), (225, 211, 190), (238, 225, 205), (220, 207, 189), (230, 217, 196)])
        rrect(x+1.2, y+1.2, x2-1.2, y2-1.2, 2, fill=tint + (255,))
        # top-left highlight
        line([(x+9, y+5), (x2-12, y+5)], (255, 246, 229, 95), 1.1)
        x += 88
    # grout
    line([(0, y), (1600, y)], (194, 178, 158, 150), 1.4)
    y += tile_h; row += 1
for x in range(0, 1610, 88):
    line([(x, 505), (x, 600)], (194, 178, 158, 70), 0.9)
# backsplash shadow under counter and glow from window
glow(390, 510, 280, 90, (255, 232, 184), 52, 24)
glow(800, 605, 800, 36, (80, 45, 28), 80, 14)

# ================================================================ COUNTER + CABINETS
# counter slab shadow on cabinets
soft_shadow(78, 620, 1180, 646, (50, 28, 18), 88, 10, 2)
# counter body
shape_grad_rect(68, 592, 1188, 630, [
    (0, (196, 139, 91)), (0.3, (218, 161, 107)), (0.58, (190, 128, 79)), (0.78, (158, 97, 58)), (1, (203, 142, 91))
], radius=2)
# top bright lip
rect(68, 592, 1188, 598, (245, 194, 141, 180))
# wood grain
for i in range(7):
    yy = 604 + i*3.2
    line([(75, yy), (1180, yy+random.uniform(-0.8,0.8))], (123, 73, 43, random.randint(30, 60)), 0.7)
# front edge
shape_grad_rect(68, 612, 1188, 632, [(0,(151, 90, 52)),(0.55,(124, 71, 42)),(1,(167, 102, 59))], radius=2)
rect(68, 630, 1188, 634, (83, 47, 29, 120))

# cabinet base fill
shape_grad_rect(86, 632, 1176, 854, [
    (0, (137, 148, 112)), (0.35, (119, 132, 98)), (0.8, (103, 117, 85)), (1, (86, 98, 71))
], radius=0)
# left and right shade
glow(95, 745, 85, 180, (45, 51, 34), 68, 30)
glow(1170, 745, 95, 180, (45, 51, 34), 75, 30)
# cabinet panel layout
sections = [(96, 264), (274, 512), (522, 698), (708, 924), (934, 1166)]
for i, (x0, x1) in enumerate(sections):
    # stile shadow/gap
    rect(x0-7, 636, x0-1, 841, (66, 78, 54, 90))
    rect(x0, 636, x0+3, 841, (157, 167, 128, 75))
    # drawers
    if i in (0,1,2,3,4):
        rrect(x0+16, 645, x1-16, 691, 4, fill=None, outline=(60, 73, 50, 130), width=2)
        rrect(x0+18, 647, x1-18, 689, 3, fill=None, outline=(174, 183, 143, 55), width=1)
    # doors
    door_top = 700
    if i in (0,2,3,4):
        rrect(x0+16, door_top, x1-16, 824, 5, fill=None, outline=(61, 74, 51, 150), width=2)
        rrect(x0+20, door_top+5, x1-20, 819, 5, fill=None, outline=(176, 186, 145, 50), width=1)
    # lower shadow
    rect(x0+8, 826, x1-8, 843, (58, 69, 48, 80))
# sink section: two fake drawers? no, apron covers
# toe kick
rect(86, 840, 1176, 858, (66, 47, 34))
rect(86, 840, 1176, 845, (49, 34, 25, 150))
for i in range(13):
    x = 100 + i*84
    line([(x, 848), (x+20, 848)], (108, 79, 57, 70), 1)

# brass hardware
def cup_pull(cx, cy, w=34, color=(197, 151, 73)):
    lw = sc(4.2)
    d.line([pt((cx-w/2, cy)), pt((cx-w/2, cy+7)), pt((cx+w/2, cy+7)), pt((cx+w/2, cy))], fill=color, width=lw, joint='curve')
    ell(cx-w/2-3, cy-3, cx-w/2+3, cy+3, fill=color)
    ell(cx+w/2-3, cy-3, cx+w/2+3, cy+3, fill=color)
    line([(cx-w/2+2, cy+2), (cx+w/2-2, cy+2)], (245, 206, 128, 150), 1)

def knob(cx, cy, r=5):
    ell(cx-r, cy-r, cx+r, cy+r, fill=(198, 151, 70), outline=(105, 71, 30, 150), width=0.7)
    ell(cx-r*0.55, cy-r*0.7, cx-r*0.05, cy-r*0.15, fill=(247, 211, 139, 180))

for idx, (x0, x1) in enumerate(sections):
    cx = (x0+x1)/2
    if idx in (0,2,3,4):
        cup_pull(cx, 674)
    if idx in (0,2,3,4):
        knob(x0+31, 762)
        knob(x1-31, 762)
# add wood knobs on drawers? brass okay

# cabinet subtle vignette
glow(630, 860, 640, 35, (44, 35, 22), 80, 14)
glow(86, 650, 90, 30, (53, 39, 24), 60, 18)
glow(1176, 650, 80, 30, (48, 35, 22), 60, 18)

# ================================================================ SINK + FAUCET
# farmhouse sink cut into cabinets
soft_shadow(258, 628, 530, 784, (47, 28, 18), 100, 10, 5)
shape_grad_rect(278, 635, 512, 780, [
    (0, (246, 238, 222)), (0.16, (232, 223, 205)), (0.62, (224, 213, 194)), (0.88, (213, 201, 181)), (1, (192, 179, 157))
], radius=9)
rrect(285, 641, 505, 772, 8, outline=(181, 166, 142, 170), width=1.5)
# panel grooves
for x in [307, 337, 367, 397, 427, 457, 487]:
    line([(x, 654), (x, 760)], (181, 166, 145, 55), 1)
# basin rim seen at top
rrect(304, 634, 486, 656, 13, fill=(247, 242, 230), outline=(163, 148, 126, 120), width=1.2)
rrect(313, 638, 477, 651, 10, fill=(130, 129, 116))
rrect(316, 640, 474, 647, 7, fill=(82, 85, 79))
# highlight on rim
line([(313, 640), (474, 640)], (255, 252, 237, 170), 1.3)
# side shadows
glow(280, 708, 24, 75, (75, 56, 40), 80, 7)
glow(510, 708, 24, 75, (75, 56, 40), 80, 7)

# bridge faucet (brass)
fc = (177, 122, 60)
fcd = (119, 77, 37)
fcl = (236, 183, 102)
# bases
for bx in [350, 442]:
    rrect(bx-16, 620, bx+16, 632, 4, fill=(153, 105, 52), outline=(95, 59, 27, 110), width=1)
    ell(bx-11, 620, bx+11, 625, fill=(207, 157, 86))
# verticals + handles
for bx in [350, 442]:
    line([(bx, 622), (bx, 606)], fc, 7)
    line([(bx-4, 622), (bx-4, 608)], fcl, 1.2)
    # handle cross
    line([(bx-18, 603), (bx+18, 603)], fcd, 4)
    ell(bx-20, 600, bx-15, 607, fill=(219, 169, 91)); ell(bx+15, 600, bx+20, 607, fill=(219, 169, 91))
# arch spout
pts = bezier([(396, 620), (396, 552), (351, 535), (352, 583)], 70)
d.line([pt(p) for p in pts], fill=fcd, width=sc(9), joint='curve')
d.line([pt((p[0]-1.5, p[1])) for p in pts], fill=fcl, width=sc(2.2), joint='curve')
# spout tip
rrect(343, 581, 360, 592, 3, fill=(139, 93, 45))
ell(344, 588, 359, 594, fill=(111, 73, 34))
# highlight glints
ell(392, 573, 399, 580, fill=(255, 225, 158, 185))
line([(347, 539), (359, 548)], (255, 229, 168, 140), 1.3)

# soap bottle at sink right
rrect(511, 565, 548, 613, 6, fill=(151, 164, 129), outline=(91, 105, 76, 100), width=1)
rrect(521, 550, 538, 570, 3, fill=(112, 85, 52))
line([(521, 548), (538, 548)], (81, 59, 37), 4)
line([(518, 579), (536, 574)], (229, 231, 197, 65), 3)
# dish brush in little cup
rrect(250, 570, 275, 614, 4, fill=(214, 199, 173), outline=(157, 139, 113, 100), width=1)
line([(260, 571), (256, 537)], (151, 116, 79), 3)
ell(250, 530, 264, 544, fill=(166, 144, 106))

# towel draped on sink edge
shape_shadow([(486, 618), (555, 618), (545, 700), (515, 724), (490, 692)], (49,30,18), 80, 8)
pts = [(486, 617), (552, 617), (546, 691), (522, 720), (506, 697), (492, 690)]
d.polygon([pt(p) for p in pts], fill=(205, 211, 183))
d.line([pt(p) for p in pts] + [pt(pts[0])], fill=(151, 161, 132), width=sc(1.4), joint='curve')
line([(491, 633), (548, 633)], (169, 180, 151), 4)
line([(500, 647), (543, 647)], (169, 180, 151), 2)
line([(497, 660), (540, 660)], (169, 180, 151), 2)
# folds
line([(510, 620), (512, 688)], (158, 168, 139, 120), 1.2)
line([(528, 620), (526, 690)], (244, 246, 223, 100), 1.2)
# fringe
for i in range(7):
    x = 506 + i*5
    line([(x, 699+random.uniform(-2,2)), (x+random.uniform(-2,2), 716+random.uniform(-4,2))], (223, 226, 200), 1)

# ================================================================ RANGE
# shadow from range
soft_shadow(1158, 585, 1492, 868, (46, 27, 17), 100, 13, 5)
# body
shape_grad_rect(1168, 590, 1484, 854, [
    (0, (245, 235, 216)), (0.12, (235, 223, 202)), (0.68, (224, 210, 187)), (0.9, (207, 191, 168)), (1, (183, 168, 145))
], radius=7)
# side shading
glow(1178, 745, 40, 150, (100, 80, 60), 60, 16)
glow(1474, 745, 40, 150, (100, 80, 60), 60, 16)
# backguard
shape_grad_rect(1184, 510, 1468, 596, [
    (0, (244, 234, 216)), (0.55, (230, 217, 195)), (1, (209, 194, 171))
], radius=5)
rrect(1196, 522, 1456, 564, 4, outline=(177, 162, 139, 100), width=1.2)
# knobs on backguard
for i, x in enumerate([1225, 1270, 1315, 1360, 1405, 1445]):
    ell(x-8, 532, x+8, 548, fill=(62, 58, 50), outline=(189, 170, 140, 120), width=1)
    ell(x-4, 535, x+3, 542, fill=(115, 108, 95))
    line([(x, 536), (x, 543)], (226, 211, 184), 1)
# brass rail
line([(1202, 573), (1450, 573)], (188, 144, 71), 3)
for x in [1205, 1447]: ell(x-5, 568, x+5, 578, fill=(204, 158, 82))
# cooktop
shape_grad_rect(1168, 584, 1484, 612, [
    (0, (65, 64, 60)), (0.32, (91, 88, 80)), (1, (42, 43, 40))
], radius=3)
# burner rings
for x in [1232, 1415]:
    ell(x-53, 585, x+53, 600, fill=None, outline=(122, 120, 110), width=2)
    ell(x-37, 587, x+37, 597, fill=None, outline=(82, 81, 75), width=1)
    # grates
    for k in range(-2, 3):
        line([(x+k*18, 583), (x+k*18, 603)], (33, 34, 32), 2)
# oven door
rrect(1198, 641, 1454, 820, 10, fill=None, outline=(167, 151, 126, 150), width=2)
rrect(1210, 652, 1442, 809, 8, fill=None, outline=(251, 242, 222, 90), width=1)
# oven glass
rrect(1230, 672, 1422, 760, 8, fill=(72, 66, 57))
rrect(1237, 678, 1415, 753, 7, fill=(52, 51, 46))
# glass reflection
line([(1250, 690), (1300, 742)], (255, 227, 173, 36), 20)
line([(1310, 685), (1355, 728)], (255, 237, 194, 27), 9)
# handle bar
rrect(1228, 776, 1424, 787, 5, fill=(177, 134, 69), outline=(112, 76, 34, 120), width=1)
line([(1235, 778), (1418, 778)], (251, 207, 123, 130), 1.4)
# feet
for x in [1188, 1464]:
    rrect(x-12, 846, x+12, 872, 4, fill=(91, 83, 69))
    ell(x-14, 866, x+14, 876, fill=(65, 58, 49))

# kettle
soft_shadow(1224, 584, 1378, 604, (28,20,16), 140, 8, 4)
# handle
arc(1226, 455, 1375, 578, 185, 355, (80, 52, 31), 12)
arc(1229, 458, 1372, 575, 186, 354, (166, 110, 65), 5)
arc(1233, 463, 1368, 571, 190, 350, (236, 163, 98), 1.4)
# body
shape_grad_rect(1245, 490, 1356, 594, [
    (0, (226, 151, 91)), (0.2, (194, 113, 64)), (0.5, (178, 94, 52)), (0.82, (143, 72, 41)), (1, (112, 54, 32))
], radius=28)
# body highlight
arc(1252, 495, 1349, 589, 185, 335, (255, 200, 139, 130), 3)
ell(1265, 505, 1303, 557, fill=(248, 181, 119, 40))
# base rim
rrect(1242, 582, 1359, 596, 8, fill=(105, 58, 35), outline=(68, 37, 23, 120), width=1)
line([(1250, 585), (1351, 585)], (223, 154, 95, 115), 1.5)
# lid
ell(1260, 476, 1340, 500, fill=(199, 119, 66), outline=(117, 61, 36, 150), width=1.4)
ell(1275, 480, 1325, 492, fill=(238, 171, 107))
# lid knob
ell(1291, 467, 1309, 483, fill=(90, 56, 35))
ell(1294, 469, 1303, 476, fill=(216, 161, 102, 150))
# spout
sp = [(1350, 538), (1382, 520), (1388, 505), (1400, 508), (1392, 528), (1360, 558)]
poly(sp, fill=(164, 90, 49), outline=(102, 52, 31, 120), width=1)
poly([(1356, 540), (1384, 517), (1392, 510), (1393, 516), (1362, 548)], fill=(228, 147, 86, 150))
# side highlight
line([(1250, 525), (1250, 572)], (255, 206, 145, 130), 2)
# steam
steam_layer = Image.new('RGBA', (CW, CH), (0,0,0,0))
sdw = ImageDraw.Draw(steam_layer)
for j in range(3):
    pts = bezier([(1300+j*9, 466), (1278+j*8, 420), (1322+j*9, 374), (1295+j*8, 322)], 50)
    sdw.line([pt(p) for p in pts], fill=(255, 248, 231, 88), width=sc(3.4-j*0.4), joint='curve')
steam_layer = steam_layer.filter(ImageFilter.GaussianBlur(sc(4)))
img.alpha_composite(steam_layer)

# towel on range handle
soft_shadow(1280, 780, 1380, 845, (44, 26, 17), 65, 7, 2)
shape_grad_rect(1278, 784, 1378, 852, [(0,(192, 169, 137)),(0.5,(176, 152, 122)),(1,(151, 129, 102))], radius=4)
for x in [1291, 1314, 1337, 1360]:
    line([(x, 790), (x-2, 846)], (228, 209, 177, 55), 2)
line([(1284, 806), (1372, 806)], (202, 183, 151, 150), 2)
line([(1284, 812), (1372, 812)], (145, 124, 98, 110), 1)

# ================================================================ WALL DECOR
# framed botanical print
soft_shadow(675, 135, 846, 315, (52, 31, 20), 85, 12, 4)
shape_grad_rect(678, 132, 844, 310, [
    (0, (136, 89, 55)), (0.35, (161, 106, 64)), (0.75, (137, 86, 52)), (1, (104, 63, 39))
], radius=2)
rect(690, 144, 832, 298, (246, 238, 219))
rect(690, 144, 832, 298, outline=(207, 191, 162, 110), width=1)
# botanical stems
for base_x, top_x, top_y, color in [(728, 716, 172, (114, 132, 91)), (770, 784, 166, (131, 148, 100)), (752, 748, 158, (94, 117, 79))]:
    pts = bezier([(base_x, 286), (base_x+8, 250), (top_x-6, 205), (top_x, top_y)], 40)
    line(pts, color, 1.7)
    for t in [0.22,0.4,0.58,0.74]:
        idx = int(t*(len(pts)-1)); x,y = pts[idx]
        ell(x-9, y-4, x+8, y+4, fill=color)
# berries
for x,y in [(723, 214),(739, 231),(780, 221),(792, 241),(757, 252)]:
    ell(x-3.2, y-3.2, x+3.2, y+3.2, fill=(193, 111, 67))
# frame highlight
line([(684, 138), (838, 138)], (219, 157, 105, 80), 1.2)
line([(684, 138), (684, 304)], (219, 157, 105, 60), 1)

# pendant lamp
# cord shadow then cord
line([(892, 58), (892, 212)], (67, 48, 33, 150), 2.2)
line([(891, 58), (891, 214)], (157, 121, 82), 1.3)
# warm halo
glow(892, 238, 230, 185, (255, 203, 120), 60, 40)
# shade
poly([(850, 262), (934, 262), (914, 210), (870, 210)], fill=(169, 95, 58), outline=(103, 52, 32, 160), width=1.2)
poly([(857, 257), (927, 257), (910, 216), (874, 216)], fill=(197, 117, 69))
# ribs / highlight
line([(874, 215), (859, 256)], (236, 157, 97, 75), 1.1)
line([(887, 214), (878, 257)], (110, 55, 33, 60), 2)
line([(903, 213), (906, 257)], (235, 156, 101, 55), 1.3)
# rim
rrect(846, 257, 938, 267, 5, fill=(102, 55, 33), outline=(62, 34, 22, 130), width=1)
line([(851, 259), (933, 259)], (235, 166, 106, 95), 1.4)
# bulb socket & bulb
rrect(885, 263, 899, 279, 3, fill=(123, 88, 53))
ell(881, 273, 903, 297, fill=(255, 226, 158, 235))
ell(886, 276, 898, 291, fill=(255, 246, 202, 230))
glow(892, 287, 85, 85, (255, 220, 143), 100, 18)

# floating shelf unit (right)
# shadow on wall
soft_shadow(1020, 245, 1454, 278, (52, 31, 20), 65, 14, 3)
soft_shadow(1020, 373, 1454, 406, (52, 31, 20), 65, 14, 3)
# brackets
for x in [1060, 1414]:
    poly([(x-9, 262), (x+9, 262), (x+2, 286), (x-3, 286)], fill=(92, 60, 40))
    poly([(x-9, 390), (x+9, 390), (x+2, 414), (x-3, 414)], fill=(92, 60, 40))
# shelves
shape_grad_rect(1022, 256, 1448, 276, [
    (0, (174, 116, 73)), (0.3, (203, 145, 95)), (0.8, (156, 96, 58)), (1, (114, 68, 43))
], radius=2)
shape_grad_rect(1022, 384, 1448, 404, [
    (0, (174, 116, 73)), (0.3, (203, 145, 95)), (0.8, (156, 96, 58)), (1, (114, 68, 43))
], radius=2)
rect(1022, 256, 1448, 259, (240, 185, 128, 90))
rect(1022, 384, 1448, 387, (240, 185, 128, 90))
rect(1022, 274, 1448, 278, (81, 48, 30, 150))
rect(1022, 402, 1448, 406, (81, 48, 30, 150))

# shelf objects: plates
for i, ww in enumerate([70, 62, 54]):
    y = 248 - i*13
    ell(1064, y-8, 1064+ww, y+8, fill=(240, 231, 214), outline=(183, 164, 139, 100), width=1)
    ell(1071, y-4, 1064+ww-7, y+3, fill=None, outline=(154, 169, 137, 95), width=1.2)
# jar with pasta
rrect(1150, 199, 1203, 256, 5, fill=(213, 222, 204, 215), outline=(135, 151, 121, 100), width=1)
rrect(1156, 213, 1197, 253, 4, fill=(203, 170, 111))
for i in range(20):
    x = random.uniform(1158, 1195); y = random.uniform(216, 250)
    line([(x, y), (x+random.uniform(-6,6), y+random.uniform(-8,8))], (168, 128, 76, 160), 0.7)
rrect(1150, 192, 1203, 206, 4, fill=(176, 122, 74))
# small pitcher
rrect(1232, 211, 1282, 257, 9, fill=(223, 211, 186), outline=(165, 147, 119, 100), width=1)
arc(1276, 220, 1303, 248, 270, 90, (184, 164, 133), 5)
line([(1238, 219), (1276, 219)], (249, 239, 217, 95), 2)
# plant pot / trailing vine
rrect(1322, 214, 1378, 258, 7, fill=(184, 107, 66), outline=(122, 66, 40, 100), width=1)
rrect(1318, 207, 1382, 219, 4, fill=(199, 122, 77))
# leaves
for i in range(22):
    t = i/21
    x = 1350 + math.sin(t*5.8)*42 + random.uniform(-7,7)
    y = 224 - t*20 + t*105 if t > 0.25 else 220
    if i < 10:
        x = 1335 + random.uniform(-13, 13); y = 212 - random.uniform(0,28)
    ell(x-7, y-3.3, x+7, y+3.3, fill=random.choice([(91, 120, 78),(112, 140, 92),(76, 103, 70)]))
# trailing stem
pts = bezier([(1350, 217), (1392, 242), (1380, 312), (1372, 376)], 50)
line(pts, (89, 113, 72), 1.4)

# lower shelf: bowls
for i, ww in enumerate([64, 53, 42]):
    y = 371 - i*13
    rrect(1060+(64-ww)/2, y-10, 1060+(64+ww)/2, y+4, ww/3, fill=(226, 214, 192), outline=(171, 152, 126, 95), width=1)
    arc(1060+(64-ww)/2+2, y-14, 1060+(64+ww)/2-2, y+3, 180, 360, (247, 238, 219), 1.5)
# copper canister
rrect(1158, 319, 1212, 384, 7, fill=(181, 108, 62), outline=(112, 60, 34, 100), width=1)
rrect(1153, 312, 1217, 325, 4, fill=(134, 78, 44))
line([(1164, 332), (1164, 374)], (241, 178, 112, 110), 2)
# glass jars
rrect(1230, 324, 1284, 384, 5, fill=(207, 216, 198, 210), outline=(138, 151, 126, 95), width=1)
rrect(1235, 332, 1279, 377, 4, fill=(201, 172, 121))
rrect(1234, 314, 1280, 326, 4, fill=(155, 132, 100))
rrect(1300, 335, 1354, 384, 5, fill=(209, 217, 201, 200), outline=(137, 150, 124, 90), width=1)
rrect(1305, 342, 1349, 378, 4, fill=(190, 128, 79))
rrect(1304, 326, 1350, 337, 4, fill=(159, 135, 102))
# small ceramic cup with utensils
rrect(1380, 344, 1418, 384, 5, fill=(213, 202, 180), outline=(161, 143, 117, 95), width=1)
for i,x in enumerate([1386, 1394, 1402, 1410]):
    line([(x, 346), (x+random.uniform(-8,8), 306+random.uniform(-8,8))], (147, 112, 76), 2)

# hanging mugs under shelf
for x, c in [(1070, (200, 124, 80)), (1118, (219, 210, 193)), (1166, (159, 173, 140))]:
    line([(x, 404), (x, 437)], (117, 88, 61), 1.3)
    # handle
    arc(x+11, 448, x+27, 470, 270, 90, shade(c,0.72), 3)
    # body
    rrect(x-13, 437, x+13, 479, 5, fill=c, outline=shade(c,0.70), width=1)
    ell(x-13, 435, x+13, 446, fill=shade(c,0.52))
    ell(x-9, 437, x+9, 444, fill=shade(c,0.38))
    ell(x-10, 471, x+10, 482, fill=shade(c,0.86))
    line([(x-9, 450), (x-9, 469)], shade(c,1.24), 1.1)
    line([(x-3, 448), (x-3, 472)], shade(c,1.12), 0.8)
    ell(x-2, 438, x+3, 442, fill=(255, 246, 222, 130))

# ================================================================ COUNTER ITEMS
# little herb pot
soft_shadow(233, 606, 295, 625, (46,26,17), 85, 6, 5)
rrect(236, 566, 292, 613, 7, fill=(185, 106, 65), outline=(120, 63, 38, 115), width=1.2)
rrect(231, 560, 297, 574, 4, fill=(198, 118, 74))
line([(242, 576), (242, 604)], (233, 148, 93, 90), 1.4)
# leaves / basil
stems = [((264, 565),(245, 527),(236, 509)), ((264,565),(272,520),(286,500)), ((264,565),(264,515),(259,489)), ((264,565),(284,535),(299,522)), ((264,565),(247,545),(224,540))]
for a,b,c in stems:
    pts = bezier([a,b,c], 34)
    line(pts, (86, 113, 72), 1.8)
    for t in [0.35,0.62,0.84]:
        x,y = pts[int(t*(len(pts)-1))]
        ell(x-10, y-5, x+9, y+5, fill=random.choice([(82, 111, 70),(103, 130, 82),(67, 96, 61)]))
        ell(x-2, y-1, x+2, y+2, fill=(151, 168, 113, 100))

# flower jug on the left, catching the window light
def draw_flower_jug(cx=172, base_y=613):
    vase_w = 72
    x0, x1 = cx-vase_w/2, cx+vase_w/2
    soft_shadow(x0-8, base_y-21, x1+22, base_y+13, (48,27,18), 95, 8, 6)
    flowers = []
    # stems first
    for i in range(11):
        fx = cx + random.uniform(-43, 37)
        fy = 425 + random.uniform(-50, 42)
        flowers.append((fx, fy, random.choice([(238, 223, 191),(241, 237, 221),(221, 158, 126),(226, 181, 83),(174, 184, 147),(216, 175, 190)])))
        pts = bezier([(cx+7, base_y-35), (cx+random.uniform(-15,18), 532), (fx+random.uniform(-10,10), 486), (fx, fy)], 42)
        line(pts, (89, 116, 70), 1.7)
        for t in [0.22, 0.45, 0.66]:
            x,y = pts[int(t*(len(pts)-1))]
            side = 1 if random.random() > 0.5 else -1
            ell(x + (0 if side>0 else -14), y-3.7, x + (10 if side>0 else -4), y+3.7, fill=(99, 125, 78))
    # jug body
    shape_grad_rect(x0, 535, x1, base_y, [
        (0, (245, 235, 216)), (0.25, (230, 217, 194)), (0.7, (211, 195, 169)), (1, (179, 161, 135))
    ], radius=11)
    # handle (small, so it clears the herb pot)
    arc(x1-4, 543, x1+22, 587, 270, 90, (195, 178, 150), 5)
    arc(x1-2, 546, x1+18, 584, 272, 88, (246, 238, 218), 1.4)
    line([(x0+10, 546), (x1-6, 546)], (255, 248, 229, 140), 2)
    line([(x0+11, 565), (x1-9, 565)], (158, 175, 143), 3)
    line([(x0+11, 572), (x1-9, 572)], (158, 175, 143), 1.2)
    # flowers
    for fx, fy, c in flowers:
        for k in range(5):
            a = k*math.tau/5 + random.uniform(-0.2,0.2)
            ex = fx + math.cos(a)*8.3; ey = fy + math.sin(a)*6.3
            ell(ex-5.8, ey-3.8, ex+5.8, ey+3.8, fill=c, outline=shade(c,0.9), width=0.4)
        ell(fx-3.4, fy-3, fx+3.4, fy+3, fill=(210, 154, 66))
    # lavender sprigs
    for i in range(3):
        x0l = cx - 14 + i*12
        pts = bezier([(cx+2, 570), (x0l, 512), (x0l-7, 478), (x0l-2, 452)], 30)
        line(pts, (104, 122, 81), 1.2)
        for t in [0.68,0.75,0.82,0.89,0.96]:
            x,y = pts[int(t*(len(pts)-1))]
            ell(x-3.2, y-2.3, x+3.2, y+2.3, fill=(146, 133, 168))

draw_flower_jug(172)

# bread board + sourdough loaf
soft_shadow(642, 598, 837, 624, (47,27,18), 90, 8, 7)
shape_grad_rect(645, 580, 835, 616, [
    (0, (211, 154, 99)), (0.4, (193, 135, 82)), (1, (147, 92, 51))
], radius=12)
line([(655, 593), (820, 593)], (231, 176, 119, 65), 1.4)
# board handle hole
ell(655, 590, 668, 603, fill=(124, 76, 44))
# loaf shadow
soft_shadow(679, 538, 801, 592, (52, 26, 15), 90, 8, 13)
# loaf
shape_grad_rect(680, 535, 802, 592, [
    (0, (211, 157, 92)), (0.25, (190, 127, 65)), (0.72, (164, 99, 48)), (1, (128, 72, 35))
], radius=26)
# flour dust and scoring
for i in range(8):
    x = random.uniform(688, 794); y = random.uniform(540, 580)
    ell(x-3, y-2, x+3, y+2, fill=(244, 224, 188, random.randint(35,80)))
for q in [[(705,556),(724,544),(742,552)], [(748,544),(770,535),(790,548)], [(719,566),(742,557),(768,568)]]:
    pts = bezier(q, 30)
    line(pts, (240, 212, 165, 150), 2.3)
# loaf highlight
arc(687, 540, 793, 589, 188, 332, (248, 195, 129, 105), 3)
# crumbs and a little spilled flour
for _ in range(14):
    x = random.uniform(668, 860); y = random.uniform(603, 618)
    ell(x-1.2, y-0.8, x+1.2, y+0.8, fill=(142, 94, 55, random.randint(45,110)))
for _ in range(6):
    x = random.uniform(700, 795); y = random.uniform(598, 611)
    ell(x-1, y-0.8, x+1, y+0.8, fill=(244, 225, 190, random.randint(80,150)))

# small butter dish
soft_shadow(817, 593, 862, 613, (47,26,15), 80, 5, 4)
rrect(817, 572, 862, 607, 5, fill=(230, 221, 203), outline=(177, 160, 135, 90), width=1)
rrect(821, 564, 858, 576, 4, fill=(239, 231, 215))
line([(823, 578), (855, 578)], (251, 243, 225, 120), 1)

# bowl of oranges
soft_shadow(848, 593, 994, 622, (50,28,16), 95, 9, 8)
# oranges behind rim
for x,y,r in [(893,570,23),(930,566,20),(960,579,18)]:
    ell(x-r, y-r, x+r, y+r, fill=(225, 132, 48), outline=(160, 83, 26, 80), width=1)
    ell(x-r*0.55, y-r*0.7, x+r*0.15, y-r*0.1, fill=(247, 176, 91, 120))
    ell(x-2, y-r-2, x+2, y-r+2, fill=(99, 117, 62))
# bowl body
shape_grad_rect(850, 563, 994, 616, [
    (0, (224, 209, 183)), (0.2, (213, 195, 166)), (0.7, (189, 170, 140)), (1, (159, 139, 110))
], radius=28)
# bowl opening ellipse
ell(857, 552, 987, 579, fill=(92, 99, 80))
ell(862, 554, 982, 575, fill=(142, 144, 114))
# front rim highlight
arc(852, 563, 992, 617, 14, 166, (239, 227, 205), 5)
arc(856, 568, 988, 612, 20, 160, (119, 153, 141), 2.2)
# orange fronts above rim
for x,y,r in [(884,566,21),(918,562,22),(952,573,18)]:
    ell(x-r, y-r, x+r, y+r, fill=(231, 138, 50))
    ell(x-r*0.5, y-r*0.7, x+r*0.25, y-r*0.1, fill=(251, 183, 98, 130))
    ell(x-2, y-r-1, x+2, y-r+3, fill=(93, 112, 60))
# bowl design dots
for i in range(9):
    x = 874 + i*12
    ell(x-2, 595, x+2, 599, fill=(116, 146, 130, 120))

# coffee mug + saucer
soft_shadow(1000, 596, 1088, 623, (49,27,16), 95, 7, 6)
ell(997, 602, 1088, 619, fill=(211, 191, 165), outline=(158, 136, 108, 100), width=1)
ell(1008, 604, 1077, 615, fill=(231, 218, 198))
# handle
arc(1048, 548, 1094, 593, 270, 90, (218, 205, 182), 8)
arc(1051, 551, 1090, 590, 272, 88, (249, 239, 220), 1.5)
# mug body
shape_grad_rect(1005, 548, 1072, 607, [
    (0, (243, 233, 214)), (0.3, (231, 218, 197)), (0.75, (218, 202, 177)), (1, (192, 175, 149))
], radius=8)
# coffee
ell(1011, 543, 1067, 558, fill=(230, 216, 194))
ell(1015, 545, 1063, 555, fill=(95, 55, 32))
ell(1021, 546, 1046, 552, fill=(130, 79, 45, 120))
# mug lip
arc(1006, 546, 1071, 560, 0, 180, (251, 243, 225), 2.4)
# little blue stripe
line([(1009, 574), (1069, 574)], (116, 138, 127), 5)
line([(1010, 581), (1068, 581)], (174, 188, 170), 1.5)
# steam
steam = Image.new('RGBA', (CW, CH), (0,0,0,0))
sdd = ImageDraw.Draw(steam)
for j in range(2):
    pts = bezier([(1028+j*16, 536), (1008+j*12, 492), (1055+j*8, 457), (1035+j*12, 418)], 45)
    sdd.line([pt(p) for p in pts], fill=(255, 249, 233, 72), width=sc(2.4), joint='curve')
steam = steam.filter(ImageFilter.GaussianBlur(sc(3.5)))
img.alpha_composite(steam)

# jam jar
soft_shadow(1094, 594, 1148, 616, (48,27,16), 80, 6, 5)
rrect(1096, 556, 1145, 607, 6, fill=(205, 157, 94, 235), outline=(147, 101, 53, 100), width=1)
rrect(1102, 563, 1139, 601, 4, fill=(175, 73, 47))
# label
rrect(1104, 576, 1137, 596, 2, fill=(239, 230, 208))
line([(1108, 581), (1133, 581)], (160, 123, 80), 1)
line([(1112, 586), (1129, 586)], (183, 149, 104), 1)
# lid
rrect(1093, 547, 1148, 560, 4, fill=(177, 126, 74))
for x in range(1098, 1145, 6):
    line([(x, 549), (x, 558)], (120, 80, 43, 100), 1)
# glass glint
line([(1101, 566), (1101, 598)], (249, 219, 169, 120), 1.4)

# small open notebook / letter at center-left
soft_shadow(665, 592, 790, 618, (47,27,17), 55, 6, 4)
poly([(668, 604), (725, 593), (786, 599), (728, 613)], fill=(231, 221, 199), outline=(182, 165, 139, 90), width=1)
poly([(668, 604), (725, 593), (724, 601), (669, 611)], fill=(246, 238, 221))
line([(680, 604), (715, 598)], (176, 159, 134, 90), 1)
line([(678, 607), (709, 602)], (186, 170, 144, 75), 1)
# sprig on notebook
line([(735, 605), (755, 594)], (100, 122, 79), 1.2)
for x,y in [(742,600),(749,597),(756,594)]:
    ell(x-4, y-2, x+4, y+2, fill=(111, 132, 86))

# ================================================================ CAT ON SILL
# cat curled, sleeping in the sun
soft_shadow(438, 495, 604, 526, (54,31,20), 100, 9, 7)
# tail curling around front
tail_pts = bezier([(577, 497), (605, 506), (591, 523), (550, 520), (513, 517)], 60)
d.line([pt(p) for p in tail_pts], fill=(169, 90, 48), width=sc(13), joint='curve')
d.line([pt((p[0], p[1]-2)) for p in tail_pts], fill=(212, 131, 76), width=sc(3.5), joint='curve')
# body
ell(462, 468, 596, 520, fill=(201, 113, 62), outline=(140, 72, 37, 150), width=1.5)
# haunch
ell(522, 473, 596, 520, fill=(188, 101, 54))
# stripes
for x0,y0,x1,y1 in [(535,478,552,510),(553,475,568,512),(571,479,586,511),(500,477,512,513),(480,484,490,515)]:
    pts = bezier([(x0,y0),(x0-3,(y0+y1)/2),(x1,y1)], 20)
    line(pts, (157, 79, 40, 100), 3.2)
# head
ell(432, 469, 501, 520, fill=(210, 122, 69), outline=(140, 72, 37, 150), width=1.4)
# ears
poly([(438, 481), (440, 451), (458, 469)], fill=(205, 117, 64), outline=(137, 69, 35, 150), width=1)
poly([(475, 468), (493, 450), (492, 482)], fill=(205, 117, 64), outline=(137, 69, 35, 150), width=1)
poly([(443, 476), (445, 459), (455, 470)], fill=(223, 145, 101))
poly([(480, 468), (490, 457), (489, 475)], fill=(223, 145, 101))
# head stripes
for q in [[(457,473),(460,484),(456,494)],[(469,470),(472,482),(469,492)]]:
    line(bezier(q, 18), (157, 79, 40, 120), 2.2)
# muzzle
ell(455, 493, 486, 516, fill=(229, 155, 105))
ell(459, 495, 482, 504, fill=(241, 180, 126, 170))
# closed eyes
arc(446, 486, 461, 496, 10, 170, (86, 53, 35), 1.8)
arc(473, 486, 488, 496, 10, 170, (86, 53, 35), 1.8)
# nose
poly([(463, 501), (472, 501), (467.5, 507)], fill=(155, 80, 67))
# mouth
arc(459, 500, 476, 514, 20, 160, (128, 70, 48), 1)
# whiskers
for dy in [-1,2,5]:
    line([(457, 504+dy*0.2), (436, 501+dy)], (255, 236, 207, 130), 0.9)
    line([(477, 504+dy*0.2), (497, 501+dy)], (255, 236, 207, 130), 0.9)
# paws tucked
ell(491, 502, 526, 520, fill=(215, 131, 78))
ell(477, 505, 508, 520, fill=(222, 137, 82))
for x in [492, 505, 518]:
    line([(x, 510), (x+1, 516)], (154, 82, 47, 100), 1)
# rim light from window on cat back/head
arc(440, 465, 596, 520, 185, 340, (255, 206, 130, 150), 3)
arc(432, 466, 502, 520, 185, 310, (255, 218, 153, 130), 2.2)
# fur strokes
for i in range(18):
    x = random.uniform(465, 590); y = random.uniform(476, 512)
    line([(x,y), (x+random.uniform(-5,5), y+random.uniform(2,5))], (157, 81, 42, 55), 0.8)

# ================================================================ RUG
# woven runner on floor in front of sink
soft_shadow(250, 868, 810, 995, (60,31,19), 120, 13, 8)
poly([(268, 886), (792, 878), (816, 982), (249, 992)], fill=(142, 82, 62))
# inner bands
for i,(off,col) in enumerate([(18,(188,165,132)),(34,(113,74,59)),(46,(213,196,166)),(64,(120,83,67)),(78,(181,160,129))]):
    poly([(268+off*0.45, 886+off*0.9), (792-off*0.3, 878+off*0.9), (792-off*0.2, 878+off*0.9+4), (268+off*0.45, 886+off*0.9+4)], fill=col)
# main cream band and stripes
poly([(298, 910), (765, 902), (772, 928), (292, 936)], fill=(204, 188, 159))
poly([(304, 916), (758, 909), (760, 913), (303, 920)], fill=(105, 120, 111))
poly([(306, 927), (755, 920), (755, 923), (306, 930)], fill=(120, 77, 62))
# simple diamonds
for i in range(8):
    x = 330 + i*56; y = 950 + (i%2)*6
    poly([(x,y-8),(x+10,y),(x,y+8),(x-10,y)], fill=(118,76,60))
    poly([(x,y-3),(x+4,y),(x,y+3),(x-4,y)], fill=(217,200,170))
# weave texture
for i in range(32):
    y = 892 + i*3
    line([(266+((y-886)*0.17), y), (799-((y-878)*0.08), y-4)], (98, 49, 31, 22), 0.7)
# fringe left/right
for side, x0, x1 in [('left', 250, 275), ('right', 790, 822)]:
    for i in range(18):
        yy = 894 + i*5.4
        line([(x0+random.uniform(-4,4), yy), (x1+random.uniform(-6,6), yy+random.uniform(-3,3))], (225, 205, 172, 170), 1.2)
# rug edge highlight
line([(268, 887), (792, 879)], (239, 203, 159, 60), 1.4)

# ================================================================ LIGHT & ATMOSPHERE
# light pool on counter from window
glow(330, 594, 290, 54, (255, 231, 166), 75, 22)
glow(590, 585, 170, 60, (255, 230, 164), 38, 25)
# warm bounce on cabinets
glow(360, 700, 250, 130, (255, 207, 128), 24, 35)
# floor sun pool
glow(540, 900, 330, 120, (255, 212, 132), 42, 40)
glow(760, 920, 220, 90, (255, 219, 145), 26, 36)

# sunbeams overlay - soft shafts that fade across the room
beam_mask = Image.new('L', (CW, CH), 0)
bd = ImageDraw.Draw(beam_mask)
beams = [
    ([(190,125),(335,120),(1020,1000),(760,1000)], 100),
    ([(320,150),(420,150),(1240,1000),(1040,1000)], 74),
    ([(440,180),(512,182),(1510,960),(1370,1000)], 56),
    ([(205,330),(252,325),(690,1000),(595,1000)], 44),
    ([(300,440),(340,438),(760,1000),(700,1000)], 30),
]
for pts, a in beams:
    bd.polygon([pt(q) for q in pts], fill=a)
beam_mask = beam_mask.filter(ImageFilter.GaussianBlur(sc(13)))
# fade the shafts from left (window) to right
fade = Image.new('L', (256, 1))
fp = fade.load()
for x in range(256):
    t = x / 255
    # bright near the window, gently fading to the right
    if t < 0.12:
        v = int(255 * (0.45 + t/0.12*0.55))
    elif t < 0.62:
        v = int(255 * (1.0 - (t-0.12)/0.50*0.45))
    else:
        v = int(255 * (0.55 - (t-0.62)/0.38*0.50))
    fp[x,0] = max(0, min(255, v))
fade = fade.resize((CW, CH), Image.Resampling.BILINEAR)
beam_mask = ImageChops.multiply(beam_mask, fade)
beam = Image.new('RGBA', (CW, CH), (255, 229, 170, 0))
beam.putalpha(beam_mask)
img.alpha_composite(beam)

# crisp little reflections near the window
refl = Image.new('RGBA', (CW, CH), (0,0,0,0))
rd = ImageDraw.Draw(refl)
for pts, a in [
    ([(214,126),(232,126),(338,590),(310,590)], 28),
    ([(246,130),(266,130),(402,590),(368,590)], 20),
    ([(390,300),(410,300),(590,592),(560,592)], 18),
]:
    rd.polygon([pt(q) for q in pts], fill=(255, 241, 200, a))
refl = refl.filter(ImageFilter.GaussianBlur(sc(10)))
img.alpha_composite(refl)

# low pool of sun across the rug and floor
sunpatch = Image.new('RGBA', (CW, CH), (0,0,0,0))
spd = ImageDraw.Draw(sunpatch)
spd.polygon([pt((322,870)),pt((690,866)),pt((758,1000)),pt((382,1000))], fill=(255, 220, 145, 30))
spd.polygon([pt((372,872)),pt((548,870)),pt((610,1000)),pt((424,1000))], fill=(255, 235, 177, 22))
sunpatch = sunpatch.filter(ImageFilter.GaussianBlur(sc(18)))
img.alpha_composite(sunpatch)

# dust motes in the beams
motes = Image.new('RGBA', (CW, CH), (0,0,0,0))
mdw = ImageDraw.Draw(motes)
for i in range(90):
    # choose a t along a beam and offset
    y = random.uniform(130, 950)
    frac = (y-130)/820
    x_left = 205 + frac*540 + random.uniform(-90, 90)
    x = x_left
    r = random.uniform(0.7, 2.6)
    a = random.randint(25, 105)
    mdw.ellipse([sc(x-r), sc(y-r), sc(x+r), sc(y+r)], fill=(255, 242, 207, a))
motes = motes.filter(ImageFilter.GaussianBlur(sc(1.2)))
img.alpha_composite(motes)

# window bloom
glow(390, 300, 320, 260, (255, 238, 198), 28, 55)
# warm top light
glow(780, 40, 650, 150, (255, 226, 175), 20, 50)
# soft vignette
vign = Image.new('RGBA', (CW, CH), (0,0,0,0))
vd = ImageDraw.Draw(vign)
# concentric dark rings via large ellipses? use radial mask
mask = Image.radial_gradient('L').resize((CW, CH), Image.Resampling.BILINEAR)
# radial is dark center? invert to make edges dark
mask = ImageChops.invert(mask)
mask = mask.point(lambda p: int(p * 0.34))
dark = Image.new('RGBA', (CW, CH), (51, 27, 17, 255))
dark.putalpha(mask)
img.alpha_composite(dark)

# subtle color grade / warm haze
warm = Image.new('RGBA', (CW, CH), (255, 196, 124, 10))
img.alpha_composite(warm)

# fine grain
noise = Image.effect_noise((CW, CH), 18).convert('L')
noise_rgb = Image.merge('RGBA', (noise, noise, noise, Image.new('L', (CW, CH), 9)))
img.alpha_composite(noise_rgb)

# ================================================================ FINAL
img = img.convert('RGB').resize((W, H), Image.Resampling.LANCZOS)
from PIL import ImageEnhance
img = ImageEnhance.Color(img).enhance(1.10)
img = ImageEnhance.Contrast(img).enhance(1.055)
img = ImageEnhance.Brightness(img).enhance(1.015)
out = Path('/tmp/vellery-mxo3uz6u/work/cozy-kitchen-morning.png')
img.save(out, quality=95)
print('saved', out, img.size)
