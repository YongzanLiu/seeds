# FracQC field-monitoring showcase

This animation presents a single time-synchronized field example: vertical and
horizontal monitoring-well panels and pumping treatment on the left; fracture
half-length before fracture hit, then width and height after fracture hit on the
right. Desktop and stacked mobile layouts use the same clock and frame timeline.

## Sources and fidelity

- The three `sources/*-reference.png` images are the user's original attachments,
  retained without modification.
- [The cleaned monitoring figure](sources/monitoring-clean.png) is the built-in imagegen annotation-removal
  version explicitly selected by the user. Only its plot interiors are embedded
  in the animation. This is a cleaned visual illustration, not recovered raw
  measurements. The complete editing prompt is in
  [annotation-removal-prompt.txt](annotation-removal-prompt.txt).
- The displayed monitoring and pumping panels, their ranges, and their event
  sequence come from that selected figure. Native monitoring arrays found in an
  older local analysis were not substituted because their responses differed.
- Only the red **Liu et al.** series from the pre-hit half-length figure is used.
  Its 76-point numeric result is packaged as
  `sources/before-hit-selected-series.dat`. The original analysis timestamps are
  08:25:51–09:03:21 on 18 April 2019, every 30 seconds.
- Post-hit green and purple curves and shaded bands are digitized from the
  supplied figure. They are display approximations, not a new inversion or
  independently available numeric results. Clock positions are calibrated to the
  five visible ticks (09:31–10:51), rather than stretching the curves to an older
  numeric result file with a different displayed window. Individual raster pixels
  resolve approximately 0.0064 mm, 1.28 m and 9 seconds. Occasional line pixels
  hidden at crossings are interpolated between visible neighbours.
- The unanalysed interval from approximately 09:03 to 09:18 is compressed into
  a 600 ms eased scan, while the right panel fades from half-length to the width
  and height axes. There is no intermediate notice or pause. No parameter values
  are added in that interval; post-hit curves begin at their first source time.
  This transition does not identify an exact fracture-hit instant. The pumping
  CSV is retained as supporting source context.

## Rebuild

Requirements: Python, NumPy, Matplotlib, Pillow. Arial is used on Windows, with
DejaVu Sans as the fallback elsewhere. No simulation or external files are needed.

```sh
python prepare_data.py
python render_animation.py
python verify_animation.py
```

Use `python render_animation.py --preview` to render six representative frames;
use `--encode-only` only when all full-resolution frames already exist.
The generated `.build/` frames and `.mpl-cache/` are local intermediates.

Copy the four current `*-v2.gif` and `*-v2-poster.png` files from `output/` to
`images/software/fracqc/` in the site.
This directory belongs in `_tools/fracqc/`, so the sources and scripts can be
committed without adding them to the public website. No Git commit or push is
performed by these scripts.
