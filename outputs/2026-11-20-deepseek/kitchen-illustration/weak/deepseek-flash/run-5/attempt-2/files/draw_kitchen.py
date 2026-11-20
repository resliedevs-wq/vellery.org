from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math, random

# ----------------------------------------------------------------------------
# Cozy Kitchen in the Morning -- a hand-built digital painting in Pillow
# ----------------------------------------------------------------------------
W, H = 1600, 1200
S = 2
CW, CH = W * S, H * S
random.seed(19)

base = Image.new("RGBA", (CW, CH), (245, 231, 211, 255))


def pt(p):
    return (int(round(p[0] * S)), int(round(p[1] * S)))


def pts(points):
    return [pt(p) for p in points]


def bx(b):
    return (int(round(b[0] * S)), int(round(b[1] * S)),
            int(round(b[2] * S)), int(round(b[3] * S)))


def C(c, a=255):
    if isinstance(c, tuple):
        if len(c) == 4:
            return c
        return (c[0], c[1], c[2], a)
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), a)


def mix(c1, c2, t):
    a = C(c1); b = C(c2)
    return (int(a[0] + (b[0] - a[0]) * t),
            int(a[1] + (b[1] - a[1]) * t),
            int(a[2] + (b[2] - a[2]) * t),
            int(a[3] + (b[3] - a[3]) * t))


def gradient_size(w, h, c1, c2, horizontal=False, stops=None):
    """Return RGB gradient image of given pixel size."""
    if stops is None:
        stops = [(0.0, C(c1)), (1.0, C(c2))]
    stops = sorted(stops, key=lambda s: s[0])
    im = Image.new("RGBA", (max(1, w), max(1, h)))
    px = im.load()
    n = w if horizontal else h
    for i in range(n):
        t = i / max(1, n - 1)
        # find stop pair
        k = 0
        while k < len(stops) - 2 and t > stops[k + 1][0]:
            k += 1
        t0, c0 = stops[k]
        t1, c1_ = stops[min(k + 1, len(stops) - 1)]
        f = 0 if t1 == t0 else (t - t0) / (t1 - t0)
        col = mix(c0, c1_, max(0, min(1, f)))
        if horizontal:
            for j in range(h):
                px[i, j] = col
        else:
            for j in range(w):
                px[j, i] = col
    return im


def grad_rect(im, b, c1, c2, radius=0, horizontal=False, stops=None, alpha=255):
    x0, y0, x1, y1 = bx(b)
    x0 = max(0, x0); y0 = max(0, y0); x1 = min(CW, x1); y1 = min(CH, y1)
    if x1 <= x0 or y1 <= y0:
        return
    g = gradient_size(x1 - x0, y1 - y0, c1, c2, horizontal, stops)
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    md = ImageDraw.Draw(mask)
    r = int(radius * S)
    if r > 0:
        md.rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), radius=r, fill=alpha)
    else:
        md.rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), fill=alpha)
    g.putalpha(mask)
    im.alpha_composite(g, (x0, y0))


def grad_poly(im, points, c1, c2, horizontal=False, stops=None, alpha=255, soft=0):
    pp = pts(points)
    x0 = max(0, min(p[0] for p in pp) - soft * 3)
    y0 = max(0, min(p[1] for p in pp) - soft * 3)
    x1 = min(CW, max(p[0] for p in pp) + soft * 3)
    y1 = min(CH, max(p[1] for p in pp) + soft * 3)
    if x1 <= x0 or y1 <= y0:
        return
    g = gradient_size(x1 - x0, y1 - y0, c1, c2, horizontal, stops)
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(p[0] - x0, p[1] - y0) for p in pp], fill=alpha)
    if soft:
        mask = mask.filter(ImageFilter.GaussianBlur(soft * S))
    g.putalpha(mask)
    im.alpha_composite(g, (x0, y0))


def grad_ring(im, b_out, b_in, r_out, r_in, c1, c2, horizontal=False, stops=None):
    """Gradient ring between an outer and an inner rounded rectangle."""
    x0, y0, x1, y1 = bx(b_out)
    x0 = max(0, x0); y0 = max(0, y0); x1 = min(CW, x1); y1 = min(CH, y1)
    if x1 <= x0 or y1 <= y0:
        return
    g = gradient_size(x1 - x0, y1 - y0, c1, c2, horizontal, stops)
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), radius=int(r_out * S), fill=255)
    ix0, iy0, ix1, iy1 = bx(b_in)
    md.rounded_rectangle((ix0 - x0, iy0 - y0, ix1 - x0, iy1 - y0),
                         radius=int(r_in * S), fill=0)
    g.putalpha(mask)
    im.alpha_composite(g, (x0, y0))


def soft_shape(im, draw_fn, color, blur=10, offset=(0, 0)):
    """Blurred translucent silhouette. draw_fn receives a scaled ImageDraw."""
    pad = int(blur * 4 * S)
    x0, y0, x1, y1 = CW, CH, 0, 0
    # ask draw_fn to give bbox through a temporary big canvas? use bounds args instead
    return


def soft_poly_shadow(im, points, color=(55, 35, 22), alpha=90, blur=14, offset=(8, 12)):
    pp = pts(points)
    ox, oy = int(offset[0] * S), int(offset[1] * S)
    pad = int(blur * 4 * S) + max(abs(ox), abs(oy))
    x0 = max(0, min(p[0] for p in pp) + ox - pad)
    y0 = max(0, min(p[1] for p in pp) + oy - pad)
    x1 = min(CW, max(p[0] for p in pp) + ox + pad)
    y1 = min(CH, max(p[1] for p in pp) + oy + pad)
    if x1 <= x0 or y1 <= y0:
        return
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(p[0] + ox - x0, p[1] + oy - y0) for p in pp], fill=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(blur * S))
    tile = Image.new("RGBA", mask.size, C(color))
    tile.putalpha(mask)
    im.alpha_composite(tile, (x0, y0))


def soft_ellipse_shadow(im, b, color=(55, 35, 22), alpha=90, blur=14, offset=(8, 12)):
    x0, y0, x1, y1 = b
    cx, cy = (x0 + x1) / 2 + offset[0], (y0 + y1) / 2 + offset[1]
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    points = [(cx + rx * math.cos(a), cy + ry * math.sin(a))
              for a in [i * math.tau / 48 for i in range(48)]]
    soft_poly_shadow(im, points, color, alpha, blur, (0, 0))


