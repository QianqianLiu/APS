#!/usr/bin/env python3
'''
Compute fluxes based on SCHISM node information
'''
from pylib import *

# Annotated by Katy Boot 9/8/2024
#-----------------------------------------------------------------------------
#Input
#hpc: kuro, femto, bora, potomac, james, frontera, levante, stampede2
#ppn:  64,   32,    20,    12,     20,     56,      128,      48
#-----------------------------------------------------------------------------

''' 
Some questions/comments

Is this for combined or uncombined output files?
What value for dx

set 
nspool = 1
ibatch = 0

Uncommented stacks and updated to 73
Adjusted wall time to 20 mins

Matching to other pextract files we've used for validation

'''
#run='/home/g/g260135/work/wangzg/DSP/RUN08a'
run = '/expanse/lustre/projects/unc107/liuquncw/schism/RUN04d/outputs'
svars=['salt'] # update to correct tracer name (ie salt, temp, etc. as per SCHISM variable outputs)
txy = 'transect_ore.bp' # create new file for Oregon inlet transect
#txy=[[[630597.229,630752.001], [4257510.76,4257544.77]],      #1st transect: [xi,yi]
     #'transect_2.bp',                                         #2nd transect; ts2.bp
     #[[519390, 522149, 525018],[4186127, 4180971, 4177533]] ] #3rd transect

sname='RUN04d/flux' # update flux calc output directory # need to create folder or not?

#optional
stacks=[73]    #output stacks # to test, select one stack to break down, otherwise [1,73] for regular run
#nspool=12       #sub-sampling frequency within each stack (1 means all)
nspool=1       #sub-sampling frequency within each stack (1 means all)
#dx=10          #interval of sub-section, used to divide transect
dx=10          #interval of sub-section, used to divide transect ** How many divisions in tr
#prj='cpp'      #projection that convert lon&lat to local project when ics=2
rvars=['salt'] #rname the varibles

#resource requst
#walltime='00:10:00'; nnode=1;  ppn=4
walltime='00:20:00'; nnode=1;  ppn=128

# Updated these values to match pextract from prev jobs
#optional: (frontera,levante,stampede2,etc.)
ibatch     =0              #0: serial mode;  1: parallel mode
qnode      ='expanse'           #specify node name, or default qnode based on HOST will be used
qname      ='compute'           #partition name
account    ='unc107'           #account name
reservation=None           #reservation information
scrout     ='screen.out'   #fname for outout and error

#-----------------------------------------------------------------------------
#on front node: 1). submit jobs first (qsub), 2) running parallel jobs (mpirun) 
#-----------------------------------------------------------------------------
brun=os.path.basename(run); jname='Rd_'+brun; bdir=os.path.abspath(os.path.curdir)
if ibatch==0: os.environ['job_on_node']='1'; os.environ['bdir']=bdir #run locally
if os.getenv('job_on_node')==None:
   if os.getenv('param')==None: fmt=0; bcode=sys.argv[0]; os.environ['qnode']=get_qnode(qnode)
   if os.getenv('param')!=None: fmt=1; bdir,bcode=os.getenv('param').split(); os.chdir(bdir)
   scode=get_hpc_command(bcode,bdir,jname,qnode,nnode,ppn,walltime,scrout,fmt,'param',qname,account,reservation)
   print(scode); os.system(scode); os._exit(0)

#-----------------------------------------------------------------------------
#on computation node
#-----------------------------------------------------------------------------
bdir=os.getenv('bdir'); os.chdir(bdir) #enter working dir
if ibatch==0: nproc=1; myrank=0
if ibatch==1: comm=MPI.COMM_WORLD; nproc=comm.Get_size(); myrank=comm.Get_rank()
if myrank==0: t0=time.time()

#-----------------------------------------------------------------------------
#do MPI work on each core
#-----------------------------------------------------------------------------
if 'nspool' not in locals(): nspool=1       #subsample
if 'rvars' not in locals(): rvars=svars     #rename variables
modules, outfmt, dstacks, dvars, dvars_2d=get_schism_output_info(run+'/outputs',1) #schism outputs info
stacks=arange(stacks[0],stacks[1]+1) if ('stacks' in locals()) else dstacks #check stacks

#check format of transects
if isinstance(txy,str) or array(txy[0]).ndim==1: txy=[txy]
rdp=read_schism_bpfile; txy=[[rdp(i).x,rdp(i).y] if isinstance(i,str) else i for i in txy]

#read grid in outputs folder
fgz=run+'/grid.npz'; fgd=run+'/hgrid.gr3'; fvd=run+'/vgrid.in'
gd=loadz(fgz,'hgrid') if fexist(fgz) else read_schism_hgrid(fgd)
vd=loadz(fgz,'vgrid') if fexist(fgz) else read_schism_vgrid(fvd)

