I have created an illustration of a **cozy kitchen in the morning** and saved the vector drawing to [cozy_kitchen.svg](file:///tmp/vellery-elu17k6o/work/cozy_kitchen.svg).

### Morning Kitchen Sketch (ASCII Preview)

```text
      =======================================================================
             ||                                       ||
           _(__)_           .---.                   _(__)_
          /      \         (7:15 )                 /      \
         '--------'         '---'                 '--------'
     [🌿] [🫙][🫙][📚]                   .-------------------------.
     ==================                  | \  \   .       _   /  / |
       [🥛] [🧂][🧂][☕]                 |  \     \  .-.     /  /  |
     ==================                  |---'-------'-'-------'---|
       ||   ||   ||                      |     _.-"""""-._         |
      (  ) (  )  ()                      |   .'           '.  /\   |
     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|  /   [🌿] [🪴]   \ ||   |~~~~
      [🫒][🥄]     .-.      _            '========================='
     -------------|   |---((_))-----------[🍞🍞][🍯]---.--.---[🌻]--[☕][🍎]
     |  [======]  |___|  [======] |  [======]   .------|  |------.  [======] |
     |  |      |  |o o o   o o o| |  |      |   |      '=='      |  |   |  | |
     |  |     o|  | .---------. | |  |     o|   '----------------'  |  o|o | |
     |  |      |  | | 🥐🥐🥐  | | |  |      |   |       ||       |  |   |  | |
     |  '------'  | '---------' | |  '------'   |      o||o      |  '---'--' |
     '------------'-------------'-'-------------'--------''------'-----------'
                  /   /   /   /      .====================.      /
        .--------'---'---'---'-.   .'   .--------------.   '.   /
      .'   [📖]   (🥐🍓)  (☕)  '. |   (   🐈💤         )    | /
      '.           (🥛)   [🌼]  .'  '.  '--------------'   .'
        '----------------------'      '===================='
```

---

### Full SVG Illustration ([cozy_kitchen.svg](file:///tmp/vellery-elu17k6o/work/cozy_kitchen.svg))

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 850" width="1200" height="850">
  <defs>
    <!-- Wall & Room Gradients -->
    <linearGradient id="wallGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F7E6CA"/>
      <stop offset="55%" stop-color="#FFF4DF"/>
      <stop offset="100%" stop-color="#EBD3B0"/>
    </linearGradient>

    <linearGradient id="floorGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#C88851"/>
      <stop offset="50%" stop-color="#B87741"/>
      <stop offset="100%" stop-color="#9E6130"/>
    </linearGradient>

    <linearGradient id="woodCounter" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#DDA067"/>
      <stop offset="40%" stop-color="#C5834B"/>
      <stop offset="100%" stop-color="#9A5F2E"/>
    </linearGradient>

    <linearGradient id="sageCabinet" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#7B9B84"/>
      <stop offset="100%" stop-color="#5B7A64"/>
    </linearGradient>

    <linearGradient id="sageCabinetDark" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#66856F"/>
      <stop offset="100%" stop-color="#4A6753"/>
    </linearGradient>

    <!-- Morning Sky & Sunrise Gradients -->
    <linearGradient id="morningSky" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#7EC4CF"/>
      <stop offset="35%" stop-color="#F6D198"/>
      <stop offset="70%" stop-color="#FBAE72"/>
      <stop offset="100%" stop-color="#FFE699"/>
    </linearGradient>

    <radialGradient id="morningSun" cx="62%" cy="68%" r="48%">
      <stop offset="0%" stop-color="#FFFDF2" stop-opacity="1"/>
      <stop offset="25%" stop-color="#FFE484" stop-opacity="0.95"/>
      <stop offset="60%" stop-color="#FFA955" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#FF8844" stop-opacity="0"/>
    </radialGradient>

    <!-- Sunbeam Gradient -->
    <linearGradient id="sunbeamGrad" x1="65%" y1="0%" x2="20%" y2="100%">
      <stop offset="0%" stop-color="#FFF8D6" stop-opacity="0.42"/>
      <stop offset="45%" stop-color="#FFE694" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#FFD466" stop-opacity="0.02"/>
    </linearGradient>

    <linearGradient id="sunbeamCore" x1="60%" y1="0%" x2="25%" y2="100%">
      <stop offset="0%" stop-color="#FFFDF0" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="#FFEA9F" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#FFD56B" stop-opacity="0.0"/>
    </linearGradient>

    <radialGradient id="floorSunPatch" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFF3B8" stop-opacity="0.55"/>
      <stop offset="65%" stop-color="#FFE082" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#FFD05B" stop-opacity="0"/>
    </radialGradient>

    <!-- Appliances & Props -->
    <linearGradient id="fridgeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#DCECE5"/>
      <stop offset="25%" stop-color="#EEF7F2"/>
      <stop offset="85%" stop-color="#C5DDD3"/>
      <stop offset="100%" stop-color="#A6C5B8"/>
    </linearGradient>

    <linearGradient id="stoveCream" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FCF6EA"/>
      <stop offset="100%" stop-color="#E7DAC3"/>
    </linearGradient>

    <linearGradient id="copperGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F7B385"/>
      <stop offset="45%" stop-color="#D47442"/>
      <stop offset="100%" stop-color="#8F3F1B"/>
    </linearGradient>

    <radialGradient id="ovenGlow" cx="50%" cy="55%" r="55%">
      <stop offset="0%" stop-color="#FFD06B"/>
      <stop offset="60%" stop-color="#E67E22"/>
      <stop offset="100%" stop-color="#5C260B"/>
    </radialGradient>

    <radialGradient id="lampGlow" cx="50%" cy="30%" r="60%">
      <stop offset="0%" stop-color="#FFF8D4" stop-opacity="0.65"/>
      <stop offset="45%" stop-color="#FFD875" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#FFB940" stop-opacity="0"/>
    </radialGradient>

    <!-- Backsplash Tile Pattern -->
    <pattern id="subwayTile" width="44" height="22" patternUnits="userSpaceOnUse">
      <rect width="44" height="22" fill="#FAF2E4"/>
      <rect x="1" y="1" width="42" height="9.5" rx="1" fill="#FFFDF8" stroke="#E2D3BE" stroke-width="1"/>
      <rect x="-21" y="11.5" width="42" height="9.5" rx="1" fill="#FFFBF3" stroke="#E2D3BE" stroke-width="1"/>
      <rect x="23" y="11.5" width="42" height="9.5" rx="1" fill="#FFFBF3" stroke="#E2D3BE" stroke-width="1"/>
    </pattern>

    <!-- Gingham Towel Pattern -->
    <pattern id="gingham" width="12" height="12" patternUnits="userSpaceOnUse">
      <rect width="12" height="12" fill="#FFF9F2"/>
      <rect width="6" height="12" fill="#D9534F" fill-opacity="0.45"/>
      <rect width="12" height="6" fill="#D9534F" fill-opacity="0.45"/>
    </pattern>

    <!-- Window Clip -->
    <clipPath id="windowClip">
      <rect x="495" y="105" width="320" height="305" rx="4"/>
    </clipPath>

    <!-- Soft Drop Shadow -->
    <filter id="softShadow" x="-10%" y="-10%" width="125%" height="125%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#4A2E14" flood-opacity="0.22"/>
    </filter>

    <filter id="steamBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.5"/>
    </filter>
  </defs>

  <!-- ==================== 1. BACKGROUND WALLS & CEILING ==================== -->
  <rect x="0" y="0" width="1200" height="630" fill="url(#wallGrad)"/>
  <ellipse cx="660" cy="300" rx="480" ry="290" fill="url(#morningSun)" opacity="0.25"/>

  <!-- Subway Tile Backsplash Zone -->
  <rect x="60" y="330" width="885" height="145" fill="url(#subwayTile)"/>
  <line x1="60" y1="330" x2="945" y2="330" stroke="#D5C2A5" stroke-width="3"/>
  <rect x="0" y="330" width="60" height="300" fill="#EAD5B7" stroke="#D2B997" stroke-width="1.5"/>

  <!-- Ceiling & Rustic Wooden Beams -->
  <rect x="0" y="0" width="1200" height="34" fill="#F2DEC0"/>
  <line x1="0" y1="34" x2="1200" y2="34" stroke="#D6BE9C" stroke-width="2"/>
  <g fill="#7A4E2D" stroke="#5A371D" stroke-width="1.5">
    <polygon points="120,0 165,0 145,38 100,38"/>
    <polygon points="390,0 435,0 422,38 377,38"/>
    <polygon points="650,0 695,0 695,38 650,38"/>
    <polygon points="920,0 965,0 978,38 933,38"/>
  </g>
  <rect x="0" y="0" width="1200" height="18" fill="#684124"/>
  <line x1="0" y1="18" x2="1200" y2="18" stroke="#8C5B37" stroke-width="2"/>

  <!-- ==================== 2. HARDWOOD FLOOR & BRAIDED RUG ==================== -->
  <rect x="0" y="618" width="1200" height="16" fill="#F5E6CE" stroke="#D1B999" stroke-width="1.5"/>
  <rect x="0" y="634" width="1200" height="216" fill="url(#floorGrad)"/>

  <g stroke="#8C5225" stroke-width="1.5" opacity="0.65">
    <line x1="0" y1="658" x2="1200" y2="658"/>
    <line x1="0" y1="686" x2="1200" y2="686"/>
    <line x1="0" y1="718" x2="1200" y2="718"/>
    <line x1="0" y1="755" x2="1200" y2="755"/>
    <line x1="0" y1="798" x2="1200" y2="798"/>
  </g>
  <g stroke="#7D471E" stroke-width="1.5" opacity="0.55">
    <line x1="180" y1="634" x2="90" y2="686"/>
    <line x1="480" y1="634" x2="430" y2="686"/>
    <line x1="820" y1="634" x2="860" y2="686"/>
    <line x1="320" y1="686" x2="250" y2="755"/>
    <line x1="690" y1="686" x2="680" y2="755"/>
    <line x1="1020" y1="686" x2="1090" y2="755"/>
    <line x1="510" y1="755" x2="465" y2="850"/>
    <line x1="870" y1="755" x2="920" y2="850"/>
  </g>

  <!-- Sunlit Window Patch on the Floor -->
  <polygon points="390,715 735,715 660,845 270,845" fill="url(#floorSunPatch)"/>
  <line x1="562" y1="715" x2="465" y2="845" stroke="#B87741" stroke-width="8" opacity="0.35"/>
  <line x1="340" y1="772" x2="700" y2="772" stroke="#B87741" stroke-width="7" opacity="0.35"/>

  <!-- Cozy Braided Oval Kitchen Rug -->
  <g transform="translate(625, 765)">
    <ellipse cx="0" cy="4" rx="235" ry="58" fill="#5C3418" opacity="0.3"/>
    <ellipse cx="0" cy="0" rx="230" ry="54" fill="#C86D48" stroke="#9C4D2E" stroke-width="3"/>
    <ellipse cx="0" cy="0" rx="202" ry="46" fill="#E8B97A" stroke="#C99655" stroke-width="2.5" stroke-dasharray="10 4"/>
    <ellipse cx="0" cy="0" rx="170" ry="38" fill="#6F8F7B" stroke="#53705E" stroke-width="2.5"/>
    <ellipse cx="0" cy="0" rx="135" ry="29" fill="#F4E3C3" stroke="#D8C29C" stroke-width="2" stroke-dasharray="8 4"/>
    <ellipse cx="0" cy="0" rx="95" ry="19" fill="#D67C56" stroke="#B55E3A" stroke-width="2"/>
    <ellipse cx="0" cy="0" rx="52" ry="9" fill="#F2D29B"/>
  </g>

  <!-- ==================== 3. SUNLIT MORNING WINDOW ==================== -->
  <rect x="478" y="88" width="354" height="346" rx="6" fill="#6B4426" opacity="0.22"/>
  <rect x="475" y="85" width="350" height="340" rx="5" fill="#FFF7E8" stroke="#D5BFA0" stroke-width="3"/>
  <rect x="488" y="98" width="324" height="314" rx="3" fill="#E5CEAE" stroke="#C4AB89" stroke-width="2"/>

  <g clip-path="url(#windowClip)">
    <rect x="495" y="105" width="320" height="305" fill="url(#morningSky)"/>
    <circle cx="685" cy="275" r="135" fill="url(#morningSun)"/>
    <circle cx="685" cy="275" r="38" fill="#FFFDF5" opacity="0.95"/>

    <g fill="#FFF5DF" opacity="0.65">
      <ellipse cx="560" cy="175" rx="48" ry="12"/>
      <ellipse cx="585" cy="170" rx="32" ry="14"/>
      <ellipse cx="745" cy="155" rx="52" ry="11"/>
      <ellipse cx="720" cy="150" rx="28" ry="12"/>
      <ellipse cx="640" cy="215" rx="40" ry="8"/>
    </g>

    <path d="M 490 330 Q 565 285 655 315 T 825 305 L 825 415 L 490 415 Z" fill="#D99B66" opacity="0.75"/>
    <path d="M 490 355 Q 600 315 710 345 T 825 340 L 825 415 L 490 415 Z" fill="#8FA876"/>
    <path d="M 490 375 Q 570 350 675 370 T 825 365 L 825 415 L 490 415 Z" fill="#698B5E"/>

    <g fill="#517049">
      <circle cx="535" cy="340" r="24"/>
      <circle cx="555" cy="345" r="19"/>
      <circle cx="518" cy="348" r="18"/>
      <circle cx="775" cy="335" r="28"/>
      <circle cx="750" cy="344" r="20"/>
    </g>
    <path d="M 535 316 A 24 24 0 0 1 558 335" fill="none" stroke="#FFE28A" stroke-width="2.5" opacity="0.8"/>
    <path d="M 750 324 A 20 20 0 0 0 732 340" fill="none" stroke="#FFE28A" stroke-width="2.5" opacity="0.8"/>

    <path d="M 615 185 Q 621 179 627 185 Q 633 179 639 185" fill="none" stroke="#8C6239" stroke-width="1.8" stroke-linecap="round"/>
    <path d="M 648 172 Q 652 167 657 172 Q 662 167 666 172" fill="none" stroke="#8C6239" stroke-width="1.5" stroke-linecap="round"/>
  </g>

  <!-- Window Panes / Muntin Bars -->
  <rect x="495" y="105" width="320" height="305" fill="none" stroke="#FFF9EE" stroke-width="6"/>
  <rect x="651" y="105" width="8" height="305" fill="#FFF9EE" stroke="#D8C3A5" stroke-width="1"/>
  <rect x="495" y="253" width="320" height="10" fill="#FFF9EE" stroke="#D8C3A5" stroke-width="1"/>
  <rect x="572" y="105" width="4" height="305" fill="#FFF9EE" opacity="0.9"/>
  <rect x="732" y="105" width="4" height="305" fill="#FFF9EE" opacity="0.9"/>
  <rect x="495" y="178" width="320" height="4" fill="#FFF9EE" opacity="0.9"/>
  <rect x="495" y="332" width="320" height="4" fill="#FFF9EE" opacity="0.9"/>

  <!-- Sheer Linen Cafe Curtains -->
  <line x1="458" y1="78" x2="842" y2="78" stroke="#6E472B" stroke-width="5" stroke-linecap="round"/>
  <circle cx="456" cy="78" r="7" fill="#D4A149" stroke="#8C6223" stroke-width="1.5"/>
  <circle cx="844" cy="78" r="7" fill="#D4A149" stroke="#8C6223" stroke-width="1.5"/>
  <path d="M 472 80 L 538 80 Q 530 185 512 255 Q 528 325 518 415 L 470 415 Q 465 250 472 80 Z" fill="#FFFDF7" fill-opacity="0.88" stroke="#E2D2B8" stroke-width="1.5"/>
  <path d="M 488 80 Q 492 175 484 255 Q 494 335 486 415" fill="none" stroke="#E5D5BC" stroke-width="1.5"/>
  <path d="M 505 80 Q 508 175 498 255 Q 508 335 502 415" fill="none" stroke="#E5D5BC" stroke-width="1.5"/>
  <path d="M 468 252 Q 492 260 514 254" fill="none" stroke="#C87A53" stroke-width="6" stroke-linecap="round"/>
  <path d="M 828 80 L 762 80 Q 770 185 788 255 Q 772 325 782 415 L 830 415 Q 835 250 828 80 Z" fill="#FFFDF7" fill-opacity="0.88" stroke="#E2D2B8" stroke-width="1.5"/>
  <path d="M 812 80 Q 808 175 816 255 Q 806 335 814 415" fill="none" stroke="#E5D5BC" stroke-width="1.5"/>
  <path d="M 795 80 Q 792 175 802 255 Q 792 335 798 415" fill="none" stroke="#E5D5BC" stroke-width="1.5"/>
  <path d="M 832 252 Q 808 260 786 254" fill="none" stroke="#C87A53" stroke-width="6" stroke-linecap="round"/>

  <!-- Wooden Window Sill -->
  <rect x="464" y="416" width="372" height="16" rx="3" fill="url(#woodCounter)" stroke="#8F5729" stroke-width="1.5"/>
  <rect x="472" y="432" width="356" height="8" fill="#B87A44"/>

  <!-- Potted Herbs on the Window Sill -->
  <g transform="translate(535, 378)">
    <g stroke="#4E7A47" stroke-width="2.5" stroke-linecap="round">
      <line x1="14" y1="15" x2="4" y2="-16"/>
      <line x1="16" y1="15" x2="12" y2="-22"/>
      <line x1="18" y1="15" x2="20" y2="-24"/>
      <line x1="20" y1="15" x2="28" y2="-18"/>
      <line x1="22" y1="15" x2="34" y2="-8"/>
    </g>
    <g stroke="#76A665" stroke-width="2" stroke-linecap="round">
      <line x1="15" y1="10" x2="7" y2="-12"/>
      <line x1="18" y1="10" x2="16" y2="-18"/>
      <line x1="21" y1="10" x2="25" y2="-14"/>
    </g>
    <polygon points="4,12 32,12 28,38 8,38" fill="#D4724A" stroke="#A65230" stroke-width="1.2"/>
    <rect x="2" y="8" width="32" height="6" rx="1.5" fill="#E07E55" stroke="#A65230" stroke-width="1.2"/>
  </g>

  <g transform="translate(632, 374)">
    <ellipse cx="8" cy="-2" rx="11" ry="8" transform="rotate(-25 8 -2)" fill="#4C8544"/>
    <ellipse cx="28" cy="-2" rx="11" ry="8" transform="rotate(25 28 -2)" fill="#4C8544"/>
    <ellipse cx="18" cy="-12" rx="12" ry="9" fill="#5FA052"/>
    <ellipse cx="10" cy="-16" rx="9" ry="7" transform="rotate(-15 10 -16)" fill="#78B866"/>
    <ellipse cx="25" cy="-15" rx="9" ry="7" transform="rotate(15 25 -15)" fill="#6EB05C"/>
    <ellipse cx="18" cy="-23" rx="8" ry="6" fill="#8CD077"/>
    <polygon points="4,14 32,14 29,42 7,42" fill="#FAF0DC" stroke="#C5B293" stroke-width="1.2"/>
    <line x1="5" y1="23" x2="31" y2="23" stroke="#5B8266" stroke-width="3"/>
    <line x1="6" y1="32" x2="30" y2="32" stroke="#D97F54" stroke-width="2.5"/>
  </g>

  <g transform="translate(722, 378)">
    <path d="M 16 14 Q 8 -4 6 -14" fill="none" stroke="#53824B" stroke-width="2"/>
    <path d="M 18 14 Q 18 -8 18 -20" fill="none" stroke="#53824B" stroke-width="2"/>
    <path d="M 20 14 Q 28 -4 31 -12" fill="none" stroke="#53824B" stroke-width="2"/>
    <ellipse cx="11" cy="2" rx="7" ry="4" transform="rotate(-30 11 2)" fill="#639658"/>
    <ellipse cx="25" cy="2" rx="7" ry="4" transform="rotate(30 25 2)" fill="#639658"/>
    <circle cx="6" cy="-15" r="6" fill="#FFF8E7"/>
    <circle cx="6" cy="-15" r="3" fill="#F5B027"/>
    <circle cx="18" cy="-21" r="7" fill="#FFF8E7"/>
    <circle cx="18" cy="-21" r="3.5" fill="#F5B027"/>
    <circle cx="31" cy="-13" r="6" fill="#FFF8E7"/>
    <circle cx="31" cy="-13" r="3" fill="#F5B027"/>
    <polygon points="4,12 32,12 28,38 8,38" fill="#D4724A" stroke="#A65230" stroke-width="1.2"/>
    <rect x="2" y="8" width="32" height="6" rx="1.5" fill="#E07E55" stroke="#A65230" stroke-width="1.2"/>
  </g>

  <circle cx="595" cy="410" r="8" fill="#E04F3E" stroke="#B03224" stroke-width="1"/>
  <path d="M 592 402 L 595 405 L 598 402" fill="none" stroke="#4D7843" stroke-width="1.5"/>
  <circle cx="610" cy="412" r="6.5" fill="#EA6546" stroke="#B03224" stroke-width="1"/>

  <!-- ==================== 4. LEFT WALL: OPEN SHELVES, PLANTS & COPPER POTS ==================== -->
  <!-- Wall Clock (7:15 AM) -->
  <g transform="translate(425, 130)" filter="url(#softShadow)">
    <circle cx="0" cy="0" r="30" fill="#6F8C78" stroke="#4D6655" stroke-width="3"/>
    <circle cx="0" cy="0" r="24" fill="#FFF9EB" stroke="#D8C5A7" stroke-width="1.5"/>
    <line x1="0" y1="-21" x2="0" y2="-17" stroke="#5A4531" stroke-width="2"/>
    <line x1="21" y1="0" x2="17" y2="0" stroke="#5A4531" stroke-width="2"/>
    <line x1="0" y1="21" x2="0" y2="17" stroke="#5A4531" stroke-width="2"/>
    <line x1="-21" y1="0" x2="-17" y2="0" stroke="#5A4531" stroke-width="2"/>
    <line x1="0" y1="0" x2="-10" y2="9" stroke="#3D2B1F" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="0" y1="0" x2="15" y2="0" stroke="#3D2B1F" stroke-width="1.8" stroke-linecap="round"/>
    <circle cx="0" cy="0" r="2.5" fill="#C95B3C"/>
  </g>

  <!-- UPPER OPEN SHELF -->
  <g filter="url(#softShadow)">
    <path d="M 125 185 L 125 212 M 125 185 L 148 185 A 18 18 0 0 0 125 205" fill="none" stroke="#4A3C31" stroke-width="3.5" stroke-linecap="round"/>
    <path d="M 340 185 L 340 212 M 340 185 L 317 185 A 18 18 0 0 1 340 300" fill="none" stroke="#4A3C31" stroke-width="3.5" stroke-linecap="round"/>
    <rect x="90" y="173" width="285" height="13" rx="2" fill="url(#woodCounter)" stroke="#8F5729" stroke-width="1.5"/>
  </g>

  <!-- Trailing Pothos Plant -->
  <g transform="translate(105, 130)">
    <polygon points="4,10 36,10 31,43 9,43" fill="#C96A44" stroke="#96492B" stroke-width="1.5"/>
    <rect x="2" y="6" width="36" height="6" rx="2" fill="#D97852" stroke="#96492B" stroke-width="1.2"/>
    <ellipse cx="10" cy="2" rx="10" ry="6" transform="rotate(-25 10 2)" fill="#4E8548"/>
    <ellipse cx="28" cy="1" rx="10" ry="6" transform="rotate(20 28 1)" fill="#5E9955"/>
    <ellipse cx="19" cy="-4" rx="11" ry="7" fill="#72B065"/>
    <path d="M 8 12 Q -4 45 2 85 Q 8 120 -2 155" fill="none" stroke="#497A42" stroke-width="2"/>
    <path d="M 16 14 Q 10 50 18 90 Q 22 115 15 135" fill="none" stroke="#5A8F52" stroke-width="1.8"/>
    <ellipse cx="-1" cy="30" rx="8" ry="5" transform="rotate(-35 -1 30)" fill="#5E9955"/>
    <ellipse cx="4" cy="52" rx="8" ry="5" transform="rotate(25 4 52)" fill="#74B368"/>
    <ellipse cx="-2" cy="75" rx="7" ry="5" transform="rotate(-30 -2 75)" fill="#4E8548"/>
    <ellipse cx="5" cy="98" rx="8" ry="5" transform="rotate(20 5 98)" fill="#69A65E"/>
    <ellipse cx="1" cy="122" rx="7" ry="4.5" transform="rotate(-25 1 122)" fill="#74B368"/>
    <ellipse cx="-3" cy="146" rx="6" ry="4" transform="rotate(15 -3 146)" fill="#5E9955"/>
    <ellipse cx="14" cy="42" rx="7" ry="4.5" transform="rotate(25 14 42)" fill="#74B368"/>
    <ellipse cx="18" cy="68" rx="7" ry="4.5" transform="rotate(-20 18 68)" fill="#5E9955"/>
    <ellipse cx="16" cy="96" rx="6.5" ry="4" transform="rotate(25 16 96)" fill="#69A65E"/>
    <ellipse cx="15" cy="122" rx="6" ry="4" transform="rotate(-15 15 122)" fill="#74B368"/>
  </g>

  <!-- Stack of Ceramic Bowls & Plates -->
  <g transform="translate(165, 138)">
    <rect x="0" y="30" width="54" height="5" rx="2" fill="#E8D8C0" stroke="#BFA98B" stroke-width="1"/>
    <rect x="2" y="25" width="50" height="5" rx="2" fill="#F5EAD8" stroke="#BFA98B" stroke-width="1"/>
    <rect x="4" y="20" width="46" height="5" rx="2" fill="#E8D8C0" stroke="#BFA98B" stroke-width="1"/>
    <path d="M 10 8 L 44 8 Q 41 20 27 20 Q 13 20 10 8 Z" fill="#6F8C78" stroke="#4D6655" stroke-width="1.2"/>
    <path d="M 12 0 L 42 0 Q 39 10 27 10 Q 15 10 12 0 Z" fill="#E07E55" stroke="#AD5734" stroke-width="1.2"/>
  </g>

  <!-- Glass Mason Jars & Cookbooks -->
  <g transform="translate(240, 122)">
    <rect x="0" y="6" width="32" height="45" rx="5" fill="#E6F4F1" fill-opacity="0.6" stroke="#A7C4BE" stroke-width="1.5"/>
    <rect x="2" y="18" width="28" height="31" rx="3" fill="#E5CFA8"/>
    <rect x="4" y="0" width="24" height="7" rx="2" fill="#C48851" stroke="#8F5B2D" stroke-width="1.2"/>
    <rect x="6" y="25" width="20" height="10" rx="1" fill="#FFF9EB" stroke="#C7B293" stroke-width="0.8"/>
  </g>
  <g transform="translate(282, 128)">
    <rect x="0" y="6" width="28" height="39" rx="5" fill="#E6F4F1" fill-opacity="0.6" stroke="#A7C4BE" stroke-width="1.5"/>
    <rect x="2" y="15" width="24" height="28" rx="3" fill="#633D22"/>
    <rect x="4" y="0" width="20" height="7" rx="2" fill="#C48851" stroke="#8F5B2D" stroke-width="1.2"/>
    <rect x="5" y="21" width="18" height="9" rx="1" fill="#FFF9EB" stroke="#C7B293" stroke-width="0.8"/>
  </g>
  <g transform="translate(322, 133)">
    <rect x="0" y="0" width="10" height="40" rx="1.5" fill="#C85A3B" stroke="#963D24" stroke-width="1"/>
    <rect x="10" y="4" width="9" height="36" rx="1.5" fill="#5D826B" stroke="#3F5C4A" stroke-width="1"/>
    <rect x="19" y="2" width="11" height="38" rx="1.5" fill="#E0A449" stroke="#AD7A2B" stroke-width="1"/>
  </g>

  <!-- LOWER OPEN SHELF -->
  <g filter="url(#softShadow)">
    <path d="M 125 280 L 125 307 M 125 280 L 148 280 A 18 18 0 0 0 125 300" fill="none" stroke="#4A3C31" stroke-width="3.5" stroke-linecap="round"/>
    <path d="M 340 280 L 340 307 M 340 280 L 317 280 A 18 18 0 0 1 340 300" fill="none" stroke="#4A3C31" stroke-width="3.5" stroke-linecap="round"/>
    <rect x="90" y="268" width="285" height="13" rx="2" fill="url(#woodCounter)" stroke="#8F5729" stroke-width="1.5"/>
  </g>

  <g transform="translate(135, 232)">
    <path d="M 6 6 L 26 6 L 30 36 L 2 36 Z" fill="#FFF8EB" stroke="#C9B69A" stroke-width="1.3"/>
    <path d="M 26 12 Q 37 12 35 23 Q 34 30 28 28" fill="none" stroke="#C9B69A" stroke-width="2.5"/>
    <g transform="translate(48, 12)">
      <rect x="0" y="4" width="16" height="20" rx="2" fill="#D96B43" stroke="#A34928" stroke-width="1"/>
      <rect x="2" y="0" width="12" height="5" rx="1" fill="#B8834E"/>
      <rect x="22" y="4" width="16" height="20" rx="2" fill="#E6AD45" stroke="#B38127" stroke-width="1"/>
      <rect x="24" y="0" width="12" height="5" rx="1" fill="#B8834E"/>
      <rect x="44" y="4" width="16" height="20" rx="2" fill="#6E8F64" stroke="#4D6945" stroke-width="1"/>
      <rect x="46" y="0" width="12" height="5" rx="1" fill="#B8834E"/>
      <rect x="66" y="4" width="16" height="20" rx="2" fill="#C45335" stroke="#8F3820" stroke-width="1"/>
      <rect x="68" y="0" width="12" height="5" rx="1" fill="#B8834E"/>
    </g>
    <g transform="translate(152, 14)">
      <rect x="0" y="0" width="20" height="22" rx="3" fill="#E07E55" stroke="#A85432" stroke-width="1.2"/>
      <path d="M 20 5 Q 27 5 27 11 Q 27 17 20 17" fill="none" stroke="#A85432" stroke-width="2"/>
      <rect x="34" y="0" width="20" height="22" rx="3" fill="#6F8C78" stroke="#4C6353" stroke-width="1.2"/>
      <path d="M 54 5 Q 61 5 61 11 Q 61 17 54 17" fill="none" stroke="#4C6353" stroke-width="2"/>
    </g>
  </g>

  <!-- Hanging Brass Rail with Copper Pans & Utensils -->
  <line x1="115" y1="342" x2="365" y2="342" stroke="#C9963B" stroke-width="4" stroke-linecap="round"/>
  <circle cx="115" cy="342" r="5" fill="#9E7123"/>
  <circle cx="365" cy="342" r="5" fill="#9E7123"/>
  <g transform="translate(148, 342)">
    <line x1="0" y1="0" x2="0" y2="32" stroke="#5A4635" stroke-width="3" stroke-linecap="round"/>
    <circle cx="0" cy="52" r="24" fill="url(#copperGrad)" stroke="#7D3516" stroke-width="2"/>
    <circle cx="-5" cy="47" r="15" fill="none" stroke="#FAD0B1" stroke-width="1.2" opacity="0.6"/>
  </g>
  <g transform="translate(212, 342)">
    <line x1="0" y1="0" x2="0" y2="28" stroke="#5A4635" stroke-width="3" stroke-linecap="round"/>
    <circle cx="0" cy="44" r="19" fill="url(#copperGrad)" stroke="#7D3516" stroke-width="2"/>
    <circle cx="-4" cy="40" r="11" fill="none" stroke="#FAD0B1" stroke-width="1.2" opacity="0.6"/>
  </g>
  <g transform="translate(268, 342)" stroke="#6B4423" stroke-width="2.5" stroke-linecap="round">
    <line x1="0" y1="0" x2="0" y2="42"/>
    <rect x="-7" y="42" width="14" height="16" rx="2" fill="#7C878E" stroke="#525B61" stroke-width="1.5"/>
    <line x1="28" y1="0" x2="28" y2="44"/>
    <ellipse cx="28" cy="50" rx="9" ry="6" fill="url(#copperGrad)" stroke="#7D3516" stroke-width="1.5"/>
    <line x1="56" y1="0" x2="56" y2="40"/>
    <ellipse cx="56" cy="47" rx="7" ry="11" fill="#C4864E" stroke="#8C592B" stroke-width="1.5"/>
  </g>

  <!-- ==================== 5. MAIN KITCHEN CABINETS, STOVE, SINK & FRIDGE ==================== -->
  <rect x="65" y="472" width="875" height="168" fill="#523318" opacity="0.18"/>

  <!-- Left Cabinet Unit -->
  <rect x="68" y="475" width="118" height="158" fill="url(#sageCabinet)" stroke="#47634F" stroke-width="2"/>
  <rect x="78" y="485" width="98" height="32" rx="2" fill="url(#sageCabinetDark)" stroke="#3E5745" stroke-width="1.5"/>
  <circle cx="127" cy="501" r="4.5" fill="#E3B354" stroke="#9E7425" stroke-width="1"/>
  <rect x="78" y="525" width="98" height="96" rx="2" fill="url(#sageCabinetDark)" stroke="#3E5745" stroke-width="1.5"/>
  <rect x="86" y="533" width="82" height="80" fill="url(#sageCabinet)" stroke="#47634F" stroke-width="1"/>
  <circle cx="162" cy="573" r="4.5" fill="#E3B354" stroke="#9E7425" stroke-width="1"/>

  <!-- Vintage Cream Stove & Oven -->
  <g transform="translate(186, 466)">
    <rect x="0" y="0" width="228" height="168" rx="4" fill="url(#stoveCream)" stroke="#C2B197" stroke-width="2"/>
    <rect x="6" y="156" width="216" height="14" fill="#3B322C"/>
    <rect x="4" y="6" width="220" height="32" rx="2" fill="#F0E4CE" stroke="#C8B79C" stroke-width="1.5"/>
    <line x1="4" y1="38" x2="224" y2="38" stroke="#B5A388" stroke-width="2"/>
    <g fill="#E0AF53" stroke="#8F6720" stroke-width="1.5">
      <circle cx="32" cy="22" r="7"/>
      <circle cx="62" cy="22" r="7"/>
      <circle cx="92" cy="22" r="7"/>
      <circle cx="136" cy="22" r="7"/>
      <circle cx="166" cy="22" r="7"/>
      <circle cx="196" cy="22" r="7"/>
    </g>
    <rect x="104" y="17" width="20" height="10" rx="2" fill="#D9A74A" stroke="#8F6720" stroke-width="1"/>
    <rect x="14" y="46" width="200" height="104" rx="5" fill="#FAF2E3" stroke="#BFB097" stroke-width="2"/>
    <rect x="28" y="54" width="172" height="7" rx="3.5" fill="#E3B354" stroke="#9E7425" stroke-width="1.2"/>

    <!-- Warm Glowing Oven Window -->
    <rect x="38" y="70" width="152" height="64" rx="6" fill="url(#ovenGlow)" stroke="#6E4E32" stroke-width="3"/>
    <line x1="40" y1="112" x2="188" y2="112" stroke="#59250C" stroke-width="2.5"/>
    <path d="M 62 111 Q 75 94 92 111 Z" fill="#C96418" stroke="#7A3306" stroke-width="1.5"/>
    <path d="M 102 111 Q 115 94 132 111 Z" fill="#C96418" stroke="#7A3306" stroke-width="1.5"/>
    <path d="M 142 111 Q 155 94 172 111 Z" fill="#C96418" stroke="#7A3306" stroke-width="1.5"/>
    <polygon points="44,74 78,74 54,130 44,130" fill="#FFE8A3" opacity="0.25"/>

    <!-- Gingham Dish Towel -->
    <g transform="translate(148, 54)">
      <path d="M 0 3 L 36 3 L 40 58 Q 20 62 2 58 Z" fill="url(#gingham)" stroke="#C9A895" stroke-width="1.2"/>
      <line x1="2" y1="51" x2="39" y2="51" stroke="#C94A46" stroke-width="2"/>
    </g>

    <rect x="12" y="-6" width="92" height="6" rx="2" fill="#3B3532"/>
    <rect x="124" y="-6" width="92" height="6" rx="2" fill="#3B3532"/>
    <g>
      <circle cx="44" cy="-7" r="3" fill="#5BC0EB"/>
      <circle cx="54" cy="-7" r="3.5" fill="#FF9F1C"/>
      <circle cx="64" cy="-7" r="3.5" fill="#5BC0EB"/>
      <circle cx="74" cy="-7" r="3" fill="#FF9F1C"/>
      <circle cx="156" cy="-7" r="3" fill="#5BC0EB"/>
      <circle cx="168" cy="-7" r="3.5" fill="#FF9F1C"/>
      <circle cx="180" cy="-7" r="3" fill="#5BC0EB"/>
    </g>
  </g>

  <!-- Whistling Tea Kettle & Cast-Iron Skillet -->
  <g transform="translate(216, 412)">
    <path d="M 10 22 Q 10 -6 30 -6 Q 50 -6 50 22" fill="none" stroke="#3B322C" stroke-width="5" stroke-linecap="round"/>
    <rect x="20" y="-9" width="20" height="6" rx="3" fill="#C4834B"/>
    <path d="M 52 34 L 70 16 L 75 21 L 58 42 Z" fill="#D9534F" stroke="#9E312E" stroke-width="1.5"/>
    <circle cx="74" cy="17" r="4" fill="#E3B354" stroke="#9E7425" stroke-width="1"/>
    <path d="M 8 48 Q 4 16 30 16 Q 56 16 52 48 Z" fill="#D94E41" stroke="#9E312E" stroke-width="1.8"/>
    <rect x="7" y="45" width="46" height="4" rx="2" fill="#D8C8B4" stroke="#8C7B68" stroke-width="1"/>
    <ellipse cx="30" cy="16" rx="14" ry="3.5" fill="#E3B354" stroke="#9E7425" stroke-width="1.2"/>
    <circle cx="30" cy="11" r="4" fill="#3B322C"/>
    <path d="M 16 40 Q 15 24 24 21" fill="none" stroke="#FFAD9E" stroke-width="3" stroke-linecap="round" opacity="0.7"/>
  </g>

  <g transform="translate(328, 444)">
    <path d="M 65 8 L 95 2 L 95 8 L 65 13 Z" fill="#332E2C"/>
    <path d="M 4 6 L 68 6 L 62 16 L 10 16 Z" fill="#3B3532" stroke="#24201E" stroke-width="1.5"/>
    <ellipse cx="36" cy="5" rx="22" ry="4" fill="#FFFDF7"/>
    <ellipse cx="32" cy="3.5" rx="7" ry="3" fill="#FFA600"/>
    <ellipse cx="46" cy="4" rx="6" ry="2.5" fill="#FFA600"/>
  </g>

  <g fill="none" stroke="#FFFDF7" stroke-linecap="round" filter="url(#steamBlur)">
    <path d="M 294 422 Q 306 402 292 382 Q 278 362 296 340 Q 312 318 298 295" stroke-width="4" opacity="0.65"/>
    <path d="M 302 416 Q 318 395 304 372 Q 290 350 310 325" stroke-width="3" opacity="0.45"/>
    <path d="M 358 438 Q 348 420 362 402 Q 374 385 360 366" stroke-width="2.8" opacity="0.45"/>
    <path d="M 372 440 Q 382 422 370 404" stroke-width="2.2" opacity="0.35"/>
  </g>

  <!-- Butcher-Block Countertop & Right Cabinets -->
  <rect x="64" y="458" width="124" height="17" rx="2" fill="url(#woodCounter)" stroke="#8F5729" stroke-width="1.5"/>
  <rect x="414" y="458" width="518" height="17" rx="2" fill="url(#woodCounter)" stroke="#8F5729" stroke-width="1.5"/>
  <rect x="414" y="475" width="518" height="158" fill="url(#sageCabinet)" stroke="#47634F" stroke-width="2"/>
  <rect x="68" y="622" width="118" height="12" fill="#3D5243"/>
  <rect x="414" y="622" width="518" height="12" fill="#3D5243"/>

  <rect x="426" y="485" width="122" height="32" rx="2" fill="url(#sageCabinetDark)" stroke="#3E5745" stroke-width="1.5"/>
  <circle cx="487" cy="501" r="4.5" fill="#E3B354" stroke="#9E7425" stroke-width="1"/>
  <rect x="426" y="525" width="122" height="90" rx="2" fill="url(#sageCabinetDark)" stroke="#3E5745" stroke-width="1.5"/>
  <rect x="435" y="534" width="104" height="72" fill="url(#sageCabinet)" stroke="#47634F" stroke-width="1"/>
  <circle cx="533" cy="570" r="4.5" fill="#E3B354" stroke="#9E7425" stroke-width="1"/>

  <!-- Farmhouse Apron-Front Ceramic Sink & Brass Faucet -->
  <g transform="translate(652, 458)">
    <path d="M 0 0 L 0 -36 Q 0 -54 18 -54 Q 34 -54 34 -34" fill="none" stroke="#D9A84A" stroke-width="5.5" stroke-linecap="round"/>
    <ellipse cx="34" cy="-33" rx="4" ry="2.5" fill="#9E7425"/>
    <rect x="-6" y="-6" width="12" height="6" rx="1" fill="#E3B354" stroke="#9E7425" stroke-width="1"/>
    <rect x="-28" y="-6" width="10" height="6" rx="1" fill="#E3B354" stroke="#9E7425" stroke-width="1"/>
    <line x1="-23" y1="-6" x2="-31" y2="-13" stroke="#D9A84A" stroke-width="3" stroke-linecap="round"/>
    <rect x="18" y="-6" width="10" height="6" rx="1" fill="#E3B354" stroke="#9E7425" stroke-width="1"/>
    <line x1="23" y1="-6" x2="31" y2="-13" stroke="#D9A84A" stroke-width="3" stroke-linecap="round"/>
  </g>
  <rect x="562" y="462" width="180" height="58" rx="5" fill="#FFFDF9" stroke="#D6C7B2" stroke-width="2" filter="url(#softShadow)"/>
  <line x1="572" y1="472" x2="732" y2="472" stroke="#EFE6D8" stroke-width="2"/>
  <rect x="562" y="527" width="87" height="88" rx="2" fill="url(#sageCabinetDark)" stroke="#3E5745" stroke-width="1.5"/>
  <rect x="570" y="535" width="71" height="72" fill="url(#sageCabinet)" stroke="#47634F" stroke-width="1"/>
  <circle cx="638" cy="570" r="4.5" fill="#E3B354" stroke="#9E7425" stroke-width="1"/>

  <rect x="655" y="527" width="87" height="88" rx="2" fill="url(#sageCabinetDark)" stroke="#3E5745" stroke-width="1.5"/>
  <rect x="663" y="535" width="71" height="72" fill="url(#sageCabinet)" stroke="#47634F" stroke-width="1"/>
  <circle cx="666" cy="570" r="4.5" fill="#E3B354" stroke="#9E7425" stroke-width="1"/>

  <rect x="756" y="485" width="164" height="32" rx="2" fill="url(#sageCabinetDark)" stroke="#3E5745" stroke-width="1.5"/>
  <circle cx="838" cy="501" r="4.5" fill="#E3B354" stroke="#9E7425" stroke-width="1"/>
  <rect x="756" y="525" width="79" height="90" rx="2" fill="url(#sageCabinetDark)" stroke="#3E5745" stroke-width="1.5"/>
  <rect x="764" y="534" width="63" height="72" fill="url(#sageCabinet)" stroke="#47634F" stroke-width="1"/>
  <circle cx="824" cy="570" r="4.5" fill="#E3B354" stroke="#9E7425" stroke-width="1"/>
  <rect x="841" y="525" width="79" height="90" rx="2" fill="url(#sageCabinetDark)" stroke="#3E5745" stroke-width="1.5"/>
  <rect x="849" y="534" width="63" height="72" fill="url(#sageCabinet)" stroke="#47634F" stroke-width="1"/>
  <circle cx="852" cy="570" r="4.5" fill="#E3B354" stroke="#9E7425" stroke-width="1"/>

  <!-- ==================== 6. COUNTERTOP ITEMS ==================== -->
  <g transform="translate(88, 405)">
    <rect x="0" y="18" width="22" height="35" rx="4" fill="#8EA858" stroke="#627836" stroke-width="1.2"/>
    <rect x="7" y="6" width="8" height="13" fill="#8EA858" stroke="#627836" stroke-width="1.2"/>
    <path d="M 11 6 L 11 0 L 18 -3" fill="none" stroke="#C9963B" stroke-width="2.5" stroke-linecap="round"/>
    <rect x="3" y="27" width="16" height="14" rx="1" fill="#FFF8E8"/>
    <g transform="translate(34, 8)">
      <line x1="10" y1="12" x2="4" y2="-16" stroke="#B5763E" stroke-width="3" stroke-linecap="round"/>
      <ellipse cx="3" cy="-20" rx="5" ry="7" transform="rotate(-15 3 -20)" fill="#C9884E" stroke="#8F5B2D" stroke-width="1.2"/>
      <line x1="20" y1="12" x2="22" y2="-18" stroke="#9E622E" stroke-width="3" stroke-linecap="round"/>
      <rect x="17" y="-26" width="10" height="11" rx="2" fill="#B5763E" stroke="#804E22" stroke-width="1.2"/>
      <line x1="30" y1="12" x2="38" y2="-14" stroke="#8C8C8C" stroke-width="2"/>
      <ellipse cx="40" cy="-19" rx="5" ry="8" transform="rotate(20 40 -19)" fill="none" stroke="#8C8C8C" stroke-width="1.5"/>
      <rect x="2" y="10" width="38" height="35" rx="3" fill="#FAF0DC" stroke="#C5B293" stroke-width="1.5"/>
      <line x1="2" y1="20" x2="40" y2="20" stroke="#6F8C78" stroke-width="3"/>
      <line x1="2" y1="36" x2="40" y2="36" stroke="#6F8C78" stroke-width="2"/>
    </g>
  </g>

  <g transform="translate(428, 424)">
    <rect x="0" y="28" width="95" height="6" rx="2" fill="#B06E38" stroke="#7D491E" stroke-width="1.2"/>
    <path d="M 10 28 Q 10 4 38 4 Q 66 4 66 28 Z" fill="#D48942" stroke="#965A22" stroke-width="1.5"/>
    <path d="M 24 12 Q 35 8 46 12" fill="none" stroke="#FCEFD8" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M 20 18 Q 35 14 50 18" fill="none" stroke="#FCEFD8" stroke-width="2" stroke-linecap="round"/>
    <path d="M 68 28 Q 70 12 80 12 Q 86 12 86 28 Z" fill="#F5DFB8" stroke="#C27B38" stroke-width="2"/>
    <path d="M 76 28 Q 78 14 88 14 Q 93 14 93 28 Z" fill="#F5DFB8" stroke="#C27B38" stroke-width="2"/>
    <g transform="translate(102, 6)">
      <rect x="0" y="6" width="22" height="22" rx="4" fill="#F5A623" stroke="#C47D0E" stroke-width="1.2"/>
      <rect x="3" y="1" width="16" height="5" rx="1.5" fill="#FFF3D6" stroke="#BFA57D" stroke-width="1"/>
      <rect x="4" y="12" width="14" height="8" rx="1" fill="#FFFDF5"/>
    </g>
  </g>

  <g transform="translate(754, 385)">
    <line x1="16" y1="30" x2="6" y2="2" stroke="#497542" stroke-width="3"/>
    <line x1="22" y1="30" x2="22" y2="-6" stroke="#497542" stroke-width="3"/>
    <line x1="28" y1="30" x2="38" y2="4" stroke="#497542" stroke-width="3"/>
    <ellipse cx="8" cy="18" rx="9" ry="5" transform="rotate(-30 8 18)" fill="#5C8F53"/>
    <ellipse cx="36" cy="18" rx="9" ry="5" transform="rotate(30 36 18)" fill="#5C8F53"/>
    <g transform="translate(5, 0)">
      <circle cx="0" cy="0" r="13" fill="#FFC425" stroke="#E09F0B" stroke-width="1.5" stroke-dasharray="5 2"/>
      <circle cx="0" cy="0" r="6" fill="#5C3A1E"/>
    </g>
    <g transform="translate(22, -10)">
      <circle cx="0" cy="0" r="15" fill="#FFD03B" stroke="#E09F0B" stroke-width="1.5" stroke-dasharray="5 2"/>
      <circle cx="0" cy="0" r="7" fill="#5C3A1E"/>
    </g>
    <g transform="translate(38, 2)">
      <circle cx="0" cy="0" r="12" fill="#FFC425" stroke="#E09F0B" stroke-width="1.5" stroke-dasharray="5 2"/>
      <circle cx="0" cy="0" r="5.5" fill="#5C3A1E"/>
    </g>
    <path d="M 8 28 L 36 28 Q 42 52 38 73 L 6 73 Q 2 52 8 28 Z" fill="#F5C453" stroke="#C9962C" stroke-width="1.5"/>
    <path d="M 36 35 Q 48 35 46 49 Q 45 58 38 56" fill="none" stroke="#C9962C" stroke-width="3"/>
    <path d="M 13 36 Q 11 52 13 65" fill="none" stroke="#FFF0B8" stroke-width="2.5" stroke-linecap="round" opacity="0.75"/>
  </g>

  <g transform="translate(818, 405)">
    <polygon points="4,0 32,0 23,20 13,20" fill="#FFF8EB" stroke="#C9B69A" stroke-width="1.5"/>
    <path d="M 30 4 Q 38 4 36 12 Q 35 16 26 15" fill="none" stroke="#C9B69A" stroke-width="2"/>
    <path d="M 11 20 L 25 20 L 34 52 L 2 52 Z" fill="#D9F0EC" fill-opacity="0.55" stroke="#9AB8B3" stroke-width="1.5"/>
    <path d="M 7 35 L 29 35 L 33 50 L 3 50 Z" fill="#4A2711"/>
    <rect x="10" y="19" width="16" height="8" rx="1.5" fill="#C4834B" stroke="#8C592B" stroke-width="1"/>
    <path d="M 18 -4 Q 24 -14 16 -24" fill="none" stroke="#FFFDF7" stroke-width="2" opacity="0.5" filter="url(#steamBlur)"/>
  </g>

  <g transform="translate(866, 424)">
    <circle cx="15" cy="10" r="10" fill="#F28522" stroke="#C7630C" stroke-width="1"/>
    <circle cx="32" cy="8" r="10" fill="#D9453A" stroke="#A62920" stroke-width="1"/>
    <circle cx="46" cy="12" r="9" fill="#F7C825" stroke="#C99E0E" stroke-width="1"/>
    <circle cx="24" cy="3" r="9" fill="#F59B38" stroke="#C7630C" stroke-width="1"/>
    <path d="M 32 -2 Q 35 -7 39 -5" fill="none" stroke="#4D7843" stroke-width="2" stroke-linecap="round"/>
    <path d="M 0 14 L 58 14 Q 52 34 29 34 Q 6 34 0 14 Z" fill="#FAF0DC" stroke="#C4B091" stroke-width="1.8"/>
    <line x1="4" y1="20" x2="54" y2="20" stroke="#D97F54" stroke-width="2.5"/>
  </g>

  <!-- ==================== 7. RETRO MINT REFRIGERATOR ==================== -->
  <g transform="translate(942, 215)" filter="url(#softShadow)">
    <rect x="0" y="0" width="186" height="418" rx="22" fill="url(#fridgeGrad)" stroke="#8FB0A3" stroke-width="2.5"/>
    <path d="M 16 24 L 16 394" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.65"/>
    <line x1="3" y1="132" x2="183" y2="132" stroke="#7A9C8F" stroke-width="3"/>
    <line x1="3" y1="135" x2="183" y2="135" stroke="#F4FBF8" stroke-width="1.5"/>
    <rect x="68" y="38" width="50" height="12" rx="6" fill="#E8ECEA" stroke="#8C9993" stroke-width="1.5"/>
    <line x1="76" y1="44" x2="110" y2="44" stroke="#6E7D76" stroke-width="2"/>
    <rect x="16" y="85" width="32" height="9" rx="4.5" fill="#E8ECEA" stroke="#7F8C86" stroke-width="1.5"/>
    <rect x="16" y="168" width="36" height="10" rx="5" fill="#E8ECEA" stroke="#7F8C86" stroke-width="1.5"/>

    <rect x="65" y="175" width="38" height="42" rx="1" transform="rotate(-5 84 196)" fill="#FFF3A8" stroke="#D9C86A" stroke-width="1"/>
    <circle cx="84" cy="179" r="4" fill="#E05A47"/>
    <line x1="71" y1="190" x2="96" y2="188" stroke="#8C7D56" stroke-width="1.5"/>
    <line x1="72" y1="198" x2="94" y2="196" stroke="#8C7D56" stroke-width="1.5"/>
    <line x1="72" y1="206" x2="88" y2="205" stroke="#8C7D56" stroke-width="1.5"/>

    <g transform="translate(116, 195) rotate(6)">
      <rect x="0" y="0" width="44" height="52" rx="1.5" fill="#FFFDF9" stroke="#C9B99F" stroke-width="1"/>
      <circle cx="22" cy="4" r="4" fill="#5B8C72"/>
      <circle cx="22" cy="24" r="10" fill="#FFB833"/>
      <path d="M 6 44 Q 22 34 38 44" fill="#78A865"/>
    </g>

    <rect x="18" y="416" width="24" height="8" rx="2" fill="#4A5752"/>
    <rect x="144" y="416" width="24" height="8" rx="2" fill="#4A5752"/>

    <g transform="translate(36, -42)">
      <rect x="0" y="6" width="84" height="36" rx="6" fill="#C98A4E" stroke="#8C5928" stroke-width="1.8"/>
      <line x1="0" y1="16" x2="84" y2="16" stroke="#9E6732" stroke-width="2"/>
      <line x1="0" y1="28" x2="84" y2="28" stroke="#9E6732" stroke-width="2"/>
      <line x1="20" y1="6" x2="20" y2="42" stroke="#9E6732" stroke-width="1.8"/>
      <line x1="42" y1="6" x2="42" y2="42" stroke="#9E6732" stroke-width="1.8"/>
      <line x1="64" y1="6" x2="64" y2="42" stroke="#9E6732" stroke-width="1.8"/>
      <path d="M 10 6 Q 28 -4 48 6 Q 68 -2 78 6" fill="#FFF8EB" stroke="#D4C2A5" stroke-width="1.2"/>
    </g>
  </g>

  <!-- ==================== 8. SLEEPING GINGER CAT ON THE RUG ==================== -->
  <g transform="translate(565, 738)" filter="url(#softShadow)">
    <ellipse cx="32" cy="18" rx="46" ry="22" fill="#FFF0A8" opacity="0.45"/>
    <ellipse cx="32" cy="16" rx="34" ry="20" fill="#E8873C" stroke="#B55D1B" stroke-width="1.5"/>
    <path d="M 22 -2 Q 26 10 22 22" fill="none" stroke="#BD5A15" stroke-width="3" stroke-linecap="round"/>
    <path d="M 34 -4 Q 38 10 34 24" fill="none" stroke="#BD5A15" stroke-width="3" stroke-linecap="round"/>
    <path d="M 46 -1 Q 50 10 46 22" fill="none" stroke="#BD5A15" stroke-width="3" stroke-linecap="round"/>
    <path d="M 58 24 Q 72 30 62 36 Q 45 40 24 34" fill="none" stroke="#E8873C" stroke-width="8" stroke-linecap="round"/>
    <path d="M 58 24 Q 72 30 62 36 Q 45 40 24 34" fill="none" stroke="#BD5A15" stroke-width="8" stroke-linecap="round" stroke-dasharray="4 7"/>
    <circle cx="10" cy="16" r="15" fill="#F09449" stroke="#B55D1B" stroke-width="1.5"/>
    <polygon points="0,6 4,-7 13,3" fill="#E8873C" stroke="#B55D1B" stroke-width="1.2"/>
    <polygon points="3,4 5,-3 10,3" fill="#F7B7A3"/>
    <polygon points="12,3 20,-7 23,7" fill="#E8873C" stroke="#B55D1B" stroke-width="1.2"/>
    <polygon points="14,3 19,-3 20,5" fill="#F7B7A3"/>
    <path d="M 2 16 Q 6 20 10 16" fill="none" stroke="#6E350E" stroke-width="1.8" stroke-linecap="round"/>
    <path d="M 13 16 Q 17 20 21 16" fill="none" stroke="#6E350E" stroke-width="1.8" stroke-linecap="round"/>
    <polygon points="9,21 13,21 11,24" fill="#E87A7A"/>
    <ellipse cx="4" cy="29" rx="6" ry="3.5" fill="#FFF9EE" stroke="#C9B293" stroke-width="1"/>
    <ellipse cx="16" cy="30" rx="6" ry="3.5" fill="#FFF9EE" stroke="#C9B293" stroke-width="1"/>
  </g>

  <!-- ==================== 9. FOREGROUND BREAKFAST TABLE & CHAIRS ==================== -->
  <g transform="translate(205, 575)">
    <path d="M 0 85 L 6 10 Q 38 -6 70 10 L 76 85" fill="none" stroke="#9E6230" stroke-width="7" stroke-linecap="round"/>
    <line x1="18" y1="6" x2="16" y2="85" stroke="#9E6230" stroke-width="4"/>
    <line x1="30" y1="3" x2="30" y2="85" stroke="#9E6230" stroke-width="4"/>
    <line x1="46" y1="3" x2="46" y2="85" stroke="#9E6230" stroke-width="4"/>
    <line x1="58" y1="6" x2="60" y2="85" stroke="#9E6230" stroke-width="4"/>
  </g>

  <g transform="translate(415, 620)">
    <line x1="12" y1="115" x2="4" y2="215" stroke="#7D491E" stroke-width="8" stroke-linecap="round"/>
    <line x1="68" y1="115" x2="78" y2="215" stroke="#7D491E" stroke-width="8" stroke-linecap="round"/>
    <line x1="10" y1="168" x2="72" y2="168" stroke="#7D491E" stroke-width="5"/>
    <ellipse cx="40" cy="112" rx="44" ry="13" fill="#B8763E" stroke="#7D491E" stroke-width="2"/>
    <path d="M 62 110 L 76 4 Q 58 -6 40 4 L 30 108" fill="none" stroke="#A86832" stroke-width="7" stroke-linecap="round"/>
    <line x1="48" y1="4" x2="41" y2="108" stroke="#A86832" stroke-width="3.5"/>
    <line x1="58" y1="3" x2="50" y2="108" stroke="#A86832" stroke-width="3.5"/>
    <line x1="67" y1="4" x2="58" y2="108" stroke="#A86832" stroke-width="3.5"/>
    <ellipse cx="38" cy="107" rx="36" ry="9" fill="#E8D5B5" stroke="#C2AB86" stroke-width="1.5"/>
  </g>

  <g transform="translate(235, 705)" filter="url(#softShadow)">
    <rect x="-18" y="30" width="36" height="115" fill="#7D491E"/>
    <path d="M -18 115 L -95 145 L -80 148 L 0 128 L 80 148 L 95 145 L 18 115 Z" fill="#693C17"/>
    <ellipse cx="0" cy="8" rx="205" ry="66" fill="#8C5425"/>
    <ellipse cx="0" cy="0" rx="205" ry="64" fill="url(#woodCounter)" stroke="#A36631" stroke-width="2"/>

    <path d="M -68 -61 L 68 -61 L 92 61 Q 0 68 -92 61 Z" fill="#FFF9ED" stroke="#DECBB0" stroke-width="1.5"/>
    <line x1="-62" y1="-58" x2="-82" y2="59" stroke="#D97F54" stroke-width="2" stroke-dasharray="6 3"/>
    <line x1="62" y1="-58" x2="82" y2="59" stroke="#D97F54" stroke-width="2" stroke-dasharray="6 3"/>

    <!-- Plate with Croissant & Berries -->
    <g transform="translate(-55, -2)">
      <ellipse cx="0" cy="4" rx="54" ry="24" fill="#D9C7AD"/>
      <ellipse cx="0" cy="0" rx="54" ry="23" fill="#FFFDF8" stroke="#E0D0B8" stroke-width="1.5"/>
      <ellipse cx="0" cy="0" rx="38" ry="15" fill="none" stroke="#6F8C78" stroke-width="1.5"/>
      <g transform="translate(-10, -4) rotate(-12)">
        <path d="M -26 6 Q -18 -14 0 -14 Q 18 -14 26 6 Q 16 12 10 2 Q 0 -4 -10 2 Q -16 12 -26 6 Z" fill="#E39339" stroke="#A86116" stroke-width="1.5"/>
        <path d="M -12 -10 Q 0 -15 12 -10" fill="none" stroke="#FFC970" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M -14 -7 Q -10 1 -12 5 M 0 -13 Q 0 -3 0 0 M 14 -7 Q 10 1 12 5" fill="none" stroke="#A86116" stroke-width="1.5"/>
      </g>
      <circle cx="20" cy="5" r="6" fill="#D9383A" stroke="#9E1E20" stroke-width="1"/>
      <circle cx="29" cy="2" r="5" fill="#E34648" stroke="#9E1E20" stroke-width="1"/>
      <circle cx="12" cy="9" r="3.5" fill="#465985"/>
      <circle cx="18" cy="11" r="3" fill="#374870"/>
      <circle cx="25" cy="9" r="3.2" fill="#465985"/>
    </g>

    <!-- Steaming Coffee Mug with Latte Art -->
    <g transform="translate(42, -16)">
      <ellipse cx="0" cy="18" rx="28" ry="12" fill="#E5D5BE" stroke="#C2B097" stroke-width="1.2"/>
      <ellipse cx="0" cy="16" rx="26" ry="10" fill="#FFFDF8"/>
      <path d="M 16 0 Q 27 0 27 8 Q 27 15 15 15" fill="none" stroke="#C96A44" stroke-width="4"/>
      <path d="M -17 -6 L 17 -6 L 14 17 Q 0 21 -14 17 Z" fill="#D97852" stroke="#A65230" stroke-width="1.5"/>
      <ellipse cx="0" cy="-6" rx="17" ry="6.5" fill="#FFF8EB" stroke="#A65230" stroke-width="1.2"/>
      <ellipse cx="0" cy="-6" rx="14.5" ry="5" fill="#6E3F1D"/>
      <path d="M 0 -4 C -5 -8 -7 -4 0 -2 C 7 -4 5 -8 0 -4 Z" fill="#F7E8D0"/>
      <g fill="none" stroke="#FFFDF7" stroke-linecap="round" filter="url(#steamBlur)">
        <path d="M -4 -14 Q -10 -28 -1 -42 Q 7 -55 -2 -68" stroke-width="3" opacity="0.7"/>
        <path d="M 5 -12 Q 12 -26 4 -38 Q -3 -50 6 -62" stroke-width="2.5" opacity="0.55"/>
      </g>
    </g>

    <!-- Fresh Orange Juice -->
    <g transform="translate(-8, -42)">
      <ellipse cx="0" cy="16" rx="12" ry="5" fill="#D9C7AD"/>
      <path d="M -12 -14 L 12 -14 L 10 15 Q 0 18 -10 15 Z" fill="#FFF8EB" fill-opacity="0.55" stroke="#C9B99F" stroke-width="1.2"/>
      <path d="M -10 -5 L 10 -5 L 9 14 Q 0 17 -9 14 Z" fill="#FFA62B"/>
      <ellipse cx="0" cy="-5" rx="10" ry="3.5" fill="#FFC257"/>
      <ellipse cx="0" cy="-14" rx="12" ry="4" fill="none" stroke="#E0D2BC" stroke-width="1.2"/>
    </g>

    <!-- Open Morning Book -->
    <g transform="translate(-138, -10) rotate(-14)">
      <path d="M 0 0 Q 20 -4 38 2 L 34 32 Q 16 26 -4 30 Z" fill="#FFFDF7" stroke="#C9B89D" stroke-width="1.2"/>
      <path d="M 38 2 Q 56 -4 76 0 L 72 30 Q 54 26 34 32 Z" fill="#F7EFE0" stroke="#C9B89D" stroke-width="1.2"/>
      <line x1="38" y1="2" x2="34" y2="32" stroke="#B5A184" stroke-width="1.5"/>
      <line x1="5" y1="8" x2="30" y2="9" stroke="#A6957C" stroke-width="1.5"/>
      <line x1="4" y1="14" x2="28" y2="15" stroke="#A6957C" stroke-width="1.5"/>
      <line x1="3" y1="20" x2="24" y2="21" stroke="#A6957C" stroke-width="1.5"/>
      <line x1="44" y1="8" x2="68" y2="8" stroke="#A6957C" stroke-width="1.5"/>
      <line x1="43" y1="14" x2="67" y2="14" stroke="#A6957C" stroke-width="1.5"/>
      <line x1="42" y1="20" x2="62" y2="20" stroke="#A6957C" stroke-width="1.5"/>
    </g>

    <!-- Small Vase with Fresh Daisies -->
    <g transform="translate(115, -18)">
      <ellipse cx="0" cy="24" rx="14" ry="6" fill="#C9B293" opacity="0.5"/>
      <path d="M -8 2 L 8 2 Q 14 14 10 24 L -10 24 Q -14 14 -8 2 Z" fill="#6F8C78" stroke="#4D6655" stroke-width="1.2"/>
      <line x1="-2" y1="2" x2="-8" y2="-14" stroke="#4E7A47" stroke-width="2"/>
      <line x1="2" y1="2" x2="7" y2="-16" stroke="#4E7A47" stroke-width="2"/>
      <circle cx="-8" cy="-15" r="7" fill="#FFFDF8" stroke="#E5D5BC" stroke-width="0.8"/>
      <circle cx="-8" cy="-15" r="3" fill="#F5B027"/>
      <circle cx="7" cy="-17" r="7.5" fill="#FFFDF8" stroke="#E5D5BC" stroke-width="0.8"/>
      <circle cx="7" cy="-17" r="3.2" fill="#F5B027"/>
    </g>
  </g>

  <!-- ==================== 10. HANGING WOVEN RATTAN PENDANT LAMPS ==================== -->
  <g transform="translate(285, 18)">
    <ellipse cx="0" cy="115" rx="95" ry="70" fill="url(#lampGlow)"/>
    <line x1="0" y1="0" x2="0" y2="75" stroke="#4A3525" stroke-width="3"/>
    <rect x="-7" y="72" width="14" height="10" rx="2" fill="#D9A84A" stroke="#8F6720" stroke-width="1.2"/>
    <circle cx="0" cy="108" r="11" fill="#FFFDF0"/>
    <path d="M -38 106 Q -36 78 0 78 Q 36 78 38 106 Z" fill="#D49553" stroke="#8F5B28" stroke-width="2"/>
    <path d="M -32 97 L 32 97 M -24 88 L 24 88" fill="none" stroke="#9E652E" stroke-width="1.5" stroke-dasharray="5 3"/>
    <ellipse cx="0" cy="106" rx="38" ry="5" fill="none" stroke="#8F5B28" stroke-width="2"/>
  </g>

  <g transform="translate(655, 18)">
    <ellipse cx="0" cy="105" rx="95" ry="70" fill="url(#lampGlow)"/>
    <line x1="0" y1="0" x2="0" y2="65" stroke="#4A3525" stroke-width="3"/>
    <rect x="-7" y="62" width="14" height="10" rx="2" fill="#D9A84A" stroke="#8F6720" stroke-width="1.2"/>
    <circle cx="0" cy="98" r="11" fill="#FFFDF0"/>
    <path d="M -38 96 Q -36 68 0 68 Q 36 68 38 96 Z" fill="#D49553" stroke="#8F5B28" stroke-width="2"/>
    <path d="M -32 87 L 32 87 M -24 78 L 24 78" fill="none" stroke="#9E652E" stroke-width="1.5" stroke-dasharray="5 3"/>
    <ellipse cx="0" cy="96" rx="38" ry="5" fill="none" stroke="#8F5B28" stroke-width="2"/>
  </g>

  <!-- ==================== 11. DIAGONAL MORNING SUNBEAMS & DUST MOTES ==================== -->
  <g pointer-events="none">
    <polygon points="500,110 648,110 310,740 80,740" fill="url(#sunbeamGrad)"/>
    <polygon points="660,110 810,110 580,790 365,790" fill="url(#sunbeamCore)"/>
    <polygon points="500,265 810,265 730,845 265,845" fill="url(#sunbeamGrad)"/>

    <g fill="#FFFDF0">
      <circle cx="545" cy="215" r="2.2" opacity="0.8"/>
      <circle cx="590" cy="240" r="1.6" opacity="0.7"/>
      <circle cx="685" cy="210" r="2.5" opacity="0.85"/>
      <circle cx="725" cy="250" r="1.8" opacity="0.7"/>
      <circle cx="485" cy="310" r="2.0" opacity="0.75"/>
      <circle cx="520" cy="350" r="2.8" opacity="0.65"/>
      <circle cx="615" cy="335" r="2.2" opacity="0.8"/>
      <circle cx="660" cy="380" r="1.7" opacity="0.75"/>
      <circle cx="430" cy="420" r="2.4" opacity="0.7"/>
      <circle cx="465" cy="475" r="1.8" opacity="0.65"/>
      <circle cx="555" cy="465" r="2.6" opacity="0.8"/>
      <circle cx="595" cy="515" r="2.0" opacity="0.7"/>
      <circle cx="380" cy="530" r="2.2" opacity="0.6"/>
      <circle cx="490" cy="575" r="2.5" opacity="0.75"/>
      <circle cx="535" cy="630" r="1.9" opacity="0.65"/>
      <circle cx="330" cy="605" r="2.1" opacity="0.55"/>
      <circle cx="445" cy="660" r="2.4" opacity="0.65"/>
      <circle cx="585" cy="690" r="2.0" opacity="0.7"/>
      <circle cx="515" cy="725" r="2.5" opacity="0.6"/>
    </g>
  </g>
</svg>
```
