Done — `pelican.svg` is saved in `/tmp/vellery-b176t_ui/work/` (14 KB, pure SVG + SMIL, no JavaScript). Open it in any browser to see the animation.

**What's animated:**
- **Wheels** — spokes, valves, and reflectors rotate (1.07 s/rev, geared ~2.25:1 vs. the cranks)
- **Cranks & pedals** — both crank arms rotate around the bottom bracket every 2.4 s, while each pedal counter-rotates so it stays level
- **Legs** — the pelican's near and far legs are solved with two-bone IK sampled at 16 keyframes, so the feet stay locked on the pedals through the full stroke (opposite phases); webbed feet ride the pedals
- **Rider life** — body bobs, head nods with effort, pouch pants, tail feathers wiggle, wing stays planted on the handlebar
- **Scene** — chain links run (dash-offset timed to crank speed), road center-line dashes stream by, speed streaks flicker, clouds drift

**Character details:** the pelican sits on the saddle leaning forward, wears a red helmet matching the frame, and has the obligatory oversized pouch beak and a determined brow.

Also in the work folder: `gen_pelican.py` (the generator that computes the leg IK keyframes — rerun it to tweak geometry/timing) and `preview.png` (a static first-frame render). Note that SMIL animations show in browsers but not in static image viewers, which will only display frame one.