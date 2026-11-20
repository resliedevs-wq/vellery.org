#!/usr/bin/env python3
"""Generate a cozy morning kitchen as a layered SVG illustration."""
import math, random
from pathlib import Path

W, H = 1600, 1200
random.seed(24)
s = []
add = s.append

add(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f4e5cd"/>
    <stop offset="0.52" stop-color="#ecd8ba"/>
    <stop offset="1" stop-color="#dcc2a0"/>
  </linearGradient>
  <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#c58d61"/>
    <stop offset="0.6" stop-color="#b1774f"/>
    <stop offset="1" stop-color="#925b3a"/>
  </linearGradient>
  <linearGradient id="woodcounter" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#d5a06d"/>
    <stop offset="0.22" stop-color="#be8454"/>
    <stop offset="1" stop-color="#96603a"/>
  </linearGradient>
  <linearGradient id="woodtable" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#c48856"/>
    <stop offset="0.55" stop-color="#ad7043"/>
    <stop offset="1" stop-color="#8d5331"/>
  </linearGradient>
  <radialGradient id="tablelight" cx="0.4" cy="0.3" r="0.72">
    <stop offset="0" stop-color="#e8b57c" stop-opacity="0.85"/>
    <stop offset="0.6" stop-color="#c98c58" stop-opacity="0.22"/>
    <stop offset="1" stop-color="#7d492b" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="cabinet" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#879a79"/>
    <stop offset="0.35" stop-color="#788b6b"/>
    <stop offset="1" stop-color="#5e7057"/>
  </linearGradient>
  <linearGradient id="cabinetdoor" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#829475"/>
    <stop offset="0.55" stop-color="#718467"/>
    <stop offset="1" stop-color="#64765b"/>
  </linearGradient>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f6cc80"/>
    <stop offset="0.36" stop-color="#fbe3ad"/>
    <stop offset="0.7" stop-color="#f6e9c6"/>
    <stop offset="1" stop-color="#dbe1b8"/>
  </linearGradient>
  <radialGradient id="sun" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#fff8d6"/>
    <stop offset="0.35" stop-color="#ffe6a2"/>
    <stop offset="1" stop-color="#ffd27b" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="hillfar" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#bdc78d"/>
    <stop offset="1" stop-color="#9dac78"/>
  </linearGradient>
  <linearGradient id="hillnear" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#a3b477"/>
    <stop offset="1" stop-color="#7e9663"/>
  </linearGradient>
  <linearGradient id="curtain" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#d9bd96"/>
    <stop offset="0.18" stop-color="#f3e2c5"/>
    <stop offset="0.45" stop-color="#fff1d7"/>
    <stop offset="0.72" stop-color="#eed9b9"/>
    <stop offset="1" stop-color="#d2b58f"/>
  </linearGradient>
  <radialGradient id="copper" cx="0.35" cy="0.3" r="0.72">
    <stop offset="0" stop-color="#ffd7a0"/>
    <stop offset="0.32" stop-color="#e39a5d"/>
    <stop offset="0.7" stop-color="#b9693d"/>
    <stop offset="1" stop-color="#8c442b"/>
  </radialGradient>
  <radialGradient id="brass" cx="0.3" cy="0.25" r="0.8">
    <stop offset="0" stop-color="#ffe6a7"/>
    <stop offset="0.4" stop-color="#d7ad5f"/>
    <stop offset="1" stop-color="#956b30"/>
  </radialGradient>
  <radialGradient id="ceramic" cx="0.3" cy="0.2" r="0.8">
    <stop offset="0" stop-color="#fffaf0"/>
    <stop offset="0.55" stop-color="#f1e2cb"/>
    <stop offset="1" stop-color="#cfb696"/>
  </radialGradient>
  <radialGradient id="catfur" cx="0.35" cy="0.25" r="0.8">
    <stop offset="0" stop-color="#e7a269"/>
    <stop offset="0.5" stop-color="#d1834f"/>
    <stop offset="1" stop-color="#ae5f36"/>
  </radialGradient>
  <linearGradient id="teal" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#6c8980"/>
    <stop offset="1" stop-color="#405d57"/>
  </linearGradient>
  <linearGradient id="beam" x1="0" y1="0" x2="0.6" y2="1">
    <stop offset="0" stop-color="#ffe3a4" stop-opacity="0.55"/>
    <stop offset="0.45" stop-color="#ffd58c" stop-opacity="0.28"/>
    <stop offset="1" stop-color="#ffd58c" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="jam" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#d46345"/>
    <stop offset="1" stop-color="#9d392b"/>
  </linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#d7a35f" stop-opacity="0.9"/>
    <stop offset="0.3" stop-color="#f3cf8d" stop-opacity="0.7"/>
    <stop offset="1" stop-color="#c68a4d" stop-opacity="0.85"/>
  </linearGradient>
  <pattern id="tilepattern" width="58" height="58" patternUnits="userSpaceOnUse">
    <rect width="58" height="58" fill="#dcc8aa"/>
    <rect x="2" y="2" width="54" height="54" rx="3" fill="#efe0c8"/>
    <path d="M 5 48 Q 20 44 53 49" stroke="#ddcab0" stroke-width="2" fill="none" opacity="0.5"/>
    <path d="M 8 8 Q 30 10 50 7" stroke="#f8ecd8" stroke-width="2" fill="none" opacity="0.7"/>
  </pattern>
  <pattern id="linen" width="14" height="14" patternUnits="userSpaceOnUse">
    <rect width="14" height="14" fill="#f2e4cd"/>
    <path d="M 0 3.5 H 14 M 0 10.5 H 14" stroke="#e3d0b3" stroke-width="1" opacity="0.55"/>
    <path d="M 3.5 0 V 14 M 10.5 0 V 14" stroke="#fff5e4" stroke-width="1" opacity="0.5"/>
  </pattern>
  <pattern id="weave" width="9" height="9" patternUnits="userSpaceOnUse">
    <rect width="9" height="9" fill="#d6b88f"/>
    <path d="M0 2 H9 M0 7 H9" stroke="#c3a178" stroke-width="1" opacity="0.5"/>
    <path d="M2 0 V9 M7 0 V9" stroke="#e6cca6" stroke-width="1" opacity="0.5"/>
  </pattern>
  <clipPath id="windowclip">
    <path d="M 552 586 L 552 330 A 248 248 0 0 1 1048 330 L 1048 586 Z"/>
  </clipPath>
  <clipPath id="tableclip">
    <ellipse cx="820" cy="990" rx="440" ry="155"/>
  </clipPath>
  <clipPath id="curtainLclip">
    <path d="M 492 92 Q 545 88 576 100 L 592 190 Q 570 260 582 330 Q 592 410 568 500 Q 555 570 540 632 L 470 632 Q 482 500 476 380 Q 470 250 480 150 Z"/>
  </clipPath>
  <clipPath id="curtainRclip">
    <path d="M 1108 92 Q 1055 88 1024 100 L 1008 190 Q 1030 260 1018 330 Q 1008 410 1032 500 Q 1045 570 1060 632 L 1130 632 Q 1118 500 1124 380 Q 1130 250 1120 150 Z"/>
  </clipPath>
  <filter id="soft4" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="4"/></filter>
  <filter id="soft8" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="8"/></filter>
  <filter id="soft14" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="14"/></filter>
  <filter id="soft26" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="26"/></filter>
  <filter id="soft45" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="45"/></filter>
  <filter id="glow" x="-100%" y="-100%" width="300%" height="300%" color-interpolation-filters="sRGB">
    <feGaussianBlur stdDeviation="16"/>
  </filter>
  <filter id="shadow" x="-40%" y="-40%" width="180%" height="180%" color-interpolation-filters="sRGB">
    <feDropShadow dx="0" dy="10" stdDeviation="9" flood-color="#5a3727" flood-opacity="0.32"/>
  </filter>
  <filter id="smallshadow" x="-50%" y="-50%" width="200%" height="200%" color-interpolation-filters="sRGB">
    <feDropShadow dx="0" dy="5" stdDeviation="5" flood-color="#4d3024" flood-opacity="0.30"/>
  </filter>
</defs>
<rect width="1600" height="1200" fill="#e5cfb1"/>
''')

# ------------------------------------------------------------------ ROOM
add('<g id="room">')
add('<rect x="0" y="0" width="1600" height="930" fill="url(#wall)"/>')
# mottled plaster
for i in range(18):
    x = random.uniform(-80, 1600); y = random.uniform(0, 900)
    rx = random.uniform(70, 240); ry = random.uniform(40, 150)
    add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{"#f8ecd8" if i%3 else "#d6ba96"}" opacity="{random.uniform(0.025,0.07):.3f}" filter="url(#soft45)"/>')
# warm glow around the window
add('<ellipse cx="800" cy="330" rx="560" ry="480" fill="#ffe6b2" opacity="0.30" filter="url(#soft45)"/>')
add('<ellipse cx="800" cy="250" rx="380" ry="330" fill="#fff1cb" opacity="0.24" filter="url(#soft45)"/>')
# wall/floor seam and floor
add('<rect x="0" y="922" width="1600" height="278" fill="url(#floor)"/>')
add('<path d="M 0 922 H 1600" stroke="#7d4d34" stroke-width="6" opacity="0.35"/>')
add('<path d="M 0 930 H 1600" stroke="#f0c092" stroke-width="2" opacity="0.25"/>')
# floor perspective lines
for y in [946, 972, 1008, 1054, 1112, 1180]:
    add(f'<path d="M 0 {y} H 1600" stroke="#7d4b32" stroke-width="2" opacity="0.16"/>')
for x0 in [30, 180, 335, 500, 675, 850, 1030, 1210, 1385, 1550]:
    xt = 800 + (x0 - 800) * 1.62
    add(f'<path d="M {x0} 925 L {xt:.0f} 1200" stroke="#74452f" stroke-width="2" opacity="0.14"/>')
# floor light pool
add('<ellipse cx="1050" cy="1080" rx="420" ry="160" fill="#ffdca0" opacity="0.20" filter="url(#soft45)"/>')
# baseboard shadow behind cabinets
add('<rect x="0" y="900" width="1600" height="34" fill="#6c4b37" opacity="0.18" filter="url(#soft8)"/>')
add('</g>')

# ------------------------------------------------------------------ WINDOW
add('<g id="window">')
# shadow of the frame on plaster
add('<path d="M 540 624 L 540 338 A 300 300 0 0 1 1110 338 L 1110 624 Z" fill="#967250" opacity="0.16" filter="url(#soft26)"/>')
# outer frame
add('<path d="M 518 612 L 518 330 A 282 282 0 0 1 1082 330 L 1082 612 Z" fill="#f7ead6" stroke="#c5a57e" stroke-width="4"/>')
add('<path d="M 530 606 L 530 332 A 270 270 0 0 1 1070 332 L 1070 606 Z" fill="#e7d0ae"/>')
# glass and view
add('<g clip-path="url(#windowclip)">')
add('<rect x="552" y="70" width="496" height="516" fill="url(#sky)"/>')
add('<ellipse cx="622" cy="128" rx="142" ry="78" fill="#bfd8d7" opacity="0.24" filter="url(#soft45)"/>')
add('<circle cx="936" cy="204" r="120" fill="url(#sun)"/>')
add('<circle cx="936" cy="204" r="47" fill="#fff5ca" opacity="0.95"/>')
# soft sun rays in the sky
add('<g stroke="#fff2c2" stroke-linecap="round" opacity="0.20">')
add('<path d="M 900 242 L 760 330" stroke-width="12" filter="url(#soft14)"/>')
add('<path d="M 958 248 L 1012 364" stroke-width="10" filter="url(#soft14)"/>')
add('<path d="M 884 196 L 700 160" stroke-width="9" filter="url(#soft14)"/>')
add('<path d="M 972 164 L 1042 120" stroke-width="7" filter="url(#soft14)"/>')
add('</g>')
# clouds
add('<g fill="#fff5da" opacity="0.5" filter="url(#soft4)">')
add('<ellipse cx="652" cy="176" rx="70" ry="16"/><ellipse cx="695" cy="166" rx="44" ry="18"/><ellipse cx="618" cy="188" rx="35" ry="10"/>')
add('<ellipse cx="1008" cy="304" rx="62" ry="12"/><ellipse cx="974" cy="296" rx="30" ry="11"/>')
add('</g>')
# distant hills
add('<path d="M 552 446 C 620 408 690 428 748 418 C 812 406 872 436 930 422 C 980 410 1020 426 1048 414 L 1048 586 L 552 586 Z" fill="url(#hillfar)"/>')
add('<path d="M 552 476 C 610 448 664 468 716 456 C 772 444 820 466 878 458 C 936 450 994 466 1048 446 L 1048 586 L 552 586 Z" fill="url(#hillnear)" opacity="0.95"/>')
# little tree line
for i, x in enumerate([575, 620, 660, 720, 790, 835, 880, 920, 1000, 1030]):
    y = 445 + (i % 3) * 6
    r = 16 + (i % 4) * 4
    add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#7f9663" opacity="0.88"/>')
    add(f'<rect x="{x-2}" y="{y}" width="4" height="20" fill="#6b5640" opacity="0.72"/>')
# large garden tree right
add('<path d="M 982 510 C 984 466 986 438 990 408" stroke="#71553c" stroke-width="11" fill="none"/>')
add('<path d="M 990 450 C 968 430 954 424 936 420 M 988 470 C 1012 448 1026 438 1044 430" stroke="#71553c" stroke-width="6" fill="none"/>')
for cx, cy, r, col in [(948,392,50,'#9bab6b'),(1004,374,58,'#a9b878'),(1032,410,42,'#8fa364'),(970,344,38,'#b3bf80'),(922,420,32,'#8da062')]:
    add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="0.9"/>')
# smaller tree left
add('<path d="M 634 516 C 636 482 636 462 632 444" stroke="#765b40" stroke-width="8" fill="none"/>')
for cx, cy, r, col in [(612,430,32,'#9cac70'),(650,418,35,'#a8b77b'),(632,398,28,'#b4c085'),(670,444,24,'#899d64')]:
    add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="0.92"/>')
# extra mid-ground trees for depth
for x, y, r, col in [(702,452,20,'#8a9e68'),(746,444,26,'#7f9560'),(782,458,18,'#91a56f'),(862,450,24,'#8ea26a'),(894,462,17,'#7c9260')]:
    add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" opacity="0.9"/>')
    add(f'<rect x="{x-2}" y="{y}" width="4" height="26" fill="#6c5841" opacity="0.7"/>')
# warm haze at the horizon
add('<rect x="552" y="420" width="496" height="74" fill="#f8e9bd" opacity="0.18" filter="url(#soft14)"/>')
# meadow
add('<path d="M 552 512 C 640 498 720 520 800 508 C 890 494 970 512 1048 502 L 1048 586 L 552 586 Z" fill="#8fa26a"/>')
add('<path d="M 552 540 C 650 526 720 548 806 534 C 900 520 980 542 1048 530 L 1048 586 L 552 586 Z" fill="#7e935f"/>')
# sunlit patches on the lawn
add('<ellipse cx="850" cy="548" rx="130" ry="34" fill="#b1c181" opacity="0.32" filter="url(#soft14)"/>')
add('<ellipse cx="660" cy="562" rx="100" ry="22" fill="#a9ba79" opacity="0.25" filter="url(#soft14)"/>')
# garden path winding toward the window
add('<path d="M 602 590 C 654 566 690 548 706 526 C 720 506 742 496 770 494 L 798 494 C 772 510 766 526 788 542 C 816 562 832 574 846 590 Z" fill="#d9c092" opacity="0.9"/>')
add('<path d="M 636 590 C 674 570 704 552 720 532 C 734 516 750 506 770 503" stroke="#ead6aa" stroke-width="10" fill="none" opacity="0.6"/>')
add('<path d="M 712 590 C 738 574 760 560 788 552" stroke="#c0a477" stroke-width="3" fill="none" opacity="0.35"/>')
# flower beds along the path
random.seed(31)
for i in range(55):
    x = random.uniform(560, 1038); y = random.uniform(522, 582)
    if 600 < x < 850 and y > 540:
        continue
    h = random.uniform(6, 20)
    add(f'<path d="M {x:.0f} {y:.0f} q {random.uniform(-4,4):.1f} {-h:.1f} {random.uniform(-6,6):.1f} {-h*1.1:.1f}" stroke="#b9c385" stroke-width="1.3" opacity="0.6" fill="none"/>')
    if i % 5 == 0:
        fx = x + random.uniform(-5,5); fy = y-h*1.05
        col = random.choice(["#f4d178","#f7eccf","#e7b66c","#d68e68"])
        add(f'<circle cx="{fx:.0f}" cy="{fy:.0f}" r="2.8" fill="{col}" opacity="0.95"/>')
        add(f'<circle cx="{fx+3:.0f}" cy="{fy+1:.0f}" r="1.8" fill="#e8a65c" opacity="0.7"/>')
# fence behind the meadow
for i in range(13):
    x = 580 + i * 38
    add(f'<path d="M {x} 568 L {x} 552" stroke="#c7ac7a" stroke-width="4" opacity="0.55"/>')
add('<path d="M 570 563 H 1040" stroke="#c7ac7a" stroke-width="3" opacity="0.55"/>')
# foreground shrubs at the window edges
for cx, cy, r, col in [(560,560,32,'#6e8758'),(584,584,25,'#5f7b4e'),(1038,558,30,'#70895a'),(1012,584,24,'#5f7a4c')]:
    add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="0.88"/>')
    add(f'<circle cx="{cx-8}" cy="{cy-8}" r="{r*0.5:.0f}" fill="#8ca36a" opacity="0.5"/>')
# tiny birds
add('<path d="M 690 258 q 11 -10 21 0 q 10 -10 21 0" stroke="#6d5f49" stroke-width="3" fill="none" stroke-linecap="round"/>')
add('<path d="M 758 236 q 7 -6 13 0 q 6 -6 13 0" stroke="#6d5f49" stroke-width="2.2" fill="none" stroke-linecap="round" opacity="0.8"/>')
# glass reflections
add('<path d="M 560 330 L 700 90 L 762 90 L 600 500 L 552 512 Z" fill="#fff8dd" opacity="0.10"/>')
add('<path d="M 860 120 L 900 76 L 940 76 L 900 250 L 860 300 Z" fill="#fff8dd" opacity="0.07"/>')
add('<path d="M 552 500 L 1048 280 L 1048 330 L 552 556 Z" fill="#fff4cf" opacity="0.05"/>')
add('<rect x="552" y="70" width="496" height="516" fill="#eab974" opacity="0.06"/>')
add('</g>')  # windowclip
# mullions and inner frame
add('<g stroke-linecap="round">')
add('<rect x="794" y="76" width="12" height="510" fill="#f8ecd9" stroke="#caaa83" stroke-width="2"/>')
add('<rect x="552" y="386" width="496" height="12" fill="#f8ecd9" stroke="#caaa83" stroke-width="2"/>')
add('<path d="M 556 330 A 244 244 0 0 1 1044 330" fill="none" stroke="#f8ecd9" stroke-width="14"/>')
add('<path d="M 556 330 A 244 244 0 0 1 1044 330" fill="none" stroke="#ccad87" stroke-width="2" opacity="0.8"/>')
# inner shadows
add('<path d="M 552 586 L 552 330 A 248 248 0 0 1 1048 330 L 1048 586" fill="none" stroke="#9f7c58" stroke-width="5" opacity="0.35"/>')
add('<path d="M 560 578 L 560 332 A 240 240 0 0 1 1040 332 L 1040 578" fill="none" stroke="#fff7e4" stroke-width="3" opacity="0.6"/>')
add('</g>')
# sill
add('<rect x="500" y="592" width="600" height="28" rx="6" fill="#f6e9d5" stroke="#c8a882" stroke-width="2"/>')
add('<rect x="512" y="620" width="576" height="17" rx="3" fill="#e5cfae"/>')
add('<path d="M 516 636 H 1084" stroke="#a9835d" stroke-width="2" opacity="0.45"/>')
add('<path d="M 530 600 H 1070" stroke="#fff9eb" stroke-width="2" opacity="0.7"/>')
# wall crack detail
add('<path d="M 360 186 C 374 200 362 212 376 226 C 386 236 380 248 390 260" stroke="#b3926f" stroke-width="1.2" opacity="0.25" fill="none"/>')
add('</g>')

# ------------------------------------------------------------------ CURTAINS
add('<g id="curtains">')
add('<path d="M 474 86 H 1126" stroke="#7a5a3b" stroke-width="8" stroke-linecap="round"/>')
add('<circle cx="466" cy="86" r="11" fill="url(#brass)"/><circle cx="1134" cy="86" r="11" fill="url(#brass)"/>')
# soft shadow of curtains
add('<path d="M 486 100 L 602 100 L 600 625 L 476 625 Z" fill="#a77d55" opacity="0.13" filter="url(#soft14)"/>')
add('<path d="M 1022 100 L 1126 100 L 1126 625 L 1058 625 Z" fill="#a77d55" opacity="0.14" filter="url(#soft14)"/>')
# left curtain
add('<path d="M 492 92 Q 545 88 576 100 L 592 190 Q 570 260 582 330 Q 592 410 568 500 Q 555 570 540 632 L 470 632 Q 482 500 476 380 Q 470 250 480 150 Z" fill="url(#curtain)" stroke="#c8a982" stroke-width="2"/>')
add('<g clip-path="url(#curtainLclip)">')
for x, col, op, w in [(500,'#c4a27b',0.45,3),(525,'#fff4dd',0.65,5),(548,'#c8a67d',0.35,3),(570,'#fff1d5',0.5,4)]:
    add(f'<path d="M {x} 95 C {x-7} 230 {x+8} 330 {x-5} 440 C {x-12} 520 {x-2} 590 {x-8} 636" stroke="{col}" stroke-width="{w}" fill="none" opacity="{op}"/>')
# fine slub texture and a woven hem
for y in range(160, 610, 38):
    add(f'<path d="M 480 {y} q 50 5 102 0" stroke="#d7bb95" stroke-width="1.2" fill="none" opacity="0.32"/>')
add('<path d="M 476 604 Q 518 610 556 604" stroke="#b9976e" stroke-width="2" fill="none" opacity="0.35"/>')
add('<path d="M 478 610 Q 518 616 552 610" stroke="#f8e8cb" stroke-width="1.5" fill="none" opacity="0.5"/>')
add('</g>')
# right curtain
add('<path d="M 1108 92 Q 1055 88 1024 100 L 1008 190 Q 1030 260 1018 330 Q 1008 410 1032 500 Q 1045 570 1060 632 L 1130 632 Q 1118 500 1124 380 Q 1130 250 1120 150 Z" fill="url(#curtain)" stroke="#c8a982" stroke-width="2"/>')
add('<g clip-path="url(#curtainRclip)">')
for x, col, op, w in [(1090,'#c4a27b',0.45,3),(1068,'#fff4dd',0.65,5),(1045,'#c8a67d',0.35,3),(1028,'#fff1d5',0.5,4)]:
    add(f'<path d="M {x} 95 C {x+7} 230 {x-8} 330 {x+5} 440 C {x+12} 520 {x+2} 590 {x+8} 636" stroke="{col}" stroke-width="{w}" fill="none" opacity="{op}"/>')
for y in range(160, 610, 38):
    add(f'<path d="M 1018 {y} q 50 5 102 0" stroke="#d7bb95" stroke-width="1.2" fill="none" opacity="0.32"/>')
add('<path d="M 1062 604 Q 1100 610 1124 604" stroke="#b9976e" stroke-width="2" fill="none" opacity="0.35"/>')
add('<path d="M 1060 610 Q 1094 616 1122 610" stroke="#f8e8cb" stroke-width="1.5" fill="none" opacity="0.5"/>')
add('</g>')
# rings
for x in [480, 500, 520, 1040, 1060, 1080, 1100, 1120]:
    add(f'<circle cx="{x}" cy="87" r="6" fill="none" stroke="#8a6644" stroke-width="2.5"/>')
add('</g>')

# ------------------------------------------------------------------ WALL DECOR
add('<g id="walldecor">')
# brass rail for copper pans
add('<path d="M 92 150 H 432" stroke="#8b673d" stroke-width="5" stroke-linecap="round"/>')
for x in [110, 196, 284, 370, 420]:
    add(f'<path d="M {x} 150 v 12" stroke="#8b673d" stroke-width="4" stroke-linecap="round"/>')
# copper pan 1
add('<g filter="url(#smallshadow)">')
add('<path d="M 172 218 L 166 160" stroke="#a85b35" stroke-width="12" stroke-linecap="round"/>')
add('<circle cx="172" cy="278" r="70" fill="url(#copper)" stroke="#8b452b" stroke-width="4"/>')
add('<circle cx="172" cy="278" r="57" fill="none" stroke="#f4b57c" stroke-width="3" opacity="0.55"/>')
add('<path d="M 129 247 A 52 52 0 0 1 198 231" stroke="#ffe0ae" stroke-width="8" fill="none" opacity="0.55" stroke-linecap="round"/>')
add('<ellipse cx="172" cy="278" rx="46" ry="10" fill="#8f4529" opacity="0.35"/>')
add('</g>')
# copper pan 2
add('<g filter="url(#smallshadow)">')
add('<path d="M 288 231 L 300 160" stroke="#a85b35" stroke-width="10" stroke-linecap="round"/>')
add('<circle cx="288" cy="270" r="54" fill="url(#copper)" stroke="#8b452b" stroke-width="4"/>')
add('<path d="M 248 250 A 42 42 0 0 1 309 235" stroke="#ffe0ae" stroke-width="6" fill="none" opacity="0.55" stroke-linecap="round"/>')
add('<ellipse cx="288" cy="270" rx="35" ry="8" fill="#8f4529" opacity="0.30"/>')
add('</g>')
# copper pan 3
add('<g filter="url(#smallshadow)">')
add('<path d="M 385 287 L 394 174" stroke="#a85b35" stroke-width="8" stroke-linecap="round"/>')
add('<circle cx="385" cy="318" r="40" fill="url(#copper)" stroke="#8b452b" stroke-width="3"/>')
add('<path d="M 355 302 A 30 30 0 0 1 401 291" stroke="#ffe0ae" stroke-width="5" fill="none" opacity="0.5" stroke-linecap="round"/>')
add('</g>')
# hanging bundle of dried herbs
add('<g transform="translate(446 196)" opacity="0.95">')
add('<path d="M 8 0 C 5 8 8 14 9 21" stroke="#8f6d47" stroke-width="2.5" fill="none"/>')
add('<path d="M 3 20 Q 10 25 16 20" stroke="#b39165" stroke-width="3" fill="none"/>')
add('<path d="M 9 23 C 4 43 3 60 1 82 M 10 23 C 12 44 14 61 15 84 M 11 22 C 18 40 23 57 29 76 M 9 24 C 15 44 18 62 22 88" stroke="#8b8158" stroke-width="2" fill="none"/>')
for cx, cy, rot, col in [(4,48,-18,'#a9ad84'),(12,40,14,'#9da57b'),(17,55,28,'#b0b28a'),(22,64,18,'#8f9a70'),(8,66,-22,'#a5a97d'),(15,72,12,'#989e73'),(4,73,-15,'#b8b58c'),(25,70,30,'#969d74')]:
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="8" ry="3.5" fill="{col}" transform="rotate({rot} {cx} {cy})"/>')
for cx, cy in [(1,82),(15,84),(29,76),(22,88)]:
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="3.5" ry="6.5" fill="#8e8296"/>')
add('<path d="M 4 24 q 8 5 15 -1" stroke="#d2b184" stroke-width="2" fill="none" opacity="0.8"/>')
add('</g>')
# wall clock
add('<g filter="url(#smallshadow)">')
add('<circle cx="1350" cy="232" r="68" fill="url(#brass)" stroke="#8b642f" stroke-width="3"/>')
add('<circle cx="1350" cy="232" r="56" fill="#f7ecda" stroke="#cba873" stroke-width="2"/>')
for i in range(12):
    a = math.radians(i * 30)
    x1 = 1350 + 46 * math.sin(a); y1 = 232 - 46 * math.cos(a)
    x2 = 1350 + 51 * math.sin(a); y2 = 232 - 51 * math.cos(a)
    add(f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="#7c6348" stroke-width="{2.4 if i%3==0 else 1.2}" stroke-linecap="round" opacity="0.75"/>')
# hands at 7:10
add('<path d="M 1350 232 L 1320 212" stroke="#5c4939" stroke-width="5" stroke-linecap="round"/>')
add('<path d="M 1350 232 L 1388 210" stroke="#5c4939" stroke-width="4" stroke-linecap="round"/>')
add('<circle cx="1350" cy="232" r="5" fill="#8f6b3e"/>')
add('<circle cx="1350" cy="232" r="62" fill="none" stroke="#f4d79e" stroke-width="1.5" opacity="0.6"/>')
add('</g>')
# small framed botanical print left of clock (very subtle)
add('<g transform="translate(1181 208)" filter="url(#smallshadow)" opacity="0.95">')
add('<rect x="0" y="0" width="78" height="104" rx="3" fill="#a67d50"/>')
add('<rect x="6" y="6" width="66" height="92" fill="#f3e6ce"/>')
add('<path d="M 39 84 C 39 62 37 46 42 30" stroke="#7d906c" stroke-width="2" fill="none"/>')
add('<path d="M 41 61 C 30 56 24 48 22 40 M 41 50 C 52 45 58 38 60 30 M 40 68 C 31 66 24 60 20 54" stroke="#7d906c" stroke-width="1.7" fill="none"/>')
add('<ellipse cx="22" cy="38" rx="7" ry="3.5" fill="#91a37c" transform="rotate(-35 22 38)"/>')
add('<ellipse cx="60" cy="28" rx="7" ry="3.5" fill="#91a37c" transform="rotate(40 60 28)"/>')
add('<ellipse cx="19" cy="52" rx="6" ry="3" fill="#91a37c" transform="rotate(-30 19 52)"/>')
add('<circle cx="42" cy="28" r="4" fill="#d7a35f"/>')
add('</g>')
add('</g>')

# ------------------------------------------------------------------ SHELVES
add('<g id="leftshelf">')
# shelf
add('<rect x="66" y="496" width="408" height="18" rx="3" fill="#b77f50" stroke="#895934" stroke-width="2"/>')
add('<path d="M 70 499 H 468" stroke="#efc28e" stroke-width="3" opacity="0.7"/>')
add('<path d="M 66 514 H 474" stroke="#7e4d2d" stroke-width="3" opacity="0.45"/>')
# brackets
for x in [98, 438]:
    add(f'<path d="M {x} 514 L {x} 552 L {x+38} 514" fill="#9a643c" stroke="#7b4c2c" stroke-width="2"/>')
# bowls stack
for i, (cx, cy, rx, ry) in enumerate([(140,468,48,16),(146,452,42,14),(152,438,36,12)]):
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#f2e2c9" stroke="#c8ab87" stroke-width="2"/>')
    add(f'<path d="M {cx-rx+5} {cy} Q {cx} {cy+ry+12} {cx+rx-5} {cy}" fill="#e8d4b7" stroke="#c8ab87" stroke-width="2"/>')
    add(f'<path d="M {cx-rx+8} {cy-2} Q {cx} {cy+6} {cx+rx-8} {cy-2}" fill="none" stroke="#8eaa9a" stroke-width="2" opacity="0.6"/>')
# canister
add('<g>')
add('<rect x="230" y="426" width="66" height="66" rx="9" fill="#dbe3d8" stroke="#a4b2a5" stroke-width="2"/>')
add('<rect x="226" y="416" width="74" height="16" rx="7" fill="#c4b18f" stroke="#967e5f" stroke-width="2"/>')
add('<circle cx="263" cy="423" r="4" fill="#8b6d4a"/>')
add('<rect x="240" y="454" width="46" height="27" rx="3" fill="#f2e8d4" opacity="0.8"/>')
add('<path d="M 250 465 H 276 M 250 473 H 268" stroke="#8fa083" stroke-width="2" opacity="0.8"/>')
add('</g>')
# potted plant on shelf
add('<g>')
add('<path d="M 337 492 L 343 442 H 395 L 401 492 Z" fill="#c4704c" stroke="#9c5136" stroke-width="2"/>')
add('<path d="M 343 456 H 395" stroke="#e9a077" stroke-width="4" opacity="0.5"/>')
add('<path d="M 368 443 C 365 421 354 406 343 398 M 369 440 C 375 416 389 405 402 400 M 368 444 C 369 424 380 414 388 410" stroke="#6f8259" stroke-width="3" fill="none"/>')
for cx, cy, rot in [(341,394,-20),(405,396,25),(389,407,10),(348,420,-15),(378,398,5)]:
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="13" ry="7" fill="#7f9364" transform="rotate({rot} {cx} {cy})"/>')
add('</g>')
# hanging mugs below shelf
for x, col in [(170, '#e9d6b8'), (282, '#b96e50')]:
    add(f'<path d="M {x} 514 v 18" stroke="#7a573c" stroke-width="3"/>')
    add(f'<path d="M {x-17} 531 q 0 34 17 34 q 17 0 17 -34 Z" fill="{col}" stroke="#8e6f52" stroke-width="2"/>')
    add(f'<path d="M {x+17} 541 q 20 -2 17 14 q -2 13 -18 10" fill="none" stroke="#8e6f52" stroke-width="5"/>')
    add(f'<ellipse cx="{x}" cy="531" rx="17" ry="5" fill="#f1dfc2" stroke="#8e6f52" stroke-width="2"/>')
    add(f'<path d="M {x-10} 539 q 3 17 9 20" stroke="#fff7e6" stroke-width="3" fill="none" opacity="0.5"/>')
add('</g>')

# right shelves
add('<g id="rightshelves">')
for sy, sx in [(390, 1160), (522, 1160)]:
    add(f'<rect x="{sx}" y="{sy}" width="386" height="16" rx="3" fill="#b77f50" stroke="#895934" stroke-width="2"/>')
    add(f'<path d="M {sx+4} {sy+3} H {sx+382}" stroke="#efc28e" stroke-width="3" opacity="0.7"/>')
    add(f'<path d="M {sx} {sy+16} H {sx+386}" stroke="#7e4d2d" stroke-width="3" opacity="0.45"/>')
    for bx in [sx+24, sx+352]:
        add(f'<path d="M {bx} {sy+16} L {bx} {sy+52} L {bx+34} {sy+16}" fill="#9a643c" stroke="#7b4c2c" stroke-width="2"/>')
# top shelf: plates
for i, (cx, cy, rx, ry) in enumerate([(1218,365,44,13),(1222,350,38,11),(1225,337,32,9)]):
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#f4e7d3" stroke="#c6a986" stroke-width="2"/>')
    add(f'<path d="M {cx-rx+5} {cy} Q {cx} {cy+ry+8} {cx+rx-5} {cy}" fill="#e9d5b8" stroke="#c6a986" stroke-width="2"/>')
# jug
add('<path d="M 1286 383 C 1288 348 1295 329 1311 323 L 1348 323 C 1364 329 1371 348 1373 383 Z" fill="#d6ded0" stroke="#9baa9d" stroke-width="2"/>')
add('<path d="M 1311 324 Q 1330 338 1348 324" fill="none" stroke="#f4f0e1" stroke-width="5" opacity="0.7"/>')
add('<path d="M 1310 346 Q 1330 354 1350 346" stroke="#8fa18c" stroke-width="2" fill="none" opacity="0.6"/>')
add('<path d="M 1371 345 q 22 2 19 17 q -3 13 -21 9" fill="none" stroke="#9baa9d" stroke-width="6"/>')
# copper pot
add('<g filter="url(#smallshadow)"><path d="M 1402 382 L 1402 362 Q 1402 346 1421 342 L 1451 342 Q 1470 346 1470 362 L 1470 382 Z" fill="url(#copper)" stroke="#8b452b" stroke-width="2"/><path d="M 1412 350 H 1460" stroke="#ffe0ae" stroke-width="3" opacity="0.55"/><path d="M 1468 352 q 16 4 13 16" stroke="#8b452b" stroke-width="5" fill="none"/><path d="M 1420 342 q 16 -12 32 0" stroke="#9a6b3c" stroke-width="4" fill="none"/></g>')
# trailing plant top shelf
add('<g><path d="M 1486 384 L 1497 348 H 1532 L 1543 384 Z" fill="#c47d58" stroke="#9a5b3e" stroke-width="2"/><path d="M 1499 352 C 1488 338 1478 330 1468 326 M 1507 350 C 1510 328 1518 314 1530 306 M 1522 352 C 1538 342 1548 338 1558 340" stroke="#72865d" stroke-width="2.5" fill="none"/>')
for cx, cy, rot in [(1465,324,-20),(1532,303,20),(1559,341,10),(1492,335,-10),(1514,323,5)]:
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="9" ry="5" fill="#829568" transform="rotate({rot} {cx} {cy})"/>')
add('</g>')
# bottom shelf: jars and bowls
add('<rect x="1190" y="474" width="58" height="48" rx="5" fill="#e8d8bc" stroke="#b69a77" stroke-width="2"/>')
add('<rect x="1184" y="465" width="70" height="13" rx="5" fill="#bfa17c" stroke="#947550" stroke-width="2"/>')
add('<rect x="1262" y="462" width="42" height="60" rx="4" fill="#c8845d" stroke="#9c5b3c" stroke-width="2"/>')
add('<rect x="1258" y="453" width="50" height="12" rx="4" fill="#e0c9a9" stroke="#aa8c68" stroke-width="2"/>')
for i, (cx, cy, rx, ry) in enumerate([(1355,512,42,12),(1360,498,36,10)]):
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#f2e2ca" stroke="#c6a986" stroke-width="2"/>')
add('<g transform="translate(1460 468)"><rect x="0" y="0" width="15" height="54" fill="#9b6a48"/><rect x="17" y="7" width="13" height="47" fill="#c08a5f"/><rect x="32" y="-4" width="17" height="58" fill="#7f8f73"/><path d="M 4 10 H 11 M 21 18 H 27 M 38 8 H 45" stroke="#e8d2ae" stroke-width="2"/></g>')
# tiny mug
add('<path d="M 1520 500 q 0 23 14 23 q 14 0 14 -23 Z" fill="#e9d6b8" stroke="#a38360" stroke-width="2"/>')
add('<path d="M 1548 505 q 14 0 11 10 q -2 8 -12 6" fill="none" stroke="#a38360" stroke-width="4"/>')
add('</g>')

# ------------------------------------------------------------------ COUNTER & CABINETS
add('<g id="cabinets">')
# tiled backsplash
add('<rect x="0" y="618" width="1600" height="96" fill="url(#tilepattern)"/>')
add('<rect x="0" y="618" width="1600" height="96" fill="#e8cda4" opacity="0.12"/>')
add('<rect x="0" y="618" width="1600" height="96" fill="none" stroke="#b79b78" stroke-width="3" opacity="0.5"/>')
add('<path d="M 0 622 H 1600" stroke="#fff3df" stroke-width="2" opacity="0.4"/>')
# countertop
add('<rect x="0" y="710" width="1600" height="34" fill="url(#woodcounter)"/>')
add('<path d="M 0 713 H 1600" stroke="#efc18d" stroke-width="4" opacity="0.8"/>')
add('<path d="M 0 741 H 1600" stroke="#6e442b" stroke-width="4" opacity="0.65"/>')
for i in range(28):
    y = 716 + random.uniform(0, 20)
    add(f'<path d="M {random.randint(0,1500)} {y:.0f} q 40 {random.uniform(-3,3):.1f} 90 0" stroke="#8d5a38" stroke-width="1.2" opacity="0.25" fill="none"/>')
# cabinet body
add('<rect x="0" y="742" width="1600" height="198" fill="url(#cabinet)"/>')
add('<rect x="0" y="742" width="1600" height="12" fill="#9cac8b" opacity="0.55"/>')
add('<rect x="0" y="925" width="1600" height="15" fill="#4d5c47"/>')
# cabinet door helper shapes
def drawer(x, y, w, h, knob=True):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="url(#cabinetdoor)" stroke="#53644d" stroke-width="2"/>')
    add(f'<rect x="{x+8}" y="{y+7}" width="{w-16}" height="{h-14}" rx="3" fill="none" stroke="#9cad8c" stroke-width="2" opacity="0.7"/>')
    add(f'<path d="M {x+10} {y+9} H {x+w-10}" stroke="#b7c5a6" stroke-width="2" opacity="0.4"/>')
    if knob:
        add(f'<circle cx="{x+w/2}" cy="{y+h/2}" r="7" fill="url(#brass)" stroke="#8e652f" stroke-width="1.5"/>')
        add(f'<circle cx="{x+w/2-2}" cy="{y+h/2-2}" r="2.5" fill="#ffe9b5" opacity="0.8"/>')

def door(x, y, w, h, knob='right'):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="url(#cabinetdoor)" stroke="#53644d" stroke-width="2"/>')
    add(f'<rect x="{x+12}" y="{y+13}" width="{w-24}" height="{h-26}" rx="3" fill="#6c7e61" stroke="#4e6049" stroke-width="2"/>')
    add(f'<rect x="{x+17}" y="{y+18}" width="{w-34}" height="{h-36}" rx="2" fill="none" stroke="#91a281" stroke-width="1.6" opacity="0.65"/>')
    kx = x + w - 20 if knob == 'right' else x + 20
    add(f'<circle cx="{kx}" cy="{y+h/2}" r="7" fill="url(#brass)" stroke="#8e652f" stroke-width="1.5"/>')
    add(f'<circle cx="{kx-2}" cy="{y+h/2-2}" r="2.5" fill="#ffe9b5" opacity="0.8"/>')

# left drawers/doors (partly behind chair and table)
drawer(24, 756, 300, 52)
door(24, 818, 142, 100, 'right')
door(176, 818, 148, 100, 'left')
# center-left cabinet (behind table)
drawer(334, 756, 290, 52)
door(334, 818, 138, 100, 'right')
door(482, 818, 142, 100, 'left')
# right of sink
drawer(1008, 756, 240, 52)
door(1008, 818, 112, 100, 'right')
door(1130, 818, 118, 100, 'left')
# toe-kick shadows
add('<path d="M 0 924 H 1600" stroke="#3f4d3a" stroke-width="3" opacity="0.5"/>')
add('</g>')

# ------------------------------------------------------------------ SINK
add('<g id="sink">')
# shadow under sink
add('<ellipse cx="810" cy="748" rx="140" ry="20" fill="#4d3024" opacity="0.25" filter="url(#soft8)"/>')
# basin opening
add('<ellipse cx="810" cy="713" rx="118" ry="20" fill="#5e4938" stroke="#efe0c8" stroke-width="5"/>')
add('<ellipse cx="810" cy="710" rx="103" ry="12" fill="#3e3027"/>')
add('<path d="M 710 714 C 740 724 880 724 910 714" stroke="#bca683" stroke-width="3" fill="none" opacity="0.6"/>')
# farmhouse apron
add('<path d="M 696 727 L 696 788 Q 696 812 724 812 L 896 812 Q 924 812 924 788 L 924 727 Z" fill="#f2e6d2" stroke="#c8b394" stroke-width="3"/>')
add('<path d="M 710 730 V 786 Q 710 799 726 799 L 894 799 Q 910 799 910 786 V 730" fill="none" stroke="#d4bf9f" stroke-width="2"/>')
for i in range(5):
    x = 730 + i * 36
    add(f'<path d="M {x} 732 V 797" stroke="#d8c4a5" stroke-width="2" opacity="0.55"/>')
add('<path d="M 704 735 C 744 745 876 745 916 735" stroke="#fff8e9" stroke-width="4" fill="none" opacity="0.6"/>')
# faucet
add('<g filter="url(#smallshadow)">')
add('<rect x="842" y="700" width="44" height="14" rx="6" fill="url(#brass)" stroke="#8e652f" stroke-width="2"/>')
add('<path d="M 858 704 V 652 C 858 623 878 610 900 610 C 922 610 939 625 939 650 V 665" stroke="url(#brass)" stroke-width="13" fill="none" stroke-linecap="round"/>')
add('<path d="M 858 704 V 652 C 858 623 878 610 900 610 C 922 610 939 625 939 650 V 665" stroke="#ffe3a2" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.55"/>')
add('<path d="M 933 663 L 945 663 L 945 684 L 933 684 Z" fill="url(#brass)" stroke="#8e652f" stroke-width="2"/>')
add('<path d="M 933 681 q 6 14 12 0" fill="#d9b36e" opacity="0.7"/>')
# handle
add('<path d="M 858 690 L 830 690" stroke="#8e652f" stroke-width="7" stroke-linecap="round"/>')
add('<circle cx="826" cy="690" r="8" fill="url(#brass)" stroke="#8e652f" stroke-width="2"/>')
add('</g>')
# soap bottle
add('<g filter="url(#smallshadow)">')
add('<rect x="952" y="673" width="28" height="42" rx="6" fill="#c78d52" stroke="#8f5b32" stroke-width="2"/>')
add('<rect x="958" y="662" width="16" height="13" rx="3" fill="#8a663c"/>')
add('<path d="M 966 662 v -10 h 16" stroke="#7a5938" stroke-width="4" fill="none"/>')
add('<rect x="956" y="684" width="20" height="17" rx="2" fill="#f0dfc2" opacity="0.75"/>')
add('</g>')
# sink edge shadow
add('<path d="M 690 812 H 930" stroke="#b69c79" stroke-width="3" opacity="0.35"/>')
add('</g>')

# ------------------------------------------------------------------ STOVE
add('<g id="stove">')
# backguard
add('<rect x="1276" y="656" width="276" height="80" rx="8" fill="#e8d9bd" stroke="#b79a73" stroke-width="3"/>')
add('<rect x="1286" y="666" width="256" height="60" rx="5" fill="#d8c5a5" stroke="#c0a680" stroke-width="2"/>')
for i in range(4):
    x = 1312 + i * 66
    add(f'<circle cx="{x}" cy="696" r="12" fill="#4f4a41" stroke="#8e6d4e" stroke-width="2"/>')
    add(f'<path d="M {x} 686 V 696" stroke="#e7d7ba" stroke-width="3"/>')
# cooktop
add('<rect x="1268" y="719" width="292" height="26" rx="5" fill="#383733" stroke="#232220" stroke-width="2"/>')
add('<path d="M 1272 722 H 1556" stroke="#7d7568" stroke-width="2" opacity="0.6"/>')
for x in [1338, 1480]:
    add(f'<ellipse cx="{x}" cy="731" rx="44" ry="12" fill="none" stroke="#1e1d1b" stroke-width="5"/>')
    for a in range(0, 360, 60):
        x1 = x + 32 * math.cos(math.radians(a)); y1 = 731 + 8 * math.sin(math.radians(a))
        x2 = x + 40 * math.cos(math.radians(a)); y2 = 731 + 10 * math.sin(math.radians(a))
        add(f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="#1e1d1b" stroke-width="3"/>')
# body
add('<rect x="1280" y="737" width="270" height="195" rx="8" fill="#eadcc2" stroke="#b79a73" stroke-width="3"/>')
add('<path d="M 1290 744 H 1540" stroke="#fff3dc" stroke-width="3" opacity="0.7"/>')
# oven door
add('<rect x="1298" y="774" width="234" height="132" rx="6" fill="#dfcfb3" stroke="#b0936d" stroke-width="3"/>')
add('<rect x="1312" y="790" width="206" height="58" rx="4" fill="#7e7666" stroke="#5c5548" stroke-width="2"/>')
add('<rect x="1320" y="798" width="190" height="42" rx="3" fill="#413d36"/>')
add('<path d="M 1330 806 Q 1370 802 1400 812" stroke="#c2a471" stroke-width="2" opacity="0.25" fill="none"/>')
add('<path d="M 1318 866 H 1512" stroke="#b99b73" stroke-width="5" stroke-linecap="round"/>')
add('<path d="M 1318 863 H 1512" stroke="#f8e8cb" stroke-width="2" stroke-linecap="round" opacity="0.7"/>')
add('<rect x="1298" y="890" width="234" height="34" rx="4" fill="#e3d3b7" stroke="#b0936d" stroke-width="2"/>')
add('<circle cx="1415" cy="907" r="4" fill="#a98557"/>')
# side highlights and shadow
add('<path d="M 1284 748 V 925" stroke="#fff3db" stroke-width="4" opacity="0.5"/>')
add('<path d="M 1545 745 V 928" stroke="#7b5c3e" stroke-width="4" opacity="0.25"/>')
# kettle
add('<g filter="url(#smallshadow)">')
add('<path d="M 1338 719 C 1308 719 1300 695 1308 675 C 1315 657 1358 655 1367 674 C 1375 693 1367 719 1338 719 Z" fill="url(#copper)" stroke="#8b452b" stroke-width="3"/>')
add('<path d="M 1318 679 C 1324 666 1352 664 1358 678" stroke="#ffe0ae" stroke-width="5" fill="none" opacity="0.55"/>')
add('<path d="M 1363 681 L 1392 660 L 1396 665 L 1369 689" fill="#b9693d" stroke="#8b452b" stroke-width="2"/>')
add('<path d="M 1318 665 C 1325 638 1352 638 1359 664" fill="none" stroke="#7a4a2f" stroke-width="7"/>')
add('<path d="M 1325 662 C 1332 646 1351 646 1355 662" fill="none" stroke="#d39963" stroke-width="3" opacity="0.7"/>')
add('<ellipse cx="1338" cy="672" rx="27" ry="7" fill="#8f4529" opacity="0.45"/>')
add('</g>')
# tiny steam above kettle
add('<path d="M 1342 646 C 1320 622 1360 610 1340 584 C 1325 564 1352 550 1342 532" stroke="#fff8e5" stroke-width="7" fill="none" opacity="0.28" filter="url(#soft4)" stroke-linecap="round"/>')
add('</g>')

# ------------------------------------------------------------------ COUNTER ITEMS
add('<g id="counteritems">')
# left bowl stack
for i, (cx, cy, rx, ry) in enumerate([(118,694,48,14),(123,681,43,12),(128,669,38,10)]):
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#efe0c7" stroke="#bd9f7b" stroke-width="2"/>')
    add(f'<path d="M {cx-rx+5} {cy} Q {cx} {cy+ry+10} {cx+rx-5} {cy}" fill="#e5d1b3" stroke="#bd9f7b" stroke-width="2"/>')
    add(f'<path d="M {cx-rx+9} {cy-1} Q {cx} {cy+5} {cx+rx-9} {cy-1}" fill="none" stroke="#819a88" stroke-width="2" opacity="0.6"/>')
# utensil crock
add('<g filter="url(#smallshadow)">')
add('<path d="M 230 705 L 238 628 L 302 628 L 310 705 Z" fill="#cfc0a4" stroke="#9b8464" stroke-width="2"/>')
add('<path d="M 240 642 H 300" stroke="#e9dcc6" stroke-width="5" opacity="0.6"/>')
for x, col in [(248,'#8a6b44'),(261,'#b1774f'),(275,'#7d8d69'),(289,'#9e6a46')]:
    add(f'<path d="M {x} 630 L {x-5} 574" stroke="{col}" stroke-width="6" stroke-linecap="round"/>')
    add(f'<path d="M {x-11} 572 q 6 -13 12 0" fill="{col}" opacity="0.8"/>')
add('</g>')
# bread board leaning
add('<g filter="url(#smallshadow)">')
add('<path d="M 362 707 L 382 610 Q 420 597 456 616 L 450 712 Z" fill="#c79460" stroke="#8f5f39" stroke-width="3"/>')
add('<path d="M 378 618 Q 420 606 450 624" stroke="#eac08a" stroke-width="4" fill="none" opacity="0.6"/>')
# bread loaf
add('<path d="M 382 674 C 382 646 410 637 429 648 C 445 657 446 679 443 695 L 390 698 Z" fill="#d8a258" stroke="#a26b32" stroke-width="2"/>')
add('<path d="M 395 656 q 12 -10 25 -2 M 391 672 q 15 -12 32 -2" stroke="#f0c987" stroke-width="3" opacity="0.65" fill="none"/>')
add('<path d="M 383 682 q 30 10 58 -1" stroke="#b0783d" stroke-width="2" opacity="0.5" fill="none"/>')
add('</g>')
# jar of honey right of sink
add('<g filter="url(#smallshadow)">')
add('<path d="M 1170 714 L 1174 668 Q 1174 660 1183 660 L 1211 660 Q 1220 660 1220 668 L 1224 714 Z" fill="url(#glass)" stroke="#a97643" stroke-width="2"/>')
add('<rect x="1172" y="651" width="50" height="12" rx="4" fill="#c8a476" stroke="#94744e" stroke-width="2"/>')
add('<path d="M 1182 678 H 1212" stroke="#f6e2bd" stroke-width="3" opacity="0.7"/>')
add('<rect x="1180" y="686" width="34" height="17" rx="2" fill="#f2e0c2" opacity="0.8"/>')
add('<path d="M 1188 692 H 1206 M 1188 698 H 1201" stroke="#a8764d" stroke-width="1.5" opacity="0.7"/>')
add('</g>')
# herb pot right counter
add('<g>')
add('<path d="M 1100 714 L 1107 681 H 1145 L 1152 714 Z" fill="#bd7150" stroke="#945039" stroke-width="2"/>')
add('<path d="M 1114 682 C 1107 665 1100 657 1092 651 M 1121 680 C 1124 658 1131 650 1142 645 M 1133 682 C 1145 674 1152 671 1160 673" stroke="#6d8158" stroke-width="2.5" fill="none"/>')
for cx, cy, rot in [(1090,649,-20),(1143,643,15),(1161,672,10),(1118,661,-8)]:
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="9" ry="5" fill="#7f9462" transform="rotate({rot} {cx} {cy})"/>')
add('</g>')
add('</g>')

# ------------------------------------------------------------------ SILL PLANTS
add('<g id="sillplants">')
# basil on left sill
add('<g filter="url(#smallshadow)">')
add('<path d="M 568 592 L 576 534 H 618 L 626 592 Z" fill="#c1714c" stroke="#995039" stroke-width="2"/>')
add('<path d="M 576 546 H 618" stroke="#e39b74" stroke-width="4" opacity="0.5"/>')
add('<path d="M 596 534 C 594 512 586 500 576 494 M 598 532 C 601 506 611 494 622 486 M 597 534 C 596 514 602 500 612 492" stroke="#687c54" stroke-width="2.6" fill="none"/>')
for cx, cy, rot, sc in [(574,491,-20,1),(623,484,22,1),(611,493,8,0.9),(585,510,-12,0.8),(603,505,4,0.9),(619,514,18,0.75)]:
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="{11*sc:.0f}" ry="{6*sc:.0f}" fill="#809660" transform="rotate({rot} {cx} {cy})"/>')
add('</g>')
# little pitcher with wildflowers right sill
add('<g filter="url(#smallshadow)">')
add('<path d="M 1006 594 C 1003 567 1009 554 1021 551 L 1048 551 C 1060 554 1066 567 1063 594 Z" fill="#d7e0d4" stroke="#99a999" stroke-width="2"/>')
add('<path d="M 1010 569 Q 1035 577 1060 569" stroke="#8fa28f" stroke-width="2" fill="none" opacity="0.55"/>')
add('<path d="M 1063 563 q 17 3 13 14 q -4 10 -16 8" fill="none" stroke="#99a999" stroke-width="5"/>')
add('<path d="M 1032 552 C 1027 526 1018 510 1006 500 M 1034 551 C 1036 522 1044 506 1055 493 M 1035 552 C 1041 530 1050 519 1062 514" stroke="#71855c" stroke-width="2" fill="none"/>')
for cx, cy, col in [(1004,498,'#f0c35b'),(1056,491,'#f5e4bd'),(1063,513,'#dd9761'),(1020,511,'#f0c35b')]:
    for a in range(0,360,60):
        add(f'<ellipse cx="{cx+6*math.cos(math.radians(a)):.1f}" cy="{cy+6*math.sin(math.radians(a)):.1f}" rx="4.5" ry="2.8" fill="{col}" transform="rotate({a} {cx+6*math.cos(math.radians(a)):.1f} {cy+6*math.sin(math.radians(a)):.1f})"/>')
    add(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#c78a3e"/>')
add('</g>')
add('</g>')

# ------------------------------------------------------------------ CHAIR & CAT
add('<g id="chaircat">')
# shadow
add('<ellipse cx="245" cy="1134" rx="172" ry="34" fill="#5a3a29" opacity="0.28" filter="url(#soft14)"/>')
# chair back
add('<path d="M 124 1044 C 110 970 108 892 118 804" stroke="#8d5936" stroke-width="18" fill="none" stroke-linecap="round"/>')
add('<path d="M 344 1044 C 356 966 357 885 348 801" stroke="#8d5936" stroke-width="18" fill="none" stroke-linecap="round"/>')
add('<path d="M 120 812 C 168 748 302 744 349 810" stroke="#8d5936" stroke-width="17" fill="none" stroke-linecap="round"/>')
add('<path d="M 126 810 C 170 758 298 754 342 807" stroke="#c08a5b" stroke-width="5" fill="none" opacity="0.55" stroke-linecap="round"/>')
# spindles
for x, bend in [(170,'-7'),(208,'-2'),(252,'3'),(298,'8')]:
    add(f'<path d="M {x} 786 C {x+int(bend)} 860 {x+int(bend)} 940 {x+int(bend)} 1008" stroke="#9a6440" stroke-width="8" fill="none" stroke-linecap="round"/>')
    add(f'<path d="M {x-1} 790 C {x+int(bend)-1} 860 {x+int(bend)-1} 930 {x+int(bend)-1} 1000" stroke="#c99264" stroke-width="2" fill="none" opacity="0.45"/>')
# seat
add('<path d="M 92 1004 Q 238 974 382 1004 L 374 1062 Q 238 1084 100 1062 Z" fill="#8f5a37" stroke="#6f422b" stroke-width="3"/>')
add('<path d="M 99 1008 Q 238 982 375 1008" stroke="#c58d5c" stroke-width="4" fill="none" opacity="0.55"/>')
# legs
add('<path d="M 120 1058 C 116 1098 112 1148 108 1200" stroke="#815030" stroke-width="15" fill="none"/>')
add('<path d="M 356 1058 C 362 1102 366 1152 370 1200" stroke="#815030" stroke-width="15" fill="none"/>')
# cushion
add('<path d="M 106 1000 Q 238 970 374 1000 L 368 1056 Q 238 1080 110 1056 Z" fill="url(#teal)" stroke="#334f49" stroke-width="3"/>')
add('<path d="M 114 1004 Q 238 978 366 1004" stroke="#8eaaa2" stroke-width="4" fill="none" opacity="0.55"/>')
add('<path d="M 118 1054 Q 238 1076 360 1054" stroke="#2e4742" stroke-width="3" fill="none" opacity="0.6"/>')
for x in [170, 238, 306]:
    add(f'<circle cx="{x}" cy="1022" r="3" fill="#2f4944" opacity="0.55"/>')
# cat shadow on cushion
add('<ellipse cx="244" cy="1047" rx="108" ry="25" fill="#243c38" opacity="0.38" filter="url(#soft8)"/>')
# curled body
add('<path d="M 141 1022 C 134 972 161 932 210 922 C 262 911 313 933 330 976 C 342 1009 330 1042 298 1055 C 263 1069 208 1064 176 1048 C 155 1037 143 1032 141 1022 Z" fill="url(#catfur)" stroke="#9e5531" stroke-width="2.5"/>')
# subtle body shading and fur texture
add('<path d="M 154 1020 C 176 1049 225 1060 273 1048" stroke="#a95b32" stroke-width="15" fill="none" opacity="0.18" filter="url(#soft8)"/>')
for d in ["M 166 978 q 17 6 25 21","M 184 950 q 17 9 23 25","M 207 933 q 14 12 16 30","M 234 923 q 10 16 10 34","M 264 922 q 7 15 6 30","M 293 930 q 4 15 0 29"]:
    add(f'<path d="{d}" stroke="#f0b27d" stroke-width="2.2" fill="none" opacity="0.34" stroke-linecap="round"/>')
# tabby bands
for d in ["M 171 965 C 189 983 195 1010 190 1038","M 198 943 C 216 963 222 994 217 1028","M 228 928 C 245 953 250 982 245 1016","M 260 921 C 276 946 279 973 275 1000"]:
    add(f'<path d="{d}" stroke="#b86438" stroke-width="9" fill="none" opacity="0.48" stroke-linecap="round"/>')
# tail curled around the front
add('<path d="M 315 1014 C 359 1018 374 1048 350 1064 C 328 1079 289 1073 278 1057 C 269 1044 284 1035 295 1042 C 303 1047 299 1055 293 1054" fill="none" stroke="#c47342" stroke-width="22" stroke-linecap="round"/>')
add('<path d="M 315 1014 C 359 1018 374 1048 350 1064 C 328 1079 289 1073 278 1057 C 269 1044 284 1035 295 1042 C 303 1047 299 1055 293 1054" fill="none" stroke="#e5a26a" stroke-width="5" stroke-linecap="round" opacity="0.55"/>')
add('<path d="M 301 1065 q 17 8 34 3" stroke="#8f4b2c" stroke-width="5" fill="none" opacity="0.3" stroke-linecap="round"/>')
# ears (behind head)
add('<path d="M 273 947 L 270 914 Q 271 904 280 910 L 301 929 Z" fill="#c47342" stroke="#9e5531" stroke-width="2.5" stroke-linejoin="round"/>')
add('<path d="M 320 929 L 338 910 Q 346 903 346 915 L 342 950 Z" fill="#c47342" stroke="#9e5531" stroke-width="2.5" stroke-linejoin="round"/>')
add('<path d="M 278 933 L 277 917 L 291 929 Z" fill="#e8a49a"/>')
add('<path d="M 331 928 L 339 915 L 339 933 Z" fill="#e8a49a"/>')
# head
add('<ellipse cx="307" cy="966" rx="46" ry="43" fill="url(#catfur)" stroke="#9e5531" stroke-width="2.5"/>')
# forehead tabby M
add('<path d="M 286 943 C 292 951 295 956 296 963 M 306 938 C 309 947 309 954 309 961 M 326 944 C 320 952 317 957 316 963" stroke="#b86438" stroke-width="4.2" fill="none" opacity="0.5" stroke-linecap="round"/>')
# cheeks, muzzle
add('<path d="M 271 971 q -7 3 -10 10 q 9 2 16 -2" fill="#f2d6b0" opacity="0.9"/>')
add('<path d="M 343 969 q 8 3 10 10 q -9 2 -16 -2" fill="#f2d6b0" opacity="0.9"/>')
add('<ellipse cx="299" cy="984" rx="19" ry="14" fill="#f4d9b7"/>')
add('<ellipse cx="316" cy="984" rx="19" ry="14" fill="#f4d9b7"/>')
add('<ellipse cx="307" cy="989" rx="24" ry="12" fill="#f4d9b7"/>')
# closed eyes
add('<path d="M 282 969 Q 291 975 300 968" stroke="#60402d" stroke-width="3" fill="none" stroke-linecap="round"/>')
add('<path d="M 315 968 Q 324 975 333 968" stroke="#60402d" stroke-width="3" fill="none" stroke-linecap="round"/>')
add('<path d="M 283 969 l -5 -3 M 332 969 l 5 -3" stroke="#60402d" stroke-width="1.8" opacity="0.7" stroke-linecap="round"/>')
# nose and mouth
add('<path d="M 303 983 Q 307 980 311 983 Q 307 988 303 983 Z" fill="#c67a6b"/>')
add('<path d="M 307 988 V 993 M 307 993 Q 300 997 296 992 M 307 993 Q 314 997 318 992" stroke="#6e4934" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
# whiskers
for y1, y2 in [(980,974),(985,984),(990,993)]:
    add(f'<path d="M 289 {y1} L 260 {y2}" stroke="#f8e4c4" stroke-width="1.4" opacity="0.8"/>')
    add(f'<path d="M 325 {y1} L 354 {y2}" stroke="#f8e4c4" stroke-width="1.4" opacity="0.8"/>')
# chest and tucked front paws
add('<path d="M 288 999 C 294 1013 320 1013 329 998 C 326 1024 298 1030 288 999 Z" fill="#f2d6b0" opacity="0.92"/>')
add('<ellipse cx="300" cy="1021" rx="25" ry="13" fill="#f5dcbc" stroke="#d5ab80" stroke-width="1.8" transform="rotate(8 300 1021)"/>')
add('<path d="M 285 1021 q 7 4 14 0 M 301 1024 q 7 3 14 -1" stroke="#d2a77b" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
add('<ellipse cx="332" cy="1017" rx="17" ry="11" fill="#f5dcbc" stroke="#d5ab80" stroke-width="1.8" transform="rotate(-14 332 1017)"/>')
add('<path d="M 326 1018 q 5 3 11 0" stroke="#d2a77b" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
# warm rim light from the window
add('<path d="M 274 935 C 296 919 325 923 340 945" stroke="#ffe1b0" stroke-width="4" fill="none" opacity="0.55" filter="url(#soft4)" stroke-linecap="round"/>')
add('<path d="M 295 1018 C 319 1029 342 1026 355 1011" stroke="#ffe1b0" stroke-width="3" fill="none" opacity="0.35" filter="url(#soft4)" stroke-linecap="round"/>')
add('</g>')

# ------------------------------------------------------------------ TABLE
add('<g id="table">')
# shadow on floor
add('<ellipse cx="855" cy="1130" rx="480" ry="80" fill="#4f3123" opacity="0.26" filter="url(#soft26)"/>')
# legs
add('<path d="M 548 1080 C 544 1120 540 1160 536 1200" stroke="#70412a" stroke-width="30" fill="none"/>')
add('<path d="M 1102 1080 C 1106 1120 1110 1160 1114 1200" stroke="#70412a" stroke-width="30" fill="none"/>')
add('<path d="M 536 1150 q 15 12 27 0" stroke="#9a6541" stroke-width="4" fill="none" opacity="0.5"/>')
# edge
add('<ellipse cx="820" cy="1016" rx="440" ry="155" fill="#7b452a"/>')
add('<ellipse cx="820" cy="1008" rx="434" ry="151" fill="#925a36"/>')
# top
add('<ellipse cx="820" cy="990" rx="440" ry="155" fill="url(#woodtable)"/>')
add('<ellipse cx="820" cy="990" rx="440" ry="155" fill="url(#tablelight)"/>')
# wood grain -- long, organic cathedral grain rather than a grid
add('<g clip-path="url(#tableclip)">')
for i in range(13):
    y = 862 + i * 21
    amp = random.uniform(9, 22)
    add(f'<path d="M 392 {y+random.uniform(-5,5):.0f} C 525 {y-amp:.0f} 690 {y+amp:.0f} 828 {y+random.uniform(-8,8):.0f} C 970 {y-amp:.0f} 1115 {y+amp*0.6:.0f} 1248 {y+random.uniform(-5,5):.0f}" stroke="#7f4a2e" stroke-width="{random.choice([1.0,1.2,1.6])}" opacity="{random.uniform(0.09,0.18):.2f}" fill="none"/>')
# broad, soft grain ribbons
for y, op in [(902,0.10),(948,0.12),(1022,0.10),(1078,0.09)]:
    add(f'<path d="M 430 {y} C 600 {y-34} 820 {y+22} 1000 {y-10} C 1100 {y-28} 1170 {y-8} 1220 {y+4}" stroke="#d6a06e" stroke-width="9" opacity="{op}" fill="none" filter="url(#soft4)"/>')
# one small knot
for rx, ry in [(13, 6),(8, 4)]:
    add(f'<ellipse cx="1030" cy="1050" rx="{rx}" ry="{ry}" fill="none" stroke="#7f4a2e" stroke-width="1.3" opacity="0.14"/>')
# soft sun patch on table
add('<ellipse cx="720" cy="938" rx="290" ry="95" fill="#ffdfaa" opacity="0.34" filter="url(#soft26)"/>')
add('<ellipse cx="650" cy="946" rx="170" ry="52" fill="#ffecc5" opacity="0.32" filter="url(#soft26)"/>')
add('<path d="M 420 888 C 590 850 930 850 1190 900" stroke="#f4c28d" stroke-width="5" fill="none" opacity="0.35" filter="url(#soft4)"/>')
# window mullion shadows falling across the tabletop
add('<g opacity="0.10" filter="url(#soft8)">')
add('<path d="M 620 872 L 664 872 L 760 1150 L 690 1150 Z" fill="#6f422b"/>')
add('<path d="M 826 866 L 866 866 L 938 1142 L 882 1142 Z" fill="#6f422b"/>')
add('</g>')
add('</g>')
# edge highlight
add('<path d="M 386 1000 C 448 1088 636 1144 820 1144 C 1004 1144 1192 1088 1254 1000" stroke="#e2a36e" stroke-width="4" fill="none" opacity="0.55"/>')
# placemat
add('<ellipse cx="842" cy="984" rx="200" ry="86" fill="url(#linen)" stroke="#d9c19e" stroke-width="2" opacity="0.98"/>')
add('<ellipse cx="842" cy="984" rx="186" ry="75" fill="none" stroke="#c9a97f" stroke-width="1.5" stroke-dasharray="7 6" opacity="0.65"/>')
# napkin lower center
add('<path d="M 742 1052 Q 810 1026 878 1052 L 860 1102 Q 806 1122 754 1098 Z" fill="#f1e2c9" stroke="#cfb491" stroke-width="2"/>')
add('<path d="M 752 1058 Q 812 1040 866 1058" stroke="#d3b993" stroke-width="3" fill="none" opacity="0.7"/>')
add('<path d="M 766 1080 Q 810 1068 854 1082" stroke="#b87858" stroke-width="2" fill="none" opacity="0.55"/>')
# spoon on napkin
add('<path d="M 786 1092 L 838 1066" stroke="#b6aa93" stroke-width="5" stroke-linecap="round"/>')
add('<ellipse cx="778" cy="1096" rx="11" ry="7" fill="#d9d0bd" stroke="#a99c84" stroke-width="1.5" transform="rotate(-24 778 1096)"/>')
add('</g>')

# ------------------------------------------------------------------ BREAKFAST
add('<g id="breakfast">')
# shadows
add('<ellipse cx="848" cy="1002" rx="172" ry="42" fill="#6e442b" opacity="0.28" filter="url(#soft8)"/>')
add('<ellipse cx="620" cy="955" rx="74" ry="20" fill="#6e442b" opacity="0.25" filter="url(#soft8)"/>')
add('<ellipse cx="1118" cy="960" rx="60" ry="17" fill="#6e442b" opacity="0.24" filter="url(#soft8)"/>')
# plate
add('<ellipse cx="850" cy="980" rx="157" ry="69" fill="#e7d9c0" stroke="#bfa987" stroke-width="3"/>')
add('<ellipse cx="850" cy="975" rx="145" ry="62" fill="#f8f1e2" stroke="#d3c0a1" stroke-width="2"/>')
add('<ellipse cx="850" cy="975" rx="132" ry="54" fill="#fbf6eb" stroke="#c9b18e" stroke-width="1.5"/>')
add('<ellipse cx="850" cy="975" rx="140" ry="58" fill="none" stroke="#8ba7ad" stroke-width="2" opacity="0.55"/>')
add('<path d="M 722 954 A 132 52 0 0 1 910 928" stroke="#fffdf5" stroke-width="4" fill="none" opacity="0.8"/>')
# toast
add('<g transform="translate(812 925) rotate(-8)">')
add('<rect x="-49" y="-8" width="98" height="69" rx="15" fill="#a76431"/>')
add('<rect x="-43" y="-12" width="86" height="65" rx="13" fill="#d99b54"/>')
add('<rect x="-38" y="-7" width="76" height="55" rx="10" fill="#e6b06b"/>')
add('<path d="M -28 5 Q -5 -5 20 4 M -33 18 Q 2 7 33 17 M -27 32 Q 0 23 25 31" stroke="#f2c98c" stroke-width="3" opacity="0.55" fill="none"/>')
# avocado smear
add('<path d="M -32 12 C -26 -2 4 -5 27 5 C 33 14 26 26 10 29 C -6 33 -28 27 -32 12 Z" fill="#8ca55f" stroke="#6f8650" stroke-width="2"/>')
add('<path d="M -18 14 C -6 7 8 8 18 13" stroke="#b7c98b" stroke-width="3" fill="none" opacity="0.7"/>')
# egg
add('<path d="M 0 10 C 16 -3 41 3 44 18 C 48 34 29 43 12 38 C -2 34 -8 22 0 10 Z" fill="#f8f0dc" stroke="#dfceb0" stroke-width="2"/>')
add('<circle cx="23" cy="20" r="13" fill="#efb33d" stroke="#d48d2d" stroke-width="2"/>')
add('<circle cx="18" cy="15" r="4" fill="#ffd87b" opacity="0.85"/>')
# chili flakes / herbs on egg
for x,y in [(12,12),(31,10),(35,26),(14,30)]:
    add(f'<circle cx="{x}" cy="{y}" r="1.8" fill="#b84d34" opacity="0.85"/>')
add('<path d="M 42 12 C 47 8 52 10 54 15" stroke="#6f8a51" stroke-width="2" fill="none" opacity="0.8"/>')
add('</g>')
# a second toast slice peeking
add('<g transform="translate(890 944) rotate(9)" opacity="0.98">')
add('<rect x="-40" y="-4" width="80" height="52" rx="12" fill="#a76431"/>')
add('<rect x="-35" y="-8" width="70" height="49" rx="10" fill="#dda05a"/>')
add('<rect x="-31" y="-4" width="62" height="41" rx="8" fill="#eab673"/>')
add('<path d="M -22 6 Q 2 -2 21 6 M -25 17 Q 4 8 24 17" stroke="#f8d39a" stroke-width="2.5" opacity="0.55" fill="none"/>')
add('</g>')
# a little salad and tomatoes on the plate
add('<g>')
for cx, cy, rot, col in [(906,966,28,'#708b4e'),(924,980,-18,'#7f9957'),(892,990,10,'#617c47'),(936,958,55,'#89a25f')]:
    add(f'<path d="M {cx} {cy} C {cx-12} {cy-10} {cx-20} {cy+2} {cx-25} {cy+12} C {cx-10} {cy+9} {cx+10} {cy+22} {cx+19} {cy+5} C {cx+10} {cy-2} {cx+3} {cy-4} {cx} {cy} Z" fill="{col}" stroke="#506b3e" stroke-width="1.2" transform="rotate({rot} {cx} {cy})"/>')
for cx, cy in [(776,987),(798,972)]:
    add(f'<circle cx="{cx}" cy="{cy}" r="14" fill="#c8523e" stroke="#9b3529" stroke-width="1.8"/>')
    add(f'<path d="M {cx-8} {cy-6} q 8 -4 14 1" stroke="#e17d64" stroke-width="2.5" fill="none" opacity="0.7"/>')
    add(f'<path d="M {cx-2} {cy-13} q 2 -5 6 -4" stroke="#69844d" stroke-width="2" fill="none"/>')
# flaky salt on the egg
for x,y in [(17,12),(28,24),(33,15),(20,28),(38,20)]:
    add(f'<circle cx="{x+802}" cy="{y+921}" r="1" fill="#fffdf3" opacity="0.8"/>')
add('</g>')
# fork
add('<g transform="translate(735 973) rotate(7)">')
add('<path d="M 0 0 V 62" stroke="#b8af9d" stroke-width="5" stroke-linecap="round"/>')
for dx in [-7,0,7]:
    add(f'<path d="M {dx} -17 V 3" stroke="#c8c0af" stroke-width="3" stroke-linecap="round"/>')
add('<path d="M -10 -17 q 10 -6 20 0" fill="none" stroke="#c8c0af" stroke-width="3"/>')
add('</g>')
# mug
add('<g>')
add('<ellipse cx="620" cy="846" rx="48" ry="15" fill="#e5d2b4" stroke="#b79a76" stroke-width="2"/>')
add('<path d="M 572 846 C 572 894 578 941 620 941 C 662 941 668 894 668 846 Z" fill="url(#ceramic)" stroke="#b79a76" stroke-width="2.5"/>')
add('<ellipse cx="620" cy="846" rx="38" ry="11" fill="#6b4029"/>')
add('<ellipse cx="620" cy="845" rx="28" ry="8" fill="#815238"/>')
add('<path d="M 604 843 q 10 -6 21 1 q 8 5 18 1" stroke="#d5a77b" stroke-width="3" fill="none" opacity="0.8"/>')
add('<path d="M 668 862 C 701 856 707 889 676 901 C 668 904 665 898 669 892 C 688 887 688 869 668 872" fill="url(#ceramic)" stroke="#b79a76" stroke-width="2.5"/>')
# painted sprig on mug
add('<g opacity="0.72" stroke="#778b68" fill="none">')
add('<path d="M 605 880 C 608 900 606 916 610 925" stroke-width="2"/>')
add('<path d="M 607 892 C 596 888 591 882 588 876 M 609 902 C 620 897 625 890 627 884" stroke-width="2"/>')
add('<ellipse cx="588" cy="875" rx="5" ry="2.6" fill="#778b68" stroke="none"/>')
add('<ellipse cx="627" cy="883" rx="5" ry="2.6" fill="#778b68" stroke="none"/>')
add('</g>')
add('<path d="M 578 856 C 580 892 584 918 598 931" stroke="#fffaf0" stroke-width="5" fill="none" opacity="0.5"/>')
add('</g>')
# steam
add('<g stroke="#fff8e8" fill="none" opacity="0.55" filter="url(#soft4)" stroke-linecap="round">')
add('<path d="M 602 832 C 578 801 615 785 596 754 C 579 726 612 713 601 684" stroke-width="7"/>')
add('<path d="M 632 828 C 657 799 624 779 645 752 C 661 730 636 714 648 690" stroke-width="5" opacity="0.7"/>')
add('<path d="M 614 822 C 604 800 620 789 612 770" stroke-width="3" opacity="0.5"/>')
add('</g>')
# jam jar
add('<g filter="url(#smallshadow)">')
add('<rect x="692" y="889" width="47" height="57" rx="7" fill="#b94432" stroke="#873124" stroke-width="2"/>')
add('<rect x="698" y="896" width="35" height="43" rx="5" fill="url(#jam)" opacity="0.9"/>')
add('<path d="M 700 904 Q 715 910 730 903" stroke="#e58160" stroke-width="3" fill="none" opacity="0.55"/>')
add('<rect x="688" y="878" width="55" height="16" rx="5" fill="#e6d2b3" stroke="#b1916c" stroke-width="2"/>')
add('<path d="M 694 885 q 7 -5 13 0 q 7 5 14 0 q 7 -5 14 0" stroke="#c27756" stroke-width="2" fill="none" opacity="0.7"/>')
add('<rect x="700" y="910" width="31" height="21" rx="2" fill="#f3e2c7" opacity="0.9"/>')
add('<path d="M 706 918 H 725 M 706 924 H 720" stroke="#a87955" stroke-width="1.5" opacity="0.65"/>')
add('<path d="M 737 879 C 755 868 764 881 752 892" stroke="#c9b28e" stroke-width="4" fill="none"/>')
add('</g>')
# butter crock
add('<g filter="url(#smallshadow)">')
add('<path d="M 936 1047 L 940 1008 Q 940 998 952 998 L 994 998 Q 1006 998 1006 1008 L 1010 1047 Z" fill="#e7dcc7" stroke="#b9a17e" stroke-width="2"/>')
add('<ellipse cx="974" cy="1002" rx="34" ry="9" fill="#f7efdf" stroke="#c6ad88" stroke-width="2"/>')
add('<path d="M 954 1000 q 20 9 40 0" stroke="#ead8ba" stroke-width="4" fill="none" opacity="0.7"/>')
add('<path d="M 962 1014 q 12 -9 23 0" fill="#f3d178" opacity="0.9"/>')
add('<path d="M 946 1022 H 1002" stroke="#c9b18e" stroke-width="2" opacity="0.6"/>')
add('</g>')
# oranges
add('<g>')
add('<circle cx="1046" cy="1019" r="29" fill="#dd8c3f" stroke="#b96a2d" stroke-width="2"/>')
add('<circle cx="1036" cy="1009" r="9" fill="#f1b264" opacity="0.55"/>')
add('<path d="M 1046 990 q 5 -10 14 -10" stroke="#6f8253" stroke-width="3" fill="none"/>')
add('<ellipse cx="1064" cy="979" rx="10" ry="4" fill="#7f9562" transform="rotate(-24 1064 979)"/>')
add('<circle cx="1081" cy="1041" r="24" fill="#d57c37" stroke="#b46128" stroke-width="2"/>')
add('<circle cx="1073" cy="1033" r="7" fill="#efaa63" opacity="0.5"/>')
add('</g>')
# glass of morning juice
add('<g filter="url(#smallshadow)">')
add('<ellipse cx="1048" cy="938" rx="32" ry="9" fill="#6e442b" opacity="0.18" filter="url(#soft4)"/>')
add('<path d="M 1028 857 L 1068 857 L 1063 927 Q 1062 937 1048 937 Q 1034 937 1033 927 Z" fill="#f5c66a" opacity="0.88" stroke="#c79554" stroke-width="2"/>')
add('<path d="M 1031 870 L 1034 923 Q 1036 931 1048 931 Q 1060 931 1061 923 L 1064 870 Z" fill="#edb34c" opacity="0.75"/>')
add('<path d="M 1030 870 Q 1048 878 1066 870" stroke="#ffe0a1" stroke-width="3" fill="none" opacity="0.8"/>')
add('<path d="M 1035 879 L 1038 918" stroke="#fff2c7" stroke-width="4" fill="none" opacity="0.6"/>')
add('<path d="M 1028 857 L 1068 857" stroke="#d8aa6c" stroke-width="2.5"/>')
# orange slice on the rim
add('<path d="M 1026 857 A 14 14 0 0 1 1054 857 Z" fill="#f08a3e" stroke="#c9632c" stroke-width="1.5"/>')
add('<path d="M 1032 857 L 1040 848 M 1038 857 L 1046 846 M 1044 857 L 1050 850" stroke="#ffd08d" stroke-width="1.5" opacity="0.8"/>')
add('</g>')
# bowl of berries in the foreground
add('<g filter="url(#smallshadow)">')
add('<ellipse cx="498" cy="1058" rx="67" ry="20" fill="#6e442b" opacity="0.22" filter="url(#soft8)"/>')
add('<path d="M 438 1024 Q 498 1048 558 1024 Q 548 1063 498 1066 Q 448 1063 438 1024 Z" fill="#e7dcc5" stroke="#b49a75" stroke-width="2.5"/>')
add('<ellipse cx="498" cy="1024" rx="60" ry="16" fill="#f4ead8" stroke="#b49a75" stroke-width="2"/>')
add('<ellipse cx="498" cy="1024" rx="49" ry="11" fill="#783f3d"/>')
for cx, cy, r, col in [(474,1018,10,'#b33e45'),(492,1013,9,'#8d3b55'),(508,1020,10,'#c44b4b'),(522,1012,8,'#6f3c5f'),(482,1027,8,'#a5363d'),(506,1008,7,'#d05a5a')]:
    add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" stroke="#6f3036" stroke-width="1"/>')
    add(f'<circle cx="{cx-3}" cy="{cy-3}" r="{r*0.28:.1f}" fill="#e88a83" opacity="0.6"/>')
for cx, cy, rot in [(490,1005,25),(514,1002,-20),(530,1020,45)]:
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="9" ry="4" fill="#6f8a51" transform="rotate({rot} {cx} {cy})"/>')
add('<path d="M 454 1032 Q 498 1044 542 1032" stroke="#cbb08b" stroke-width="2" fill="none" opacity="0.6"/>')
add('</g>')
# fallen petals on the table
add('<g opacity="0.85">')
add('<ellipse cx="1080" cy="980" rx="8" ry="4" fill="#f2cf7b" transform="rotate(-22 1080 980)"/>')
add('<ellipse cx="1102" cy="1002" rx="7" ry="3.5" fill="#f7e6c0" transform="rotate(18 1102 1002)"/>')
add('<ellipse cx="1058" cy="1000" rx="6" ry="3" fill="#e7a35d" transform="rotate(42 1058 1000)"/>')
add('</g>')
# vase and flowers
add('<g>')
add('<ellipse cx="1120" cy="944" rx="53" ry="14" fill="#6e442b" opacity="0.22" filter="url(#soft8)"/>')
add('<path d="M 1092 942 C 1084 900 1093 864 1110 854 L 1134 854 C 1151 864 1160 900 1152 942 Z" fill="#e8dcc4" stroke="#b59d79" stroke-width="2.5"/>')
add('<path d="M 1094 880 Q 1122 890 1152 880 M 1088 908 Q 1122 918 1156 908" stroke="#cbb28b" stroke-width="2" fill="none" opacity="0.7"/>')
add('<path d="M 1094 932 Q 1122 940 1150 932" stroke="#93a487" stroke-width="5" fill="none" opacity="0.55"/>')
add('<path d="M 1096 871 C 1099 880 1103 885 1108 891" stroke="#fff8e8" stroke-width="4" fill="none" opacity="0.55"/>')
# stems
for d in ["M 1122 858 C 1114 806 1098 770 1082 744","M 1122 856 C 1128 800 1140 764 1158 734","M 1121 858 C 1122 806 1120 774 1116 736","M 1122 860 C 1104 820 1088 792 1072 774","M 1122 860 C 1142 820 1160 796 1176 780"]:
    add(f'<path d="{d}" stroke="#6d8355" stroke-width="2.6" fill="none"/>')
# leaves
for cx, cy, rot in [(1094,804,-25),(1148,792,25),(1110,790,-10),(1078,790,-35),(1168,810,30),(1128,810,15)]:
    add(f'<ellipse cx="{cx}" cy="{cy}" rx="14" ry="6" fill="#7e9560" transform="rotate({rot} {cx} {cy})"/>')
# flowers
def daisy(cx, cy, r, petal, center, n=8):
    for a in range(0,360,360//n):
        px = cx + r*math.cos(math.radians(a)); py = cy + r*math.sin(math.radians(a))
        add(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{r*0.62:.1f}" ry="{r*0.34:.1f}" fill="{petal}" transform="rotate({a} {px:.1f} {py:.1f})"/>')
    add(f'<circle cx="{cx}" cy="{cy}" r="{r*0.42:.1f}" fill="{center}"/>')
daisy(1078, 734, 15, "#f6d77d", "#d59b3e", 9)
daisy(1116, 720, 18, "#f8eccb", "#d6a24b", 9)
daisy(1160, 728, 14, "#e7a35d", "#b96b32", 8)
daisy(1098, 756, 11, "#f4c467", "#c28a35", 8)
daisy(1144, 762, 10, "#f7e0b4", "#cb9444", 8)
# small lavender sprigs
for x in [1068, 1128, 1176]:
    for i in range(4):
        add(f'<ellipse cx="{x + (i%2)*4}" cy="{770-i*9}" rx="4" ry="7" fill="#9a8ba5" opacity="0.8"/>')
add('</g>')
add('</g>')

# ------------------------------------------------------------------ LIGHT
add('<g id="light">')
# broad volumetric sunbeams from the window
add('<path d="M 560 110 L 700 100 L 318 1200 L 74 1200 Z" fill="url(#beam)" opacity="0.24" filter="url(#soft26)"/>')
add('<path d="M 742 98 L 882 96 L 786 1200 L 592 1200 Z" fill="url(#beam)" opacity="0.28" filter="url(#soft26)"/>')
add('<path d="M 930 120 L 1044 150 L 1278 1200 L 1082 1200 Z" fill="url(#beam)" opacity="0.22" filter="url(#soft45)"/>')
add('<path d="M 552 430 L 1048 424 L 1214 1200 L 872 1200 Z" fill="url(#beam)" opacity="0.14" filter="url(#soft45)"/>')
# a brighter core shaft
add('<path d="M 638 104 L 704 102 L 438 1200 L 330 1200 Z" fill="#fff0c5" opacity="0.10" filter="url(#soft26)"/>')
# glow at the window edge
add('<path d="M 1030 120 C 1090 280 1080 470 1048 610" stroke="#ffe4a8" stroke-width="42" fill="none" opacity="0.20" filter="url(#soft26)"/>')
add('<path d="M 552 120 C 510 280 512 470 534 610" stroke="#ffe4a8" stroke-width="30" fill="none" opacity="0.14" filter="url(#soft26)"/>')
# sunlit kiss on the chair and wall
add('<ellipse cx="270" cy="930" rx="210" ry="190" fill="#ffd89a" opacity="0.12" filter="url(#soft45)"/>')
add('<ellipse cx="800" cy="905" rx="330" ry="120" fill="#ffe2a7" opacity="0.10" filter="url(#soft45)"/>')
# dust motes, concentrated in the beams
random.seed(77)
for i in range(64):
    x = random.uniform(430, 1260); y = random.uniform(150, 1100)
    r = random.uniform(1.0, 4.6)
    op = random.uniform(0.12, 0.62)
    add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff3cd" opacity="{op:.2f}" filter="url(#soft4)"/>')
# a few lazy dust threads catching the light
add('<path d="M 690 620 C 650 700 660 780 620 850" stroke="#ffeec6" stroke-width="3" fill="none" opacity="0.12" filter="url(#soft4)"/>')
add('<path d="M 960 520 C 920 620 940 700 900 790" stroke="#ffeec6" stroke-width="4" fill="none" opacity="0.10" filter="url(#soft4)"/>')
# bright rims on table items from the window
add('<path d="M 577 850 C 585 890 592 923 614 934" stroke="#fff4da" stroke-width="4" fill="none" opacity="0.72"/>')
add('<path d="M 1082 865 C 1072 900 1072 928 1082 940" stroke="#fff4da" stroke-width="4" fill="none" opacity="0.50"/>')
add('<ellipse cx="980" cy="958" rx="230" ry="45" fill="#ffe2a7" opacity="0.20" filter="url(#soft26)"/>')
add('</g>')

# warm vignette edge
add('<rect width="1600" height="1200" fill="none" stroke="#6d4932" stroke-width="44" opacity="0.12"/>')
add('</svg>')

out = Path(__file__).parent / "cozy_kitchen.svg"
out.write_text("\n".join(s), encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size/1024:.1f} KB)")
