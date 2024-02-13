%07_27

clear;clc;close all
%Figure 

Elements=load('Elements.txt');
Nodes=load('Nodes.txt');

dep=load('VIMS_depth.txt');


long=Nodes(:,2); lati=Nodes(:,3); nv=Elements(:,3:5);
depth=griddata(dep(:,2),dep(:,3),dep(:,4),long,lati,'natural');

%[long,lati]=my_project_NC(x,y,'reverse');

%%Build Figure w/ no color
patch('Faces',nv,'Vertices',[long lati],...
'FaceVertexCData',depth,'FaceColor','none','EdgeColor','k');
box('off'); grid off

% patch('Faces',nv,'Vertices',[long lati],...
% 'FaceVertexCData',depth,'FaceColor','interp','EdgeColor','k');
% 
hold on
set(gca,'visible','off')
exportgraphics(gcf,'SCHISM_Configuration_Grid.png','Resolution',300)


% Color each face "interp" instead of "none" for color


%%
% Med scale plot for NC coastline focus - w/ bathymetry and grid
patch('Faces',nv,'Vertices',[long lati],...
'FaceVertexCData',depth,'FaceColor','interp','EdgeColor','k');
box('on'); grid off

colorbar

hold on

axis equal; axis([-77.1 -75.3 34.5 36.5])
caxis([0 15]); %set colormap limits to depth range
hold on

