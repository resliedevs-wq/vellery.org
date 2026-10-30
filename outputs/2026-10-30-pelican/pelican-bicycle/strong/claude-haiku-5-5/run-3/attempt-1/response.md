I wrote the animation to `/tmp/vellery-wrr7ewxh/work/pelican.svg` (480×300). I could not render or validate it: every Bash call failed with `apply-seccomp ... Permission denied`, so I wrote the file by hand and have not seen it run.

What's in it:
- **Pelican:** white body with a folded gray wing, S-curved neck, and a long orange bill with pouch. It sits on the saddle with its hip on the seat.
- **Pedaling:** the leg is a hip–knee–ankle path that is animated through eight crank positions (every 45°). I solved the joint positions by hand, so the knee and foot may be a few pixels off the pedal at mid-stroke.
- **Bike:** both wheels spin, with spokes and a red valve marker so the rotation shows. The chainring has dashed teeth, and the near and far cranks turn with it.
- **Motion:** the wheels turn every 0.8 s and the cranks every 1.6 s, so the gear ratio is 2:1. The road markings scroll at the speed the wheels roll, the speed lines flicker, and the pelican's upper body bobs slightly.

Once Bash works again, open the file in a browser or run it through an SVG renderer to confirm the leg tracks the pedal and nothing looks broken.