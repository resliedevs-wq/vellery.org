from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance
import math, random

random.seed(7)

W, H = 1600, 1200
S = 2
IW, IH = W * S, H * S

# ---------------- palette ----------------
WALL_TOP    = (250, 237, 214)
WALL_BOT    = (235, 208, 170)
CREAM       = (248, 237, 217)
CREAM_DARK  = (226, 207, 178)
PAPER       = (250, 242, 227)
WOOD_HI     = (203, 154, 100)
WOOD        = (171, 119, 74)
WOOD_MID    = (150, 99, 60)
WOOD_DARK   = (105, 68, 42)
SAGE        = (139, 158, 128)
SAGE_LIGHT  = (169, 184, 154)
SAGE_DARK   = (91, 112, 86)
FOREST      = (57, 76, 58)
TERRA       = (190, 104, 70)
TERRA_LIGHT = (218, 143, 105)
HONEY       = (226, 167, 84)
GOLD        = (231, 183, 99)
INK         = (76, 55, 41)
INK_SOFT    = (109, 81, 60)
BLUSH       = (226, 183, 155)

def mix(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))

def rgba(c, a=255):
    return (c[0], c[1], c[2], a)

# ---------------- low-level helpers ----------------
def sbox(box):
    return tuple(int(round(v * S)) for v in box)

def spt(p):
    return (int(round(p[0] * S)), int(round(p[1] * S)))

def vgrad(size, top, bottom):
    w, h = size
    g = Image.new("RGBA", (1, max(1, h)))
    px = g.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y] = rgba(mix(top, bottom, t))
    return g.resize((w, h), Image.Resampling.BILINEAR)

def hgrad(size, left, right):
    w, h = size
    g = Image.new("RGBA", (max(1, w), 1))
    px = g.load()
    for x in range(w):
        t = x / max(1, w - 1)
        px[x, 0] = rgba(mix(left, right, t))
    return g.resize((w, h), Image.Resampling.BILINEAR)

def rounded_mask(size, radius):
    w, h = size
    m = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(m)
    md.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(radius), fill=255)
    return m

class Art:
    def __init__(self):
        self.img = Image.new("RGBA", (IW, IH), (255, 255, 255, 255))
        self.d = ImageDraw.Draw(self.img)

    def comp(self, layer):
        self.img.alpha_composite(layer)
        self.d = ImageDraw.Draw(self.img)

    def rr(self, box, r, fill=None, outline=None, width=1):
        self.d.rounded_rectangle(sbox(box), radius=int(r * S), fill=rgba(fill) if fill and len(fill) == 3 else fill,
                                 outline=rgba(outline) if outline and len(outline) == 3 else outline,
                                 width=int(width * S))

    def el(self, box, fill=None, outline=None, width=1):
        self.d.ellipse(sbox(box), fill=rgba(fill) if fill and len(fill) == 3 else fill,
                       outline=rgba(outline) if outline and len(outline) == 3 else outline,
                       width=int(width * S))

    def poly(self, pts, fill=None, outline=None, width=1):
        pp = [spt(p) for p in pts]
        self.d.polygon(pp, fill=rgba(fill) if fill and len(fill) == 3 else fill,
                       outline=rgba(outline) if outline and len(outline) == 3 else outline,
                       width=int(width * S))

    def ln(self, pts, fill, width=2, joint="curve"):
        self.d.line([spt(p) for p in pts], fill=rgba(fill) if len(fill) == 3 else fill,
                    width=max(1, int(width * S)), joint=joint)

    def arc(self, box, a1, a2, fill, width=2):
        self.d.arc(sbox(box), a1, a2, fill=rgba(fill) if len(fill) == 3 else fill, width=max(1, int(width * S)))

    def chord(self, box, a1, a2, fill):
        self.d.chord(sbox(box), a1, a2, fill=rgba(fill) if len(fill) == 3 else fill)

    def pieslice(self, box, a1, a2, fill):
        self.d.pieslice(sbox(box), a1, a2, fill=rgba(fill) if len(fill) == 3 else fill)

    def grad_rect(self, box, r, top, bottom, vertical=True, outline=None, width=1):
        b = sbox(box)
        w, h = b[2] - b[0], b[3] - b[1]
        if w <= 0 or h <= 0:
            return
        g = vgrad((w, h), top, bottom) if vertical else hgrad((w, h), top, bottom)
        m = rounded_mask((w, h), r * S)
        layer = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
        layer.paste(g, (b[0], b[1]), m)
        self.comp(layer)
        if outline:
            self.rr(box, r, fill=None, outline=outline, width=width)

    def shadow(self, box, blur=14, alpha=70, color=(73, 50, 35), offset=(0, 5)):
        b = sbox((box[0] + offset[0], box[1] + offset[1], box[2] + offset[0], box[3] + offset[1]))
        layer = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.ellipse(b, fill=rgba(color, alpha))
        layer = layer.filter(ImageFilter.GaussianBlur(blur * S))
        self.comp(layer)

    def shadow_rect(self, box, r=10, blur=12, alpha=55, color=(73, 50, 35), offset=(0, 6)):
        b = sbox((box[0] + offset[0], box[1] + offset[1], box[2] + offset[0], box[3] + offset[1]))
        layer = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle(b, radius=int(r * S), fill=rgba(color, alpha))
        layer = layer.filter(ImageFilter.GaussianBlur(blur * S))
        self.comp(layer)

    def glow(self, center, radius, color=(255, 222, 156), alpha=120, blur=28):
        cx, cy = spt(center)
        r = int(radius * S)
        layer = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgba(color, alpha))
        layer = layer.filter(ImageFilter.GaussianBlur(blur * S))
        self.comp(layer)

    def text(self, pos, txt, font, fill):
        self.d.text(spt(pos), txt, font=font, fill=rgba(fill) if len(fill) == 3 else fill)


def bezier(p0, p1, p2, p3, n=60):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt**3*p0[0] + 3*mt**2*t*p1[0] + 3*mt*t**2*p2[0] + t**3*p3[0]
        y = mt**3*p0[1] + 3*mt**2*t*p1[1] + 3*mt*t**2*p2[1] + t**3*p3[1]
        pts.append((x, y))
    return pts

def poly_ellipse(cx, cy, rx, ry, n=90):
    return [(cx + rx * math.cos(2*math.pi*i/n), cy + ry * math.sin(2*math.pi*i/n)) for i in range(n)]

def wavy_panel(x0, x1, y0, y1, amp=12, waves=5):
    pts = []
    n = 70
    for i in range(n + 1):
        y = y0 + (y1 - y0) * i / n
        x = x0 + amp * math.sin(waves * math.pi * i / n)
        pts.append((x, y))
    for i in range(n, -1, -1):
        y = y0 + (y1 - y0) * i / n
        x = x1 + amp * math.sin(waves * math.pi * i / n + 0.9)
        pts.append((x, y))
    return pts

# ---------------- build ----------------
A = Art()

# wall wash
wall = vgrad((IW, IH), WALL_TOP, WALL_BOT)
A.img.alpha_composite(wall)
A.d = ImageDraw.Draw(A.img)

# very subtle plaster mottling
mottle = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
md = ImageDraw.Draw(mottle)
for _ in range(120):
    x = random.uniform(0, W) * S
    y = random.uniform(0, 780) * S
    rx = random.uniform(50, 260) * S
    ry = random.uniform(25, 110) * S
    c = random.choice([(255, 244, 224), (214, 178, 139), (255, 231, 195)])
    md.ellipse([x-rx, y-ry, x+rx, y+ry], fill=rgba(c, random.randint(3, 8)))
mottle = mottle.filter(ImageFilter.GaussianBlur(35 * S))
A.comp(mottle)

# ceiling shadow at very top
A.grad_rect((0, 0, W, 55), 0, (205, 174, 137), WALL_TOP, vertical=True)
A.ln([(0, 57), (W, 57)], (222, 194, 159), 2)

# soft warm wash on the room wall (kept off the glass)
A.glow((880, 520), 230, (255, 218, 154), 10, 100)


# =========================================================
# WINDOW
# =========================================================
win_out = (122, 72, 812, 704)
win_in  = (152, 101, 782, 676)

# outer shadow on wall
A.shadow_rect((112, 76, 818, 708), 10, 22, 60, (108, 76, 50), (10, 18))

# outer cream casing
A.grad_rect(win_out, 10, (252, 243, 226), (225, 205, 174), True, (205, 180, 148), 2)
A.rr((133, 82, 801, 694), 8, fill=None, outline=(239, 225, 203), width=4)
A.rr((143, 92, 791, 686), 5, fill=None, outline=(198, 169, 137), width=2)

