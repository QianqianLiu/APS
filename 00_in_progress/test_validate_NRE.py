#!/usr/bin/env python3
from pylib import *
#from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

# Import stations and extract points from model outputs
bpfile = 'station_nre.bp'
bp = read_schism_bpfile(bpfile)
stations = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180]

S = loadz('/home/liuquncw/APS/Obs/ModMon/NRE_WQ_2019.npz')
#mod = loadz('./mod_at_nre_stations.npz')
mod = loadz('/expanse/lustre/projects/unc107/kboot/ModelResults/RUN04d/mod_at_nre_stations.npz')
model_run_name = 'RUN04d'
model_run_descrip = '2019 Hindcast Simulation'

# Convert timesteps to datestr
mond = [datenum(2019, i + 1, 1) for i in range(23)]
Mond = np.array(mond)
mons = Mond * 24 * 3600
datetime = num2date(Mond)
Datestr = [datetime[i].strftime('%m') for i in range(23)]

# Initialize r-squared array for all stations
r_df = np.full(len(stations), np.nan)
#r_sq_df = np.full(len(stations), np.nan)

def calculate_r_value(observed, modeled):
    # Calculate the correlation matrix
    corr_matrix = np.corrcoef(observed, modeled)
    # Extract the correlation coefficient
    return corr_matrix[0, 1]

for i, sta in enumerate([20, 30, 50, 70, 100, 160]):
    print(i)

    pd = (S.station == sta) & (S.depthcat == "S") & (S.time >= datenum(2019,1,1)) & (S.time < datenum(2020,1,1))
    #pd = (S.station == 20) & (S.depthcat == "S") & (S.time >= datenum(2019,1,1)) & (S.time < datenum(2020,1,1))
    pdm = stations.index(sta)
    #pdm = stations.index(20)

    # Extract model points at same timesteps as observed
    # take observation time and limit to only 2019
    obs_times = S.time[pd] # this is a datenum
    mod_times = mod.time + datenum(2019, 1, 1)
    model_temps_at_observed_times = np.interp(obs_times, mod_times, mod.temp[pdm, :])
    
    # Make a quick plot before R-squared calculation
    figure(figsize=[8,4])
    plot(obs_times, model_temps_at_observed_times,'-*b')
    #plot(obs_times, S.temp[pd], "-*r")
    plot(obs_times, S.temp[20], "-*r")
    savefig('figures_validate/sta_{}.png'.format(sta))


    # Calculate R-squared
    #r_sq = r2_score(S.temp[pd], model_temps_at_observed_times)
    #r_sq_df[pdm] = r_sq  # index into r_sq_df
    #print(f"station {sta}, Temp R-Squared: {r_sq}")

    # calculate R-values
    r_val = calculate_r_value(S.temp[pd], model_temps_at_observed_times)
    r_df[pdm] = r_val 
    #print(f"station {sta}, Temp R-Squared: {r_sq}")
    print(f"station {sta}, Temp R-value: {r_val}")

#scp -r kboot@login.expanse.sdsc.edu:/expanse/lustre/projects/unc107/kboot/ModelResults/RUN04d/figures_validate/*.png .
# Print r-squared values for all stations
print("Final R-Squared values for all stations:")
print(r_sq_df)
print("Final R-values for all stations:")
print(r_df)

# note nan values are stations not selected in enumerate

    