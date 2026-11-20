#!/usr/bin/env python3
"""Generate pelican.svg — a pelican actively riding a bicycle (SMIL animation).

Wheels spin, cranks rotate, pedals stay level (counter-rotated), and the
pelican's legs are solved with two-bone IK sampled at 16 keyframes so the
feet track the pedals exactly.
"""
import math

OUT = "pelican.svg"

# ---- geometry constants -------------------------------------------------
BBX, BBY = 385.0, 360.0            # bottom bracket (crank center)
CRANK_R = 40.0
NEAR_PEDAL = (BBX + CRANK_R, BBY)  # crank arm drawn at angle 0 (to the right)
FAR_PEDAL = (BBX - CRANK_R, BBY)   # opposite arm
HIP_N = (344.0, 236.0)             # near-side hip
HIP_F = (331.0, 238.0)             # far-side hip
THIGH, SHANK = 88.0, 90.0

T_CRANK = "2.4s"   # one crank revolution
T_WHEEL = "1.07s"  # wheel revolution (gear ratio ~2.25)
T_CHAIN = "0.8s"   # chain dash cycle
T_BOB = "1.2s"     # body bob / head nod (2x per crank rev)


def knee(hip, pedal):
    """Two-bone IK; pick the knee-forward solution."""
    dx, dy = pedal[0] - hip[0], pedal[1] - hip[1]
    d = math.hypot(dx, dy)
    a = (THIGH * THIGH - SHANK * SHANK + d * d) / (2 * d)
    h = math.sqrt(max(THIGH * THIGH - a * a, 0.0))
    ux, uy = dx / d, dy / d
    cands = [(hip[0] + a * ux + h * uy, hip[1] + a * uy - h * ux),
             (hip[0] + a * ux - h * uy, hip[1] + a * uy + h * ux)]
    return max(cands, key=lambda k: k[0])


def leg_values(hip, phase=0.0):
    """16 IK keyframes (+ repeat of first) as an SMIL `values` string.

    The pedal orbits the bottom bracket; `phase` offsets the far leg by pi.
    """
    ds, dmax = 1e9, 0.0
    parts = []
    for k in range(17):
        th = phase + 2 * math.pi * k / 16
        p = (BBX + CRANK_R * math.cos(th), BBY + CRANK_R * math.sin(th))
        d = math.hypot(p[0] - hip[0], p[1] - hip[1])
        ds, dmax = min(ds, d), max(dmax, d)
        kx, ky = knee(hip, p)
        parts.append(f"M {hip[0]:.1f} {hip[1]:.1f} L {kx:.1f} {ky:.1f} "
                     f"L {p[0]:.1f} {p[1]:.1f}")
    return "; ".join(parts), ds, dmax


near_vals, ndmin, ndmax = leg_values(HIP_N, 0.0)
far_vals, fdmin, fdmax = leg_values(HIP_F, math.pi)
for name, dmin, dmax in (("near", ndmin, ndmax), ("far", fdmin, fdmax)):
    print(f"{name} leg reach: {dmin:.1f}..{dmax:.1f} "
          f"(max possible {THIGH + SHANK:.0f})")
    assert dmax < THIGH + SHANK - 1, f"{name} leg over-extended!"

# chainring bolt holes, 5 at r=23 around the BB
holes = []
for i in range(5):
    a = math.pi * 2 * i / 5
    holes.append(f'<circle cx="{BBX + 23 * math.cos(a):.1f}" '
                 f'cy="{BBY + 23 * math.sin(a):.1f}" r="2.6" fill="#3c4046"/>')