def rr(d, b, r, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = bx(b)
    d.rounded_rectangle((x0, y0, x1, y1), radius=int(r * S),
                        fill=C(fill) if fill else None,
                        outline=C(outline) if outline else None,
                        width=max(1, int(width * S)))


def el(d, b, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = bx(b)
    d.ellipse((x0, y0, x1, y1), fill=C(fill) if fill else None,
              outline=C(outline) if outline else None, width=max(1, int(width * S)))


def pg(d, points, fill=None, outline=None, width=1):
    pp = pts(points)
    d.polygon(pp, fill=C(fill) if fill else None)
    if outline:
        d.line(pp + [pp[0]], fill=C(outline), width=max(1, int(width * S)), joint="curve")


def ln(d, points, fill, width=2, joint="curve"):
    d.line(pts(points), fill=C(fill), width=max(1, int(width * S)), joint=joint)


def arc(d, b, start, end, fill, width=2):
    d.arc(bx(b), start=start, end=end, fill=C(fill), width=max(1, int(width * S)))


def bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt**3*p0[0] + 3*mt**2*t*p1[0] + 3*mt*t**2*p2[0] + t**3*p3[0]
        y = mt**3*p0[1] + 3*mt**2*t*p1[1] + 3*mt*t**2*p2[1] + t**3*p3[1]
        out.append((x, y))
    return out


def glow(im, center, radius, color, alpha=90, aspect=1.0, blur=None):
    cx, cy = center
    rx, ry = radius, radius * aspect
    b = (cx - rx, cy - ry, cx + rx, cy + ry)
    x0, y0, x1, y1 = bx(b)
    x0 = max(0, x0); y0 = max(0, y0); x1 = min(CW, x1); y1 = min(CH, y1)
    if x1 <= x0 or y1 <= y0:
        return
    w, h = x1 - x0, y1 - y0
    # smooth radial falloff from a small mask (fast and much softer than bands)
    gw = max(12, min(128, w // (2 * S)))
    gh = max(12, min(128, h // (2 * S)))
    small = Image.new("L", (gw, gh), 0)
    sp = small.load()
    for yy in range(gh):
        vy = (yy + .5) / gh * 2 - 1
        for xx in range(gw):
            vx = (xx + .5) / gw * 2 - 1
            d = min(1.0, math.hypot(vx, vy))
            sp[xx, yy] = int(alpha * (1 - d) ** 2.1)
    mask = small.resize((w, h), Image.BICUBIC)
    if blur is None:
        blur = max(1, int(min(rx, ry) * 0.16))
    mask = mask.filter(ImageFilter.GaussianBlur(blur * S))
    tile = Image.new("RGBA", (w, h), C(color))
    tile.putalpha(mask)
    im.alpha_composite(tile, (x0, y0))

def screen_light(im, mask, color, strength=255):
    """Screen a warm color through a grayscale mask (adds real light)."""
    rgb = im.convert("RGB")
    light = Image.new("RGB", rgb.size, C(color)[:3])
    scr = ImageChops.screen(rgb, light)
    m = mask.point(lambda a: min(255, int(a * strength / 255)))
    out = Image.composite(scr.convert("RGBA"), im, m)
    return out


def clipped_texture(im, box, draw_fn, alpha=30):
    x0, y0, x1, y1 = bx(box)
    w, h = x1 - x0, y1 - y0
    if w <= 0 or h <= 0:
        return
    tile = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    draw_fn(td, w, h)
    tile.putalpha(tile.getchannel("A").point(lambda a: a * alpha // 255))
    im.alpha_composite(tile, (x0, y0))


# ============================================================================
# 1. WALL
# ============================================================================
grad_rect(base, (0, 0, W, H), "#e5c5a1", "#c99a73",
          stops=[(0.0, C("#e8caa7")), (0.45, C("#ddba93")),
                 (0.78, C("#cfaa83")), (1.0, C("#b78967"))])
# broad ambient washes
glow(base, (700, 330), 750, "#ffdca0", 44, aspect=0.85, blur=90)
glow(base, (1310, 180), 500, "#ffc987", 24, blur=80)
glow(base, (160, 570), 420, "#8b6a58", 50, blur=90)
glow(base, (1460, 820), 420, "#9a6f51", 44, blur=90)

# subtle plaster mottling
for _ in range(85):
    x = random.uniform(0, W); y = random.uniform(0, H)
    r = random.uniform(30, 150)
    c = random.choice(["#f4dcb9", "#c49a75", "#efcfaa", "#d5ad88"])
    glow(base, (x, y), r, c, random.randint(5, 12), aspect=random.uniform(.4, 1.1),
         blur=int(r * .5))

# wall shadow around window (painted before the view so the glass stays clear)
soft_poly_shadow(base, [(214, 64), (1078, 64), (1078, 662), (214, 662)],
                 (55, 34, 20), 105, 18, (16, 22))

# ============================================================================
# 2. WINDOW VIEW
# ============================================================================
win = (250, 108, 1038, 630)
grad_rect(base, win, "#7fb3c6", "#f9d697",
          stops=[(0, C("#78afc4")), (.38, C("#b8d1cd")),
                 (.62, C("#e8d9b6")), (.82, C("#f8d59c")), (1, C("#efc17f"))])
# soft morning clouds
cloud = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); cd = ImageDraw.Draw(cloud)
cloud_groups = [
    (646, 276, 250, 20, 52, 18),
    (968, 322, 210, 15, 42, 14),
    (472, 344, 180, 13, 38, 12),
    (790, 142, 160, 12, 26, 10),
]
for (cx, cy, w, h, a, n) in cloud_groups:
    for j in range(5):
        ox = (j - 2) * w * .17
        oy = math.sin(j * 1.7 + cx) * h * .28
        rw = w * (.30 + .07 * (j % 2))
        rh = h * (.65 + .13 * ((j + 1) % 3))
        cd.ellipse(bx((cx + ox - rw, cy + oy - rh, cx + ox + rw, cy + oy + rh)),
                   fill=(255, 246, 229, a))
    cd.ellipse(bx((cx - w * .38, cy - h * .4, cx + w * .38, cy + h * .4)),
               fill=(255, 247, 233, a + 6))
cloud = cloud.filter(ImageFilter.GaussianBlur(8 * S))
base.alpha_composite(cloud)
for (cx, cy, w, h, a, n) in cloud_groups:
    glow(base, (cx - w * .18, cy - 2), w * .28, "#fff8e8", 16, aspect=.6, blur=10)

# sun and cloud haze
glow(base, (874, 218), 250, "#ffda91", 76, blur=55)
glow(base, (874, 218), 95, "#ffeec0", 120, blur=24)
for rr_, a in [(68, 24), (48, 30), (34, 38)]:
    glow(base, (874, 218), rr_, "#fff5cf", a, blur=10)
el(ImageDraw.Draw(base), (844, 188, 904, 248), "#ffeab4")
el(ImageDraw.Draw(base), (852, 195, 896, 241), "#fff8dd")
el(ImageDraw.Draw(base), (859, 203, 889, 233), "#fffdf2")
# delicate sun rays
ray_ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); rd = ImageDraw.Draw(ray_ov)
for ang in range(8, 176, 14):
    a = math.radians(ang)
    p0 = (874 + math.cos(a) * 58, 218 + math.sin(a) * 58)
    p1 = (874 + math.cos(a) * 200, 218 + math.sin(a) * 200)
    rd.line(pts([p0, p1]), fill=(255, 239, 187, 18), width=int(2.0 * S))
ray_ov = ray_ov.filter(ImageFilter.GaussianBlur(5 * S))
base.alpha_composite(ray_ov)
for cx, cy, w, h, al in [(770, 165, 180, 24, 28), (935, 285, 200, 18, 20),
                          (575, 240, 190, 18, 18), (350, 300, 230, 24, 20)]:
    glow(base, (cx, cy), max(w, h) * .55, "#fff6da", al, aspect=h / w, blur=22)
# warm horizon
glow(base, (870, 470), 480, "#ffdc99", 28, aspect=.32, blur=55)

# distant hills
def hill(ybase, amp, phase, color, alpha=255):
    p = []
    for i in range(0, 81):
        x = 250 + (1040 - 250) * i / 80
        y = ybase + amp * math.sin(i / 80 * math.tau * 1.2 + phase) + amp * .35 * math.sin(i / 80 * math.tau * 3.1 + phase * 2)
        p.append((x, y))
    p += [(1040, 630), (250, 630)]
    pg(ImageDraw.Draw(base), p, color)

hill(432, 20, 0.7, "#b4c18c")
hill(472, 24, 2.4, "#91a771")
hill(518, 18, 4.1, "#718f58")

# meadow + garden path
pg(ImageDraw.Draw(base), [(250, 555), (1040, 540), (1040, 630), (250, 630)], "#78934e")
pg(ImageDraw.Draw(base), [(250, 585), (400, 552), (560, 560), (700, 590), (830, 566),
                          (1040, 582), (1040, 630), (250, 630)], "#93a45d")
pg(ImageDraw.Draw(base), [(650, 630), (700, 605), (760, 589), (810, 592),
                          (790, 630)], "#cdbb7c")

# distant trees
def tree(cx, cy, scale, dark, light, alpha=255):
    # trunk
    ln(ImageDraw.Draw(base), [(cx, cy + 8 * scale), (cx - 2 * scale, cy + 40 * scale)],
       "#6b7150", 3 * scale)
    for i in range(9):
        a = i / 9 * math.tau
        dx = math.cos(a) * 20 * scale + random.uniform(-6, 6) * scale
        dy = math.sin(a) * 13 * scale + random.uniform(-5, 5) * scale
        r = random.uniform(13, 24) * scale
        el(ImageDraw.Draw(base), (cx + dx - r, cy + dy - r * .8,
                                  cx + dx + r, cy + dy + r * .8),
           dark if i % 2 else light)
    glow(base, (cx + 8 * scale, cy - 5 * scale), 28 * scale, "#ffe1a1", 18, blur=10)

tree(340, 490, 1.25, "#4f6d45", "#71915a")
tree(945, 475, 1.6, "#43603e", "#64854f")
tree(1010, 505, 1.0, "#405a39", "#688a4e")
tree(560, 500, .65, "#6d8656", "#8ca068")
tree(760, 505, .52, "#77905d", "#93a66f")

# tiny fence
for i in range(8):
    x = 650 + i * 47
    ln(ImageDraw.Draw(base), [(x, 545), (x - 1, 574)], "#7f7957", 3)
ln(ImageDraw.Draw(base), [(650, 554), (980, 546)], "#8c845f", 2)
ln(ImageDraw.Draw(base), [(650, 565), (980, 558)], "#8c845f", 2)

# a small cottage tucked into the hills
soft_ellipse_shadow(base, (465, 458, 590, 505), (68, 56, 35), 55, 7, (5, 5))
pg(ImageDraw.Draw(base), [(472, 459), (528, 425), (588, 459), (576, 468), (482, 468)],
   "#a4603f")
pg(ImageDraw.Draw(base), [(480, 458), (528, 431), (578, 458)], "#c47b50")
grad_rect(base, (484, 460, 574, 502), "#d8c39e", "#ab916e")
pg(ImageDraw.Draw(base), [(482, 459), (576, 459), (576, 468), (482, 468)], "#8c6b4d")
# chimney
grad_rect(base, (548, 422, 564, 451), "#b09a78", "#806b50")
pg(ImageDraw.Draw(base), [(546, 422), (566, 422), (562, 416), (550, 416)], "#7a5f45")
# warm windows and door
rr(ImageDraw.Draw(base), (497, 472, 516, 488), 1, "#f3c56e")
rr(ImageDraw.Draw(base), (542, 472, 560, 488), 1, "#f3c56e")
rr(ImageDraw.Draw(base), (523, 474, 537, 501), 1, "#77543b")
ln(ImageDraw.Draw(base), [(530, 474), (530, 500)], "#5e402e", 1)
glow(base, (507, 479), 18, "#ffd087", 40, blur=7)
glow(base, (551, 479), 18, "#ffd087", 34, blur=7)
# chimney smoke
smoke = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); sm = ImageDraw.Draw(smoke)
pth = bez((556, 415), (570, 398), (546, 378), (562, 358), 30)
sm.line(pts(pth), fill=(248, 236, 214, 42), width=int(4 * S), joint="curve")
smoke = smoke.filter(ImageFilter.GaussianBlur(5 * S)); base.alpha_composite(smoke)

# wildflowers and grass flecks
for _ in range(70):
    x = random.uniform(270, 1020); y = random.uniform(555, 626)
    c = random.choice(["#d8c890", "#e4d5a3", "#b2ba7e", "#7d8f63"])
    el(ImageDraw.Draw(base), (x, y, x + random.uniform(2, 5), y + random.uniform(2, 4)), c)

# foreground branch, top left
branch = bez((250, 160), (320, 190), (405, 170), (470, 215), 40)
ln(ImageDraw.Draw(base), branch, "#5e6245", 4)
for t in [0.15, 0.32, 0.52, 0.7, 0.86]:
    p = branch[int(t * (len(branch) - 1))]
    ln(ImageDraw.Draw(base), [(p[0], p[1]), (p[0] + 15, p[1] - 18)], "#5e6245", 2)
leaves = [(268, 165, 8), (296, 181, 9), (315, 197, 8), (334, 183, 7),
          (353, 177, 9), (372, 184, 8), (393, 180, 9), (414, 193, 8),
          (433, 202, 9), (452, 205, 7), (464, 194, 6), (288, 198, 7),
          (375, 201, 7), (410, 207, 6)]
for lx, ly, r in leaves:
    el(ImageDraw.Draw(base), (lx - r, ly - r * .55, lx + r, ly + r * .6), "#5f7048")
    el(ImageDraw.Draw(base), (lx - r * .7, ly - r * .4, lx + r * .3, ly + r * .1), "#7b8a58")
    ln(ImageDraw.Draw(base), [(lx - r * .8, ly), (lx + r * .7, ly - 1)], "#4b5c3c", 1)
    arc(ImageDraw.Draw(base), (lx - r * .9, ly - r * .6, lx + r * .2, ly + r * .1),
        200, 340, "#b9b97f", 1)
# a few berries
for (lx, ly) in [(282, 184), (343, 194), (405, 196)]:
    el(ImageDraw.Draw(base), (lx - 3, ly - 3, lx + 3, ly + 3), "#a56a4d")
    el(ImageDraw.Draw(base), (lx - 2, ly - 2, lx, ly), "#d89d74")

# two tiny birds
for (bx_, by_, sc) in [(680, 155, 1.0), (725, 132, .8)]:
    arc(ImageDraw.Draw(base), (bx_ - 11 * sc, by_ - 6 * sc, bx_, by_ + 6 * sc),
        195, 345, "#6f715c", 2 * sc)
    arc(ImageDraw.Draw(base), (bx_, by_ - 6 * sc, bx_ + 11 * sc, by_ + 6 * sc),
        195, 345, "#6f715c", 2 * sc)

# soft glass reflection

glass = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
gd = ImageDraw.Draw(glass)
gd.polygon(pts([(355, 108), (520, 108), (405, 630), (268, 630)]), fill=(255, 250, 230, 14))
gd.polygon(pts([(790, 108), (845, 108), (700, 630), (650, 630)]), fill=(255, 250, 230, 10))
base.alpha_composite(glass)

# ============================================================================
# 3. WINDOW FRAME, SILL, CURTAINS
# ============================================================================
# outer casing -- ring, so the morning view stays visible
grad_ring(base, (218, 72, 1074, 660), (246, 100, 1046, 632), 13, 7,
          "#dec29b", "#b68a61", stops=[(0, C("#e4caa5")), (.55, C("#cfae86")),
                                       (1, C("#ae825a"))])
rr(ImageDraw.Draw(base), (226, 80, 1066, 652), 10, None, "#8f6645", 2)
rr(ImageDraw.Draw(base), (232, 86, 1060, 646), 8, None, "#f8edda", 2)
# pane frame ring
grad_ring(base, (240, 94, 1052, 638), (258, 110, 1034, 622), 7, 2,
          "#f5e8cf", "#ddc6a4", stops=[(0, C("#fbf0d9")), (.6, C("#ecdcbe")),
                                       (1, C("#d3b993"))])
rr(ImageDraw.Draw(base), (242, 96, 1050, 636), 6, None, "#9e7554", 2)
rr(ImageDraw.Draw(base), (252, 104, 1040, 628), 4, None, "#a47b58", 2)
# muntins with shadows
soft_poly_shadow(base, [(639, 110), (653, 110), (653, 622), (639, 622)],
                 (60, 40, 25), 90, 4, (5, 5))
grad_rect(base, (635, 110, 657, 622), "#f2e4c8", "#d6bd99", radius=2, horizontal=True)
ln(ImageDraw.Draw(base), [(637, 112), (637, 620)], "#fff3dc", 2)
ln(ImageDraw.Draw(base), [(655, 112), (655, 620)], "#b08a65", 1)
soft_poly_shadow(base, [(258, 356), (1034, 356), (1034, 370), (258, 370)],
                 (60, 40, 25), 90, 4, (5, 5))
grad_rect(base, (258, 352, 1034, 374), "#f2e4c8", "#d3b994", radius=2)
ln(ImageDraw.Draw(base), [(260, 354), (1032, 354)], "#fff4df", 2)
ln(ImageDraw.Draw(base), [(260, 372), (1032, 372)], "#a98360", 1)
# inner window shadow (top)
sh = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
for i, a in enumerate([45, 28, 15]):
    sd.rectangle(bx((258, 110 + i * 4, 1034, 118 + i * 4)), fill=(46, 35, 24, a))
base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4 * S)))

# sill
soft_poly_shadow(base, [(206, 642), (1086, 642), (1086, 682), (206, 682)],
                 (55, 36, 24), 100, 9, (8, 10))
grad_rect(base, (208, 638, 1084, 678), "#c89863", "#956439", radius=5)
grad_rect(base, (208, 638, 1084, 650), "#e1b47d", "#c59563", radius=4)
ln(ImageDraw.Draw(base), [(214, 641), (1078, 641)], "#f4cfa0", 2)
grad_rect(base, (220, 672, 1072, 688), "#80532e", "#5f3c23", radius=3)
ln(ImageDraw.Draw(base), [(226, 675), (1066, 675)], "#a97948", 1)

# curtain rod
ln(ImageDraw.Draw(base), [(176, 44), (1102, 44)], "#5b4534", 6)
ln(ImageDraw.Draw(base), [(180, 40), (1098, 40)], "#a47d56", 2)
for cx in (178, 1100):
    el(ImageDraw.Draw(base), (cx - 12, 32, cx + 12, 56), "#6e523a")
    el(ImageDraw.Draw(base), (cx - 8, 34, cx + 4, 44), "#b68c5f")
# rod finial shadows
soft_ellipse_shadow(base, (160, 50, 1120, 80), (50, 30, 20), 65, 8, (0, 10))

def curtain(side):
    if side == "left":
        outer = [(188, 56), (334, 56), (324, 170), (310, 282), (284, 402),
                 (304, 470), (329, 538), (345, 632), (188, 632), (190, 500),
                 (192, 402), (196, 210)]
        tie_c = (284, 404)
    else:
        outer = [(962, 56), (1104, 56), (1104, 210), (1103, 402), (1104, 500),
                 (1108, 632), (950, 632), (967, 538), (992, 470), (1012, 402),
                 (986, 282), (972, 170)]
        tie_c = (1012, 404)
    soft_poly_shadow(base, outer, (60, 38, 24), 60, 12, (8, 10))
    grad_poly(base, outer, "#fbf0dc", "#d8c1a2", stops=[(0, C("#fcf3e1")),
              (.4, C("#f4e7d0")), (.75, C("#e5d1b3")), (1, C("#d1b796"))])
    # folds
    if side == "left":
        fold_specs = [(208, 210, 198, 630, 34, 48), (240, 170, 240, 630, 26, 38),
                      (272, 240, 278, 632, 24, 42), (306, 300, 320, 632, 17, 28)]
    else:
        fold_specs = [(1082, 210, 1090, 630, 34, 45), (1054, 170, 1052, 630, 26, 34),
                      (1024, 240, 1018, 632, 24, 38), (994, 300, 980, 632, 17, 25)]
    ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for (x0, y0, x1, y1, w, a) in fold_specs:
        pth = bez((x0, y0), (x0 - 8, y0 + 120), (x1 + 10, y1 - 100), (x1, y1), 30)
        od.line(pts(pth), fill=(100, 68, 43, a), width=int(w * .45 * S), joint="curve")
    ov = ov.filter(ImageFilter.GaussianBlur(9 * S))
    base.alpha_composite(ov)
    # bright folds
    ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for (x0, y0, x1, y1) in ([(222, 150, 222, 610), (257, 140, 262, 620),
                              (288, 230, 300, 620), (1080, 150, 1078, 610),
                              (1042, 150, 1038, 620), (1010, 230, 1002, 620)]):
        pth = bez((x0, y0), (x0 + 4, y0 + 150), (x1 + 2, y1 - 100), (x1, y1), 24)
        od.line(pts(pth), fill=(255, 247, 224, 36), width=int(9 * S), joint="curve")
    ov = ov.filter(ImageFilter.GaussianBlur(7 * S)); base.alpha_composite(ov)
    # embroidered sprigs
    for (sx, sy) in ([(246, 455), (270, 500), (1012, 470), (1036, 520)]):
        pth = bez((sx, sy), (sx + 6, sy + 16), (sx - 4, sy + 30), (sx + 2, sy + 44), 12)
        ln(ImageDraw.Draw(base), pth, "#a8a789", 2)
        for k in range(3):
            lx, ly = pth[4 + k * 3]
            el(ImageDraw.Draw(base), (lx - 6, ly - 3, lx + 2, ly + 4), "#96a07d")
    # rings at the curtain rod
    xs = range(207, 330, 21) if side == "left" else range(972, 1092, 21)
    for rx in xs:
        d = ImageDraw.Draw(base)
        d.ellipse(bx((rx - 5, 40, rx + 5, 54)), outline=C("#8a6a49"), width=max(1, int(1.5 * S)))
        d.arc(bx((rx - 5, 40, rx + 5, 54)), 190, 350, fill=C("#d4ae7b"), width=max(1, int(1.2 * S)))
    # gathered fabric tie-back
    tc = tie_c
    # gathered fabric bow tied at the cinch
    kx, ky = tie_c
    if side == "left":
        tail1 = [(kx - 4, ky + 4), (kx - 14, ky + 56), (kx - 9, ky + 84),
                 (kx - 2, ky + 78), (kx - 6, ky + 52), (kx + 2, ky + 6)]
        tail2 = [(kx + 4, ky + 5), (kx + 15, ky + 48), (kx + 11, ky + 72),
                 (kx + 4, ky + 68), (kx + 7, ky + 45), (kx - 1, ky + 6)]
        loop_l = [(kx, ky), (kx - 34, ky - 19), (kx - 29, ky + 8), (kx - 5, ky + 5)]
        loop_r = [(kx, ky), (kx + 27, ky - 16), (kx + 24, ky + 9), (kx + 4, ky + 5)]
    else:
        tail1 = [(kx + 4, ky + 4), (kx + 14, ky + 56), (kx + 9, ky + 84),
                 (kx + 2, ky + 78), (kx + 6, ky + 52), (kx - 2, ky + 6)]
        tail2 = [(kx - 4, ky + 5), (kx - 15, ky + 48), (kx - 11, ky + 72),
                 (kx - 4, ky + 68), (kx - 7, ky + 45), (kx + 1, ky + 6)]
        loop_l = [(kx, ky), (kx + 34, ky - 19), (kx + 29, ky + 8), (kx + 5, ky + 5)]
        loop_r = [(kx, ky), (kx - 27, ky - 16), (kx - 24, ky + 9), (kx - 4, ky + 5)]
    soft_ellipse_shadow(base, (kx - 30, ky - 20, kx + 27, ky + 16),
                        (64, 40, 25), 75, 5, (2, 4))
    # ribbon tails
    for tail, shade in [(tail1, "#a86b48"), (tail2, "#c1855d")]:
        pg(ImageDraw.Draw(base), tail, shade)
        ln(ImageDraw.Draw(base), [tail[0], tail[1], tail[2]], "#8b5337", 2)
        ln(ImageDraw.Draw(base), [tail[5], tail[4], tail[3]], "#d49a71", 1)
    # bow loops
    pg(ImageDraw.Draw(base), loop_l, "#b97954")
    pg(ImageDraw.Draw(base), loop_r, "#a96a47")
    pg(ImageDraw.Draw(base), [(kx - 19, ky - 9), (kx - 27, ky - 13),
                              (kx - 23, ky + 3), (kx - 5, ky + 2)], "#cf936b")
    pg(ImageDraw.Draw(base), [(kx + 16, ky - 8), (kx + 24, ky - 10),
                              (kx + 20, ky + 3), (kx + 5, ky + 2)], "#c78a61")
    # knot
    el(ImageDraw.Draw(base), (kx - 8, ky - 9, kx + 8, ky + 9), "#8f5538")
    el(ImageDraw.Draw(base), (kx - 5, ky - 7, kx + 3, ky + 1), "#cb9069")
    el(ImageDraw.Draw(base), (kx - 3, ky + 3, kx + 5, ky + 8), "#7b452e")
    # a few gathers pulled into the knot
    for ang in (-46, -22, 22, 46):
        r = math.radians(ang)
        p0 = (kx + math.cos(r) * 8, ky + math.sin(r) * 8)
        p1 = (kx + math.cos(r) * 31, ky + math.sin(r) * 25)
        ln(ImageDraw.Draw(base), [p0, p1], "#a98769", 1)

    # small top pleats where the curtain meets the rod
    xs0, xs1 = (198, 326) if side == "left" else (970, 1096)
    for px in range(xs0, xs1, 14):
        shade = "#ceb595" if (px // 14) % 2 else "#fff8e9"
        pth = bez((px, 58), (px + 2, 72), (px - 2, 84), (px + 1, 98), 8)
        ln(ImageDraw.Draw(base), pth, shade, 1)

curtain("left")
curtain("right")

# ============================================================================
# 4. CAT ON THE WINDOWSILL
# ============================================================================
soft_ellipse_shadow(base, (372, 596, 586, 650), (73, 46, 29), 100, 9, (5, 7))
# tail curls around front
tail = bez((520, 612), (596, 600), (576, 647), (500, 645), 35)
ln(ImageDraw.Draw(base), tail, "#a85f36", 17)
ln(ImageDraw.Draw(base), [(p[0], p[1] - 3) for p in tail], "#d88a50", 9)
# body
grad_poly(base, [(393, 606), (408, 574), (456, 558), (511, 568), (554, 592),
                 (562, 624), (538, 641), (457, 646), (405, 638)],
          "#e2a365", "#b8683f", stops=[(0, C("#eab073")), (.55, C("#d0874f")),
                                     (1, C("#a85c38"))])
# head
el(ImageDraw.Draw(base), (392, 563, 458, 624), "#e3a162")
el(ImageDraw.Draw(base), (401, 571, 452, 623), "#edb779")
# ears
pg(ImageDraw.Draw(base), [(397, 579), (396, 554), (417, 570)], "#c67a49")
pg(ImageDraw.Draw(base), [(435, 568), (454, 554), (453, 582)], "#c67a49")
pg(ImageDraw.Draw(base), [(400, 575), (400, 562), (410, 570)], "#e5a184")
pg(ImageDraw.Draw(base), [(441, 569), (449, 562), (449, 577)], "#e5a184")
# face
el(ImageDraw.Draw(base), (410, 590, 446, 617), "#f0c08c")
# closed eyes
for ex in (416, 434):
    arc(ImageDraw.Draw(base), (ex - 7, 589, ex + 5, 601), 10, 170, "#6d432d", 2)
# nose & mouth
pg(ImageDraw.Draw(base), [(426, 600), (432, 600), (429, 604)], "#b76a62")
ln(ImageDraw.Draw(base), [(429, 604), (429, 608), (424, 610)], "#86503d", 1)
ln(ImageDraw.Draw(base), [(429, 608), (434, 610)], "#86503d", 1)
# whiskers
for dy in (-3, 1, 5):
    ln(ImageDraw.Draw(base), [(414, 604 + dy), (390, 601 + dy * 2)], "#f4d8b1", 1)
    ln(ImageDraw.Draw(base), [(442, 604 + dy), (466, 601 + dy * 2)], "#f4d8b1", 1)
# stripes and fur
for (x0, y0, x1, y1) in [(449, 575, 467, 593), (470, 582, 491, 597), (493, 590, 514, 604),
                          (514, 599, 536, 611), (418, 568, 430, 578)]:
    ln(ImageDraw.Draw(base), [(x0, y0), (x1, y1)], "#b2683f", 5)
# paws tucked
el(ImageDraw.Draw(base), (436, 614, 482, 640), "#f0c18d")
ln(ImageDraw.Draw(base), [(451, 621), (450, 631)], "#cf9364", 1)
ln(ImageDraw.Draw(base), [(462, 620), (462, 631)], "#cf9364", 1)
# warm rim light
rim = bez((403, 634), (437, 646), (506, 646), (548, 632), 30)
ln(ImageDraw.Draw(base), rim, "#f8d59b", 2)
arc(ImageDraw.Draw(base), (394, 564, 459, 626), 190, 300, "#ffdb9f", 2)

# potted herb on right sill
soft_ellipse_shadow(base, (904, 620, 1002, 650), (55, 38, 23), 100, 7, (4, 6))
pg(ImageDraw.Draw(base), [(927, 620), (977, 620), (970, 648), (934, 648)], "#b56f4c")
pg(ImageDraw.Draw(base), [(932, 620), (968, 620), (963, 631), (937, 631)], "#8e5439")
grad_rect(base, (929, 617, 975, 629), "#d79469", "#b56f4c", radius=2)
for stem, ang in [((949, 620), -1.35), ((946, 620), -1.75), ((952, 620), -1.6),
                  ((944, 620), -2.0), ((956, 620), -1.15), ((940, 620), -1.2)]:
    ex = stem[0] + math.cos(ang) * 48; ey = stem[1] + math.sin(ang) * 48
    pth = bez((stem[0], stem[1]), (stem[0] + math.cos(ang) * 14, stem[1] - 15),
              (ex - 6, ey + 10), (ex, ey), 18)
    ln(ImageDraw.Draw(base), pth, "#587052", 2)
    for k in (8, 12, 16):
        px, py = pth[k]
        el(ImageDraw.Draw(base), (px - 8, py - 4, px + 7, py + 4), "#748b64")
        el(ImageDraw.Draw(base), (px - 5, py - 2, px + 4, py + 2), "#8ea077")
# tiny ceramic bird by the pot
el(ImageDraw.Draw(base), (886, 626, 906, 646), "#e8dfcb")
pg(ImageDraw.Draw(base), [(904, 630), (914, 624), (909, 638)], "#e8dfcb")
ln(ImageDraw.Draw(base), [(888, 638), (883, 646)], "#c7b89e", 2)

# ============================================================================
# 5. TILE BACKSPLASH
# ============================================================================
# under window
grad_rect(base, (40, 680, 1122, 800), "#d8c3a4", "#c3aa8a")
# tiles
tile_w, tile_h = 102, 52
for row in range(3):
    y = 680 + row * tile_h
    off = 0 if row % 2 == 0 else -tile_w // 2
    for col in range(-1, 12):
        x = 42 + col * tile_w + off
        if x > 1112:
            continue
        shade = random.choice(["#ede0ca", "#e8d8bf", "#f2e7d3", "#e4d4ba", "#eee2cd"])
        x0 = max(42, x + 2); x1 = min(1118, x + tile_w - 2)
        if x1 <= x0:
            continue
        grad_rect(base, (x0, y + 2, x1, y + tile_h - 2), shade,
                  mix(shade, "#c5ae8f", .28), radius=3)
        # top sheen and lower shadow
        ln(ImageDraw.Draw(base), [(x0 + 2, y + 4), (x1 - 3, y + 4)], "#fbf2df", 1)
        ln(ImageDraw.Draw(base), [(x0 + 2, y + tile_h - 4), (x1 - 3, y + tile_h - 4)], "#b89f81", 1)
        if random.random() < .25:
            glow(base, ((x0 + x1) / 2, y + 18), 20, "#ffffff", 18, aspect=.42, blur=8)
# tile group behind stove, up higher
grad_rect(base, (1122, 565, 1600, 800), "#c9ad89", "#b79a78")
for row in range(5):
    y = 565 + row * tile_h
    off = 0 if row % 2 == 0 else -tile_w // 2
    for col in range(-1, 5):
        x = 1122 + col * tile_w + off
        x0 = max(1122, x + 2); x1 = min(1600, x + tile_w - 2)
        if x1 <= x0:
            continue
        shade = random.choice(["#e5d2b6", "#dfc9aa", "#e9d8be", "#d8c1a1"])
        grad_rect(base, (x0, y + 2, x1, min(798, y + tile_h - 2)), shade,
                  mix(shade, "#b39470", .26), radius=3)
        ln(ImageDraw.Draw(base), [(x0 + 2, y + 4), (x1 - 3, y + 4)], "#f5e7cf", 1)
# counter shadow on tiles
sh = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
sd.rectangle(bx((30, 782, 1135, 800)), fill=(45, 28, 18, 100))
base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8 * S)))
# tile shelf/trim line
ln(ImageDraw.Draw(base), [(40, 678), (1122, 678)], "#b28f6a", 2)

