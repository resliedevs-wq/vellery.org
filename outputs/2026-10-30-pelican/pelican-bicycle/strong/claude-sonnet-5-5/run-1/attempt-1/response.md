I wrote `pelican.svg` in the working directory, but I haven't rendered or opened it. Every Bash call failed with a sandbox error (`apply-seccomp … Permission denied`). That means I couldn't render it to check how it looks, and I couldn't run a script to generate the animation. I worked out the leg keyframes by hand and wrote the file directly instead. Please open it in a browser and check it.

**The scene** (800×500, pure SVG with SMIL animation, no scripts):
- **Pelican:** It sits on the saddle with a white body, an S-curved neck, and a big orange bill with a pouch. One wing grips the handlebar, and the head bobs twice per pedal revolution.
- **Legs:** Each leg has a hip, a knee and a foot, and the foot follows the pedal around the crank circle. I worked out 12 knee positions per revolution so the knees bend plausibly. The far leg runs half a turn out of phase and is drawn behind the frame.
- **Bicycle:** The frame is red. The wheel spokes spin, the cranks and pedals turn, and the chainring turns too.
- **Background:** The road dashes scroll left at the same speed the wheels turn, so the bike appears to roll forward. Clouds drift across the sky.

Everything loops every 1.2 seconds. The 12-frame legs are slightly angular where the keyframes are interpolated, which I'd expect to be barely visible at this size.