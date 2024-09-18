#!/usr/bin/env python3
from pylib import *
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

# coordinates of PS stations (ps1 to ps9)
lon_ps=c_[-76.47653, -76.42758,-76.34330,-76.26680,-76.20060,-76.24867,-76.22947,-76.30570,-76.37275]
lat_ps=c_[35.1201,35.15056667,35.13125,35.11841667,35.1225,35.08255,35.03205,35.02616667,35.09986667]


S=loadz('/home/liuquncw/APS/Obs/ModMon/PS_WQ_2021.npz') 
# This a snapshot at time of collection --> one salinity measurement per month
# NOAA NDBC station salinity --> possibly more accurate comparison, more timeseries with accurate times 
#mod=loadz('./mod_at_ps_wq_stations.npz')
mod = loadz('/expanse/lustre/projects/unc107/kboot/ModelResults/RUN04d/mod_at_ps_wq_stations.npz')
model_run_name = 'RUN04d'
model_run_descrip='2019 Hindcast Simulation'

# Convert timesteps to datestr
mond = [datenum(2019, i + 1, 1) for i in range(23)]
Mond = np.array(mond); mons = Mond * 24 * 3600
datetime = num2date(Mond)
Datestr = [datetime[i].strftime('%m') for i in range(23)]

# Functions for R-value and RMSE
# Initialize value arrays for all stations
length = arange(9)
r_df = np.full(len(length), np.nan)
rmse_df = np.full(len(length), np.nan)
#r_sq_df = np.full(len(stations), np.nan)

def calc_r_value(observed, modeled):
    # Calculate the correlation matrix
    corr_matrix = np.corrcoef(observed, modeled)
    # Extract the correlation coefficient
    return corr_matrix[0, 1]

def calc_rmse_value(observed, modeled):
    mse = mean_squared_error(observed, modeled)
    rmse = np.sqrt(mse) # root of mse
    return rmse

# make a sample plot
figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,30)],str='%d/%b')
xts,xls=xts[::60],xls[::60]; xls[0]=xls[0]+', 2018'

# Select and plot PS stations with R and RMSE values in each subplot
for i in arange(9):
    print(i)
    subplot(3,3,i+1)

    #pd=(S.station==i+1)*(S.depthcat==1)
    #pd = (S.station == sta) & (S.depthcat == "S") & (S.time >= datenum(2019,1,1)) & (S.time < datenum(2020,1,1))
    pd=(S.station==i+1) & (S.depthcat==1) & (S.time >= datenum(2019,1,1)) & (S.time < datenum(2020,1,1))

    # No low pass or smoothing filter used here
    plot(S.time[pd],S.temp[pd],'r*', label='Observed')
    plot(mod.time+datenum(2019,1,1),mod.temp[i,:],'b', label='Model')
    setp(gca(),xticks=Mond, xticklabels=[], xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    
    # Calc R and RMSE
    obs_times = S.time[pd] # this is a datenum
    mod_times = mod.time + datenum(2019, 1, 1)
    #mod_temp_at_obs_times = np.interp(obs_times, mod_times, mod.salt[pdm, :])
    mod_temp_at_obs_times = np.interp(obs_times, mod_times, mod.temp[i, :])

    # calculate R-values and RMSE
    r_val = calc_r_value(S.temp[pd], mod_temp_at_obs_times).round(4)
    rmse_val = calc_rmse_value(S.temp[pd], mod_temp_at_obs_times).round(2)
    r_df[i] = r_val
    rmse_df[i] = rmse_val
    print(f"station {i}, Temp R-value: {r_val}, Temp RMSE: {rmse_val}")
    text(datenum(2019, 1, 10), 22, f'R = {r_val:.3f}\nRMSE = {rmse_val:.3f}', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

    if i>=6: setp(gca(),xticks=Mond,xticklabels=Datestr,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    if i ==7:
        plt.xlabel('Month')
    if i ==3:
        plt.ylabel('Temperature (\u00b0C)')
    xticks(rotation=70)
    grid(linestyle = '--', linewidth = 0.5)
    title('Station {}'.format(i+1))
    if i==1:
        plt.legend()
    else:
        continue

plt.suptitle('Temperature at Pamlico Sound Stations - {}'.format(model_run_name))
savefig('figures_validate/Compare_Temp_PS_WQ_{}.png'.format(model_run_name))

clf()
figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,30)],str='%d/%b')
xts,xls=xts[::60],xls[::60]; xls[0]=xls[0]+', 2018'
for i in arange(9):
    print(i)
    subplot(3,3,i+1)
    #pd=(S.station==i+1)*(S.depthcat==1)
    pd=(S.station==i+1) & (S.depthcat==1) & (S.time >= datenum(2019,1,1)) & (S.time < datenum(2020,1,1))
    plot(S.time[pd],S.salt[pd],'r*', label='Observed')
    plot(mod.time+datenum(2019,1,1),mod.salt[i,:],'b', label='Model')
    setp(gca(),xticks=Mond, xticklabels=[], xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    
    # Calc R and RMSE
    obs_times = S.time[pd] # this is a datenum
    mod_times = mod.time + datenum(2019, 1, 1)
    mod_salt_at_obs_times = np.interp(obs_times, mod_times, mod.temp[i, :])

    # calculate R-values and RMSE
    r_val = calc_r_value(S.salt[pd], mod_salt_at_obs_times).round(3)
    rmse_val = calc_rmse_value(S.salt[pd], mod_salt_at_obs_times).round(2)
    r_df[i] = r_val
    rmse_df[i] = rmse_val
    print(f"station {i}, Salinity R-value: {r_val}, Salinity RMSE: {rmse_val}")
    text(datenum(2019, 9, 1), 5, f'R = {r_val:.2f}\nRMSE = {rmse_val:.2f}', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

    if i>=6: setp(gca(),xticks=Mond,xticklabels=Datestr,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    xticks(rotation=70)
    if i==7:
        plt.xlabel('Month')
    if i==3:
        plt.ylabel('Salinity (PSU)')
    grid(linestyle = '--', linewidth = 0.5)
    title('Station {}'.format(i+1))
    if i==1:
        plt.legend()
    else:
        continue
plt.suptitle('Surface Salinity at Pamlico Sound Stations - {}'.format(model_run_name))
plt.axis('on')
savefig('figures_validate/Compare_Salt_PS_WQ_{}.png'.format(model_run_name))

