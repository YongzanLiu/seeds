"""Verify the numerical example and the decoded scientific animation."""
from pathlib import Path
import json
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent
data=np.load(ROOT/'model'/'upc-pressure-field.npz')
model=json.loads((ROOT/'model'/'model-verification.json').read_text())
meta=json.loads((ROOT/'output'/'rendering-metadata.json').read_text())
timeline=json.loads((ROOT/'output'/'animation-timeline.json').read_text())
p=data['pressure_MPa']
assert p.shape==(121,120,60,10) and np.isfinite(p).all()
assert np.all(p[0]==30.) and p.min()>=10.-1e-4 and p.max()<=30.+1e-4
assert np.max(np.diff(p,axis=0))<1e-4
assert model['benchmark']['max_absolute_error']<1.e-11
assert model['max_relative_linear_residual']<1.1e-9
assert model['max_relative_volume_balance_error']<1.e-5
assert model['fracture_components']==3
assert not meta['preview_only'] and len(meta['sampled_visibility'])==121
assert meta['sampled_visibility'][0]['mean_fracture_opacity']==0.
assert meta['sampled_visibility'][-1]['mean_fracture_opacity']>.95
assert meta['pressure_colorbar_MPa']==[10,30]
fracture_mean=float(p[-1][data['fracture_mask']].mean())
matrix_mean=float(p[-1][~data['fracture_mask']].mean())
assert matrix_mean-fracture_mean>5.,'Insufficient pressure contrast for UPC to emerge'

gif_path=ROOT/'output'/'geoftsim-upc-pressure-depletion-v2.gif'
errors=[];durations=[];bar=None;first=None;last=None
with Image.open(gif_path) as gif:
    assert gif.n_frames==121 and gif.size==(1440,900) and gif.info['loop']==0
    for i in range(gif.n_frames):
        gif.seek(i);durations.append(gif.info['duration'])
        assert durations[-1]==timeline['durations_ms'][i]
        frame=np.asarray(gif.convert('RGB')).astype(int)
        assert np.all(frame[850:890]==255),'The removed footer captions remain visible'
        current_bar=frame[760:770,300:1140]
        if bar is None:bar=current_bar.copy()
        else:assert np.array_equal(bar,current_bar),'The color scale changed between frames'
        if i==0:first=frame.copy()
        if i==120:last=frame.copy()
        if i not in [0,5,15,30,60,90,120]:continue
        original=np.asarray(Image.open(ROOT/'.build'/'frames'/f'frame-{i:03d}.png').convert('RGB')).astype(int)
        error=float(np.abs(frame-original).mean());errors.append(error)
        assert error<4.,(i,error)
change=float(np.abs(last[200:650,290:1180]-first[200:650,290:1180]).mean())
assert change>8.
assert sum(durations)==timeline['total_duration_ms']
report={'status':'passed','frames':121,'dimensions':[1440,900],'loop_duration_ms':sum(durations),
    'mean_final_fracture_pressure_MPa':fracture_mean,'mean_final_matrix_pressure_MPa':matrix_mean,
    'maximum_decoded_frame_MAE':max(errors),'model_image_change_MAE':change,
    'color_scale_identical_across_all_frames':True,'gif_bytes':gif_path.stat().st_size,
    'model_data_bytes':(ROOT/'model'/'upc-pressure-field.npz').stat().st_size}
(ROOT/'output'/'verification-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