set(gca,'xtick',[-78:0.5:-74],'xticklabel',num2str([78:-0.5:74]'),'fontsize',12);
set(gca,'ytick',[33:0.5:37],'yticklabel',num2str([33:0.5:37]'),'fontsize',12);
box('on'); grid off

xlabel('Longitude (^oW)','fontsize',12)
ylabel('Latitude (^oN)','fontsize',12)

hold off

%% 
%set(gca,'xtick',[-77:1:-75],'xticklabel',num2str([78:-1:74]'),'fontsize',12);
% set(gca,'ytick',[33:1:36],'yticklabel',num2str([33:1:36]'),'fontsize',12);
% box('off'); grid off
% set(gca,'visible','off')
% xlabel('Longitude (^oW)','fontsize',12)
% ylabel('Latitude (^oN)','fontsize',12)
% exportgraphics(gcf,'SCHISM_Configuration_NCCoastline.png','Resolution',300)
% % % 
% 
 %%
%Zoomed in scale for focus on APS study area - Resolution Focus, no color

% % patch('Faces',nv,'Vertices',[long lati],...
% % 'FaceVertexCData',depth,'FaceColor','none','EdgeColor','k');
% % hold on
% % 
% % axis equal; axis([-77.3 -75.1 34.4 36.6])
% % % % set(gca,'xtick',[-78:1:-74],'xticklabel',num2str([78:-1:74]'),'fontsize',12);
% % % % set(gca,'ytick',[33:1:36],'yticklabel',num2str([33:1:36]'),'fontsize',12);
% % box('off'); grid off %turn box and grid on/off as needed
% % set(gca,'visible','off') %Turns off axis and tickmarks
% % % % xlabel('Longitude (^oW)','fontsize',12)
% % % % ylabel('Latitude (^oN)','fontsize',12)
% % exportgraphics(gcf,'SCHISM_Configuration_APSRegionMesh.png','Resolution',300)

%Zoomed in scale for focus on APS study area - Bathymetry Focus, with color

% patch('Faces',nv,'Vertices',[long lati],...
% 'FaceVertexCData',depth,'FaceColor','interp','EdgeColor','none');
% caxis([0 60]); %set colormap limits to depth range
% %colormap(winter);
% colorbar
% c = colorbar
% c.Label.String = 'Water Depth (meter)'
% hold on
% 
% axis equal; axis([-77.3 -75.1 34.4 36.6])
% set(gca,'xtick',[-78:1:-74],'xticklabel',num2str([78:-1:74]'),'fontsize',12);
% set(gca,'ytick',[33:1:36],'yticklabel',num2str([33:1:36]'),'fontsize',12);
% box('on'); grid on %turn box and grid on/off as needed
% % set(gca,'visible','off') %Turns off axis and tickmarks
% xlabel('Longitude (^oW)','fontsize',12)
% ylabel('Latitude (^oN)','fontsize',12)
% exportgraphics(gcf,'SCHISM_Configuration_APSRegionBathymetry.png','Resolution',300)

%Zoomed in scale for focus on Albemarle Sound
% axis equal; axis([-76.9 -75.3 35.6 36.6])
% set(gca,'xtick',[-78:0.1:-74],'xticklabel',num2str([78:-0.1:74]'),'fontsize',12);
% set(gca,'ytick',[33:0.1:37],'yticklabel',num2str([33:0.1:37]'),'fontsize',12);
% box('on'); grid on
% xlabel('Longitude (^oW)','fontsize',12)
% ylabel('Latitude (^oN)','fontsize',12)
% exportgraphics(gcf,'SCHISM_Configuration_AlbemarleZoom.png','Resolution',300)

%Zoomed in scale for focus on Pamlico Sound

% axis equal; axis([-77.1 -75.3 34.5 35.7])
% set(gca,'xtick',[-78:0.1:-74],'xticklabel',num2str([78:-0.1:74]'),'fontsize',12);
% set(gca,'ytick',[33:0.1:37],'yticklabel',num2str([33:0.1:37]'),'fontsize',12);
% box('on'); grid on
% xlabel('Longitude (^oW)','fontsize',12)
% ylabel('Latitude (^oN)','fontsize',12)
% exportgraphics(gcf,'SCHISM_Configuration_PamlicoZoom.png','Resolution',300)

%Zoomed in scale for resolution of open ocean through inlet

patch('Faces',nv,'Vertices',[long lati],...
'FaceVertexCData',depth,'FaceColor','interp','EdgeColor','k');
caxis([-10 40]); %set colormap limits to depth range
hold on

axis equal; axis([-76.8 -76.2 35.9 36.27])

set(gca,'xtick',[-78:0.1:-74],'xticklabel',num2str([78:-0.1:74]'),'fontsize',12);
set(gca,'ytick',[33:0.1:37],'yticklabel',num2str([33:0.1:37]'),'fontsize',12);
box('on'); grid on
xlabel('Longitude (^oW)','fontsize',12)
ylabel('Latitude (^oN)','fontsize',12)
exportgraphics(gcf,'SCHISM_Configuration_NeuseZoom.png','Resolution',300)

%% Check for terminal nodes
fl=0;
for N=1:size(Nodes,1)
    NinE=find(Elements(:,2:4)==N);
    if size(NinE)<=1
        fl=fl+1;
        TerminalNodes(fl)=N;
    end
end

if fl==0
    disp('No Terminal Node founded')
end

%% cfl condition
load cfl.txt;
lon=Nodes(:,2); lat=Nodes(:,3);

scfl=find(cfl>=3 & cfl<=5);
for i=1:size(scfl)
plot(lon(Elements(scfl(i),2:4)), lat(Elements(scfl(i),2:4)),'*y');
hold on
end

scfl=find(cfl<=3);
for i=1:size(scfl)
plot(lon(Elements(scfl(i),2:4)), lat(Elements(scfl(i),2:4)),'*r');
hold on
end
scfl=find(cfl<=2);
for i=1:size(scfl)
plot(lon(Elements(scfl(i),2:4)), lat(Elements(scfl(i),2:4)),'*g');
hold on
end

lon=long; lat=lati;

for i=1:size(Elements,1)
EN=Elements(i,2:4);
lone=lon(EN); late=lat(EN);
d1=pos2dist(lone(1),late(1),lone(2),late(2),1);
d2=pos2dist(lone(1),late(1),lone(3),late(3),1);
d3=pos2dist(lone(2),late(2),lone(3),late(3),1);
DeltaL(i)=mean([d1 d2 d3]).*1000;
end


[x,y]=my_project_NC(lon,lat,'forward');
for i=1:size(x,1)
xt=x(i);
yt=y(i);
xx=x; yy=y;
xx(i)=0; yy(i)=0;

dist = abs( (xx-xt) + sqrt(-1)*(yy-yt));
[iix,jjx] = find(dist==min(dist(:)));

res(i)=min(dist(:));%% Resolution of mesh - closest distance from surrounding nodes to each node. 
end
%%You can get the minimum resolution by the command of min(res)


patch('Faces',nv,'Vertices',[lon lat],'FaceVertexCData',res'.*1e3,'FaceColor','interp','EdgeColor','none')
%%patch('Faces',nv,'Vertices',[lon lat],'FaceVertexCData',res');
h=colorbar('position',[0.8 0.35 0.02 0.2]); ylabel(h,'Horizontal Resolution (meter)','fontsize',14);
caxis([0 1200])

p = patch('Faces',nv,'Vertices',[lon lat],'FaceVertexCData',res');
p.FaceColor = 'interp';
colorbar
caxis([0 1200])



D=mean([depth(EN)]);
CFL=DeltaL./sqrt(9.81.*D);
Figure
patch('Faces',Elements(:,2:4),'Vertices',[Nodes(:,2) Nodes(:,3)],...
'FaceVertexCData',0.*depth,'FaceColor','none','EdgeColor','k');
hold on
scfl=find(CFL<=3);
for i=1:length(scfl)
plot(lon(Elements(scfl(i),2:4)), lat(Elements(scfl(i),2:4)),'*g');
hold on
end


scfl=find(CFL<=2);
for i=1:length(scfl)
plot(lon(Elements(scfl(i),2:4)), lat(Elements(scfl(i),2:4)),'*r');
hold on
end


scfl=find(CFL>=3 & CFL<=5);
for i=1:length(scfl)
plot(lon(Elements(scfl(i),2:4)), lat(Elements(scfl(i),2:4)),'*y');
hold on
end