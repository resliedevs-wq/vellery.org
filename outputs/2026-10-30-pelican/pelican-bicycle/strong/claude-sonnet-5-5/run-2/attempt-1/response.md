I saved the animation to `/tmp/vellery-q83fja60/work/pelican.svg`, but I haven't seen it rendered. Bash failed in this session with a sandbox error (`apply-seccomp … setgroups`). That meant I couldn't run a script or render a preview. I wrote the SVG by hand and calculated the leg keyframes manually. Open it in a browser to check it. Some proportions, such as the wing reaching the handlebar or the knee clearance, may need small tweaks.

- **Pelican:** it sits on the saddle, with a white body, tail, a long neck that bobs slightly, and an orange bill with a pouch. One wing reaches the handlebar.
- **Legs and cranks:** both legs and both crank arms move through 12 keyframes per turn, one turn every 1.2 seconds. The legs are half a turn out of phase, and each leg bends so its foot stays on the pedal. The chainring turns with the cranks.
- **Wheels:** both wheels spin once every 0.6 seconds. A red and a yellow dot on each wheel make the spin visible.
- **Scenery:** the road dashes scroll to match the wheel speed. Clouds drift across the sky and speed lines streak past.

The animation uses only SVG's built-in timing (SMIL), so it needs no scripts or CSS.