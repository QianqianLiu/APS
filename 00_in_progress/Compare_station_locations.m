% Plot stations and bathymetry
clear;clc;close all 
%APS_mesh % create variables for current grid
load hgrid_aps_RUN04d.mat
figure
patch('Faces',nm,'Vertices',[lonm latm],...
    'FaceVertexCData',bathy,'FaceColor','flat','EdgeColor','k');
colormap(jet);
caxis([0 10]);
colorbar;
hold on
xlim([-77 -75]);
ylim([34.5 36.5]);
plot(-76.67000000,34.72000000,'*r') %Beaufort
%ginput() % click to select coords
%{ 
Station coordinates - actual
1 -77.95360000 34.22750000 
2 -77.78670000 34.21330000 
3 -76.67000000 34.72000000 Beaufort
4 -75.70420000 35.20860000
5 -75.54810000 35.79500000 Oregon
6 -75.74670000 36.18330000 
%}

%--> Plot extracted stations versus actual locations

% plot(x,y,bathy) % each is 119604x1

% plot station locations