clear; close all

%% read grid information
fname='hgrid.gr3';
fid=fopen(fname,'r');
char=fgetl(fid);
tmp1=str2num(fgetl(fid));
fclose(fid);

ne=fix(tmp1(1));
np=fix(tmp1(2));

fid=fopen(fname);
c1=textscan(fid,'%d%f%f%f',np,'headerLines',2);
fclose(fid);
fid=fopen(fname);
c2=textscan(fid,'%d%d%d%d%d%d',ne,'headerLines',2+np);
fclose(fid);

x=c1{2}(:);
y=c1{3}(:);
bathy=c1{4}(:);
i34=c2{2}(:);

nm(1:ne,1:4)=nan;
for i=1:ne
  for j=1:i34(i)
    nm(i,j)=fix(c2{j+2}(i));
  end %for j
end %for i

close all;


%% Elements and Nodes in SCHISM Configuration

salt=squeeze(ncread('schout_50.nc','salt',[32,1,1],[1,Inf,Inf]));
salt=double(salt);
hvel=squeeze(ncread('schout_50.nc','hvel',[1,32,1,1],[2,1,Inf,Inf]));
uu=squeeze(double(hvel(1,:,:)));
vv=squeeze(double(hvel(2,:,:)));

Node=load('node.txt');  
lonm=Node(:,2);
latm=Node(:,3);

load('NC_coastline.txt')

% load SurfaceU_Day216_to_275.mat
% load SurfaceV_Day216_to_275.mat
% 
% load BottomTemp_Day216_to_275.mat
% clear temp
lay=1; %20 for surface; 1 for bottom;

%% winds in August and September of 2016
% % % load /Users/qianqianliu/Documents/MATLAB/MuskegonLake/Met/MKGM4_h2016_09.txt % September
% % % load /Users/qianqianliu/Documents/MATLAB/MuskegonLake/Met/MKGM4_h2016_08.txt % September
% % % mkgm4=MKGM4_h2016_08;
% % % time1=datenum(mkgm4(:,1),mkgm4(:,2),mkgm4(:,3),mkgm4(:,4),mkgm4(:,5),mkgm4(:,1).*0);
% % % Wdir1=mkgm4(:,6);
% % % Wnd1=mkgm4(:,7);
% % % % Convert wind speed and direction to Ugeo and Vgeo
% % % RperD=pi/180;
% % % Ugeo1=-Wnd1.*sin(Wdir1*RperD); %% winds in August
% % % Vgeo1=-Wnd1.*cos(Wdir1*RperD);
% % % 
% % % mkgm4=MKGM4_h2016_09;
% % % time2=datenum(mkgm4(:,1),mkgm4(:,2),mkgm4(:,3),mkgm4(:,4),mkgm4(:,5),mkgm4(:,1).*0);
% % % Wdir2=mkgm4(:,6);
% % % Wnd2=mkgm4(:,7);
% % % % Convert wind speed and direction to Ugeo and Vgeo
% % % RperD=pi/180;
% % % Ugeo2=-Wnd2.*sin(Wdir2*RperD); %% winds in September
% % % Vgeo2=-Wnd2.*cos(Wdir2*RperD);
% % % time=cat(1,time1,time2);
% % % ugeo=cat(1,Ugeo1,Ugeo2);
% % % vgeo=cat(1,Vgeo1,Vgeo2);

%%
Figure
set(hfig,'units','inches','position',[0 0 10 8])
set(hfig,'papersize',[10 8],'paperposition',[0 0 10 8])


%% can choose the points that can form the griddata
xx=linspace(-77.5,-74.5,120);
yy=linspace(33.5,36.5,80);
[xx,yy]=meshgrid(xx,yy);

% % xx2=linspace(-77.5,-74.5,240);
% % yy2=linspace(33.5,36.5,160);
% % [xx2,yy2]=meshgrid(xx2,yy2);

fl=0;
for i=1:120
    for j=1:80
        fl=fl+1;
        loc(fl)=closest(lonm,latm,xx(j,i),yy(j,i));
    end
end

Loc_uniq=uniq(loc);


x1=-77.5; x2=-75; y1=34.5; y2=36; 
 LL=pos2dist(y1,x1,y1,x2,2);
 WW=pos2dist(y1,x1,y2,x1,2);
 
%lonm(1)=-86.29; latm(1)=43.2;
scale=0.1;step=2;
for i=1:size(uu,2)
%%axes('position',[0.1 0.4 0.8 0.55])
% axes('position',[0.1 0.2 0.8 0.7])

%% salinity

patch('Faces',nm(:,1:4),'Vertices',[lonm latm],'FaceVertexCData',squeeze(salt(:,i)),'FaceColor','interp','EdgeColor','None');

hold on

U=squeeze(uu(:,i));                                           %153+i)); % this for daily data
V=squeeze(vv(:,i)); %153+i)); % this for daily data
quiver(lonm(Loc_uniq),latm(Loc_uniq),U(Loc_uniq)*scale,V(Loc_uniq)*scale,'autoscale','off','color','w')
hold on
plot(NC_coastline(:,1),NC_coastline(:,2),'-k','linewidth',2)

