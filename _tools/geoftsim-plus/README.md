# GeoFTSim+ UPC reservoir showcase

This standalone scientific illustration supports the GeoFTSim+ software card.
It is generated with a small, reproducible pressure-diffusion solver and standard
plotting tools. It is **not output from GeoFTSim+**, a field history match, or a
multiphase/geomechanical validation of that code.

## Model

The reservoir is 1,200 × 600 × 200 m, discretized into 120 × 60 × 10 cells. Static,
vertical, piecewise planar fractures form U, P and C in plan view. Their finite
grid representation is an equivalent high-permeability zone, not a resolved
physical aperture. Three prescribed-pressure completions begin production on
days 0, 20 and 40, respectively, which makes the letters emerge progressively.

The single-phase, constant-property equation is

`S dp/dt = div((k / mu) grad(p))`.

Initial pressure is 30 MPa, producing completions maintain 10 MPa, and all six
outer boundaries are closed. Matrix permeability is 1e-17 m²; equivalent fracture
zone permeability is 1e-14 m². Effective bulk storage is 1.2e-10 Pa⁻¹ and viscosity
is 2e-3 Pa·s. Gravity, thermal effects, fracture propagation, fluid phase behavior,
and mechanical deformation are omitted from this showcase.

Backward Euler integration and harmonic face conductivities give a conservative
three-dimensional finite-volume calculation. Linear solves, monotonic pressure
decline, pressure bounds, an analytical homogeneous benchmark, and a storage/
production volume balance are checked in `model/model-verification.json`.

## Display

- A fixed orthographic camera shows a reservoir cutaway. The exposed section is
  at z=140 m, with fracture panels visible above it up to z=200 m.
- Pressure uses one fixed **10–30 MPa** `turbo` color scale. Matrix-face colors are
  linearly sampled from the saved 3D pressure field. The finer display surface
  does not imply a finer numerical solution.
- Panel opacity follows drawdown, solely to make the static fractures emerge
  from the initially uniform reservoir. No fracture growth is implied.
- The 121 frames show days 0–120. The first and final frames hold briefly for a
  clean loop; the final frame is also the reduced-motion poster.

## Rebuild

Requirements: Python, NumPy, SciPy, Matplotlib, Pillow. The renderer uses Arial on
Windows and falls back to DejaVu Sans elsewhere. No external input files or
network connections are required.

```sh
python pressure_model.py
python render_animation.py
python verify_animation.py
```

`python render_animation.py --preview` renders representative frames.
`--encode-only` is appropriate only after all current PNG frames exist.

The model and reports stay in this directory under `_tools/geoftsim-plus/`.
Copy `output/geoftsim-upc-pressure-depletion-v2.gif` and the matching poster to
`images/software/geoftsim-plus/` for the website. Jekyll does not publish this
underscore-prefixed source directory. Generated frames, font caches and duplicate
media outputs are ignored by Git; model arrays and verification reports remain
eligible for a commit.