# glass frame
A.grad_rect((151, 100, 783, 677), 5, (190, 146, 101), (146, 98, 61), True, (121, 80, 51), 3)

# ---- outside view ----
b = sbox((164, 113, 770, 664))
gw, gh = b[2] - b[0], b[3] - b[1]
gmask = Image.new("L", (gw, gh), 0)
ImageDraw.Draw(gmask).rectangle([0, 0, gw, gh], fill=255)
outside = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
outside.alpha_composite(vgrad((gw, gh), (255, 244, 211), (245, 200, 155)))
od = ImageDraw.Draw(outside)

# early sun, soft and low
sx, sy = gw*0.78, gh*0.17
sun_glow = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
sgd = ImageDraw.Draw(sun_glow)
for rad, a in [(245, 22), (185, 28), (128, 36), (78, 48)]:
    sgd.ellipse([sx-rad, sy-rad, sx+rad, sy+rad], fill=rgba((255, 242, 191), a))
sun_glow = sun_glow.filter(ImageFilter.GaussianBlur(34*S))
outside.alpha_composite(sun_glow)
od = ImageDraw.Draw(outside)
od.ellipse([sx-30, sy-30, sx+30, sy+30], fill=rgba((255, 247, 207), 200))
od.ellipse([sx-16, sy-16, sx+16, sy+16], fill=rgba((255, 253, 235), 238))
od.ellipse([sx-8, sy-8, sx+8, sy+8], fill=rgba((255, 255, 248), 255))

# far hills, soft blue-sage
od.polygon([(0, int(gh*0.55)), (int(gw*0.14), int(gh*0.49)), (int(gw*0.30), int(gh*0.53)),
            (int(gw*0.45), int(gh*0.47)), (int(gw*0.61), int(gh*0.52)), (int(gw*0.80), int(gh*0.475)),
            (gw, int(gh*0.515)), (gw, int(gh*0.67)), (0, int(gh*0.67))],
           fill=rgba((195, 199, 160), 200))
od.polygon([(0, int(gh*0.59)), (int(gw*0.18), int(gh*0.55)), (int(gw*0.38), int(gh*0.58)),
            (int(gw*0.55), int(gh*0.54)), (int(gw*0.74), int(gh*0.585)), (int(gw*0.90), int(gh*0.55)),
            (gw, int(gh*0.58)), (gw, int(gh*0.73)), (0, int(gh*0.73))],
           fill=rgba((168, 180, 140), 210))
od.rectangle([0, int(gh*0.51), gw, int(gh*0.59)], fill=rgba((255, 238, 200), 55))

# meadow
od.polygon([(0, int(gh*0.62)), (int(gw*0.22), int(gh*0.59)), (int(gw*0.50), int(gh*0.63)),
            (int(gw*0.76), int(gh*0.58)), (gw, int(gh*0.62)), (gw, gh), (0, gh)],
           fill=rgba((154, 169, 123), 245))

# little orchard trees along the meadow
def small_tree(cx, base, crown_y, r, trunk_col=(125, 96, 66)):
    od.line([(cx, base), (cx+2, crown_y)], fill=rgba(trunk_col, 220), width=max(3, int(r*0.18)))
    od.line([(cx+1, crown_y+r*0.6), (cx-r*0.55, crown_y+r*0.15)], fill=rgba(trunk_col, 200), width=max(2, int(r*0.09)))
    od.line([(cx+2, crown_y+r*0.7), (cx+r*0.55, crown_y+r*0.25)], fill=rgba(trunk_col, 200), width=max(2, int(r*0.09)))
    clusters = [(-r*0.5, r*0.02, r*0.62), (r*0.5, -r*0.02, r*0.58),
                (0, -r*0.46, r*0.68), (0, r*0.24, r*0.54), (-r*0.24, -r*0.15, r*0.48)]
    for dx, dy, rr in clusters:
        od.ellipse([cx+dx-rr, crown_y+dy-rr*0.78, cx+dx+rr, crown_y+dy+rr*0.78],
                   fill=rgba((84, 110, 77), 235))
    for dx, dy, rr in clusters:
        od.ellipse([cx+dx-rr*0.82, crown_y+dy-rr*0.72, cx+dx+rr*0.1, crown_y+dy+rr*0.05],
                   fill=rgba((119, 143, 96), 120))
    od.ellipse([cx-r*0.38, crown_y-r*0.54, cx+r*0.1, crown_y-r*0.16], fill=rgba((186, 189, 124), 78))

for cx, base, cy, r in [(gw*0.075, gh*0.72, gh*0.47, 47),
                        (gw*0.185, gh*0.73, gh*0.43, 58),
                        (gw*0.315, gh*0.74, gh*0.50, 38),
                        (gw*0.875, gh*0.73, gh*0.44, 54),
                        (gw*0.965, gh*0.75, gh*0.49, 40)]:
    small_tree(cx, base, cy, r)
# distant tiny trees, a dotted treeline
for i in range(23):
    x = random.uniform(0, gw)
    y = random.uniform(gh*0.505, gh*0.585)
    r = random.uniform(4, 10)
    od.ellipse([x-r, y-r, x+r, y+r], fill=rgba((111, 133, 96), 175))

# weathered fence, softened by shrubs
fy = gh*0.665
for i in range(14):
    x = i*gw/13 + 5
    od.rectangle([x, fy-26, x+4, fy+58], fill=rgba((186, 164, 127), 115))
od.rectangle([0, fy-4, gw, fy+2], fill=rgba((203, 181, 143), 100))
od.rectangle([0, fy+27, gw, fy+32], fill=rgba((196, 175, 138), 90))
# climbing roses on the fence
for i in range(18):
    x = random.uniform(gw*0.02, gw*0.32)
    y = random.uniform(fy-20, fy+35)
    r = random.uniform(2.5, 5)
    od.ellipse([x-r, y-r, x+r, y+r], fill=rgba((246, 224, 199), 190))
    od.ellipse([x-r*.3, y-r*.3, x+r*.3, y+r*.3], fill=rgba((216, 160, 93), 190))

# hedges and flower border
for _ in range(70):
    x = random.uniform(-10, gw+10)
    y = random.uniform(gh*0.68, gh*0.88)
    r = random.uniform(12, 40)
    c = random.choice([(100, 126, 87), (116, 140, 98), (88, 114, 81), (132, 150, 104)])
    od.ellipse([x-r, y-r*0.6, x+r, y+r*0.6], fill=rgba(c, 220))
# grasses and wildflowers
for _ in range(120):
    x = random.uniform(0, gw)
    y = random.uniform(gh*0.76, gh*0.99)
    h = random.uniform(9, 30)
    od.line([(x, y), (x+random.uniform(-5, 5), y-h)],
            fill=rgba(random.choice([(146, 168, 107), (181, 185, 119), (122, 148, 95)]), random.randint(55, 115)),
            width=1)
for _ in range(26):
    x = random.uniform(0, gw)
    y = random.uniform(gh*0.78, gh*0.96)
    r = random.uniform(2.5, 5.5)
    od.ellipse([x-r, y-r, x+r, y+r], fill=rgba(random.choice([(250, 231, 190), (243, 202, 159), (247, 242, 217)]), 220))
    od.ellipse([x-r*0.3, y-r*0.3, x+r*0.3, y+r*0.3], fill=rgba((206, 151, 78), 225))

# two birds in the warm sky
for bx, by, sz in [(gw*0.53, gh*0.27, 6), (gw*0.58, gh*0.235, 4)]:
    od.arc([bx-sz*2, by-sz, bx, by+sz], 200, 340, (114, 105, 80), 2)
    od.arc([bx, by-sz, bx+sz*2, by+sz], 200, 340, (114, 105, 80), 2)

# depth of field: just the foreground softens
blurred = outside.filter(ImageFilter.GaussianBlur(2.2 * S))
mask = Image.new("L", (gw, gh), 0)
mdm = ImageDraw.Draw(mask)
mdm.rectangle([0, int(gh*0.79), gw, gh], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(16*S))
outside = Image.composite(blurred, outside, mask)
# gentle atmospheric softness
outside = outside.filter(ImageFilter.GaussianBlur(0.6*S))

# glass tint + subtle reflections
outside.alpha_composite(Image.new("RGBA", (gw, gh), (255, 236, 195, 18)))
grd = ImageDraw.Draw(outside)
grd.polygon([(int(gw*0.57), 0), (int(gw*0.61), 0),
             (int(gw*0.38), int(gh*0.9)), (int(gw*0.34), int(gh*0.9))],
            fill=rgba((255, 249, 232), 10))
