Created the animated SVG [pelican.svg](file:///tmp/vellery-ugt8ddk9/work/pelican.svg) depicting a pelican riding a bicycle along a coastal boardwalk.

### Highlights
- **Pelican & Pose**: The pelican sits firmly on the leather saddle with its wings gripping the handlebars, an expressive eye, crest feathers, and its iconic long hooked beak and gular pouch.
- **Synchronized Pedaling & Drivetrain**:
  - **Cranks & Chainring** rotate clockwise on a `2.0s` loop, driving the **rear cog**, **animated chain**, and **front/rear spoked wheels** (`1.0s` loop, 2:1 gear ratio).
  - **Inverse-Kinematic Legs**: Both near and far legs (180° out of phase) follow 36 keyframed positions per revolution so the webbed feet stay planted on the horizontal pedals while the knees bend naturally around the frame.
  - **Secondary Motion & Parallax**: Subtle body bob, head nod, gular pouch bounce, wind speed lines, drifting clouds/sailboats, boardwalk railing (`2.0s`), and road stripes locked 1:1 to the wheel circumference (`427.26px` per `1.0s`).
- **Verification**: Validated XML well-formedness via Python `xml.etree.ElementTree` and inspected PNG renders generated with `rsvg-convert` across `0°`, `90°`, and `270°` crank poses.
