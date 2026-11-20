Created an animated SVG of a pelican riding a bicycle at [pelican.svg](file:///tmp/vellery-8ss511g2/work/pelican.svg).

### What's Implemented
- **Pelican Rider**: Seated squarely on the bicycle saddle (`#pelican-body-group`) with a long hooked bill, bouncing gular pouch, crown tuft, fluttering tail feathers, and both wings (`#near-wing` and far wing) gripping the handlebars.
- **Pedaling Kinematics**: Two-link inverse-kinematics leg motion (`#near-leg` and `#far-leg`, 37 keyframe steps over a `1.6s` cycle) keeps both webbed feet locked onto the horizontal counter-rotating pedals throughout each revolution, paired with subtle body bobbing.
- **Moving Drivetrain & Wheels**:
  - Chainring and both crank arms (`#near-crank-system`, `#far-crank-system`) rotate continuously around the bottom bracket (`1.6s` per revolution).
  - Spoked front and rear wheels (`#front-wheel`, `#rear-wheel`) and the rear sprocket spin at a 2:1 ratio (`0.8s` per revolution), matched by animated chain links (`stroke-dashoffset`).
- **Coastal Scenery**: Scrolling road markings, boardwalk posts, ocean highlights, drifting clouds, and breeze lines reinforce forward motion.

### Verification
- Parsed [pelican.svg](file:///tmp/vellery-8ss511g2/work/pelican.svg) with Python `xml.etree.ElementTree` to verify valid XML and matching `values`/`keyTimes` counts across all 11 `<animate>` and 16 `<animateTransform>` elements.
- Rendered preview PNGs with `rsvg-convert` and visually inspected the initial frame and four-phase pedaling snapshots.
