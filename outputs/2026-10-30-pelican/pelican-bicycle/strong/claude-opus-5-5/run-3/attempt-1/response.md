I've saved the animation as `pelican.svg`, but I haven't seen it play. Every shell command failed with a sandbox error (`apply-seccomp … Permission denied`), so I couldn't check the XML or render a preview. I wrote the file by hand, and the leg positions were calculated by hand as well. Open it in a browser to check it.

**What's in it** (animated SVG, 400×300, no scripts):
- **The pelican sits on the saddle.** It has a white body with black wing-tip feathers and an S-shaped neck. Its long orange beak sticks out past the front wheel, and its throat pouch wobbles. One wing reaches forward and holds the handlebar. The head bobs in time with the pedalling.
- **Cranks and pedals** go round once per second. The chainring turns with them.
- **Legs follow the pedals.** The hip stays fixed, and the knee positions were worked out at 12 points around each pedal stroke so the feet stay on the pedals. The near and far legs are half a turn apart, and the far leg is drawn behind the frame in a darker orange.
- **Wheels** turn once every 0.75s. Orange reflectors on the spokes make the turning easy to see.
- **The background scrolls** to show forward motion: road markings and grass move at about the same speed as the wheels roll, bushes and clouds move more slowly, and a few faint speed lines appear behind the bike.

The animation uses SVG's built-in animation tags (SMIL), which current Chrome, Firefox and Safari play, including when the file is shown as an `<img>`. The knee moves in a straight line between the 12 calculated points, so if the leg motion looks slightly jerky, more points would smooth it out.