# ============================================================================
# 6. CABINETS & COUNTER
# ============================================================================
# cabinet body
soft_poly_shadow(base, [(34, 835), (1124, 835), (1124, 1202), (34, 1202)],
                 (45, 31, 22), 100, 11, (0, 10))
grad_rect(base, (38, 838, 1118, 1205), "#758b77", "#465c4b",
          stops=[(0, C("#7b917c")), (.45, C("#637a66")), (1, C("#425747"))])
# vertical face frame edges
grad_rect(base, (38, 838, 1118, 856), "#8ca08a", "#617765")
# toe kick
grad_rect(base, (48, 1148, 1108, 1205), "#33463a", "#22322a")
ln(ImageDraw.Draw(base), [(48, 1148), (1108, 1148)], "#1e2c24", 4)

def cabinet_door(x0, y0, x1, y1, knob="right", knob_y=None, drawer=False):
    # stile/rail shadow
    grad_rect(base, (x0, y0, x1, y1), "#6f8672", "#4e6554")
    rr(ImageDraw.Draw(base), (x0, y0, x1, y1), 3, None, "#415747", 2)
    # inset panel
    inset = 10
    if drawer:
        grad_rect(base, (x0 + inset, y0 + inset, x1 - inset, y1 - inset),
                  "#5e7562", "#506857", radius=2)
        ln(ImageDraw.Draw(base), [(x0 + inset + 2, y0 + inset + 2),
                                  (x1 - inset - 2, y0 + inset + 2)], "#405646", 2)
        # cup pull
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2 + 2
        rr(ImageDraw.Draw(base), (cx - 22, cy - 7, cx + 22, cy + 7), 6, None, "#b58a51", 4)
        ln(ImageDraw.Draw(base), [(cx - 23, cy), (cx + 23, cy)], "#e0b878", 2)
        el(ImageDraw.Draw(base), (cx - 26, cy - 4, cx - 18, cy + 4), "#c79a5e")
        el(ImageDraw.Draw(base), (cx + 18, cy - 4, cx + 26, cy + 4), "#c79a5e")
    else:
        grad_rect(base, (x0 + inset, y0 + inset, x1 - inset, y1 - inset),
                  "#5c7360", "#526957", radius=2)
        rr(ImageDraw.Draw(base), (x0 + inset, y0 + inset, x1 - inset, y1 - inset),
           2, None, "#3d5343", 2)
        ln(ImageDraw.Draw(base), [(x0 + inset + 3, y0 + inset + 3),
                                  (x1 - inset - 3, y0 + inset + 3)], "#7c927c", 2)
        ln(ImageDraw.Draw(base), [(x0 + inset + 3, y1 - inset - 3),
                                  (x1 - inset - 3, y1 - inset - 3)], "#3a4e3f", 3)
        # brass knob
        kx = x1 - 24 if knob == "right" else x0 + 24
        ky = knob_y if knob_y is not None else (y0 + y1) / 2
        el(ImageDraw.Draw(base), (kx - 6, ky - 6, kx + 6, ky + 6), "#8d6636")
        el(ImageDraw.Draw(base), (kx - 4, ky - 4, kx + 4, ky + 4), "#c79a5c")
        el(ImageDraw.Draw(base), (kx - 3, ky - 4, kx + 1, ky - 1), "#efd19a")

