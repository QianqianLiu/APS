clear;clc;close all

modelname = 'RUN04d';
APS_mesh

x1=-78; x2=-75; y1=34.5; y2=36.5;
LL=pos2dist(y1,x1,y1,x2,2);
MM=pos2dist(y1,x1,y2,x1,2);


load NC_coastline.txt
load salt_si.mat

seasons={'Winter','Spring','Summer','Fall'};

figure;

for i=1:4
    if i==1;
        t=tiledlayout(2,2);
        t.TileSpacing = 'compact'
        nexttile
    end 
    
    patch('Faces',nm(:,1:4),'Vertices',[lonm latm],'FaceVertexCData',squeeze(salt_si(:,i)),'FaceColor','interp','EdgeColor','None');
    hold on
    plot(NC_coastline(:,1),NC_coastline(:,2),'-k','linewidth',1,'color',[.5 .5 .5])
    axis([x1 x2 y1 y2])
    pbaspect([LL/MM,1,1])
    caxis([5 37])
    %text(-77.5,36,seasons(i),'fontsize',14)
    title(seasons(i))
    hold off
    if i<4; nexttile; end
end

saveas(gcf, 'SSal_Spatial_.png');
