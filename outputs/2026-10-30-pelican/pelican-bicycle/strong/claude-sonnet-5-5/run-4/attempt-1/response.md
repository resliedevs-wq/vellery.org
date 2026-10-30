I wrote `pelican.svg` in the working directory, but I haven't rendered or opened it. The shell sandbox failed on every command (`apply-seccomp … Permission denied`), so I couldn't run a generator script or a renderer. I wrote the SVG by hand instead, with the leg positions worked out by hand. Open it in a browser to check how it looks.

**What moves** (all native SVG animation, with no scripts or external files):
- **Pedalling:** Both cranks go round once every 1.2 s, with the two cranks opposite each other.
- **Legs:** Each leg is a thigh and shin joined at the knee. They follow the pedals, so the knees flex and the feet stay on the pedals. I worked the knee positions out by hand at 12 points around the pedal circle and the browser interpolates between them.
- **Wheels:** Both wheels spin in step with the pedalling. A red marker on each rim makes the rotation easy to see.
- **Scenery:** The road dashes slide backwards at about the wheel's rolling speed, and the clouds drift past.
- **Pelican:** It sits on the saddle with its wing on the handlebar. The body bobs gently, and the long bill and pouch are drawn at the front.

The knee positions and the pedal-to-ground clearance come from hand arithmetic. The feet may not sit perfectly on the pedals at every point in the cycle.