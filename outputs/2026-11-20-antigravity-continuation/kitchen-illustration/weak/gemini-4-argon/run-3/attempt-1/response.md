Here is a drawing of a cozy kitchen in the morning—saved as a full-color vector illustration in [cozy_kitchen_morning.svg](file:///tmp/vellery-dyykkw49/work/cozy_kitchen_morning.svg), alongside an ASCII sketch and the embedded SVG source below.

### ASCII Preview

```text
  ====================================================================================
   ||                           ||                     ||             |          ||
   ||    ____________________   ||     .---------.     ||             |          ||
   ||   |  _  RETRO FRIDGE   |  ||    /           \    ||           .-'-.        ||
   ||   | (_)                |   _   |  RANGE HOOD |    _          /     \       ||
   ||   |                    |  [_]_[_______________]  [_]        | (   ) |      ||
   ||   |--------------------|  ===   |  o  |  Y  |    ===     .====================.
   ||   |   .----.          ||        | (_) |     |            ||  \  |  /   .-.   ||
   ||   |   |note|       [] ||  ___  _             _           || -- (O) -- (   )  ||
   ||   |   '----'          || |   || |   (   )   | |          ||  /  |  \   '-'   ||
   ||   |         .---.     || |   || |    ) (    | |          ||------------------||
   ||   |         |pic|  [] || |   || |   .---.   | |          ||  .~.  \||/  .~.  ||
   ||   |         '---'     ||_|___||_|__/_____\__|_|____||____||__[_]__[__]__[_]__||
   ||   |                    |=============================|        ___||___        |
   ||   |                    |  [======] | o o o  (L) o o || [====] |      | [====] |
   ||   |                    |  |   |  | | .------------. || |  | | |______| |    | |
   ||   |                    |  |  o|o | | |  .------.  | || | o|o| |  |   | | [] | |
   ||   |                    |  |   |  | | | (________) | || |  | | | o|o  | |====| |
   ||   '--------------------'  '------' '-'------------'-''------'-'------'-'------'
  /          /               /            /   (   )   /           .---------.        \
 /          /               /   .====================.      .--. /   \ | /   \ .--.   \
/          /               /   /  /\    /\    /\      \    |    |  Croissants |    |   \
          /               /   /  /  \  /  \  /  \  ,=._\   |    |  & Coffee   |    |
         /   *  .  *     /   /   \  /  \  /  \  / ( -.- )  |.--.|     (_)     |.--.|
        /     .    *    /   '======================`---'==='    '\___________/'    '
       /               /                                            ||   ||
```

---

### SVG Illustration ([cozy_kitchen_morning.svg](file:///tmp/vellery-dyykkw49/work/cozy_kitchen_morning.svg))

- **Morning Sunlight:** Golden-hour sunbeams streaming diagonally through a cottage window with sheer linen curtains and potted culinary herbs on the sill.
- **Kitchen Details:** Sage-green shaker cabinets with brass hardware, a butcher-block countertop, zellige subway tile backsplash, a vintage cream fridge with trailing pothos, and a whistling copper kettle steaming on the farmhouse range.
- **Breakfast Nook & Cat:** A ginger tabby cat curled asleep on a woven runner rug in the sunbeam, next to a round oak breakfast table set with fresh croissants, strawberry jam, a French press, a steaming latte, daffodils in a pitcher, and an open morning book.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 850" width="1200" height="850">
  <defs>
    <!-- Wall & Ceiling Gradients -->
    <linearGradient id="wallGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F7E5C8"/>
      <stop offset="55%" stop-color="#FBEAD0"/>
      <stop offset="100%" stop-color="#E5C9A1"/>
    </linearGradient>
    <linearGradient id="rightWallGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#E9CFA8"/>
      <stop offset="100%" stop-color="#D7B88E"/>
    </linearGradient>
    <linearGradient id="ceilingGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E8CFB0"/>
      <stop offset="100%" stop-color="#F6E4C8"/>
    </linearGradient>
    <linearGradient id="floorGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#B87642"/>
      <stop offset="45%" stop-color="#CD8B52"/>
      <stop offset="100%" stop-color="#8F5528"/>
    </linearGradient>

    <!-- Morning Sky & Sun Gradients -->
    <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#9BB8D3"/>
      <stop offset="32%" stop-color="#E8C3A9"/>
      <stop offset="68%" stop-color="#FDD79A"/>
      <stop offset="100%" stop-color="#FFF2C2"/>
    </linearGradient>
    <radialGradient id="sunGlow" cx="65%" cy="62%" r="55%">
      <stop offset="0%" stop-color="#FFFDF0" stop-opacity="1"/>
      <stop offset="25%" stop-color="#FFE79E" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#FDBB6B" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#FD9E58" stop-opacity="0"/>
    </radialGradient>

    <!-- Sunbeam Gradients -->
    <linearGradient id="sunbeam1" x1="70%" y1="15%" x2="20%" y2="95%">
      <stop offset="0%" stop-color="#FFF6CC" stop-opacity="0.42"/>
      <stop offset="45%" stop-color="#FFE699" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#FFD470" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="sunbeam2" x1="75%" y1="20%" x2="35%" y2="100%">
      <stop offset="0%" stop-color="#FFF9D9" stop-opacity="0.36"/>
      <stop offset="55%" stop-color="#FFE8A3" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#FFD269" stop-opacity="0.0"/>
    </linearGradient>
    <radialGradient id="floorSunPatch" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFF3B8" stop-opacity="0.55"/>
      <stop offset="60%" stop-color="#FFE184" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#FFCC5C" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="lampGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFF5C0" stop-opacity="0.7"/>
      <stop offset="40%" stop-color="#FFD573" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#FFB84D" stop-opacity="0"/>
    </radialGradient>

    <!-- Wood, Sage Cabinet & Metal Gradients -->
    <linearGradient id="sageCabinet" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#7D967E"/>
      <stop offset="100%" stop-color="#5D755F"/>
    </linearGradient>
    <linearGradient id="sageDark" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#637B65"/>
      <stop offset="100%" stop-color="#4A5F4C"/>
    </linearGradient>
    <linearGradient id="butcherBlock" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#B9733E"/>
      <stop offset="35%" stop-color="#D7935B"/>
      <stop offset="70%" stop-color="#E2A46D"/>
      <stop offset="100%" stop-color="#B36E39"/>
    </linearGradient>
    <linearGradient id="beamWood" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#5E3A20"/>
      <stop offset="50%" stop-color="#784C2C"/>
      <stop offset="100%" stop-color="#4B2D17"/>
    </linearGradient>
    <linearGradient id="copperGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F6B082"/>
      <stop offset="40%" stop-color="#D47442"/>
      <stop offset="75%" stop-color="#9E4820"/>
      <stop offset="100%" stop-color="#ECA070"/>
    </linearGradient>
    <linearGradient id="brassGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FCE394"/>
      <stop offset="50%" stop-color="#D4A338"/>
      <stop offset="100%" stop-color="#9A6E18"/>
    </linearGradient>
    <linearGradient id="fridgeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFF7E5"/>
      <stop offset="75%" stop-color="#F5E5C9"/>
      <stop offset="100%" stop-color="#DEC8A4"/>
    </linearGradient>
    <linearGradient id="tableTopGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E7AC72"/>
      <stop offset="55%" stop-color="#C9854B"/>
      <stop offset="100%" stop-color="#9E612D"/>
    </linearGradient>

    <!-- Subway / Zellige Tile Pattern -->
    <pattern id="tilePattern" width="44" height="24" patternUnits="userSpaceOnUse">
      <rect width="44" height="24" fill="#F4E7D1"/>
      <rect x="1" y="1" width="20" height="10" rx="1.5" fill="#FFF7E8" stroke="#E2D1B5" stroke-width="0.8"/>
      <rect x="23" y="1" width="20" height="10" rx="1.5" fill="#FBF0DC" stroke="#E2D1B5" stroke-width="0.8"/>
      <rect x="-10" y="13" width="20" height="10" rx="1.5" fill="#F9ECDA" stroke="#E2D1B5" stroke-width="0.8"/>
      <rect x="12" y="13" width="20" height="10" rx="1.5" fill="#FFF9EE" stroke="#E2D1B5" stroke-width="0.8"/>
      <rect x="34" y="13" width="20" height="10" rx="1.5" fill="#F7E9D3" stroke="#E2D1B5" stroke-width="0.8"/>
    </pattern>

    <!-- Soft Blur Filters -->
    <filter id="softBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
    <filter id="steamBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
    <filter id="shadowBlur" x="-10%" y="-10%" width="130%" height="130%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>

    <!-- Window Clip Path -->
    <clipPath id="windowClip">
      <rect x="650" y="128" width="270" height="270" rx="6"/>
    </clipPath>
  </defs>

  <!-- ================= BACKGROUND WALLS, CEILING & FLOOR ================= -->
  <rect x="0" y="55" width="1030" height="535" fill="url(#wallGrad)"/>
  <polygon points="1030,55 1200,0 1200,720 1030,590" fill="url(#rightWallGrad)"/>
  <line x1="1030" y1="55" x2="1030" y2="590" stroke="#D1B28A" stroke-width="2"/>

  <!-- Ceiling & Exposed Timber Beams -->
  <polygon points="0,0 1200,0 1030,55 0,55" fill="url(#ceilingGrad)"/>
  <rect x="0" y="42" width="1035" height="24" fill="url(#beamWood)"/>
  <line x1="0" y1="66" x2="1035" y2="66" stroke="#3B2210" stroke-width="2"/>
  <polygon points="160,0 200,0 230,44 195,44" fill="url(#beamWood)"/>
  <polygon points="480,0 520,0 535,44 500,44" fill="url(#beamWood)"/>
  <polygon points="810,0 850,0 845,44 810,44" fill="url(#beamWood)"/>
  <polygon points="1030,42 1200,0 1200,26 1030,66" fill="#5A371E"/>

  <!-- Wooden Plank Floor -->
  <polygon points="0,590 1030,590 1200,720 1200,850 0,850" fill="url(#floorGrad)"/>
  <g stroke="#7D481F" stroke-width="1.3" opacity="0.55">
    <line x1="0" y1="620" x2="1069" y2="620"/>
    <line x1="0" y1="655" x2="1115" y2="655"/>
    <line x1="0" y1="695" x2="1167" y2="695"/>
    <line x1="0" y1="740" x2="1200" y2="740"/>
    <line x1="0" y1="792" x2="1200" y2="792"/>
    <line x1="140" y1="590" x2="40" y2="850"/>
    <line x1="310" y1="590" x2="240" y2="850"/>
    <line x1="485" y1="590" x2="460" y2="850"/>
    <line x1="650" y1="590" x2="685" y2="850"/>
    <line x1="825" y1="590" x2="920" y2="850"/>
    <line x1="980" y1="590" x2="1145" y2="850"/>
  </g>

  <!-- Right Wall Beadboard Wainscoting -->
  <polygon points="1030,390 1200,455 1200,720 1030,590" fill="#6D846E"/>
  <g stroke="#566B57" stroke-width="1.5">
    <line x1="1030" y1="390" x2="1200" y2="455" stroke="#859E86" stroke-width="5"/>
    <line x1="1055" y1="400" x2="1055" y2="609"/>
    <line x1="1080" y1="410" x2="1080" y2="628"/>
    <line x1="1105" y1="419" x2="1105" y2="647"/>
    <line x1="1130" y1="429" x2="1130" y2="666"/>
    <line x1="1155" y1="438" x2="1155" y2="685"/>
    <line x1="1180" y1="448" x2="1180" y2="704"/>
  </g>
  <polygon points="1030,572 1200,700 1200,720 1030,590" fill="#4E624F"/>

  <!-- ================= TILED BACKSPLASH ================= -->
  <rect x="185" y="250" width="845" height="175" fill="url(#tilePattern)"/>
  <rect x="185" y="247" width="845" height="4" fill="#D9C3A3"/>
  <polygon points="560,250 940,250 860,425 470,425" fill="#FFE69E" opacity="0.22"/>

  <!-- ================= LARGE COTTAGE WINDOW (MORNING VIEW) ================= -->
  <g clip-path="url(#windowClip)">
    <rect x="650" y="128" width="270" height="270" fill="url(#skyGrad)"/>
    <circle cx="825" cy="285" r="135" fill="url(#sunGlow)"/>
    <circle cx="825" cy="285" r="34" fill="#FFFDF4" opacity="0.95"/>
    <g fill="#FFF5DF" opacity="0.65">
      <ellipse cx="715" cy="190" rx="45" ry="12"/>
      <ellipse cx="740" cy="185" rx="30" ry="10"/>
      <ellipse cx="865" cy="170" rx="50" ry="11"/>
      <ellipse cx="835" cy="175" rx="32" ry="8"/>
    </g>
    <path d="M645,335 Q710,295 790,320 T925,310 L925,400 L645,400 Z" fill="#C9A882" opacity="0.7"/>
    <path d="M645,352 Q745,320 830,345 T925,338 L925,400 L645,400 Z" fill="#8FA382" opacity="0.85"/>
    <circle cx="675" cy="340" r="42" fill="#6F8C5E"/>
    <circle cx="705" cy="355" r="35" fill="#88A66E"/>
    <circle cx="685" cy="330" r="28" fill="#A9C282" opacity="0.7"/>
    <circle cx="905" cy="348" r="38" fill="#779464"/>
    <circle cx="885" cy="362" r="28" fill="#9BB57A"/>
    <path d="M745,215 Q750,209 755,214 Q760,209 765,215" fill="none" stroke="#8C7365" stroke-width="1.6" stroke-linecap="round"/>
    <path d="M772,205 Q776,200 780,204 Q784,200 788,205" fill="none" stroke="#8C7365" stroke-width="1.4" stroke-linecap="round"/>
  </g>

  <!-- Window Frame & Mullions -->
  <rect x="642" y="120" width="286" height="284" rx="4" fill="none" stroke="#F5E8D0" stroke-width="14"/>
  <rect x="649" y="127" width="272" height="270" fill="none" stroke="#D9C3A0" stroke-width="3"/>
  <line x1="785" y1="127" x2="785" y2="397" stroke="#F4E7CF" stroke-width="7"/>
  <line x1="785" y1="127" x2="785" y2="397" stroke="#D6C09D" stroke-width="1.5"/>
  <line x1="649" y1="262" x2="921" y2="262" stroke="#F4E7CF" stroke-width="7"/>
  <line x1="649" y1="262" x2="921" y2="262" stroke="#D6C09D" stroke-width="1.5"/>

  <!-- Sheer Linen Curtains & Wooden Curtain Rod -->
  <line x1="615" y1="106" x2="955" y2="106" stroke="#6E4726" stroke-width="6" stroke-linecap="round"/>
  <circle cx="613" cy="106" r="7" fill="#59381D"/>
  <circle cx="957" cy="106" r="7" fill="#59381D"/>
  <path d="M625,108 L672,108 Q668,200 658,265 Q670,335 660,402 L620,402 Q628,310 622,255 Q628,180 625,108 Z" fill="#FFF9EC" opacity="0.86" stroke="#E5D4B7" stroke-width="1.2"/>
  <path d="M636,110 Q642,200 632,262 Q642,330 635,400" fill="none" stroke="#E5D3B5" stroke-width="1.5"/>
  <path d="M650,110 Q655,200 646,262 Q655,330 648,400" fill="none" stroke="#E5D3B5" stroke-width="1.5"/>
  <path d="M622,262 Q642,268 659,262" fill="none" stroke="#C9A87C" stroke-width="4" stroke-linecap="round"/>
  <path d="M898,108 L945,108 Q942,180 948,255 Q942,310 950,402 L910,402 Q900,335 912,265 Q902,200 898,108 Z" fill="#FFF9EC" opacity="0.86" stroke="#E5D4B7" stroke-width="1.2"/>
  <path d="M920,110 Q914,200 924,262 Q914,330 922,400" fill="none" stroke="#E5D3B5" stroke-width="1.5"/>
  <path d="M934,110 Q928,200 938,262 Q928,330 935,400" fill="none" stroke="#E5D3B5" stroke-width="1.5"/>
  <path d="M911,262 Q928,268 948,262" fill="none" stroke="#C9A87C" stroke-width="4" stroke-linecap="round"/>

  <!-- Windowsill & Potted Morning Herbs -->
  <rect x="632" y="397" width="306" height="12" rx="3" fill="#E6C99E" stroke="#C8A87A" stroke-width="1.5"/>
  <polygon points="688,373 714,373 710,398 692,398" fill="#C86D44"/>
  <rect x="686" y="369" width="30" height="5" rx="1.5" fill="#D97C52"/>
  <g fill="#5E8C49">
    <ellipse cx="695" cy="361" rx="8" ry="6" transform="rotate(-20 695 361)"/>
    <ellipse cx="707" cy="360" rx="8" ry="6" transform="rotate(20 707 360)"/>
    <ellipse cx="701" cy="353" rx="9" ry="6"/>
    <ellipse cx="694" cy="350" rx="6" ry="4" fill="#7DAE63"/>
    <ellipse cx="708" cy="352" rx="6" ry="4" fill="#7DAE63"/>
  </g>
  <polygon points="755,375 779,375 775,398 759,398" fill="#C86D44"/>
  <rect x="753" y="371" width="28" height="5" rx="1.5" fill="#D97C52"/>
  <g stroke="#4F7942" stroke-width="2.2" stroke-linecap="round">
    <path d="M767,371 L760,343"/>
    <path d="M767,371 L767,338"/>
    <path d="M767,371 L775,345"/>
    <path d="M767,371 L754,352"/>
    <path d="M767,371 L780,353"/>
  </g>
  <polygon points="842,374 868,374 864,398 846,398" fill="#C86D44"/>
  <rect x="840" y="370" width="30" height="5" rx="1.5" fill="#D97C52"/>
  <circle cx="848" cy="362" r="8" fill="#699654"/>
  <circle cx="860" cy="361" r="9" fill="#5B8747"/>
  <circle cx="854" cy="355" r="8" fill="#7DAA65"/>
  <circle cx="851" cy="353" r="2" fill="#FFF5BA"/>
  <circle cx="861" cy="357" r="2" fill="#FFF5BA"/>

  <!-- ================= VINTAGE CREAM REFRIGERATOR (LEFT) ================= -->
  <ellipse cx="110" cy="604" rx="85" ry="14" fill="#5A3518" opacity="0.35"/>
  <rect x="28" y="168" width="160" height="432" rx="22" fill="url(#fridgeGrad)" stroke="#C9B08A" stroke-width="2"/>
  <path d="M172,168 Q188,168 188,190 L188,580 Q188,600 172,600 L166,600 L166,168 Z" fill="#D7BF9B"/>
  <line x1="32" y1="295" x2="174" y2="295" stroke="#BFA57E" stroke-width="3"/>
  <line x1="32" y1="298" x2="174" y2="298" stroke="#FFFDF7" stroke-width="1.5"/>
  <rect x="142" y="242" width="10" height="34" rx="5" fill="url(#brassGrad)" stroke="#8B6315" stroke-width="1"/>
  <rect x="142" y="325" width="10" height="52" rx="5" fill="url(#brassGrad)" stroke="#8B6315" stroke-width="1"/>
  <path d="M88,215 L112,215 L100,226 Z" fill="url(#brassGrad)"/>
  <circle cx="100" cy="215" r="4" fill="#FCE394"/>
  <rect x="55" y="335" width="42" height="50" transform="rotate(-4 76 360)" fill="#FFFDF5" stroke="#D8C7A8" stroke-width="1"/>
  <circle cx="75" cy="338" r="4" fill="#D95B43"/>
  <line x1="62" y1="350" x2="88" y2="348" stroke="#A6957B" stroke-width="1.5"/>
  <line x1="62" y1="358" x2="85" y2="356" stroke="#A6957B" stroke-width="1.5"/>
  <line x1="63" y1="366" x2="80" y2="365" stroke="#A6957B" stroke-width="1.5"/>
  <rect x="98" y="395" width="36" height="40" transform="rotate(6 116 415)" fill="#FFFFFF" stroke="#D8C7A8" stroke-width="1"/>
  <rect x="102" y="399" width="28" height="24" transform="rotate(6 116 415)" fill="#89B399"/>
  <circle cx="118" cy="396" r="3.5" fill="#E6A145"/>
  <rect x="44" y="598" width="18" height="10" rx="3" fill="#5C4938"/>
  <rect x="148" y="598" width="18" height="10" rx="3" fill="#5C4938"/>

  <!-- Wicker Basket & Trailing Ivy on Top of Fridge -->
  <rect x="48" y="136" width="54" height="32" rx="5" fill="#C68B50" stroke="#9A6530" stroke-width="1.5"/>
  <line x1="48" y1="146" x2="102" y2="146" stroke="#9A6530" stroke-width="1.5"/>
  <line x1="48" y1="156" x2="102" y2="156" stroke="#9A6530" stroke-width="1.5"/>
  <polygon points="122,135 156,135 150,168 128,168" fill="#C4673F"/>
  <rect x="119" y="130" width="40" height="7" rx="2" fill="#D67950"/>
  <g fill="#558248">
    <circle cx="130" cy="124" r="10"/>
    <circle cx="142" cy="121" r="11" fill="#689658"/>
    <circle cx="152" cy="126" r="9"/>
    <path d="M150,132 Q170,155 166,185 Q162,215 173,240" fill="none" stroke="#4D7840" stroke-width="2.5"/>
    <ellipse cx="163" cy="152" rx="7" ry="5" transform="rotate(25 163 152)" fill="#6C9B5C"/>
    <ellipse cx="171" cy="168" rx="7" ry="5" transform="rotate(-15 171 168)"/>
    <ellipse cx="162" cy="186" rx="7" ry="5" transform="rotate(20 162 186)" fill="#6C9B5C"/>
    <ellipse cx="169" cy="205" rx="6" ry="4.5" transform="rotate(-20 169 205)"/>
    <ellipse cx="165" cy="224" rx="6" ry="4" transform="rotate(15 165 224)" fill="#6C9B5C"/>
    <ellipse cx="173" cy="240" rx="5" ry="3.5"/>
  </g>

  <!-- ================= RANGE HOOD & HANGING COPPER COOKWARE ================= -->
  <polygon points="365,66 495,66 530,210 330,210" fill="#F5E3C6" stroke="#D5BC98" stroke-width="2"/>
  <rect x="322" y="206" width="216" height="22" rx="3" fill="url(#beamWood)"/>
  <rect x="330" y="198" width="200" height="8" fill="url(#copperGrad)"/>
  <line x1="350" y1="258" x2="510" y2="258" stroke="url(#brassGrad)" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="350" cy="258" r="4" fill="#9A6E18"/>
  <circle cx="510" cy="258" r="4" fill="#9A6E18"/>
  <line x1="378" y1="258" x2="378" y2="288" stroke="#7A5A2B" stroke-width="2"/>
  <circle cx="378" cy="304" r="16" fill="url(#copperGrad)" stroke="#8F3F1B" stroke-width="1.5"/>
  <circle cx="378" cy="304" r="11" fill="#DA7F4D"/>
  <line x1="418" y1="258" x2="418" y2="305" stroke="#6E5A4F" stroke-width="2.2"/>
  <rect x="411" y="305" width="14" height="17" rx="2" fill="#6E5A4F"/>
  <line x1="452" y1="258" x2="452" y2="308" stroke="url(#brassGrad)" stroke-width="2.2"/>
  <path d="M443,308 A9,9 0 0,0 461,308 Z" fill="url(#copperGrad)"/>
  <line x1="488" y1="258" x2="488" y2="274" stroke="#B58E58" stroke-width="1.8"/>
  <path d="M488,274 L480,304 M488,274 L488,308 M488,274 L496,304" stroke="#5E7B4C" stroke-width="3" stroke-linecap="round"/>

  <!-- ================= OPEN WOODEN WALL SHELVES ================= -->
  <rect x="200" y="185" width="112" height="10" rx="2" fill="url(#butcherBlock)" stroke="#8D5225" stroke-width="1"/>
  <path d="M215,195 L215,212 L228,195" fill="none" stroke="url(#brassGrad)" stroke-width="2.5"/>
  <path d="M295,195 L295,212 L282,195" fill="none" stroke="url(#brassGrad)" stroke-width="2.5"/>
  <rect x="212" y="148" width="26" height="37" rx="4" fill="#FFF8EB" stroke="#D9C7AC" stroke-width="1.2"/>
  <rect x="214" y="143" width="22" height="6" rx="2" fill="#C7834B"/>
  <rect x="217" y="160" width="16" height="10" rx="1" fill="#E8D5B7"/>
  <rect x="245" y="154" width="24" height="31" rx="4" fill="#FFF8EB" stroke="#D9C7AC" stroke-width="1.2"/>
  <rect x="247" y="149" width="20" height="6" rx="2" fill="#C7834B"/>
  <path d="M278,158 L296,158 L300,185 L274,185 Z" fill="#7D9B8C"/>
  <path d="M296,163 Q306,163 306,171 Q306,179 298,179" fill="none" stroke="#7D9B8C" stroke-width="2.5"/>

  <rect x="200" y="268" width="112" height="10" rx="2" fill="url(#butcherBlock)" stroke="#8D5225" stroke-width="1"/>
  <path d="M215,278 L215,295 L228,278" fill="none" stroke="url(#brassGrad)" stroke-width="2.5"/>
  <path d="M295,278 L295,295 L282,278" fill="none" stroke="url(#brassGrad)" stroke-width="2.5"/>
  <path d="M212,256 Q212,268 228,268 Q244,268 244,256 Z" fill="#E07A5F"/>
  <path d="M214,248 Q214,258 228,258 Q242,258 242,248 Z" fill="#F2CC8F"/>
  <path d="M216,240 Q216,249 228,249 Q240,249 240,240 Z" fill="#81B29A"/>
  <rect x="255" y="246" width="14" height="22" rx="2" fill="#E9C46A" stroke="#C9A24B" stroke-width="1"/>
  <rect x="256" y="242" width="12" height="4" rx="1" fill="#8D5225"/>
  <rect x="274" y="246" width="14" height="22" rx="2" fill="#C85A32" stroke="#A34522" stroke-width="1"/>
  <rect x="275" y="242" width="12" height="4" rx="1" fill="#8D5225"/>
  <rect x="292" y="246" width="14" height="22" rx="2" fill="#6B8E4E" stroke="#53703B" stroke-width="1"/>
  <rect x="293" y="242" width="12" height="4" rx="1" fill="#8D5225"/>

  <rect x="542" y="205" width="90" height="10" rx="2" fill="url(#butcherBlock)" stroke="#8D5225" stroke-width="1"/>
  <path d="M555,215 L555,230 L566,215" fill="none" stroke="url(#brassGrad)" stroke-width="2.5"/>
  <path d="M618,215 L618,230 L607,215" fill="none" stroke="url(#brassGrad)" stroke-width="2.5"/>
  <rect x="550" y="195" width="42" height="10" rx="1.5" fill="#C85A38"/>
  <rect x="553" y="186" width="38" height="9" rx="1.5" fill="#5E807F"/>
  <rect x="555" y="178" width="34" height="8" rx="1.5" fill="#E5A93C"/>
  <circle cx="610" cy="192" r="13" fill="#FFF5E1" stroke="#D9C3A1" stroke-width="1.2"/>
  <ellipse cx="610" cy="179" rx="7" ry="3" fill="#E27D60"/>
  <path d="M622,190 Q630,185 627,196" fill="none" stroke="#FFF5E1" stroke-width="3"/>

  <rect x="945" y="210" width="76" height="10" rx="2" fill="url(#butcherBlock)" stroke="#8D5225" stroke-width="1"/>
  <path d="M956,220 L956,235 L967,220" fill="none" stroke="url(#brassGrad)" stroke-width="2.5"/>
  <path d="M1010,220 L1010,235 L999,220" fill="none" stroke="url(#brassGrad)" stroke-width="2.5"/>
  <rect x="954" y="178" width="22" height="32" rx="3" fill="#784B2A" stroke="#E8D8BE" stroke-width="2"/>
  <rect x="956" y="172" width="18" height="6" rx="1.5" fill="#B5733D"/>
  <polygon points="986,185 1010,185 1006,210 990,210" fill="#D47448"/>
  <circle cx="992" cy="179" r="8" fill="#5D8A4E"/>
  <circle cx="1003" cy="178" r="9" fill="#73A162"/>
  <path d="M1006,185 Q1018,205 1014,235" fill="none" stroke="#537E44" stroke-width="2"/>
  <circle cx="1014" cy="202" r="5" fill="#6D9B5D"/>
  <circle cx="1016" cy="218" r="5" fill="#588449"/>
  <circle cx="1013" cy="233" r="4.5" fill="#73A162"/>

  <!-- ================= BASE CABINETS, FARMHOUSE STOVE & SINK ================= -->
  <rect x="190" y="425" width="840" height="170" fill="url(#sageCabinet)" stroke="#475B48" stroke-width="2"/>
  <rect x="194" y="576" width="832" height="22" fill="#374738"/>

  <rect x="204" y="438" width="118" height="32" rx="2" fill="url(#sageDark)" stroke="#88A189" stroke-width="1.5"/>
  <rect x="252" y="451" width="22" height="6" rx="3" fill="url(#brassGrad)"/>
  <rect x="204" y="478" width="56" height="88" rx="2" fill="url(#sageDark)" stroke="#88A189" stroke-width="1.5"/>
  <rect x="210" y="485" width="44" height="74" fill="#69826A"/>
  <circle cx="252" cy="520" r="4" fill="url(#brassGrad)"/>
  <rect x="266" y="478" width="56" height="88" rx="2" fill="url(#sageDark)" stroke="#88A189" stroke-width="1.5"/>
  <rect x="272" y="485" width="44" height="74" fill="#69826A"/>
  <circle cx="274" cy="520" r="4" fill="url(#brassGrad)"/>

  <rect x="335" y="425" width="195" height="168" rx="3" fill="#FAF0DC" stroke="#C8B290" stroke-width="2"/>
  <rect x="338" y="432" width="189" height="34" fill="#EFE0C4" stroke="#C8B290" stroke-width="1.5"/>
  <g fill="url(#brassGrad)" stroke="#875F12" stroke-width="1">
    <circle cx="362" cy="449" r="6"/>
    <circle cx="386" cy="449" r="6"/>
    <circle cx="410" cy="449" r="6"/>
    <circle cx="454" cy="449" r="6"/>
    <circle cx="478" cy="449" r="6"/>
    <circle cx="502" cy="449" r="6"/>
  </g>
  <circle cx="432" cy="449" r="9" fill="#FFFDF7" stroke="url(#brassGrad)" stroke-width="2"/>
  <line x1="432" y1="449" x2="432" y2="443" stroke="#5A4535" stroke-width="1.2"/>
  <line x1="432" y1="449" x2="437" y2="451" stroke="#5A4535" stroke-width="1.2"/>
  <rect x="350" y="474" width="165" height="96" rx="5" fill="#F4E5CA" stroke="#C2AB87" stroke-width="2"/>
  <rect x="364" y="483" width="137" height="8" rx="4" fill="url(#brassGrad)"/>
  <rect x="372" y="500" width="121" height="52" rx="6" fill="#462614" stroke="#B69E7B" stroke-width="2"/>
  <rect x="376" y="504" width="113" height="44" rx="4" fill="#E88B38" opacity="0.5"/>
  <line x1="376" y1="532" x2="489" y2="532" stroke="#7A441F" stroke-width="2"/>
  <path d="M405,532 Q432,512 460,532 Z" fill="#D48C46"/>

  <rect x="542" y="438" width="132" height="32" rx="2" fill="url(#sageDark)" stroke="#88A189" stroke-width="1.5"/>
  <rect x="597" y="451" width="22" height="6" rx="3" fill="url(#brassGrad)"/>
  <rect x="542" y="478" width="63" height="88" rx="2" fill="url(#sageDark)" stroke="#88A189" stroke-width="1.5"/>
  <rect x="548" y="485" width="51" height="74" fill="#69826A"/>
  <circle cx="597" cy="520" r="4" fill="url(#brassGrad)"/>
  <rect x="611" y="478" width="63" height="88" rx="2" fill="url(#sageDark)" stroke="#88A189" stroke-width="1.5"/>
  <rect x="617" y="485" width="51" height="74" fill="#69826A"/>
  <circle cx="619" cy="520" r="4" fill="url(#brassGrad)"/>
  <path d="M598,454 L622,454 L627,518 L594,518 Z" fill="#FFF9EB" stroke="#DECDB0" stroke-width="1"/>
  <line x1="602" y1="454" x2="600" y2="518" stroke="#C85A38" stroke-width="2.5"/>
  <line x1="618" y1="454" x2="620" y2="518" stroke="#C85A38" stroke-width="2.5"/>

  <rect x="692" y="424" width="182" height="58" rx="5" fill="#FFFDF8" stroke="#D9CBB5" stroke-width="2"/>
  <rect x="698" y="430" width="170" height="46" rx="3" fill="#F7EFE0" stroke="#E5D9C5" stroke-width="1"/>
  <rect x="692" y="488" width="88" height="78" rx="2" fill="url(#sageDark)" stroke="#88A189" stroke-width="1.5"/>
  <rect x="698" y="495" width="76" height="64" fill="#69826A"/>
  <circle cx="771" cy="526" r="4" fill="url(#brassGrad)"/>
  <rect x="786" y="488" width="88" height="78" rx="2" fill="url(#sageDark)" stroke="#88A189" stroke-width="1.5"/>
  <rect x="792" y="495" width="76" height="64" fill="#69826A"/>
  <circle cx="795" cy="526" r="4" fill="url(#brassGrad)"/>

  <rect x="886" y="438" width="130" height="38" rx="2" fill="url(#sageDark)" stroke="#88A189" stroke-width="1.5"/>
  <rect x="940" y="454" width="22" height="6" rx="3" fill="url(#brassGrad)"/>
  <rect x="886" y="482" width="130" height="40" rx="2" fill="url(#sageDark)" stroke="#88A189" stroke-width="1.5"/>
  <rect x="940" y="499" width="22" height="6" rx="3" fill="url(#brassGrad)"/>
  <rect x="886" y="528" width="130" height="38" rx="2" fill="url(#sageDark)" stroke="#88A189" stroke-width="1.5"/>
  <rect x="940" y="544" width="22" height="6" rx="3" fill="url(#brassGrad)"/>

  <rect x="186" y="414" width="506" height="14" rx="2" fill="url(#butcherBlock)" stroke="#8C5223" stroke-width="1.2"/>
  <rect x="874" y="414" width="158" height="14" rx="2" fill="url(#butcherBlock)" stroke="#8C5223" stroke-width="1.2"/>

  <path d="M783,422 L783,384 Q783,364 798,364 Q813,364 813,382 L813,392" fill="none" stroke="url(#brassGrad)" stroke-width="6" stroke-linecap="round"/>
  <rect x="777" y="416" width="12" height="8" rx="2" fill="url(#brassGrad)"/>
  <line x1="762" y1="420" x2="774" y2="412" stroke="url(#brassGrad)" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="804" y1="420" x2="792" y2="412" stroke="url(#brassGrad)" stroke-width="3.5" stroke-linecap="round"/>

  <!-- ================= COUNTERTOP ITEMS, STOVE KETTLE & STEAM ================= -->
  <rect x="210" y="346" width="46" height="68" rx="6" fill="#D49257" stroke="#A66A38" stroke-width="1.5"/>
  <circle cx="233" cy="356" r="4" fill="#F4E7D1"/>
  <rect x="266" y="378" width="32" height="36" rx="3" fill="#FFF7E5" stroke="#D5C2A5" stroke-width="1.5"/>
  <line x1="274" y1="378" x2="268" y2="352" stroke="#A36631" stroke-width="3" stroke-linecap="round"/>
  <circle cx="267" cy="350" r="6" fill="#A36631"/>
  <line x1="282" y1="378" x2="282" y2="348" stroke="#B87A44" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="290" y1="378" x2="297" y2="354" stroke="#8C999E" stroke-width="2" stroke-linecap="round"/>

  <rect x="342" y="411" width="180" height="5" rx="1" fill="#3B3532"/>
  <ellipse cx="390" cy="413" rx="18" ry="3" fill="#5EC2FF" opacity="0.85"/>
  <ellipse cx="390" cy="413" rx="10" ry="2" fill="#FFF5B8"/>

  <path d="M366,411 Q364,376 390,376 Q416,376 414,411 Z" fill="url(#copperGrad)" stroke="#8B3D19" stroke-width="1.5"/>
  <ellipse cx="390" cy="377" rx="12" ry="4" fill="#E69B6C" stroke="#8B3D19" stroke-width="1.2"/>
  <circle cx="390" cy="373" r="3.5" fill="#4A2E1B"/>
  <path d="M410,396 Q424,390 427,378" fill="none" stroke="url(#copperGrad)" stroke-width="5" stroke-linecap="round"/>
  <path d="M372,382 Q372,356 390,356 Q408,356 408,382" fill="none" stroke="#3B2516" stroke-width="3.5"/>

  <rect x="448" y="403" width="56" height="8" rx="3" fill="#2D2A29"/>
  <line x1="502" y1="406" x2="524" y2="402" stroke="#2D2A29" stroke-width="4" stroke-linecap="round"/>
  <g fill="none" stroke="#FFFDF5" stroke-width="3.5" stroke-linecap="round" opacity="0.62" filter="url(#steamBlur)">
    <path d="M429,372 Q438,352 426,332 Q415,312 430,290"/>
    <path d="M436,368 Q448,346 437,325 Q428,305 440,282"/>
    <path d="M468,396 Q460,376 472,358 Q482,340 470,322"/>
    <path d="M482,394 Q490,375 480,356"/>
  </g>

  <path d="M915,394 Q915,414 952,414 Q989,414 989,394 Z" fill="#B5713B" stroke="#8C5223" stroke-width="1.5"/>
  <circle cx="936" cy="390" r="10" fill="#E05A3F"/>
  <circle cx="952" cy="388" r="11" fill="#F4A236"/>
  <circle cx="968" cy="391" r="9.5" fill="#F2C94C"/>
  <circle cx="945" cy="380" r="9" fill="#8AB158"/>

  <!-- ================= WOVEN PENDANT LAMP ================= -->
  <circle cx="770" cy="195" r="110" fill="url(#lampGlow)"/>
  <line x1="770" y1="0" x2="770" y2="145" stroke="#4B321C" stroke-width="2.5"/>
  <path d="M722,190 Q725,142 770,142 Q815,142 818,190 Z" fill="#D89A5B" stroke="#9C6531" stroke-width="2"/>
  <path d="M733,165 Q770,170 807,165" fill="none" stroke="#A66D36" stroke-width="1.5"/>
  <path d="M726,178 Q770,184 814,178" fill="none" stroke="#A66D36" stroke-width="1.5"/>
  <ellipse cx="770" cy="192" rx="16" ry="8" fill="#FFF8D4"/>

  <!-- ================= COZY VINTAGE RUNNER RUG & SLEEPING CAT ================= -->
  <ellipse cx="520" cy="705" rx="340" ry="95" fill="url(#floorSunPatch)"/>
  <polygon points="235,638 690,638 730,742 185,742" fill="#C95F3D" stroke="#8E3B21" stroke-width="2"/>
  <polygon points="247,646 678,646 712,734 203,734" fill="#E8B878" stroke="#A64B2E" stroke-width="1.5"/>
  <polygon points="262,656 664,656 692,724 223,724" fill="#63826E"/>
  <g fill="#F6DEC0" stroke="#C95F3D" stroke-width="1.5">
    <polygon points="330,670 365,690 330,710 295,690"/>
    <polygon points="460,670 495,690 460,710 425,690"/>
    <polygon points="590,670 625,690 590,710 555,690"/>
  </g>
  <g stroke="#F2E2C8" stroke-width="2" stroke-linecap="round">
    <line x1="232" y1="642" x2="220" y2="642"/>
    <line x1="224" y1="658" x2="212" y2="658"/>
    <line x1="216" y1="674" x2="204" y2="674"/>
    <line x1="208" y1="690" x2="195" y2="690"/>
    <line x1="200" y1="706" x2="187" y2="706"/>
    <line x1="192" y1="722" x2="179" y2="722"/>
    <line x1="186" y1="738" x2="172" y2="738"/>
    <line x1="692" y1="642" x2="705" y2="642"/>
    <line x1="700" y1="660" x2="713" y2="660"/>
    <line x1="708" y1="678" x2="721" y2="678"/>
    <line x1="715" y1="696" x2="729" y2="696"/>
    <line x1="722" y1="714" x2="736" y2="714"/>
    <line x1="728" y1="732" x2="742" y2="732"/>
  </g>

  <!-- Sleeping Ginger Tabby Cat -->
  <g transform="translate(385, 692)">
    <ellipse cx="36" cy="18" rx="46" ry="20" fill="#593115" opacity="0.35"/>
    <ellipse cx="36" cy="10" rx="38" ry="22" fill="#E58B3C" stroke="#B8621B" stroke-width="1.5"/>
    <path d="M22,-8 Q28,4 22,16" fill="none" stroke="#C0641C" stroke-width="3" stroke-linecap="round"/>
    <path d="M36,-11 Q42,3 35,18" fill="none" stroke="#C0641C" stroke-width="3" stroke-linecap="round"/>
    <path d="M50,-8 Q55,4 48,16" fill="none" stroke="#C0641C" stroke-width="3" stroke-linecap="round"/>
    <path d="M68,14 Q82,24 62,29 Q42,32 24,26" fill="none" stroke="#E58B3C" stroke-width="9" stroke-linecap="round"/>
    <path d="M68,14 Q82,24 62,29" fill="none" stroke="#FFF3DF" stroke-width="4" stroke-linecap="round"/>
    <circle cx="10" cy="10" r="16" fill="#EE9648" stroke="#B8621B" stroke-width="1.2"/>
    <polygon points="-2,0 3,-12 12,-3" fill="#DF8132" stroke="#B8621B" stroke-width="1"/>
    <polygon points="10,-3 18,-13 23,-1" fill="#DF8132" stroke="#B8621B" stroke-width="1"/>
    <polygon points="1,-2 4,-9 9,-3" fill="#F5B5A2"/>
    <polygon points="13,-3 17,-9 20,-2" fill="#F5B5A2"/>
    <path d="M1,11 Q5,15 9,11" fill="none" stroke="#6B3710" stroke-width="1.6" stroke-linecap="round"/>
    <path d="M12,11 Q16,15 20,11" fill="none" stroke="#6B3710" stroke-width="1.6" stroke-linecap="round"/>
    <polygon points="9,15 12,15 10.5,17" fill="#E88073"/>
    <ellipse cx="4" cy="24" rx="7" ry="4" fill="#FFF7E8"/>
    <ellipse cx="16" cy="25" rx="7" ry="4" fill="#FFF7E8"/>
  </g>

  <!-- ================= FOREGROUND BREAKFAST TABLE & CHAIRS ================= -->
  <ellipse cx="835" cy="805" rx="275" ry="42" fill="#4F2C12" opacity="0.38"/>

  <!-- Left Wooden Windsor Chair -->
  <g stroke="#6E411F" stroke-width="2" stroke-linecap="round">
    <path d="M565,675 Q560,555 612,555 Q664,555 660,675" fill="none" stroke="#9D6234" stroke-width="8"/>
    <line x1="582" y1="572" x2="584" y2="672" stroke="#8B5429" stroke-width="3.5"/>
    <line x1="597" y1="560" x2="598" y2="672" stroke="#8B5429" stroke-width="3.5"/>
    <line x1="612" y1="556" x2="612" y2="672" stroke="#8B5429" stroke-width="3.5"/>
    <line x1="627" y1="560" x2="626" y2="672" stroke="#8B5429" stroke-width="3.5"/>
    <line x1="642" y1="572" x2="640" y2="672" stroke="#8B5429" stroke-width="3.5"/>
    <line x1="578" y1="690" x2="562" y2="818" stroke="#7A4821" stroke-width="8"/>
    <line x1="654" y1="690" x2="665" y2="818" stroke="#7A4821" stroke-width="8"/>
    <line x1="600" y1="688" x2="592" y2="795" stroke="#5E3617" stroke-width="7"/>
    <line x1="570" y1="760" x2="658" y2="760" stroke="#6E411F" stroke-width="4.5"/>
    <ellipse cx="622" cy="682" rx="64" ry="18" fill="#A96B3A" stroke="#6E411F" stroke-width="2"/>
    <ellipse cx="624" cy="675" rx="56" ry="13" fill="#FFF6E3" stroke="#D9C5A3" stroke-width="1.5"/>
  </g>

  <!-- Right Wooden Chair with Draped Knit Throw -->
  <g stroke="#6E411F" stroke-width="2" stroke-linecap="round">
    <path d="M995,680 Q992,560 1044,560 Q1096,560 1090,680" fill="none" stroke="#9D6234" stroke-width="8"/>
    <line x1="1012" y1="576" x2="1012" y2="676" stroke="#8B5429" stroke-width="3.5"/>
    <line x1="1028" y1="564" x2="1028" y2="676" stroke="#8B5429" stroke-width="3.5"/>
    <line x1="1044" y1="561" x2="1044" y2="676" stroke="#8B5429" stroke-width="3.5"/>
    <line x1="1060" y1="564" x2="1060" y2="676" stroke="#8B5429" stroke-width="3.5"/>
    <line x1="1076" y1="576" x2="1074" y2="676" stroke="#8B5429" stroke-width="3.5"/>
    <line x1="988" y1="695" x2="975" y2="822" stroke="#7A4821" stroke-width="8"/>
    <line x1="1075" y1="695" x2="1090" y2="822" stroke="#7A4821" stroke-width="8"/>
    <line x1="1050" y1="692" x2="1058" y2="798" stroke="#5E3617" stroke-width="7"/>
    <line x1="982" y1="765" x2="1082" y2="765" stroke="#6E411F" stroke-width="4.5"/>
    <ellipse cx="1028" cy="688" rx="65" ry="18" fill="#A96B3A" stroke="#6E411F" stroke-width="2"/>
    <path d="M1040,558 Q1088,560 1095,605 L1085,715 Q1070,722 1056,712 L1060,625 Q1048,595 1035,575 Z" fill="#E8A948" stroke="#B87E26" stroke-width="1.5"/>
  </g>

  <!-- Farmhouse Round Wooden Breakfast Table -->
  <rect x="814" y="670" width="36" height="125" rx="6" fill="#7D4A22" stroke="#573114" stroke-width="2"/>
  <path d="M818,775 L735,826 L755,832 L826,792 Z" fill="#6E3F1B" stroke="#4D2B10" stroke-width="1.5"/>
  <path d="M846,775 L928,826 L908,832 L838,792 Z" fill="#6E3F1B" stroke="#4D2B10" stroke-width="1.5"/>
  <path d="M832,785 L832,840 L845,840 L845,785 Z" fill="#593214"/>
  <ellipse cx="832" cy="648" rx="196" ry="64" fill="#8C5225"/>
  <ellipse cx="832" cy="640" rx="196" ry="62" fill="url(#tableTopGrad)" stroke="#7D471E" stroke-width="2"/>
  <polygon points="778,580 886,580 906,700 758,700" fill="#FFF8E8" stroke="#E0CEB0" stroke-width="1.5"/>
  <line x1="786" y1="581" x2="768" y2="699" stroke="#C86D44" stroke-width="2" opacity="0.65"/>
  <line x1="878" y1="581" x2="896" y2="699" stroke="#C86D44" stroke-width="2" opacity="0.65"/>

  <!-- ================= MORNING BREAKFAST ITEMS ON TABLE ================= -->
  <ellipse cx="832" cy="622" rx="28" ry="9" fill="#B59E7D" opacity="0.4"/>
  <path d="M812,568 L850,568 Q858,595 852,620 Q832,626 810,620 Q804,595 812,568 Z" fill="#FFFDF7" stroke="#D8C7AC" stroke-width="1.5"/>
  <path d="M850,576 Q866,576 866,592 Q866,608 852,608" fill="none" stroke="#FFFDF7" stroke-width="4"/>
  <path d="M850,576 Q866,576 866,592 Q866,608 852,608" fill="none" stroke="#D8C7AC" stroke-width="1.2"/>
  <g stroke="#4E7A43" stroke-width="2.5" stroke-linecap="round">
    <path d="M824,568 L802,522"/>
    <path d="M830,568 L828,512"/>
    <path d="M836,568 L856,520"/>
    <path d="M820,568 L792,542"/>
    <path d="M842,568 L868,540"/>
  </g>
  <g fill="#6D9B64">
    <ellipse cx="795" cy="542" rx="10" ry="6" transform="rotate(-25 795 542)"/>
    <ellipse cx="812" cy="548" rx="9" ry="6" transform="rotate(-15 812 548)"/>
    <ellipse cx="848" cy="546" rx="10" ry="6" transform="rotate(20 848 546)"/>
    <ellipse cx="868" cy="540" rx="10" ry="6" transform="rotate(30 868 540)"/>
    <ellipse cx="822" cy="534" rx="8" ry="5" fill="#82B078"/>
    <ellipse cx="838" cy="532" rx="8" ry="5" fill="#82B078"/>
  </g>
  <g>
    <circle cx="802" cy="520" r="11" fill="#FFE066"/>
    <circle cx="802" cy="520" r="5" fill="#F2994A"/>
    <circle cx="828" cy="510" r="12" fill="#FFE680"/>
    <circle cx="828" cy="510" r="5.5" fill="#F2994A"/>
    <circle cx="856" cy="518" r="11" fill="#FFD952"/>
    <circle cx="856" cy="518" r="5" fill="#F2994A"/>
    <circle cx="815" cy="528" r="9" fill="#FFF0A8"/>
    <circle cx="842" cy="527" r="9.5" fill="#FFE066"/>
  </g>

  <ellipse cx="732" cy="646" rx="46" ry="18" fill="#FFFDF8" stroke="#D5C4A8" stroke-width="1.8"/>
  <ellipse cx="732" cy="646" rx="34" ry="12" fill="#F9F1E1" stroke="#E5D7BE" stroke-width="1"/>
  <path d="M708,645 Q716,626 736,632 Q752,638 746,650 Q736,642 724,642 Q714,644 708,645 Z" fill="#DF8E3C" stroke="#A65E18" stroke-width="1.2"/>
  <path d="M718,634 Q725,640 722,644 M730,632 Q736,639 733,644" fill="none" stroke="#A65E18" stroke-width="1.2"/>
  <path d="M724,653 Q735,638 752,643 Q764,648 758,657 Q748,651 738,651 Q730,653 724,653 Z" fill="#E99D4B" stroke="#A65E18" stroke-width="1.2"/>
  <rect x="762" y="596" width="22" height="26" rx="4" fill="#C93B2B" stroke="#F5E8D3" stroke-width="1.5"/>
  <rect x="760" y="591" width="26" height="6" rx="2" fill="#E8C391" stroke="#B58D58" stroke-width="1"/>
  <rect x="765" y="604" width="16" height="10" rx="1" fill="#FFF9EC"/>

  <rect x="892" y="576" width="32" height="50" rx="4" fill="#5A3319" stroke="#D99B66" stroke-width="2"/>
  <rect x="892" y="576" width="12" height="50" fill="#FFF4DC" opacity="0.25"/>
  <path d="M890,576 L926,576 L922,568 L894,568 Z" fill="url(#copperGrad)"/>
  <line x1="908" y1="558" x2="908" y2="568" stroke="url(#brassGrad)" stroke-width="2.5"/>
  <circle cx="908" cy="557" r="4" fill="url(#brassGrad)"/>
  <path d="M924,584 Q938,584 938,600 Q938,616 924,616" fill="none" stroke="#4A2E1B" stroke-width="3.5"/>

  <ellipse cx="874" cy="656" rx="26" ry="10" fill="#FFFDF8" stroke="#D5C4A8" stroke-width="1.5"/>
  <path d="M858,630 L890,630 L887,654 Q874,658 861,654 Z" fill="#E07A5F" stroke="#B5573E" stroke-width="1.2"/>
  <ellipse cx="874" cy="630" rx="16" ry="5.5" fill="#FFF8EB" stroke="#B5573E" stroke-width="1"/>
  <ellipse cx="874" cy="630" rx="13" ry="4" fill="#5C3419"/>
  <path d="M874,632 Q870,628 872,627 Q874,627 874,629 Q874,627 876,627 Q878,628 874,632 Z" fill="#FFF3DC"/>
  <path d="M889,635 Q899,635 899,643 Q899,651 888,650" fill="none" stroke="#E07A5F" stroke-width="3"/>
  <g fill="none" stroke="#FFFDF5" stroke-width="2.5" stroke-linecap="round" opacity="0.7" filter="url(#steamBlur)">
    <path d="M870,620 Q864,606 873,594 Q880,582 872,570"/>
    <path d="M879,618 Q886,605 878,592"/>
  </g>

  <g transform="translate(788, 666) rotate(-6)">
    <path d="M0,6 Q22,0 44,6 L44,32 Q22,26 0,32 Z" fill="#FFFDF6" stroke="#C7B293" stroke-width="1.2"/>
    <path d="M44,6 Q66,0 88,6 L88,32 Q66,26 44,32 Z" fill="#FAF2E1" stroke="#C7B293" stroke-width="1.2"/>
    <line x1="44" y1="6" x2="44" y2="32" stroke="#B59F7E" stroke-width="1.5"/>
    <line x1="8" y1="12" x2="36" y2="11" stroke="#B8A68E" stroke-width="1.2"/>
    <line x1="8" y1="17" x2="36" y2="16" stroke="#B8A68E" stroke-width="1.2"/>
    <line x1="8" y1="22" x2="28" y2="21" stroke="#B8A68E" stroke-width="1.2"/>
    <line x1="52" y1="12" x2="80" y2="11" stroke="#B8A68E" stroke-width="1.2"/>
    <line x1="52" y1="17" x2="80" y2="16" stroke="#B8A68E" stroke-width="1.2"/>
    <line x1="52" y1="22" x2="74" y2="21" stroke="#B8A68E" stroke-width="1.2"/>
    <path d="M44,32 Q42,42 36,46" fill="none" stroke="#C84B31" stroke-width="2.2" stroke-linecap="round"/>
  </g>

  <!-- ================= VOLUMETRIC GOLDEN MORNING SUNBEAMS & DUST MOTES ================= -->
  <polygon points="650,128 780,128 475,785 170,785" fill="url(#sunbeam1)"/>
  <polygon points="790,128 920,128 710,825 460,825" fill="url(#sunbeam2)"/>
  <polygon points="650,268 920,268 785,840 340,840" fill="url(#sunbeam1)" opacity="0.65"/>

  <g fill="#FFFCE6">
    <circle cx="695" cy="235" r="2.2" opacity="0.8"/>
    <circle cx="742" cy="260" r="1.6" opacity="0.65"/>
    <circle cx="645" cy="310" r="2.5" opacity="0.75"/>
    <circle cx="688" cy="340" r="1.8" opacity="0.6"/>
    <circle cx="590" cy="380" r="2.2" opacity="0.8"/>
    <circle cx="635" cy="420" r="1.5" opacity="0.7"/>
    <circle cx="545" cy="455" r="2.6" opacity="0.75"/>
    <circle cx="580" cy="495" r="1.8" opacity="0.6"/>
    <circle cx="485" cy="525" r="2.2" opacity="0.85"/>
    <circle cx="520" cy="575" r="2.0" opacity="0.7"/>
    <circle cx="445" cy="615" r="2.5" opacity="0.75"/>
    <circle cx="490" cy="650" r="1.7" opacity="0.65"/>
    <circle cx="395" cy="665" r="2.3" opacity="0.8"/>
    <circle cx="670" cy="480" r="2.0" opacity="0.75"/>
    <circle cx="715" cy="535" r="2.4" opacity="0.7"/>
    <circle cx="630" cy="560" r="1.8" opacity="0.65"/>
    <circle cx="755" cy="450" r="2.1" opacity="0.8"/>
    <circle cx="815" cy="325" r="1.9" opacity="0.75"/>
  </g>
</svg>
```
