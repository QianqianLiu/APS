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

patch('Faces',nv,'Vertices',[long lati],...
'FaceVertexCData',depth,'FaceColor','interp','EdgeColor','none');
caxis([0 50]); %set colormap limits to depth range

colormap(); %jet
colorbar;
c = colorbar;
c.Label.String = 'Water Depth (meter)';
hold on;

axis equal; axis([-78 -74.8 33.5 36.5]);
set(gca,'xtick',[-78:1:-74],'xticklabel',num2str([78:-1:74]'),'fontsize',12);
set(gca,'ytick',[33:1:36],'yticklabel',num2str([33:1:36]'),'fontsize',12);
box('on'); grid on %turn box and grid on/off as needed
% % set(gca,'visible','off') %Turns off axis and tickmarks

xlabel('Longitude (^oW)','fontsize',12);
ylabel('Latitude (^oN)','fontsize',12);
hold on
%% Plot Stations

title('Monitoring Station Locations')

% Used for comparison right now
%stations= [8658120, 8658163, 8656483, 8654467, 8652587, 8651370];
%station_names= ['WLON7, Wilmington, NC','JMPN7 - Wrightsville Beach, NC','BFTN7 Beaufort, NC','HCGN7 - USCG Station Hatteras, NC','ORIN7 - Oregon Inlet Marina, NC','DUKN7 - Duck Pier, NC'];

% lon=[77.95360000, -77.78670000, -76.67000000, -75.70420000, -75.54810000,
% -75.74670000]
% lat=[34.22750000, 34.21330000, 34.72000000, 35.20860000, 35.79500000,
% 36.18330000]

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

%{
% NOAA NDBC
%plot(-75.454,35.010, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k'); text(-75.424,35.010, '41025');
%plot(-74.842,36.609, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');%text(-74.812,36.609, '44014');
plot(-75.593,36.258, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-75.563,36.258, '44100');
plot(-75.714,36.200, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-75.884,36.300, '44056');
    
plot(-75.421,36.001, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-75.391,36.001, '44086');
plot(-75.330,35.750, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-75.300,35.750, '44095'); 
plot(-75.454,35.010, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-75.424,35.010, '41025');
plot(-76.949,34.213, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-77.019,34.303, '41159'); 
plot(-76.949,34.207, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-77.059,34.137, '41064');  
plot(-77.362,33.988, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-77.332,33.988, '41037');
plot(-77.715,34.142, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-77.685,34.142, '41110');
plot(-77.715,34.141, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-77.785,34.071, '41038'); 
%plot(-77.764,33.441, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    %text(-77.734,33.441, '41013');
%plot(-78.016,33.722, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    %text(-77.986,33.722, '41108');
%plot(-78.477,33.837, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    %text(-78.447,33.837, '41024');
    
plot(-75.739,36.190, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-75.689,36.190, 'FRFN7');  

plot(-76.525,34.622, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    text(-76.495,34.622, 'CLKN7');


%}
%%%%% These stations outside of model mesh area    
%plot(-72.196,34.751, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    %text(-72.166,34.751, '41001');
%plot(-74.945,31.760, 'Marker','o','MarkerSize',5,'MarkerEdgeColor','k','MarkerFaceColor','k');
    %text(-74.915,31.760, '41002');

hold off
exportgraphics(gcf,'figures/NDBC_Station_Locations.png','Resolution',300)