# drawers + doors across
for (x0, x1) in [(60, 305), (327, 544), (566, 783), (805, 1022)]:
    cabinet_door(x0, 862, x1, 930, drawer=True)
for (x0, x1), knob in [((60, 305), "right"), ((327, 544), "right"),
                        ((566, 783), "right"), ((805, 1022), "right")]:
    cabinet_door(x0, 942, x1, 1138, knob=knob, knob_y=1038)
# narrow filler at right
cabinet_door(1038, 862, 1100, 930, drawer=True)
cabinet_door(1038, 942, 1100, 1138, knob="left", knob_y=1040)

# counter butcher block
soft_poly_shadow(base, [(18, 790), (1148, 790), (1148, 856), (18, 856)],
                 (42, 27, 18), 110, 8, (6, 12))
grad_rect(base, (14, 788, 1150, 850), "#bd8852", "#85582f",
          stops=[(0, C("#c9955d")), (.24, C("#b9854f")), (.8, C("#9d6b3e")), (1, C("#7e522e"))])
# top surface highlight
grad_rect(base, (18, 788, 1148, 808), "#d6a369", "#b57f49")
ln(ImageDraw.Draw(base), [(24, 790), (1144, 790)], "#efc189", 2)
# front lip
grad_rect(base, (18, 838, 1148, 852), "#7a4e2b", "#5e3a20")
ln(ImageDraw.Draw(base), [(24, 840), (1142, 840)], "#b07b49", 2)
# wood grain
ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
random.seed(31)
for _ in range(46):
    y = random.uniform(792, 846)
    x0 = random.uniform(18, 1050); length = random.uniform(45, 260)
    pth = bez((x0, y), (x0 + length * .33, y + random.uniform(-3, 3)),
              (x0 + length * .66, y + random.uniform(-3, 3)),
              (x0 + length, y + random.uniform(-2, 2)), 20)
    od.line(pts(pth), fill=(92, 56, 30, random.randint(35, 80)),
            width=int(random.uniform(.7, 1.8) * S), joint="curve")
