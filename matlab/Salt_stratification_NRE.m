clear;clc;close all
APS_mesh

load salt_tsi_run04d.mat
salt_tops_04d=salt_si;

load salt_bsi_run04d.mat
salt_bots_04d=salt_si;

salt_strat_04d=salt_bots_04d-salt_tops_04d;


load salt_tsi_ssp585.mat
salt_tops_ssp585=salt_si;

load salt_bsi_ssp585.mat
salt_bots_ssp585=salt_si;

salt_strat_ssp585=salt_bots_ssp585-salt_tops_ssp585;


load NC_coastline.txt
salt_diff=salt_strat_ssp585 - salt_strat_04d;
%salt_diff=salt_strat_04d;

%y1=34.5; y2=36.5; x1=-77; x2=-75.5;
%y1=35.3; y2=35.9; x1=-75.9; x2=-75.3;


hfig=figure;
set(hfig,'units','inches','position',[0 0 17*0.8 11*0.8])
set(hfig,'papersize',[8.9 12],'paperposition',[0 0 8.9 12])

set(gcf,'defaultaxeslinewidth',1)
set(gcf,'defaultaxesfontweight','bold')
set(gcf,'defaultaxesfontsize',14)
set(gcf,'defaulttextfontsize',14)

lmar=0.05;
xlen=0.41; ylen=0.6;

pos(1,:)=[lmar,0.3+0.04,0.3,ylen];
pos(2,:)=[lmar+0.3+0.03,0.3+0.04,0.6,ylen];
pos_cb=[lmar,0.94+0.046,0.94,0.02]


%pos(1,:)=[lmar,lmar+ylen+0.04,xlen,ylen];
%pos(2,:)=[lmar+xlen+0.05,lmar+ylen+0.04,xlen,ylen];
%pos(3,:)=[lmar,lmar,xlen,ylen];
%pos(4,:)=[lmar+xlen+0.05,lmar,xlen,ylen];
%seasons={'a) Winter','b) Spring','c) Summer','d) Fall'};



y1=34.7; y2=36.4; x1=-77; x2=-75.5
LL=pos2dist(y1,x1,y1,x2,2);
WW=pos2dist(y1,x1,y2,x1,2);

si=1;
axes('position',pos(si,:));
patch('Faces',nm,'Vertices',[lonm latm],...
'FaceVertexCData',mean(salt_diff,2),'FaceColor','interp','EdgeColor','none');
%colormap(jet)
%colorbar
hold on
plot(NC_coastline(:,1),NC_coastline(:,2),'color',[.5 .5 .5])
axis tight
axis([x1 x2 y1 y2])
pbaspect([LL/WW, 1,1])
%text(-77.2,35.15,seasons(si),'fontsize',14)
caxis([-0.4 0.4])
set(gca,'xtick',[x1:0.3:x2],'xticklabel',num2str(-[x1:0.3:x2]'));
set(gca,'ytick',[y1:0.3:y2],'yticklabel',num2str([y1:0.3:y2]'));
grid on
xlabel('Longitude (^oW)');
ylabel('Latitude (^oN)');


y1=34.9; y2=35.2; x1=-77.1; x2=-76.5;
LL=pos2dist(y1,x1,y1,x2,2);
WW=pos2dist(y1,x1,y2,x1,2);

si=2
axes('position',pos(si,:));
patch('Faces',nm,'Vertices',[lonm latm],...
'FaceVertexCData',mean(salt_diff,2),'FaceColor','interp','EdgeColor','none');
%colormap(jet)
%colorbar
hold on
plot(NC_coastline(:,1),NC_coastline(:,2),'color',[.5 .5 .5])
axis tight
axis([x1 x2 y1 y2])
pbaspect([LL/WW, 1,1])
%text(-77.2,35.15,seasons(si),'fontsize',14)
caxis([-0.4 0.4])
set(gca,'xtick',[x1:0.1:x2],'xticklabel',num2str(-[x1:0.1:x2]'));
set(gca,'ytick',[y1:0.1:y2],'yticklabel',num2str([y1:0.1:y2]'));
grid on
xlabel('Longitude (^oW)');
%ylabel('Latitude (^oN)');

hold on

% 0
plot(-77.1220, 35.21060,'o','markerfacecolor','k','markersize',5)
text(-77.1220, 35.21060+0.02,'0','fontsize',14,'color','k')
% 10
%plot(-77.09035, 35.17793,'o','markerfacecolor','r','markersize',8)
% 20
plot(-77.07648, 35.1533,'o','markerfacecolor','k','markersize',5)
text(-77.07648, 35.1533+0.02,'20','fontsize',14,'color','k')
% 30
plot(-77.03525, 35.11375,'o','markerfacecolor','k','markersize',5)
text(-77.03525, 35.11375+0.02,'30','fontsize',14,'color','k')

%40
%plot(-77.03174, 35.10972,'o','markerfacecolor','r','markersize',8)
% 50
plot(-77.0064, 35.07952,'or','markerfacecolor','k','markersize',5)
text(-77.0064, 35.07952+0.02,'50','fontsize',14,'color','k')

% 60
plot(-76.96925, 35.02465,'or','markerfacecolor','k','markersize',5)
text(-76.96925, 35.02465+0.02,'60','fontsize',14,'color','k')

% 70 
plot(-76.95943, 35.01472,'or','markerfacecolor','k','markersize',5)
text(-76.95943+0.02, 35.01472+0.02,'70','fontsize',14,'color','k')

% 100 
plot(-76.8755, 34.9766,'or','markerfacecolor','k','markersize',5)
text(-76.8755, 34.9766+0.02,'100','fontsize',14,'color','k')

% 120
plot(-76.81515, 34.94888,'or','markerfacecolor','k','markersize',5)
text(-76.81515, 34.94888+0.02,'120','fontsize',14,'color','k')

% 140
plot(-76.7374, 34.9661,'o','markerfacecolor','k','markersize',5)
text(-76.7374, 34.9661+0.02,'140','fontsize',14,'color','k')

% 160
plot(-76.66407, 35.0144,'or','markerfacecolor','k','markersize',5)
text(-76.66407, 35.0144+0.02,'160','fontsize',14,'color','k')

% 180
plot(-76.52602, 35.06413,'o','markerfacecolor','k','markersize',5)
text(-76.52602, 35.06413+0.02,'180','fontsize',14,'color','k')



h1=colorbar_hori_rb(pos_cb,-0.4,0.4,0.02,'Salinity (PSU)',5);
exportgraphics(gcf,'Salinity_stratification_ssp585-R2009.png','resolution',300)



