"""Illustrative 3D pressure diffusion around prescribed UPC-shaped fractures.

This self-contained demonstration is not a GeoFTSim+ simulation or a multiphase
geomechanical benchmark. It supplies a reproducible scalar field for a showcase.
"""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
import json
import time
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import cg, spsolve, LinearOperator
from scipy.ndimage import label

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'model'
OUT.mkdir(exist_ok=True)
PARAMS={
    'domain_m':[1200.,600.,200.], 'grid_cells':[120,60,10],
    'initial_pressure_MPa':30.,'producer_pressure_MPa':10.,
    'matrix_permeability_m2':1.e-17,'equivalent_fracture_zone_permeability_m2':1.e-14,
    'effective_bulk_storage_per_Pa':1.2e-10,'fluid_viscosity_Pa_s':2.e-3,
    'fracture_zone_half_width_m':8.,'dt_days':1.,'end_day':120.,
    'producers':[
        {'letter':'U','xy_m':[240.,120.],'completion_z_m':[80.,120.],'start_day':0.},
        {'letter':'P','xy_m':[480.,320.],'completion_z_m':[80.,120.],'start_day':20.},
        {'letter':'C','xy_m':[810.,290.],'completion_z_m':[80.,120.],'start_day':40.},
    ],
    'boundaries':'No flow on all six external faces; active completion cells at fixed pressure.',
    'assumptions':'Single phase, isothermal, constant properties, no gravity, fixed prescribed fractures; no mechanics or multiphase calculation.',
}


def geometry():
    # Piecewise planar vertical panels; their plan-view traces form UPC.
    angle=np.linspace(np.pi,2*np.pi,25)
    u=np.vstack(([130.,460.],[130.,210.],
        np.column_stack((240+110*np.cos(angle),210+90*np.sin(angle)))[1:], [350.,460.]))
    angle=np.linspace(np.pi/2,-np.pi/2,25)
    p=np.vstack(([480.,120.],[480.,460.],[600.,460.],
        np.column_stack((600+110*np.cos(angle),370+90*np.sin(angle)))[1:], [480.,280.]))
    angle=np.linspace(np.deg2rad(55),np.deg2rad(305),45)
    c=np.column_stack((930+120*np.cos(angle),290+170*np.sin(angle)))
    return {'U':u,'P':p,'C':c}


def operator(k,spacing):
    """Cell-centred conservative finite-volume diffusion, harmonic face means."""
    indices=np.arange(k.size,dtype=np.int32).reshape(k.shape)
    diag=np.zeros_like(k)
    rows=[];cols=[];values=[]
    for axis,dx in enumerate(spacing):
        lo=[slice(None)]*3;hi=lo.copy();lo[axis]=slice(None,-1);hi[axis]=slice(1,None)
        lo,hi=tuple(lo),tuple(hi)
        face=2*k[lo]*k[hi]/(k[lo]+k[hi])/dx**2
        diag[lo]+=face;diag[hi]+=face
        i,j=indices[lo].ravel(),indices[hi].ravel()
        rows.extend([i,j]);cols.extend([j,i]);values.extend([-face.ravel(),-face.ravel()])
    rows.append(indices.ravel());cols.append(indices.ravel());values.append(diag.ravel())
    return sparse.coo_matrix((np.concatenate(values),(np.concatenate(rows),np.concatenate(cols))),shape=(k.size,k.size)).tocsr()


def benchmark():
    shape=(9,7,5);k=np.ones(shape)
    lap=operator(k,[1.,1.,1.])
    exact=np.broadcast_to(np.linspace(1,0,shape[0])[:,None,None],shape).copy().ravel()
    fixed=np.zeros(shape,bool);fixed[[0,-1],:,:]=True;fixed=fixed.ravel();free=~fixed
    sol=np.where(fixed,exact,0.)
    sol[free]=spsolve(lap[free][:,free],-(lap[free]@sol))
    error=float(np.max(abs(sol-exact)))
    assert error<1.e-11
    return {'analytic_case':'3D homogeneous linear pressure, two fixed opposite faces and four no-flow faces','max_absolute_error':error}


