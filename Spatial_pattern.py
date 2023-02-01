#!/usr/bin/env python3

from pylib import *

gd = read_schism_hgrid("/home/bootk/schism/RUN01d/hgrid.gr3")
gd.x, gd.y = proj_pts(gd.x, gd.y, "epsg:26918", "epsg:4326")

C=ReadNC('/home/bootk/schism/RUN01d/outputs/schout_49.nc')
#C=ReadNC('/home/bootk/schism/RUN02d/outputs/')

close('all')
figure(figsize=[15,6]); set_cmap('jet')
subplot(3,3,1)
gd.plot(fmt=1,value=C.salt.val.data[0,:,0],clim=[0,34],ticks=11)
title('schout_49.nc; time: 1; layer 1')

subplot(3,3,2)
gd.plot(fmt=1,value=C.salt.val.data[0,:,14],clim=[0,34],ticks=11)
title('schout_49.nc; time: 1; layer 15')


subplot(3,3,3)
gd.plot(fmt=1,value=C.salt.val.data[0,:,31],clim=[0,34],ticks=11)
title('schout_49.nc; time: 1; layer 32')


subplot(3,3,4)
gd.plot(fmt=1,value=C.salt.val.data[59,:,0],clim=[0,34],ticks=11)
title('schout_49.nc; time: 60; layer 1')


subplot(3,3,5)
gd.plot(fmt=1,value=C.salt.val.data[59,:,14],clim=[0,34],ticks=11)
title('schout_49.nc; time: 60; layer 15')

subplot(3,3,6)
gd.plot(fmt=1,value=C.salt.val.data[59,:,31],clim=[0,34],ticks=11)
title('schout_49.nc; time: 60; layer 32')


subplot(3,3,7)
gd.plot(fmt=1,value=C.salt.val.data[119,:,0],clim=[0,34],ticks=11)
title('schout_49.nc; time: 120; layer 1')

subplot(3,3,8)
gd.plot(fmt=1,value=C.salt.val.data[119,:,14],clim=[0,34],ticks=11)
title('schout_49.nc; time: 120; layer 15')

subplot(3,3,9)
gd.plot(fmt=1,value=C.salt.val.data[119,:,31],clim=[0,34],ticks=11)
title('schout_49.nc; time: 120; layer 32')

show(block=False)

num2date(240+datenum(2019,1,1))
savefig('Salt_schout49_RUN01d.png')



close('all')
figure(figsize=[15,6]); set_cmap('jet')
subplot(3,3,1)
gd.plot(fmt=1,value=C.salt.val.data[0,:,0],clim=[0,34],ticks=11)
title('schout_49.nc; time: 1; layer 1')
setp(gca(),xlim=[-77,-75],ylim=[34.5,36.5])

subplot(3,3,2)
gd.plot(fmt=1,value=C.salt.val.data[0,:,14],clim=[0,34],ticks=11)
title('schout_49.nc; time: 1; layer 15')
setp(gca(),xlim=[-77,-75],ylim=[34.5,36.5])

subplot(3,3,3)
gd.plot(fmt=1,value=C.salt.val.data[0,:,34],clim=[0,34],ticks=11)
ylabel('Latitude ($\mathregular{^o}$N)')
xlabel('Longitude ($\mathregular{^o}$W)')
xts=[-78,-77,-76,-75,-74]
xls=[str(-i) for i in xts]
setp(gca(),xticks=xts,xticklabels=xls)
set_cmap("jet")
#title('schout_49.nc; time: 1; layer 35')
title('Surface Salinity on 29 August 2019') #,num2str(datenum(2019,1,1)+240))
setp(gca(),xlim=[-77,-75],ylim=[34.5,36.5])

subplot(3,3,4)
gd.plot(fmt=1,value=C.salt.val.data[59,:,0],clim=[0,34],ticks=11)
title('schout_49.nc; time: 60; layer 1')
setp(gca(),xlim=[-77,-75],ylim=[34.5,36.5])

subplot(3,3,5)
gd.plot(fmt=1,value=C.salt.val.data[59,:,14],clim=[0,34],ticks=11)
title('schout_49.nc; time: 60; layer 15')
setp(gca(),xlim=[-77,-75],ylim=[34.5,36.5])

subplot(3,3,6)
gd.plot(fmt=1,value=C.salt.val.data[59,:,34],clim=[0,34],ticks=11)
title('schout_49.nc; time: 60; layer 35')
setp(gca(),xlim=[-77,-75],ylim=[34.5,36.5])

subplot(3,3,7)
gd.plot(fmt=1,value=C.salt.val.data[119,:,0],clim=[0,34],ticks=11)
title('schout_49.nc; time: 120; layer 1')
setp(gca(),xlim=[-77,-75],ylim=[34.5,36.5])

subplot(3,3,8)
gd.plot(fmt=1,value=C.salt.val.data[119,:,14],clim=[0,34],ticks=11)
title('schout_49.nc; time: 120; layer 15')
setp(gca(),xlim=[-77,-75],ylim=[34.5,36.5])

subplot(3,3,9)
gd.plot(fmt=1,value=C.salt.val.data[119,:,34],clim=[0,34],ticks=11)
title('schout_49.nc; time: 120; layer 35')
setp(gca(),xlim=[-77,-75],ylim=[34.5,36.5])

show(block=False)

num2date(240+datenum(2019,1,1))
savefig('Salt_schout49.png')