holes = "\n    ".join(holes)

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="820" height="520" viewBox="0 0 820 520">
  <title>A pelican riding a bicycle</title>
  <desc>Animated scene: spinning wheels, rotating cranks with level pedals,
  and a pedaling pelican on the saddle. Pure SMIL, no JavaScript.</desc>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#a8d8ff"/>
      <stop offset="1" stop-color="#eaf7ff"/>
    </linearGradient>
  </defs>

  <!-- ======= background ======= -->
  <rect width="820" height="520" fill="url(#sky)"/>
  <circle cx="730" cy="76" r="56" fill="#ffd95e" opacity="0.25"/>
  <circle cx="730" cy="76" r="40" fill="#ffd95e"/>
  <g fill="#ffffff" opacity="0.9">
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="900 60; -280 60" dur="36s" begin="-14s" repeatCount="indefinite"/>
      <ellipse cx="0" cy="0" rx="48" ry="16"/>
      <ellipse cx="-32" cy="6" rx="30" ry="12"/>
      <ellipse cx="34" cy="7" rx="28" ry="11"/>
    </g>
    <g opacity="0.8">
      <animateTransform attributeName="transform" type="translate"
        values="950 128; -260 128" dur="52s" begin="-33s" repeatCount="indefinite"/>
      <ellipse cx="0" cy="0" rx="40" ry="13"/>
      <ellipse cx="28" cy="6" rx="24" ry="10"/>
      <ellipse cx="-26" cy="6" rx="22" ry="9"/>
    </g>
  </g>
  <path d="M -20 449 Q 190 398 430 449 Z" fill="#9ed07f"/>
  <path d="M 360 449 Q 620 392 840 449 Z" fill="#8fc771"/>
  <rect x="0" y="449" width="820" height="71" fill="#5c6169"/>
  <line x1="0" y1="450" x2="820" y2="450" stroke="#464b52" stroke-width="3"/>
  <g opacity="0.5">
    <animateTransform attributeName="transform" type="translate"
      values="0 0; -80 0" dur="0.35s" repeatCount="indefinite"/>
    <line x1="0" y1="488" x2="900" y2="488" stroke="#c9ced6" stroke-width="6"
      stroke-dasharray="42 38"/>
  </g>
  <g stroke="#5ea34a" stroke-width="3" stroke-linecap="round" fill="none">
    <path d="M 96 448 C 94 441 95 435 99 430 M 103 448 C 104 442 107 438 111 435"/>
    <path d="M 700 448 C 698 441 699 435 703 430 M 707 448 C 708 442 711 438 715 435"/>
    <path d="M 66 448 C 65 444 66 441 68 438"/>
  </g>

  <!-- speed streaks -->
  <g stroke-linecap="round" opacity="0.3">
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="0 0; -90 0" dur="0.8s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.7;0" dur="0.8s" repeatCount="indefinite"/>
      <line x1="52" y1="300" x2="140" y2="300" stroke="#dfeefb" stroke-width="6"/>
    </g>
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="0 0; -90 0" dur="0.8s" begin="-0.27s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.7;0" dur="0.8s" begin="-0.27s" repeatCount="indefinite"/>
      <line x1="30" y1="338" x2="126" y2="338" stroke="#dfeefb" stroke-width="6"/>
    </g>
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="0 0; -90 0" dur="0.8s" begin="-0.53s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.7;0" dur="0.8s" begin="-0.53s" repeatCount="indefinite"/>
      <line x1="70" y1="262" x2="152" y2="262" stroke="#dfeefb" stroke-width="6"/>
    </g>
  </g>
  <ellipse cx="400" cy="453" rx="245" ry="8" fill="#14171a" opacity="0.16"/>

  <!-- ======= far-side leg + crank (behind the frame) ======= -->
  <path fill="none" stroke="#b97a1e" stroke-width="10" stroke-linecap="round"
        stroke-linejoin="round" d="M 331.0 238.0 L 374.4 299.1 L 345.0 360.0">
    <animate attributeName="d" dur="{T_CRANK}" repeatCount="indefinite"
      values="{far_vals}"/>
  </path>
  <g>
    <animateTransform attributeName="transform" type="rotate"
      from="0 {BBX:g} {BBY:g}" to="360 {BBX:g} {BBY:g}" dur="{T_CRANK}" repeatCount="indefinite"/>
    <line x1="{BBX:g}" y1="{BBY:g}" x2="{FAR_PEDAL[0]:g}" y2="{BBY:g}"
      stroke="#23262a" stroke-width="8" stroke-linecap="round"/>
    <g>
      <animateTransform attributeName="transform" type="rotate"
        from="360 {FAR_PEDAL[0]:g} {BBY:g}" to="0 {FAR_PEDAL[0]:g} {BBY:g}"
        dur="{T_CRANK}" repeatCount="indefinite"/>
      <rect x="{FAR_PEDAL[0] - 9:g}" y="356" width="18" height="8" rx="2.5" fill="#1d2024"/>
      <path d="M 339 356 L 357 356 L 365 350 L 362 359 L 356 362 L 339 362 Z"
        fill="#b97a1e" stroke="#8a5a12" stroke-width="1.5"/>
    </g>
  </g>

  <!-- ======= wheels ======= -->
  <g>
    <circle cx="235" cy="360" r="84" fill="none" stroke="#2b2b2b" stroke-width="10"/>
    <circle cx="235" cy="360" r="74" fill="none" stroke="#99a1a9" stroke-width="5"/>
    <g>
      <animateTransform attributeName="transform" type="rotate"
        from="0 235 360" to="360 235 360" dur="{T_WHEEL}" repeatCount="indefinite"/>
      <path d="M 235 289 L 235 431 M 164 360 L 306 360
               M 185 310 L 285 410 M 185 410 L 285 310"
        stroke="#c2c8ce" stroke-width="2.5" fill="none"/>
      <circle cx="235" cy="291" r="3.5" fill="#f2a33c"/>
    </g>
    <circle cx="235" cy="360" r="13" fill="none" stroke="#3c4046" stroke-width="5"/>
    <circle cx="235" cy="360" r="7" fill="#4a4f57"/>
    <circle cx="235" cy="360" r="3" fill="#2b2b2b"/>
  </g>
  <g>
    <circle cx="565" cy="360" r="84" fill="none" stroke="#2b2b2b" stroke-width="10"/>
    <circle cx="565" cy="360" r="74" fill="none" stroke="#99a1a9" stroke-width="5"/>
    <g>
      <animateTransform attributeName="transform" type="rotate"
        from="0 565 360" to="360 565 360" dur="{T_WHEEL}" repeatCount="indefinite"/>
      <path d="M 565 289 L 565 431 M 494 360 L 636 360
               M 515 310 L 615 410 M 515 410 L 615 310"
        stroke="#c2c8ce" stroke-width="2.5" fill="none"/>
      <circle cx="565" cy="291" r="3.5" fill="#f2a33c"/>
    </g>
    <circle cx="565" cy="360" r="7" fill="#4a4f57"/>
    <circle cx="565" cy="360" r="3" fill="#2b2b2b"/>
  </g>

  <!-- ======= frame ======= -->
  <g fill="none" stroke="#d64545" stroke-linecap="round">
    <line x1="235" y1="360" x2="385" y2="360" stroke-width="7"/>
    <line x1="235" y1="360" x2="343" y2="262" stroke-width="6"/>
    <line x1="385" y1="360" x2="340" y2="254" stroke-width="7"/>
    <line x1="385" y1="360" x2="538" y2="300" stroke-width="7"/>
    <line x1="342" y1="262" x2="529" y2="272" stroke-width="7"/>
    <line x1="527" y1="268" x2="546" y2="326" stroke-width="9"/>
    <line x1="546" y1="326" x2="565" y2="357" stroke-width="6"/>
  </g>
  <line x1="341" y1="250" x2="347" y2="268" stroke="#6b7076" stroke-width="6"/>
  <path d="M 304 246 C 310 237 332 235 348 240 C 356 243 358 247 352 249
           L 336 254 C 320 257 306 252 304 246 Z" fill="#4a3a2c"/>
  <line x1="527" y1="268" x2="509" y2="242" stroke="#6b7076" stroke-width="6"
    stroke-linecap="round"/>
  <path d="M 509 242 C 503 235 495 236 492 244" fill="none" stroke="#3a3d42"
    stroke-width="6" stroke-linecap="round"/>
  <circle cx="492" cy="244" r="4.5" fill="#1d2024"/>

  <!-- chainring (rotates with the cranks) -->
  <g>
    <animateTransform attributeName="transform" type="rotate"
      from="0 {BBX:g} {BBY:g}" to="360 {BBX:g} {BBY:g}" dur="{T_CRANK}" repeatCount="indefinite"/>
    <circle cx="{BBX:g}" cy="{BBY:g}" r="27" fill="none" stroke="#3c4046" stroke-width="5"/>
    <circle cx="{BBX:g}" cy="{BBY:g}" r="19" fill="none" stroke="#3c4046" stroke-width="2" opacity="0.55"/>
    {holes}
  </g>

  <!-- chain -->
  <g stroke="#3c4046" stroke-width="3.5" stroke-dasharray="6 3" fill="none" opacity="0.95">
    <line x1="235" y1="348" x2="385" y2="333">
      <animate attributeName="stroke-dashoffset" values="0;-54" dur="{T_CHAIN}" repeatCount="indefinite"/>
    </line>
    <line x1="385" y1="387" x2="235" y2="372">
      <animate attributeName="stroke-dashoffset" values="0;-54" dur="{T_CHAIN}" repeatCount="indefinite"/>
    </line>
  </g>

  <!-- near-side crank arm + level pedal -->
  <g>
    <animateTransform attributeName="transform" type="rotate"
      from="0 {BBX:g} {BBY:g}" to="360 {BBX:g} {BBY:g}" dur="{T_CRANK}" repeatCount="indefinite"/>
    <line x1="{BBX:g}" y1="{BBY:g}" x2="{NEAR_PEDAL[0]:g}" y2="{BBY:g}"
      stroke="#2f3338" stroke-width="9" stroke-linecap="round"/>
    <g>
      <animateTransform attributeName="transform" type="rotate"
        from="360 {NEAR_PEDAL[0]:g} {BBY:g}" to="0 {NEAR_PEDAL[0]:g} {BBY:g}"
        dur="{T_CRANK}" repeatCount="indefinite"/>
      <rect x="{NEAR_PEDAL[0] - 9:g}" y="356" width="18" height="8" rx="2.5" fill="#1d2024"/>
      <circle cx="{NEAR_PEDAL[0]:g}" cy="{BBY:g}" r="2.5" fill="#555a60"/>
    </g>
  </g>

  <!-- ======= the pelican ======= -->
  <g>
    <animateTransform attributeName="transform" type="translate"
      values="0 0; 0 -2.4; 0 0" dur="{T_BOB}" repeatCount="indefinite"/>
    <!-- tail feathers -->
    <g>
      <animateTransform attributeName="transform" type="rotate"
        values="0 280 182; 4 280 182; 0 280 182; -3 280 182; 0 280 182"
        dur="{T_BOB}" repeatCount="indefinite"/>
      <path d="M 272 180 C 250 170 238 152 244 134 C 254 148 264 160 278 170 Z"
        fill="#f4f1ea" stroke="#d8d2c4" stroke-width="2"/>
      <path d="M 268 190 C 244 188 228 172 226 152 C 240 164 256 176 272 184 Z"
        fill="#f4f1ea" stroke="#d8d2c4" stroke-width="2"/>
    </g>
    <!-- body, sitting on the saddle -->
    <ellipse cx="310" cy="188" rx="58" ry="45" transform="rotate(-18 310 188)"
      fill="#fdfcf8" stroke="#d9d3c8" stroke-width="2"/>
    <ellipse cx="300" cy="202" rx="42" ry="26" transform="rotate(-18 300 202)"
      fill="#f0ece2" opacity="0.85"/>
    <!-- neck + head -->
    <g>
      <animateTransform attributeName="transform" type="rotate"
        values="0 350 150; 2.2 350 150; 0 350 150; -1.4 350 150; 0 350 150"
        dur="{T_BOB}" repeatCount="indefinite"/>
      <path d="M 320 156 C 336 108 356 82 398 80 L 414 98 C 384 96 358 114 346 160 Z"
        fill="#fdfcf8" stroke="#d9d3c8" stroke-width="2"/>
      <circle cx="410" cy="90" r="16" fill="#fdfcf8" stroke="#d9d3c8" stroke-width="2"/>
      <path d="M 424 95 C 452 97 480 104 510 114 C 500 134 470 142 446 130
               C 432 122 426 108 424 95 Z" fill="#ef8c2a" stroke="#a35a12" stroke-width="1.5">
        <animate attributeName="d" dur="{T_BOB}" repeatCount="indefinite"
          values="M 424 95 C 452 97 480 104 510 114 C 500 134 470 142 446 130 C 432 122 426 108 424 95 Z;
                  M 424 95 C 452 97 480 104 510 114 C 504 142 466 154 440 138 C 429 127 426 108 424 95 Z;
                  M 424 95 C 452 97 480 104 510 114 C 500 134 470 142 446 130 C 432 122 426 108 424 95 Z"/>
      </path>
      <path d="M 424 82 C 458 86 490 96 514 108 L 510 114 C 482 103 452 96 424 95 Z"
        fill="#f7ab3f" stroke="#a35a12" stroke-width="1.5"/>
      <path d="M 394 82 A 17 17 0 0 1 428 82 L 431 84 L 392 84 Z" fill="#d64545"/>
      <path d="M 400 68 C 405 65 413 65 419 68 L 417 73 C 412 71 407 71 402 73 Z"
        fill="#ffffff" opacity="0.85"/>
      <path d="M 403 70 L 401 78 M 412 69 L 412 78" stroke="#b03434" stroke-width="2" fill="none"/>
      <path d="M 398 84 C 399 94 403 101 408 104" stroke="#b03434" stroke-width="2" fill="none"/>
      <circle cx="407" cy="90" r="4.5" fill="#ffffff" stroke="#c9c2b6" stroke-width="1"/>
      <circle cx="408.5" cy="90.5" r="2.3" fill="#1d2024"/>
      <circle cx="407.6" cy="89.6" r="0.8" fill="#ffffff"/>
      <path d="M 399 83 L 415 85" stroke="#555a60" stroke-width="2.5" stroke-linecap="round"/>
    </g>
    <!-- wing reaching to the handlebar -->
    <path d="M 326 154 C 380 160 436 196 492 232 L 498 246
             C 442 214 384 194 318 186 C 314 176 318 162 326 154 Z"
      fill="#eef2f7" stroke="#c6cfda" stroke-width="2"/>
    <path d="M 342 168 C 392 180 434 200 468 220 M 334 178 C 384 190 424 206 456 226"
      fill="none" stroke="#ccd6e0" stroke-width="2"/>
  </g>

  <!-- ======= near-side leg (over everything, on the pedal) ======= -->
  <g>
    <path fill="none" stroke="#f2a33c" stroke-width="11" stroke-linecap="round"
          stroke-linejoin="round" d="M 344.0 236.0 L 425.2 270.0 L 425.0 360.0">
      <animate attributeName="d" dur="{T_CRANK}" repeatCount="indefinite"
        values="{near_vals}"/>
    </path>
    <g>
      <animateTransform attributeName="transform" type="rotate"
        from="360 {NEAR_PEDAL[0]:g} {BBY:g}" to="0 {NEAR_PEDAL[0]:g} {BBY:g}"
        dur="{T_CRANK}" repeatCount="indefinite"/>
      <path d="M 419 356 L 437 356 L 445 350 L 442 359 L 436 362 L 419 362 Z"
        fill="#f2a33c" stroke="#b97a1e" stroke-width="1.5"/>
    </g>
  </g>
</svg>
'''

with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg)} bytes)")
