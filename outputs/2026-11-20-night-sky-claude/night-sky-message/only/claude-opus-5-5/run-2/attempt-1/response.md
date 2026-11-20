I couldn't find a hidden message in `night-sky.png`. The image is an 800×500 night scene with a moon, mountains, a lake and pine trees, and none of the usual hiding places held anything.

**What I checked:**
- **File structure:** The PNG has only image-data chunks plus its required header and end marker. There's no text, EXIF or comment metadata, and nothing is appended after the end of the image.
- **Compressed pixel data:** It unpacks to exactly the expected 800×500 RGB size, with no leftover bytes. Every row uses the same standard encoding setting, so nothing is hidden there either.
- **Least-significant-bit hiding:** I tried the lowest three bits of each colour channel and of all three combined, read row by row and column by column, in both bit orders. Nothing readable came out; the low bits just follow the colour gradients and dithering.
- **Faint visual text:** I boosted contrast and amplified small local differences across the whole image and in zoomed sections. They show only the scene's own edges and gradient banding, with no faint letters or shapes.
- **Shapes in the scene:** The moon's reflection lines and the water streaks taper smoothly and don't look like Morse code or any other pattern.

**What it could still be:**
- A tool that needs a password, like steghide or OpenStego. These generally can't be read without the key, and no such tools are installed here.
- A message hidden in the scene itself, such as star positions forming a shape, which this kind of analysis wouldn't decode.
- No message at all, or the wrong copy of the file.

If you know which tool or method was used, or have a password, tell me and I'll try again with that.

I put a few temporary analysis images in the project folder to look at them, and deleted them afterwards. Nothing else in the directory changed.