base.alpha_composite(ov)
random.seed(19)

# cutting board leaning at left
soft_poly_shadow(base, [(92, 716), (248, 704), (270, 795), (108, 797)],
                 (48, 29, 18), 100, 8, (8, 8))
pg(ImageDraw.Draw(base), [(100, 712), (236, 700), (260, 795), (108, 797)], "#b77b47")
pg(ImageDraw.Draw(base), [(104, 714), (233, 703), (252, 780), (112, 783)], "#cb9259")
pg(ImageDraw.Draw(base), [(110, 716), (228, 706), (246, 774), (116, 778)], "#d8a36a")
ln(ImageDraw.Draw(base), [(122, 720), (231, 711)], "#e7b77e", 2)
# handle hole
el(ImageDraw.Draw(base), (163, 715, 180, 732), "#9d693e")
el(ImageDraw.Draw(base), (166, 718, 177, 729), "#7c4f2e")
# wood grain
for i in range(5):
    ln(ImageDraw.Draw(base), [(130 + i * 15, 724 + i), (150 + i * 15, 768 - i)], "#bd8450", 1)

# utensil crock
soft_ellipse_shadow(base, (288, 756, 376, 810), (48, 30, 18), 110, 7, (5, 5))
# utensils first
for (x, h, bend, colr) in [(316, 72, -9, "#9d6f45"), (332, 86, 3, "#c3945d"),
                            (348, 64, 12, "#81603f"), (357, 78, -4, "#ad7d4d")]:
    ln(ImageDraw.Draw(base), [(x, 780), (x + bend, 780 - h)], colr, 4)
    el(ImageDraw.Draw(base), (x + bend - 6, 780 - h - 9, x + bend + 6, 780 - h + 5), colr)
pg(ImageDraw.Draw(base), [(340, 706), (350, 730), (346, 758), (333, 758),
                          (336, 730)], "#b7b09a")
# whisk loops
for dx in (-5, 0, 5):
    arc(ImageDraw.Draw(base), (330 + dx, 700, 350 + dx, 748), 260, 100, "#b8b5a0", 1)
# crock body
grad_rect(base, (296, 744, 372, 798), "#dfd3bb", "#b7a88b", radius=6)
rr(ImageDraw.Draw(base), (296, 744, 372, 798), 6, None, "#8d7d64", 2)
el(ImageDraw.Draw(base), (298, 738, 370, 758), "#e7ddc7")
el(ImageDraw.Draw(base), (304, 742, 364, 754), "#bcae94")
# painted stripe
ln(ImageDraw.Draw(base), [(300, 770), (368, 770)], "#a87350", 3)
ln(ImageDraw.Draw(base), [(300, 776), (368, 776)], "#c08a63", 1)

# lemon bowl right of sink
soft_ellipse_shadow(base, (884, 762, 1018, 818), (47, 29, 18), 120, 8, (8, 7))
# bowl
grad_rect(base, (886, 742, 1014, 802), "#c08a57", "#8b5a33", radius=10)
el(ImageDraw.Draw(base), (886, 730, 1014, 766), "#d7a36b")
el(ImageDraw.Draw(base), (894, 735, 1006, 760), "#9c693d")
# lemons
for (cx, cy, r) in [(918, 733, 27), (956, 728, 29), (986, 738, 24)]:
    el(ImageDraw.Draw(base), (cx - r, cy - r * .82, cx + r, cy + r * .82), "#e5c24e")
    el(ImageDraw.Draw(base), (cx - r * .8, cy - r * .68, cx + r * .55, cy + r * .35), "#f2d76f")
    arc(ImageDraw.Draw(base), (cx - r, cy - r * .82, cx + r, cy + r * .82),
        160, 330, "#c3a13d", 2)
    # little nub
    el(ImageDraw.Draw(base), (cx + r - 4, cy - 3, cx + r + 4, cy + 3), "#a99b48")
# bowl front highlight
ln(ImageDraw.Draw(base), [(894, 758), (1004, 758)], "#d9a26b", 2)

# coffee mug near range
soft_ellipse_shadow(base, (1030, 764, 1094, 808), (45, 28, 17), 120, 7, (5, 5))
rr(ImageDraw.Draw(base), (1034, 726, 1086, 796), 8, "#e5d6bd")
rr(ImageDraw.Draw(base), (1039, 731, 1081, 791), 6, "#c7b596")
el(ImageDraw.Draw(base), (1032, 730, 1088, 750), "#efe3cc")
el(ImageDraw.Draw(base), (1040, 735, 1080, 747), "#6f4e35")
arc(ImageDraw.Draw(base), (1078, 740, 1104, 778), 270, 90, "#d6c5a7", 6)
ln(ImageDraw.Draw(base), [(1042, 744), (1046, 780)], "#f6ecd7", 2)
# steam
ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
for k in range(3):
    sx = 1047 + k * 14
    pth = bez((sx, 722), (sx - 10, 700), (sx + 12, 678), (sx - 2, 650), 30)
    od.line(pts(pth), fill=(255, 248, 230, 50), width=int(5 * S), joint="curve")
ov = ov.filter(ImageFilter.GaussianBlur(5 * S)); base.alpha_composite(ov)

# little bowl of fresh eggs
soft_ellipse_shadow(base, (424, 766, 544, 820), (48, 29, 18), 115, 8, (6, 7))
# bowl body
grad_poly(base, [(436, 776), (534, 776), (527, 801), (511, 813),
                 (459, 813), (443, 801)],
          "#f7f0e2", "#cbbb9f", stops=[(0, C("#fbf5e8")), (.55, C("#eadfcb")),
                                        (1, C("#c3b196"))])
el(ImageDraw.Draw(base), (432, 758, 538, 794), "#f3ebdd")
el(ImageDraw.Draw(base), (440, 764, 530, 788), "#b9aa91")
# eggs (small warm cream ovals, nestled together)
for (cx, cy, rx, ry, tint) in [(460, 750, 18, 24, "#e8d2b0"),
                                (490, 745, 18, 25, "#efdbbd"),
                                (516, 755, 16, 22, "#e2caa6")]:
    soft_ellipse_shadow(base, (cx - rx + 4, cy + ry - 8, cx + rx + 8, cy + ry + 6),
                        (60, 42, 27), 55, 4, (0, 0))
    el(ImageDraw.Draw(base), (cx - rx, cy - ry, cx + rx, cy + ry), tint)
    el(ImageDraw.Draw(base), (cx - rx + 4, cy - ry + 2, cx + rx - 8, cy + ry - 7), "#fbf0da")
    el(ImageDraw.Draw(base), (cx - 8, cy - ry + 4, cx + 3, cy - ry + 12), "#fffaf0")
    arc(ImageDraw.Draw(base), (cx - rx, cy - ry, cx + rx, cy + ry), 60, 160, "#c3a47d", 1)
    for (sx, sy) in [(-8, 7), (4, -4), (7, 10), (-2, 14), (10, 2)]:
        el(ImageDraw.Draw(base), (cx + sx, cy + sy, cx + sx + 2, cy + sy + 2), "#b99974")
# front rim
arc(ImageDraw.Draw(base), (432, 756, 538, 798), 0, 180, "#fbf5e8", 7)
arc(ImageDraw.Draw(base), (432, 762, 538, 800), 0, 180, "#9c896f", 2)
ln(ImageDraw.Draw(base), [(440, 779), (530, 779)], "#a38f73", 2)
# sage stripe and porcelain shine
arc(ImageDraw.Draw(base), (438, 766, 532, 804), 15, 165, "#80967f", 2)
arc(ImageDraw.Draw(base), (440, 770, 530, 806), 22, 158, "#fdf8ec", 2)
el(ImageDraw.Draw(base), (451, 787, 490, 799), "#fcf6e9")
# tiny thyme sprig
ln(ImageDraw.Draw(base), [(527, 759), (540, 737)], "#5f7854", 2)
for lx, ly in [(534, 747), (538, 741), (530, 741)]:
    el(ImageDraw.Draw(base), (lx - 5, ly - 3, lx + 4, ly + 3), "#7d9166")

# ============================================================================
# 7. FARMHOUSE SINK & FAUCET
# ============================================================================
# apron-front farmhouse sink
soft_poly_shadow(base, [(542, 812), (864, 812), (864, 936), (542, 936)],
                 (40, 26, 17), 130, 12, (9, 13))
# apron body (porcelain)
grad_rect(base, (548, 812, 858, 928), "#f8f1e3", "#cbbb9f",
          stops=[(0, C("#fbf5e8")), (.5, C("#eee3d0")), (1, C("#c9b89b"))], radius=17)
# broad rim around the basin opening
rr(ImageDraw.Draw(base), (542, 778, 864, 844), 18, "#f5edde")
rr(ImageDraw.Draw(base), (552, 785, 854, 838), 15, None, "#d7c7ae", 2)
# basin opening (dark, with reflected morning light)
grad_rect(base, (560, 790, 846, 835), "#5d594b", "#b5a78f",
          stops=[(0, C("#4f4d42")), (.38, C("#777161")), (.72, C("#a39780")),
                 (1, C("#c9bca2"))], radius=13)
# inner walls of the basin
pg(ImageDraw.Draw(base), [(560, 792), (583, 833), (600, 833), (576, 792)], "#d6c8b0")
pg(ImageDraw.Draw(base), [(846, 792), (826, 833), (812, 833), (832, 792)], "#766e5e")
# reflected window in the basin
ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
od.polygon(pts([(640, 795), (718, 795), (744, 828), (660, 830)]), fill=(218, 228, 217, 30))
od.polygon(pts([(624, 796), (641, 796), (657, 830), (638, 830)]), fill=(250, 244, 226, 22))
ov = ov.filter(ImageFilter.GaussianBlur(6 * S)); base.alpha_composite(ov)
# drain and inner lip
el(ImageDraw.Draw(base), (677, 810, 731, 828), "#8e826b")
el(ImageDraw.Draw(base), (684, 812, 724, 825), "#5b5444")
for dx in (-10, 0, 10):
    ln(ImageDraw.Draw(base), [(702, 812), (702 + dx, 825)], "#3e3a31", 1)
el(ImageDraw.Draw(base), (697, 813, 707, 823), "#a89b80")
ln(ImageDraw.Draw(base), [(566, 828), (838, 828)], "#e1d4bc", 2)
ln(ImageDraw.Draw(base), [(564, 796), (564, 830)], "#fbf4e6", 2)
# apron front, with a soft rounded bottom
grad_poly(base, [(550, 836), (856, 836), (856, 900), (849, 918),
                 (559, 918), (550, 900)],
          "#f9f2e4", "#d4c4a8", stops=[(0, C("#fdf7ea")), (.55, C("#eee2ce")),
                                        (1, C("#d1bfa2"))])
