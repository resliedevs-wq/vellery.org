I wrote `pelican.svg` (800×500) to `/tmp/vellery-9pyoex4h/work/`, but I haven't rendered it or checked it for XML errors. The Bash sandbox failed to start in this session (`apply-seccomp … setgroups: Permission denied`), so I couldn't run `xmllint` or a renderer. I wrote the file directly with the Write tool. Open it in a browser to check how it looks.

**What moves** (SMIL, no JavaScript):
- **Wheels:** both spin, with spokes and a yellow valve marker so the rotation is visible. The road dashes scroll at roughly the speed of the wheel rim.
- **Cranks:** they turn once every 1.2 s. The far crank is 180° out of phase.
- **Legs:** the pelican sits on the saddle, and each leg bends at the knee as the foot follows its pedal around. I computed these joint positions by hand (inverse kinematics every 30°), and the motion is interpolated between those 12 poses.
- **Upper body:** the pelican bobs slightly with each pedal stroke, and its head sways. A tuft on its helmet flutters, and one wing reaches the handlebar.
- **Scenery:** the clouds, hills and ground scroll at different speeds, and white wind streaks fly past.

If the leg poses look wrong in a render, tell me and I'll adjust the keyframes.