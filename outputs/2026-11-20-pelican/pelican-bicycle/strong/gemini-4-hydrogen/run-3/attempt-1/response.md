Created the animated SVG at [pelican.svg](file:///tmp/vellery-m8t4scpu/work/pelican.svg).

### Implemented Details
- **Pelican on the saddle**: Seated torso resting on the leather saddle with subtle pedaling cadence bobbing, tail feather flutter, periodic eye blink, gular pouch & hooked bill, and both wings gripping the swept-back handlebars.
- **Active pedaling & IK legs**: Both cranks, the chainring, rear cog, and chain animate in a `1.6s` pedaling cycle (`2:1` gear ratio with the wheels), with both horizontal pedals and 36-frame inverse-kinematics pelican legs/webbed feet staying locked onto the moving pedals.
- **Moving wheels & coastal scenery**: Front and rear spoked wheels (`0.8s` per revolution) with tire tread marks, valve stems, and spoke reflectors, synced with scrolling road dashes, boardwalk posts, drifting clouds, and a distant sailboat.

### Verification
- Parsed [pelican.svg](file:///tmp/vellery-m8t4scpu/work/pelican.svg) with Python's `xml.etree.ElementTree` (`XML valid`).
- Rendered via `rsvg-convert` (`pelican_final.png` at `t=0`, plus mid-stroke frame inspection prior to the final far-pedal layer-order tweak) to verify composition and mechanical alignment.
