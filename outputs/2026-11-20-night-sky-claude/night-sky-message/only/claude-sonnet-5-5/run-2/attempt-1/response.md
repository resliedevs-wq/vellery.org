I couldn't find a hidden message in `night-sky.png`, so I can't tell you what it says.

What I checked:
- **Visible content:** The image shows a moonlit lake, mountains, pine trees, an aurora and a shooting star. I saw no text and no obvious hidden figure.
- **File structure:** It's a plain 800×500 RGB PNG. It has only the standard header, image data and end chunks, with no text or metadata chunks and no data appended after the end.
- **LSB steganography:** I pulled out the least-significant bits of the red, green and blue channels, alone and together. They don't decode to readable bytes. When I rendered them as images, they showed only the gradient banding you'd expect from smooth sky and water. I zoomed in on a noisy patch in the aurora and it was the same banding.

I haven't ruled out other methods. These are the ones I haven't tried:
- Higher bit planes, or a different pixel order such as column-major or per-channel interleaving.
- A password-protected tool such as `steghide` or `outguess`. Neither is installed here.
- Subtle colour differences, for example pixels off by 1–2 levels, that a contrast stretch would reveal.
- A message in the image's visual content, such as the star positions or the ripples under the moon.

Tell me if you have a hint, such as the method, a password or where the image came from, and I'll try those next. I deleted my scratch files, so the working directory is as I found it.