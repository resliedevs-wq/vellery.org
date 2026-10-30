I created `pelican.svg` in the working directory. It's a 800×500 animated SVG that loops every 2.1 seconds:

- **Wheels:** both spin clockwise, one turn every 0.75 s. A red dot on each rim makes the rotation visible.
- **Cranks and chainring:** turn once per 2.1 s. The wheels turn 2.8 times per crank turn, which matches a typical gear ratio.
- **Pelican:** sits on the saddle with its legs pedaling. Each foot follows its pedal, and the legs bend at the knee as they move. The wing flaps gently.
- **Bike:** a red diamond frame with a chain, handlebars, and a saddle. The bike stays in place; only the wheels and cranks move.

I couldn't check the result visually or with an XML parser. The sandbox blocked every shell command, so I verified the file by reading it. The leg positions were computed by hand at 30° steps, so the pedaling motion may look a little rough. Open the file in a browser to check it. If the legs look off, I can recompute the keyframes at finer steps.