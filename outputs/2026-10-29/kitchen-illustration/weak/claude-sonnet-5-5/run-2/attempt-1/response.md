I drew the kitchen as an SVG, but I couldn't render it to check how it looks. This machine has no SVG renderer (`rsvg-convert`, ImageMagick, Inkscape and `cairosvg` are all missing). Open `/tmp/vellery-o9bcjis6/work/cozy_kitchen.svg` in any browser to see it.

**What's in the picture**
- **Light:** A low sun shines through a window with a sky gradient, distant hills and soft clouds. Coral curtains frame the window. A pale golden beam spreads across the counter and floor, with a few dust motes floating in it.
- **Cabinets and shelf:** Sage-green cabinets with brass knobs. A shelf holds jars, two mugs and a small plant.
- **Lighting and walls:** A warm orange pendant lamp hangs with a soft glow. The wall is cream, with a tiled backsplash.
- **Counter:**
  - a red kettle steaming on the burner
  - a toaster
  - a mug of coffee with steam curling up
  - a fruit bowl
  - a vase of daisies
  - a potted plant
- **Floor:** Warm wood planks with a red rug. A ginger cat sleeps curled up on the rug in the sunbeam.

If the beam overlay looks off in your viewer, it's the `mix-blend-mode:screen` polygon near the end of the file. Deleting that attribute should fix it. I can also change the palette, make it a different time of day, or add things like a table with breakfast.