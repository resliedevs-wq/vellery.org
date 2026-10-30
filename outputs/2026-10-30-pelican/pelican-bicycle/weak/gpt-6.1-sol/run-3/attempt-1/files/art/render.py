import re
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

S = 3
im = Image.new('RGB', (1200*S, 1000*S), '#f8f2e5')
d = ImageDraw.Draw(im)

def xy(values):
    return [(round(x*S), round(y*S)) for x, y in values]

def paths(data):
    ts = re.findall(r'[MLQCZ]|-?\d+(?:\.\d+)?', data)
    i, p, start, arr, result = 0, (0, 0), (0, 0), [], []
    while i < len(ts):
        cmd = ts[i]; i += 1
        n = {'M':2, 'L':2, 'Q':4, 'C':6, 'Z':0}[cmd]
        v = list(map(float, ts[i:i+n])); i += n
        if cmd == 'M':
            if arr: result.append(arr)
            p = start = tuple(v); arr = [p]
        elif cmd == 'L':
            p = tuple(v); arr.append(p)
        elif cmd in ('Q', 'C'):
            old = p
            for j in range(1, 61):
                t = j/60; u = 1-t
                if cmd == 'Q':
                    q = tuple(u*u*old[k]+2*u*t*v[k]+t*t*v[k+2] for k in (0,1))
                else:
                    q = tuple(u**3*old[k]+3*u*u*t*v[k]+3*u*t*t*v[k+2]+t**3*v[k+4] for k in (0,1))
                arr.append(q)
            p = q
        elif cmd == 'Z':
            arr.append(start); p = start
    if arr: result.append(arr)
    return result

def visit(e, inherited):
    a = dict(inherited); a.update(e.attrib)
    tag = e.tag.split('}')[-1]
    fill = a.get('fill', '#000000'); stroke = a.get('stroke', 'none')
    fill = None if fill == 'none' else fill
    stroke = None if stroke == 'none' else stroke
    width = round(float(a.get('stroke-width', 1))*S)
    if tag in ('circle', 'ellipse'):
        x, y = float(a['cx']), float(a['cy'])
        rx = float(a.get('r', a.get('rx', 0))); ry = float(a.get('r', a.get('ry', 0)))
        d.ellipse((round((x-rx)*S),round((y-ry)*S),round((x+rx)*S),round((y+ry)*S)), fill=fill, outline=stroke, width=width)
    elif tag == 'rect':
        x,y = float(a.get('x', 0)),float(a.get('y', 0))
        d.rectangle((x*S,y*S,(x+float(a['width']))*S,(y+float(a['height']))*S), fill=fill)
    elif tag == 'path':
        for path in paths(a['d']):
            pts = xy(path)
            if fill: d.polygon(pts, fill=fill)
            if stroke:
                d.line(pts, fill=stroke, width=width, joint='curve')
                if a.get('stroke-linecap') == 'round':
                    r = width/2
                    for x,y in (pts[0],pts[-1]): d.ellipse((x-r,y-r,x+r,y+r),fill=stroke)
    for child in e: visit(child, a)

visit(ET.parse('/tmp/vellery-psac9px6/work/art/pelican.svg').getroot(), {})
im.resize((1200,1000), Image.Resampling.LANCZOS).save('/tmp/vellery-psac9px6/work/art/pelican.png')