# shadow under the rim
ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
od.rectangle(bx((552, 837, 854, 850)), fill=(91, 67, 43, 55))
ov = ov.filter(ImageFilter.GaussianBlur(5 * S)); base.alpha_composite(ov)
# smooth porcelain front with a soft centre highlight
el(ImageDraw.Draw(base), (580, 844, 826, 910), "#f5ecdb")
ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
od.ellipse(bx((588, 843, 818, 908)), fill=(255, 250, 238, 80))
od.ellipse(bx((790, 850, 854, 918)), fill=(118, 92, 63, 28))
ov = ov.filter(ImageFilter.GaussianBlur(14 * S)); base.alpha_composite(ov)
# side shading
ln(ImageDraw.Draw(base), [(553, 842), (553, 902)], "#fdf7ea", 3)
ln(ImageDraw.Draw(base), [(852, 842), (852, 902)], "#b3a187", 3)
ln(ImageDraw.Draw(base), [(570, 851), (570, 910)], "#f0e4cf", 2)
ln(ImageDraw.Draw(base), [(836, 851), (836, 910)], "#d2c2a8", 2)
arc(ImageDraw.Draw(base), (554, 900, 854, 936), 0, 180, "#9c8a71", 2)
# soft foot shadow on the cabinet
ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
od.ellipse(bx((556, 912, 852, 940)), fill=(50, 34, 21, 60))
ov = ov.filter(ImageFilter.GaussianBlur(9 * S)); base.alpha_composite(ov)

# faucet
soft_poly_shadow(base, [(714, 640), (822, 640), (822, 800), (714, 800)],
                 (40, 26, 16), 90, 9, (12, 10))
# base
el(ImageDraw.Draw(base), (708, 780, 768, 802), "#9e7b4e")
el(ImageDraw.Draw(base), (714, 778, 762, 792), "#c9a468")
# main neck
neck = bez((734, 788), (728, 704), (742, 652), (786, 646), 35)
for w, colr in [(12, "#6e5438"), (8, "#b08a54"), (4, "#d9b77d")]:
    ln(ImageDraw.Draw(base), neck, colr, w)
# spout curving down
spout = bez((786, 646), (820, 646), (818, 686), (811, 704), 25)
for w, colr in [(12, "#6e5438"), (8, "#b08a54"), (4, "#d9b77d")]:
    ln(ImageDraw.Draw(base), spout, colr, w)
el(ImageDraw.Draw(base), (800, 698, 822, 714), "#8a6a42")
el(ImageDraw.Draw(base), (804, 701, 817, 708), "#c9a76d")
# handles
for hx in (704, 774):
    ln(ImageDraw.Draw(base), [(hx, 778), (hx - 1, 762)], "#8d6c43", 4)
    ln(ImageDraw.Draw(base), [(hx - 8, 759), (hx + 7, 759)], "#c29c63", 3)
    el(ImageDraw.Draw(base), (hx - 9, 756, hx - 4, 762), "#d8b478")
# water drop glint
el(ImageDraw.Draw(base), (811, 714, 817, 721), "#dbe5df")

# linen dish towel draped over the sink rim
soft_poly_shadow(base, [(560, 842), (650, 842), (646, 984), (558, 984)],
                 (47, 29, 18), 95, 7, (6, 8))
# top fold over the rim
grad_poly(base, [(560, 834), (646, 836), (649, 854), (558, 852)],
          "#f0e3cd", "#cbb493")
# hanging cloth
grad_poly(base, [(561, 848), (646, 850), (643, 938), (650, 982),
                 (636, 976), (624, 986), (611, 977), (598, 986),
                 (586, 977), (574, 984), (562, 976), (556, 940)],
          "#eadcc4", "#c1a985", stops=[(0, C("#f2e6d1")), (.6, C("#ddcbb0")),
                                        (1, C("#c0a783"))])
# red woven stripes
for xx in (578, 596, 614, 632):
    ln(ImageDraw.Draw(base), [(xx, 854), (xx - 2, 977)], "#a34e3b", 4)
    ln(ImageDraw.Draw(base), [(xx + 7, 854), (xx + 5, 977)], "#d2a371", 1)
# folds and shading
for xx in (570, 588, 606, 624, 640):
    ln(ImageDraw.Draw(base), [(xx, 854), (xx - 2, 976)], "#a98f6e", 1)
ln(ImageDraw.Draw(base), [(563, 854), (563, 938)], "#fbf2e0", 2)
ln(ImageDraw.Draw(base), [(644, 854), (642, 940)], "#9b8263", 2)
# fringe
for xx in range(560, 652, 6):
    ln(ImageDraw.Draw(base), [(xx, 978), (xx + 1, 988)], "#cdb795", 2)

# ============================================================================
# 8. RANGE, KETTLE, PAN RACK, SHELF
# ============================================================================
# range shadow
soft_poly_shadow(base, [(1138, 770), (1502, 770), (1502, 1190), (1138, 1190)],
                 (46, 28, 18), 120, 14, (8, 10))
# backguard
grad_rect(base, (1142, 588, 1500, 786), "#eadfc9", "#c4ae8e", radius=12)
rr(ImageDraw.Draw(base), (1142, 588, 1500, 786), 12, None, "#9a7e5d", 3)
grad_rect(base, (1152, 600, 1490, 764), "#e4d5bc", "#d0b997", radius=8)
ln(ImageDraw.Draw(base), [(1152, 600), (1490, 600)], "#fbf1dc", 3)
# embossed border on the range backguard
rr(ImageDraw.Draw(base), (1166, 612, 1478, 772), 9, None, "#d3bd9d", 2)
rr(ImageDraw.Draw(base), (1174, 620, 1470, 764), 7, None, "#fbf0dc", 1)
# small hinge details
for hx in (1184, 1460):
    el(ImageDraw.Draw(base), (hx - 3, 640, hx + 3, 646), "#bfa986")

# little enamel clock on the backguard
el(ImageDraw.Draw(base), (1390, 610, 1466, 686), "#9f7f58")
el(ImageDraw.Draw(base), (1394, 614, 1462, 682), "#d9c29b")
el(ImageDraw.Draw(base), (1400, 620, 1456, 676), "#f4ecda")
el(ImageDraw.Draw(base), (1404, 624, 1452, 672), "#fbf6e9")
for ang in range(0, 360, 30):
    r0 = 21 if ang % 90 else 17
    x0 = 1428 + math.cos(math.radians(ang)) * r0
    y0 = 648 + math.sin(math.radians(ang)) * r0
    x1 = 1428 + math.cos(math.radians(ang)) * 24
    y1 = 648 + math.sin(math.radians(ang)) * 24
    ln(ImageDraw.Draw(base), [(x0, y0), (x1, y1)], "#8a7151", 1 if ang % 90 else 2)
# hour and minute hands (a little after seven)
ln(ImageDraw.Draw(base), [(1428, 648), (1414, 637)], "#4f3c2a", 4)
ln(ImageDraw.Draw(base), [(1428, 648), (1444, 632)], "#4f3c2a", 3)
el(ImageDraw.Draw(base), (1425, 645, 1431, 651), "#5e4630")
# glass glint
arc(ImageDraw.Draw(base), (1404, 624, 1452, 672), 200, 300, "#ffffff", 2)
# small maker's line beneath the clock
ln(ImageDraw.Draw(base), [(1408, 696), (1448, 696)], "#c6af8c", 1)

# range body
grad_rect(base, (1148, 772, 1494, 1188), "#efe4d0", "#c8b293",
          stops=[(0, C("#eee2cd")), (.55, C("#ddccb1")), (1, C("#c0a787"))], radius=10)
rr(ImageDraw.Draw(base), (1148, 772, 1494, 1188), 10, None, "#967a59", 3)
# cooktop
grad_rect(base, (1154, 762, 1490, 792), "#4a443a", "#27251f", radius=5)
for gx in (1190, 1302, 1414):
    rr(ImageDraw.Draw(base), (gx - 44, 768, gx + 44, 786), 5, None, "#6b6252", 3)
    for gy in (772, 782):
        ln(ImageDraw.Draw(base), [(gx - 38, gy), (gx + 38, gy)], "#171612", 2)
# knobs
for i in range(5):
    kx = 1184 + i * 70
    ky = 812
    el(ImageDraw.Draw(base), (kx - 11, ky - 11, kx + 11, ky + 11), "#8d6a44")
    el(ImageDraw.Draw(base), (kx - 8, ky - 8, kx + 8, ky + 8), "#d5b57d")
    ln(ImageDraw.Draw(base), [(kx, ky - 7), (kx, ky - 1)], "#6f5334", 2)
# oven door
rr(ImageDraw.Draw(base), (1176, 850, 1466, 1088), 12, "#e7dac4", "#a98d6b", 3)
rr(ImageDraw.Draw(base), (1190, 870, 1452, 1054), 10, "#5a4e3f", "#8d7456", 4)
grad_rect(base, (1200, 880, 1442, 1044), "#494139", "#171615", radius=7)
# warm oven light and a loaf baking inside
glow(base, (1322, 982), 130, "#ffb35f", 60, aspect=.66, blur=26)
glow(base, (1322, 990), 62, "#ffd28d", 34, aspect=.7, blur=14)
# rack
for ry in (1010, 1026):
    ln(ImageDraw.Draw(base), [(1215, ry), (1428, ry)], "#6b5c4a", 2)
    for rx in range(1220, 1428, 20):
        ln(ImageDraw.Draw(base), [(rx, ry), (rx + 8, ry)], "#4c4035", 1)
# golden boule on the rack
soft_ellipse_shadow(base, (1272, 978, 1370, 1015), (32, 22, 15), 60, 5, (0, 6))
el(ImageDraw.Draw(base), (1274, 968, 1370, 1008), "#965225")
el(ImageDraw.Draw(base), (1277, 963, 1367, 1003), "#c57b36")
el(ImageDraw.Draw(base), (1282, 963, 1348, 995), "#e2a056")
el(ImageDraw.Draw(base), (1293, 968, 1338, 983), "#f0ba6f")
# scoring
for sx in (1298, 1320, 1342):
    pth = bez((sx, 970), (sx + 5, 977), (sx + 4, 985), (sx + 8, 992), 10)
    ln(ImageDraw.Draw(base), pth, "#9f5b2e", 2)
ln(ImageDraw.Draw(base), [(1283, 993), (1358, 991)], "#b06b33", 1)
# flour dust and warm shine
el(ImageDraw.Draw(base), (1302, 968, 1314, 974), "#f5d9a7")
el(ImageDraw.Draw(base), (1332, 976, 1341, 980), "#f2d19a")
glow(base, (1304, 974), 24, "#ffe0a4", 18, blur=9)

# soft reflection in the glass
ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
od.polygon(pts([(1212, 1042), (1322, 882), (1366, 882), (1256, 1042)]),
           fill=(255, 234, 199, 13))
od.polygon(pts([(1218, 1042), (1232, 1042), (1342, 884), (1328, 884)]),
           fill=(255, 244, 217, 18))
ov = ov.filter(ImageFilter.GaussianBlur(8 * S)); base.alpha_composite(ov)
# folded tea towel on the handle
soft_ellipse_shadow(base, (1356, 842, 1430, 916), (45, 29, 17), 60, 5, (3, 5))
pg(ImageDraw.Draw(base), [(1362, 840), (1424, 840), (1421, 874), (1427, 902),
                          (1412, 894), (1402, 908), (1392, 898), (1381, 908),
                          (1371, 897), (1360, 904), (1358, 874)],
   "#dfd0b6")
