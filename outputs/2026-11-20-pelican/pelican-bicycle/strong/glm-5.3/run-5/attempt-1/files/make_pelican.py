#!/usr/bin/env python3
"""Generate pelican.svg: a pelican riding a bicycle (SMIL animation).

The legs are two-segment (thigh + shin) chains solved with inverse kinematics
so the feet follow the pedals around the crank circle. Keyframes are sampled
every 22.5 degrees of crank rotation and fed to <animate attributeName="d">.
"""
import math

W, H = 800, 520

# --- bicycle geometry -------------------------------------------------------
REAR = (235.0, 382.0)     # rear wheel center
FRONT = (565.0, 382.0)    # front wheel center
WHEEL_R = 78.0
BB = (390.0, 382.0)       # bottom bracket (crank center)
CRANK_R = 48.0
SEAT_TUBE_TOP = (352.0, 264.0)
HEAD_TOP = (548.0, 250.0)
HEAD_BOT = (558.0, 286.0)
GRIP = (505.0, 259.0)
CRANK_DUR = 1.6           # seconds per crank revolution
WHEEL_DUR = 1.4           # seconds per wheel revolution

# --- pelican legs -----------------------------------------------------------
HIP_NEAR = (354.0, 268.0)
HIP_FAR = (346.0, 272.0)
L1, L2 = 88.0, 84.0       # thigh, shin


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def ik(hip, foot, l1, l2):
    """Knee position for hip->foot chain, bending forward (+x)."""
    dx, dy = foot[0] - hip[0], foot[1] - hip[1]
    d = clamp(math.hypot(dx, dy), abs(l1 - l2) + 0.5, l1 + l2 - 0.5)
    base = math.atan2(dy, dx)
    cos_a = clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1.0, 1.0)
    a = math.acos(cos_a)
    k1 = (hip[0] + l1 * math.cos(base + a), hip[1] + l1 * math.sin(base + a))
    k2 = (hip[0] + l1 * math.cos(base - a), hip[1] + l1 * math.sin(base - a))
    return k1 if k1[0] > k2[0] else k2


