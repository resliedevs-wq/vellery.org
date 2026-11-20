import sys
from write_png import write_gray_png, write_rgb_png

data = open('raw.rgb','rb').read()
w, h = 800, 500
stride = w * 3

px = [[data[(y*stride + x*3):(y*stride + x*3 + 3)] for x in range(w)] for y in range(h)]

# 1) bit planes per channel (bit 0 = LSB)
for ch, cname in enumerate('RGB'):
    for bit in range(8):
        rows = []
        for y in range(h):
            row = bytearray(w)
            for x in range(w):
                row[x] = 255 if (px[y][x][ch] >> bit) & 1 else 0
            rows.append(row)
        write_gray_png(f'plane_{cname}{bit}.png', w, h, rows)
    print('wrote bit planes for', cname)

# 2) rare-color map: colors occurring <= 3 times highlighted
from collections import Counter
cnt = Counter(bytes(px[y][x]) for y in range(h) for x in range(w))
rare = {c for c, n in cnt.items() if n <= 3}
rows = []
for y in range(h):
    row = bytearray(w*3)
    for x in range(w):
        c = bytes(px[y][x])
        if c in rare:
            row[x*3:x*3+3] = b'\xff\xff\xff'
        else:
            row[x*3:x*3+3] = b'\x00\x00\x00'
    rows.append(row)
write_rgb_png('rare.png', w, h, rows)
print('rare colors:', len(rare), 'of', len(cnt), 'total distinct')

# 3) histogram summary
print('top colors:', cnt.most_common(5))