grd.line([(int(gw*0.49), 0), (int(gw*0.22), gh)], fill=rgba((255, 255, 247), 28), width=2*S)
grd.line([(int(gw*0.28), 0), (int(gw*0.12), int(gh*0.55))], fill=rgba((255, 255, 247), 18), width=2*S)
# faint interior reflection on glass
grd.rectangle([0, 0, gw, int(gh*0.025)], fill=rgba((255, 247, 228), 55))

A.img.paste(outside, (b[0], b[1]), gmask)
A.d = ImageDraw.Draw(A.img)

# frame mullions
# vertical centre bar
A.grad_rect((445, 112, 475, 675), 2, (203, 158, 111), (142, 96, 59), True, (118, 77, 49), 2)
# horizontal bar
A.grad_rect((157, 388, 779, 418), 2, (210, 166, 119), (151, 103, 64), True, (118, 77, 49), 2)
# little bevel highlights
A.ln([(450, 118), (450, 668)], (233, 197, 152), 2)
A.ln([(163, 394), (772, 394)], (233, 197, 152), 2)

# window inner frame highlights and shadows
A.ln([(160, 111), (774, 111)], (232, 192, 145), 2)
A.ln([(160, 666), (774, 666)], (112, 72, 47), 3)

# ---- sill ----
A.shadow_rect((98, 686, 826, 748), 8, 16, 75, (100, 70, 46), (8, 15))
A.grad_rect((98, 678, 826, 732), 5, (252, 241, 220), (219, 195, 162), True, (198, 169, 132), 2)
A.rr((110, 686, 814, 726), 3, fill=(240, 225, 203))
A.ln([(108, 690), (818, 690)], (255, 250, 236), 3)
A.ln([(104, 730), (822, 730)], (175, 145, 112), 2)
# sill supporting brackets
A.poly([(138, 732), (170, 732), (158, 762), (130, 762)], fill=(221, 201, 172))
A.poly([(752, 732), (784, 732), (794, 762), (766, 762)], fill=(214, 193, 164))
A.ln([(138, 733), (132, 758)], (184, 154, 121), 2)
A.ln([(752, 733), (766, 758)], (184, 154, 121), 2)


# =========================================================
# CURTAINS
# =========================================================
# brass rod
A.ln([(46, 58), (884, 58)], (145, 101, 61), 7)
A.ln([(48, 55), (882, 55)], (211, 165, 101), 3)
A.el((32, 42, 58, 72), fill=(177, 129, 73), outline=(123, 83, 49), width=2)
A.el((874, 42, 900, 72), fill=(177, 129, 73), outline=(123, 83, 49), width=2)
A.el((38, 48, 52, 62), fill=(223, 181, 115))
A.el((880, 48, 894, 62), fill=(223, 181, 115))

# left curtain: soft linen
def curtain(x0, x1, y0, y1, flip=1):
    layer = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    pts = []
    n = 50
    for i in range(n + 1):
        y = y0 + (y1-y0)*i/n
        edge = x0 - 10 * math.sin(i/n*math.pi*3) * flip
        pts.append((edge, y))
    # wavy gathered bottom
    for i in range(18, -1, -1):
        yy = y1 + 6 * math.sin(i/18*math.pi*3)
        pts.append((x0 + (x1-x0)*i/18, yy))
    for i in range(n + 1):
        y = y0 + (y1-y0)*i/n
        edge = x1 + 11 * math.sin(i/n*math.pi*3 + 1.2) * flip
        pts.append((edge, y))
    ld.polygon([(p[0]*S, p[1]*S) for p in pts], fill=rgba((243, 224, 196), 232))
    # folds
    for k in range(4):
        xx = x0 + (x1-x0)*(k+0.5)/4
        fold = bezier((xx, y0), (xx+8*flip, y0+120), (xx-8*flip, y1-150), (xx+4, y1), 40)
        ld.line([(p[0]*S, p[1]*S) for p in fold], fill=rgba((205, 172, 137), 70), width=3*S)
        hi = bezier((xx-7, y0), (xx-2, y0+110), (xx-16, y1-130), (xx-7, y1), 40)
        ld.line([(p[0]*S, p[1]*S) for p in hi], fill=rgba((255, 246, 227), 80), width=2*S)
    # shade at top
    for yy in range(int(y0), int(y0)+110):
        a = int(22 * (1 - (yy-y0)/110))
        ld.line([(x0*S, yy*S), (x1*S, yy*S)], fill=rgba((156, 118, 84), a), width=S)
    layer = layer.filter(ImageFilter.GaussianBlur(0.5*S))
    A.comp(layer)

curtain(52, 166, 62, 748, 1)
curtain(754, 872, 62, 742, -1)
# curtain tiebacks
A.arc((42, 434, 186, 494), 20, 205, (166, 118, 79), 3)
A.arc((744, 434, 888, 494), 335, 160, (166, 118, 79), 3)


# =========================================================
# TILE BACKSPLASH + COUNTER
# =========================================================
# tiles
tile_top, tile_bot = 728, 801
cols, rows = 19, 2
tw = W / cols
for r in range(rows):
    for c in range(cols):
        x0 = c*tw
        y0 = tile_top + r*(tile_bot-tile_top)/rows
        base = (203, 207, 178) if (r+c) % 3 else (213, 213, 185)
        if (c*7+r*3) % 5 == 0:
            base = (197, 204, 176)
        A.rr((x0+1.3, y0+1.3, x0+tw-1.3, y0+(tile_bot-tile_top)/rows-1.3), 2,
             fill=base, outline=(183, 186, 158), width=0.7)
        # glaze highlight
        A.ln([(x0+6, y0+7), (x0+tw-7, y0+7)], mix(base, (255, 255, 245), 0.65), 1.2)
# soft warm light falling across the tiles
tile_tint = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
td = ImageDraw.Draw(tile_tint)
td.rectangle([0, tile_top*S, IW, tile_bot*S], fill=rgba((255, 225, 178), 18))
td.polygon([(0, tile_top*S), (430*S, tile_top*S), (540*S, tile_bot*S), (0, tile_bot*S)],
           fill=rgba((255, 241, 205), 22))
A.comp(tile_tint)

# counter body shadow under lip
A.rect if False else None
A.shadow_rect((0, 798, W, 896), 0, 18, 70, (66, 47, 34), (0, 10))

# countertop wood
A.grad_rect((0, 795, W, 882), 0, (215, 168, 111), (147, 95, 57), True, (112, 73, 45), 2)
# butcher-block streaks
for i in range(26):
    y = random.uniform(801, 878)
    x0 = random.uniform(-50, W)
    x1 = x0 + random.uniform(150, 640)
    A.ln([(x0, y), (x1, y+random.uniform(-2.5, 2.5))],
         random.choice([(194, 145, 94), (129, 83, 51), (229, 184, 127)]),
         random.uniform(0.8, 2.2))
# surface ink lines / joins
A.ln([(0, 803), (W, 803)], (240, 203, 154), 2)
A.ln([(0, 876), (W, 876)], (83, 55, 36), 3)
A.ln([(0, 882), (W, 882)], (99, 66, 43), 3)
# front lip shadow
A.grad_rect((0, 882, W, 901), 0, (117, 78, 49), (80, 53, 35), True)


# =========================================================
# CABINETS / LOWER KITCHEN
# =========================================================
A.grad_rect((0, 899, W, H), 0, (148, 163, 133), (112, 131, 108), True)
A.ln([(0, 901), (W, 901)], (85, 105, 82), 3)

def cabinet_door(x0, x1, y0, y1, label=None):
    A.shadow_rect((x0+7, y0+8, x1-7, y1-6), 8, 10, 40, (49, 64, 49), (0, 6))
    A.rr((x0, y0, x1, y1), 8, fill=(139, 156, 128), outline=(88, 108, 86), width=2)
    A.rr((x0+13, y0+13, x1-13, y1-13), 5, fill=(151, 167, 139), outline=(102, 122, 97), width=2)
    A.rr((x0+22, y0+22, x1-22, y1-22), 4, fill=(145, 162, 134), outline=(159, 175, 145), width=1)
    # woodgrain-ish soft shading
    A.grad_rect((x0+22, y0+22, x1-22, y1-22), 4, (159, 174, 146), (132, 150, 124), True)
    A.ln([(x0+24, y0+18), (x1-24, y0+18)], (180, 193, 164), 2)
    A.ln([(x0+22, y1-17), (x1-22, y1-17)], (105, 124, 99), 2)
    # brass knob
    cx = (x0+x1)/2
    A.el((cx-8, (y0+y1)/2-8, cx+8, (y0+y1)/2+8), fill=(189, 145, 83), outline=(128, 89, 48), width=1.5)
    A.el((cx-4, (y0+y1)/2-5, cx+1, (y0+y1)/2), fill=(232, 195, 130))