% % S=griddata(lonm,latm,salt(:,i),xx2,yy2);
% % pcolor(xx2,yy2,S)
%quiver(lonm(1:step:end),latm(1:step:end),U(1:step:end)*scale,V(1:step:end)*scale,'autoscale','off','color','k')
%% what about only look at direction?
% % uamp=sqrt(U.^2+V.^2);
% % udir=U./uamp; vdir=V./uamp;
% % patch('Faces',Elements(:,2:4),'Vertices',[lonm latm],...
% % 'FaceVertexCData',uamp,'FaceColor','interp','EdgeColor','none');
% % hold on
% % quiver(lonm(1:step:end),latm(1:step:end),udir(1:step:end)*scale,vdir(1:step:end)*scale,'autoscale','off','color','k')


caxis([0 0.2])

hold on
%%%%plot(lon,lat,'.k')
%text(-86.346,43.26,['Bottom Temperature on ', datestr(datenum(2016,9,2+1,i,0,0))],'fontsize',14,'color','r');
title(['Surface Salinity on ', datestr(datenum(2019,9,2,i,0,0))],'fontsize',14,'color','r');

% datestr(datenum(datenum(2016,3,0)+153+i))
grid on
axis([x1 x2 y1 y2])
box on
set(gca,'xtick',[-77.5:0.5:-74.5],'xticklabel',num2str(-[-77.5:0.5:-74.5]'));
xlabel('Longitude (^oW)')
ylabel('Latitude (^oN)')
set(gca,'ytick',[33.5:0.5:36.5],'yticklabel',num2str([33.5:0.5:36.5]'));
pbaspect([LL/WW, 1,1])

cmap=colormap(jet);
hc=colorbar;
caxis([0 35])
ylabel(hc,'PSU')

%patch('Faces',inv,'Vertices',[lonm lat],'FaceVertexCData',rem','FaceColor','none','EdgeColor',[.5 .5 .5])
%'FaceVertexCData',h,'FaceColor','interp','EdgeColor','None');

%hc=colorbar('location','south','position',[0.5 0.46 0.4 0.02]);
%hc=colorbar('location','south','position',[0.5 0.28 0.4 0.02]);
%
%colormap(cmap_bgr)

%% Plot DO
% % % % axes('position',[0.1 0.1 0.8 0.28])
% % % % h7=plot(Time,DO(:,1),'color',[.5 .5 0],'linewidth',2);
% % % % hold on;grid on
% % % % h8=plot(Time,DO(:,4),'color',[0 .5 .5],'linewidth',2);
% % % % 
% % % % legend([h7 h8],'2 meter DO','11 meter DO');
% % % % set(gca,'xtick',datenum(2016,8,1:15:90),'xticklabel',datestr(datenum(2016,8,1:15:90)),'fontsize',12)
% % % % set(gca,'xlim',[datenum(2016,8,1) datenum(2016,10,1)],'ylim',[0 150])
% % % % hold on
% % % % plot(datenum(2016,8,3,i,0,0)+[0 0],[0 160],'-.k','linewidth',2);
% % % % 
% % % % ylabel('DO (%)','fontsize',12)
% % % % h=gca;
% % % % h.XTickLabelRotation=16;


% % tt=datenum(2016,8,3,i,0,0); tt2=datenum(2016,8,3,i+1,0,0);
% % tindx=find(time>=tt & time<tt2);
% % uwnd=nanmean(ugeo(tindx)); vwnd=nanmean(vgeo(tindx));
% % q=quiver(-86.34,43.27,uwnd*0.005,vwnd*0.005,'autoscale','off','color','k','linewidth',3);
% % q.MaxHeadSize=1;
% % axis equal;axis([-86.38 -86.246 43.2 43.28])
% % 
% % %%text(-86.33,43.27,'Wind at NOAA C-MAN Station','fontsize',16)
% % text(-86.33,43.27,['Wind at C-MAN: ',num2str(mag,'%3.1f'),' m/s'],'fontsize',16)

MM(:,i)=getframe(hfig);%,[0 0 560 420]);%getframe(gca);
clf
end


save /Users/qianqianliu/Documents/MATLAB/mpgwrite/src/Animation_Salt_APS_2019.mat MM cmap

%%oad cmap_bgr.mat


video = VideoWriter('Salt_APS_RUN02b.avi', 'Uncompressed AVI');
video.FrameRate = 10;
open(video)
writeVideo(video, MM);
close(video);

% % cmap=jet;
% % % save Movie_TopVel_hrly.mat MM cmap_bgr
% % mpgwrite([MM;MM;MM;],cmap,'TopSalt_APS_hrly', 1)


%% Wind at NOAA MKGM4 C-MAN Station


%save BottomTemp_Day216_to_275.mat temp Elements lonm latm lon lat 

%save Movie_TopT_Mus2_hrly.mat MM cmap_bgr
%cd /Users/qianqianliu/Documents/MATLAB/TOOLS/mpgwrite/src/
%mpgwrite([MM;MM;MM;MM;MM;], cmap_bgr, 'TopT_Mus2_hrly', 1)

%save Movie_BotT_Mus2_hrly.mat MM cmap_bgr
%cd /Users/qianqianliu/Documents/MATLAB/TOOLS/mpgwrite/src/
%mpgwrite([MM;MM;MM;MM;MM;MM;MM;], cmap_bgr, 'BotT_Mus2_hrly', 1)

%suptitle('Bottom Temperature for MUS2 at the beginning of September')
%print('-depsc2','BottomT_Mus2')

