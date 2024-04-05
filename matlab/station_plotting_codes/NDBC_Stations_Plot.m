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
nv=Elements(:,3:5); % elements 
depth=griddata(dep(:,2),dep(:,3),dep(:,4),long,lati,'natural');

% % Build Grid w/ no color
% patch('Faces',nv,'Vertices',[long lati],...
% 'FaceVertexCData',depth,'FaceColor','none','EdgeColor','k');
% hold on

%% Bathymetry - Zoomed in scale for focus on APS study area with color
figure;
patch('Faces',nv,'Vertices',[long lati],...
'FaceVertexCData',depth,'FaceColor','interp','EdgeColor','none');
caxis([0 50]); %set colormap limits to depth range

colormap(); %jet
colorbar;
c = colorbar;
c.Label.String = 'Water Depth (meters)';
hold on;
axis equal; axis([-78 -74.8 33.5 36.5]);
set(gca,'xtick',[-78:1:-74],'xticklabel',num2str([78:-1:74]'),'fontsize',12);
set(gca,'ytick',[33:1:36],'yticklabel',num2str([33:1:36]'),'fontsize',12);
box('on'); 
hold on

% Used for comparison right now
stations = {'8658120', '8658163', '8656483', '8654467', '8652587', '8651370'};
station_names= {'WLON7 - Wilmington, NC','JMPN7 - Wrightsville Beach, NC','BFTN7 - Beaufort, NC','HCGN7 - USCG Station Hatteras, NC','ORIN7 - Oregon Inlet Marina, NC','DUKN7 - Duck Pier, NC'};

lon=[-77.95360000, -77.78670000, -76.67000000, -75.70420000, -75.54810000, -75.74670000]
lat=[34.22750000, 34.21330000, 34.72000000, 35.20860000, 35.79500000,36.18330000]

for i=1:length(stations)
    plot(lon(i),lat(i), 'Marker','diamond','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    %text(lon(i)-0.02,lat(i)+.06, stations(i));
end
%annotation('textbox', [0.01, 0.1, 0.2, 0.4], 'String', station_names, 'BackgroundColor', 'w', 'EdgeColor', 'k', 'FontSize', 10);
xlabel('Longitude (^oW)','fontsize',12);
ylabel('Latitude (^oN)','fontsize',12);
title('Albemarle-Pamlico Sound, North Carolina','fontsize',12);

text(-78.0,34.32, 'WLON7');
text(-77.706,34.213, 'JMPN7');
text(-76.865,34.617, 'BFTN7');
text(-75.804,35.10, 'HCGN7');
text(-75.518,35.846, 'ORIN7');
text(-75.70,36.184, 'DUKN7');
grid('off');
hold off
exportgraphics(gcf,'NDBC_Station_Locations.png','Resolution',300)

%{
plot(-77.954,34.228, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-77.924,34.288, 'WLON7');
plot(-77.786,34.213, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-77.756,34.213, 'JMPN7');
plot(-76.671,34.717, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-76.761,34.817, 'BFTN7');
plot(-75.704,35.209, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-75.804,35.139, 'HCGN7');
plot(-75.548,35.796, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-75.518,35.846, 'ORIN7');
plot(-75.746,36.184, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-75.816,36.084, 'DUKN7');

%}

