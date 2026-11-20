Created the animated SVG at [pelican.svg](file:///tmp/vellery-mfqws35o/work/pelican.svg) (`800x520`, declarative SMIL animations with no external dependencies).

### What's included
- **Pelican rider**: Seated directly on the leather saddle with a subtle double-frequency pedaling bob, S-curved neck, hooked upper mandible and golden gular pouch, wind-swept head crest feathers, fluttering red scarf, and wings gripping the swept-back handlebars.
- **Active pedaling & drivetrain**:
  - 36-keyframe inverse-kinematics leg and webbed-foot paths (`1.6s` crank cycle) keeping both near and far feet planted on the tilting pedals 180° out of phase.
  - Rotating 5-arm chainring (`1.6s`), animated bicycle chain links (`stroke-dashoffset`), rotating rear cog, and spoked front and rear wheels with tread blocks, valve stems, and spoke reflectors (`0.8s` per wheel revolution, 2:1 gear ratio).
- **Coastal boardwalk scene**: Parallax drifting clouds, distant lighthouse headland, gliding seagulls, sparkling ocean waves, and scrolling boardwalk railing posts and road dashes synchronized to the wheel speed.

### Verification
- Parsed [pelican.svg](file:///tmp/vellery-mfqws35o/work/pelican.svg) with Python's `xml.etree.ElementTree` (valid XML, 45 `<animate>`/`<animateTransform>` elements, 105K).
- Rendered static frames with `rsvg-convert` across crank phases (`0°` and `90°`/`270°`) to inspect the saddle contact, leg IK, wing grips, and wheel alignment.
