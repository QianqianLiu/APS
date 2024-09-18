clear
clc

modelname = 'RUN04d';
%%%%%%% Extract salinity data and compile to .mat file for spatial comparison %%%%%%%%%%%%%

% Example file schout_70.nc 
% NC file format:
%%%%% Time dimension --> 120 for 5 days - each file is 5 days 

%Seasonal Values:

% Winter --> 1:19
% Spring --> 20:36
% Summer --> 37:55
% Fall --> 56:73

	% • Spring - April 1 - July 1; Use May 
	% • Summer: July 1 - October 1; Use August
	% • Fall: October 1 - January 1; Use November
	% • Winter: January 1 - April 1; Use February


% winter: 
%4 season: winter, spring, summer, fall

%seas=datenum(2019,[1,4,7,10],1)-datenum(2019,1,0);
%seae=datenum(2019,[3,6,9,12],31)-datenum(2019,1,0);

seas=datenum(2019,[2,5,8,11],1)-datenum(2019,1,0);
seae=datenum(2019,[2,5,8,11],31)-datenum(2019,1,0);

salt=[];

for si=1:4
    si
    days=seas(si);
    daye=seae(si);

    files=ceil(days/5);
    filee=ceil(daye/5);

    salt=[];
for fi=files:filee;
    fi
    filen=['schout_',num2str(fi),'.nc'];
    sali=squeeze(ncread(filen,'salt',[21,1,1],[1,inf,inf]));
    for day=1:5;
    sald(:,day)=squeeze(mean(sali(:,(day-1)*24+1:day*24),2));
    end
    salt=cat(2,salt,sald); % daily averaged salinity
end
totdays=[(files-1)*5+1:1:filee*5]; %for the beginning file    
ind=find(totdays>=days & totdays<=daye);

salt_si(:,si)=mean(salt(:,ind),2);
end

save salt_si.mat salt_si


% salt: dimension is noden*hours
% % 
% % for si=1:4
% %     hrs=(seas(si)-1)*24+1;
% %     hre=seae(si)*24;
% % 
% %     floor(seas(si)/5)
% %     ceil(seae(si)/5)
% % 
% %     salt_si(:,si)=mean(salt(:,hrs:hre));
% % end

