The static first frame renders exactly as intended — pelican seated on the saddle, near leg reaching the forward pedal, far leg behind the frame. The animation structure is all SMIL, so here's the final result:

**Saved: `pelican.svg`** (800×500, pure SMIL — no JavaScript, works when opened in any browser)

What's animated:

- **Wheels** — both spin clockwise at 0.9 s/rev (spokes + valve dot make the rotation readable)
- **Cranks & pedals** — chainring + crank arms rotate at 1.6 s/rev; each pedal counter-rotates so it stays level while orbiting the bottom bracket
- **Legs** — both legs are two-bar IK solved at 8 keyframes per crank revolution, so the webbed feet actually track the pedals through the full stroke (near leg in front of the frame, far leg darker behind it)
- **Chain** — dashes march at chainring surface speed
- **Road** — scrolling dashes whose speed matches the tire circumference, so nothing looks like it's slipping
- **Pelican life** — body bobs with each pedal stroke, wing flutters, neck/head sways, and the scarf streams backward in the apparent wind; clouds drift past for depth

Everything is phase-locked: legs, cranks, and body bob share the same 1.6 s clock, and ground speed equals wheel surface speed (544 px/s).

Note: some image viewers (e.g. static thumbnails, macOS Quick Look) don't run SMIL — open it in Chrome/Firefox to see it ride.