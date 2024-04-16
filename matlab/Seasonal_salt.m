clear;clc;close all
APS_mesh
load salt_si_ssp370.mat
salt_si_ssp370=salt_si;
load salt_si_ssp585.mat
salt_si_ssp585=salt_si;
load salt_si_run04d.mat
salt_si_04d=salt_si;

load NC_coastline.txt

salt_diff=salt_si_ssp585 - salt_si_04d;
%y1=34.5; y2=36.5; x1=-77; x2=-75.5;
%y1=35.3; y2=35.9; x1=-75.9; x2=-75.3;
y1=34.5; y2=36.5; x1=-77; x2=-75.3;
LL=pos2dist(y1,x1,y1,x2,2);
WW=pos2dist(y1,x1,y2,x1,2);

hfig=figure;
set(hfig,'units','inches','position',[0 0 8.9 12])
set(hfig,'papersize',[8.9 12],'paperposition',[0 0 8.9 12])

set(gcf,'defaultaxeslinewidth',1)
set(gcf,'defaultaxesfontweight','bold')
set(gcf,'defaultaxesfontsize',10)
set(gcf,'defaulttextfontsize',10)

lmar=0.05;
xlen=0.41; ylen=0.41;
pos(1,:)=[lmar,lmar+ylen+0.04,xlen,ylen];
pos(2,:)=[lmar+xlen+0.05,lmar+ylen+0.04,xlen,ylen];
pos(3,:)=[lmar,lmar,xlen,ylen];
pos(4,:)=[lmar+xlen+0.05,lmar,xlen,ylen];
pos_cb=[lmar,lmar+ylen*2+0.04+0.046,0.05+xlen*2,0.02]
seasons={'a) Winter','b) Spring','c) Summer','d) Fall'};
for si=1:4
%subplot(2,2,si)
axes('position',pos(si,:));
patch('Faces',nm,'Vertices',[lonm latm],...
'FaceVertexCData',salt_diff(:,si),'FaceColor','interp','EdgeColor','none');
%colormap(jet)
%colorbar
hold on
plot(NC_coastline(:,1),NC_coastline(:,2),'color',[.5 .5 .5])
axis tight
axis([x1 x2 y1 y2])
pbaspect([LL/WW, 1,1])
text(-76.8,36.4,seasons(si),'fontsize',14)
caxis([-3 3])
set(gca,'xtick',[x1:0.5:x2],'xticklabel',num2str(-[x1:0.5:x2]'));
set(gca,'ytick',[y1:0.5:y2],'yticklabel',num2str([y1:0.5:y2]'));
grid on
if si>2; xlabel('Longitude (^oW)');end
if si==1 | si==3; ylabel('Latitude (^oN)');end

end
h1=colorbar_hori_rb(pos_cb,-3,3,0.2,'Salinity (PSU)',5);

exportgraphics(gcf,'Salt_diff_SSP585-RUN04d.png','resolution',300)