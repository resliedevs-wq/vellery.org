I wrote `pelican.svg` to the working directory (`/tmp/vellery-9c08vty7/work/pelican.svg`). I have not rendered it or checked that it parses, because every shell command in this session failed with a sandbox error (`apply-seccomp ... Permission denied`). Open it in a browser to see the animation.

What's in the file (800×500):

- **Pelican:** sits on the saddle, with a long bill and pouch, neck, folded wing, and a wing-arm on the handlebar. Its wing flaps gently.
- **Bicycle:** red frame, chainring and crank arms, and a chain. Both wheels have spokes that turn clockwise, so the bike moves right.
- **Cranks and pedals:** the crank arms rotate once every 1.6 s. Each foot is on a pedal and follows it around the circle. The legs bend with the knees forward.
- **Motion cues:** the road dashes scroll left at the wheels' rolling speed, and the clouds drift slowly left as a background.

The animation is SMIL, so it runs when the SVG is opened directly in a browser. It won't run in an image viewer that ignores SMIL.

The leg and pedal keyframes were calculated by hand, not by a script, so the feet may be off the pedals by a few pixels. If the shell comes back, I can render frames and check that and the XML. I haven't committed anything.