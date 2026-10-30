Here's a pelican riding a bike, as an SVG you can paste into a `.svg` file or open in a browser:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 290" width="400" height="290">
  <!-- sky and ground -->
  <rect width="400" height="290" fill="#cfe9ff"/>
  <line x1="0" y1="268" x2="400" y2="268" stroke="#6a8f4e" stroke-width="6"/>

  <!-- wheels -->
  <circle cx="100" cy="215" r="50" fill="none" stroke="#222" stroke-width="7"/>
  <circle cx="300" cy="215" r="50" fill="none" stroke="#222" stroke-width="7"/>
  <circle cx="100" cy="215" r="5" fill="#222"/>
  <circle cx="300" cy="215" r="5" fill="#222"/>

  <!-- bike frame, fork, handlebar -->
  <g stroke="#d1443c" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M100 215 L190 215 L265 130 L150 130 Z"/>
    <path d="M190 215 L150 130"/>
    <path d="M265 130 L300 215"/>
    <path d="M265 130 L272 112 L286 112"/>
  </g>

  <!-- crank and pedal -->
  <circle cx="190" cy="215" r="9" fill="#222"/>
  <line x1="190" y1="215" x2="202" y2="230" stroke="#222" stroke-width="5" stroke-linecap="round"/>

  <!-- seat -->
  <rect x="132" y="120" width="30" height="8" rx="4" fill="#222"/>

  <!-- legs -->
  <path d="M168 112 L186 205" stroke="#f0a030" stroke-width="5" stroke-linecap="round"/>

  <!-- tail -->
  <path d="M118 84 L92 74 L100 96 Z" fill="#ddd" stroke="#333" stroke-width="2"/>

  <!-- body -->
  <ellipse cx="172" cy="92" rx="55" ry="26" transform="rotate(-18 172 92)" fill="#fff" stroke="#333" stroke-width="2"/>

  <!-- wing -->
  <path d="M125 90 Q160 52 205 78 Q170 92 125 98 Z" fill="#999" stroke="#333" stroke-width="2"/>

  <!-- neck (outline, then white fill) -->
  <path d="M205 80 Q225 70 228 56" stroke="#333" stroke-width="26" stroke-linecap="round" fill="none"/>
  <path d="M205 80 Q225 70 228 56" stroke="#fff" stroke-width="22" stroke-linecap="round" fill="none"/>

  <!-- head -->
  <circle cx="232" cy="50" r="17" fill="#fff" stroke="#333" stroke-width="2"/>
  <circle cx="236" cy="45" r="3.5" fill="#222"/>

  <!-- beak and pouch -->
  <path d="M244 44 L300 62 L296 70 L244 56 Z" fill="#f0a030" stroke="#333" stroke-width="2"/>
  <path d="M244 56 Q268 100 296 70 L290 68 Q268 86 244 56 Z" fill="#f7c06a" stroke="#333" stroke-width="2"/>
</svg>
```