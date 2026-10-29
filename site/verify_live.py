#!/usr/bin/env python3
"""Compare every page and script on the live site with dist/, so a deploy that left
something stale is caught right away.

Usage: python3 site/verify_live.py [https://vellery.org]
"""

import hashlib
import json
import pathlib
import sys
import time
import urllib.request

DIST = pathlib.Path(__file__).resolve().parent.parent / "dist"
HOST = (sys.argv[1] if len(sys.argv) > 1 else "https://vellery.org").rstrip("/")


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"})
    return urllib.request.urlopen(request, timeout=20).read()


def stale():
    out = []
    for f in sorted(DIST.rglob("*")):
        if f.is_file() and f.suffix not in (".svg", ".png"):
            url = f"{HOST}/{f.relative_to(DIST)}".replace("index.html", "")
            if hashlib.md5(fetch(url)).digest() != hashlib.md5(f.read_bytes()).digest():
                out.append(url)
    # Matching HTML is insufficient if a build silently removed model reveal.
    expected = json.loads((DIST.parent / "site" / "reveal.generated.js").read_text()
                          .removeprefix("export default ").rstrip(";\n"))
    url = f"{HOST}/api/reveal?task=kitchen-illustration"
    if not expected or json.loads(fetch(url)) != expected:
        out.append(url)
    return out


for attempt in range(4):
    out = stale()
    if not out:
        print("live site matches dist/")
        sys.exit(0)
    time.sleep(5)
print("STALE on the live site:", *out, sep="\n  ")
sys.exit(1)