def leg_paths(hip, phase_deg):
    """17 keyframes (every 22.5 deg) of the leg path for one crank cycle."""
    paths = []
    for i in range(17):
        th = math.radians((i * 22.5 + phase_deg) % 360.0)
        ankle = (BB[0] + CRANK_R * math.cos(th),
                 BB[1] + CRANK_R * math.sin(th) - 6.0)   # top of pedal
        knee = ik(hip, ankle, L1, L2)
        web = (ankle[0] + 8.0, ankle[1] + 9.0)
        toe = (ankle[0] + 30.0, ankle[1] + 1.0)
        pts = [hip, knee, ankle, web, toe]
        paths.append("M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts))
    return paths


def leg_anim(paths):
    keytimes = ";".join(f"{i / 16:.4f}" for i in range(17))
    values = ";\n           ".join(paths)
    return (f'dur="{CRANK_DUR}s" repeatCount="indefinite" calcMode="linear" '
            f'keyTimes="{keytimes}" values="{values}"')


near = leg_paths(HIP_NEAR, 0.0)
far = leg_paths(HIP_FAR, 180.0)

# --- spokes -----------------------------------------------------------------
def spokes():
    lines = []
    for k in range(8):
        a = math.radians(k * 45)
        x1, y1 = 10 * math.cos(a), 10 * math.sin(a)
        x2, y2 = 62 * math.cos(a), 62 * math.sin(a)
        lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    return "\n      ".join(lines)


def wheel(cx, cy):
    return f'''<g transform="translate({cx},{cy})">
      <circle r="{WHEEL_R}" fill="none" stroke="#2f2f33" stroke-width="11"/>
      <circle r="68" fill="none" stroke="#c8cdd2" stroke-width="5"/>
      <g>
        <animateTransform attributeName="transform" type="rotate"
          values="0;360" dur="{WHEEL_DUR}s" repeatCount="indefinite"/>
        {spokes()}
        <circle cx="0" cy="-62" r="4" fill="#d64550"/>
      </g>
      <circle r="9" fill="#555b63"/>
    </g>'''


def crank(phase_from, phase_to):
    return f'''<g transform="translate({BB[0]},{BB[1]})">
      <g>
        <animateTransform attributeName="transform" type="rotate"
          values="{phase_from};{phase_to}" dur="{CRANK_DUR}s" repeatCount="indefinite"/>
        <line x1="0" y1="0" x2="{CRANK_R}" y2="0" stroke="#41474f" stroke-width="8" stroke-linecap="round"/>
        <g transform="translate({CRANK_R},0)">
          <g>
            <animateTransform attributeName="transform" type="rotate"
              values="0;-360" dur="{CRANK_DUR}s" repeatCount="indefinite"/>
            <rect x="-13" y="-4" width="26" height="8" rx="3" fill="#2f2f33"/>
          </g>
        </g>
      </g>
    </g>'''


svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <title>Pelican riding a bicycle</title>
  <desc>A cartoon pelican with a helmet sits on the saddle of a red bicycle,
  actively pedaling. Wheels, cranks, chain and legs are animated while the
  road rushes past.</desc>

  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#aee0fb"/>
      <stop offset="1" stop-color="#eef9ff"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  <circle cx="90" cy="78" r="34" fill="#ffd97d" opacity="0.95"/>

  <!-- clouds drifting left -->
  <g opacity="0.9">
    <animateTransform attributeName="transform" type="translate"
      values="0 0;-400 0" dur="20s" repeatCount="indefinite"/>
    <g fill="#ffffff">
      <ellipse cx="200" cy="80" rx="52" ry="18"/>
      <ellipse cx="238" cy="70" rx="34" ry="14"/>
      <ellipse cx="600" cy="115" rx="46" ry="16"/>
      <ellipse cx="634" cy="105" rx="28" ry="12"/>
      <ellipse cx="1000" cy="70" rx="52" ry="18"/>
      <ellipse cx="1038" cy="60" rx="34" ry="14"/>
      <ellipse cx="1400" cy="110" rx="46" ry="16"/>
      <ellipse cx="1434" cy="100" rx="28" ry="12"/>
    </g>
  </g>

  <!-- wind streaks -->
  <g stroke="#ffffff" stroke-width="6" stroke-linecap="round" opacity="0.65"
     fill="none" stroke-dasharray="60 46">
    <path d="M 60 148 H 216">
      <animate attributeName="stroke-dashoffset" values="0;106" dur="0.7s"
        repeatCount="indefinite"/>
    </path>
    <path d="M 40 196 H 196">
      <animate attributeName="stroke-dashoffset" values="0;106" dur="0.55s"
        begin="-0.2s" repeatCount="indefinite"/>
    </path>
    <path d="M 70 244 H 226">
      <animate attributeName="stroke-dashoffset" values="0;106" dur="0.85s"
        begin="-0.45s" repeatCount="indefinite"/>
    </path>
  </g>

  <!-- ground -->
  <rect x="0" y="440" width="{W}" height="18" fill="#9ed36a"/>
  <rect x="0" y="456" width="{W}" height="4" fill="#7ab84f"/>
  <rect x="0" y="460" width="{W}" height="60" fill="#6b7280"/>
  <path d="M 0 490 H {W}" stroke="#ffd23f" stroke-width="6" stroke-dasharray="42 30" fill="none">
    <animate attributeName="stroke-dashoffset" values="0;72" dur="0.206s"
      repeatCount="indefinite"/>
  </path>

  <ellipse cx="400" cy="466" rx="250" ry="10" fill="#000" opacity="0.12"/>

  <!-- far crank + far leg -->
  {crank(180, 540)}
  <path fill="none" stroke="#2b2b2b" stroke-width="13" stroke-linecap="round"
        stroke-linejoin="round" d="{far[0]}">
    <animate attributeName="d" {leg_anim(far)}/>
  </path>
  <path fill="none" stroke="#cf8630" stroke-width="8" stroke-linecap="round"
        stroke-linejoin="round" d="{far[0]}">
    <animate attributeName="d" {leg_anim(far)}/>
  </path>

  <!-- wheels -->
  {wheel(*REAR)}
  {wheel(*FRONT)}

  <!-- frame -->
  <g stroke="#d64550" stroke-width="7" stroke-linecap="round" fill="none">
    <path d="M {HEAD_TOP[0]} {HEAD_TOP[1]} L {HEAD_BOT[0]} {HEAD_BOT[1]}"/>
    <path d="M {SEAT_TUBE_TOP[0]} {SEAT_TUBE_TOP[1]} L {BB[0]} {BB[1]}"/>
    <path d="M {SEAT_TUBE_TOP[0]} {SEAT_TUBE_TOP[1] + 2} L {HEAD_TOP[0]} {HEAD_TOP[1] + 8}"/>
    <path d="M {HEAD_BOT[0]} {HEAD_BOT[1]} L {BB[0]} {BB[1]}"/>
    <path d="M {SEAT_TUBE_TOP[0]} {SEAT_TUBE_TOP[1]} L {REAR[0]} {REAR[1]}"/>
    <path d="M {BB[0]} {BB[1]} L {REAR[0]} {REAR[1]}" stroke="#b8354a"/>
    <path d="M {HEAD_BOT[0]} {HEAD_BOT[1]} Q 562 335 {FRONT[0]} {FRONT[1]}" stroke="#b8354a"/>
  </g>

  <!-- chainring, cog, chain -->
  <circle cx="{BB[0]}" cy="{BB[1]}" r="24" fill="none" stroke="#6b7280" stroke-width="4"/>
  <g>
    <animateTransform attributeName="transform" type="rotate"
      values="0;360" dur="{CRANK_DUR}s" repeatCount="indefinite"/>
    <g transform="translate({BB[0]},{BB[1]})" fill="#6b7280">
      <circle cx="13" cy="0" r="3.5"/><circle cx="-13" cy="0" r="3.5"/>
      <circle cx="0" cy="13" r="3.5"/><circle cx="0" cy="-13" r="3.5"/>
      <circle cx="9" cy="9" r="3.5"/><circle cx="-9" cy="-9" r="3.5"/>
    </g>
  </g>
  <circle cx="{REAR[0]}" cy="{REAR[1]}" r="9" fill="none" stroke="#6b7280" stroke-width="3"/>
  <g stroke="#3f4750" stroke-width="4" stroke-dasharray="7 5" fill="none">
    <path d="M {REAR[0] + 1} {REAR[1] - 8} L {BB[0]} {BB[1] - 23}">
      <animate attributeName="stroke-dashoffset" values="0;-12" dur="0.13s"
        repeatCount="indefinite"/>
    </path>
    <path d="M {REAR[0] + 1} {REAR[1] + 8} L {BB[0]} {BB[1] + 23}">
      <animate attributeName="stroke-dashoffset" values="0;12" dur="0.13s"
        repeatCount="indefinite"/>
    </path>
  </g>

  <!-- seat post, saddle, stem, handlebar -->
  <path d="M {SEAT_TUBE_TOP[0]} {SEAT_TUBE_TOP[1]} L 350 246" stroke="#555b63" stroke-width="6"/>
  <path d="M 316 252 Q 322 242 348 240 Q 388 238 408 252 L 404 262
           Q 380 266 332 265 Q 318 262 316 252 Z"
        fill="#3f4750" stroke="#2b2b2b" stroke-width="3"/>
  <path d="M {HEAD_TOP[0]} {HEAD_TOP[1]} L 536 240" stroke="#555b63" stroke-width="6" stroke-linecap="round"/>
  <path d="M 536 240 C 520 232 506 238 504 258" stroke="#2f2f33" stroke-width="7"
        stroke-linecap="round" fill="none"/>
  <circle cx="{GRIP[0]}" cy="{GRIP[1]}" r="6" fill="#2f2f33"/>

  <!-- pelican -->
  <g>
    <animateTransform attributeName="transform" type="translate"
      values="0 0;0 2.2;0 0" keyTimes="0;0.5;1" dur="0.8s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="rotate" additive="sum"
      values="0 352 250;1.4 352 250;0 352 250;-1 352 250;0 352 250"
      keyTimes="0;0.25;0.5;0.75;1" dur="{CRANK_DUR}s" repeatCount="indefinite"/>

    <!-- tail feathers -->
    <path d="M 276 196 L 242 180 L 262 194 L 234 194 L 260 204 L 244 214 L 272 210 Z"
          fill="#f9f5ee" stroke="#2b2b2b" stroke-width="3" stroke-linejoin="round"/>

    <!-- body with neck and head -->
    <path d="M 272 192
      C 262 202 266 212 282 216
      C 302 230 320 246 350 252
      C 378 258 408 254 426 242
      C 442 230 448 212 444 196
      C 452 174 458 152 456 130
      C 455 118 458 106 468 98
      C 456 82 436 86 432 102
      C 428 118 430 130 426 144
      C 420 162 412 176 400 184
      C 372 192 330 186 300 188
      C 288 188 278 189 272 192 Z"
      fill="#f9f5ee" stroke="#2b2b2b" stroke-width="3" stroke-linejoin="round"/>

    <!-- folded far wing hint -->
    <path d="M 398 198 C 372 226 344 240 314 238" fill="none"
          stroke="#d9d0c1" stroke-width="5" stroke-linecap="round"/>

    <!-- beak (slightly chattering) -->
    <g>
      <animateTransform attributeName="transform" type="rotate"
        values="0 470 112;-5 470 112;0 470 112" keyTimes="0;0.5;1"
        dur="{CRANK_DUR}s" repeatCount="indefinite"/>
      <path d="M 468 116 C 470 148 500 170 540 162 C 566 156 582 148 590 142 L 470 116 Z"
            fill="#f4a261" stroke="#2b2b2b" stroke-width="3" stroke-linejoin="round"/>
      <path d="M 466 92 L 590 136 C 594 138 594 142 590 143 L 470 117 Z"
            fill="#f2c14e" stroke="#2b2b2b" stroke-width="3" stroke-linejoin="round"/>
    </g>

    <!-- eye -->
    <circle cx="448" cy="112" r="6.5" fill="#ffffff" stroke="#2b2b2b" stroke-width="2"/>
    <circle cx="450" cy="113" r="3" fill="#2b2b2b"/>
    <circle cx="448.5" cy="110.8" r="1" fill="#ffffff"/>

    <!-- helmet -->
    <path d="M 422 99 C 424 81 444 73 460 79 C 472 83 478 93 476 101
             L 472 104 C 466 95 456 91 448 91 C 438 91 429 95 426 103 Z"
          fill="#e63946" stroke="#2b2b2b" stroke-width="3" stroke-linejoin="round"/>
    <path d="M 440 77 C 438 83 437 89 438 93 M 458 81 C 457 87 457 92 458 96"
          fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity="0.8"/>
    <path d="M 424 101 Q 428 117 436 123" fill="none" stroke="#2b2b2b" stroke-width="2.5"/>

    <!-- near wing reaching the handlebar -->
    <path d="M 396 192
      C 430 178 468 186 496 220
      C 506 234 510 248 506 262
      C 500 254 494 250 488 248
      C 492 256 490 264 484 270
      C 476 264 470 258 462 254
      C 452 250 442 250 432 252
      C 412 256 396 240 392 214 Z"
      fill="#f9f5ee" stroke="#2b2b2b" stroke-width="3" stroke-linejoin="round"/>
    <path d="M 402 200 C 428 190 456 196 480 222" fill="none"
          stroke="#d9d0c1" stroke-width="4" stroke-linecap="round"/>
  </g>

  <!-- near crank + near leg -->
  {crank(0, 360)}
  <path fill="none" stroke="#2b2b2b" stroke-width="14" stroke-linecap="round"
        stroke-linejoin="round" d="{near[0]}">
    <animate attributeName="d" {leg_anim(near)}/>
  </path>
  <path fill="none" stroke="#f0a13c" stroke-width="9" stroke-linecap="round"
        stroke-linejoin="round" d="{near[0]}">
    <animate attributeName="d" {leg_anim(near)}/>
  </path>
  <circle cx="{HIP_NEAR[0]}" cy="{HIP_NEAR[1]}" r="13" fill="#f9f5ee"/>
</svg>
'''

with open("/tmp/vellery-munnzlng/work/pelican.svg", "w") as f:
    f.write(svg)
print("wrote pelican.svg,", len(svg), "bytes")