#compute transect information - take point coordinates, divide 
nps,dsa=[],[]; # number of points nps and segment distances (?) dsa
sx,sy,sinds,angles=[],[],[],[]; # x and y coords, segment indices, angles
ns=len(txy); # number of transects (2 points = 1 transect)
pxy=ones(ns).astype('O'); # Create an array of length `ns`, cast to object type.
ipt=0 # track segment indices using ipt
for m,[x0,y0] in enumerate(txy):
    #compute transect pts -- along distance dx or total between the two end points
    x0=array(x0); y0=array(y0)
    if 'dx' in locals():  #divide transect evenly
       ds=abs(diff(x0+1j*y0)); # find segment distance
       s=cumsum([0,*ds]); # cumulative sum of ds segment distances
       npt=int(s[-1]/dx)+1; # find number of points needed for even division of each segment in transect
       ms=linspace(0,s[-1],npt) # generate points until the last point (Transect end)
       xi=interpolate.interp1d(s,x0)(ms); yi=interpolate.interp1d(s,y0)(ms) # interpolate points to transect accordingly
    else:
       xi,yi=x0,y0;
    npt=len(xi); ds=abs(diff(xi+1j*yi))
    if sum(gd.inside_grid(c_[xi,yi])==0)!=0: sys.exit('pts outside of domain: {}'.format(m))
    if 'prj' in locals(): pxi,pyi=proj_pts(xi,yi,'epsg:4326',prj); ds=abs(diff(pxi+1j*pyi))

    #transect property
    angle=array([arctan2(yi[i+1]-yi[i],xi[i+1]-xi[i]) for i in arange(npt-1)])   #angle for each transect subsection
    #pie,pip,pacor=gd.compute_acor(c_[xi,yi]); sigma=(vd.sigma[pip]*pacor[...,None]).sum(axis=1)  #sigma coord.

    nps.append(npt); pxy[m]=c_[xi,yi].T; dsa.append(ds); sx.extend(xi); sy.extend(yi)
    sinds.append(arange(ipt,ipt+npt)); angles.append(angle); ipt=ipt+npt

#compute flux
S=zdata(); S.time=[]; S.flux=[[] for i in txy]; S.tflux=[[[] for i in txy] for i in svars]
for istack in stacks:
    if istack%nproc!=myrank: continue
    t00=time.time(); C=read_schism_output(run,['zcor','hvel',*svars],c_[sx,sy],istack,nspool=nspool,hgrid=gd,vgrid=vd,fmt=1) #read profile
    for m,npt in enumerate(nps): #for each transect
        sind=sinds[m]; angle=angles[m][:,None,None]; ds=dsa[m][:,None,None]
        dz=diff(C.zcor[sind],axis=2); dz=(dz[:-1]+dz[1:])/2; dz[dz<0]=0
        U=C.hvel[sind]; U=(U[:-1,:,:-1]+U[:-1,:,1:]+U[1:,:,:-1]+U[1:,:,1:])/4; u,v=U[...,0],U[...,1]

        #volume flux, and tracers flux
        flx=((sin(angle)*u-cos(angle)*v)*dz*ds).sum(axis=0).sum(axis=1); S.flux[m].extend(flx)
        for n,svar in enumerate(svars):
            T=C.__dict__[svar][sind]; tr=(T[:-1,:,:-1]+T[:-1,:,1:]+T[1:,:,:-1]+T[1:,:,1:])/4
            flx=((sin(angle)*u-cos(angle)*v)*dz*ds*tr).sum(axis=0).sum(axis=1); S.tflux[n][m].extend(flx)
    S.time.extend(C.time); C=None
    print('reading stack {} on rank {}: {:0.2f}'.format(istack,myrank,time.time()-t00)); sys.stdout.flush()
S.time,S.flux,S.tflux=array(S.time),array(S.flux).T,array(S.tflux).T; S.save('.schism_flux_{}'.format(myrank))

#gather flux for all ranks
if ibatch==1: comm.Barrier() 
C=zdata(); C.nps=array(nps); C.xy=pxy; C.xy0=txy; C.time,C.flux=[],[]; tflux=[]
if myrank==0:
   for i in arange(nproc):
       fname='.schism_flux_{}.npz'.format(i); s=read(fname)
       C.time.extend(s.time); C.flux.extend(s.flux); tflux.extend(s.tflux); os.remove(fname)
   it=argsort(C.time); C.time=array(C.time)[it]; C.flux=array(C.flux)[it].T.astype('float32')
   for i,rvar in enumerate(rvars): C.__dict__['flux_'+rvar]=array(tflux)[it][...,i].T.astype('float32')

   #save
   sdir=os.path.dirname(os.path.abspath(sname))
   if not fexist(sdir): os.system('mkdir -p '+sdir)
   savez(sname,C)

#-----------------------------------------------------------------------------
#finish MPI jobs
#-----------------------------------------------------------------------------
if ibatch==1: comm.Barrier()
if myrank==0: dt=time.time()-t0; print('total time used: {} s'.format(dt)); sys.stdout.flush()
sys.exit(0) if qnode in ['bora'] else os._exit(0)
