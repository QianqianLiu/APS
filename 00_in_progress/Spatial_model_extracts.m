clear
clc

%%%%%%% Extract salinity data and compile to .mat file for spatial comparison %%%%%%%%%%%%%

% Example file schout_70.nc 
% NC file format:
%%%%% Time dimension --> 120 for 5 days - each file is 5 days 

%Seasonal Values:

% Winter --> 1:19
% Spring --> 20:36
% Summer --> 37:55
% Fall --> 56:73

	% • Spring - April 1 - July 1
	% • Summer: July 1 - October 1
	% • Fall: October 1 - January 1
	% • Winter: January 1 - April 1


% winter: 
%4 season: winter, spring, summer, fall
seas=datenum(2019,[1,4,7,10],1)-datenum(2019,1,0);
seae=datenum(2019,[3,6,9,12],31)-datenum(2019,1,0);

salt=[];
for fi=1:73;
    filen=['schout_',num2str(fi),'.nc'];
    sali=squeeze(ncread(filen,'salt',[21,1,1],[1,inf,inf]));
    salt=cat(2,salt,sali); % second dimension: 120*fi
end

% salt: dimension is noden*hours

for si=1:4
    hrs=(seas(si)-1)*24+1;
    hre=seae(si)*24;

    salt_si(:,si)=mean(salt(:,hrs:hre));
end







ncf = ['/Users/kboothomefolder/git_liu/APS/00_in_progress/schout_70.nc'];

ncdisp(ncf);

time=ncread(ncf,'time'); % 120 x 1
salt=ncread(ncf,'salt'); % 21 (vertical layers) x 119604 (nodes) x 120 (time)
temp=ncread(ncf,'temp'); 
depth=ncread(ncf,'depth');
elev=ncread(ncf,'elev');% 119604 (nodes) x 120(time)
hvel=ncread(ncf,'hvel'); % 4d --> [time,u-component,v-component, # components(2)]

%%%%%%%%%% Loop for .nc variable extraction & cat %%%%%%%%%%%%%%%%%%%%%%%%%

salt_ann=[];
temp_ann=[];
elev_ann=[];
hvel_ann=[];
time_ann=[];


file_range=[70]; % 1:73 set range of files here, includes first and last

first = num2str(file_range(1));
last = num2str(file_range(end));

for i=1:length(file_range); 
    filenum = file_range(i);
    oy=num2str(filenum);

    % Update file path - expanse and computer path
    %ncf = ['/expanse/lustre/scratch/kboot/temp_project/RUN2002a/outputs/schout_',oy,'.nc'];
    ncf = ['/Users/kboothomefolder/git_liu/APS/00_in_progress/schout_70.nc'];
    ncf %test file name by printing

    % read salinity and temp variables and cat by the 3rd (time) dimension

    salt=ncread(ncf,'salt'); 
    salt_ann=cat(3,salt_ann,salt);

    temp=ncread(ncf,'temp'); 
    temp_ann=cat(3,temp_ann,temp);

    elev=ncread(ncf,'elev'); 
    elev_ann=cat(2,elev_ann,elev);

    hvel=ncread(ncf,'hvel'); 
    hvel_ann=cat(4,hvel_ann,hvel);

    %salt_ann=cat(# of dimensions, salt_ann, salt data)

end


%% Test spatial comparison for figure

% Plot each note datapoint for surface (1) vertical layer, mean for
% timesteps/4

% X and Y coords for node points, same in every file, UTM (meters)

x = ncread(ncf,'SCHISM_hgrid_node_x'); % in meters
y = ncread(ncf,'SCHISM_hgrid_node_y');
%[X,Y]=meshgrid(x,y);

x=x';
%y=y';

% Start with salinity mean - each file/30

surf_salt = salt_ann(1,:,:);
SS_winter = mean(surf_salt(1,:,1:30),3,'omitnan');

    
%%
%%%%%% 4. Map of one-day precip example: 
imagescn(x,y,SS_winter(:)); 
cb = colorbar; 
ylabel(cb,'Mean precipitation (m)');
ylabel('Y (m)');
xlabel('X (m)');
cmocean thermal % sets the colormap
hold off



%% Actual loop

% find mean of salinity values along the third dimension of
    % salt_ann (time) for specific dates

for t=1:size(salt_ann,3) % time dimension
    
    SS_seasonal=mean(salt_ann(:,:,t-13:t),3);

end

file_path = sprintf('./SS_seasonal_%s_%s.mat', first, last);
save(file_path, 'SS_seasonal');
