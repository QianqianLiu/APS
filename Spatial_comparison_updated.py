#!/usr/bin/env python3

from pylib import *

gd = read_schism_hgrid("/expanse/lustre/scratch/kboot/temp_project/RUN2002_a/hgrid.gr3")
gd.x, gd.y = proj_pts(gd.x, gd.y, "epsg:26918", "epsg:4326")

C=ReadNC('/expanse/lustre/scratch/kboot/temp_project/RUN2002_a/outputs/schout_49.nc')

close('all')
figure(figsize=[15,6]); set_cmap('jet')

subplot(2,2,1)
print(C.salt.val.data.shape)
gd.plot(fmt=1,value=C.salt.val.data[0,:,20],clim=[0,36.5],ticks=11)
#num2date(datenum(2019, 1, 1) + 240)
title('schout_49.nc; 08-29-2019; Surface Salinity')
setp(gca(),xlim=[-77.5,-74.5],ylim=[33.7,36.5])

subplot(2,2,3)
gd.plot(fmt=1,value=C.temp.val.data[0,:,20]*9/5+32,clim=[30,90],ticks=11)
title('schout_49.nc; 08-29-2019; Surface Temp')
setp(gca(),xlim=[-77.5,-74.5],ylim=[33.7,36.5])

C=ReadNC('/expanse/lustre/scratch/kboot/temp_project/RUN2002_a/outputs/schout_61.nc')
subplot(2,2,2)
gd.plot(fmt=1,value=C.salt.val.data[0,:,20],clim=[0,36.5],ticks=11)
title('schout_49.nc; 10-28-2019; Surface Salinity')
setp(gca(),xlim=[-77.5,-74.5],ylim=[33.7,36.5])

subplot(2,2,4)
gd.plot(fmt=1,value=C.temp.val.data[0,:,20]*9/5+32,clim=[30,90],ticks=11)
title('schout_49.nc; 10-28-2019; Surface Temp')
setp(gca(),xlim=[-77.5,-74.5],ylim=[33.7,36.5])

show(block=False)

savefig('Temp_Salt_Spatial_RUN2002.png')

