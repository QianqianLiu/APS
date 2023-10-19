#!/usr/bin/env python3
#create boundary condition based on ORAS5 data
from pylib import *
close("all")

#------------------------------------------------------------------------------
#input
#------------------------------------------------------------------------------
StartT=datenum(2019,1,1); EndT=datenum(2020,1,1); dt=1/24
grd='mb20221128_dp_correct.npz'
dir_oras5='C:/Mobile Bay/SCHISM/BigModel/mb_20220303'
iLP=0; fc=0.5  #iLP=1: remove tidal signal with cutoff frequency fc (day)

ifix=0  #ifix=0: fix ORAS5 nan 1st, then interp;  ifix=1: interp 1st, then fixed nan
#------------------------------------------------------------------------------
#interpolate ORAS5 data to boundary
#------------------------------------------------------------------------------
mtime=arange(StartT,EndT+dt,dt); nt=len(mtime)

#variables for each files
snames=['elev2D.th.nc','TEM_3D.th.nc','SAL_3D.th.nc','uv3D.th.nc']
svars=['sossheig','votemper','vosaline',['vozocrtx','vomecrty']] # variable names in ORAS5
mvars=['elev','temp','salt',['u','v']] # variable names for SCHISM
fnames=['Oras5_modified.nc'] # ORAS5 file names
print(fnames)

#read hgrid
gd=loadz(grd).hgrid; vd=loadz(grd).vgrid; gd.x,gd.y=gd.lon,gd.lat; nvrt=vd.nvrt

#get bnd node xyz
bind=gd.iobn[0]; nobn=gd.nobn[0]
lxi0=gd.x[bind]%360; lyi0=gd.y[bind]; bxy=c_[lxi0,lyi0] #for 2D
lxi=tile(lxi0,[nvrt,1]).T.ravel(); lyi=tile(lyi0,[nvrt,1]).T.ravel() #for 3D
if vd.ivcor==2:
    lzi=abs(compute_zcor(vd.sigma,gd.dp[bind],ivcor=2,vd=vd)).ravel()
else:
    lzi=abs(compute_zcor(vd.sigma[bind],gd.dp[bind])).ravel();
bxyz=c_[lxi,lyi,lzi]
sx0,sy0,sz0=None,None,None

