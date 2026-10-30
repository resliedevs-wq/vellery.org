I've created `pelican.svg` (600×400). It animates on a loop using SVG's built-in animation, so no JavaScript is needed.

**What's in it:**
- **The pelican sits on the saddle.** Its body rests on the seat, one wing stretches forward to grip the handlebar, and its head and neck bob gently in time with the pedalling. It has a long orange bill with a pouch that wobbles slightly.
- **The cranks turn.** The chainring and both crank arms rotate once every 1.2 seconds. The pedals counter-rotate so they stay level.
- **The legs pedal.** Each orange leg has a thigh and shin with a working knee, and I calculated the knee position for every 30° of crank turn so the webbed feet stay on the pedals. The far leg is a darker shade, half a turn out of step, and drawn behind the frame.
- **The wheels spin.** Both wheels turn every 0.8 seconds, with a yellow valve on each so the rotation is easy to see. The chain moves forward along the top and back along the bottom.
- **The scene moves.** Road markings scroll at the same speed as the wheel rims, trees scroll more slowly for depth, and clouds drift past. There are also flickering speed lines.

**I haven't seen it render.** Every shell command failed because of a sandbox error, so I couldn't preview it or check it with an SVG tool. I wrote the file by hand and checked the leg positions on paper: every shin comes out at 66px to within about 0.1px.

Open it in any modern browser to watch it. The animation runs in Chrome, Firefox and Safari, but some image viewers and editors only show a still frame.