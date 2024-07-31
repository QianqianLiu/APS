%% compare zos in the model of GDDL-ESM4 for scenarios ssp370 and ssp585.
% Compare sea level in 2019 with sea level in 2100. How the sea level
% around the open boundary has changed? Apply this change to our
% hydrodynamic model and see how the sea level rise would affect
% hydrodynamic in the estuary.

%Edited from Zos_CMIP6_GFDL_ESM4.m
%% ssp370
fname='zos_Omon_GFDL-ESM4_ssp370_r1i1p1f1_gn_201501-203412.nc';
lon=ncread(fname,'lon');
lat=ncread(fname,'lat');
zos=ncread(fname,'zos'); % Sea Surface Height Above Geoid (m) - (lat, lon, time)
zos1=ncread('zos_Omon_GFDL-ESM4_ssp370_r1i1p1f1_gn_209501-210012.nc','zos');
zos_2019=zos(:,:,12*4+1:12*5); % slice out 2019
zos_2100=zos1(:,:,12*5+1:12*6); % slice out 2100
load NC_coastline.txt

% SSP 370 
figure
subplot(2,1,1)
pcolor(lon,lat,squeeze(mean(zos_2100,3))-squeeze(mean(zos_2019,3)))
hold on
plot(NC_coastline(:,1),NC_coastline(:,2),'color','r')
colormap('jet')
axis([-78 -73 32.5 37])
caxis([-0.3 0.3])
title('SSP370: 2100 Mean - 2019 Mean')
colorbar

% ssp585
fname='zos_Omon_GFDL-ESM4_ssp585_r1i1p1f1_gn_201501-203412.nc';
lon=ncread(fname,'lon');
lat=ncread(fname,'lat');
zos=ncread(fname,'zos');
zos1=ncread('zos_Omon_GFDL-ESM4_ssp585_r1i1p1f1_gn_209501-210012.nc','zos');
zos_2019=zos(:,:,12*4+1:12*5);
zos_2100=zos1(:,:,12*5+1:12*6);
%load NC_coastline.txt

%Figure
subplot(2,1,2)
pcolor(lon,lat,squeeze(mean(zos_2100,3))-squeeze(mean(zos_2019,3)))
hold on
plot(NC_coastline(:,1),NC_coastline(:,2),'color','r')
colormap('jet')
axis([-78 -73 32.5 37])
caxis([-0.3 0.3])
title('SSP585: 2100 Mean - 2019 Mean')
colorbar

exportgraphics(gcf,'./Zos_comp_GFDL_3Scenarios.png','resolution',300)


%% Look at 5 years average
%%%%%%%%%%%%%%%%
fname='zos_Omon_GFDL-ESM4_ssp370_r1i1p1f1_gn_201501-203412.nc';
lon=ncread(fname,'lon');
lat=ncread(fname,'lat');
zos=ncread(fname,'zos');
zos1=ncread('zos_Omon_GFDL-ESM4_ssp370_r1i1p1f1_gn_209501-210012.nc','zos');

zos_2017to2021=zos(:,:,12*2+1:12*7);
zos_2096to2100=zos1(:,:,12*1+1:12*6);
pcolor(lon,lat,squeeze(mean(zos_2096to2100,3))-squeeze(mean(zos_2017to2021,3)))
hold on
plot(NC_coastline(:,1),NC_coastline(:,2),'color','r')
colormap('jet')
axis([-78 -73 32.5 37])
caxis([-0.3 0.3])
title('SSP370: 5 years around 2098- 5 years around 2019')
colorbar


%%%%%%%%%%%---------
nodes=load('../Input/hgrid_RUN04_node.txt');
obnd=load('OceanOpenBry.txt'); % node number for the ocean open boundary
[Lon,Lat]=my_project_NC(nodes(:,2),nodes(:,3),'reverse');
lono=Lon(obnd); lato=Lat(obnd);


