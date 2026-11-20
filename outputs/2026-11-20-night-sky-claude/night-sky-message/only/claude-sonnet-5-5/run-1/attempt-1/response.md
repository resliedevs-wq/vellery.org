I couldn't find a hidden message in `night-sky.png`, so I can't tell you what it says.

**What I checked**
- **Visible content:** It's an 800×500 illustration of a moon over a lake, with mountains, pines, an aurora and a shooting star. I saw no text in it.
- **File structure:** The PNG has only the standard header, image-data and end chunks. There are no text or metadata chunks, and no data appended after the end of the file.
- **Hidden bits in the pixels:** I checked the lowest two bit planes of the red, green and blue channels, alone and combined. I read them in 8 bit alignments and searched for readable ASCII. I also drew each channel's lowest bit plane as an image.
- **Result of the pixel checks:** The bit-plane images show only banding and ripple patterns from smooth gradients. The ASCII searches returned only short strings of gibberish.

**What I didn't try**
- The message could be hidden with a method that needs a password or key, such as steghide-style embedding or a keyed pixel order.
- It could also sit in the pixel data in a form I didn't test, such as a pattern in the colour values, or a message spread over bit planes above the second.
- `zsteg`, `binwalk` and `exiftool` aren't installed here, and numpy isn't either. I used Python with PIL instead.

If you know how the message was hidden, or have a hint such as a tool, password or the file's origin, I can try that next.

I deleted the temporary images I made in the working directory. The copies I wrote to the session temp folder (`$TMPDIR`) are still there, because my cleanup command was blocked.