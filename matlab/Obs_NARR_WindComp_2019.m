%% Compare wind data from NARR and NOAA NDBC HCGN7

% from HCGN7
load HCGN7H_2019.txt %% time in UTC
OBS=HCGN7H_2019;

time2=datenum(OBS(:,1),OBS(:,2),OBS(:,3),OBS(:,4),OBS(:,5),OBS(:,1).*0);
Wdir2=OBS(:,6);
Wnd2=OBS(:,7);
Tair2=OBS(:,14);
Tdew2=OBS(:,16);

% Convert wind speed and direction to Ugeo and Vgeo
RperD=pi/180;
Ugeo2=-Wnd2.*sin(Wdir2*RperD);
Vgeo2=-Wnd2.*cos(Wdir2*RperD);


% wind data from NARR

air1='/Users/qianqianliu/Documents/Research/NorthCarolinaCoastal/Input/sflux/sflux_air_1.0275.nc'
lon=double(ncread(air1,'lon'));
lat=double(ncread(air1,'lat'));

latO=35.209; lonO=-75.704;
[ii,jj]=closest(lon,lat,lonO,latO);

for day=1:365
str1=num2str(1000+day);
filen=['/Users/qianqianliu/Documents/Research/NorthCarolinaCoastal/Input/sflux/sflux_air_1.0',str1(2:4),'.nc'];
uwind1=double(ncread(filen,'uwind',[ii,jj,1],[1,1,inf])); % Surface Eastward Air Velocity (10m AGL)
vwind1=double(ncread(filen,'vwind',[ii,jj,1],[1,1,inf])); % Surface Northward Air Velocity (10m AGL)

uwd(day)=mean(uwind1);
vwd(day)=mean(vwind1);
end



dn=0;
for dd=datenum(2019,1,1):1:datenum(2019,12,31);
    dn=dn+1;
%    ind1=find(time1>=dd & time1<dd+1);
%    ugeo1(dn)=nanmean(Ugeo1(ind1));
%    vgeo1(dn)=nanmean(Vgeo1(ind1));

    ind2=find(time2>=dd & time2<dd+1);
    ugeo2(dn)=nanmean(Ugeo2(ind2));
    vgeo2(dn)=nanmean(Vgeo2(ind2));
end

Figure
set(hfig,'units','inches','position',[0 0 28 4])
set(hfig,'papersize',[28 4],'paperposition',[0 0 28 4])

%subplot(2,1,1)
%yr=[datenum(2011+ii,1,2)-datenum(2012,1,1):datenum(2012+ii,1,1)-datenum(2012,1,1)];
ylabel('m/s','fontsize',14)
feather(uwd,vwd,'r');
hold on
feather(ugeo2,vgeo2,'k');
axis equal; 
set(gca,'xtick',[datenum(2019,1:2:12,1)-datenum(2019,1,1)+1],'xticklabel',datestr([datenum(2019,1:2:12,1)]'))
grid on
%legend([h2 h1],'HCGN7 OBS','NARR','fontsize',12)

title('Daily-averaged Winds in 2019 in m/s (Black: HCGN7 OBS; Red: NARR)')
exportgraphics(gcf,'Wind_NARR_HCGN7_Comp_2019.png','resolution',300)
