import struct, zlib, sys

data = open(sys.argv[1], 'rb').read()
pos = 8
idat = b''
while pos < len(data):
    length = struct.unpack('>I', data[pos:pos+4])[0]
    ctype = data[pos+4:pos+8]
    chunk = data[pos+8:pos+8+length]
    if ctype == b'IHDR':
        w, h, depth, color, comp, filt, inter = struct.unpack('>IIBBBBB', chunk)
        print('IHDR', w, h, depth, color, 'interlace', inter)
    elif ctype == b'IDAT':
        idat += chunk
    pos += 12 + length

raw = zlib.decompress(idat)
channels = {0:1, 2:3, 3:1, 4:2, 6:4}[color]
bpp = channels  # bytes per pixel (8-bit only)
stride = w * bpp
assert len(raw) == (stride + 1) * h, (len(raw), (stride+1)*h)

prev = bytearray(stride)
out = bytearray()
p = 0
for y in range(h):
    f = raw[p]; p += 1
    line = bytearray(raw[p:p+stride]); p += stride
    if f == 1:  # Sub
        for i in range(bpp, stride):
            line[i] = (line[i] + line[i-bpp]) & 0xFF
    elif f == 2:  # Up
        for i in range(stride):
            line[i] = (line[i] + prev[i]) & 0xFF
    elif f == 3:  # Average
        for i in range(stride):
            a = line[i-bpp] if i >= bpp else 0
            line[i] = (line[i] + ((a + prev[i]) >> 1)) & 0xFF
    elif f == 4:  # Paeth
        for i in range(stride):
            a = line[i-bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i-bpp] if i >= bpp else 0
            pp = a + b - c
            pa, pb, pc = abs(pp-a), abs(pp-b), abs(pp-c)
            pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
            line[i] = (line[i] + pr) & 0xFF
    out += line
    prev = line

open(sys.argv[2], 'wb').write(out)
print('wrote', len(out), 'bytes of raw RGB to', sys.argv[2])
