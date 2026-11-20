Done — `pelican.svg` (11.8 KB, pure SMIL — no JavaScript or CSS needed, just open it in any browser).

**The scene:** a pelican perched on the saddle of a red bicycle, gripping the handlebar with its wing, big pouch beak, blinking eye, tail feathers — pedaling hard with scrolling road, drifting clouds, speed lines and a sun.

**What moves:**
- **Cranks + pedals** — rotate around the bottom bracket (1.2 s/rev); pedals stay level while orbiting, as real pedals do
- **The pelican's legs actually pedal** — I precomputed two-bone IK keyframes (hip fixed on the saddle, 105 px thigh + 105 px shin) every 30° of the pedal circle and morph the leg path through them, with the far leg 180° out of phase. Webbed feet ride the pedals via circular `animateMotion` paths
- **Wheels** — spokes, rim and rear cog spin clockwise (0.7 s/rev, geared faster than the cranks)
- **Chain** — dashes circulate between chainring and rear cog in the correct direction
- **Body bob** — the pelican bobs twice per crank revolution; road markings scroll left at wheel speed to sell the forward motion

**Verification:** I rendered frames with rsvg and pixel-audited the layout, and scripted a math audit of every keyframe — this caught one genuinely wrong knee position (θ=300°) which I fixed. Final audit passes: all 13 keyframes × 4 leg paths keep both bones exactly 105 px, every foot stays on the 45 px pedal circle, and the far leg is exactly half a revolution out of phase with the near one.

One caveat: rsvg and other static thumbnailers render SMIL at an arbitrary clock, so a static preview may show a mid-pedal pose — in a browser it animates properly from t=0.