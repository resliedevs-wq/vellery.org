I wrote `pelican.svg` to `/tmp/vellery-2zcdv4ul/work/`, but I haven't seen it render or checked that it parses. Every Bash call failed with `apply-seccomp: ... Permission denied`, so I couldn't run a validator or a renderer.

The file is an 800×500 SVG with SMIL animation, so it plays on its own in a browser:

- **Pelican:** sits on the saddle with its body, neck, head, and long bill with a pouch. Its head bobs and its wing flaps gently.
- **Legs:** both legs run from the hip to the pedals, with the feet following the pedal circle. I computed the leg positions by hand at 30° steps and wrote them directly into the file.
- **Cranks:** the chainring, crank arms, and pedals rotate once every 2 seconds.
- **Wheels:** spin at a 2.75:1 ratio to the cranks, with spokes and a red valve so the rotation shows.
- **Road:** dashed centre line scrolls to suggest the bike moving forward.

Once Bash works again, please open the file in a browser. Check the leg and foot positions in particular, since I couldn't confirm them visually.