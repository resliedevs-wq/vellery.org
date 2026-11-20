Created an animated SVG of a pelican actively riding a bicycle at [pelican.svg](file:///tmp/vellery-sw7q185w/work/pelican.svg).

### What's Included
- **Pelican Rider**: Seated directly on the brown saddle with both wings gripping the handlebars, windswept crest feathers, long upper bill with hooked red nail, and an orange gular pouch that gently bobs in time with the pedal cadence.
- **Active Pedaling & Crank Motion**: Two-bone inverse-kinematics keyframes (`36` frames per `1.2s` revolution) drive both the near and far feathered thighs, orange lower legs, and webbed feet on horizontal pedals attached to rotating front and rear crank arms (`180°` out of phase), along with a rotating `24`-tooth chainring and animated chain loop.
- **Moving Wheels & Scenery**: Both `82px`-radius wheels rotate clockwise (`1.2s` per turn) with spokes, tire tread marks, valve stems, and spoke reflectors, paired with road dashes and coastal railing posts scrolling at the matching wheel-circumference speed against drifting clouds and sea sparkles.

### Verification
- Validated [pelican.svg](file:///tmp/vellery-sw7q185w/work/pelican.svg) XML structure (`viewBox="0 0 900 600"`, `24` SMIL `<animate>` / `<animateTransform>` elements).
- Rendered [pelican.svg](file:///tmp/vellery-sw7q185w/work/pelican.svg) and a `25%`-cycle (`90°`) snapshot via `rsvg-convert` to visually inspect seating posture, leg extension, crank/pedal alignment, and wheel geometry.
