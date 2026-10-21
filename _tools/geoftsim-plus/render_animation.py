"""Plot an orthographic 3D cutaway using a reproducible pressure-diffusion field."""
from pathlib import Path
import os
os.environ['MPLCONFIGDIR']=str(Path(__file__).resolve().parent/'.mpl-cache')
os.environ['OPENBLAS_NUM_THREADS']='1'
import argparse
import json
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, colors
from matplotlib.collections import PolyCollection, LineCollection
from matplotlib.cm import ScalarMappable
from matplotlib.font_manager import fontManager
from PIL import Image
from scipy.spatial import cKDTree
from scipy.ndimage import map_coordinates

ROOT=Path(__file__).resolve().parent
DATA=np.load(ROOT/'model'/'upc-pressure-field.npz')
PARAMS=json.loads((ROOT/'model'/'model-verification.json').read_text())['parameters']
OUT=ROOT/'output';FRAMES=ROOT/'.build'/'frames'
OUT.mkdir(exist_ok=True);FRAMES.mkdir(parents=True,exist_ok=True)
W,H,DPI=1440,900,120
NAVY,MUTED='#17384d','#607788'
font='DejaVu Sans'
for filename in ['arial.ttf','arialbd.ttf']:
    p=Path('C:/Windows/Fonts')/filename
    if p.exists():fontManager.addfont(str(p));font='Arial'
plt.rcParams.update({'font.family':font,'font.size':15,'text.color':NAVY,
    'axes.labelcolor':NAVY,'xtick.color':MUTED,'ytick.color':MUTED,
    'axes.edgecolor':'#b7c8d2','savefig.facecolor':'white'})

X,Y,Z=DATA['x'],DATA['y'],DATA['z']
LX,LY,LZ=PARAMS['domain_m']
XE=np.linspace(0,LX,len(X)+1);YE=np.linspace(0,LY,len(Y)+1)
ZE=np.linspace(0,LZ,len(Z)+1)
CUT=140.
AZ,EL=np.deg2rad(-84),np.deg2rad(55)
RIGHT=np.array([-np.sin(AZ),np.cos(AZ),0.])
UP=np.array([-np.sin(EL)*np.cos(AZ),-np.sin(EL)*np.sin(AZ),np.cos(EL)])
VIEW=np.array([np.cos(EL)*np.cos(AZ),np.cos(EL)*np.sin(AZ),np.sin(EL)])


def project(points):
    points=np.asarray(points)
    return np.stack((points@RIGHT,points@UP),axis=-1)


def quad(a,b,c,d):return np.array([a,b,c,d],float)