# sink cabinet = central; hide behind objects, still pleasant
for x0, x1 in [(18, 270), (285, 556), (572, 846), (864, 1110), (1126, 1238)]:
    cabinet_door(x0, x1, 900, 1188)

# wide drawers instead of one tall panel for middle two? Keep simple shaker.
# add narrow top drawer band
for x0, x1 in [(18, 270), (285, 556), (572, 846), (864, 1110), (1126, 1238)]:
    A.rr((x0+6, 908, x1-6, 954), 5, fill=(144, 160, 132), outline=(107, 126, 101), width=1.5)
    cx = (x0+x1)/2
    A.rr((cx-13, 927, cx+13, 934), 3, fill=(190, 147, 85), outline=(123, 84, 46), width=1)

# things are added later


# =========================================================
# STOVE (right)
# =========================================================
stove_x0, stove_x1 = 1264, 1576
# stove shadow
A.shadow_rect((stove_x0-6, 790, stove_x1, 1150), 8, 20, 90, (50, 58, 45), (8, 14))
# side panel
A.grad_rect((stove_x0, 806, stove_x1, 1150), 6, (233, 219, 192), (196, 178, 149), True, (155, 134, 106), 2)
# cooktop
A.grad_rect((stove_x0-10, 788, stove_x1+4, 824), 5, (66, 74, 68), (34, 41, 39), True, (28, 32, 30), 2)
A.ln([(stove_x0-2, 793), (stove_x1, 793)], (117, 124, 111), 2)
# burners
for bx, by, br in [(1326, 806, 31), (1479, 806, 30)]:
    A.el((bx-br, by-br*0.34, bx+br, by+br*0.34), fill=(26, 31, 29), outline=(84, 91, 82), width=2)
    A.el((bx-br*0.64, by-br*0.22, bx+br*0.64, by+br*0.22), fill=(42, 48, 44), outline=(99, 103, 92), width=1.5)
    A.el((bx-br*0.3, by-br*0.1, bx+br*0.3, by+br*0.1), fill=(28, 33, 30))
# control panel
A.grad_rect((stove_x0+12, 824, stove_x1-10, 892), 3, (227, 213, 187), (188, 169, 141), True, (153, 131, 103), 2)
for i in range(5):
    cx = stove_x0 + 55 + i*63
    A.el((cx-13, 842, cx+13, 868), fill=(207, 185, 152), outline=(128, 103, 73), width=2)
    A.el((cx-7, 848, cx+7, 862), fill=(164, 135, 98), outline=(117, 88, 58), width=1)
    A.ln([(cx, 849), (cx, 856)], (82, 57, 38), 2)
# oven door
A.grad_rect((stove_x0+14, 902, stove_x1-12, 1118), 6, (229, 215, 189), (192, 173, 143), True, (149, 126, 98), 2)
A.grad_rect((stove_x0+38, 932, stove_x1-36, 1082), 8, (58, 70, 65), (33, 43, 41), True, (77, 65, 50), 3)
# glass reflection
A.poly([(stove_x0+52, 940), (stove_x0+178, 940), (stove_x0+90, 1072), (stove_x0+52, 1072)],
       fill=(84, 101, 94), outline=None)
A.ln([(stove_x0+55, 940), (stove_x0+108, 940)], (157, 168, 146), 3)
# towel rail / handle
A.rr((stove_x0+58, 901, stove_x1-58, 913), 6, fill=(191, 150, 88), outline=(118, 82, 45), width=2)
A.rr((stove_x0+80, 906, stove_x1-80, 909), 2, fill=(240, 204, 139))
# little legs
for lx in [stove_x0+24, stove_x1-34]:
    A.rr((lx, 1120, lx+12, 1150), 3, fill=(149, 127, 99))
# drawer at bottom
A.rr((stove_x0+36, 1126, stove_x1-34, 1174), 4, fill=(221, 205, 178), outline=(155, 133, 106), width=2)
A.rr((stove_x0+66, 1144, stove_x1-64, 1151), 3, fill=(178, 139, 83))

# stove backsplash, deep sage zellige
A.grad_rect((1264, 664, 1576, 800), 4, (103, 126, 103), (65, 85, 68), True, (47, 63, 49), 2)
for j, yy in enumerate(range(672, 800, 25)):
    for i, xx in enumerate(range(1271, 1580, 35)):
        base = [ (113, 136, 110), (105, 128, 103), (94, 118, 96), (119, 139, 112) ][(i+j*2) % 4]
        A.rr((xx+1, yy+2, min(xx+34, 1574), yy+23), 3, fill=base, outline=(75, 96, 75), width=0.8)
        A.ln([(xx+5, yy+6), (min(xx+29, 1570), yy+6)], mix(base, (255, 249, 225), .35), 1)
# soft morning light glancing across the tiles
tile_light = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
tld = ImageDraw.Draw(tile_light)
tld.polygon([(1264*S, 664*S), (1430*S, 664*S), (1390*S, 800*S), (1264*S, 800*S)],
            fill=rgba((255, 225, 170), 24))
tld.rectangle([1264*S, 664*S, 1576*S, 674*S], fill=rgba((255, 236, 196), 30))
A.comp(tile_light)
A.ln([(1270, 671), (1570, 671)], (185, 199, 167), 1)

# linen towel on the oven handle, with a hand-stitched stripe
A.shadow_rect((1346, 920, 1436, 1034), 8, 12, 52, (73, 53, 38), (3, 7))
towel_pts = [(1344, 910), (1438, 910), (1442, 1008), (1438, 1028),
             (1420, 1012), (1404, 1030), (1388, 1012), (1372, 1030), (1354, 1012), (1338, 1024)]
A.poly(towel_pts, fill=(243, 232, 209), outline=(178, 155, 124), width=1.6)
A.poly([(1344, 910), (1360, 910), (1355, 1018), (1338, 1024)], fill=(233, 219, 193))
A.ln([(1371, 921), (1366, 1016)], (214, 197, 169), 2)
A.ln([(1392, 918), (1390, 1020)], (252, 244, 226), 2)
A.ln([(1414, 920), (1419, 1012)], (211, 193, 165), 2)
# terracotta band and tiny leaf
A.ln([(1348, 971), (1436, 966)], (183, 105, 73), 5)
A.ln([(1348, 977), (1436, 972)], (224, 161, 118), 2)
A.ln([(1392, 939), (1392, 955)], (102, 127, 88), 2)
A.el((1386, 933, 1392, 941), fill=(108, 136, 92))
A.el((1392, 936, 1400, 944), fill=(108, 136, 92))


# =========================================================
# OPEN SHELVES (right)
# =========================================================
shelf_x0, shelf_x1 = 918, 1580

def shelf(y, thickness=20):
    A.shadow_rect((shelf_x0+8, y+12, shelf_x1, y+thickness+18), 4, 18, 70, (96, 67, 45), (0, 8))
    A.grad_rect((shelf_x0, y, shelf_x1, y+thickness), 3, (207, 156, 99), (141, 91, 54), True, (109, 70, 43), 2)
    A.ln([(shelf_x0+2, y+3), (shelf_x1-2, y+3)], (235, 191, 133), 2)
    A.ln([(shelf_x0+2, y+thickness-3), (shelf_x1-2, y+thickness-3)], (113, 72, 44), 2)
    # brackets
    for bx in [shelf_x0+52, shelf_x1-64]:
        A.poly([(bx-10, y+thickness), (bx+10, y+thickness), (bx+6, y+thickness+38), (bx, y+thickness+42), (bx-6, y+thickness+38)],
               fill=(151, 100, 60), outline=(105, 68, 42), width=1.5)

shelf(288, 22)
shelf(516, 20)

# --- upper shelf: plates, jars, jug, trailing plant
# plate stack leaning
A.shadow_rect((940, 170, 1056, 286), 6, 10, 55, (88, 60, 39), (3, 8))
for i in range(3):
    off = i*10
    A.el((948+off, 178+off*0.45, 1048-off*0.2, 288+off*0.1), fill=(243, 229, 205), outline=(186, 157, 121), width=2)
    A.el((960+off, 190+off*0.45, 1035-off*0.2, 276+off*0.05), fill=(235, 218, 191), outline=(205, 175, 137), width=1)
    A.arc((948+off, 178+off*0.45, 1048-off*0.2, 288+off*0.1), 200, 340, (255, 250, 236), 2)
# small plate stand
A.ln([(1000, 288), (1000, 206)], (123, 84, 52), 4)

