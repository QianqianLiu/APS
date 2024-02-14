#!/usr/bin/env python3

from pylib import *

gd = read_schism_hgrid("/expanse/lustre/scratch/kboot/temp_project/RUN2002a/hgrid.gr3")
gd.x, gd.y = proj_pts(gd.x, gd.y, "epsg:26918", "epsg:4326")

hindcast_model='RUN04d'
hindcast_name='2019'
compare_model='RUN2002a'
compare_name='2002'

######################### Read selected .nc output files ####################
C=ReadNC('/expanse/lustre/scratch/kboot/temp_project/RUN2002a/outputs/schout_49.nc')
H=ReadNC('/expanse/lustre/scratch/liuquncw/temp_project/schism/RUN04d/outputs/schout_49.nc')
temp_dif1 = H.temp.val.data[0,:,20] - C.temp.val.data[0,:,20]

C2=ReadNC('/expanse/lustre/scratch/kboot/temp_project/RUN2002a/outputs/schout_61.nc')
H2 = ReadNC('/expanse/lustre/scratch/liuquncw/temp_project/schism/RUN04d/outputs/schout_61.nc')

salt_dif2 = C2.temp.val.data[0,:,20] - H2.temp.val.data[0,:,20]

close('all')
figure(figsize=[12,3]); set_cmap('bwr')

subplot(1,2,1)
print(C.temp.val.data.shape)
gd.plot(fmt=1,value=temp_dif1,clim=[-2,2],ticks=11)
title('08-29; {}-{} WL'.format(hindcast_name,compare_name))
setp(gca(),xlim=[-77.397,-75.377],ylim=[34.537,35.617])

subplot(1,2,2)
gd.plot(fmt=1,value=temp_dif2,clim=[-2,2],ticks=10)
title('10-28; {}-{} WL'.format(hindcast_name, compare_name))
setp(gca(),xlim=[-77.397,-75.377],ylim=[34.537,35.617])

plt.subplots_adjust(top=0.75)
plt.suptitle('Spatial Comparison of Temperature - {} v {} Hindcast - Pamlico Sound'.format(hindcast_name, compare_name), fontsize = 20)

savefig('/expanse/lustre/projects/unc108/kboot/ModelResults/{}/figures/Temp_Spatial_{}v{}_pamlico.png'.format(compare_model, hindcast_name, compare_name))

########################### Albemarle Sound Figure #######################

close('all')
figure(figsize=[12,3]); set_cmap('bwr')

subplot(1,2,1)
print(C.temp.val.data.shape)
gd.plot(fmt=1,value=temp_dif1,clim=[-2,2],ticks=11)
title('08-29; {}-{} WL'.format(hindcast_name, compare_name))
setp(gca(),xlim=[-76.894,-75.278],ylim=[35.467,36.798])

subplot(1,2,2)
gd.plot(fmt=1,value=temp_dif2,clim=[-2,2],ticks=11)
title('10-28; {}-{} WL'.format(hindcast_name, compare_name))
setp(gca(),xlim=[-76.894,-75.278],ylim=[35.467,36.798])
plt.subplots_adjust(top=0.75)
plt.suptitle('Spatial Comparison of Temperature - {} v {} Hindcast - Albemarle Sound'.format(hindcast_name, compare_name), fontsize = 20)

savefig('/expanse/lustre/projects/unc108/kboot/ModelResults/{}/figures/Temp_Spatial_{}v{}_albemarle.png'.format(compare_model, hindcast_name, compare_name))
