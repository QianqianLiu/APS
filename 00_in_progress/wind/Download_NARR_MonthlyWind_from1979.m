
% Load u-wind and v-wind components from NARR 
% Time is January 1979 through June 2024

clear;clc;close all
url_u='http://psl.noaa.gov/thredds/dodsC/Datasets/NARR/Monthlies/monolevel/uwnd.10m.mon.mean.nc?time[0:1:537],lat[109:1:109][262:1:262],lon[109:1:109][262:1:262],uwnd[0:1:200][109:1:109][262:1:262]';
uwnd1=ncread(url_u,'uwnd');
url_u='http://psl.noaa.gov/thredds/dodsC/Datasets/NARR/Monthlies/monolevel/uwnd.10m.mon.mean.nc?time[0:1:537],lat[109:1:109][262:1:262],lon[109:1:109][262:1:262],uwnd[201:1:537][109:1:109][262:1:262]';
uwnd2=ncread(url_u,'uwnd');
uwnd1=squeeze(uwnd1); uwnd2=squeeze(uwnd2);
uwnd=cat(1, uwnd1,uwnd2);

lon_u=ncread(url_u,'lon');
lat_u=ncread(url_u,'lat');
time_u=ncread(url_u,'time');

%https://psl.noaa.gov/thredds/dodsC/Datasets/NARR/Monthlies/monolevel/vwnd.10m.mon.mean.nc.html
%level: 10m; northward_wind, v-wind; m/s

url_v='http://psl.noaa.gov/thredds/dodsC/Datasets/NARR/Monthlies/monolevel/vwnd.10m.mon.mean.nc?time[0:1:537],lat[109:1:109][262:1:262],lon[109:1:109][262:1:262],vwnd[0:1:200][109:1:109][262:1:262]';
vwnd1=ncread(url_v,'vwnd');
url_v='http://psl.noaa.gov/thredds/dodsC/Datasets/NARR/Monthlies/monolevel/vwnd.10m.mon.mean.nc?time[0:1:537],lat[109:1:109][262:1:262],lon[109:1:109][262:1:262],vwnd[201:1:537][109:1:109][262:1:262]';
vwnd2=ncread(url_v,'vwnd');
vwnd1=squeeze(vwnd1); vwnd2=squeeze(vwnd2);
vwnd=cat(1, vwnd1,vwnd2);
lon_v=ncread(url_v,'lon');
lat_v=ncread(url_v,'lat');
time_v=ncread(url_v,'time');

wind(:,1)=time_u; 
wind(:,2)=uwnd;
wind(:,3)=vwnd;
save('wind_monthly.txt','wind','-ascii')

%%%%%%%%%%% Make windrose diagrams %%%%%%%%%%%%%%%%%%%%%%%%%
mag = sqrt(uwnd.^2 + vwnd.^2);
dir = atan2d(vwnd, uwnd);  % atan2d returns the angle in degrees

% Windrose of all monthly data 1979 to 2023
figure;
WindRose(dir, mag);
filename = 'windrose_plot_1979to2023.png';
saveas(gcf, filename);

% mags and dirs for each month for rose plot
mo_length = floor(length(mag)/12);
mag_mo = nan(12, mo_length);
dir_mo = nan(12, mo_length);
limit = length(mag) - mod(length(mag), 12);

for i = 1:12
    disp(['Processing month ', num2str(i)]); 
    ind = i:12:limit;
    mag_vals = mag(ind);
    dir_vals = dir(ind);
    mag_mo(i, :) = mag_vals';
    dir_mo(i, :) = dir_vals';
end

mag_1 = mag_mo(1,:);
dir_1 = dir_mo(1,:);
figure;
WindRose(dir_1, mag_1);
title(['Month ', num2str(1)]);
filename = 'windrose_plot_1979to2023_jan.png';
saveas(gcf, filename);

% Plot with wind rose subplot for each month
for i = 1:12;
    dir_mo = dir(i,:);
    mag_mo = mag(i,:);
    figure;
    WindRose(dir_1, mag_1);
    tt = ['Month ', num2str(i)];
    thandle = title(tt);
    titlePosition = get(thandle, 'Position'); 
    titlePosition(2) = titlePosition(2) + 0.1; 
    set(thandle, 'Position', titlePosition); 
    filename = ['windrose_plot_1979to2023_', num2str(i), '.png'];
    saveas(gcf, filename);
end

% Average for each month
% for i = 1:12;
%     i
%     ind = i:12:length(mag); % Extract index for every 12th value 
%     mag_vales = mag(ind); % extract values
%     mo_avg = mean(mag_vales);
%     mag_av = [mag_av; mo_avg];
% end
