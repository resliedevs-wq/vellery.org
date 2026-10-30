Here's a pelican on a bike as an SVG. I wrote it by hand and didn't render it, so the proportions may need tweaking.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 280" width="400" height="280">
  <!-- Sky, sun, and ground -->
  <rect width="400" height="280" fill="#cfeefc"/>
  <circle cx="345" cy="45" r="22" fill="#ffeb3b"/>
  <rect y="255" width="400" height="25" fill="#7cb342"/>

  <!-- Wheels -->
  <g fill="none" stroke="#222" stroke-width="5">
    <circle cx="110" cy="210" r="50"/>
    <circle cx="290" cy="210" r="50"/>
  </g>
  <circle cx="110" cy="210" r="4" fill="#222"/>
  <circle cx="290" cy="210" r="4" fill="#222"/>

  <!-- Frame -->
  <g fill="none" stroke="#d32f2f" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
    <path d="M110 210 L190 210 L160 150 Z"/>   <!-- chainstay, seat tube, seat stay -->
    <path d="M160 150 L270 150 L290 210"/>     <!-- top tube and fork -->
    <path d="M190 210 L270 150"/>              <!-- down tube -->
    <path d="M270 150 L278 120 L292 116"/>     <!-- stem and handlebar -->
  </g>
  <path d="M150 146 L172 146" stroke="#222" stroke-width="7" stroke-linecap="round"/>  <!-- saddle -->
  <circle cx="190" cy="210" r="6" fill="#444"/>                                       <!-- bottom bracket -->

  <!-- Legs and feet -->
  <path d="M180 130 L195 200" stroke="#f08c00" stroke-width="6" stroke-linecap="round"/>
  <path d="M190 200 L210 204" stroke="#f08c00" stroke-width="5" stroke-linecap="round"/>

  <!-- Tail -->
  <path d="M130 112 L104 104 L110 122 Z" fill="#9e9e9e"/>

  <!-- Body -->
  <ellipse cx="180" cy="110" rx="55" ry="32" transform="rotate(-18 180 110)" fill="#f5f5f0" stroke="#666" stroke-width="2"/>

  <!-- Neck (outline, then fill) -->
  <path d="M215 95 Q240 80 252 62" fill="none" stroke="#666" stroke-width="26" stroke-linecap="round"/>
  <path d="M215 95 Q240 80 252 62" fill="none" stroke="#f5f5f0" stroke-width="22" stroke-linecap="round"/>

  <!-- Head -->
  <circle cx="260" cy="58" r="18" fill="#f5f5f0" stroke="#666" stroke-width="2"/>
  <circle cx="264" cy="54" r="4" fill="#111"/>
  <circle cx="265" cy="53" r="1.2" fill="#fff"/>

  <!-- Bill and pouch -->
  <path d="M270 52 L352 72 Q356 78 350 82 L284 84 Q276 80 270 70 Z" fill="#f9a825" stroke="#b26a00" stroke-width="2"/>
  <path d="M286 82 Q300 114 326 98 L348 82 Z" fill="#ffcc80" stroke="#b26a00" stroke-width="2"/>

  <!-- Wing -->
  <path d="M150 96 Q170 70 205 80 Q190 100 180 118 Q160 118 130 112 Z" fill="#37474f"/>
</svg>
```