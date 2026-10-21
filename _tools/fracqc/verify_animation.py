"""Check clocks, scan registration, source bounds and decoded GIF frames."""
from pathlib import Path
import json
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent
timeline=json.loads((ROOT/'animation-timeline.json').read_text())
frames=timeline['frames']
data=np.load(ROOT/'display-data.npz')
assert len(frames)==147
assert sum(f['phase']=='pre' for f in frames)==76
assert sum(f['phase']=='transition' for f in frames)==12
assert all(f['phase']!='gap' and '→' not in f['clock'] for f in frames)
assert all(b['minute_of_day']>=a['minute_of_day'] for a,b in zip(frames,frames[1:]))
assert frames[76]['phase']=='transition' and frames[88]['phase']=='post'
assert frames[88]['minute_of_day']-frames[75]['minute_of_day']>14
assert all(f['duration_ms']==50 for f in frames[76:88])
assert frames[75]['duration_ms']==frames[88]['duration_ms']==90
assert max(b['minute_of_day']-a['minute_of_day'] for a,b in zip(frames[75:88],frames[76:89]))<2
for key in data.files:assert np.isfinite(data[key]).all(),key
for name in ['width','height']:
    for well in ['horizontal','vertical']:
        value=data[f'{name}_{well}']
        assert np.all(data[f'{name}_{well}_lower']<=value+1e-9)
        assert np.all(data[f'{name}_{well}_upper']>=value-1e-9)

source=np.asarray(Image.open(ROOT/'sources'/'monitoring-clean.png').convert('RGB'))
assert source.shape==(1395,1127,3)
black_marker_checks=[]
for box in [(106,136,1038,497),(106,621,1046,987)]:
    x0,y0,x1,y1=box
    fraction=(source[y0:y1,x0:x1].max(axis=2)<40).mean(axis=0)
    assert fraction.max()<.15,'A solid black vertical reference line remains'
    black_marker_checks.append(float(fraction.max()))

results=[]
gold=np.array([211,144,44])
for mobile in [False,True]:
    prefix='fracqc-field-characterization'+('-mobile' if mobile else '')+'-v2'
    path=ROOT/'output'/(prefix+'.gif')
    mode='mobile' if mobile else 'desktop'
    size=(840,1740) if mobile else (1600,1000)
    errors=[];scan_errors=[];durations=[]
    with Image.open(path) as gif:
        assert gif.n_frames==len(frames)
        assert gif.size==size and gif.info['loop']==0
        for i in range(gif.n_frames):
            gif.seek(i);durations.append(gif.info['duration'])
            assert durations[-1]==frames[i]['duration_ms']
            if i not in [0,40,75,76,81,82,87,88,118,146]:continue
            decoded=np.asarray(gif.convert('RGB')).astype(int)
            original=np.asarray(Image.open(ROOT/'.build'/mode/f'frame-{i:03d}.png').convert('RGB')).astype(int)
            mae=float(np.abs(decoded-original).mean());errors.append(mae)
            assert mae<4.,(mode,i,mae)
            # Check all three cursors at the very same clock coordinate.
            x0,xw=(.13,.74) if mobile else (.073,.48)
            t=frames[i]['minute_of_day'];begin=8*60+17+51/60;end=11*60+12+50/60
            expected=(x0+xw*(t-begin)/(end-begin))*size[0]
            ys=[.80,.63,.47] if mobile else [.70,.44,.21]
            for y in ys:
                row=decoded[round((1-y)*size[1]),:]
                hits=np.where(np.max(abs(row-gold),axis=1)<3)[0]
                assert len(hits),(mode,i,y)
                distance=float(np.min(abs(hits-expected)))
                assert distance<3,(mode,i,distance)
                scan_errors.append(distance)
    results.append({'file':path.name,'frames':len(frames),'dimensions':size,
        'duration_ms':sum(durations),'bytes':path.stat().st_size,
        'max_decoded_frame_mae':max(errors),'max_scan_registration_error_px':max(scan_errors)})
report={'status':'passed','transition':'600 ms continuous sweep with right-panel fades; no intermediate notice or pause; no added inversion results',
    'monitoring_black_marker_max_column_fraction':black_marker_checks,'animations':results}
(ROOT/'verification-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
