"""Render the FracQC scientific showcase from the packaged display dataset."""
from pathlib import Path
import argparse
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR'] = str(ROOT / '.mpl-cache')
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, colors
from matplotlib.font_manager import fontManager
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.cm import ScalarMappable
from PIL import Image

DATA = np.load(ROOT / 'display-data.npz')
OUT = ROOT / 'output'
OUT.mkdir(exist_ok=True)
NAVY, MUTED, GOLD = '#17384d', '#607788', '#d3902c'
GREEN, PURPLE, BLUE, RED = '#378649', '#9060b8', '#2879bb', '#da4c46'
has_arial=False
for f in ['arial.ttf', 'arialbd.ttf']:
    p = Path('C:/Windows/Fonts') / f
    if p.exists(): fontManager.addfont(str(p));has_arial=True
plt.rcParams.update({'font.family':'Arial' if has_arial else 'DejaVu Sans', 'font.size':14, 'text.color':NAVY,
    'axes.labelcolor':MUTED,'xtick.color':MUTED,'ytick.color':MUTED,
    'axes.edgecolor':'#ccdae2','axes.linewidth':.8,'savefig.facecolor':'white'})


def clock(t):
    sec = round(t*60)
    return f'{sec//3600:02d}:{sec//60%60:02d}:{sec%60:02d}'


PRE_T, POST_T = DATA['pre_time'], DATA['post_time']
# Every pre-hit result (30 s), then every second raster sample (~108 s).
STEPS = [('pre', float(t)) for t in PRE_T]
# Compress the unanalysed interval into a short, eased sweep, with no notice
# screen or pause. These are presentation frames, not new inversion samples.
TRANSITION_COUNT = 12
for u in np.linspace(0, 1, TRANSITION_COUNT+2)[1:-1]:
    eased = u*u*(3-2*u)
    STEPS.append(('transition', float(PRE_T[-1]+eased*(POST_T[0]-PRE_T[-1]))))
STEPS += [('post', float(t)) for t in POST_T[::2]]
if STEPS[-1][1] != POST_T[-1]: STEPS.append(('post', float(POST_T[-1])))
DURATIONS = [90]*len(STEPS)
DURATIONS[0], DURATIONS[-1] = 600, 1800
for i in range(len(PRE_T),len(PRE_T)+TRANSITION_COUNT):DURATIONS[i]=50


def style(ax, *, grid=False):
    ax.spines[['top','right']].set_visible(False)
    ax.tick_params(length=3, labelsize=12)
    if grid: ax.grid(axis='y', color='#e6edf1', linewidth=.7); ax.set_axisbelow(True)


def time_axis(ax, begin, end, labels=True, ticks=None):
    ax.set_xlim(begin, end)
    ticks = ticks or [510, 540, 570, 600, 630, 660]
    ax.set_xticks(ticks, [f'{int(t)//60:02d}:{int(t)%60:02d}' for t in ticks])
    ax.tick_params(axis='x', labelbottom=labels)


