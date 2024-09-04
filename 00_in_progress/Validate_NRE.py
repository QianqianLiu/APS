#!/usr/bin/env python3
from pylib import *
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

# import stations and extract points from model outputs

bpfile='station_nre.bp'
bp = read_schism_bpfile(bpfile)
stations=[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180]

S=loadz('/home/liuquncw/APS/Obs/ModMon/NRE_WQ_2019.npz')
#mod=loadz('./mod_at_nre_stations.npz')
mod = loadz('/expanse/lustre/projects/unc107/kboot/ModelResults/RUN04d/mod_at_nre_stations.npz')
model_run_name = 'RUN04d'
model_run_descrip='2019 Hindcast Simulation'

# Convert timesteps to datestr
mond = [datenum(2019, i + 1, 1) for i in range(23)]
Mond = np.array(mond); mons = Mond * 24 * 3600
datetime = num2date(Mond)
Datestr = [datetime[i].strftime('%m') for i in range(23)]

# Functions for R-value and RMSE
# Initialize value arrays for all stations
r_df = np.full(len(stations), np.nan)
rmse_df = np.full(len(stations), np.nan)
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

# Select and plot NRE stations with R and RMSE values in each subplot
for i,sta in enumerate([20, 30, 50, 70,100,160]):
    print(i)
    pd = (S.station == sta) & (S.depthcat == "S") & (S.time >= datenum(2019,1,1)) & (S.time < datenum(2020,1,1))
    pdm = stations.index(sta)

    # make subplots
    subplot(3,2,i+1)
    plot(S.time[pd],S.temp[pd],'r*', label='Observed')
    plot(mod.time+datenum(2019,1,1),mod.temp[pdm,:],'b', label='Model')
    
    # Extract model points at same timesteps as observed
    # take observation time and limit to only 2019
    obs_times = S.time[pd] # this is a datenum
    mod_times = mod.time + datenum(2019, 1, 1)
    mod_temps_at_obs_times = np.interp(obs_times, mod_times, mod.temp[pdm, :])
    
    # calculate R-values and RMSE
    r_val = calc_r_value(S.temp[pd], mod_temps_at_obs_times).round(3)
    rmse_val = calc_rmse_value(S.temp[pd], mod_temps_at_obs_times).round(2)
    r_df[pdm] = r_val
    rmse_df[pdm] = rmse_val

    #print(f"station {sta}, Temp R-Squared: {r_sq}")
    print(f"station {sta}, Temp R-value: {r_val}, Temp RMSE: {rmse_val}")

    text(datenum(2019, 7, 15), 10, f'R = {r_val:.2f}\nRMSE = {rmse_val:.2f}', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
    
    setp(gca(),xticks=Mond,xticklabels=[],xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    if i>3: setp(gca(),xticks=Mond,xticklabels=Datestr,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    if i>3:
        plt.xlabel('Month')
    if i ==2:
        plt.ylabel('Temperature (\u00b0C)')
    xticks(rotation=70)
    title('Station {}'.format(sta))
    grid(linestyle = '--', linewidth = 0.5)
    if i==1:
        plt.legend()
    else:
        continue
plt.suptitle('Temperature Comparison at NRE Stations - {}'.format(model_run_descrip))
show(block=False)
savefig('figures_validate/Compare_Temp_NRE_{}.png'.format(model_run_name))

#scp -r kboot@login.expanse.sdsc.edu:/expanse/lustre/projects/unc107/kboot/ModelResults/RUN04d/figures_validate/*.png .
# Print r-squared values for all stations
print("Final RMSE values for all stations:")
print(r_df)
print("Final R-values for all stations:")
print(rmse_df)

# Next figure for Salinity
figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,30)],str='%d/%b')
xts,xls=xts[::60],xls[::60]; xls[0]=xls[0]+', 2018'


for i,sta in enumerate([20, 30, 50,70,100,160]):
    print(i)
    subplot(3,2,i+1)
    pd = (S.station == sta) & (S.depthcat == "S") & (S.time >= datenum(2019,1,1)) & (S.time < datenum(2020,1,1))
    pd2 = (S.station == sta) & (S.depthcat == "B") & (S.time >= datenum(2019,1,1)) & (S.time < datenum(2020,1,1))
    pdm=stations.index(sta)
    
    plot(S.time[pd],S.salt[pd],'r*', label='Observed Surface')
    plot(S.time[pd2],S.salt[pd2],'m*', label='Observed Bottom')
    plot(mod.time+datenum(2019,1,1),mod.salt[pdm,:],'b', label='Model Surface?')

    obs_times = S.time[pd] # this is a datenum
    mod_times = mod.time + datenum(2019, 1, 1)
    mod_salt_at_obs_times = np.interp(obs_times, mod_times, mod.salt[pdm, :])
    
    # calculate R-values and RMSE
    r_val = calc_r_value(S.salt[pd], mod_salt_at_obs_times).round(3)
    rmse_val = calc_rmse_value(S.salt[pd], mod_salt_at_obs_times).round(2)
    r_df[pdm] = r_val
    rmse_df[pdm] = rmse_val
    print(f"station {sta}, Temp R-value: {r_val}, Temp RMSE: {rmse_val}")
    text(datenum(2019, 2, 1), 20, f'R = {r_val:.2f}\nRMSE = {rmse_val:.2f}', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

    setp(gca(),xticks=Mond,xticklabels=[],xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    if i>3: setp(gca(),xticks=Mond,xticklabels=Datestr,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    if i>3:
        plt.xlabel('Month')
    if i ==2:
        plt.ylabel('Salinity (PSU)')
    xticks(rotation=70)
    title('Station {}'.format(sta))
    grid(linestyle = '--', linewidth = 0.5)
    if i==1:
        plt.legend()
    else:
        continue
plt.suptitle('Salinity Comparison at NRE Stations - {}'.format(model_run_descrip))
show(block=False)
savefig('figures_validate/Compare_Salt_NRE_{}.png'.format(model_run_name))


