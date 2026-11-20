Done — `pelican.svg` is saved at `/tmp/vellery-munnzlng/work/pelican.svg` (17.8 KB, pure SVG + SMIL, no scripts or external assets).

**What's in the scene**
- A helmeted pelican perched on the saddle — plump body, big orange beak with pouch, and one wing stretched forward gripping the handlebar
- A red diamond-frame bicycle with chainring, chain, saddle, and swept-back handlebars, on a scrolling road with drifting clouds, wind streaks, and a sun

**The animations** (all `repeatCount="indefinite"`)
- **Wheels** spin (spokes + a red rim marker rotate, 360°/1.4s), speed-matched to the scrolling road dashes
- **Crank arms + pedals** rotate around the bottom bracket (1.6s/rev); each pedal counter-rotates so it stays level
- **Legs actually pedal** — this was the fun part: I solved two-segment inverse kinematics (thigh + shin, knees bending forward) so each foot tracks its pedal around the crank circle, sampled every 22.5° into 17-keyframe `<animate attributeName="d">` morphs (near leg in front of the frame, far leg behind it, 180° out of phase)
- **Chain** dashes move, the pelican's body **bobs and sways** with the pedal effort, the **beak chatters** slightly, and clouds/wind streaks drift past

**Verification** — I rendered it with `rsvg-convert` and pixel-probed the result: all shapes are where they should be (wheels, beak, helmet, saddle visible under the pelican, legs stroked orange over the cranks), XML validates, and every animation element checks out (10 `<animate>` + 11 `<animateTransform>`, all keyframe lists consistent).

Note: the animation uses SMIL, so open the file in a browser (Chrome/Firefox/Safari) to see it move — static image viewers will only show frame 0. The generator `make_pelican.py` sits next to it if you'd like tweaks — geometry (crank radius, leg lengths, speeds) is parameterized at the top.