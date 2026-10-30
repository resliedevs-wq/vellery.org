I've saved the animation as `pelican.svg`, but I couldn't view or check it. The sandbox blocked every shell command (`apply-seccomp … Permission denied`), so I couldn't run a script to generate it or render a frame to look at. I wrote the SVG by hand and worked out the leg positions myself. Open it in a browser to see whether it looks right.

**What's in it:**
- **The pelican:** it sits on the saddle and bobs slightly with each pedal stroke. It has a white body, tail feathers, an S-shaped neck, a yellow crest, a long orange bill with a hooked tip and throat pouch, and an eye that blinks. One wing reaches forward with its dark wingtip wrapped around the handlebar.
- **Pedalling:** the cranks turn once every 1.6 seconds. Both legs bend at the knee and their webbed feet stay on the pedals. The far leg is half a turn behind the near one and drawn behind the frame. I calculated the leg positions for 12 points around each crank turn, and the animation blends between them.
- **The bike:** the wheels spin once every 0.8 seconds, so they turn twice for each crank turn, like a real gear ratio. The chain and chainring move in step with the cranks.
- **The scene:** the road markings scroll past at about the speed the wheels would travel. There are also speed lines and slowly drifting hills and clouds.

It only uses SVG's built-in animation, with no JavaScript, so it should work whether you open it directly or embed it with an `<img>` tag.