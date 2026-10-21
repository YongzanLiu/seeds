"""Prepare the portable FracQC plot dataset from packaged source materials.

No inversion is run and no monitoring pixels are inpainted by this script.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import shutil
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'sources'
SOURCE.mkdir(exist_ok=True)


def minute(iso):
    dt = datetime.fromisoformat(iso)
    return dt.hour * 60 + dt.minute + dt.second / 60 + dt.microsecond / 60e6


# Keep the clock convention of the original analysis notebooks (whole seconds).
h_start = 8*60 + 17 + 51/60
pump = []
with (SOURCE / 'pumping-stage19.csv').open(encoding='utf-8-sig') as f:
    for row in csv.reader(f):
        if not row or row[0].startswith('#'):
            continue
        dt = datetime.strptime(row[0].strip(), '%d/%b/%Y %H:%M:%S+0000')
        pump.append([dt.hour*60+dt.minute+dt.second/60, float(row[1]), float(row[2])])
pump = np.array(pump)[::3]

# The selected red reference series matches this 76-point, 30-second result.
pre = np.loadtxt(SOURCE / 'before-hit-selected-series.dat')
pre_t = h_start + 8 + np.arange(len(pre))*0.5

# Extract the displayed post-hit curves and shaded intervals from the user's
# figure rather than substituting a different inversion model. The 58 time
# samples and clock endpoints are checked against the matching numeric H-well file.
im = np.asarray(Image.open(SOURCE / 'after-hit-reference.png').convert('RGB')).astype(int)
# Read clock positions from the supplied plot, independently of the old NPY
# result timestamps. Its displayed window is shorter than that NPY file.
clock_tick_x = np.array([158., 291., 424., 556., 689.])
clock_tick_minute = np.array([571., 591., 611., 631., 651.])
clock_fit = np.polyfit(clock_tick_x, clock_tick_minute, 1)
xs = np.arange(72., 774., 6.)
post_t = np.polyval(clock_fit, xs)
curves = {}
for name, (top, bottom, lo, hi) in {
    'width': (10, 166, 0., 1.), 'height': (207, 363, 100., 300.)
}.items():
    for well in ['horizontal', 'vertical']:
        center, lower, upper = [], [], []
        for xi in xs:
            x = int(round(np.clip(xi, 72, 773)))
            col = im[top+2:bottom-1, x]
            rr, gg, bb = col.T
            if well == 'horizontal':
                ink = (gg-rr > 20) & (gg-bb > 20)
                if name == 'width': ink &= np.arange(len(col)) < 90
                target = np.array([233, 241, 231])
            else:
                ink = (rr-gg > 15) & (bb-gg > 30)
                if name == 'width': ink &= np.arange(len(col)) < 108
                if name == 'height': ink &= np.arange(len(col)) < 95
                target = np.array([240, 235, 244])
            hits = np.where(ink)[0]
            if not len(hits):
                center.append(float('nan'));lower.append(float('nan'));upper.append(float('nan'))
                continue
            # A separate legend swatch can occupy the same x column. Use the
            # upper connected ink run, which belongs to the plotted curve.
            runs=np.split(hits,np.where(np.diff(hits)>1)[0]+1)
            cy = float(np.median(runs[0])) + top+2
            band = np.where(np.max(np.abs(col-target), axis=1) <= 2)[0] + top+2
            # Select only the band close to the curve, excluding the other legend.
            band = band[np.abs(band-cy) < (35 if name=='width' else 45)]
            y0 = min(float(band.min()) if len(band) else cy, cy)
            y1 = max(float(band.max()) if len(band) else cy, cy)
            val = lambda y: hi-(y-top)/(bottom-top)*(hi-lo)
            center.append(val(cy)); lower.append(val(y1)); upper.append(val(y0))
        for suffix, values in [('',center),('_lower',lower),('_upper',upper)]:
            values=np.array(values)
            finite=np.isfinite(values)
            # Occasional anti-aliased/overlapping line pixels are interpolated
            # between visible neighbours, only for the raster-derived display.
            curves[f'{name}_{well}{suffix}']=np.interp(xs,xs[finite],values[finite])

np.savez_compressed(ROOT / 'display-data.npz',
    pump_time=pump[:,0], bhp_psi=pump[:,1], slurry_bbl_min=pump[:,2],
    pre_time=pre_t, half_length_m=pre[:,0], post_time=post_t, **curves)

report = {
    'date': '2019-04-18',
    'clock_convention': 'Clock labels from the original stage-19 analysis; no timezone conversion.',
    'left_panels': {
        'source': 'Supplied monitoring figure; plot data are embedded as a raster, with a separately drawn scan cursor. Native data found locally were not substituted because they did not reproduce this figure.',
        'limits_as_labeled_in_supplied_figure': {'vertical_strain_rate_per_s': [-2e-10,2e-10], 'horizontal_strain': [-1e-9,1e-9]},
        'pumping': 'The pumping panel is also embedded from the approved monitoring figure. The packaged CSV is supporting source context, not substituted into the displayed figure.',
        'annotation_cleanup': 'monitoring-clean.png is the built-in imagegen annotation-removal output chosen by the user. It is a visual source figure, not recovered raw measurement data. The three reference PNGs are retained unchanged.',
    },
    'before_hit': {'selected_series': 'Liu et al. (red triangles in supplied chart)',
        'result_file': 'sources/before-hit-selected-series.dat',
        'n': len(pre), 'first_minute_of_day': float(pre_t[0]), 'last_minute_of_day': float(pre_t[-1]),
        'timestamp_basis': 'Original pre-hit notebook: monitoring start 08:17:51 + 8 min, 30-second increments. The separately assembled pumping subplot in the supplied figure is not used to stretch these timestamps.'},
    'after_hit': {'n':len(xs), 'first_minute_of_day':float(post_t[0]), 'last_minute_of_day':float(post_t[-1]),
        'source': 'Curves and shaded intervals digitized from supplied after-hit PNG. This is a raster-derived display approximation, not new inversion data or a confidence-interval interpretation.',
        'timestamp_basis': 'Least-squares affine mapping from the five visible clock tick positions on the supplied figure, 09:31 through 10:51. Do not stretch to the longer legacy NPY inversion time range. X sampling is for animation, not a claim about the original inversion sampling interval.',
        'clock_fit_minutes_per_pixel_and_intercept':clock_fit.tolist(),
        'clock_fit_max_residual_seconds':float(np.max(np.abs(np.polyval(clock_fit,clock_tick_x)-clock_tick_minute))*60),
        'pixel_quantization': 'About 0.0064 mm in width and 1.28 m in height; time alignment approximately 10 seconds per pixel. Isolated missing line pixels at intersections are interpolated from visible neighbours.'},
    'transition': 'Compress approximately 09:03 to 09:18 into a 600 ms eased scan and fade between right-panel layouts. No intermediate notice, pause or added inversion values; not an inferred exact fracture-hit time.',
    'source_files': [p.name for p in SOURCE.iterdir() if p.is_file()],
    'source_image_sha256': {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.glob('*.png')},
}
(ROOT/'data-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'display_dataset_bytes':(ROOT/'display-data.npz').stat().st_size,'post_range':[float(post_t[0]),float(post_t[-1])],'pre_range':[float(pre_t[0]),float(pre_t[-1])]},indent=2))
