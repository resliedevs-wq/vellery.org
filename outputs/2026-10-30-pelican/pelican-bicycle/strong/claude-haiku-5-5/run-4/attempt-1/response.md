I wrote the animation to `/tmp/vellery-f0skp59c/work/pelican.svg`, but I have not rendered or validated it. The Bash tool failed with a sandbox error (`apply-seccomp ... Permission denied`), so I couldn't run a parser or open it in a browser.

What the file contains:

- **Pelican on the saddle:** white body, grey wing and tail, long S-neck, orange-yellow bill with pouch.
- **Wheels:** both rotate clockwise, so the bike reads as moving right. Spokes and a valve mark make the rotation visible. The rear sprocket turns with the rear wheel.
- **Cranks:** the chainring and two crank arms with pedals rotate once every 3 seconds. The wheels turn at 2× that rate, matching the 28/14 chainring-to-sprocket ratio.
- **Feet:** the legs are animated so each foot stays on its pedal. I computed the knee positions by hand at 30° steps, so the knee joints are approximate.
- **Motion:** the road's center dashes scroll left to suggest speed, and the upper body rocks slightly about the hip.

Open it in a browser to check it, since SMIL animation doesn't play in most static SVG previewers. If the leg or wheel motion looks wrong, tell me what you see and I'll adjust it. I can also run an XML validity check once the Bash tool works again.