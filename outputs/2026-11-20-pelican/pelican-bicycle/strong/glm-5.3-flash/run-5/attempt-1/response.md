The wing now looks like a proper tapered wing with feather scallops, and the scene reads well. `pelican.svg` is complete and verified (valid XML, renders cleanly — preview at `pelican-preview.png` is the static first frame).

**What's animated** (all native SMIL, no scripts — works in any modern browser):

- **Wheels** — spokes spin at 0.8 s/rev, rolling speed matched to the road
- **Cranks & pedals** — both crank arms rotate (1.6 s/rev, 180° out of phase) around the bottom bracket; each pedal counter-rotates so it stays level, with webbed pelican feet riding on them
- **Legs** — genuinely pedaling: hip fixed on the saddle, knee positions computed with two-bone IK at 8 crank phases per revolution, synced exactly to the crank cycle
- **Chain** — top and bottom runs scroll in opposite directions, as a real chain circulates
- **Pelican life** — body bobs and rocks with each pedal stroke, wing bounces on the handlebar grip, throat pouch jiggles, eye blinks every ~5 s
- **Environment** — road dashes, grass tufts and pebbles scroll past at wheel speed, speed lines stream by, clouds drift (parallax), sun rays slowly rotate

Open it in a browser (e.g. `firefox pelican.svg` or embed via `<img src="pelican.svg">`) to see it ride.