def build_geometry():
    polygons=[];lookup=[];kind=[]
    # Exposed horizontal pressure section, plus visible front and right faces.
    display_x=np.linspace(0,LX,len(X)*2+1)
    display_y=np.linspace(0,LY,len(Y)*2+1)
    for i in range(len(display_x)-1):
        for j in range(len(display_y)-1):
            polygons.append(quad([display_x[i],display_y[j],CUT],[display_x[i+1],display_y[j],CUT],
                [display_x[i+1],display_y[j+1],CUT],[display_x[i],display_y[j+1],CUT]))
            lookup.append((i//2,j//2,6,7,.5));kind.append('matrix')
    for i in range(len(X)):
        for k in range(7):
            polygons.append(quad([XE[i],0,ZE[k]],[XE[i+1],0,ZE[k]],
                [XE[i+1],0,ZE[k+1]],[XE[i],0,ZE[k+1]]))
            lookup.append((i,0,k,k,0.));kind.append('matrix')
    for j in range(len(Y)):
        for k in range(7):
            polygons.append(quad([LX,YE[j],ZE[k]],[LX,YE[j+1],ZE[k]],
                [LX,YE[j+1],ZE[k+1]],[LX,YE[j],ZE[k+1]]))
            lookup.append((len(X)-1,j,k,k,0.));kind.append('matrix')
    # Planar fracture panels above the exposed section. The network is fixed;
    # opacity follows drawdown, so undrained panels do not reveal UPC at t=0.
    ix,iy=np.where(DATA['fracture_mask'])
    tree=cKDTree(np.column_stack((X[ix],Y[iy])))
    trace_segments=[];trace_lookup=[]
    for letter in 'UPC':
        path=DATA['trace_'+letter]
        for a,b in zip(path[:-1],path[1:]):
            _,hit=tree.query((a+b)/2)
            i,j=int(ix[hit]),int(iy[hit])
            for z0,z1 in zip([140,160,180],[160,180,200]):
                k=int(np.argmin(abs(Z-(z0+z1)/2)))
                polygons.append(quad([*a,z0],[*b,z0],[*b,z1],[*a,z1]))
                lookup.append((i,j,k,k,0.));kind.append('fracture')
            trace_segments.append([[*a,200.3],[*b,200.3]])
            trace_lookup.append((i,j,len(Z)-1))
    polygons=np.array(polygons)
    order=np.argsort(polygons.mean(axis=1)@VIEW)
    return polygons[order],np.array(lookup)[order],np.array(kind)[order],np.array(trace_segments),np.array(trace_lookup)


def render(preview=False):
    polygons,lookup,kind,trace_segments,trace_lookup=build_geometry()
    projected=project(polygons)
    fig=plt.figure(figsize=(W/DPI,H/DPI),dpi=DPI,facecolor='white')
    fig.text(.04,.947,'GeoFTSim+',fontsize=29,fontweight='bold',va='center')
    fig.text(.04,.896,'Fracture-controlled reservoir depletion',fontsize=19,color=MUTED)
    timer=fig.text(.96,.947,'Day 0',fontsize=23,fontweight='bold',ha='right',va='center')
    ax=fig.add_axes((.025,.215,.95,.64))
    ax.set_aspect('equal');ax.axis('off')
    bounds=project([[x,y,z] for x in [0,LX] for y in [0,LY] for z in [0,270]])
    ax.set_xlim(bounds[:,0].min()-35,bounds[:,0].max()+35)
    ax.set_ylim(bounds[:,1].min()-35,bounds[:,1].max()+10)
    cmap=plt.get_cmap('turbo');norm=colors.Normalize(10,30)
    faces=PolyCollection(projected,edgecolors='none',antialiased=False,zorder=2)
    ax.add_collection(faces)

    # Light cutaway edges and the bounding frame establish the full 3D volume.
    def line3d(points,**kwargs):
        xy=project(points);return ax.plot(xy[:,0],xy[:,1],**kwargs)[0]
    line3d([[0,0,0],[LX,0,0],[LX,LY,0]],color='#587283',lw=1.0,zorder=3)
    line3d([[0,0,0],[0,0,CUT],[0,LY,CUT],[LX,LY,CUT],[LX,0,CUT],[0,0,CUT]],color='#587283',lw=.8,alpha=.65,zorder=3)
    line3d([[LX,0,0],[LX,0,CUT]],color='#587283',lw=.8,alpha=.65,zorder=3)
    for p in [[0,0],[0,LY],[LX,LY],[LX,0]]:
        line3d([[*p,CUT],[*p,LZ]],color='#aebec8',lw=.8,alpha=.6,ls=(0,(3,3)),zorder=1)
    line3d([[0,0,LZ],[0,LY,LZ],[LX,LY,LZ],[LX,0,LZ],[0,0,LZ]],color='#aebec8',lw=.8,alpha=.6,zorder=1)
    # Sparse reference grid on the exposed section; never outlines the letters.
    for x in np.arange(100,LX,100):line3d([[x,0,CUT+.1],[x,LY,CUT+.1]],color='white',alpha=.08,lw=.5,zorder=3)
    for y in np.arange(100,LY,100):line3d([[0,y,CUT+.1],[LX,y,CUT+.1]],color='white',alpha=.08,lw=.5,zorder=3)
    edges=LineCollection(project(trace_segments),linewidths=1.1,antialiased=True,zorder=5)
    ax.add_collection(edges)
    heads=[]
    for well in PARAMS['producers']:
        x,y=well['xy_m']
        line3d([[x,y,CUT],[x,y,258]],color='#536b7a',lw=3.,zorder=6)
        line3d([[x,y,CUT],[x,y,258]],color='#d5e0e6',lw=1.,zorder=7)
        xy=project([x,y,258])
        heads.append(ax.scatter([xy[0]],[xy[1]],s=48,facecolor='white',edgecolor='#536b7a',linewidth=1.4,zorder=8))
    # Dimensions describe the physical model, not a second scalar quantity.
    for pos,label in [([LX*.5,-42,-6],'1,200 m'),([LX+34,LY*.55,0],'600 m')]:
        xy=project(pos);ax.text(*xy,label,fontsize=12,color=MUTED,ha='center',va='center')
    cb=fig.colorbar(ScalarMappable(norm=norm,cmap=cmap),cax=fig.add_axes((.19,.14,.62,.018)),orientation='horizontal',ticks=[10,15,20,25,30])
    cb.ax.tick_params(labelsize=13,length=3);cb.outline.set_linewidth(.6)
    cb.set_label('Reservoir pressure (MPa)',fontsize=15,labelpad=7)

    ii,jj,k0,k1=lookup[:,:4].astype(int).T;weight=lookup[:,4]
    coordinates=((polygons.mean(axis=1)-np.array([X[0],Y[0],Z[0]]))/np.array([X[1]-X[0],Y[1]-Y[0],Z[1]-Z[0]])).T
    ti,tj,tk=trace_lookup.T
    selected=[0,5,15,30,60,90,120] if preview else range(len(DATA['days']))
    visibility=[]
    for index in selected:
        p=DATA['pressure_MPa'][index]
        # Linear resampling makes the visual section smooth without overshoot;
        # no extra simulation resolution or independent data are implied.
        sampled=map_coordinates(p,coordinates,order=1,mode='nearest')
        frac=kind=='fracture'
        sampled[frac]=p[ii[frac],jj[frac],k0[frac]]
        rgba=cmap(norm(sampled))
        rgba[frac,3]=np.clip((30-sampled[frac])/20*1.7,0,1)
        faces.set_facecolors(rgba)
        edge_p=p[ti,tj,tk]
        trace_rgba=cmap(norm(edge_p));trace_rgba[:,3]=np.clip((30-edge_p)/20*1.7,0,1)
        edges.set_colors(trace_rgba)
        day=float(DATA['days'][index]);timer.set_text(f'Day {day:.0f}')
        for head,well in zip(heads,PARAMS['producers']):head.set_facecolor('#d3902c' if day>=well['start_day'] else 'white')
        fig.savefig(FRAMES/f'frame-{index:03d}.png',dpi=DPI)
        visibility.append({'day':day,'mean_fracture_opacity':float(rgba[frac,3].mean()),
            'fracture_pressure_min_MPa':float(sampled[frac].min()),'fracture_pressure_max_MPa':float(sampled[frac].max())})
    plt.close(fig)
    (OUT/'rendering-metadata.json').write_text(json.dumps({'projection':'Orthographic, azimuth -84°, elevation 55°; all coordinates in metres.',
        'exposed_section_z_m':CUT,'pressure_colorbar_MPa':[10,30],'colormap':'turbo',
        'matrix_display_sampling':'Linear interpolation of the 3D finite-volume field onto a refined display surface; no smoothing of the solved data.',
        'fracture_display':'Prescribed panels from z=140 to 200 m; opacity is clamp(1.7*(30-p)/20,0,1), purely for gradual visibility. Geometry never propagates.',
        'preview_only':preview,'sampled_visibility':visibility},indent=2),encoding='utf-8')


def encode():
    # Put exact white first so Pillow's lookup quantizer preserves the large
    # white background rather than assigning it to the neighbouring gray bin.
    palette=[(255,255,255)]
    palette+=[tuple(round(v*255) for v in colors.to_rgb(c)) for c in [NAVY,MUTED,'#d3902c','#536b7a','#d5e0e6','#587283','#aebec8']]
    palette+=[tuple(np.round(np.array(plt.get_cmap('turbo')(s)[:3])*255).astype(int)) for s in np.linspace(0,1,180)]
    palette+=[(v,v,v) for v in np.linspace(0,255,44).astype(int)]
    flat=[int(v) for rgb in palette for v in rgb];flat+=[255]*(768-len(flat))
    pal=Image.new('P',(1,1));pal.putpalette(flat)
    frames=[]
    for i in range(len(DATA['days'])):
        with Image.open(FRAMES/f'frame-{i:03d}.png') as im:
            frames.append(im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE))
    durations=[110]*len(frames);durations[0]=650;durations[-1]=1800
    target=OUT/'geoftsim-upc-pressure-depletion-v2.gif'
    frames[0].save(target,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=1,optimize=True)
    with Image.open(FRAMES/f'frame-{len(frames)-1:03d}.png') as im:
        im.convert('RGB').save(OUT/'geoftsim-upc-pressure-depletion-v2-poster.png',optimize=True)
    (OUT/'animation-timeline.json').write_text(json.dumps({'frames':len(frames),'days':DATA['days'].tolist(),
        'durations_ms':durations,'total_duration_ms':sum(durations),'dimensions':[W,H]},indent=2),encoding='utf-8')
    print('GIF bytes',target.stat().st_size,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');parser.add_argument('--encode-only',action='store_true');args=parser.parse_args()
    start=time.monotonic()
    if not args.encode_only:render(args.preview)
    if not args.preview:encode()
    print('Elapsed',round(time.monotonic()-start,2),flush=True)