pg(ImageDraw.Draw(base), [(1367, 843), (1418, 843), (1415, 872), (1420, 893),
                          (1408, 886), (1399, 898), (1389, 889), (1378, 899),
                          (1368, 889), (1365, 872)], "#eee1ca")
for xx in (1375, 1390, 1406):
    ln(ImageDraw.Draw(base), [(xx, 846), (xx - 2, 892)], "#c5b193", 2)
for xx in (1380, 1401):
    ln(ImageDraw.Draw(base), [(xx, 845), (xx - 3, 896)], "#85967f", 4)
ln(ImageDraw.Draw(base), [(1364, 853), (1419, 853)], "#b49c7b", 1)
for xx in range(1362, 1424, 6):
    ln(ImageDraw.Draw(base), [(xx, 896), (xx, 908)], "#d0bb99", 1)
# oven handle
ln(ImageDraw.Draw(base), [(1204, 838), (1438, 838)], "#7a5b39", 8)
ln(ImageDraw.Draw(base), [(1204, 834), (1438, 834)], "#d8b77c", 3)
for hx in (1220, 1422):
    el(ImageDraw.Draw(base), (hx - 7, 832, hx + 7, 846), "#a67d4c")
# bottom drawer
rr(ImageDraw.Draw(base), (1184, 1106, 1458, 1168), 8, "#d4c1a2", "#a38866", 2)
ln(ImageDraw.Draw(base), [(1214, 1138), (1428, 1138)], "#9f825d", 3)
ln(ImageDraw.Draw(base), [(1214, 1135), (1428, 1135)], "#e4d2b5", 1)
# side panel highlights/shadows
ln(ImageDraw.Draw(base), [(1154, 786), (1154, 1180)], "#f7f0df", 3)
ln(ImageDraw.Draw(base), [(1488, 786), (1488, 1180)], "#a48968", 4)

# copper kettle
soft_ellipse_shadow(base, (1238, 716, 1384, 784), (43, 26, 17), 120, 8, (8, 7))
# spout
spout = bez((1240, 706), (1208, 684), (1200, 660), (1210, 644), 26)
for w, colr in [(13, "#7a4324"), (9, "#b66533"), (4, "#e0995b")]:
    ln(ImageDraw.Draw(base), spout, colr, w)
# handle
handle = bez((1240, 664), (1246, 612), (1350, 608), (1356, 666), 35)
ln(ImageDraw.Draw(base), handle, "#4a3526", 9)
ln(ImageDraw.Draw(base), handle, "#8c613d", 5)
ln(ImageDraw.Draw(base), [(p[0], p[1] - 2) for p in handle], "#c08f5c", 1)
# body
grad_poly(base, [(1240, 676), (1250, 652), (1280, 640), (1330, 642),
                 (1360, 660), (1372, 700), (1368, 744), (1350, 764),
                 (1250, 764), (1236, 740)],
          "#d98a4e", "#873d20", stops=[(0, C("#e7a161")), (.3, C("#cf7a41")),
                                       (.68, C("#a9552b")), (1, C("#7a351d"))])
# lid
el(ImageDraw.Draw(base), (1272, 630, 1342, 654), "#c06e38")
el(ImageDraw.Draw(base), (1280, 634, 1334, 650), "#e2a066")
el(ImageDraw.Draw(base), (1298, 620, 1318, 638), "#9f4f27")
el(ImageDraw.Draw(base), (1302, 617, 1314, 627), "#d9985d")
# highlights
ln(ImageDraw.Draw(base), [(1260, 668), (1252, 738)], "#f3bd7c", 7)
ln(ImageDraw.Draw(base), [(1268, 662), (1262, 720)], "#ffe0ad", 2)
ln(ImageDraw.Draw(base), [(1344, 676), (1352, 732)], "#7f3a22", 4)
glow(base, (1288, 690), 30, "#ffd49a", 35, aspect=.9, blur=14)
# base
rr(ImageDraw.Draw(base), (1252, 754, 1368, 770), 5, "#5e3420")
ln(ImageDraw.Draw(base), [(1256, 756), (1364, 756)], "#a86135", 2)
# steam wisp
ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
pth = bez((1310, 614), (1328, 590), (1292, 558), (1318, 528), 35)
od.line(pts(pth), fill=(255, 248, 231, 52), width=int(5 * S), joint="curve")
ov = ov.filter(ImageFilter.GaussianBlur(7 * S)); base.alpha_composite(ov)

# wall rail and copper pans
ln(ImageDraw.Draw(base), [(1138, 258), (1512, 258)], "#7c5b3b", 7)
ln(ImageDraw.Draw(base), [(1138, 254), (1512, 254)], "#c09460", 2)
for hx in (1160, 1490):
    rr(ImageDraw.Draw(base), (hx - 5, 250, hx + 5, 274), 2, "#6f5236")
# pans
for i, (cx, cy, r) in enumerate([(1210, 344, 58), (1330, 362, 52), (1450, 336, 62)]):
    # handle
    ln(ImageDraw.Draw(base), [(cx, cy - r - 2), (cx + 6, cy - r - 54)], "#8b5a32", 7)
    el(ImageDraw.Draw(base), (cx + 2, cy - r - 60, cx + 12, cy - r - 50), "#b57c45")
    # pan body
    soft_ellipse_shadow(base, (cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14),
                        (51, 30, 18), 80, 8, (7, 9))
    el(ImageDraw.Draw(base), (cx - r, cy - r, cx + r, cy + r), "#8e4e2a")
    el(ImageDraw.Draw(base), (cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8), "#b96a39")
    el(ImageDraw.Draw(base), (cx - r + 18, cy - r + 18, cx + r - 18, cy + r - 18), "#8b4a28")
    el(ImageDraw.Draw(base), (cx - r + 25, cy - r + 23, cx + r - 25, cy + r - 25), "#c27745")
    arc(ImageDraw.Draw(base), (cx - r + 24, cy - r + 22, cx + r - 24, cy + r - 22),
        200, 340, "#e7a667", 3)
    arc(ImageDraw.Draw(base), (cx - r, cy - r, cx + r, cy + r), 120, 220, "#f0bf7d", 2)
    glow(base, (cx - 12, cy - 16), 22, "#ffd49a", 30, blur=12)

# wooden shelf
soft_poly_shadow(base, [(1114, 486), (1528, 486), (1528, 512), (1114, 512)],
                 (53, 33, 20), 100, 7, (0, 9))
grad_rect(base, (1108, 480, 1534, 506), "#a97142", "#6d4327", radius=3)
ln(ImageDraw.Draw(base), [(1114, 482), (1528, 482)], "#d29a5e", 3)
ln(ImageDraw.Draw(base), [(1114, 503), (1528, 503)], "#5c3922", 2)
for hx in (1148, 1462):
    pg(ImageDraw.Draw(base), [(hx, 504), (hx, 544), (hx + 10, 504)], "#69442a")
# items on shelf: stack of plates
for i in range(4):
    y = 478 - i * 7
    el(ImageDraw.Draw(base), (1160, y - 5, 1250, y + 7), "#ece1cc")
    el(ImageDraw.Draw(base), (1166, y - 3, 1244, y + 4), "#d9cab0")
    arc(ImageDraw.Draw(base), (1160, y - 5, 1250, y + 7), 200, 340, "#f6ecd9", 1)
# teapot
el(ImageDraw.Draw(base), (1272, 432, 1352, 482), "#d8c3a2")
el(ImageDraw.Draw(base), (1280, 438, 1344, 473), "#e6d5b8")
pg(ImageDraw.Draw(base), [(1350, 452), (1372, 445), (1362, 462)], "#d8c3a2")
arc(ImageDraw.Draw(base), (1262, 440, 1292, 474), 250, 120, "#b79c78", 4)
el(ImageDraw.Draw(base), (1300, 423, 1326, 438), "#b99a72")
# jar
rr(ImageDraw.Draw(base), (1380, 426, 1434, 482), 7, "#dfd3bc")
rr(ImageDraw.Draw(base), (1384, 420, 1430, 438), 4, "#b48a5c")
ln(ImageDraw.Draw(base), [(1389, 452), (1425, 452)], "#b9a17f", 3)
ln(ImageDraw.Draw(base), [(1389, 458), (1425, 458)], "#b9a17f", 1)
# trailing plant at shelf right
soft_ellipse_shadow(base, (1436, 452, 1506, 484), (51, 31, 18), 80, 6, (5, 6))
pg(ImageDraw.Draw(base), [(1443, 450), (1497, 450), (1492, 486), (1449, 486)], "#b46d49")
pg(ImageDraw.Draw(base), [(1448, 450), (1492, 450), (1488, 459), (1452, 459)], "#8d5237")
el(ImageDraw.Draw(base), (1438, 442, 1502, 460), "#c8835a")
# leaves and vines
for k in range(5):
    sx = 1450 + k * 10
    pth = bez((sx, 448), (sx - 18, 438), (sx - 8, 416), (sx - 22, 400), 20)
    ln(ImageDraw.Draw(base), pth, "#5e7457", 2)
    for j in (6, 11, 16):
        px, py = pth[j]
        el(ImageDraw.Draw(base), (px - 6, py - 4, px + 5, py + 3), "#758b67")
for k in range(3):
    sx = 1470 + k * 8
    pth = bez((sx, 482), (sx + 14, 506), (sx - 4, 522), (sx + 10, 540), 18)
    ln(ImageDraw.Draw(base), pth, "#617758", 2)
    for j in (7, 12, 16):
        px, py = pth[j]
        el(ImageDraw.Draw(base), (px - 5, py - 3, px + 5, py + 3), "#718763")

# utensils under shelf
for (hx, length, kind) in [(1180, 88, "spoon"), (1212, 74, "whisk"), (1244, 96, "spoon"),
                            (1450, 78, "ladle"), (1480, 64, "spoon")]:
    ln(ImageDraw.Draw(base), [(hx, 508), (hx, 508 + length)], "#9b784d", 3)
    if kind == "spoon":
        el(ImageDraw.Draw(base), (hx - 9, 508 + length - 8, hx + 9, 508 + length + 10),
           "#a98050")
        el(ImageDraw.Draw(base), (hx - 5, 508 + length - 4, hx + 5, 508 + length + 5),
           "#c49b67")
    else:
        for s in (-5, 0, 5):
            arc(ImageDraw.Draw(base), (hx + s - 5, 508 + length - 20,
                                       hx + s + 5, 508 + length + 8), 250, 110, "#b5b3a2", 1)
# S hooks
for hx in (1180, 1212, 1244, 1450, 1480):
    arc(ImageDraw.Draw(base), (hx - 6, 500, hx + 6, 520), 180, 20, "#7d6d55", 2)

# ============================================================================
# 9. LEFT WALL DETAILS
# ============================================================================
# framed botanical print
soft_poly_shadow(base, [(42, 154), (212, 154), (212, 344), (42, 344)],
                 (54, 35, 21), 80, 8, (8, 10))
