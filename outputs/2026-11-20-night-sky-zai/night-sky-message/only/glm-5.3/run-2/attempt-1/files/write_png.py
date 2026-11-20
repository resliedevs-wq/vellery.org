import struct, zlib, sys

def write_gray_png(path, w, h, rows):
    """rows: list of bytearray/bytes, each w bytes (0-255 gray)"""
    raw = b''.join(b'\x00' + bytes(r) for r in rows)
    comp = zlib.compress(raw, 9)
    def chunk(t, d):
        c = struct.pack('>I', len(d)) + t + d
        return c + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 0, 0, 0, 0))
    png += chunk(b'IDAT', comp)
    png += chunk(b'IEND', b'')
    open(path, 'wb').write(png)

def write_rgb_png(path, w, h, rows):
    """rows: list of bytes, each w*3 bytes"""
    raw = b''.join(b'\x00' + bytes(r) for r in rows)
    comp = zlib.compress(raw, 9)
    def chunk(t, d):
        c = struct.pack('>I', len(d)) + t + d
        return c + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', comp)
    png += chunk(b'IEND', b'')
    open(path, 'wb').write(png)