# glass jar with grains
A.shadow_rect((1070, 196, 1168, 288), 10, 8, 40, (88, 60, 39), (3, 6))
A.grad_rect((1076, 198, 1162, 286), 9, (216, 194, 154), (179, 147, 102), True, (147, 114, 76), 2)
A.grad_rect((1084, 220, 1154, 278), 6, (200, 167, 112), (162, 127, 79), True)
# grain speckles
for _ in range(28):
    x = random.uniform(1087, 1151); y = random.uniform(229, 275)
    A.el((x-2, y-1.5, x+2, y+1.5), fill=random.choice([(226, 197, 145), (138, 102, 65), (245, 220, 167)]))
# jar lid
A.rr((1082, 185, 1156, 206), 5, fill=(186, 147, 94), outline=(125, 88, 52), width=2)
A.ln([(1088, 191), (1151, 191)], (225, 189, 131), 2)
# glass shine
A.ln([(1088, 207), (1088, 274)], (255, 247, 226), 3)
A.ln([(1095, 210), (1095, 258)], (255, 247, 226), 1)

# little sage jug
A.shadow_rect((1182, 210, 1258, 288), 10, 8, 35, (88, 60, 39), (3, 6))
A.grad_rect((1188, 220, 1252, 288), 14, (158, 174, 146), (105, 126, 102), True, (80, 98, 77), 2)
A.el((1195, 207, 1245, 239), fill=(150, 168, 140), outline=(83, 101, 79), width=2)
A.el((1202, 210, 1238, 228), fill=(172, 187, 157))
A.arc((1217, 225, 1280, 273), 270, 90, (107, 128, 102), 3)
A.ln([(1200, 232), (1200, 274)], (208, 218, 189), 2)

# trailing plant
A.shadow_rect((1322, 232, 1444, 288), 8, 8, 38, (88, 60, 39), (3, 6))
A.grad_rect((1330, 238, 1438, 288), 8, (205, 141, 96), (151, 92, 59), True, (122, 72, 46), 2)
A.rr((1330, 230, 1438, 249), 5, fill=(180, 113, 76), outline=(119, 70, 45), width=2)
# leaves on vines
vines = [
    [(1384, 240), (1380, 270), (1392, 300), (1374, 330), (1388, 358), (1370, 384)],
    [(1398, 242), (1405, 274), (1397, 302), (1410, 332), (1398, 360)],
    [(1368, 244), (1352, 278), (1360, 308), (1343, 338)],
]
for vi, vine in enumerate(vines):
    A.ln(vine, (79, 109, 74), 2)
    for i, (x, y) in enumerate(vine[1:]):
        ang = -0.65 if (i + vi) % 2 == 0 else 1.1
        rx, ry = 14, 8
        pts = []
        for k in range(24):
            a = 2*math.pi*k/24
            px = x + rx*math.cos(a)*math.cos(ang) - ry*math.sin(a)*math.sin(ang)
            py = y + rx*math.cos(a)*math.sin(ang) + ry*math.sin(a)*math.cos(ang)
            pts.append((px, py))
        A.poly(pts, fill=random.choice([(89, 123, 83), (107, 139, 95), (75, 107, 73)]), outline=(60, 88, 58), width=1)

# stack of small bowls at far right
for i in range(3):
    yy = 288 - 14 - i*13
    A.grad_rect((1454-i*2, yy-13, 1520+i*2, yy+5), 12, (239, 217, 188), (192, 156, 117), True, (165, 128, 90), 1.5)

# --- lower shelf: cookbooks, lemons, canisters, little art
# books
A.shadow_rect((934, 402, 1066, 516), 4, 10, 52, (88, 60, 39), (3, 8))
books = [((940, 428, 986, 516), (171, 97, 69)), ((984, 414, 1028, 516), (112, 132, 108)),
         ((1026, 424, 1064, 516), (213, 178, 125)), ((1042, 440, 1078, 516), (147, 108, 77))]
for (bx0, by0, bx1, by1), col in books:
    A.rr((bx0, by0, bx1, by1), 2, fill=col, outline=mix(col, (56, 39, 27), 0.45), width=1.5)
    A.rr((bx0+4, by0+6, bx0+8, by1-7), 2, fill=mix(col, (255, 244, 220), 0.18))
    for k in range(2):
        yy = by0 + 18 + k*8
        A.ln([(bx0+12, yy), (bx1-8, yy)], mix(col, (245, 221, 180), 0.45), 1.2)
# open book lying at angle on top? skip
# lemon bowl
A.shadow((1068, 470, 1190, 518), 8, 45, (88, 60, 39), (3, 6))
A.pieslice((1072, 468, 1186, 542), 0, 180, (203, 177, 143))
A.chord((1068, 460, 1190, 518), 0, 180, (226, 205, 173))
A.arc((1068, 460, 1190, 518), 0, 180, (161, 128, 93), 2)
for lx, ly in [(1093, 470), (1121, 464), (1148, 472), (1132, 480), (1104, 482)]:
    A.el((lx-13, ly-11, lx+13, ly+11), fill=(234, 194, 87), outline=(167, 130, 50), width=1.5)
    A.el((lx+8, ly-9, lx+13, ly-4), fill=(248, 218, 123))
    A.ln([(lx+9, ly-3), (lx+2, ly+1)], (255, 245, 196), 1.2)

# canisters
for cx, col in [(1210, (225, 209, 179)), (1264, (211, 189, 155))]:
    A.shadow_rect((cx-24, 438, cx+24, 516), 8, 7, 34, (88, 60, 39), (2, 5))
    A.grad_rect((cx-22, 442, cx+22, 516), 8, mix(col, (255, 250, 238), 0.22), mix(col, (101, 80, 59), 0.08), True, (151, 128, 99), 1.6)
    A.rr((cx-25, 432, cx+25, 452), 5, fill=mix(col, (156, 119, 78), 0.28), outline=(121, 91, 60), width=1.5)
    A.ln([(cx-12, 462), (cx+12, 462)], mix(col, (255, 250, 236), 0.55), 2)
    A.el((cx-3, 478, cx+3, 484), fill=(164, 126, 80))

# small framed picture leaning
A.shadow_rect((1312, 424, 1420, 516), 3, 8, 45, (88, 60, 39), (3, 6))
A.rr((1314, 416, 1418, 516), 3, fill=(159, 105, 64), outline=(103, 67, 42), width=2)
A.rr((1324, 428, 1408, 506), 2, fill=(240, 227, 201), outline=(202, 173, 133), width=1)
# tiny landscape inside
A.poly([(1328, 486), (1352, 446), (1375, 470), (1392, 450), (1404, 486), (1404, 502), (1328, 502)], fill=(151, 168, 131))
A.el((1378, 438, 1394, 454), fill=(237, 190, 105))
A.ln([(1338, 492), (1394, 492)], (118, 141, 105), 1.5)

# trailing herb at far right hung from shelf
A.ln([(1502, 528), (1502, 558)], (191, 176, 140), 3)
A.ln([(1502, 548), (1482, 582)], (91, 116, 80), 2)
A.ln([(1502, 548), (1520, 588)], (91, 116, 80), 2)
for x, y in [(1480, 586), (1492, 604), (1512, 592), (1524, 612), (1478, 620), (1504, 634)]:
    A.el((x-9, y-4, x+9, y+4), fill=(104, 136, 88), outline=(71, 97, 64), width=1)


# =========================================================
# SINK + FAUCET
# =========================================================
# ceramic farmhouse sink
A.shadow_rect((284, 788, 656, 866), 22, 16, 75, (56, 40, 29), (0, 8))
# faucet (behind the basin rim)
faucet = [(480, 804), (480, 760), (486, 724), (501, 704), (521, 700),
          (540, 708), (550, 728), (552, 756), (548, 776)]
A.ln(faucet, (99, 68, 43), 11)
A.ln(faucet, (188, 145, 88), 7)
A.ln([(481, 790), (482, 752), (490, 721), (507, 706), (526, 705)],
     (239, 199, 134), 2)