def render(mobile=False, preview=False):
    W,H = (840,1740) if mobile else (1600,1000)
    fig = plt.figure(figsize=(W/120,H/120),dpi=120,facecolor='white')
    frame_dir = ROOT / '.build' / ('mobile' if mobile else 'desktop')
    frame_dir.mkdir(parents=True,exist_ok=True)
    if mobile:
        leftx,leftw = .13,.74
        panels = [(leftx,.745,leftw,.12),(leftx,.57,leftw,.12),(leftx,.425,leftw,.095)]
        right_box = (.05,.045,.90,.31)
        param_boxes = [(.15,.22,.73,.08),(.15,.085,.73,.08)]
        half_box = (.15,.12,.73,.17)
        cbar_boxes = [(.13,.875,.74,.007),(.13,.70,.74,.007)]
        title_y, sub_y, phase_y, section_y = .972,.946,.904,.924
        clock_pos=(.95,.972)
        result_title_y=.331
    else:
        leftx,leftw = .073,.48
        panels = [(leftx,.625,leftw,.18),(leftx,.355,leftw,.18),(leftx,.145,leftw,.14)]
        right_box = (.625,.105,.345,.735)
        param_boxes = [(.69,.515,.265,.205),(.69,.215,.265,.205)]
        half_box = (.69,.34,.265,.36)
        cbar_boxes = [(.073,.822,.48,.011),(.073,.552,.48,.011)]
        title_y, sub_y, phase_y, section_y = .955,.906,.855,.863
        clock_pos=(.97,.955)
        result_title_y=.795

    fig.text(.035,title_y,'FracQC',fontsize=29,fontweight='bold',va='center')
    fig.text(.035,sub_y,'Field strain → fracture geometry',fontsize=19,color=MUTED,va='center')
    timer=fig.text(*clock_pos,'',ha='right',fontsize=23 if mobile else 25,fontweight='bold',va='center')
    result_bg = FancyBboxPatch((right_box[0],right_box[1]),right_box[2],right_box[3],
        transform=fig.transFigure,boxstyle='round,pad=0.008,rounding_size=0.013',
        facecolor='#f5f8fa',edgecolor='#e0e9ee',linewidth=1,zorder=-10)
    fig.add_artist(result_bg)
    phase=fig.text(right_box[0]+.018,result_title_y,'',fontsize=17,fontweight='bold')
    result_sub=fig.text(right_box[0]+.018,result_title_y-(.023 if mobile else .042),'',fontsize=13,color=MUTED)
    fig.text(.035,.018,'18 Apr 2019  •  Time-synchronized field example',fontsize=12,color=MUTED)

    axes=[fig.add_axes(p) for p in panels]
    begin,end = 8*60+17+51/60, 11*60+12+50/60
    heatmaps = [('vertical','Vertical monitoring well · strain rate',(103,134,1040,499),2.,r'$10^{-10}$ s$^{-1}$'),
                ('horizontal','Horizontal offset well · strain',(103,619,1048,989),10.,r'$10^{-10}$ $\epsilon$')]
    monitoring_file=ROOT/'sources'/'monitoring-clean.png'
    if not monitoring_file.exists():monitoring_file=ROOT/'sources'/'monitoring-reference.png'
    monitoring_image=np.asarray(Image.open(monitoring_file).convert('RGB'))
    sx,sy=monitoring_image.shape[1]/1127,monitoring_image.shape[0]/1395
    cursor=[]
    for ax,(key,label,box,limit,unit),cbbox in zip(axes,heatmaps,cbar_boxes):
        x0,y0,x1,y1=[round(v*(sx if i%2==0 else sy)) for i,v in enumerate(box)]
        value=monitoring_image[y0:y1,x0:x1]
        depth=(3800,3000) if key=='vertical' else (5500,4100)
        ax.imshow(value,extent=(begin,end,*depth),aspect='auto',interpolation='nearest',rasterized=True)
        ax.set_ylim((3800,3000) if key=='vertical' else (5500,4100))
        ax.set_yticks([3000,3400,3800] if key=='vertical' else [4200,4800,5400])
        ax.set_ylabel('Depth (m)' if key=='vertical' else 'Trace (m)',fontsize=12)
        ax.text(0,1.31 if mobile else 1.25,label,transform=ax.transAxes,fontsize=15,fontweight='bold')
        time_axis(ax,begin,end,False)
        ax.tick_params(labelsize=12,length=2)
        cb=fig.colorbar(ScalarMappable(norm=colors.Normalize(-limit,limit),cmap='seismic'),cax=fig.add_axes(cbbox),orientation='horizontal',ticks=[-limit,0,limit])
        cb.ax.tick_params(labelsize=10,length=2,pad=1)
        cb.outline.set_linewidth(.5)
        cb.ax.text(1.015,.5,unit,transform=cb.ax.transAxes,fontsize=10,va='center')
        cursor.append(ax.axvline(PRE_T[0],color=GOLD,lw=2.2,zorder=8))

    pump=axes[2]
    # Embed the pumping panel from the same approved figure, preserving its
    # registration and event sequence with the two monitoring heatmaps.
    px0,py0,px1,py1=[round(v*(sx if i%2==0 else sy)) for i,v in enumerate((103,1062,1047,1298))]
    pump.imshow(monitoring_image[py0:py1,px0:px1],extent=(begin,end,4,16),aspect='auto',interpolation='nearest')
    twin=pump.twinx()
    twin.set_ylim(0,30);twin.set_yticks([0,15,30]);twin.tick_params(axis='y',colors=RED,labelsize=11,length=2)
    twin.set_ylabel('Rate (bbl/min)',fontsize=11,color=RED)
    pump.set_ylim(4,16);pump.set_yticks([5,10,15])
    pump.set_ylabel('BHP (10³ psi)',fontsize=11,color=BLUE)
    pump.tick_params(axis='y',colors=BLUE,labelsize=11)
    pump.text(0,1.12,'Pumping treatment',transform=pump.transAxes,fontsize=15,fontweight='bold')
    time_axis(pump,begin,end,True,ticks=[510,570,630,660] if mobile else [510,540,570,600,630,660])
    pump.set_xlabel('Monitoring time',fontsize=12,labelpad=6)
    style(pump);twin.spines['top'].set_visible(False)
    cursor.append(pump.axvline(PRE_T[0],color=GOLD,lw=2.2,zorder=8))

    half=fig.add_axes(half_box,facecolor='#f5f8fa')
    half.set_ylim(95,207);half.set_yticks([100,150,200]);half.set_ylabel('Half-length (m)',fontsize=13)
    time_axis(half,PRE_T[0]-.5,PRE_T[-1]+.5,ticks=[510,525,540]);style(half,grid=True)
    half_line,=half.plot([],[],color=RED,lw=1.6,marker='^',ms=4.5,mfc='white',mew=1.15)
    half_dot,=half.plot([],[],marker='o',color=GOLD,ms=7)
    half.set_xlabel('Monitoring time',fontsize=12)
    half_note=fig.text(right_box[0]+right_box[2]/2,right_box[1]+(.02 if mobile else .08),
        'Fracture growth before well intersection',ha='center',fontsize=12,color=MUTED)

    params=[]
    for name,box,ylim,yticks in [('width',param_boxes[0],(0,1),[0,.5,1]),
                               ('height',param_boxes[1],(100,320),[100,200,300])]:
        ax=fig.add_axes(box,facecolor='#f5f8fa')
        ax.set_ylim(*ylim);ax.set_yticks(yticks)
        ax.set_ylabel('Width (mm)' if name=='width' else 'Height (m)',fontsize=13)
        time_axis(ax,POST_T[0],POST_T[-1],True,ticks=[570,600,630,660]);style(ax,grid=True)
        if name=='height':ax.set_xlabel('Monitoring time',fontsize=12)
        for well,c in [('horizontal',GREEN),('vertical',PURPLE)]:
            line,=ax.plot([],[],color=c,lw=2,label=well.title()+' well')
            dot,=ax.plot([],[],color=c,marker='o',ms=5)
            params.append((ax,name,well,c,line,dot))
        if name=='width':
            ax.legend(loc='lower left',fontsize=10,frameon=False,handlelength=1.6)
        ax.set_visible(False)
    fills=[]
    original_alphas={}

    def fade_axis(ax, opacity):
        # Restore each artist's own opacity (including the source shaded bands)
        # after the transition; do not alter the plotted parameter values.
        for artist in ax.findobj():
            if not hasattr(artist,'set_alpha'):continue
            if artist not in original_alphas:original_alphas[artist]=artist.get_alpha()
            base=original_alphas[artist]
            artist.set_alpha(opacity*(1. if base is None else base))

    indices = [0,40,len(PRE_T)-1,len(PRE_T),len(PRE_T)+5,len(PRE_T)+6,
               len(PRE_T)+TRANSITION_COUNT-1,len(PRE_T)+TRANSITION_COUNT,len(STEPS)-1] if preview else range(len(STEPS))
    for idx in indices:
        state,t = STEPS[idx]
        timer.set_text(clock(t))
        u=(t-PRE_T[-1])/(POST_T[0]-PRE_T[-1]) if state=='transition' else None
        is_post=state=='post' or (state=='transition' and u>=.5)
        opacity=abs(2*u-1) if state=='transition' else 1.
        phase.set_text('AFTER FRACTURE HIT' if is_post else 'BEFORE FRACTURE HIT')
        result_sub.set_text('Width and height from two monitoring wells' if is_post else 'Fracture half-length · Liu et al.')
        phase.set_alpha(opacity);result_sub.set_alpha(opacity)
        half.set_visible(not is_post);half_note.set_visible(not is_post)
        half_note.set_alpha(opacity)
        for ln in cursor: ln.set_xdata([t,t])
        n=np.searchsorted(PRE_T,t,side='right')
        half_line.set_data(PRE_T[:n],DATA['half_length_m'][:n])
        if n:half_dot.set_data([PRE_T[n-1]],[DATA['half_length_m'][n-1]])
        for fill in fills:fill.remove()
        fills=[]
        for ax,name,well,c,line,dot in params:
            ax.set_visible(is_post)
            if not is_post:continue
            n=np.searchsorted(POST_T,t,side='right')
            value=DATA[f'{name}_{well}']
            line.set_data(POST_T[:n],value[:n])
            if n:dot.set_data([POST_T[n-1]],[value[n-1]])
            fills.append(ax.fill_between(POST_T[:n],DATA[f'{name}_{well}_lower'][:n],
                DATA[f'{name}_{well}_upper'][:n],color=c,alpha=.12,lw=0,zorder=1))
        if not is_post:fade_axis(half,opacity)
        for ax in {p[0] for p in params}:
            if is_post:fade_axis(ax,opacity)
        fig.savefig(frame_dir/f'frame-{idx:03d}.png',dpi=120)
    plt.close(fig)


