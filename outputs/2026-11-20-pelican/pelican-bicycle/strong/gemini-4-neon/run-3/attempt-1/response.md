Created the animated SVG of a pelican actively riding a bicycle and saved it to [pelican.svg](file:///tmp/vellery-rp_p211q/work/pelican.svg).

### Highlights
- **Pelican seated on the saddle**: A plump white pelican with a hooked golden bill, pendulous throat pouch, S-curved neck, fluttering head crest, blinking eye, and layered wings sits solidly on the brown leather cruiser saddle while gripping the swept-back handlebars.
- **Synchronized cranks, wheels & leg kinematics**:
  - Front and rear spoked wheels (with reflectors and whitewall rims), chainring, rear cog, and chain links all rotate clockwise in a 2:1 gear ratio (`0.9s` wheel revolution, `1.8s` crank revolution).
  - Near and far crank arms rotate smoothly around the bottom bracket while both pedals counter-rotate to remain strictly horizontal.
  - Both pelican legs and webbed feet are driven by 24-step inverse kinematics (`<animate>` on path geometry) so the webbed feet stay locked to the moving pedals throughout the full pedaling cycle.
- **Coastal motion cues**: Road dashes, boardwalk railing posts, shimmering ocean waves, distant coastal hills, drifting clouds, and breeze lines scroll continuously to convey active forward riding.
