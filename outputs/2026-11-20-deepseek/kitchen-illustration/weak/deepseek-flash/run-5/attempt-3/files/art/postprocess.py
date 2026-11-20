from PIL import Image, ImageFilter, ImageChops, ImageEnhance, ImageDraw
from pathlib import Path

src = Path('art/cozy_kitchen_2x.png')
out = Path('art/cozy_kitchen.png')
im = Image.open(src).convert('RGB').resize((1600,1200), Image.LANCZOS)

# --- gentle highlight bloom, preserving crisp edges ---
gray = im.convert('L')
mask = gray.point(lambda v: 0 if v < 205 else min(255, (v-205)*5))
mask = mask.filter(ImageFilter.GaussianBlur(14))
bloom = Image.new('RGB', im.size, (255, 214, 150))
bloom = Image.composite(bloom, Image.new('RGB', im.size, (0,0,0)), mask)
im = Image.blend(im, ImageChops.screen(im, bloom), 0.12)

# --- a whisper of window haze ---
haze = Image.new('RGB', im.size, (0,0,0))
d = ImageDraw.Draw(haze)
d.ellipse((300, -40, 1320, 930), fill=(205,143,72))
haze = haze.filter(ImageFilter.GaussianBlur(180))
im = Image.blend(im, ImageChops.screen(im, haze), 0.055)

# --- paper/canvas grain ---
noise = Image.effect_noise(im.size, 13).convert('L')
noise = noise.filter(ImageFilter.GaussianBlur(0.3))
grain = Image.merge('RGB', (noise, noise, noise))
im = Image.blend(im, ImageChops.overlay(im, grain), 0.045)

# --- vignette ---
vig = Image.new('L', im.size, 0)
d = ImageDraw.Draw(vig)
d.ellipse((-200, -140, 1800, 1340), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(160))
edge = Image.new('RGB', im.size, (71, 45, 33))
im = Image.composite(im, Image.blend(im, edge, 0.26), vig)

# --- warm highlights, gently cooler shadows ---
r, g, b = im.split()
r = r.point(lambda v: min(255, int(v * 1.018 + 1.5)))
g = g.point(lambda v: min(255, int(v * 1.006)))
b = b.point(lambda v: max(0, int(v * 0.986)))
im = Image.merge('RGB', (r, g, b))

im = ImageEnhance.Color(im).enhance(1.035)
im = ImageEnhance.Contrast(im).enhance(1.045)
im = ImageEnhance.Brightness(im).enhance(1.005)
im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=2))
im.save(out, optimize=True)
print(out, im.size, out.stat().st_size//1024, 'KB')