# base + collar
A.el((462, 792, 498, 814), fill=(191, 149, 90), outline=(105, 71, 43), width=2)
A.rr((468, 778, 492, 797), 5, fill=(209, 168, 104), outline=(109, 74, 44), width=2)
# spout tip
A.rr((543, 764, 558, 786), 5, fill=(170, 125, 73), outline=(92, 62, 39), width=2)
A.el((544, 781, 557, 790), fill=(113, 80, 49))
# compact side lever at the base
A.ln([(478, 792), (455, 790)], (160, 118, 69), 5)
A.rr((447, 786, 461, 796), 3, fill=(197, 154, 92), outline=(101, 68, 41), width=1.5)
# basin rim
A.grad_rect((288, 786, 646, 858), 24, (250, 241, 221), (214, 196, 169), True, (156, 130, 101), 2)
A.rr((298, 792, 636, 850), 21, fill=(245, 233, 212), outline=(190, 169, 139), width=1.5)
# basin interior
A.grad_rect((311, 801, 623, 847), 18, (137, 156, 152), (86, 107, 105), True, (67, 86, 86), 2)
A.rr((320, 808, 614, 840), 14, fill=(116, 137, 134), outline=(89, 108, 106), width=1)
A.arc((320, 806, 614, 846), 8, 172, (171, 188, 180), 2)
A.ln([(338, 824), (476, 824)], (159, 178, 170), 3)
A.ln([(344, 831), (430, 831)], (141, 160, 154), 1.5)
# drain
A.el((458, 817, 480, 833), fill=(83, 100, 98), outline=(58, 75, 74), width=1.5)
A.el((463, 820, 475, 829), fill=(110, 126, 121))
# glints on rim
A.arc((294, 790, 640, 856), 190, 345, (255, 250, 237), 3)
A.ln([(306, 798), (330, 798)], (255, 251, 240), 3)
# farmhouse apron front, fluted
A.shadow_rect((300, 848, 640, 912), 16, 12, 65, (83, 61, 43), (0, 9))
A.grad_rect((302, 848, 638, 909), 15, (249, 239, 220), (214, 195, 169), True, (162, 135, 105), 2)
for fx in range(318, 630, 17):
    A.ln([(fx, 858), (fx, 897)], (226, 210, 186), 2)
    A.ln([(fx+4, 858), (fx+4, 897)], (249, 242, 227), 1)
A.rr((302, 848, 638, 863), 7, fill=(250, 242, 226))
A.arc((312, 884, 628, 916), 15, 165, (206, 187, 161), 2)
A.ln([(313, 855), (627, 855)], (255, 249, 237), 2)


# =========================================================
# KETTLE
# =========================================================
# shadow
A.shadow((1312, 758, 1452, 808), 10, 60, (53, 47, 33), (4, 4))
# body
A.grad_rect((1326, 646, 1436, 794), 36, (210, 96, 66), (147, 67, 46), True, (112, 50, 35), 2)
# spout
A.poly([(1428, 690), (1470, 666), (1478, 678), (1440, 714)], fill=(185, 82, 57), outline=(110, 49, 35), width=2)
A.ln([(1438, 690), (1468, 672)], (234, 133, 95), 2)
# handle arc
A.arc((1350, 590, 1418, 690), 180, 360, (103, 74, 47), 9)
A.arc((1352, 593, 1416, 687), 180, 360, (188, 143, 89), 4)
# lid
A.grad_rect((1354, 630, 1410, 654), 10, (223, 132, 91), (170, 79, 54), True, (114, 49, 35), 2)
A.el((1374, 618, 1390, 633), fill=(165, 115, 64), outline=(103, 65, 41), width=1.5)
# shine on body
A.arc((1338, 660, 1430, 782), 195, 260, (249, 170, 120), 4)
A.ln([(1342, 684), (1348, 744)], (240, 158, 112), 4)
# base
A.grad_rect((1322, 784, 1440, 800), 6, (117, 78, 48), (82, 55, 37), True, (67, 44, 31), 2)


# =========================================================
# SCENE DETAILS: CAT, PLANTS, BOWL, BOARD, MUGS, VASE
# =========================================================
# --- potted rosemary on left sill
A.shadow((156, 672, 244, 706), 6, 45, (88, 60, 39), (2, 4))
A.grad_rect((172, 628, 236, 690), 8, (207, 132, 92), (158, 88, 57), True, (117, 65, 42), 2)
A.rr((168, 620, 240, 640), 6, fill=(182, 105, 71), outline=(116, 64, 42), width=2)
# stems
for i in range(9):
    ang = -1.2 + i*0.3
    x0, y0 = 204 + random.uniform(-9, 9), 624
    x1, y1 = x0 + math.cos(ang)*random.uniform(18, 38), y0 - random.uniform(22, 55)
    A.ln([(x0, y0), (x1, y1)], (84, 111, 71), 2)
    for k in range(3):
        t = 0.35 + k*0.22
        lx, ly = x0+(x1-x0)*t, y0+(y1-y0)*t
        A.ln([(lx-7, ly+2), (lx, ly-2), (lx+7, ly+2)], (93, 125, 78), 2)
# tiny pot highlight
A.ln([(181, 636), (180, 676)], (235, 169, 121), 3)
A.rr((188, 646, 220, 660), 3, fill=(205, 133, 92), outline=(151, 87, 56), width=1)


# --- sleeping ginger cat on the sill
# cushion
A.shadow((578, 672, 762, 714), 8, 58, (92, 58, 35), (2, 4))
A.rr((576, 678, 764, 714), 16, fill=(172, 105, 77), outline=(124, 69, 50), width=2)
A.ln([(590, 690), (750, 690)], (207, 135, 101), 2)
A.ln([(590, 701), (748, 701)], (143, 86, 64), 2)
# body
cat = (205, 131, 69)
cat_light = (227, 158, 93)
cat_dark = (171, 101, 56)
# tail
A.ln([(736, 682), (744, 698), (700, 708), (632, 704), (612, 692)],
     cat_dark, 18)
A.ln([(740, 682), (746, 696), (702, 706), (636, 702)], cat, 10)
# body ellipse
A.el((595, 636, 735, 700), fill=cat, outline=cat_dark, width=2)
A.el((606, 644, 721, 690), fill=cat_light)
# haunch
A.el((658, 642, 742, 704), fill=cat, outline=cat_dark, width=1.5)
A.el((671, 652, 731, 696), fill=cat_light)
# stripes on body
for x, y0, y1 in [(650, 646, 674), (674, 646, 678), (698, 648, 676)]:
    A.arc((x-14, y0, x+14, y1+10), 245, 300, cat_dark, 3)
A.arc((620, 640, 666, 678), 255, 300, cat_dark, 3)
A.arc((692, 647, 728, 684), 250, 305, cat_dark, 3)
# tail curling around the front
tail = bezier((726, 666), (748, 682), (732, 700), (694, 702), 50)
A.ln(tail, (139, 79, 46), 19)
A.ln(tail, cat, 15)
A.ln([(x, y-3) for x, y in tail[2:22]], (231, 162, 96), 4)
for tx, ty in [(716, 692), (700, 698), (684, 700)]:
    A.ln([(tx-4, ty-10), (tx+5, ty-6)], cat_dark, 3)
# soft shadow under the cat's back
A.shadow((594, 688, 742, 706), 5, 45, (123, 79, 51), (0, 2))
# head
A.el((580, 632, 654, 700), fill=cat, outline=cat_dark, width=2)
A.el((590, 640, 649, 691), fill=cat_light)
# ears
A.poly([(589, 648), (589, 618), (612, 637)], fill=cat, outline=cat_dark, width=1.5)
A.poly([(627, 633), (650, 616), (647, 650)], fill=cat, outline=cat_dark, width=1.5)
A.poly([(594, 643), (594, 625), (607, 637)], fill=(215, 143, 119))
A.poly([(634, 634), (646, 624), (644, 641)], fill=(215, 143, 119))
# face markings
A.arc((594, 648, 608, 659), 205, 335, (111, 69, 47), 2)
A.arc((616, 648, 630, 659), 205, 335, (111, 69, 47), 2)
A.poly([(607, 664), (615, 664), (611, 670)], fill=(178, 103, 91))
A.ln([(611, 670), (611, 674)], (112, 73, 51), 1.5)
A.arc((602, 670, 612, 678), 0, 160, (112, 73, 51), 1.5)
A.arc((612, 670, 622, 678), 20, 180, (112, 73, 51), 1.5)
# forehead M
A.ln([(600, 641), (606, 650), (612, 642), (618, 650), (624, 641)], (167, 96, 55), 2)
# cheeks and whiskers
A.el((580, 658, 590, 676), fill=(235, 166, 103))
A.el((628, 658, 638, 676), fill=(235, 166, 103))
for yy in [666, 672]:
    A.ln([(580, yy), (557, yy-2)], (110, 72, 50), 1)
    A.ln([(638, yy), (660, yy-3)], (110, 72, 50), 1)
# paws tucked
A.el((607, 679, 632, 696), fill=(236, 168, 104), outline=(183, 112, 66), width=1.5)
A.el((620, 681, 642, 696), fill=(232, 160, 99), outline=(183, 112, 66), width=1.5)
for x in [614, 625, 635]:
    A.ln([(x, 687), (x, 692)], (171, 102, 60), 1)
# sleeping zzz (tiny, subtle)
A.text((666, 604), "z", None, (248, 226, 189)) if False else None


