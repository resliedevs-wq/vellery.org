I've created `pelican.svg`, an animated scene of a pelican riding a bicycle that loops forever. I couldn't look at it: every shell command failed with a sandbox error, so I couldn't render a frame or check the file. I worked out the leg positions by hand instead, so it needs a quick look in a browser.

**What it shows:**
- **The rider:** a white pelican sits on the saddle with one wing on the handlebar. It has the big orange beak and pouch, a small yellow crest, and an eye that blinks now and then. Its head and neck bob gently.
- **The pedalling:** the cranks and chainring turn once a second, and the pedals stay level as they go round. Each orange webbed foot stays on its pedal, and the far leg is half a turn behind the near one.
- **The wheels:** both wheels spin clockwise, the way they would going forward. The spokes, tread marks and a red reflector make the spin easy to see, and the chain runs around the chainring and rear sprocket.
- **The sense of speed:** the road markings scroll past at about the speed the wheels would move the bike, and there are speed lines behind the bird and clouds drifting across a sky with a sun.

**How the legs work:** a pure SVG file can't work out on the fly where a knee should bend to keep a foot on a turning pedal. So I calculated the hip, knee and foot positions for 12 points around each turn and the file moves smoothly between them. The foot should stay within about 1 pixel of the pedal.

The file uses only SVG's built-in animation, with no scripts. It should play in any modern browser, whether opened directly or used as an `<img>`.