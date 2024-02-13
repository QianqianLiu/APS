%%% I realized elements in *.2dm is not right. should be E3T instead of E6T

Elements=load('Elements.txt');
Nodes=load('Nodes.txt');

%dep=load('dep.txt');


dep=load('VIMS_depth.txt');

long=Nodes(:,2); lati=Nodes(:,3); nv=Elements(:,2:4);
h=griddata(dep(:,2),dep(:,3),dep(:,4),long,lati,'natural');
ind=find(isnan(h));
h(ind)=0;

%[lonm,latm]=my_project_Champlain(x,y,'reverse');
[x,y]=my_project_NC(long,lati,'forward');

fileID=fopen('hgrid.gr3','w');
fprintf(fileID,'%s\n','hgrid.gr3');
fprintf(fileID,'%d %d \n',size(nv,1),length(x))

for NN=1:length(x);
    fprintf(fileID,'%d %14.6f %14.6f %6.2f \n',NN,x(NN), y(NN), h(NN));
end

for EE=1:size(nv,1);
    fprintf(fileID,'%d %d %d %d %d \n',EE,3, nv(EE,1), nv(EE,2), nv(EE,3));
end
fclose(fileID);

fileID=fopen('hgrid.ll','w');
fprintf(fileID,'%s\n','hgrid.ll');
fprintf(fileID,'%d %d \n',size(nv,1),length(x))

for NN=1:length(x);
    fprintf(fileID,'%d %14.6f %14.6f %6.2f \n',NN,long(NN), lati(NN), h(NN));
end
for EE=1:size(nv,1);
    fprintf(fileID,'%d %d %d %d %d \n',EE,3, nv(EE,1), nv(EE,2), nv(EE,3));
end

fclose(fileID);



fileID=fopen('tvd.prop','w');
for EE=1:size(nv,1);
    fprintf(fileID,'%d %d\n',EE,1);
end
fclose(fileID);



fileID=fopen('albedo.gr3','w');
fprintf(fileID,'%s\n','albedo.gr3');
fprintf(fileID,'%d %d \n',size(nv,1),length(x))
albedov=0.01;

for NN=1:length(x);
    fprintf(fileID,'%d %14.6f %14.6f %14.7f \n',NN,x(NN), y(NN), albedov);
end

for EE=1:size(nv,1);
    fprintf(fileID,'%d %d %d %d %d \n',EE,3, nv(EE,1), nv(EE,2), nv(EE,3));
end
fclose(fileID);
