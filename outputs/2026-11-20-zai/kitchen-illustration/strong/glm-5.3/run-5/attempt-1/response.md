Done — `kitchen.svg` is saved at `/tmp/vellery-nt9ll05d/work/kitchen.svg` (900×700).

**What's in the scene:**
- **Table** — small kitchen table, front view: wood-tone slab top, two front legs, back legs and a stretcher visible behind, shadow on the floor
- **Three red apples** — a pyramid of two nestled plus one on top, each with stem, leaf, and a left-side highlight (exactly three)
- **Blue mug** — muted steel-blue with handle, steam curls, and "MONDAY" printed across the body
- **Folded newspaper** — stacked sheets with fold crease and headline/column lines
- **Gray cat** — curled up asleep on the newspaper: closed eye, tucked paw, tabby stripes, tail draping over the paper's edge
- **Morning light** — window on the left with a low sun, three soft light rays slanting down-right, a warm pool on the tabletop, dust motes, and all shadows cast to the right of the objects
- Warm, muted palette (creams, tans, dusty red/blue/gray); no people

One note on verification: the Bash tool isn't usable in this session ("no permission client configured"), so I couldn't run an XML validator or renderer. I did a full manual pass over the file instead, which caught a real bug — the three apples used `r=` on `<ellipse>` (which would have rendered them invisibly) — and that's now fixed. All elements are well-formed, quoted, and closed, so it should open cleanly in any browser or vector editor.