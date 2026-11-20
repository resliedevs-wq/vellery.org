Everything verifies. The animation is complete and saved at `/tmp/vellery-2drbrqrb/work/pelican.svg`.

**What's in it** — a cartoon pelican on a red road bike, built entirely with SMIL animations (no CSS/JS needed, works in any modern browser):

- **Pelican** — white body with folded wing, long neck, big beak with the signature orange gular pouch, sitting on the saddle with one wing resting on the handlebar. The body bobs gently in rhythm with the pedal strokes, and both orange legs pump up and down with feet on the pedals (near leg in front of the frame, far leg behind it).
- **Crankset** — chainring and both crank arms rotate once per second; each pedal counter-rotates so it stays level, just like a real bike.
- **Legs** — keyframed bézier paths whose endpoints I verified to lie on the pedal circle (max deviation 0.57px) and whose keyframe spacing exactly matches the crank's linear rotation, so the feet stay glued to the pedals through the whole cycle.
- **Wheels** — spoked wheels spinning at a ground speed consistent with the scrolling road dashes (~910 px/s).
- **Chain** — dashed top and bottom runs animating in opposite directions, matching the chainring's rotation.
- **Scenery** — gradient sky, glowing sun, seamlessly looping drifting clouds, ground shadow, and speed lines streaking behind the pelican.

Open the file in a browser to see it move. XML validity, layer ordering, and pixel-level placement (tires, frame, saddle, beak, pouch, chain, legs, pedals) were all verified via rendered-frame probes.