# --- bowl of oranges (left counter)
A.shadow((68, 754, 302, 806), 14, 60, (80, 51, 35), (4, 5))
# bowl back rim
A.pieslice((70, 720, 300, 810), 0, 180, (232, 213, 184))
A.chord((64, 708, 306, 790), 0, 180, (245, 230, 207))
A.arc((64, 708, 306, 790), 0, 180, (166, 133, 99), 3)
# oranges behind rim
for (ox, oy, r) in [(122, 728, 29), (168, 710, 32), (216, 721, 30), (252, 740, 25), (145, 742, 27)]:
    A.el((ox-r, oy-r, ox+r, oy+r), fill=(230, 158, 55), outline=(155, 97, 35), width=2)
    A.arc((ox-r+4, oy-r+4, ox+r-4, oy+r-4), 200, 330, (247, 190, 92), 3)
    A.el((ox-r*0.55, oy-r*0.7, ox-r*0.05, oy-r*0.2), fill=(245, 190, 105))
    # dimple
    A.el((ox-3, oy-r+3, ox+3, oy-r+9), fill=(181, 112, 39))
# bowl front
A.chord((62, 734, 308, 842), 0, 180, (240, 222, 194))
A.arc((62, 734, 308, 842), 0, 180, (158, 120, 84), 3)
A.arc((80, 746, 290, 826), 20, 160, (205, 176, 140), 4)
# rim highlight
A.arc((64, 708, 306, 790), 195, 345, (255, 247, 229), 3)
# small painted stripe
A.arc((74, 752, 296, 834), 15, 165, (188, 100, 70), 3)
# loose orange with leaf on counter
A.el((34, 760, 84, 806), fill=(232, 160, 56), outline=(155, 97, 35), width=2)
A.el((41, 768, 62, 786), fill=(246, 191, 96))
A.ln([(60, 765), (72, 758)], (99, 130, 83), 3)
A.el((68, 752, 84, 763), fill=(114, 148, 92), outline=(82, 111, 70), width=1)


# --- bread board with loaf
A.shadow_rect((682, 772, 966, 816), 14, 12, 62, (72, 46, 31), (5, 7))
# board
A.grad_rect((684, 736, 966, 808), 14, (215, 165, 106), (157, 103, 60), True, (114, 73, 42), 2)
A.rr((698, 748, 952, 795), 8, fill=(201, 150, 94), outline=(173, 124, 73), width=1)
# handle hole
A.el((918, 752, 944, 778), fill=(174, 120, 70), outline=(123, 81, 49), width=2)
A.el((925, 758, 937, 771), fill=(108, 74, 48))
# board grain
for i in range(9):
    yy = 750 + i*5
    A.ln([(704, yy), (902, yy+random.uniform(-1, 1))], (225, 178, 121), 1)
# rustic loaf
A.el((721, 687, 884, 780), fill=(184, 119, 59), outline=(126, 77, 41), width=2)
A.el((729, 683, 877, 768), fill=(213, 151, 84))
A.el((738, 689, 866, 744), fill=(231, 178, 109))
# floury top
A.el((748, 691, 858, 738), fill=(236, 188, 123))
A.el((760, 692, 836, 726), fill=(241, 199, 139))
# curved scoring, with a shadowed cut and a pale crumb edge
for sx in [745, 772, 799, 826]:
    pth = bezier((sx, 700), (sx+4, 711), (sx+6, 722), (sx+3, 733), 24)
    A.ln([(x-1, y+1) for x, y in pth], (153, 92, 47), 6)
    A.ln(pth, (244, 195, 127), 3)
    A.ln([(x+1, y) for x, y in pth[:16]], (251, 216, 158), 1.5)
# crust shading and shine
A.arc((726, 684, 880, 778), 195, 322, (238, 183, 114), 3)
A.arc((730, 694, 874, 772), 20, 150, (168, 101, 51), 2)
A.ln([(742, 712), (752, 705)], (252, 209, 148), 2)
# seeds / flour flecks
for _ in range(24):
    x = random.uniform(744, 860); y = random.uniform(699, 753)
    A.el((x-1.5, y-1, x+1.5, y+1), fill=random.choice([(134, 84, 47), (162, 108, 62)]))
for _ in range(30):
    x = random.uniform(752, 852); y = random.uniform(698, 750)
    A.el((x-1, y-1, x+1, y+1), fill=(249, 222, 172))
# one leaning slice
A.poly([(854, 739), (912, 718), (932, 766), (876, 782)], fill=(209, 146, 81), outline=(129, 79, 43), width=2)
A.poly([(862, 743), (907, 726), (922, 759), (878, 773)], fill=(240, 195, 135))
# slice crust
A.poly([(854, 739), (912, 718), (917, 731), (864, 752)], fill=(187, 119, 60))
A.arc((865, 742, 913, 765), 205, 330, (231, 173, 106), 5)
# airy crumb holes
for _ in range(15):
    x = random.uniform(873, 916); y = random.uniform(737, 766)
    r = random.uniform(1, 2.4)
    A.el((x-r, y-r*0.8, x+r, y+r*0.8), fill=(205, 149, 91))
for _ in range(16):
    x = random.uniform(866, 918); y = random.uniform(732, 770)
    A.el((x-1, y-1, x+1, y+1), fill=(248, 218, 168))
# butter knife
A.poly([(688, 766), (742, 748), (748, 756), (696, 776)], fill=(195, 198, 190), outline=(126, 130, 121), width=1.5)
A.rr((668, 765, 704, 781), 5, fill=(138, 89, 53), outline=(88, 57, 37), width=1.5)
A.ln([(700, 756), (738, 753)], (246, 246, 231), 2)


# --- two mugs + steam
def mug(cx, base_y, w, h, body_col, accent, handle_side=1):
    x0, x1 = cx-w/2, cx+w/2
    y0, y1 = base_y-h, base_y
    A.shadow((x0-10, y1-9, x1+22, y1+15), 7, 50, (73, 48, 34), (3, 4))
    # handle
    hb = (x1-4, y0+20, x1+34, y0+70) if handle_side > 0 else (x0-30, y0+20, x0+8, y0+70)
    A.arc(hb, 270 if handle_side > 0 else 90, 90 if handle_side > 0 else 270, body_col, 8)
    A.arc(hb, 270 if handle_side > 0 else 90, 90 if handle_side > 0 else 270, mix(body_col, (255, 245, 225), .35), 2)
    # body
    A.grad_rect((x0, y0, x1, y1), 12, mix(body_col, (255, 248, 232), .22), mix(body_col, (74, 47, 33), .12), True, (97, 68, 49), 2)
    # top ellipse
    A.el((x0+2, y0-9, x1-2, y0+11), fill=mix(body_col, (255, 250, 238), .32), outline=(97, 68, 49), width=1.5)
    A.el((x0+8, y0-4, x1-8, y0+6), fill=(86, 59, 42))
    A.el((x0+9, y0-2, x1-11, y0+4), fill=(122, 78, 48))
    # accent stripe
    A.arc((x0+2, y0+h*0.52, x1-2, y1-2), 10, 170, accent, 3)
    A.ln([(x0+8, y0+18), (x0+8, y1-16)], mix(body_col, (255, 250, 238), .38), 3)

mug(1002, 806, 65, 92, (229, 218, 198), (181, 103, 73), 1)
mug(1092, 808, 59, 78, (187, 108, 76), (224, 174, 115), -1)

# steam
steam_layer = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
sd = ImageDraw.Draw(steam_layer)
# small feathery curls
for path, alpha, wdt in [
    (bezier((992, 708), (984, 690), (998, 680), (994, 660), 38), 155, 3.4),
    (bezier((1004, 708), (1012, 688), (998, 676), (1006, 654), 38), 100, 2.5),
    (bezier((1016, 710), (1022, 692), (1010, 682), (1016, 668), 30), 75, 2),
    (bezier((1084, 726), (1076, 708), (1092, 696), (1086, 674), 34), 145, 3.2),
    (bezier((1097, 726), (1106, 704), (1090, 692), (1098, 670), 34), 95, 2.5),
    (bezier((1108, 728), (1114, 712), (1102, 704), (1108, 690), 26), 65, 2),
]:
    sd.line([(x*S, y*S) for x, y in path], fill=rgba((255, 252, 244), alpha), width=max(1, int(wdt*S)), joint="curve")
steam_layer = steam_layer.filter(ImageFilter.GaussianBlur(3.2*S))
A.comp(steam_layer)