#for each variables
for n,sname in enumerate(snames):
    svar=svars[n]; mvar=mvars[n];
    if isinstance(svar,str): svar=[svar]; mvar=[mvar];

    #interp in space
    S=zdata(); S.time=[]
    [exec('S.{}=[]'.format(i)) for i in mvar];
    C=ReadNC('{}/{}'.format(dir_oras5,fnames[0]),1)
    ctime=array(C.variables['time_counter'])/24+datenum(2018,12,16,0,0,0); sx=double(array(C.variables['nav_lon'][0]))%360
    sy=double(array(C.variables['nav_lat'][0])); sz=double(array(C.variables['deptht'][:])); nz=len(sz)
    fpz=lzi>=sz.max(); lzi[fpz]=sz.max()-1e-6

    if not array_equal(sx,sx0)*array_equal(sy,sy0)*array_equal(sz,sz0):
          sx0 = sx; sy0 = sy; sz0 = sz;
          #get interp index for ORAS5 data
          if ifix==0:
               #sxi,syi=meshgrid(sx,sy);
               sxy=double(c_[sx.ravel(),sy.ravel()]);  
               #exec("cvs=double(array(C.variables['{}'][{}]))".format(svar[0],0)); 
               cvs=array(C.variables['votemper'][0]); sindns=[]; sindps=[]
               for ii in arange(60):
                    print('computing ORAS5 interpation index: level={}/{}'.format(ii,nz)) 
                    cv=cvs[ii]; ds=cv.shape; cv=cv.ravel();
                    fpn=abs(cv)>1e3; sindn=nonzero(fpn)[0]; sindr=nonzero(~fpn)[0];
                    if len(sindr)>0:
                       sindp=sindr[near_pts(sxy[sindn],sxy[sindr])];
                       sindns.append(sindn); sindps.append(sindp)

               #get interp index for pts
               print('get new interp indices: {}'.format(fnames[0]))             
               #sx0=sx.ravel(); sy0=sy.ravel(); sz0=sz[:];
               nsxy = len(lxi0); nsz = int_(len(lzi)/nsxy);
               idx0, idy0 = int_(zeros(nsxy)), int_(zeros(nsxy)); idx, idy = int_(zeros(len(lzi))), int_(zeros(len(lzi)));
               ratx0, raty0 = zeros(nsxy), zeros(nsxy); ratx, raty = zeros(len(lzi)), zeros(len(lzi));
               
               for jj,lxi0i in enumerate(lxi0):
                   dis = square(lxi0i-sx)+square(lyi0[jj]-sy);
                   mindex = argwhere(dis==dis.min());
                   
                   if lxi0i <= sx[mindex[0,0],mindex[0,1]]:
                       idy0[jj] = mindex[0,1]-1
                   else:
                       idy0[jj] = mindex[0,1]

                   if lyi0[jj] <= sy[mindex[0,0],mindex[0,1]]:
                       idx0[jj] = mindex[0,0]-1
                   else:
                       idx0[jj] = mindex[0,0]
                                              
                   idx[jj*nsz:(jj+1)*nsz] = idx0[jj];                     
                   idy[jj*nsz:(jj+1)*nsz] = idy0[jj];
                       
                   ratx0[jj] = (lxi0i-sx[idx0[jj],idy0[jj]])/(sx[idx0[jj],idy0[jj]+1]-sx[idx0[jj],idy0[jj]]);
                   ratx[jj*nsz:(jj+1)*nsz] = ratx0[jj];

                   raty0[jj] =  (lyi0[jj]-sy[idx0[jj],idy0[jj]])/(sy[idx0[jj]+1,idy0[jj]]-sy[idx0[jj],idy0[jj]]);             
                   raty[jj*nsz:(jj+1)*nsz] = raty0[jj];

               idz=((lzi[:,None]-sz[None,:])>=0).sum(axis=1)-1; ratz=(lzi-sz[idz])/(sz[idz+1]-sz[idz])
               ratz[idz<0] = 0;
               idzp1 = idz+1;
               idz[idz<0] = 0;
               
               # figure(figsize=[10,8])
               # levels=[15,15.5,16,16.5,17,17.5,18]
               # cvs0 = cvs[0];
               # cvs0[cvs0>18]=NaN;
               # cvs0[cvs0<15]=NaN;
               # contourf(sx,sy,cvs0,vmin=15,vmax=18,levels=levels, extend='both');colorbar()
               # # plot(lxi0,lyi0,'b.',ms=5)
               # # plot(lxi0[0],lyi0[0],'b.',ms=10)
               # # plot(sx[idx0[0],idy0[0]],sy[idx0[0],idy0[0]],'ro',ms=10)
               # # plot(sx[idx0[0]+1,idy0[0]],sy[idx0[0]+1,idy0[0]],'rs',ms=10)
               # # plot(sx[idx0[0],idy0[0]+1],sy[idx0[0],idy0[0]+1],'rh',ms=10)
               # # plot(sx[idx0[0]+1,idy0[0]+1],sy[idx0[0]+1,idy0[0]+1],'r*',ms=10)
               # scatter(lxi0,lyi0,s=50,c=vi[0,:,20,0],vmin=15, vmax=18);colorbar()
                

    S.time.extend(ctime)
    

    for i, cti in enumerate(ctime):
            for k,svari in enumerate(svar):
                exec("cv=double(array(C.variables['{}'][{}]))".format(svari,i)); mvari=mvar[k]

                #interp in space
                if mvari=='elev':
                    #remove ORAS5 nan pts
                    if ifix==0:
                        sindn,sindp=sindns[0],sindps[0]
                        cv=cv.ravel(); fpn=(abs(cv[sindn])>1e3)*(abs(cv[sindp])<1e3); cv[sindn]=cv[sindp]; fpn=abs(cv)>1e3 #init fix
                        if sum(fpn)!=0: fni=nonzero(fpn)[0]; fri=nonzero(~fpn)[0]; fpi=fri[near_pts(sxy[fni],sxy[fri])]; cv[fni]=cv[fpi] #final fix
                        #fpn=abs(cv.ravel())>1e3; cv.ravel()[fpn]=sp.interpolate.griddata(sxy[~fpn,:],cv.ravel()[~fpn],sxy[fpn,:],'nearest') #old method
                        cv=cv.reshape(ds)

                    #find parent pts
                    v0=array([cv[idx0,idy0],cv[idx0,idy0+1],cv[idx0+1,idy0],cv[idx0+1,idy0+1]])

                    #remove nan in parent pts
                    if ifix==1:
                        for ii in arange(4):fpn=abs(v0[ii])>1e3; v0[ii,fpn]=sp.interpolate.griddata(bxy[~fpn,:],v0[ii,~fpn],bxy[fpn,:],'nearest')

                    #interp
                    v1=v0[0]*(1-ratx0)+v0[1]*ratx0;  v2=v0[2]*(1-ratx0)+v0[3]*ratx0
                    vi=v1*(1-raty0)+v2*raty0

                else:
                    #remove ORAS5 nan pts
                    if ifix==0:
                        for ii in arange(len(sindns)):
                            sindn,sindp=sindns[ii],sindps[ii]
                            cvi=cv[ii].ravel(); fpn=(abs(cvi[sindn])>1e3)*(abs(cvi[sindp])<1e3); cvi[sindn]=cvi[sindp]; fpn=abs(cvi)>1e3 #init fix
                            if sum(fpn)!=0: fni=nonzero(fpn)[0]; fri=nonzero(~fpn)[0]; fpi=fri[near_pts(sxy[fni],sxy[fri])]; cvi[fni]=cvi[fpi] #final fix
                            #fpn=abs(cv[ii].ravel())>1e3; cv[ii].ravel()[fpn]=sp.interpolate.griddata(sxy[~fpn,:],cv[ii].ravel()[~fpn],sxy[fpn,:],'nearest') #old method

                    v0=array([cv[idz,idx,idy],cv[idz,idx,idy+1],cv[idz,idx+1,idy],cv[idz,idx+1,idy+1],
                              cv[idzp1,idx,idy],cv[idzp1,idx,idy+1],cv[idzp1,idx+1,idy],cv[idzp1,idx+1,idy+1]])

                    #remove nan in parent pts
                    if ifix==1:
                        for ii in arange(8): fpn=abs(v0[ii])>1e3; v0[ii,fpn]=sp.interpolate.griddata(bxyz[~fpn,:],v0[ii,~fpn],bxyz[fpn,:],'nearest',rescale=True)

                    v11=v0[0]*(1-ratx)+v0[1]*ratx;  v12=v0[2]*(1-ratx)+v0[3]*ratx; v1=v11*(1-raty)+v12*raty
                    v21=v0[4]*(1-ratx)+v0[5]*ratx;  v22=v0[6]*(1-ratx)+v0[7]*ratx; v2=v21*(1-raty)+v22*raty
                    vi=v1*(1-ratz)+v2*ratz

                #save data
                exec('S.{}.append(vi)'.format(mvari))
    C.close();
    S.time=array(S.time); [exec('S.{}=array(S.{})'.format(i,i)) for i in mvar]

    #interp in time
    for mvari in mvar:
        exec('vi=S.{}'.format(mvari))
        svi=interpolate.interp1d(S.time,vi,axis=0)(mtime)
        if iLP==1: svi=lpfilt(svi,dt,fc) #low-pass
        exec('S.{}=svi'.format(mvari))
    S.time=mtime

    #reshape the data, and save
    [exec('S.{}=S.{}.reshape([{},{},{}])'.format(i,i,nt,nobn,nvrt)) for i in mvar if i!='elev']

    #--------------------------------------------------------------------------
    #create netcdf
    #--------------------------------------------------------------------------
    nd=zdata(); nd.file_format='NETCDF4'

    #define dimensions
    nd.dimname=['nOpenBndNodes', 'nLevels', 'nComponents', 'one', 'time']
    if sname=='elev2D.th.nc':
        snvrt=1; ivs=1; vi=S.elev[...,None,None]
    elif sname=='uv3D.th.nc':
        snvrt=nvrt; ivs=2; vi=c_[S.u[...,None],S.v[...,None]]
    elif sname in ['TEM_3D.th.nc','SAL_3D.th.nc']:
        snvrt=nvrt; ivs=1; exec('vi=S.{}[...,None]'.format(mvar[0]))
    nd.dims=[nobn,snvrt,ivs,1,nt]

    # print(mvar,nd.dims,vi.shape)

    #--time step, time, and time series----
    nd.vars=['time_step', 'time', 'time_series']
    nd.time_step=zdata()
    nd.time_step.attrs=['long_name'];nd.time_step.long_name='time step in seconds'
    nd.time_step.dimname=('one',); nd.time_step.val=array(dt*86400)

    nd.time=zdata()
    nd.time.attrs=['long_name'];nd.time.long_name='simulation time in seconds'
    nd.time.dimname=('time',); nd.time.val=(S.time-S.time[0])*86400

    nd.time_series=zdata()
    nd.time_series.attrs=[]
    nd.time_series.dimname=('time','nOpenBndNodes','nLevels','nComponents')
    nd.time_series.val=vi.astype('float32')

    WriteNC(sname,nd)