def solve():
    start=time.monotonic()
    spacing=np.array(PARAMS['domain_m'])/PARAMS['grid_cells']
    x,y,z=[(np.arange(n)+.5)*dx for n,dx in zip(PARAMS['grid_cells'],spacing)]
    xx,yy=np.meshgrid(x,y,indexing='ij')
    paths=geometry();mask=np.zeros(xx.shape,bool);letter_masks={}
    for name,path in paths.items():
        distance=np.full(xx.shape,np.inf)
        for a,b in zip(path[:-1],path[1:]):
            d=b-a
            s=np.clip(((xx-a[0])*d[0]+(yy-a[1])*d[1])/np.dot(d,d),0,1)
            distance=np.minimum(distance,np.hypot(xx-a[0]-s*d[0],yy-a[1]-s*d[1]))
        letter_masks[name]=distance<=PARAMS['fracture_zone_half_width_m']
        mask|=letter_masks[name]
    assert label(mask)[1]==3,'UPC fracture zones must form three connected components'
    permeability=np.where(mask[:,:,None],PARAMS['equivalent_fracture_zone_permeability_m2'],PARAMS['matrix_permeability_m2'])
    permeability=np.broadcast_to(permeability,(len(x),len(y),len(z))).copy()
    diffusivity=permeability/(PARAMS['fluid_viscosity_Pa_s']*PARAMS['effective_bulk_storage_per_Pa'])*86400.
    lap=operator(diffusivity,spacing)
    assert np.max(abs(lap@np.ones(lap.shape[0])))<1e-9
    wells=[]
    for producer in PARAMS['producers']:
        a,b=producer['xy_m'];z0,z1=producer['completion_z_m']
        footprint=((xx-a)**2+(yy-b)**2<=12.**2)&mask
        completion=footprint[:,:,None]&((z>=z0)&(z<=z1))[None,None,:]
        assert completion.any()
        wells.append(completion.ravel())
    times=np.arange(0,PARAMS['end_day']+PARAMS['dt_days']/2,PARAMS['dt_days'])
    u=np.ones(lap.shape[0]);snapshots=[np.full(permeability.shape,30.,dtype=np.float32)]
    metrics=[];previous_stage=None
    bulk_factor=PARAMS['effective_bulk_storage_per_Pa']*(PARAMS['initial_pressure_MPa']-PARAMS['producer_pressure_MPa'])*1.e6*np.prod(spacing)
    for day in times[1:]:
        active=tuple(i for i,p in enumerate(PARAMS['producers']) if day>p['start_day'])
        if active!=previous_stage:
            fixed=np.logical_or.reduce([wells[i] for i in active]);free=~fixed
            a=sparse.eye(free.sum(),format='csr')+PARAMS['dt_days']*lap[free][:,free]
            invdiag=1/a.diagonal()
            preconditioner=LinearOperator(a.shape,matvec=lambda v:v*invdiag)
            previous_stage=active
        old=u.copy();u[fixed]=0.
        iterations=[0]
        def count(_):iterations[0]+=1
        new,info=cg(a,old[free],x0=old[free],M=preconditioner,rtol=1.e-9,atol=1.e-12,maxiter=2000,callback=count)
        assert info==0,('CG did not converge',day,info)
        residual=float(np.linalg.norm(a@new-old[free])/np.linalg.norm(old[free]))
        u[free]=new
        assert u.min()>-1.e-7 and u.max()<1+1.e-7
        assert np.max(u-old)<1.e-7,'Pressure increased during depletion'
        loss=float((old-u).sum()*bulk_factor)
        production=float((-np.sum((lap@u)[fixed])+(old[fixed]-u[fixed]).sum()/PARAMS['dt_days'])*bulk_factor)
        balance=abs(loss-production*PARAMS['dt_days'])/max(loss,1.e-12)
        pressure=(10+20*u).reshape(permeability.shape)
        snapshots.append(pressure.astype(np.float32))
        metrics.append({'day':float(day),'active_wells':len(active),'iterations':iterations[0],
            'relative_residual':residual,'storage_loss_m3':loss,'production_m3_day':production,
            'relative_volume_balance_error':balance,'minimum_MPa':float(pressure.min()),'maximum_MPa':float(pressure.max())})
        if int(day)%20==0:print(f'day {day:.0f}, CG {iterations[0]}, residual {residual:.2g}, balance {balance:.2g}',flush=True)
    fields=np.stack(snapshots)
    np.savez_compressed(OUT/'upc-pressure-field.npz',x=x,y=y,z=z,days=times,pressure_MPa=fields,
        fracture_mask=mask,**{f'trace_{n}':p for n,p in paths.items()})
    report={'purpose':'Illustrative numerical pressure-diffusion example for the software page; not output from GeoFTSim+.',
        'parameters':PARAMS,'benchmark':benchmark(),'shape':list(fields.shape),'fracture_components':3,
        'pressure_range_MPa':[float(fields.min()),float(fields.max())],
        'max_relative_linear_residual':max(m['relative_residual'] for m in metrics),
        'max_relative_volume_balance_error':max(m['relative_volume_balance_error'] for m in metrics),
        'snapshots_monotone':bool(np.max(np.diff(fields,axis=0))<1e-4),
        'production_steps':metrics,'elapsed_seconds':time.monotonic()-start}
    assert report['max_relative_volume_balance_error']<1.e-5
    (OUT/'model-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['production_steps','parameters']},indent=2),flush=True)


if __name__=='__main__':solve()