# --- crock with wooden spoons & a little jar, between board and mugs
A.shadow((904, 772, 956, 808), 7, 45, (73, 48, 34), (2, 4))
A.grad_rect((902, 738, 950, 806), 8, (164, 179, 148), (111, 131, 105), True, (82, 101, 78), 2)
A.el((904, 730, 948, 750), fill=(148, 164, 137), outline=(82, 101, 78), width=2)
for x, top in [(912, 690), (926, 680), (938, 696)]:
    A.ln([(x, 742), (x+random.uniform(-3, 3), top)], (176, 130, 75), 3)
    A.el((x-5, top-4, x+5, top+4), fill=(195, 150, 91), outline=(125, 87, 51), width=1)
A.ln([(910, 758), (910, 792)], (203, 214, 187), 2)


# --- vase of wildflowers
A.shadow((1136, 772, 1236, 812), 10, 55, (73, 48, 34), (3, 4))
# stems first
stems = [
    bezier((1182, 776), (1160, 706), (1165, 624), (1148, 568), 60),
    bezier((1188, 776), (1188, 708), (1198, 632), (1192, 552), 60),
    bezier((1196, 776), (1212, 702), (1206, 638), (1230, 578), 60),
    bezier((1202, 776), (1224, 724), (1240, 664), (1258, 608), 60),
    bezier((1178, 776), (1150, 716), (1130, 662), (1112, 612), 60),
]
for st in stems:
    A.ln(st, (103, 130, 84), 2.5)
# leaves
for x, y, ang in [(1168, 682, -0.7), (1200, 654, 0.8), (1218, 710, 0.6), (1154, 660, -0.5), (1238, 656, 0.9), (1194, 690, -0.8)]:
    A.el((x-13, y-5, x+13, y+5), fill=(113, 143, 91), outline=(77, 106, 70), width=1)
# flowers
flowers = [(1148, 568, 20, (246, 227, 187), (220, 157, 66)),
           (1192, 552, 23, (248, 236, 206), (214, 143, 62)),
           (1230, 578, 18, (238, 191, 139), (182, 104, 60)),
           (1258, 608, 17, (243, 211, 160), (203, 138, 68)),
           (1112, 612, 19, (250, 235, 202), (215, 157, 76)),
           (1214, 604, 15, (226, 175, 149), (173, 98, 66)),
           (1170, 604, 14, (249, 238, 208), (213, 160, 73))]
for fx, fy, fr, petal, center in flowers:
    for k in range(7):
        a = 2*math.pi*k/7
        px, py = fx + 9*math.cos(a), fy + 9*math.sin(a)
        A.el((px-8, py-7, px+8, py+7), fill=petal, outline=mix(petal, (126, 92, 66), .35), width=1)
    A.el((fx-5, fy-5, fx+5, fy+5), fill=center, outline=(154, 100, 49), width=1.2)
# small buds
for bx, by in [(1132, 590), (1244, 594), (1180, 578), (1220, 640)]:
    A.el((bx-4, by-4, bx+4, by+4), fill=(223, 155, 121), outline=(157, 95, 66), width=1)
# vase
A.grad_rect((1148, 704, 1236, 806), 24, (238, 223, 199), (189, 167, 139), True, (141, 113, 87), 2)
A.rr((1150, 690, 1234, 722), 10, fill=(226, 208, 181), outline=(156, 128, 98), width=2)
A.el((1156, 691, 1228, 708), fill=(123, 91, 66))
A.arc((1154, 700, 1230, 724), 0, 180, (241, 226, 205), 3)
# vase decoration
A.arc((1162, 730, 1224, 784), 15, 165, (180, 119, 87), 3)
A.ln([(1166, 724), (1164, 778)], (255, 246, 229), 3)
# reflections
A.ln([(1174, 736), (1172, 782)], (248, 238, 219), 2)


# --- small lemon + knife on board? already. Add scattered flour specks
for _ in range(35):
    x = random.uniform(700, 950); y = random.uniform(790, 803)
    A.el((x-1.4, y-1, x+1.4, y+1), fill=(242, 226, 196))


# =========================================================
# LIGHT: beams, glow, window patch, vignette, texture
# =========================================================
# golden beams from the window (soft)
beam = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
bd = ImageDraw.Draw(beam)
bd.polygon([(180*S, 150*S), (410*S, 140*S), (1010*S, 810*S), (620*S, 880*S)],
           fill=rgba((255, 224, 158), 22))
bd.polygon([(470*S, 150*S), (620*S, 145*S), (1170*S, 760*S), (930*S, 830*S)],
           fill=rgba((255, 231, 174), 15))
bd.polygon([(210*S, 430*S), (660*S, 420*S), (1120*S, 860*S), (770*S, 890*S)],
           fill=rgba((255, 219, 151), 11))
beam = beam.filter(ImageFilter.GaussianBlur(30*S))
# sunlight streams into the room, not across the view outside
room_mask = Image.new("L", (IW, IH), 255)
rmd = ImageDraw.Draw(room_mask)
rmd.rounded_rectangle(sbox((88, 48, 884, 762)), radius=18*S, fill=0)
room_mask = room_mask.filter(ImageFilter.GaussianBlur(12*S))
beam.putalpha(ImageChops.multiply(beam.getchannel("A"), room_mask))
A.comp(beam)

# bright patch on counter and wall
patch = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
pd = ImageDraw.Draw(patch)
pd.polygon([(690*S, 760*S), (1120*S, 760*S), (1250*S, 890*S), (760*S, 900*S)],
           fill=rgba((255, 230, 174), 38))
pd.polygon([(510*S, 90*S), (710*S, 90*S), (850*S, 420*S), (610*S, 430*S)],
           fill=rgba((255, 241, 204), 20))
patch = patch.filter(ImageFilter.GaussianBlur(24*S))
patch.putalpha(ImageChops.multiply(patch.getchannel("A"), room_mask))
A.comp(patch)

# little dust motes in the light
motes = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
md = ImageDraw.Draw(motes)
for _ in range(90):
    x = random.uniform(300, 1130); y = random.uniform(120, 820)
    r = random.uniform(0.8, 3.0)
    a = random.randint(25, 110)
    md.ellipse([(x-r)*S, (y-r)*S, (x+r)*S, (y+r)*S], fill=rgba((255, 241, 205), a))
motes = motes.filter(ImageFilter.GaussianBlur(1.1*S))
A.comp(motes)

# a broad shaft of morning sun crossing the room
morning = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
mrd = ImageDraw.Draw(morning)
mrd.polygon([(782*S, 680*S), (842*S, 652*S), (1268*S, 1088*S), (1012*S, 1145*S)],
            fill=rgba((255, 226, 170), 17))
mrd.polygon([(704*S, 782*S), (1138*S, 788*S), (1325*S, 958*S), (772*S, 946*S)],
            fill=rgba((255, 220, 158), 20))
mrd.polygon([(1018*S, 1188*S), (1180*S, 1188*S), (1110*S, 1118*S), (992*S, 1118*S)],
            fill=rgba((255, 231, 178), 16))
morning = morning.filter(ImageFilter.GaussianBlur(30*S))
A.comp(morning)

# foreground warm bounce
A.glow((380, 880), 300, (255, 197, 127), 14, 90)
A.glow((1200, 920), 300, (255, 213, 155), 14, 90)

# vignette corners
vig = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
vd = ImageDraw.Draw(vig)
# dark edges drawn as big thick rounded frame
for i in range(16):
    inset = i * 18 * S
    a = int(5 + i*1.1)
    vd.rounded_rectangle([inset, inset, IW-inset, IH-inset], radius=120*S,
                         outline=rgba((87, 57, 34), a), width=25*S)
vig = vig.filter(ImageFilter.GaussianBlur(36*S))
A.comp(vig)

# subtle canvas paper grain
noise = Image.effect_noise((IW, IH), 20).convert("L")
noise_rgb = Image.new("RGBA", (IW, IH), (0, 0, 0, 0))
noise_rgb.paste(Image.merge("RGBA", (noise, Image.new("L", (IW, IH), 172), Image.new("L", (IW, IH), 120), Image.new("L", (IW, IH), 26))), (0, 0))
# blend with low alpha, warm-tinted via colorize-ish approach
paper = Image.new("RGBA", (IW, IH), (120, 86, 55, 0))
paper.putalpha(noise.point(lambda v: int(abs(v-128) * 0.12)))
A.comp(paper)

# gentle warm color grade
grade = Image.new("RGBA", (IW, IH), (255, 190, 115, 14))
A.comp(grade)

# downscale for final smoothness
final = A.img.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
# a gentle editorial grade: a little more warmth and depth
final = ImageEnhance.Color(final).enhance(1.09)
final = ImageEnhance.Contrast(final).enhance(1.035)
final = ImageEnhance.Brightness(final).enhance(1.005)
final = ImageEnhance.Sharpness(final).enhance(1.04)
final.save("cozy_kitchen_morning.png", optimize=True)
print("saved", final.size)