rr(ImageDraw.Draw(base), (38, 148, 216, 344), 4, "#6b4b31", "#4f3624", 3)
rr(ImageDraw.Draw(base), (48, 158, 206, 334), 2, "#d8c6a7")
rr(ImageDraw.Draw(base), (58, 168, 196, 324), 1, "#f1e8d6")
# botanical sprig
pth = bez((126, 314), (116, 275), (132, 234), (120, 194), 40)
ln(ImageDraw.Draw(base), pth, "#6d7b58", 3)
for i in range(2, 36, 4):
    x, y = pth[i]
    side = 1 if i % 8 == 2 else -1
    ln(ImageDraw.Draw(base), [(x, y), (x + side * 22, y - 12)], "#778663", 2)
    el(ImageDraw.Draw(base), (x + side * 22 - 9, y - 18, x + side * 22 + 9, y - 7),
       "#8d9a76")
    ln(ImageDraw.Draw(base), [(x + side * 22, y - 12), (x + side * 30, y - 16)],
       "#6a7858", 1)
# seed head
for a in range(0, 360, 45):
    ln(ImageDraw.Draw(base), [(120, 194), (120 + math.cos(math.radians(a)) * 10,
                                           194 + math.sin(math.radians(a)) * 10)],
       "#9b8a64", 1)
el(ImageDraw.Draw(base), (117, 191, 123, 197), "#a7895e")
# little caption
ln(ImageDraw.Draw(base), [(102, 304), (142, 304)], "#b0a18b", 1)

# peg rail and apron
soft_poly_shadow(base, [(34, 382), (220, 382), (220, 666), (34, 666)],
                 (48, 31, 20), 80, 8, (8, 9))
grad_rect(base, (32, 376, 222, 394), "#8f6845", "#5e412a", radius=3)
for px in (62, 112, 164, 208):
    el(ImageDraw.Draw(base), (px - 5, 384, px + 5, 396), "#c29862")
    ln(ImageDraw.Draw(base), [(px, 388), (px, 402)], "#9e794e", 3)
# linen apron
pg(ImageDraw.Draw(base), [(64, 398), (160, 398), (170, 470), (166, 632),
                          (58, 632), (54, 470)], "#ded0b9")
pg(ImageDraw.Draw(base), [(68, 402), (156, 402), (163, 470), (158, 626),
                          (62, 626), (59, 470)], "#eadfc9")
# neck strap
ln(ImageDraw.Draw(base), [(83, 400), (80, 378)], "#c3ad8d", 3)
ln(ImageDraw.Draw(base), [(140, 400), (143, 378)], "#c3ad8d", 3)
# folds
for x in (85, 108, 132):
    ln(ImageDraw.Draw(base), [(x, 410), (x + 2, 620)], "#cbb89b", 2)
ln(ImageDraw.Draw(base), [(76, 428), (150, 428)], "#c7b294", 1)
# pocket
rr(ImageDraw.Draw(base), (78, 486, 146, 546), 5, "#c7a27a")
rr(ImageDraw.Draw(base), (82, 490, 142, 542), 4, None, "#a87e56", 2)
for i in range(5):
    ln(ImageDraw.Draw(base), [(84, 495 + i * 9), (140, 495 + i * 9)], "#b48c66", 1)
# wooden spoon in pocket
ln(ImageDraw.Draw(base), [(132, 494), (142, 410)], "#9a6e41", 4)
el(ImageDraw.Draw(base), (137, 400, 151, 416), "#ad7a48")
# small embroidered leaf
el(ImageDraw.Draw(base), (112, 566, 126, 576), "#9a9b76")
ln(ImageDraw.Draw(base), [(103, 594), (137, 594)], "#b58d6b", 1)
# straw hat hanging at right peg
soft_ellipse_shadow(base, (174, 402, 258, 462), (50, 32, 20), 80, 6, (5, 6))
el(ImageDraw.Draw(base), (176, 418, 254, 456), "#c9a567")
el(ImageDraw.Draw(base), (192, 406, 238, 448), "#d7b77a")
el(ImageDraw.Draw(base), (198, 414, 232, 440), "#b08d56")
ln(ImageDraw.Draw(base), [(202, 430), (228, 430)], "#8e6c44", 4)
# hanging dried herbs at left edge
for k in range(4):
    sx = 30 + k * 13
    pth = bez((sx, 380), (sx - 6, 424), (sx + 6, 470), (sx - 2, 510), 24)
    ln(ImageDraw.Draw(base), pth, "#8b8160", 2)
    for j in (5, 9, 13, 17):
        px, py = pth[j]
        el(ImageDraw.Draw(base), (px - 5, py - 3, px + 4, py + 4), "#9d936e")
# string
ln(ImageDraw.Draw(base), [(22, 378), (76, 378)], "#8e7c5f", 1)

# ============================================================================
# 10. SUNLIGHT, SHADOWS, ATMOSPHERE
# ============================================================================
# broad sunbeams
beam = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
bd = ImageDraw.Draw(beam)
bd.polygon(pts([(300, 180), (610, 116), (1530, 870), (1130, 1120)]),
           fill=(255, 218, 156, 14))
bd.polygon(pts([(390, 260), (760, 140), (1598, 1000), (1330, 1180)]),
           fill=(255, 224, 163, 10))
bd.polygon(pts([(250, 400), (500, 250), (940, 1200), (660, 1200)]),
           fill=(255, 232, 181, 9))
beam = beam.filter(ImageFilter.GaussianBlur(28 * S))
base.alpha_composite(beam)

# light pool on counter and cabinets
pool = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
pd = ImageDraw.Draw(pool)
pd.polygon(pts([(820, 780), (1090, 760), (1240, 1000), (940, 1090)]),
           fill=(255, 220, 158, 30))
pd.polygon(pts([(600, 800), (760, 790), (830, 1180), (650, 1180)]),
           fill=(255, 226, 168, 18))
pd.polygon(pts([(250, 680), (480, 650), (610, 800), (330, 810)]),
           fill=(255, 231, 177, 20))
pool = pool.filter(ImageFilter.GaussianBlur(20 * S))
base.alpha_composite(pool)

# stronger morning light, screened over the room
lm = Image.new("L", (CW, CH), 0); ld = ImageDraw.Draw(lm)
# soft beams crossing the air
ld.polygon(pts([(280, 130), (470, 112), (1430, 840), (1210, 980), (900, 980)]), fill=23)
ld.polygon(pts([(470, 160), (610, 130), (1450, 1020), (1300, 1160), (1080, 1160)]), fill=16)
# sun pooled on the counter and a little on the upper cabinet faces
ld.polygon(pts([(770, 762), (1050, 762), (1140, 898), (860, 918)]), fill=50)
ld.polygon(pts([(272, 782), (500, 778), (556, 848), (300, 852)]), fill=36)
ld.polygon(pts([(858, 852), (1040, 846), (1080, 1080), (900, 1098)]), fill=17)
lm = lm.filter(ImageFilter.GaussianBlur(18 * S))
base = screen_light(base, lm, "#ffd7a1", 255)

# crisp sunlit edge on top of window and left curtain
lm2 = Image.new("L", (CW, CH), 0); ld = ImageDraw.Draw(lm2)
ld.polygon(pts([(210, 60), (340, 55), (320, 360), (245, 640), (195, 640)]), fill=38)
ld.polygon(pts([(930, 120), (1030, 120), (1010, 500), (960, 620), (1000, 620)]), fill=20)
lm2 = lm2.filter(ImageFilter.GaussianBlur(12 * S))
base = screen_light(base, lm2, "#ffe1b4", 255)

# window mullion shadows on counter
mull = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
md = ImageDraw.Draw(mull)
md.polygon(pts([(690, 790), (760, 790), (940, 1200), (850, 1200)]),
           fill=(70, 42, 24, 42))
md.polygon(pts([(290, 790), (330, 790), (500, 1200), (450, 1200)]),
           fill=(70, 42, 24, 28))
mull = mull.filter(ImageFilter.GaussianBlur(16 * S))
base.alpha_composite(mull)

# sunlit rim light on objects
rim = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
rd = ImageDraw.Draw(rim)
for pth in [bez((1040, 590), (1060, 640), (1050, 700), (1080, 780), 25),
            bez((1148, 620), (1136, 680), (1156, 740), (1144, 790), 25),
            bez((300, 835), (340, 900), (310, 980), (356, 1080), 25)]:
    rd.line(pts(pth), fill=(255, 228, 174, 40), width=int(5 * S), joint="curve")
rim = rim.filter(ImageFilter.GaussianBlur(5 * S))
base.alpha_composite(rim)

# dust motes
mote = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
md = ImageDraw.Draw(mote)
random.seed(77)
for _ in range(95):
    x = random.uniform(360, 1240); y = random.uniform(150, 980)
    # concentrate inside beam
    xx = x + (y - 200) * .22
    if random.random() < .4:
        xx = random.uniform(500, 1450)
    r = random.uniform(.7, 3.4)
    a = random.randint(20, 95)
    md.ellipse((xx * S, y * S, (xx + r) * S, (y + r) * S), fill=(255, 239, 199, a))
mote = mote.filter(ImageFilter.GaussianBlur(1.1 * S))
base.alpha_composite(mote)

# warm color grade
grade = Image.new("RGBA", (CW, CH), (255, 179, 104, 10))
base.alpha_composite(grade)
# cool shadow wash in lower corners
shade = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
sd = ImageDraw.Draw(shade)
sd.ellipse((-300 * S, 760 * S, 460 * S, 1400 * S), fill=(47, 40, 33, 56))
sd.ellipse((1180 * S, 920 * S, 1900 * S, 1420 * S), fill=(42, 34, 27, 44))
shade = shade.filter(ImageFilter.GaussianBlur(80 * S))
base.alpha_composite(shade)

# vignette
vig = Image.new("L", (500, 375), 0)
vp = vig.load()
for yy in range(375):
    for xx in range(500):
        dx = (xx - 250) / 250; dy = (yy - 187.5) / 187.5
        d = math.sqrt(dx * dx * .82 + dy * dy * 1.05)
        a = max(0, min(150, int((d - .42) * 195)))
        vp[xx, yy] = a
vig = vig.resize((CW, CH), Image.LANCZOS).filter(ImageFilter.GaussianBlur(28 * S))
vt = Image.new("RGBA", (CW, CH), (38, 26, 18))
vt.putalpha(vig)
base.alpha_composite(vt)

# canvas grain
noise = Image.effect_noise((CW, CH), 32).convert("L")
noise_rgba = Image.new("RGBA", (CW, CH), (245, 235, 220))
noise_rgba.putalpha(noise.point(lambda a: int((a - 128) * 0.10 + 7)))
base.alpha_composite(noise_rgba)
# fine paper fibers
fib = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); fd = ImageDraw.Draw(fib)
random.seed(5)
for _ in range(900):
    x = random.uniform(0, W) * S; y = random.uniform(0, H) * S
    l = random.uniform(1, 5) * S
    fd.line((x, y, x + l, y + random.uniform(-.8, .8) * S),
            fill=(255, 245, 226, random.randint(4, 14)), width=1)
base.alpha_composite(fib)

# final downscale with a gentle color lift
out = base.convert("RGB").resize((W, H), Image.LANCZOS)
from PIL import ImageEnhance
out = ImageEnhance.Color(out).enhance(1.055)
out = ImageEnhance.Contrast(out).enhance(1.035)
out.save("cozy_kitchen_morning.png", quality=95)
print("saved", out.size)
