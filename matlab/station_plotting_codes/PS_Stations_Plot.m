%% Plot stations in a map using matlab, use one kind of dot for one 
% datatype (red circle for water levels, black square for other stations, 
% etc.) bathymetry background; include text to label station names for each 
% station.

clear;clc;close all 

Elements=load('Elements.txt');
Nodes=load('Nodes.txt');

dep=load('VIMS_depth.txt');
PSsta=xlsread('PS_Station_Locations.xls');
PSsta_num = PSsta(1:9 , 1);
PSsta_lat = PSsta(1:9 , 4);
PSsta_lon = PSsta(1:9, 5);


long=Nodes(:,2); % longitude
lati=Nodes(:,3); % latitude
nv=Elements(:,3:5); % elements 
depth=griddata(dep(:,2),dep(:,3),dep(:,4),long,lati,'natural');


%%

patch('Faces',nv,'Vertices',[long lati],...
'FaceVertexCData',depth,'FaceColor','interp','EdgeColor','none');
caxis([0 25]); %set colormap limits to depth range

colormap(); %jet
colorbar;
c = colorbar;
c.Label.String = 'Water Depth (meter)';
hold on;

axis equal; axis([-76.8 -75.8 34.8 35.4]);
set(gca,'xtick',[-78:1:-74],'xticklabel',num2str([78:-1:74]'),'fontsize',12);
set(gca,'ytick',[33:1:36],'yticklabel',num2str([33:1:36]'),'fontsize',12);
box('on'); grid on %turn box and grid on/off as needed
% % set(gca,'visible','off') %Turns off axis and tickmarks

xlabel('Longitude (^oW)','fontsize',12);
ylabel('Latitude (^oN)','fontsize',12);
hold on

%% Plot Stations

title('Pamlico Sound Stations')

for i=(1:9);
    labels = {'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6', 'PS7', 'PS8', 'PS9'};
    plot(PSsta_lon(i),PSsta_lat(i),'Marker','o','MarkerSize',5,'MarkerEdgeColor','w','MarkerFaceColor','w');
    text(PSsta_lon(i),PSsta_lat(i), labels(i), 'Position', [PSsta_lon(i)+0.01, PSsta_lat(i)+0.01],'Color', 'w');
end

exportgraphics(gcf,'PS_Station_Locations.png','Resolution',300)