lon=double(lon); lat=double(lat);
for mon=1:12

zos_present=mean(zos_2017to2021(:,:,mon:12:end),3);
zos_future=mean(zos_2096to2100(:,:,mon:12:end),3);
zos_SLR=zos_future-zos_present;
zos_obc=griddata(lon,lat,zos_SLR,lono,lato);
aa=isnan(zos_obc);
[val,id]=min(aa);
zos_obc(1:id-1)=zos_obc(id);

aa=isnan(zos_obc);
[val,id]=max(aa);
zos_obc(id:end)=zos_obc(id-1);

obc_SLR(:,mon)=zos_obc;

Figure
pcolor(lon,lat,zos_future-zos_present)
hold on
plot(NC_coastline(:,1),NC_coastline(:,2),'color','r')
colormap('jet')
axis([-78 -73 32.5 37])
caxis([-0.3 0.3])
title(['SPS370: ',Month(mon)])
colorbar
end

save('Obc_SLR_2098-2019_SSP370.txt','obc_SLR','-ascii')

%%
fname='zos_Omon_GFDL-ESM4_ssp585_r1i1p1f1_gn_201501-203412.nc';
lon=ncread(fname,'lon');
lat=ncread(fname,'lat');
zos=ncread(fname,'zos');
zos1=ncread('zos_Omon_GFDL-ESM4_ssp585_r1i1p1f1_gn_209501-210012.nc','zos');

zos_2017to2021=zos(:,:,12*2+1:12*7);
zos_2096to2100=zos1(:,:,12*1+1:12*6);
pcolor(lon,lat,squeeze(mean(zos_2096to2100,3))-squeeze(mean(zos_2017to2021,3)))
hold on
plot(NC_coastline(:,1),NC_coastline(:,2),'color','r')
colormap('jet')
axis([-78 -73 32.5 37])
caxis([-0.3 0.3])
title('SSP585: 5 years around 2098- 5 years around 2019')
colorbar

%%%%%%%%%%%---------

lon=double(lon); lat=double(lat);
for mon=1:12
zos_present=mean(zos_2017to2021(:,:,mon:12:end),3);
zos_future=mean(zos_2096to2100(:,:,mon:12:end),3);
zos_SLR=zos_future-zos_present;
zos_obc=griddata(lon,lat,zos_SLR,lono,lato);
aa=isnan(zos_obc);
[val,id]=min(aa);
zos_obc(1:id-1)=zos_obc(id);

aa=isnan(zos_obc);
[val,id]=max(aa);
zos_obc(id:end)=zos_obc(id-1);

obc_SLR_585(:,mon)=zos_obc;

% Figure
% pcolor(lon,lat,zos_future-zos_present)
% hold on
% plot(NC_coastline(:,1),NC_coastline(:,2),'color','r')
% colormap('jet')
% axis([-78 -73 32.5 37])
% caxis([-0.3 0.3])
% title(['SSP585: ',Month(mon)])
% colorbar
end

save('Obc_SLR_2098-2019_SSP585.txt','obc_SLR_585','-ascii')



%% SSS585
lon=ncread('zos_Omon_E3SM-1-1_ssp585_r1i1p1f1_gr_201501-201912.nc','lon');
lat=ncread('zos_Omon_E3SM-1-1_ssp585_r1i1p1f1_gr_201501-201912.nc','lat');
zos=ncread('zos_Omon_E3SM-1-1_ssp585_r1i1p1f1_gr_201501-201912.nc','zos');
zos1=ncread('zos_Omon_E3SM-1-1_ssp585_r1i1p1f1_gr_209501-209912.nc','zos');

Figure
subplot(1,2,1)
[xx,yy]=meshgrid(lon,lat);
pcolor(xx,yy,squeeze(zos(:,:,1))')

load /Users/liuq/Documents/Research/NorthCarolinaCoastal/Mesh/NC_coastline.txt
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