def encode(mobile=False):
    prefix='fracqc-field-characterization'+('-mobile' if mobile else '')+'-v2'
    folder=ROOT/'.build'/('mobile' if mobile else 'desktop')
    # Fixed palette preserves the diverging scale and eliminates frame-to-frame
    # changes in heatmap colors caused by independent histogram quantization.
    palette=[]
    palette += [tuple(np.round(np.array(plt.get_cmap('seismic')(x)[:3])*255).astype(int)) for x in np.linspace(0,1,161)]
    palette += [tuple([i]*3) for i in np.linspace(0,255,42).astype(int)]
    palette += [colors.to_rgb(c) for c in []]
    for c in [NAVY,MUTED,GOLD,GREEN,PURPLE,BLUE,RED,'#f5f8fa','#e0e9ee','#ccdae2','#e6edf1']:
        palette.append(tuple(round(v*255) for v in colors.to_rgb(c)))
    for c in [GREEN,PURPLE]:
        rgb=np.array(colors.to_rgb(c))*255
        for alpha in [.12,.20,.35]:palette.append(tuple(np.round(rgb*alpha+np.array([245,248,250])*(1-alpha)).astype(int)))
    flat=[int(v) for rgb in palette for v in rgb]
    flat += [255]*(768-len(flat))
    pal=Image.new('P',(1,1));pal.putpalette(flat)
    frames=[]
    for i in range(len(STEPS)):
        with Image.open(folder/f'frame-{i:03d}.png') as im:
            frames.append(im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE))
    gif=OUT/(prefix+'.gif')
    frames[0].save(gif,save_all=True,append_images=frames[1:],duration=DURATIONS,
        loop=0,optimize=True,disposal=1)
    poster_idx=len(STEPS)-1
    shutil_source=folder/f'frame-{poster_idx:03d}.png'
    with Image.open(shutil_source) as im:im.convert('RGB').save(OUT/(prefix+'-poster.png'),optimize=True)
    print(prefix,gif.stat().st_size,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');parser.add_argument('--encode-only',action='store_true');args=parser.parse_args()
    start=time.monotonic()
    for mobile in [False,True]:
        if not args.encode_only:render(mobile,args.preview)
        if not args.preview:encode(mobile)
    (ROOT/'animation-timeline.json').write_text(json.dumps({'frames':[{'phase':p,'clock':clock(t),'minute_of_day':t,'duration_ms':DURATIONS[i]} for i,(p,t) in enumerate(STEPS)],'n':len(STEPS),'dimensions':{'desktop':[1600,1000],'mobile':[840,1740]}},indent=2),encoding='utf-8')
    print('Elapsed',round(time.monotonic()-start,2),flush=True)
