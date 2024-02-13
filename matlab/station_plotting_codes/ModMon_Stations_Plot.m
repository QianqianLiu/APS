%% Plot stations in a map using matlab, use one kind of dot for one 
% datatype (red circle for water levels, black square for other stations, 
% etc.) bathymetry background; include text to label station names for each 
% station.

clear;clc;close all 

Elements=load('Elements.txt');
Nodes=load('Nodes.txt');

dep=load('VIMS_depth.txt');

long=Nodes(:,2); % longitude
lati=Nodes(:,3); % latitude
nv=Elements(:,3:5); % elements orig 2:4
depth=griddata(dep(:,2),dep(:,3),dep(:,4),long,lati,'natural');

% % Build Grid w/ no color
% patch('Faces',nv,'Vertices',[long lati],...
% 'FaceVertexCData',depth,'FaceColor','none','EdgeColor','k');
% hold on

%% Bathymetry - Zoomed in scale for focus on APS study area with color

patch('Faces',nv,'Vertices',[long lati],...
'FaceVertexCData',depth,'FaceColor','interp','EdgeColor','none');
caxis([0 10]); %set colormap limits to depth range

colormap();
colorbar;
c = colorbar;
c.Label.String = 'Water Depth (meter)';
hold on;

axis equal; axis([-77.13 -76 34.85 35.25]);
set(gca,'xtick',[-78:1:-74],'xticklabel',num2str([78:-1:74]'),'fontsize',12);
set(gca,'ytick',[33:1:36],'yticklabel',num2str([33:1:36]'),'fontsize',12);
box('on'); grid on %turn box and grid on/off as needed
% % set(gca,'visible','off') %Turns off axis and tickmarks

xlabel('Longitude (^oW)','fontsize',12);
ylabel('Latitude (^oN)','fontsize',12);
hold on

%% Plot Stations

NREsta=xlsread('NRE_Station_Locations.xlsx');
NREsta_num = string(NREsta(1:19 , 1));
NREsta_lat = NREsta(1:19 , 3);
NREsta_lon = NREsta(1:19 , 4);

%NRE Stations that are active include 0, 20, 30, 50, 60, 70, 100, 120, 140,
%160, 180

% Inactive include 10, 40, 80, 90, 110, 130, 150, 170

%for i=(1:19);
for i=[1, 3:4, 6:8, 11, 13, 15, 17, 19];
        plot(NREsta_lon(i),NREsta_lat(i),'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
        text(NREsta_lon(i),NREsta_lat(i), NREsta_num(i), 'Position', [NREsta_lon(i)+0.01, NREsta_lat(i)+0.01],'Color', 'k');
end

dep=load('VIMS_depth.txt');
PSsta=xlsread('PS_Station_Locations.xls');
PSsta_num = PSsta(1:9 , 1);
PSsta_lat = PSsta(1:9 , 4);
PSsta_lon = PSsta(1:9, 5);

for i=(1:9);
    labels = {'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6', 'PS7', 'PS8', 'PS9'};
    plot(PSsta_lon(i),PSsta_lat(i),'Marker','o','MarkerSize',5,'MarkerEdgeColor','w','MarkerFaceColor','w');
    text(PSsta_lon(i),PSsta_lat(i), labels(i), 'Position', [PSsta_lon(i)+0.01, PSsta_lat(i)+0.01],'Color', 'w');
end

%% Alt

title('ModMon Neuse River Estuary Station Locations')

plot(-77.12220,35.21060, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-77.11220,35.21060, '0');
    
plot(-77.09035,35.17793, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-77.08035,35.17793, '10');
plot(-77.07648,35.1533, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-77.06648,35.1533, '20');
plot(-77.03525,35.11375, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-77.06525,35.11375, '30');
plot(-77.03174,35.10972, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-77.02174,35.10972, '40');
plot(-77.0064,35.07952, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-76.9964,35.07952, '50'); 
plot(-76.96925,35.02465, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-77.00925,35.02465, '60');
    
plot(-76.95943,35.01472, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-76.94943,35.02472, '70','Color','w');
plot(-76.94418,34.9986, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-76.98418,34.9886, '80');
plot(-76.9215,34.9905, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-76.9115,34.9905, '90','Color','w');
plot(-76.8755,34.9766, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-76.8655,34.9766, '100','Color','w');
plot(-76.8418,34.9617, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-76.8318,34.9617, '110','Color','w');
plot(-76.81515,34.94888, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-76.80515,34.94888, '120','Color','w');
    
plot(-76.7678,34.9525, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-76.7578,34.9525, '130','Color','w');
plot(-76.7374,34.9661, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-76.7274,34.9661, '140','Color','w');
plot(-76.6977,34.9875, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-76.6877,34.9875, '150','Color','w');
plot(-76.66407,35.0144, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-76.65407,35.0144, '160','Color','w');
plot(-76.5972,35.0274, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-76.5872,35.0274, '170','Color','w');
plot(-76.52602,35.06413, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','w');
    text(-76.51602,35.06413, '180','Color','w');


hold off
exportgraphics(gcf,'ModMonNRE_Station_Locations.png','Resolution',300)