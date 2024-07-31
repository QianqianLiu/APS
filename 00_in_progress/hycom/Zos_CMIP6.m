%% compare zos in the model of E3SM-2-0 for scenarios ssp370 and ssp585.
% Compare sea level in 2019 with sea level in 2100. How the sea level
% around the open boundary has changed? Apply this change to our
% hydrodynamic model and see how the sea level rise would affect
% hydrodynamic in the estuary.


%% ssp370

%ncdisp('/Users/kboothomefolder/Library/CloudStorage/OneDrive-UNC-Wilmington/SCHISM_NC/Matlab/CMIP6/zos_Omon_E3SM-2-0_ssp370_r3i1p1f1_gr_209501-210012.nc','lon');

lon=ncread('zos_Omon_E3SM-2-0_ssp370_r3i1p1f1_gr_201501-202412.nc','lon');
lat=ncread('zos_Omon_E3SM-2-0_ssp370_r3i1p1f1_gr_209501-210012.nc','lat');
zos=ncread('zos_Omon_E3SM-2-0_ssp370_r3i1p1f1_gr_201501-202412.nc','zos');
zos1=ncread('zos_Omon_E3SM-2-0_ssp370_r3i1p1f1_gr_209501-210012.nc','zos');

Figure
subplot(1,2,1)
[xx,yy]=meshgrid(lon,lat);
pcolor(xx,yy,squeeze(zos(:,:,1))')

load NC_coastline.txt
hold on
plot(NC_coastline(:,1)+360,NC_coastline(:,2),'color','r')
colormap('jet')
axis([-78+360 -72+360 30 38])
caxis([-0.2 0.2])
title('SPS370: 2015')
colorbar

subplot(1,2,2)
pcolor(xx,yy,squeeze(zos1(:,:,1))')
hold on
plot(NC_coastline(:,1)+360,NC_coastline(:,2),'color','r')
colormap('jet')
axis([-78+360 -72+360 30 38])
caxis([-0.2 0.2])
title('SPS370: 2095')
colorbar


%% SPS585
lon=ncread('zos_Omon_E3SM-1-1_ssp585_r1i1p1f1_gr_201501-201912.nc','lon');
lat=ncread('zos_Omon_E3SM-1-1_ssp585_r1i1p1f1_gr_201501-201912.nc','lat');
zos=ncread('zos_Omon_E3SM-1-1_ssp585_r1i1p1f1_gr_201501-201912.nc','zos');
zos1=ncread('zos_Omon_E3SM-1-1_ssp585_r1i1p1f1_gr_209501-209912.nc','zos');

Figure
subplot(1,2,1)
[xx,yy]=meshgrid(lon,lat);
pcolor(xx,yy,squeeze(zos(:,:,1))')

load NC_coastline.txt
hold on
plot(NC_coastline(:,1)+360,NC_coastline(:,2),'color','r')
colormap('jet')
axis([-78+360 -72+360 30 38])
caxis([-0.2 0.2])
title('SPS585: 2015')
colorbar

subplot(1,2,2)
pcolor(xx,yy,squeeze(zos1(:,:,1))')
hold on
plot(NC_coastline(:,1)+360,NC_coastline(:,2),'color','r')
colormap('jet')
axis([-78+360 -72+360 30 38])
caxis([-0.2 0.2])
title('SPS585: 2095')
colorbar