Done — saved as `/tmp/vellery-x_scpy1w/work/pelican.svg` (11 KB, self-contained, no scripts or external assets).

**The scene:** A cartoon pelican in a forward-lean riding posture, perched on the saddle of a teal bicycle, wing stretched out to the handlebar grip, webbed feet on the pedals — all in a sunny beach setting with speed lines and a scrolling road.

**Everything that moves (pure SMIL, loops seamlessly):**
- **Wheels** — spokes and valve stems rotate (0.9 s/rev)
- **Cranks & pedals** — chainring spins at 1.2 s/rev; pedal platforms counter-rotate so they stay level through the stroke
- **Legs** — both legs are keyframed along the pedal circle (8 poses/rev), the far leg 180° out of phase, so the feet stay locked to the pedals
- **Chain** — dash-offset animation makes the top run flow forward, bottom run backward
- **Body & head** — a subtle bob synced to the pedal strokes, head slightly out of phase
- **Road + wind dashes** — scrolling to sell the motion

**Notes on viewing:** Open it in any browser (Chrome, Firefox, Safari) — SMIL animations run automatically with no JavaScript. Static image viewers and some editors (like librsvg-based previews) will show only frame one. I rendered a static PNG preview at `/tmp/vellery-x_scpy1w/render/pelican2.png` to verify the composition, which is what's shown above.