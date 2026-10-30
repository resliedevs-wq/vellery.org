I saved the animation as `/tmp/vellery-_1fti9sj/work/pelican.svg`, but I couldn't render or open it. Every Bash command failed in this session with a sandbox error (`apply-seccomp … nested userns is capability-restricted`). I wrote the SVG by hand and checked its coordinates by calculation only. I haven't seen it play, so the layout may need small tweaks. Open it in a browser to check.

What's in it:
- **Pelican on the saddle:** it has a white body, a grey folded wing and a long S-curved neck. It has a big orange bill with a yellow pouch, and its wing reaches the handlebar. The head bobs slightly, and the body bobs with each pedal stroke.
- **Cranks and wheels:** the cranks turn once every 1.2 s, and the pedals counter-rotate so they stay flat. Both wheels spin once every 0.6 s, with spokes and a yellow marker on each rim.
- **Legs:** both legs are animated from 12 keyframes. I worked out the knee positions by hand so each foot follows its pedal. The far leg runs half a turn behind and is drawn darker.
- **Motion cues:** the road dashes, trees, hills and clouds scroll at different speeds, and speed lines fade out behind the pelican.

I'd check first that the knees clear the body and that the foot stays on the pedal through the whole stroke. If either looks off, tell me and I'll adjust the keyframes.